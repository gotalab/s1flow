"""What more than one test file uses (a test file imports from here, never from another test file): test projects,
a s1flow.toml whose models are this module's fakes, and tasks attached to them; the CLI in this process or a fresh one;
a runtime policy and a client for it; tasks and evaluations written in a test."""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import pytest

from s1flow import Client
from s1flow.client import Boolean, BooleanAnswer, BoxAnswer, BoxEdges, Capabilities, Choice, ChoiceAnswer, ModelBuild, ModelSpec, Response, Usage
from s1flow.client.lineup import Lineup
from s1flow.eval.candidate import Candidate
from s1flow.eval.evaluation import Calls, Estimate, Evaluation, Failures, Latency, ObjectiveScore, Selective
from s1flow.eval.task import Task
from s1flow.objectives import Coverage, Objective
from s1flow.policies import DecisionRule, PolicySpec, asked
from s1flow.project import Project

HERE = Path(__file__).resolve().parent  # on PYTHONPATH in an s1flow process: toy_provider is importable
BENCH = HERE.parent / "apps" / "bench"  # s1flow's own evaluation project: its tasks are the tests' real cases
# A real line-up and stored policies the tests own: a frozen copy of the bench's, which re-running the bench leaves alone.
PROJECT = HERE / "fixtures" / "project"

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


def write_cases(task: Task, rows: list[dict[str, Any]]) -> Task:
    """Write `rows` as the task's cases file (task.dir / task.cases: a .json array, else JSON lines) and read them
    from it again, as a task.py's data is read."""
    path = task.dir / task.cases
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows) if path.suffix == ".json" else "".join(json.dumps(r) + "\n" for r in rows))
    task.load_cases().forget()
    return task


def labelled(task: Task, y: Any, dir: Path) -> Task:
    """The task reading cases 0..n-1 with these labels and empty states, as binary_preds names them, from a cases
    file written in `dir` (the task's evaluation set, eval/evalset.py, is made from them)."""
    task.dir, task.cases, task.state, task.label = dir, "cases.jsonl", lambda r: {}, lambda r: r["label"]
    return write_cases(task, [{"id": str(i), "label": v.item() if hasattr(v, "item") else v} for i, v in enumerate(y)])


def attach(task: Task, project: Project, dir: Path | None = None) -> Task:
    """A task written in a test, as if loaded from the project."""
    task.project = project
    task.dir = dir or task.dir
    return task


CONDITIONS = ("data", "adapter", "contract", "binding", "run")  # what eval.run.Conditions holds


def change_condition(task: Task, what: str, model: str) -> str:
    """Change one condition scoring `model`'s base run depends on, as another process could while it is scored;
    the words a refusal names it with."""
    from s1flow.eval import run
    from s1flow.eval.objectives.declare import Constraints

    if what == "data":
        path = task.dir / task.cases
        path.write_text(json.dumps([{**row, "label": not row["label"]} for row in json.loads(path.read_text())]))
        return "input data or labels"
    if what == "adapter":
        state = task.state
        task.state = lambda row: state(row)  # the same inputs from other code
        return "the input adapter"
    if what == "contract":
        task.constraints = Constraints(min_recall=0.01)
        return "the evaluation contract"
    if what == "binding":
        task.where.lineup().models[model].concurrency = 8
        return f"the execution conditions of {model}"
    meta = run.run_path(task, "base", model).with_suffix(".meta.json")
    meta.write_text(meta.read_text() + "\n")
    return f"the runs of {model}"


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
    write = store.write_new if spec is item else store.write_evaluated
    write(item, adopted=Switch(action="spec", version=spec.version, previous=store.current(spec.task), by="t", reason=reason))


def point(store, task: str, version: int):
    """Point current at a saved version, as a base branch's channels.json does."""
    from s1flow.policies.file import ChannelsFile

    (store.dir(task) / "channels.json").write_text(ChannelsFile(channels={"current": version}).dump())


def s1flow(*args: str, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """`s1flow ARGS` in a fresh process, without the caller's S1FLOW_* settings (cli runs it in this one)."""
    e = {k: v for k, v in os.environ.items() if not k.startswith("S1FLOW_")} | {"PYTHONPATH": str(HERE)} | (env or {})
    return subprocess.run([sys.executable, "-c", "from s1flow.cli import main; main()", *args], cwd=cwd, capture_output=True, text=True, env=e)


# ---------- a runtime policy and a client that answers it, without a project ----------


def runtime_spec(**changes: Any) -> PolicySpec:
    """ticket@v1: one boolean question at threshold 0.5, on fake_client's `trusted` connection."""
    return PolicySpec.model_validate({
        'task': 'ticket', 'version': 1, 'connection': 'trusted', 'model_id': 'fixed-v1',
        'at': '2026-10-24T00:00:00Z',
        'questions': {'bug': asked(Boolean(instructions='Is this a bug?'), DecisionRule(threshold=.5))},
        **changes,
    })


def fake_client(monkeypatch: pytest.MonkeyPatch, *, spec: ModelSpec | None = None,
                probability: float = .8) -> tuple[Client, list[Any]]:
    """A Client whose `trusted` model answers P(true) = `probability` to every question; `calls` lists each model
    built (its spec) and each state asked."""
    spec = spec or ModelSpec(provider='application:factory', id='fixed-v1')
    out = Client(connections=Lineup(default=[], models={'trusted': spec}))
    calls: list[Any] = []

    class Model:
        id = spec.id
        capabilities = Capabilities(image=True)
        concurrency = 1

        async def decide(self, state: Any, questions: Any, **kw: Any) -> Response:
            calls.append(state)
            return Response(answers={key: BooleanAnswer(probability=probability) for key in questions}, answered_by=self.id)

    def build(model: Any, **kw: Any) -> Model:
        assert isinstance(model, ModelSpec)
        calls.append(model)
        return Model()

    monkeypatch.setattr(out.connections, 'build', build)
    return out, calls


# ---------- tasks and evaluations written in a test (objectives, tiebreak, loss) ----------


def task(objs: list[Any], **kw: Any) -> Task:
    """A boolean task: the first of `objs` its objective, the rest its tiebreak."""
    return Task(id="t", cases="x.jsonl", state=lambda r: r["x"], question=Boolean(instructions="?"), label=lambda r: r["y"],
                objective=objs[0] if objs else None, tiebreak=objs[1:], **kw)


CHOICE = Choice(instructions="?", criteria={"a": None, "b": None, "c": None})


def declared(objs: list[Any], question: Any = CHOICE, **kw: Any) -> Task:
    """`task` with another question (a choice of three), named as a bench task."""
    return Task(id="gh-ruff-area", cases="x", state=lambda r: r, question=question, label=lambda r: r,
                objective=objs[0] if objs else None, tiebreak=objs[1:], **kw)


def scored(o: Objective, v: float, half: float = 0.05) -> ObjectiveScore:
    return ObjectiveScore(objective=o, value=v, interval=(v - half, v + half))


def ev(model: str, scores: list[ObjectiveScore], cost: float = 1.0, p99: float = 100.0, n: int = 100) -> Evaluation:
    """An evaluation of `model` on n cases: these objective scores, this cost per 10,000 cases and latency."""
    lat = Latency(n=n, p50_ms=p99 / 2, p90_ms=p99, p95_ms=p99, p99_ms=p99, max_ms=p99, spread=2.0, retried=0, unrecorded=0, concurrency=[4], concurrency_unknown=0)
    return Evaluation(
        candidate=Candidate(model=model), answered_by=model, answered_by_all=[model], answered_ids=[str(i) for i in range(n)], n=n, probabilities=True,
        failures=Failures(calls=n, failed=0, unsupported=0, data_errors=0, unlabeled=0), accuracy=Estimate(value=0.9, interval=(0.85, 0.95)),
        objective=scores[0], tiebreak=scores[1:], calls=Calls(cost_per_10k_usd=cost, latency=lat),
    )


def cov(model: str, v: float, **kw: Any) -> Evaluation:
    """`ev` with Coverage() as the objective, at value v."""
    sel = Selective(target_accuracy=0.95, coverage=Estimate(value=v, interval=(v - 0.05, v + 0.05)), accuracy=0.96, n=50, errors=2, lower=0.9, labels_needed=None, min_probability=0.9)
    return ev(model, [scored(Coverage(), v)], **kw).model_copy(update={"selective": [sel]})


# ---------- fake models a test project names (make_project) ----------


class Sharp:
    """Right on every case (state["y"]), with the probability it was made with: "good" 0.97, "vague" 0.6."""

    def __init__(self, b: ModelBuild):
        self.sure = {"good": 0.97, "vague": 0.6}[b.name]
        self.id, self.concurrency, self.capabilities = f"sharp:{self.sure}", 4, Capabilities()

    async def decide(self, state, questions, *, options=None):
        p = self.sure if state["y"] else 1 - self.sure
        return Response(answers={"q": BooleanAnswer(probability=p)}, answered_by=f"{self.id}-v2", usage=Usage(cost_usd=0.0001))


class Timed:
    """Answers right on every case after 120 ms, with one retry as a provider would report it."""

    def __init__(self, b=None):
        self.id, self.concurrency, self.capabilities = "fake:t", 4, Capabilities()
        self.ms, self.retries = 120, 1

    async def decide(self, state, questions, *, options=None):
        q = next(iter(questions))
        a = ChoiceAnswer(choice="wake", probabilities={"wake": 0.99, "sleep": 0.01})
        return Response(answers={q: a}, answered_by=self.id, latency_ms=self.ms, retries=self.retries)


class Parity:
    """Whether state["i"] is even: right below 8, wrong from 8 on, both at high probability. Counts its calls."""

    calls = 0

    def __init__(self, build):
        self.id = 'wire:' + build.spec.id
        self.capabilities = build.spec.capabilities
        self.concurrency = build.spec.concurrency or 1

    async def decide(self, state, questions, *, options=None):
        Parity.calls += 1
        yes = state['i'] % 2 == 0
        if state['i'] >= 8:
            yes = not yes
        return Response(answers={qid: BooleanAnswer(probability=.99 if yes else .01) for qid in questions},
                        answered_by=self.id, latency_ms=10, retries=0,
                        usage=Usage(cost_usd=.01, cost_source='billed'))


TRUTH = BoxEdges(top=0.1, bottom=0.5, left=0.2, right=0.6)


class CompareFake:
    """Reads state["truth"] for any question type: "good" right, "bad" wrong; "choice-none" and "box-none" leave out
    the distribution or the box confidence."""

    def __init__(self, build: ModelBuild, mode: str) -> None:
        self.id = f"wire:{build.spec.id}"
        self.capabilities = build.spec.capabilities
        self.concurrency = 2
        self.mode = mode

    async def decide(self, state: dict[str, Any], questions: dict[str, Any], *, options: dict[str, Any] | None = None) -> Response:
        answer: dict[str, Any] = {}
        truth = bool(state.get("truth", False))
        for qid, question in questions.items():
            if question.type == "boolean":
                probability = 0.9 if truth else 0.1
                if self.mode == "bad":
                    probability = 1 - probability
                answer[qid] = BooleanAnswer(probability=probability)
            elif question.type == "choice":
                choice = "a" if truth else "b"
                if self.mode == "bad":
                    choice = "b" if truth else "a"
                probabilities = None if self.mode == "choice-none" else {"a": 0.9 if choice == "a" else 0.1, "b": 0.9 if choice == "b" else 0.1}
                answer[qid] = ChoiceAnswer(choice=choice, probabilities=probabilities)
            else:
                answer[qid] = BoxAnswer(box=TRUTH, confidence=None if self.mode == "box-none" else 0.8)
        return Response(answers=answer, answered_by=self.id, usage=Usage(input_tokens=3, cost_usd=0.01, cost_source="billed"), latency_ms=4, retries=0)


def compare_fake(mode: str) -> Callable[[ModelBuild], CompareFake]:
    return lambda build: CompareFake(build, mode)


def headline(t, evs):
    """The report's headline on these evaluations, ranked as report.render ranks them."""
    from s1flow.eval import report

    return report.headline(t, evs, *report.compared(t, evs))
