# Compare model and question variants

Evaluation commands need `s1flow[eval]`. `run` asks models and saves answers; `report` reads them, across
the current line-up and every task question variant (it replaces `compare` and `rank`):

Evaluation uses the selected project's connections unless overridden with `--connections PATH`; the CLI
priority is explicit `--connections`, then `S1FLOW_CONNECTIONS`, then the selected project's `s1flow.toml`.
These sources are not merged. See `references/cli.md` for project search boundaries and the SDK's separate
explicit-construction rules.

```bash
s1flow run <task> --models <model[:version][/variant]>   # the first run also writes tasks/<task>/split.json: commit it
s1flow report <task>                         # the candidates by the task's objective, the ranking's pick marked
s1flow report <task> --json                  # every metric of each candidate, and the ranking, for an agent
s1flow report <task> --json --limit 20 --offset 12
s1flow report <task> --candidate jev:1.14/policy  # exact candidate detail
s1flow report <task> --out DIR               # DIR/comparison.json (with chart arrays) and DIR/questions/<variant>.md
s1flow report --from DIR/comparison.json --json  # read the snapshot offline
```

The candidate ID is `model[:version][/variant]`; `base` is omitted from the ID. Text, JSON and the optional page
read the same evaluations, so candidate IDs, scores, intervals, rules and reasons do not drift between views.
`--out` leaves stdout compact and writes the complete renderer input and a Markdown report per question. `--from` reads only
that file: it does not rescore, call a provider, certify the snapshot as current, or consult the task's current
files. Use the exact ID with `--candidate`; an unknown ID is an error listing the available IDs.

The snapshot is development-only (`scope=dev`). It excludes the held-out test share; adopting the selected candidate
or running the explicit final `s1flow check <task> --candidate ...` reads it before treating a choice as a production result. It preserves the task
source, comparison timestamp and data/evaluation/input identities. Each row keeps provider, concrete model ID,
distribution, declared and recorded concurrency, latency, and cost provenance (`billed`, stored `list` displayed as
estimated, `mixed`, or unknown). Unknown values stay unknown, and missing, refused, unsupported or failed cases keep their reasons.

| surface | boolean | choice | score | box |
|---|---|---|---|---|
| direct `Client` | provider-dependent | provider-dependent | provider-dependent | provider-dependent |
| evaluation comparison | yes | yes | explicitly unsupported | yes |
| v2 runtime policy | one question | one question | unsupported | unsupported |

For Boolean rows, the configured P(positive) rule and its precision/recall and calibration data are
separate from the minimum-probability selection curve. Choice rows can show a selected-answer probability curve.
Box rows compare the common task metrics and use box confidence for selection. If a run has no genuine
distribution or box confidence, the corresponding probability curve is absent. A provider's confidence is its
own signal; do not describe it as the probability of the selected answer.

The JSON `candidates` stay in model/variant order, including below-target results; `ranking` orders the
complete ones by the task's declared objective, `tiebreak` and constraints, and marks the pick. The v2
snapshot contains metric definitions (unit and measurement basis) and each candidate's values and intervals.
Plain-answer metrics, configured objective scores at a fitted rule, and selective coverage/accuracy pairs are
kept distinct. Read all relevant metrics. The ranking's pick follows the task's declared objective; among candidates
it cannot tell apart it follows `tiebreak`, which the template sets to lower latency, then lower API cost: a
preference written in task.py, not a measured difference. Missing or stale evidence remains unknown.

The person owns the decision criteria, including concerns not represented by a metric. An agent may explain
trade-offs, but must not invent weights, priorities or a strict cutoff, or select a candidate unless authorized
with a selection rule; the ranking's pick is a suggestion under the declared objective, not a decision.
Policy adoption remains a separate action:

```bash
s1flow adopt <task> <candidate> --reason "..."
s1flow check <task> --against v<N>
```

`report` and the HTML page do not adopt or activate anything. `adopt` records the selected
candidate and reason and makes it current; `check` is the explicit held-out comparison; merging the pull request
that carries the change releases it. A valid
unevaluated policy can still be run through the base runtime when that is an intentional, separately reviewed
path, but it has no evaluation evidence.

To add a model or version, edit the project's `s1flow.toml`, declare capabilities when known, and run it on the
same task cases. Compare latency only when actual concurrency and retry recording make the measurements alike;
otherwise leave the comparison unknown and measure again with `--fresh --concurrency N`. Historical benchmark
files are context, not evidence for a current choice.

Scores and Coverage use answered labelled dev cases. Refused/unsupported cases are counted separately, not included in that denominator. Inspect the scored count and refusal count together; differing answered populations are not automatically ranked as comparable.

