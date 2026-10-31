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
    """Yields (fit, eval) index pairs into the full arrays, over the dev share only: the folds scikit-learn's
    LeaveOneOut, StratifiedKFold or KFold (shuffled, random_state=split.seed) give, made here because importing
    scikit-learn takes most of a second of every evaluating command (tests/test_split.py holds them equal)."""
    dev = p.dev
    yd = y[dev]
    k = min(split.k, len(dev))
    if p.method == "loo":
        k, fold = len(dev), np.arange(len(dev))
    elif _stratifiable(yd, k):
        fold = _stratified(yd, k, np.random.RandomState(split.seed))
    else:  # some label has fewer than k cases
        fold = _plain(len(dev), k, np.random.RandomState(split.seed))
    every = np.arange(len(dev))
    for i in range(k):
        yield dev[every[fold != i]], dev[every[fold == i]]


def _plain(n: int, k: int, rng: np.random.RandomState) -> np.ndarray:
    """KFold's: the shuffled cases cut in k runs, the first n % k one longer."""
    order = np.arange(n)
    rng.shuffle(order)
    sizes = np.full(k, n // k)
    sizes[: n % k] += 1
    fold = np.empty(n, dtype=int)
    fold[order] = np.repeat(np.arange(k), sizes)
    return fold


def _stratified(y: np.ndarray, k: int, rng: np.random.RandomState) -> np.ndarray:
    """StratifiedKFold's: each label's cases dealt round robin over the folds in sorted label order, then each
    label's fold numbers shuffled (labels taken in order of first appearance)."""
    _, first, inverse = np.unique(y, return_index=True, return_inverse=True)
    _, by_appearance = np.unique(first, return_inverse=True)
    code = by_appearance[inverse]
    ordered = np.sort(code)
    allocation = np.asarray([np.bincount(ordered[i::k], minlength=len(first)) for i in range(k)])
    fold = np.empty(len(y), dtype=int)
    for c in range(len(first)):
        of_label = np.arange(k).repeat(allocation[:, c])
        rng.shuffle(of_label)
        fold[code == c] = of_label
    return fold


def describe(p: Plan) -> str:
    return f"{NAMES[p.method]} ({p.note})"
