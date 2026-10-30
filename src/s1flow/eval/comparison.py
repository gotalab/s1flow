"""One neutral development comparison for terminal readers and agents.

The comparison is deliberately a read of the current line-up and saved run
evidence.  It never builds a provider or asks a model.  ``metrics`` owns all
numbers; this module assembles the common snapshot and bounded terminal views.
Comparison itself does not rank or recommend candidates.  The explicit
selection/adoption paths continue to use ``eval.select`` separately.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..client.identity import digest, execution_digest
from ..client.models import ModelSpec
from ..client.questions import Choice, Question
from ..core import clock
from ..core.errors import ConfigError, NotFound, S1flowError
from ..policies.kinds import KindParams
from ..policies.rule import DecisionRule
from . import evalset, metrics, select
from .candidate import Candidate
from .evaluation import (
    Calls,
    ChartData,
    DistributionEvidence,
    Estimate,
    Evaluation,
    Failures,
)
from .objectives.declare import Constraints, Objective
from .run import run_path
from .task import Task


class Measurement(BaseModel):
    model_config = ConfigDict(extra='forbid')
    provider: str
    model_id: str
    distribution: DistributionEvidence
    declared_concurrency: int | None = Field(ge=1)


class MetricDefinition(BaseModel):
    """Meaning of one key in :attr:`ComparisonRow.metrics`."""

    model_config = ConfigDict(extra='forbid', frozen=True)
    key: str
    label: str
    unit: Literal['share', 'number']
    basis: str
    direction: Literal['max', 'min']


class ComparisonRow(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    candidate: str
    model: str
    variant: str
    n: int = Field(ge=0, description='Answered labelled development cases scored for this candidate')
    value: float | None
    interval: tuple[float, float] | None
    rule: DecisionRule | None
    metrics: dict[str, Estimate]
    excluded: list[str] = Field(default_factory=list)
    adoption_blocked: list[str] = Field(default_factory=list)
    probabilities: bool
    failures: Failures
    calls: Calls
    measurement: Measurement
    question: Question
    charts: ChartData | None = None

    @model_validator(mode="after")
    def _metric_estimates_are_finite(self) -> "ComparisonRow":
        for key, estimate in self.metrics.items():
            values = [estimate.value] if estimate.interval is None else [estimate.value, *estimate.interval]
            if any(value is not None and not math.isfinite(value) for value in values):
                raise ValueError(f"metric {key!r} contains a non-finite estimate")
        return self


class Comparison(BaseModel):
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/comparison@2'] = Field(default='s1flow/comparison@2', alias='schema')
    id: str
    task: str
    source: str = ""
    at: str
    scope: Literal['dev'] = 'dev'
    question_type: Literal['boolean', 'choice', 'box']
    kind_params: KindParams
    objective: Objective
    constraints: Constraints
    data_digest: str
    evaluation_contract_digest: str
    input_adapter_digest: str
    binding_digests: dict[str, str]
    run_digests: dict[str, str]
    n: int = Field(ge=0, description='All labelled development cases in the task')
    metric_definitions: list[MetricDefinition]
    notices: list[str] = Field(default_factory=list)
    candidates: list[ComparisonRow]

    @model_validator(mode="after")
    def _metric_definitions_match_rows(self) -> "Comparison":
        definition_keys = [definition.key for definition in self.metric_definitions]
        if len(definition_keys) != len(set(definition_keys)):
            raise ValueError("metric_definitions contains duplicate keys")
        expected = set(definition_keys)
        for row in self.candidates:
            actual = set(row.metrics)
            if actual != expected:
                raise ValueError(
                    f"candidate {row.candidate!r} metric keys do not match metric_definitions"
                )
        return self


@dataclass(frozen=True)
class _CandidateInput:
    candidate: Candidate
    question: Question
    spec: ModelSpec | None
    path: Path
    run_digest: str


def _run_digest(path: Path) -> str:
    """Digest the saved run and metadata without embedding records in a snapshot."""
    return digest({
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None,
        path.with_suffix(".meta.json").name: hashlib.sha256(path.with_suffix(".meta.json").read_bytes()).hexdigest()
        if path.with_suffix(".meta.json").exists() else None,
    })


def _variants(task: Task, variants: Sequence[str] | None = None) -> list[str]:
    chosen = list(variants) if variants is not None else ["base", *task.variants]
    return list(dict.fromkeys(chosen))


def _inputs(task: Task, variants: Sequence[str] | None = None, only: Sequence[str] | None = None) -> list[_CandidateInput]:
    lineup = task.where.lineup()
    wanted = set(only or ())
    out: list[_CandidateInput] = []
    for model in lineup.probe_names():
        for variant in _variants(task, variants):
            candidate = Candidate(model=model, variant=variant)
            if wanted and candidate.name not in wanted:
                continue
            path = run_path(task, variant, model)
            spec: ModelSpec | None
            try:
                spec = lineup.resolved(model)
            except S1flowError:
                spec = None
            out.append(_CandidateInput(candidate, task.questions(variant)[task.question_id], spec, path, _run_digest(path)))
    return out


def _dev_n(task: Task) -> int:
    sf = evalset.current(task)
    return sum(1 for case in task.load_cases().labelled() if sf.assign.get(case.id) != "test")


def _measurement(item: _CandidateInput, pr: metrics.Preds | None) -> Measurement:
    spec = item.spec
    provider = "unknown" if spec is None else spec.provider
    model_id = "unknown" if spec is None else spec.id
    declared = None if spec is None else spec.concurrency
    distribution: DistributionEvidence = "unknown"
    # ``metrics.load`` has already selected the current prompt, request
    # identity and answering model.  Use that aggregate rather than reading
    # append-only history here: old generations must not change this display.
    if pr is not None and pr.distribution is not None:
        distribution = pr.distribution
    return Measurement(provider=provider, model_id=model_id, distribution=distribution, declared_concurrency=declared)


def _adoption_blocked(task: Task, item: _CandidateInput) -> list[str]:
    blocked: list[str] = []
    if task.kind.type == "box":
        blocked.append("box questions are comparable but cannot be adopted as runtime policies")
    spec = item.spec
    if spec is not None and spec.versions is not None and spec.version is None:
        blocked.append("model is an alias; adopt a pinned model version")
    return blocked


def _missing_reason(item: _CandidateInput, pr: metrics.Preds | None, error: Exception | None = None) -> list[str]:
    if error is not None:
        return [str(error)]
    if not item.path.exists():
        return [f"missing run evidence for {item.candidate.name}"]
    if pr is None:
        return [f"could not read run evidence for {item.candidate.name}"]
    reasons: list[str] = []
    if pr.never_asked:
        reasons.append(f"{len(pr.never_asked)} labelled dev cases never asked")
    if pr.failed_cases:
        reasons.append(f"{len(pr.failed_cases)} labelled dev cases failed on every call")
    if pr.never_asked or pr.failed_cases:
        reasons.append("current metrics unavailable: run evidence is stale or incomplete")
    if not pr.ids and pr.refused_cases:
        reasons.append(f"{len(pr.refused_cases)} labelled dev cases refused or unsupported")
    if not pr.ids and pr.data_errors:
        reasons.append(f"{pr.data_errors} calls ended in task data errors")
    if not pr.ids:
        reasons.append("no current answers; run evidence is stale or empty")
    return reasons


def _empty_failures(total: int, reason: str | None = None) -> Failures:
    return Failures(calls=0, failed=0, unsupported=0, data_errors=0, unlabeled=0,
                    never_asked=total if reason else 0, failed_cases=0, refused_cases=0)


_KNOWN_METRIC_LABELS = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "F1",
    "macro_f1": "macro-F1",
    "mean_iou": "mean IoU",
    "auroc": "AUROC",
    "brier": "Brier score",
    "ece": "ECE",
}
_KNOWN_METRIC_UNITS: dict[str, Literal["share", "number"]] = {
    "accuracy": "share", "precision": "share", "recall": "share",
    "f1": "number", "macro_f1": "number", "mean_iou": "number",
    "auroc": "number", "brier": "number", "ece": "number",
}
_KNOWN_METRIC_DIRECTIONS: dict[str, Literal["max", "min"]] = {
    "accuracy": "max", "precision": "max", "recall": "max", "f1": "max",
    "macro_f1": "max", "mean_iou": "max", "auroc": "max", "brier": "min", "ece": "min",
}


def _target_key(target: float) -> str:
    """Stable, compact target text used in selective metric keys."""
    return format(float(target), ".15g")


def _objective_metric_key(objective: Objective) -> str:
    """Keep params in the key: distinct configured objectives stay distinct."""
    return f"objective:{objective.key}"


def _primary_rule_infeasible(evaluation: Evaluation | None) -> bool:
    """A fitted primary objective has no valid rule when its rule field is unset."""
    score = None if evaluation is None else evaluation.objective
    return bool(score is not None and score.objective.sets is not None and score.rule is None)


def _plain_reading_basis(task: Task) -> str:
    """Describe the runtime's plain reading used by descriptive metrics."""
    kind = task.kind
    if kind.type == "boolean":
        return "plain binary reading: P(true) >= 0.5"
    if kind.binary:
        positive = task.kind_params.positive or "positive"
        return f"plain binary reading: P({positive}) >= 0.5"
    if kind.type == "choice":
        return "plain choice reading: selected option with highest probability (default rule)"
    if kind.type == "box":
        return f"plain box reading: correct at IoU >= {kind.iou:g}"
    return "plain reading"


def _metric_definitions(task: Task, evaluations: Sequence[Evaluation]) -> list[MetricDefinition]:
    """Build the shared metric vocabulary from the task and available evidence."""
    out: list[MetricDefinition] = []
    seen: set[str] = set()

    def add(key: str, label: str, unit: Literal["share", "number"], basis: str,
            direction: Literal["max", "min"]) -> None:
        if key not in seen:
            out.append(MetricDefinition(key=key, label=label, unit=unit, basis=basis, direction=direction))
            seen.add(key)

    reading = _plain_reading_basis(task)
    plain_bases = {
        "accuracy": f"{reading}; correct / answered labelled dev cases",
        "precision": f"{reading}; true positives / predicted positives among answered labelled dev cases",
        "recall": f"{reading}; true positives / labelled positives among answered labelled dev cases",
        "f1": f"{reading}; harmonic mean of precision and recall over answered labelled dev cases",
        "macro_f1": f"{reading}; mean of per-class F1 over answered labelled dev cases",
        "mean_iou": f"{reading}; mean IoU over answered labelled dev cases",
    }
    add("accuracy", "accuracy", "share", plain_bases["accuracy"], "max")
    for key in task.kind.report:
        if key in _KNOWN_METRIC_LABELS:
            add(key, _KNOWN_METRIC_LABELS[key], _KNOWN_METRIC_UNITS[key],
                plain_bases.get(key, "plain answers over answered labelled dev cases"), _KNOWN_METRIC_DIRECTIONS[key])

    # Probability-derived metrics are included only when at least one current
    # evaluation has genuine probability support. Rows without it remain null.
    if any(e.probabilities for e in evaluations):
        if task.kind.type == "box":
            add("auroc", "AUROC", "number",
                "recorded box confidence; hit-ranking AUROC over answered labelled dev cases", "max")
            add("ece", "ECE", "number",
                "recorded box confidence; calibration of hit correctness over answered labelled dev cases", "min")
        elif task.kind.binary:
            add("auroc", "AUROC", "number",
                "genuine model probabilities; binary positive-vs-negative AUROC over answered labelled dev cases", "max")
            add("brier", "Brier score", "number",
                "genuine model probabilities; binary Brier score over answered labelled dev cases", "min")
            add("ece", "ECE", "number",
                "genuine model probabilities; calibration of answer correctness over answered labelled dev cases", "min")
        else:
            add("auroc", "AUROC", "number",
                "genuine model probabilities; macro one-v-rest AUROC over options and answered labelled dev cases", "max")
            add("brier", "Brier score", "number",
                "genuine model probabilities; multiclass Brier score over answered labelled dev cases", "min")
            add("ece", "ECE", "number",
                "genuine model probabilities; calibration of selected-answer correctness over answered labelled dev cases", "min")

    for i, objective in enumerate(task.objectives):
        if (
            i == 0
            and objective.name == "coverage"
            and any(
                s.target_accuracy == cast(float, objective.params["target_accuracy"])
                for evaluation in evaluations
                for s in evaluation.selective
            )
        ):
            # The primary Coverage score is the same configured target as the
            # selective coverage/accepted-accuracy pair. Keep row.value/rule
            # as primary context, but expose one neutral metric projection.
            continue
        if i == 0:
            where = "configured primary objective"
            reading_basis = (
                "CV chosen rule"
                if task.primary.sets is not None
                else _plain_reading_basis(task)
            )
        else:
            where = "configured tiebreak objective"
            reading_basis = (
                "primary CV chosen rule"
                if task.primary.sets is not None
                else "primary plain rule"
            )
        basis = f"{where}; {reading_basis}; denominator: answered labelled dev cases"
        add(_objective_metric_key(objective), objective.label, objective.unit, basis, objective.direction)

    targets = sorted({s.target_accuracy for e in evaluations for s in e.selective})
    for target in targets:
        key = _target_key(target)
        coverage_basis = f"target reference {key}; target-specific CV chosen rule; observed accepted / answered labelled dev cases"
        accepted_basis = f"target reference {key}; target-specific CV chosen rule; observed correct accepted / accepted labelled dev cases"
        add(f"coverage:{key}", f"coverage (target reference {100 * target:g}%)", "share", coverage_basis, "max")
        add(f"accepted_accuracy:{key}", f"accepted accuracy (target reference {100 * target:g}%)", "share", accepted_basis, "max")
    return out


def _row_metrics(evaluation: Evaluation | None, definitions: Sequence[MetricDefinition], *, incomplete: bool) -> dict[str, Estimate]:
    """Project one Evaluation into the shared neutral metric vocabulary."""
    missing = {d.key: Estimate(value=None, interval=None) for d in definitions}
    if evaluation is None or incomplete:
        return missing

    values: dict[str, Estimate] = {}
    if evaluation.accuracy is not None:
        values["accuracy"] = evaluation.accuracy
    for key, estimate in evaluation.measures.items():
        values[key] = estimate
    if evaluation.probabilities:
        if evaluation.auroc is not None:
            values["auroc"] = evaluation.auroc
        if evaluation.brier is not None:
            values["brier"] = Estimate(value=evaluation.brier)
        if evaluation.ece is not None:
            values["ece"] = Estimate(value=evaluation.ece)

    primary_infeasible = _primary_rule_infeasible(evaluation)
    for score in evaluation.scores:
        values[_objective_metric_key(score.objective)] = (
            Estimate(value=None, interval=None)
            if primary_infeasible else Estimate(value=score.value, interval=score.interval)
        )
    for selective in evaluation.selective:
        key = _target_key(selective.target_accuracy)
        values[f"coverage:{key}"] = selective.coverage
        values[f"accepted_accuracy:{key}"] = Estimate(value=selective.accuracy)

    return {d.key: values.get(d.key, Estimate(value=None, interval=None)) for d in definitions}


def _actual_row(item: _CandidateInput, task: Task, total: int, *, include_charts: bool) -> tuple[ComparisonRow, Evaluation | None, str | None]:
    """Read one candidate, returning its row and Evaluation (if scored)."""
    reason: list[str] = []
    error: Exception | None = None
    pr: metrics.Preds | None = None
    evaluation: Evaluation | None = None
    chart_notice: str | None = None
    if item.spec is None:
        reason.append(f"model {item.candidate.model!r} is no longer in the current line-up")
    elif not item.path.exists():
        reason.append(f"missing run evidence for {item.candidate.name}")
    else:
        if item.question.type not in item.spec.capabilities.question_types:
            reason.append(f"model does not declare support for {item.question.type} questions")
        if isinstance(item.question, Choice) and item.spec.capabilities.max_options is not None and len(item.question.criteria) > item.spec.capabilities.max_options:
            reason.append(f"question has {len(item.question.criteria)} options > model limit {item.spec.capabilities.max_options}")
        try:
            pr = metrics.load(task, item.candidate.variant, item.candidate.model)
            evaluation = metrics.evaluate(task, pr, variant=item.candidate.variant)
        except (S1flowError, ValueError, OSError) as exc:
            error = exc
            reason.append(str(exc))
    if error is None and pr is not None:
        reason.extend(_missing_reason(item, pr))
    question = item.question
    failures = evaluation.failures if evaluation is not None else _empty_failures(total, reason[0] if reason else None)
    probabilities = bool(pr.probabilities) if pr is not None else False
    incomplete = bool(pr is not None and (pr.never_asked or pr.failed_cases))
    charts = None
    if include_charts and evaluation is not None and not incomplete:
        try:
            assert pr is not None
            charts = metrics.chart_data(task, pr, evaluation)
        except (S1flowError, ValueError, OSError) as exc:
            # A renderer problem must not make a numerically eligible
            # candidate ineligible.  Keep it as snapshot metadata instead.
            chart_notice = f"charts unavailable for {item.candidate.name}: {exc}"
    infeasible = _primary_rule_infeasible(evaluation)
    objective = None if evaluation is None or incomplete or infeasible else evaluation.objective
    row = ComparisonRow(
        candidate=item.candidate.name, model=item.candidate.model, variant=item.candidate.variant,
        n=0 if evaluation is None else evaluation.n,
        value=None if objective is None else objective.value,
        interval=None if objective is None else objective.interval,
        rule=None if objective is None else objective.rule,
        metrics={},
        excluded=reason, adoption_blocked=_adoption_blocked(task, item), probabilities=probabilities,
        failures=failures, calls=Calls() if evaluation is None else evaluation.calls,
        measurement=_measurement(item, pr), question=question, charts=charts,
    )
    return row, evaluation, chart_notice


def collect(task: Task, *, variants: Sequence[str] | None = None, only: Sequence[str] | None = None,
            include_charts: bool = False) -> Comparison:
    """Build the current dev comparison without model calls or provider fetches.

    Chart series are opt-in because an agent summary should stay bounded.  The
    evidence identity and metric values are identical with or without them.
    """
    if task.kind.type == "score":
        raise ConfigError(f"{task.id}: score questions are not supported by comparison yet")
    data_digest = task.data_digest
    contract_digest = task.evaluation_contract_digest
    adapter_digest = task.input_adapter_digest
    # A neutral comparison has a stable, human-readable order independent of
    # objective direction, constraints, intervals, or API cost.
    inputs = sorted(
        _inputs(task, variants, only),
        key=lambda x: (x.candidate.model, x.candidate.variant != "base", x.candidate.variant),
    )
    binding_digests = {
        item.candidate.model: execution_digest(item.spec, '') if item.spec is not None else 'unresolved'
        for item in inputs
    }
    total = _dev_n(task)
    rows: list[ComparisonRow] = []
    evaluations: dict[str, Evaluation] = {}
    observed_evaluations: list[Evaluation] = []
    population_evaluations: list[Evaluation] = []
    incomplete: dict[str, bool] = {}
    notices = [
        "development cases only; the held-out test share was not scored or exposed in this comparison",
        "constraints are reference metadata; this comparison does not filter or select candidates",
    ]
    for item in inputs:
        row, evaluation, chart_notice = _actual_row(item, task, total, include_charts=include_charts)
        rows.append(row)
        if chart_notice:
            notices.append(chart_notice)
        if evaluation is not None:
            observed_evaluations.append(evaluation)
        incomplete[item.candidate.name] = bool(evaluation is not None and evaluation.failures.missing)
        if evaluation is not None and not evaluation.failures.missing:
            population_evaluations.append(evaluation)
        if evaluation is not None and evaluation.n and not evaluation.failures.missing and not row.excluded:
            evaluations[item.candidate.name] = evaluation

    definitions = _metric_definitions(task, observed_evaluations)
    rows_by_name = {r.candidate: r for r in rows}
    for item in inputs:
        row = rows_by_name[item.candidate.name]
        row.metrics = _row_metrics(
            evaluations.get(item.candidate.name),
            definitions,
            incomplete=incomplete.get(item.candidate.name, False),
        )
    ordered = rows

    if len({tuple(sorted(e.answered_ids)) for e in population_evaluations}) > 1:
        notices.append("answered populations differ across candidates; each candidate remains visible and no candidate is selected")
    latency_notice = select.unlike(list(evaluations.values()))
    if latency_notice:
        notices.append(latency_notice.en(task.id))
    run_digests = {item.candidate.name: item.run_digest for item in inputs}
    if task.data_digest != data_digest or task.evaluation_contract_digest != contract_digest or task.input_adapter_digest != adapter_digest:
        raise ConfigError(f"{task.id}: comparison data, adapter or evaluation contract changed during comparison")
    current_run_digests = {item.candidate.name: _run_digest(item.path) for item in inputs}
    if current_run_digests != run_digests:
        raise ConfigError(f"{task.id}: run evidence changed during comparison; compare again")
    current_bindings = {
        item.candidate.model: execution_digest(task.where.lineup().resolved(item.candidate.model), '')
        if item.spec is not None else 'unresolved' for item in inputs
    }
    if current_bindings != binding_digests:
        raise ConfigError(f"{task.id}: model connection conditions changed during comparison; compare again")
    comparison_id = digest({
        "schema": "s1flow/comparison@2", "task": task.id, "variants": _variants(task, variants),
        "data_digest": data_digest, "evaluation_contract_digest": contract_digest,
        "input_adapter_digest": adapter_digest, "binding_digests": binding_digests, "run_digests": run_digests,
    })
    excluded_count = sum(bool(row.excluded) for row in ordered)
    if excluded_count:
        notices.append(f"{excluded_count} candidates have missing or ineligible evidence; see each candidate's excluded reasons")
    return Comparison(
        id=comparison_id, task=task.id, source=task.source, at=clock.now(), scope="dev",
        question_type=task.kind.type, kind_params=task.kind_params,
        objective=task.primary, constraints=task.constraints,
        data_digest=data_digest, evaluation_contract_digest=contract_digest, input_adapter_digest=adapter_digest,
        binding_digests=binding_digests, run_digests=run_digests,
        n=total, metric_definitions=definitions, notices=notices, candidates=ordered,
    )


def read(path: Path | str) -> Comparison:
    """Read a previously saved comparison; no task or current state is consulted."""
    path = Path(path)
    try:
        return Comparison.model_validate(json.loads(path.read_text()))
    except (OSError, ValueError) as exc:
        raise ConfigError(f"{path}: invalid comparison snapshot: {exc}") from None

def _row_summary(row: ComparisonRow) -> dict[str, Any]:
    """The bounded candidate shape used by ``report --json``."""
    calls = row.calls
    latency = {
        "p50_ms": None if calls.latency is None else calls.latency.p50_ms,
        "p90_ms": None if calls.latency is None else calls.latency.p90_ms,
        "p99_ms": None if calls.latency is None else calls.latency.p99_ms,
        "concurrency": [] if calls.latency is None else calls.latency.concurrency,
        "concurrency_unknown": None if calls.latency is None else calls.latency.concurrency_unknown,
    }
    return {
        "candidate": row.candidate, "model": row.model, "variant": row.variant,
        "n": row.n, "value": row.value, "interval": row.interval,
        "rule": None if row.rule is None else row.rule.model_dump(mode="json"),
        "metrics": {key: estimate.model_dump(mode="json") for key, estimate in row.metrics.items()},
        "basis": row.measurement.distribution,
        "excluded": row.excluded, "adoption_blocked": row.adoption_blocked,
        "probabilities": row.probabilities,
        "selection_basis": ("box confidence" if row.question.type == "box" else "selected-answer probability") if row.probabilities else None,
        "failures": {"calls": row.failures.calls, "failed": row.failures.failed, "unsupported": row.failures.unsupported,
                      "data_errors": row.failures.data_errors, "unlabeled": row.failures.unlabeled,
                      "never_asked": row.failures.never_asked, "failed_cases": row.failures.failed_cases,
                      "refused_cases": row.failures.refused_cases},
        "calls": {"latency": latency, "cost_per_10k_usd": calls.cost_per_10k_usd,
                  "cost_total_usd": calls.cost_total_usd, "cost_source": calls.cost_source,
                  "cost_unknown": calls.cost_unknown},
        "measurement": row.measurement.model_dump(mode="json"),
    }


def summary(comparison: Comparison, *, offset: int = 0, limit: int = 12, candidate: str | None = None,
            snapshot: str | None = None) -> dict[str, Any]:
    rows = comparison.candidates
    if candidate is not None:
        selected = next((r for r in rows if r.candidate == candidate), None)
        if selected is None:
            raise NotFound(f"no candidate {candidate!r}; candidates: {', '.join(r.candidate for r in rows) or 'none'}")
        detail_payload: dict[str, Any] = {
            "schema": "s1flow/comparison-detail@2", "task": comparison.task, "id": comparison.id,
            "scope": comparison.scope, "as_of": comparison.at,
            "question_type": comparison.question_type,
            "kind_params": comparison.kind_params.model_dump(mode="json"),
            "scoring_population": "answered labelled dev cases",
            "provenance": "saved snapshot" if snapshot else "current comparison",
            "objective": comparison.objective.model_dump(mode="json"),
            "constraints": comparison.constraints.model_dump(mode="json"),
            "metric_definitions": [definition.model_dump(mode="json") for definition in comparison.metric_definitions],
            "candidate": selected.model_dump(mode="json", exclude={"charts"}),
        }
        if snapshot:
            detail_payload["snapshot"] = snapshot
            detail_payload["current_certified"] = False
        return detail_payload
    page = rows[offset: offset + limit]
    payload: dict[str, Any] = {
        "schema": "s1flow/comparison-summary@2", "task": comparison.task, "source": comparison.source[:500],
        "id": comparison.id, "as_of": comparison.at, "scope": comparison.scope, "question_type": comparison.question_type,
        "kind_params": comparison.kind_params.model_dump(mode="json"),
        "scoring_population": "answered labelled dev cases",
        "objective": comparison.objective.model_dump(mode="json"),
        "constraints": comparison.constraints.model_dump(mode="json"),
        "n": comparison.n, "candidate_count": len(rows), "offset": offset, "limit": limit,
        "metric_definitions": [definition.model_dump(mode="json") for definition in comparison.metric_definitions],
        "provenance": "saved snapshot" if snapshot else "current comparison",
        "candidates": [_row_summary(row) for row in page], "notices": [n[:500] for n in comparison.notices[:12]],
    }
    if snapshot:
        payload["snapshot"] = snapshot
        payload["current_certified"] = False
    return payload


def text(comparison: Comparison, *, offset: int = 0, limit: int = 12, candidate: str | None = None,
         snapshot: str | None = None) -> str:
    if candidate is not None:
        row = next((r for r in comparison.candidates if r.candidate == candidate), None)
        if row is None:
            raise NotFound(f"no candidate {candidate!r}; candidates: {', '.join(r.candidate for r in comparison.candidates) or 'none'}")
        detail = summary(comparison, candidate=candidate, snapshot=snapshot)["candidate"]
        return "\n".join([
            f"{comparison.task} · {row.candidate}: n {row.n}, value {row.value if row.value is not None else '—'}"
            + (f" [{row.interval[0]:.4g}, {row.interval[1]:.4g}]" if row.interval else ""),
            f"scope: {comparison.scope}; as-of: {comparison.at}; provenance: {('saved snapshot (offline; not current certification)' if snapshot else 'current comparison')}",
            f"interpretation: {comparison.question_type} {json.dumps(comparison.kind_params.model_dump(mode='json'))}",
            f"question: {json.dumps(detail['question'], ensure_ascii=False)}",
            f"metric definitions: {json.dumps([d.model_dump(mode='json') for d in comparison.metric_definitions], ensure_ascii=False)}",
            f"metrics: {json.dumps(detail['metrics'], ensure_ascii=False)}",
            f"rule: {json.dumps(detail['rule'], ensure_ascii=False)}",
            f"calls: {json.dumps(detail['calls'], ensure_ascii=False)}",
            f"failures: {json.dumps(detail['failures'], ensure_ascii=False)}",
            f"measurement: {json.dumps(detail['measurement'], ensure_ascii=False)}",
            f"excluded: {', '.join(row.excluded) or 'none'}",
            f"adoption: {', '.join([*row.excluded, *row.adoption_blocked]) or 'eligible; explicit adoption required'}",
        ])
    provenance = f"snapshot {snapshot} as of {comparison.at} (offline; not current certification)" if snapshot else f"current as of {comparison.at}"
    objective = comparison.objective
    constraints = comparison.constraints.model_dump(mode="json")
    lines = [f"{comparison.task}: {comparison.n} dev cases, {len(comparison.candidates)} candidates, {provenance}",
             f"id: {comparison.id}; scope: {comparison.scope}; objective: {objective.label} ({'max' if objective.maximize else 'min'}); constraints: {json.dumps(constraints, ensure_ascii=False)}",
             "selection: none; candidates are shown in model and variant order"]
    lines.append("metric definitions: " + json.dumps([definition.model_dump(mode="json") for definition in comparison.metric_definitions], ensure_ascii=False))
    for row in comparison.candidates[offset: offset + limit]:
        value = "—" if row.value is None else f"{row.value:.4g}"
        interval = "" if row.interval is None else f" [{row.interval[0]:.4g}, {row.interval[1]:.4g}]"
        p90 = "unknown" if row.calls.latency is None else f"{row.calls.latency.p90_ms:.4g}ms"
        p99 = "unknown" if row.calls.latency is None else f"{row.calls.latency.p99_ms:.4g}ms"
        cost = "unknown" if row.calls.cost_per_10k_usd is None or row.calls.cost_unknown else f"${row.calls.cost_per_10k_usd:.4g}/10k ({row.calls.cost_source or 'unknown'})"
        why = f" ({'; '.join(row.excluded)})" if row.excluded else ""
        blocked = f"; adoption blocked: {', '.join(row.adoption_blocked)}" if row.adoption_blocked else ""
        metric_text = "; ".join(f"{key}={format(estimate.value, '.4g') if estimate.value is not None else '—'}" for key, estimate in row.metrics.items())
        lines.append(f"  {row.candidate:<28} n={row.n:<4} value={value}{interval} metrics={metric_text or '—'} cost={cost} basis={row.measurement.distribution} p90={p90} p99={p99}{why}{blocked}")
    if len(comparison.candidates) > offset + limit:
        lines.append(f"… {len(comparison.candidates) - offset - limit} more; use --offset/--limit")
    if comparison.notices:
        lines.append("notices: " + "; ".join(n[:240] for n in comparison.notices[:3]))
    return "\n".join(lines)
