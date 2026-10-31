"""What each type of question is measured by, and what each of its numbers is called, wherever it is shown:
the objectives a kind takes, the numbers it reports, the measures that exist for it and the comparison's metric
definitions. One row per kind. Names, units and directions are METRICS' (declare.py), the rest MEASURES'."""

from __future__ import annotations

from typing import Any

import pytest

from s1flow.client import Boolean, Box, Choice, Score
from s1flow.eval import Task, comparison
from s1flow.eval.candidate import Candidate
from s1flow.eval.evaluation import Estimate, Evaluation, Failures, Selective
from s1flow.eval.objectives.measure import MEASURES, measured_as
from s1flow.objectives import AUROC, MAE, QWK, Accuracy, F1, MacroF1
from s1flow.policies.kinds import KindParams

AB = {"a": None, "b": None}
PER_CASE = "over answered labelled dev cases"
P = "genuine model probabilities"
SELECTIVE = [
    ("coverage:0.95", "coverage (target reference 95%)", "share", "max",
     "target reference 0.95; target-specific CV chosen rule; observed accepted / answered labelled dev cases"),
    ("accepted_accuracy:0.95", "accepted accuracy (target reference 95%)", "share", "max",
     "target reference 0.95; target-specific CV chosen rule; observed correct accepted / accepted labelled dev cases"),
]


def binary(reading: str) -> list[tuple[str, str, str, str, str]]:
    return [
        ("accuracy", "accuracy (all)", "share", "max", f"{reading}; correct / answered labelled dev cases"),
        ("f1", "F1", "number", "max", f"{reading}; harmonic mean of precision and recall {PER_CASE}"),
        ("precision", "precision", "share", "max", f"{reading}; true positives / predicted positives among answered labelled dev cases"),
        ("recall", "recall", "share", "max", f"{reading}; true positives / labelled positives among answered labelled dev cases"),
        ("auroc", "AUROC", "number", "max", f"{P}; binary positive-vs-negative AUROC {PER_CASE}"),
        ("brier", "Brier score", "number", "min", f"{P}; binary Brier score {PER_CASE}"),
        ("ece", "ECE", "number", "min", f"{P}; calibration of answer correctness {PER_CASE}"),
        ("objective:accuracy{}", "accuracy (all)", "share", "max",
         "configured primary objective; CV chosen rule; denominator: answered labelled dev cases"),
        *SELECTIVE,
    ]


BINARY_OBJECTIVES = ("accuracy", "coverage", "recall", "expected_loss", "auroc", "f1", "loss")
BINARY_MEASURES = ["accuracy", "auroc", "brier", "coverage", "ece", "expected_loss", "f1", "loss", "precision", "recall"]
CHOICE_READING = "plain choice reading: selected option with highest probability (default rule)"
SCORE_READING = "plain score reading: the expected level, rounded (.5 up)"
BOX_READING = "plain box reading: correct at IoU >= 0.5"

# kind: question, params, Kind.objectives, Kind.report, the measures that exist, and the comparison's metric
# definitions (key, label, unit, direction, basis) with probabilities and one coverage target
KINDS: dict[str, tuple[Any, KindParams, tuple[str, ...], tuple[str, ...], list[str], list[tuple[str, str, str, str, str]]]] = {
    "boolean": (
        Boolean(instructions="?"), KindParams(), BINARY_OBJECTIVES, ("f1", "precision", "recall"), BINARY_MEASURES,
        binary("plain binary reading: P(true) >= 0.5"),
    ),
    "positive choice": (
        Choice(instructions="?", criteria=AB), KindParams(positive="a"), BINARY_OBJECTIVES, ("f1", "precision", "recall"), BINARY_MEASURES,
        binary("plain binary reading: P(a) >= 0.5"),
    ),
    "choice": (
        Choice(instructions="?", criteria=AB), KindParams(), ("accuracy", "coverage", "auroc", "macro_f1", "loss"), ("macro_f1",),
        ["accuracy", "auroc", "brier", "coverage", "ece", "loss", "macro_f1"],
        [
            ("accuracy", "accuracy (all)", "share", "max", f"{CHOICE_READING}; correct / answered labelled dev cases"),
            ("macro_f1", "macro-F1", "number", "max", f"{CHOICE_READING}; mean of per-class F1 {PER_CASE}"),
            ("auroc", "AUROC", "number", "max", f"{P}; macro one-v-rest AUROC over options and answered labelled dev cases"),
            ("brier", "Brier score", "number", "min", f"{P}; multiclass Brier score {PER_CASE}"),
            ("ece", "ECE", "number", "min", f"{P}; calibration of selected-answer correctness {PER_CASE}"),
            ("objective:accuracy{}", "accuracy (all)", "share", "max",
             f"configured primary objective; {CHOICE_READING}; denominator: answered labelled dev cases"),
            *SELECTIVE,
        ],
    ),
    "score": (
        Score(instructions="?", criteria=["low", "mid", "high"]), KindParams(), ("mae", "qwk", "accuracy", "coverage", "auroc"), ("mae", "qwk"),
        ["accuracy", "auroc", "brier", "coverage", "ece", "mae", "qwk"],
        [
            ("accuracy", "accuracy (all)", "share", "max", f"{SCORE_READING}; correct / answered labelled dev cases"),
            ("mae", "MAE (levels)", "number", "min", f"expected level; mean absolute error in levels {PER_CASE}"),
            ("qwk", "QWK", "number", "max", f"{SCORE_READING}; quadratic weighted kappa {PER_CASE}"),
            ("auroc", "AUROC", "number", "max", f"{P}; mean over the cuts k of AUROC(label >= k, P(level >= k)) {PER_CASE}"),
            ("brier", "Brier score", "number", "min", f"{P}; ranked probability score over (levels - 1), {PER_CASE}"),
            ("ece", "ECE", "number", "min", f"{P}; calibration of the rounded level's correctness {PER_CASE}"),
            ("objective:mae{}", "MAE (levels)", "number", "min",
             f"configured primary objective; {SCORE_READING}; denominator: answered labelled dev cases"),
            *SELECTIVE,
        ],
    ),
    "box": (
        Box(instructions="?"), KindParams(), ("accuracy", "coverage", "auroc", "mean_iou"), ("mean_iou",),
        ["accuracy", "auroc", "brier", "coverage", "ece", "mean_iou"],
        [
            ("accuracy", "accuracy (all)", "share", "max", f"{BOX_READING}; correct / answered labelled dev cases"),
            ("mean_iou", "mean IoU", "number", "max", f"{BOX_READING}; mean IoU {PER_CASE}"),
            ("auroc", "AUROC", "number", "max", f"recorded box confidence; hit-ranking AUROC {PER_CASE}"),
            ("brier", "Brier score", "number", "min", f"recorded box confidence; Brier score of hit correctness {PER_CASE}"),
            ("ece", "ECE", "number", "min", f"recorded box confidence; calibration of hit correctness {PER_CASE}"),
            ("objective:accuracy{}", "accuracy (all)", "share", "max",
             f"configured primary objective; {BOX_READING}; denominator: answered labelled dev cases"),
            *SELECTIVE,
        ],
    ),
}


def _evaluation() -> Evaluation:
    """Scored with probabilities, at the default coverage target: every metric a comparison can define."""
    selective = Selective(target_accuracy=0.95, coverage=Estimate(value=0.5), accuracy=0.96, n=5, errors=0, lower=0.9,
                          labels_needed=None, min_probability=0.9)
    return Evaluation(candidate=Candidate(model="m"), answered_by="m", answered_by_all=["m"], n=10, probabilities=True,
                      failures=Failures(calls=10, failed=0, unsupported=0, data_errors=0, unlabeled=0), selective=[selective])


@pytest.mark.parametrize("name", KINDS)
def test_each_kind_names_its_metrics_one_way(name):
    question, params, objectives, reported, measures, definitions = KINDS[name]
    task = Task(id="t", cases="x", state=lambda r: r, question=question, label=lambda r: r, kind_params=params)
    kind = task.kind
    assert kind.objectives == objectives
    assert kind.report == reported
    assert sorted(m for m, measured in MEASURES if measured == measured_as(kind)) == measures
    got = [(d.key, d.label, d.unit, d.direction, d.basis) for d in comparison._metric_definitions(task, [_evaluation()])]
    assert got == definitions


@pytest.mark.parametrize("make, label, unit, direction", [
    (AUROC, "AUROC", "number", "max"), (Accuracy, "accuracy (all)", "share", "max"), (F1, "F1", "number", "max"),
    (MacroF1, "macro-F1", "number", "max"), (MAE, "MAE (levels)", "number", "min"), (QWK, "QWK", "number", "max"),
])
def test_each_objective_without_params_is_named_as_its_metric(make, label, unit, direction):
    o = make()
    assert (o.label, o.unit, o.direction) == (label, unit, direction)
