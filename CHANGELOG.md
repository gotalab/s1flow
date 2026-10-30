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
- Merging the pull request is the release. `s1flow promote` and the `next` channel are gone: `adopt` (and
  `optimize`, when it finds a better question) saves the new version and makes it current in `channels.json`, so the
  pull request shows the switch and its merge ships it. `policy create` makes the version it saves current too. A
  rollback is a pull request that points `current` at an older version.
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

Each removed command fails with one line naming what replaces it.

### Added

- `tiebreak` takes `"latency"` and `"cost"` beside objectives, in the order that ranks the tied candidates
  (`tiebreak=["cost", "latency"]` puts API cost first). A tiebreak naming neither still has latency and then API
  cost after it, as before.
- `s1flow init --task` writes every default into task.py: `split=Split(test=0.3, k=5, seed=1)`,
  `objective=Accuracy()`, `tiebreak=["latency", "cost"]`, `constraints=Constraints()`. The task measures and ranks
  as it did with them left out.
