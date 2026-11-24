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
s1flow optimize ticket-bug --json                  # a new candidate; report and adopt as for any other
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

A coding agent with the s1flow Skill improves the question the way a person would: it reads the current question's
mistakes on the train and validation cases (`s1flow report TASK --out DIR`, then `DIR/questions/<variant>.md`),
writes a new wording as a variant in task.py, runs it, and shows it beside the current one. It never reads the test
share, so `s1flow adopt` can still check the pick there. `report` notes that a variant may have been written from
the cases it is scored on, so its values there lean high. The Skill's `references/improve.md` holds the steps.

## Optimize the prompt

`s1flow optimize` is the other way, and experimental: its options and the record it saves may change between
releases.

`s1flow optimize` runs the optimizer task.py names (`optimizer=Gepa(budget=300, reflection=None)` in the
template). GEPA searches for better prompts using a stand-in score (half correctness, half 1 − Brier score) on the
train and validation cases; the test share is never given to it. s1flow then runs the best prompt on every case as
a new candidate. It doesn't train model weights, and it never makes the new prompt live: `s1flow report` compares
it with the others, and `s1flow adopt` makes it current when you pick it. `--budget`, `--reflection`,
`--patience` and `--max-cost` change GEPA's settings for one run.

Another optimizer plugs in the same way: an object with `name`, `settings()` and `run(problem)` in task.py
(`problem` holds the task, the model, the question to start from, and the train and validation cases; `run`
returns a `Found`: the question, the model calls, what it spent beside them, and anything of its own in `detail`),
or a package's factory under the `s1flow.optimizers` entry point group, named by a string
(`optimizer="my-optimizer"`). Every optimizer's result is saved in the same record,
`tasks/<task>/optimized/<variant>.json` (`s1flow/optimized@2`).
