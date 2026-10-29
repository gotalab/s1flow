"""astral-sh/ruff: which part of Ruff does an issue concern?

Derived from flat maintainer labels:
formatter (formatter, style), server, configuration (configuration, cli, rule-selection),
linter (rule, fixes, suppression, isort, docstring, diagnostics, linter, preview). Issues whose labels
fall in two of these are left out: their answer is ambiguous.
"""

from s1flow.objectives import Coverage
from s1flow.questions import Choice
from s1flow.eval import Task

task = Task(
    id="gh-ruff-area",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"]},
    question_id="area",
    question=Choice(
        instructions="Which part of Ruff (a Python linter and formatter) does this issue concern?",
        criteria={
            "linter": "Lint rules, their fixes, suppression comments (noqa), import sorting, docstring checks, diagnostics or preview rules.",
            "formatter": "The code formatter: how formatted code looks.",
            "server": "The language server (LSP) and editor integration.",
            "configuration": "Settings, the command-line interface, or selecting which rules are enabled.",
        },
    ),
    label=lambda r: r["label"],
    # Labels go on an issue only when the answer is sure: the workflow reads `unsure` (policies v1-v3 chose by this).
    objective=Coverage(target_accuracy=0.95),
    source="GitHub issues of astral-sh/ruff (labels applied by maintainers)",
    show=lambda r: r["title"],
)
