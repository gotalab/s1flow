"""Production feedback never joins a label to a newer call just because its case ID repeats."""

from conftest import attach, make_project

from s1flow.client import Boolean
from s1flow.client.identity import state_digest
from s1flow.eval import Task, feedback
from s1flow.eval.candidate import Candidate
from s1flow.eval.evaluation import Estimate, Evaluation, Failures, ObjectiveScore
from s1flow.eval.objectives.declare import Accuracy, ExpectedLoss
from s1flow.eval.policy import EvaluatedPolicy, Evidence, Selection
from s1flow.policies import DecisionRule, PolicySpec
from s1flow.policies.file import asked
from s1flow.policies.log import AnsweredLog, Decision, FeedbackLog


def task_at(tmp_path):
    project = make_project(tmp_path)
    (tmp_path / "cases.json").write_text("[]")
    return attach(Task(id="toy", cases="cases.json", state=lambda row: row, label=lambda row: row.get("label"),
                       question=Boolean(instructions="Yes?"), objective=Accuracy(), dir=tmp_path), project)


def answer(id, *, at="2026-10-24T00:00:00Z", state=None, state_hash=None, policy_digest="policy", execution="exec"):
    return AnsweredLog(at=at, case_id="same-business-id", state=state,
                       state_sha256=state_hash or state_digest(state if state is not None else {"id": id}),
                       decision=Decision(decision_id=id, policy="toy@v1", policy_digest=policy_digest, execution_digest=execution,
                                         value=True, probability=0.9, p_positive=0.9, answered_by="model", latency_ms=1))


def label(id, value=False, *, at="2026-10-24T01:00:00Z", policy_digest="policy"):
    return FeedbackLog(at=at, decision_id=id, policy="toy@v1", policy_digest=policy_digest, label=value)


def test_exact_decision_join_latest_correction_and_no_state_carry(tmp_path):
    task = task_at(tmp_path)
    old = answer("old", state={"text": "old input"})
    new = answer("new", at="2026-10-24T00:30:00Z")
    logs = feedback.Logs(answered=[old, new, old], feedback=[label("old"), label("old", True, at="2026-10-24T02:00:00Z")])
    rows = {row.decision.decision_id: row for row in feedback.cases(task, logs)}
    assert len(rows) == 2 and rows["old"].label is True
    assert rows["new"].label is feedback.MISSING and rows["new"].state is None
    assert logs.issues.duplicates == 1
    # Repeatedly inspecting the same logs does not inflate diagnostics.
    feedback.cases(task, logs)
    assert logs.issues.duplicates == 1


def test_unknown_mismatched_and_conflicting_references_excluded(tmp_path):
    task = task_at(tmp_path)
    logs = feedback.Logs(answered=[answer("ok"), answer("conflict"), answer("conflict", state_hash="other")],
                         feedback=[label("unknown"), label("ok", policy_digest="wrong"), label("conflict")])
    rows = feedback.cases(task, logs)
    assert [r.decision.decision_id for r in rows] == ["ok"] and rows[0].label is feedback.MISSING
    assert logs.issues.unknown_feedback == logs.issues.policy_mismatch == logs.issues.conflicting_decisions == 1


def test_wrong_retained_input_is_never_added(tmp_path):
    task = task_at(tmp_path)
    logs = feedback.Logs(answered=[answer("wrong-state", state={"text": "changed"}, state_hash="not-this-input")],
                         feedback=[label("wrong-state")])
    assert feedback.cases(task, logs) == [] and logs.issues.invalid_state == 1


def adopted(task, objective):
    spec = PolicySpec(task="toy", version=1, connection="m", model_id="model", questions={"q": asked(task.question, DecisionRule(threshold=0.5))})
    evaluation = Evaluation(candidate=Candidate(model="m"), answered_by="model", answered_by_all=["model"], n=20,
                            probabilities=True, failures=Failures(calls=20, failed=0, unsupported=0, data_errors=0, unlabeled=0),
                            objective=ObjectiveScore(objective=objective, value=0, interval=(0, 1)))
    policy = EvaluatedPolicy(spec=spec, candidate=Candidate(model="m"), answered_by="model",
                             selection=Selection(by="test", reason="test", tied=["m"]),
                             evidence=Evidence(data_sha256="data", execution_digest="exec", evaluation=evaluation,
                                               test=None, compared=["m"]))
    task.policies.write_new(policy)
    return policy


def test_production_uses_adopted_primary_and_direction_not_task_accuracy(tmp_path):
    task = task_at(tmp_path)
    policy = adopted(task, ExpectedLoss(fn=2, fp=9))
    logs = feedback.Logs(answered=[answer(str(i), policy_digest=policy.spec.digest) for i in range(20)],
                         feedback=[label(str(i), policy_digest=policy.spec.digest) for i in range(20)])
    prod = feedback.production(task, feedback.cases(task, logs), [])[0]
    assert prod.primary == ExpectedLoss(fn=2, fp=9) and prod.objective.value == 9
    assert prod.below is True and prod.accuracy.value == 0
    assert "bias" in prod.observed_subset


def test_changed_execution_identity_prevents_evidence_comparison(tmp_path):
    task = task_at(tmp_path)
    policy = adopted(task, ExpectedLoss(fn=2, fp=9))
    logs = feedback.Logs(answered=[answer("one", policy_digest=policy.spec.digest, execution="changed")],
                         feedback=[label("one", policy_digest=policy.spec.digest)])
    prod = feedback.production(task, feedback.cases(task, logs), [])[0]
    assert prod.below is None and prod.objective.value is None and "execution" in prod.comparison_reason


def test_custom_objective_hash_change_does_not_reuse_old_measure(tmp_path):
    from s1flow.eval.objectives.custom import Custom, per_case

    @per_case(direction="min")
    def custom_loss(label, reading):
        return float(reading is None or label != reading.value)

    task = task_at(tmp_path).copy(objective=custom_loss())
    policy = adopted(task, task.primary)
    key = task.primary.key
    old = task.custom[key]
    task.custom[key] = Custom(objective=old.objective.model_copy(update={"code_sha256": "changed"}), measure=old.measure)
    logs = feedback.Logs(answered=[answer("one", policy_digest=policy.spec.digest)],
                         feedback=[label("one", policy_digest=policy.spec.digest)])
    prod = feedback.production(task, feedback.cases(task, logs), [])[0]
    assert prod.objective.value is None and prod.below is None and "custom objective code" in prod.comparison_reason


def test_new_cases_use_decision_id_and_exact_events_deduplicate(tmp_path):
    task = task_at(tmp_path)
    logs = feedback.Logs(answered=[answer("first", state={"text": "one"}), answer("second", state={"text": "two"})],
                         feedback=[label("first"), label("first"), label("second")])
    rows = feedback.cases(task, logs)
    assert logs.issues.duplicates == 1
    result = feedback.add(task, rows, write=False)
    assert result.added == 2
    assert "duplicates 1" in feedback.markdown(task, [], result, issues=logs.issues)
