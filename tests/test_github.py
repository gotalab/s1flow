"""The GitHub source on fetched issues (no network): how labels are used, why a case got its label, and gh."""

import json

from conftest import cli, make_project

from s1flow.sources import github


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
    p = make_project(tmp_path / "p")
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
    d = p.tasks_dir / "t"
    d.mkdir(parents=True)
    (d / "data.jsonl").write_text("".join(json.dumps({"id": f"#{n}", "label": "bug"}) + "\n" for n in (1, 2)))
    assert github.add_rationales(p, "o/r", "t") == (1, 2)  # the comments were cached: gh is not called
    rows = [json.loads(x) for x in (d / "data.jsonl").read_text().splitlines()]
    assert [r["rationale"] for r in rows] == ["A crash, so a bug.", ""]


def test_without_gh_the_command_says_what_to_install(tmp_path, monkeypatch):
    p = fetched(tmp_path, [issue(1, "bug")])
    monkeypatch.chdir(p.root)
    monkeypatch.setattr(github.shutil, "which", lambda name: None)
    got = cli("github", "fetch", "o/r")
    assert got.exit_code == 2 and github.GH_MISSING in got.err
    assert cli("github", "audit", "o/r").exit_code == 0  # reads what fetch saved: no gh needed
