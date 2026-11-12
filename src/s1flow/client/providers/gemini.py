"""Google's Decisions API on the Gemini API (`POST /v1beta/decisions`): Gemini Decision 1 without OpenRouter
in between.

The wire format is System One's, with three differences (https://aistudio.google.com/docs/decisions-api,
2026-11-12): the state goes in `input`, as text or content blocks (JSON is sent as its text); a yes / no
question's criteria are `true_description` / `false_description`; and usage is `total_input_tokens`, with no
cost (s1flow.toml's list price estimates it). The key goes in `x-goog-api-key`.

Images, audio, video and PDFs are content blocks with base64 `data` (media.gemini_blocks). An input the safety
filters block is a 400 whose error `code` names the filter: the provider refused the input (Rejected). A key
Google does not accept is a 400 too (`API_KEY_INVALID`), even when none was sent.
"""

import re
from typing import Any

from ...core.errors import ProviderError, Rejected
from ..answers import Response, Usage
from ..media import gemini_blocks, text_of
from ..models import Capabilities, ModelBuild, ModelSpec, check_supported
from ..questions import Boolean, Choice, Questions
from ..state import State, has_media
from .build import NoOptions, options, spec_options
from .http import Request, send
from .needs import Needs, declares, origin
from . import systemone

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
BLOCKED = re.compile(r'"code"\s*:\s*"(safety|prohibited_content|blocklist|image_safety|content_blocked)"')
BOOLEAN_CRITERIA = {"true": "true_description", "false": "false_description"}


def wire_questions(qs: Questions) -> dict[str, Any]:
    wire = systemone.questions(qs)
    for name, q in qs.items():
        if isinstance(q, Boolean) and q.criteria:
            wire[name]["criteria"] = {BOOLEAN_CRITERIA.get(k, k): v for k, v in q.criteria.items()}
        elif isinstance(q, Choice):
            wire[name]["criteria"] = {k: v or "" for k, v in q.criteria.items()}  # "" for an option without a description
    return wire


def input_of(state: State) -> str | list[dict[str, str]]:
    if has_media(state):
        return gemini_blocks(state)
    return text_of(state)


class GeminiModel:
    def __init__(self, model_id: str, *, concurrency: int = 8, capabilities: Capabilities | None = None):
        self.model_id = model_id
        self.id = f"gemini:{model_id}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities()

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        body: dict[str, Any] = {"model": self.model_id, "input": input_of(state), "questions": wire_questions(questions)}
        if options:
            body.update(options)
        return Request(f"{BASE_URL}/decisions", body, keys={"x-goog-api-key": ("", "GEMINI_API_KEY")})

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        try:
            posted = await send(self.request(state, questions, options=options))
        except ProviderError as e:
            if e.status == 400 and BLOCKED.search(str(e)):
                raise Rejected(f"blocked by the provider's safety filters: {str(e)[:200]}", e.status) from e
            if e.status == 400 and "API_KEY_INVALID" in str(e):  # Google's answer to a bad key is a 400, not a 401
                raise ProviderError(f"the provider did not accept GEMINI_API_KEY ({str(e)[:120]}): check the key", e.status) from e
            raise
        data = posted.data
        usage = data.get("usage") or {}
        return Response(
            answers=systemone.answers(data["answers"]),
            answered_by=data.get("model", self.model_id),
            usage=Usage(input_tokens=usage.get("total_input_tokens") or 0, raw=usage or None),  # priced from s1flow.toml's list
            latency_ms=posted.latency_ms,
            retries=posted.retries,
        )


def needs(spec: ModelSpec) -> Needs:
    spec_options(NoOptions, spec)
    return Needs(keys=("GEMINI_API_KEY",), hosts=(origin(BASE_URL),))


@declares(needs)
def build(b: ModelBuild) -> GeminiModel:
    options(NoOptions, b)
    return GeminiModel(b.spec.id, concurrency=b.spec.concurrency or 8, capabilities=b.spec.capabilities)
