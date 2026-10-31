"""Focused evidence and chart tests for the canonical development comparison."""

from __future__ import annotations

import asyncio
import copy
import json
from pathlib import Path
from typing import Any

import pytest

from conftest import CONDITIONS, TRUTH, change_condition, cli, compare_fake, make_project, write_cases
from s1flow.client import (
    Boolean,
    Box,
    Choice,
)
from s1flow.core.errors import ConfigError
from s1flow.eval import comparison, evalset, metrics, records, run
from s1flow.eval.objectives.declare import AUROC, Constraints, Coverage
from s1flow.eval.task import Task
from s1flow.policies.kinds import KindParams


def task_fixture(tmp_path: Path, *, question: Any, mode: str = "good", models: dict[str, Any] | None = None,
                 variants: bool = False, box_capability: bool = False) -> Task:
    factories = models or {"fake": compare_fake(mode)}
    project = make_project(tmp_path, factories)
    if box_capability:
        config = project.root / "s1flow.toml"
        config.write_text(config.read_text() + "\n[models.fake.capabilities]\nquestion_types = [\"boolean\", \"choice\", \"score\", \"box\"]\n")
    directory = project.tasks_dir / "compare"
    directory.mkdir(parents=True)
    variants_map = {"alt": question} if variants else {}
    task = Task(id="compare", cases="cases.json", state=lambda row: row["state"], label=lambda row: row["label"],
                question=question, variants=variants_map, project=project, dir=directory)
    label = {"choice": lambda truth: "a" if truth else "b", "box": lambda truth: TRUTH.model_dump()}.get(question.type, bool)
    write_cases(task, [{"id": str(i), "state": {"truth": i % 2 == 1}, "label": label(i % 2 == 1)} for i in range(12)])
    split = evalset.SplitFile(seed=1, test_share=1 / 3, at="", source="test", assign={str(i): "test" if i >= 8 else "train" for i in range(12)})
    (directory / "split.json").write_text(split.model_dump_json(by_alias=True))
    return task


def run_saved(task: Task, models: list[str], variants: list[str] = ["base"]) -> None:
    for model in models:
        for variant in variants:
            asyncio.run(run.run_model(task, model, limit=None, variant=variant))


def test_collects_model_variants_in_neutral_model_variant_order(tmp_path):
    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"),
                        models={"good": compare_fake("good"), "bad": compare_fake("bad")}, variants=True)
    run_saved(task, ["good", "bad"], ["base", "alt"])
    got = comparison.collect(task)
    assert {row.candidate for row in got.candidates} == {"good", "good/alt", "bad", "bad/alt"}
    assert all(row.charts is None for row in got.candidates)
    assert [row.candidate for row in got.candidates] == ["bad", "bad/alt", "good", "good/alt"]
    assert not hasattr(got, "recommended")
    assert all("recommended" not in row.model_dump() for row in got.candidates)


def test_missing_and_stale_candidates_remain_visible(tmp_path):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"), variants=True)
    run_saved(task, ["fake"], ["base"])
    missing_path = run.run_path(task, "alt", "fake")
    rows = {row.candidate: row for row in comparison.collect(task).candidates}
    assert "fake/alt" in rows and any("missing run" in reason for reason in rows["fake/alt"].excluded)
    case_path = task.dir / task.cases
    rows = json.loads(case_path.read_text())
    rows[0]["state"] = {"truth": True}
    case_path.write_text(json.dumps(rows))
    task.load_cases().forget()
    stale = comparison.collect(task)
    stale_row = next(row for row in stale.candidates if row.candidate == "fake")
    assert stale_row.value is None and any("stale" in reason for reason in stale_row.excluded)
    assert "1 cases never asked" in stale_row.excluded  # the words report and adopt use (evaluation.why_missing)
    assert stale_row.metrics["accuracy"].value is None
    assert not missing_path.exists()


def test_collect_does_not_build_provider_or_fetch_network(tmp_path, monkeypatch):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"))
    run_saved(task, ["fake"])
    monkeypatch.setattr(type(task.where), "client", lambda self: (_ for _ in ()).throw(AssertionError("built provider")))
    assert comparison.collect(task).candidates[0].candidate == "fake"


def test_summary_is_bounded_and_detail_selects_one_candidate(tmp_path):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"))
    run_saved(task, ["fake"])
    compact = comparison.collect(task)
    full = comparison.collect(task, include_charts=True)
    assert compact.id == full.id
    payload = comparison.summary(full, limit=1)
    dumped = json.dumps(payload)
    assert payload["id"] == full.id and payload["objective"]["name"] == "accuracy"
    assert "charts" not in payload["candidates"][0] and "question" not in payload["candidates"][0]
    assert "answered_ids" not in dumped and "run_digests" not in dumped
    assert len(payload["candidates"]) == 1
    detail = comparison.summary(full, candidate="fake")
    assert detail["candidate"]["candidate"] == "fake" and "question" in detail["candidate"] and "charts" not in detail["candidate"]


def test_snapshot_read_is_offline_and_rejects_bad_files(tmp_path, monkeypatch):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"))
    run_saved(task, ["fake"])
    snapshot = tmp_path / "comparison.json"
    snapshot.write_text(comparison.collect(task, include_charts=True).model_dump_json(by_alias=True))
    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.chdir(other)
    loaded = comparison.read(snapshot)
    result = comparison.summary(loaded, snapshot=str(snapshot))
    assert result["snapshot"] == str(snapshot) and result["current_certified"] is False
    cli_result = cli("report", "--from", str(snapshot), "--json")
    assert cli_result.exit_code == 0 and json.loads(cli_result.output)["provenance"] == "saved snapshot"
    bad = tmp_path / "bad.json"
    bad.write_text("{}")
    with pytest.raises(ConfigError, match="invalid comparison snapshot"):
        comparison.read(bad)
    invalid = tmp_path / "invalid-utf8.json"
    invalid.write_bytes(b"\xff")
    with pytest.raises(ConfigError, match="invalid comparison snapshot"):
        comparison.read(invalid)


def test_measurement_ignores_historical_distribution_rows(tmp_path):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"))
    run_saved(task, ["fake"])
    path = run.run_path(task, "base", "fake")
    current = records.read(path)
    historical = current[0].model_copy(update={"at": "0000-01-01T00:00:00.000Z", "distribution": "none"})
    path.write_text(historical.line() + "\n" + "\n".join(row.line() for row in current) + "\n")
    row = comparison.collect(task).candidates[0]
    assert row.measurement.distribution == "native"


def test_comparison_notices_unlike_latency_provenance(tmp_path):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"), models={"good": compare_fake("good"), "bad": compare_fake("bad")})
    run_saved(task, ["good", "bad"])
    path = run.run_path(task, "base", "bad")
    rows = [record.model_copy(update={"concurrency": 4}) for record in records.read(path)]
    path.write_text("\n".join(record.line() for record in rows) + "\n")
    result = comparison.collect(task)
    assert any("latency not compared" in notice for notice in result.notices)
    summary = comparison.summary(result)
    assert any("latency not compared" in notice for notice in summary["notices"])


@pytest.mark.parametrize(
    ("question", "mode", "box_capability", "basis"),
    [
        (Boolean(instructions="truth?"), "good", False, "selected-answer probability"),
        (Choice(instructions="which?", criteria={"a": None, "b": None}), "good", False, "selected-answer probability"),
        (Box(instructions="where?"), "good", True, "box confidence"),
    ],
)
def test_selection_sweep_has_exact_dev_counts_and_basis(tmp_path, question, mode, box_capability, basis):
    task = task_fixture(tmp_path, question=question, mode=mode, box_capability=box_capability)
    run_saved(task, ["fake"])
    row = comparison.collect(task, include_charts=True).candidates[0]
    assert row.charts is not None and row.charts.selection_basis == basis
    if question.type == "box":
        assert row.adoption_blocked
        assert row.metrics["mean_iou"].value == pytest.approx(1.0)
    assert row.charts.selection_unavailable is None
    selected = next(point for point in row.charts.selection_sweep if point.min_probability == 0.8)
    assert selected.total == 8 and selected.accepted == 8 and selected.correct == 8


@pytest.mark.parametrize(
    ("question", "mode", "box_capability"),
    [
        (Choice(instructions="which?", criteria={"a": None, "b": None}), "choice-none", False),
        (Box(instructions="where?"), "box-none", True),
    ],
)
def test_declared_native_without_actual_distribution_is_unavailable(tmp_path, question, mode, box_capability):
    task = task_fixture(tmp_path, question=question, mode=mode, box_capability=box_capability)
    run_saved(task, ["fake"])
    loaded = metrics.load(task, "base", "fake")
    assert not loaded.probabilities and loaded.distribution == "none"
    row = comparison.collect(task, include_charts=True).candidates[0]
    assert row.charts is not None and not row.charts.selection_sweep and row.charts.selection_unavailable


def test_held_out_changes_do_not_change_dev_value(tmp_path):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"))
    run_saved(task, ["fake"])
    before = comparison.collect(task)
    case_path = task.dir / task.cases
    rows = json.loads(case_path.read_text())
    rows[8]["label"] = True
    case_path.write_text(json.dumps(rows))
    task.load_cases().forget()
    after = comparison.collect(task)
    assert before.candidates[0].value == after.candidates[0].value
    assert before.data_digest != after.data_digest


@pytest.mark.parametrize('change', ['endpoint', 'concurrency', 'model'])
def test_comparison_identity_changes_with_effective_connection_conditions(tmp_path, change):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions='truth?'))
    run_saved(task, ['fake'])
    before = comparison.collect(task)
    spec = task.where.lineup().models['fake']
    if change == 'endpoint':
        spec.options['base_url'] = 'https://another-endpoint.invalid'
    elif change == 'concurrency':
        spec.concurrency = 8
    else:
        spec.id = 'different-concrete-model'
    after = comparison.collect(task)
    assert after.id != before.id


@pytest.mark.parametrize('what', CONDITIONS)
@pytest.mark.parametrize('reading', ['_inputs', '_actual_row'])  # once the questions and specs are cached; the run
def test_a_condition_changed_while_comparing_refuses_the_comparison(tmp_path, monkeypatch, what, reading):
    task = task_fixture(tmp_path, question=Boolean(instructions='truth?'))
    run_saved(task, ['fake'])
    named, read = [], getattr(comparison, reading)

    def read_then_change(*args, **kwargs):
        got = read(*args, **kwargs)
        named.append(change_condition(task, what, 'fake'))
        return got

    monkeypatch.setattr(comparison, reading, read_then_change)
    with pytest.raises(ConfigError) as refused:
        comparison.collect(task)
    assert str(refused.value) == f'compare: {named[0]} changed during the comparison; compare again'


MUTATIONS = {
    "unknown question type": lambda d: d.__setitem__("question_type", "score-ish"),
    "unknown distribution": lambda d: d["candidates"][0]["measurement"].__setitem__("distribution", "bogus"),
    "NaN in a chart": lambda d: d["candidates"][0]["charts"]["selection_sweep"][0].__setitem__("min_probability", float("nan")),
    "NaN metric": lambda d: d["candidates"][0]["metrics"]["accuracy"].__setitem__("value", float("nan")),
    "infinite interval": lambda d: d["candidates"][0]["metrics"]["accuracy"].__setitem__("interval", [0.0, float("inf")]),
    "a metric without its row": lambda d: d["candidates"][0]["metrics"].pop("accuracy"),
    "a metric defined twice": lambda d: d["metric_definitions"].append(copy.deepcopy(d["metric_definitions"][0])),
}


@pytest.mark.parametrize("mutate", MUTATIONS.values(), ids=MUTATIONS.keys())
def test_a_snapshot_with_unknown_contracts_nonfinite_values_or_mismatched_metric_keys_is_refused(tmp_path, mutate):
    task = task_fixture(tmp_path, question=Boolean(instructions="truth?"))
    run_saved(task, ["fake"])
    data = comparison.collect(task, include_charts=True).model_dump(mode="json", by_alias=True)
    mutate(data)
    with pytest.raises(ValueError):
        comparison.Comparison.model_validate(data)


def test_missing_run_has_unknown_actual_probability_evidence(tmp_path):
    from s1flow.client import Boolean

    task = task_fixture(tmp_path, question=Boolean(instructions='truth?'))
    row = comparison.collect(task).candidates[0]
    assert row.measurement.distribution == 'unknown'
    assert row.probabilities is False


def test_metrics_match_evaluation_and_summary_has_no_selection_fields(tmp_path):
    task = task_fixture(tmp_path, question=Boolean(instructions='truth?'))
    run_saved(task, ['fake'])
    result = comparison.collect(task)
    row = result.candidates[0]
    evaluated = metrics.evaluate(task, metrics.load(task, 'base', 'fake'))
    assert row.metrics['accuracy'].value == evaluated.accuracy.value
    assert row.metrics['f1'].value == evaluated.measures['f1'].value
    assert row.metrics['precision'].value == evaluated.measures['precision'].value
    assert row.metrics['recall'].value == evaluated.measures['recall'].value
    assert row.metrics['auroc'].value == evaluated.auroc.value
    assert 'recommended' not in result.model_dump_json()
    assert 'tied' not in result.model_dump_json()
    payload = comparison.summary(result)
    assert 'recommended' not in json.dumps(payload)
    assert {d['key'] for d in payload['metric_definitions']} >= {'accuracy', 'precision', 'recall', 'auroc', 'objective:accuracy{}'}
    definitions = {d['key']: d for d in payload['metric_definitions']}
    assert 'P(true) >= 0.5' in definitions['accuracy']['basis']


def test_below_target_candidate_keeps_plain_metrics_and_is_not_excluded(tmp_path):
    base = task_fixture(tmp_path, question=Boolean(instructions='truth?'), mode='bad')
    task = base.copy(objective=Coverage(target_accuracy=0.99))
    run_saved(task, ['fake'])
    result = comparison.collect(task)
    row = result.candidates[0]
    assert row.value is None
    assert row.metrics['accuracy'].value == pytest.approx(0.0)
    assert 'objective:coverage{"target_accuracy": 0.99}' not in row.metrics
    assert not any('target' in reason.lower() for reason in row.excluded)


def test_infeasible_primary_rule_keeps_plain_metrics_and_nulls_fitted_score(tmp_path):
    base = task_fixture(tmp_path, question=Boolean(instructions='truth?'), mode='bad')
    task = base.copy(constraints=Constraints(min_precision=0.99, min_recall=0.99))
    run_saved(task, ['fake'])
    row = comparison.collect(task).candidates[0]
    assert row.value is None and row.rule is None and row.excluded == []
    assert row.metrics['accuracy'].value == pytest.approx(0.0)
    assert row.metrics['f1'].value == pytest.approx(0.0)
    assert row.metrics['objective:accuracy{}'].value is None


def test_positive_choice_reports_binary_metrics(tmp_path):
    task = task_fixture(tmp_path, question=Choice(instructions='which?', criteria={'a': None, 'b': None}))
    task = task.copy(kind_params=KindParams(positive='a'))
    run_saved(task, ['fake'])
    row = comparison.collect(task).candidates[0]
    evaluated = metrics.evaluate(task, metrics.load(task, 'base', 'fake'))
    assert row.metrics['accuracy'].value == evaluated.accuracy.value
    assert row.metrics['f1'].value == evaluated.measures['f1'].value
    assert row.metrics['precision'].value == evaluated.measures['precision'].value
    assert row.metrics['recall'].value == evaluated.measures['recall'].value
    assert 'P(a) >= 0.5' in next(d for d in comparison.collect(task).metric_definitions if d.key == 'accuracy').basis


def test_plain_choice_and_box_basis_names_the_runtime_reading(tmp_path):
    choice_task = task_fixture(tmp_path / 'choice', question=Choice(instructions='which?', criteria={'a': None, 'b': None}))
    run_saved(choice_task, ['fake'])
    choice_accuracy = next(d for d in comparison.collect(choice_task).metric_definitions if d.key == 'accuracy')
    assert 'selected option with highest probability' in choice_accuracy.basis

    box_task = task_fixture(tmp_path / 'box', question=Box(instructions='where?'), box_capability=True)
    box_task = box_task.copy(kind_params=KindParams(iou=0.7))
    run_saved(box_task, ['fake'])
    box_iou = next(d for d in comparison.collect(box_task).metric_definitions if d.key == 'mean_iou')
    assert 'IoU >= 0.7' in box_iou.basis


def test_primary_coverage_uses_selective_metric_once(tmp_path):
    base = task_fixture(tmp_path, question=Boolean(instructions='truth?'))
    task = base.copy(objective=Coverage(target_accuracy=0.95))
    run_saved(task, ['fake'])
    result = comparison.collect(task)
    keys = {d.key for d in result.metric_definitions}
    assert 'objective:coverage{"target_accuracy": 0.95}' not in keys
    assert {'coverage:0.95', 'accepted_accuracy:0.95'} <= keys
    assert {'coverage:0.95', 'accepted_accuracy:0.95'} <= set(result.candidates[0].metrics)


def test_secondary_coverage_at_a_different_target_stays_distinct(tmp_path):
    base = task_fixture(tmp_path, question=Boolean(instructions='truth?'))
    task = base.copy(objective=Coverage(target_accuracy=0.95), tiebreak=[Coverage(target_accuracy=0.9)])
    run_saved(task, ['fake'])
    keys = {d.key for d in comparison.collect(task).metric_definitions}
    assert 'objective:coverage{"target_accuracy": 0.95}' not in keys
    assert 'objective:coverage{"target_accuracy": 0.9}' in keys


def test_all_negative_auroc_does_not_hide_plain_metrics(tmp_path):
    task = task_fixture(tmp_path, question=Boolean(instructions='truth?'), mode='good')
    case_path = task.dir / task.cases
    rows = json.loads(case_path.read_text())
    for row in rows:
        row['label'] = False
    case_path.write_text(json.dumps(rows))
    task.load_cases().forget()
    run_saved(task, ['fake'])
    task = task.copy(objective=AUROC())
    result = comparison.collect(task)
    row = result.candidates[0]
    assert row.excluded == []
    assert row.metrics['accuracy'].value == pytest.approx(0.5)
    assert row.metrics['objective:auroc{}'].value is None


def test_no_rule_objectives_describe_plain_choice_and_auroc_readings(tmp_path):
    choice_task = task_fixture(tmp_path / 'choice', question=Choice(instructions='which?', criteria={'a': None, 'b': None}))
    run_saved(choice_task, ['fake'])
    choice_result = comparison.collect(choice_task)
    choice_defs = {d.key: d for d in choice_result.metric_definitions}
    assert 'plain choice reading: selected option with highest probability' in choice_defs['objective:accuracy{}'].basis

    auroc_task = task_fixture(tmp_path / 'auroc', question=Boolean(instructions='truth?'))
    auroc_task = auroc_task.copy(objective=AUROC())
    run_saved(auroc_task, ['fake'])
    auroc_result = comparison.collect(auroc_task)
    auroc_defs = {d.key: d for d in auroc_result.metric_definitions}
    assert 'plain binary reading: P(true) >= 0.5' in auroc_defs['objective:auroc{}'].basis
