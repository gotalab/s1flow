---
name: s1flow
description: Try, build, measure, ship and improve typed decisions (yes/no, one-of-N, a level, a box) with s1flow. Use to try a model on a few inputs, put a decision in production with or without an evaluation, collect and label cases, compare models and question variants, adopt a policy in a pull request, call a policy from an app or CI, and measure it in production. Not for reading code or judging whether work is complete.
---

# s1flow

s1flow asks a model one typed question about an input (`state`): yes/no, one of as many options as the model
takes (often about 20), a score (a level) or a box. A
task holds the labelled cases and the question (`tasks/<id>/task.py`); a policy is the version an app runs
(`policies/<task>/vN.json`). If the CLI is absent: `uv tool install "s1flow[eval]"`.

Three principles:

- **The CLI measures, records and switches. It decides nothing.** `run`, `report` and `feedback measure`
  measure; `adopt` records why in `history.jsonl` and is the only command that changes which version is current.
  Which candidate to adopt, whether to merge, the objective, the labels, and whether to add production cases are
  decided by the person, or by you when the person has written down how.
- **Rules live in files.** `task.py` and `s1flow.toml` hold every rule the CLI follows. `init` writes the defaults
  out so they can be read and changed.
- **One command per purpose.** Flow: `cases`, `run`, `optimize`, `report`, `adopt`, `decide`, `feedback`.
  Setup and distribution: `init`, `doctor`, `models`, `export`.

**`criteria.md`.** Before any of those decisions, read `tasks/<id>/criteria.md` if it exists: the person's written
decision criteria. Follow it when it covers the decision; otherwise ask the person. Copy any number in it (for
example "a false negative costs 3x a false positive") into `task.py`'s objective, because the CLI reads only
`task.py`. Never invent weights, cutoffs or a pick, and never adopt or merge on your own.

**No evaluation needed to start.** To see what a model answers, call it on the inputs the person gives:
`s1flow decide --model liquid:d1.2 --state @input.json --boolean "Is this a bug report?"` (`--questions` for choice,
score or box). `provider:id` needs no project, only that provider's key (`references/setup.md`); nothing is saved.
To put a decision of any type in production without measuring it first, write it as a policy and save it
unevaluated (`references/app.md`, "Ship without an evaluation"): its log keeps every answer, so cases can come later.

**Open the question type's playbook** whenever you choose or change `objective=`, suggest a metric, a target or a
hand-off line (which answers a person takes), or before `adopt`. The type is `question=` in `task.py`:
`references/types/boolean.md`, `references/types/choice.md`, `references/types/score.md` or
`references/types/box.md`. It says what to ask and what today's objectives can and cannot do. Other types have none yet.

Read the one reference for the stage at hand:

| Stage | Read |
|---|---|
| Start a project, agree on the decision, collect cases, write `task.py`, review labels | `references/collect.md` |
| Run models and question variants, optimize, read `report`, charts, a new model version | `references/measure.md` |
| Adopt a candidate, write the reason and the PR body, go back (adopt the older one again) | `references/ship.md` |
| Call a policy from an app, a workflow or another language; decision logs; `export` | `references/app.md` |
| Record the right answers, measure production, add cases, improve the question | `references/learn.md` |
| Keys and hosts in a sandbox or CI, `doctor`, `models`, exit codes, `--json`, names | `references/setup.md` |
