"""What every dialect reads alike: an answer that does not fit `Answer`, and a question the model declined."""

from __future__ import annotations

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
    Refusal,
    Response,
    ScoreAnswer,
)
from ..questions import Boolean, Choice, Questions, Score


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
    if not isinstance(response.answered_by, str) or not response.answered_by.strip():
        raise ProviderError(f"{provider} returned blank answered_by outside the contract")
    if not isinstance(response.answers, dict):
        raise ProviderError(f"{provider} returned malformed answers outside the contract")
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
    if isinstance(question, Boolean):
        fits = isinstance(answer, BooleanAnswer)
    elif isinstance(question, Choice):
        fits = isinstance(answer, ChoiceAnswer)
    elif isinstance(question, Score):
        fits = isinstance(answer, ScoreAnswer)
    else:
        fits = isinstance(answer, BoxAnswer)
    if isinstance(answer, Refusal):
        return
    if not fits:
        kind = getattr(answer, "type", type(answer).__name__)
        _fail(qid, f"answer type {kind!r} does not fit a {question.type} question")

    validate_answer_values(qid, answer, options=question.criteria.keys() if isinstance(question, Choice) else None,
                           levels=len(question.criteria) if isinstance(question, Score) else None)


def validate_answer_values(
    qid: str, answer: Answer, *, options: Iterable[str] | None = None, levels: int | None = None,
) -> None:
    """Validate numeric answer values and any option/level membership available to a reader."""
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
    if isinstance(answer, ScoreAnswer):
        score = _number(qid, "score", answer.score)
        if levels is not None and not 0 <= score <= levels - 1:
            _fail(qid, f"score {score:g} is outside the levels 0..{levels - 1}")
        _distribution(qid, answer.probabilities, (str(i) for i in range(levels)) if levels is not None else None)
        _confidence(qid, answer.confidence)
        return
    if isinstance(answer, BoxAnswer):
        box = answer.box
        for edge in ("top", "bottom", "left", "right"):
            value = getattr(box, edge, None)
            if value is None:
                _fail(qid, f"box is missing {edge}")
            _number(qid, f"box.{edge}", value, low=0, high=1)
        if box.top > box.bottom or box.left > box.right:
            _fail(qid, f"box edges are out of order: {box}")
        _confidence(qid, answer.confidence)
        _confidence(qid, answer.agreement, name="agreement")


def _distribution(qid: str, probabilities: object, options: Iterable[str] | None) -> None:
    if probabilities is None:
        return
    if not isinstance(probabilities, dict):
        _fail(qid, f"probabilities must be a mapping, got {type(probabilities).__name__}")
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


def _confidence(qid: str, value: object, *, name: str = "confidence") -> None:
    if value is not None:
        _probability(qid, name, value)


def _probability(qid: str, name: str, value: object) -> float:
    return _number(qid, name, value, low=0, high=1)


def _number(qid: str, name: str, value: object, *, low: float | None = None, high: float | None = None) -> float:
    if isinstance(value, bool):
        _fail(qid, f"{name} must be a finite number, got {value!r}")
    if not isinstance(value, (int, float, str)):
        _fail(qid, f"{name} must be a finite number, got {value!r}")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        _fail(qid, f"{name} must be a finite number, got {value!r}")
    if not math.isfinite(number) or (low is not None and number < low) or (high is not None and number > high):
        bounds = ""
        if low is not None and high is not None:
            bounds = f" between {low:g} and {high:g}"
        elif low is not None:
            bounds = f" at least {low:g}"
        elif high is not None:
            bounds = f" at most {high:g}"
        _fail(qid, f"{name} must be finite{bounds}, got {value!r}")
    return number


def _fail(qid: str, detail: str) -> NoReturn:
    raise ProviderError(f"the provider answered {qid} outside the contract: {detail}")
