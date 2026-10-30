"""Tasks: one task is one decision. `tasks/<id>/task.py` defines `task`: what it asks, how its rows become
states and labels, how it is split and what it optimizes. Its cases are read by eval/cases.py.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import marshal
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from ..client import images
from ..client.identity import digest
from ..client.questions import Question
from ..client.state import State
from ..core import place
from ..core.errors import ConfigError, invalid
from .kinds import Kind, KindParams, kind_of
from .candidate import variant_name
from .cases import Case, Cases, Row
from .objectives.declare import CallKey, Constraints, Objective, check, default_for, fitted
from .objectives.measure import Measure
from .objectives.custom import Custom
from .optimizers import Gepa, Optimizer

if TYPE_CHECKING:
    from ..project import Project
    from .policy import Store


def _evaluation_revision() -> str:
    """Editable installs must not certify measurements made by different evaluation code."""
    root = Path(__file__).parent
    return digest({str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in sorted(root.rglob("*.py"))})


EVALUATION_IMPLEMENTATION_REVISION = _evaluation_revision()


class Optimized(BaseModel):
    """tasks/<id>/optimized/<variant>.json: a question an optimizer wrote (eval/optimizers.py), the same for every
    optimizer: what it was given and set to, what it cost; what only it records is in `detail`."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/optimized@2"] = Field(default="s1flow/optimized@2", alias="schema")
    variant: str
    model: str  # the model it was optimized for
    optimizer: str  # its name: gepa, or an entry point's
    settings: dict[str, Any]  # what it was set to
    at: str
    question: Question
    seed_question: Question
    start: str = "base"  # the question it began from
    split: dict[Literal["train", "val", "test"], list[str]]  # the cases it read from, selected on, never saw
    model_calls: int
    cost_usd: float | None  # what it spent beside the model's calls (a reflection LM); None: not priced
    detail: dict[str, Any] = {}  # what only this optimizer records

    @classmethod
    def read(cls, text: str) -> Optimized:
        """A record of either schema, as @2."""
        import json

        try:
            data = json.loads(text)
        except ValueError:
            return cls.model_validate_json(text)  # malformed: pydantic says where, as a ValidationError
        if isinstance(data, dict) and data.get("schema") == "s1flow/optimized@1":
            return OptimizedV1.model_validate_json(text).upgrade()
        return cls.model_validate_json(text)


class OptimizedV1(BaseModel):
    """tasks/<id>/optimized/<variant>.json before optimizers were pluggable: GEPA's alone. Read only."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/optimized@1"] = Field(default="s1flow/optimized@1", alias="schema")
    variant: str
    model: str  # the model it was optimized for
    surrogate: str = "0.5 * correctness + 0.5 * (1 - per-case Brier); prompt-only search"
    method: Literal["gepa"]
    at: str
    question: Question
    seed_question: Question
    start: str = "base"  # the question it began from
    context: str | None = None  # the team's criteria file shown to the reflection LM
    rationales: int | None = None  # train / val cases with a rationale
    split: dict[Literal["train", "val", "test"], list[str]]  # the cases GEPA read from, selected on, never saw
    seed: int
    budget: int
    merge: bool = False
    patience: int | None = None
    max_cost: float | None = None
    reflection_lm: str
    reflection_calls: int
    reflection_cost_usd: float | None  # None: the reflection LM was not priced
    model_calls: int
    candidates: int
    val_scores: list[float]
    best_index: int

    def upgrade(self) -> Optimized:
        return Optimized(
            variant=self.variant, model=self.model, optimizer="gepa", at=self.at, question=self.question,
            seed_question=self.seed_question, start=self.start, split=self.split, model_calls=self.model_calls,
            cost_usd=self.reflection_cost_usd,
            settings={"budget": self.budget, "reflection": self.reflection_lm, "patience": self.patience,
                      "max_cost": self.max_cost, "merge": self.merge, "seed": self.seed},
            detail={"surrogate": self.surrogate, "context": self.context, "rationales": self.rationales,
                    "reflection_calls": self.reflection_calls, "candidates": self.candidates,
                    "val_scores": self.val_scores, "best_index": self.best_index},
        )


@dataclass
class Split:
    """The test share held out (evalset.py), and the cross-validation over the rest, chosen by its size (split.py)."""

    test: float = 0.3  # the share of the labelled cases held out as test, stratified by label (evalset.py)
    k: int = 5
    seed: int = 1

    def __post_init__(self) -> None:
        if not (isinstance(self.test, float) and 0 < self.test < 1):
            raise ConfigError(f"Split(test={self.test!r}): the share held out as test is a number between 0 and 1, such as 0.3")


@dataclass
class Task:
    id: str
    cases: str  # the file of its cases, relative to the task dir; .json (array) or .jsonl
    state: Callable[[Row], State]
    question: Question
    label: Callable[[Row], Any]  # None excludes the row from scoring
    question_id: str = "q"
    # What the question's type leaves open (policies/kinds.py), kept as it is in a policy: KindParams(positive="wake")
    # scores a choice as binary, P(positive) against a true / false label; KindParams(iou=0.7) is a box's bar for a hit.
    kind_params: KindParams = field(default_factory=KindParams)
    split: Split = field(default_factory=Split)
    # What the task optimizes: `objective` (it alone decides how a policy reads its answers; None: the kind's
    # default, Accuracy for a boolean, choice or box question), and `tiebreak`, what orders the candidates it cannot
    # tell apart, in order: more objectives (eval/objectives/declare.py), "latency" (p90 per case) and "cost" (API
    # cost per 10,000 cases) (eval/select.py). With no tiebreak, the candidates it cannot tell apart are listed
    # unordered. A custom objective (@per_case / @on_set, called with its params) goes in either.
    # Both are kept as declared; `objectives` holds the objectives they resolve to, `ties` the tiebreak resolved,
    # and `custom` the custom ones' functions.
    objective: Objective | Custom | None = None
    tiebreak: list[Objective | Custom | CallKey] = field(default_factory=list)
    constraints: Constraints = field(default_factory=Constraints)  # what a model may not exceed
    # What `s1flow optimize` runs (eval/optimizers.py): Gepa(...) with its settings, an optimizer object, or the
    # name of one (an entry point in the s1flow.optimizers group).
    optimizer: Optimizer | str = field(default_factory=Gepa)
    variants: dict[str, Question] = field(default_factory=dict)
    source: str = ""  # where the data comes from, with its license
    show: Callable[[Row], str] | None = None  # one line per case in reports
    dir: Path = Path()
    optimized: dict[str, Optimized] = field(default_factory=dict)  # tasks/<id>/optimized/*.json, by variant
    project: Project | None = field(default=None, repr=False)
    _cases: Cases | None = field(default=None, init=False, repr=False)
    custom: dict[str, Custom] = field(default_factory=dict, init=False, repr=False)  # the task's custom objectives, by key
    objectives: list[Objective] = field(default_factory=list, init=False, repr=False)  # the objective, then those in `tiebreak`
    ties: list[Objective | CallKey] = field(default_factory=list, init=False, repr=False)  # `tiebreak` resolved, in order

    def __post_init__(self) -> None:
        if why := place.task_id_error(self.id):
            raise ConfigError(why)
        try:
            kind = self.kind
        except ValueError as e:
            raise ConfigError(f"{self.id}: kind_params: {e}") from None
        default = default_for(kind)
        if default is None:
            raise ConfigError(f"{self.id}: {self.kind.type} questions are not evaluated yet (no metric scores them)")

        def declared(x: Any) -> Any:
            if isinstance(x, Custom):
                self.custom[x.objective.key] = x
                return x.objective
            return fitted(x, self.kind)

        for name in self.variants:
            variant_name(name)
        primary = declared(self.objective or default)
        self.ties = [x if isinstance(x, str) else declared(x) for x in self.tiebreak]
        check(primary, self.ties, self.kind, self.id, frozenset(self.custom))
        self.objectives = [primary, *(x for x in self.ties if isinstance(x, Objective))]
        if self.constraints.floors and not (self.kind.binary and self.primary.sets == "threshold"):
            raise ConfigError(f"{self.id}: min_precision and min_recall limit the P(positive) threshold, so they need a binary question "
                              f"and an objective that sets it (Accuracy, F1, ExpectedLoss, Recall); {self.primary.label} sets {self.primary.sets or 'none'}")

    @property
    def kind(self) -> Kind:
        """What the question's type means for labels, readings and objectives (policies/kinds.py)."""
        return kind_of(self.question, self.kind_params)

    @property
    def evaluation_contract_digest(self) -> str:
        """The current scoring and selection rules, apart from mutable test-use history."""
        from . import evalset

        split = evalset.current(self)
        lineup = self.project.lineup() if self.project is not None else None
        prices = {name: lineup.resolved(name).price for name in lineup.probe_names()} if lineup is not None else {}
        return digest({
            "implementation": EVALUATION_IMPLEMENTATION_REVISION,
            "question_id": self.question_id, "question": self.question, "variants": self.variants,
            "kind_params": self.kind_params, "objectives": self.objectives,
            "custom": {key: custom.objective for key, custom in self.custom.items()},
            "constraints": self.constraints, "declared_prices": prices,
            "split_config": {"test": self.split.test, "k": self.split.k, "seed": self.split.seed},
            "split": {"seed": split.seed, "test_share": split.test_share, "assign": split.assign},
            "ties": [x if isinstance(x, str) else x.key for x in self.ties],  # the tiebreak, in order
        })

    @property
    def data_digest(self) -> str:
        """Current source data and materialized model inputs, including referenced image bytes."""
        cases = self.load_cases()
        cases.forget()
        return digest({"source": cases.data_sha256(), "cases": [
            {"id": case.id, "state": self.model_state(case), "label": case.label}
            for case in cases.all()
        ]})

    @property
    def input_adapter_digest(self) -> str:
        """Identity of the input adapter's code; actual input bytes are request-hashed separately."""
        fn = inspect.unwrap(self.state)
        try:
            source = inspect.getsource(fn)
        except (OSError, TypeError):
            code = getattr(fn, "__code__", None)
            if code is not None:
                source = marshal.dumps(code).hex()
            else:
                try:
                    source = inspect.getsource(type(fn))
                except (OSError, TypeError):
                    raise ConfigError(f"{self.id}: cannot identify the input adapter's code") from None
        # Include the containing module to catch changes to its helper functions and constants.
        path = inspect.getsourcefile(fn)
        module_source = Path(path).read_text() if path and Path(path).is_file() else ""
        return digest({"module": getattr(fn, "__module__", type(fn).__module__),
                       "callable": getattr(fn, "__qualname__", type(fn).__qualname__),
                       "source": source, "module_source": module_source})

    @property
    def where(self) -> Project:
        if self.project is None:
            raise ConfigError(f"{self.id} was not loaded from a project (Project.task)")
        return self.project

    @property
    def policies(self) -> Store:
        """The project's policies, with their evidence (eval/policy.py)."""
        from .policy import store

        return store(self.where)

    @property
    def primary(self) -> Objective:
        return self.objectives[0]

    @property
    def custom_measures(self) -> dict[str, Measure]:
        """What measures the task's custom objectives, by key (measure.bound)."""
        return {k: x.measure for k, x in self.custom.items()}

    def copy(self, **changes: Any) -> Task:
        """The same task with some fields changed (another objective, tiebreak, constraints), the cases it read kept.
        A resolved custom objective passed back (one of `objectives`) is declared again with its function."""
        mine = lambda x: self.custom.get(x.key, x) if isinstance(x, Objective) else x  # noqa: E731
        if "objective" in changes:
            changes["objective"] = mine(changes["objective"])
        if "tiebreak" in changes:
            changes["tiebreak"] = [mine(x) for x in changes["tiebreak"]]
        out = replace(self, **changes)
        out._cases = self._cases
        return out

    @property
    def coverage_target(self) -> float:
        """The accuracy the table of sure answers keeps: the objective's, when it is Coverage, else 0.95."""
        return cast(float, self.primary.params["target_accuracy"]) if self.primary.name == "coverage" else 0.95

    @property
    def error_losses(self) -> tuple[float, float]:
        """(miss, false alarm) for the binary threshold table: the objective's or a `tiebreak` ExpectedLoss's, else 1 and 1."""
        return next(((cast(float, o.params["fn"]), cast(float, o.params["fp"])) for o in self.objectives if o.name == "expected_loss"), (1.0, 1.0))

    def questions(self, variant: str = "base") -> dict[str, Question]:
        q = self.question if variant == "base" else self.variants[variant]
        return {self.question_id: q}

    def add_optimized(self, art: Optimized) -> None:
        """A question an optimizer wrote, as one more variant."""
        variant_name(art.variant)
        self.optimized[art.variant] = art
        self.variants[art.variant] = art.question

    def model_state(self, case: Case) -> State:
        """The state a model receives: images loaded and prepared (client/images.materialize)."""
        return images.materialize(case.state, self.dir)

    def load_cases(self) -> Cases:
        """The task's cases (eval/cases.py): its rows, production's feedback, the corrections. Read once."""
        if self._cases is None or self._cases.state is not self.state or self._cases.label is not self.label:
            self._cases = Cases(self.id, self.dir, self.cases, self.state, self.label, self.show)
        return self._cases


def load(project: Project, task_id: str) -> Task:
    path = project.task_dir(task_id) / "task.py"
    spec = importlib.util.spec_from_file_location(f"s1flow_task_{path.parent.name}", path)
    if spec is None or spec.loader is None:
        raise ConfigError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        task: Task = module.task
    except ConfigError as e:
        raise ConfigError(f"{path}: {e}") from None
    except Exception as e:  # a task.py is user code: any error in it is a configuration error
        raise ConfigError(f"{path}: {type(e).__name__}: {e}") from e
    if task.id != path.parent.name:  # a task's directory is named its id, as runs/, reports/ and policies/ are
        raise ConfigError(f"{path}: id {task.id!r} does not match its directory tasks/{path.parent.name}: set id={path.parent.name!r}")
    task.dir = path.parent
    task.project = project
    for f in sorted((task.dir / "optimized").glob("*.json")):
        try:
            art = Optimized.read(f.read_text())
        except ValidationError as e:
            raise ConfigError(f"{f}: {invalid(e)}") from None
        task.add_optimized(art)
    return task
