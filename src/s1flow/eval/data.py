"""`s1flow cases check`: whether a task's cases are ready to evaluate, before any call.

Collecting is the agent's work (any source, converted in a few lines to the task's data file);
this is the one place that says whether the result is usable.
"""

import json
from typing import Any
from collections import Counter

from pydantic import BaseModel

from ..core.errors import DataError
from ..client.state import has_unprepared_media
from ..policies.kinds import same_label
from . import evalset
from .cases import Case
from .shown import pct
from .task import Task

MINORITY = 0.2  # a binary task whose smaller side is under this share: Accuracy favours the larger side


class DataCheck(BaseModel):
    cases: int
    labelled: int
    labels: dict[str, int]  # label -> cases
    errors: list[str] = []  # cases that cannot be scored as they are
    warnings: list[str] = []  # usable, but likely to mislead
    test: int | None = None  # cases held out in the evaluation set, when it exists
    unassigned: int = 0  # labelled after split.json was written: placed by their ID's hash when it is read
    corrected: dict[str, int] = {}  # corrections.jsonl: verdict -> cases


def _label(label: Any) -> str:
    """A label as the count of labels names it: a multichoice's options in one order, a boxes label by how many."""
    if isinstance(label, (list, tuple)):
        if all(isinstance(k, str) for k in label):
            return ", ".join(sorted(label)) or "none"
        return "1 box" if len(label) == 1 else f"{len(label)} boxes"
    return str(label)


def label_errors(task: Task, cases: list[Case]) -> list[str]:
    """The labels the task's question cannot score ("<id>: <why>"): a run refuses them before its first call, as
    the report that reads its answers would fail on them."""
    return [f"{c.id}: {wrong}" for c in cases if c.label is not None and (wrong := task.kind.label_error(c.label)) is not None]


def check(task: Task) -> DataCheck:
    try:
        cases = task.load_cases().all()
        fixes = task.load_cases().corrections()
    except DataError as e:
        return DataCheck(cases=0, labelled=0, labels={}, errors=[str(e)])
    errors: list[str] = []
    warnings: list[str] = []
    kind = task.kind
    collected = {c.id: c.label for c in task.load_cases().collected()}
    for f in fixes.values():
        if f.id not in collected:
            errors.append(f"{f.id}: corrected in corrections.jsonl, but no case has this id")
        elif not same_label(kind, collected[f.id], f.was):
            warnings.append(f"{f.id}: corrected from {f.was!r}, but the collected label is now {collected[f.id]!r}; read it again")
    for id_, n in Counter(c.id for c in cases).items():
        if n > 1:
            errors.append(f"{id_}: {n} cases share this id")
    labelled = [c for c in cases if c.label is not None]
    errors += label_errors(task, labelled)
    for c in labelled:
        if c.state in (None, "", [], {}):
            errors.append(f"{c.id}: the state is empty")
        elif has_unprepared_media(c.state):
            try:
                task.model_state(c)
            except DataError as e:
                errors.append(f"{c.id}: {e}")
    seen: dict[str, Case] = {}
    for c in labelled:
        key = json.dumps(c.state, sort_keys=True, ensure_ascii=False, default=str)
        if key in seen and not same_label(kind, seen[key].label, c.label):
            warnings.append(f"{seen[key].id} and {c.id} have the same state and different labels ({seen[key].label!r} / {c.label!r})")
        seen.setdefault(key, c)
    labels = Counter(_label(c.label) for c in labelled)
    if kind.binary and labelled:
        small = min(labels.get("True", 0), labels.get("False", 0)) / len(labelled)
        if small < MINORITY and task.primary.name == "accuracy":
            warnings.append(f"the smaller side is {pct(small)} of the cases: Accuracy rewards always answering the larger side; consider F1 or Recall as the objective")
    if len(labelled) < 50:
        warnings.append(f"{len(labelled)} labelled cases: intervals will be wide, and the held-out test share small; aim for 200 or more")
    for k in kind.options:
        if not kind.binary and labels.get(k, 0) == 0:
            warnings.append(f"option {k!r} has no labelled case")
    said = getattr(task.question, "criteria", None) or {}  # a box question has none
    if todo := [str(k) for k, v in (said.items() if isinstance(said, dict) else enumerate(said)) if v and "TODO" in v]:
        warnings.append(f"the criteria of {', '.join(todo)} still say TODO: the model reads them as written; fill them in task.py")
    sf = evalset.read(task)
    return DataCheck(
        cases=len(cases), labelled=len(labelled), labels=dict(labels.most_common()), errors=errors, warnings=warnings,
        test=None if sf is None else len(evalset.current(task).ids("test")), unassigned=0 if sf is None else sum(c.id not in sf.assign for c in labelled),
        corrected=dict(Counter(f.verdict for f in fixes.values()).most_common()),
    )


def markdown(task: Task, r: DataCheck) -> str:
    L = [f"# {task.id} · data", "", f"{r.cases} cases, {r.labelled} labelled: " + ", ".join(f"{k} {v}" for k, v in r.labels.items())]
    if r.corrected:
        L.append("corrected: " + ", ".join(f"{k} {v}" for k, v in r.corrected.items()))
    if r.test is not None:
        L.append(f"evaluation set: test {r.test}" + (f" ({r.unassigned} cases labelled since split.json, placed by their ID's hash)" if r.unassigned else ""))
    L += [""] + [f"- ✗ {e}" for e in r.errors[:50]] + [f"- ⚠ {w}" for w in r.warnings[:50]]
    if not r.errors and not r.warnings:
        L.append("- ok")
    return "\n".join(L) + "\n"
