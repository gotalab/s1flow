# Decision logs

A bound policy writes one JSON line per event to the file given to `policies.load(..., log=...)`,
`decide --log`, or the decide Action's `log` input. `s1flow feedback measure <task> <files>` reads
these v2 events. Write them through s1flow rather than by hand. There are three record types:

An answered call contains the reading, a unique `decision_id`, the policy and execution digests, and
the model that answered. `case_id` is optional context and may repeat. `state` is `null` unless the
caller deliberately requested `keep_state`.

```json
{"schema":"s1flow/log@2","type":"answered","at":"2026-10-24T05:00:00.000Z","case_id":"#1234","state_sha256":"414b0331802d5a2e22476b79c6633f951f5c2f032bf4ef49253f14fe07181ea5","state":null,"decision":{"value":true,"probability":0.91,"below_min_probability":false,"p_positive":0.91,"distribution":null,"expected":null,"confidence":null,"decision_id":"dec-1234-1","policy":"gh-myrepo-bug@v1","policy_digest":"32473886e6de42a8aee35bd0d35def4024970807c5a513519f3a58e9cc5eefde","answered_by":"typesafe/jev-1.14-20261014","latency_ms":391.2,"execution_digest":"a4f5b3b2d5c6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f70","response":{"answers":{"bug":{"type":"boolean","probability":0.91}},"answered_by":"typesafe/jev-1.14-20261014","usage":{"input_tokens":412,"output_tokens":0,"cost_usd":0.000017,"cost_source":"billed","raw":null},"latency_ms":388.0,"retries":null,"provider_metadata":{}}}}
```

A failed call has no `decision_id`; its `state_sha256`, policy digest and error are still recorded.

```json
{"schema":"s1flow/log@2","type":"failed","at":"2026-10-24T05:01:00.000Z","case_id":"#1235","state_sha256":"9f2c000000000000000000000000000000000000000000000000000000000000","policy":"gh-myrepo-bug@v1","policy_digest":"32473886e6de42a8aee35bd0d35def4024970807c5a513519f3a58e9cc5eefde","error":"ProviderError: HTTP 401 from openrouter.ai"}
```

Feedback learned later points to the exact answered event by `decision_id`. It has no `case_id`:

```json
{"schema":"s1flow/log@2","type":"feedback","at":"2026-10-24T09:30:00.000Z","decision_id":"dec-1234-1","policy":"gh-myrepo-bug@v1","policy_digest":"32473886e6de42a8aee35bd0d35def4024970807c5a513519f3a58e9cc5eefde","label":true}
```

`below_min_probability` is `null` when no lower bound is configured, otherwise `true` or `false`.
It is an output signal for the caller, not a refusal and not a claim that the label is correct.

The complete schema is [`schema/log-2.json`](https://github.com/gotalab/s1flow/blob/main/schema/log-2.json).
In Python, inspect the same contract with
`pydantic.TypeAdapter(s1flow.policies.log.Log).json_schema()`. OpenTelemetry exports the same three
records through `s1flow.decide` and `s1flow.feedback`; records without the v2 identity fields are not
reconstructed as current decisions.
