"""Evaluation records compose with, and reference, separately stored runtime specs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
from ..client.models import ModelSpec
from ..core.errors import ConfigError, NotFound
from ..project import Project
from ..policies.file import CURRENT, Policies, PolicySpec, Ref, atomic_write
from ..policies.history import Switch
from .candidate import Candidate
from .evaluation import Evaluation
from . import policy_v2 as v2

Pin = Literal['yes', 'no', 'alias']
TestVerdict = Literal['kept', 'below', 'inconclusive']


def pin(spec: ModelSpec, model: str) -> Pin:
    if ':' in model or spec.version is not None:
        return 'yes'
    return 'alias' if spec.alias else 'no'


class Evidence(BaseModel):
    model_config = ConfigDict(extra='forbid')
    data_sha256: str
    execution_digest: str | None
    input_adapter_digest: str = ''
    evaluation_contract_digest: str | None = None  # unknown for historical evidence; never inferred
    git_sha: str | None = None
    evaluation: Evaluation
    test: TestVerdict | None
    compared: list[str]


class Selection(BaseModel):
    """Who picked the candidate and why. s1flow records the pick; it does not recommend one."""
    model_config = ConfigDict(extra='forbid')
    by: str
    reason: str
    tied: list[str]  # the candidates the primary objective could not tell apart at the top when it was picked
    forced: bool = False  # written although the held-out test showed it below (adopt --force); `reason` says why


def forced_rule(selection: Selection, evidence: Evidence) -> None:
    if selection.forced and evidence.test != 'below':
        raise ValueError(f'forced, but the held-out test shows it {evidence.test or "not measured"}: only a version below is forced')


class EvaluatedPolicy(BaseModel):
    """Explicit runtime specification and the evaluation that selected it."""
    model_config = ConfigDict(extra='forbid')
    spec: PolicySpec
    candidate: Candidate
    selection: Selection
    evidence: Evidence
    answered_by: str

    @model_validator(mode='after')
    def _same_candidate(self) -> EvaluatedPolicy:
        if self.candidate != self.evidence.evaluation.candidate:
            raise ValueError('evaluation candidate does not match the selected candidate')
        if self.candidate.model != self.spec.connection:
            raise ValueError('candidate model does not match the execution connection')
        forced_rule(self.selection, self.evidence)
        return self


class EvaluationRecord(BaseModel):
    """vN.evaluation.json; never embeds or redefines the runtime specification."""
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/policy-evaluation@3'] = Field(default='s1flow/policy-evaluation@3', alias='schema')
    policy_digest: str
    candidate: Candidate
    selection: Selection
    evidence: Evidence
    answered_by: str

    @classmethod
    def from_policy(cls, policy: EvaluatedPolicy) -> EvaluationRecord:
        return cls(policy_digest=policy.spec.digest, candidate=policy.candidate, selection=policy.selection,
                   evidence=policy.evidence, answered_by=policy.answered_by)

    @model_validator(mode='after')
    def _forced_below(self) -> EvaluationRecord:
        forced_rule(self.selection, self.evidence)
        return self

    def attach(self, spec: PolicySpec) -> EvaluatedPolicy:
        if self.policy_digest != spec.digest:
            raise ConfigError(f'{spec.ref}: evaluation record does not match the stored policy digest')
        return EvaluatedPolicy(spec=spec, candidate=self.candidate, selection=self.selection,
                               evidence=self.evidence, answered_by=self.answered_by)

    def dump(self) -> str:
        return self.model_dump_json(by_alias=True, indent=1) + '\n'


def read_record(text: str) -> EvaluationRecord:
    """A stored evaluation record of either schema, as @3."""
    data = json.loads(text)
    if isinstance(data, dict) and data.get('schema') == 's1flow/policy-evaluation@2':
        return upgrade(v2.EvaluationRecord.model_validate_json(text))
    return EvaluationRecord.model_validate_json(text)


def upgrade(old: v2.EvaluationRecord) -> EvaluationRecord:
    # Not forced: 0.1.0a1 stored a version below on the held-out test without --force, so @2 cannot say.
    selection = Selection(by=old.selection.by, reason=old.selection.reason, tied=old.selection.tied)
    evidence = Evidence.model_validate(old.evidence.model_dump(exclude={'test_uses'}))
    return EvaluationRecord(policy_digest=old.policy_digest, candidate=old.candidate, selection=selection,
                            evidence=evidence, answered_by=old.answered_by)


class Store:
    """Evaluated policy store. Runtime storage owns locks, publication and the current version."""

    def __init__(self, root: Path):
        self.runtime = Policies(root)
        self.root = self.runtime.root

    def dir(self, task: str) -> Path:
        return self.runtime.dir(task)

    def versions(self, task: str) -> list[int]:
        return self.runtime.versions(task)

    def next_version(self, task: str) -> int:
        return self.runtime.next_version(task)

    def current(self, task: str) -> int | None:
        return self.runtime.current(task)

    def switch(self, task: str, entry: Switch) -> None:
        self.runtime.switch(task, entry)

    def log(self, task: str, entry: Switch) -> None:
        self.runtime.log(task, entry)

    def history(self, task: str) -> list[Switch]:
        return self.runtime.history(task)

    def tasks(self) -> list[str]:
        return self.runtime.tasks()

    def get(self, ref: Ref) -> EvaluatedPolicy:
        return self.read(ref.task, version=ref.version, channel=ref.channel or CURRENT)

    def _record_path(self, spec: PolicySpec) -> Path:
        return self.runtime._file(spec.task, f'v{spec.version}.evaluation.json')

    def read(self, task: str, version: int | None = None, channel: str = CURRENT) -> EvaluatedPolicy:
        spec = self.runtime.read(task, version=version, channel=channel)
        path = self._record_path(spec)
        if not path.is_file():
            raise NotFound(f'{spec.ref} has no evaluation record; the runtime specification is usable explicitly')
        try:
            return read_record(path.read_text()).attach(spec)
        except (ValidationError, OSError, ValueError) as e:
            raise ConfigError(f'{path}: invalid evaluation record: {e}') from None

    def write_new(self, policy: EvaluatedPolicy, *, adopted: Switch | None = None) -> None:
        """Save the policy and its evaluation record; `adopted` (s1flow adopt's) also makes it the version that runs."""
        # Validate before any write, including values copied with model_copy(update=...).
        policy = EvaluatedPolicy.model_validate_json(policy.model_dump_json())
        record = EvaluationRecord.from_policy(policy)
        with self.runtime.locked(policy.spec.task):
            if adopted is not None:
                self.runtime._may_switch(policy.spec.task, adopted)
            self.runtime._write_new(policy.spec)
            atomic_write(self._record_path(policy.spec), record.dump(), immutable=True)
            if adopted is not None:
                self.runtime._switch(policy.spec.task, adopted)


def store(project: Project) -> Store:
    return Store(project.policies_dir)


class Shipped(BaseModel):
    policy: str
    version: int
    current: bool
    candidate: str | None
    model: str
    model_version: str | None
    answered_by: str | None
    pin: Pin | None
    at: str
    digest: str
    evaluated: bool


class TaskPolicies(BaseModel):
    task: str
    current: int | None
    policies: list[Shipped]


def overview(project: Project, tasks: list[str] | None = None) -> list[TaskPolicies]:
    saved = store(project)
    known = sorted({*project.task_ids(), *saved.tasks()})
    if unknown := [t for t in tasks or [] if t not in known]:
        raise NotFound(f'no task {unknown[0]!r}; tasks: {", ".join(known) or "none"}')
    lineup = project.lineup()
    out = []
    for task in tasks or known:
        current = saved.current(task)
        shipped = []
        for version in reversed(saved.versions(task)):
            spec = saved.runtime.read(task, version=version)
            record = saved.read(task, version=version) if saved._record_path(spec).exists() else None
            model, _, requested = spec.connection.partition(':')
            configured = lineup.models.get(model)
            declared = next((name for name, item in (configured.versions or {}).items() if item.id == spec.model_id), None) if configured else None
            model_version = requested or declared
            shipped.append(Shipped(policy=spec.ref, version=version, current=version == current,
                                   candidate=record.candidate.name if record else None, model=model, model_version=model_version,
                                   answered_by=record.answered_by if record else None,
                                   pin='yes' if model_version else None if configured is None else 'alias' if configured.versions else 'no',
                                   at=spec.at, digest=spec.digest, evaluated=record is not None))
        out.append(TaskPolicies(task=task, current=current, policies=shipped))
    return out
