# Feedback and improvement

Record the correct answer for each decision once you know it, measure the policy in production, and turn logged
decisions into new cases.

## Record feedback

A `case_id` identifies a business item, such as a ticket. A `decision_id` identifies one judgment of one input by
one policy. Record feedback against the decision ID you got back; if the issue is edited or you call again, you
get a new ID.

```bash
s1flow feedback record ticket-bug@v1 DECISION_ID true --log decisions.jsonl \
  --path policies/ticket-bug/v1.json
s1flow feedback measure ticket-bug decisions.jsonl --json         # measures; --add also adds the cases
```

When people correct answers in bulk, such as a reviewer fixing labels in a spreadsheet, import them in one go
instead of one `record` per decision:

```bash
s1flow feedback import ticket-bug@v1 labels.csv --log decisions.jsonl --path policies/ticket-bug/v1.json
```

The file is a CSV whose header has `decision_id` and `label` (other columns are ignored, and a label is read as
`record` reads it), or JSON Lines of `{"decision_id": ..., "label": ...}`. Every row is checked first: a label that
doesn't answer the question, a decision the log holds under another policy, or two labels for one decision stops
the import, and nothing is written. A decision ID the log doesn't hold is recorded, with a notice, since its
decision may be in another log.

Your app records nothing unless it says where: give `policies.load(..., log=PATH)` (or `decide --log`), or set up an
OpenTelemetry tracer provider. Without either, the first `decide` warns, and `feedback` raises instead of dropping
the label.

## Measure in production

Measurement skips unknown IDs, conflicting answers, mismatched policy digests and feedback that can't be tied
to a valid input, and reports each one it skipped. Duplicate events are counted once, and later corrections stay in
the history of the same decision. `measure` only measures and counts the cases it could add; `--add` adds them
to `tasks/<task>/feedback.jsonl`. A decision's input becomes a new case only if that input was logged.

Production measurement uses the objective and decision rule you adopted. It describes only the decisions that
have feedback, and reports what share of decisions that is. Having lots of labels doesn't mean they were
collected without bias.

## Improve the question

A coding agent with the s1flow Skill improves the question the way a person would, and keeps the three shares of
the labelled cases to three jobs:

```bash
s1flow report ticket-bug --split train --out work    # the mistakes to write from: work/questions/<variant>.md
s1flow run ticket-bug --models jev/plain,jev/scope   # the variants it wrote in task.py
s1flow report ticket-bug --split val                 # pick among them on cases their writer never read
s1flow adopt ticket-bug jev/plain --reason "..."     # the held-out test, read once, for the pick
```

It writes each variant from the train cases alone: every case the current question got wrong or answered under 0.9,
with the model's top answers (`--split train --out`). It picks on the validation cases alone, and `adopt` checks the
pick on the test share, which nothing read before. In s1flow's own comparison, a question written from every train
and validation mistake scored well on them but not on the test share, while one written from train and picked on
validation held up there. `report` notes that a variant may have been written from the cases it is scored on, so
its values there lean high. The Skill's `references/improve.md` holds the steps.
