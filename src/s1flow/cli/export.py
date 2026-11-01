"""`s1flow export`: each task's current policy in one file (policies.json). The base install runs it."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .common import command, policy_root


def export(a: argparse.Namespace) -> int:
    """Each task's current policy and its digest in one file, for an app in another repository or language."""
    from ..policies import policy_set
    from ..policies.file import policy_id

    root = policy_root(a)
    assert root is not None
    b = policy_set.export(root, a.tasks or None)
    Path(a.out).write_text(b.dump())
    for task, e in b.policies.items():
        print(f"{policy_id(task, e.version)} (current) sha256:{e.digest[:12]}")
    print(f"wrote {a.out}: load with policies.load(<task>, path={a.out!r}, client=Client(connections=...))")
    return 0


def add(sub: Any) -> None:
    ex = command(sub, "export", export, context=("project",), help="write the policies an app uses into one file (policies.json)",
                 description="One file with each task's current policy and its digest, for an app in another repository or "
                             "language to vendor and review in its own pull requests. policies.load(task, path=FILE, client=...) reads it.")
    ex.add_argument("tasks", nargs="*", help="the tasks (default: every task with a current version)")
    ex.add_argument("--out", default="policies.json")
