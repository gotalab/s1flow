"""`s1flow run`: ask the models about a task's cases (cached)."""

import argparse
import json
import sys
from typing import Any

from ..core.errors import ConfigError
from .common import command, positive, project


def run(a: argparse.Namespace) -> int:
    """Ask the candidates about a task's cases (cached) and write runs/<task>/<variant>/<model[:version]>.jsonl; the first
    run on a task also fixes its held-out test share (tasks/<task>/split.json), the one command that writes it."""
    import asyncio

    from ..eval import evalset
    from ..eval import run as running
    from ..eval.task import load

    p = project(a)
    models = p.client().connections
    names = a.models.split(",") if a.models else [m.name for m in models.list(default_only=True)]
    if not names:
        raise ConfigError(f"{models.path} lists no `default` models to run: pass --models a,b or add default = [...]")
    task = load(p, a.task)
    running.candidates(task, names)  # every name checked before the split is written
    running.require_labels(task, task.load_cases().all())  # and every label: the split is stratified by them
    if note := evalset.fix(task):
        print(f"notice: {note}", file=sys.stderr)
    stats = asyncio.run(running.run(task, names, fresh=a.fresh, concurrency=a.concurrency))
    print(json.dumps(stats, indent=1))
    return 0


def add(sub: Any) -> None:
    p = command(sub, "run", run, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--models", help="comma-separated candidates, model[:version][/variant]: jev:1.14, decider@openrouter/policy (default: s1flow.toml's `default`, on the task's own question)")
    p.add_argument("--fresh", action="store_true", help="call again instead of reading the cache (to measure latency and wall time)")
    p.add_argument("--concurrency", type=positive, help="calls in flight per model (default: the model's own); with it, models run one after another. 1 times each call alone")
