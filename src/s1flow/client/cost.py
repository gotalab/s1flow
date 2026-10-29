"""What a call cost: what the model billed, else an estimate from its list price, else not known.

Providers know no prices. A model that returns what it charged (AI Gateway, OpenRouter) reports it as
`billed`; for the others s1flow.toml may declare a `Price`, and the line-up prices each call from the tokens it
reports (`Listed`), marked `list`. A list cost is an estimate, and the evaluation works it out again from the
recorded tokens when it reports (eval/metrics.py), so a corrected price needs no call.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .answers import CostSource, Response, Usage
from .models import Capabilities, DecisionModel, Price
from .questions import Questions
from .state import Image, State


def images_in(state: State) -> int:
    return sum(isinstance(p, Image) for p in state) if isinstance(state, list) else 0


def estimate(usage: Usage, price: Price | None, images: int | None = None) -> Usage:
    """The usage, its cost priced from the list where the model billed nothing; as it is otherwise."""
    if price is None or usage.cost_source == "billed":
        return usage
    cost = price.cost(usage.input_tokens, usage.output_tokens, images)
    if cost is None:
        return usage
    return usage.model_copy(update={"cost_usd": cost, "cost_source": "list"})


def recorded(usage: Usage | None, price: Price | None) -> tuple[float | None, CostSource | None]:
    """A recorded call's (cost, source): billed as billed, else tokens times today's list price, else as recorded
    (None, None: no usage recorded)."""
    if usage is None:
        return None, None
    if price is None or usage.cost_source == "billed":
        return usage.cost_usd, usage.cost_source
    listed = price.cost(usage.input_tokens, usage.output_tokens, None)
    return (usage.cost_usd, usage.cost_source) if listed is None else (listed, "list")


@dataclass
class Spend:
    """The API cost of some calls: the costs known, in the order they were added, how many calls are not
    known (counted as nothing, not as free), and where the known ones came from."""

    costs: list[float] = field(default_factory=list)
    unknown: int = 0
    sources: set[CostSource] = field(default_factory=set)

    def add(self, cost_usd: float | None, source: CostSource | None) -> None:
        if cost_usd is None or source is None:  # a cost that does not say where it came from (an answer cached before 2026-10-19) is not known
            self.unknown += 1
            return
        self.costs.append(cost_usd)
        self.sources.add(source)

    @property
    def total_usd(self) -> float:
        total = 0.0
        for c in self.costs:  # in call order (sum() would compensate, and give other last digits)
            total += c
        return total

    @property
    def source(self) -> Literal["billed", "list", "mixed"] | None:
        """billed, list (an estimate) or both; None when no known cost says."""
        return "mixed" if len(self.sources) > 1 else next(iter(self.sources), None)


class Listed:
    """A model of the line-up whose calls are priced from its spec's list price (`estimate`)."""

    def __init__(self, inner: DecisionModel, price: Price):
        self.inner, self.price = inner, price
        self.id, self.concurrency = inner.id, inner.concurrency

    @property
    def capabilities(self) -> Capabilities:
        return self.inner.capabilities

    @capabilities.setter
    def capabilities(self, caps: Capabilities) -> None:  # --verify sets the declaration aside on the model it calls
        self.inner.capabilities = caps

    def __getattr__(self, name: str) -> Any:
        """What the provider's model adds beyond the contract (`request`), as its own."""
        return getattr(self.inner, name)

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        d = await self.inner.decide(state, questions, options=options)
        return d.model_copy(update={"usage": estimate(d.usage, self.price, images_in(state))})


def listed(model: DecisionModel, price: Price | None) -> DecisionModel:
    return model if price is None else Listed(model, price)
