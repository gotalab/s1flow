"""Validated execution specifications and their immutable, atomic local store.

Runtime files contain only execution settings. Evaluation records are separate files
owned by s1flow.eval; reading a policy never reads those records.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as installed_version
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from ..client.lineup import NAME
from ..client.questions import Boolean, Choice, Question
from ..core import clock, place
from ..core.errors import ConfigError, NotFound, invalid
from . import history
from .history import Switch
from .kinds import Kind, KindParams, kind_of
from .rule import DecisionRule
from .state_shape import JSONSchema, validate_schema

SCHEMA: Literal['s1flow/policy@2'] = 's1flow/policy@2'
CURRENT = 'current'  # the one channel: the version that runs. Merging the change that points it is the release
IDENTIFIER = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]*')
VERSION = re.compile(r'v([1-9]\d*)')


def identifier(name: str, what: str = 'task') -> str:
    if not IDENTIFIER.fullmatch(name) or name in ('.', '..'):
        raise ConfigError(f'{what} {name!r}: letters, digits, underscore, dot and hyphen only; start with a letter or digit')
    return name


def version_number(spec: str) -> int | None:
    m = VERSION.fullmatch(spec)
    return int(m.group(1)) if m else None


def policy_id(task: str, version: int) -> str:
    return f'{task}@v{version}'


def channel_name(name: str) -> str:
    if name != CURRENT:
        raise ConfigError(f'channel {name!r}: the one channel is `current`; name a version (TASK@v3) for another '
                          '(`next` and named channels were removed after 0.1.0a1)')
    return name


@dataclass(frozen=True)
class Ref:
    task: str
    channel: str | None = None
    version: int | None = None

    def __post_init__(self) -> None:
        identifier(self.task)
        if self.channel is not None:
            channel_name(self.channel)
        if self.version is not None and (isinstance(self.version, bool) or self.version < 1):
            raise ConfigError('a policy version is a positive integer')
        if self.version is not None and self.channel is not None:
            raise ConfigError('a policy reference names a version or a channel, not both')

    @classmethod
    def parse(cls, text: str) -> Ref:
        task, at, which = text.partition('@')
        if (at and not which) or '@' in which:
            raise ConfigError(f'policy {text!r}: TASK, TASK@current or TASK@vN')
        identifier(task)
        if (n := version_number(which)) is not None:
            return cls(task, version=n)
        return cls(task, channel=channel_name(which) if which else None)

    def names(self, task: str, version: int, channel: str | None = None) -> bool:
        return task == self.task and self.version in (None, version) and (self.channel is None or channel is None or self.channel == channel)

    def __str__(self) -> str:
        return policy_id(self.task, self.version) if self.version is not None else f'{self.task}@{self.channel or CURRENT}'


def digest(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def policy_digest(content: dict[str, Any]) -> str:
    """Hash the complete runtime specification; evaluation never enters this content."""
    return digest(content)


def _sdk_version() -> str:
    try:
        return installed_version('s1flow')
    except PackageNotFoundError:
        return 'source'


PolicyQuestion = Annotated[Boolean | Choice, Field(discriminator='type')]


class Asked(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    question: PolicyQuestion
    kind: KindParams = KindParams()
    rule: DecisionRule

    @model_validator(mode='after')
    def _applicable(self) -> Asked:
        kind = self.of()
        if self.question.type == 'choice' and not kind.options:
            raise ValueError('a choice question requires at least one option')
        if self.rule.threshold is not None and not kind.binary:
            raise ValueError('threshold applies only to a boolean or a choice with a positive option')
        return self

    def of(self) -> Kind:
        return kind_of(self.question, self.kind)


def asked(question: Question, rule: DecisionRule, params: KindParams = KindParams()) -> Asked:
    if not isinstance(question, (Boolean, Choice)):
        raise ValueError('a policy supports boolean and choice questions only; use Client directly for score and box')
    return Asked(question=question, kind=params, rule=rule)


class PolicySpec(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True, populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/policy@2'] = Field(default=SCHEMA, alias='schema')
    task: str
    version: int = Field(ge=1, strict=True)
    connection: str
    model_id: str = Field(min_length=1)
    questions: dict[str, Asked] = Field(min_length=1, max_length=1)
    at: str = Field(default_factory=clock.now)
    s1flow_version: str = Field(default_factory=_sdk_version)
    state_schema: JSONSchema | None = None

    @model_validator(mode='after')
    def _valid(self) -> PolicySpec:
        try:
            if self.state_schema is not None:
                validate_schema(self.state_schema)
            identifier(self.task)
            base, colon, version = self.connection.partition(':')
            if not NAME.fullmatch(base) or (colon and (not version or re.search(r'[\s:/,]', version))):
                raise ConfigError('connection is a registered model name, optionally followed by :version')
            for qid in self.questions:
                identifier(qid, 'question id')
        except ConfigError as e:
            raise ValueError(str(e)) from None
        return self

    @property
    def ref(self) -> str:
        return policy_id(self.task, self.version)

    @property
    def question_id(self) -> str:
        return next(iter(self.questions))

    @property
    def asked(self) -> Asked:
        return self.questions[self.question_id]

    @property
    def question(self) -> Question:
        return self.asked.question

    @property
    def rule(self) -> DecisionRule:
        return self.asked.rule

    @property
    def kind(self) -> Kind:
        return self.asked.of()

    @property
    def digest(self) -> str:
        return policy_digest(self.model_dump(mode='json', by_alias=True))

    def with_question(self, question: Question) -> PolicySpec:
        data = self.model_dump(mode='python', by_alias=True)
        data['questions'] = {self.question_id: asked(question, self.rule, self.asked.kind)}
        return PolicySpec.model_validate(data)

    def dump(self) -> str:
        return self.model_dump_json(by_alias=True, indent=1) + '\n'


class ChannelsFile(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/channels@1'] = Field(default='s1flow/channels@1', alias='schema')
    channels: dict[str, int] = Field(default_factory=dict)

    @model_validator(mode='after')
    def _valid(self) -> ChannelsFile:
        for version in self.channels.values():  # a file from 0.1.0a1 may still name `next` or others: read, never used
            if isinstance(version, bool) or version < 1:
                raise ValueError('channel versions are positive integers')
        return self

    def dump(self) -> str:
        return self.model_dump_json(by_alias=True, indent=1) + '\n'


def read_file(path: Path) -> PolicySpec:
    if not path.is_file():
        raise NotFound(f'no policy {path}')
    try:
        return PolicySpec.model_validate_json(path.read_text(encoding='utf-8'))
    except (ValidationError, OSError, UnicodeDecodeError) as e:
        detail = invalid(e) if isinstance(e, ValidationError) else str(e)
        raise ConfigError(f'{path} is not a v2 policy: {detail}') from None


@contextmanager
def _writer_lock(path: Path) -> Iterator[None]:
    """Serialize local writers with the platform's standard-library file lock."""
    with path.open('a+b') as stream:
        if sys.platform == 'win32':
            import msvcrt

            # Windows locks a byte range from the current offset. All writers use byte zero.
            if os.fstat(stream.fileno()).st_size == 0:
                stream.write(b'\0')
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)


def _sync_dir(directory: Path) -> None:
    # Windows cannot open directories through os.open for fsync. File bytes were
    # already flushed; atomic publication still applies, but directory durability
    # across power loss is a POSIX guarantee here.
    if sys.platform == 'win32':
        return
    fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write(path: Path, text: str, *, immutable: bool = False) -> None:
    """Publish complete bytes in the same filesystem, never exposing a partial file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        if immutable:
            try:
                os.link(temporary, path)
            except FileExistsError:
                raise ConfigError(f'{path} already exists; saved versions cannot be overwritten') from None
        else:
            os.replace(temporary, path)
        _sync_dir(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Policies:
    """Runtime store. Every writer shares the per-task advisory lock."""

    def __init__(self, root: Path):
        self.root = place.absolute(root, "policy root")

    def dir(self, task: str) -> Path:
        identifier(task)
        path = self.root / task
        if not path.resolve().is_relative_to(self.root):
            raise ConfigError(f'policy task {task!r} escapes {self.root}')
        return path

    def _file(self, task: str, name: str) -> Path:
        path = self.dir(task) / name
        if not path.resolve().is_relative_to(self.dir(task).resolve()):
            raise ConfigError(f'policy path escapes its task directory: {path}')
        return path

    @contextmanager
    def locked(self, task: str) -> Iterator[None]:
        self.dir(task).mkdir(parents=True, exist_ok=True)
        path = self._file(task, '.write.lock')
        with _writer_lock(path):
            yield

    def versions(self, task: str) -> list[int]:
        return sorted(n for p in self.dir(task).glob('v*.json') if (n := version_number(p.stem)) is not None)

    def next_version(self, task: str) -> int:
        return max(self.versions(task), default=0) + 1

    def current(self, task: str) -> int | None:
        """The version that runs (channels.json's `current`), None before one is chosen."""
        path = self._file(task, 'channels.json')
        if not path.exists():
            return None
        try:
            return ChannelsFile.model_validate_json(path.read_text()).channels.get(CURRENT)
        except (ValidationError, OSError) as e:
            raise ConfigError(f'{path}: {e}') from None

    def tasks(self) -> list[str]:
        return sorted(d.name for d in self.root.iterdir() if d.is_dir() and IDENTIFIER.fullmatch(d.name) and self.versions(d.name)) if self.root.is_dir() else []

    def known(self, task: str) -> None:
        if not self.versions(task):
            raise NotFound(f'no policy of {task!r}; tasks with policies: {", ".join(self.tasks()) or "none"}')

    def get(self, ref: Ref) -> PolicySpec:
        return self.read(ref.task, version=ref.version, channel=ref.channel or CURRENT)

    def read(self, task: str, version: int | None = None, channel: str = CURRENT) -> PolicySpec:
        self.known(task)
        if version is None:
            channel_name(channel)
            version = self.current(task)
            if version is None:
                raise NotFound(f'{task} has no current version; s1flow adopt picks one, s1flow adopt --spec FILE saves one')
        if isinstance(version, bool) or version < 1:
            raise ConfigError('a policy version is a positive integer')
        spec = read_file(self._file(task, f'v{version}.json'))
        if spec.task != task or spec.version != version:
            raise ConfigError(f'{task}@v{version}: stored specification names {spec.ref}')
        return spec

    def _write_new(self, spec: PolicySpec) -> None:
        spec = PolicySpec.model_validate_json(spec.dump())
        latest = max(self.versions(spec.task), default=0)
        if spec.version <= latest:
            raise ConfigError(f'{spec.task} already has v{latest}; a new policy is v{latest + 1}')
        atomic_write(self._file(spec.task, f'v{spec.version}.json'), spec.dump(), immutable=True)

    def write_new(self, spec: PolicySpec, *, adopted: Switch | None = None) -> None:
        """Save a new version; `adopted` (s1flow adopt's) also makes it the version that runs (merging that change
        ships it)."""
        with self.locked(spec.task):
            if adopted is not None:
                self._may_switch(spec.task, adopted)
            self._write_new(spec)
            if adopted is not None:
                self._switch(spec.task, adopted)

    def _may_switch(self, task: str, entry: Switch) -> None:
        """Before anything is written: a switch from what current no longer is would undo another adopt."""
        if entry.action == 'refused':
            raise ConfigError(f'{task}: a refused candidate switches nothing')
        if entry.previous != self.current(task):
            raise ConfigError(f'{task}: current changed while adopting (v{self.current(task)}, not v{entry.previous}); adopt again')

    def _switch(self, task: str, entry: Switch) -> None:
        """The one writer of channels.json: points current at entry.version, after saying why in history.jsonl (a
        line whose switch did not happen is told apart by channels.json; a switch with no why could not be)."""
        self._may_switch(task, entry)
        self.read(task, version=entry.version)
        self._log(task, entry)
        atomic_write(self._file(task, 'channels.json'), ChannelsFile(channels={CURRENT: entry.version}).dump())

    def _log(self, task: str, entry: Switch) -> None:
        with self._file(task, 'history.jsonl').open('a', encoding='utf-8') as f:
            f.write(entry.line())

    def switch(self, task: str, entry: Switch) -> None:
        """Point current at a saved version, as s1flow adopt does for a rollback (TASK@vN)."""
        with self.locked(task):
            self._switch(task, entry)

    def log(self, task: str, entry: Switch) -> None:
        """Record a candidate adopt refused; current is left as it is."""
        if entry.action != 'refused':
            raise ConfigError(f'{task}: only a refused candidate is recorded without switching current')
        with self.locked(task):
            self._log(task, entry)

    def history(self, task: str) -> list[Switch]:
        return history.read(self._file(task, 'history.jsonl'))
