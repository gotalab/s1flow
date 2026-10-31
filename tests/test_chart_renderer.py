"""The portable renderer consumes snapshots without model/evaluation dependencies."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugin/skills/s1flow/scripts/charts.py'


def invoke(*args: str):
    return subprocess.run([sys.executable, '-S', str(SCRIPT), *args], capture_output=True, text=True)


def snapshot():
    return json.loads((ROOT / 'schema/fixtures/comparison-2.valid.json').read_text())


def test_renderer_help_and_export_need_only_standard_library(tmp_path):
    assert invoke('--help').returncode == 0
    source = tmp_path / 'comparison.json'
    data = snapshot()
    source.write_text(json.dumps(data))
    destination = tmp_path / 'new' / 'view.html'
    done = invoke(str(source), '--out', str(destination))
    assert done.returncode == 0 and done.stderr == ''
    assert done.stdout.strip() == str(destination)
    page = destination.read_text()
    embedded = page.split('<script id="comparison-data" type="application/json">', 1)[1].split('</script>', 1)[0]
    assert json.loads(embedded) == data
    # PNG export uses an in-memory blob Image; no external scripts or data fetches.
    assert '<script src=' not in page and 'fetch(' not in page
    assert source.read_text() == json.dumps(data)


def test_instructions_cannot_escape_embedded_json_or_title(tmp_path):
    data = snapshot()
    attack = '</script><script>window.injected = true</script> & <img src=x>'
    data['task'] = attack
    data['candidates'][0]['question']['instructions'] = attack
    source = tmp_path / 'comparison.json'; source.write_text(json.dumps(data))
    assert invoke(str(source)).returncode == 0
    page = source.with_suffix('.html').read_text()
    assert '<script>window.injected' not in page and '<img src=x>' not in page
    embedded = page.split('<script id="comparison-data" type="application/json">', 1)[1].split('</script>', 1)[0]
    assert json.loads(embedded) == data


@pytest.mark.parametrize('content', [b'\xff', b'null', b'{"schema":"old"}', b'{"x":NaN}'])
def test_bad_snapshot_is_a_clean_input_error(tmp_path, content):
    source = tmp_path / 'bad.json'; source.write_bytes(content)
    done = invoke(str(source))
    assert done.returncode == 2 and done.stderr.startswith('error:')
    assert 'Traceback' not in done.stderr and not source.with_suffix('.html').exists()


def test_renderer_cannot_overwrite_its_input(tmp_path):
    source = tmp_path / 'comparison.json'; source.write_text(json.dumps(snapshot()))
    before = source.read_bytes()
    done = invoke(str(source), '--out', str(source))
    assert done.returncode == 2 and source.read_bytes() == before


def test_a_snapshot_that_is_not_v2_requires_regeneration(tmp_path):
    source = tmp_path / 'old.json'
    source.write_text(json.dumps({'schema': 's1flow/comparison@1', 'scope': 'dev'}))
    done = invoke(str(source))
    assert done.returncode == 2 and 'regenerate' in done.stderr
    assert not source.with_suffix('.html').exists()
