"""google-gemini/gemini-cli: which `kind/` label does a new issue get?

Built from the issues `s1flow github fetch google-gemini/gemini-cli` saved that carry
exactly one `kind/` label (any labeller). The criteria start from the
repository's own label descriptions; a TODO marks a label without one.
"""

from s1flow.eval import Task
from s1flow.questions import Choice

task = Task(
    id="gh-gemini-kind",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"]},
    question_id="kind",
    question=Choice(
        instructions="What kind of GitHub issue is this?",
        criteria={
            'kind/bug': 'Something is broken: an error, a crash, wrong output, or behaviour that differs from what is documented or expected.',
            'kind/enhancement': 'A request for a new capability or a change to how something works; nothing is broken.',
            'kind/question': 'The reporter asks how to do something or whether something is possible; no change is requested.',
        },
    ),
    label=lambda r: r["label"],
    source="GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)",
    show=lambda r: r["title"],
)
