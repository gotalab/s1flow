"""The cost table (Loss; Accuracy and ExpectedLoss are fixed forms of it), custom objectives, and
whether the weights make the choice."""

import asyncio
import json

import numpy as np
import pytest
from conftest import Sharp, attach, binary_preds, declared, labelled, make_project, task

from s1flow.client import Boolean, Box
from s1flow.core.errors import ConfigError
from s1flow.eval import Task, adopt, check, metrics, report
from s1flow.eval import run as running
from s1flow.eval.objectives.measure import Table, bound, pairs
from s1flow.eval.weights import decides, sensitivity
from s1flow.objectives import Accuracy, Loss, Coverage, ExpectedLoss, Objective, Reading, on_set, per_case
from s1flow.eval.kinds import ChoiceKind


def choice_pairs(labels, said, probability=0.9):
    kind = ChoiceKind(keys=["a", "b", "c"])
    readings = [None if s is None else Reading(value=s, probability=probability, below_min_probability=False,
                                               distribution=[probability if k == s else (1 - probability) / 2 for k in "abc"]) for s in said]
    return kind, pairs(kind, labels, readings)


def test_a_table_charges_each_answer_on_each_label():
    kind, p = choice_pairs(["a", "a", "b", "c", "c"], ["a", "b", "c", None, "c"])
    o = Loss(default=1.0, losses={"a": {"b": 3.0}, "c": {"a": 10.0}})
    # a right (0), a->b (3), b->c (default 1), c failed (its row's most: c->a 10), c right (0)
    assert bound(o, kind).value(p) == pytest.approx((3 + 1 + 10) / 5)
    unsure_loss = Loss(default=1.0, unsure=0.25)
    assert bound(unsure_loss, kind).value(p) == pytest.approx((1 + 1 + 0.25) / 5)  # a failed call loses `unsure`
    unsure = p.at(min_probability=0.95)  # every answer under it: abstained
    assert bound(unsure_loss, kind).value(unsure) == pytest.approx(5 * 0.25 / 5)
    assert bound(Loss(), kind).value(unsure) == pytest.approx(3 / 5)  # without unsure, an unsure answer is read as given


def test_the_table_chooses_the_rule_its_question_reads():
    assert declared([Loss()]).primary.sets is None  # a choice, no unsure: the most probable option, as given
    assert declared([Loss(unsure=0.2)]).primary.sets == "min_probability"
    binary = Task(id="t", cases="x", state=lambda r: r, question=Boolean(instructions="?"), label=lambda r: r, objective=Loss())
    assert binary.primary.sets == "threshold" and binary.primary.params == {"default": 1.0, "losses": {}, "unsure": None}


def test_accuracy_and_expected_cost_are_the_table_by_name(tmp_path):
    rng = np.random.default_rng(3)
    y = np.array([True, False] * 150)
    p = np.clip(np.where(y, 0.65, 0.35) + rng.normal(0, 0.25, 300), 0, 1)
    by_name = metrics.evaluate(labelled(task([ExpectedLoss(fn=5, fp=1)]), y, tmp_path), binary_preds(p, y)).objective
    as_table = metrics.evaluate(labelled(task([Loss(default=0, losses={"true": {"false": 5}, "false": {"true": 1}})]), y, tmp_path), binary_preds(p, y)).objective
    assert by_name is not None and as_table is not None
    assert (by_name.value, by_name.interval, by_name.rule) == (as_table.value, as_table.interval, as_table.rule)  # bit for bit
    kind, cp = choice_pairs(["a", "b", "c", "a"] * 25, ["a", "b", "a", None] * 25)
    acc, cost = bound(Accuracy(), kind).value(cp), bound(Loss(), kind).value(cp)
    assert acc == float(cp.correct.mean()) and acc == pytest.approx(1 - cost, abs=1e-15)  # a share right, or the mean cost of an error
    assert Table(keys=[True, False], loss=np.array([[0.0, 2.0], [1.0, 0.0]])).total(binary_preds(p, y).pairs) > 0


TABLE_ERRORS = {
    "a key that is not an option": (lambda: declared([Loss(losses={"a": {"z": 2}})]), "names 'z', which is not an answer"),
    "a right answer charged": (lambda: declared([Loss(losses={"a": {"a": 2}})]), "a right answer loses 0"),
    "a binary table keyed by an option": (lambda: Task(id="t", cases="x", state=lambda r: r, question=Boolean(instructions="?"),
                                                       label=lambda r: r, objective=Loss(losses={"yes": {"no": 2}})), "not an answer \\(true, false\\)"),
    "a negative cost": (lambda: Loss(default=-1), "0 or more"),
}


@pytest.mark.parametrize("name", TABLE_ERRORS)
def test_a_table_that_cannot_be_read_is_stopped_when_it_loads(name):
    make, message = TABLE_ERRORS[name]
    with pytest.raises(ConfigError, match=message):
        make()


# ---------- custom objectives ----------


@per_case(direction="min", sets="threshold")
def wake_cost(label: bool, reading: Reading | None, *, miss: float = 5.0) -> float:
    if reading is None or (label and not reading.value):
        return miss
    return 1.0 if reading.value and not label else 0.0


@on_set(direction="max")
def caught(labels: list, readings: list, *, at_least: float = 0.5) -> float | None:
    positives = [r for y, r in zip(labels, readings) if y]
    return sum(1 for r in positives if r is not None and r.p_positive >= at_least) / len(positives) if positives else None


def own_task(tmp_path, objective, **kw):
    p = make_project(tmp_path, {"good": Sharp, "vague": Sharp})
    if not (tmp_path / "data.jsonl").exists():
        rows = [{"id": str(i), "y": i % 2 == 0} for i in range(60)]
        (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"y": r["y"]}, question=Boolean(instructions="?"),
                       label=lambda r: r["y"], objective=objective, **kw), p)


def test_a_custom_objective_is_declared_by_its_function_and_params():
    own = wake_cost(miss=20)
    o = own.objective
    assert o.name == "wake_cost" and o.params == {"miss": 20.0} and o.direction == "min" and o.sets == "threshold"
    assert o.code_sha256 and len(o.code_sha256) == 64 and wake_cost().objective.params == {"miss": 5.0}  # defaults kept too
    y = np.array([True, True, False, False])
    p = binary_preds(np.array([0.9, 0.2, 0.7, 0.1]), y).pairs  # right, missed, false alarm, right
    t = Task(id="t", cases="x", state=lambda r: r, question=Boolean(instructions="?"), label=lambda r: r, objective=own, tiebreak=[caught()])
    assert bound(t.primary, t.kind, t.custom_measures).value(p) == pytest.approx((0 + 20 + 1 + 0) / 4)
    assert bound(t.objectives[1], t.kind, t.custom_measures).value(p) == 0.5
    with pytest.raises(ConfigError, match="task.py defines no such function"):
        bound(t.primary, t.kind)  # the declaration alone cannot be measured
    again = t.copy(objective=t.primary, tiebreak=t.objectives[1:])  # resolved ones passed back keep their functions
    assert again.objectives == t.objectives and bound(again.primary, again.kind, again.custom_measures).value(p) == pytest.approx(5.25)


def test_a_custom_objective_goes_through_adopt_and_check(tmp_path):
    t = own_task(tmp_path, wake_cost(miss=3))
    for name in ("good", "vague"):
        asyncio.run(running.run_model(t, name, limit=None, variant="base"))
    listed = adopt.shortlist(t)
    r = adopt.adopt(t, listed.fits[0].candidate, "you", "fewest costly misses", listed=listed, force=True)
    o = r.evidence.evaluation.objective
    assert o is not None and o.objective == wake_cost(miss=3).objective and o.objective.code_sha256 == wake_cost().objective.code_sha256
    assert r.spec.rule.threshold is not None  # it set the threshold, as it declares
    first = check.check(t)
    assert first.verdict in ("pass", "better", "no_difference") and not any("changed after" in n for n in first.notes)
    edited = _define("def wake_cost(label, reading, *, miss: float = 5.0) -> float:\n"  # the same objective, its code edited
                     "    return 0.0 if reading is not None and reading.value == label else miss + 1", direction="min", sets="threshold")
    again = check.check(own_task(tmp_path, edited(miss=3)))
    assert any(f"wake_cost changed after toy@v{r.spec.version}" in n for n in again.notes)
    with pytest.raises(ConfigError, match="wake_cost, a function of task.py's that is gone"):
        check.check(own_task(tmp_path, Accuracy()))


OWN_ERRORS = {
    "no direction": (lambda: per_case()(lambda label, reading: 0.0), "needs direction="),
    "a field a rule does not have": (lambda: per_case(direction="max", sets="none")(lambda label, reading: 0.0), "sets= min_probability or threshold"),
    "one positional argument": (lambda: per_case(direction="max")(lambda label: 0.0), "takes two arguments"),
    "a param without a default": (lambda: _define("def f(label, reading, *, w: float) -> float: return w"), "takes two arguments"),
    "a param without a type": (lambda: _define("def f(label, reading, *, w=1.0): return w"), "param w needs a type annotation"),
    "a default that is not JSON": (lambda: _define("def f(label, reading, *, w: object = object()) -> float: return 0.0"), "is not JSON"),
    "a built-in's name": (lambda: _define("def accuracy(label, reading, *, w: float = 1.0) -> float: return 0.0"), "built-in's name"),
    "an unknown param": (lambda: wake_cost(mis=3), "no param mis"),
    "a declaration with a hash but no function": (lambda: declared([Objective(name="mine", direction="max", sets=None, unit="number", label="m",
                                                                              code_sha256="0" * 64)]), "carries a code hash but no function"),
}


def _define(src: str, direction: str = "max", sets: str | None = None):
    import linecache

    name = f"<own-{abs(hash(src))}>"
    linecache.cache[name] = (len(src), None, [src + "\n"], name)  # so inspect.getsource can read it, as from a task.py
    scope: dict = {}
    exec(compile(src, name, "exec"), scope)
    fn = next(v for k, v in scope.items() if callable(v) and not k.startswith("__"))
    return per_case(direction=direction, sets=sets)(fn)


@pytest.mark.parametrize("name", OWN_ERRORS)
def test_a_custom_objective_that_cannot_be_measured_is_stopped_when_it_loads(name):
    make, message = OWN_ERRORS[name]
    with pytest.raises(ConfigError, match=message):
        make()


# ---------- do the weights make the choice ----------


def two_kinds_of_error():
    """a never misses but raises 40 false alarms; b raises none but misses 40: equal at fn = fp."""
    y = np.array([True] * 100 + [False] * 100)
    a = np.where(y, 0.9, np.r_[[0.9] * 40, [0.1] * 60][np.arange(200) % 100])
    b = np.where(y, np.r_[[0.1] * 40, [0.9] * 60][np.arange(200) % 100], 0.1)
    return y, {"a": binary_preds(a, y), "b": binary_preds(b, y)}


def test_halving_and_doubling_the_weights_shows_they_make_the_choice(tmp_path):
    y, preds = two_kinds_of_error()
    for name, pr in preds.items():
        pr.model = name
    t = labelled(task([ExpectedLoss(fn=1, fp=1)]), y, tmp_path)
    moved = sensitivity(t, preds)
    assert [(r.factor, r.objective.params["fn"], r.tied) for r in moved] == [(0.5, 0.5, ["a", "b"]), (2.0, 2.0, ["a"])]
    assert decides(["a", "b"], moved) and not decides(["a", "b"], moved[:1])
    evs = [metrics.evaluate(t, pr) for pr in preds.values()]
    text = "\n".join(report.weights_table(t, *report.compared(t, evs), preds))
    assert "## With other weights" in text and "The candidates tied at the top change" in text and "halved: loss per case (miss 0.5, false alarm 1)" in text
    unweighted = task([Coverage()])
    assert sensitivity(labelled(task([Accuracy()]), y, tmp_path), preds) == [] and report.weights_table(unweighted, *report.compared(unweighted, evs), preds) == []
    table = sensitivity(labelled(task([Loss(losses={"true": {"false": 1}, "false": {"true": 1}})]), y, tmp_path), preds)
    assert [r.objective.params["losses"] for r in table] == [{"true": {"false": 0.5}, "false": {"true": 0.5}}, {"true": {"false": 2.0}, "false": {"true": 2.0}}]


def test_a_kind_that_takes_no_table_says_so():
    with pytest.raises(ConfigError, match="loss does not apply to a box question"):
        Task(id="t", cases="x", state=lambda r: r, question=Box(instructions="?"), label=lambda r: r, objective=Loss())
