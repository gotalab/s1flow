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
policies/ticket-bug/history.jsonl       one line per adopt: when, which version, the one before, who, why
```

## Evidence and releases

An evaluation record points to the policy's digest and to fingerprints of how it ran, the dataset, the input
adapter and the evaluation contract. Changing the evaluation code, objectives, constraints, scoring code,
declared prices or the split invalidates an old shortlist or adoption record, so rescore and adopt again.
Evaluation records never change the policy itself, and the runtime never reads them.

`adopt` records the chosen candidate and your reason, and makes it current. It refuses evidence that is out of
date, and writes nothing when the candidate falls short on the test set: `--force` ships it anyway, and the
evaluation record marks it `forced`, with your reason as the why. `--force` overrides only the held-out test,
never stale evidence. On the pull request, the `s1flow check` Action compares the version the base branch ships
with the one the pull request makes current, on today's test cases, and fails when it is worse.

The check asks both versions again rather than trusting what their evidence says, because the pull request could
have written that evidence. So a version adopted with `--force` fails the check like any other version below; the
comment shows that it was forced, by whom and why, and merging it anyway is a person's call. A pull request that rewrites, renames or
removes a saved `vN.json` or `vN.evaluation.json` fails (and so does one whose files cannot be listed): versions are never rewritten, so both versions the check
reads are the ones that shipped. A check that cannot measure (a pull request from a fork gets no keys, and some answers are not
cached) is pending; the workflow `s1flow init --ci` writes fails on it (`on-pending: fail`; `warn` lets it pass).
When the pull request edits a file under `tasks/<task>/` (`task.py`, `split.json`, the cases, their corrections)
or `s1flow.toml`, which set the rules and the cases the check applies, the comment says so: the check used the
edited files, so review that diff.

A policy that was never evaluated, written by hand, is saved and made current by `adopt --spec FILE --reason
"..."` with only the base runtime; s1flow reports that there is no evidence for it.

To go back to a version that ran before, save it again as the next version: `adopt --spec` with its `vN.json`
renumbered brings back exactly that spec, unevaluated; `s1flow adopt TASK CANDIDATE` with its candidate measures
that candidate again on today's task, question and cases. Versions are only added, so the pull request is checked
as any adopt is; reverting the one that adopted the newer version would remove a saved version, which the check
Action refuses.

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

The public JSON Schemas in `schema/`, one per file s1flow reads or writes, are generated from the types. JSON
Schema only checks structure. Use
`s1flow adopt --spec FILE --check` for checks across fields, such as whether the positive option you set on a choice
question works with a threshold, and to check the policy against a connection file.
