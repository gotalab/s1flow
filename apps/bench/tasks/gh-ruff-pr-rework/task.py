"""astral-sh/ruff: will a pull request need rework after review?

Built from the merged PRs the Skill's `github.py fetch` saved, those by people
(bot-authored PRs left out). Positive when 2 or more commits were pushed after the first human
review; review bots and the author's own reviews do not count. The state is
what is known when the PR opens: title, description, author association, size and touched paths.
"""

from s1flow.objectives import Coverage, ExpectedLoss
from s1flow.eval import Task
from s1flow.questions import Boolean

task = Task(
    id="gh-ruff-pr-rework",
    cases="data.jsonl",
    state=lambda r: {k: r[k] for k in ("title", "body", "author", "size", "files")},
    question_id="rework",
    question=Boolean(
        instructions="Will this pull request need further changes after a maintainer reviews it?",
        criteria={
            "true": "Likely to need rework: large or cross-cutting, touches core or risky areas, unclear description, no tests, or a first-time contributor.",
            "false": "Likely to merge as is: small and focused, clear description, tests included, or routine changes.",
        },
    ),
    label=lambda r: r["label"],
    objective=Coverage(target_accuracy=0.95), tiebreak=[ExpectedLoss(fn=1, fp=1)],
    source="Merged PRs of astral-sh/ruff (review history via the GitHub API)",
    show=lambda r: r["title"],
)
