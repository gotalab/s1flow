# choice: one of N options

The label is an option key. The model gives a probability per option (one-hot on its answer when it gives none:
※ in `report`). The answer is the most probable option, and the hand-off line reads that option's probability. How
an objective acts, and whose numbers these are: `collect.md`, "Agree on the decision".

## Purposes and their metric

| The person wants... | Standard metric | In `task.py` | Sets |
|---|---|---|---|
| as many right as possible, every option alike | accuracy | `Accuracy()` (the default) | nothing |
| rare options to count as much as common ones | macro-F1 | `MacroF1()` | nothing |
| some confusions to cost more than others | cost matrix | `Loss(default=1, losses={"server": {"formatter": 3}})` | nothing |
| each option's probability to rank its cases above the rest | one-vs-rest AUROC, averaged over the options | `AUROC()` | nothing |
| act on sure answers only, a person takes the rest | coverage at a target accuracy | `Coverage(target_accuracy=X)` | min probability |
| the same, and a person's look has a cost against a mistake's | expected cost with abstention | `Loss(default=1, unsure=c)`, with `losses=` for the costly confusions | min probability |
| one option against the rest (bug or not) | binary metrics | `kind_params=KindParams(positive="bug")`, then `boolean.md` | as there |

`report` shows every candidate's macro-F1, whatever the objective. Per-option recall, weighted F1 and Cohen's kappa
are not built in: an `@on_set` function in `task.py` (`collect.md`, "Write task.py"). Top-k accuracy does not apply:
a policy acts on one option.

## Ask the person

- Each option's meaning in one line (`collect.md`): it becomes the option's criteria.
- Are some options much rarer, and do they matter as much as the common ones? Yes means `MacroF1()`. With a
  hand-off too, keep Coverage or Loss as the objective and read each candidate's macro-F1 in `report`, or put
  `MacroF1()` in `tiebreak`.
- Do some confusions cost more than others ("a server error read as a formatter issue is 3 times worse")? Write only
  the cells the person names in `losses`; `default` covers the rest.
- Does one option drive the action and the rest mean "not that"? Then it is a one-against-the-rest decision:
  `positive=` and `boolean.md`.
- Will a person look at the answers the model is unsure of? If so, what accuracy must the automatic ones keep, or
  what does one look cost against one mistake?

## The hand-off line

- `Coverage(target_accuracy=X)`: the largest share answered while the sure answers keep accuracy X (the exact option).
- `Loss(..., unsure=c)`: c for every unsure answer, each mistake its cost in the table; the line with the lowest
  mean loss.
- `Accuracy()`, `MacroF1()`, `AUROC()` and `Loss` without `unsure` set nothing: a policy adopted on them acts on every
  answer, the most probable option.
- The line reads the probability the model gave its option. Only a candidate whose `report` row has no ※ has one.
