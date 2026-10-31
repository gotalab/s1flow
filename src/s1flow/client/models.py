"""The decision-model contract, and what it takes to add a model.

What crosses the boundary:

- in: a `State` (text, JSON, or a list of parts whose images are prepared `Image`s) and `Questions`
- out: a `Response` (a `Refusal` for a question the model declined), or one of four errors
  (`Unsupported`, `Rejected`, `ProviderError`, `DataError`, core/errors.py)
- declared up front: each model's `Capabilities` (s1flow.toml), checked before any call

A `ModelSpec` (one entry of s1flow.toml) is turned into a `DecisionModel` by a `ProviderFactory`,
built in (s1flow.client.providers) or your own ("package.module:factory").
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from ..core.errors import DataError, NotFound, Unsupported
from .answers import Response
from .questions import TEXT_TYPES, Choice, Questions, QuestionType
from .state import State, has_image, has_unprepared_image

VERSION = re.compile(r"[^\s:/,]+")  # a version's name (ModelSpec.versions)


class Capabilities(BaseModel):
    """Declared per model in s1flow.toml and checked before any call. Each claim is one that
    `s1flow models --verify` tests (question types, image, box): a 200 does not prove a model sees the image."""

    model_config = ConfigDict(extra="forbid")
    question_types: frozenset[QuestionType] = TEXT_TYPES
    image: bool = False
    distribution: Literal["native", "sampled", "none"] = "native"
    context_tokens: int = Field(default=32_000, gt=0)
    max_options: int | None = Field(default=None, gt=0)
    # The longest instructions / option description the model is known to take, in characters.
    # Not checked before a call (the exact limit is not published); `optimize` writes within it.
    max_instructions_chars: int | None = Field(default=None, gt=0)
    max_description_chars: int | None = Field(default=None, gt=0)
    # Requests a minute the model allows (a free tier's limit). The provider paces its calls to it, and
    # choosing a model shows it; it is the model's declaration, not something --verify can test.
    per_minute: int | None = Field(default=None, gt=0)

    @field_serializer("question_types")
    def _sorted(self, v: frozenset[QuestionType]) -> list[QuestionType]:
        return sorted(v)  # a set dumps in hash order, which changes between runs: a policy's diff would show it


class Price(BaseModel):
    """A model's list price, declared in s1flow.toml (`price.input_per_mtok = ...`) for a model that bills nothing back.

    What it costs is an estimate from the tokens the model reports (client/cost.py): a model can charge what
    tokens do not show (cached input, unseen reasoning, a minimum), so a model that returns what it billed
    (AI Gateway, OpenRouter) is never priced from here. A price these four parts cannot write is left out."""

    model_config = ConfigDict(extra="forbid")
    input_per_mtok: float = Field(default=0.0, ge=0)  # USD per million input tokens
    output_per_mtok: float = Field(default=0.0, ge=0)
    per_request: float = Field(default=0.0, ge=0)  # USD per call
    per_image: float = Field(default=0.0, ge=0)  # USD per image in the state
    as_of: str  # the day the price was read (YYYY-MM-DD); `s1flow models --verify` warns when it is old
    source: str  # where it was read: a URL, or how

    def cost(self, input_tokens: int, output_tokens: int, images: int | None = 0) -> float | None:
        """USD for one call; None when the call reported no tokens to price, or the images were not counted."""
        if (self.input_per_mtok or self.output_per_mtok) and not (input_tokens or output_tokens):
            return None
        if self.per_image and images is None:
            return None
        # Per token first, then times the tokens: the order the prices in code had, so the numbers stay the same.
        tokens = input_tokens * (self.input_per_mtok / 1_000_000) + output_tokens * (self.output_per_mtok / 1_000_000)
        return tokens + self.per_request + self.per_image * (images or 0)


@runtime_checkable
class DecisionModel(Protocol):
    id: str  # goes into the evaluation's cache key: changes when the endpoint or the model does
    capabilities: Capabilities
    concurrency: int

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response: ...


class Version(BaseModel):
    """One version a model serves, under a name its other models share (`jev:1.14`, `jev@openrouter:1.14`; `4.1-flash-2026-10-17`)."""

    model_config = ConfigDict(extra="forbid")
    id: str  # the provider's own string for it, sent as it is (`typesafe/jev-1.14`)
    # What this version takes beyond (or short of) the model: each field given replaces the model's.
    capabilities: Capabilities | None = None




class ModelSpec(BaseModel):
    """One model of s1flow.toml (an entry of `[models]`): which provider calls it, with what id, and what it takes."""

    model_config = ConfigDict(extra="forbid")
    provider: str  # a built-in kind (providers.BUILTIN) or your own, as "package.module:factory"
    provider_revision: str | None = Field(default=None, min_length=1)  # app-declared custom implementation commit/package revision
    id: str  # what the provider sends (the provider's own string for the model)
    # None: the model serves one version. A mapping version -> Version: `name:<version>` asks for that version,
    # each is probed by `s1flow models --verify` and shown by `s1flow models`. With versions, an `id` that is
    # none of theirs is an alias (`jev-latest`): it runs and compares, and a policy names a version instead.
    versions: dict[str, Version] | None = None
    concurrency: int | None = Field(default=None, ge=1)  # None: the provider's default
    capabilities: Capabilities = Capabilities()
    options: dict[str, Any] = Field(default_factory=dict)  # provider-specific, validated by its factory
    price: Price | None = None  # a list price, for a model that does not return what it billed
    note: str = ""

    @field_validator("versions")
    @classmethod
    def _versions(cls, v: dict[str, Version] | None) -> dict[str, Version] | None:
        """A version is s1flow's own name, any string but empty and without whitespace, ":" (`model:version`), "/"
        (`model:version/variant`, a candidate) or "," (--models a,b). It is not parsed: `1.14`, `2026-10-17` and
        `4.1-flash-2026-10-17` are names alike."""
        if v is not None and (bad := [k for k in v if not VERSION.fullmatch(k)]):
            raise ValueError(f"a version is not empty and holds no whitespace, ':', '/' or ',': {bad}")
        return v

    @property
    def alias(self) -> bool:
        """The model declares versions and `id` is none of theirs: which one answers can change under it."""
        return self.versions is not None and self.version is None

    @property
    def version(self) -> str | None:
        """The version whose id `id` is, if it is one."""
        return next((k for k, v in (self.versions or {}).items() if v.id == self.id), None)

    def at(self, version: str) -> ModelSpec:
        """The model as one version: that version's id as `id`, its capabilities over the model's, and no versions."""
        if self.versions is None or version not in self.versions:
            known = ", ".join(self.versions or {}) or "none"
            raise NotFound(f"no version {version!r}; versions: {known}")
        v = self.versions[version]
        update: dict[str, Any] = {"id": v.id, "versions": None}
        if v.capabilities is not None:
            own = self.capabilities.model_dump(exclude_unset=True) | v.capabilities.model_dump(exclude_unset=True)
            update["capabilities"] = Capabilities.model_validate(own)
        return self.model_copy(update=update)

    def resolved(self) -> ModelSpec:
        """What the model sends as it is: the version `id` is, when it is one."""
        return self if self.version is None else self.at(self.version)


@dataclass(frozen=True)
class ModelBuild:
    """What a provider factory gets to build one model."""

    name: str  # the name in s1flow.toml
    spec: ModelSpec  # at the version asked for with `name:<version>` (ModelSpec.at): `spec.id` is what to send
    cache_dir: Path | None = None  # where a provider may keep what it computes once (price lists)


# Builds the model or raises ConfigError when the spec does not fit the provider.
ProviderFactory = Callable[[ModelBuild], DecisionModel]


def check_supported(model: DecisionModel, state: State, questions: Questions) -> None:
    if has_unprepared_image(state):  # the case is wrong whatever the model takes
        raise DataError("the state has image references that were never prepared; pass task.model_state(case)")
    caps = model.capabilities
    for qid, q in questions.items():
        if q.type not in caps.question_types:
            raise Unsupported(f"{model.id} does not take {q.type} questions ({qid})")
        if caps.max_options and isinstance(q, Choice) and len(q.criteria) > caps.max_options:
            raise Unsupported(f"{model.id} takes at most {caps.max_options} options ({qid})")
    if has_image(state) and not caps.image:
        raise Unsupported(f"{model.id} does not take images")
