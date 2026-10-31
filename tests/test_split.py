"""split.folds makes, without importing scikit-learn, the folds its splitters give."""
import numpy as np
import pytest
from sklearn.model_selection import KFold, LeaveOneOut, StratifiedKFold

from s1flow.eval import split
from s1flow.eval.task import Split


def sklearn_folds(p: split.Plan, y: np.ndarray, s: Split) -> list[tuple[list[int], list[int]]]:
    dev, yd = p.dev, y[p.dev]
    k = min(s.k, len(dev))
    if p.method == "loo":
        it = LeaveOneOut().split(dev)
    elif split._stratifiable(yd, k):
        it = StratifiedKFold(k, shuffle=True, random_state=s.seed).split(dev, yd)
    else:
        it = KFold(k, shuffle=True, random_state=s.seed).split(dev)
    return [(dev[fit].tolist(), dev[ev].tolist()) for fit, ev in it]


@pytest.mark.parametrize("seed", range(30))
def test_the_folds_are_scikit_learns(seed):
    rng = np.random.default_rng(seed)
    n = int(rng.integers(2, 40) if seed % 3 == 0 else rng.integers(60, 300))  # leave-one-out, or k-fold
    labels = rng.choice([[True, False], ["a", "b", "c"], [0, 1, 2, 3, 4]][seed % 3], n)
    if seed % 4 == 0:
        labels[0] = "rare" if labels.dtype.kind == "U" else 9  # one label under k cases: plain k-fold
    p = split.plan(n, rng.choice(n, int(rng.integers(0, n // 3 + 1)), replace=False))
    s = Split(k=int(rng.integers(2, 8)), seed=int(rng.integers(0, 2**31)))
    mine = [(fit.tolist(), ev.tolist()) for fit, ev in split.folds(p, labels, s)]
    assert mine == sklearn_folds(p, labels, s)
