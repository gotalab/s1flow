"""The Agent Skill the package carries: `s1flow skill install`, `skill path`, `guide`, `init` leaving it out, the wheel
holding it, and plugin/skills/ kept a copy of skills/."""

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
TOPICS = ["adopt-and-run", "charts", "cli", "collect", "compare", "fix", "logs", "new-version", "review", "sandbox", "task", "workflow"]


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
    assert src == REPO / "skills" / "s1flow"
    text = (src / "SKILL.md").read_text()
    assert text.startswith("---\nname: s1flow\ndescription:")
    assert skill.topics() == TOPICS
    assert all(f"`references/{t}.md`" in text for t in TOPICS)
    assert len(text.splitlines()) < 50


def test_the_skill_points_only_at_what_an_installed_package_has():
    """A wheel user has the Skill and the CLI, not this repository: no reference sends them to a file of it."""
    repo_only = re.compile(r"(?<![\w/.])(?:decide/action\.yml|examples/|README|DESIGN\.md|PRODUCT\.md|PLAN\.md|apps/bench)")
    for f in sorted(skill.source().rglob("*.md")):
        text = re.sub(r"https://github\.com/\S+", "", f.read_text())
        assert not repo_only.search(text), f"{f.name}: {repo_only.search(text)[0]}"


def test_the_log_lines_in_the_guide_are_what_s1flow_reads():
    from pydantic import TypeAdapter

    from s1flow.policies.log import Log

    text = (skill.source() / "references" / "logs.md").read_text()
    lines = re.findall(r"```json\n(.+?)\n```", text)
    got = [TypeAdapter(Log).validate_json(line).type for line in lines]
    assert got == ["answered", "failed", "feedback"]


def test_install_writes_both_agent_dirs_at_the_git_root(repo, capsys):
    code, out, _ = run("skill", "install", capsys=capsys)
    assert code == 0
    for d in (".agents/skills/s1flow", ".claude/skills/s1flow"):
        copy = repo / d
        assert (copy / "SKILL.md").read_text() == (skill.source() / "SKILL.md").read_text()
        assert {p.stem for p in (copy / "references").iterdir()} == set(TOPICS)
        marker = json.loads((copy / skill.MARKER).read_text())
        assert marker["schema"] == "s1flow/skill-marker@1" and marker["s1flow_version"] == skill.version() and set(marker["files"]) == {"SKILL.md", "scripts/charts.py", "scripts/charts.html", *(f"references/{t}.md" for t in TOPICS)}
    assert out.count(f"(s1flow {skill.version()}): {3 + len(TOPICS)} added") == 2  # SKILL.md, renderer, template and references
    assert not (repo / "sub" / ".claude").exists() and not (repo.parent / "home").exists()


def test_install_dir_and_user(repo, capsys):
    a, b = repo.parent / "a", repo.parent / "b"
    assert run("skill", "install", "--dir", str(a), "--dir", str(b), capsys=capsys)[0] == 0
    assert (a / "s1flow" / "SKILL.md").is_file() and (b / "s1flow" / "references" / "review.md").is_file()
    assert not (repo / ".claude").exists()

    assert run("skill", "install", "--user", capsys=capsys)[0] == 0
    home = repo.parent / "home"
    assert (home / ".agents/skills/s1flow/SKILL.md").is_file() and (home / ".claude/skills/s1flow/SKILL.md").is_file()
    assert not (repo / ".claude").exists()


def test_a_file_changed_there_is_kept_unless_forced(repo, capsys):
    copy = repo / ".claude/skills/s1flow"
    skill.install(repo / ".claude/skills")
    mine = copy / "references" / "review.md"
    mine.write_text("our own notes\n")

    code, out, _ = run("skill", "install", "--dir", str(repo / ".claude/skills"), capsys=capsys)
    assert code == 0 and "  skipped references/review.md: changed there (--force overwrites it)" in out
    assert f"{len(TOPICS) + 2} unchanged, 1 skipped" in out and mine.read_text() == "our own notes\n"
    assert skill.install(repo / ".claude/skills").skipped == ["references/review.md"]  # still protected the next time

    run("skill", "install", "--dir", str(repo / ".claude/skills"), "--force", capsys=capsys)
    assert mine.read_text() == (skill.source() / "references" / "review.md").read_text()


def test_an_older_copy_is_updated_and_a_copy_made_by_hand_is_not_overwritten(repo):
    copy = repo / ".claude/skills/s1flow"
    skill.install(repo / ".claude/skills")
    old = copy / "references" / "fix.md"
    old.write_text("what 0.0.1 wrote\n")  # as an older s1flow wrote it: the marker records this content
    (copy / "references" / "gone.md").write_text("a reference this version dropped\n")
    m = json.loads((copy / skill.MARKER).read_text())
    m["s1flow_version"], m["files"]["references/fix.md"] = "0.0.1", skill._hash(old.read_bytes())
    m["files"]["references/gone.md"] = skill._hash((copy / "references" / "gone.md").read_bytes())
    (copy / skill.MARKER).write_text(json.dumps(m))
    assert skill.stale(repo) == [f"{copy} is from s1flow 0.0.1, this is {skill.version()}: s1flow skill install updates it"]

    done = skill.install(repo / ".claude/skills")
    assert (done.updated, done.removed, done.skipped) == (["references/fix.md"], ["references/gone.md"], [])
    assert old.read_text() == (skill.source() / "references" / "fix.md").read_text() and skill.stale(repo) == []

    by_hand = repo / "hand"
    shutil.copytree(skill.source(), by_hand / "s1flow")
    (by_hand / "s1flow" / "SKILL.md").write_text("edited\n")
    assert skill.install(by_hand).skipped == ["SKILL.md"]  # no marker: s1flow cannot tell it wrote this


def test_a_link_to_the_package_copy_is_left_alone(repo, capsys):
    (repo / ".claude/skills").mkdir(parents=True)
    (repo / ".claude/skills/s1flow").symlink_to(skill.source())
    _, out, _ = run("skill", "install", "--dir", str(repo / ".claude/skills"), capsys=capsys)
    assert "it is the package's own copy (a link)" in out and not (skill.source() / skill.MARKER).exists()


def test_path_and_guide(capsys):
    assert run("skill", "path", capsys=capsys)[1].strip() == str(skill.source())
    code, out, _ = run("guide", capsys=capsys)
    assert code == 0 and out.startswith("# s1flow\n") and "| The job | Read |" in out and "description:" not in out
    _, out, _ = run("guide", "review", capsys=capsys)
    assert out == (skill.source() / "references" / "review.md").read_text()
    code, _, err = run("guide", "nope", capsys=capsys)
    assert code == 2 and err.strip() == f"error: no guide on 'nope'; the topics: {', '.join(TOPICS)}"


def test_the_skill_commands_run_on_the_base_install(tmp_path):
    code = ("import sys\nfor m in ('numpy', 'scipy', 'sklearn', 'litellm', 'PIL'): sys.modules[m] = None\n"
            f"sys.argv = ['s1flow', 'skill', 'install', '--dir', {str(tmp_path)!r}]\nfrom s1flow.cli import main; main()")
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert (tmp_path / "s1flow" / "SKILL.md").is_file()


def test_init_writes_only_the_project_unless_asked(repo):
    """The Skill comes from the plugin or `skill install`, and the CI workflow only with --ci."""
    done = cli("init")
    assert done.exit_code == 0, done.output
    assert (repo / "sub" / "s1flow" / "s1flow.toml").is_file()
    assert sorted(p.name for p in repo.iterdir()) == [".git", "sub"]

    assert cli("init", "other", "--ci").exit_code == 0
    assert (repo / ".github/workflows/s1flow-check.yml").is_file()
    assert not (repo / ".claude").exists() and not (repo / ".agents").exists()


@pytest.mark.skipif(shutil.which("uv") is None, reason="needs uv to build the wheel")
def test_the_wheel_carries_the_skill(tmp_path):
    done = subprocess.run(["uv", "build", "--wheel", "--out-dir", str(tmp_path), str(REPO)], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    names = zipfile.ZipFile(next(tmp_path.glob("s1flow-*.whl"))).namelist()
    assert "s1flow/skills/s1flow/SKILL.md" in names
    assert "s1flow/skills/s1flow/scripts/charts.html" in names
    assert {f"s1flow/skills/s1flow/references/{t}.md" for t in TOPICS} <= set(names)


def test_the_plugin_carries_the_same_skill():
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "sync_plugin.py"), "--check"], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr


def test_the_chart_page_draws_from_a_shared_snapshot_without_evaluation_dependencies(tmp_path):
    """Charts use a fresh fake-provider report, never certify bundled historical runs."""
    import asyncio
    from conftest import make_project
    from test_eval_identity import Fake
    from s1flow.eval import metrics, comparison
    from s1flow.eval.run import run as run_models
    from s1flow.eval.task import load

    project = make_project(tmp_path / "project", {"fake": Fake})
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
