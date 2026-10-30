# Changelog

## Unreleased

### Breaking changes for 0.1.0a1 users

- `s1flow github fetch | audit | rationale` left the CLI. The same steps are the Skill's script,
  `python .agents/skills/s1flow/scripts/github.py fetch | audit | rationale owner/repo [--project DIR]`
  (`s1flow skill install` writes it; standard library and the `gh` CLI only). It reads and writes the same
  `data/raw/github/` files and finds the project as the CLI did, so a fetch already made carries on where it stopped.
- `s1flow policy validate FILE` is now `s1flow policy create FILE --check`. With `--connections` it still checks
  the binding. `policy create` takes `--connections` too and checks the binding before it saves.
- `s1flow optimize prompt TASK` is now `s1flow optimize TASK`. Its `--pr` and `--dry-run` options are gone: open
  the pull request with your agent or `gh pr create`; its `--json` result no longer has `branch`.
- `s1flow compare` and `s1flow rank` merge into `s1flow report`, which now prints the candidates ordered by the
  task's objective with the ranking's pick marked (what `rank` printed). `--json` gives every metric of each
  candidate (what `compare --json` gave) plus `ranking` (what `rank --json` gave, now under that key).
  `--json` prints this comparison summary, not the old `s1flow/report@1` document. `--candidate` and `--from` work
  as on `compare`; `--limit` and `--offset` now page the ranking too. The text names each candidate it does not
  rank (no runs, or not every case answered). With no runs, `report` exits 0 and says so, where `rank` exited 2.
- `report` no longer writes `reports/<task>/<variant>/latest.md` and `latest.json`. `--out DIR` takes a directory
  (`compare --out` took a file) and writes `DIR/comparison.json` (what `compare --out` wrote) and `DIR/questions/<variant>.md` / `.json` (what `latest.*` held) for each
  question with runs. Its `--variant` option is gone: every question variant is in one report.
- Merging the pull request is the release. `s1flow promote` and the `next` channel are gone: `adopt` saves the new
  version and makes it current in `channels.json`, so the pull request shows the switch and its merge ships it.
- Only `adopt` points `current`. `adopt TASK@vN --reason` is the rollback, and `adopt --spec FILE --reason` saves an
  unevaluated runtime spec as the next version and makes it current; both run on the base install, and outside an
  s1flow project with `--root` (and `--connections` for `--spec`). `policy create`
  is `adopt --spec` with `--root`, and now needs `--reason` (`--check` does not).
- Each switch appends a line to `policies/<task>/history.jsonl` (`schema/history-1.json`): when, the version, the one
  before, who, why, and for a measured candidate the held-out test's verdict and whether `--force` wrote it. A
  candidate `adopt` refuses as below on the held-out test gets a `refused` line too.
- `optimize` no longer makes anything current, and no longer compares on the held-out test: it writes the new
  question and runs it on every case as a candidate, `<model>/<variant>`. `report` lists it and `adopt` ships it.
  Its `--json` has `candidate` in place of `verdict`, `reason`, `check` and `policy`.
- `adopt` writes nothing when the held-out test shows the candidate below (exit 1); `--force`, which was on
  `promote`, now writes it anyway. `promotion-overrides.jsonl` is no longer written.
- Named channels (`TASK@staging`) are gone: a policy is `TASK`, `TASK@current` or `TASK@vN`. A `channels.json`
  from 0.1.0a1 still reads its `current`; its other names are ignored and dropped on the next write. A policy set
  0.1.0a1 exported from another channel still loads by `TASK` or `TASK@vN`.
  `policy export --channel` is gone (it exports each task's current version), and `s1flow.policies.NEXT` with it.
- `check` compares current with `--against vN`; its default candidate is current when `--against` names another
  version, else an edited question. The `s1flow check` Action reads the version `current` names on the base
  commit (the pull request's base, or the commit before a push) and passes it as `--against`; its `against`
  input now defaults to that; when it cannot read the base commit, it warns and checks current alone. `check`
  no longer writes `reports/<task>/checks.json`.
- Evaluation records (`vN.evaluation.json`) are now `s1flow/policy-evaluation@3` (`schema/policy-evaluation-3.json`;
  `evaluated-policy-2.json` is now `evaluated-policy-3.json`). `selection.recommended` is gone: s1flow records who
  picked and why, not what it would have picked. `evidence.test_uses` is gone: it counted only the uses on the machine
  that ran, and CI lost them. `selection.forced` is new: `true` when `adopt --force` wrote a version below on the
  held-out test, and `reason` says why. `@2` records still read, as `@3`, never forced: 0.1.0a1 stored a
  version below on the held-out test without `--force`, so a `@2` record cannot say. `forced` is refused on a record
  whose held-out test is not below. `adopt --json` prints the new shape.
- `s1flow tasks` shows each task's current policy; its `--json` has `current` (a version) in place of
  `channels`, and each policy `current: true|false` in place of `channels: [...]`.
- Only `s1flow run` writes `tasks/<task>/split.json`, the first time it runs on a task. `report` no longer writes
  it, and `adopt`, `optimize` and `check` refuse with "the first `s1flow run TASK` fixes the held-out test share"
  when it is missing, instead of drawing one of their own (a CI checkout would draw it again on every run). Cases
  added later are placed by a hash of their ID, at the task's `split.test`, when the file is read; the file is
  never rewritten. A run with too few labelled cases to hold out a test share asks the models and writes no
  file yet; a later run does. The file is now
  `s1flow/split@2` (`schema/split-2.json`) without `uses`: it counted only the uses on the machine that ran. `@1`
  files still read. `check --json` no longer has `test_uses`.
- The `s1flow check` Action fails a pending check (`on-pending: fail`, the new input's default; `warn` restores
  the warning). `s1flow init --ci` writes `on-pending: fail` into the workflow. A check that cannot measure (a
  pull request from a fork gets no keys, and some answers are not cached) no longer lets the change merge.
- `check` never passes on stored evidence: it asks both versions again. A version adopted with `--force` fails as
  any version below does; the comment shows that it was forced, by whom and why. A version adopted without an
  evaluation (`adopt --spec`) is checked like any other (it used to stop with "no evaluation record"). A
  candidate older than the version it is checked against that ran before it (`--history FILE`, default the
  task's `history.jsonl`; the Action passes the base commit's) gets the new verdict `rollback`: measured, shown,
  exit 0. The Action fails a pull request that rewrites, renames or removes a saved `vN.json` or
  `vN.evaluation.json` (or whose files it cannot list), and
  flags one that edits files under `tasks/<task>/` or `s1flow.toml`, which set the rules and the cases the check
  applies.
- `report` marks no pick: the `*` mark and `ranking[].recommended` are gone, and `=` marks the candidates the
  objective cannot tell apart at the top (`ranking[].tied`). The Markdown report's headline says which candidate
  the tiebreak puts first instead of which is "chosen", and its `◎` is now `=`. The weights table shows the
  candidates tied at the top with the weights halved and doubled, in place of a recommended one.
- A `tiebreak` with neither `"latency"` nor `"cost"` no longer has them added after it: with no tiebreak, the
  candidates the objective cannot tell apart are listed by name, unordered. The template keeps
  `tiebreak=["latency", "cost"]`; write it into an older task.py to keep the old order.
- `feedback measure` only measures by default; `--add` also adds the cases to `tasks/<task>/feedback.jsonl`
  (it used to add them unless `--dry-run`). `--dry-run` fails, naming the replacement. Its `--json` `added` has
  `written`.
- `s1flow report` with no task lists every task's current version, as `s1flow tasks` does, with the last switch
  from `history.jsonl` (who, when, why); its `--json` has `why`. `s1flow tasks` shows the same lines.
- `report --json` has `order`: what orders the `tied` rows (`by`, task.py's tiebreak as applied; `skipped`, and
  `why`). With nothing in `by`, the order of the tied rows says nothing.
- `s1flow optimize` runs the optimizer task.py names: `optimizer=Gepa(budget=300, reflection=None)` (the template
  writes it; it is also the default), another object with `name`, `settings()` and `run(problem)`, or the name of
  an `s1flow.optimizers` entry point. `--budget` no longer has a default of its own: with `--reflection`,
  `--patience` and `--max-cost` it changes GEPA's settings for one run, and is refused for another optimizer.
  `tasks/<task>/optimized/*.json` is now `s1flow/optimized@2`, one record for every optimizer: `optimizer`,
  `settings`, `model_calls`, `cost_usd` (what it spent beside the model's calls), and what only it records in
  `detail` (GEPA's reflection LM, candidates and val scores). `@1` records still read. `optimize --json`'s
  `optimization` has the new shape.

Each removed command fails with one line naming what replaces it.

### Added

- `tiebreak` takes `"latency"` and `"cost"` beside objectives, in the order that ranks the tied candidates
  (`tiebreak=["cost", "latency"]` puts API cost first).
- `s1flow init --task` writes every default into task.py: `split=Split(test=0.3, k=5, seed=1)`,
  `objective=Accuracy()`, `tiebreak=["latency", "cost"]`, `constraints=Constraints()`. The task measures as it
  did with them left out, and orders tied candidates as 0.1.0a1 did.
