# Review the labels

Collected labels are often wrong, and sometimes the state does not hold what decides them. After
the first `run`, read the cases again with the user:

```bash
s1flow cases review <id>             # models disagreeing at 0.9+, and the same state with another label
s1flow cases review <id> --sample 30 # also 30 drawn at random from the rest (how many: below)
s1flow cases review <id> --json      # the same, with each case's state, for you to read
s1flow cases correct <id> <case> --verdict relabel --label <option> --reason "<the criterion>" [--by <person>]
s1flow report <id>                  # development score against corrected labels; no new calls
```

The roles:

- **s1flow points.** It does not judge which label is right.
- **You investigate and propose.** For each listed case, read its source (the issue, its comments,
  linked PRs, who applied the label and when) and apply the question's criteria **as written** in
  `task.py`. Propose one verdict with a one-line reason naming the criterion or what is missing:
  - `relabel`: the criteria give another option;
  - `keep`: the label is right, the models are wrong;
  - `unclear`: the criteria do not settle it (two options fit, or none);
  - `missing`: what decides it is not in the state (only the code, a linked PR, or a later event tells).
- **The user decides.** Record a verdict only after the user agrees, with `--by` naming them (it defaults to git config user.name: pass it when that is not the person who decided). Batch
  the proposals so the user reads quickly; never record your own reading as theirs.

Do not reinterpret the criteria to make a case fit. When the criteria do not settle a case, that is
`unclear`, not a relabel.

**The random sample.** Reading only what the models dispute fixes labels toward those models and says
nothing about the cases they agree with. A random sample (`cases review --sample N`; s1flow records which cases it drew, so their corrections count) gives the label
error rate. Choose its size with the user from what the numbers will be used for; s1flow has no default.
If none of the sampled labels is wrong, the error rate is still only known to be under:

| sampled | 10 | 20 | 30 | 50 | 100 |
|---|---|---|---|---|---|
| error rate under (95%) | 31% | 17% | 12% | 7% | 4% |

The error rate should be well under what the decision turns on: the gap between the models being
chosen from, or the slack between the target accuracy and 100% (a 95% target needs labels wrong far
less than 5%, so 50 to 100). A first look at whether the labels are usable needs about 20 to 30. A
development set with under about 100 cases: read all its cases instead. Review and sampling use
train + val only. Keep test labels held out for the explicit final check of the selected policy.

**When the task itself is in question.** `cases review` lists every `unclear` and `missing` with its
reason. These are evidence about the task, not the labels. When they are a noticeable share of what
was read (as a rough guide, more than one in ten) or their reasons repeat, stop correcting. With the
user, decide whether to change the task, judged against the objective agreed first (`collect.md`): sharpen an
option's criteria, merge or split options, add to the state what the app will have at the time it
asks, or narrow the decision. Write the change in `task.py`, then review again. Do not change the
decision, its options or the objective without the user.
