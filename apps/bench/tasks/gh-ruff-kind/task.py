"""astral-sh/ruff: what kind of issue is this?

Ruff's labels are flat and applied by maintainers (`gh-audit`: 2,166 human, 4 bot). The kinds are
derived from them, first match wins: bug > question > documentation >
feature (rule, wish, accepted, needs-design, plugin). A bug in a rule counts as a bug.
"""

from s1flow.objectives import Coverage
from s1flow.questions import Choice
from s1flow.eval import Task

task = Task(
    id="gh-ruff-kind",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"]},
    question_id="kind",
    question=Choice(
        instructions="What kind of issue is this, filed against Ruff (a Python linter and formatter)?",
        criteria={
            "bug": "Something isn't working: a crash, a false positive or negative, a wrong fix, or output that differs from what is documented.",
            "question": "Asking for support or clarification about how Ruff behaves or how to configure it.",
            "documentation": "Improvements or additions to the documentation.",
            "feature": "A request to implement a new lint rule, extend an existing one, or add a capability; nothing is broken.",
        },
    ),
    label=lambda r: r["label"],
    # Labels go on an issue only when the answer is sure: the workflow reads `unsure` (policies v1-v3 chose by this).
    objective=Coverage(target_accuracy=0.95),
    source="GitHub issues of astral-sh/ruff (labels applied by maintainers)",
    show=lambda r: r["title"],
)
