"""Provider contract on recorded responses (no network)."""

import asyncio

import httpx
import pytest
import respx

from s1flow.client.providers.gateway import BASE_URL, GatewayModel
from s1flow.client.providers.llm import json_schema, to_answers
from s1flow.client.providers.openai_decisions import BASE_URL as OPENAI_URL, DecisionsModel
from s1flow.core.errors import Unsupported
from s1flow.client import Boolean, Capabilities, Choice, Image, Score

QS = {
    "route": Choice(instructions="担当", criteria={"billing": "請求", "technical": None}),
    "refund": Boolean(instructions="返金を求めているか"),
}

# Recorded from convaiinnovations/laya on 2026-10-03, trimmed.
LAYA = {
    "model": "convaiinnovations/laya",
    "answers": {
        "route": {"type": "choice", "choice": "billing", "probabilities": {"billing": 0.9999, "technical": 0}},
        "refund": {"type": "boolean", "probability": 0.9978},
    },
    "usage": {"inputTokens": 82, "outputTokens": 0},
    "providerMetadata": {"typesafe": {"confidence": {"route": 0.9994}}, "gateway": {"cost": "0"}},
}


@respx.mock
def test_gateway_parses_answers(monkeypatch):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "test")
    route = respx.post(f"{BASE_URL}/evaluate").mock(return_value=httpx.Response(200, json=LAYA))
    r = asyncio.run(GatewayModel("convaiinnovations/laya").decide("二重に請求された", QS))
    assert route.calls[0].request.headers["authorization"] == "Bearer test"
    assert r.answers["route"].choice == "billing" and r.answers["route"].confidence == 0.9994
    assert r.answers["refund"].probability == 0.9978
    assert r.usage.cost_usd == 0.0 and r.usage.cost_source == "billed" and r.usage.input_tokens == 82
    assert r.usage.raw == LAYA["usage"]  # kept as returned, so a cost can be worked out again


@respx.mock
def test_gateway_retries_on_429(monkeypatch):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "test")
    respx.post(f"{BASE_URL}/evaluate").mock(side_effect=[httpx.Response(429), httpx.Response(200, json=LAYA)])
    r = asyncio.run(GatewayModel("convaiinnovations/laya").decide("x", QS))
    assert r.answers["route"].choice == "billing"
    assert r.retries == 1 and r.latency_ms < 400  # the 500ms backoff is not the model's latency


def test_unsupported_is_raised_before_any_call():
    m = GatewayModel("typesafe-ai/jev", capabilities=Capabilities(question_types={"choice"}))
    with pytest.raises(Unsupported):
        asyncio.run(m.decide("x", QS))
    with pytest.raises(Unsupported):
        img = Image(media_type="image/png", data="AAAA", sha256="0", width=300, height=300)
        asyncio.run(GatewayModel("typesafe-ai/jev").decide(["x", img], QS))


def test_llm_schema_and_sampled_distribution():
    qs = QS | {"urgency": Score(instructions="緊急度", criteria=["low", "high"])}
    schema = json_schema(qs)
    assert schema["properties"]["route"]["enum"] == ["billing", "technical"]
    assert schema["properties"]["urgency"]["enum"] == [0, 1]
    one = to_answers([{"route": "billing", "refund": True, "urgency": 1}], qs, distribution=False)
    assert one["route"].probabilities is None and one["refund"].probability == 1.0
    many = to_answers(
        [{"route": "billing", "refund": True, "urgency": 1}] * 3 + [{"route": "technical", "refund": False, "urgency": 0}],
        qs,
        distribution=True,
    )
    assert many["route"].probabilities == {"billing": 0.75, "technical": 0.25}
    assert many["refund"].probability == 0.75
    assert many["urgency"].score == pytest.approx(0.75)


# Recorded from gpt-6-luna on the OpenAI Decisions API on 2026-10-07, usage trimmed.
LUNA = {
    "model": "gpt-6-luna",
    "answers": [
        {"type": "choice", "name": "route", "choice": "billing",
         "probabilities": [{"value": "billing", "probability": 0.94}, {"value": "technical", "probability": 0.06}], "confidence": 0.88},
        {"type": "predicate", "name": "refund", "probability": 0.47},
        {"type": "score", "name": "urgency", "score": 0.41,
         "probabilities": [{"value": 0, "label": "0", "probability": 0.59}, {"value": 1, "label": "1", "probability": 0.41}], "confidence": 0.18},
    ],
    "usage": {"input_tokens": 375, "output_tokens": 0, "total_tokens": 375},
}


@respx.mock
def test_decisions_wire_format_and_answers(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    route = respx.post(f"{OPENAI_URL}/decisions").mock(return_value=httpx.Response(200, json=LUNA))
    qs = QS | {"urgency": Score(instructions="緊急度", criteria=["low", "high"])}
    r = asyncio.run(DecisionsModel("gpt-6-luna").decide("二重に請求された", qs))
    sent = route.calls[0].request.read()
    assert b'"type":"predicate"' in sent.replace(b" ", b"") and b'"levels"' in sent
    assert r.answers["route"].probabilities == {"billing": 0.94, "technical": 0.06} and r.answers["route"].confidence == 0.88
    assert r.answers["refund"].type == "boolean" and r.answers["refund"].probability == 0.47
    assert r.answers["urgency"].score == 0.41 and r.answers["urgency"].probabilities == {"0": 0.59, "1": 0.41}
    # The provider knows no price: s1flow.toml's list price estimates it (tests/test_prices.py).
    assert r.usage.input_tokens == 375 and r.usage.cost_usd is None and r.usage.raw == {"input_tokens": 375, "output_tokens": 0, "total_tokens": 375}


def test_clef_option_names_are_made_safe_and_mapped_back():
    from s1flow.client.providers.cloudflare import safe_options

    sent, back = safe_options({"kind": Choice(instructions="種類", criteria={"kind/bug": "壊れている", "kind/question": None})})
    assert all("/" not in k for k in sent["kind"].criteria)
    assert sorted(back["kind"].values()) == ["kind/bug", "kind/question"]
    assert safe_options(QS)[1] == {}  # plain names go through unchanged


# Recorded from jev on TypeSafe's own API on 2026-10-07.
TYPESAFE = {"model": "jev-1.13.0", "answers": {"refund": {"type": "noul", "noul": 0.84}}, "usage": {"input_tokens": 276, "output_tokens": 0}}


@respx.mock
def test_typesafe_direct_sends_noul_and_reports_tokens(monkeypatch):
    from s1flow.client.providers.typesafe import BASE_URL as TS_URL, TypeSafeModel

    monkeypatch.setenv("TYPESAFE_API_KEY", "test")
    route = respx.post(f"{TS_URL}/systemone").mock(return_value=httpx.Response(200, json=TYPESAFE))
    r = asyncio.run(TypeSafeModel("jev-latest").decide("返金して", {"refund": QS["refund"]}))
    assert b'"noul"' in route.calls[0].request.read()
    assert r.answers["refund"].type == "boolean" and r.answers["refund"].probability == 0.84
    assert r.answered_by == "jev-1.13.0" and r.usage.input_tokens == 276 and r.usage.cost_usd is None and r.usage.cost_source is None


def test_an_answer_outside_the_contract_is_a_named_provider_failure():
    from s1flow.client.providers.systemone import answers as parse_answers
    from s1flow.client.providers.openai_decisions import parse_decisions
    from s1flow.core.errors import ProviderError

    with pytest.raises(ProviderError, match="answered level outside the contract: .*score"):
        parse_decisions([{"type": "score", "name": "level", "probabilities": []}])
    with pytest.raises(ProviderError, match="answered q outside the contract"):
        parse_answers({"q": {"type": "choice"}}, None)
    with pytest.raises(ProviderError, match="answered q outside the contract"):
        parse_answers({"q": None}, None)


def test_a_refusal_is_the_questions_answer_and_the_others_still_count():
    from s1flow.client import Refusal
    from s1flow.client.providers.systemone import answers as parse_answers
    from s1flow.client.providers.openai_decisions import parse_decisions

    got = parse_answers({"q": {"type": "refusal", "refusal": "unsafe"}, "b": {"type": "noul", "noul": 0.9}}, None)
    assert got["q"] == Refusal(reason="unsafe") and got["b"].probability == 0.9
    assert parse_decisions([{"type": "refusal", "name": "q"}]) == {"q": Refusal()}


def test_the_system_one_dialect_is_one_module():
    from s1flow.client.providers import systemone

    qs = {"bug": Boolean(instructions="Is it a bug?"), "level": Score(instructions="How bad?", criteria=["low", "high"])}
    assert systemone.questions(qs)["bug"]["type"] == "noul" and systemone.questions(qs, noul=False)["bug"]["type"] == "boolean"
    assert systemone.questions(qs)["level"] == {"type": "score", "instructions": "How bad?", "criteria": ["low", "high"]}
    got = systemone.answers({"bug": {"type": "noul", "noul": 0.8}, "level": {"type": "score", "score": 1, "probabilities": {"0": 0.2, "1": 0.8}}},
                            {"level": 0.6})
    assert got["bug"].probability == 0.8 and got["level"].confidence == 0.6 and got["level"].probabilities == {"0": 0.2, "1": 0.8}


def _keyed_models():
    from s1flow.client.providers.openrouter import BASE_URL as OR_URL, OpenRouterModel
    from s1flow.client.providers.typesafe import BASE_URL as TS_URL, TypeSafeModel

    return [  # each built-in provider that sends a key: the model, the URL it posts to, the key it reads
        (lambda: GatewayModel("typesafe-ai/jev"), f"{BASE_URL}/evaluate", "AI_GATEWAY_API_KEY"),
        (lambda: OpenRouterModel("typesafe-ai/jev"), f"{OR_URL}/systemone", "OPENROUTER_API_KEY"),
        (lambda: TypeSafeModel("jev-latest"), f"{TS_URL}/systemone", "TYPESAFE_API_KEY"),
        (lambda: DecisionsModel("gpt-6-luna"), f"{OPENAI_URL}/decisions", "OPENAI_API_KEY"),
    ]


@pytest.mark.parametrize("model,url,env", _keyed_models(), ids=lambda x: x if isinstance(x, str) and x.endswith("KEY") else "")
@respx.mock
def test_an_unset_key_is_left_for_a_proxy_and_named_when_refused(monkeypatch, model, url, env):
    """No key in the environment: the call goes out without it (a sandbox's proxy may add it), and a 401 or 403
    back is the missing key's error, with where to get one."""
    from s1flow.core.errors import ConfigError

    monkeypatch.delenv(env, raising=False)
    route = respx.post(url).mock(return_value=httpx.Response(401, json={"error": "no key"}))
    with pytest.raises(ConfigError, match=rf"{env} is not set and the provider refused the call without it \(401: .*\): get one at https://"):
        asyncio.run(model().decide("返金して", {"refund": QS["refund"]}))
    assert "authorization" not in route.calls[0].request.headers


@respx.mock
def test_a_proxy_that_adds_the_key_answers_without_it(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    route = respx.post(f"{OPENAI_URL}/decisions").mock(return_value=httpx.Response(200, json=LUNA))
    r = asyncio.run(DecisionsModel("gpt-6-luna").decide("二重に請求された", QS))
    assert "authorization" not in route.calls[0].request.headers and r.answers["refund"].probability == 0.47


@respx.mock
def test_a_set_key_refused_is_named_and_a_403_stays_the_providers(monkeypatch):
    from s1flow.core.errors import ConfigError, ProviderError

    monkeypatch.setenv("OPENAI_API_KEY", "wrong")
    route = respx.post(f"{OPENAI_URL}/decisions").mock(return_value=httpx.Response(401, json={"error": "bad key"}))
    with pytest.raises(ProviderError, match=r"the provider did not accept OPENAI_API_KEY \(401: .*\): check the key") as e:
        asyncio.run(DecisionsModel("gpt-6-luna").decide("x", QS))
    assert not isinstance(e.value, ConfigError) and e.value.status == 401
    assert route.calls[0].request.headers["authorization"] == "Bearer wrong"
    route.mock(return_value=httpx.Response(403, json={"error": "flagged by moderation"}))
    with pytest.raises(ProviderError, match=r"^403: ") as e:
        asyncio.run(DecisionsModel("gpt-6-luna").decide("x", QS))
    assert not isinstance(e.value, ConfigError)


@pytest.mark.parametrize("model,env", [("vercel_ai_gateway/anthropic/claude-haiku-4.5", "AI_GATEWAY_API_KEY"), ("gpt-5-mini", "OPENAI_API_KEY")])
def test_an_llm_without_its_key_sends_a_stand_in_and_names_the_key_when_refused(monkeypatch, model, env):
    """LiteLLM will not send without a key, so an unset one goes as a stand-in a proxy replaces; a 401 back is the
    missing key's error. A key that is set goes as is."""
    litellm = pytest.importorskip("litellm")
    from s1flow.client.providers import llm
    from s1flow.core.errors import ConfigError

    sent = []

    async def refuse(**kw):
        sent.append(kw["api_key"])
        raise litellm.AuthenticationError("no key", llm_provider="openai", model=model)

    monkeypatch.setattr(litellm, "acompletion", refuse)
    monkeypatch.delenv(env, raising=False)
    with pytest.raises(ConfigError, match=rf"{env} is not set and the provider refused the call without it"):
        asyncio.run(llm.complete(model, []))
    assert sent == [llm.UNSET_KEY]

    async def answer(**kw):
        sent.append(kw["api_key"])
        return "response"

    monkeypatch.setattr(litellm, "acompletion", answer)
    monkeypatch.setenv(env, "real")
    assert asyncio.run(llm.complete(model, [])).response == "response" and sent[-1] == "real"
