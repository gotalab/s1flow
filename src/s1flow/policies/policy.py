"""Execute a PolicySpec only through the Client explicitly supplied by its application."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

from ..client import AsyncClient, Client, loop
from ..client.answers import Refusal
from ..client.identity import execution_digest, state_digest
from ..client.models import ModelSpec
from ..client.state import State, has_unprepared_image
from ..core import clock, place
from ..core.errors import ConfigError, DataError, NotFound, ProviderError, Rejected
from . import log as logs
from . import policy_set as policy_sets
from .file import Policies, PolicySpec, Ref, read_file
from .log import AnsweredLog, Decision, FailedLog, FeedbackLog
from .state_shape import mismatch

try:
    from opentelemetry import trace as _otel_trace
    _tracer: Any = _otel_trace.get_tracer('s1flow')
except ImportError:  # pragma: no cover
    _tracer = None


class DecisionPolicy:
    """Bind a validated execution specification to the application's allowed connections."""

    def __init__(self, spec: PolicySpec, *, client: Client | AsyncClient, log: Path | str | None = None,
                 keep_state: bool = False):
        if not isinstance(client, (Client, AsyncClient)):
            raise ConfigError('DecisionPolicy requires an explicit Client or AsyncClient')
        # Revalidate copies: model_copy(update=...) and mutation of nested dicts bypass pydantic validators.
        self.spec = PolicySpec.model_validate_json(spec.dump())
        self.client = client
        self._aio = client.aio if isinstance(client, Client) else client
        self.log = place.absolute(log, "log") if log is not None else None
        self.keep_state = keep_state
        self.model_spec = self._bind()

    @property
    def execution_digest(self) -> str:
        return execution_digest(self.model_spec, self.spec.digest)

    def _bind(self) -> ModelSpec:
        connection, wanted = self.spec.connection, self.spec.model_id
        try:
            trusted = self.client.connections.resolved(connection)
            if trusted.id != wanted and ':' not in connection:
                declared = self.client.connections.retrieve(connection).spec
                version = next((name for name, item in (declared.versions or {}).items() if item.id == wanted), None)
                if version is not None:
                    trusted = declared.at(version)
            if trusted.id != wanted:
                raise ConfigError(f'{self.spec.ref}: {connection!r} does not allow model_id {wanted!r}')
        except NotFound as e:
            raise ConfigError(f'{self.spec.ref}: {e}') from None
        return trusted.model_copy(deep=True)

    def decide(self, state: State, case_id: str | None = None) -> Decision:
        return loop.run(self._decide(state, case_id))

    async def adecide(self, state: State, case_id: str | None = None) -> Decision:
        return await self._decide(state, case_id)

    async def _decide(self, state: State, case_id: str | None) -> Decision:
        spec = self.spec
        started = time.perf_counter()
        try:
            input_digest = state_digest(state)
        except (ValueError, TypeError) as e:
            raise DataError(f"policy input is not finite JSON or prepared Image data: {e}") from None
        try:
            if has_unprepared_image(state):
                raise DataError('policy input has an image reference; prepare an Image explicitly before deciding')
            if spec.state_schema is not None and (wrong := mismatch(spec.state_schema, state)):
                raise DataError(f'{spec.ref}: input shape mismatch: {"; ".join(wrong[:3])}')
            result = await self._aio.responses.create(model=self.model_spec, state=state,
                                                       questions={spec.question_id: spec.question})
            answer = result.answers[spec.question_id]
            if isinstance(answer, Refusal):
                raise Rejected(f'{spec.ref}: the model refused {spec.question_id}' + (f': {answer.reason}' if answer.reason else ''))
            try:
                reading = spec.kind.read([answer], spec.rule)
            except ProviderError as e:
                raise ProviderError(f'{spec.ref}: {spec.question_id}: {e}') from None
        except Exception as e:
            self._write(FailedLog(at=clock.now(ms=True), case_id=case_id, state_sha256=input_digest,
                                  policy=spec.ref, policy_digest=spec.digest, error=f'{type(e).__name__}: {str(e)[:300]}'))
            raise
        decision = Decision(**dict(reading), decision_id=str(uuid4()), policy=spec.ref, policy_digest=spec.digest,
                            execution_digest=self.execution_digest, answered_by=result.answered_by,
                            latency_ms=(time.perf_counter() - started) * 1000, response=result)
        self._write(AnsweredLog(at=clock.now(ms=True), case_id=case_id, state_sha256=input_digest,
                                state=state if self.keep_state else None, decision=decision))
        return decision

    def feedback(self, decision_id: str, label: Any, *, policy_digest: str | None = None) -> None:
        """Record a label for an explicit decision ID. Cross-process joins belong to evaluation."""
        record_feedback(self.spec, decision_id, label, log=self.log, policy_digest=policy_digest)

    def _write(self, rec: AnsweredLog | FailedLog) -> None:
        _emit(self.log, rec, self.model_spec.provider, self.model_spec.id)


def record_feedback(spec: PolicySpec, decision_id: str, label: Any, *, log: Path | str | None,
                    policy_digest: str | None = None) -> None:
    """Record a label for a decision of this policy. It calls no model, so it needs no connections."""
    if not decision_id or not isinstance(decision_id, str):
        raise ConfigError('feedback requires a decision_id')
    if policy_digest is not None and policy_digest != spec.digest:
        raise ConfigError('feedback policy_digest does not match this policy')
    kind = spec.kind
    wrong = label not in kind.options if isinstance(label, str) and kind.options else kind.label_error(kind.as_label(label)) is not None
    if wrong:
        labels = [*kind.options, *(['true', 'false'] if kind.binary else [])]
        raise ConfigError(f'{spec.ref}: label {label!r} is not an answer to its question; one of: {", ".join(labels)}')
    _emit(place.absolute(log, "log") if log is not None else None,
           FeedbackLog(at=clock.now(ms=True), decision_id=decision_id, policy=spec.ref, policy_digest=spec.digest,
                       label=kind.as_label(label)))


def _emit(log: Path | None, rec: AnsweredLog | FailedLog | FeedbackLog, provider: str | None = None,
          model: str | None = None) -> None:
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('a', encoding='utf-8') as stream:
            stream.write(rec.model_dump_json(by_alias=True) + '\n')
    if _tracer is not None:
        name, attrs = logs.span(rec, provider, model)
        with _tracer.start_as_current_span(name) as span:
            span.set_attributes(attrs)


def resolve(policy: str | None = None, *, path: Path | str | None = None, root: Path | None = None) -> PolicySpec:
    """The policy spec `load` binds: from a policy file or policy set at `path`, or from the policies directory `root`."""
    ref = Ref.parse(policy) if policy is not None else None
    if path is not None:
        source = place.absolute(path, "policy path")
        try:
            data = json.loads(source.read_text()) if source.is_file() else None
        except (ValueError, OSError) as e:
            raise ConfigError(f'{source}: {e}') from None
        spec = policy_sets.read(source, data, ref) if policy_sets.is_policy_set(data) else read_file(source)
        if ref is not None and not ref.names(spec.task, spec.version):
            raise NotFound(f'{source} holds {spec.ref}, not {policy}')
        return spec
    if ref is None:
        raise ConfigError('load requires a policy reference or path=')
    if root is None:
        raise ConfigError("policy loading requires path=FILE or root=DIRECTORY; the SDK does not discover projects")
    return Policies(root).get(ref)


def load(policy: str | None = None, *, client: Client | AsyncClient, path: Path | str | None = None,
         root: Path | None = None, log: Path | str | None = None, keep_state: bool = False) -> DecisionPolicy:
    return DecisionPolicy(resolve(policy, path=path, root=root), client=client, log=log, keep_state=keep_state)
