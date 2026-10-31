"""List prices: data in s1flow.toml, not code; an estimate from recorded tokens; never 0 for "not known" (no network)."""

import asyncio
import datetime as dt
import re
from pathlib import Path

import httpx
import pytest
import respx
from conftest import make_project

from s1flow.client import Capabilities, ChoiceAnswer, Response
from s1flow.client.answers import Usage
from s1flow.client.cost import Spend, estimate, recorded
from s1flow import Client
from s1flow.client.models import ModelSpec, Price
from s1flow.eval import metrics, report
from s1flow.project import verify
from s1flow.eval import run as running
from s1flow.eval.evaluation import cost_note
from s1flow.eval.task import load

ROOT = Path(__file__).resolve().parents[1]
P = Price(input_per_mtok=0.042, as_of="2026-10-03", source="test")


def test_no_provider_holds_a_price():
    for f in (ROOT / "src" / "s1flow" / "client" / "providers").glob("*.py"):
        assert not re.search(r"PRICE|USD_PER", f.read_text()), f.name


def test_a_list_price_gives_the_numbers_the_constants_gave():
    # The constants that were in typesafe.py, cloudflare.py and openai_decisions.py, priced as they priced.
    for mtok, per_token in [(0.042, 0.042 / 1_000_000), (0.24, 0.24e-6), (0.09, 0.09e-6), (0.10, 0.10 / 1_000_000)]:
        for tokens in (1, 276, 12_345):
            assert Price(input_per_mtok=mtok, as_of="2026-10-03", source="t").cost(tokens, 7) == tokens * per_token


def test_what_a_price_cannot_tell_is_not_known():
    assert P.cost(0, 0) is None  # the model reported no tokens
    with_image = Price(per_request=0.001, per_image=0.01, as_of="2026-10-03", source="t")
    assert with_image.cost(0, 0, images=2) == pytest.approx(0.021) and with_image.cost(5, 0, images=None) is None
    assert Price(as_of="2026-10-03", source="free").cost(10, 10) == 0.0  # free is 0, and said so


def test_billed_is_never_repriced_and_list_is_marked():
    billed = Usage(input_tokens=100, cost_usd=0.5, cost_source="billed")
    assert estimate(billed, P) is billed
    listed = estimate(Usage(input_tokens=100), P)
    assert listed.cost_source == "list" and listed.cost_usd == 100 * (0.042 / 1_000_000)
    assert estimate(Usage(), P).cost_usd is None  # no tokens: still not known, not 0
    assert recorded(billed, P) == (0.5, "billed") and recorded(Usage(input_tokens=100), P) == (100 * (0.042 / 1_000_000), "list")
    assert recorded(Usage(cost_usd=0.7), P) == (0.7, None)  # nothing to price: as recorded
    assert recorded(None, P) == (None, None)  # no usage recorded: not known


def test_a_spend_counts_the_unknown_apart_and_says_where_the_costs_came_from():
    s = Spend()
    assert s.source is None and s.total_usd == 0.0
    s.add(0.5, "billed")
    s.add(None, None)
    assert (s.costs, s.unknown, s.source) == ([0.5], 1, "billed")
    s.add(0.25, "list")
    assert s.total_usd == 0.75 and s.source == "mixed"
    s.add(0.1, None)  # a cost whose source is not recorded says nothing of where the others came from
    assert s.sources == {"billed", "list"}


@respx.mock
def test_the_line_up_prices_a_model_that_bills_nothing(tmp_path, monkeypatch):
    from s1flow.client.providers.typesafe import BASE_URL

    monkeypatch.setenv("TYPESAFE_API_KEY", "test")
    toml = tmp_path / "s1flow.toml"
    toml.write_text('default = ["jev"]\n[models.jev]\nprovider = "typesafe"\nid = "jev-latest"\n'
                    'price = { input_per_mtok = 0.042, as_of = "2026-10-03", source = "t" }\n')
    respx.post(f"{BASE_URL}/systemone").mock(return_value=httpx.Response(200, json={
        "model": "jev-1.13.0", "answers": {"q": {"type": "noul", "noul": 0.8}}, "usage": {"input_tokens": 276, "output_tokens": 0}}))
    from s1flow.client.questions import Boolean

    m = Client(connections=toml).connections.build("jev")
    d = asyncio.run(m.decide("x", {"q": Boolean(instructions="?")}))
    assert m.id == "typesafe:jev-latest" and d.usage.cost_source == "list" and d.usage.cost_usd == 276 * (0.042 / 1_000_000)  # as typesafe.py priced it


class Tokens:
    """Answers every case with 1,000 input tokens and no cost, as a model that bills nothing back."""

    def __init__(self, b=None):
        self.id, self.concurrency, self.capabilities = "fake:tokens", 4, Capabilities()

    async def decide(self, state, questions, *, options=None):
        q = next(iter(questions))
        return Response(answers={q: ChoiceAnswer(choice="wake", probabilities={"wake": 0.9, "sleep": 0.1})}, answered_by=self.id,
                        usage=Usage(input_tokens=1000))


def test_a_report_prices_the_recorded_tokens_with_todays_price(tmp_path):
    p = make_project(tmp_path, {"tok": Tokens}, copy_tasks=("nod-wake",))
    asyncio.run(running.run(load(p, "nod-wake"), ["tok"], limit=20))
    e = metrics.evaluate(t := load(p, "nod-wake"), metrics.load(t, "base", "tok"))
    assert e.calls.cost_per_10k_usd is None and e.calls.cost_unknown == e.failures.calls  # no price: not known, not free
    assert "calls whose API cost is not known" in report.write(t, "base", t.where.root / "out")
    toml = tmp_path / "s1flow.toml"
    toml.write_text(toml.read_text().replace('id = "tok"', 'id = "tok"\nprice = { input_per_mtok = 2.0, as_of = "2026-10-19", source = "t" }'))
    p2 = type(p)(p.root)  # s1flow.toml read again; the runs are the same
    e = metrics.evaluate(t := load(p2, "nod-wake"), metrics.load(t, "base", "tok"))
    assert e.calls.cost_per_10k_usd == pytest.approx(1000 * 2.0 / 1_000_000 * 10_000) and e.calls.cost_source == "list"
    assert e.calls.price and e.calls.price.as_of == "2026-10-19" and e.calls.cost_unknown == 0


def test_the_note_says_which_costs_are_estimates():
    assert cost_note([("a", "billed", None, 0)]) is None
    note = cost_note([("a", "billed", None, 0), ("jev", "list", "2026-10-03", 0), ("x", None, None, 3)])
    assert note and "jev (list price of 2026-10-03)" in note and "x 3" in note and "do not compare as they are" in note


# ---------- s1flow models --verify ----------


def spec(provider, model, **price):
    return ModelSpec(provider=provider, id=model, price=Price(as_of=price.pop("as_of", "2026-10-15"), source="t", **price))


@respx.mock
def test_verify_compares_a_price_with_the_providers_list(monkeypatch):
    from s1flow.client.providers import openrouter

    monkeypatch.setattr(openrouter, "_listed", None)
    listing = respx.get(openrouter.MODELS_URL).mock(return_value=httpx.Response(200, json={"data": [
        {"id": "a/m", "pricing": {"prompt": "0.0000001", "completion": "0.0000004"}}]}))
    today = dt.date(2026, 10, 19)
    assert verify.check_price(spec("openrouter", "a/m", input_per_mtok=0.1, output_per_mtok=0.4), None, today).status == "same"
    drift = verify.check_price(spec("openrouter", "a/m", input_per_mtok=0.2, output_per_mtok=0.4), None, today)
    assert drift.status == "differs" and "input_per_mtok 0.2 here, 0.1 listed" in drift.detail
    old = verify.check_price(spec("openrouter", "a/m", input_per_mtok=0.1, output_per_mtok=0.4, as_of="2026-06-01"), None, today)
    assert old.status == "old"
    assert verify.check_price(spec("openrouter", "b/m", input_per_mtok=0.1), None, today).status == "unlisted"
    assert listing.call_count == 1  # read once a process
    assert verify.check_price(ModelSpec(provider="openrouter", id="a/m"), None, today) is None  # no price: billed


def test_verify_says_when_a_price_cannot_be_checked(monkeypatch):
    got = verify.check_price(spec("typesafe", "jev-latest", input_per_mtok=0.042, as_of="2025-01-01"), None)
    assert got and got.status == "unchecked" and "publishes no price list" in got.detail

    def down(spec, cache_dir):
        raise httpx.ConnectError("no network")

    from s1flow.client.providers import gateway

    monkeypatch.setattr(gateway.build, "published", down)
    assert verify.check_price(spec("gateway", "x/y", input_per_mtok=1), None).status == "unreadable"


def test_a_cost_that_does_not_say_where_it_came_from_is_not_known():
    from s1flow.client.cost import Spend

    s = Spend()
    s.add(0.01, "billed")
    s.add(0.02, None)  # an answer cached before costs carried their source
    assert s.total_usd == 0.01 and s.unknown == 1 and s.source == "billed"
