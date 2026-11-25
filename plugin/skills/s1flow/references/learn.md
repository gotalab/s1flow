# Learn: feedback from production

## Record the right answer

When the right label is learned, record it with the exact `decision_id` the decision returned:

```python
policy.feedback(decision.decision_id, label)
```

From a workflow or another process:

```bash
s1flow feedback record <task>[@vN] <decision_id> <label> --log "$RUNNER_TEMP/s1flow-log.jsonl"
```

It calls no model, so it takes no `--connections`; `--path` reads a policy file or `policies.json` instead of `policies/`. The label is
a class key, `true` / `false`, a score's level (`2`), or a box as JSON (`{"top": 0.1, "bottom": 0.3, "left": 0.2, "right": 0.6}`). `case_id` can repeat and is never a feedback key: a repeated case can have
several decision ids. Keep the answered and feedback logs together.

When labels arrive in bulk (a person corrected answers in a spreadsheet, a review queue exported its results), import
the file instead of recording one at a time:

```bash
s1flow feedback import <task>[@vN] labels.csv --log decisions.jsonl   # CSV header: decision_id,label (other columns ignored)
s1flow feedback import <task>[@vN] labels.jsonl --log decisions.jsonl # {"decision_id": ..., "label": ...} per line
```

Every row is checked before anything is written; one wrong row (a label that doesn't answer the question, a decision
the log holds under another version, two labels for one decision) writes nothing and names its line. Split a file
that mixes versions and import each part under its version. A corrected label only counts if it reaches a log:
when the person's app or tool keeps corrections elsewhere, export them with the decision ids and import them here.

Nothing is recorded without a place to record it: a policy loaded without `log=` (and with no OpenTelemetry tracer
provider) warns on its first decide, and its `feedback` raises. If the person's app has no `log=`, add it first.

## Measure production

```bash
s1flow feedback measure <task> logs/*.jsonl          # measure only; adds nothing
s1flow feedback measure <task> logs/*.jsonl --add    # also add cases to tasks/<task>/feedback.jsonl
```

It needs an s1flow project with the task (`s1flow init --task <task>`; a policy saved outside one with `--root`
has none yet). It reads decision and feedback logs (or OpenTelemetry JSON exports) and measures each policy version on the
decisions that got a label. Exit 1 when production is shown below. Any other line stops it with the file and line.

`--add` adds only decisions whose state was kept (`keep_state=True`, `decide --keep-state`, the Action's
`keep-state`) and whose label is valid. Adding production cases changes what every later run measures, so ask
the person first, or follow `criteria.md` if it says when to add them. Say how many cases it would add and from
which dates.

## Improve after production signals

When production is below, or the labels show a pattern the question misses:

1. Read the labelled production cases with the person (`collect.md`, review the labels). A wrong label or a state
   missing what decides the case is fixed there, not by a new question.
2. With the cases added, `s1flow run <task> --models <current's candidate>` (with no `--models`, `run` asks
   `s1flow.toml`'s `default` on the task's own question). For a changed question, `improve.md`.
3. `s1flow report <task>`: show the candidates, the tied ones as tied.
4. If the person picks one, `ship.md`: adopt with a reason, a pull request, and their merge.

Never treat optimize's own score or a historical benchmark as production evidence.
