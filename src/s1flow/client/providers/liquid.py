"""Liquid's own API (`POST https://api.liquid.ai/decisions/v1/systemone`): d1.2 and d1.2-ultra without a gateway
in between.

The System One wire format (systemone.py, yes/no is `noul`), with three differences
(https://docs.liquid.ai/api/reference/decision-models/make-decisions, 2026-11-16): images are `image_url` parts in
the state array, as OpenRouter takes them, and not TypeSafe's `assets`; usage carries the billed cost when the
model is priced; and a box answer carries `found`, with no `box` when the model does not find the target.

s1flow's box has no "not found" answer (questions.Box), so a box the model did not find is read as the model
declining that question (Refusal), which an evaluation counts as no answer.
"""

from typing import Any

from ..answers import Response, Usage
from ..media import chat_parts, images_only
from ..models import Capabilities, ModelBuild, ModelSpec, check_supported
from ..questions import Questions
from ..state import State, has_image
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


class LiquidModel:
    def __init__(self, model_id: str, *, concurrency: int = 8, capabilities: Capabilities | None = None):
        self.model_id = model_id
        self.id = f"liquid:{model_id}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities()

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        images_only(state, self.id)
        body: dict[str, Any] = {"model": self.model_id, "state": state, "questions": systemone.questions(questions)}
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
            answers=systemone.answers(_not_found_as_refusal(data["answers"])),
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
