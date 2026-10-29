# Policies, evidence and promotion

A policy is the specification your app runs. Evaluation records sit next to it, and channels say which version
is live: `current` is the version your app runs by default, `adopt` points `next` at the candidate you chose,
and you can name other channels yourself.
This page covers how the three fit together, and when `promote` refuses.

## Files

```
policies/ticket-bug/v1.json             the PolicySpec your app runs
policies/ticket-bug/v1.evaluation.json  the evaluation and selection record, if there is one
policies/ticket-bug/channels.json       which version each channel (current, next, ...) points to
```

## Evidence and promotion

An evaluation record points to the policy's digest and to fingerprints of how it ran, the dataset, the input
adapter and the evaluation contract. Changing the evaluation code, objectives, constraints, scoring code,
declared prices or the split invalidates an old shortlist or adoption record, so rescore and adopt again.
Evaluation records never change the policy itself, and the runtime never reads them.

`adopt` records the chosen candidate and your reason; `promote` changes a channel. Promoting an evaluated policy
is refused if its evidence is out of date, and normally refused if it fell short on the test set. `--force` can
override a test-set shortfall, but never mismatched identities. You can also promote a policy that has never been
evaluated, using only the base runtime; s1flow reports that there is no evidence for it.

```bash
s1flow promote ticket-bug@v1 --root policies --connections connections.toml --json
s1flow policy export ticket-bug --out policies.json
```

## Exporting and deploying

An exported policy set contains the policies and their content digests, but no evaluation data or credentials.
The app that receives it supplies its own connection file. A digest shows the content is unchanged; it doesn't
show who approved it. Ship policies through your app's normal, trusted release process. A policy can't load
remote code or install packages.

## Schemas

The public JSON Schemas in `schema/` are generated from the types: `policy-2.json`, `policy-evaluation-2.json`,
`policy-set-2.json`, `decision-2.json`, `log-2.json` and `run-2.json`. JSON Schema only checks structure. Use
`s1flow policy validate` for checks across fields, such as whether the positive option you set on a choice
question works with a threshold, and to check the policy against a connection file.
