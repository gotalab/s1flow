"""The line-up, read from s1flow.toml. Edit s1flow.toml, not this file, to add or change a model.

Each entry is a `ModelSpec`; its `provider` names the factory that builds it: a built-in kind
(providers.BUILTIN), "package.module:factory", or an entry point in the `s1flow.providers` group.

Lineup owns configuration data, validation and name/version resolution only. It neither builds
providers nor owns a provider cache. Client.connections owns those runtime operations.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, PrivateAttr, ValidationError, field_validator, model_validator

from ..core import place
from ..core.errors import ConfigError, NotFound, invalid
from .models import ModelSpec

NAME = re.compile(r"[A-Za-z0-9][\w.+@-]*")  # no ":" (it asks for a version) and no "," (it separates --models)
BUILTIN_LINEUP = Path(__file__).resolve().parents[1] / "templates" / "s1flow.toml"  # what `init` copies


class Lineup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    default: list[str]
    models: dict[str, ModelSpec]
    _path: Path | None = PrivateAttr(default=None)

    @field_validator("models")
    @classmethod
    def _names(cls, v: dict[str, ModelSpec]) -> dict[str, ModelSpec]:
        if bad := [n for n in v if not NAME.fullmatch(n)]:
            raise ValueError(f"model names may hold letters, digits and . _ + @ - only: {bad}")
        return v

    @model_validator(mode="after")
    def _default_known(self) -> Lineup:
        if unknown := [n for n in self.default if n not in self.models]:
            raise ValueError(f"default names models that are not in the line-up: {unknown}")
        return self

    @classmethod
    def read(cls, path: Path) -> Lineup:
        """Read s1flow.toml and check its shape; nothing is built."""
        path = place.absolute(path, "connections")
        try:
            lineup = cls.model_validate(tomllib.loads(path.read_text()))
        except ValidationError as e:
            raise ConfigError(f"{path}: {invalid(e)}") from None
        except (tomllib.TOMLDecodeError, OSError, UnicodeDecodeError) as e:
            raise ConfigError(f"cannot read connections from {path}: {e}; check connections=PATH in the SDK or --connections PATH in the CLI") from None
        lineup._path = path
        return lineup

    def spec(self, name: str) -> ModelSpec:
        """A model's entry as s1flow.toml writes it (`jev:1.14` gives jev's)."""
        base = name.partition(":")[0]
        if base not in self.models:
            raise NotFound(f"unknown connection {base!r}; known: {', '.join(self.models) or 'none'}; source: {self._path or 'supplied Lineup'}")
        return self.models[base]

    def resolved(self, name: str) -> ModelSpec:
        """What `jev` or `jev:1.14` sends: the model at that version (ModelSpec.at), or as it is."""
        base, _, version = name.partition(":")
        spec = self.spec(base)
        if not version:
            return spec.resolved()
        if spec.versions is None:
            raise ConfigError(f"{base} declares no versions, so it cannot be asked for one ({name})")
        try:
            return spec.at(version)
        except NotFound as e:
            raise NotFound(f"{base}: {e}") from None

    def probe_names(self) -> list[str]:
        """Every name, and each version a spec lists: what `s1flow models --verify` checks by default."""
        return [*self.models] + [f"{n}:{v}" for n, s in self.models.items() for v in s.versions or {}]
