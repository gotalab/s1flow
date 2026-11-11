"""What every built-in provider sends for fixed inputs, how it reads fixed replies, and how a policy turns fixed
answers into decisions, against tests/fixtures/wire-format.json (no network).

A saved answer, cache entry or adoption stays valid across s1flow releases while its identity matches
(client/identity.py), and that identity hashes no s1flow version or source. So when this test fails, decide:
if answers saved before the change no longer stand for the new request or reading, bump identity.REQUEST (what
is sent or read) or identity.EXECUTION (what a policy decides); if they still stand, leave it. Then rewrite the
file and commit it with the change:

    S1FLOW_WRITE_WIRE_FORMAT=1 pytest tests/test_wire_format.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import httpx
import pytest
import respx

from s1flow.client import BooleanAnswer, ChoiceAnswer, Client, Image
from s1flow.client import identity
from s1flow.client.models import Capabilities, ModelSpec
from s1flow.client.questions import Boolean, Choice, Score
from s1flow.policies import DecisionRule
from s1flow.policies.kinds import KindParams, kind_of

FILE = Path(__file__).parent / "fixtures" / "wire-format.json"

QUESTIONS = {
    "kind": Choice(instructions="What kind of issue?", criteria={"kind/bug": "it is broken", "kind/question": None}),
    "refund": Boolean(instructions="Does it ask for a refund?"),
    "urgency": Score(instructions="How urgent?", criteria=["low", "high"]),
}
# Keys out of order at two depths: what is sent is the state with its keys sorted.
TEXT = {"title": "Crash on start", "meta": {"z": 1, "a": [{"y": 2, "b": 3}]}}
PIXEL = Image(media_type="image/png", data="iVBORw0KGgo=", sha256="0" * 64, width=4, height=3)
WITH_IMAGE = ["The screen shows:", PIXEL]

SYSTEM_ONE = {
    "kind": {"type": "choice", "choice": "kind/bug", "probabilities": {"kind/bug": 0.8, "kind/question": 0.2}, "confidence": 0.7},
    "refund": {"type": "noul", "noul": 0.1},
    "urgency": {"type": "score", "score": 0.6, "probabilities": {"0": 0.4, "1": 0.6}},
}
REPLIES: dict[str, dict[str, Any]] = {
    "typesafe": {"model": "jev-1.14.0", "answers": SYSTEM_ONE, "usage": {"input_tokens": 90, "output_tokens": 0}},
    "gateway": {"model": "typesafe-ai/jev", "answers": SYSTEM_ONE | {"refund": {"type": "boolean", "probability": 0.1}},
                "usage": {"inputTokens": 90, "outputTokens": 0},
                "providerMetadata": {"typesafe": {"confidence": {"kind": 0.9}}, "gateway": {"cost": "0.00001"}}},
    "openrouter": {"model": "typesafe/jev", "answers": SYSTEM_ONE, "usage": {"input_tokens": 90, "output_tokens": 0, "cost": 0.00001}},
    "cloudflare": {"result": {"model": "clef", "answers": SYSTEM_ONE | {"kind": SYSTEM_ONE["kind"] | {
        "choice": "o0_kind_bug", "probabilities": {"o0_kind_bug": 0.8, "o1_kind_question": 0.2}}}, "usage": {"input_tokens": 90}}},
    "openai-decisions": {"model": "gpt-6-luna", "answers": [
        {"type": "choice", "name": "kind", "choice": "kind/bug",
         "probabilities": [{"value": "kind/bug", "probability": 0.8}, {"value": "kind/question", "probability": 0.2}], "confidence": 0.7},
        {"type": "predicate", "name": "refund", "probability": 0.1},
        {"type": "score", "name": "urgency", "score": 0.6,
         "probabilities": [{"value": 0, "label": "0", "probability": 0.4}, {"value": 1, "label": "1", "probability": 0.6}]},
    ], "usage": {"input_tokens": 90, "output_tokens": 0}},
}
MODELS = {
    "typesafe": ModelSpec(provider="typesafe", id="jev-1.14.0", capabilities=Capabilities(image=True)),
    "gateway": ModelSpec(provider="gateway", id="typesafe-ai/jev", capabilities=Capabilities(image=True)),
    "openrouter": ModelSpec(provider="openrouter", id="typesafe/jev", capabilities=Capabilities(image=True)),
    "cloudflare": ModelSpec(provider="cloudflare", id="clef", capabilities=Capabilities(image=True)),
    "openai-decisions": ModelSpec(provider="openai-decisions", id="gpt-6-luna"),
    "llm": ModelSpec(provider="llm", id="openai/gpt-test", capabilities=Capabilities(image=True)),
}
# Headers every call carries from httpx, or a key: not what a provider chooses to send.
TRANSPORT = {"host", "accept", "accept-encoding", "connection", "user-agent", "content-length", "content-type", "authorization"}


def _sent(request: httpx.Request) -> dict[str, Any]:
    return {"url": str(request.url), "headers": {k: v for k, v in request.headers.items() if k.lower() not in TRANSPORT},
            "body": json.loads(request.content)}


def _read(response: Any) -> dict[str, Any]:
    return {"answered_by": response.answered_by, "answers": {k: a.model_dump(mode="json") for k, a in response.answers.items()}}


def _http(provider: str) -> dict[str, Any]:
    out = {}
    with respx.mock(assert_all_called=False) as mock:
        route = mock.post().mock(return_value=httpx.Response(200, json=REPLIES[provider]))
        for name, state in (("text", TEXT), ("image", WITH_IMAGE)):
            if name == "image" and not MODELS[provider].capabilities.image:
                continue
            got = Client().responses.create(model=MODELS[provider], state=state, questions=QUESTIONS)
            out[name] = {"sent": _sent(route.calls.last.request), "read": _read(got)}
    return out


def _llm(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    import litellm

    calls: list[dict[str, Any]] = []
    content = json.dumps({"kind": "kind/bug", "refund": False, "urgency": 1})

    async def acompletion(**kwargs: Any) -> Any:
        calls.append({k: v for k, v in kwargs.items() if k != "api_key"})
        usage = SimpleNamespace(prompt_tokens=90, completion_tokens=12, model_dump=lambda mode=None: {"prompt_tokens": 90})
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))], usage=usage, _hidden_params={})

    monkeypatch.setattr(litellm, "acompletion", acompletion)
    out = {}
    for name, state in (("text", TEXT), ("image", WITH_IMAGE)):
        got = Client().responses.create(model=MODELS["llm"], state=state, questions=QUESTIONS)
        out[name] = {"sent": calls[-1], "read": _read(got)}
    return out


def _decisions() -> dict[str, Any]:
    """What a policy decides from fixed answers, under each rule a policy can hold."""
    yes_no = kind_of(QUESTIONS["refund"])
    choice = kind_of(QUESTIONS["kind"], KindParams(positive="kind/bug"))
    bug = ChoiceAnswer(choice="kind/bug", probabilities={"kind/bug": 0.7, "kind/question": 0.3})
    cases = {
        "boolean threshold 0.3": (yes_no, [BooleanAnswer(probability=0.4)], DecisionRule(threshold=0.3)),
        "boolean min probability 0.9": (yes_no, [BooleanAnswer(probability=0.8)], DecisionRule(min_probability=0.9)),
        "choice min probability 0.6": (kind_of(QUESTIONS["kind"]), [bug], DecisionRule(min_probability=0.6)),
        "choice with a positive, min probability 0.8": (choice, [bug], DecisionRule(min_probability=0.8)),
        "choice with a positive, threshold 0.75": (choice, [bug], DecisionRule(threshold=0.75)),
    }
    return {name: kind.read(answers, rule).model_dump(mode="json") for name, (kind, answers, rule) in cases.items()}


def test_what_is_sent_and_read_is_what_the_identity_formats_name(monkeypatch):
    for env in ("TYPESAFE_API_KEY", "AI_GATEWAY_API_KEY", "OPENROUTER_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(env, raising=False)
    monkeypatch.setenv("CLEF_RELAY_URL", "https://relay.test")
    now = {
        "request": identity.REQUEST, "execution": identity.EXECUTION,
        "providers": {p: _http(p) for p in REPLIES} | {"llm": _llm(monkeypatch)},
        "decisions": _decisions(),
    }
    text = json.dumps(now, ensure_ascii=False, indent=1) + "\n"  # key order kept: the order sent is compared too
    if os.environ.get("S1FLOW_WRITE_WIRE_FORMAT"):
        FILE.write_text(text)
    assert text == FILE.read_text(), (
        "what a provider sends or reads, or what a policy decides, changed (diff tests/fixtures/wire-format.json): "
        "bump identity.REQUEST or EXECUTION unless saved answers still stand, then rewrite it (see this file's docstring)")
