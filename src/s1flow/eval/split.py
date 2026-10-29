"""Splitting (SPEC §8): cross-validation over the dev share, chosen by its size. The held-out test share is
the task's evaluation set (evalset.py); here it is only left out.

Under `SMALL` dev cases, leave-one-out; from there on, stratified k-fold (k-fold when some label has fewer
than k cases). Nothing here calls a model: splits are recomputed over cached answers.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterator

import numpy as np
from sklearn.model_selection import KFold, LeaveOneOut, StratifiedKFold

from .task import Split

SMALL = 50  # below this, leave-one-out
NAMES = {"loo": "leave-one-out", "stratified-kfold": "stratified k-fold"}


@dataclass
class Plan:
    method: str  # loo | stratified-kfold
    dev: np.ndarray  # indices used for CV
    test: np.ndarray  # held-out indices (may be empty)
    note: str


def _stratifiable(y: np.ndarray, k: int) -> bool:
    return min(Counter(y.tolist()).values()) >= k


def plan(n: int, test: np.ndarray) -> Plan:
    """`test`: the indices of the evaluation set's test cases (evalset.py), left out of the CV."""
    test = np.sort(test)
    dev = np.setdiff1d(np.arange(n), test)
    m = "loo" if len(dev) < SMALL else "stratified-kfold"
    note = f"{len(test)} test cases of the fixed evaluation set held out" if len(test) else "no test case among these: CV numbers only"
    return Plan(method=m, dev=dev, test=test, note=note)


def folds(p: Plan, y: np.ndarray, split: Split) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """Yields (fit, eval) index pairs into the full arrays, over the dev share only."""
    dev = p.dev
    yd = y[dev]
    k = min(split.k, len(dev))
    if p.method == "loo":
        it = LeaveOneOut().split(dev)
    elif _stratifiable(yd, k):
        it = StratifiedKFold(k, shuffle=True, random_state=split.seed).split(dev, yd)
    else:  # some label has fewer than k cases
        it = KFold(k, shuffle=True, random_state=split.seed).split(dev)
    for fit, ev in it:
        yield dev[fit], dev[ev]


def describe(p: Plan) -> str:
    return f"{NAMES[p.method]} ({p.note})"
