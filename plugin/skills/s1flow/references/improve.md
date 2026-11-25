# Improve the question

Open this when the person asks to improve the question (the prompt, the wording, the criteria), when a report shows
the current question's mistakes share a pattern, or when production is below (`learn.md`).

You improve it: read the current question's mistakes, write better wordings as variants in `task.py`, run them,
pick one, and show it beside the current question. The CLI only measures, and `adopt` confirms a pick on the
held-out test. The result is one more candidate, adopted only if the person picks it (`ship.md`).

## Three shares, three jobs

The first `run` split the labelled cases (`split.json`): **train**, **val** and the held-out **test**.

- **Write from train.** Whoever writes a variant reads the mistakes on train alone:
  `s1flow report <task> --split train --out <dir>`.
- **Pick on val.** Compare the variants on val alone, by the numbers: `s1flow report <task> --split val`.
- **Check on test, once.** `adopt` reads test for the one candidate the person picks.

Keep the jobs apart. A question written from every development case scores well on them and worse on new ones. In
s1flow's own comparison (massive-ja-intent, jev 1.14, coverage at 95% accuracy), an agent that read every train and
val mistake reached 98% coverage on them, but on the test share its sure answers were 88-91% right instead of 95%,
on all four models tried. Builders that read train only and were picked on val held up on test: accuracy 83.9% for
the original question, 90.8% for the pick (GEPA's question reached 85.1%).

## What a writer may read

`task.py`, `context.md`, `criteria.md`, and what `report --split train --out <dir>` writes:
`<dir>/questions/<variant>.md` and `<variant>.json`. The JSON's `unsure_or_wrong` lists, per model, every train case
it got wrong or answered under 0.9 (label, answer, probability, the three likeliest answers), in the cases file's
order; `cases` holds each one's `state` and `rationale`. Group and order them as the pattern hunt needs (by label,
the wrong first).

Never, while writing a question: val's or test's cases (`report --split val --out`, `report --out` without
`--split`, the cases file, `split.json`), the `runs/` files, or the test numbers `adopt` prints. The val table
(`report --split val`, no `--out`) is for picking, after the variants are written.

## Steps

1. **Labels first.** `s1flow cases review <task>`. A wrong label, or a state missing what decides the case, is fixed
   in `collect.md` ("Review the labels"), not by a new question.
2. **Read the mistakes on train.** Current's question is the one the current policy asks (`s1flow report` with no
   task names current's candidate; `base` unless a variant was adopted). `s1flow report <task> --split train --out
   <dir>`, then that variant's JSON under `<dir>/questions/`, its list for current's model.
3. **List what goes wrong.** Start a fresh agent with no other context, if you can, and give it only what a writer
   may read. It lists every pattern the mistakes share that the question misses or says wrong: an option's
   criteria too narrow, two options that overlap, a rule the team follows that the question leaves out, an option
   with no description. With each, the cases it explains. Tell the person the few that explain the most. If none
   explains several cases, say so: a new wording is unlikely to help, and better labels, more cases or another
   model may.
4. **Write one variant per pattern.** One fresh agent each (in parallel if you can), given the same files and its
   one pattern, writes one entry of `variants=` in `task.py`: the same type and options as current's question,
   starting from its text and changing what the pattern points to.

   ```python
   variants={
       # Pattern: refactors with a behaviour change answered "refactor" (5 of the 8 at 0.9 or more, train).
       "behaviour": Choice(instructions="...", criteria={"bug": "...", "refactor": "...", "feature": "..."}),
   },
   ```

   Write the rule, never a case's text, id or label: a question that recites its cases only fits them. First try,
   for a choice: one plain sentence per option saying what it covers. It did best in the comparison above. Rules
   added only to `instructions` changed nothing there, and keywords or examples taken from train fitted train
   alone. Keep within the model's `max_instructions_chars` and `max_description_chars` (`s1flow models`) where
   declared. Without fresh agents, write them yourself, reading only what a writer may read.
5. **Check them for train's words.** A variant that borrows train's wording grows sure on the cases holding those
   words, right or wrong, and val and test cannot show it when their cases are worded like train's. In the
   comparison above, a variant that added keywords each found in one train case reached 90% coverage on train and
   76% on val; the plain-sentence one reached 88% and 84%.
   - `s1flow cases check <task>` names each variant that repeats a train case's text (six words in a row; a kana,
     a kanji or a katakana word counts as one) and the cases it comes from. Rewrite that part as the rule it stands
     for. In Japanese six words is a short phrase, so a plain definition of an option can match a case by chance
     (を連絡先に追加する): keep it when it says only what the option means.
   - The check sees only copied text. Start one more fresh agent, not a writer, with each variant's change from
     current's question and the train log the writers read (step 2's JSON). For every word, name, number and
     example the variant adds, it searches the states in that log: one found in only one or two of them, or a
     translation or rewording of one, is borrowed, not a rule. It lists them with their cases; replace each with
     the meaning it stood for, or remove it. Without a fresh agent, do the search yourself.
6. **Run them** on current's model, named as `report` names it: `s1flow run <task> --models <model>/<a>,<model>/<b>`.
   It asks every case, the test share too, for `adopt`. Say the cost first, variants x cases
   (`s1flow cases check <task>`) x current's `API $/10k` / 10,000, and run when the person says go (or
   `criteria.md` covers that spend).
7. **Pick on val.** `s1flow report <task> --split val`: each variant beside current's question. Keep the best one
   if it beats current's question on the primary objective; otherwise keep current's.
8. **Another round** starts from the kept question's train mistakes (step 2). Stop after two rounds in a row with
   no gain on val, or when the person, or `criteria.md`, says to stop. Each round reads train again and picks on
   val again, so val's numbers lean a little higher each time; `report --split val` notes it.
9. **Show it and let the person pick.** The kept variant beside current's question, val's numbers, the pattern it
   fixes. If the person picks it, `ship.md`: adopt that one candidate, once. Never adopt several variants to see
   which passes, and never change a variant toward a test result: the test would be choosing, and its verdict
   would no longer show anything. If `adopt` shows it below, bring that to the person.
