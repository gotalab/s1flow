# Call a policy from a workflow or another language

## GitHub Actions

The `gotalab/s1flow/decide@v0.1.0a1` Action answers one case with a v2 policy. Its required inputs are
`policy`, `state` and `connections`. The connections file is a trusted application allow-list: every
connection listed there is granted to this invocation. Optional inputs are `case-id` (log context),
`log`, `keep-state`, `path`, `working-directory` and `package`.

The outputs are `answer`, `probability`, `below_min_probability`, `decision_id` and `policy`.
`below_min_probability` is `null` when the policy has no lower bound, otherwise `true` or `false`.
Keep `decision_id` with the case. When a label is learned, pass that exact value to
`feedback record`; `case-id` can repeat and is not a feedback key. A failed Action has no decision
to record, so `continue-on-error` is useful when the workflow should leave the case unchanged.

The Action installs the requested package as part of workflow setup when the repository does not list
s1flow. The Python SDK never installs packages from a policy or input data. The model keys stay in
repository secrets; `s1flow doctor --policy TASK --connections s1flow.toml` names the variables and
hosts without printing values.

This example keeps issue text in environment variables and passes it to `jq --arg`; it never places
untrusted text in shell source:

```yaml
name: s1flow label issues
on:
  issues:
    types: [opened]
permissions:
  contents: read
  issues: write
jobs:
  decide:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - id: state
        env:
          TITLE: ${{ github.event.issue.title }}
          BODY: ${{ github.event.issue.body }}
        run: |
          {
            echo 'json<<S1FLOW_EOF'
            jq -cn --arg t "$TITLE" --arg b "${BODY:0:2000}" '{title: $t, body: $b}'
            echo 'S1FLOW_EOF'
          } >> "$GITHUB_OUTPUT"
      - id: s1
        uses: gotalab/s1flow/decide@v0.1.0a1
        continue-on-error: true
        with:
          working-directory: s1flow
          policy: gh-myrepo-bug
          state: ${{ steps.state.outputs.json }}
          connections: s1flow.toml
          case-id: "#${{ github.event.issue.number }}"
          log: ${{ runner.temp }}/s1flow-log.jsonl
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
      - name: Act on the answer
        if: steps.s1.outcome == 'success'
        env:
          GH_TOKEN: ${{ github.token }}
          ISSUE: ${{ github.event.issue.number }}
          ANSWER: ${{ steps.s1.outputs.answer }}
          BELOW_MIN_PROBABILITY: ${{ steps.s1.outputs.below_min_probability }}
          DECISION_ID: ${{ steps.s1.outputs.decision_id }}
        run: |
          if [ "$BELOW_MIN_PROBABILITY" = true ]; then
            label=needs-triage
          else
            label="area:$ANSWER"
          fi
          gh label create "$label" --force -R "$GITHUB_REPOSITORY" >/dev/null
          gh issue edit "$ISSUE" -R "$GITHUB_REPOSITORY" --add-label "$label"
          echo "decision_id=$DECISION_ID -> $label" >> "$GITHUB_STEP_SUMMARY"
      - uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2
        with:
          name: s1flow-log-${{ github.run_id }}
          path: ${{ runner.temp }}/s1flow-log.jsonl
```

When the right label is known, use the id saved with the case:

```bash
s1flow feedback record gh-myrepo-bug "$DECISION_ID" "$LABEL" \
  --connections s1flow.toml --log "$RUNNER_TEMP/s1flow-log.jsonl"
```

If the label arrives in a separate event, the application can look up the saved id or deliberately
call the policy again in that event and record the new call's returned id. Do not substitute an issue
number for it. Keep the answered and feedback logs together, then measure them with
`s1flow feedback measure gh-myrepo-bug logs/*.jsonl`.

## Without s1flow

- `s1flow policy export --out policies.json` writes a runtime-only policy set for an application to
  vendor and review. `policies.load("<task>", path="policies.json", client=client)` reads it with an
  explicit `Client`.
- The JSON Schemas for policies, logs and runs are in the public
  [s1flow schema directory](https://github.com/gotalab/s1flow/tree/main/schema). The v2 log contract is
  [log-2.json](https://github.com/gotalab/s1flow/blob/main/schema/log-2.json).
