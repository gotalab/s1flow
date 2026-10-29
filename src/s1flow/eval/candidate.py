"""The model and question variant compared by evaluation."""
from __future__ import annotations
import re
from pydantic import BaseModel, ConfigDict
from ..core.errors import ConfigError

VARIANT = re.compile(r'[A-Za-z0-9][\w.+@-]*')


def variant_name(name: str) -> str:
    if not VARIANT.fullmatch(name) or name == 'base':
        raise ConfigError(f'variant {name!r}: letters, digits and . _ + @ - only, and not base')
    return name


class Candidate(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    model: str
    variant: str = 'base'

    @property
    def name(self) -> str:
        return self.model if self.variant == 'base' else f'{self.model}/{self.variant}'

    @classmethod
    def parse(cls, name: str) -> Candidate:
        model, slash, variant = name.partition('/')
        if not model or (slash and not variant) or '/' in variant or any(c.isspace() for c in name):
            raise ConfigError(f'candidate {name!r}: model[:version][/variant], no spaces')
        return cls(model=model, variant=variant or 'base')
