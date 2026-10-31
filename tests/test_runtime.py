"""Runtime-only boundaries: no evaluation imports or external provider calls."""
from __future__ import annotations
from conftest import fake_client, runtime_spec, ship

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from s1flow import ConfigError, DataError, ProviderError
from s1flow.client.answers import BooleanAnswer, Response
from s1flow.client.models import Capabilities, ModelSpec, Version
from s1flow.client.state import Image
from s1flow.policies import DecisionPolicy, DecisionRule, Policies, PolicySpec, asked, load
from s1flow.policies.file import Ref
from s1flow.policies.history import Switch
from s1flow.policies.state_shape import schema_of
from s1flow.questions import Boolean, Choice, Score


def test_unevaluated_policy_roundtrip_and_events(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = Policies(tmp_path / 'policies')
    spec = runtime_spec()
    ship(store, spec)
    assert store.read('ticket').digest == spec.digest
    c, calls = fake_client(monkeypatch)
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
        DecisionPolicy(runtime_spec())  # type: ignore[call-arg]
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
        runtime_spec(**changes)


def test_choice_threshold_cannot_be_ignored() -> None:
    q = Choice(instructions='area', criteria={'a': 'A', 'b': 'B'})
    with pytest.raises(ValidationError, match='threshold'):
        asked(q, DecisionRule(threshold=.6))
    with pytest.raises(ValidationError, match='finite|less than|greater than'):
        DecisionRule(min_probability=float('nan'))


def test_binding_fails_before_model_build_or_communication(monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = fake_client(monkeypatch)
    for changes in ({'model_id': 'not-authorized'}, {'connection': 'missing'}):
        with pytest.raises(ConfigError):
            DecisionPolicy(runtime_spec(**changes), client=c)
    assert calls == []


def test_binding_declared_versions_is_exact(monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = fake_client(monkeypatch, spec=ModelSpec(provider='app:factory', id='alias', versions={
        'v1': Version(id='fixed-v1'), 'v2': Version(id='fixed-v2'),
    }))
    assert DecisionPolicy(runtime_spec(), client=c).model_spec.id == 'fixed-v1'
    assert DecisionPolicy(runtime_spec(connection='trusted:v1'), client=c).model_spec.id == 'fixed-v1'
    with pytest.raises(ConfigError):
        DecisionPolicy(runtime_spec(connection='trusted:v2'), client=c)
    assert calls == []


def test_shape_and_image_refs_fail_before_call(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = fake_client(monkeypatch)
    runtime = DecisionPolicy(runtime_spec(state_schema=schema_of([{'text': 'a'}])), client=c)
    with pytest.raises(DataError, match='shape mismatch'):
        runtime.decide({'changed': 'a'})
    runtime = DecisionPolicy(runtime_spec(), client=c)
    for state in ([{'type': 'image', 'path': str(tmp_path / 'secret')}], [{'type': 'image', 'url': 'https://example.invalid/a.png'}]):
        with pytest.raises(DataError, match='prepare an Image'):
            runtime.decide(state)
    assert calls == []
    # The entire array is checked, including elements after the old preview limit.
    runtime = DecisionPolicy(runtime_spec(state_schema={'type': 'array', 'items': {'type': 'string'}}), client=c)
    with pytest.raises(DataError, match=r'state\[20\]'):
        runtime.decide(['x'] * 20 + [1])
    assert calls == []


def test_prepared_image_is_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    c, calls = fake_client(monkeypatch)
    image = Image(media_type='image/png', data='YWJj', sha256='x', width=1, height=1)
    runtime = DecisionPolicy(runtime_spec(state_schema={'type': 'array', 'items': {'type': 'image'}}), client=c)
    assert runtime.decide([image]).value is True
    assert calls[-1] == [image]


def test_invalid_answer_never_becomes_decision(monkeypatch: pytest.MonkeyPatch) -> None:
    c, _ = fake_client(monkeypatch, probability=1.2)
    with pytest.raises(ProviderError):
        DecisionPolicy(runtime_spec(), client=c).decide('input')


def test_immutable_publish_and_concurrent_adopts(tmp_path: Path) -> None:
    root = tmp_path / 'policies'
    stores = [Policies(root), Policies(root)]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda store: _publish(store, runtime_spec()), stores))
    assert sorted(results) == ['conflict', 'saved']
    assert stores[0].read('ticket', version=1).digest == runtime_spec().digest
    assert not list((root / 'ticket').glob('.v1.json.*'))
    # two adopts from v1 at once: one makes its version current, the other finds current changed and writes nothing
    stores[0].write_new(runtime_spec(version=2), adopted=Switch(action='spec', version=2, previous=None, by='a', reason='r'))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda sv: _publish(sv[0], runtime_spec(version=sv[1]), Switch(action='spec', version=sv[1], previous=2, by='a', reason='r')),
                                [(stores[0], 3), (stores[1], 4)]))
    assert sorted(results) == ['conflict', 'saved']
    current = stores[0].current('ticket')
    assert current in (3, 4) and len(stores[0].versions('ticket')) == 3  # v1, v2 and the winner
    assert [line['version'] for line in map(json.loads, (root / 'ticket' / 'history.jsonl').read_text().splitlines())] == [2, current]


def _publish(store: Policies, spec: PolicySpec, adopted: Switch | None = None) -> str:
    try:
        store.write_new(spec, adopted=adopted)
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
        Policies(root).write_new(runtime_spec())


@pytest.mark.parametrize(('minimum', 'expected'), [(None, None), (.9, True), (.8, False)])
def test_probability_lower_bound_is_explicit(monkeypatch: pytest.MonkeyPatch, minimum: float | None, expected: bool | None) -> None:
    c, _ = fake_client(monkeypatch)
    spec = runtime_spec(questions={'bug': asked(Boolean(instructions='bug'), DecisionRule(min_probability=minimum))})
    assert DecisionPolicy(spec, client=c).decide('input').below_min_probability is expected


def test_empty_choice_and_unsupported_shape_rejected() -> None:
    with pytest.raises(ValidationError, match='at least one'):
        asked(Choice(instructions='choose', criteria={}), DecisionRule())
    for shape in ({'anyOf': []}, {'type': 'array', 'items': []}, {'type': 'string', 'minLength': 2}):
        with pytest.raises(ValidationError):
            runtime_spec(state_schema=shape)


@pytest.mark.parametrize('state', [{'number': float('nan')}, {'object': object()}])
def test_unhashable_or_nonfinite_input_is_data_error_before_call(monkeypatch: pytest.MonkeyPatch, state: Any) -> None:
    c, calls = fake_client(monkeypatch)
    with pytest.raises(DataError, match='not finite JSON'):
        DecisionPolicy(runtime_spec(), client=c).decide(state)
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


def test_runtime_conditions_need_no_evaluation_adapter_metadata(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from s1flow.client.identity import execution_digest

    c, _ = fake_client(monkeypatch)
    spec = runtime_spec()
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
    c, _ = fake_client(monkeypatch)
    class BlankIdentity:
        id, concurrency, capabilities = 'fixed-v1', 1, Capabilities()
        async def decide(self, state: Any, questions: Any, **kw: Any) -> Response:
            return Response(answers={'bug': BooleanAnswer(probability=.8)}, answered_by=answered_by)
    monkeypatch.setattr(c.connections, 'build', lambda *args, **kw: BlankIdentity())
    log = tmp_path / 'events.jsonl'
    with pytest.raises(ProviderError, match='answered_by'):
        DecisionPolicy(runtime_spec(), client=c, log=log).decide('input')
    events = [json.loads(line) for line in log.read_text().splitlines()]
    assert [event['type'] for event in events] == ['failed']
    assert 'answered_by' in events[0]['error']


def test_policy_schema_matches_runtime_question_scope() -> None:
    from jsonschema import Draft202012Validator
    from s1flow.questions import Box

    validator = Draft202012Validator(PolicySpec.model_json_schema(by_alias=True))
    valid = runtime_spec().model_dump(mode='json', by_alias=True)
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
