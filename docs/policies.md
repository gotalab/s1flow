# Policies, evidence and releases

A policy is the specification your app runs. Evaluation records sit next to it, and `channels.json` names the
`current` version, the one your app runs. `adopt` saves the candidate you chose as a new version and makes it
current in your working tree; the pull request that carries that change is the review, and merging it is the
release. There is no separate switch to flip after the merge.
This page covers how the three fit together, and when `adopt` refuses.

## Files

```
policies/ticket-bug/v1.json             the PolicySpec your app runs
policies/ticket-bug/v1.evaluation.json  the evaluation and selection record, if there is one
policies/ticket-bug/channels.json       {"channels": {"current": 3}}: the version that runs
```

## Evidence and releases

An evaluation record points to the policy's digest and to fingerprints of how it ran, the dataset, the input
adapter and the evaluation contract. Changing the evaluation code, objectives, constraints, scoring code,
declared prices or the split invalidates an old shortlist or adoption record, so rescore and adopt again.
Evaluation records never change the policy itself, and the runtime never reads them.

`adopt` records the chosen candidate and your reason, and makes it current. It refuses evidence that is out of
date, and writes nothing when the candidate falls short on the test set: `--force` ships it anyway, but never
mismatched identities. On the pull request, the `s1flow check` Action compares the version the base branch ships
with the one the pull request makes current, on today's test cases, and fails when it is worse.

A policy that was never evaluated, written by hand and saved with only the base runtime, is current as soon as
`policy create` saves it; s1flow reports that there is no evidence for it.

To roll back, point `current` in `channels.json` at the older version in a pull request; versions are never
rewritten, so the older one is still there.

```bash
s1flow policy create spec.json --root policies --connections connections.toml --json
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
`s1flow policy create --check` for checks across fields, such as whether the positive option you set on a choice
question works with a threshold, and to check the policy against a connection file.
