"""Evaluation semantics over the runtime's validated readings.

The runtime owns interpretation and label validation. These explicit subclasses add
only scoring, supported objectives and report measures; they never replace reading.
"""
import math
from typing import Any, ClassVar, Protocol

from ..client.answers import BoxEdges
from ..client.boxes import iou
from ..client.questions import Question
from ..policies import kinds as runtime
from ..policies.kinds import ABSENT, KindParams, Reading


class Kind(runtime.Kind, Protocol):
    @property
    def objectives(self) -> tuple[str, ...]: ...
    @property
    def report(self) -> tuple[str, ...]: ...
    def correct(self, label: Any, r: Reading | None) -> bool: ...
    def brier(self, label: Any, r: Reading) -> float: ...


class _Scoring:
    def correct(self, label: Any, r: Reading | None) -> bool:
        return r is not None and r.value == label

    def brier(self, label: Any, r: Reading) -> float:
        raise NotImplementedError("this question has no per-case Brier score")


class _BinaryScoring(_Scoring):
    objectives: ClassVar[tuple[str, ...]] = ("accuracy", "coverage", "recall", "expected_loss", "auroc", "f1", "loss")
    report: ClassVar[tuple[str, ...]] = ("f1", "precision", "recall")

    def brier(self, label: Any, r: Reading) -> float:
        assert r.p_positive is not None
        return float((r.p_positive - label) ** 2)


class BooleanKind(_BinaryScoring, runtime.BooleanKind):
    pass


class PositiveChoiceKind(_BinaryScoring, runtime.PositiveChoiceKind):
    pass


class ChoiceKind(_Scoring, runtime.ChoiceKind):
    objectives: ClassVar[tuple[str, ...]] = ("accuracy", "coverage", "auroc", "macro_f1", "loss")
    report: ClassVar[tuple[str, ...]] = ("macro_f1",)

    def brier(self, label: Any, r: Reading) -> float:
        assert r.distribution is not None
        return sum((p - (1.0 if k == label else 0.0)) ** 2 for k, p in zip(self.keys, r.distribution)) / 2


class ScoreKind(_Scoring, runtime.ScoreKind):
    """Right when the expected level, rounded, is the label; how far off is MAE, agreement over the levels QWK."""

    objectives: ClassVar[tuple[str, ...]] = ("mae", "qwk", "accuracy", "coverage", "auroc")
    report: ClassVar[tuple[str, ...]] = ("mae", "qwk")

    def brier(self, label: Any, r: Reading) -> float:
        """The ranked probability score: the squared gaps of the two cumulative distributions, over L - 1."""
        assert r.distribution is not None
        cum, gap = 0.0, 0.0
        for j, p in enumerate(r.distribution[:-1]):
            cum += p
            gap += (cum - (1.0 if label <= j else 0.0)) ** 2
        return gap / (self.levels - 1)


class BoxKind(_Scoring, runtime.BoxKind):
    objectives: ClassVar[tuple[str, ...]] = ("accuracy", "coverage", "auroc", "mean_iou")
    report: ClassVar[tuple[str, ...]] = ("mean_iou",)

    def correct(self, label: Any, r: Reading | None) -> bool:
        return r is not None and isinstance(r.value, BoxEdges) and iou(r.value, BoxEdges.model_validate(label)) >= self.hit_iou


class _ReadScoring(_Scoring):
    """Right when the value read is the label's, or nothing was read from a case labelled absent."""

    objectives: ClassVar[tuple[str, ...]] = ("accuracy", "coverage", "auroc")
    report: ClassVar[tuple[str, ...]] = ("value_accuracy", "absent_accuracy")

    def correct(self, label: Any, r: Reading | None) -> bool:
        if r is None:
            return False
        if label is ABSENT or r.value is None:
            return label is ABSENT and r.value is None
        return self.same(label, r.value)

    def same(self, label: Any, value: Any) -> bool:
        return bool(value == label)


class TextKind(_ReadScoring, runtime.TextKind):
    pass


class NumberKind(_ReadScoring, runtime.NumberKind):
    def same(self, label: Any, value: Any) -> bool:
        return math.isclose(value, label, rel_tol=1e-9, abs_tol=1e-12)


class DateKind(_ReadScoring, runtime.DateKind):
    pass


class EstimateKind(_Scoring, runtime.EstimateKind):
    """Right within `tolerance` of the label; how far off is the mean error."""

    objectives: ClassVar[tuple[str, ...]] = ("mean_error", "accuracy", "coverage", "auroc")
    report: ClassVar[tuple[str, ...]] = ("mean_error",)

    def correct(self, label: Any, r: Reading | None) -> bool:
        # the float's own error on top: 0.1 + 0.2 is within 0.3 of 0
        return r is not None and isinstance(r.value, float) and abs(r.value - label) <= self.tolerance * (1 + 1e-9) + 1e-12


def kind_of(question: Question, params: KindParams = KindParams()) -> Kind:
    kind = runtime.kind_of(question, params)
    if isinstance(kind, runtime.TextKind):
        return TextKind()
    if isinstance(kind, runtime.NumberKind):
        return NumberKind()
    if isinstance(kind, runtime.DateKind):
        return DateKind()
    if isinstance(kind, runtime.EstimateKind):
        return EstimateKind(**kind.model_dump())
    if isinstance(kind, runtime.PositiveChoiceKind):
        return PositiveChoiceKind(**kind.model_dump())
    if isinstance(kind, runtime.ChoiceKind):
        return ChoiceKind(**kind.model_dump())
    if isinstance(kind, runtime.ScoreKind):
        return ScoreKind(**kind.model_dump())
    if isinstance(kind, runtime.BoxKind):
        return BoxKind(**kind.model_dump())
    return BooleanKind()
