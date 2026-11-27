"""astral-sh/ruff: what kind of issue is this?

Ruff's labels are flat and applied by maintainers (`gh-audit`: 2,166 human, 4 bot). The kinds are
derived from them, first match wins: bug > question > documentation >
feature (rule, wish, accepted, needs-design, plugin). A bug in a rule counts as a bug.

The labels are kept as the maintainers applied them, though about 3 in 10 cannot be read from the issue: they
record what the maintainers decided later. A false-positive report they judge intended gets `question`, and an
issue labelled only `rule` counts as feature even when it reports a false positive (Ruff has no label for a
feature request). A label learned in production is the same kind of later decision, so this task shows a decision
that should mostly go to a person; its low numbers say that, not that the models are weak. Reading 40 of the 109
cases that at least 80% of the stronger models answer against (2026-11-25): 23 later decisions, 9 `rule`-only
bug reports, 8 that fit two kinds, none where the label was right and the models wrong.
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
    # 90%: the kind describes the issue and routes it nowhere; whoever reads it first corrects a wrong one.
    objective=Coverage(target_accuracy=0.90),
    source="GitHub issues of astral-sh/ruff (labels applied by maintainers)",
    show=lambda r: r["title"],
)
