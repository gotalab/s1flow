# Fix and improve

Record the right answer when it is learned with the exact id returned by the decision:

```python
runtime.feedback(decision.decision_id, label)
```

From a workflow or another process, pass that same id positionally and bind the policy to the
application's trusted connections:

```bash
s1flow feedback record <task> <decision_id> <label> \
  --connections s1flow.toml --log "$RUNNER_TEMP/s1flow-log.jsonl"
```

`case_id` is useful for searching logs but cannot identify a unique call. A repeated case can have
several decision ids.

`s1flow feedback measure <task> logs/*.jsonl` measures production from v2 decision and feedback logs.
It adds only decisions whose state was deliberately kept (`keep_state=True` or `decide
--keep-state`) to the task. Run `s1flow check <task>` when the policy needs a fresh test comparison.

To improve the question, use the explicit development command:

```bash
s1flow optimize <task> --budget 800 --patience 5
```

It writes a new question with the optimization extra and runs it as a new candidate (`<model>/<variant>`);
it ships nothing. Compare it with `s1flow report <task>` and, if the person picks it, `s1flow adopt` it like
any candidate. The held-out test remains the final check; never treat optimization's
surrogate score or a historical benchmark as current production evidence.
