"""`tiebreak`: objectives, read at the primary objective's rule, and "latency" (only when measured alike) and "cost",
in the order it lists them; one naming neither has latency and then API cost after it."""

import asyncio
import json

import numpy as np
import pytest
from conftest import binary_preds, labelled, make_project
from test_latency import Timed
from test_objectives import ev, scored, task

from s1flow.eval import metrics, report
from s1flow.eval import run as running
from s1flow.core.errors import ConfigError
from s1flow.eval.evaluation import Estimate
from s1flow.eval.evaluation import Latency as LatencyStats
from s1flow.eval.select import rank, unlike, unlike_among_tied
from s1flow.eval.task import load
from s1flow.policies.rule import DecisionRule
from s1flow.objectives import AUROC, Accuracy, Constraints, Coverage, ExpectedLoss


def noisy(n=300, seed=0):
    rng = np.random.default_rng(seed)
    y = np.array([True, False] * (n // 2))
    return np.clip(np.where(y, 0.7, 0.3) + rng.normal(0, 0.25, n), 0, 1), y


def test_tiebreak_is_read_at_the_rule_the_policy_uses():
    p, y = noisy()
    cost = ExpectedLoss(fn=3, fp=1)
    under_coverage = metrics.evaluate(labelled(task([Coverage(target_accuracy=0.9), cost]), y), binary_preds(p, y)).tiebreak[0]
    under_accuracy = metrics.evaluate(labelled(task([Accuracy(), cost]), y), binary_preds(p, y)).tiebreak[0]
    as_primary = metrics.evaluate(labelled(task([cost]), y), binary_preds(p, y)).objective
    # Coverage sets a min probability and no threshold: the policy reads True at P >= 0.5, as Accuracy's does,
    # so the errors ExpectedLoss counts are the same; as the objective it picks its own cut, and costs less.
    assert under_coverage.value == under_accuracy.value and under_coverage.rule is None
    assert as_primary is not None and as_primary.chosen is not None and as_primary.chosen < 0.5 and as_primary.rule == DecisionRule(threshold=as_primary.chosen)
    assert as_primary.value is not None and under_coverage.value is not None and as_primary.value < under_coverage.value
    assert under_coverage.interval and under_coverage.interval[0] <= under_coverage.value <= under_coverage.interval[1]


def test_latency_is_each_cases_call_at_the_dev_p90(tmp_path):
    rng = np.random.default_rng(1)

    class Uneven(Timed):
        async def decide(self, state, questions, *, options=None):
            self.ms = float(rng.integers(50, 500))
            return await super().decide(state, questions, options=options)

    p = make_project(tmp_path, {"slow": Uneven}, copy_tasks=("nod-wake",))
    t = load(p, "nod-wake")
    asyncio.run(running.run(t, ["slow"], limit=40))
    pr = metrics.load(t, "base", "slow")
    lines = [json.loads(x) for x in running.run_path(t, "base", "slow").read_text().splitlines()]
    slowest = {}
    for r in lines:
        slowest[r["id"]] = max(slowest.get(r["id"], 0.0), r["latency_ms"])
    assert list(pr.case_latency_ms) == [slowest[i] for i in pr.ids]
    e = metrics.evaluate(t, pr)
    lat = e.calls.case_latency_p90_ms
    assert lat is not None and lat.value is not None and lat.interval and lat.interval[0] <= lat.value <= lat.interval[1]
    assert min(slowest.values()) <= lat.value <= max(slowest.values())


def test_an_unrecorded_latency_is_left_out_not_zero():
    assert metrics._percentile(np.array([np.nan, 100.0, 300.0]), 50) == 200.0
    assert metrics._percentile(np.array([np.nan]), 90) is None
    p, y = noisy(40)
    e = metrics.evaluate(labelled(task([Accuracy()]), y), binary_preds(p, y))  # Preds with no latency at all
    assert e.calls.case_latency_p90_ms is None and e.calls.latency is None


def timed(model, cov, p90, half=10.0, cost=1.0, concurrency=4, unrecorded=0, auroc=None):
    lat = LatencyStats(n=100, p50_ms=p90 / 2, p90_ms=p90, p95_ms=p90, p99_ms=p90, max_ms=p90, spread=2.0, retried=0,
                       unrecorded=unrecorded, concurrency=[concurrency], concurrency_unknown=0)
    e = ev(model, [scored(Coverage(), cov), *([] if auroc is None else [scored(AUROC(), auroc, 0.01)])], cost=cost)
    return e.model_copy(update={"answered_ids": [str(i) for i in range(e.n)], "calls": e.calls.model_copy(update={"latency": lat, "case_latency_p90_ms": Estimate(value=p90, interval=(p90 - half, p90 + half))})})


def order(evs, tiebreak=()):
    return [x.candidate for x in rank(Coverage(), task([Coverage(), *tiebreak]).ties, Constraints(), evs)]


def test_the_faster_of_the_tied_comes_first_when_measured_alike():
    cheap_slow, dear_fast = timed("cheap-slow", 0.80, 300, cost=0.1), timed("dear-fast", 0.79, 100, cost=5.0)
    assert order([cheap_slow, dear_fast]) == ["dear-fast", "cheap-slow"]  # latency before API cost
    sharp = [timed("cheap-slow", 0.80, 300, cost=0.1, auroc=0.9), timed("dear-fast", 0.79, 100, cost=5.0, auroc=0.7)]
    assert order(sharp, [AUROC()]) == ["cheap-slow", "dear-fast"]  # tiebreak objectives before either
    close = timed("dear-close", 0.79, 290, half=20, cost=5.0)  # its interval reaches the fastest's: latency does not tell them apart
    assert order([cheap_slow, close]) == ["cheap-slow", "dear-close"]
    assert unlike([cheap_slow, dear_fast]) is None


def test_latency_measured_unalike_is_skipped_and_says_how_to_measure_again():
    a, b = timed("a", 0.80, 300, cost=0.1, concurrency=8), timed("b", 0.79, 100, cost=5.0, concurrency=1)
    ranked = rank(Coverage(), ["latency", "cost"], Constraints(), [a, b])
    assert [x.candidate for x in ranked] == ["a", "b"]  # not by speed: by API cost
    why = unlike_among_tied(ranked, [a, b])
    assert why is not None and why.concurrencies == [1, 8]
    assert "concurrency 1, 8" in why.en("t") and "--concurrency N" in why.en("t") and "same N for all" in why.en("t")
    old = timed("old", 0.79, 100, cost=5.0, unrecorded=3)  # saved before retries were recorded
    assert order([timed("a", 0.80, 300, cost=0.1), old]) == ["a", "old"] and unlike([a, old]).unrecorded == ["old"]  # type: ignore[union-attr]


def test_the_report_names_what_ordered_the_tie_and_what_was_skipped():
    t = task([Coverage()])
    a, b = timed("a", 0.80, 300, cost=5.0), timed("b", 0.79, 100, cost=0.1)
    alike = report.headline(t, [a, b])
    assert "compared by p90 latency, then API cost, **b** is chosen" in alike and "latency not compared" not in alike
    a8 = timed("a", 0.80, 300, cost=5.0, concurrency=8)
    unalike = report.headline(t, [a8, b])
    assert "the lowest API cost is chosen: **b**" in unalike and "Latency not compared (concurrency 4, 8)" in unalike


def test_tiebreak_says_where_latency_and_cost_go():
    cheap_slow, dear_fast = timed("cheap-slow", 0.80, 300, cost=0.1), timed("dear-fast", 0.79, 100, cost=5.0)
    assert order([cheap_slow, dear_fast], ["cost", "latency"]) == ["cheap-slow", "dear-fast"]
    assert order([cheap_slow, dear_fast], ["cost"]) == ["cheap-slow", "dear-fast"]  # latency not used at all
    assert task([Coverage(), "cost"]).ties == ["cost"]
    sharp = [timed("cheap-slow", 0.80, 300, cost=0.1, auroc=0.7), timed("dear-fast", 0.79, 100, cost=5.0, auroc=0.9)]
    assert order(sharp, ["latency", AUROC()]) == ["dear-fast", "cheap-slow"]  # latency before the objective, as listed
    t = task([Coverage(), AUROC()])
    assert t.ties == [AUROC(), "latency", "cost"] and t.objectives == [Coverage(), AUROC()]  # the default after it
    unalike = [timed("a", 0.80, 300, cost=5.0, concurrency=8), timed("b", 0.79, 100, cost=0.1)]
    assert "latency not compared" not in report.headline(task([Coverage(), "cost"]), unalike)  # not asked for: not warned of
    assert "compared by API cost, then p90 latency" in report.headline(task([Coverage(), "cost", "latency"]),
                                                                       [timed("a", 0.80, 300, cost=5.0), timed("b", 0.79, 100, cost=0.1)])


@pytest.mark.parametrize("tiebreak, why", [(["speed"], "takes objectives and 'latency' and 'cost', got 'speed'"),
                                           (["cost", "cost"], "'cost' is listed twice"), ([object()], "tiebreak= lists objectives")])
def test_tiebreak_takes_objectives_latency_and_cost_only(tiebreak, why):
    with pytest.raises(ConfigError, match=why):
        task([Coverage(), *tiebreak])
