"""`s1flow check`: before a change ships, ask both versions about the same test cases of today's data
and compare them case by case.

    candidate   `current`, a version, or `draft` (current's model and rule with the task's current
                question, for a PR that edits the question before adopting it)
    against     the version to compare with: on a pull request, the one current names on its base branch
                (the Action reads it there and passes `--against vN`); `current` by default

The two are not compared through the numbers stored in their evidence: the data grows, and the
stored numbers were measured on other cases. Each is asked again (cached answers cost nothing,
so an unchanged version is free) and the answers are read exactly as the SDK reads them
(policies/kinds.py): each label with the policy's reading makes the pairs the task's objectives are
measured on (objectives/measure.py), as metrics measures them. The verdict rests on paired bootstrap
intervals of the difference on the task's primary objective:

    fail (exit 1)  the candidate is worse beyond the interval; or the primary's constraint (Coverage: the
                   accuracy of the sure answers; Recall: the false alarms) is shown broken (one-sided 95%
                   Clopper-Pearson) or got worse beyond its interval; or a floor of the task's constraints
                   (min_precision, min_recall) is shown broken the same way; or it breaks a cost constraint
    pass (exit 0)  otherwise; "better" when the interval is above 0, or when only the candidate keeps the
                   constraint; "no difference shown" when it spans 0
    pending        no calls allowed and some answers are not cached (exit 2)

With only one version (no candidate), current alone is checked against the target.

Nothing stored passes a check: what a version's evidence says, the PR could have written. It is asked again, so
`adopt --force` (selection.forced) fails as any version below does; the comment shows that it was forced and why.
A version adopted without an evaluation (adopt --spec) is asked like any other.

Here the versions are chosen and the verdict given; calls.py asks them, paired.py measures them, comment.py
writes the PR comment. Nothing is written but the answer cache.
"""

from __future__ import annotations

import asyncio
import random
from typing import Literal

from pydantic import BaseModel

from ...client.questions import Question
from ...policies import DecisionPolicy
from ...core.errors import ConfigError, DataError, S1flowError
from ...policies.file import CURRENT, version_number
from .. import evalset
from ..objectives import measure
from ..objectives.measure import bound
from ..shown import usd
from ..task import Task
from .calls import Side, Version, ask, missing
from .paired import Diffs, SideSummary, keeps, paired, resamples, shown, summary


Verdict = Literal["fail", "better", "no_difference", "pass", "pending"]


class CheckResult(BaseModel):
    task: str
    n: int
    sample: int | None
    verdict: Verdict
    primary_label: str = ""
    target_accuracy: float = 0.95
    data_sha256: str | None = None
    sides: list[SideSummary] = []
    diff: Diffs | None = None
    reasons: list[str] = []
    notes: list[str] = []
    need_calls: dict[str, int] = {}  # pending: calls each version would make

    @property
    def exit(self) -> int:
        return {"fail": 1, "pending": 2}.get(self.verdict, 0)


def _current(task: Task, r: Version) -> Question | None:
    """The question the task now holds for the variant `r` was evaluated on (None when the variant is gone, or `r`
    was adopted without an evaluation)."""
    v = r.variant
    if v is None or v != "base" and v not in task.variants:
        return None
    return task.questions(v)[task.question_id]


def pick(task: Task, spec: str) -> tuple[str, Version]:
    """`current`, `v3`, or `draft` (current with the task's current question); named as asked for."""
    store = task.policies
    if spec == "draft":
        _, base = pick(task, CURRENT)
        if base.record is None:
            raise S1flowError(f"{base.spec.ref} was adopted without an evaluation (adopt --spec): it has no variant of the task's to draft an edited question from")
        q = _current(task, base)
        if q is None:
            raise S1flowError(f"{base.spec.ref} was evaluated on the variant {base.variant}, which the task no longer has")
        return "draft", Version(base.spec.with_question(q), base.record)
    n = version_number(spec)
    runtime = store.runtime.read(task.id, version=n) if n is not None else store.runtime.read(task.id, channel=spec)
    return spec, Version(runtime, store.record(runtime))


def default_candidate(task: Task, against: Version) -> str | None:
    """Current when against is another version (a pull request that adopted one), else an edit to the shipped
    question (a pull request that changes it before adopting it), else none."""
    current = task.policies.current(task.id)
    if current is not None and current != against.spec.version:
        return CURRENT
    q = _current(task, against)
    if q is not None and q != against.spec.question:
        return "draft"
    return None


def check(
    task: Task, against: str = CURRENT, candidate: str | None = None, sample: int | None = None, cached_only: bool = False,
) -> CheckResult:
    """`cached_only`: make no calls (a PR from a fork has no keys); when some are needed, the verdict is `pending`."""
    base_name, base_r = pick(task, against)
    cand_spec = candidate or default_candidate(task, base_r)
    cand = pick(task, cand_spec) if cand_spec else None
    notes: list[str] = []
    if cand and cand[1].spec.ref == base_r.spec.ref and cand[1].spec.question == base_r.spec.question:
        cand = None
        notes.append(f"{cand_spec} is the same version as {base_name}, so {base_name} alone is checked")
    return compare([(base_name, base_r)] + ([cand] if cand else []), task, sample, cached_only, notes)


def custom_code(task: Task, versions: list[tuple[str, Version]]) -> list[str]:
    """A custom objective a version was chosen on, against task.py's: gone is a ConfigError (both versions are
    measured with task.py's code, and there is none), changed is a note."""
    mine = {o.name: o for o in task.objectives if o.code_sha256}
    out: list[str] = []
    for name, v in versions:
        if (r := v.record) is None:
            continue
        e = r.evidence.evaluation
        for sc in [e.objective, *e.tiebreak]:
            o = sc.objective if sc is not None else None
            if o is None or o.code_sha256 is None:
                continue
            if o.name not in mine:
                raise ConfigError(f"{task.id}: {r.spec.ref} was chosen on {o.name}, a function of task.py's that is gone; check measures both "
                                  f"versions with task.py's code (restore {o.name}, or adopt a version chosen on the new objective)")
            if mine[o.name].code_sha256 != o.code_sha256 and (note := f"{o.name} changed after {r.spec.ref} (measured again with today's code)") not in out:
                out.append(note)
    return out


def compare(
    versions: list[tuple[str, Version]], task: Task, sample: int | None = None, cached_only: bool = False, notes: list[str] | None = None,
) -> CheckResult:
    """The base version alone, or the base and a candidate."""
    # Bind before test exposure. Stale conditions can be measured again, never silently certified.
    fresh_notes: list[str] = []
    for name, v in versions:
        if (r := v.record) is None:
            fresh_notes.append(f"{name} ({v.spec.ref}) was adopted without an evaluation (adopt --spec): this check is its first measurement")
            continue
        runtime = DecisionPolicy(v.spec, client=task.where.client())
        if (runtime.execution_digest != r.evidence.execution_digest or
                task.input_adapter_digest != r.evidence.input_adapter_digest):
            fresh_notes.append(f"{name}: execution conditions changed; measured again with the current binding and input adapter")
        if r.selection.forced:
            fresh_notes.append(f"{name} ({v.spec.ref}) was adopted with --force although the held-out test showed it below, by {r.selection.by}: "
                               f"{r.selection.reason}")
    changed = custom_code(task, versions)  # before any call: a missing function fails without spending
    sf = evalset.fixed(task)  # the test share the first run fixed (committed with the task)
    notes = (notes or []) + changed + fresh_notes
    by_id = task.load_cases().by_id()
    test = [i for i in sf.ids("test") if i in by_id and by_id[i].label is not None]
    if not test:
        raise DataError(f"{task.id}: no labelled case in the test share of {evalset.path(task).name}; nothing to check on")
    if sample and sample < len(test):
        test = sorted(random.Random(task.split.seed).sample(test, sample))
        notes.append(f"checked on {sample} of the {len(sf.ids('test'))} test cases (all of them after the merge)")
    cases = [by_id[i] for i in test]
    if cached_only and (need := {name: n for name, r in versions if (n := missing(task, r, cases))}):
        return CheckResult(
            task=task.id, n=len(cases), sample=sample, verdict="pending", need_calls=need, notes=notes,
            reasons=["some answers are not in the cache, and without keys there is no verdict (" + ", ".join(f"{k} {v}" for k, v in need.items()) + "); a run with keys decides (after the merge, or a PR from a branch of this repository)"],
        )

    async def both() -> list[Side]:
        return list(await asyncio.gather(*(ask(task, name, r, cases) for name, r in versions)))

    sides = asyncio.run(both())
    o0 = task.primary
    b0 = bound(o0, task.kind, task.custom_measures)
    c = b0.constraint
    sha = task.data_digest
    summaries = [summary(task, s) for s in sides]
    reasons: list[str] = []
    for s in sides:
        if s.policy.record is not None and s.policy.record.evidence.data_sha256 != sha:
            notes.append(f"{s.name} was chosen on other data (the values shown are measured again on today's test cases)")
            break
    checked = sides[-1]  # the candidate, or current alone
    if c is not None and c.broken(*c.count(checked.pairs)):
        reasons.append(f"{checked.name}: the {c.what} is {'below' if c.at_least else 'above'} {c.limit} "
                       f"(one-sided 95%: {c.shown_broken})")
    for f in measure.floors(task.constraints):  # a draft keeps the policy's rule, so no choice kept its floors
        if f.broken(*f.count(checked.pairs)):
            reasons.append(f"{checked.name}: the {f.what} is below {f.limit} (one-sided 95%: {f.shown_broken})")
    cap, cost = task.constraints.cost_per_10k_usd, summaries[-1].cost_per_10k_usd
    if cap is not None and (cost is None or summaries[-1].cost_unknown):
        return CheckResult(task=task.id, n=len(cases), sample=sample, verdict="pending", sides=summaries, notes=notes,
                           reasons=[f"{checked.name}: API cost constraint cannot be verified because cost is unknown"])
    if cap is not None and cost is not None and cost > cap:
        reasons.append(f"{checked.name}: the API cost is {usd(cost, 2)} per 10k, above the constraint {usd(cap, 2)}")
    p99_cap, p99 = task.constraints.latency_p99_ms, summaries[-1].latency_p99_ms
    if p99_cap is not None and p99 is None:
        return CheckResult(task=task.id, n=len(cases), sample=sample, verdict="pending", sides=summaries, notes=notes,
                           reasons=[f"{checked.name}: latency constraint cannot be verified because latency is unknown"])
    if p99_cap is not None and p99 is not None and p99 > p99_cap:
        reasons.append(f"{checked.name}: p99 is {p99:.0f}ms, above the constraint {p99_cap:.0f}ms (a cached answer keeps the time it took when asked; few cases make it noisy)")
    verdict: Verdict = "pass"
    diffs = None
    if len(sides) == 2:
        base, cand_s = sides
        draws = resamples(len(cases), task.split.seed)
        cov, acc = shown(task)
        assert cov.constraint is not None
        diffs = Diffs(
            primary=paired(b0.value, base, cand_s, draws), coverage=paired(cov.value, base, cand_s, draws),
            sure_accuracy=paired(cov.constraint.rate, base, cand_s, draws), accuracy=paired(acc.value, base, cand_s, draws),
        )
        lo, hi = diffs.primary.interval
        worse = hi < 0 if o0.maximize else lo > 0
        better = lo > 0 if o0.maximize else hi < 0
        if c is not None and not keeps(b0, base) and keeps(b0, cand_s):
            # the value counts only where the constraint holds: one that breaks it is not the bar to keep
            worse, better = False, True
            notes.append(f"on the test cases {base.name}'s {c.what} {c.missed} {c.limit}, so {cand_s.name}, which {c.excuse}, counts as better")
        if worse:
            reasons.append(f"{o0.label} is worse than {base.name}'s (the difference's 95% interval is {'below' if o0.maximize else 'above'} 0)")
        if c is not None:
            # at a fixed rule the value can hold while the constraint gets worse: that is what the constraint protects
            lo_c, hi_c = paired(c.rate, base, cand_s, draws).interval
            if hi_c < 0 if c.at_least else lo_c > 0:
                reasons.append(f"the {c.what} is {'lower' if c.at_least else 'higher'} than {base.name}'s (the difference's 95% interval is {'below' if c.at_least else 'above'} 0)")
        verdict = "better" if better else "no_difference"
    return CheckResult(
        task=task.id, n=len(cases), sample=sample, verdict="fail" if reasons else verdict, primary_label=o0.label,
        target_accuracy=task.coverage_target, data_sha256=sha, sides=summaries, diff=diffs, reasons=reasons, notes=notes,
    )
