"""What every dialect reads alike: an answer that does not fit `Answer`, and a question the model declined."""

import math
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from typing import Any, NoReturn

from pydantic import ValidationError

from ...core.errors import ProviderError
from ..answers import (
    Answer,
    BooleanAnswer,
    BoxAnswer,
    ChoiceAnswer,
    DateAnswer,
    EstimateAnswer,
    MultiChoiceAnswer,
    NumberAnswer,
    Refusal,
    Response,
    ScoreAnswer,
    TextAnswer,
)
from ..questions import Choice, MultiChoice, RangeEstimate, Questions, Score

# The answer each type of question takes.
FITS: dict[str, type] = {
    "boolean": BooleanAnswer, "choice": ChoiceAnswer, "score": ScoreAnswer, "box": BoxAnswer,
    "text": TextAnswer, "number": NumberAnswer, "date": DateAnswer, "estimate": EstimateAnswer,
    "multichoice": MultiChoiceAnswer,
}


@contextmanager
def outside_contract(qid: str) -> Iterator[None]:
    """An answer that does not fit `Answer` (a score without its value, say) is the provider's failure, named as such."""
    try:
        yield
    except (AttributeError, OverflowError, ValidationError, KeyError, TypeError, ValueError) as e:
        detail = e.errors()[0]["msg"] if isinstance(e, ValidationError) else f"{type(e).__name__}: {e}"
        raise ProviderError(f"the provider answered {qid} outside the contract: {detail}") from e


def refusal(a: dict[str, Any]) -> Refusal | None:
    """`{"type": "refusal"}` (the Decisions API, and the Gateway's endpoints, 2026-10): the model declined to
    answer this question. Like an LLM's content refusal, it is the model's limit, not a failed call."""
    if not isinstance(a, dict):
        return None
    if a.get("type") != "refusal":
        return None
    why = a.get("refusal") or a.get("message") or a.get("reason")
    return Refusal(reason=str(why)[:200] if why else None)


def validate_response(response: object, questions: Questions, provider: str) -> Response:
    """Validate the provider's typed response against the questions it was asked."""
    if not isinstance(response, Response):
        raise ProviderError(f"{provider} returned a malformed response outside the contract")
    try:  # once more from its values: model_construct and model_copy(update=...) skip the types this relies on
        Response.model_validate(response.model_dump(warnings=False))
    except ValidationError as e:
        raise ProviderError(f"{provider} returned a malformed response outside the contract: {e}") from None
    if not response.answered_by.strip():
        raise ProviderError(f"{provider} returned blank answered_by outside the contract")
    missing = [qid for qid in questions if qid not in response.answers]
    if missing:
        raise ProviderError(f"{provider} answered without {', '.join(missing)}, outside the contract")
    extra = [qid for qid in response.answers if qid not in questions]
    if extra:
        raise ProviderError(f"{provider} answered extra {', '.join(extra)}, outside the contract")
    for qid, question in questions.items():
        _validate_answer(qid, question, response.answers[qid])
    return response


def _validate_answer(qid: str, question: Any, answer: Answer) -> None:
    if isinstance(answer, Refusal):
        return
    if not isinstance(answer, FITS[question.type]):
        kind = getattr(answer, "type", type(answer).__name__)
        _fail(qid, f"answer type {kind!r} does not fit a {question.type} question")

    validate_answer_values(qid, answer, options=question.criteria.keys() if isinstance(question, (Choice, MultiChoice)) else None,
                           levels=len(question.criteria) if isinstance(question, Score) else None,
                           within=(question.min, question.max) if isinstance(question, RangeEstimate) else None)


def validate_answer_values(
    qid: str, answer: Answer, *, options: Iterable[str] | None = None, levels: int | None = None,
    within: tuple[float, float] | None = None,
) -> None:
    """Validate numeric answer values and any option/level membership available to a reader. The answer types
    already hold the rest (a box's edges are in 0..1 and in order: `BoxEdges`)."""
    if isinstance(answer, BooleanAnswer):
        _probability(qid, "probability", answer.probability)
        return
    if isinstance(answer, ChoiceAnswer):
        if options is not None:
            allowed = tuple(options)
            if answer.choice not in allowed:
                _fail(qid, f"choice {answer.choice!r} is not an option ({', '.join(allowed)})")
        _distribution(qid, answer.probabilities, options)
        _confidence(qid, answer.confidence)
        return
    if isinstance(answer, MultiChoiceAnswer):
        among = None if options is None else tuple(options)
        if among is not None and (unknown := [c for c in answer.choices if c not in among]):
            _fail(qid, f"choices {', '.join(map(repr, unknown))} are not options ({', '.join(among)})")
        if len(set(answer.choices)) < len(answer.choices):
            _fail(qid, f"choices name an option twice: {answer.choices}")
        for key, value in (answer.probabilities or {}).items():
            _probability(qid, f"probability for {key!r}", value)
        return
    if isinstance(answer, ScoreAnswer):
        score = answer.score
        if not math.isfinite(score):
            _fail(qid, f"score must be finite, got {score!r}")
        if levels is not None and not 0 <= score <= levels - 1:
            _fail(qid, f"score {score:g} is outside the levels 0..{levels - 1}")
        _distribution(qid, answer.probabilities, (str(i) for i in range(levels)) if levels is not None else None)
        _confidence(qid, answer.confidence)
        return
    if isinstance(answer, BoxAnswer):
        _confidence(qid, answer.found, name="found")
        _confidence(qid, answer.confidence)
        _confidence(qid, answer.agreement, name="agreement")
        return
    if isinstance(answer, (TextAnswer, NumberAnswer, DateAnswer)):
        if isinstance(answer, NumberAnswer):
            for name in ("value", "guess"):
                if (x := getattr(answer, name)) is not None and not math.isfinite(x):
                    _fail(qid, f"{name} must be finite, got {x!r}")
        _confidence(qid, answer.p_null, name="p_null")
        _confidence(qid, answer.confidence)
        if answer.span is not None and not 0 <= answer.span[0] <= answer.span[1]:
            _fail(qid, f"span {list(answer.span)} is not a start and an end in order")
        return
    if isinstance(answer, EstimateAnswer):
        for name in ("value", "p10", "p90"):
            if (x := getattr(answer, name)) is not None and not math.isfinite(x):
                _fail(qid, f"{name} must be finite, got {x!r}")
        if answer.p10 is not None and answer.p90 is not None and answer.p10 > answer.p90:
            _fail(qid, f"p10 {answer.p10:g} is over p90 {answer.p90:g}")
        slack = 1e-9 * (within[1] - within[0]) if within is not None else 0.0  # a float a hair past an end is not a failure
        if within is not None and not within[0] - slack <= answer.value <= within[1] + slack:
            _fail(qid, f"estimate {answer.value!r} is outside {within[0]:g}..{within[1]:g}")


def _distribution(qid: str, probabilities: dict[str, float] | None, options: Iterable[str] | None) -> None:
    if not probabilities:
        return  # an empty map has the same no-distribution meaning as None
    allowed = None if options is None else set(options)
    positive = False
    # Readers normalize over the question's options and ignore other sparse-map keys.
    for key, value in probabilities.items():
        probability = _probability(qid, f"probability for {key!r}", value)
        if allowed is not None and key in allowed and probability > 0:
            positive = True
    if allowed is not None and not positive:
        _fail(qid, "distribution has no positive mass on the question's options")


def _confidence(qid: str, value: float | None, *, name: str = "confidence") -> None:
    if value is not None:
        _probability(qid, name, value)


def _probability(qid: str, name: str, value: float) -> float:
    if not 0 <= value <= 1:  # NaN too
        _fail(qid, f"{name} must be finite between 0 and 1, got {value!r}")
    return value


def _fail(qid: str, detail: str) -> NoReturn:
    raise ProviderError(f"the provider answered {qid} outside the contract: {detail}")
