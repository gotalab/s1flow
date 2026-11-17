"""Liquid's own API (`POST https://api.liquid.ai/decisions/v1/systemone`): d1.2 and d1.2-ultra without a gateway
in between.

The System One wire format (systemone.py, yes/no is `noul`), with three differences
(https://docs.liquid.ai/api/reference/decision-models/make-decisions, 2026-11-16): images are `image_url` parts in
the state array, as OpenRouter takes them, and not TypeSafe's `assets`; usage carries the billed cost when the
model is priced; and a box answer carries `found`, with no `box` when the model does not find the target.

The questions that read a value or estimate one go in the same `questions` (checked by real calls, 2026-11-17):
`text`, `number` and `date` answer the value with `found`, which is 1 - `p_null`, and a null value when nothing is
there; a `RangeEstimate` is a `number` with a `range`, answered with its median and an `interval` (p10, p90).
A `MultiChoice` is a `choice` with `multiple`, answered with the `choices` that apply and each option's own
probability. A `span` is kept for a text state only: for a JSON state Liquid counts in its own rendering of it.

s1flow's box has no "not found" answer (questions.Box), so a box the model did not find is read as the model
declining that question (Refusal), which an evaluation counts as no answer.
"""

from typing import Any

from ..answers import Answer, DateAnswer, MultiChoiceAnswer, EstimateAnswer, NumberAnswer, ReadAnswer, Response, TextAnswer, Usage
from ..media import chat_parts, images_only
from ..models import Capabilities, ModelBuild, ModelSpec, check_supported
from ..questions import FIELD_TYPES, MultiChoice, Question, Questions, RangeEstimate
from ..state import State, has_image
from .contract import outside_contract, refusal
from .build import NoOptions, options, spec_options
from .http import Request, send
from .needs import Needs, declares, origin
from . import systemone

BASE_URL = "https://api.liquid.ai/decisions/v1"


def _not_found_as_refusal(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        qid: {"type": "refusal", "reason": f"box not found (found {a.get('found')})"}
        if isinstance(a, dict) and a.get("type") == "box" and a.get("box") is None else a
        for qid, a in raw.items()
    }


READ: dict[Any, type[TextAnswer] | type[NumberAnswer] | type[DateAnswer]] = {"text": TextAnswer, "number": NumberAnswer, "date": DateAnswer}


OWN = FIELD_TYPES | {"multichoice"}  # asked in Liquid's own shape, not System One's


def _field(q: Question) -> dict[str, Any]:
    if isinstance(q, MultiChoice):
        return {"type": "choice", "multiple": True, "instructions": q.instructions, "criteria": q.criteria}
    if isinstance(q, RangeEstimate):
        wire = q.model_dump(exclude_none=True, exclude={"type", "min", "max"})
        return {"type": "number", "range": [q.min, q.max]} | wire
    return q.model_dump(exclude_none=True)


def _read(q: Question, a: dict[str, Any], text_state: bool) -> Answer:
    if isinstance(q, MultiChoice):
        return MultiChoiceAnswer(choices=a["choices"], probabilities=a.get("probabilities") or None)
    if isinstance(q, RangeEstimate):
        low, high = a.get("interval") or (None, None)
        return EstimateAnswer(value=a["number"], p10=low, p90=high)
    found, span = a.get("found"), a.get("span")
    read: ReadAnswer = READ[q.type](value=a[q.type], p_null=None if found is None else 1 - found, span=tuple(span) if span and text_state else None)
    return read


def _questions(questions: Questions) -> dict[str, Any]:
    rest = systemone.questions({k: q for k, q in questions.items() if q.type not in OWN})
    return {k: _field(q) if q.type in OWN else rest[k] for k, q in questions.items()}


def _answers(questions: Questions, state: State, raw: dict[str, Any]) -> dict[str, Answer]:
    rest = systemone.answers(_not_found_as_refusal({k: a for k, a in raw.items() if k not in questions or questions[k].type not in OWN}))
    out: dict[str, Answer] = {}
    for qid, a in raw.items():
        if qid in rest:
            out[qid] = rest[qid]
        elif (r := refusal(a)) is not None:
            out[qid] = r
        else:
            with outside_contract(qid):
                out[qid] = _read(questions[qid], a, isinstance(state, str))
    return out


class LiquidModel:
    def __init__(self, model_id: str, *, concurrency: int = 8, capabilities: Capabilities | None = None):
        self.model_id = model_id
        self.id = f"liquid:{model_id}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities()

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        images_only(state, self.id)
        body: dict[str, Any] = {"model": self.model_id, "state": state, "questions": _questions(questions)}
        if has_image(state):
            body["state"] = chat_parts(state)
        if options:
            body.update(options)
        return Request(f"{BASE_URL}/systemone", body, keys={"Authorization": ("Bearer ", "LIQUID_API_KEY")})

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        posted = await send(self.request(state, questions, options=options))
        data = posted.data
        usage = data.get("usage") or {}
        cost = usage.get("cost")
        return Response(
            answers=_answers(questions, state, data["answers"]),
            answered_by=data.get("model", self.model_id),
            usage=Usage(input_tokens=usage.get("input_tokens") or 0, output_tokens=usage.get("output_tokens") or 0,
                        cost_usd=float(cost) if cost is not None else None, cost_source="billed" if cost is not None else None,
                        raw=usage or None),
            latency_ms=posted.latency_ms,
            retries=posted.retries,
        )


def needs(spec: ModelSpec) -> Needs:
    spec_options(NoOptions, spec)
    return Needs(keys=("LIQUID_API_KEY",), hosts=(origin(BASE_URL),))


@declares(needs)
def build(b: ModelBuild) -> LiquidModel:
    options(NoOptions, b)
    return LiquidModel(b.spec.id, concurrency=b.spec.concurrency or 8, capabilities=b.spec.capabilities)
