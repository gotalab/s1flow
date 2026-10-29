"""Evaluation semantics over the runtime's validated readings.

The runtime owns interpretation and label validation. These explicit subclasses add
only scoring, supported objectives and report measures; they never replace reading.
"""
from __future__ import annotations

from typing import Any, ClassVar, Protocol

from ..client.answers import BoxEdges
from ..client.boxes import iou
from ..client.questions import Question
from ..policies import kinds as runtime
from ..policies.kinds import KindParams, Reading


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
    # Client supports Score, but no scoring contract is implemented for Task.
    objectives: ClassVar[tuple[str, ...]] = ()
    report: ClassVar[tuple[str, ...]] = ()


class BoxKind(_Scoring, runtime.BoxKind):
    objectives: ClassVar[tuple[str, ...]] = ("accuracy", "coverage", "auroc", "mean_iou")
    report: ClassVar[tuple[str, ...]] = ("mean_iou",)

    def correct(self, label: Any, r: Reading | None) -> bool:
        return r is not None and isinstance(r.value, BoxEdges) and iou(r.value, BoxEdges.model_validate(label)) >= self.hit_iou


def kind_of(question: Question, params: KindParams = KindParams()) -> Kind:
    kind = runtime.kind_of(question, params)
    if isinstance(kind, runtime.PositiveChoiceKind):
        return PositiveChoiceKind(**kind.model_dump())
    if isinstance(kind, runtime.ChoiceKind):
        return ChoiceKind(**kind.model_dump())
    if isinstance(kind, runtime.ScoreKind):
        return ScoreKind(**kind.model_dump())
    if isinstance(kind, runtime.BoxKind):
        return BoxKind(**kind.model_dump())
    return BooleanKind()
