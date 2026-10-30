# Setup: projects, keys, scripting the CLI

## Install and init

```bash
uv tool install "s1flow[eval]"         # base + evaluation; add ,optimize for `optimize`, ,llm for LLM models
s1flow init [dir] --task <id>          # dir (default s1flow/): s1flow.toml, tasks/<id>/task.py, .gitignore
s1flow init --ci                       # also .github/workflows/s1flow-check.yml at the git root
s1flow init --skill                    # also write this Skill where agents read it
```

`init` writes nothing outside the project unless asked. Ask the person before `--ci` (a PR check that calls
models on every PR that changes a task, a policy or `s1flow.toml`, with `on-pending: fail`) and before `--skill`.
The base install runs `init`, `decide`, `feedback record`, `adopt --spec`, `export` and
`doctor`; the rest need `s1flow[eval]`. The SDK never installs packages at runtime.

## Keys and hosts: doctor

In a cloud agent or CI, keys are environment variables and the network may reach only allow-listed hosts. Run
the read-only check before the first model call:

```bash
s1flow doctor --models a,b --reach
s1flow doctor --policy TASK --connections s1flow.toml --reach
```

It names the variables and hosts each connection needs, never printing a value; `--reach` sends one plain HTTPS
request per host, without a key. A missing key or blocked host is a setup issue: give the operator the name from
`doctor`. A sandbox whose proxy adds the key on the way out (a network secret) keeps it out of the environment, so
`doctor` reports it as not set; leave the variable unset there and confirm with one `decide` call. s1flow sends
without a key it cannot find, and a 401 or 403 names the key as missing.

A local `.env` is a CLI convenience: it loads only from the selected project and its nearest Git ancestor, and
never replaces a variable already set. The SDK never reads `.env`.

## Models

```bash
s1flow models                          # the line-up in s1flow.toml, next to what --verify found
s1flow models --verify [--models jev:1.15]   # ask plain questions; check every claim; writes models.verified.json
```

A model and its versions are declared in `s1flow.toml` (`[models."jev@openrouter".versions."1.15"]`, `id = ...`).
`--verify` checks only what is declared; finding new versions is in `measure.md`.

## Project and connection discovery

`--project PATH` and `--connections PATH` work before or after the subcommand, only where `--help` lists them.
`--project` selects the directory containing `s1flow.toml`, or a directory containing `s1flow/s1flow.toml`. It
does not change cwd, so `--connections`, `--log` and other relative paths start at the invocation cwd. Without it
the CLI searches upward from cwd to the nearest Git boundary; outside Git, only cwd and cwd/`s1flow`. The error
for a missing project names where it searched and which option to pass.

Connections: `--connections` when given, else the project's `s1flow.toml`; never merged. `decide --policy`,
`feedback record` and `doctor --policy` need explicit `--connections`. `report --from` takes neither option.

## Names

- A policy reference is `TASK` (current) or `TASK@vN` (`ticket-kind@v3`).
- A candidate is `model[:version][/variant]` (`jev:1.14/policy`; `base` is omitted). Candidates belong to
  evaluation; a saved policy names only its `connection`, exact `model_id`, question and rule.
- Files: `tasks/<id>/` (`task.py`, `data.jsonl`, `split.json`, `criteria.md`, `context.md`, `corrections.jsonl`,
  `feedback.jsonl`), `runs/<task>/`, `policies/<task>/` (`vN.json`, `channels.json`, `history.jsonl`).

## Exit codes and output

| code | means | what to do |
|---|---|---|
| 0 | completed | read the output or saved file |
| 1 | a gate failed or a finding exists | report the verdict; do not retry unchanged |
| 2 | usage, configuration, could not run, or a pending check | read the `error:` line and fix the named input |

A usage error is one `error: ... (see s1flow <command> --help)` line. A `notice:` line on stderr is a warning.
`check --cached-only` returns 2 when an answer is needed but not cached. A removed command
prints its replacement and exits 2.

`--json` gives machine-readable output for `report`, `adopt`, `check`, `optimize`, `cases review`,
`feedback measure`, `decide`, `doctor` and `models`. Other commands print their verdict and name the files they
wrote.
