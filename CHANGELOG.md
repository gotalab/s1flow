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

Each removed command fails with one line naming what replaces it.
