"""What a decision model answers: one answer per question, in the shape of its type, and the `Response`
that carries them.

Field names follow the decision-model SDKs (TypeSafe, OpenAI, OpenRouter, Workers AI): `probability`
(yes / no), `choice` / `score` with `probabilities` and the vendor's `confidence`. A question the model
declined is a `Refusal`, the others of the same call still answered (OpenAI's per-question refusal).
"""

from __future__ import annotations

from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BoxEdges(BaseModel):
    """Edges as fractions of the image's height (top, bottom) and width (left, right), from the top-left."""

    model_config = ConfigDict(frozen=True)
    top: float = Field(ge=0, le=1)
    bottom: float = Field(ge=0, le=1)
    left: float = Field(ge=0, le=1)
    right: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def _ordered(self) -> BoxEdges:
        if self.top > self.bottom or self.left > self.right:
            raise ValueError(f"box edges out of order: {self}")
        return self

    @classmethod
    def clipped(cls, top: float, bottom: float, left: float, right: float) -> BoxEdges:
        """A model's box, clipped into the image and put in order (a float a hair past 1 is not a failure)."""
        c = lambda v: min(1.0, max(0.0, float(v)))
        (t, b), (l, r) = sorted((c(top), c(bottom))), sorted((c(left), c(right)))
        return cls(top=t, bottom=b, left=l, right=r)


class _Answer(BaseModel):
    # Frozen, like Response: a value set after construction would skip validation, and the contract
    # (providers/contract.py) relies on these types for everything but ranges and options.
    model_config = ConfigDict(extra="forbid", frozen=True)


class BooleanAnswer(_Answer):
    type: Literal["boolean"] = "boolean"
    probability: float  # P(true)


class ChoiceAnswer(_Answer):
    type: Literal["choice"] = "choice"
    choice: str
    probabilities: dict[str, float] | None = None  # None when the model returns no distribution
    confidence: float | None = None  # the vendor's own number (TypeSafe's is rescaled by the number of options)


class ScoreAnswer(_Answer):
    type: Literal["score"] = "score"
    score: float  # the level, or the expected level when the model gives a distribution
    probabilities: dict[str, float] | None = None  # keyed by the level's index, "0".."L-1"
    confidence: float | None = None


class BoxAnswer(_Answer):
    type: Literal["box"] = "box"
    box: BoxEdges
    confidence: float | None = None  # jev's confidence in its box
    agreement: float | None = None  # a box from k samples: the mean IoU of the samples with the answer


class Refusal(_Answer):
    """The model declined to answer this question (its limit, not a failed call)."""

    type: Literal["refusal"] = "refusal"
    reason: str | None = None


Answer = Annotated[Union[BooleanAnswer, ChoiceAnswer, ScoreAnswer, BoxAnswer, Refusal], Field(discriminator="type")]
Given = BooleanAnswer | ChoiceAnswer | ScoreAnswer | BoxAnswer  # an answer that is not a refusal


CostSource = Literal["billed", "list"]


class Usage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float | None = None  # None: not known (never 0 for "not known")
    # billed: what the model said it charged. list: an estimate, tokens times a list price (s1flow.toml's,
    # or LiteLLM's for an LLM). None: not known.
    cost_source: CostSource | None = None
    raw: dict[str, Any] | None = None  # the usage as the model returned it, kept so a cost can be worked out again


class Response(BaseModel):
    """One call's answers, keyed by question name."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    answers: dict[str, Answer]
    answered_by: str  # the model that actually answered (a version, where the model names one)
    usage: Usage = Field(default_factory=Usage)
    # The attempt that answered, request to response: retries and the backoff before them left out.
    latency_ms: float = 0.0
    retries: int = 0  # attempts before the answering one
    provider_metadata: dict[str, Any] = Field(default_factory=dict)  # what the model adds (routing, samples)
