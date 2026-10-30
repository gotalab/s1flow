"""policies/<task>/history.jsonl: why current points where it does. `s1flow adopt` appends one line each time it
switches current (a measured candidate, an unmeasured spec, a rollback) and each time it refuses a candidate the
held-out test shows below, so a choice made by trying candidates on the test share leaves a trace. Nothing else
writes it; a rollback makes no new version, so this is the one place its reason is kept outside git.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from ..core import clock
from ..core.errors import ConfigError, invalid

Action = Literal['adopt', 'spec', 'rollback', 'refused']


class Switch(BaseModel):
    """One line of history.jsonl."""
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/history@1'] = Field(default='s1flow/history@1', alias='schema')
    at: str = Field(default_factory=clock.now)
    action: Action  # adopt: a measured candidate; spec: a version saved without evaluation; rollback: an older version
    version: int = Field(ge=1)  # what current points at after it (refused: the version it would have been)
    previous: int | None = Field(ge=1)  # what current pointed at before
    by: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    candidate: str | None = None  # adopt and refused: the candidate, model[:version][/variant]
    test: Literal['kept', 'below', 'inconclusive'] | None = None  # adopt and refused: the held-out test's verdict
    forced: bool = False  # adopt: written although the held-out test showed it below (adopt --force)

    def line(self) -> str:
        return self.model_dump_json(by_alias=True) + '\n'


def read(path: Path) -> list[Switch]:
    if not path.exists():
        return []
    out = []
    for n, text in enumerate(path.read_text().splitlines(), 1):
        if text.strip():
            try:
                out.append(Switch.model_validate_json(text))
            except ValidationError as e:
                raise ConfigError(f'{path}:{n}: {invalid(e)}') from None
    return out
