# Driving the CLI from a script or an agent

## Exit codes

Every command repeats these codes in `--help`:

| code | means | what to do |
|---|---|---|
| 0 | completed | read the output or saved file |
| 1 | a gate failed or a finding exists | report the verdict; do not retry unchanged |
| 2 | usage, configuration, execution failure, or a pending check | read the `error:` line and fix the named input or connection |

Usage errors are one `error: ... (see s1flow <command> --help)` line. A `notice:` line on stderr is a
warning and does not change the result. `check --cached-only` returns 2 when an answer is needed but
is not cached.

## Runtime commands

Policy execution always receives an explicit trusted connections file:

```bash
s1flow decide --policy ticket-kind --state @state.json \
  --connections s1flow.toml --log "$RUNNER_TEMP/s1flow-log.jsonl" --json
s1flow feedback record ticket-kind DECISION_ID true \
  --connections s1flow.toml --log "$RUNNER_TEMP/s1flow-log.jsonl"
s1flow policy create spec.json --root policies
s1flow policy create spec.json --connections s1flow.toml --check
s1flow promote ticket-kind@v3 --root policies --connections s1flow.toml --json
```

The file passed to `--connections` is the complete allow-list for that invocation. Keep a dedicated
application file there; do not let an incoming policy choose a provider, import code, or discover a
connection beside itself. `decide --policy`, `feedback record`, `doctor --policy` and `promote` all
require this explicit binding. `policy create --check` validates the portable file without saving it;
with `--connections` it also checks the binding.

`decide --policy --json` returns a `Decision`, including `decision_id` and
`below_min_probability`. The latter is `null` when the policy has no lower bound, `true` when the
chosen value is below it, and `false` otherwise. The same names are written by `--github-output` for
an Action. Record feedback with the exact `decision_id`; `case_id` is only a context field on a log
entry and is allowed to repeat.

`promote` accepts `TASK@vN`, not a channel name. A valid policy with no evaluation record can be
promoted manually. When an evaluation record exists, it must still match the supplied model binding
and current execution conditions; the command reports the held-out test result. `--force` only
overrides a below test verdict, never stale evidence.

## Project and connection discovery

Use `--project PATH` and `--connections PATH` only where the command's `--help` lists them.
For those commands, they work before or after the subcommand:

```bash
s1flow --project ./repo --connections ./prod.toml decide --policy ticket-kind --state @state.json
s1flow decide --policy ticket-kind --state @state.json --project ./repo --connections ./prod.toml
```

`init`, `guide` and `skill` accept neither option. `policy create` accepts only
`--connections`; `policy export`, `cases check` and `cases correct` accept only `--project`.
An unsupported command option fails before the command runs. Offline `report --from` rejects both options.
An unevaluated `promote --root` rejects `--project`, since `--root` already selects its store.

`--project` selects the exact directory containing `s1flow.toml`, or a repository directory containing
`s1flow/s1flow.toml`. It does not change cwd, so `--connections`, `--log`, and other relative paths still
start at the invocation cwd. Without `--project`, the CLI searches upward from the invocation cwd to the
nearest Git boundary. Outside Git it searches only the cwd and cwd/`s1flow`; use `--project` from a deeper
directory. A missing project/config error names the search start and location and tells you which explicit
option to supply.

Commands that use connection configuration choose it in this order: explicit `--connections`, `S1FLOW_CONNECTIONS`, then
the selected project's `s1flow.toml`. These sources are alternatives; s1flow never merges them. Policy
execution, `promote`, and `feedback record` require explicit `--connections`, so `S1FLOW_CONNECTIONS` alone cannot
grant runtime access. CLI dotenv loading is limited to the selected project/root
and its nearest Git ancestor; the Python SDK never loads dotenv or uses this project discovery. The pre-release
rename removes `--models-file` without a compatibility alias.

The SDK constructor is explicit: use `Client(connections=...)` or `AsyncClient(connections=...)` for a string
alias, while a direct `ModelSpec` or `DecisionModel` needs no connection file. Relative SDK connection, cache,
and log paths are fixed when the object is constructed. `policies.load` requires `path=` or `root=` and
resolves an explicit policy path at load time.

Provider auxiliary-cache settings belong only to `Client(cache_dir=...)` or `AsyncClient(cache_dir=...)`.
`Lineup` contains configuration data and name/version resolution; it does not construct providers or
carry a cache directory. Use `client.connections.build()` / `.check()` for those runtime operations.
This provider cache is distinct from the evaluation's saved model answers.

## Names and development commands

A policy reference is `TASK`, `TASK@CHANNEL` or `TASK@vN` (`ticket-kind`, `ticket-kind@next`,
`ticket-kind@v3`). The unqualified form uses the `current` channel. `feedback record` takes the
policy reference, the exact `decision_id`, then the label.

Evaluation commands need the explicit evaluation extra. Prompt optimization is named so that it is
clear what changes:

```bash
uv tool install 's1flow[eval,optimize]'
s1flow run <task> --models <model>:<version>
s1flow report <task>                         # the candidates by the objective, the ranking's pick marked
s1flow optimize <task>                       # propose a changed question
s1flow check <task> --candidate next         # final test comparison
```

`report` is the one view of the saved development runs, for terminal readers and agents; it includes the base
question plus every task variant (it replaces `compare` and `rank`):

```bash
s1flow report <task>                          # the candidates by the task's objective
s1flow report <task> --json --limit 20 --offset 12
s1flow report <task> --candidate model:version/variant
s1flow report <task> --out DIR                # DIR/comparison.json (with chart arrays) and DIR/<variant>.md
s1flow report --from DIR/comparison.json --json  # offline; no rescoring or live certification
```

`--json` and text are bounded views of the same candidate IDs and numerical evidence. `--out` keeps stdout
compact and writes the full snapshot. `--from` reads only that snapshot and accepts the same pagination or exact
candidate selectors. A snapshot is development-scoped; it does not read the held-out test share, call a model,
or activate a policy. Use `references/charts.md` to render it for human inspection.

`candidate` names such as `model:version/variant` belong to evaluation. They are not fields in the
runtime `PolicySpec`; a saved runtime specification names only its registered `connection`, exact
`model_id`, question and rule.

Commands with `--json` emit machine-readable results for `tasks`, `models`, `doctor`, `adopt`,
`promote`, `check`, `report`, `cases review`, `feedback measure`, `optimize` and `decide`, and for
`policy create`. Other commands
print their verdict and use the exit code; commands that write files name the files they wrote.
