"""Optimizers: what `s1flow optimize` runs to write a new question for a model. task.py names one:

    optimizer=Gepa(budget=300)     an object (here the built-in GEPA's settings; any object with `name`,
                                   `settings()` and `run(problem)` will do)
    optimizer="gepa"               a name: the built-in GEPA with its defaults, or an entry point in the
                                   `s1flow.optimizers` group, a factory called with no arguments

s1flow gives it the problem (eval/optimize.py): the task, the model, the question to start from, and the train
and val cases of the task's fixed split. The test share is not in the problem's cases (the task object can still
read every case: an optimizer installed from a package runs with the access task.py itself has). It returns what it found: the question,
the model calls it made, what it spent beside them, and what only it records (`detail`). s1flow writes the record
(task.Optimized) the same way for every optimizer, then asks the new question about every case.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from importlib.metadata import entry_points
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from ..client.questions import Question
from ..core.errors import ConfigError

if TYPE_CHECKING:
    from .cases import Case
    from .task import Task

GROUP = "s1flow.optimizers"


@dataclass(frozen=True)
class Problem:
    """What an optimizer is given."""

    task: Task
    model: str  # the model the question is written for: a name of s1flow.toml, model[:version]
    start: Question  # the question it begins from
    train: list[Case]  # cases to learn from
    val: list[Case]  # cases to select on; the test share is in neither


@dataclass
class Found:
    """What an optimizer returns."""

    question: Question
    model_calls: int  # calls to `model` (cached answers count too)
    cost_usd: float | None = None  # what it spent beside the model's calls (a reflection LM); None: not priced
    detail: dict[str, Any] = field(default_factory=dict)  # what only this optimizer records


@runtime_checkable
class Optimizer(Protocol):
    @property
    def name(self) -> str:
        """What the record calls it."""
        ...

    def settings(self) -> dict[str, Any]:
        """What it was set to, as JSON: kept in the record."""
        ...

    def run(self, problem: Problem) -> Found: ...


@dataclass(frozen=True)
class Gepa:
    """The built-in optimizer: GEPA (eval/gepa.py, install s1flow[optimize]) rewrites the question from the
    model's mistakes on train, read by a reflection LM, and keeps the best on val."""

    budget: int = 300  # model calls on train and val
    reflection: str | None = None  # an `llm` model of s1flow.toml; None: gpt-6.1-sol on OpenAI's API (OPENAI_API_KEY)
    patience: int | None = None  # stop after this many proposals without a new best on val
    max_cost: float | None = None  # stop once the reflection LM has cost this much (USD, list price)
    merge: bool = False  # let GEPA combine candidates that won on different cases
    minibatch: int = 8  # train cases the reflection LM reads per proposal
    seed: int = 1
    name: str = field(default="gepa", init=False)

    def settings(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if k != "name"}

    def run(self, problem: Problem) -> Found:
        from . import gepa  # needs s1flow[optimize]

        return gepa.run(problem, self)


def resolve(optimizer: Optimizer | str) -> Optimizer:
    """task.py's `optimizer`: an object as it is; a name, the built-in or an entry point's factory."""
    if not isinstance(optimizer, str):
        if isinstance(optimizer, type) or not isinstance(optimizer, Optimizer):  # Gepa, not Gepa(): the class itself
            raise ConfigError(f"optimizer={optimizer!r}: an optimizer has `name`, `settings()` and `run(problem)`")
        return optimizer
    if optimizer == "gepa":
        return Gepa()
    found = entry_points(group=GROUP, name=optimizer)
    if not found:
        known = sorted({"gepa", *(e.name for e in entry_points(group=GROUP))})
        raise ConfigError(f"no optimizer {optimizer!r}; known: {', '.join(known)} (a package adds one under the {GROUP} entry point group)")
    try:
        made = next(iter(found)).load()()
    except Exception as e:  # a third-party factory: whatever it raises (an import, a bad target) is its package's
        raise ConfigError(f"the {optimizer!r} optimizer ({GROUP} entry point) failed to load: {type(e).__name__}: {e}") from None
    if isinstance(made, type) or not isinstance(made, Optimizer):
        raise ConfigError(f"the {optimizer!r} entry point made {made!r}, which has no `name`, `settings()` and `run(problem)`")
    return made
