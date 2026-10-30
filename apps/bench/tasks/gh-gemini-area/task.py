"""google-gemini/gemini-cli: which `area/` label does a new issue get?

Built from the issues `github.py fetch google-gemini/gemini-cli` (the Skill's script) saved that carry
exactly one `area/` label (any labeller). The criteria start from the
repository's own label descriptions; a TODO marks a label without one.
"""

from s1flow.eval import Task
from s1flow.questions import Choice

task = Task(
    id="gh-gemini-area",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"]},
    question_id="area",
    question=Choice(
        instructions="Which area of Gemini CLI does this GitHub issue belong to?",
        criteria={
            'area/agent': 'Issues related to Core Agent, Tools, Memory, Sub-Agents, Hooks, Agent Quality',
            'area/core': 'Issues related to User Interface, OS Support, Core Functionality',
            'area/documentation': 'Gemini CLI documentation tasks and issues',
            'area/enterprise': 'Issues related to Telemetry, Policy, Quota / Licensing',
            'area/extensions': 'Issues related to Gemini CLI extensions capability',
            'area/non-interactive': 'Issues related to GitHub Actions, SDK, 3P Integrations, Shell Scripting, Command line automation',
            'area/platform': 'Issues related to Build infra, Release mgmt, Testing, Eval infra, Capacity, Quota mgmt',
            'area/security': 'Issues related to security',
        },
    ),
    variants={
    # The triage bot's own definitions, from .github/workflows/gemini-scheduled-issue-triage.yml (2026-10-03).
        "policy": Choice(
            instructions="Which area of Gemini CLI does this GitHub issue belong to?",
            criteria={
                "area/agent": 'The "brain" of the CLI: core agent logic, model quality, tool/function calling, memory, web search, generated code quality, sub-agents.',
                "area/core": "The fundamental CLI app: UI/UX, installation, OS compatibility, performance, command parsing, theming, flickering.",
                "area/documentation": "Website docs, READMEs, inline help text.",
                "area/enterprise": "Telemetry, policy, quota / licensing.",
                "area/extensions": "Gemini CLI extensions capability.",
                "area/non-interactive": "GitHub Actions, SDK, third-party integrations, shell scripting, command line automation.",
                "area/platform": "Platform specific behavior.",
                "area/security": "Authentication, authorization, privacy, data leaks, credential storage.",
            },
        ),
    },
    label=lambda r: r["label"],
    source="GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)",
    show=lambda r: r["title"],
)
