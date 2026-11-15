# Ship: adopt and the pull request

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
  revert the adopt pull request: that removes a saved version.
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

Open a pull request with the change to `policies/<task>/` (and `tasks/<task>/` if `task.py` or `split.json`
changed). The body says:

- the task and the switch (`v3 -> v4`, or an unevaluated `--spec`);
- the reason, as recorded;
- the report lines for the adopted candidate and what it was chosen over, below-target ones included;
- the held-out test verdict `adopt` printed (`kept`, `inconclusive`, or `below` with `--force`) and its numbers;
- that merging releases it, and that merging is the person's call.

Edits under `tasks/<task>/` or to `s1flow.toml` change what the next run measures: say so in the PR body. Never
edit a saved `vN.json` or `vN.evaluation.json`; adopt a new version instead.

Bring the person the verdict, and leave the merge to them.
