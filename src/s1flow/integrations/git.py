"""git, for the commands that record what was decided: the commit a policy was made at, and who picked it.
The evaluation itself runs no command and changes nothing outside the project (its runs, split files and policies)."""

from __future__ import annotations

import subprocess
from pathlib import Path


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
