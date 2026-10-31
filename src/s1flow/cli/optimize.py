"""`s1flow optimize`: a new candidate question from task.py's optimizer; it ships nothing."""

from __future__ import annotations

import argparse
from typing import Any

from .common import command, positive, project


def optimize(a: argparse.Namespace) -> int:
    """Optimize current's question for a model into a new candidate with task.py's optimizer (GEPA by default, needs
    s1flow[optimize]); it ships nothing: report compares it with the others, adopt makes it current when a person
    picks it."""
    from ..eval import optimize as optimizing
    from ..eval.task import load

    task = load(project(a), a.task)
    r = optimizing.optimize(task, model=a.model, budget=a.budget, reflection=a.reflection, patience=a.patience, max_cost=a.max_cost)
    if a.json:
        print(r.model_dump_json(indent=1))
        return 0
    o = r.optimization
    spent = "not priced" if o.cost_usd is None else f"${o.cost_usd}"
    print(f"{r.task}: candidate {r.candidate}  (from {r.start}, by {o.optimizer}: {o.model_calls} model calls, {spent} beside them)")
    print(f"compare it: s1flow report {r.task}; adopt it: s1flow adopt {r.task} {r.candidate} --reason \"...\"")
    return 0


def add(sub: Any) -> None:
    p = command(sub, "optimize", optimize, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--json", action="store_true")
    p.add_argument("--model", help="model whose question is optimized (default: current's)")
    # GEPA's settings, for this run: task.py's `optimizer=Gepa(...)` sets them
    p.add_argument("--budget", type=positive, help="GEPA: model calls on train/val (task.py's Gepa(budget=...), 300 when not set)")
    p.add_argument("--reflection", help="GEPA: the reflection LM, an `llm` model of s1flow.toml (default: task.py's Gepa(reflection=...), else gpt-6.1-sol on OpenAI's API, OPENAI_API_KEY)")
    p.add_argument("--patience", type=int, help="GEPA: stop after this many proposals without a new best on val")
    p.add_argument("--max-cost", type=float, help="GEPA: stop once the reflection LM has cost this much (USD)")
