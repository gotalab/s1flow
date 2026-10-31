"""The evaluation set: which labelled case is train, val or test, kept across versions.

    tasks/<id>/split.json  {"schema": "s1flow/split@2", "seed": 1, "assign": {"<id>": "test", ...}}

The one owner of the held-out test share. `s1flow run` writes it, the first time it runs on a task, and
nothing else does: from the labelled cases, `task.split.test` of them held out, stratified by label, then
train / val within the rest (or from the split an optimization already used, so the cases GEPA never saw
stay test). A case labelled later is assigned by a hash of its id when the file is read, so no case ever
moves and the file never changes. Every evaluation holds out its test cases (metrics.evaluate) and
`check` compares on them. Before the first run, `current` gives the assignment run will write; `adopt`,
`check` and `optimize` refuse until the file is there (in CI: until it is committed).

How often the test share was looked at is not counted here: a count kept only where it ran, and lost in
CI, told nothing. `adopt` records each candidate it tried on it, refused or not, in history.jsonl.
"""

from __future__ import annotations

import hashlib
import math
import random
from pathlib import Path
from typing import Literal

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from ..core import clock
from ..core.errors import DataError
from .cases import Case
from .task import Task

Role = Literal["train", "val", "test"]
TRAIN_SHARE = 0.6  # of the rest


class SplitFile(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/split@2"] = Field(default="s1flow/split@2", alias="schema")
    seed: int
    test_share: float
    at: str  # when it was made
    source: str  # where the first assignment came from
    assign: dict[str, Role]  # as the first run wrote it; current() adds the cases labelled since

    def ids(self, role: Role) -> list[str]:
        return [i for i, r in self.assign.items() if r == role]


def path(task: Task) -> Path:
    return task.dir / "split.json"


def read(task: Task) -> SplitFile | None:
    """The file as written, without the cases labelled since."""
    p = path(task)
    if not p.exists():
        return None
    try:
        return SplitFile.model_validate_json(p.read_text())
    except ValueError as e:
        raise DataError(f"{p}: not a split file: {e}") from None


def initial(task: Task, labelled: list[Case], seed: int) -> dict[Role, list[str]]:
    """test / train / val, stratified by label: `task.split.test` of the labelled cases held out as test."""
    from sklearn.model_selection import train_test_split

    n_test = math.ceil(task.split.test * len(labelled))  # as train_test_split rounds it
    if len(labelled) - n_test < 2:
        raise DataError(f"{task.id}: {len(labelled)} labelled cases; holding out a test share and cross-validating the rest needs {n_test + 2} or more")
    y = np.array([str(c.label) for c in labelled])
    labels, counts = np.unique(y, return_counts=True)
    # stratify when every label can reach both sides: else (a label with one case, more labels than test cases) draw at random
    strat = y if min(counts) >= 2 and min(n_test, len(labelled) - n_test) >= len(labels) else None
    _, test = train_test_split(np.arange(len(labelled)), test_size=n_test, random_state=seed, stratify=strat)
    test_ids = {labelled[i].id for i in test}
    by: dict[str, list[Case]] = {}
    for c in labelled:
        if c.id not in test_ids:
            by.setdefault(str(c.label), []).append(c)
    rng = random.Random(seed)
    train, val = [], []
    for group in by.values():
        rng.shuffle(group)
        cut = max(1, round(len(group) * TRAIN_SHARE)) if len(group) > 1 else 1
        train += group[:cut]
        val += group[cut:]
    return {"train": [c.id for c in train], "val": [c.id for c in val], "test": sorted(test_ids)}


def _hashed(seed: int, cid: str, test_share: float) -> Role:
    h = hashlib.sha256(f"{seed}:{cid}".encode()).digest()
    u, v = int.from_bytes(h[:4]) / 2**32, int.from_bytes(h[4:8]) / 2**32
    return "test" if u < test_share else "train" if v < TRAIN_SHARE else "val"


def current(task: Task) -> SplitFile:
    """The task's split: the file's (else the one the first run will write) and the cases labelled since, by
    their hash. Writes nothing."""
    sf = read(task) or _initial(task)
    for c in task.load_cases().labelled():
        if c.id not in sf.assign:
            sf.assign[c.id] = _hashed(sf.seed, c.id, sf.test_share)
    return sf


def fixed(task: Task) -> SplitFile:
    """`current`, once the first run has written it: what adopt, check and optimize choose and compare on."""
    if not path(task).exists():
        raise DataError(f"{task.id}: no {path(task).name} yet: the first `s1flow run {task.id}` fixes the held-out test share "
                        "(commit it with the task, so CI checks on the same cases)")
    return current(task)


def fix(task: Task) -> str | None:
    """Write the split if the task has none (s1flow run, the one writer); what it did, to show, or None.
    Too few labelled cases to hold out a test share writes nothing: run still asks the models (to review the
    answers before labelling), and a later run fixes it."""
    if path(task).exists():
        return None
    try:
        sf = _initial(task)
    except DataError as e:
        return f"the held-out test share is not fixed yet ({e}); a run after labelling more cases fixes it"
    path(task).write_text(sf.model_dump_json(by_alias=True, indent=1) + "\n")
    return f"fixed the evaluation set ({path(task).name}: {len(sf.ids('test'))} test cases, from {sf.source}); commit it with the task"


def _initial(task: Task) -> SplitFile:
    art = next(iter(task.optimized.values()), None)
    sp = art.split if art else initial(task, task.load_cases().labelled(), task.split.seed)
    assign: dict[str, Role] = {i: role for role in ("train", "val", "test") for i in sp[role]}
    # the share cases labelled later are held out at: the task's, not what rounding made of the first few cases
    return SplitFile(seed=task.split.seed, test_share=task.split.test, at=clock.now(),
                     source=f"optimized/{art.variant}" if art else "initial", assign=assign)
