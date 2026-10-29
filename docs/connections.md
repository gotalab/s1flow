# Connections and discovery

A connection file is your app's list of the models it is allowed to call. This page explains which file is
trusted, and how the SDK and the CLI find it.

## The connection file

The TOML format uses `default` and `[models.NAME]` sections (see the example in
[Run decisions in your app](app.md#your-first-decision)). A connection can also point to a custom provider that
your app implements.

The whole file you pass is the set of allowed models, so give production its own file rather than a research
catalog full of unrelated credentials. A policy can't supply a provider import, an endpoint URL, or a credential
name or value, and s1flow never merges a project catalog into your app's file.

## The SDK

`Client()` and `AsyncClient()` don't look for a project or config file, `S1FLOW_CONNECTIONS`, `.env`, or a
built-in catalog. Providers still read their own API key variables when a configured model needs them.

Pass `connections=` when a direct call names a model by an alias such as `"triage"`. A `ModelSpec` or
`DecisionModel` passed directly is already explicit and needs no connection file. The connections are available
as `client.connections`.

Relative paths for `connections`, the cache and the log are resolved against the working directory when the
client or policy is created. The SDK never loads dotenv files. `policies.load` needs an explicit `path=` or
`root=`. It never looks for a policy in the current project, and it resolves an explicit policy path when
`load` is called.

`cache_dir` is optional and only applies to `Client` and `AsyncClient`. Providers use it for supporting data
such as price lists. s1flow never uses it to reuse model answers at runtime; evaluation has its own answer
cache. `s1flow.client.lineup.Lineup.read(path)` only reads configuration: pass cache settings to the client, and use
`client.connections.build()` or `.check()` to build or check providers.

## The CLI

The CLI accepts `--project PATH` and `--connections PATH` only on commands that list them in `--help`. On those
commands, the option can go before or after the subcommand. An option a command doesn't take is an error before
anything runs: `policy create`, for example, takes `--connections` but not `--project`.

`--project` must point exactly at a directory that contains `s1flow.toml`, or at a repository that contains
`s1flow/s1flow.toml`; it doesn't search upward. It doesn't change the working directory, so other relative paths in the command are still
resolved from where you ran it. Without `--project`, the CLI searches upward from the current directory to the
nearest Git root. Outside a Git repository, it only checks the current directory and `./s1flow`, so use
`--project` when you run it from deeper inside.

Evaluation commands pick a connection file in this order: `--connections`, then `S1FLOW_CONNECTIONS`, then the
selected project's `s1flow.toml`. Running a policy, `promote` and `feedback record` all require an explicit
`--connections`. `S1FLOW_CONNECTIONS` is read only by the CLI, and on its own it never allows a policy to run.

The CLI only loads `.env` files from the selected project or root and the directories above it, up to the
nearest Git root. When it can't find a
project, the error says where the search started and where it looked, and suggests `--project PATH` or
`--connections PATH`.
