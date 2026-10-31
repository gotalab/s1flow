"""`s1flow report` lists the candidates by the task's objectives and constraints; `s1flow adopt` writes the one a
person picks as the next policy. Nothing is called: the runs are already scored.

The list (select.rank) marks no pick: a free tier's rate limit, how long a model is served and whether its
version can be pinned count too, so a person or an agent picks, and the policy records who picked and why.

A policy names the version that answers. An alias model (s1flow.toml `versions`, with an `id` that is
none of theirs: `jev-latest`) runs and compares, but cannot be adopted: which version answered its runs
is not known from s1flow.toml, and the runs cannot say it either (the alias moves while they are made).
Its versions, run by name (`jev:1.14`), are candidates of their own.

Candidates are every model with runs on the task's question and on each of its variants (an
optimized question competes with the original). The policy's rule is the one the primary objective sets
(`Objective.sets`), as chosen on all the dev cases.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field

from pydantic import BaseModel

from ..client.models import ModelSpec
from ..client.identity import execution_digest, require_provider_revision
from ..core.errors import ConfigError, NotFound, S1flowError
from ..policies import DecisionPolicy
from ..policies.rule import DecisionRule
from ..policies.file import PolicySpec, asked as one_question
from ..policies.history import Switch
from .candidate import Candidate
from ..policies.state_shape import schema_of
from . import evalset, metrics, weights
from .evaluation import Calls, Evaluation, ObjectiveScore
from .policy import EvaluatedPolicy, Evidence, Pin, Selection, pin
from .run import Conditions, ask_again
from .select import Ranked, rank, unlike_among_tied
from .task import Task

Listed = tuple[str, str, str]  # (candidate name, model, variant)
def adoptable(spec: ModelSpec, model: str) -> None:
    """Refuse an alias model: a policy must name the version that answers, and s1flow.toml says it of no alias."""
    require_provider_revision(spec)
    if pin(spec, model) == "alias":
        versions = " or ".join(f"{model}:{v}" for v in spec.versions or {})
        raise S1flowError(f"{model} is an alias ({spec.id}): the version answering it can change, so a policy "
                         f"cannot name it; run a version instead (s1flow run <task> --models {versions}) and adopt that")


def validate_evidence(task: Task, policy: EvaluatedPolicy) -> None:
    """Only current model/input/data conditions can support adopting an evaluated policy."""
    runtime = DecisionPolicy(policy.spec, client=task.where.client())
    adoptable(runtime.model_spec, policy.spec.connection)
    if runtime.execution_digest != policy.evidence.execution_digest:
        raise ConfigError(f"{policy.spec.ref}: execution conditions changed; measure and adopt again")
    if policy.evidence.input_adapter_digest != task.input_adapter_digest:
        raise ConfigError(f"{policy.spec.ref}: input adapter changed; measure and adopt again")
    if policy.evidence.evaluation_contract_digest != task.evaluation_contract_digest:
        raise ConfigError(f"{policy.spec.ref}: evaluation contract changed or is unknown; rescore and adopt again")
    if task.data_digest != policy.evidence.data_sha256:
        raise ConfigError(f"{policy.spec.ref}: input data or labels changed; measure and adopt again")


def candidates(task: Task, only: list[str] | None = None, variants: list[str] | None = None) -> list[Listed]:
    """Every run on a question the task still has, by a model (or a version of one) still in the line-up."""
    known: set[str] = set(task.where.declared_connections().names(versions=True))
    out = []
    for variant in variants or ["base", *task.variants]:
        d = task.where.runs_dir / task.id / variant
        for path in sorted(d.glob("*.jsonl")) if d.exists() else []:
            model = path.stem
            if model not in known or (only and model not in only):
                continue
            out.append((Candidate(model=model, variant=variant).name, model, variant))
    return out


def missing(pr: metrics.Preds) -> str:
    """Why a candidate has no answer to some labelled cases: never asked, or every call failed (not a refusal)."""
    return " and ".join(x for x in (
        f"{len(pr.never_asked)} cases never asked" if pr.never_asked else "",
        f"{len(pr.failed_cases)} cases whose every call failed" if pr.failed_cases else "",
    ) if x)


def rule_for(task: Task, score: ObjectiveScore) -> DecisionRule:
    """The rule the primary objective sets (`objective.sets`), as chosen on all the dev cases."""
    o0 = task.primary
    if o0.sets is None:
        return DecisionRule()
    if score.rule is None:
        raise S1flowError(f"{o0.label}: no {o0.sets.replace('_', ' ')} keeps its constraint and the task's floors on the dev cases, so there is no rule to adopt yet")
    return score.rule


class Row(BaseModel):
    """One candidate as the list shows it: measured on train + val (the test share is not shown)."""

    candidate: str  # Candidate.name
    n: int  # labelled train + val cases it answered; refusals remain visible in their own count
    refused: int  # labelled cases it refused or does not support: the model's limit, left out of its denominator
    tied: bool  # the primary objective cannot tell it from the best on it
    excluded: list[str]  # constraints it breaks; it cannot be picked
    scores: list[ObjectiveScore]  # one per objective, the primary first: measured on the answers
    calls: Calls  # what its calls took: latency, API cost (0: free; None: not known) and where that cost came from
    pin: Pin  # whether a policy of it names the version that answers
    per_minute: int | None  # the model's rate limit, when s1flow.toml declares one (Capabilities.per_minute)


class Order(BaseModel):
    """What orders the candidates the primary objective cannot tell apart (`tied`): `by`, task.py's tiebreak as
    applied; none: they are listed by name, and their order says nothing."""

    by: list[str]  # objective keys, "latency", "cost", in the order applied
    skipped: list[str]  # named by the tiebreak but not applied ("latency": measured unalike)
    why: str | None = None  # why one was skipped, and how to measure again


@dataclass
class Shortlist:
    """Every candidate scored on train + val, best first. Building it writes nothing and shows no test result."""

    task: Task
    measured: Conditions  # every candidate listed, the ones left out for missing cases too
    ranked: list[Ranked]
    evaluations: dict[str, Evaluation]
    preds: dict[str, metrics.Preds]
    cands: list[Listed]
    reweighted: list[weights.Reweighted] = field(default_factory=list)  # the weights halved and doubled (ExpectedLoss, Loss)

    @property
    def fits(self) -> list[Ranked]:
        """The candidates that can be picked: within the constraints, with a value on the primary objective."""
        return [x for x in self.ranked if not x.excluded and x.scores[0].value is not None]

    @property
    def tied(self) -> list[str]:
        return [x.candidate for x in self.ranked if x.tied_with_best]

    def order(self) -> Order:
        ties = self.task.ties
        unlike = unlike_among_tied(self.ranked, list(self.evaluations.values())) if "latency" in ties else None
        keys = [t if isinstance(t, str) else t.key for t in ties]
        skipped = ["latency"] if unlike else []
        return Order(by=[k for k in keys if k not in skipped], skipped=skipped, why=unlike.en(self.task.id) if unlike else None)

    def pickable(self, pick: str) -> Ranked:
        """The candidate named `pick` (model[:version][/variant]), or an error listing the ones that can be picked."""
        Candidate.parse(pick)
        picked = next((x for x in self.fits if x.candidate == pick), None)
        if picked is None:
            why = next((f" ({', '.join(x.excluded)})" for x in self.ranked if x.candidate == pick and x.excluded), "")
            raise S1flowError(f"{pick!r} cannot be picked{why}; pick one of: {', '.join(x.candidate for x in self.fits) or 'none'}")
        return picked

    def rows(self) -> list[Row]:
        models = self.task.where.declared_connections()
        fits = {x.candidate for x in self.fits}
        out = []
        for x in self.ranked:
            e, model = self.evaluations[x.candidate], next(c[1] for c in self.cands if c[0] == x.candidate)
            spec = models.retrieve(model).spec
            out.append(Row(
                candidate=x.candidate, n=e.n, refused=e.failures.refused_cases or 0, tied=x.tied_with_best,
                excluded=x.excluded if x.excluded or x.candidate in fits else ["no value on the primary objective"],
                scores=x.scores, calls=e.calls,
                pin=pin(spec, model), per_minute=models.resolved(model).capabilities.per_minute,
            ))
        return out


def shortlist(task: Task, only: list[str] | None = None, variants: list[str] | None = None) -> Shortlist:
    if not task.kind.adoptable:
        raise S1flowError(f"a policy ships boolean and choice questions; {task.id} asks a {task.kind.type}")
    cands = candidates(task, only, variants)
    if not cands:
        raise NotFound(f"no runs for {task.id}; s1flow run {task.id} first")
    measured = Conditions.now(task, [Candidate(model=m, variant=v) for _, m, v in cands], task.where.declared_connections().resolved)
    preds = {name: metrics.load(task, variant, model) for name, model, variant in cands}
    gaps = {c: missing(preds[c[0]]) for c in cands if preds[c[0]].never_asked or preds[c[0]].failed_cases}
    if gaps:
        # candidates compared on different cases are not compared: a model that skipped the new cases, or whose calls
        # failed on some, is scored on the rest only and can look better than one that answered them all
        why = ", ".join(f"{c[0]} ({gap})" for c, gap in gaps.items())
        again = ask_again(task, [(c[1], c[2]) for c in gaps])
        cands = [c for c in cands if c not in gaps]
        if not cands:
            raise S1flowError(f"every candidate misses cases: {why}; ask them again: {again}")
        warnings.warn(f"left out until it has an answer to every case: {why}; ask them again: {again}", stacklevel=2)
        preds = {c[0]: preds[c[0]] for c in cands}
    evaluations = {name: metrics.evaluate(task, preds[name], variant=variant) for name, model, variant in cands}
    ranked = rank(task.primary, task.ties, task.constraints, list(evaluations.values()))
    moved = weights.sensitivity(task, preds, {c[0]: c[2] for c in cands})
    if "latency" in task.ties and (unlike := unlike_among_tied(ranked, list(evaluations.values()))):
        warnings.warn(unlike.en(task.id), stacklevel=2)
    if changed := measured.changed(task, task.where.declared_connections().resolved):
        raise ConfigError(f"{task.id}: {changed} changed during ranking; rank again")
    return Shortlist(task=task, measured=measured, ranked=ranked, evaluations=evaluations, preds=preds, cands=cands, reweighted=moved)


def adopt(
    task: Task, pick: str, by: str, reason: str, *, only: list[str] | None = None, force: bool = False,
    variants: list[str] | None = None, listed: Shortlist | None = None, git_sha: str | None = None,
) -> EvaluatedPolicy:
    """The policy of the picked candidate (a name from the shortlist), stored as the task's current version: the
    pull request that carries it ships it when it merges. One below on the held-out test is not stored unless
    `force`; history.jsonl records it either way (policies/history.py). `git_sha`: the commit it was made at (the
    CLI asks git, integrations/git.py)."""
    s = listed or shortlist(task, only, variants)
    current = task.where.client().connections.resolved
    if changed := s.measured.changed(task, current):
        raise ConfigError(f"{task.id}: {changed} changed since ranking; rank again before adopting")
    if not by.strip() or not reason.strip():
        raise S1flowError("a policy records who adopted it and why: give both by and reason")
    picked = s.pickable(pick)
    name, model, variant = next(c for c in s.cands if c[0] == pick)
    pr = s.preds[name]
    models = task.where.client().connections
    adoptable(models.retrieve(model).spec, model)
    spec = models.resolved(model)  # the model at the version picked: its id, its own capabilities
    answered_by = pr.version or spec.id
    policies = task.policies
    version = policies.next_version(task.id)
    evalset.fixed(task)  # the test share it is confirmed on: the one the first run fixed
    # Ordinary ranking never reads test. Adoption explicitly confirms this selected candidate.
    pr = metrics.load(task, variant, model, include_test=True)
    if pr.never_asked or pr.failed_cases:
        raise S1flowError(f"{name}: selected candidate needs current answers on every case before adoption")
    e = metrics.evaluate(task, pr, variant=variant, include_test=True)
    runtime = PolicySpec(
        task=task.id, version=version, connection=model, model_id=spec.id,
        questions={task.question_id: one_question(task.questions(variant)[task.question_id], rule_for(task, picked.scores[0]), task.kind_params)},
        state_schema=schema_of([task.model_state(c) for c in task.load_cases().all()]),
    )
    if changed := s.measured.changed(task, current):  # after the reads above: the test cases and the picked run
        raise ConfigError(f"{task.id}: {changed} changed during adoption; rank again before adopting")
    test = metrics.test_verdict(task, e)
    r = EvaluatedPolicy(
        spec=runtime, candidate=e.candidate, answered_by=answered_by,
        selection=Selection(by=by.strip(), reason=reason.strip(), tied=s.tied, forced=test == "below" and force),
        evidence=Evidence(
            data_sha256=s.measured.data,
            execution_digest=execution_digest(spec, runtime.digest),
            input_adapter_digest=s.measured.input_adapter,
            evaluation_contract_digest=s.measured.evaluation_contract,
            evaluation=e, test=test,
            compared=[c[0] for c in s.cands], git_sha=git_sha,
        ),
    )
    validate_evidence(task, r)
    entry = Switch(action="adopt", version=version, previous=policies.current(task.id), by=r.selection.by, reason=r.selection.reason,
                   candidate=name, test=r.evidence.test, forced=r.selection.forced)
    if r.evidence.test != "below" or force:
        policies.write_evaluated(r, adopted=entry)
    else:
        policies.log(task.id, entry.model_copy(update={"action": "refused"}))
    return r
