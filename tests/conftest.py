"""Test projects: a s1flow.toml whose models are this module's fakes, and tasks attached to it."""

from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import pytest

from s1flow.client import ModelBuild
from s1flow.eval.task import Task
from s1flow.project import Project

BENCH = Path(__file__).resolve().parents[1] / "apps" / "bench"  # s1flow's own evaluation project: s1flow.toml, tasks/, runs/

# name -> factory(ModelBuild). `build` below is the provider every fake in a test project names.
FAKES: dict[str, Callable[[ModelBuild], Any]] = {}


def build(b: ModelBuild) -> Any:
    return FAKES[b.name](b)


@dataclass
class Ran:
    exit_code: int
    output: str  # stdout
    err: str


def cli(*args: str) -> Ran:
    """`s1flow ARGS` in this process (s1flow.cli.main): its exit code, stdout and stderr."""
    from s1flow.cli import main

    out, err, shown = io.StringIO(), io.StringIO(), warnings.showwarning
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), pytest.raises(SystemExit) as e:
            main(list(args))
    finally:
        warnings.showwarning = shown
    return Ran(int(e.value.code or 0), out.getvalue(), err.getvalue())


def make_project(
    root: Path, fakes: dict[str, Callable[[ModelBuild], Any]] | None = None, copy_tasks: tuple[str, ...] = (), versions: dict[str, dict[str, str]] | None = None,
) -> Project:
    """A project in `root`: the given fakes (`versions`: name -> label -> id, for those that declare some) and copies of real tasks."""
    root.mkdir(parents=True, exist_ok=True)
    fakes = fakes or {}
    FAKES.update(fakes)
    toml = ["default = " + json.dumps(list(fakes)), ""]
    for name in fakes:
        toml += [f'[models."{name}"]', 'provider = "conftest:build"', 'provider_revision = "test-fixture-v1"', f'id = "{name}"', ""]
        for label, id_ in (versions or {}).get(name, {}).items():
            toml += [f'[models."{name}".versions."{label}"]', f'id = "{id_}"', ""]
    (root / "s1flow.toml").write_text("\n".join(toml))
    for t in copy_tasks:
        d = t
        shutil.copytree(BENCH / "tasks" / d, root / "tasks" / d, ignore=shutil.ignore_patterns("split.json", "feedback.jsonl", "optimized"))
        src = root / "tasks" / d / "task.py"  # the data stays where it is: point at it from the copy
        src.write_text(re.sub(r'cases="([^"]+)"', lambda m: f'cases="{(BENCH / "tasks" / d / m[1]).resolve()}"', src.read_text(), count=1))
    return Project(root)


def labelled(task: Task, y: Any) -> Task:
    """A task written in a test with no cases file: cases 0..n-1 with these labels, as binary_preds names them
    (the task's evaluation set, eval/evalset.py, is made from them)."""
    from s1flow.eval.cases import Case, Cases

    cases = Cases(task.id, task.dir, task.cases, task.state, task.label)
    cases._all = [Case(id=str(i), state={}, label=v.item() if hasattr(v, "item") else v) for i, v in enumerate(y)]
    task._cases = cases
    return task


def attach(task: Task, project: Project, dir: Path | None = None) -> Task:
    """A task written in a test, as if loaded from the project."""
    task.project = project
    task.dir = dir or task.dir
    return task


@pytest.fixture
def no_ci(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)


def binary_preds(p: Any, y: Any, **kw: Any) -> Any:
    """A boolean task's Preds from P(true) per case, as metrics.load makes them from runs."""
    from s1flow.eval import metrics
    from s1flow.eval.objectives import measure
    from s1flow.policies import DecisionRule
    from s1flow.policies.kinds import Average
    from s1flow.eval.kinds import BooleanKind

    kind = BooleanKind()
    readings = [kind.reading(Average(distributed=True, p_positive=float(x)), DecisionRule()) for x in p]
    pairs = measure.pairs(kind, [bool(v) for v in y], readings)
    return metrics.Preds(model="m", ids=[str(i) for i in range(len(readings))], pairs=pairs, probabilities=True, **kw)


def ship(store, item, reason: str = "t"):
    """Save a policy (a PolicySpec, or an EvaluatedPolicy in an eval Store) and make it current, as adopt does."""
    from s1flow.policies.history import Switch

    spec = getattr(item, "spec", item)
    store.write_new(item, adopted=Switch(action="spec", version=spec.version, previous=store.current(spec.task), by="t", reason=reason))


def point(store, task: str, version: int, reason: str = "t"):
    """Point current at a saved version, as adopt TASK@vN does."""
    from s1flow.policies.history import Switch

    store.switch(task, Switch(action="rollback", version=version, previous=store.current(task), by="t", reason=reason))
