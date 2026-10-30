"""Installed CLI/SDK behavior through a real local HTTP provider, without paid API calls."""
from __future__ import annotations

from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Thread


@contextmanager
def local_model():
    calls = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            calls.append(request)
            text = request['state']['text']
            probability = 2.0 if text == 'invalid-response' else .9 if text.startswith('bug') else .1
            payload = {
                'model': request['model'],
                'answers': {qid: {'type': 'noul', 'noul': probability} for qid in request['questions']},
                'usage': {'input_tokens': 10, 'output_tokens': 0},
            }
            data = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/v1', calls
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def exercise_runtime(root: Path, python: str = sys.executable, *, evaluate: bool = True):
    """Also callable from the development interpreter against an isolated base-only wheel install."""
    root.mkdir(parents=True, exist_ok=True)
    other = root / 'application'; other.mkdir()
    env = dict(os.environ, S1FLOW_TEST_API_KEY='local-test-only', NO_PROXY='127.0.0.1,localhost',
               GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='user.name', GIT_CONFIG_VALUE_0='Runtime integration test')
    env.pop('S1FLOW_CONNECTIONS', None)
    env.pop('PYTHONPATH', None)

    def cli(*args, cwd=root, expected=0):
        result = subprocess.run([str(Path(python).with_name('s1flow.exe' if os.name == 'nt' else 's1flow')), *map(str, args)], cwd=cwd, env=env,
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == expected, (args, result.stdout, result.stderr)
        return result

    with local_model() as (endpoint, calls):
        models = root / 's1flow.toml'
        models.write_text(
            'default = ["local"]\n[models.local]\nprovider = "typesafe"\nid = "local-v1"\nconcurrency = 2\n'
            f'options.base_url = "{endpoint}"\noptions.api_key_env = "S1FLOW_TEST_API_KEY"\n'
            '[models.local.versions.v1]\nid = "local-v1"\n'
        )
        source = root / 'bug.json'
        source.write_text(json.dumps({
            'schema': 's1flow/policy@2', 'task': 'ticket-bug', 'version': 1,
            'connection': 'local', 'model_id': 'local-v1',
            'questions': {'bug': {'question': {'type': 'boolean', 'instructions': 'Is this a bug?'},
                                  'rule': {'threshold': .5}}},
        }))
        checked = json.loads(cli('policy', 'create', source, '--connections', models, '--check', '--json').stdout)
        assert checked['binding_checked'] and not calls
        cli('policy', 'create', source, '--root', root / 'policies', expected=2)  # it makes v1 current: why?
        created = json.loads(cli('policy', 'create', source, '--root', root / 'policies', '--reason', 'the first', '--json').stdout)
        policy_path = Path(created['path'])
        second = root / 'bug-v2.json'
        second.write_text(json.dumps({**json.loads(source.read_text()), 'version': 2}))
        adopted = json.loads(cli('adopt', '--spec', second, '--reason', 'try v2', '--json').stdout)  # the base install switches
        assert adopted == {'policy': 'ticket-bug@v2', 'previous': 1, 'evaluated': False, 'path': str(root / 'policies/ticket-bug/v2.json')}
        back = json.loads(cli('adopt', 'ticket-bug@v1', '--reason', 'v2 misread', '--json').stdout)
        assert back['policy'] == 'ticket-bug@v1' and back['previous'] == 2
        history = [json.loads(x) for x in (root / 'policies/ticket-bug/history.jsonl').read_text().splitlines()]
        assert [(h['action'], h['version'], h['previous'], h['reason']) for h in history] == [
            ('spec', 1, None, 'the first'), ('spec', 2, 1, 'try v2'), ('rollback', 1, 2, 'v2 misread')]
        assert history[1]['by'] == 'Runtime integration test'
        log = root / 'decisions.jsonl'
        common = ['--policy', 'ticket-bug@v1', '--path', policy_path, '--connections', models]
        decisions = []
        for text, label in [('bug report', True), ('feature request', False)]:
            decision = json.loads(cli('decide', *common, '--state', json.dumps({'text': text}), '--case-id', 'same-ticket',
                                      '--log', log, '--keep-state', '--json', cwd=other).stdout)
            assert decision['value'] is label and decision['below_min_probability'] is None
            decisions.append(decision)
            cli('feedback', 'record', 'ticket-bug@v1', decision['decision_id'], str(label).lower(),
                '--path', policy_path, '--connections', models, '--log', log, cwd=other)
        assert len(calls) == 2 and decisions[0]['decision_id'] != decisions[1]['decision_id']
        recorded = [json.loads(line) for line in log.read_text().splitlines()]
        assert [event['type'] for event in recorded] == ['answered', 'feedback', 'answered', 'feedback']
        assert recorded[1]['decision_id'] == decisions[0]['decision_id']
        assert recorded[3]['decision_id'] == decisions[1]['decision_id']

        sdk = subprocess.run([python, '-c', '''
import json, sys
from s1flow import Client, policies
client = Client(connections=sys.argv[1])
policy = policies.load(path=sys.argv[2], client=client, log=sys.argv[3], keep_state=True)
decision = policy.decide({"text": "bug from SDK"}, case_id="sdk-ticket")
policy.feedback(decision.decision_id, True)
assert decision.value is True
assert not any(name == "s1flow.eval" or name.startswith("s1flow.eval.") for name in sys.modules)
print(json.dumps({"decision_id": decision.decision_id, "value": decision.value}))
''', str(models), str(policy_path), str(root / 'sdk.jsonl')], cwd=other, env=env,
                             capture_output=True, text=True, timeout=60)
        assert sdk.returncode == 0, sdk.stderr
        assert json.loads(sdk.stdout)['value'] is True
        assert len(calls) == 3

        cli('decide', *common, '--state', '{"text":"invalid-response"}', expected=2)
        assert len(calls) == 4
        bad = json.loads(source.read_text()); bad['provider'] = 'untrusted.module:factory'
        rejected = root / 'bad.json'; rejected.write_text(json.dumps(bad))
        cli('policy', 'create', rejected, '--connections', models, '--check', expected=2)
        bad.pop('provider'); bad['model_id'] = 'not-allowed'; rejected.write_text(json.dumps(bad))
        cli('policy', 'create', rejected, '--connections', models, '--check', expected=2)
        cli('decide', *common, '--state', '[{"type":"image","url":"http://127.0.0.1/secret"}]', expected=2)
        assert len(calls) == 4  # all three refusals above happen before network access

        if not evaluate:
            return {'runtime_calls': len(calls), 'decision_ids': [d['decision_id'] for d in decisions]}
        directory = root / 'tasks' / 'ticket-bug'; directory.mkdir(parents=True)
        directory.joinpath('task.py').write_text(
            'from s1flow.eval import Task\nfrom s1flow.questions import Boolean\n'
            'task = Task(id="ticket-bug", cases="data.jsonl", state=lambda r: {"text": r["text"]}, '
            'label=lambda r: r["label"], question_id="bug", question=Boolean(instructions="Is this a bug?"))\n'
        )
        rows = [{'id': str(i), 'text': f'{"bug" if i % 2 else "feature"} {i}', 'label': bool(i % 2)} for i in range(40)]
        directory.joinpath('data.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows))
        cli('run', 'ticket-bug')
        count = len(calls)
        cli('run', 'ticket-bug')
        assert len(calls) == count  # measured identical requests are reused
        report = json.loads(cli('report', 'ticket-bug', '--json').stdout)
        assert report['candidates'][0]['n'] == 28 and report['ranking'][0]['tied']
        assert all('test' not in row for row in report['candidates'])
        adopted = cli('adopt', 'ticket-bug', 'local', '--reason', 'local HTTP integration proof', '--json')
        assert json.loads(adopted.stdout)['spec']['version'] == 3 and 'current' in adopted.stderr
        assert json.loads((root / 'policies/ticket-bug/channels.json').read_text())['channels'] == {'current': 3}  # merging ships it
        checked = json.loads(cli('check', 'ticket-bug', '--json').stdout)  # v1 and v2 are unevaluated: current alone
        assert checked['n'] == 12 and checked['verdict'] in ('pass', 'no_difference')
        deployed = json.loads(cli('decide', '--policy', 'ticket-bug@v3', '--path', root / 'policies/ticket-bug/v3.json',
                                  '--connections', models, '--state', '{"text":"bug again"}', '--case-id', 'same-ticket',
                                  '--log', log, '--keep-state', '--json', cwd=other).stdout)
        cli('feedback', 'record', 'ticket-bug@v3', deployed['decision_id'], 'true', '--connections', models,
            '--path', root / 'policies/ticket-bug/v3.json', '--log', log)
        measured = json.loads(cli('feedback', 'measure', 'ticket-bug', log, '--json').stdout)
        current = next(r for r in measured['production'] if r['policy'] == 'ticket-bug@v3')
        assert current['objective']['value'] == 1 and current['comparison_reason'] is None
        return {'runtime_calls': len(calls), 'dev': 28, 'test': 12, 'primary': current['objective']['value']}


def test_runtime_to_evaluation_through_local_http(tmp_path):
    result = exercise_runtime(tmp_path)
    assert result['primary'] == 1 and result['runtime_calls'] >= 44
