"""OpenRouter's System One endpoint (`POST /api/v1/systemone`): Kev, Tev1, Mercury Decide, Solar Decide.

The System One wire format (systemone.py): yes/no questions are `noul`, answers carry their own
`confidence`, and usage reports the billed cost.

Images are `image_url` parts with a base64 data URL in the top-level state array
(OpenRouter's Multimodal Decisions guide). Models without image input answer 400;
TypeSafe's `assets` is dropped without an error, so it must not be sent here (2026-10-15).
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Any

from ..answers import Response, Usage
from ..images import image_url_parts
from ..models import Capabilities, ModelBuild, ModelSpec, Price, check_supported
from ..questions import Questions
from ..state import State, has_image
from .build import NoOptions, options, spec_options
from .http import Request, send
from .needs import Needs, declares, origin
from .published import per_token, publishes
from . import systemone

BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterModel:
    def __init__(self, model_id: str, *, concurrency: int = 8, capabilities: Capabilities | None = None):
        self.model_id = model_id
        self.id = f"openrouter:{model_id}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities()
        per_minute = self.capabilities.per_minute  # free models allow 20 requests a minute
        self.interval = 60 / per_minute if per_minute else 0.0
        self._next = 0.0

    async def _pace(self) -> None:
        if self.interval:
            now = time.monotonic()
            wait, self._next = max(0.0, self._next - now), max(now, self._next) + self.interval
            await asyncio.sleep(wait)

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        body: dict[str, Any] = {"model": self.model_id, "state": state, "questions": systemone.questions(questions)}
        if has_image(state):
            body["state"] = image_url_parts(state)
        if options:
            body.update(options)
        return Request(f"{BASE_URL}/systemone", body, keys={"Authorization": ("Bearer ", "OPENROUTER_API_KEY")})

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        req = self.request(state, questions, options=options)
        await self._pace()
        posted = await send(req)
        data = posted.data
        usage = data.get("usage") or {}
        cost = usage.get("cost")
        return Response(
            answers=systemone.answers(data["answers"]),
            answered_by=data.get("model", self.model_id),
            usage=Usage(input_tokens=usage.get("input_tokens") or 0, output_tokens=usage.get("output_tokens") or 0,
                        cost_usd=float(cost) if cost is not None else None, cost_source="billed" if cost is not None else None,
                        raw=usage or None),
            latency_ms=posted.latency_ms,
            retries=posted.retries,
            provider_metadata={"provider": data.get("provider")},
        )


def needs(spec: ModelSpec) -> Needs:
    spec_options(NoOptions, spec)
    return Needs(keys=("OPENROUTER_API_KEY",), hosts=(origin(BASE_URL),))


MODELS_URL = f"{BASE_URL}/models?output_modalities=decisions"  # the decision models' list, no key needed
_listed: dict[str, dict[str, Any]] | None = None


def published(spec: ModelSpec, cache_dir: Path | None) -> Price | None:
    """OpenRouter's model list (it bills each call, so a model of it needs no price in s1flow.toml). Read once a process."""
    global _listed
    if _listed is None:
        import httpx

        r = httpx.get(MODELS_URL, timeout=30)
        r.raise_for_status()
        _listed = {m["id"]: m.get("pricing") or {} for m in r.json()["data"]}
    p = _listed.get(spec.id)
    if p is None:
        return None
    return per_token(p.get("prompt"), p.get("completion"), MODELS_URL, p.get("request"), p.get("image"))


@publishes(published)
@declares(needs)
def build(b: ModelBuild) -> OpenRouterModel:
    options(NoOptions, b)
    return OpenRouterModel(b.spec.id, concurrency=b.spec.concurrency or 8, capabilities=b.spec.capabilities)
