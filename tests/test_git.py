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


def test_the_evaluation_runs_no_command():
    import importlib
    import pkgutil

    import s1flow.eval as ev

    for m in pkgutil.walk_packages(ev.__path__, "s1flow.eval."):
        assert "subprocess" not in vars(importlib.import_module(m.name)), m.name  # lint-imports holds the same as a contract
