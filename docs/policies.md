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
date, and writes nothing when the candidate falls short on the test set: `--force` ships it anyway, and the
evaluation record marks it `forced`, with your reason as the why, but never mismatched identities. On the pull request, the `s1flow check` Action compares the version the base branch ships
with the one the pull request makes current, on today's test cases, and fails when it is worse.

The check asks both versions again rather than trusting what their evidence says, because the pull request could
have written that evidence. So a version adopted with `--force` fails the check like any other version below; the
comment shows that it was forced, by whom and why, and merging it anyway is a person's call. A version adopted with
`adopt --spec` has no evidence and is asked like any other. Going back to an older version that ran before the base
branch's current (the base commit's `history.jsonl` says so) is a rollback: the check measures it and shows the
numbers, but passes, even where it breaks a constraint (a rollback restores what ran; the person decides it).
Adopting again a newer version that was rolled back from is checked as usual. A pull request that rewrites, renames or
removes a saved `vN.json` or `vN.evaluation.json` fails (and so does one whose files cannot be listed): versions are never rewritten, so both versions the check
reads are the ones that shipped. A check that cannot measure (a pull request from a fork gets no keys, and some answers are not
cached) is pending; the workflow `s1flow init --ci` writes fails on it (`on-pending: fail`; `warn` lets it pass).
When the pull request edits a file under `tasks/<task>/` (`task.py`, `split.json`, the cases, their corrections)
or `s1flow.toml`, which set the rules and the cases the check applies, the comment says so: the check used the
edited files, so review that diff.

A policy that was never evaluated, written by hand, is saved and made current by `adopt --spec FILE --reason
"..."` with only the base runtime; s1flow reports that there is no evidence for it.

To roll back, `s1flow adopt TASK@vN --reason "..."` points `current` at the older version; versions are never
rewritten, so the older one is still there. Open the pull request with that change.

Only `adopt` points `current`, and each time it does, it appends why to `policies/<task>/history.jsonl` (when,
which version, the one before, who, why, and for a measured candidate the held-out test's verdict). A candidate it
refuses because the held-out test shows it below gets a line too, so trying candidates on the test share until
one passes leaves a trace.

```bash
s1flow adopt --spec spec.json --reason "hand-written first rule" --json
s1flow adopt ticket-bug@v1 --reason "v2 misreads feature requests"
s1flow export ticket-bug --out policies.json
```

## Exporting and deploying

An exported policy set contains the policies and their content digests, but no evaluation data or credentials.
The app that receives it supplies its own connection file. A digest shows the content is unchanged; it doesn't
show who approved it. Ship policies through your app's normal, trusted release process. A policy can't load
remote code or install packages.

## Schemas

The public JSON Schemas in `schema/` are generated from the types: `policy-2.json`, `policy-evaluation-3.json`,
`policy-set-2.json`, `decision-2.json`, `log-2.json`, `history-1.json` and `run-2.json`. JSON Schema only checks structure. Use
`s1flow adopt --spec FILE --check` for checks across fields, such as whether the positive option you set on a choice
question works with a threshold, and to check the policy against a connection file. `policy-evaluation-2.json`
stays for records earlier versions wrote: s1flow still reads them, as `@3` records.
