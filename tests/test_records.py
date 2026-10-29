"""The outcome contract: how a call's end becomes a run record (no network)."""

import asyncio
import json

import httpx
import pytest
import respx

from s1flow.core.errors import DataError, ProviderError, Rejected, Unsupported

from s1flow.eval import records
from s1flow.eval.records import PredictionRecord
from s1flow.client.providers.http import classify, post_json
from s1flow.client import BooleanAnswer, Response, Refusal, Boolean, ModelSpec
from s1flow.client.identity import request_digest

URL = "https://example.test/v1/systemone"
BASE = {"id": "a", "model": "jev", "prompt": "p1", "at": "2026-10-16",
        "request_digest": request_digest(ModelSpec(provider="typesafe", id="jev"), {"text": "case a"}, {"q": Boolean(instructions="?")})}


@pytest.mark.parametrize("status, text, kind", [
    (422, "too long", Rejected),
    (413, "payload too large", Rejected),
    (400, '{"error":{"message":"Phala does not accept \\"image_url\\" parts in state"}}', Rejected),
    (400, '{"detail":{"error_type":"api_usage_error","message":"Invalid request."}}', ProviderError),
    (401, "unauthorized", ProviderError),
])
def test_classify(status, text, kind):
    e = classify(status, text)
    assert type(e) is kind and e.status == status


@respx.mock
def test_post_json_retries_then_fails_with_the_status():
    route = respx.post(URL).mock(side_effect=[httpx.Response(503), httpx.Response(503), httpx.Response(503)])
    with pytest.raises(ProviderError) as e:
        asyncio.run(post_json(URL, {}, {}, attempts=3))
    assert e.value.status == 503 and route.call_count == 3


@respx.mock
def test_post_json_does_not_retry_a_refusal():
    route = respx.post(URL).mock(return_value=httpx.Response(422, text="nope"))
    with pytest.raises(Rejected):
        asyncio.run(post_json(URL, {}, {}))
    assert route.call_count == 1


@respx.mock
def test_post_json_rejects_an_unreadable_body():
    respx.post(URL).mock(return_value=httpx.Response(200, text="<html>"))
    with pytest.raises(ProviderError, match="unreadable"):
        asyncio.run(post_json(URL, {}, {}))


@pytest.mark.parametrize("exc, outcome, status", [
    (Unsupported("no images"), "unsupported", None),
    (Rejected("too big", 413), "rejected", 413),
    (ProviderError("boom", 502), "failed", 502),
    (DataError("image file not found"), "data_error", None),
    (KeyError("answers"), "failed", None),
])
def test_every_exception_has_one_outcome(exc, outcome, status):
    r = records.from_exception(BASE, exc)
    assert (r.outcome, r.status) == (outcome, status) and r.reason


def test_a_line_says_its_outcome_and_reads_back():
    ok = records.from_response(BASE, Response(answers={"q": BooleanAnswer(probability=0.9)}, answered_by="jev-1.13.0"), "q", False, 8)
    d = json.loads(ok.line())
    assert d["outcome"] == "answered" and d["answer"]["probability"] == 0.9 and PredictionRecord.model_validate(d) == ok
    refused = json.loads(records.from_exception(BASE, Rejected("too big", 413)).line())
    assert (refused["outcome"], refused["reason"], refused["status"]) == ("rejected", "too big", 413)
    with pytest.raises(ValueError):
        PredictionRecord.model_validate(BASE | {"outcome": "failed", "error": "boom"})  # the old keys are not read


def test_a_record_must_be_consistent():
    with pytest.raises(ValueError):
        PredictionRecord.model_validate(BASE | {"outcome": "answered"})  # no answer
    with pytest.raises(ValueError):
        PredictionRecord.model_validate(BASE | {"outcome": "failed", "answer": {"type": "boolean", "probability": 1.0}})


def test_numeric_ids_become_strings():
    assert PredictionRecord.model_validate(BASE | {"id": 5, "outcome": "failed", "reason": "x"}).id == "5"
    assert records.from_exception(BASE | {"id": 7}, ProviderError("boom")).id == "7"


def test_a_bare_not_supported_400_stays_a_failure():
    assert type(classify(400, '{"error":"response_format not supported"}')) is ProviderError


def test_an_answer_needs_its_value():
    with pytest.raises(ValueError):
        BooleanAnswer.model_validate({"type": "boolean"})
    with pytest.raises(ValueError):  # the other types' keys are not read: one shape per type
        BooleanAnswer.model_validate({"type": "boolean", "probability": 0.9, "choice": None})


def test_a_refusal_is_recorded_as_rejected():
    r = records.from_response(BASE, Response(answers={"q": Refusal(reason="unsafe")}, answered_by="m"), "q", False, 8)
    assert (r.outcome, r.reason, r.answer) == ("rejected", "the model refused to answer q: unsafe", None)
