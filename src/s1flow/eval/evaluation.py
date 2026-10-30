"""What an evaluation of one candidate measured: the one shape that choosing, reports, policies and
checks read. `eval.metrics.evaluate` makes it from the runs; nothing else computes these numbers.

Two groups that never share a field: what was measured on the answers (`objective`, `tiebreak`, accuracy, ...) and
what the calls took (`calls`: latency, API cost, throughput). The calls limit candidates (Constraints) and
order the tied ones where `tiebreak` lists "latency" and "cost" (select.py); they are never an objective.

Every value is measured out of fold on the cases outside the held-out test share (a threshold is
chosen on the fit side and applied to the other), with a 95% bootstrap interval where one is
computed. `test` is the held-out share, read at the thresholds chosen on the rest.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ..client.models import Price
from .candidate import Candidate
from ..policies.rule import DecisionRule
from .objectives.declare import Objective

Interval = tuple[float, float]
DistributionEvidence = Literal['native', 'sampled', 'none', 'mixed', 'unknown']


class _Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Estimate(_Frozen):
    value: float | None
    interval: Interval | None = None


class Failures(_Frozen):
    """`calls` to `unlabeled` count call records; the `*_cases` and `never_asked` count labelled cases.
    A case never asked or with every call failed has no answer the model gave: a candidate missing one is
    not compared with the others (`missing`). A refused case is the model's limit, left out of its denominator.
    The case counts are None in an evaluation stored before 2026-10-19 (not counted then)."""

    calls: int  # call records scored, one per case
    failed: int
    unsupported: int  # refused before or by the provider
    data_errors: int  # the task's own errors
    unlabeled: int
    never_asked: int | None = None  # labelled cases with no record under the question
    failed_cases: int | None = None  # labelled cases asked whose every call failed
    refused_cases: int | None = None  # labelled cases refused or unsupported, none answered

    @property
    def missing(self) -> int:
        """Labelled cases this candidate has no answer to for want of a call: never asked, or every call failed."""
        return (self.never_asked or 0) + (self.failed_cases or 0)


class Selective(_Frozen):
    """Answer sure only where the probability reaches a cut, keeping `target_accuracy` on the sure answers."""

    target_accuracy: float
    coverage: Estimate  # share sure
    accuracy: float | None  # of the sure share
    n: int  # sure
    errors: int
    lower: float  # one-sided 95% Clopper-Pearson lower bound of `accuracy`
    labels_needed: int | None  # labels still needed, at this error rate, before `lower` reaches the target
    min_probability: float | None  # the cut chosen on all the dev cases; None when no cut keeps the target


class ObjectiveScore(_Frozen):
    """One of the task's objectives."""

    objective: Objective
    value: float | None
    interval: Interval | None = None
    rule: DecisionRule | None = None  # the rule it sets, chosen on all the dev cases: its one field (objective.sets), a min probability or a P(positive) cut. None: it sets none, none keeps its constraint, or in `tiebreak` (read at the primary's)
    constraint: float | None = None  # the share its constraint keeps (Coverage: sure accuracy; Recall: false alarms), out of fold: it can pass the bound a little

    @property
    def chosen(self) -> float | None:
        """The value of the rule field its objective sets; None when there is none."""
        s = self.objective.sets
        return None if self.rule is None or s is None else getattr(self.rule, s)


class ErrorLossThreshold(_Frozen):
    """A binary task's P(positive) cut, chosen as ExpectedLoss chooses it on the task's error losses (else 1 and 1)."""

    accuracy: float  # out of fold, at the cuts chosen on each fit side
    misses: int
    false_alarms: int
    median: float  # of the cuts chosen per fold
    chosen: float  # on all the dev cases: what a policy uses


class SweepRow(_Frozen):
    """Per run: a positive below the threshold is a miss, a negative at or above it a false alarm."""

    threshold: float
    misses: int
    positives: int
    false_alarms: int
    negatives: int


class Floor(_Frozen):
    """One of the task's floors (Constraints.min_precision, min_recall) at the threshold the primary objective sets."""

    what: str  # precision | recall
    bound: float
    rate: float | None  # out of fold, at the cuts chosen on each fit side (with the floors kept there): it can pass the floor a little
    test: tuple[int, int] | None = None  # on the test share at the dev cases' threshold: (cases that count, out of)


class TestResult(_Frozen):
    n: int
    accuracy: float  # at the plain argmax
    coverage: float  # at the dev's min probability for the first target
    sure_accuracy: float | None  # accuracy of that covered share
    tuned_accuracy: float | None  # binary: at the dev's chosen P(positive) cut
    primary: Estimate  # the task's primary objective on the test share
    constraint: tuple[int, int] | None = None  # the primary's constraint on the test share: (cases that count, out of)


class HighConfidenceError(_Frozen):
    id: str
    label: bool | str
    predicted: bool | str
    probability: float


class Latency(_Frozen):
    """Per answered call: the answering attempt alone (retries left out)."""

    n: int
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    spread: float | None  # p99 / p50: 1 is steady, 3 has a long tail
    retried: int  # calls that needed a retry before answering
    unrecorded: int  # saved before retries were kept: may include backoff
    concurrency: list[int]
    concurrency_unknown: int


class Throughput(_Frozen):
    per_min: float
    seconds: float
    calls: int
    concurrency: int
    measured: bool  # a run that made every call itself; else latency summed over the concurrency


class Calls(_Frozen):
    """What the calls took rather than what they answered: how long an app waits and what the model charges
    (API cost). Read from the call records alone (metrics.calls)."""

    latency: Latency | None = None  # per answered call
    # Per dev case, its answered call's latency, at p90, with an interval from the
    # evaluation's resample of the dev cases: what `tiebreak`'s "latency" orders the tied candidates by (select.py)
    case_latency_p90_ms: Estimate | None = None
    throughput: Throughput | None = None
    # API cost, over the calls whose cost is known (`cost_unknown` are not, and count as nothing, not as free).
    cost_per_10k_usd: float | None = None
    cost_total_usd: float | None = None
    cost_source: Literal["billed", "list", "mixed"] | None = None  # list: an estimate, from `price` and the recorded tokens; None: unknown
    cost_unknown: int = 0
    price: Price | None = None  # the list price the estimate used (s1flow.toml, with its as_of)


class Evaluation(_Frozen):
    candidate: Candidate
    answered_by: str | None  # the answering model scored (Response.answered_by, as its run records name it)
    answered_by_all: list[str]  # every answering model on file, latest first
    answered_ids: list[str] = []  # exact dev population for automatic comparisons
    n: int  # labelled dev cases scored
    probabilities: bool  # False when the model returned single answers only
    failures: Failures
    split: str | None = None
    split_method: str | None = None
    accuracy: Estimate | None = None
    measures: dict[str, Estimate] = {}  # the kind's own numbers, by name (Kind.report): f1, macro_f1, mean_iou
    auroc: Estimate | None = None
    brier: float | None = None
    ece: float | None = None
    selective: list[Selective] = []  # one per target accuracy, the report's first
    error_loss_threshold: ErrorLossThreshold | None = None
    floors: list[Floor] = []  # the task's floors, when it sets any
    sweep: list[SweepRow] | None = None
    objective: ObjectiveScore | None = None  # the task's objective (None: nothing was scored)
    tiebreak: list[ObjectiveScore] = []  # the task's `tiebreak`, in its order, read at the objective's rule
    test: TestResult | None = None
    high_confidence_errors: list[HighConfidenceError] = []
    calls: Calls = Calls()

    @property
    def primary(self) -> ObjectiveScore | None:
        return self.objective

    @property
    def scores(self) -> list[ObjectiveScore]:
        """The objective's score, then those of the objectives in `tiebreak`, in its order."""
        return [] if self.objective is None else [self.objective, *self.tiebreak]


COST_NOTE = "Where the API costs come from: "  # the line a report and a check write when an API cost is an estimate or not known


def cost_note(costs: list[tuple[str, str | None, str | None, int]]) -> str | None:
    """(name, cost source, the list price's as_of, calls whose cost is not known) per candidate -> one line;
    None when every cost shown is what was billed."""
    billed = [n for n, s, _, _ in costs if s == "billed"]
    listed = [f"{n} (list price of {a})" if a else n for n, s, a, _ in costs if s == "list"]
    mixed = [n for n, s, _, _ in costs if s == "mixed"]
    unknown = [f"{n} {u}" for n, _, _, u in costs if u]
    if not (listed or mixed or unknown):
        return None
    parts = [f"billed: {', '.join(billed)}"] if billed else []
    parts += [f"estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): {', '.join(listed)}"] if listed else []
    parts += [f"billed and estimated summed: {', '.join(mixed)}"] if mixed else []
    parts += [f"calls whose API cost is not known (left out of the mean, not counted as 0): {', '.join(unknown)}"] if unknown else []
    tail = " Billed and estimated API costs sit side by side, so their differences do not compare as they are." if billed and (listed or mixed) else ""
    return COST_NOTE + "; ".join(parts) + "." + tail


class _ChartModel(_Frozen):
    model_config = ConfigDict(extra='forbid', frozen=True, allow_inf_nan=False)


class ThresholdPoint(_ChartModel):
    threshold: float = Field(ge=0, le=1)
    objective: float | None
    precision: float | None
    recall: float | None
    misses: int
    false_alarms: int


class ProbabilityBin(_ChartModel):
    lower: float
    upper: float
    positives: int
    negatives: int


class CalibrationPoint(_ChartModel):
    probability: float
    observed: float
    n: int


class SelectionPoint(_ChartModel):
    """One exploratory dev point for the minimum probability selection curve.

    ``coverage`` is the share of answered labelled dev cases accepted at this
    cut.  ``sure_accuracy`` is intentionally nullable: an empty accepted
    set has no accuracy to report.  Counts are kept alongside the rates so a
    renderer never has to reconstruct them from the chart.
    """

    min_probability: float = Field(ge=0, le=1)
    coverage: float = Field(ge=0, le=1)
    sure_accuracy: float | None = Field(ge=0, le=1)
    accepted: int = Field(ge=0)
    correct: int = Field(ge=0)
    total: int = Field(ge=0)


class ChartData(_ChartModel):
    """Report-owned dev series; exploratory sweeps are distinct from CV estimates.

    ``selection_sweep`` holds dev rates while its selected cut, when present,
    is the minimum probability chosen on all dev cases.  For binary kinds the
    candidate's selected P(positive) threshold stays fixed during that sweep.
    """
    scope: Literal["dev"] = "dev"
    rule: Literal["out-of-fold"] = "out-of-fold"
    n: int
    raw_value: float | None
    cv_value: float | None
    threshold_sweep: list[ThresholdPoint] = []
    distribution: list[ProbabilityBin] = []
    calibration: list[CalibrationPoint] = []
    selection_sweep: list[SelectionPoint] = []
    selection_basis: Literal["selected-answer probability", "box confidence"] | None = None
    selection_unavailable: str | None = None
    unavailable: str | None = None


class ChartSummary(_ChartModel):
    """Dev comparison findings computed by the report, not its renderer."""
    candidate_count: int
    improved_count: int
    largest_change_candidate: str | None = None
    largest_change_raw: float | None = None
    largest_change_cv: float | None = None
    cost_quality_frontier: list[str] = []
    frontier_axes: Literal["objective,cost"] = "objective,cost"
