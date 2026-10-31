# Ship: adopt, the pull request, check

`adopt` is the only command that changes which version is current. Merging the pull request that carries it is
the release.

## Who decides

Which candidate to adopt and whether to merge belong to the person. Read `tasks/<task>/criteria.md` first: when it
covers the choice, follow it and quote it in the reason; otherwise show the candidates (`measure.md`) and ask.
Never run `adopt` or merge on your own judgement, and never pass `--force` unless the person says so.

## Adopt

```bash
s1flow adopt <task> <candidate> --reason "..."    # write vN, make it current, append to history.jsonl
s1flow adopt --spec spec.json --reason "..."      # a runtime spec, saved unevaluated, made current
s1flow adopt --spec spec.json --check             # validate only; save nothing
```

- `adopt TASK CANDIDATE` scores the chosen candidate on the held-out test and records the result. If the held-out
  test shows it below (its constraint or floors broken, or worse than its train + val interval), nothing is written, exit 1, and `history.jsonl` gets a `refused` line.
  `--force` writes it anyway, marked `forced`; the reason must say why. Stale evidence is refused.
- `--spec` needs only the base install. `--spec` takes a `PolicySpec` (task/version, a trusted
  `connection` and exact `model_id`, one boolean or choice question, a rule, an optional input shape). It has no
  evaluation evidence. It always checks the binding: against the project's `s1flow.toml`, or `--connections FILE`.
- Outside an s1flow project (an app's repository), add `--root policies`, and `--connections FILE` with `--spec`.
- A saved `vN.json` is never overwritten. `channels.json` names the one `current` version.
- To go back to an older version, save it again as the next one: `adopt --spec` with its `vN.json` renumbered
  brings back exactly that spec; `adopt <task> <its candidate>` measures the candidate again on today's task. Never
  revert the adopt pull request: removing a saved version fails the check Action.
- Who adopted comes from `git config user.name`.

### The reason

The reason is kept in `history.jsonl` (and, for a candidate, in `vN.evaluation.json`), and `report` shows the last one. Write it for someone who
reads it a year later:

- who chose, and by what: "Picked by <person>" or "by criteria.md: <the rule>";
- what it was chosen over, with the numbers that decided it (the objective, and latency or cost if a tie was
  broken by them);
- for a forced version, why the test result is accepted.

Example: `"Picked by Ana: tied with gpt-x on ExpectedLoss(fn=3); half the p90 latency (410 vs 820 ms)."`

## The pull request

```bash
s1flow check <task> --against v<N>      # current against the version it replaces, on today's test cases
```

Open a pull request with the change to `policies/<task>/` (and `tasks/<task>/` if `task.py` or `split.json`
changed). The body says:

- the task and the switch (`v3 -> v4`, or an unevaluated `--spec`);
- the reason, as recorded;
- the report lines for the adopted candidate and what it was chosen over, below-target ones included;
- the `check` verdict and its numbers;
- that merging releases it, and that merging is the person's call.

## Read check

`check` is the CI gate (`init --ci` writes the workflow). It asks both versions again on the test cases and
compares them case by case; stored evidence never passes it. Exit 0 pass, 1 worse, 2 could not run or pending.

- **Worse** (exit 1): the new current loses on the test cases. Bring the numbers to the person.
- **Forced**: a version adopted with `--force` fails; the comment shows its reason. The person decides whether to
  merge anyway.
- **Pending** (exit 2): answers are needed that only a run with keys can get (`--cached-only`, a fork). The
  workflow `init --ci` writes sets `on-pending: fail`, so the check fails until it runs with keys.
- **A rewritten `vN.json`** fails: saved versions are immutable. Adopt a new version instead.
- **Edits under `tasks/<task>/` or to `s1flow.toml`** are flagged: they change what the next run measures. Say so
  in the PR body.

`--sample N` checks N test cases only (the workflow uses 40). `--markdown FILE` writes the PR comment.
`--candidate draft` checks the task's edited question before anything is adopted.

Bring the person the verdict, and leave the merge to them.
