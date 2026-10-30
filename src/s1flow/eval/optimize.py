"""`s1flow optimize`: a new candidate, the shipped question rewritten for a model. It ships nothing:

    1. GEPA rewrites current's question for a model (current's, unless --model), on train / val (gepa.py);
       the test share is never shown to it
    2. the new question answers every case, as one more question variant (train / val are cached from GEPA)

`s1flow report` then lists it beside the others and `s1flow adopt` makes it current when a person picks it, as for
any candidate. The optimization artifact is kept: what was tried, and what it cost.
"""

from __future__ import annotations

import asyncio
import datetime as dt

from pydantic import BaseModel

from . import adopt, gepa
from .candidate import Candidate
from .run import run_model
from .task import Optimized, Task


class OptimizeResult(BaseModel):
    task: str
    variant: str  # the new question's name
    start: str  # the question it started from
    model: str
    candidate: str  # what report and adopt call it: model/variant
    optimization: Optimized  # what GEPA tried and what it cost


def optimize(
    task: Task, budget: int, *, model: str | None = None, reflection: str | None = None,
    patience: int | None = None, max_cost: float | None = None,
) -> OptimizeResult:
    current = task.policies.read(task.id)
    model = model or current.candidate.model
    adopt.adoptable(task.where.client().connections.retrieve(model).spec, model)  # before GEPA spends anything: it must be adoptable
    start = current.candidate.variant if model == current.candidate.model else "base"
    name = f"optimize-{model}-{dt.datetime.now().strftime('%Y%m%d-%H%M')}"
    art = gepa.optimize(task, model, budget=budget, reflection=reflection, start=start, name=name, patience=patience, max_cost=max_cost)
    asyncio.run(run_model(task, model, limit=None, variant=name))
    return OptimizeResult(task=task.id, variant=name, start=start, model=model, candidate=Candidate(model=model, variant=name).name, optimization=art)
