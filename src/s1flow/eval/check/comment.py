"""The PR comment a check writes (`s1flow check --markdown`), found again by its marker."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..evaluation import cost_note
from ..objectives.declare import METRICS, Objective
from ..objectives.measure import BOOTSTRAP
from ..shown import pct, usd
from ..task import Task
from .paired import Diff

if TYPE_CHECKING:
    from . import CheckResult


def _num(o: Objective, x: float | None) -> str:
    if x is None:
        return "—"
    return pct(x, 1) if o.unit == "share" else f"{x:.3f}"


def _diff(o: Objective | None, d: Diff) -> str:
    lo, hi = d.interval
    if not np.isfinite(d.diff):
        return "—"
    if o is not None and o.unit != "share":
        return f"{d.diff:+.3f} [{lo:+.3f}, {hi:+.3f}]"
    return f"{100 * d.diff:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]"


MARKER = "<!-- s1flow-check:{task} -->"


def error_markdown(task_id: str, message: str) -> str:
    return "\n".join([MARKER.format(task=task_id), f"### s1flow check · {task_id}: ⚠️ could not run", "", f"- {message}"]) + "\n"


def markdown(task: Task, r: CheckResult) -> str:
    o0 = task.primary
    if r.verdict == "pending":
        return "\n".join([MARKER.format(task=task.id), f"### s1flow check · {task.id}: ⏸ pending", "", *[f"- {x}" for x in r.reasons + r.notes]]) + "\n"
    head = {"fail": "❌ fail", "better": "✅ pass (better)", "no_difference": "✅ pass (no difference shown)", "pass": "✅ pass"}[r.verdict]
    sides = r.sides
    two = len(sides) == 2
    L = [MARKER.format(task=task.id), f"### s1flow check · {task.id}: {head}", ""]
    what = " and ".join(f"**{s.name}** ({s.policy}, {s.model}" + (f"/{s.variant}" if s.variant not in ("base", None) else "") + ")" for s in reversed(sides))
    L.append(f"Asked {what} again about today's {r.n} test cases and compared them." if two else f"Checked {what} on today's {r.n} test cases.")
    L.append("")
    L += [f"- {x}" for x in r.reasons]
    if r.reasons:
        L.append("")
    L += ["| | " + " | ".join(s.name for s in sides) + (" | difference [95% interval] |" if two else " |"), "|---|" + "---|" * (len(sides) + two)]
    d = r.diff
    # the rows every check shows, by the measure they are; the primary takes the row that measures the same
    fixed: list[tuple[str | None, str, list[str], str]] = [
        ("coverage", "sure share", [f"{pct(s.coverage, 1)} ({s.sure})" for s in sides], _diff(None, d.coverage) if d else ""),
        (None, "sure accuracy", [f"{pct(s.sure_accuracy, 1)} ({s.sure_errors} wrong)" for s in sides], _diff(None, d.sure_accuracy) if d else ""),
        ("accuracy", METRICS["accuracy"].label, [pct(s.accuracy, 1) for s in sides], _diff(None, d.accuracy) if d else ""),
    ]
    rows: list[tuple[str, list[str], str]] = []
    if o0.name not in {name for name, *_ in fixed}:
        rows.append((f"**{o0.label}**", [_num(o0, s.objectives[0]) for s in sides], _diff(o0, d.primary) if d else ""))
    rows += [(f"**{o0.label}**" if name == o0.name else label, cells, diff) for name, label, cells, diff in fixed]
    for label, cells, diff in rows:
        L.append(f"| {label} | " + " | ".join(cells) + (f" | {diff} |" if two else " |"))
    # what the calls took, apart from what was measured on the answers
    L += ["", "| calls | " + " | ".join(s.name for s in sides) + " |", "|---|" + "---|" * len(sides),
          "| API cost per 10k | " + " | ".join(usd(s.cost_per_10k_usd, 2) for s in sides) + " |",
          "| calls (cached) | " + " | ".join(f"{s.calls} ({s.cached})" for s in sides) + " |", ""]
    L += [f"- {x}" for x in r.notes]
    if note := cost_note([(s.name, s.cost_source, None, s.cost_unknown) for s in sides]):
        L.append(f"- {note}")
    L.append(f"- Target accuracy {pct(r.target_accuracy)}. The differences are a paired bootstrap ({BOOTSTRAP} resamples); an interval across 0 shows no difference at this many cases.")
    return "\n".join(L) + "\n"
