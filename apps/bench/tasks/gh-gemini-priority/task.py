"""google-gemini/gemini-cli: which `priority/` label does a new issue get?

Built from the issues `s1flow github fetch google-gemini/gemini-cli` saved that carry
exactly one `priority/` label (any labeller). The criteria start from the
repository's own label descriptions; a TODO marks a label without one.
"""

from s1flow.eval import Task
from s1flow.questions import Choice

task = Task(
    id="gh-gemini-priority",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"]},
    question_id="priority",
    question=Choice(
        instructions="How urgent is this GitHub issue for the maintainers?",
        criteria={
            'priority/p1': 'Important and should be addressed in the near term.',
            'priority/p2': 'Important but can be addressed in a future release.',
            'priority/p3': 'Backlog - a good idea but not currently a priority.',
        },
    ),
    variants={
    # The triage bot's own definitions, from .github/workflows/gemini-scheduled-issue-triage.yml (2026-10-03).
        "policy": Choice(
            instructions="How urgent is this GitHub issue for the Gemini CLI maintainers? Judge its impact.",
            criteria={
                "priority/p1": "Critical but workable, or worse: severe issues without a reasonable workaround that significantly degrade the developer experience, e.g. specific tools failing consistently (web_search returns 500s), persistent PTY streaming hangs, memory leaks leading to OOM after short use; also critical failures breaking core functionality.",
                "priority/p2": "Significant issues: affect some workflows but a clear workaround exists, or non-critical bugs, e.g. theme flickering, confusing error messages, minor UI misalignment, failing to read deeply nested config files.",
                "priority/p3": "Minor or enhancements: trivial bugs, typos, documentation requests, or feature requests.",
            },
        ),
    },
    label=lambda r: r["label"],
    source="GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)",
    show=lambda r: r["title"],
)
