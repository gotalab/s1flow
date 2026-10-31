"""`s1flow init`: make a project, and with --skill write the Agent Skill. The base install runs it."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from ..core.errors import ConfigError
from .common import command


def init(a: argparse.Namespace) -> int:
    """Make a project in ./s1flow: s1flow.toml, a task, .gitignore, with --ci the CI workflow, with --skill the Agent
    Skill (<git root>/.agents/skills/s1flow/ and .claude/skills/s1flow/; the plugin brings it too). Nothing else
    outside the project."""
    from .. import skill
    from ..project import scaffold

    if a.force and not a.skill:
        raise ConfigError("--force overwrites changed Skill files: it goes with --skill")
    here = Path.cwd()
    # run inside the project (s1flow.toml here), `init` adds to it instead of making s1flow/s1flow/
    target = here if a.dir == "s1flow" and (here / "s1flow.toml").is_file() else here / a.dir
    for line in scaffold.init(target, a.task, workflow=a.ci):
        print(line)
    if a.skill:
        for target in skill.targets():
            for line in skill.lines(skill.install(target, force=a.force)):
                print(line)
    return 0


def add(sub: Any) -> None:
    p = command(sub, "init", init)
    p.add_argument("--task", help="also write tasks/<id>/task.py to fill in")
    p.add_argument("dir", nargs="?", default="s1flow", help="the project directory, made here; everything s1flow writes goes in it (default: s1flow, or this directory when it holds s1flow.toml)")
    p.add_argument("--ci", action="store_true", help="also write .github/workflows/s1flow-check.yml at the git root")
    p.add_argument("--skill", action="store_true", help="also write the Agent Skill into <git root>/.agents/skills/s1flow/ and .claude/skills/s1flow/")
    p.add_argument("--force", action="store_true", help="with --skill: overwrite Skill files changed there since s1flow wrote them")
