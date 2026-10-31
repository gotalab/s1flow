"""Shared by the provider factories: read a spec's `options` into the provider's own type."""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, ConfigDict, ValidationError

from ...core.errors import ConfigError, invalid
from ..models import ModelBuild, ModelSpec


class Options(BaseModel):
    """A provider's options. Unknown keys are an error, so a typo in s1flow.toml does not pass silently."""

    model_config = ConfigDict(extra="forbid")


class NoOptions(Options):
    pass


O = TypeVar("O", bound=Options)


def spec_options(kind: type[O], spec: ModelSpec) -> O:
    try:
        return kind.model_validate(spec.options)
    except ValidationError as e:
        raise ConfigError(f"options do not fit provider {spec.provider!r}: {invalid(e)}") from None


def options(kind: type[O], b: ModelBuild) -> O:
    try:
        return spec_options(kind, b.spec)
    except ConfigError as e:
        raise ConfigError(f"{b.name}: {e}") from None
