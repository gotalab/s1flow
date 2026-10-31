"""`s1flow report`: one command reads the saved runs (it replaces compare and rank)."""

from __future__ import annotations

import json

import pytest

from conftest import cli, compare_fake, make_project

TASK = '''from s1flow.eval import Task
from s1flow.questions import Boolean

task = Task(id="truth", cases="data.jsonl", state=lambda r: {"truth": r["truth"]}, label=lambda r: r["truth"],
            question=Boolean(instructions="truth?"))
'''


@pytest.fixture
def ran(tmp_path, monkeypatch):
    project = make_project(tmp_path / "p", {"good": compare_fake("good"), "bad": compare_fake("bad"), "late": compare_fake("good")})
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
    assert lines[0].startswith("truth: ") and lines[2].split()[:2] == ["=", "good"]  # best first; no pick marked
    assert not (ran.root / "reports").exists()
    assert (ran.tasks_dir / "truth" / "split.json").exists()  # fixed on first use, as before


def test_json_holds_every_metric_and_the_ranking(ran):
    got = json.loads(cli("report", "truth", "--json").output)
    assert {c["candidate"] for c in got["candidates"]} == {"good", "bad", "late"}
    assert got["ranking"][0]["candidate"] == "good" and got["ranking"][0]["tied"] and "recommended" not in got["ranking"][0]
    assert set(got["order"]) == {"by", "skipped", "why"}  # what orders the tied rows
    by_name = {c["candidate"]: c for c in got["candidates"]}
    assert by_name["good"]["value"] == got["ranking"][0]["scores"][0]["value"]  # one number for the objective


def test_out_writes_the_snapshot_and_markdown_and_from_reads_it(ran):
    got = cli("report", "truth", "--out", "out")
    assert got.exit_code == 0 and "wrote out/comparison.json, out/questions/base.md, out/questions/base.json" in got.err
    assert (ran.root / "out" / "questions" / "base.md").read_text().startswith("# truth")
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


def test_reading_saved_runs_builds_no_provider(ran, monkeypatch):
    from s1flow.client.providers import llm
    from s1flow.core.errors import ConfigError

    def missing():
        raise ConfigError("the llm provider needs LiteLLM: install s1flow[llm]")

    monkeypatch.setattr(llm, "require_litellm", missing)  # an install without the llm extra
    config = ran.root / "s1flow.toml"
    config.write_text(config.read_text() + '\n[models.chat]\nprovider = "llm"\nid = "openai/gpt-x"\n')
    got = cli("report", "truth")
    assert got.exit_code == 0, got.err
    assert got.output.splitlines()[2].split()[:2] == ["=", "good"] and "not ranked:" in got.output


def test_a_variant_named_comparison_leaves_the_snapshot_alone(ran):
    task_py = ran.tasks_dir / "truth" / "task.py"
    task_py.write_text(task_py.read_text().replace('question=Boolean(instructions="truth?"))',
                                                   'question=Boolean(instructions="truth?"), variants={"comparison": Boolean(instructions="true?")})'))
    assert cli("run", "truth", "--models", "good/comparison").exit_code == 0
    assert cli("report", "truth", "--out", "out").exit_code == 0
    assert json.loads((ran.root / "out" / "comparison.json").read_text())["schema"] == "s1flow/comparison@2"
    assert (ran.root / "out" / "questions" / "comparison.md").is_file()
