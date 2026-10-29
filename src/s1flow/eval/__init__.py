"""The evaluation stack: tasks and their cases, runs, metrics, choosing, checking, optimizing, feedback.

A task.py imports what it needs from here, the objectives and the question types:

    from s1flow.objectives import Coverage
    from s1flow.questions import Choice
    from s1flow.eval import KindParams, Split, Task
"""

from ..policies.kinds import KindParams
from .cases import Case
from .task import Split, Task

__all__ = ["Case", "KindParams", "Split", "Task"]
