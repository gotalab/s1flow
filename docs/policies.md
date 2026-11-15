# Policies, evidence and releases

A policy is the specification your app runs. Evaluation records sit next to it, and `channels.json` names the
`current` version, the one your app runs. `adopt` saves the candidate you chose as a new version and makes it
current in your working tree; the pull request that carries that change is the review, and merging it is the
release.
This page covers how the three fit together, and when `adopt` refuses.

## Files

```
policies/ticket-bug/v1.json             the PolicySpec your app runs
policies/ticket-bug/v1.evaluation.json  the evaluation and selection record, if there is one
policies/ticket-bug/channels.json       {"schema": "s1flow/channels@1", "channels": {"current": 3}}: the version that runs
policies/ticket-bug/history.jsonl       one line per switch of current, and per refused candidate: when, which version, who, why
```

## Evidence and releases

An evaluation record points to the policy's digest and to fingerprints of how it ran, the dataset, the input
adapter and the evaluation contract. Changing the evaluation code, objectives, constraints, scoring code,
declared prices or the split invalidates an old shortlist or adoption record, so rescore and adopt again.
Evaluation records never change the policy itself, and the runtime never reads them.

`adopt` records the chosen candidate and your reason, and makes it current. It refuses evidence that is out of
date, and writes nothing when the candidate falls short on the test set: `--force` ships it anyway, and the
evaluation record marks it `forced`, with your reason as the why. `--force` overrides only the held-out test,
never stale evidence. That held-out test is the one pass or fail s1flow gives a policy before it ships. The pull
request that carries the new version shows the result in `vN.evaluation.json` and `history.jsonl`, and merging it is
a person's call.

A saved `vN.json` or `vN.evaluation.json` is never rewritten, renamed or removed: `adopt` only adds a version, so
the version an app ran can always be read again as it shipped.

A policy that was never evaluated, written by hand, is saved and made current by `adopt --spec FILE --reason
"..."` with only the base runtime; s1flow reports that there is no evidence for it.

To go back to a version that ran before, save it again as the next version: `adopt --spec` with its `vN.json`
renumbered brings back exactly that spec, unevaluated; `s1flow adopt TASK CANDIDATE` with its candidate measures
that candidate again on today's task, question and cases. Don't revert the pull request that adopted the newer
version: that removes a saved version.

Only `adopt` points `current`, and each time it does, it appends why to `policies/<task>/history.jsonl` (when,
which version, the one before, who, why, and for a measured candidate the held-out test's verdict). A candidate it
refuses because the held-out test shows it below gets a line too, so trying candidates on the test share until
one passes leaves a trace.

```bash
s1flow adopt --spec spec.json --reason "hand-written first rule" --json
s1flow adopt ticket-bug d1@vercel/short --reason "v2 misreads feature requests"
s1flow export ticket-bug --out policies.json
```

## Exporting and deploying

An exported policy set contains the policies and their content digests, but no evaluation data or credentials.
The app that receives it supplies its own connection file. A digest shows the content is unchanged; it doesn't
show who approved it. Ship policies through your app's normal, trusted release process. A policy can't load
remote code or install packages.

## Schemas

The public JSON Schemas in `schema/` are generated from the types (`scripts/write_schemas.py`): the policy, an
exported policy set, the decision log, a decision and a response, a case, a run, the split, the comparison, the
evaluation record and the history. JSON Schema only checks structure. Use
`s1flow adopt --spec FILE --check` for checks across fields, such as whether the positive option you set on a choice
question works with a threshold, and to check the policy against a connection file.
