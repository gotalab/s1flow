"""A provider of your own, as s1flow.toml names one ("toy_provider:build"): it answers all four question types
from the words of the state, so a test can call it without a network. Imports s1flow.client and its errors alone."""

from __future__ import annotations

import os
from typing import Any

from s1flow.client import (
    BooleanAnswer, BoxAnswer, BoxEdges, Capabilities, ChoiceAnswer, Response, ModelBuild, Questions, Refusal, ScoreAnswer, State, Usage,
)
from s1flow.client.models import check_supported
from s1flow.core.errors import ConfigError


class Toy:
    def __init__(self, b: ModelBuild):
        self.id, self.concurrency = f"toy:{b.spec.id}", 2
        self.capabilities = Capabilities(question_types=frozenset({"boolean", "choice", "score", "box"}), image=True)
        self.calls = 0
        self.key_env: str | None = b.spec.options.get("key")  # a key it needs, as the built-in providers do

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        if self.key_env and not os.environ.get(self.key_env):
            raise ConfigError(f"{self.key_env} is not set")
        self.calls += 1
        text = str(state).lower()
        out: dict[str, Any] = {}
        for qid, q in questions.items():
            if "refuse" in q.instructions:
                out[qid] = Refusal(reason="not this one")
            elif q.type == "boolean":
                out[qid] = BooleanAnswer(probability=0.9 if "bug" in text else 0.1)
            elif q.type == "choice":
                pick = next((k for k in q.criteria if k in text), next(iter(q.criteria)))
                out[qid] = ChoiceAnswer(choice=pick, probabilities={k: 0.8 if k == pick else 0.2 / (len(q.criteria) - 1) for k in q.criteria}, confidence=0.7)
            elif q.type == "score":
                probs = {"0": 0.1, "1": 0.3, "2": 0.6}
                out[qid] = ScoreAnswer(score=sum(int(k) * p for k, p in probs.items()), probabilities=probs)
            else:
                out[qid] = BoxAnswer(box=BoxEdges(top=0.1, bottom=0.5, left=0.2, right=0.6), confidence=0.95)
        return Response(answers=out, answered_by=f"{self.id}-1", usage=Usage(input_tokens=10, cost_usd=0.00001), latency_ms=5.0, retries=0)


def build(b: ModelBuild) -> Toy:
    return Toy(b)
