"""policies.json (`s1flow policy export`): the policies an app uses, in one file it vendors and loads from."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from test_client import s1flow

from s1flow import Client, policies
from s1flow.core.errors import ConfigError, NotFound
from s1flow.policies import policy_set
from s1flow.policies.file import PolicySpec, read_file

BENCH = Path(__file__).resolve().parents[1] / "apps" / "bench"
SCHEMA = json.loads((BENCH.parents[1] / "schema" / "policy-set-2.json").read_text())


@pytest.fixture
def project(tmp_path):
    shutil.copytree(BENCH / "policies", tmp_path / "policies")
    (tmp_path / "s1flow.toml").write_text("default = []\n[models]\n")
    return tmp_path


def runtime_load(*args, **kwargs):
    return policies.load(*args, client=Client(connections=BENCH / "s1flow.toml"), **kwargs)


def test_an_export_holds_each_policy_as_its_file_without_its_evidence_with_its_digest(project):
    b = policy_set.export(project / "policies", channel="next")
    assert {t: e.version for t, e in b.policies.items()} == {"gh-ruff-area": 3, "gh-ruff-kind": 1, "nod-wake": 1}
    for task, e in b.policies.items():
        f = project / "policies" / task / f"v{e.version}.json"
        assert "high_confidence_errors" in json.loads(f.with_name(f.stem + ".evaluation.json").read_text())["evidence"]["evaluation"]  # the cases a model got wrong, with their labels
        assert e.policy == read_file(f) and e.digest == read_file(f).digest
    assert "high_confidence_errors" not in b.dump()
    assert list(Draft202012Validator(SCHEMA).iter_errors(json.loads(b.dump()))) == []
    assert b.dump() == policy_set.export(project / "policies", channel="next").dump()  # no timestamp: the same versions, the same bytes
    assert list(policy_set.export(project / "policies").policies) == ["gh-ruff-area"]  # current: the tasks that have one
    with pytest.raises(NotFound):
        policy_set.export(project / "policies", channel="nightly")


def test_a_policy_loads_from_the_policy_set_as_from_policies(project, tmp_path):
    out = tmp_path / "policies.json"
    out.write_text(policy_set.export(project / "policies", ["nod-wake", "gh-ruff-area"], "next").dump())
    loaded = runtime_load("nod-wake", path=out)
    direct = runtime_load("nod-wake@next", root=project / "policies")
    assert "evidence" not in loaded.spec.model_dump() and loaded.spec.digest == direct.spec.digest  # the log names the version in policies/
    assert loaded.spec == direct.spec
    assert runtime_load("gh-ruff-area", path=out).spec.version == 3
    assert runtime_load("gh-ruff-area@v3", path=out).spec.version == 3 and runtime_load("gh-ruff-area@next", path=out).spec.version == 3
    with pytest.raises(NotFound, match="holds gh-ruff-area@v3 from next, not gh-ruff-area@v2"):
        runtime_load("gh-ruff-area@v2", path=out)
    with pytest.raises(NotFound, match="not gh-ruff-area@current"):
        runtime_load("gh-ruff-area@current", path=out)
    with pytest.raises(ConfigError, match="name a task"):
        runtime_load(path=out)
    with pytest.raises(NotFound, match="no policy of gh-ruff-kind"):
        runtime_load("gh-ruff-kind", path=out)


def test_a_policy_set_edited_by_hand_is_refused(project, tmp_path):
    out = tmp_path / "policies.json"
    data = json.loads(policy_set.export(project / "policies", ["nod-wake"], "next").dump())
    data["policies"]["nod-wake"]["policy"]["questions"]["next"]["rule"]["min_probability"] = 0.1
    out.write_text(json.dumps(data))
    with pytest.raises(ConfigError, match="does not match its version or digest"):
        runtime_load("nod-wake", path=out)
    data["policies"]["nod-wake"]["extra"] = 1
    out.write_text(json.dumps(data))
    with pytest.raises(ConfigError, match="not a v2 policy set"):
        runtime_load("nod-wake", path=out)


def test_the_commands_export_and_read_the_policy_set(project):
    done = s1flow("policy", "export", "nod-wake", "--channel", "next", "--out", "policies.json", cwd=project)
    assert done.returncode == 0, done.stderr
    assert "nod-wake@v1 (next)" in done.stdout and (project / "policies.json").is_file()
    shutil.rmtree(project / "policies")  # the app has the one file, not policies/
    (project / "policies").mkdir()
    runtime_load("nod-wake", path=project / "policies.json", log=project / "log.jsonl").feedback("c1", True)
    assert json.loads((project / "log.jsonl").read_text())["policy"] == "nod-wake@v1"
