"""Do the weights make the choice? With ExpectedLoss or a loss table as the objective, the candidates are
ranked again with its weights halved and doubled (declare.reweighted), from the answers already scored: no
call is made. When the candidates tied at the top change, the weights decide the choice, and they are the task
owner's to set (s1flow has no default for them). report shows it.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import metrics
from .objectives.declare import Objective, reweighted
from .select import Ranked, rank
from .task import Task

FACTORS = (0.5, 2.0)


@dataclass(frozen=True)
class Reweighted:
    factor: float
    objective: Objective  # the objective with its weights moved
    tied: list[str]  # the candidates the objective cannot tell from the best on it; empty: none within the constraints


def sensitivity(task: Task, preds: dict[str, metrics.Preds], variants: dict[str, str] | None = None) -> list[Reweighted]:
    """The candidates tied at the top with the primary objective's weights halved and doubled; empty when it has
    no weights to move. `preds`: each candidate's scored answers, by name; `variants`: each one's variant (base)."""
    out = []
    for f in FACTORS:
        o = reweighted(task.primary, f)
        if o is None:
            return []
        t = task.copy(objective=o)
        evs = [metrics.evaluate(t, pr, variant=(variants or {}).get(name, "base")) for name, pr in preds.items()]
        ranked = rank(t.primary, t.ties, t.constraints, evs)
        out.append(Reweighted(factor=f, objective=t.primary, tied=top(ranked)))
    return out


def top(ranked: list[Ranked]) -> list[str]:
    """The candidates the objective cannot tell from the best on it, by name."""
    return sorted(x.candidate for x in ranked if x.tied_with_best)


def decides(tied: list[str], moved: list[Reweighted]) -> bool:
    """Whether halving or doubling the weights changes the candidates tied at the top."""
    return any(r.tied != tied for r in moved)
