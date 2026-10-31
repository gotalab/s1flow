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

`Client()` and `AsyncClient()` don't look for a project or config file, `.env`, or a
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
cache. Reading a connection file builds nothing: use `client.connections.build()` or `.check()` to build or check
providers.

## The CLI

`s1flow COMMAND --help` lists whether the command takes `--project PATH` and `--connections PATH`.

`--project` must point exactly at a directory that contains `s1flow.toml`, or at a repository that contains
`s1flow/s1flow.toml`; it doesn't search upward. Without `--project`, the CLI searches upward from the current directory to the
nearest Git root. Outside a Git repository, it only checks the current directory and `./s1flow`, so use
`--project` when you run it from deeper inside.

Evaluation commands use `--connections` when given, else the selected project's `s1flow.toml`. `decide --policy`, `feedback record`, `doctor --policy`, and `adopt --spec --root` need an explicit
`--connections`.

The CLI reads `.env` in the project directory (or cwd with no project) and every directory above it up to the
Git root, nearest first; a variable already set wins. When it can't find a
project, the error says where the search started and where it looked, and suggests `--project PATH` or
`--connections PATH`.
