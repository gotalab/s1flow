# Feedback and improvement

Record the correct answer for each decision once you know it, measure the policy in production, and turn logged
decisions into new cases.

## Record feedback

A `case_id` identifies a business item, such as a ticket. A `decision_id` identifies one judgment of one input by
one policy. Record feedback against the decision ID you got back; if the issue is edited or you call again, you
get a new ID.

```bash
s1flow feedback record ticket-bug@v1 DECISION_ID true --log decisions.jsonl \
  --path policies/ticket-bug/v1.json --connections connections.toml
s1flow feedback measure ticket-bug decisions.jsonl --dry-run --json
s1flow optimize ticket-bug --budget 300 --json
```

## Measure in production

Measurement skips unknown IDs, conflicting answers, mismatched policy digests and feedback that can't be tied
to a valid input, and reports each one it skipped. Duplicate events are counted once, and later corrections stay in
the history of the same decision. A decision's input becomes a new case only if that input was logged.

Production measurement uses the objective and decision rule you adopted. It describes only the decisions that
have feedback, and reports what share of decisions that is. Having lots of labels doesn't mean they were
collected without bias.

## Optimize the prompt

GEPA searches for better prompts using a stand-in score (half correctness, half 1 − Brier score) on the train and
validation cases, then runs the best one on every case as a new candidate. It doesn't train model weights, and it
never makes the new prompt live: `s1flow report` compares it with the others, and `s1flow adopt` makes it current
when you pick it.
