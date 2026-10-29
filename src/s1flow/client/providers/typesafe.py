"""TypeSafe's own API (`POST https://api.typesafe.ai/v1/systemone`): jev without a gateway in between.

The System One wire format (systemone.py, yes/no is `noul`). Usage carries tokens but no cost: the
model's list price (s1flow.toml `price`) gives an estimate.

Images go in top-level `assets` and are referenced from the state, behind the
`TypeSafe-Danger-Zone-Images` header (jev 1.13 and 1.14, 2026-10-15). Box questions need the
same header and jev 1.14: 1.13 (still `jev-latest` on 2026-10-16) answers a bare 400, so s1flow.toml
declares box on the 1.14 version only.
"""

from __future__ import annotations

from typing import Any

from ..answers import Response, Usage
from ..images import typesafe_assets
from ..models import Capabilities, ModelBuild, ModelSpec, check_supported
from ..questions import Questions, has_box
from ..state import State, has_image
from .build import Options, options, spec_options
from .http import Request, send
from .needs import Needs, declares, origin
from . import systemone

BASE_URL = "https://api.typesafe.ai/v1"


class TypeSafeModel:
    def __init__(
        self, model_id: str, *, concurrency: int = 8, capabilities: Capabilities | None = None,
        base_url: str = BASE_URL, api_key_env: str = "TYPESAFE_API_KEY",
    ):
        self.model_id = model_id
        # Another server that speaks this API caches apart from TypeSafe's.
        self.id = f"typesafe:{model_id}" if base_url == BASE_URL else f"typesafe:{base_url}:{model_id}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities()
        self.base_url = base_url
        self.api_key_env = api_key_env

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        body: dict[str, Any] = {"model": self.model_id, "state": state, "questions": systemone.questions(questions)}
        headers = {}
        if has_image(state):
            body["state"], body["assets"] = typesafe_assets(state)
        if has_image(state) or has_box(questions):
            headers["TypeSafe-Danger-Zone-Images"] = "true"
        if options:
            body.update(options)
        return Request(f"{self.base_url}/systemone", body, headers, {"Authorization": ("Bearer ", self.api_key_env)})

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        posted = await send(self.request(state, questions, options=options))
        data = posted.data
        usage = data.get("usage") or {}
        return Response(
            answers=systemone.answers(data["answers"]),
            answered_by=data.get("model", self.model_id),
            # No cost: TypeSafe returns none (a list price in s1flow.toml estimates it, client/cost.py).
            usage=Usage(input_tokens=usage.get("input_tokens") or 0, output_tokens=usage.get("output_tokens") or 0, raw=usage or None),
            latency_ms=posted.latency_ms,
            retries=posted.retries,
        )


class TypeSafeOptions(Options):
    base_url: str = BASE_URL  # any server that speaks TypeSafe's API
    api_key_env: str = "TYPESAFE_API_KEY"


def needs(spec: ModelSpec) -> Needs:
    o = spec_options(TypeSafeOptions, spec)
    return Needs(keys=(o.api_key_env,), hosts=(origin(o.base_url),))


@declares(needs)
def build(b: ModelBuild) -> TypeSafeModel:
    o = options(TypeSafeOptions, b)
    return TypeSafeModel(b.spec.id, concurrency=b.spec.concurrency or 8, capabilities=b.spec.capabilities, base_url=o.base_url, api_key_env=o.api_key_env)
