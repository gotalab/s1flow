"""A portable set of v2 execution specifications, without evaluation records."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
from ..core.errors import ConfigError, NotFound, invalid
from .file import Policies, PolicySpec, Ref, policy_id

SCHEMA: Literal['s1flow/policy-set@2'] = 's1flow/policy-set@2'


class Entry(BaseModel):
    model_config = ConfigDict(extra='forbid')
    version: int = Field(ge=1)
    digest: str
    policy: PolicySpec

    @model_validator(mode='after')
    def _content(self) -> Entry:
        if self.policy.version != self.version or self.policy.digest != self.digest:
            raise ValueError('exported policy does not match its version or digest')
        return self


class PolicySet(BaseModel):
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/policy-set@2'] = Field(default=SCHEMA, alias='schema')
    channel: Literal['current']
    policies: dict[str, Entry]

    @model_validator(mode='after')
    def _references(self) -> PolicySet:
        if any(task != entry.policy.task for task, entry in self.policies.items()):
            raise ValueError('exported task does not match its specification')
        return self

    def dump(self) -> str:
        return self.model_dump_json(by_alias=True, indent=1) + '\n'


def export(root: Path, tasks: list[str] | None = None) -> PolicySet:
    """Each task's current policy (every task with one when none are named)."""
    store = Policies(root)
    names = tasks or [task for task in store.tasks() if store.current(task) is not None]
    if not names:
        raise NotFound(f'no task in {root} has a current policy')
    entries = {}
    for task in names:
        spec = store.read(task)
        entries[task] = Entry(version=spec.version, digest=spec.digest, policy=spec)
    return PolicySet(channel='current', policies=entries)


def is_policy_set(data: Any) -> bool:
    return isinstance(data, dict) and str(data.get('schema', '')).startswith('s1flow/policy-set@')


def read(path: Path, data: Any, ref: Ref | None) -> PolicySpec:
    try:
        bundle = PolicySet.model_validate(data)
    except ValidationError as e:
        raise ConfigError(f'{path} is not a v2 policy set: {invalid(e)}') from None
    if ref is None:
        raise ConfigError(f'{path} holds multiple policies; name a task')
    if ref.task not in bundle.policies:
        raise NotFound(f'{path} has no policy of {ref.task}')
    entry = bundle.policies[ref.task]
    if not ref.names(ref.task, entry.version):
        raise NotFound(f'{path} holds {policy_id(ref.task, entry.version)}, not {ref}')
    return entry.policy
