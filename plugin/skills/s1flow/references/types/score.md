# score: a level

The levels are 0..L-1 in the order of the question's criteria, and the label is a level. The model gives a
probability per level (one-hot on its score when it gives none: ※ in `report`). The answer is the expected level,
rounded (a half up), which is not always the most probable level: half on 1 and half on 3 answers 2. The hand-off
line reads the probability of the level answered. How an objective acts, and whose numbers these are: `collect.md`,
"Agree on the decision".

## Purposes and their metric

| The person wants... | Standard metric | In `task.py` | Sets |
|---|---|---|---|
| close on average, the distance counts | MAE (in levels) | `MAE()` (the default) | nothing |
| agreement with people's grades, a big miss worse than a small one | QWK (quadratic weighted kappa) | `QWK()` | nothing |
| the exact level, each level its own action | accuracy | `Accuracy()` | nothing |
| one cut drives the action (act on 3 and up) | the cut's recall, precision, cost | a boolean question for the cut ("Is it 3 or more?"), `boolean.md` | as there |
| P(level ≥ k) to rank the cases at each cut | ordinal AUROC, averaged over the cuts | `AUROC()` | nothing |
| act on sure answers only, a person takes the rest | coverage at a target accuracy (exact level) | `Coverage(target_accuracy=X)` | min probability |
| the same, with "near enough" or a review cost in levels | mean loss with abstention | an `@per_case` function, below | min probability |

`report` shows every candidate's MAE whatever the objective, and `report --json` and the chart page its QWK too.
Within-one accuracy (off by at most one level), RMSE and Spearman's rank correlation are not built in: an
`@per_case` or `@on_set` function in `task.py` (`collect.md`, "Write task.py"). `Loss` does not take a score.

## Ask the person

- What does each level lead to? When each level triggers its own action, the exact level matters (`Accuracy()`);
  when the level is a measure (quality, urgency), the distance does (`MAE()`, `QWK()`). When one cut drives the
  action ("act on 3 and up"), the decision is a yes/no: propose a boolean question for the cut.
- Is one level off acceptable? Two?
- Is reading too high as bad as reading too low? If not, the cost differs by side: an `@per_case` function.
- Will a person look at the answers the model is unsure of? If so, what accuracy on the exact level must the
  automatic ones keep, or what does one look cost, in levels off?

## The hand-off line

- `Coverage(target_accuracy=X)` answers the largest share it can while the sure answers keep the exact level X of
  the time. A level off counts as wrong.
- For a line by distance, write the loss in `task.py`: what a sure answer is off by, and what an unsure one costs.
  The line with the lowest mean loss is chosen:

  ```python
  from s1flow.objectives import Reading, per_case

  @per_case(direction="min", sets="min_probability")
  def levels_off_or_review(label: int, reading: Reading | None, *, review: float = 0.5) -> float:
      if reading is None or reading.below_min_probability:
          return review            # a person takes it
      return float(abs(reading.value - label))

  task = Task(..., objective=levels_off_or_review(review=0.5))   # `review` comes from the person
  ```

  A custom objective holds no constraint: it cannot say "keep MAE under 0.3 on the sure answers", only trade the
  cost of a look against the levels off.
- The line reads one level's probability, not a cut's: an answer split between 3 and 4 is sure it is 3 or more,
  but each level holds about half, so the line can hand it to a person. Another reason to ask a cut as a boolean.
- `MAE()`, `QWK()`, `Accuracy()` and `AUROC()` set nothing: a policy adopted on them acts on every answer.
- The line reads the probability the model gave the level. Only a candidate whose `report` row has no ※ has one.
