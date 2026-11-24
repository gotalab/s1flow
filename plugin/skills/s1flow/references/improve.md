# Improve the question

Open this when the person asks to improve the question (the prompt, the wording, the criteria), when a report shows
the current question's mistakes share a pattern, or when production is below (`learn.md`).

You improve it: read the mistakes on the development cases, write a better wording as a variant in `task.py`, run
it, and show it beside the current question. The CLI only measures it, and `adopt` confirms a pick on the held-out
test. `s1flow optimize` is another way (below). Either way the result is one more candidate, adopted only if the
person picks it (`ship.md`).

## What you may read

Only the development cases (train + val): what `report` (and its `--out` files `questions/<variant>.md` and `.json`)
and `cases review` show, the rows of the case ids they list, `task.py`, `context.md` and `criteria.md`.

Never read the `runs/` files, the cases file as a whole, the test ids in `split.json` or their rows, or the test
numbers `adopt` prints, while writing a question. `run` saves the test share's answers too, for `adopt`. That held-out
test is the only check that a new question did not just fit the cases you read; a question written with it in view
leaves nothing to check it.

## Steps

1. **Labels first.** `s1flow cases review <task>`. A wrong label, or a state missing what decides the case, is fixed
   in `collect.md` ("Review the labels"), not by a new question.
2. **Read the mistakes.** Current's question is the one the current policy asks (`s1flow report` with no task names
   current's candidate; `base` unless a variant was adopted). `s1flow report <task> --out report`, then
   `report/questions/<variant>.md` for that question: "Wrong at a high probability", and "Cases the models disagree
   on" when two models or more ran on it. `<variant>.json`'s `high_confidence_errors` lists every one past the 8
   shown. For a case's whole state, search the cases file for that id and read only its row. Read
   `tasks/<task>/context.md`: how the team already decides.
3. **Name the pattern** the wrong answers share and the question misses or says wrong: an option's criteria too
   narrow, two options that overlap, a rule the team follows that the question leaves out. Tell the person in a
   sentence or two. If there is none, say so: a new wording is unlikely to help, and better labels, more cases or
   another model may.
4. **Write one variant** in `task.py`, of the same type with the same options as current's question, starting from
   its text and changing only what the pattern points to:

   ```python
   variants={
       # Mistakes: refactors with a behaviour change answered "refactor" (5 of the 8 at 0.9 or more).
       "behaviour": Choice(instructions="...", criteria={"bug": "...", "refactor": "...", "feature": "..."}),
   },
   ```

   Write the rule, never a case's text, id or label: a question that recites the cases it is scored on only fits
   them.
5. **Run it** on current's model, named as `report` names it: `s1flow run <task> --models <model>/<variant>`. It
   asks every case, the test share too. Say its cost first, cases (`s1flow cases check <task>`) x current's
   `API $/10k` / 10,000, and run it when the person says go (or `criteria.md` covers that spend).
6. **Show it.** `s1flow report <task>`, read as `measure.md` says, current's question and the variant side by side.
   Report notes that a variant may have been written from the cases it is scored on: say that its numbers lean high,
   and that `adopt` checks on the held-out test whether it holds.
7. **One round, unless told more.** Each round reads the same cases again, so its numbers lean higher. Write another
   variant only when the person, or `criteria.md`, says to.
8. **If the person picks it,** `ship.md`. Adopt that one candidate, once. Never adopt several variants to see which
   passes, and never change a variant toward a test result: the test would be choosing, and its verdict would no
   longer show anything. If `adopt` shows it below, bring that to the person.

## Optimize

```bash
s1flow optimize <task>     # needs s1flow[optimize]
```

It runs task.py's `optimizer=Gepa(budget=300, reflection=None)` (or an optimizer plugged in there) on current's
question (GEPA takes boolean and choice questions), and saves the result as a new candidate `<model>/<variant>`.
`--budget`, `--model`, `--reflection`, `--patience` and `--max-cost` override it for one run. It reads
`tasks/<task>/context.md`, and the train and val cases, never the test share. It ships nothing: compare it in
`report` and adopt it like any candidate (`ship.md`). Its own score is not evidence. `optimize` is experimental: its
options and the record it saves may change between releases, and it may be removed once compared with the steps
above. Say so when suggesting it.
