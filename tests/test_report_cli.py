"""`s1flow report`: one command reads the saved runs (it replaces compare and rank)."""

from __future__ import annotations

import json

import pytest

from conftest import cli, make_project
from test_comparison import fake

TASK = '''from s1flow.eval import Task
from s1flow.questions import Boolean

task = Task(id="truth", cases="data.jsonl", state=lambda r: {"truth": r["truth"]}, label=lambda r: r["truth"],
            question=Boolean(instructions="truth?"))
'''


@pytest.fixture
def ran(tmp_path, monkeypatch):
    project = make_project(tmp_path / "p", {"good": fake("good"), "bad": fake("bad"), "late": fake("good")})
    d = project.tasks_dir / "truth"
    d.mkdir(parents=True)
    (d / "task.py").write_text(TASK)
    (d / "data.jsonl").write_text("".join(json.dumps({"id": str(i), "truth": i % 2 == 1}) + "\n" for i in range(30)))
    monkeypatch.chdir(project.root)
    assert cli("run", "truth", "--models", "good,bad").exit_code == 0  # late: in the line-up, never run
    return project


def test_report_ranks_by_the_objective_and_writes_only_the_evaluation_set(ran):
    got = cli("report", "truth")
    assert got.exit_code == 0
    lines = got.output.splitlines()
    assert lines[0].startswith("truth: ") and lines[2].split()[:2] == ["*", "good"]  # best first, the pick marked
    assert not (ran.root / "reports").exists()
    assert (ran.tasks_dir / "truth" / "split.json").exists()  # fixed on first use, as before


def test_json_holds_every_metric_and_the_ranking(ran):
    got = json.loads(cli("report", "truth", "--json").output)
    assert {c["candidate"] for c in got["candidates"]} == {"good", "bad", "late"}
    assert got["ranking"][0]["candidate"] == "good" and got["ranking"][0]["recommended"]
    by_name = {c["candidate"]: c for c in got["candidates"]}
    assert by_name["good"]["value"] == got["ranking"][0]["scores"][0]["value"]  # one number for the objective


def test_out_writes_the_snapshot_and_markdown_and_from_reads_it(ran):
    got = cli("report", "truth", "--out", "out")
    assert got.exit_code == 0 and "wrote out/comparison.json, out/base.md, out/base.json" in got.err
    assert (ran.root / "out" / "base.md").read_text().startswith("# truth")
    offline = cli("report", "--from", "out/comparison.json", "--json")
    assert offline.exit_code == 0 and json.loads(offline.output)["provenance"] == "saved snapshot"
    assert cli("report", "--from", "out/comparison.json", "--out", "again").exit_code == 2


def test_text_names_what_it_does_not_rank_and_pages_by_limit(ran):
    got = cli("report", "truth", "--limit", "1")
    assert got.exit_code == 0
    assert [x.split()[1] for x in got.output.splitlines()[2:3]] == ["good"] and "1 more: --offset 1" in got.output
    assert "not ranked: late" in got.output  # a candidate without runs is named, not dropped
    assert len(json.loads(cli("report", "truth", "--json", "--limit", "1").output)["ranking"]) == 1


def test_one_candidate_in_full_as_text(ran):
    got = cli("report", "truth", "--candidate", "good")
    assert got.exit_code == 0 and got.output.startswith("truth · good: n ") and "metric definitions: [" in got.output


def test_out_must_be_a_directory(ran):
    (ran.root / "taken.json").write_text("{}")
    got = cli("report", "truth", "--out", "taken.json")
    assert got.exit_code == 2 and "--out takes a directory" in got.err and "Traceback" not in got.err


@pytest.mark.parametrize("old", ["compare", "rank"])
def test_the_old_names_say_report(ran, old):
    got = cli(old, "truth")
    assert got.exit_code == 2 and "it is now `report`" in got.err
