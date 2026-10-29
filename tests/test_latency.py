"""Latency: what one call's time means, how a run records it, and how a report uses it (no network)."""

import asyncio
import json

import numpy as np
from conftest import binary_preds, make_project
from test_objectives import cov

from s1flow.objectives import Constraints, Coverage
from s1flow.client import Capabilities, ChoiceAnswer, Response
from s1flow.eval import metrics, records, report
from s1flow.eval import run as running
from s1flow.eval.task import load


class Timed:
    """Answers right on every case after 120 ms, with one retry as a provider would report it."""

    def __init__(self, b=None):
        self.id, self.concurrency, self.capabilities = "fake:t", 4, Capabilities()
        self.ms, self.retries = 120, 1

    async def decide(self, state, questions, *, options=None):
        q = next(iter(questions))
        a = ChoiceAnswer(choice="wake", probabilities={"wake": 0.99, "sleep": 0.01})
        return Response(answers={q: a}, answered_by=self.id, latency_ms=self.ms, retries=self.retries)


def test_a_run_records_retries_and_the_concurrency_it_ran_at(tmp_path):
    p = make_project(tmp_path, {"timed": Timed}, copy_tasks=("nod-wake",))
    task = load(p, "nod-wake")
    asyncio.run(running.run(task, ["timed"], limit=3, concurrency=1))
    path = running.run_path(task, "base", "timed")
    assert {(r.latency_ms, r.retries, r.concurrency) for r in records.read(path)} == {(120.0, 1, 1)}
    assert json.loads(path.with_suffix(".meta.json").read_text())["measured"]["concurrency"] == 1
    # Asked again with the model's own concurrency, a cached answer keeps the conditions it was measured under.
    asyncio.run(running.run(task, ["timed"], limit=3, fresh=False))
    client = p.client()
    hit, cached = asyncio.run(running.call(p.cache_dir, client, client.connections.build("timed"), task.model_state(task.load_cases().all()[0]), task.questions("base"), 0, spec=client.connections.resolved("timed")))
    assert cached and hit.concurrency == 1


def preds(ms, retries=None, concurrency=8):
    n = len(ms)
    return binary_preds(
        [0.9] * n, [True] * n, latency_ms=np.array(ms, dtype=float), retries=retries if retries is not None else [0] * n, concurrency=[concurrency] * n,
    )


def test_latency_stats_show_the_tail_and_what_is_unknown():
    ms = [100.0] * 98 + [900.0, 1000.0]
    t = metrics.latency(preds(ms, retries=[0] * 97 + [2, None, 1]))
    assert t and t.p50_ms == 100 and t.max_ms == 1000 and t.p99_ms > 800 and (t.spread or 0) > 8
    assert t.retried == 2 and t.unrecorded == 1 and t.concurrency == [8] and t.n == 100


def test_a_time_budget_takes_slow_models_out_of_the_headline(tmp_path):
    from s1flow.client import Choice
    from s1flow.eval import Task

    t = Task(id="t", cases="x", state=lambda r: r, question=Choice(instructions="?", criteria={"a": None, "b": None}), label=lambda r: r, objective=Coverage())
    fast, slow = (e.model_copy(update={"answered_ids": [str(i) for i in range(e.n)]})
                  for e in (cov("fast", 0.6, p99=150.0), cov("slow", 0.9, p99=900.0)))
    budgeted = t.copy(constraints=Constraints(latency_p99_ms=200))
    text = report.headline(budgeted, [fast, slow])
    assert "**fast**" in text and "slow breaks a constraint and is left out (p99 900ms > 200ms)" in text
    assert "**slow**" in report.headline(t, [fast, slow])


def test_llm_retries_are_ours_and_left_out_of_the_latency(monkeypatch):
    import litellm

    from s1flow.client.providers import llm

    calls = []

    async def fake(**kw):
        calls.append(kw["num_retries"])
        if len(calls) == 1:
            raise litellm.RateLimitError("slow down", llm_provider="openai", model="m")
        return "response"

    monkeypatch.setattr(litellm, "acompletion", fake)
    done = asyncio.run(llm.complete("openai/m", [], api_key_env=None))
    assert done.response == "response" and done.retries == 1 and done.latency_ms < 400
    assert calls == [0, 0]  # litellm does not retry on its own
