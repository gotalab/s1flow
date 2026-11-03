"""eval/select.py at its edges: a candidate exactly at a constraint's limit is kept, and intervals that only touch
tie. These pin the boundary as decided (2026-11-03), since no invariant tells `>` from `>=`."""

from conftest import ev

from s1flow.eval.evaluation import Estimate, ObjectiveScore
from s1flow.eval.select import rank, violations
from s1flow.objectives import Constraints, Coverage, ExpectedLoss


def scored(o, value, interval):
    return ObjectiveScore(objective=o, value=value, interval=interval)


def test_a_candidate_exactly_at_a_limit_is_kept():
    at = ev("m", [scored(Coverage(), 0.8, (0.7, 0.9))], cost=1.5, p99=200.0, n=100)
    assert violations(Constraints(latency_p99_ms=200, cost_per_10k_usd=1.5, min_labels=100), at) == []
    assert violations(Constraints(latency_p99_ms=199.9), at) == ["p99 200ms > 200ms"]
    assert violations(Constraints(cost_per_10k_usd=1.49), at) == ["API cost $1.50 per 10k > $1.49"]
    assert violations(Constraints(min_labels=101), at) == ["100 labels < 101"]


def tied(objective, best, other):
    """Whether `other` is tied with `best` on `objective`, each a (value, interval)."""
    ranked = rank(objective, [], Constraints(), [ev("best", [scored(objective, *best)]), ev("other", [scored(objective, *other)])])
    assert ranked[0].candidate in ("best", "other") and next(x for x in ranked if x.candidate == "best").tied_with_best
    return next(x for x in ranked if x.candidate == "other").tied_with_best


def test_intervals_that_touch_tie():
    assert tied(Coverage(), (0.8, (0.7, 0.9)), (0.6, (0.5, 0.7)))  # maximized: its upper end reaches the best's lower
    assert not tied(Coverage(), (0.8, (0.7, 0.9)), (0.6, (0.5, 0.6999)))
    assert tied(ExpectedLoss(), (0.2, (0.1, 0.3)), (0.4, (0.3, 0.5)))  # minimized: its lower end reaches the best's upper
    assert not tied(ExpectedLoss(), (0.2, (0.1, 0.3)), (0.4, (0.3001, 0.5)))


def latency_first(slower_interval):
    """The order when `slow` is better on the objective, and `fast` (p90 100ms, 90..110) faster on latency."""
    def timed(model, value, p90, interval):
        e = ev(model, [scored(Coverage(), value, (value - 0.05, value + 0.05))])
        return e.model_copy(update={"calls": e.calls.model_copy(update={"case_latency_p90_ms": Estimate(value=p90, interval=interval)})})

    evs = [timed("fast", 0.79, 100.0, (90.0, 110.0)), timed("slow", 0.80, 120.0, slower_interval)]
    return [x.candidate for x in rank(Coverage(), ["latency"], Constraints(), evs)]


def test_latency_intervals_that_touch_tie():
    assert latency_first((110.0, 130.0)) == ["slow", "fast"]  # touching: latency does not tell them apart, the objective does
    assert latency_first((110.5, 130.0)) == ["fast", "slow"]
