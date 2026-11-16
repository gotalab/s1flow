"""Values read from the state (text, number, date) and estimates: the questions, their answers, OpenRouter's
Extractions route and the contract. Answers below are the ones the models gave on 2026-11-16."""

import asyncio
import datetime as dt
import json

import httpx
import pytest
import respx
from pydantic import ValidationError

from s1flow.client import Capabilities, Client, DateAnswer, EstimateAnswer, Image, ModelSpec, NumberAnswer, Refusal, TextAnswer
from s1flow.client.providers import extractions
from s1flow.client.providers.contract import validate_response
from s1flow.client.providers.openrouter import EXTRACTIONS_URL, OpenRouterModel
from s1flow.client.answers import Response
from s1flow.core.errors import ProviderError, Unsupported
from s1flow.policies.kinds import kind_of
from s1flow.questions import Boolean, Date, Estimate, Number, Text

STATE = "Invoice INV-2291 issued 2026-09-02, net 30. Total $1080."
QS = {
    "invoice": Text(instructions="The invoice number"),
    "total": Number(instructions="The total", unit="USD"),
    "issued": Date(instructions="The issue date"),
    "days": Estimate(instructions="Days until it is paid", min=0, max=120, step=1),
}
CLAIRIC = {
    "invoice": {"type": "text", "value": "INV-2291", "guess": "INV-2291", "span": [8, 16], "p_null": 0.00001, "confidence": 0.99998},
    "total": {"type": "number", "value": 1080, "guess": 1080, "p_null": 0.0004, "confidence": 0.9978},
    "issued": {"type": "date", "value": "2026-09-02", "guess": "2026-09-02", "p_null": 0.00002, "confidence": 0.99998},
    "days": {"type": "estimate", "value": 30, "mean": 29.54, "median": 30, "p10": 26, "p90": 31, "p_below": 2e-8, "p_above": 4e-7},
}
FIELD_MODEL = ModelSpec(provider="openrouter", id="cloudflare/clairic",
                        capabilities=Capabilities(question_types=frozenset({"text", "number", "date", "estimate"})))


def test_a_field_question_is_sent_as_it_is_written():
    assert extractions.fields(QS) == {
        "invoice": {"type": "text", "instructions": "The invoice number"},
        "total": {"type": "number", "instructions": "The total", "unit": "USD"},
        "issued": {"type": "date", "instructions": "The issue date"},
        "days": {"type": "estimate", "instructions": "Days until it is paid", "min": 0, "max": 120, "step": 1},
    }


def test_an_estimate_needs_its_range_in_order():
    with pytest.raises(ValidationError, match="min is under its max"):
        Estimate(instructions="?", min=5, max=5)
    with pytest.raises(ValidationError):
        Estimate(instructions="?", min=0, max=5, step=0)
    with pytest.raises(ValidationError, match="Extra inputs"):
        Number(instructions="?", units="USD")


def test_each_answer_is_read_with_what_its_model_gave():
    got = extractions.answers(CLAIRIC)
    assert got["invoice"] == TextAnswer(value="INV-2291", guess="INV-2291", span=(8, 16), p_null=0.00001, confidence=0.99998)
    assert got["total"] == NumberAnswer(value=1080.0, guess=1080.0, p_null=0.0004, confidence=0.9978)
    assert got["issued"].value == dt.date(2026, 9, 2)
    assert got["days"] == EstimateAnswer(value=30.0, p10=26.0, p90=31.0)
    # Nothing there: Clairic keeps its guess and how sure it is of it, Perplexity and ScaleDown say nothing more.
    absent = extractions.answers({
        "po": {"type": "text", "value": None, "guess": "INV-2291", "span": [8, 16], "p_null": 0.99999, "confidence": 0.9989},
        "bare": {"type": "text", "value": None},
        "price": {"type": "number", "value": None, "guess": 3, "p_null": 0.9999, "confidence": 0.023},
    })
    assert absent["po"].value is None and absent["po"].guess == "INV-2291" and absent["po"].p_null == 0.99999
    assert absent["bare"] == TextAnswer(value=None)
    assert absent["price"].value is None and absent["price"].guess == 3.0
    # Schematron: the value alone.
    assert extractions.answers({"total": {"type": "number", "value": 1080}})["total"] == NumberAnswer(value=1080.0)
    assert extractions.answers({"q": {"type": "refusal", "refusal": "unsafe"}})["q"] == Refusal(reason="unsafe")


@pytest.mark.parametrize("answer", [
    {"type": "list", "value": ["a"]},  # a type s1flow has no question for
    {"type": "number"},  # no value
    {"type": "number", "value": "many"},
    {"type": "date", "value": "next week"},
    {"type": "estimate", "value": None},
])
def test_an_answer_that_does_not_fit_is_the_providers_failure(answer):
    with pytest.raises(ProviderError, match="answered q outside the contract"):
        extractions.answers({"q": answer})


@respx.mock
def test_openrouter_asks_fields_on_the_extractions_route():
    route = respx.post(EXTRACTIONS_URL).mock(return_value=httpx.Response(200, json={
        "model": "cloudflare/clairic-20261029", "provider": "Cloudflare", "answers": CLAIRIC,
        "usage": {"input_tokens": 543, "output_tokens": 0, "passes": 3, "cost": 0.0000543}}))
    got = Client().responses.create(model=FIELD_MODEL, state=STATE, questions=QS)
    sent = json.loads(route.calls.last.request.content)
    assert sent == {"model": "cloudflare/clairic", "state": STATE, "fields": extractions.fields(QS)}
    assert got.answered_by == "cloudflare/clairic-20261029" and got.usage.cost_usd == 0.0000543 and got.usage.cost_source == "billed"
    assert got.answers["invoice"].span == (8, 16) and got.answers["days"].p90 == 31.0
    # A JSON state is read as its text.
    Client().responses.create(model=FIELD_MODEL, state={"note": STATE}, questions=QS)
    assert json.loads(route.calls.last.request.content)["state"] == json.dumps({"note": STATE}, ensure_ascii=False, indent=1)


def test_one_call_asks_one_route():
    model = OpenRouterModel("cloudflare/clairic", capabilities=Capabilities(image=True, question_types=frozenset({"text", "boolean"})))
    with pytest.raises(Unsupported, match="another route than the rest: ask invoice in a call of their own"):
        asyncio.run(model.decide(STATE, {"invoice": QS["invoice"], "paid": Boolean(instructions="Is it paid?")}))
    image = Image(media_type="image/png", data="iVBORw0KGgo=", sha256="0" * 64, width=10, height=10)
    with pytest.raises(Unsupported, match="from a text state"):
        asyncio.run(model.decide(["A scan:", image], {"invoice": QS["invoice"]}))
    with pytest.raises(Unsupported, match="does not take number questions"):
        asyncio.run(model.decide(STATE, {"total": QS["total"]}))


@pytest.mark.parametrize(("qid", "answer", "detail"), [
    ("invoice", NumberAnswer(value=1.0), "answer type 'number' does not fit a text question"),
    ("invoice", TextAnswer(value="x", p_null=1.5), "p_null must be finite between 0 and 1"),
    ("invoice", TextAnswer(value="x", span=(9, 3)), r"span \[9, 3\] is not a start and an end in order"),
    ("total", NumberAnswer(value=float("inf")), "value must be finite"),
    ("days", EstimateAnswer(value=30, p10=40, p90=20), "p10 40 is over p90 20"),
    ("days", EstimateAnswer(value=121), r"estimate 121 is outside 0\.\.120"),
])
def test_the_contract_checks_a_field_answer_against_its_question(qid, answer, detail):
    with pytest.raises(ProviderError, match=detail):
        validate_response(Response(answers={qid: answer}, answered_by="m"), {qid: QS[qid]}, "m")
    ok = Response(answers={"days": EstimateAnswer(value=30, p10=26, p90=31), "issued": DateAnswer(value=None)}, answered_by="m")
    assert validate_response(ok, {"days": QS["days"], "issued": QS["issued"]}, "m") is ok


def test_a_field_question_has_no_kind_yet():
    """Asked through the client; nothing labels, reads or holds one until its kind exists."""
    for q in QS.values():
        with pytest.raises(ValueError, match=f"a {q.type} question is not evaluated or held by a policy yet"):
            kind_of(q)
