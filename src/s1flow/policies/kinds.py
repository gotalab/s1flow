"""What s1flow knows about each type of question, in one place: what a label is, how the answers
to one case become a `Reading`, which rules apply, and whether
a policy ships it. Adding a type of question is adding a class here.

    kind = kind_of(question, KindParams())          # a task's or a policy's question, with what its type leaves open
    kind.read(answers, rule)                        # average the answers, then read the average
    kind.label_error(label)                            # cases check and feedback
    same_label(kind, a, b)                             # two labels that say the same (review, cases check)

| kind               | label                        | value                                   | probability          | rule sets               |
|--------------------|------------------------------|-----------------------------------------|----------------------|----------------------------|
| boolean            | true / false                 | P(true) >= threshold                    | of the value         | threshold, min_probability |
| choice             | an option's key              | the most probable option, on average    | of that option       | min_probability            |
| choice + positive  | true / false                 | P(positive) >= threshold                | of the value         | threshold, min_probability |
| multichoice        | the options that apply, []   | each option whose P >= 0.5 (P from its probability, else 1 / 0 from its choices) | of the whole set | min_probability |
| score              | a level, 0..L-1              | the expected level, rounded (.5 up)     | of that level        | min_probability            |
| box                | {top, bottom, left, right}   | the first answer's box                  | none (`confidence`)  | min_probability            |
| text, number, date | the value, or False (absent) | the value read, None when absent        | of the value         | min_probability            |
| estimate           | a number in min..max         | the estimate                            | none (`confidence`)  | min_probability            |

A value read from the state may be absent, and None already means "no label", so a task labels a case
that holds nothing `ABSENT` (False). The probability of a value read is what the model gives: `p_null` when it
read nothing, else P(something there) times its confidence in the value; 1 when it gives neither. An
estimate's confidence is how narrow its p10 - p90 interval is against the question's range.

Repeats are averaged before anything is read, so the evaluation (eval/metrics.py) and a
policy in production (policy.py) read a case alike: `average` then `reading`, here and nowhere else.
`probability` is the probability of the value given, never a vendor's `confidence` (TypeSafe's is
rescaled by the number of options). pydantic only: production imports it.
"""

import datetime as dt
import math
from dataclasses import dataclass
from typing import Any, ClassVar, Literal, Protocol, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, SerializerFunctionWrapHandler, ValidationError, model_serializer

from ..client.answers import (
    Answer, BooleanAnswer, BoxAnswer, BoxEdges, ChoiceAnswer, DateAnswer, EstimateAnswer, MultiChoiceAnswer, NumberAnswer, ScoreAnswer,
    TextAnswer,
)
from ..client.questions import Box, Choice, MultiChoice, Question, QuestionType, RangeEstimate, Score
from ..client.providers.contract import validate_answer_values
from ..core.errors import ProviderError
from .rule import DecisionRule, RuleField

ABSENT: Literal[False] = False  # the label of a case whose state holds nothing for a text, number or date question
SELECTIVE: frozenset[RuleField] = frozenset({"min_probability"})
BINARY: frozenset[RuleField] = frozenset({"threshold", "min_probability"})
# a task's label: True / False (binary), an option's key, a level, a box, a value read (False: absent), a number,
# the options that apply (a multichoice)
Label = Union[bool, int, float, str, BoxEdges, list[str]]


class Reading(BaseModel):
    """One case, read: the value, its probability and whether it is under the rule's min_probability,
    with what the kind reads it from."""

    # True / False (binary), an option's key, a level, a box, a value read (None: nothing there), an estimate,
    # the options that apply in the question's order (a multichoice)
    value: Union[bool, int, float, str, BoxEdges, tuple[str, ...], None]
    probability: float | None = None  # of `value`; None for a box (see `confidence`)
    below_min_probability: bool | None = None  # None when no probability lower bound is configured
    p_positive: float | None = None  # binary: P(true), or P(positive) for a choice scored as binary
    distribution: list[float] | None = None  # choice and score: the mean distribution over the options or levels
    expected: float | None = None  # score: the expected level; estimate: the estimate
    # box: the mean confidence (jev), or agreement of samples (LLM); estimate: how narrow its interval is
    confidence: float | None = None


@dataclass(frozen=True)
class Average:
    """The answers to one case, averaged: what a rule reads. `distributed`: every answer carried
    probabilities (a box: a confidence or an agreement); False when some were read as one-hot."""

    distributed: bool
    p_positive: float | None = None
    distribution: list[float] | None = None
    expected: float | None = None
    confidence: float | None = None
    box: BoxEdges | None = None
    value: Union[float, str, tuple[str, ...], None] = None  # a value read (None: nothing there), an estimate, the options that apply


class Kind(Protocol):
    @property
    def type(self) -> QuestionType: ...
    @property
    def adoptable(self) -> bool: ...
    @property
    def sets(self) -> frozenset[RuleField]: ...  # the rule fields it can choose
    @property
    def options(self) -> list[str]: ...  # a choice's keys, in order; empty for the others
    @property
    def binary(self) -> bool: ...  # read as P(positive) against a true / false label
    @property
    def iou(self) -> float: ...  # a box is right at this IoU with the label box or more

    def label_error(self, label: Any) -> str | None: ...
    def as_label(self, answer: Any) -> Any: ...
    def average(self, answers: Sequence[Answer]) -> Average: ...
    def reading(self, average: Average, rule: DecisionRule) -> Reading: ...
    def read(self, answers: Sequence[Answer], rule: DecisionRule) -> Reading: ...


class _Kind(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    type: ClassVar[QuestionType]
    adoptable: ClassVar[bool] = False
    sets: ClassVar[frozenset[RuleField]] = SELECTIVE
    answer: ClassVar[tuple[Any, ...]]  # the answer types it reads

    @property
    def options(self) -> list[str]:
        return []

    @property
    def binary(self) -> bool:
        return "threshold" in self.sets

    @property
    def iou(self) -> float:
        return 0.5

    def label_error(self, label: Any) -> str | None:
        raise NotImplementedError

    def as_label(self, answer: Any) -> Any:
        """A right answer given in production (a feedback record) as the task labels it."""
        return answer

    def average(self, answers: Sequence[Answer]) -> Average:
        raise NotImplementedError

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        raise NotImplementedError

    def read(self, answers: Sequence[Answer], rule: DecisionRule) -> Reading:
        """The answers to one case (one, or an LLM's samples), averaged and read."""
        return self.reading(self.average(answers), rule)

    def _given(self, answers: Sequence[Answer]) -> list[Any]:
        if not answers:
            raise ValueError("no answers to read")
        if wrong := next((a for a in answers if not isinstance(a, self.answer)), None):
            raise ProviderError(f"answered a {self.type} question as {wrong.type}, outside the contract")
        options = self.options if self.type == "choice" else getattr(self, "keys", None) if self.type == "multichoice" else None
        levels = getattr(self, "levels", None) if self.type == "score" else None
        within = (self.low, self.high) if isinstance(self, EstimateKind) else None
        for answer in answers:
            validate_answer_values(self.type, answer, options=options, levels=levels, within=within)
        return list(answers)


def same_label(kind: Kind, a: Any, b: Any) -> bool:
    """Whether two labels of a task say the same: compared as the kind reads them, so a multichoice's options
    in any order are one label, and 0 is not False (no value)."""
    try:
        a, b = kind.as_label(a), kind.as_label(b)
    except (TypeError, ValueError):  # a label the task cannot hold: compared as written
        pass
    return bool(a == b) and isinstance(a, bool) == isinstance(b, bool)


def _mean(xs: Sequence[float]) -> float:
    """Added in order, as numpy adds a few values: Python's own sum() of floats is compensated (3.12+),
    and an average one bit apart can move a chosen threshold."""
    total = 0.0
    for x in xs:
        total += x
    return total / len(xs)


def _below_min_probability(rule: DecisionRule, probability: float) -> bool | None:
    return None if rule.min_probability is None else probability < rule.min_probability


class _Binary(_Kind):
    sets: ClassVar[frozenset[RuleField]] = BINARY
    adoptable: ClassVar[bool] = True

    def label_error(self, label: Any) -> str | None:
        return None if isinstance(label, bool) else f"a binary task's label is true or false, got {label!r}"

    def p_positive(self, a: Any) -> tuple[float, bool]:
        raise NotImplementedError

    def average(self, answers: Sequence[Answer]) -> Average:
        ps = [self.p_positive(a) for a in self._given(answers)]
        return Average(distributed=all(d for _, d in ps), p_positive=_mean([p for p, _ in ps]))

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        p = average.p_positive
        assert p is not None
        value = p >= (0.5 if rule.threshold is None else rule.threshold)
        prob = p if value else 1 - p
        return Reading(value=value, probability=prob, below_min_probability=_below_min_probability(rule, prob), p_positive=p)


class BooleanKind(_Binary):
    type: ClassVar[QuestionType] = "boolean"
    answer: ClassVar[tuple[Any, ...]] = (BooleanAnswer,)

    def p_positive(self, a: Any) -> tuple[float, bool]:
        return float(a.probability), True


class PositiveChoiceKind(_Binary):
    """A choice scored as binary: P(positive) against a true / false label."""

    type: ClassVar[QuestionType] = "choice"
    answer: ClassVar[tuple[Any, ...]] = (ChoiceAnswer,)
    keys: list[str]
    positive: str

    @property
    def options(self) -> list[str]:
        return self.keys

    def as_label(self, answer: Any) -> Any:
        return answer == self.positive if isinstance(answer, str) else answer

    def p_positive(self, a: Any) -> tuple[float, bool]:
        """The choice's share on `positive`; the flag says whether it came from a distribution (False: a
        single answer read as 0 or 1)."""
        probs = a.probabilities
        if not probs:
            return (1.0 if a.choice == self.positive else 0.0), False
        total = sum(v for k, v in probs.items() if k in self.keys)
        if total <= 0:
            return (1.0 if a.choice == self.positive else 0.0), True
        return probs.get(self.positive, 0.0) / total, True


class ChoiceKind(_Kind):
    type: ClassVar[QuestionType] = "choice"
    adoptable: ClassVar[bool] = True
    answer: ClassVar[tuple[Any, ...]] = (ChoiceAnswer,)
    keys: list[str]

    @property
    def options(self) -> list[str]:
        return self.keys

    def label_error(self, label: Any) -> str | None:
        return None if label in self.keys else f"label {label!r} is not an option ({', '.join(self.keys)})"

    def one(self, a: ChoiceAnswer) -> tuple[list[float], bool]:
        """One answer's probabilities over the options, normalized; one-hot when it gave none."""
        probs = a.probabilities
        v = [0.0] * len(self.keys)
        if probs:
            v = [max(0.0, probs.get(c, 0.0)) for c in self.keys]
            s = sum(v)
            if s > 0:
                return [x / s for x in v], True
        if a.choice in self.keys:
            v[self.keys.index(a.choice)] = 1.0
        return v, bool(probs)

    def average(self, answers: Sequence[Answer]) -> Average:
        ds = [self.one(a) for a in self._given(answers)]
        dist = [_mean([d[j] for d, _ in ds]) for j in range(len(self.keys))]
        return Average(distributed=all(h for _, h in ds), distribution=dist)

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        dist = average.distribution
        assert dist is not None
        i = max(range(len(dist)), key=lambda j: dist[j])
        return Reading(value=self.keys[i], probability=dist[i], below_min_probability=_below_min_probability(rule, dist[i]), distribution=dist)


class MultiChoiceKind(_Kind):
    """Every option that applies, each its own yes or no at 0.5. Right when the set is the label's. Its probability
    is that of the whole set: the product over the options of how sure each one's yes or no is. Evaluated, not
    adoptable."""

    type: ClassVar[QuestionType] = "multichoice"
    answer: ClassVar[tuple[Any, ...]] = (MultiChoiceAnswer,)
    keys: list[str]

    def label_error(self, label: Any) -> str | None:
        ok = isinstance(label, (list, tuple)) and all(isinstance(k, str) and k in self.keys for k in label) and len(set(label)) == len(label)
        return None if ok else f"a multichoice label is the list of the options that apply ({', '.join(self.keys)}), [] for none; got {label!r}"

    def as_label(self, answer: Any) -> Any:
        """The options in the question's order; ValueError for anything that is not a list of its options."""
        if (wrong := self.label_error(answer)) is not None:
            raise ValueError(wrong)
        return tuple(k for k in self.keys if k in answer)

    def one(self, a: MultiChoiceAnswer) -> tuple[list[float], bool]:
        """One answer's P(it applies) per option; 1 or 0 from its choices where it gave no probability."""
        probs = a.probabilities or {}
        return [float(probs[k]) if k in probs else (1.0 if k in a.choices else 0.0) for k in self.keys], all(k in probs for k in self.keys)

    def average(self, answers: Sequence[Answer]) -> Average:
        ds = [self.one(a) for a in self._given(answers)]
        each = [_mean([d[j] for d, _ in ds]) for j in range(len(self.keys))]
        value = tuple(k for k, p in zip(self.keys, each) if p >= 0.5)
        return Average(distributed=all(h for _, h in ds), confidence=math.prod(max(p, 1 - p) for p in each), value=value)

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        assert isinstance(average.value, tuple) and average.confidence is not None
        return Reading(value=average.value, probability=average.confidence, below_min_probability=_below_min_probability(rule, average.confidence))


class ScoreKind(_Kind):
    """Levels 0..L-1 in the order of the question's criteria. Evaluated, not adoptable: no policy holds a score."""

    type: ClassVar[QuestionType] = "score"
    answer: ClassVar[tuple[Any, ...]] = (ScoreAnswer,)
    levels: int

    def label_error(self, label: Any) -> str | None:
        ok = isinstance(label, int) and not isinstance(label, bool) and 0 <= label < self.levels
        return None if ok else f"a score label is a level, 0..{self.levels - 1}, got {label!r}"

    def one(self, a: ScoreAnswer) -> tuple[list[float], float, bool]:
        """One answer's distribution over the levels and its expected level (the score itself when it gave
        no probabilities, read one-hot at the nearest level)."""
        probs = a.probabilities
        if probs:
            v = [max(0.0, probs.get(str(j), 0.0)) for j in range(self.levels)]
            s = sum(v)
            if s > 0:
                dist = [x / s for x in v]
                return dist, sum(j * p for j, p in enumerate(dist)), True
        dist = [0.0] * self.levels
        dist[self._level(a.score)] = 1.0
        return dist, float(a.score), False

    def _level(self, expected: float) -> int:
        return min(self.levels - 1, max(0, int(expected + 0.5)))

    def average(self, answers: Sequence[Answer]) -> Average:
        ds = [self.one(a) for a in self._given(answers)]
        dist = [_mean([d[j] for d, _, _ in ds]) for j in range(self.levels)]
        return Average(distributed=all(h for _, _, h in ds), distribution=dist, expected=_mean([e for _, e, _ in ds]))

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        dist, expected = average.distribution, average.expected
        assert dist is not None and expected is not None
        level = self._level(expected)
        return Reading(value=level, probability=dist[level], below_min_probability=_below_min_probability(rule, dist[level]), distribution=dist, expected=expected)


class BoxKind(_Kind):
    """A box, right at `iou` with the label box or more. The confidence (jev's, or the agreement of an LLM's
    samples) stands in for a probability."""

    type: ClassVar[QuestionType] = "box"
    answer: ClassVar[tuple[Any, ...]] = (BoxAnswer,)
    hit_iou: float = 0.5

    @property
    def iou(self) -> float:
        return self.hit_iou

    def label_error(self, label: Any) -> str | None:
        try:
            BoxEdges.model_validate(label)
        except ValidationError:
            return f"a box label needs top, bottom, left, right in 0..1, got {label!r}"
        return None

    def average(self, answers: Sequence[Answer]) -> Average:
        given: list[BoxAnswer] = self._given(answers)
        confs = [(a.confidence, True) if a.confidence is not None else (a.agreement, True) if a.agreement is not None else (1.0, False) for a in given]
        return Average(
            distributed=all(d for _, d in confs), confidence=_mean([float(c) for c, _ in confs]), box=given[0].box,
        )

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        assert average.box is not None and average.confidence is not None
        return Reading(value=average.box, below_min_probability=_below_min_probability(rule, average.confidence), confidence=average.confidence)


class _ReadKind(_Kind):
    """A value read from the state, or nothing: the first answer's. Evaluated, not adoptable."""

    def canonical(self, value: Any) -> Union[float, str]:
        """A value as readings and labels hold it, so two that mean the same are equal; ValueError when it is none."""
        raise NotImplementedError

    def label_error(self, label: Any) -> str | None:
        if label is ABSENT:
            return None
        try:
            self.canonical(label)
        except (TypeError, ValueError) as e:
            return f"a {self.type} label is {e}, or False when the state holds none; got {label!r}"
        return None

    def as_label(self, answer: Any) -> Any:
        return ABSENT if answer is ABSENT or answer is None else self.canonical(answer)

    def average(self, answers: Sequence[Answer]) -> Average:
        a = self._given(answers)[0]
        try:
            value: Union[float, str, None] = None if a.value is None else self.canonical(a.value)
        except ValueError:  # an empty text: nothing was read
            value = None
        if value is None:  # how sure that nothing is there: p_null, else what an empty text came with (a guess's confidence is not it)
            sure = a.p_null if a.p_null is not None else a.confidence if a.value is not None else None
            return Average(distributed=sure is not None, confidence=1.0 if sure is None else float(sure))
        parts = [1 - float(a.p_null)] if a.p_null is not None else []
        parts += [float(a.confidence)] if a.confidence is not None else []
        return Average(distributed=bool(parts), confidence=math.prod(parts), value=value)

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        assert average.confidence is not None
        return Reading(value=average.value, probability=average.confidence, below_min_probability=_below_min_probability(rule, average.confidence))


class TextKind(_ReadKind):
    """Right when the text is the label's, apart from the white space around and between its words."""

    type: ClassVar[QuestionType] = "text"
    answer: ClassVar[tuple[Any, ...]] = (TextAnswer,)

    def canonical(self, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("the text as the state writes it")
        return " ".join(value.split())


class NumberKind(_ReadKind):
    type: ClassVar[QuestionType] = "number"
    answer: ClassVar[tuple[Any, ...]] = (NumberAnswer,)

    def canonical(self, value: Any) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("a number")
        return float(value)


class DateKind(_ReadKind):
    """Held as the ISO day (2026-09-02), which a label is written as."""

    type: ClassVar[QuestionType] = "date"
    answer: ClassVar[tuple[Any, ...]] = (DateAnswer,)

    def label_error(self, label: Any) -> str | None:
        if isinstance(label, dt.date):  # a label is saved as JSON
            return f"a date label is a day written as YYYY-MM-DD ({label.isoformat()[:10]!r}), got {label!r}"
        return super().label_error(label)

    def canonical(self, value: Any) -> str:
        if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
            return value.isoformat()
        if not isinstance(value, str):
            raise ValueError("a day as YYYY-MM-DD")
        try:
            return dt.date.fromisoformat(value).isoformat()
        except ValueError:
            raise ValueError("a day as YYYY-MM-DD") from None


class EstimateKind(_Kind):
    """A number between `low` and `high`, right within `tolerance` of the label. How narrow its p10 - p90 interval
    is against the range stands in for a probability. Evaluated, not adoptable."""

    type: ClassVar[QuestionType] = "estimate"
    answer: ClassVar[tuple[Any, ...]] = (EstimateAnswer,)
    low: float
    high: float
    tolerance: float

    def label_error(self, label: Any) -> str | None:
        ok = isinstance(label, (int, float)) and not isinstance(label, bool) and self.low <= label <= self.high
        return None if ok else f"an estimate's label is a number in {self.low:g}..{self.high:g}, got {label!r}"

    def as_label(self, answer: Any) -> Any:
        return float(answer) if isinstance(answer, (int, float)) and not isinstance(answer, bool) else answer

    def average(self, answers: Sequence[Answer]) -> Average:
        a: EstimateAnswer = self._given(answers)[0]
        if a.p10 is None or a.p90 is None:
            return Average(distributed=False, confidence=1.0, value=float(a.value))
        narrow = 1 - (a.p90 - a.p10) / (self.high - self.low)
        return Average(distributed=True, confidence=min(1.0, max(0.0, narrow)), value=float(a.value))

    def reading(self, average: Average, rule: DecisionRule) -> Reading:
        assert isinstance(average.value, float) and average.confidence is not None
        return Reading(value=average.value, below_min_probability=_below_min_probability(rule, average.confidence),
                       expected=average.value, confidence=average.confidence)


class KindParams(BaseModel):
    """What a question's type leaves open, the same in a task (`Task.kind_params`) and a policy (`kind`):
    `positive` scores a choice as binary (P(positive) against a true / false label), `iou` is a box's bar
    for a hit (0.5 when unset), `tolerance` how far from the label an estimate is still right (half a step when
    unset; a hundredth of the range for a question without a step). An unset one is left out of the JSON."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    positive: str | None = None
    iou: float | None = Field(default=None, gt=0, le=1)
    tolerance: float | None = Field(default=None, ge=0)

    @model_serializer(mode="wrap")
    def _set_only(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        return {k: v for k, v in handler(self).items() if v is not None}


def kind_of(question: Question, params: KindParams = KindParams()) -> Kind:
    """The kind of a question with what its type leaves open; a param its type does not take is a ValueError."""
    if params.tolerance is not None and not isinstance(question, RangeEstimate):
        raise ValueError(f"tolerance is how far off an estimate is still right; this one is {question.type}")
    if params.positive is not None and not isinstance(question, Choice):
        raise ValueError(f"positive scores a choice question as binary; this one is {question.type}")
    if params.iou is not None and not isinstance(question, Box):
        raise ValueError(f"iou is a box question's bar for a hit; this one is {question.type}")
    if isinstance(question, Choice):
        keys = list(question.criteria)
        if params.positive is None:
            return ChoiceKind(keys=keys)
        if params.positive not in keys:
            raise ValueError(f"positive {params.positive!r} is not an option ({', '.join(keys)})")
        return PositiveChoiceKind(keys=keys, positive=params.positive)
    if isinstance(question, MultiChoice):
        return MultiChoiceKind(keys=list(question.criteria))
    if isinstance(question, Score):
        return ScoreKind(levels=len(question.criteria))
    if isinstance(question, Box):
        return BoxKind(hit_iou=0.5 if params.iou is None else params.iou)
    if isinstance(question, RangeEstimate):
        default = question.step / 2 if question.step is not None else (question.max - question.min) / 100
        return EstimateKind(low=question.min, high=question.max, tolerance=default if params.tolerance is None else params.tolerance)
    return {"text": TextKind, "number": NumberKind, "date": DateKind, "boolean": BooleanKind}[question.type]()
