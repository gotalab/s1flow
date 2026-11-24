"""AI Gateway native decision models (`POST /v1/decisions`): OpenAI's Decisions wire format
(openai_decisions.py) plus a `box` question; usage reports the billed cost.

`/v1/evaluate` (System One format) is deprecated (2026-11). Images go as `input_image` parts: Drex Max v1.1 refuses
the `image_url` parts `/v1/evaluate` took, and Mo read them without seeing the picture (2026-11-24).
"""

from pathlib import Path
from typing import Any

from ..answers import Response, Usage
from ..media import images_only
from ..models import Capabilities, ModelBuild, ModelSpec, Price, check_supported
from ..questions import Questions
from ..state import State
from .build import NoOptions, options
from .http import Request, send
from .needs import Needs, declares, origin
from .openai_decisions import decisions_input, decisions_questions, parse_decisions
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
        images_only(state, self.id)
        body: dict[str, Any] = {"model": self.model_id, "input": decisions_input(state), "questions": decisions_questions(questions, box=True)}
        if options:
            body["providerOptions"] = options
        return Request(f"{BASE_URL}/decisions", body, keys={"Authorization": ("Bearer ", "AI_GATEWAY_API_KEY")})

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        posted = await send(self.request(state, questions, options=options))
        data = posted.data
        gateway = (data.get("provider_metadata") or {}).get("gateway") or {}
        cost = gateway.get("cost")
        usage = data.get("usage") or {}
        return Response(
            answers=parse_decisions(data["answers"]),
            answered_by=data.get("model", self.model_id),
            usage=Usage(input_tokens=usage.get("input_tokens") or 0, output_tokens=usage.get("output_tokens") or 0,
                        cost_usd=float(cost) if cost is not None else None, cost_source="billed" if cost is not None else None,
                        raw=usage or None),
            latency_ms=posted.latency_ms,
            retries=posted.retries,
            provider_metadata={"routing": gateway.get("routing")},
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
