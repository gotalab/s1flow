"""The Skill's GitHub script on fetched issues (no network): how labels are used, why a case got its label, and gh."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/s1flow/scripts/github.py"
spec = importlib.util.spec_from_file_location("skill_github", SCRIPT)
github = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github)


def invoke(*args: str, env: dict[str, str] | None = None):
    return subprocess.run([sys.executable, "-S", str(SCRIPT), *args], capture_output=True, text=True, env=env)


def issue(n, *labels, by="human"):
    actor = {"login": "bot[bot]", "__typename": "Bot"} if by == "bot" else {"login": "maintainer", "__typename": "User"}
    return {
        "number": n, "title": f"Issue {n}", "body": "text", "createdAt": f"2026-10-{n:02d}T00:00:00Z", "author": {"login": "reporter"},
        "labels": {"nodes": [{"name": label} for label in labels]},
        "timelineItems": {"nodes": [
            {"__typename": "LabeledEvent", "label": {"name": label}, "actor": actor, "createdAt": f"2026-10-{n:02d}T01:00:00Z"} for label in labels
        ]},
    }


def fetched(tmp_path, issues, labels=()):
    p = tmp_path / "p"
    p.mkdir(parents=True)
    (p / "s1flow.toml").write_text("")
    d = github.repo_dir(p, "o/r")
    d.mkdir(parents=True)
    (d / "issues.jsonl").write_text("".join(json.dumps(i) + "\n" for i in issues))
    (d / "labels.json").write_text(json.dumps([{"name": n, "description": desc} for n, desc in labels]))
    return p


def test_audit_counts_each_group_and_who_applied_it(tmp_path):
    issues = [issue(3, "area/cli", "area/docs"), issue(2, "area/cli", by="bot"), issue(1)]
    p = fetched(tmp_path, issues, [("area/cli", "The CLI"), ("area/docs", "")])
    md = github.audit(p, "o/r")
    assert "3 issues (2026-10-01 to 2026-10-03). Unlabelled 1 (33%)." in md
    assert "| area | 2 (67%) | 1 | 2 / 1 / 0 | area/cli (2), area/docs (1) |" in md
    assert "1 labels without a description: area/docs" in md
    assert (github.repo_dir(p, "o/r") / "audit.md").read_text() == md


def test_a_rationale_is_what_maintainers_wrote_around_the_labelling(tmp_path):
    p = fetched(tmp_path, [issue(1, "bug"), issue(2, "bug")])
    comments = [
        {"createdAt": "2026-10-01T02:00:00Z", "authorAssociation": "MEMBER", "body": "A crash, so a bug.", "author": {"login": "m"}},
        {"createdAt": "2026-10-01T02:00:00Z", "authorAssociation": "NONE", "body": "+1", "author": {"login": "someone"}},
        {"createdAt": "2026-10-05T00:00:00Z", "authorAssociation": "MEMBER", "body": "Much later.", "author": {"login": "m"}},
    ]
    (github.repo_dir(p, "o/r") / "comments.jsonl").write_text(
        json.dumps({"number": 1, "comments": comments}) + "\n" + json.dumps({"number": 2, "comments": []}) + "\n")
    d = p / "tasks" / "t"
    d.mkdir(parents=True)
    (d / "data.jsonl").write_text("".join(json.dumps({"id": f"#{n}", "label": "bug"}) + "\n" for n in (1, 2)))
    assert github.add_rationales(p, "o/r", "t") == (1, 2)  # the comments were cached: gh is not called
    rows = [json.loads(x) for x in (d / "data.jsonl").read_text().splitlines()]
    assert [r["rationale"] for r in rows] == ["A crash, so a bug.", ""]


def test_without_gh_the_script_says_what_to_install_and_audit_still_runs(tmp_path):
    p = fetched(tmp_path, [issue(1, "bug")])
    no_gh = {"PATH": str(tmp_path / "empty")}
    got = invoke("fetch", "o/r", "--project", str(p), env=no_gh)
    assert got.returncode == 2 and github.GH_MISSING in got.stderr and "Traceback" not in got.stderr
    assert invoke("audit", "o/r", "--project", str(p), env=no_gh).returncode == 0  # reads what fetch saved


def test_the_project_is_found_as_the_cli_finds_it(tmp_path, monkeypatch):
    p = fetched(tmp_path / "repo", [issue(1, "bug")])  # repo/p/s1flow.toml
    (tmp_path / "repo" / ".git").mkdir()
    assert github.find_project(p) == p
    (tmp_path / "repo" / "p").rename(tmp_path / "repo" / "s1flow")
    assert github.find_project(tmp_path / "repo") == tmp_path / "repo" / "s1flow"  # DIR's s1flow/ child
    monkeypatch.chdir(tmp_path / "repo" / "s1flow" / "data")
    assert github.find_project(None) == tmp_path / "repo" / "s1flow"  # searched up from here
    (tmp_path / "repo" / ".git").rmdir()
    with pytest.raises(github.Stop):  # outside Git only the starting directory counts, as in the CLI
        github.find_project(None)
    got = invoke("audit", "o/r", "--project", str(tmp_path / "elsewhere"))
    assert got.returncode == 2 and "no s1flow project" in got.stderr and "Traceback" not in got.stderr


