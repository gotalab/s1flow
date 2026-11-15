"""google-gemini/gemini-cli: will a pull request need rework after review?

Built from the merged PRs the Skill's `github.py fetch` saved, those by people
(bot-authored PRs left out). Positive when 2 or more commits were pushed after the first human
review; review bots (gemini-code-assist) and the author's own reviews do not count. The state is
what is known when the PR opens: title, description, author association, size and touched paths.
"""

from s1flow.objectives import AUROC, ExpectedLoss
from s1flow.eval import Task
from s1flow.questions import Boolean

task = Task(
    id="gh-gemini-pr-rework",
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
    # A forecast: reviewers take the pull requests most likely to need rework first, and nothing is acted on
    # alone. So what counts is whether the probability puts them in the right order.
    objective=AUROC(), tiebreak=[ExpectedLoss(fn=1, fp=1)],
    source="Merged PRs of google-gemini/gemini-cli (review history via the GitHub API)",
    show=lambda r: r["title"],
)
