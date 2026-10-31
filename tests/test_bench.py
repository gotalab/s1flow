"""apps/bench, s1flow's own evaluation project, still reads with this code: its tasks, line-up, policies and report
snapshots. Nothing here pins what the bench holds (which models, versions or results), so re-running or adopting
there changes no test; a failure here means a change made the bench's committed records unreadable. Then rewrite
those records to the current shape, or re-run the bench, in the same change; do not loosen these tests. Tests of
the package's own behaviour read the frozen copy in tests/fixtures/project instead (conftest.PROJECT)."""

import json
import re
import shutil

import pytest
from conftest import BENCH, cli

from s1flow.client.lineup import Lineup
from s1flow.eval.policy import Store
from s1flow.policies.file import read_file

TASKS = sorted(p.parent.name for p in (BENCH / "tasks").glob("*/task.py"))
SNAPSHOTS = sorted((BENCH / "reports").glob("*/comparison.json"))
POLICIES = sorted(p for p in (BENCH / "policies").glob("*/v*.json") if re.fullmatch(r"v\d+\.json", p.name))


def test_the_bench_has_something_to_read():
    assert TASKS and SNAPSHOTS and POLICIES


@pytest.mark.parametrize("task", TASKS)
def test_each_task_loads_and_its_cases_check(task):
    done = cli("cases", "check", task, "--project", str(BENCH))
    assert done.exit_code == 0, done.err


@pytest.mark.parametrize("snapshot", SNAPSHOTS, ids=lambda p: p.parent.name)
def test_each_report_snapshot_reads_offline(snapshot):
    done = cli("report", "--from", str(snapshot), "--json")
    assert done.exit_code == 0, done.err
    assert json.loads(done.output)


def test_each_stored_policy_reads_with_the_policy_layer_alone(tmp_path):
    shutil.copytree(BENCH / "policies", tmp_path / "policies")  # a copy: reading must not need to write
    store = Store(tmp_path / "policies")
    for path in POLICIES:
        spec = read_file(tmp_path / "policies" / path.parent.name / path.name)
        assert spec.question_id in spec.questions and spec.kind and spec.rule, path
        assert store.evaluated(spec.task, version=spec.version).spec == spec, path


def test_the_line_up_and_what_each_task_runs_read():
    assert cli("models", "--project", str(BENCH)).exit_code == 0  # s1flow.toml with models.verified.json
    done = cli("report", "--project", str(BENCH), "--json")  # no task: every task's current version and why
    assert done.exit_code == 0, done.err
    assert {t["task"] for t in json.loads(done.output)} == set(TASKS)


def test_a_model_has_a_list_price_exactly_when_its_api_returns_no_cost():
    """As the line-up's header says: AI Gateway and OpenRouter return what they billed; the others need a price."""
    lineup = Lineup.read(BENCH / "s1flow.toml")
    for name, spec in lineup.models.items():
        if spec.provider in ("gateway", "openrouter"):
            assert spec.price is None, f"{name} is billed by {spec.provider}: drop its price"
        elif spec.provider in ("typesafe", "cloudflare", "openai-decisions"):
            assert spec.price is not None, f"{name}: {spec.provider} returns no cost, so it needs a list price"
