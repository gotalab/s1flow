"""Objectives and constraints: what a task optimizes, how a candidate is chosen, and how each value is measured."""

import re
from pathlib import Path

import numpy as np
import pytest
from conftest import binary_preds, labelled

from s1flow.core.errors import ConfigError
from s1flow.eval.candidate import Candidate
from s1flow.eval.evaluation import Calls, Estimate, Evaluation, Failures, ObjectiveScore, Selective
from s1flow.objectives import AUROC, Accuracy, Constraints, Coverage, ExpectedLoss, F1, Objective, Recall
from s1flow.eval import evaluation
from s1flow.client import Boolean, Choice, Score
from s1flow.eval import Task, evalset, metrics
from s1flow.eval.objectives import measure
from s1flow.eval.objectives.measure import MEASURES, bound, measured_as
from s1flow.eval.select import rank
from s1flow.eval.kinds import BooleanKind, kind_of
from s1flow.policies.kinds import KindParams


def task(objs, **kw):
    return Task(id="t", cases="x.jsonl", state=lambda r: r["x"], question=Boolean(instructions="?"), label=lambda r: r["y"],
                objective=objs[0] if objs else None, tiebreak=objs[1:], **kw)


def scored(o: Objective, v: float, half: float = 0.05) -> ObjectiveScore:
    return ObjectiveScore(objective=o, value=v, interval=(v - half, v + half))


def ev(model, scores: list[ObjectiveScore], cost=1.0, p99=100.0, n=100) -> Evaluation:
    lat = evaluation.Latency(n=n, p50_ms=p99 / 2, p90_ms=p99, p95_ms=p99, p99_ms=p99, max_ms=p99, spread=2.0, retried=0, unrecorded=0, concurrency=[4], concurrency_unknown=0)
    return Evaluation(
        candidate=Candidate(model=model), answered_by=model, answered_by_all=[model], answered_ids=[str(i) for i in range(n)], n=n, probabilities=True,
        failures=Failures(calls=n, failed=0, unsupported=0, data_errors=0, unlabeled=0), accuracy=Estimate(value=0.9, interval=(0.85, 0.95)),
        objective=scores[0], tiebreak=scores[1:], calls=Calls(cost_per_10k_usd=cost, latency=lat),
    )


def cov(model, v, **kw) -> Evaluation:
    sel = Selective(target_accuracy=0.95, coverage=Estimate(value=v, interval=(v - 0.05, v + 0.05)), accuracy=0.96, n=50, errors=2, lower=0.9, labels_needed=None, min_probability=0.9)
    return ev(model, [scored(Coverage(), v)], **kw).model_copy(update={"selective": [sel]})


def test_objectives_must_fit_the_task():
    with pytest.raises(ConfigError, match="binary"):
        Task(id="t", cases="x", state=lambda r: r, question=Choice(instructions="?", criteria={"a": None, "b": None, "c": None}),
             label=lambda r: r, objective=Recall(max_false_alarm=0.01))
    assert task([]).objectives == [Accuracy().model_copy(update={"sets": "threshold"})]  # none listed: accuracy, at the cut it chooses
    with pytest.raises(ConfigError, match="score"):
        Task(id="t", cases="x", state=lambda r: r, question=Score(instructions="?", criteria=["low", "high"]), label=lambda r: r)
    task([Recall(max_false_alarm=0.01), ExpectedLoss()])  # a boolean task takes them


def test_the_best_on_the_primary_wins_when_the_intervals_part():
    ranked = rank(Coverage(), [], Constraints(), [cov("a", 0.9), cov("b", 0.5, cost=0.1)])
    assert [x.candidate for x in ranked] == ["a", "b"] and ranked[0].tied_with_best and not ranked[1].tied_with_best


def test_a_tie_on_the_primary_goes_to_the_next_objective_then_the_cheaper():
    c, a = Coverage(), AUROC()
    tied = [ev("a", [scored(c, 0.80), scored(a, 0.80)], cost=5.0), ev("b", [scored(c, 0.78), scored(a, 0.95)], cost=1.0), ev("c", [scored(c, 0.79), scored(a, 0.80)], cost=0.5)]
    only_cov = [e.model_copy(update={"tiebreak": []}) for e in tied]
    assert rank(c, ["latency", "cost"], Constraints(), only_cov)[0].candidate == "c"  # cheapest among the tied
    assert rank(c, [a], Constraints(), tied)[0].candidate == "b"  # the next objective first


def test_constraints_exclude_and_say_why():
    ranked = rank(Coverage(), [], Constraints(latency_p99_ms=200, min_labels=50), [cov("fast", 0.6), cov("slow", 0.9, p99=900)])
    assert ranked[0].candidate == "fast"
    assert {x.candidate: x.excluded for x in ranked[1:]} == {"slow": ["p99 900ms > 200ms"]}
    assert rank(Coverage(), [], Constraints(min_labels=50), [cov("few", 0.9, n=10)])[0].excluded == ["10 labels < 50"]


def test_lower_is_better_for_expected_cost():
    o = ExpectedLoss(fn=5, fp=1)
    assert rank(o, [], Constraints(), [ev("a", [scored(o, 0.3, 0.01)]), ev("b", [scored(o, 0.1, 0.01)])])[0].candidate == "b"


preds = binary_preds


def test_recall_and_cost_are_measured_out_of_fold():
    rng = np.random.default_rng(0)
    y = np.array([True] * 100 + [False] * 100)
    p = np.clip(np.where(y, 0.8, 0.2) + rng.normal(0, 0.25, 200), 0, 1)
    t = labelled(task([Recall(max_false_alarm=0.05), ExpectedLoss(fn=5, fp=1)]), y)
    e = metrics.evaluate(t, preds(p, y))
    rec, cost = e.scores
    assert rec.value is not None and rec.interval and rec.constraint is not None
    assert 0.8 < rec.value <= 1 and rec.constraint <= 0.1 and rec.interval[0] <= rec.value <= rec.interval[1]
    # The sure-answer table keeps the objective's target when it is Coverage, else 0.95.
    assert [s.target_accuracy for s in e.selective] == [0.95]
    # `tiebreak` is read at the primary's rule, the policy's: ExpectedLoss counts the errors at Recall's cut and
    # chooses no rule of its own.
    assert cost.value is not None and cost.rule is None and 0 <= cost.value < 0.5
    assert e.error_loss_threshold is not None and e.error_loss_threshold.chosen < 0.5  # the error table's cut: misses cost 5x, so it moves down
    both = metrics.evaluate(labelled(task([Coverage(), Coverage(target_accuracy=0.9)]), y), preds(p, y), target=0.95)  # a then Coverage adds its own
    assert [s.target_accuracy for s in both.selective] == [0.95, 0.9]
    assert (both.selective[1].coverage.value or 0) >= (both.selective[0].coverage.value or 0)


def test_recall_threshold_keeps_the_false_alarm_rate():
    y = np.array([True, True, True, False, False, False, False])
    p = np.array([0.9, 0.7, 0.4, 0.6, 0.3, 0.2, 0.1])
    recall = lambda m: metrics.search(bound(Recall(max_false_alarm=m), BooleanKind()), preds(p, y).pairs)
    assert recall(0.25) == 0.4  # one false alarm in four (0.6), the lowest such cut
    assert recall(0.2) == 0.7  # none


def test_accuracy_as_an_objective_leaves_the_test_share_out():
    y = np.array([True, False] * 100)
    t = labelled(task([Accuracy(), AUROC()]), y)
    test = np.array([int(i) for i in evalset.current(t).ids("test")])
    p = np.where(y, 0.9, 0.1)
    p[test] = 1 - p[test]  # every held-out case wrong: it must not count when candidates are ranked
    e = metrics.evaluate(t, preds(p, y))
    acc, au = e.scores
    assert len(test) == 60 and e.accuracy.value == 1.0 and e.test is None
    assert acc.value == 1.0 and acc.interval == (1.0, 1.0) and au.value == 1.0
    final = metrics.evaluate(t, preds(p, y), include_test=True)
    assert final.test is not None and final.test.accuracy == 0.0


CHOICE = Choice(instructions="?", criteria={"a": None, "b": None, "c": None})
HAND_WRITTEN = Objective(name="coverage", params={"target_accuracy": 0.9}, direction="min", sets="min_probability", unit="share", label="x")
LATENCY_BY_HAND = Objective(name="latency", direction="min", sets=None, unit="number", label="p99")


def declared(objs, question=CHOICE, **kw):
    return Task(id="gh-ruff-area", cases="x", state=lambda r: r, question=question, label=lambda r: r,
                objective=objs[0] if objs else None, tiebreak=objs[1:], **kw)


# One case per error stopped when a task.py loads (ConfigError, naming the task).
LOAD_ERRORS = {
    "objective the question type does not take": (lambda: declared([Recall(max_false_alarm=0.01)]), re.escape(
        "gh-ruff-area: recall needs a binary question (boolean, or a choice with positive); a choice takes accuracy, coverage, auroc, macro_f1")),
    "latency as the objective": (lambda: declared([LATENCY_BY_HAND]), "no objective named 'latency'"),
    "the same objective twice": (lambda: declared([Coverage(), Coverage(target_accuracy=0.95)]), "listed twice"),
    "an objective with no such name": (lambda: declared([Accuracy(), LATENCY_BY_HAND]), "no objective named 'latency'"),
    "a built-in written by hand": (lambda: declared([HAND_WRITTEN]), re.escape("coverage is a built-in objective; declare it with its function (Coverage(...))")),
    "Coverage in then under another objective": (lambda: declared([Accuracy(), Coverage()]), "coverage decides min_probability, so it only ranks as the objective"),
    "then holding something else": (lambda: declared([Coverage(), "accuracy"]), "tiebreak= takes objectives and .latency. and .cost., got .accuracy."),
    "objective= given a list": (lambda: Task(id="gh-ruff-area", cases="x", state=lambda r: r, question=CHOICE, label=lambda r: r,
                                             objective=[Coverage()]), "objective= is one objective"),
}


@pytest.mark.parametrize("name", LOAD_ERRORS)
def test_a_task_py_that_declares_what_it_cannot_is_stopped_when_it_loads(name):
    make, message = LOAD_ERRORS[name]
    with pytest.raises(ConfigError, match=message):
        make()


def test_an_objective_that_sets_what_the_kind_does_not_read_is_stopped():
    """Unreachable with the built-ins (each kind takes only those it reads); the guard is for a task's own."""
    from s1flow.eval.objectives.declare import check
    from s1flow.eval.kinds import ChoiceKind

    class Unread(ChoiceKind):
        sets = frozenset()

    with pytest.raises(ConfigError, match="sets a min_probability, which a choice question is not read by"):
        check(Coverage(), [], Unread(keys=["a", "b"]), "t")


def test_what_a_task_py_may_declare():
    declared([Coverage(), Coverage(target_accuracy=0.9)])  # another target is another objective
    t = declared([Coverage(), ExpectedLoss(fn=2, fp=1)], kind_params=KindParams(positive="a"))
    assert t.objectives == [Coverage(), ExpectedLoss(fn=2, fp=1)] and declared([]).primary == Accuracy()
    with pytest.raises(Exception):
        Objective(name="latency", direction="min", sets=None, unit="ms", label="p90")  # measured on the calls: never an objective
    with pytest.raises(ConfigError, match="target_accuracy is a share"):
        Coverage(target_accuracy=1.5)
    with pytest.raises(Exception):
        Objective(name="mine", unit="number", label="x")  # a direction and the rule it sets are not optional


def test_every_objective_a_kind_takes_is_measured():
    kinds = [kind_of(Boolean(instructions="?")), kind_of(Choice(instructions="?", criteria={"a": None, "b": None})),
             kind_of(Choice(instructions="?", criteria={"a": None, "b": None}), KindParams(positive="a"))]
    from s1flow.client import Box
    from s1flow.eval.objectives.declare import BUILT_IN

    kinds.append(kind_of(Box(instructions="?")))
    for k in kinds:
        for name in k.objectives:
            if name in BUILT_IN:
                assert (name, measured_as(k)) in MEASURES, (name, k.type)
        assert all((name, measured_as(k)) in MEASURES for name in (*k.report, "brier", "accuracy", "auroc"))


def test_f1_has_an_interval_and_chooses_the_threshold():
    rng = np.random.default_rng(0)
    y = np.array([True] * 100 + [False] * 100)
    p = np.clip(np.where(y, 0.7, 0.3) + rng.normal(0, 0.25, 200), 0, 1)
    f1 = metrics.evaluate(labelled(task([F1()]), y), preds(p, y)).objective
    assert f1.value is not None and f1.interval and f1.interval[0] <= f1.value <= f1.interval[1]
    assert f1.rule is not None and f1.rule.threshold is not None


def test_recall_on_the_test_share_is_judged_by_its_false_alarms():
    """The held-out share keeps the false-alarm bound, or shows it broken, whatever the recall."""
    rng = np.random.default_rng(0)
    y = np.array([True, False] * 150)
    p = np.clip(np.where(y, 0.8, 0.2) + rng.normal(0, 0.2, 300), 0, 1)
    t = labelled(task([Recall(max_false_alarm=0.1)]), y)
    test = np.array([int(i) for i in evalset.current(t).ids("test")])
    e = metrics.evaluate(t, preds(p, y), include_test=True)
    assert e.test is not None and e.test.constraint is not None and metrics.test_verdict(t, e) == "kept"
    loud = p.copy()
    loud[test[~y[test]]] = 0.99  # every held-out negative raises an alarm
    e = metrics.evaluate(t, preds(loud, y), include_test=True)
    k, n = e.test.constraint if e.test and e.test.constraint else (0, 0)
    assert k == n > 0 and metrics.test_verdict(t, e) == "below"


def test_no_branch_on_an_objective_outside_its_declaration():
    """Measuring is MEASURES', declaring is declare.py's: nothing asks which built-in an objective is."""
    src = Path(__file__).resolve().parents[1] / "src" / "s1flow"
    names = "Coverage|Recall|ExpectedLoss|AUROC|Accuracy|F1|MacroF1"
    found = [f"{p.relative_to(src)}:{i}" for p in src.rglob("*.py") for i, line in enumerate(p.read_text().splitlines(), 1)
             if re.search(rf"isinstance\([^)]*\b({names})\b", line)]
    assert not found


def test_floors_limit_the_threshold_and_are_never_relaxed():
    y = np.array([True, True, True, False, False, False, False])
    p = np.array([0.9, 0.7, 0.4, 0.6, 0.3, 0.2, 0.1])
    b, pairs = bound(ExpectedLoss(), BooleanKind()), preds(p, y).pairs
    at = lambda **floors: metrics.search(b, pairs, floors=measure.floors(Constraints(**floors)))  # noqa: E731
    assert at(min_precision=0.75, min_recall=0.66) == 0.4  # one false alarm (0.6); 0.7 loses as much, the lower kept
    assert at(min_precision=0.8, min_recall=0.66) == 0.7  # at 0.4 three of four read positive are: 75%
    assert at(min_precision=0.8, min_recall=0.9) == np.inf  # no cut keeps both: none, not the nearest


def test_a_model_no_threshold_lets_keep_the_floors_is_not_chosen():
    rng = np.random.default_rng(0)
    y = np.array([True, False] * 150)
    t = labelled(task([ExpectedLoss()], constraints=Constraints(min_precision=0.8, min_recall=0.8)), y)
    good = metrics.evaluate(t, preds(np.clip(np.where(y, 0.8, 0.2) + rng.normal(0, 0.1, 300), 0, 1), y), include_test=True)
    blind = metrics.evaluate(t, preds(rng.uniform(0, 1, 300), y), include_test=True).model_copy(update={"candidate": Candidate(model="blind")})
    assert good.objective is not None and good.objective.rule is not None
    assert [f.what for f in good.floors] == ["precision", "recall"] and all((f.rate or 0) >= 0.75 and f.test for f in good.floors)
    assert metrics.test_verdict(t, good) == "kept"
    assert blind.objective is not None and blind.objective.rule is None and all(f.test is None for f in blind.floors)
    excluded = {x.candidate: x.excluded for x in rank(t.primary, [], t.constraints, [good, blind])}
    assert excluded == {"m": [], "blind": ["no threshold keeps precision ≥ 80% and recall ≥ 80% on the dev cases"]}


def test_floors_need_an_objective_that_sets_a_binary_threshold():
    with pytest.raises(ConfigError, match="min_precision and min_recall limit the P.positive. threshold"):
        task([AUROC()], constraints=Constraints(min_recall=0.8))
    with pytest.raises(ConfigError, match="min_precision and min_recall"):
        declared([Coverage()], constraints=Constraints(min_precision=0.8))


def test_floors_leave_the_error_losses_table_alone_and_the_evaluation_reads_back():
    """With ExpectedLoss as the objective its cut is also the report's error-loss table: floors limit the first only,
    so a fold where no cut keeps them leaves no inf in the table (an inf is written as null and does not read back)."""
    rng = np.random.default_rng(0)
    y = np.array([True, False] * 150)
    p = np.clip(np.where(y, 0.65, 0.35) + rng.normal(0, 0.2, 300), 0, 1)
    plain = metrics.evaluate(labelled(task([ExpectedLoss()]), y), preds(p, y))
    floored = metrics.evaluate(labelled(task([ExpectedLoss()], constraints=Constraints(min_precision=0.85)), y), preds(p, y))
    assert floored.error_loss_threshold == plain.error_loss_threshold and floored.error_loss_threshold is not None and np.isfinite(floored.error_loss_threshold.median)
    assert Evaluation.model_validate_json(floored.model_dump_json()) == floored
