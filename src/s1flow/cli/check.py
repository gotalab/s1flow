"""`s1flow check`: the CI gate, two versions compared case by case on today's test cases."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .common import command, guard, positive, project


def check(a: argparse.Namespace) -> int:
    """Ask both versions about today's test cases and compare them case by case. Exit 0 pass, 1 worse, 2 could not run or pending."""
    from ..eval import check as checking
    from ..eval.check import comment
    from ..eval.task import load

    task_id, markdown = a.task, a.markdown

    def write(text: str) -> None:
        if markdown:
            markdown.parent.mkdir(parents=True, exist_ok=True)
            markdown.write_text(text)

    def failed(message: str) -> None:  # the PR still hears why
        write(comment.error_markdown(task_id, message))

    task = guard(lambda: load(project(a), task_id), failed)
    r = guard(lambda: checking.check(task, a.against, a.candidate, a.sample, a.cached_only), failed)
    md = comment.markdown(task, r)
    write(md)
    print(r.model_dump_json(indent=1) if a.json else md)
    return r.exit


def add(sub: Any) -> None:
    p = command(sub, "check", check, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--against", default="current", help="the version to compare with: vN (on a pull request, the base branch's current) or current")
    p.add_argument("--candidate", help="current, vN, or `draft` (the task's current question); default: current when --against names another version, else the edited question; else current alone, against its target")
    p.add_argument("--sample", type=positive, help="check this many test cases only (a cheap PR check)")
    p.add_argument("--cached-only", action="store_true", help="make no calls (no keys, e.g. a PR from a fork); pending when some are needed")
    p.add_argument("--json", action="store_true")
    p.add_argument("--markdown", type=Path, help="also write the PR comment here")
