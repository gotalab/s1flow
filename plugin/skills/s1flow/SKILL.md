---
name: s1flow
description: Call typed decision models directly, run saved policies, or compare and improve model and instruction variants with s1flow. Use for yes/no and one-of-N decisions in apps or CI, labelled-case evaluation, human or authorized-agent candidate selection, visual comparisons, and production feedback. Not for reading code or judging whether work is complete.
---

# s1flow

s1flow asks typed questions about an input; a runtime policy owns one question. This Skill routes each job to the
relevant reference; the CLI runs it (if absent: `uv tool install "s1flow[eval]"`). `s1flow init` makes a project in
`s1flow/` and nothing else; ask before passing `--ci` (a PR check workflow). The CLI discovers the selected project; the SDK never discovers configuration.

For evaluation, `s1flow report TASK` is the one view across model and question variants. It reads saved development
runs only: no model call, held-out test score, or activation. It orders candidates by the task's declared objective and
marks the ranking's pick; `--json` adds every metric. Keep below-target results visible. The person owns the
criteria. An agent chooses only with delegated criteria and authority, without inventing weights or strict cutoffs.

The base install creates, validates and runs a v2 policy: task/version, trusted `connection` and exact `model_id`,
one boolean or choice question, rule and optional input shape. Bind runtime code to an explicit `Client`; CLI
policy execution requires `--connections PATH`. The SDK never installs from policy/input; evaluation commands
remain development work and `run`, `report`, `adopt` need `s1flow[eval]`.

The direct `Client` supports provider-supported boolean, choice, score and box questions. Evaluation comparison
supports boolean, choice and box; score is explicitly unsupported. A v2 policy supports one boolean or choice.
Box has common metrics and confidence curves; Boolean adds precision/recall, threshold curves and calibration;
Choice has a selected-answer probability curve. Omit curves without genuine probability or box confidence; vendor
confidence is not selected-answer probability.

Read the one reference for the job at hand (`s1flow guide <topic>` prints it too):

| The job | Read |
|---|---|
| Agree on the decision and its objective; collect labelled cases (GitHub, logs, existing labels) | `references/collect.md` |
| Write `task.py` and check the cases (`cases check`) | `references/task.md` |
| Compare model × question variants; inspect or paginate the compact result | `references/compare.md` |
| Review the labels with the user (`cases review`, `cases correct`, the random sample) | `references/review.md` |
| Render a report with multiple metrics and exportable figures from a saved snapshot | `references/charts.md` |
| Pick a policy with the user, promote it, call it from the app | `references/adopt-and-run.md` |
| A provider offers a new version of a model: notice it, ask, run, compare with current | `references/new-version.md` |
| Call it from a GitHub workflow or another language (an example to copy) | `references/workflow.md` |
| What a decision log line looks like, and its JSON Schema | `references/logs.md` |
| Record the right answers, measure in production, improve the question | `references/fix.md` |
| A cloud agent or CI: keys, allow-listed hosts (`s1flow doctor`) | `references/sandbox.md` |
| Configure connections and projects; script the CLI: exit codes, `--json`, names | `references/cli.md` |

The runtime returns `decision_id`; store it when a later label may arrive. Feedback uses it, while `case_id` is
only a log annotation. `below_min_probability` is `null` when unset, otherwise `true` or `false`.
Comparison evidence is dev-scoped: unknowns stay unknown; source/date, provider/model, measured concurrency,
billed/list (displayed as estimated)/mixed/unknown cost remain visible; `adopt` records the selected candidate and reason and
reads its held-out result, while `promote` alone changes the active channel.
