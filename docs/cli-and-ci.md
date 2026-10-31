# CLI, agents and CI

## The CLI

Every command has `--help`. Add `--json` for machine-readable output; notices and errors go to stderr. Exit code 0
means success, 1 means a gate failed or something was found, and 2 means usage, configuration, could not run, or a
pending check. To tell a pending check from an error, read `verdict` in `check --json`.

## The Agent Skill

Install the Skill as step 2 of the [quick start](../README.md#quick-start) shows. The plugin also carries a Cursor
manifest and follows the Agent Plugins format, for teams that import it into a Cursor team marketplace. `SKILL.md`
says which of its six references (collect, measure, ship, app, learn, setup) to read at each stage. It lives in
`plugin/skills/s1flow/`, which the plugin and the package both carry. The Skill drives collecting cases, comparing,
reviewing and improving through the same CLI; it isn't a second implementation.

Given a request like the one in the quick start, the Skill fetches the issues with its `github.py` script, then
runs `cases check`, `run` and `report`, and leaves the choice of candidate to you.

## GitHub Actions

`decide/action.yml` uses the base package and an explicit `connections` input, and outputs `answer`,
`probability`, `below_min_probability`, `decision_id` and `policy`. Evaluation uses `action.yml` with the `eval`
extra, and `s1flow init --ci` writes the workflow for it: on a pull request that adopts a policy, it checks the
new version against the one the base branch ships and posts the result as a comment. What it compares, and when
it passes, fails or is pending, is in [Policies, evidence and releases](policies.md#evidence-and-releases).

Input is passed through files and environment variables, never pasted into shell commands. The workflow installs
the package you choose up front; loading a policy at runtime never installs anything. In production workflows,
pin the Action to a release tag or commit SHA, and the package to a version. See [examples/](../examples) for
workflows that call the decide Action.
