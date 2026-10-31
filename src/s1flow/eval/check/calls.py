"""Asking a version about the test cases as production does (policies.Policy), through the evaluation's cache."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from ... import policies
from ...client import cost
from ...core.errors import ProviderError
from ...policies.file import PolicySpec
from ..cases import Case
from ..objectives import measure
from ..objectives.measure import Pairs
from ..policy import EvaluatedPolicy
from ..run import CachedClient, cached
from ..task import Task


@dataclass(frozen=True)
class Version:
    """A version check asks: what runs, and the evaluation it was adopted on (none for one adopted with adopt --spec)."""

    spec: PolicySpec
    record: EvaluatedPolicy | None = None

    @property
    def variant(self) -> str | None:
        return self.record.candidate.variant if self.record else None


@dataclass
class Side:
    """One version's answers to the test cases, read as the SDK reads them."""

    name: str  # how it was asked for: current, next, v2, draft
    policy: Version
    pairs: Pairs  # each test case's label and the policy's reading (none when the call failed)
    spend: cost.Spend = field(default_factory=cost.Spend)
    latency_ms: list[float] = field(default_factory=list)
    latency_unknown: int = 0
    calls: int = 0
    cached: int = 0


async def ask(task: Task, name: str, r: Version, cases: list[Case]) -> Side:
    """Each case decided by the policy as in production (policies.Policy), through the evaluation's cache."""
    client = CachedClient(task.where.client(), task.where.cache_dir)
    policy = policies.DecisionPolicy(r.spec, client=client)
    sem = asyncio.Semaphore(client.connections.build(policy.model_spec).concurrency)
    side = Side(name, r, measure.pairs(task.kind, [], []))
    errors: list[str] = []

    async def one(case: Case) -> policies.Decision | None:
        async with sem:
            try:
                state = task.model_state(case)
                d = await policy.adecide(state)
            except ProviderError as e:  # a failed call has no answer: not sure, not right
                errors.append(f"{type(e).__name__}: {str(e)[:200]}")
                return None
        x = d.response
        assert x is not None  # a decision made here holds its response; one read from a span does not
        hit = client.responses.hit(x)
        side.calls += not hit
        side.cached += hit
        # A cached answer keeps the cost it was made at; a list cost is priced again from the policy's price.
        u = cost.estimate(x.usage, policy.model_spec.price, cost.images_in(state))
        side.spend.add(u.cost_usd, u.cost_source)
        if client.responses.timing_current(x):
            side.latency_ms.append(x.latency_ms)
        else:
            side.latency_unknown += 1
        return d

    outs = await asyncio.gather(*(one(c) for c in cases))
    if cases and len(errors) == len(cases):  # no network, the model is down: nothing was measured, which is not a pass
        raise ProviderError(f"{name}: every call failed ({errors[0]})")
    side.pairs = measure.pairs(task.kind, [c.label for c in cases], outs)  # the labels are the task's; the readings, the policy's
    return side


def missing(task: Task, r: Version, cases: list[Case]) -> int:
    """Calls this version would have to make: answers not in the cache."""
    policy = policies.DecisionPolicy(r.spec, client=task.where.client())
    qs = {r.spec.question_id: r.spec.question}
    return sum(not cached(task.where.cache_dir, policy.model_spec, task.model_state(c), qs) for c in cases)
