"""Cloudflare Workers AI's System One models: Clef and Clef-flash.

Called through `clef-proxy/` (a local `wrangler dev` relay with an AI binding), so the
wrangler login is enough and no API token is needed. Start it with
`npx wrangler dev --config clef-proxy/wrangler.jsonc --port 8788`.

Images go in Clef's own top-level `images[]` (data URLs, at most 4), which the model reads
before the state; `[image n]` stays in the state where each one was. `assets` is refused.
"""

from __future__ import annotations

import re
from typing import Any

from ..answers import ChoiceAnswer, Response, Usage
from ..endpoints import cloudflare_relay
from ..images import data_url, placeholders
from ..models import Capabilities, ModelBuild, ModelSpec, check_supported
from ..questions import Questions
from ..state import State, has_image
from .build import NoOptions, options
from .http import Request, send
from .needs import Needs, declares, origin
from . import systemone



def safe_options(questions: Questions) -> tuple[Questions, dict[str, dict[str, str]]]:
    """Workers AI rejects option names with "/" ("kind/bug", 2026-10-07): send safe names, keep the way back."""
    out: Questions = {}
    back: dict[str, dict[str, str]] = {}
    for qid, q in questions.items():
        if q.type == "choice" and any(not re.fullmatch(r"[\w-]+", k) for k in q.criteria):
            names = {k: f"o{i}_" + re.sub(r"[^\w-]", "_", k) for i, k in enumerate(q.criteria)}
            out[qid] = q.model_copy(update={"criteria": {names[k]: v for k, v in q.criteria.items()}})
            back[qid] = {v: k for k, v in names.items()}
        else:
            out[qid] = q
    return out, back



class CloudflareModel:
    def __init__(self, model: str, *, concurrency: int = 8, capabilities: Capabilities | None = None):
        self.model = model
        self.id = f"cloudflare:{model}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities(context_tokens=65_536)

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        sent, _ = safe_options(questions)
        body: dict[str, Any] = {"model": self.model, "state": state, "questions": systemone.questions(sent)}
        if has_image(state):
            body["state"], imgs = placeholders(state)
            body["images"] = [data_url(i) for i in imgs]
        return Request(f"{cloudflare_relay()}/run/@cf/cloudflare/{self.model}", body)

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        _, back = safe_options(questions)
        posted = await send(self.request(state, questions, options=options))
        data = posted.data
        out = data["result"]
        usage = out.get("usage") or {}
        answers = systemone.answers(out["answers"])
        for qid, names in back.items():
            a = answers.get(qid)
            if isinstance(a, ChoiceAnswer):
                answers[qid] = a.model_copy(update={
                    "choice": names.get(a.choice, a.choice),
                    "probabilities": {names.get(k, k): p for k, p in a.probabilities.items()} if a.probabilities else a.probabilities,
                })
        return Response(
            answers=answers,
            answered_by=out.get("model", self.model),
            usage=Usage(input_tokens=usage.get("input_tokens") or 0, raw=usage or None),  # priced from s1flow.toml's list, if any
            latency_ms=posted.latency_ms,
            retries=posted.retries,
            provider_metadata={"ai_ms": data.get("ai_ms")},
        )


def needs(spec: ModelSpec) -> Needs:
    """No key: the relay calls Workers AI with its own wrangler login."""
    relay = cloudflare_relay()
    return Needs(hosts=(origin(relay),), note=f"through the clef-proxy relay at {relay} (CLEF_RELAY_URL), which needs a wrangler login")


@declares(needs)
def build(b: ModelBuild) -> CloudflareModel:
    options(NoOptions, b)
    return CloudflareModel(b.spec.id, concurrency=b.spec.concurrency or 8, capabilities=b.spec.capabilities)
