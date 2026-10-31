"""Current evidence requires the request measured then, and dev stays separate."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from conftest import make_project
from s1flow.client.answers import BooleanAnswer, Response, Usage
from s1flow.client.identity import execution_digest, model_digest, request_digest, state_digest
from s1flow.client.models import ModelSpec, Price
from s1flow.client.questions import Boolean
from s1flow.client.state import Image
from s1flow.core.errors import ConfigError
from s1flow.eval import evalset, metrics, records, report, run
from s1flow.eval.cases import Case, Cases
from s1flow.eval.evaluation import Calls
from s1flow.eval.objectives.declare import Constraints
from s1flow.eval.review import review
from s1flow.eval.select import rank, violations
from s1flow.eval.task import Task


class Fake:
    calls = 0

    def __init__(self, build):
        self.id = 'wire:' + build.spec.id
        self.capabilities = build.spec.capabilities
        self.concurrency = build.spec.concurrency or 1

    async def decide(self, state, questions, *, options=None):
        Fake.calls += 1
        # Dev is perfect; test deliberately wrong at high probability.
        yes = state['i'] % 2 == 0
        if state['i'] >= 8:
            yes = not yes
        return Response(answers={qid: BooleanAnswer(probability=.99 if yes else .01) for qid in questions},
                        answered_by=self.id, latency_ms=10, retries=0,
                        usage=Usage(cost_usd=.01, cost_source='billed'))


@pytest.fixture
def task(tmp_path):
    project = make_project(tmp_path, {'fake': Fake})
    d = tmp_path / 'tasks' / 'identity'
    d.mkdir(parents=True)
    t = Task(id='identity', cases='cases.json', state=lambda r: r['state'], label=lambda r: r['label'],
             question=Boolean(instructions='Is even?'), project=project, dir=d)
    cs = Cases(t.id, d, t.cases, t.state, t.label)
    cs._all = [Case(id=str(i), state={'i': i}, label=i % 2 == 0) for i in range(12)]
    t._cases = cs
    (d / t.cases).write_text(json.dumps([{'id': c.id, 'state': c.state, 'label': c.label} for c in cs._all]))
    sf = evalset.SplitFile(seed=1, test_share=1/3, at='', source='test',
                           assign={str(i): 'test' if i >= 8 else 'train' for i in range(12)})
    (d / 'split.json').write_text(sf.model_dump_json(by_alias=True))
    Fake.calls = 0
    return t


def change_case(task, case_id, **changes):
    path = task.dir / task.cases
    rows = json.loads(path.read_text())
    for row in rows:
        if row['id'] == case_id:
            row.update(changes)
    path.write_text(json.dumps(rows))
    task.load_cases().forget()


def go(task):
    return asyncio.run(run.run_model(task, 'fake', limit=None, variant='base'))


def test_input_and_effective_binding_invalidate_skip_and_metrics(task):
    assert go(task)['calls'] == 12
    assert go(task)['skipped'] == 12
    change_case(task, '0', state={'i': 100})
    assert '0' not in metrics.load(task, 'base', 'fake').ids
    assert go(task)['calls'] == 1
    assert go(task)['skipped'] == 12
    task.where.client().connections.lineup.models['fake'].options['temperature'] = .7
    assert metrics.load(task, 'base', 'fake').ids == []
    assert go(task)['calls'] == 12


def test_digest_inputs_rules_secrets_and_images():
    spec = ModelSpec(provider='typesafe', id='v1', options={'base_url': 'https://example.test', 'api_key': 'one'})
    qs = {'q': Boolean(instructions='Yes?')}
    first = request_digest(spec, {'text': 'a'}, qs)
    assert first != request_digest(spec, {'text': 'b'}, qs)
    assert first != request_digest(spec.model_copy(update={'options': {'base_url': 'https://else.test'}}), {'text': 'a'}, qs)
    other_secret = spec.model_copy(update={'options': spec.options | {'api_key': 'two'}, 'note': 'changed', 'price': Price(as_of='2026-10-24', source='fixture', input_per_mtok=1)})
    assert model_digest(spec) == model_digest(other_secret)
    assert execution_digest(spec, 'rule-a') != execution_digest(spec, 'rule-b')
    with pytest.raises(TypeError):
        execution_digest(spec, 'rule-a', 'eval-only-adapter')  # runtime does not certify app preprocessing
    image = Image(media_type='image/png', data='YQ==', sha256='same-untrusted-value', width=1, height=1)
    changed = image.model_copy(update={'data': 'Yg=='})
    assert state_digest([image]) != state_digest([changed])
    assert request_digest(spec, [image], qs) != request_digest(spec, [changed], qs)


def test_defaults_exclude_test_values_errors_review_and_charts(task, monkeypatch):
    go(task)
    pr = metrics.load(task, 'base', 'fake')
    assert set(pr.ids) == {str(i) for i in range(8)}
    e = metrics.evaluate(task, pr)
    assert e.n == 8 and e.test is None and e.accuracy.value == 1
    assert not e.high_confidence_errors
    assert e.calls.cost_total_usd == pytest.approx(.08)
    full = metrics.load(task, 'base', 'fake', include_test=True)
    final = metrics.evaluate(task, full, include_test=True)
    assert final.test.n == 4 and final.test.accuracy == 0
    assert final.n == 8 and final.accuracy.value == 1 and not final.high_confidence_errors
    assert final.calls.cost_total_usd == pytest.approx(.08)
    reviewed = review(task, sample=99)
    assert {x.id for x in reviewed.listed + reviewed.sample} <= set(pr.ids)
    md = report.write(task, "base", task.where.root / "out")
    assert 'Test (read once' not in md and 'labelled dev cases' in md
    saved = json.loads((task.where.root / 'out' / 'base.json').read_text())
    chart = saved['charts']['fake']
    assert chart['scope'] == 'dev' and chart['n'] == 8 and chart['cv_value'] == e.objective.value


def test_unknown_constraints_and_different_populations_refuse_recommendation(task):
    go(task)
    e = metrics.evaluate(task, metrics.load(task, 'base', 'fake'))
    unknown = e.model_copy(update={'calls': Calls()})
    assert len(violations(Constraints(latency_p99_ms=100, cost_per_10k_usd=100), unknown)) == 2
    second = e.model_copy(update={'candidate': e.candidate.model_copy(update={'model': 'second'}), 'answered_ids': e.answered_ids[:-1]})
    ranked = rank(task.primary, [], task.constraints, [e, second])
    assert all(any('different answered' in reason for reason in r.excluded) for r in ranked)


def test_comparison_binds_saved_fold_values_to_the_current_data(task):
    from s1flow.eval import comparison
    go(task)
    original = comparison.collect(task, include_charts=True)
    row = next(r for r in original.candidates if r.candidate == "fake")
    assert row.n == 8 and row.charts.n == 8
    assert row.value == row.charts.cv_value
    assert len(row.charts.threshold_sweep) >= 101
    assert sum(b.positives + b.negatives for b in row.charts.distribution) == 8
    c = task.load_cases()._all[0]
    change_case(task, "0", label=not c.label)
    changed = comparison.collect(task, include_charts=True)
    assert changed.data_digest != original.data_digest and changed.id != original.id



def test_declared_custom_provider_revision_invalidates_current_answers(task):
    assert go(task)['calls'] == 12
    assert go(task)['skipped'] == 12
    spec = task.where.client().connections.lineup.models['fake']
    assert spec.provider_revision == 'test-fixture-v1'
    spec.provider_revision = 'test-fixture-v2'
    assert metrics.load(task, 'base', 'fake').ids == []
    rerun = go(task)
    assert rerun['calls'] == 12 and rerun['cached'] == 0 and rerun['skipped'] == 0


def test_unversioned_custom_code_cannot_reuse_or_create_evaluation_evidence(task):
    assert go(task)['calls'] == 12
    spec = task.where.client().connections.lineup.models['fake']
    spec.provider_revision = None
    before = Fake.calls
    # Even with persisted genuine answers, unversioned custom code cannot be
    # cached, skipped, scored, or presented as a fresh measurement.
    with pytest.raises(ConfigError, match='needs provider_revision'):
        go(task)
    with pytest.raises(ConfigError, match='needs provider_revision'):
        metrics.load(task, 'base', 'fake')
    client = task.where.client()
    model = client.connections.build(spec, name='fake')
    with pytest.raises(ConfigError, match='needs provider_revision'):
        asyncio.run(run.call(task.where.cache_dir, client, model, {'i': 0}, task.questions(), spec=spec))
    assert Fake.calls == before
    # Raw historical reading remains possible without certifying its identity.
    assert len(records.read(run.run_path(task, 'base', 'fake'))) == 12
    # The direct Client remains available for unassessed application calls.
    asyncio.run(client.responses.create(model=spec, state={'i': 0}, questions=task.questions()))
    assert Fake.calls == before + 1


def test_cloudflare_relay_is_part_of_effective_identity(monkeypatch):
    from s1flow.client.providers.cloudflare import CloudflareModel
    spec = ModelSpec(provider='cloudflare', id='clef')
    monkeypatch.setenv('CLEF_RELAY_URL', 'https://first-relay.test')
    first = model_digest(spec)
    monkeypatch.setenv('CLEF_RELAY_URL', 'https://second-relay.test')
    assert model_digest(spec) != first
    assert CloudflareModel('clef').request({'text': 'a'}, {'q': Boolean(instructions='?')}).url.startswith('https://second-relay.test/')


def test_concurrency_changes_invalidate_performance_without_rebuying_answers(task):
    spec = task.where.lineup().resolved('fake')
    first = execution_digest(spec, 'policy')
    assert asyncio.run(run.run_model(task, 'fake', limit=None, variant='base', concurrency=1))['calls'] == 12
    assert metrics.evaluate(task, metrics.load(task, 'base', 'fake')).calls.latency is not None
    before = Fake.calls
    assert asyncio.run(run.run_model(task, 'fake', limit=None, variant='base', concurrency=8))['skipped'] == 12
    current = metrics.evaluate(task, metrics.load(task, 'base', 'fake'))
    assert current.n == 8 and current.calls.latency is None and current.calls.case_latency_p90_ms is None
    assert Fake.calls == before
    task.where.lineup().models['fake'].concurrency = 8
    assert metrics.evaluate(task, metrics.load(task, 'base', 'fake')).calls.latency is None
    assert asyncio.run(run.run_model(task, 'fake', limit=None, variant='base', concurrency=8, fresh=True))['calls'] == 12
    assert metrics.evaluate(task, metrics.load(task, 'base', 'fake')).calls.latency.concurrency == [8]
    changed = spec.model_copy(update={'concurrency': 8})
    assert execution_digest(changed, 'policy') != first
    assert request_digest(spec.model_copy(update={'concurrency': 1}), {'i': 0}, task.questions()) == request_digest(changed, {'i': 0}, task.questions())


def test_comparison_identity_tracks_held_out_data_without_exposing_test_scores(task):
    from s1flow.eval import comparison
    go(task)
    original = comparison.collect(task, include_charts=True)
    change_case(task, "8", label=False)
    changed = comparison.collect(task, include_charts=True)
    assert changed.data_digest != original.data_digest and changed.id != original.id
    assert [r.value for r in changed.candidates] == [r.value for r in original.candidates]
    task.constraints = Constraints(latency_p99_ms=5)
    constrained = comparison.collect(task, include_charts=True)
    assert constrained.evaluation_contract_digest != changed.evaluation_contract_digest
    assert constrained.id != changed.id
    assert all("test" not in row.model_dump() for row in constrained.candidates)



def test_chart_summary_and_cost_quality_frontier_are_owned_by_report(task):
    go(task)
    report.write(task, "base", task.where.root / "out")
    saved = json.loads((task.where.root / 'out' / 'base.json').read_text())
    assert saved['chart_summary']['candidate_count'] == 1
    assert saved['chart_summary']['cost_quality_frontier'] == ['fake']
    script = (Path(__file__).resolve().parents[1] / 'skills/s1flow/scripts/charts.py').read_text()
    assert 'const better = ' not in script and 'const front = [...rs].sort' not in script


def test_cached_client_reports_stale_timing_without_rebuying_raw_answer(task):
    cached = run.CachedClient(task.where.client(), task.where.cache_dir)
    spec = task.where.lineup().resolved('fake').model_copy(update={'concurrency': 1})
    before = Fake.calls
    first = asyncio.run(cached.responses.create(model=spec, state={'i': 0}, questions=task.questions()))
    assert cached.responses.timing_current(first)
    response = asyncio.run(cached.responses.create(model=spec.model_copy(update={'concurrency': 8}), state={'i': 0}, questions=task.questions()))
    assert cached.responses.hit(response) and not cached.responses.timing_current(response)
    assert Fake.calls == before + 1
