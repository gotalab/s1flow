"""The Agent Skill the package carries: `s1flow init --skill`, `init` leaving it out unless asked, and the wheel holding
it."""

import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from conftest import cli

from s1flow import skill
from s1flow.cli import main as base

REPO = Path(__file__).resolve().parents[1]
TOPICS = ["app", "collect", "learn", "measure", "setup", "ship"]
TYPES = ["boolean", "box", "choice", "score"]  # references/types/<type>.md: one playbook per question type
REFERENCES = [*(f"references/{t}.md" for t in TOPICS), *(f"references/types/{t}.md" for t in TYPES)]


def run(*args, capsys):
    with pytest.raises(SystemExit) as e:
        base(list(args))
    out = capsys.readouterr()
    return e.value.code, out.out, out.err


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A git repository to work in, and a home of its own."""
    (tmp_path / "work" / ".git").mkdir(parents=True)
    (tmp_path / "work" / "sub").mkdir()
    monkeypatch.chdir(tmp_path / "work" / "sub")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    return tmp_path / "work"


def test_the_skill_routes_each_job_to_one_reference():
    src = skill.source()
    assert src == REPO / "plugin" / "skills" / "s1flow"
    text = (src / "SKILL.md").read_text()
    assert text.startswith("---\nname: s1flow\ndescription:")
    assert sorted(p.stem for p in (src / "references").glob("*.md")) == TOPICS
    assert all(f"`references/{t}.md`" in text for t in TOPICS)
    assert sorted(p.stem for p in (src / "references" / "types").glob("*.md")) == TYPES
    assert all(f"`references/types/{t}.md`" in text for t in TYPES)  # one hop from SKILL.md, never through another reference
    assert len(text.splitlines()) < 50


@pytest.mark.parametrize("type_", TYPES)
def test_a_playbook_names_only_objectives_its_type_takes(type_):
    """Each `Name(` a playbook writes in code is a built-in objective its question type accepts, so the playbook
    cannot drift from what task.py will load."""
    from s1flow.eval.kinds import kind_of
    from s1flow.eval.objectives.declare import BUILT_IN
    from s1flow.questions import Boolean, Box, Choice, Score

    question = {"boolean": Boolean(instructions="?"), "choice": Choice(instructions="?", criteria={"a": "A", "b": "B"}),
                "score": Score(instructions="?", criteria=["low", "high"]), "box": Box(instructions="?")}[type_]
    takes = set(kind_of(question).objectives)
    by_function = {make.__name__: name for name, make in BUILT_IN.items()}
    text = (skill.source() / "references" / "types" / f"{type_}.md").read_text()
    named = {by_function[f] for f in re.findall(r"`(\w+)\(", text) if f in by_function}
    assert named and named <= takes, f"{type_}.md names {sorted(named - takes)}, which a {type_} question does not take"


def test_the_skill_points_only_at_what_an_installed_package_has():
    """A wheel user has the Skill and the CLI, not this repository: no reference sends them to a file of it."""
    repo_only = re.compile(r"(?<![\w/.])(?:decide/action\.yml|examples/|README|DESIGN\.md|PRODUCT\.md|PLAN\.md|apps/bench)")
    for f in sorted(skill.source().rglob("*.md")):
        text = re.sub(r"https://github\.com/\S+", "", f.read_text())
        assert not repo_only.search(text), f"{f.name}: {repo_only.search(text)[0]}"


def test_the_log_lines_in_the_guide_are_what_s1flow_reads():
    from pydantic import TypeAdapter

    from s1flow.policies.log import Log

    text = (skill.source() / "references" / "app.md").read_text()
    lines = re.findall(r"```json\n(.+?)\n```", text)
    got = [TypeAdapter(Log).validate_json(line).type for line in lines]
    assert got == ["answered", "failed", "feedback"]


def test_init_skill_writes_both_agent_dirs_at_the_git_root(repo, capsys):
    code, out, _ = run("init", "--skill", capsys=capsys)
    assert code == 0
    for d in (".agents/skills/s1flow", ".claude/skills/s1flow"):
        copy = repo / d
        assert (copy / "SKILL.md").read_text() == (skill.source() / "SKILL.md").read_text()
        assert {p.relative_to(copy).as_posix() for p in (copy / "references").rglob("*.md")} == set(REFERENCES)
        marker = json.loads((copy / skill.MARKER).read_text())
        assert marker["schema"] == "s1flow/skill-marker@1" and marker["s1flow_version"] == skill.version() and set(marker["files"]) == {"SKILL.md", "scripts/charts.py", "scripts/charts.html", "scripts/github.py", *REFERENCES}
    assert out.count(f"(s1flow {skill.version()}): {4 + len(REFERENCES)} added") == 2  # SKILL.md, renderer, template, github.py and references
    assert not (repo / "sub" / ".claude").exists() and not (repo.parent / "home").exists()


def test_a_file_changed_there_is_kept_unless_forced(repo, capsys):
    copy = repo / ".claude/skills/s1flow"
    skill.install(repo / ".claude/skills")
    mine = copy / "references" / "ship.md"
    mine.write_text("our own notes\n")

    code, out, _ = run("init", "--skill", capsys=capsys)
    assert code == 0 and "  skipped references/ship.md: changed there (--force overwrites it)" in out
    assert f"{len(REFERENCES) + 3} unchanged, 1 skipped" in out and mine.read_text() == "our own notes\n"
    assert skill.install(repo / ".claude/skills").skipped == ["references/ship.md"]  # still protected the next time

    run("init", "--skill", "--force", capsys=capsys)
    assert mine.read_text() == (skill.source() / "references" / "ship.md").read_text()


def test_a_copy_an_earlier_version_wrote_is_updated_and_a_copy_made_by_hand_is_not_overwritten(repo):
    copy = repo / ".claude/skills/s1flow"
    skill.install(repo / ".claude/skills")
    old = copy / "references" / "learn.md"
    old.write_text("what 0.0.1 wrote\n")  # as an older s1flow wrote it: the marker records this content
    (copy / "references" / "gone.md").write_text("a reference this version dropped\n")
    m = json.loads((copy / skill.MARKER).read_text())
    m["s1flow_version"], m["files"]["references/learn.md"] = "0.0.1", skill._hash(old.read_bytes())
    m["files"]["references/gone.md"] = skill._hash((copy / "references" / "gone.md").read_bytes())
    (copy / skill.MARKER).write_text(json.dumps(m))
    assert skill.stale(repo) == [f"{copy} is from s1flow 0.0.1, this is {skill.version()}: s1flow init --skill updates it"]

    done = skill.install(repo / ".claude/skills")
    assert (done.updated, done.removed, done.skipped) == (["references/learn.md"], ["references/gone.md"], [])
    assert old.read_text() == (skill.source() / "references" / "learn.md").read_text() and skill.stale(repo) == []

    by_hand = repo / "hand"
    shutil.copytree(skill.source(), by_hand / "s1flow")
    (by_hand / "s1flow" / "SKILL.md").write_text("edited\n")
    assert skill.install(by_hand).skipped == ["SKILL.md"]  # no marker: s1flow cannot tell it wrote this


@pytest.mark.parametrize("was, now, stale", [
    ("0.1.0a2", "0.1.0a3", True),  # releases are alphas for now: the number after `a` is what moves
    ("0.1.0a9", "0.1.0a10", True), ("0.1.0a3", "0.1.0b1", True), ("0.1.0rc1", "0.1.0", True), ("0.1.0", "0.1.1a1", True),
    ("0.1.0a3", "0.1.0a3", False), ("0.1.0a3", "0.1.0a2", False), ("0.1.0", "0.1.0rc1", False),
])
def test_a_copy_from_an_earlier_prerelease_is_stale(repo, monkeypatch, was, now, stale):
    copy = repo / ".claude/skills/s1flow"
    skill.install(repo / ".claude/skills")
    m = json.loads((copy / skill.MARKER).read_text())
    (copy / skill.MARKER).write_text(json.dumps(m | {"s1flow_version": was}))
    monkeypatch.setattr(skill, "version", lambda: now)
    assert bool(skill.stale(repo)) is stale


def test_a_link_to_the_package_copy_is_left_alone(repo, capsys):
    (repo / ".claude/skills").mkdir(parents=True)
    (repo / ".claude/skills/s1flow").symlink_to(skill.source())
    _, out, _ = run("init", "--skill", capsys=capsys)
    assert "it is the package's own copy (a link)" in out and not (skill.source() / skill.MARKER).exists()


def test_the_skill_commands_run_on_the_base_install(tmp_path):
    code = ("import sys\nfor m in ('numpy', 'scipy', 'sklearn', 'litellm', 'PIL'): sys.modules[m] = None\n"
            "sys.argv = ARGS\nfrom s1flow.cli import main; main()")
    (tmp_path / ".git").mkdir()
    done = subprocess.run([sys.executable, "-c", code.replace("ARGS", "['s1flow', 'init', '--skill', '--task', 't']")], capture_output=True, text=True, cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    assert (tmp_path / ".claude/skills/s1flow/SKILL.md").is_file() and (tmp_path / "s1flow/tasks/t/task.py").is_file()
    for args in (["export"], ["adopt", "--spec", "nope.json", "--validate"]):  # the base install runs them (here: nothing to export, no file)
        ran = subprocess.run([sys.executable, "-c", code.replace("ARGS", repr(["s1flow", *args]))], capture_output=True, text=True, cwd=tmp_path)
        assert "Traceback" not in ran.stderr and "s1flow[eval]" not in ran.stderr, ran.stderr


def test_init_writes_only_the_project_unless_asked(repo):
    """The Skill only with --skill (the plugin brings it too)."""
    done = cli("init")
    assert done.exit_code == 0, done.output
    assert (repo / "sub" / "s1flow" / "s1flow.toml").is_file()
    assert sorted(p.name for p in repo.iterdir()) == [".git", "sub"]


@pytest.mark.skipif(shutil.which("uv") is None, reason="needs uv to build the wheel")
def test_the_wheel_carries_the_skill(tmp_path):
    done = subprocess.run(["uv", "build", "--wheel", "--out-dir", str(tmp_path), str(REPO)], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    names = zipfile.ZipFile(next(tmp_path.glob("s1flow-*.whl"))).namelist()
    assert "s1flow/skills/s1flow/SKILL.md" in names
    assert "s1flow/skills/s1flow/scripts/charts.html" in names
    assert {f"s1flow/skills/s1flow/{r}" for r in REFERENCES} <= set(names)


def test_the_chart_page_draws_from_a_shared_snapshot_without_evaluation_dependencies(tmp_path):
    """Charts use a fresh fake-provider report, never certify bundled historical runs."""
    import asyncio
    from conftest import Parity, make_project
    from s1flow.eval import metrics, comparison
    from s1flow.eval.run import run as run_models
    from s1flow.eval.task import load

    project = make_project(tmp_path / "project", {"fake": Parity})
    directory = project.tasks_dir / "chart-test"
    directory.mkdir(parents=True)
    (directory / "task.py").write_text(
        'from s1flow.client import Boolean\nfrom s1flow.eval import Task\n'
        'task = Task(id="chart-test", cases="cases.json", state=lambda r: {"i": r["i"]}, '
        'label=lambda r: r["label"], question=Boolean(instructions="Is even?"))\n'
    )
    (directory / "cases.json").write_text(json.dumps([{"id": str(i), "i": i, "label": i % 2 == 0} for i in range(40)]))
    task = load(project, "chart-test")
    asyncio.run(run_models(task, ["fake"]))
    snapshot = tmp_path / "comparison.json"
    snapshot.write_text(comparison.collect(task, include_charts=True).model_dump_json(by_alias=True))
    dev_n = len(metrics.load(task, "base", "fake").ids)
    out = tmp_path / "charts.html"
    done = subprocess.run([sys.executable, "-S", str(skill.source() / "scripts" / "charts.py"), str(snapshot), "--out", str(out)],
                          cwd=project.root, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr[-2000:]
    page = out.read_text()
    data = json.loads(page.split('<script id="comparison-data" type="application/json">', 1)[1].split('</script>', 1)[0])
    assert data["scope"] == "dev" and data["candidates"] and "<script src=" not in page
    assert data == json.loads(snapshot.read_text())
    assert len(done.stdout.splitlines()) == 1 and done.stderr == ""
    assert all(r["n"] == dev_n < 40 for r in data["candidates"])
    assert all(len(r["charts"]["threshold_sweep"]) >= 101 and "cases" not in r for r in data["candidates"])
    assert all(sum(b["positives"] + b["negatives"] for b in r["charts"]["distribution"]) == dev_n for r in data["candidates"])


def test_init_inside_the_project_adds_to_it(repo, capsys):
    assert run("init", capsys=capsys)[0] == 0
    project = repo / "sub" / "s1flow"
    import os
    os.chdir(project)
    code, out, _ = run("init", "--skill", capsys=capsys)
    assert code == 0 and not (project / "s1flow").exists() and (repo / ".claude/skills/s1flow/SKILL.md").is_file()
    code, _, err = run("init", "--force", capsys=capsys)
    assert code == 2 and "--force overwrites changed Skill files: it goes with --skill" in err
