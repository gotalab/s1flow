# boolean: yes or no

The label is `true` or `false`. The model gives P(yes). Two numbers can be chosen from the data: the **threshold**
(P(yes) at or above it reads yes) and the **min probability**, the hand-off line (an answer whose own probability,
P(yes) for a yes and 1 - P(yes) for a no, is under it is unsure, and a person takes it). One objective sets one of the
two, never both. How an objective acts, and whose numbers these are: `collect.md`, "Agree on the decision".

## Purposes and their metric

| The person wants... | Standard metric | In `task.py` | Sets |
|---|---|---|---|
| as many right as possible, both mistakes about as bad | accuracy | `Accuracy()` (the default) | threshold |
| one mistake N times worse than the other | expected cost | `ExpectedLoss(fn=N, fp=1)` for a miss, `ExpectedLoss(fn=1, fp=N)` for a false alarm | threshold |
| catch the positives, false alarms at most X of the noes | recall at a fixed false-positive rate | `Recall(max_false_alarm=X)` | threshold |
| a rare positive found, the rest is the bulk | F1 of the positive | `F1()` | threshold |
| precision or recall never under a floor | precision / recall | `constraints=Constraints(min_precision=, min_recall=)` beside an objective that sets the threshold | — |
| P(yes) to rank the yeses above the noes, no cut yet | AUROC | `AUROC()` | nothing |
| act on sure answers only, a person takes the rest | coverage at a target accuracy | `Coverage(target_accuracy=X)` | min probability |
| the same, and a person's look has a cost against a mistake's | expected cost with abstention | `Loss(losses={"true": {"false": N}}, unsure=c)` (a miss costs N; a false alarm is `{"false": {"true": N}}`) | min probability |

The question report (`collect.md`) shows every candidate's F1 whatever the objective, and `report --json` its
precision and recall too. F-beta and PR-AUC (for a rare positive) are not built in: an `@on_set` function in `task.py`
(`collect.md`, "Write task.py").

## Ask the person

- What happens after a yes, and after a no, and who acts on it? When the app acts only on a yes (close the issue, page
  someone) and a no leaves things as they were, an unsure answer and a no do the same thing: the cut matters
  (`ExpectedLoss`, `Recall`), not a hand-off line.
- **Which mistake hurts more, a false negative (a yes read as no) or a false positive (a no read as yes), and by how
  much?** Take the answer's own words to the objective: "about the same" is `Accuracy()`, "a miss is 5 times worse" is
  `ExpectedLoss(fn=5, fp=1)`, "a wrong yes is 5 times worse" is `ExpectedLoss(fn=1, fp=5)`, "false alarms under 2% of
  the noes" is `Recall(max_false_alarm=0.02)`.
- Is one side rare? `cases check` warns under 20% while the objective is `Accuracy()`. Accuracy then rewards always
  answering the larger side: agree on `F1()`, `Recall(...)` or `ExpectedLoss(...)` instead.
- Is there a precision or recall the team already promises? That is a floor in `Constraints`.
- Will a person look at the answers the model is unsure of? If so, what accuracy must the automatic ones keep (a
  Coverage target), or what does one look cost against one mistake (Loss's `unsure`)?

## The hand-off line

- `Coverage(target_accuracy=X)` answers the largest share it can while the sure answers keep accuracy X. It does not
  choose the threshold: an answer is right or wrong as read at P(yes) 0.5, and a miss and a false alarm count the
  same.
- `Loss(..., unsure=c)` charges c for every unsure answer and each mistake its cost in the table
  (`losses[label][answer]`, `default` for the rest), and chooses the line with the lowest mean loss, from a fixed grid
  (`collect.md`). The threshold stays at 0.5.
- Every other objective but `AUROC()` chooses the threshold and no line; `AUROC()` chooses neither (read at 0.5). A
  policy adopted on any of them acts on every answer.
- A threshold chosen by cost and a hand-off line together are not supported yet. If the person needs both, say so;
  `Loss` with the miss and false-alarm costs and an `unsure` cost is the nearest.
- The line reads the answer's probability (P(yes) for a yes, 1 - P(yes) for a no) from P(yes) as the model gave it.
  Only a candidate with no ※ in the question report has one; on the others every answer has probability 1.
