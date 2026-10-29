# Compare model and question variants

Evaluation commands need `s1flow[eval]`. `run` asks models and saves answers; `report` and `rank` remain
available for their existing detailed and objective-specific consumers. `compare` is the preferred compact
overview across the current line-up and every task question variant:

Evaluation uses the selected project's connections unless overridden with `--connections PATH`; the CLI
priority is explicit `--connections`, then `S1FLOW_CONNECTIONS`, then the selected project's `s1flow.toml`.
These sources are not merged. See `references/cli.md` for project search boundaries and the SDK's separate
explicit-construction rules.

```bash
s1flow run <task> --models <model[:version][/variant]>
s1flow report <task>                         # development report; no held-out test selection
s1flow compare <task>                        # compact text, 12 candidates by default
s1flow compare <task> --json                 # the same bounded result for an agent
s1flow compare <task> --limit 20 --offset 12
s1flow compare <task> --candidate jev:1.14/policy  # exact candidate detail
s1flow compare <task> --out comparison.json  # full snapshot, including chart arrays
s1flow compare --from comparison.json --json  # read the snapshot offline
```

The candidate ID is `model[:version][/variant]`; `base` is omitted from the ID. The comparison uses one
snapshot for text, JSON and the optional page, so candidate IDs, scores, intervals, rules and reasons do not
drift between views. `--out` leaves stdout compact and writes the complete renderer input. `--from` reads only
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

Comparison is observational: candidates stay in model/variant order, including below-target results. Its v2
snapshot contains metric definitions (unit and measurement basis) and each candidate's values and intervals.
Plain-answer metrics, configured objective scores at a fitted rule, and selective coverage/accuracy pairs are
kept distinct. Read all relevant metrics; no overall winner or fixed speed/cost preference is implied.
Stored task constraints are reference conditions here, not a filter. Missing or stale evidence remains unknown.

The person owns the decision criteria, including concerns not represented by a metric. An agent may explain
trade-offs, but must not invent weights, priorities or a strict cutoff, or select a candidate unless authorized
with a selection rule. `rank` remains an explicitly requested objective-based view with its existing ordering
rules; it is not a required comparison step. Policy adoption remains a separate action:

```bash
s1flow adopt <task> <candidate> --reason "..."
s1flow check <task> --candidate next
s1flow promote <task>@v<N> --connections s1flow.toml
```

`compare`, `report`, `rank`, and the HTML page do not adopt or activate anything. `adopt` records the selected
candidate and reason; `check` is the explicit held-out comparison; `promote` changes the active channel. A valid
unevaluated policy can still be run through the base runtime when that is an intentional, separately reviewed
path, but it has no evaluation evidence.

To add a model or version, edit the project's `s1flow.toml`, declare capabilities when known, and run it on the
same task cases. Compare latency only when actual concurrency and retry recording make the measurements alike;
otherwise leave the comparison unknown and measure again with `--fresh --concurrency N`. Historical benchmark
files are context, not evidence for a current choice.

Scores and Coverage use answered labelled dev cases. Refused/unsupported cases are counted separately, not included in that denominator. Inspect the scored count and refusal count together; differing answered populations are not automatically ranked as comparable.

