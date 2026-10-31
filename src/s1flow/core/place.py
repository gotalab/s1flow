"""Explicit path resolution and bounded project discovery for CLI/development tools.

The runtime Client and policy loader never discover a project. Within Git, discovery
stops at the nearest repository root. Outside Git, only the starting directory and
its s1flow/ child are checked; choose --project explicitly from deeper directories.
"""

from __future__ import annotations

import re
from pathlib import Path

from .errors import ConfigError

CONFIG = "s1flow.toml"
DIR = "s1flow"
TASK_ID = re.compile(r"[a-z0-9][a-z0-9-]*")  # a task's id and its directory: no @ (a policy is TASK@vN), no _ or capitals


def task_id_error(task_id: str) -> str | None:
    """Why `task_id` cannot name a task, None when it can."""
    if TASK_ID.fullmatch(task_id):
        return None
    return f"task id {task_id!r}: lowercase letters, digits and hyphens, starting with a letter or digit (gh-bug, nod-wake)"


def absolute(path: str | Path, what: str) -> Path:
    """Resolve a caller-owned path once, before later work can change the cwd."""
    try:
        return Path(path).expanduser().resolve()
    except (OSError, RuntimeError, ValueError) as e:
        raise ConfigError(f"cannot resolve {what} path {path!s}: {e}") from None


def git_root(start: Path) -> Path | None:
    """The nearest directory at or above the absolute path `start` that holds .git; None outside Git."""
    return next((d for d in [start, *start.parents] if (d / ".git").exists()), None)


def search_dirs(start: Path) -> list[Path]:
    """Directories inside the nearest Git root; without Git, just start."""
    top = git_root(start)
    return [start] if top is None else [d for d in [start, *start.parents] if d.is_relative_to(top)]


def _at(directory: Path) -> Path | None:
    for candidate in (directory, directory / DIR):
        if (candidate / CONFIG).is_file():
            return candidate
    return None


def find(start: Path | None = None) -> Path | None:
    here = absolute(start or Path.cwd(), "project")
    return next((found for directory in search_dirs(here) if (found := _at(directory)) is not None), None)


def project(path: Path | None = None, *, required: bool = True) -> Path | None:
    """An explicit project directory (no ascent), or bounded discovery from cwd."""
    here = absolute(path if path is not None else Path.cwd(), "project")
    if path is not None and not here.is_dir():
        raise ConfigError(f"project directory {here} does not exist or is not a directory; use --project PATH with the directory containing {CONFIG}")
    found = _at(here) if path is not None else find(here)
    if found is None and (required or path is not None):
        boundary = here if path is not None else search_dirs(here)[-1]
        raise ConfigError(f"no s1flow project found: searched {here} through {boundary} for {CONFIG} or {DIR}/{CONFIG}; "
                          "use --project PATH or run s1flow init")
    return found
