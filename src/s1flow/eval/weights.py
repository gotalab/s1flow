"""Do the weights make the choice? With ExpectedLoss or a loss table as the objective, the candidates are
ranked again with its weights halved and doubled (declare.reweighted), from the answers already scored: no
call is made. When the recommendation moves, the weights decide it, and they are the task owner's to set
(s1flow has no default for them). rank and report show it.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import metrics
from .objectives.declare import Objective, reweighted
from .select import rank
from .task import Task

FACTORS = (0.5, 2.0)


@dataclass(frozen=True)
class Reweighted:
    factor: float
    objective: Objective  # the objective with its weights moved
    recommended: str | None  # None: no candidate within the constraints
    tied: list[str]


def sensitivity(task: Task, preds: dict[str, metrics.Preds], variants: dict[str, str] | None = None) -> list[Reweighted]:
    """The recommendation and the tie with the primary objective's weights halved and doubled; empty when it has
    no weights to move. `preds`: each candidate's scored answers, by name; `variants`: each one's variant (base)."""
    out = []
    for f in FACTORS:
        o = reweighted(task.primary, f)
        if o is None:
            return []
        t = task.copy(objective=o)
        evs = [metrics.evaluate(t, pr, variant=(variants or {}).get(name, "base")) for name, pr in preds.items()]
        ranked = rank(t.primary, t.ties, t.constraints, evs)
        fits = [x for x in ranked if not x.excluded and x.scores[0].value is not None]
        out.append(Reweighted(factor=f, objective=t.primary, recommended=fits[0].candidate if fits else None, tied=[x.candidate for x in ranked if x.tied_with_best]))
    return out


def decides(recommended: str | None, moved: list[Reweighted]) -> bool:
    """Whether halving or doubling the weights changes the recommendation."""
    return any(r.recommended != recommended for r in moved)
