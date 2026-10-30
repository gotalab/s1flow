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

Each removed command fails with one line naming what replaces it.
