"""OpenRouter's Extractions wire format (`POST /api/alpha/extractions`, alpha, 2026-11-16): the questions that
read a value or estimate one, sent as `fields`, and the answers read back. Workers AI speaks the same `fields`
to Clairic.

    fields(qs)      # {"total": {"type": "number", "instructions": ..., "unit": "USD"}}
    answers(raw)    # {"total": NumberAnswer(value=1080.0, p_null=0.0004, confidence=0.998)}

An answer carries what its model has: Clairic a `p_null` and a `confidence` in its `guess`, Perplexity's and
ScaleDown's a `confidence` on a value they found and nothing on one they did not, Schematron the value alone.
An estimate's `value` is the model's own point (Clairic: the mean, on the grid when there is a `step`).
"""

from typing import Any

from ..answers import Answer, DateAnswer, EstimateAnswer, NumberAnswer, ReadAnswer, TextAnswer
from ..questions import Questions
from .contract import outside_contract, refusal

READ: dict[Any, type[TextAnswer] | type[NumberAnswer] | type[DateAnswer]] = {"text": TextAnswer, "number": NumberAnswer, "date": DateAnswer}


def fields(qs: Questions) -> dict[str, Any]:
    return {k: q.model_dump(exclude_none=True) for k, q in qs.items()}


def answers(raw: dict[str, Any]) -> dict[str, Answer]:
    out: dict[str, Answer] = {}
    for qid, a in raw.items():
        if (r := refusal(a)) is not None:
            out[qid] = r
            continue
        with outside_contract(qid):
            out[qid] = _answer(a)
    return out


def _answer(a: dict[str, Any]) -> Answer:
    kind = a.get("type")
    if kind == "estimate":
        return EstimateAnswer(value=a["value"], p10=a.get("p10"), p90=a.get("p90"))
    if kind in READ:
        span = a.get("span")
        read: ReadAnswer = READ[kind](value=a["value"], guess=a.get("guess"), p_null=a.get("p_null"), confidence=a.get("confidence"),
                                      span=tuple(span) if span else None)
        return read
    raise TypeError(f"no answer type {kind!r}")
