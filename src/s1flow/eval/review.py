"""`s1flow cases review`: the cases whose label is worth reading again, and what the reading so far says.

A case is listed when models answered something else with a high probability, or when another case has the
same state and a different label. s1flow only points; a person (with an agent) reads each case against the
question's criteria as written and records a verdict with `s1flow cases correct` (task.Correction).

Reading only the cases models disagree with favours those models, so a random sample of the other cases can be
read too (`sample`): its relabel share is the label error rate the list cannot show. How many to sample, and
when unclear and missing are too many, depend on what the task is for; the Skill says how to choose, not this code.
"""

from __future__ import annotations

import json
import random
from typing import Any

from pydantic import BaseModel, ValidationError

from ..core import clock
from ..core.errors import DataError, NotFound, Unsupported, invalid
from . import evalset, metrics
from .objectives.measure import cp_lower
from .run import run_path
from .cases import CORRECTIONS, SAMPLED, Correction, ReviewSample, Verdict
from .shown import pct
from .task import Task


class Opinion(BaseModel):
    model: str
    answer: Any
    probability: float


class Listed(BaseModel):
    id: str
    label: Any
    text: str
    state: Any
    role: str | None  # train / val / test in the evaluation set, when it exists
    why: list[str]
    opinions: list[Opinion] = []  # the models that answered something else at min_probability or more
    sampled: bool = False


class Tally(BaseModel):
    read: int
    verdicts: dict[str, int]
    sample_read: int
    sample_relabelled: int
    error_rate: tuple[float, float] | None  # 95% interval of the label error rate, from the random sample
    premise: list[str]  # the reasons given for unclear and missing: evidence about the task, not the labels


class Review(BaseModel):
    task: str
    models: list[str]
    min_probability: float
    listed: list[Listed]
    sample: list[Listed]
    tally: Tally


def _models(task: Task) -> list[str]:
    d = run_path(task, "base", "x").parent
    return sorted(p.stem for p in d.glob("*.jsonl")) if d.exists() else []


def review(task: Task, *, min_probability: float = 0.9, limit: int = 30, sample: int = 0, include_read: bool = False) -> Review:
    if task.kind.type == "box":
        raise Unsupported(f"{task.id}: review lists label disagreements; box tasks are not supported yet")
    fixes = task.load_cases().corrections()
    by_id = task.load_cases().by_id()
    sf = evalset.current(task)
    role = lambda i: sf.assign.get(i)
    by_id = {cid: c for cid, c in by_id.items() if role(cid) != "test"}
    fixes = {cid: f for cid, f in fixes.items() if cid in by_id}
    models = _models(task)
    opinions: dict[str, list[Opinion]] = {}
    for m in models:
        try:
            pr = metrics.load(task, "base", m)
        except NotFound:
            continue
        if not len(pr.y):
            continue
        pred, conf = pr.pairs.value, pr.pairs.probability
        for i, cid in enumerate(pr.ids):
            if pred[i] != pr.y[i] and conf[i] >= min_probability:
                opinions.setdefault(cid, []).append(Opinion(model=m, answer=_plain(pred[i]), probability=float(conf[i])))
    why: dict[str, list[str]] = {}
    for cid, ops in opinions.items():
        answers = sorted({json.dumps(o.answer) for o in ops})
        why[cid] = [f"{len(ops)}/{len(models)} models answered {', '.join(answers)} (probability {min_probability:g} or more)"]
    seen: dict[str, str] = {}
    for c in by_id.values():
        if c.label is None:
            continue
        key = json.dumps(c.state, sort_keys=True, ensure_ascii=False, default=str)
        if key in seen and by_id[seen[key]].label != c.label:
            for a, b in ((seen[key], c.id), (c.id, seen[key])):
                why.setdefault(a, []).append(f"the same state as {b}, with another label ({by_id[b].label!r})")
        seen.setdefault(key, c.id)

    def listed(cid: str, reasons: list[str], sampled: bool = False) -> Listed:
        c = by_id[cid]
        ops = sorted(opinions.get(cid, []), key=lambda o: -o.probability)
        return Listed(id=cid, label=c.label, text=c.text, state=c.state, role=role(cid), why=reasons, opinions=ops, sampled=sampled)

    todo = [cid for cid in why if cid in by_id and by_id[cid].label is not None and (include_read or cid not in fixes)]
    # the strongest first: more models disagreeing, then the higher probability
    todo.sort(key=lambda cid: (-len(opinions.get(cid, [])), -max((o.probability for o in opinions.get(cid, [])), default=0)))
    rest = [c.id for c in by_id.values() if c.label is not None and c.id not in why and c.id not in fixes]
    picked = sorted(random.Random(task.split.seed).sample(rest, min(sample, len(rest))))
    if picked:  # kept, so a correction of one counts toward the label error rate (`correct`)
        (task.dir / SAMPLED).write_text(ReviewSample(ids=sorted(sampled(task) | set(picked))).model_dump_json(indent=1) + "\n")
    return Review(
        task=task.id, models=models, min_probability=min_probability,
        listed=[listed(cid, why[cid]) for cid in todo[:limit]],
        sample=[listed(cid, ["drawn at random (to estimate the label error rate)"], sampled=True) for cid in picked],
        tally=tally(fixes),
    )


def tally(fixes: dict[str, Correction]) -> Tally:
    verdicts: dict[str, int] = {}
    for f in fixes.values():
        verdicts[f.verdict] = verdicts.get(f.verdict, 0) + 1
    sampled = [f for f in fixes.values() if f.sampled]
    k = sum(f.verdict == "relabel" for f in sampled)
    n = len(sampled)
    rate = (cp_lower(k, n, 0.975), 1 - cp_lower(n - k, n, 0.975)) if n else None  # two-sided Clopper-Pearson
    doubtful = [f for f in fixes.values() if f.verdict in ("unclear", "missing")]
    premise = [f"{f.verdict}: {f.id}: {f.reason}" for f in doubtful]
    return Tally(read=len(fixes), verdicts=verdicts, sample_read=len(sampled), sample_relabelled=k, error_rate=rate, premise=premise)


def sampled(task: Task) -> set[str]:
    """The cases `review` has drawn at random (review-sample.json)."""
    path = task.dir / SAMPLED
    if not path.exists():
        return set()
    try:
        return set(ReviewSample.model_validate_json(path.read_text()).ids)
    except ValidationError as e:
        raise DataError(f"{task.id}: {SAMPLED}: {invalid(e)}") from None


def correct(task: Task, case_id: str, verdict: Verdict, *, reason: str, by: str, label: Any = None) -> Correction:
    """Append one decision to corrections.jsonl, checked against the task as collected. A case `review` drew at
    random is recorded as sampled."""
    collected = {c.id: c for c in task.load_cases().collected()}
    if case_id not in collected:
        raise NotFound(f"{task.id}: no case {case_id!r}")
    was = collected[case_id].label
    if not reason.strip():
        raise DataError("a correction needs its reason: which criterion decides it, or what is missing")
    if verdict == "relabel":
        if (wrong := task.kind.label_error(label)) is not None:
            raise DataError(f"{case_id}: {wrong}")
        if label == was:
            raise DataError(f"{case_id}: the label is already {label!r}; record keep instead")
    try:
        fix = Correction(id=case_id, verdict=verdict, label=label if verdict == "relabel" else None, was=was, reason=reason.strip(),
                         by=by, at=clock.now(), sampled=case_id in sampled(task))
    except ValidationError as e:
        raise DataError(invalid(e)) from None
    with (task.dir / CORRECTIONS).open("a") as f:
        f.write(fix.model_dump_json() + "\n")
    task.load_cases().forget()
    return fix


def _plain(v: Any) -> Any:
    return v.item() if hasattr(v, "item") else v


def markdown(task: Task, r: Review) -> str:
    t = r.tally
    L = [f"# {task.id} · review", ""]
    L.append(f"{len(r.listed)} cases from the answers of {len(r.models)} models ({', '.join(r.models) or 'no runs yet'}), {len(r.sample)} at random.")
    if t.read:
        L.append("Read {}: {}".format(t.read, ", ".join(f"{k} {v}" for k, v in sorted(t.verdicts.items()))))
    if t.error_rate is not None:
        lo, hi = t.error_rate
        L.append(f"Of {t.sample_read} sampled cases read, {t.sample_relabelled} relabelled: the label error rate is about {pct(lo, sign='')}-{pct(hi)}")
    else:
        L.append("No sampled case read yet: the label error rate is not known (--sample N)")
    if t.premise:
        L += ["", f"## Evidence against the premise (unclear or missing {len(t.premise)} of {t.read} read)", "",
              "Not label errors: evidence about the question, its options' criteria or the state. When there are many, or their reasons agree, a person decides whether to revise the task before fixing labels.", ""]
        L += [f"- {x}" for x in t.premise[:20]]
    L += ["", "How to decide: apply the question's criteria as written. When they do not decide it, unclear; when the state lacks what decides it, missing.", ""]
    for n, x in enumerate(r.listed + r.sample, 1):
        L += [f"## {n}. {x.id} · label {x.label!r}" + (f" · {x.role}" if x.role else ""), "", x.text[:300], ""]
        L += [f"- {w}" for w in x.why]
        L += [f"  - {o.model}: {o.answer!r} ({o.probability:.2f})" for o in x.opinions]
        L += ["", f"`s1flow cases correct {task.id} {x.id} --verdict relabel|keep|unclear|missing [--label X] --reason \"...\"`", ""]
    if not r.listed and not r.sample:
        L.append("- No case to read")
    return "\n".join(L) + "\n"
