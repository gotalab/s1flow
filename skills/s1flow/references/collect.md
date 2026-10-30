# Agree on the decision and collect the cases

## Agree on the decision and the objective

One task is one decision: a boolean, or one of at most 20 options. Write down with the user:

- the question in one sentence, and for a choice, each option's meaning in one line under about
  100 characters (it becomes the option's criteria word for word);
- what the model sees (`state`): only what the app will have at the moment it asks, in the
  same shape (a dict of fields, or text). A field the app will not have at runtime leaks the answer;
- what counts as the right answer (`label`), and who gave it: a person, a bot, a later event;
- the objective. For a yes/no decision, ask one question: **which mistake hurts more, a miss (a yes
  read as no) or a false alarm (a no read as yes), and by how much?** Take the answer's own words to the
  objective; never pick the weights yourself:

| The user says... | Objective |
|---|---|
| about the same | `Accuracy()` (the default) |
| a miss is N times worse (or a false alarm is) | `ExpectedLoss(fn=N, fp=1)` |
| false alarms must stay under X% of the noes | `Recall(max_false_alarm=X)` |
| the positives matter, the rest is the bulk | `F1()` |
| act only on sure answers, a person takes the rest | `Coverage(target_accuracy=0.95)` |

  Each of these on a yes/no decision except Coverage chooses the P(yes) threshold from the data (0.5 is no
  better a cut than any other), and the policy keeps it. Precision or recall the decision cannot go below is a
  floor (`task.md`). For a choice: `Accuracy()`, `MacroF1()` if the rare options matter as much, or Coverage.

That is the task's `objective=`. A second objective that should only break ties goes in `tiebreak=[...]`;
latency and API cost are not objectives (limit them with `constraints=`; they order the remaining ties on their own).

The direct `Client` supports boolean, choice, score and box questions when the provider supports them. Evaluation
comparison supports boolean, choice and box; score is explicitly unsupported there. A v2 runtime policy accepts
one boolean or choice question.

## Collect the cases

Write `tasks/<id>/data.jsonl` (a task's directory is named its id), one case per line:
`{"id": "...", ...fields..., "label": ...}`. Convert from wherever the cases are with a few
lines of Python; s1flow has no importer on purpose. Where to look, by purpose:

| Source | Notes |
|---|---|
| GitHub issues and PRs | `scripts/github.py` below. Labels a bot applied are that bot's output: scoring against them measures agreement with the bot, not accuracy. Say which. |
| The app's own logs | The states the app really sends, with the outcome learned later (a reply, a refund, a revert) as the label. |
| Labels people already gave | A support tool's tags, a review queue, a spreadsheet. Keep who labelled. |
| No labels anywhere | Draft labels for 50-100 cases, have the user correct them, and use only the corrected ones. Never score against unreviewed drafts. |
| A public dataset | Only to compare models on a similar decision; record its license in `source`. |

Aim for 200 or more labelled cases (fewer gives wide intervals and a small held-out test share),
every option present, and the newest cases when the decision drifts over time.

## GitHub

GitHub access is the user's own `gh` login. GraphQL allows 5,000 points an hour (a page costs one
or two); never use the search API for bulk work (30 requests a minute).

```bash
python <skill>/scripts/github.py fetch owner/repo --issues 1500 --prs 600   # data/raw/github/<owner>__<repo>/, resumable
python <skill>/scripts/github.py audit owner/repo                           # per label group: coverage, doubles, who applied
python <skill>/scripts/github.py rationale owner/repo --id gh-<repo>-area   # after data.jsonl: the maintainers' comments around each label
```

`<skill>` is this Skill's directory. It finds the project as the CLI does (or `--project DIR`). The script needs only Python's
standard library and the GitHub CLI (`gh`, logged in). `rationale` looks each case's label up as a GitHub
label name: it fills only a task whose choice keys are the label names as they are (not a true/false task). Read the audit with the user before writing a
task: a group that is rarely used, or used twice on the same issue, is not one decision yet.

Then write the task yourself, with the user: `tasks/<id>/data.jsonl` from
`data/raw/github/<owner>__<repo>/issues.jsonl` (one fetched issue per line: `number`, `title`, `body`,
`createdAt`, `labels.nodes[].name`, and `timelineItems.nodes[]` whose `LabeledEvent`s say who applied each
label: a `Bot` actor or a login ending in `[bot]` is a bot), and `task.py` as below. One row per issue:
`{"id": "#<number>", "label": ..., "created": "<createdAt>", "title": ..., "body": <body, stripped, its first
2000 characters>}`; tell the user how many issues you left out and why. Two forms:

- A label group (`area/cli`, `area/docs`): a `Choice` whose criteria are the labels' descriptions
  (`labels.json`), from the issues carrying exactly one label of the group; leave out those with none or two.
  Ask whether to keep only labels a person applied (a bot's labels measure agreement with the bot).
- One label against the rest, for labels without a prefix (bug / not-bug): a `Boolean`, true for the issues
  carrying it, false for the issues carrying other labels only. Unlabelled issues are left out, since nobody
  decided them; ask the user whether some labels do not say "not a bug" (`duplicate`, `question` on a bug
  report) and leave those issues out. The smaller side is often under 20%: agree on `F1()` or
  `Recall(...)` instead of Accuracy.

`state` is what the app will send (`{"title": r["title"], "body": r["body"]}`), `source` names the repository
and that the labels are as applied there. Then `s1flow cases check <id>`.

Fetch only what the task needs (`--issues 300 --prs 0`); `github` reads, it never writes to the repository.
