# CLI, agents and CI

## The CLI

Every command has `--help`. Add `--json` for machine-readable output; notices and errors go to stderr. Exit code 0
means success, 1 means a gate failed or something was found, and 2 means usage, configuration or could not run.

## The Agent Skill

Install the Skill as [Get started](get-started.md#add-the-skill-to-your-coding-agent) shows. The plugin also carries a Cursor
manifest and follows the Agent Plugins format, for teams that import it into a Cursor team marketplace. `SKILL.md`
says which of its six references (collect, measure, ship, app, learn, setup) to read at each stage. It lives in
`plugin/skills/s1flow/`, which the plugin and the package both carry. The Skill drives collecting cases, comparing,
reviewing and improving through the same CLI; it isn't a second implementation.

Given a request like the one in the quick start, the Skill fetches the issues with its `github.py` script, then
runs `cases check`, `run` and `report`, and leaves the choice of candidate to you.

## GitHub Actions

`decide/action.yml` uses the base package and an explicit `connections` input, and outputs `answer`,
`probability`, `below_min_probability`, `decision_id` and `policy`. Evaluation has no Action: `adopt` tests the
candidate on the held-out test cases where you run it, and the pull request carries the result
([Policies, evidence and releases](policies.md#evidence-and-releases)).

After `actions/checkout` and a step that writes the state as JSON, a workflow calls it like this (`s1flow/` holds
the project's `policies/` and `s1flow.toml`):

```yaml
      - id: s1
        uses: gotalab/s1flow/decide@v0.1.0a6
        with:
          working-directory: s1flow
          policy: gh-myrepo-bug                   # the task's current version
          state: ${{ steps.state.outputs.json }}  # JSON in the shape the task was evaluated on
          connections: s1flow.toml                # the models this workflow lets the policy call
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
      - if: steps.s1.outputs.below_min_probability != 'true'
        env:
          ANSWER: ${{ steps.s1.outputs.answer }}
        run: echo "act on $ANSWER here"
```

Input is passed through files and environment variables, never pasted into shell commands. The workflow installs
the package you choose up front; loading a policy at runtime never installs anything. In production workflows,
pin the Action to a release tag or commit SHA, and the package to a version. See [examples/](https://github.com/gotalab/s1flow/tree/main/examples) for
workflows that call the decide Action.
