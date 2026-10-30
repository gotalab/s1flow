"""What a task optimizes and what it may not exceed, as declarations: the one shape that choosing,
optimizing, checking in CI and measuring in production read, kept as is in a policy's evidence.
pydantic only; what a value is on a set of answers is eval/objectives/measure.py's (`MEASURES`).

    Coverage(target_accuracy=0.95)   # Objective(name="coverage", params={"target_accuracy": 0.95}, ...)

A task names one `objective` (the only one that decides how a policy reads its answers) and, in `tiebreak`, more
objectives, in order, for the candidates it cannot tell apart. Objectives are never summed with weights (there
is no basis for the weights): a model is chosen on the objective among those that meet the constraints, and
only models whose intervals overlap the best are compared on `tiebreak`, in its order. `tiebreak`'s objectives are
measured at the rule the objective sets, the one a policy reads with; they choose none of their own.

Everything here is measured on the answers. What the calls took (latency, API cost) is never an objective: it is
read from the call records (Evaluation.calls) in two places only, the limits a model must stay within
(`Constraints`) and `tiebreak`'s "latency" and "cost", where it lists them (eval/select.py).

| objective                   | value                                                    | kind     | sets            | direction | constraint                         |
|-----------------------------|----------------------------------------------------------|----------|-----------------|-----------|------------------------------------|
| `Accuracy()`                | 1 when right (a failed call is 0)                        | per case | threshold (binary) | max    | —                                  |
| `Coverage(target_accuracy)` | 1 when not `unsure`                                      | per case | min_probability | max       | accuracy of the sure >= target     |
| `Recall(max_false_alarm)`   | share of the positives read True                         | set      | threshold       | max       | false alarms <= max                |
| `ExpectedLoss(fn, fp)`      | fn for a miss, fp for a false alarm                      | per case | threshold       | min       | —                                  |
| `AUROC()`                   | does the probability put right answers first             | set      | —               | max       | —                                  |
| `F1()`                      | F1 of the positive (binary)                              | set      | threshold       | max       | —                                  |
| `MacroF1()`                 | the mean F1 over a choice's options                      | set      | —               | max       | —                                  |
| `Loss(default, losses, unsure)` | the table's loss for the answer given on the label  | per case | see below       | min       | —                                  |

`Loss` is a table of what each answer loses on each label (0 when right); `Accuracy` (every error 1, read
as 1 - the mean loss) and `ExpectedLoss` (a miss fn, a false alarm fp) are fixed forms of it, measured by the
same code. It chooses a min probability when it sets an `unsure` loss (an unsure answer loses that), else a
binary question's threshold, and nothing for a choice. On a binary question every objective that reads the answer
chooses the threshold it is read at: 0.5 is no better a cut than any other, so it is chosen on the data. A custom objective (@per_case / @on_set,
objectives/custom.py) is an `Objective` with its source's sha256.

Every value is measured out of fold (a rule is chosen on the fit side) and carries a 95% bootstrap
interval. Only the built-ins hold a constraint.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from ...core.errors import ConfigError
from ..kinds import BooleanKind, ChoiceKind, Kind
from ...policies.rule import RuleField


class Objective(BaseModel):
    """One objective. Everything that changes its value is in `params`; `sets` is the Rule field it
    chooses (None: it reads the plain answer)."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    name: str  # "coverage", "expected_loss", or a custom one (objectives/custom.py)
    params: dict[str, JsonValue] = {}
    direction: Literal["max", "min"]
    sets: RuleField | None
    unit: Literal["share", "number"]  # how a value is shown
    label: str
    code_sha256: str | None = None  # a custom objective only

    @property
    def maximize(self) -> bool:
        return self.direction == "max"

    @property
    def key(self) -> str:
        """The name and params: two objectives with the same key are the same objective."""
        return self.name + json.dumps(self.params, sort_keys=True)


def _share(name: str, x: float, *, top: bool) -> float:
    if not (0 < x < 1 or (top and x == 1)):
        raise ConfigError(f"{name} is a share in (0, 1{']' if top else ')'}, got {x!r}")
    return float(x)


def Coverage(target_accuracy: float = 0.95) -> Objective:
    """The share answered sure, most probable first, while the sure share keeps `target_accuracy`."""
    t = _share("target_accuracy", target_accuracy, top=True)
    return Objective(name="coverage", params={"target_accuracy": t}, direction="max", sets="min_probability", unit="share",
                     label=f"coverage at {100 * t:.0f}% accuracy")


def Recall(max_false_alarm: float) -> Objective:
    """The positives caught while the false alarms stay at `max_false_alarm` of the negatives."""
    m = _share("max_false_alarm", max_false_alarm, top=False)
    return Objective(name="recall", params={"max_false_alarm": m}, direction="max", sets="threshold", unit="share",
                     label=f"recall at {100 * m:g}% false alarms or fewer")


def ExpectedLoss(fn: float = 1.0, fp: float = 1.0) -> Objective:
    """(fn x misses + fp x false alarms) per case: lower is better."""
    if fn < 0 or fp < 0:
        raise ConfigError(f"losses are 0 or more, got fn={fn!r}, fp={fp!r}")
    return Objective(name="expected_loss", params={"fn": float(fn), "fp": float(fp)}, direction="min", sets="threshold", unit="number",
                     label=f"loss per case (miss {fn:g}, false alarm {fp:g})")


def AUROC() -> Objective:
    return Objective(name="auroc", direction="max", sets=None, unit="number", label="AUROC")


def Accuracy() -> Objective:
    return Objective(name="accuracy", direction="max", sets=None, unit="share", label="accuracy (all)")


def F1() -> Objective:
    """F1 of the positive (2 x hits / (positives + cases read positive)), at the P(positive) threshold it chooses."""
    return Objective(name="f1", direction="max", sets="threshold", unit="number", label="F1")


def MacroF1() -> Objective:
    return Objective(name="macro_f1", direction="max", sets=None, unit="number", label="macro-F1")


def Loss(default: float = 1.0, losses: dict[str, dict[str, float]] | None = None, unsure: float | None = None) -> Objective:
    """The mean loss per case of a table: `losses[label][answer]` (a choice's options, or "true" / "false" for a
    binary question), `default` for every other error, 0 when right. A failed call loses `unsure`, else the most
    its label's row loses. With `unsure`, an answer under the min probability it chooses loses that instead."""
    numbers = [default, *(c for row in (losses or {}).values() for c in row.values()), *([] if unsure is None else [unsure])]
    if any(not isinstance(c, (int, float)) or isinstance(c, bool) or c < 0 for c in numbers):
        raise ConfigError(f"losses are numbers, 0 or more: got {numbers!r}")
    params: dict[str, JsonValue] = {
        "default": float(default), "losses": {str(t): {str(a): float(c) for a, c in row.items()} for t, row in (losses or {}).items()},
        "unsure": None if unsure is None else float(unsure),
    }
    label = "loss per case (table" + ("" if unsure is None else f", unsure {unsure:g}") + ")"
    # sets: a min probability with unsure; else a binary question's threshold, nothing for a choice (fitted())
    return Objective(name="loss", params=params, direction="min", sets="threshold" if unsure is None else "min_probability",
                     unit="number", label=label)


BUILT_IN: dict[str, Callable[..., Objective]] = {
    "coverage": Coverage, "recall": Recall, "expected_loss": ExpectedLoss, "auroc": AUROC, "accuracy": Accuracy, "f1": F1, "macro_f1": MacroF1,
    "loss": Loss,
}


class Constraints(BaseModel):
    """Limits a model must stay within to be chosen at all: two on its calls (latency, API cost per 10,000 cases,
    Evaluation.calls), one on its labels, and two floors on what a binary question reads positive. The P(positive)
    threshold the objective sets is chosen among those that keep the floors; a model that no threshold lets keep them
    on the dev cases is not chosen (a floor is never relaxed to find one)."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    latency_p99_ms: float | None = Field(default=None, gt=0)
    cost_per_10k_usd: float | None = Field(default=None, ge=0)
    min_labels: int | None = Field(default=None, gt=0)  # fewer labelled cases than this: not enough to decide
    min_precision: float | None = Field(default=None, gt=0, le=1)  # of the cases read positive, the share that are
    min_recall: float | None = Field(default=None, gt=0, le=1)  # of the positive cases, the share read positive

    @property
    def floors(self) -> dict[str, float]:
        """The floors set, by name."""
        return {k: v for k, v in (("precision", self.min_precision), ("recall", self.min_recall)) if v is not None}


def default_for(kind: Kind) -> Objective | None:
    """The kind's default objective (the first it takes); None when s1flow has no such objective yet."""
    make = BUILT_IN.get(kind.objectives[0]) if kind.objectives else None
    return None if make is None else make()


def reweighted(o: Objective, factor: float) -> Objective | None:
    """The objective with its weights moved by `factor` against the rest, to see whether they make the choice:
    ExpectedLoss's miss against its false alarm; a loss table's listed cells against its default (or, with none
    listed, its default against `unsure`). None for an objective with no weights to move."""
    p = o.params
    if o.name == "expected_loss":
        return ExpectedLoss(fn=cast(float, p["fn"]) * factor, fp=cast(float, p["fp"]))
    if o.name == "loss":
        rows = cast(dict[str, dict[str, float]], p["losses"])
        unsure = cast(float | None, p["unsure"])
        if rows:
            return Loss(cast(float, p["default"]), {t: {a: c * factor for a, c in row.items()} for t, row in rows.items()}, unsure)
        if unsure is not None:
            return Loss(cast(float, p["default"]) * factor, None, unsure)
    return None


def fitted(o: Any, kind: Kind) -> Any:
    """A declaration as it reads this kind's answers: Accuracy and a loss table without `unsure` choose a binary
    question's threshold and nothing on a choice. Anything else as it is."""
    if isinstance(o, Objective) and o.code_sha256 is None and (o.name == "accuracy" or (o.name == "loss" and o.params.get("unsure") is None)):
        return o.model_copy(update={"sets": "threshold" if kind.binary else None})
    return o


def _table_keys(o: Objective, kind: Kind, where: str) -> None:
    keys = ["true", "false"] if kind.binary else kind.options
    rows = cast(dict[str, dict[str, Any]], o.params.get("losses") or {})
    if bad := sorted({k for t, row in rows.items() for k in (t, *row) if k not in keys}):
        raise ConfigError(f"{where}: the loss table names {', '.join(map(repr, bad))}, which {'is' if len(bad) == 1 else 'are'} not an answer "
                          f"({', '.join(keys)})")
    if right := [t for t, row in rows.items() if row.get(t)]:
        raise ConfigError(f"{where}: the loss table charges a right answer ({', '.join(right)}); a right answer loses 0")


CallKey = Literal["latency", "cost"]
CALL_KEYS: tuple[CallKey, ...] = ("latency", "cost")  # what the calls took, as `tiebreak` may name it (eval/select.py)


def check(objective: Any, tiebreak: list[Any], kind: Kind, where: str, custom: frozenset[str] = frozenset()) -> None:
    """What a task.py may declare, refused when it loads (`where`: the task; `custom`: the keys of its custom objectives,
    objectives/custom.py)."""
    allowed = ", ".join(k for k in kind.objectives if k in BUILT_IN)
    if not isinstance(objective, Objective):
        raise ConfigError(f"{where}: objective= is one objective (Coverage(...), Accuracy(), ...), got {type(objective).__name__}")
    calls = [x for x in tiebreak if isinstance(x, str)]
    if bad := next((x for x in calls if x not in CALL_KEYS), None):
        raise ConfigError(f"{where}: tiebreak= takes objectives and {' and '.join(map(repr, CALL_KEYS))}, got {bad!r}")
    if dup := next((x for x in CALL_KEYS if calls.count(x) > 1), None):
        raise ConfigError(f"{where}: {dup!r} is listed twice in tiebreak=")
    tiebreak = [x for x in tiebreak if not isinstance(x, str)]
    if bad := next((x for x in tiebreak if not isinstance(x, Objective)), None):
        raise ConfigError(f"{where}: tiebreak= lists objectives (Accuracy(), MacroF1(), ...) and \"latency\" / \"cost\", got {type(bad).__name__}; "
                          "latency and API cost limit candidates as constraints= (latency_p99_ms, cost_per_10k_usd)")
    seen: set[str] = set()
    if objective.sets != "min_probability" and (c := next((x for x in tiebreak if x.name == "coverage"), None)):
        raise ConfigError(f"{where}: {c.label} in tiebreak=: coverage decides min_probability, so it only ranks as the objective; "
                          f"as tiebreak it is read at {objective.name}'s rule, which sets no min probability, and is 1.0 for every candidate")
    for o in [objective, *tiebreak]:
        if o.code_sha256 is not None:  # a custom one: its function measures it
            if o.key not in custom:
                raise ConfigError(f"{where}: {o.name} carries a code hash but no function; declare it with @per_case or @on_set "
                                  "in task.py (s1flow.objectives) and call it")
            if o.sets is not None and o.sets not in kind.sets:
                raise ConfigError(f"{where}: {o.name} sets a {o.sets}, which a {kind.type} question is not read by ({', '.join(sorted(kind.sets))})")
            if o.key in seen:
                raise ConfigError(f"{where}: {o.label} is listed twice")
            seen.add(o.key)
            continue
        make = BUILT_IN.get(o.name)
        if make is None:
            raise ConfigError(f"{where}: no objective named {o.name!r}; the built-ins are {', '.join(BUILT_IN)}")
        try:
            same = fitted(make(**o.params), kind) == o
        except (TypeError, ConfigError):
            same = False
        if not same:
            raise ConfigError(f"{where}: {o.name} is a built-in objective; declare it with its function ({make.__name__}(...)), not by hand")
        if o.name not in kind.objectives:
            binary = o.name in BooleanKind.objectives and o.name not in ChoiceKind.objectives  # recall, expected_loss
            need = "needs a binary question (boolean, or a choice with positive)" if binary else f"does not apply to a {kind.type} question"
            raise ConfigError(f"{where}: {o.name} {need}; a {kind.type} takes {allowed}")
        if o.sets is not None and o.sets not in kind.sets:
            raise ConfigError(f"{where}: {o.name} sets a {o.sets}, which a {kind.type} question is not read by ({', '.join(sorted(kind.sets))})")
        if o.name == "loss":
            _table_keys(o, kind, where)
        if o.key in seen:
            raise ConfigError(f"{where}: {o.label} is listed twice")
        seen.add(o.key)
