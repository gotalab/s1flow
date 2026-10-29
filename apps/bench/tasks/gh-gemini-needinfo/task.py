"""google-gemini/gemini-cli: does a new issue need more information before anyone can act on it?

Built from triaged issues (any `area/` label), positive when they carry `status/need-information`.
The repository's Gemini triage bot applies these labels.
"""

from s1flow.eval import Task
from s1flow.questions import Boolean

task = Task(
    id="gh-gemini-needinfo",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"]},
    question_id="need_information",
    question=Boolean(
        instructions="Does this GitHub issue need more information from the reporter before a maintainer can act on it?",
        criteria={
            "true": "Missing what is needed to act: no reproduction steps, no version or environment, no error output, or the request is too vague to tell what is wanted.",
            "false": "A maintainer can start: the problem or request is clear and the needed details are there.",
        },
    ),
    label=lambda r: r["label"],
    source="GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)",
    show=lambda r: r["title"],
)
