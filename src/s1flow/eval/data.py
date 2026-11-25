"""`s1flow cases check`: whether a task's cases are ready to evaluate, before any call.

Collecting is the agent's work (any source, converted in a few lines to the task's data file);
this is the one place that says whether the result is usable.
"""

import json
import re
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
COPIED = 6  # words in a row a variant shares with a train case, beyond its base question, before the check names them
# A word: a katakana word, one kana or kanji (Japanese and Chinese have no spaces), or a run of other letters and digits.
_CJK = "\u3040-\u309f\u3400-\u9fff\uf900-\ufaff"
WORD = re.compile(f"[\u30a0-\u30ff]+|[{_CJK}]|[^\\W\u30a0-\u30ff{_CJK}]+")


class DataCheck(BaseModel):
    cases: int
    labelled: int
    labels: dict[str, int]  # label -> cases
    errors: list[str] = []  # cases that cannot be scored as they are
    warnings: list[str] = []  # usable, but likely to mislead
    test: int | None = None  # cases held out in the evaluation set, when it exists
    unassigned: int = 0  # labelled after split.json was written: placed by their ID's hash when it is read
    corrected: dict[str, int] = {}  # corrections.jsonl: verdict -> cases


def _label(kind: Any, label: Any) -> str:
    """A label as the count of labels names it: a multichoice's options in one order, a boxes label by how many.
    A label the kind cannot hold is named as written (`label_errors` reports it)."""
    if kind.type == "multichoice" and isinstance(label, (list, tuple)) and all(isinstance(k, str) for k in label):
        return ", ".join(sorted(label)) or "none"
    if kind.type == "boxes" and isinstance(label, (list, tuple)):
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
    labels = Counter(_label(kind, c.label) for c in labelled)
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
    if sf is not None:  # variants are written from train's mistakes, after the first run fixed the shares
        train = set(evalset.current(task).ids("train"))
        warnings += copied(task, [c for c in labelled if c.id in train])
    return DataCheck(
        cases=len(cases), labelled=len(labelled), labels=dict(labels.most_common()), errors=errors, warnings=warnings,
        test=None if sf is None else len(evalset.current(task).ids("test")), unassigned=0 if sf is None else sum(c.id not in sf.assign for c in labelled),
        corrected=dict(Counter(f.verdict for f in fixes.values()).most_common()),
    )


def _texts(value: Any) -> list[str]:
    """Every string a question or a state holds (a dict's values, not its keys: a question's keys are its options)."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [t for v in value.values() for t in _texts(v)]
    if isinstance(value, (list, tuple)):
        return [t for v in value for t in _texts(v)]
    return []


def _runs(text: str) -> list[tuple[tuple[str, ...], int, int]]:
    """Every COPIED words in a row in `text`: the words (case folded), where the first starts and the last ends."""
    w = list(WORD.finditer(text.casefold()))
    return [(tuple(m.group() for m in w[i:i + COPIED]), w[i].start(), w[i + COPIED - 1].end()) for i in range(len(w) - COPIED + 1)]


def _spans(text: str, shared: dict[tuple[str, ...], list[str]]) -> list[tuple[str, list[str]]]:
    """The stretches of `text` made of overlapping shared runs, each with the cases holding any of its runs."""
    spans: list[tuple[int, int, list[str]]] = []  # start, end, cases
    for words, a, b in _runs(text):
        if words not in shared:
            continue
        if spans and a < spans[-1][1]:  # overlaps the stretch so far
            start, _, ids = spans.pop()
            spans.append((start, b, ids + [i for i in shared[words] if i not in ids]))
        else:
            spans.append((a, b, list(shared[words])))
    return [(text[a:b], ids) for a, b, ids in spans]


def copied(task: Task, train: list[Case]) -> list[str]:
    """The variants that repeat a train case's text: the runs of COPIED words a variant shares with a train
    case's state and not with the base question. A question written from train cases that recites them fits
    them alone, and the held-out shares cannot show it when their cases are worded like train's."""
    base = {r[0] for t in _texts(task.question.model_dump()) for r in _runs(t)}
    texts = {n: _texts(q.model_dump()) for n, q in task.variants.items()}
    wanted = {r[0] for ts in texts.values() for t in ts for r in _runs(t)} - base
    shared: dict[tuple[str, ...], list[str]] = {}  # run -> the train cases holding it, in the cases file's order
    for c in train if wanted else []:
        for words in {r[0] for t in _texts(c.state) for r in _runs(t)} & wanted:
            shared.setdefault(words, []).append(c.id)
    out = []
    for name, ts in texts.items():
        if spans := [s for t in ts for s in _spans(t, shared)]:
            said = "; ".join(f'"{s}" ({", ".join(ids[:3])}{f" and {len(ids) - 3} more" if len(ids) > 3 else ""})' for s, ids in spans[:3])
            more = f" and {len(spans) - 3} more" if len(spans) > 3 else ""
            out.append(f"variant {name!r} repeats train cases' text: {said}{more}. A question that recites its cases fits them "
                       "alone: write the rule they share")
    return out


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
