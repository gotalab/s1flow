# Changelog

## Unreleased

### Breaking changes

0.1.0a1 had almost no users, so these come with no migration path: a file in an older format is refused.

- The CLI has 12 commands. `compare` and `rank` are `report`; `tasks` is `report` with no task; `policy create`
  and `policy validate` are `adopt --spec` (with `--check` to validate only); `policy export` is `export`;
  `skill install` is `init --skill`; `optimize prompt` is `optimize`. `promote`, `guide`, `skill path` and
  `github` are gone (the Skill's `scripts/github.py` fetches from GitHub).
- Merging the pull request is the release: `adopt` saves the next version and makes it current. A policy is
  `TASK` or `TASK@vN`; the `next` and named channels are gone. Each switch appends to `policies/<task>/history.jsonl`.
- `adopt` refuses a candidate below on the held-out test unless `--force`. `optimize` writes a candidate and
  makes nothing current. Only `s1flow run` writes `split.json`.
- `check` asks both versions again and compares current with `--against vN`. The Action fails a pending check
  by default, and a pull request that rewrites, renames or removes a saved version.
- `report` marks no pick: `=` marks the candidates tied at the top, ordered only by task.py's `tiebreak`.
- `feedback measure` only measures; `--add` also adds the cases.
- `optimize` runs the optimizer task.py names (`Gepa` by default).
- Files now read only as `s1flow/policy-evaluation@3`, `s1flow/split@2`, `s1flow/optimized@2` and `s1flow/run@2`.
- Evaluation records, runs and cached answers written before retries, case counts and evidence digests were
  recorded are no longer read.
- `S1FLOW_CONNECTIONS` is gone: pass `--connections PATH`, else the project's `s1flow.toml` is read.
- `s1flow init` inside a project adds to it. The Agent Skill is one `SKILL.md` and six references by stage.

### Added

- `s1flow models` runs on the base install. `s1flow models --verify` needs only `s1flow[images]`; before, both
  needed `s1flow[eval]` and `s1flow[images]`.
- `tiebreak` takes `"latency"` and `"cost"` beside objectives, in the order that ranks the tied candidates
  (`tiebreak=["cost", "latency"]` puts API cost first).
- `s1flow init --task` writes every default into task.py: `split=Split(test=0.3, k=5, seed=1)`,
  `objective=Accuracy()`, `tiebreak=["latency", "cost"]`, `constraints=Constraints()`. The task measures as it
  did with them left out, and orders tied candidates as 0.1.0a1 did.
