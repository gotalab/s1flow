"""integrations/git.py: the commands the evaluation leaves to the CLI (a local repository, no network)."""

import subprocess

from s1flow.integrations import git


def repo(path):
    for args in (["init", "-q", "-b", "main"], ["config", "user.name", "T"], ["config", "user.email", "t@example.com"],
                 ["commit", "-q", "--allow-empty", "-m", "start"]):
        subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, check=True, capture_output=True, text=True).stdout.strip()


def test_sha_is_the_head_of_the_repository_the_project_is_in(tmp_path):
    inside, beside = tmp_path / "r", tmp_path / "o"
    inside.mkdir(), beside.mkdir()
    head = repo(inside)
    assert git.sha(inside) == head and git.sha(beside) != head


def test_a_dry_run_lists_the_steps_and_changes_nothing(tmp_path):
    head = repo(tmp_path)
    (tmp_path / "policy.json").write_text("{}")
    pr = git.open_pr(tmp_path, "s1flow/optimize-toy", [tmp_path / "policy.json", tmp_path / "gone.json"], "toy: v2", "body", dry_run=True)
    assert pr.files == ["policy.json"] and pr.commands[0] == "git switch -c s1flow/optimize-toy"
    assert any(c.startswith("gh pr create --base main") for c in pr.commands)
    assert git.sha(tmp_path) == head and "policy.json" in subprocess.run(
        ["git", "status", "--porcelain"], cwd=tmp_path, capture_output=True, text=True).stdout  # nothing committed


def test_the_evaluation_runs_no_command():
    import importlib
    import pkgutil

    import s1flow.eval as ev

    for m in pkgutil.walk_packages(ev.__path__, "s1flow.eval."):
        assert "subprocess" not in vars(importlib.import_module(m.name)), m.name  # lint-imports holds the same as a contract
