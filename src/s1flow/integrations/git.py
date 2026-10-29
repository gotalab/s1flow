"""git and GitHub, for the commands that record or share what was decided: the commit a policy was made at,
who picked it, and the pull request `s1flow optimize --pr` opens. The evaluation itself runs no command and changes
nothing outside the project (its runs, split files and policies)."""

from __future__ import annotations

import subprocess
from pathlib import Path

from pydantic import BaseModel

from ..core.errors import S1flowError


def _run(args: list[str], cwd: Path | None = None) -> str | None:
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=5, cwd=str(cwd) if cwd else None)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() or None


def sha(root: Path) -> str | None:
    """HEAD of the repository the project is in; None outside one."""
    return _run(["git", "rev-parse", "HEAD"], root)


def user(root: Path) -> str | None:
    """The selected project's git config user.name; None when unset."""
    return _run(["git", "config", "user.name"], root)


class PullRequest(BaseModel):
    branch: str
    files: list[str]
    url: str = ""
    commands: list[str] = []  # dry run: what would run
    body: str = ""


def open_pr(project_root: Path, branch: str, files: list[Path], title: str, body: str, dry_run: bool = False) -> PullRequest:
    """`files` on a new branch from HEAD, committed, pushed and opened as a PR into the branch it started from.
    Needs a clean tree apart from those files; returns to the branch it started on."""

    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=project_root, capture_output=True, text=True, check=True).stdout.strip()

    root = Path(git("rev-parse", "--show-toplevel"))
    here = git("rev-parse", "--abbrev-ref", "HEAD")
    paths = [str(f.resolve().relative_to(root)) for f in files if f.exists()]
    steps = [
        ["git", "switch", "-c", branch],
        ["git", "add", "--", *paths],
        ["git", "commit", "-m", title],
        ["git", "push", "-u", "origin", branch],
        ["gh", "pr", "create", "--base", here, "--title", title, "--body-file", "-"],
        ["git", "switch", here],
    ]
    if dry_run:
        return PullRequest(branch=branch, files=paths, commands=[" ".join(s) for s in steps], body=body)
    dirty = [ln[3:] for ln in git("status", "--porcelain").splitlines() if ln[3:] not in paths]
    if dirty:
        raise S1flowError(f"the tree has other changes ({', '.join(dirty[:5])}); commit or stash them first")
    url = ""
    for s in steps:
        res = subprocess.run(s, cwd=root, input=body if s[0] == "gh" else None, capture_output=True, text=True)
        if res.returncode:
            raise S1flowError(f"{' '.join(s[:3])} failed: {res.stderr.strip()[:300]}")
        if s[0] == "gh":
            url = res.stdout.strip()
    return PullRequest(branch=branch, files=paths, url=url)
