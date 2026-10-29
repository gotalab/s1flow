"""What check measures on each version's answers, with objectives/measure.py's measures: a summary of each, and
the paired bootstrap of the difference between two (both read on the same resamples of the cases)."""

from __future__ import annotations

from typing import Callable, Literal

import numpy as np
from pydantic import BaseModel

from ..objectives.declare import Accuracy, Coverage
from ..objectives.measure import BOOTSTRAP, Bound, Pairs, bound, finite, interval
from ..task import Task
from .calls import Side


class SideSummary(BaseModel):
    name: str
    policy: str
    model: str
    variant: str
    objectives: list[float | None]  # in the task's order
    coverage: float  # share sure
    sure_accuracy: float | None
    accuracy: float
    sure: int
    sure_errors: int
    failed: int
    cost_per_10k_usd: float | None  # None when no call's cost is known
    cost_source: Literal["billed", "list", "mixed"] | None = None  # list: an estimate from the policy's list price
    cost_unknown: int = 0
    latency_p99_ms: float | None
    calls: int
    cached: int


class Diff(BaseModel):
    base: float
    candidate: float
    diff: float
    interval: tuple[float, float]


class Diffs(BaseModel):
    primary: Diff
    coverage: Diff
    sure_accuracy: Diff
    accuracy: Diff


def _nan(v: float | None) -> float:
    return float("nan") if v is None else v


def shown(task: Task) -> tuple[Bound, Bound]:
    """What every check shows beside the objectives: Coverage at the task's target (its value the sure share, its
    constraint the sure accuracy), and accuracy."""
    return bound(Coverage(task.coverage_target), task.kind), bound(Accuracy(), task.kind)


def summary(task: Task, s: Side) -> SideSummary:
    p = s.pairs
    n = len(p)
    cov, acc = shown(task)
    assert cov.constraint is not None
    lat = np.array(s.latency_ms)
    return SideSummary(
        name=s.name, policy=s.policy.spec.ref, model=s.policy.spec.model_id, variant=s.policy.candidate.variant,
        objectives=[finite(_nan(bound(o, task.kind, task.custom_measures).value(p))) for o in task.objectives],
        coverage=_nan(cov.value(p)), sure_accuracy=finite(_nan(cov.constraint.rate(p))), accuracy=_nan(acc.value(p)),
        sure=int(p.sure.sum()), sure_errors=int((p.sure & ~p.correct).sum()), failed=int((~p.ok).sum()),
        cost_per_10k_usd=s.spend.total_usd / n * 10_000 if n and s.spend.costs else None,
        cost_source=s.spend.source, cost_unknown=s.spend.unknown,
        latency_p99_ms=float(np.percentile(lat, 99)) if len(lat) and not s.latency_unknown else None,
        calls=s.calls, cached=s.cached,
    )


def resamples(n: int, seed: int) -> list[np.ndarray]:
    """BOOTSTRAP resamples of the n test cases, shared by every difference a check measures."""
    rng = np.random.default_rng(seed)
    return [rng.integers(0, n, n) for _ in range(BOOTSTRAP)]


def paired(f: Callable[[Pairs], float | None], base: Side, cand: Side, draws: list[np.ndarray]) -> Diff:
    """The candidate's `f` less the base's, with its interval over the resamples `draws` (a draw `f` reads nothing on is left out)."""
    b0, c0 = _nan(f(base.pairs)), _nan(f(cand.pairs))
    d = [x for i in draws if not np.isnan(x := _nan(f(cand.pairs[i])) - _nan(f(base.pairs[i])))]
    return Diff(base=b0, candidate=c0, diff=c0 - b0, interval=interval(d) or (float("nan"), float("nan")))


def keeps(b: Bound, s: Side) -> bool | None:
    """Whether the version keeps the primary's constraint on these cases (None: nothing to count)."""
    assert b.constraint is not None
    return b.constraint.holds(*b.constraint.count(s.pairs))
