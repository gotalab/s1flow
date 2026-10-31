"""`s1flow cases check | review | correct`: a task's cases, and their labels reviewed and corrected."""

from __future__ import annotations

import argparse
from typing import Any, cast

from ..core.errors import ConfigError
from .common import Parser, command, label, project


def cases_check(a: argparse.Namespace) -> int:
    """Check a task's cases before running it: states build, labels fit the question, duplicates, balance, the split.
    Exit 1 when a case is wrong."""
    from ..eval import data as checking
    from ..eval.task import load

    task = load(project(a), a.task)
    r = checking.check(task)
    print(checking.markdown(task, r))
    return 1 if r.errors else 0


def cases_review(a: argparse.Namespace) -> int:
    """The cases whose label is worth reading again (models disagreeing at a high probability, the same state with
    another label), a random sample, and what the corrections so far say about the task."""
    from ..eval import review as reviewing
    from ..eval.task import load

    task = load(project(a), a.task)
    r = reviewing.review(task, min_probability=a.min_probability, limit=a.limit, sample=a.sample, include_read=a.include_read)
    print(r.model_dump_json(indent=1) if a.json else reviewing.markdown(task, r))
    return 0


def cases_correct(a: argparse.Namespace) -> int:
    """Record a decision about one case's label in corrections.jsonl (the collected data stays as it is)."""
    from ..eval import review as reviewing
    from ..eval.cases import VERDICTS, Verdict
    from ..eval.task import load
    from ..integrations import git

    if a.verdict not in VERDICTS:
        raise ConfigError(f"verdict is one of {', '.join(VERDICTS)}, got {a.verdict!r}")
    value = None if a.label is None else label(a.label)
    task = load(project(a), a.task)
    by = a.by or git.user(task.where.root)
    if not by:
        raise ConfigError("a correction records who decided: give --by or set git config user.name")
    fix = reviewing.correct(task, a.case_id, cast(Verdict, a.verdict), reason=a.reason, by=by, label=value)
    print(f"{fix.id}: {fix.verdict}" + (f" {fix.was!r} -> {fix.label!r}" if fix.verdict == "relabel" else "") + f" ({VERDICTS[fix.verdict]})")
    return 0


def add(sub: Any) -> None:
    group = sub.add_parser("cases", context=("project", "connections"), help="check a task's cases; review and correct their labels",
                           description="Check a task's cases, and review and correct their labels.").add_subparsers(dest="action", required=True, parser_class=Parser)
    p = command(group, "check", cases_check, context=("project",))
    p.add_argument("task")
    p = command(group, "review", cases_review, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--min-probability", type=float, default=0.9, help="list a case when a model answered something else at this probability or more")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--sample", type=int, default=0, help="cases drawn at random from the rest, to estimate the label error rate (how many: see the Skill)")
    p.add_argument("--all", action="store_true", dest="include_read", help="also list cases already corrected")
    p.add_argument("--json", action="store_true")
    p = command(group, "correct", cases_correct, context=("project",))
    p.add_argument("task")
    p.add_argument("case_id")
    p.add_argument("--verdict", required=True, help="relabel | keep | unclear | missing")
    p.add_argument("--reason", required=True, help="the criterion that decides it, or what the state lacks")
    p.add_argument("--by", help="who decided (default: git config user.name)")
    p.add_argument("--label", help="relabel only: the new label (a class key, or true / false)")
