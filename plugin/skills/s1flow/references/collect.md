# Collect: the decision, the cases, the task

## Start

```bash
s1flow init --task <id>      # s1flow/: s1flow.toml, tasks/<id>/task.py, .gitignore; nothing else
```

Ask before passing `--ci` or `--skill` (`setup.md`). A task's directory is named its id.

## Agree on the decision

Read `tasks/<id>/criteria.md` first, if it exists. One task is one decision: a boolean, or one of as many options as the
model takes (often about 20). Write down with the person:

- the question in one sentence, and for a choice, each option's meaning in one line under about 100 characters
  (it becomes the option's criteria word for word);
- what the model sees (`state`): only what the app will have at the moment it asks, in the same shape. A field
  the app will not have at runtime leaks the answer;
- what counts as the right answer (`label`), and who gave it: a person, a bot, a later event;
- the objective. For a yes/no decision, ask: **which mistake hurts more, a false negative (a yes read as no) or a
  false positive (a no read as yes), and by how much?** Take the answer's own words to the objective; never pick
  the weights yourself. Write the answer into `criteria.md` if the person agrees, so the next decision can use it.

| The person says... | Objective |
|---|---|
| about the same | `Accuracy()` (the default) |
| a false negative is N times worse (or a false positive is) | `ExpectedLoss(fn=N, fp=1)` |
| false positives must stay under X% of the noes | `Recall(max_false_alarm=X)` |
| the positives matter, the rest is the bulk | `F1()` |
| act only on sure answers, a person takes the rest | `Coverage(target_accuracy=0.95)` |

On a yes/no decision every objective here but Coverage chooses the P(yes) threshold from the data, and the policy
keeps it. For a choice: `Accuracy()`, `MacroF1()` if the rare options matter as much, or Coverage.

- **The held-out test share.** Ask how many cases to hold out (`split=Split(test=0.3, k=5, seed=1)` is the
  default). The test share is never shown while choosing; `adopt` and `check` read it. Fewer than about 200
  cases leaves a small test share.

## Collect the cases

You decide where to look and how many to collect, and tell the person what you chose and why. Write
`tasks/<id>/data.jsonl`, one case per line: `{"id": "...", ...fields..., "label": ...}`. Convert with a few lines
of Python; s1flow has no importer on purpose.

| Source | Notes |
|---|---|
| GitHub issues and PRs | `scripts/github.py` below. Labels a bot applied measure agreement with the bot, not accuracy. Say which. |
| The app's own logs | The states the app really sends, with the outcome learned later (a reply, a refund, a revert) as the label. |
| Labels people already gave | A support tool's tags, a review queue, a spreadsheet. Keep who labelled. |
| No labels anywhere | Draft labels for 50-100 cases, have the person correct them, and use only the corrected ones. Never score against unreviewed drafts. |
| A public dataset | Only to compare models on a similar decision; record its license in `source`. |

Aim for 200 or more labelled cases, every option present, and the newest cases when the decision drifts.

### GitHub

Access is the person's own `gh` login. GraphQL allows 5,000 points an hour (a page costs one or two); never use
the search API for bulk work (30 requests a minute). `<skill>` is this Skill's directory; the script needs only
Python's standard library and `gh`, and finds the project as the CLI does (or `--project DIR`). It reads; it
never writes to the repository.

```bash
python <skill>/scripts/github.py fetch owner/repo --issues 300 --prs 0   # data/raw/github/<owner>__<repo>/, resumable
python <skill>/scripts/github.py audit owner/repo                        # per label group: coverage, doubles, who applied
python <skill>/scripts/github.py rationale owner/repo --id <id>          # after data.jsonl: maintainers' comments around each label
```

Read the audit with the person before writing a task: a group that is rarely used, or used twice on one issue,
is not one decision yet. `rationale` fills only a task whose choice keys are the label names as they are.

`issues.jsonl` has one issue per line: `number`, `title`, `body`, `createdAt`, `labels.nodes[].name`, and
`timelineItems.nodes[]`, whose `LabeledEvent`s say who applied each label (a `Bot` actor or a login ending in
`[bot]` is a bot). One row per issue: `{"id": "#<number>", "label": ..., "created": "<createdAt>", "title": ...,
"body": <stripped, first 2000 characters>}`. Tell the person how many issues you left out and why. Two forms:

- A label group (`area/cli`, `area/docs`): a `Choice` whose criteria are the labels' descriptions (`labels.json`),
  from issues carrying exactly one label of the group. Ask whether to keep only labels a person applied.
- One label against the rest (bug / not-bug): a `Boolean`, true for issues carrying it, false for issues carrying
  other labels only. Leave unlabelled issues out. Ask whether some labels do not mean "not a bug" (`duplicate`,
  `question`). The smaller side is often under 20%: agree on `F1()` or `Recall(...)` instead of Accuracy.

`state` is what the app will send (`{"title": r["title"], "body": r["body"]}`); `source` names the repository and
says the labels are as applied there.

## Write task.py

`init --task` writes `tasks/<id>/task.py` with every default written out. Fill it in:

```python
task = Task(
    id="ticket-kind",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"][:1500]},
    question_id="kind",
    question=Choice(instructions="What kind of ticket is this?", criteria={"bug": "...", "question": "...", "feature": "..."}),
    label=lambda r: r["label"],          # None leaves the case out
    split=Split(test=0.3, k=5, seed=1),
    objective=Accuracy(),
    tiebreak=["latency", "cost"],
    constraints=Constraints(),
    source="where the cases come from, with its license",
    show=lambda r: r["title"],           # one line per case in reports
)
```

- A boolean question with a choice-like label uses `Boolean(...)`; a choice scored as one option against the rest
  sets `kind_params=KindParams(positive="bug")`.
- Uneven costs: `ExpectedLoss(fn=, fp=)`, or `Loss(default=1, losses={"server": {"formatter": 3}})` (right answer
  -> answer given -> loss; "true" / "false" for a boolean). The weights come from the person or `criteria.md`.
  Show the person report's lines for the weights halved and doubled.
- A measure s1flow lacks is a function in task.py:
  `@per_case(direction="min", sets="threshold") def wake_loss(label, reading, *, miss: float = 20.0) -> float`,
  then `objective=wake_loss(miss=20)`.
- `objective=` is the one objective that sets how the policy reads its answers. `tiebreak=[...]` orders, in turn,
  the candidates it cannot tell apart: more objectives, `"latency"` (p90 per case) and `"cost"` (API cost per
  10,000 cases). One left out is not used; with no tiebreak, the tied are listed by name, unordered.
- `constraints=Constraints(latency_p99_ms=..., cost_per_10k_usd=..., min_labels=...)` excludes candidates. On a
  binary task, `min_precision=` and `min_recall=` are floors: the threshold is chosen among those that keep both,
  and a model that cannot is excluded with the reason. Floors come from the person, like weights. They need an
  objective that sets the threshold (any binary objective but Coverage and AUROC).
- `optimizer=Gepa(budget=300, reflection=None)` is what `optimize` runs (`measure.md`).
- How the team already decides (a triage policy, CONTRIBUTING, a bot's prompt) goes in `tasks/<id>/context.md`:
  `optimize` reads it, the model never does. `criteria.md` is for the person's decision criteria, not the model.

Supported question types: the direct `Client` takes boolean, choice, score and box where the provider does;
evaluation compares boolean, choice and box (score is unsupported); a policy holds one boolean or choice.

## Check the cases

```bash
s1flow cases check <id>
```

Fix every ✗ (a state that does not build, a label outside the options, a duplicate with another label). Read
every ⚠ with the person: a smaller side under 20% means Accuracy rewards always answering the larger side.

## Review the labels

Collected labels are often wrong, and sometimes the state does not hold what decides them. After the first
`run`, read the cases again with the person:

```bash
s1flow cases review <id>             # models disagreeing at 0.9+, and the same state with another label
s1flow cases review <id> --sample 30 # also 30 drawn at random from the rest
s1flow cases review <id> --json      # the same, with each case's state
s1flow cases correct <id> <case> --verdict relabel --label <option> --reason "<the criterion>" --by <person>
s1flow report <id>                   # scores against the corrected labels; no new calls
```

- **s1flow points.** It does not judge which label is right.
- **You investigate and propose.** Read each listed case's source (the issue, its comments, linked PRs, who
  labelled it and when) and apply the question's criteria **as written** in `task.py`. Propose one verdict with a
  one-line reason: `relabel` (the criteria give another option), `keep` (the label is right, the models are
  wrong), `unclear` (the criteria do not settle it), `missing` (what decides it is not in the state).
- **The person decides.** Labels are theirs, unless `criteria.md` says how to settle such a case. Record a verdict
  only after they agree, with `--by` naming them (the default is `git config user.name`). Batch the proposals;
  never record your own reading as theirs. Do not stretch the criteria to fit a case: that is `unclear`.

**The random sample.** Reading only what the models dispute moves labels toward those models. A random sample
(`--sample N`; s1flow records which cases it drew) gives the label error rate. Choose its size with the person;
s1flow has no default. With no wrong label found, the error rate is only known to be under:

| sampled | 10 | 20 | 30 | 50 | 100 |
|---|---|---|---|---|---|
| error rate under (95%) | 31% | 17% | 12% | 7% | 4% |

It should be well under what the decision turns on (a 95% target needs labels wrong far less than 5%, so 50 to
100). A first look needs 20 to 30. Under about 100 development cases: read them all. Review uses train + val only;
test labels stay held out.

**When the task itself is in question.** `cases review` lists every `unclear` and `missing` with its reason. When
they are more than about one in ten of what was read, or their reasons repeat, stop correcting. With the person,
decide whether to sharpen an option's criteria, merge or split options, add to the state what the app will have,
or narrow the decision. Write the change in `task.py`, then review again. Never change the decision, its options
or the objective without the person.
