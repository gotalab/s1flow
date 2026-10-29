"""Runtime interpretation is shared; scoring and evidence remain evaluation-owned."""
import json

import pytest
from conftest import attach, make_project

from s1flow.client import Boolean, BooleanAnswer, Box
from s1flow.client.answers import BoxAnswer, BoxEdges
from s1flow.eval import Task
from s1flow.eval.kinds import kind_of as eval_kind
from s1flow.eval.objectives import measure
from s1flow.policies import DecisionRule
from s1flow.policies.kinds import KindParams, kind_of


def test_runtime_has_no_scoring_and_evaluation_uses_same_reading():
    question = Boolean(instructions="Yes?")
    runtime, evaluated = kind_of(question), eval_kind(question)
    answer = BooleanAnswer(probability=0.75)
    rule = DecisionRule(threshold=0.8, min_probability=0.6)
    assert runtime.read([answer], rule) == evaluated.read([answer], rule)
    assert not hasattr(runtime, "correct") and not hasattr(runtime, "objectives") and not hasattr(runtime, "brier")
    assert evaluated.correct(False, evaluated.read([answer], rule))
    assert evaluated.brier(True, evaluated.read([answer], rule)) == 0.0625
    assert not measure.pairs(evaluated, [False], [runtime.read([answer], rule)]).sure[0]


def test_box_evaluation_preserves_iou_semantics():
    kind = eval_kind(Box(instructions="Find it"), KindParams(iou=0.8))
    box = BoxEdges(top=0.1, bottom=0.8, left=0.1, right=0.8)
    reading = kind.read([BoxAnswer(box=box, confidence=0.9)], DecisionRule())
    assert kind.correct(box, reading) and kind.report == ("mean_iou",)
    assert reading.below_min_probability is None


def test_current_data_digest_includes_input_adapter_result_and_labels(tmp_path):
    project = make_project(tmp_path)
    data = tmp_path / "data.json"
    data.write_text(json.dumps([{"id": "1", "text": "first", "label": True}]))
    task = attach(Task(id="toy", cases="data.json", dir=tmp_path, state=lambda row: {"text": row["text"]},
                       label=lambda row: row["label"], question=Boolean(instructions="Yes?")), project)
    before = task.data_digest
    data.write_text(json.dumps([{"id": "1", "text": "second", "label": True}]))
    assert task.data_digest != before
    assert task.input_adapter_digest == task.input_adapter_digest


def test_current_data_digest_includes_materialized_image_bytes(tmp_path):
    image = pytest.importorskip("PIL.Image")
    path = tmp_path / "screen.png"
    image.new("RGB", (300, 300), "red").save(path)
    (tmp_path / "data.json").write_text('[{"id":"1","label":true}]')
    task = Task(id="toy", cases="data.json", dir=tmp_path,
                state=lambda row: ["Look", {"type": "image", "path": "screen.png"}],
                label=lambda row: row["label"], question=Boolean(instructions="Yes?"))
    before = task.data_digest
    image.new("RGB", (300, 300), "blue").save(path)
    assert task.data_digest != before


def test_run_adopt_and_check_share_runtime_interpretation_and_freshness(tmp_path, no_ci):
    import asyncio

    from s1flow.client import Capabilities, Response
    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt, check, run

    class Model:
        def __init__(self, build):
            self.id, self.capabilities, self.concurrency = build.spec.id, Capabilities(), build.spec.concurrency or 4

        async def decide(self, state, questions, *, options=None):
            return Response(answers={key: BooleanAnswer(probability=0.9 if state["truth"] else 0.1) for key in questions},
                            answered_by=self.id)

    project = make_project(tmp_path, {"m": Model})
    data = tmp_path / "data.json"
    data.write_text(json.dumps([{"id": str(i), "input": bool(i % 2), "label": bool(i % 2)} for i in range(40)]))
    task = attach(Task(id="toy", cases="data.json", dir=tmp_path, state=lambda row: {"truth": row["input"]},
                       label=lambda row: row["label"], question=Boolean(instructions="Yes?")), project)
    asyncio.run(run.run_model(task, "m", limit=None, variant="base"))
    selected = adopt.adopt(task, "m", "test", "local deterministic evidence")
    adopt.validate_evidence(task, selected)
    assert selected.evidence.evaluation.test is not None
    result = check.check(task, against="next")
    assert result.verdict == "pass" and result.sides[0].accuracy == 1 and result.test_uses >= 2
    # A standalone application only needs its runtime spec and trusted connections.
    from s1flow.policies import DecisionPolicy
    from s1flow.eval import feedback
    production_log = tmp_path / "production.jsonl"
    runtime = DecisionPolicy(selected.spec, client=project.client(), log=production_log, keep_state=True)
    decision = runtime.decide({"truth": True}, case_id="business-item")
    runtime.feedback(decision.decision_id, True)
    logs = feedback.read([production_log])
    measured = feedback.production(task, feedback.cases(task, logs), logs.failed)[0]
    assert measured.primary == task.primary and measured.objective.value == 1.0
    assert measured.comparison_reason is None
    # Adapter provenance remains a separate evaluation guard, even when inputs agree.
    edited_adapter = task.copy(state=lambda row: {"truth": bool(row["input"])})
    with pytest.raises(ConfigError, match="input adapter changed"):
        adopt.validate_evidence(edited_adapter, selected)
    listed = adopt.shortlist(task)
    # A same-ID edit invalidates the adoption evidence before promotion.
    data.write_text(json.dumps([{"id": str(i), "input": bool(i % 2), "label": not bool(i % 2)} for i in range(40)]))
    with pytest.raises(ConfigError, match="data or labels changed"):
        adopt.validate_evidence(task, selected)
    with pytest.raises(ConfigError, match="comparison data or execution conditions changed"):
        adopt.adopt(task, "m", "test", "stale list", listed=listed)


def test_evaluated_adoption_requires_custom_provider_revision():
    from s1flow.client.models import ModelSpec
    from s1flow.core.errors import ConfigError
    from s1flow.eval.adopt import adoptable

    with pytest.raises(ConfigError, match="provider_revision"):
        adoptable(ModelSpec(provider="app:provider", id="model"), "model")
    adoptable(ModelSpec(provider="app:provider", id="model", provider_revision="commit-123"), "model")
    adoptable(ModelSpec(provider="typesafe", id="model"), "model")


def test_custom_objective_readings_preserve_unconfigured_probability_bound():
    from s1flow.eval.objectives.custom import readings

    kind = eval_kind(Boolean(instructions="Yes?"))
    reading = kind.read([BooleanAnswer(probability=0.8)], DecisionRule())
    pairs = measure.pairs(kind, [True], [reading])
    assert readings(pairs)[0].below_min_probability is None
    assert readings(pairs.at(min_probability=0.9))[0].below_min_probability is True
    assert readings(pairs.at(min_probability=0.7))[0].below_min_probability is False


def scoring_task(tmp_path, objective, *, concurrency=None, price=None):
    import asyncio
    import numpy as np

    from s1flow.client import Capabilities, Response, Usage
    from s1flow.eval import run

    class Model:
        def __init__(self, build):
            self.id, self.capabilities, self.concurrency = build.spec.id, Capabilities(), build.spec.concurrency or 4

        async def decide(self, state, questions, *, options=None):
            return Response(answers={key: BooleanAnswer(probability=state["p"]) for key in questions},
                            answered_by=self.id, usage=Usage(input_tokens=100), latency_ms=1.0)

    project = make_project(tmp_path, {"m": Model})
    if concurrency is not None:
        config = project.root / "s1flow.toml"
        config.write_text(config.read_text() + f"concurrency = {concurrency}\n")
    if price is not None:
        config = project.root / "s1flow.toml"
        config.write_text(config.read_text() + f'price.input_per_mtok = {float(price)}\nprice.as_of = "2026-10-24"\nprice.source = "test"\n')
    rng = np.random.default_rng(42)
    rows = [{"id": str(i), "p": float(p), "label": bool(i % 2)}
            for i, p in enumerate(np.clip(np.where(np.arange(80) % 2, 0.7, 0.3) + rng.normal(0, 0.2, 80), 0, 1))]
    (tmp_path / "data.json").write_text(json.dumps(rows))
    task = attach(Task(id="toy", cases="data.json", dir=tmp_path, state=lambda row: {"p": row["p"]},
                       label=lambda row: row["label"], question=Boolean(instructions="Yes?"), objective=objective), project)
    asyncio.run(run.run_model(task, "m", limit=None, variant="base"))
    return task


def test_old_shortlist_cannot_ship_a_rule_for_a_changed_loss(tmp_path, monkeypatch):
    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt
    from s1flow.eval.objectives.declare import ExpectedLoss

    task = scoring_task(tmp_path, ExpectedLoss(fn=0.1, fp=1))

    async def unexpected_call(**kwargs):
        raise AssertionError("scoring-only changes must reuse valid raw answers")

    monkeypatch.setattr(task.where.client().responses, "create", unexpected_call)
    before = adopt.shortlist(task)
    changed = task.copy(objective=ExpectedLoss(fn=5, fp=1))
    fresh = adopt.shortlist(changed)
    assert before.evaluations["m"].primary.rule != fresh.evaluations["m"].primary.rule
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.adopt(changed, "m", "test", "changed losses", listed=before)
    # Raw requests have not changed. Current rescoring needs no model run.
    adopted = adopt.adopt(changed, "m", "test", "rescored losses", listed=fresh)
    assert adopted.spec.rule == fresh.evaluations["m"].primary.rule


@pytest.mark.parametrize("change", ["objective", "cost", "floor", "tiebreak", "split_config", "split_assignment"])
def test_scoring_changes_invalidate_shortlist_and_adoption_evidence(tmp_path, change):
    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt, evalset
    from s1flow.eval.objectives.declare import AUROC, Constraints, ExpectedLoss
    from s1flow.eval.task import Split

    task = scoring_task(tmp_path, ExpectedLoss(fn=0.1, fp=1))
    listed = adopt.shortlist(task)
    policy = adopt.adopt(task, "m", "test", "initial scoring", listed=listed)
    changed = task
    if change == "objective":
        changed = task.copy(objective=ExpectedLoss(fn=5, fp=1))
    elif change == "cost":
        changed = task.copy(constraints=Constraints(cost_per_10k_usd=0.001))
    elif change == "floor":
        changed = task.copy(constraints=Constraints(min_recall=0.8))
    elif change == "tiebreak":
        changed = task.copy(tiebreak=[AUROC()])
    elif change == "split_config":
        changed = task.copy(split=Split(k=3))
    else:
        path = evalset.path(task)
        saved = json.loads(path.read_text())
        dev = next(key for key, role in saved["assign"].items() if role == "train")
        test = next(key for key, role in saved["assign"].items() if role == "test")
        saved["assign"][dev], saved["assign"][test] = "test", "train"
        path.write_text(json.dumps(saved))
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.adopt(changed, "m", "test", "changed scoring", listed=listed)
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.validate_evidence(changed, policy)


def test_custom_code_change_invalidates_adoption_evidence(tmp_path):
    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt
    from test_loss import _define

    original = _define("def own_loss(label, reading): return float(reading is None or reading.value != label)", direction="min")
    edited = _define("def own_loss(label, reading): return 2.0 * float(reading is None or reading.value != label)", direction="min")
    task = scoring_task(tmp_path, original())
    listed = adopt.shortlist(task)
    policy = adopt.adopt(task, "m", "test", "original objective", listed=listed)
    changed = task.copy(objective=edited())
    assert task.primary.key == changed.primary.key and task.primary.code_sha256 != changed.primary.code_sha256
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.validate_evidence(changed, policy)
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.adopt(changed, "m", "test", "edited code", listed=listed)


def test_evaluation_contract_ignores_usage_history_but_rejects_unknown_evidence(tmp_path):
    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt, evalset
    from s1flow.eval.objectives.declare import ExpectedLoss

    task = scoring_task(tmp_path, ExpectedLoss())
    policy = adopt.adopt(task, "m", "test", "current contract")
    before = task.evaluation_contract_digest
    evalset.record_use(task, "check", "bookkeeping only")
    saved = json.loads(evalset.path(task).read_text())
    saved["at"] = "2099-01-01T00:00:00Z"
    evalset.path(task).write_text(json.dumps(saved))
    assert task.evaluation_contract_digest == before
    adopt.validate_evidence(task, policy)
    unknown = policy.model_copy(update={"evidence": policy.evidence.model_copy(update={"evaluation_contract_digest": None})})
    with pytest.raises(ConfigError, match="evaluation contract changed or is unknown"):
        adopt.validate_evidence(task, unknown)


def test_evaluation_implementation_change_invalidates_shortlist_and_evidence(tmp_path, monkeypatch):
    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt
    from s1flow.eval import task as task_module
    from s1flow.eval.objectives.declare import ExpectedLoss

    task = scoring_task(tmp_path, ExpectedLoss())
    listed = adopt.shortlist(task)
    policy = adopt.adopt(task, "m", "test", "current evaluator", listed=listed)
    monkeypatch.setattr(task_module, "EVALUATION_IMPLEMENTATION_REVISION", "changed-scoring-code", raising=False)
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.adopt(task, "m", "test", "stale evaluator", listed=listed)
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.validate_evidence(task, policy)


def test_concurrency_change_invalidates_old_shortlist_but_reuses_raw_answers(tmp_path):
    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt
    from s1flow.eval.objectives.declare import ExpectedLoss
    from s1flow.project import Project

    task = scoring_task(tmp_path, ExpectedLoss(), concurrency=1)
    listed = adopt.shortlist(task)
    path = task.where.root / "s1flow.toml"
    path.write_text(path.read_text().replace("concurrency = 1", "concurrency = 8"))
    task.project = Project(task.where.root)
    with pytest.raises(ConfigError, match="comparison data or execution conditions changed"):
        adopt.adopt(task, "m", "test", "stale concurrency", listed=listed)
    fresh = adopt.shortlist(task)
    assert fresh.evaluations["m"].n == listed.evaluations["m"].n
    assert fresh.evaluations["m"].calls.latency is None


def test_final_check_does_not_certify_cached_latency_from_other_concurrency(tmp_path):
    from s1flow.eval import adopt, check
    from s1flow.eval.objectives.declare import Constraints, ExpectedLoss
    from s1flow.project import Project

    task = scoring_task(tmp_path, ExpectedLoss())
    adopt.adopt(task, "m", "test", "measured under initial concurrency")
    path = task.where.root / "s1flow.toml"
    path.write_text(path.read_text() + "concurrency = 8\n")
    task.project = Project(task.where.root)
    task.constraints = Constraints(latency_p99_ms=10)
    result = check.check(task, against="next", cached_only=True)
    assert result.sides[0].cached == result.n and result.sides[0].calls == 0
    assert result.verdict == "pending" and result.sides[0].latency_p99_ms is None
    assert "latency constraint cannot be verified" in result.reasons[0]


def test_requested_run_width_change_invalidates_shortlist_without_new_calls(tmp_path, monkeypatch):
    import asyncio

    from s1flow.core.errors import ConfigError
    from s1flow.eval import adopt, run
    from s1flow.eval.objectives.declare import ExpectedLoss

    task = scoring_task(tmp_path, ExpectedLoss())
    listed = adopt.shortlist(task)

    async def unexpected_call(**kwargs):
        raise AssertionError("unchanged raw requests must remain reusable")

    monkeypatch.setattr(task.where.client().responses, "create", unexpected_call)
    asyncio.run(run.run_model(task, "m", limit=None, variant="base", concurrency=8))
    with pytest.raises(ConfigError, match="run evidence changed"):
        adopt.adopt(task, "m", "test", "stale requested width", listed=listed)
    fresh = adopt.shortlist(task)
    assert fresh.evaluations["m"].n == listed.evaluations["m"].n
    assert fresh.evaluations["m"].calls.latency is None


def test_price_change_invalidates_scoring_evidence_while_raw_requests_remain_reusable(tmp_path, monkeypatch):
    from s1flow.client.identity import request_digest
    from s1flow.core.errors import ConfigError, S1flowError
    from s1flow.eval import adopt
    from s1flow.eval.objectives.declare import Constraints, ExpectedLoss
    from s1flow.project import Project

    task = scoring_task(tmp_path, ExpectedLoss(), price=1).copy(constraints=Constraints(cost_per_10k_usd=2))
    listed = adopt.shortlist(task)
    assert listed.evaluations["m"].calls.cost_per_10k_usd == pytest.approx(1)
    policy = adopt.adopt(task, "m", "test", "under the current cost cap", listed=listed)
    state = task.model_state(task.load_cases().all()[0])
    original_request = request_digest(task.where.lineup().resolved("m"), state, task.questions())
    config = task.where.root / "s1flow.toml"
    config.write_text(config.read_text().replace("price.input_per_mtok = 1.0", "price.input_per_mtok = 10.0"))
    task.project = Project(task.where.root)
    assert request_digest(task.where.lineup().resolved("m"), state, task.questions()) == original_request

    async def unexpected_call(**kwargs):
        raise AssertionError("a price correction must rescore the existing raw responses")

    monkeypatch.setattr(task.where.client().responses, "create", unexpected_call)
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.adopt(task, "m", "test", "stale price", listed=listed)
    with pytest.raises(ConfigError, match="evaluation contract changed"):
        adopt.validate_evidence(task, policy)
    fresh = adopt.shortlist(task)
    assert fresh.evaluations["m"].calls.cost_per_10k_usd == pytest.approx(10)
    assert not fresh.fits and "API cost" in fresh.rows()[0].excluded[0]
    with pytest.raises(S1flowError, match="API cost"):
        adopt.adopt(task, "m", "test", "new price exceeds cap", listed=fresh)
