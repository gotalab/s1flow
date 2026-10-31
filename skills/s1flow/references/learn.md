# Learn: feedback from production

## Record the right answer

When the right label is learned, record it with the exact `decision_id` the decision returned:

```python
policy.feedback(decision.decision_id, label)
```

From a workflow or another process:

```bash
s1flow feedback record <task>[@vN] <decision_id> <label> \
  --connections s1flow.toml --log "$RUNNER_TEMP/s1flow-log.jsonl"
```

`--connections` is required; `--path` reads a policy file or `policies.json` instead of `policies/`. The label is
a class key, or `true` / `false`. `case_id` can repeat and is never a feedback key: a repeated case can have
several decision ids. Keep the answered and feedback logs together.

## Measure production

```bash
s1flow feedback measure <task> logs/*.jsonl          # measure only; adds nothing
s1flow feedback measure <task> logs/*.jsonl --add    # also add cases to tasks/<task>/feedback.jsonl
```

It reads decision and feedback logs (or OpenTelemetry JSON exports) and measures each policy version on the
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
   `s1flow.toml`'s `default` on the task's own question), then `s1flow optimize <task>` for a changed
   question (`measure.md`). Optimize ships nothing.
3. `s1flow report <task>`: show the candidates, the tied ones as tied.
4. If the person picks one, `ship.md`: adopt with a reason, a pull request, `check`, and their merge.

Never treat optimize's own score or a historical benchmark as production evidence.
