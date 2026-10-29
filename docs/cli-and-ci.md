# CLI, agents and CI

## The CLI

Every command has `--help`. Add `--json` for machine-readable output; notices and errors go to stderr. Exit code 0
means success, 1 means a gate failed (for example, a policy fell short of
its target), and 2 means invalid input or configuration, or a check that couldn't finish. To tell a pending result from a configuration error, read the `status` or `verdict` field in the JSON.

## The Agent Skill

The Skill ships as a plugin for Claude Code (`/plugin marketplace add gotalab/s1flow`, then
`/plugin install s1flow@s1flow`) and for Codex (`codex plugin marketplace add gotalab/s1flow`). The plugin also
carries a Cursor manifest and follows the Agent Plugins format, for teams that import it into a Cursor team
marketplace. For any other agent, `s1flow skill install` copies the Skill into `.agents/skills/` and
`.claude/skills/` at the Git root (`--user` puts it in your home directory instead). `s1flow init` never installs
it. `s1flow guide` lists its topic guides. The source lives in `skills/s1flow/`, and `scripts/sync_plugin.py`
writes the plugin copy. The Skill
drives collecting cases, comparing, reviewing and improving through the same CLI; it isn't a second
implementation.

A typical request to your agent: *"Use s1flow to decide whether a new GitHub issue is a bug. Call the task is-bug,
collect 200 labeled issues, compare the models and show me the result."* The Skill runs `s1flow github fetch`, `cases check`, `run`
and `compare`, and leaves the choice of candidate to you.

## GitHub Actions

`decide/action.yml` uses the base package and an explicit `connections` input, and outputs the decision ID and
whether the answer cleared the threshold. Evaluation uses `action.yml` with the `eval` extra (`s1flow init --ci` writes a workflow for it): on a pull request
that changes a policy, it tests the new policy against the current one on the test cases and posts the result as a comment.

Input is passed through files and environment variables, never pasted into shell commands. The workflow installs
the package you choose up front; loading a policy at runtime never installs anything. In production workflows,
pin the Action to a release tag or commit SHA, and the package to a version. See [examples/](../examples) for
example workflows.
