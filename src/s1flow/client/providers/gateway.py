"""AI Gateway native decision models (`POST /v1/evaluate`): jev, Laya, d1. The System One wire format
(systemone.py), yes / no as `boolean`; usage reports the billed cost.

Images (2026-10-16): the documented AI SDK `file` part reaches no model as an image
(the base64 arrives as text). d1 sees `image_url` parts, which is not documented.
jev through the gateway is text-only ("TypeSafe AI accepts text and JSON state only"),
and Laya answers 422.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import systemone
from ..answers import Response, Usage
from ..images import image_url_parts
from ..models import Capabilities, ModelBuild, ModelSpec, Price, check_supported
from ..questions import Questions
from ..state import State, has_image
from .build import NoOptions, options
from .http import Request, send
from .needs import Needs, declares, origin
from .published import per_token, publishes
from . import pricing

BASE_URL = "https://ai-gateway.vercel.sh/v1"


class GatewayModel:
    def __init__(self, model_id: str, *, concurrency: int = 8, capabilities: Capabilities | None = None):
        self.model_id = model_id
        self.id = f"gateway:{model_id}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities()

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        body: dict[str, Any] = {"model": self.model_id, "state": state, "questions": systemone.questions(questions, noul=False)}
        if has_image(state):
            body["state"] = image_url_parts(state)
        if options:
            body["providerOptions"] = options
        return Request(f"{BASE_URL}/evaluate", body, keys={"Authorization": ("Bearer ", "AI_GATEWAY_API_KEY")})

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        posted = await send(self.request(state, questions, options=options))
        data = posted.data
        meta = data.get("providerMetadata") or {}
        cost = (meta.get("gateway") or {}).get("cost")
        usage = data.get("usage") or {}
        return Response(
            answers=systemone.answers(data["answers"], (meta.get("typesafe") or {}).get("confidence")),
            answered_by=data.get("model", self.model_id),
            usage=Usage(input_tokens=usage.get("inputTokens") or 0, output_tokens=usage.get("outputTokens") or 0,
                        cost_usd=float(cost) if cost is not None else None, cost_source="billed" if cost is not None else None,
                        raw=usage or None),
            latency_ms=posted.latency_ms,
            retries=posted.retries,
            provider_metadata={"routing": (meta.get("gateway") or {}).get("routing")},
        )


def needs(spec: ModelSpec) -> Needs:
    return Needs(keys=("AI_GATEWAY_API_KEY",), hosts=(origin(BASE_URL),))


def published(spec: ModelSpec, cache_dir: Path | None) -> Price | None:
    """The gateway's model list (it bills each call, so a model of it needs no price in s1flow.toml)."""
    p = pricing.listed(spec.id, cache_dir)
    return None if p is None else per_token(*p, source=pricing.MODELS_URL)


@publishes(published)
@declares(needs)
def build(b: ModelBuild) -> GatewayModel:
    options(NoOptions, b)
    return GatewayModel(b.spec.id, concurrency=b.spec.concurrency or 8, capabilities=b.spec.capabilities)
