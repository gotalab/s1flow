"""Custom objectives: a function in task.py, measured like a built-in (out of fold, an interval, the
test share, check), on each label and the `Reading` of its answers.

    @per_case(direction="min", sets="threshold")
    def wake_loss(label: bool, reading: Reading | None, *, miss: float = 20.0) -> float:   # one case's value; the set's is the mean
        ...

    @on_set(direction="max")
    def my_f2(labels: list, readings: list[Reading | None], *, beta: float = 2.0) -> float | None:
        ...

    task = Task(..., objective=wake_loss(miss=20))

Calling the function with its params gives a `Custom`: the declaration (an `Objective` named after the function,
every param with its value, defaults included, and the sha256 of its source) and what measures it. `Task`
keeps the two apart: a policy's evidence holds the declaration alone, production never runs the function,
and nothing is registered globally. A reading is None where the call failed. No constraint: a built-in holds
one, a custom one does not (yet).
"""

from __future__ import annotations

import hashlib
import inspect
import json
import textwrap
from dataclasses import dataclass
from typing import Any, Callable, Literal, get_args

import numpy as np

from ...core.errors import ConfigError
from ...policies.kinds import Reading
from ...policies.rule import RuleField
from .declare import BUILT_IN, Objective
from .measure import Measure, Pairs

Shape = Literal["per_case", "on_set"]
RESERVED = {*BUILT_IN, "latency", "cost"}


@dataclass(frozen=True)
class Custom:
    """A custom objective, called with its params: the declaration and what measures it."""

    objective: Objective
    measure: Measure


def readings(p: Pairs) -> list[Reading | None]:
    """The cases' readings as the function receives them (None: the call failed)."""
    binary, choice = p.measured == "boolean", p.distribution is not None
    out: list[Reading | None] = []
    for i in range(len(p)):
        if not p.ok[i]:
            out.append(None)
            continue
        v = p.value[i]
        out.append(Reading.model_construct(
            value=bool(v) if isinstance(v, (bool, np.bool_)) else v, probability=float(p.probability[i]), below_min_probability=bool(p.unsure[i]) if p.min_probability_set[i] else None,
            p_positive=float(p.p_positive[i]) if binary else None,
            distribution=[float(x) for x in p.distribution[i]] if choice and p.distribution is not None else None,
            expected=None, confidence=float(p.confidence[i]) if p.measured == "box" else None,
        ))
    return out


def _label(y: Any) -> Any:
    return bool(y) if isinstance(y, (bool, np.bool_)) else y


class Declared:
    """A function declared with @per_case or @on_set: call it with its params for a `Custom`."""

    def __init__(self, fn: Callable[..., Any], shape: Shape, direction: Any, sets: Any, unit: str, label: str | None):
        self.fn, self.shape = fn, shape
        self.where = f"{inspect.getsourcefile(fn) or '?'}: {fn.__name__}"
        if direction not in ("max", "min") or (sets is not None and sets not in get_args(RuleField)):
            raise ConfigError(f"{self.where}: @{shape} needs direction= (max or min), and sets= min_probability or threshold when it "
                              f"chooses one (left out: it reads the plain answer), got direction={direction!r}, sets={sets!r}")
        if fn.__name__ in RESERVED:
            raise ConfigError(f"{self.where}: {fn.__name__} is a built-in's name; name your own objective otherwise")
        if unit not in ("share", "number"):
            raise ConfigError(f"{self.where}: unit= is share or number, got {unit!r} (latency and API cost are measured on the calls, never as an objective; constraints= limits them)")
        self.direction, self.sets, self.unit, self.label = direction, sets, unit, label or fn.__name__
        self.defaults = self._params()
        self.code_sha256 = hashlib.sha256(textwrap.dedent(inspect.getsource(fn)).encode()).hexdigest()

    def _params(self) -> dict[str, Any]:
        """The params after the two the function measures with: each with a default (the value kept in the
        evidence) and a type annotation."""
        what = "label and reading" if self.shape == "per_case" else "labels and readings"
        ps = list(inspect.signature(self.fn).parameters.values())
        first = [x for x in ps[:2] if x.kind in (x.POSITIONAL_ONLY, x.POSITIONAL_OR_KEYWORD) and x.default is x.empty]
        if len(first) != 2 or any(x.kind in (x.VAR_POSITIONAL, x.VAR_KEYWORD) for x in ps) or any(x.default is x.empty for x in ps[2:]):
            raise ConfigError(f"{self.where}: an objective takes two arguments, the {what}, then its params with defaults "
                              f"(def {self.fn.__name__}({'label, reading' if self.shape == 'per_case' else 'labels, readings'}, *, weight: float = 1.0))")
        out = {}
        for x in ps[2:]:
            if x.annotation is x.empty:
                raise ConfigError(f"{self.where}: param {x.name} needs a type annotation")
            out[x.name] = self._json(x.name, x.default)
        return out

    def _json(self, name: str, value: Any) -> Any:
        try:
            return json.loads(json.dumps(value))
        except (TypeError, ValueError):
            raise ConfigError(f"{self.where}: param {name} = {value!r} is not JSON: the evidence keeps every param's value") from None

    def __call__(self, **given: Any) -> Custom:
        if unknown := sorted(set(given) - set(self.defaults)):
            raise ConfigError(f"{self.where}: no param {', '.join(unknown)}; it takes {', '.join(self.defaults) or 'none'}")
        params = {**self.defaults, **{k: self._json(k, v) for k, v in given.items()}}
        o = Objective(name=self.fn.__name__, params=params, direction=self.direction, sets=self.sets, unit=self.unit,  # type: ignore[arg-type]
                      label=self.label, code_sha256=self.code_sha256)
        return Custom(objective=o, measure=Measure(self._per_case(params) if self.shape == "per_case" else self._on_set(params)))

    def _per_case(self, params: dict[str, Any]) -> Callable[[Pairs, Any], float | None]:
        fn, seen = self.fn, {}  # a case's value depends on its label and reading alone: computed once per distinct case

        def value(p: Pairs, _: Any) -> float | None:
            if not len(p):
                return None
            total = 0.0
            for y, r in zip(p.y, readings(p)):
                key = (repr(y), None if r is None else tuple(r.__dict__.values()).__repr__())
                if key not in seen:
                    seen[key] = float(fn(_label(y), r, **params))
                total += seen[key]
            return total / len(p)

        return value

    def _on_set(self, params: dict[str, Any]) -> Callable[[Pairs, Any], float | None]:
        fn = self.fn

        def value(p: Pairs, _: Any) -> float | None:
            if not len(p):
                return None
            v = fn([_label(y) for y in p.y], readings(p), **params)
            return None if v is None else float(v)

        return value


def per_case(*, direction: Any = None, sets: Any = None, unit: str = "number", label: str | None = None) -> Callable[[Callable[..., Any]], Declared]:
    """A custom objective from one case's label and reading: the set's value is the mean over its cases."""
    return lambda fn: Declared(fn, "per_case", direction, sets, unit, label)


def on_set(*, direction: Any = None, sets: Any = None, unit: str = "number", label: str | None = None) -> Callable[[Callable[..., Any]], Declared]:
    """A custom objective from all the cases' labels and readings at once (None: no value on these cases)."""
    return lambda fn: Declared(fn, "on_set", direction, sets, unit, label)
