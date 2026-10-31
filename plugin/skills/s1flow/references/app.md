# App: call a policy, log it, export it

## Connections

An application owns its trusted model connections. The file passed as `connections` is the complete allow-list
for that call: every connection in it is granted. Keep a dedicated file for the app. A policy cannot choose a
provider, import code, or find a connection beside itself. The SDK never discovers a project, never reads
`.env`, and never installs packages from a policy or input.

## Python

Anchor paths to the file, so starting the app from another directory changes nothing:

```python
from pathlib import Path
from s1flow import Client, policies

APP = Path(__file__).resolve().parent
client = Client(connections=APP / "connections.toml")  # grants every connection listed in this file
policy = policies.load(path=APP / "policies/ticket-kind/v1.json", client=client,
                       log=APP / "decisions.jsonl")
decision = policy.decide({"title": "...", "body": "..."}, case_id="issue-123")
print(decision.value, decision.probability, decision.below_min_probability, decision.decision_id)

policy.feedback(decision.decision_id, True)   # when the right label is known: the exact id returned above
```

- `policies.load` needs `path=` or `root=`; `policies.load("<task>", path="policies.json", client=client)` reads
  an exported set. `keep_state=True` keeps the state in the log so `feedback measure --add` can use it.
- `Client(connections=...)` / `AsyncClient(connections=...)` for a string alias; a direct `ModelSpec` or
  `DecisionModel` needs no file. Relative paths are fixed when the object is built. Provider cache settings go only
  in `Client(cache_dir=...)`. `client.connections.build()` / `.check()` run the connection checks.
- The direct `Client` asks boolean, choice, score and box questions where the provider supports them; a policy
  holds one boolean or choice.
- Store `decision_id` when a label may arrive later. `case_id` is log context only and may repeat.

## Low-probability answers

`below_min_probability` is `None` when the policy has no `min_probability`, `True` below it, `False` at or above.
It is a signal, not a refusal. What the app does with such an answer (send it to a person, a default label, do
nothing) is the app's decision: ask the person, or follow `criteria.md`, and do not pick one yourself.

## CLI

```bash
s1flow decide --policy ticket-kind --state @state.json \
  --connections s1flow.toml --log "$RUNNER_TEMP/s1flow-log.jsonl" --json
s1flow decide --model jev --boolean "Is this a bug report?" --state @state.json   # a model, no policy
```

`--policy` always needs explicit `--connections`. `--json` prints the `Decision` (with `decision_id` and
`below_min_probability`, `null` / `true` / `false`); `--github-output` writes `answer`, `probability`,
`below_min_probability`, `decision_id`, `policy`. `--path` reads a policy file or `policies.json`;
`--keep-state` keeps the state in the log; `--case-id` is log context.

## GitHub Actions

`gotalab/s1flow/decide@v0.1.0a1` answers one case. Required inputs: `policy`, `state`, `connections`. Optional:
`case-id`, `log`, `keep-state`, `path`, `working-directory`, `package`. Outputs: `answer`, `probability`,
`below_min_probability`, `decision_id`, `policy`. It installs s1flow in the workflow when the repository does not
list it. Keys stay in repository secrets. A failed step has no decision to record, so `continue-on-error` leaves
the case unchanged. Keep untrusted text in environment variables and pass it to `jq --arg`, never into shell source:

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

The `needs-triage` branch is one app's choice for low-probability answers; ask what yours should do. Recording
the label later is in `learn.md`. If the label arrives in a separate event, look up the saved `decision_id`; never
substitute an issue number for it.

## Another repository or language: export

```bash
s1flow export [tasks...] --out policies.json   # each task's current policy and its digest, in one file
```

The app vendors `policies.json` and reviews changes to it in its own pull requests. Python reads it with
`policies.load(task, path=...)`; the decide Action and `decide --path` take it too. Another language reads the
policy and log JSON Schemas in the [schema directory](https://github.com/gotalab/s1flow/tree/main/schema).

## Decision logs

A bound policy writes one JSON line per event to `log=`, `decide --log` or the Action's `log`. Write them through
s1flow, not by hand. `feedback measure` reads them. Three record types (schema `s1flow/log@2`):

An answered call has a unique `decision_id`, the policy and execution digests and the model that answered.
`state` is `null` unless `keep_state` was asked for.

```json
{"schema":"s1flow/log@2","type":"answered","at":"2026-10-24T05:00:00.000Z","case_id":"#1234","state_sha256":"414b0331802d5a2e22476b79c6633f951f5c2f032bf4ef49253f14fe07181ea5","state":null,"decision":{"value":true,"probability":0.91,"below_min_probability":false,"p_positive":0.91,"distribution":null,"expected":null,"confidence":null,"decision_id":"dec-1234-1","policy":"gh-myrepo-bug@v1","policy_digest":"32473886e6de42a8aee35bd0d35def4024970807c5a513519f3a58e9cc5eefde","answered_by":"typesafe/jev-1.14-20261014","latency_ms":391.2,"execution_digest":"a4f5b3b2d5c6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f70","response":{"answers":{"bug":{"type":"boolean","probability":0.91}},"answered_by":"typesafe/jev-1.14-20261014","usage":{"input_tokens":412,"output_tokens":0,"cost_usd":0.000017,"cost_source":"billed","raw":null},"latency_ms":388.0,"retries":0,"provider_metadata":{}}}}
```

A failed call has no `decision_id`; its `state_sha256`, policy digest and error are recorded.

```json
{"schema":"s1flow/log@2","type":"failed","at":"2026-10-24T05:01:00.000Z","case_id":"#1235","state_sha256":"9f2c000000000000000000000000000000000000000000000000000000000000","policy":"gh-myrepo-bug@v1","policy_digest":"32473886e6de42a8aee35bd0d35def4024970807c5a513519f3a58e9cc5eefde","error":"ProviderError: HTTP 401 from openrouter.ai"}
```

Feedback points to the answered event by `decision_id`, and has no `case_id`:

```json
{"schema":"s1flow/log@2","type":"feedback","at":"2026-10-24T09:30:00.000Z","decision_id":"dec-1234-1","policy":"gh-myrepo-bug@v1","policy_digest":"32473886e6de42a8aee35bd0d35def4024970807c5a513519f3a58e9cc5eefde","label":true}
```

The full schema is [`schema/log-2.json`](https://github.com/gotalab/s1flow/blob/main/schema/log-2.json); in
Python, `pydantic.TypeAdapter(s1flow.policies.log.Log).json_schema()`. OpenTelemetry exports the same three
records through `s1flow.decide` and `s1flow.feedback`.
