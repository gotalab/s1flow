---
name: s1flow
description: Build, measure, ship and improve typed yes/no and one-of-N decisions with s1flow. Use to collect and label cases, compare models and question variants, adopt a policy in a pull request, call a policy from an app or CI, and measure it in production. Not for reading code or judging whether work is complete.
---

# s1flow

s1flow asks a model one typed question about an input (`state`): yes/no, or one of up to 20 options. A task holds
the labelled cases and the question (`tasks/<id>/task.py`); a policy is the version an app runs
(`policies/<task>/vN.json`). If the CLI is absent: `uv tool install "s1flow[eval]"`.

Three principles:

- **The CLI measures, records and switches. It decides nothing.** `run`, `report`, `check` and `feedback measure`
  measure; `adopt` records why in `history.jsonl` and is the only command that changes which version is current.
  Which candidate to adopt, whether to merge, the objective, the labels, and whether to add production cases are
  decided by the person, or by you when the person has written down how.
- **Rules live in files.** `task.py` and `s1flow.toml` hold every rule the CLI follows. `init` writes the defaults
  out so they can be read and changed.
- **One command per purpose.** Flow: `cases`, `run`, `optimize`, `report`, `adopt`, `check`, `decide`, `feedback`.
  Setup and distribution: `init`, `doctor`, `models`, `export`.

**`criteria.md`.** Before any of those decisions, read `tasks/<id>/criteria.md` if it exists: the person's written
decision criteria. Follow it when it covers the decision; otherwise ask the person. Copy any number in it (for
example "a false negative costs 3x a false positive") into `task.py`'s objective, because the CLI reads only
`task.py`. Never invent weights, cutoffs or a pick, and never adopt or merge on your own.

Read the one reference for the stage at hand:

| Stage | Read |
|---|---|
| Start a project, agree on the decision, collect cases, write `task.py`, review labels | `references/collect.md` |
| Run models and question variants, optimize, read `report`, charts, a new model version | `references/measure.md` |
| Adopt a candidate, write the reason and the PR body, read `check`, go back (revert the pull request) | `references/ship.md` |
| Call a policy from an app, a workflow or another language; decision logs; `export` | `references/app.md` |
| Record the right answers, measure production, add cases, improve the question | `references/learn.md` |
| Keys and hosts in a sandbox or CI, `doctor`, `models`, exit codes, `--json`, names | `references/setup.md` |
