"""Values read from the state and estimates in the evaluation: labels, what is right, what the hand-off rule
reads, their measures, end to end (no network)."""

import asyncio
import datetime as dt
import json

import pytest

from conftest import attach, make_project

from s1flow.client import Capabilities, DateAnswer, EstimateAnswer, MultiChoiceAnswer, NumberAnswer, Response, TextAnswer
from s1flow.core.errors import ConfigError, DataError, ProviderError, Unsupported
from s1flow.eval import Task, comparison, data, metrics, report, review
from s1flow.eval import run as running
from s1flow.eval.kinds import kind_of
from s1flow.eval.objectives import measure
from s1flow.objectives import Accuracy, Coverage, MAE, MeanError, OptionF1
from s1flow.policies import DecisionRule
from s1flow.policies.kinds import ABSENT, KindParams, same_label
from s1flow.questions import Boolean, Date, MultiChoice, Number, RangeEstimate, Text

TEXT, NUMBER, DATE = Text(instructions="The order number"), Number(instructions="The total"), Date(instructions="The day it shipped")
DAYS = RangeEstimate(instructions="Days until it is paid", min=0, max=120, step=1)
PLAIN = DecisionRule()


def test_each_field_question_has_its_kind():
    t, n, d, e = kind_of(TEXT), kind_of(NUMBER), kind_of(DATE), kind_of(DAYS)
    assert [k.type for k in (t, n, d, e)] == ["text", "number", "date", "estimate"]
    assert not any(k.binary for k in (t, n, d, e)) and all(k.sets == {"min_probability"} for k in (t, n, d, e))
    assert t.objectives == n.objectives == d.objectives == ("accuracy", "coverage", "auroc")
    assert t.report == ("value_accuracy", "absent_accuracy")
    assert e.objectives == ("mean_error", "accuracy", "coverage", "auroc") and e.report == ("mean_error",)
    assert (e.low, e.high, e.tolerance) == (0, 120, 0.5)  # half a step
    assert kind_of(RangeEstimate(instructions="?", min=0, max=50)).tolerance == 0.5  # no step: a hundredth of the range
    assert kind_of(DAYS, KindParams(tolerance=3)).tolerance == 3
    with pytest.raises(ValueError, match="tolerance is how far off an estimate is still right; this one is number"):
        kind_of(NUMBER, KindParams(tolerance=1))
    with pytest.raises(ValueError, match="iou is a box question's bar"):
        kind_of(TEXT, KindParams(iou=0.5))


def test_a_label_is_the_value_or_absent():
    t, n, d, e = kind_of(TEXT), kind_of(NUMBER), kind_of(DATE), kind_of(DAYS)
    for kind in (t, n, d):
        assert kind.label_error(ABSENT) is None and kind.as_label(ABSENT) is ABSENT
    assert t.label_error("A-4417") is None and t.as_label("  A-4417\n rev 2 ") == "A-4417 rev 2"
    assert t.label_error("") == "a text label is the text as the state writes it, or False when the state holds none; got ''"
    assert t.label_error(4417) is not None and t.label_error(True) is not None
    assert n.label_error(12) is None and n.as_label(12) == 12.0 and n.label_error("12") is not None
    assert n.label_error(True) == "a number label is a number, or False when the state holds none; got True"
    assert d.label_error("2026-03-05") is None and d.as_label(dt.date(2026, 3, 5)) == "2026-03-05"
    assert d.label_error("March 5") == "a date label is a day as YYYY-MM-DD, or False when the state holds none; got 'March 5'"
    assert e.label_error(30) is None and e.label_error(30.5) is None
    assert e.label_error(121) == "an estimate's label is a number in 0..120, got 121"
    assert e.label_error(ABSENT) is not None  # an estimate is never absent


@pytest.mark.parametrize(("answer", "value", "probability", "distributed"), [
    (TextAnswer(value="A-4417", p_null=0.1, confidence=0.9), "A-4417", 0.81, True),  # P(there) x confidence in it
    (TextAnswer(value="A-4417", confidence=0.9), "A-4417", 0.9, True),  # Perplexity, ScaleDown
    (TextAnswer(value=" A-4417 "), "A-4417", 1.0, False),  # Schematron: the value alone
    (TextAnswer(value=None, guess="INV-1", p_null=0.97, confidence=0.99), None, 0.97, True),  # Clairic: sure of a guess it did not give
    (TextAnswer(value=None), None, 1.0, False),
    (TextAnswer(value="  ", confidence=0.9), None, 0.9, True),  # an empty text is nothing read
])
def test_a_value_is_read_with_the_probability_its_model_gives(answer, value, probability, distributed):
    kind = kind_of(TEXT)
    avg = kind.average([answer])
    r = kind.reading(avg, DecisionRule(min_probability=0.95))
    assert (r.value, avg.distributed) == (value, distributed) and r.probability == pytest.approx(probability)
    assert r.below_min_probability is (probability < 0.95)


def test_right_is_the_same_value_or_nothing_on_an_absent_case():
    t, n, d = kind_of(TEXT), kind_of(NUMBER), kind_of(DATE)
    read = lambda kind, a: kind.read([a], PLAIN)
    assert t.correct("A-4417", read(t, TextAnswer(value="A-4417 "))) and not t.correct("A-4417", read(t, TextAnswer(value="a-4417")))
    assert t.correct(ABSENT, read(t, TextAnswer(value=None))) and not t.correct(ABSENT, read(t, TextAnswer(value="A-4417")))
    assert not t.correct("A-4417", read(t, TextAnswer(value=None))) and not t.correct("A-4417", None)
    assert n.correct(1080.0, read(n, NumberAnswer(value=1080))) and n.correct(0.3, read(n, NumberAnswer(value=0.1 + 0.2)))
    assert not n.correct(1080.0, read(n, NumberAnswer(value=1080.5))) and not n.correct(0.0, read(n, NumberAnswer(value=None)))
    assert n.correct(0.0, read(n, NumberAnswer(value=0)))  # zero is a value, not absent
    assert d.correct("2026-03-05", read(d, DateAnswer(value="2026-03-05"))) and not d.correct("2026-03-05", read(d, DateAnswer(value="2026-03-06")))
    with pytest.raises(ProviderError, match="answered a text question as number"):
        read(t, NumberAnswer(value=1))


def test_an_estimate_is_right_within_its_tolerance_and_sure_when_its_interval_is_narrow():
    kind = kind_of(DAYS, KindParams(tolerance=2))
    narrow = kind.read([EstimateAnswer(value=30, p10=27, p90=33)], DecisionRule(min_probability=0.9))
    wide = kind.read([EstimateAnswer(value=30, p10=0, p90=120)], DecisionRule(min_probability=0.9))
    bare = kind.average([EstimateAnswer(value=30)])
    assert (narrow.value, narrow.expected, narrow.probability) == (30.0, 30.0, None) and narrow.confidence == pytest.approx(0.95)
    assert narrow.below_min_probability is False and wide.confidence == 0.0 and wide.below_min_probability is True
    assert (bare.confidence, bare.distributed) == (1.0, False)
    assert kind.correct(32.0, narrow) and kind.correct(28.0, narrow) and not kind.correct(32.5, narrow) and not kind.correct(30.0, None)
    with pytest.raises(ProviderError, match="estimate 130.0 is outside 0..120"):
        kind.read([EstimateAnswer(value=130)], PLAIN)


def test_the_measures_of_a_value_read():
    kind = kind_of(TEXT)
    answers = [TextAnswer(value="a", confidence=0.9), TextAnswer(value="x", confidence=0.6), TextAnswer(value=None, p_null=0.8),
               TextAnswer(value="d", p_null=0.3, confidence=1.0), None]
    labels = ["a", "b", ABSENT, ABSENT, "e"]  # right, wrong, right (absent), wrong (read on an absent case), no answer
    p = measure.pairs(kind, labels, [None if a is None else kind.read([a], PLAIN) for a in answers])
    assert list(p.correct) == [True, False, True, False, False]
    assert list(p.probability) == pytest.approx([0.9, 0.6, 0.8, 0.7, 0.0])
    assert measure.bound(Accuracy(), kind).value(p) == 0.4
    assert measure.measure("value_accuracy", p) == pytest.approx(1 / 3) and measure.measure("absent_accuracy", p) == 0.5
    assert measure.measure("auroc", p) == 1.0  # every right one (0.9, 0.8) is surer than every wrong one (0.6, 0.7)
    assert measure.measure("brier", p) == pytest.approx((0.01 + 0.36 + 0.04 + 0.49 + 0) / 5)
    assert [measure.shown(p, i) for i in (0, 2, 3)] == [("a", "a"), ("absent", "absent"), ("absent", "d")]
    sure = p.at(min_probability=0.75)
    assert list(sure.sure) == [True, False, True, False, False] and measure.bound(Coverage(target_accuracy=0.95), kind).value(sure) == 0.4
    none_absent = measure.pairs(kind, ["a"], [kind.read([answers[0]], PLAIN)])
    assert measure.measure("absent_accuracy", none_absent) is None


def test_the_mean_error_of_an_estimate():
    kind = kind_of(DAYS)
    readings = [kind.read([EstimateAnswer(value=v, p10=v - 2, p90=v + 2)], PLAIN) for v in (30, 44)] + [None]
    p = measure.pairs(kind, [30, 40, 100], readings)
    assert list(p.correct) == [True, False, False]
    assert measure.measure("mean_error", p) == pytest.approx((0 + 4 + 100) / 3)  # a failed call: as far as 100 can be in 0..120
    assert measure.bound(MeanError(), kind).value(p) == measure.measure("mean_error", p)


def test_objectives_are_declared_for_the_kinds_that_take_them():
    task = lambda q, **kw: Task(id="t", cases="d.jsonl", state=lambda r: r["t"], question=q, label=lambda r: r["y"], **kw)
    assert task(DAYS).primary == MeanError() and task(TEXT).primary == Accuracy()
    assert task(TEXT, objective=Coverage(target_accuracy=0.99)).primary.name == "coverage"
    with pytest.raises(ConfigError, match="mean_error does not apply to a number question; a number takes accuracy, coverage, auroc"):
        task(NUMBER, objective=MeanError())
    with pytest.raises(ConfigError, match="mae does not apply to a estimate question"):
        task(DAYS, objective=MAE())
    with pytest.raises(ConfigError, match="tolerance is how far off an estimate is still right"):
        task(Boolean(instructions="?"), kind_params=KindParams(tolerance=1))


class Reader:
    """Reads the order number the state gives, sure; on every fifth case it reads one where there is none, unsure."""

    id, model_id, concurrency = "fake:reader", "fake-reader", 4
    capabilities = Capabilities(question_types={"text", "estimate"})

    def __init__(self, b=None):
        pass

    async def decide(self, state, questions, *, options=None):
        n, order, boxes = state.split()
        out = {}
        for qid, q in questions.items():
            if q.type == "text":
                made_up = order == "-" and int(n) % 5 == 0
                there = order != "-" or made_up
                out[qid] = TextAnswer(value=(f"X-{n}" if made_up else order) if there else None, guess=order, p_null=0.4 if made_up else 0.02 if there else 0.98,
                                      confidence=0.99)
            else:
                off = int(n) % 4 == 0
                out[qid] = EstimateAnswer(value=int(boxes) + (3 if off else 0), p10=int(boxes) - (20 if off else 1), p90=int(boxes) + (20 if off else 1))
        return Response(answers=out, answered_by=self.model_id)


def _project(tmp_path):
    p = make_project(tmp_path, {"reader": Reader})
    rows = [{"id": str(i), "n": i, "order": f"A-{i}" if i % 3 else None, "boxes": 5 + i % 40} for i in range(90)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p, lambda r: f"{r['n']} {r['order'] or '-'} {r['boxes']}"


def test_a_text_task_runs_reports_and_compares(tmp_path):
    p, state = _project(tmp_path)
    task = attach(Task(id="text-test", cases="data.jsonl", dir=tmp_path, state=state, question_id="order_number", question=TEXT,
                       label=lambda r: r["order"] or ABSENT, objective=Coverage(target_accuracy=0.99)), p)
    asyncio.run(running.run_model(task, "reader", limit=None, variant="base"))
    pr = metrics.load(task, "base", "reader")  # a value that was not read comes back from the saved run
    assert pr.probabilities
    e = metrics.evaluate(task, pr)
    assert e.measures["value_accuracy"].value == 1.0 and 0.5 < e.measures["absent_accuracy"].value < 1.0
    assert e.selective[0].accuracy == 1.0 and 0.8 < e.selective[0].coverage.value < 1.0  # the made-up fifth of the absent cases is left out
    md = report.render(task, "base", [e], {"reader": pr})
    assert "with a value" in md and "with none)" in md and "Value read: right when it equals the label" in md
    assert "| accuracy (value there) |" in md
    c = comparison.collect(task)
    row = next(r for r in c.candidates if r.model == "reader")
    assert c.question_type == "text" and {"value_accuracy", "absent_accuracy", "brier", "ece"} <= set(row.metrics)
    assert row.adoption_blocked == []
    with pytest.raises(Unsupported, match="text tasks are not supported yet"):
        review.review(task)


def test_an_estimate_task_runs_reports_and_compares(tmp_path):
    p, state = _project(tmp_path)
    task = attach(Task(id="estimate-test", cases="data.jsonl", dir=tmp_path, state=state, question_id="boxes",
                       question=RangeEstimate(instructions="How many boxes", min=0, max=50, step=1), label=lambda r: r["boxes"],
                       tiebreak=[Accuracy()]), p)
    asyncio.run(running.run_model(task, "reader", limit=None, variant="base"))
    pr = metrics.load(task, "base", "reader")
    e = metrics.evaluate(task, pr)
    assert e.objective and e.objective.objective == MeanError() and e.objective.value == pytest.approx(0.75, abs=0.15)  # 3 off on a fourth
    assert e.selective[0].accuracy == 1.0  # the wide fourth is left out at the chosen min probability
    md = report.render(task, "base", [e], {"reader": pr})
    assert "(right within 0.5 of the label)" in md and "| mean error |" in md and "Estimate: right within 0.5 of the label" in md
    row = next(r for r in comparison.collect(task).candidates if r.model == "reader")
    assert row.value == e.objective.value and {"mean_error", "brier"} <= set(row.metrics)
    assert row.adoption_blocked == []


def test_a_task_whose_cases_all_have_no_value_is_measured_as_absent():
    kind = kind_of(TEXT)
    answers = [TextAnswer(value=None, p_null=0.9), TextAnswer(value="x", confidence=0.5), TextAnswer(value=None, p_null=0.7)]
    p = measure.pairs(kind, [ABSENT] * 3, [kind.read([a], PLAIN) for a in answers])
    assert measure.measure("value_accuracy", p) is None and measure.measure("absent_accuracy", p) == pytest.approx(2 / 3)
    assert measure.shown(p, 1) == ("absent", "x") and measure.written(p, p.y[0]) == "absent"


def test_an_empty_text_is_nothing_read_and_as_sure_as_p_null():
    r = kind_of(TEXT).read([TextAnswer(value=" ", p_null=0.1, confidence=0.9)], PLAIN)
    assert r.value is None and r.probability == pytest.approx(0.1)


def test_a_date_label_is_written_as_text():
    assert "YYYY-MM-DD" in kind_of(DATE).label_error(dt.date(2026, 9, 2))
    assert kind_of(DATE).label_error("2026-09-02") is None


def test_a_number_label_of_zero_is_not_the_absent_label(tmp_path):
    p, state = _project(tmp_path)
    (tmp_path / "data.jsonl").write_text("".join(json.dumps({"id": str(i), "n": i, "order": None, "boxes": 0}) + "\n" for i in range(30)))
    task = attach(Task(id="zero-test", cases="data.jsonl", dir=tmp_path, state=state, question_id="total", question=NUMBER,
                       label=lambda r: r["boxes"]), p)
    fix = review.correct(task, "3", "relabel", reason="no total is stated", by="tester", label=ABSENT)
    assert fix.was == 0 and fix.label is False


# ---------- multichoice: every option that applies ----------

TOPICS = MultiChoice(instructions="What does the customer complain about?", criteria={"late": "late", "damage": "damaged", "billing": "a wrong charge"})


def test_a_multichoice_label_is_the_list_of_options_that_apply():
    kind = kind_of(TOPICS)
    assert kind.type == "multichoice" and kind.objectives[0] == "accuracy"
    assert kind.label_error([]) is None and kind.label_error(["damage", "late"]) is None
    for bad in ("late", ["late", "late"], ["refund"], None, True):
        assert "list of the options that apply" in kind.label_error(bad)
    assert kind.as_label(["damage", "late"]) == ("late", "damage")  # in the question's order
    assert kind.as_label("damage, late") == ("late", "damage") and kind.as_label("none") == () and kind.as_label("late") == ("late",)  # typed on the CLI
    for bad in ("late,refund", ["late", "refund"], 3):  # never read with an unknown option dropped
        with pytest.raises(ValueError, match="list of the options that apply"):
            kind.as_label(bad)
    assert same_label(kind, ["damage", "late"], ("late", "damage")) and not same_label(kind, ["late"], ["late", "damage"])
    assert not same_label(kind_of(Number(instructions="How many?")), 0, ABSENT)  # 0 is a number, False no value
    with pytest.raises(ValueError, match="positive scores a choice question"):
        kind_of(TOPICS, KindParams(positive="late"))


def test_a_multichoice_is_read_option_by_option_and_is_as_sure_as_the_whole_set():
    kind = kind_of(TOPICS)
    r = kind.read([MultiChoiceAnswer(choices=["late"], probabilities={"late": 0.9, "damage": 0.2, "billing": 0.0})], DecisionRule(min_probability=0.8))
    assert r.value == ("late",) and r.probability == pytest.approx(0.9 * 0.8 * 1.0) and r.below_min_probability is True
    avg = kind.average([MultiChoiceAnswer(choices=["late", "billing"])])  # no probabilities: sure of everything, and said so
    assert avg.value == ("late", "billing") and avg.confidence == 1.0 and avg.distributed is False
    assert kind.read([MultiChoiceAnswer(choices=[], probabilities={"late": 0.1, "damage": 0.2, "billing": 0.3})], PLAIN).value == ()
    with pytest.raises(ProviderError, match="are not options"):
        kind.read([MultiChoiceAnswer(choices=["refund"])], PLAIN)


def test_the_measures_of_a_multichoice():
    kind = kind_of(TOPICS)
    given = [(["late"], 0.9), (["late", "damage"], 0.6), ([], 0.8), (["billing"], 0.7), None]
    labels = [["late"], ["late"], [], ["damage", "billing"], ["late"]]  # right, one too many, right (none), one missed, no answer
    readings = [None if g is None else kind.read([MultiChoiceAnswer(choices=g[0], probabilities={k: (g[1] if k in g[0] else 0.0) for k in kind.keys})], PLAIN)
                for g in given]
    p = measure.pairs(kind, labels, readings)
    assert list(p.correct) == [True, False, True, False, False]
    assert measure.bound(Accuracy(), kind).value(p) == 0.4
    # options chosen: late, late, damage, billing (4), of which the labels have 3; the labels have 5
    assert measure.measure("option_precision", p) == 0.75 and measure.measure("option_recall", p) == 0.6
    assert measure.measure("option_f1", p) == pytest.approx(2 * 3 / (4 + 5)) == measure.bound(OptionF1(), kind).value(p)
    assert measure.shown(p, 1) == ("late", "late, damage") and measure.shown(p, 2) == ("none", "none")


class Tagger:
    """A fake model: reads the tags from the state, misses the last tag of every fifth case with a low probability."""

    def __init__(self, spec):
        self.id, self.model_id, self.concurrency = "fake:tagger", "fake-tagger", 4
        self.capabilities = Capabilities(question_types=frozenset({"multichoice"}))

    async def decide(self, state, questions, *, options=None):
        n, tags = state.split("|")
        said = [t for t in tags.split(",") if t]
        unsure = int(n) % 5 == 0 and bool(said)
        chosen = said[:-1] if unsure else said
        qid, q = next(iter(questions.items()))
        probs = {k: (0.45 if unsure and k == said[-1] else 0.97 if k in chosen else 0.02) for k in q.criteria}
        return Response(answers={qid: MultiChoiceAnswer(choices=chosen, probabilities=probs)}, answered_by=self.model_id)


def test_a_multichoice_task_runs_reports_and_compares(tmp_path):
    p = make_project(tmp_path, {"tagger": Tagger})
    keys = list(TOPICS.criteria)
    rows = [{"id": str(i), "n": i, "tags": [k for j, k in enumerate(keys) if (i >> j) & 1]} for i in range(80)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(id="tags-test", cases="data.jsonl", dir=tmp_path, state=lambda r: f"{r['n']}|{','.join(r['tags'])}", question_id="complaints",
                       question=TOPICS, label=lambda r: r["tags"], objective=Coverage(target_accuracy=0.99), tiebreak=[OptionF1()]), p)
    asyncio.run(running.run_model(task, "tagger", limit=None, variant="base"))
    pr = metrics.load(task, "base", "tagger")
    e = metrics.evaluate(task, pr)
    assert e.probabilities and e.accuracy and 0.7 < e.accuracy.value < 0.95
    assert e.measures["option_precision"].value == 1.0 and 0.8 < e.measures["option_recall"].value < 1.0
    assert e.selective[0].accuracy == 1.0 and 0.6 < e.selective[0].coverage.value < 0.95  # the unsure fifth is left out
    md = report.render(task, "base", [e], {"tagger": pr})
    assert "| option F1 |" in md and "Multichoice: every option the model gives 0.5 or more" in md and "late 28" in md
    c = comparison.collect(task)
    row = next(r for r in c.candidates if r.model == "tagger")
    assert c.question_type == "multichoice" and {"option_f1", "option_precision", "option_recall", "brier"} <= set(row.metrics)
    assert row.adoption_blocked == []
    with pytest.raises(Unsupported, match="multichoice tasks are not supported yet"):
        review.review(task)
    assert not [w for w in data.check(task).warnings if "same state" in w]
    fix = review.correct(task, "1", "relabel", reason="also damaged", by="tester", label=["damage", "late"])
    assert fix.was == ["late"] and fix.label == ["damage", "late"]
    with pytest.raises(DataError, match="already"):
        review.correct(task, "3", "relabel", reason="same set", by="tester", label=["damage", "late"])


def test_a_multichoice_label_the_task_cannot_hold_stops_the_measurement(tmp_path):
    p = make_project(tmp_path, {"tagger": Tagger})
    write = lambda bad: (tmp_path / "data.jsonl").write_text("".join(  # noqa: E731
        json.dumps({"id": str(i), "n": i, "tags": ["late", "refund"] if bad and not i else ["late"]}) + "\n" for i in range(6)))
    write(False)
    task = attach(Task(id="tags-bad", cases="data.jsonl", dir=tmp_path, state=lambda r: f"{r['n']}|late", question_id="complaints",
                       question=TOPICS, label=lambda r: r["tags"]), p)
    asyncio.run(running.run_model(task, "tagger", limit=None, variant="base"))
    write(True)  # case 0 is relabelled with an option the question lacks, after its answers were saved
    task.load_cases().forget()
    assert any(e.startswith("0: a multichoice label") for e in data.check(task).errors)
    with pytest.raises(DataError, match="cannot score"):
        asyncio.run(running.run_model(task, "tagger", limit=None, variant="base"))
    with pytest.raises(DataError, match="^0: a multichoice label .* `s1flow cases check`"):
        metrics.load(task, "base", "tagger")
