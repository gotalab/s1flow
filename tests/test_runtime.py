"""Runtime-only boundaries: no evaluation imports or external provider calls."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from s1flow import Client, ConfigError, DataError, ProviderError
from s1flow.client.answers import BooleanAnswer, Response
from s1flow.client.lineup import Lineup
from s1flow.client.models import Capabilities, ModelSpec, Version
from s1flow.client.state import Image
from s1flow.policies import DecisionPolicy, DecisionRule, Policies, PolicySpec, asked, load
from s1flow.policies.file import Ref
from s1flow.policies.log import AnsweredLog, FeedbackLog, from_span, span
from s1flow.policies.policy_set import export
from s1flow.policies.state_shape import schema_of
from s1flow.questions import Boolean, Choice, Score


def policy(**changes: Any) -> PolicySpec:
    return PolicySpec.model_validate({
        'task': 'ticket', 'version': 1, 'connection': 'trusted', 'model_id': 'fixed-v1',
        'at': '2026-10-24T00:00:00Z',
        'questions': {'bug': asked(Boolean(instructions='Is this a bug?'), DecisionRule(threshold=.5))},
        **changes,
    })


def client(monkeypatch: pytest.MonkeyPatch, *, spec: ModelSpec | None = None,
           probability: float = .8) -> tuple[Client, list[Any]]:
    spec = spec or ModelSpec(provider='application:factory', id='fixed-v1')
    out = Client(connections=Lineup(default=[], models={'trusted': spec}))
    calls: list[Any] = []

    class Model:
        id = spec.id
        capabilities = Capabilities(image=True)
        concurrency = 1

        async def decide(self, state: Any, questions: Any, **kw: Any) -> Response:
            calls.append(state)
            return Response(answers={key: BooleanAnswer(probability=probability) for key in questions}, answered_by=self.id)

    def build(model: Any, **kw: Any) -> Model:
        assert isinstance(model, ModelSpec)
        calls.append(model)
        return Model()

    monkeypatch.setattr(out.connections, 'build', build)
    return out, calls


def test_unevaluated_policy_roundtrip_and_events(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = Policies(tmp_path / 'policies')
    spec = policy()
    store.write_new(spec, current=True)
    assert store.read('ticket').digest == spec.digest
    c, calls = client(monkeypatch)
    log = tmp_path / 'events.jsonl'
    runtime = load('ticket', root=store.root, client=c, log=log)
    first = runtime.decide({'text': 'broken'}, case_id='same')
    second = runtime.decide({'text': 'different'}, case_id='same')
    assert first.value is True and first.below_min_probability is None
    assert first.decision_id != second.decision_id
    runtime.feedback(first.decision_id, True, policy_digest=first.policy_digest)
    events = [json.loads(line) for line in log.read_text().splitlines()]
    assert all(event['schema'] == 's1flow/log@2' for event in events)
    assert events[0]['state_sha256'] != events[1]['state_sha256']
    assert events[2]['decision_id'] == first.decision_id
    assert events[2]['policy_digest'] == spec.digest
    assert 'case_id' not in events[2]
    assert 'state_schema' in json.loads((store.dir('ticket') / 'v1.json').read_text())
    assert len(calls) == 3  # one trusted model build, two calls
    with pytest.raises(ConfigError, match='policy_digest'):
        runtime.feedback(first.decision_id, True, policy_digest='different')
    with pytest.raises(ConfigError, match='label'):
        runtime.feedback(first.decision_id, 'true')


def test_no_implicit_client() -> None:
    with pytest.raises(TypeError):
        DecisionPolicy(policy())  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        load('ticket')  # type: ignore[call-arg]


@pytest.mark.parametrize('changes', [
    {'candidate': {'model': 'trusted'}}, {'evidence': {}}, {'model': {'provider': 'evil:factory', 'id': 'x'}},
    {'connection': 'https://evil.invalid'}, {'task': '../escape'}, {'questions': {}},
    {'questions': {'q': {'question': {'type': 'score', 'instructions': 'rate', 'criteria': ['low', 'high']}, 'rule': {}}}},
    {'schema': 's1flow/policy@1'},
])
def test_spec_rejects_legacy_or_authority_fields(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        policy(**changes)


def test_choice_threshold_cannot_be_ignored() -> None:
    q = Choice(instructions='area', criteria={'a': 'A', 'b': 'B'})
    with pytest.raises(ValidationError, match='threshold'):
        asked(q, DecisionRule(threshold=.6))
    with pytest.raises(ValidationError, match='finite|less than|greater than'):
        DecisionRule(min_probability=float('nan'))


def test_binding_fails_before_model_build_or_communication(monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = client(monkeypatch)
    for changes in ({'model_id': 'not-authorized'}, {'connection': 'missing'}):
        with pytest.raises(ConfigError):
            DecisionPolicy(policy(**changes), client=c)
    assert calls == []


def test_binding_declared_versions_is_exact(monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = client(monkeypatch, spec=ModelSpec(provider='app:factory', id='alias', versions={
        'v1': Version(id='fixed-v1'), 'v2': Version(id='fixed-v2'),
    }))
    assert DecisionPolicy(policy(), client=c).model_spec.id == 'fixed-v1'
    assert DecisionPolicy(policy(connection='trusted:v1'), client=c).model_spec.id == 'fixed-v1'
    with pytest.raises(ConfigError):
        DecisionPolicy(policy(connection='trusted:v2'), client=c)
    assert calls == []


def test_shape_and_image_refs_fail_before_call(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = client(monkeypatch)
    runtime = DecisionPolicy(policy(state_schema=schema_of([{'text': 'a'}])), client=c)
    with pytest.raises(DataError, match='shape mismatch'):
        runtime.decide({'changed': 'a'})
    runtime = DecisionPolicy(policy(), client=c)
    for state in ([{'type': 'image', 'path': str(tmp_path / 'secret')}], [{'type': 'image', 'url': 'https://example.invalid/a.png'}]):
        with pytest.raises(DataError, match='prepare an Image'):
            runtime.decide(state)
    assert calls == []
    # The entire array is checked, including elements after the old preview limit.
    runtime = DecisionPolicy(policy(state_schema={'type': 'array', 'items': {'type': 'string'}}), client=c)
    with pytest.raises(DataError, match=r'state\[20\]'):
        runtime.decide(['x'] * 20 + [1])
    assert calls == []


def test_prepared_image_is_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = client(monkeypatch)
    image = Image(media_type='image/png', data='YWJj', sha256='x', width=1, height=1)
    runtime = DecisionPolicy(policy(state_schema={'type': 'array', 'items': {'type': 'image'}}), client=c)
    assert runtime.decide([image]).value is True
    assert calls[-1] == [image]


def test_invalid_answer_never_becomes_decision(monkeypatch: pytest.MonkeyPatch) -> None:
    c, _ = client(monkeypatch, probability=1.2)
    with pytest.raises(ProviderError):
        DecisionPolicy(policy(), client=c).decide('input')


def test_immutable_publish_and_concurrent_current_writes(tmp_path: Path) -> None:
    root = tmp_path / 'policies'
    stores = [Policies(root), Policies(root)]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda store: _publish(store, policy()), stores))
    assert sorted(results) == ['conflict', 'saved']
    assert stores[0].read('ticket', version=1).digest == policy().digest
    stores[0].write_new(policy().model_copy(update={'version': 2}))
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda version: Policies(root).set_current('ticket', version), [1, 2]))
    assert stores[0].current('ticket') in (1, 2)
    assert not list((root / 'ticket').glob('.v1.json.*'))


def _publish(store: Policies, spec: PolicySpec) -> str:
    try:
        store.write_new(spec)
    except ConfigError:
        return 'conflict'
    return 'saved'


@pytest.mark.parametrize('reference', ['../escape', '/tmp/a', 'a/../b', 'a@v0', 'a@../x', 'a@v1@next'])
def test_reference_traversal_rejected(reference: str) -> None:
    with pytest.raises(ConfigError):
        Ref.parse(reference)


def test_named_store_rejects_symlink_escape(tmp_path: Path) -> None:
    root, outside = tmp_path / 'policies', tmp_path / 'outside'
    root.mkdir(); outside.mkdir()
    (root / 'ticket').symlink_to(outside, target_is_directory=True)
    with pytest.raises(ConfigError, match='escapes'):
        Policies(root).write_new(policy())


def test_export_is_runtime_only_and_digest_checked(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = Policies(tmp_path / 'policies')
    store.write_new(policy(), current=True)
    bundle = export(store.root)
    source = tmp_path / 'policies.json'
    source.write_text(bundle.dump())
    c, _ = client(monkeypatch)
    assert load('ticket', path=source, client=c).decide('x').value is True
    data = json.loads(source.read_text())
    assert 'evidence' not in data['policies']['ticket']['policy']
    data['policies']['ticket']['policy']['model_id'] = 'tampered'
    source.write_text(json.dumps(data))
    with pytest.raises(ConfigError, match='digest'):
        load('ticket', path=source, client=c)


def test_v2_spans_keep_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    c, _ = client(monkeypatch)
    runtime = DecisionPolicy(policy(), client=c)
    decision = runtime.decide('x')
    answered = AnsweredLog(at='now', case_id='case', state_sha256='input', decision=decision)
    for event in [answered, FeedbackLog(at='later', decision_id=decision.decision_id,
                                       policy=decision.policy, policy_digest=decision.policy_digest, label=True)]:
        name, attrs = span(event)
        restored = from_span(name, event.at, attrs)
        assert restored is not None
        if isinstance(restored, AnsweredLog):
            assert restored.decision.decision_id == decision.decision_id
        else:
            assert restored.decision_id == decision.decision_id
        assert restored.model_dump(by_alias=True)['schema'] == 's1flow/log@2'


@pytest.mark.parametrize(('minimum', 'expected'), [(None, None), (.9, True), (.8, False)])
def test_probability_lower_bound_is_explicit(monkeypatch: pytest.MonkeyPatch, minimum: float | None, expected: bool | None) -> None:
    c, _ = client(monkeypatch)
    spec = policy(questions={'bug': asked(Boolean(instructions='bug'), DecisionRule(min_probability=minimum))})
    assert DecisionPolicy(spec, client=c).decide('input').below_min_probability is expected


def test_empty_choice_and_unsupported_shape_rejected() -> None:
    with pytest.raises(ValidationError, match='at least one'):
        asked(Choice(instructions='choose', criteria={}), DecisionRule())
    for shape in ({'anyOf': []}, {'type': 'array', 'items': []}, {'type': 'string', 'minLength': 2}):
        with pytest.raises(ValidationError):
            policy(state_schema=shape)


@pytest.mark.parametrize('state', [{'number': float('nan')}, {'object': object()}])
def test_unhashable_or_nonfinite_input_is_data_error_before_call(monkeypatch: pytest.MonkeyPatch, state: Any) -> None:
    c, calls = client(monkeypatch)
    with pytest.raises(DataError, match='not finite JSON'):
        DecisionPolicy(policy(), client=c).decide(state)
    assert calls == []


def test_runtime_import_does_not_require_posix_locking() -> None:
    import subprocess
    import sys

    # A Windows Python installation has no fcntl module. Read-only SDK imports
    # must work before any platform-specific writer implementation is needed.
    code = "import sys; sys.modules['fcntl'] = None; import s1flow.policies; print('ok')"
    result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == 'ok'


def test_windows_writer_locks_byte_zero_and_unlocks_on_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    import os
    import sys
    from s1flow.policies import file as storage

    observed = []

    def locking(fd: int, operation: int, count: int) -> None:
        observed.append((operation, os.lseek(fd, 0, os.SEEK_CUR), count))

    fake_msvcrt = SimpleNamespace(LK_LOCK=1, LK_UNLCK=2, locking=locking)
    monkeypatch.setitem(sys.modules, 'msvcrt', fake_msvcrt)
    monkeypatch.setattr(storage.sys, 'platform', 'win32')
    with pytest.raises(RuntimeError, match='write failed'):
        with storage._writer_lock(tmp_path / '.write.lock'):
            raise RuntimeError('write failed')
    assert observed == [(1, 0, 1), (2, 0, 1)]
    assert (tmp_path / '.write.lock').read_bytes() == b'\0'


def test_windows_directory_sync_limitation_does_not_swallow_file_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from s1flow.policies import file as storage

    monkeypatch.setattr(storage.sys, 'platform', 'win32')
    storage._sync_dir(tmp_path)  # supported explicitly as a no-op on this platform
    def failed_sync(fd: int) -> None:
        raise OSError('file flush failed')
    monkeypatch.setattr(storage.os, 'fsync', failed_sync)
    with pytest.raises(OSError, match='file flush failed'):
        storage.atomic_write(tmp_path / 'new.json', '{}')
    assert not (tmp_path / 'new.json').exists()
    assert list(tmp_path.iterdir()) == []


def test_runtime_conditions_need_no_evaluation_adapter_metadata(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from s1flow.client.identity import execution_digest

    c, _ = client(monkeypatch)
    spec = policy()
    path = tmp_path / 'policy.json'
    path.write_text(spec.dump())
    direct = DecisionPolicy(spec, client=c)
    loaded = load(path=path, client=c)
    first = direct.decide({'text': 'first input'})
    second = loaded.decide({'text': 'second input'})
    expected = execution_digest(c.connections.resolved('trusted'), spec.digest)
    assert first.execution_digest == second.execution_digest == expected
    assert not hasattr(direct, 'input_adapter_digest')
    with pytest.raises(TypeError, match='input_adapter_digest'):
        DecisionPolicy(spec, client=c, input_adapter_digest='evaluation-only')  # type: ignore[call-arg]
    with pytest.raises(TypeError, match='input_adapter_digest'):
        load(path=path, client=c, input_adapter_digest='evaluation-only')  # type: ignore[call-arg]


@pytest.mark.parametrize('answered_by', ['', '  \t\n'])
def test_missing_answering_identity_is_failed_event_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, answered_by: str) -> None:
    c, _ = client(monkeypatch)
    class BlankIdentity:
        id, concurrency, capabilities = 'fixed-v1', 1, Capabilities()
        async def decide(self, state: Any, questions: Any, **kw: Any) -> Response:
            return Response(answers={'bug': BooleanAnswer(probability=.8)}, answered_by=answered_by)
    monkeypatch.setattr(c.connections, 'build', lambda *args, **kw: BlankIdentity())
    log = tmp_path / 'events.jsonl'
    with pytest.raises(ProviderError, match='answered_by'):
        DecisionPolicy(policy(), client=c, log=log).decide('input')
    events = [json.loads(line) for line in log.read_text().splitlines()]
    assert [event['type'] for event in events] == ['failed']
    assert 'answered_by' in events[0]['error']


def test_policy_schema_matches_runtime_question_scope() -> None:
    from jsonschema import Draft202012Validator
    from s1flow.questions import Box

    validator = Draft202012Validator(PolicySpec.model_json_schema(by_alias=True))
    valid = policy().model_dump(mode='json', by_alias=True)
    assert list(validator.iter_errors(valid)) == []
    for question in [Score(instructions='rate', criteria=['a', 'b']), Box(instructions='find')]:
        with pytest.raises(ValueError, match='boolean and choice'):
            asked(question, DecisionRule())
        invalid = {**valid, 'questions': {'q': {'question': question.model_dump(), 'rule': {}}}}
        assert list(validator.iter_errors(invalid))
        with pytest.raises(ValidationError):
            PolicySpec.model_validate(invalid)
    for questions in [{}, {'q1': valid['questions']['bug'], 'q2': valid['questions']['bug']}]:
        invalid = {**valid, 'questions': questions}
        assert list(validator.iter_errors(invalid))
        with pytest.raises(ValidationError):
            PolicySpec.model_validate(invalid)


def test_invalid_utf8_policy_is_config_error(tmp_path: Path) -> None:
    from s1flow.policies.file import read_file

    path = tmp_path / 'invalid.json'
    path.write_bytes(b'\xff\xfeinvalid')
    with pytest.raises(ConfigError, match='not a v2 policy'):
        read_file(path)
