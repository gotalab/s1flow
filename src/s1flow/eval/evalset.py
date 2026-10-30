"""The evaluation set: which labelled case is train, val or test, kept across versions.

    tasks/<id>/split.json  {"schema": "s1flow/split@1", "seed": 1, "assign": {"<id>": "test", ...}, "uses": [...]}

The one owner of the held-out test share. Made from the split an optimization already used (so the
cases GEPA never saw stay test), else from the labelled cases: `task.split.test` of them held out,
stratified by label, then train / val within the rest. A case added later is assigned by a hash of
its id, so no case ever moves. Every evaluation holds out its test cases (metrics.evaluate) and
`check` compares on them. Until the file is written, `current` computes the same assignment without
writing it; the first `report` writes it (or `adopt`, `check`, `optimize`, whichever comes first).

`uses` counts the times the test share was looked at to choose or check something: a test share
looked at often stops being held out (choices drift toward it), so `check` asks for new cases then.
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
MANY_USES = 20  # past this, the test share wants new labels


class Use(BaseModel):
    at: str
    by: str  # adopt | check (propose in uses recorded before 2026-10-20)
    what: str


class SplitFile(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/split@1"] = Field(default="s1flow/split@1", alias="schema")
    seed: int
    test_share: float
    at: str  # when it was made
    source: str  # where the first assignment came from
    assign: dict[str, Role]
    uses: list[Use] = Field(default_factory=list)

    def ids(self, role: Role) -> list[str]:
        return [i for i, r in self.assign.items() if r == role]


def path(task: Task) -> Path:
    return task.dir / "split.json"


def read(task: Task) -> SplitFile | None:
    p = path(task)
    return SplitFile.model_validate_json(p.read_text()) if p.exists() else None


def _write(task: Task, sf: SplitFile) -> None:
    path(task).write_text(sf.model_dump_json(by_alias=True, indent=1) + "\n")


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
    """The task's split as `ensure` would leave it, without writing anything."""
    return _made(task)[0]


def ensure(task: Task) -> tuple[SplitFile, list[str]]:
    """The task's split, written on first use and extended to new labelled cases. Returns the notes to show."""
    sf, notes = _made(task)
    if notes:
        _write(task, sf)
    return sf, notes


def _made(task: Task) -> tuple[SplitFile, list[str]]:
    rows = task.load_cases().labelled()
    sf = read(task)
    notes: list[str] = []
    if sf is None:
        art = next(iter(task.optimized.values()), None)
        sp = art.split if art else initial(task, rows, task.split.seed)
        assign: dict[str, Role] = {i: role for role in ("train", "val", "test") for i in sp[role]}
        n_test = len(sp["test"])
        sf = SplitFile(
            seed=task.split.seed, test_share=round(n_test / max(1, len(assign)), 3),
            at=clock.now(),
            source=f"optimized/{art.variant}" if art else "initial", assign=assign,
        )
        notes.append(f"fixed the evaluation set ({path(task).name}: {n_test} test cases, from {sf.source})")
    new = [c.id for c in rows if c.id not in sf.assign]
    for cid in new:
        sf.assign[cid] = _hashed(sf.seed, cid, sf.test_share)
    if new:
        notes.append(f"assigned {len(new)} new cases ({sum(sf.assign[c] == 'test' for c in new)} to test)")
    return sf, notes


def record_use(task: Task, by: str, what: str) -> int:
    """Count every explicit look, including CI; this file is a local ledger only."""
    sf, _ = ensure(task)
    sf.uses.append(Use(at=clock.now(), by=by, what=what))
    _write(task, sf)
    return len(sf.uses)
