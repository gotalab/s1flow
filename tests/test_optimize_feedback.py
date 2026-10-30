"""optimize (with GEPA stubbed) and feedback from production logs (no network)."""

import asyncio
import json

import pytest
from conftest import attach, make_project

from s1flow.eval.candidate import Candidate
from s1flow.objectives import Coverage, Recall
from s1flow.policies import DecisionPolicy, DecisionRule, PolicySpec
from s1flow.eval.policy import EvaluatedPolicy, Evidence, Selection
from s1flow.policies.file import asked
from s1flow.client.identity import state_digest
from s1flow.policies.state_shape import schema_of
from s1flow.client import Capabilities, Choice, ChoiceAnswer, Response, ModelBuild
from s1flow.eval import Task, evalset, feedback, metrics
from s1flow.eval.evaluation import Evaluation, Failures, ObjectiveScore
from s1flow.eval import optimize as optimizing
from s1flow.core.errors import ProviderError, Unsupported
from s1flow.eval import adopt as adopting
from s1flow.eval import report
from s1flow.eval import run as running
from s1flow.eval.task import Optimized
from s1flow.policies.kinds import KindParams

CLASSES = ["a", "b", "c"]


def q(text: str) -> Choice:
    return Choice(instructions=text, criteria={c: None for c in CLASSES})


class ByQuestion:
    """Sure and right on `Better?`, sure and wrong on `Worse?`; otherwise fairly sure and right on a and b, unsure and wrong on c."""

    def __init__(self, b: ModelBuild | None = None):
        self.id, self.capabilities, self.concurrency = "byq", Capabilities(), 4

    async def decide(self, state, questions, *, options=None):
        k, question = next(iter(questions.items()))
        truth = state["text"]
        sure = question.instructions in ("Better?", "Worse?")
        wrong = question.instructions == "Worse?" or (not sure and truth == "c")
        pick = CLASSES[(CLASSES.index(truth) + 1) % 3] if wrong else truth
        top = 0.97 if sure else 0.6 if wrong else 0.8
        return Response(answers={k: ChoiceAnswer(choice=pick, probabilities={c: top if c == pick else (1 - top) / 2 for c in CLASSES})}, answered_by="byq-1")


@pytest.fixture
def task(tmp_path, no_ci):
    p = make_project(tmp_path, {"m": ByQuestion})
    rows = [{"id": str(i), "text": CLASSES[i % 3]} for i in range(120)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"text": r["text"]}, question=q("Which?"),
                    label=lambda r: r["text"], objective=Coverage(target_accuracy=0.9)), p)


def current(task: Task) -> EvaluatedPolicy:
    asyncio.run(running.run_model(task, "m", limit=None, variant="base"))
    e = metrics.evaluate(task, metrics.load(task, "base", "m", include_test=True), include_test=True)
    spec = PolicySpec(task="toy", version=1, connection="m", model_id="m", questions={"q": asked(task.question, DecisionRule(min_probability=0.9))}, state_schema=schema_of([{"text": "a"}]))
    runtime = DecisionPolicy(spec, client=task.where.client())
    r = EvaluatedPolicy(
        spec=spec, candidate=Candidate(model="m"), answered_by="byq-1",
        selection=Selection(by="t", reason="t", tied=["m"]),
        evidence=Evidence(data_sha256=task.data_digest, execution_digest=runtime.execution_digest,
                          input_adapter_digest=task.input_adapter_digest, evaluation_contract_digest=task.evaluation_contract_digest, evaluation=e, test=None, compared=["m"]),
    )
    task.policies.write_new(r, current=True)
    return r



def stub_optimize(monkeypatch, task: Task, text: str) -> None:
    def optimize(t, model, *, budget, reflection, start, name, **kw):
        sf, _ = evalset.ensure(t)  # as gepa.optimize does: train and val from the fixed split
        art = Optimized(
            variant=name, model=model, method="gepa", at="2026-10-16T00:00:00Z", question=q(text), seed_question=task.question, start=start,
            split={r: sf.ids(r) for r in ("train", "val", "test")}, seed=1, budget=budget, reflection_lm=reflection or "r", reflection_calls=1,
            reflection_cost_usd=0.01, model_calls=budget, candidates=2, val_scores=[0.5, 0.9], best_index=1,
        )
        task.optimized[name], task.variants[name] = art, q(text)
        return art

    monkeypatch.setattr(optimizing.gepa, "optimize", optimize)


def test_a_better_question_becomes_the_candidate(task, monkeypatch):
    current(task)
    stub_optimize(monkeypatch, task, "Better?")
    r = optimizing.optimize(task, 50)
    assert r.verdict == "adopted" and r.policy == "toy@v2" and r.check and r.check.verdict == "better"
    store = task.policies
    assert store.current("toy") == 2 and store.read("toy", version=2).candidate.variant == r.variant  # the pull request ships it


def test_a_question_that_does_not_win_writes_nothing(task, monkeypatch):
    current(task)
    stub_optimize(monkeypatch, task, "Worse?")
    r = optimizing.optimize(task, 50)
    assert r.verdict == "no_gain" and task.policies.versions("toy") == [1]


def test_rank_leaves_out_a_candidate_that_skipped_cases(task):
    current(task)
    task.variants["v"] = q("Better?")
    asyncio.run(running.run_model(task, "m", limit=60, variant="v"))
    with pytest.warns(UserWarning, match="never asked"):
        listed = adopting.shortlist(task)
    assert listed.recommended == "m" and [c[0] for c in listed.cands] == ["m"]


class FailsOnC(ByQuestion):
    """ByQuestion whose calls fail on the cases it gets wrong: scored on the rest alone, it would look perfect."""

    def __init__(self, b=None):
        super().__init__(b)
        self.id = "flaky"  # its own answer cache

    async def decide(self, state, questions, *, options=None):
        if state["text"] == "c":
            raise ProviderError("ConnectError: All connection attempts failed")
        return await super().decide(state, questions, options=options)


class RefusesC(ByQuestion):
    def __init__(self, b=None):
        super().__init__(b)
        self.id = "picky"

    async def decide(self, state, questions, *, options=None):
        if state["text"] == "c":
            raise Unsupported("not this input")
        return await super().decide(state, questions, options=options)


def test_rank_leaves_out_a_candidate_whose_calls_failed_on_some_cases(tmp_path, no_ci):
    p = make_project(tmp_path, {"m": ByQuestion, "flaky": FailsOnC, "picky": RefusesC})
    rows = [{"id": str(i), "text": CLASSES[i % 3]} for i in range(120)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"text": r["text"]}, question=q("Which?"),
                       label=lambda r: r["text"], objective=Coverage(target_accuracy=0.9)), p)
    asyncio.run(running.run(task, ["m", "flaky", "picky"]))
    with pytest.warns(UserWarning, match=r"flaky \(28 cases whose every call failed\); ask them again: s1flow run toy --models flaky"):
        listed = adopting.shortlist(task)
    assert [c[0] for c in listed.cands] == ["m", "picky"]  # a refusal is the model's limit: it stays, scored on what it answered
    rows_ = {r.candidate: r for r in listed.rows()}
    assert (rows_["m"].n, rows_["m"].refused) == (84, 0) and (rows_["picky"].n, rows_["picky"].refused) == (56, 28)
    md = report.write(task, "base", task.where.root / "out")
    assert "flaky ✕ | 56 |" in md and "Not compared: flaky (28 cases whose every call failed)" in md and "`s1flow run toy --models flaky`" in md
    assert "**flaky**" not in md.split("## Comparison")[0]  # not the report's pick either


# ---------- feedback ----------


def production_policy(task):
    spec = PolicySpec(task="toy", version=1, connection="m", model_id="m",
                      questions={"q": asked(task.question, DecisionRule(threshold=0.5) if task.kind.binary else DecisionRule(min_probability=0.9), task.kind_params)})
    runtime = DecisionPolicy(spec, client=task.where.client())
    e = Evaluation(candidate=Candidate(model="m"), answered_by="byq-1", answered_by_all=["byq-1"], n=120, probabilities=True,
                   failures=Failures(calls=120, failed=0, unsupported=0, data_errors=0, unlabeled=0),
                   objective=ObjectiveScore(objective=task.primary, value=0.8, interval=(0.7, 0.9)))
    r = EvaluatedPolicy(spec=spec, candidate=Candidate(model="m"), answered_by="byq-1",
                        selection=Selection(by="t", reason="t", tied=["m"]),
                        evidence=Evidence(data_sha256=task.data_digest, execution_digest=runtime.execution_digest,
                                          evaluation=e, test=None, compared=["m"]))
    task.policies.write_new(r)
    return r


def logs(tmp_path, task, with_feedback=range(10)):
    adopted = production_policy(task)
    lines = []
    for i in range(10):
        lines.append({"type": "answered", "at": f"2026-10-16T00:00:0{i}", "case_id": f"c{i}", "state_sha256": state_digest({"text": "a"}), "state": {"text": "a"} if i < 8 else None,
                      "decision": {"decision_id": f"d{i}", "policy_digest": adopted.spec.digest, "execution_digest": adopted.evidence.execution_digest, "value": "a" if i != 1 else "b", "probability": 0.9 if i < 8 else 0.5, "below_min_probability": i >= 8, "policy": "toy@v1", "answered_by": "byq-1", "latency_ms": 1.0}})
        if i in with_feedback:
            lines.append({"type": "feedback", "at": f"2026-10-16T01:00:0{i}", "decision_id": f"d{i}", "policy_digest": adopted.spec.digest, "policy": "toy@v1", "label": "a" if i != 9 else "zzz"})
    lines.append({"type": "failed", "at": "2026-10-16T00:00:10", "case_id": "c10", "state_sha256": "x", "policy_digest": adopted.spec.digest, "policy": "toy@v1", "error": "ProviderError: 503"})
    lines.append({"type": "answered", "at": "2026-10-16T00:00:00", "case_id": "c0", "state_sha256": "x",
                          "decision": {"decision_id": "other-d0", "policy_digest": "other", "execution_digest": "other", "value": "b", "probability": 0.9, "below_min_probability": False, "policy": "other@v1", "answered_by": "byq-1", "latency_ms": 1.0}})
    p = tmp_path / "log.jsonl"
    p.write_text("".join(json.dumps(x) + "\n" for x in lines))
    return p


def test_production_accuracy_comes_from_the_feedback(task, tmp_path):
    found = feedback.read([logs(tmp_path, task)])
    prod = feedback.production(task, feedback.cases(task, found), found.failed)[0]
    assert (prod.answered, prod.failed, prod.with_feedback, prod.correct, prod.sure_n) == (10, 1, 9, 8, 8)  # c9's label is not an option
    assert prod.accuracy.interval and prod.below is False  # 7 of 8 sure ones right: too few to show it below 90%


def test_scarce_feedback_gives_no_interval(task, tmp_path):
    found = feedback.read([logs(tmp_path, task, with_feedback=(1, 2))])  # 2 of 10: maybe only corrections
    prod = feedback.production(task, feedback.cases(task, found), found.failed)[0]
    assert prod.feedback_share == 0.2 and prod.accuracy.value == 0.5 and prod.accuracy.interval is None and prod.below is None


def test_answered_cases_become_labelled_cases(task, tmp_path):
    evalset.ensure(task)
    cs = feedback.cases(task, feedback.read([logs(tmp_path, task)]))
    out = feedback.add(task, cs)
    assert (out.added, out.no_state, out.no_label, out.invalid_label, out.already) == (8, 1, 0, 1, 0)
    assert "keep the state in the log: `s1flow decide --log FILE --keep-state`, the decide Action's `keep-state: true`" in feedback.markdown(task, [], out)
    by = task.load_cases().by_id()
    assert by["prod:d0"].state == {"text": "a"} and by["prod:d1"].label == "a" and by["prod:d1"].source == "feedback" and by["0"].label == "a"
    assert "prod:d0" in evalset.read(task).assign
    assert feedback.add(task, cs).already == 8


def test_an_otlp_export_reads_like_the_jsonl(task, tmp_path):
    def attrs(d):
        return [{"key": k, "value": {"boolValue": v} if isinstance(v, bool) else {"doubleValue": v} if isinstance(v, float) else {"stringValue": v}} for k, v in d.items()]

    adopted = production_policy(task)
    spans = [
        {"name": "s1flow.decide", "startTimeUnixNano": "1760572800000000000",
         "attributes": attrs({"s1flow.policy": "toy@v1", "s1flow.decision_id": "d0", "s1flow.policy_digest": adopted.spec.digest, "s1flow.execution_digest": adopted.evidence.execution_digest, "s1flow.case_id": "c0", "s1flow.below_min_probability": False, "s1flow.probability": 0.9, "s1flow.answer": '"a"',
                                   "gen_ai.response.model": "byq-1", "s1flow.latency_ms": 1.0, "s1flow.state_sha256": "x"})},
        {"name": "s1flow.feedback", "startTimeUnixNano": "1760572900000000000", "attributes": attrs({"s1flow.policy": "toy@v1", "s1flow.decision_id": "d0", "s1flow.policy_digest": adopted.spec.digest, "s1flow.execution_digest": adopted.evidence.execution_digest, "s1flow.case_id": "c0", "s1flow.label": '"a"'})},
    ]
    p = tmp_path / "otlp.jsonl"
    p.write_text(json.dumps({"resourceSpans": [{"scopeSpans": [{"spans": spans}]}]}) + "\n")
    found = feedback.read([p])
    cs = feedback.cases(task, found)
    assert len(cs) == 1 and cs[0].label == "a" and cs[0].state is None
    assert feedback.production(task, cs, found.failed)[0].correct == 1


def test_production_measures_the_primarys_own_constraint(task, tmp_path):
    """Each logged Decision is a reading: a Recall policy is judged in production by its false alarms."""
    t = attach(Task(id="toy", cases="data.jsonl", dir=task.dir, state=lambda r: {"text": r["text"]}, question=q("Which?"), kind_params=KindParams(positive="a"),
                    label=lambda r: r["text"] == "a", objective=Recall(max_false_alarm=0.1)), task.where)
    adopted = production_policy(t)
    lines = []
    for i in range(40):
        label, said = (True, True) if i < 20 else (False, i < 32)  # 12 of the 20 negatives raised an alarm
        lines.append({"type": "answered", "at": "2026-10-16T00:00:00", "case_id": f"c{i}", "state_sha256": "x",
                      "decision": {"decision_id": f"d{i}", "policy_digest": adopted.spec.digest, "execution_digest": adopted.evidence.execution_digest, "value": said, "probability": 0.9, "p_positive": 0.9 if said else 0.1, "below_min_probability": False, "policy": "toy@v1",
                                  "answered_by": "byq-1", "latency_ms": 1.0}})
        lines.append({"type": "feedback", "at": "2026-10-16T01:00:00", "decision_id": f"d{i}", "policy_digest": adopted.spec.digest, "policy": "toy@v1", "label": label})
    (tmp_path / "recall.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))
    found = feedback.read([tmp_path / "recall.jsonl"])
    prod = feedback.production(t, feedback.cases(t, found), found.failed)[0]
    assert prod.correct == 28 and prod.below is True
    md = feedback.markdown(t, [prod], feedback.Added(added=0, no_state=0, no_label=0, invalid_label=0, already=0))
    assert "(its lower bound is over the cap)" in md


def test_a_log_line_in_an_older_shape_names_its_file_and_line(tmp_path):
    from s1flow.core.errors import DataError
    from s1flow.eval import feedback

    log = tmp_path / "log.jsonl"
    log.write_text('{"type": "answered", "policy": "t@1", "observed_at": "2026-10-20T00:00:00+00:00"}\n')
    with pytest.raises(DataError, match=r"log.jsonl:1: invalid log record"):
        feedback.read([log])
