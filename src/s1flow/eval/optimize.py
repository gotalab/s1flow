"""`s1flow optimize`: optimize the shipped question, and adopt the result as next only when it is better on
the test share.

    1. GEPA rewrites current's question for current's model, on train / val (gepa.py)
    2. the new question answers every case (train / val are cached from GEPA; test is new)
    3. adopt builds the next version from that model's runs on current's question and the new one
       (chosen and thresholded on train / val), without storing it
    4. check compares it with current on the test share; only `better` (the interval of the
       difference above 0, or the target met where current misses it) is stored, on the `next` channel

The optimization artifact is kept either way: what was tried, and what it cost.
"""

from __future__ import annotations

import asyncio
import datetime as dt
from typing import Literal

from pydantic import BaseModel

from ..policies.file import NEXT
from . import adopt, check, gepa
from .check import CheckResult
from .run import run_model
from .task import Optimized, Task


class OptimizeResult(BaseModel):
    task: str
    variant: str  # the new question's name
    start: str  # the question it started from
    model: str
    optimization: Optimized  # what GEPA tried and what it cost
    chosen_variant: str  # what adopt chose on train / val
    verdict: Literal["adopted", "no_gain"]
    reason: str = ""
    check: CheckResult | None = None
    policy: str | None = None  # its id, `<task>@vN`, stored on the next channel


def optimize(
    task: Task, budget: int, *, model: str | None = None, reflection: str | None = None,
    patience: int | None = None, max_cost: float | None = None, git_sha: str | None = None,
) -> OptimizeResult:
    current = task.policies.read(task.id)
    model = model or current.candidate.model
    adopt.adoptable(task.where.client().connections.retrieve(model).spec, model)  # before GEPA spends anything: the result must ship
    start = current.candidate.variant if model == current.candidate.model else "base"
    name = f"optimize-{model}-{dt.datetime.now().strftime('%Y%m%d-%H%M')}"
    art = gepa.optimize(task, model, budget=budget, reflection=reflection, start=start, name=name, patience=patience, max_cost=max_cost)
    asyncio.run(run_model(task, model, limit=None, variant=name))
    listed = adopt.shortlist(task, only=[model], variants=list(dict.fromkeys([start, name])))
    # the same model on two questions, kept only when check finds it better on test: optimize picks on its own
    d = adopt.adopt(task, listed.recommended, "s1flow optimize", f"the question optimized for {model}, better than {current.spec.ref} (current) on the held-out test",
                    listed=listed, write=False, git_sha=git_sha)
    out = OptimizeResult(
        task=task.id, variant=name, start=start, model=model, optimization=art,
        chosen_variant=d.candidate.variant, verdict="no_gain",
    )
    if d.candidate.variant != name:
        out.reason = f"on train / val the question it started from ({start}) is better: the new one was not chosen"
        return out
    out.check = r = check.compare([("current", current), ("optimized", d)], task)
    if r.verdict != "better":
        out.reason = "not shown better than current on the test share (" + ("; ".join(r.reasons) or "the difference's interval spans 0") + ")"
        return out
    task.policies.write_new(d)
    task.policies.set_channel(task.id, d.spec.version, NEXT)
    out.verdict, out.policy = "adopted", d.spec.ref
    return out
