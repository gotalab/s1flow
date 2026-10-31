"""What a task chooses by: its objective, the objectives that order the rest (tiebreak=) and its constraints
(s1flow.eval.objectives.declare), and custom objectives (@per_case / @on_set, s1flow.eval.objectives.custom),
for a task.py."""

from .eval.objectives.declare import (
    AUROC, Accuracy, Constraints, Loss, Coverage, ExpectedLoss, F1, MAE, MacroF1, Objective, QWK, Recall,
)
from .eval.objectives.custom import Custom, on_set, per_case
from .policies.kinds import Reading

__all__ = ["AUROC", "Accuracy", "Constraints", "Loss", "Coverage", "ExpectedLoss", "F1", "MAE", "MacroF1", "Objective", "QWK", "Custom", "Reading", "Recall",
           "on_set", "per_case"]
