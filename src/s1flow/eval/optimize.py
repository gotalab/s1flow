"""`s1flow optimize`: a new candidate, the shipped question rewritten for a model. It ships nothing:

    1. task.py's optimizer (eval/optimizers.py; Gepa by default) rewrites current's question for a model (current's,
       unless --model), given the train and val cases of the task's fixed split; the test share is never in it
    2. s1flow writes what it found, the same record for every optimizer (tasks/<id>/optimized/<variant>.json)
    3. the new question answers every case, as one more question variant (train / val are cached from step 1)

`s1flow report` then lists it beside the others and `s1flow adopt` makes it current when a person picks it, as for
any candidate.
"""

from __future__ import annotations

import asyncio
import dataclasses
import datetime as dt
from typing import Any

from pydantic import BaseModel

from ..core import clock
from ..core.errors import ConfigError
from . import adopt, evalset
from .candidate import Candidate
from .optimizers import Gepa, Problem, resolve
from .run import run_model
from .task import Optimized, Task


class OptimizeResult(BaseModel):
    task: str
    variant: str  # the new question's name
    start: str  # the question it started from
    model: str
    candidate: str  # what report and adopt call it: model/variant
    optimization: Optimized  # what the optimizer was given and set to, what it found and what it cost


def optimize(task: Task, *, model: str | None = None, **overrides: Any) -> OptimizeResult:
    """`overrides`: settings of task.py's Gepa to change for this run (the CLI's --budget, --reflection, ...)."""
    optimizer = resolve(task.optimizer)
    if overrides := {k: v for k, v in overrides.items() if v is not None}:
        if not isinstance(optimizer, Gepa):
            raise ConfigError(f"{', '.join('--' + k.replace('_', '-') for k in overrides)} set GEPA's settings; "
                              f"{task.id} optimizes with {optimizer.name}: set its settings in task.py")
        optimizer = dataclasses.replace(optimizer, **overrides)
    current = task.policies.read(task.id)
    model = model or current.candidate.model
    adopt.adoptable(task.where.client().connections.retrieve(model).spec, model)  # before it spends anything: it must be adoptable
    start = current.candidate.variant if model == current.candidate.model else "base"
    name = f"optimize-{model}-{dt.datetime.now().strftime('%Y%m%d-%H%M')}"
    sf = evalset.fixed(task)
    by_id = task.load_cases().by_id()
    split = {role: [i for i in sf.ids(role) if i in by_id] for role in ("train", "val", "test")}
    seed_q = task.question if start == "base" else task.variants[start]
    found = optimizer.run(Problem(task=task, model=model, start=seed_q,
                                  train=[by_id[i] for i in split["train"]], val=[by_id[i] for i in split["val"]]))
    art = Optimized(variant=name, model=model, optimizer=optimizer.name, settings=optimizer.settings(), at=clock.now(),
                    question=found.question, seed_question=seed_q, start=start, split=split,  # type: ignore[arg-type]
                    model_calls=found.model_calls, cost_usd=found.cost_usd, detail=found.detail)
    out = task.dir / "optimized" / f"{name}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(art.model_dump_json(indent=1) + "\n")
    task.add_optimized(art)
    asyncio.run(run_model(task, model, limit=None, variant=name))
    return OptimizeResult(task=task.id, variant=name, start=start, model=model, candidate=Candidate(model=model, variant=name).name, optimization=art)
