# Evaluate and compare

Measure the same policy your app runs against your own labeled cases, compare models and prompts, and record
which one you picked. Your coding agent can do all of this through the s1flow Skill; this page is the reference
behind it.

## Install the evaluation tools

Install these in your development environment, not in the production image:

| Extra | What it adds |
|---|---|
| `eval` | numpy, scipy and scikit-learn for evaluation, comparison and reports |
| `llm` | LiteLLM, to compare against LLMs |
| `optimize` | the `eval` and `llm` extras plus GEPA, for prompt optimization |
| `images` | Pillow, for preparing images |
| `otel` | the OpenTelemetry API, for optional tracing spans |

```bash
uv tool install "s1flow[eval]"
```

## The commands

```bash
s1flow init --task ticket-bug   # add --ci for the pull request check
# Fill in tasks/ticket-bug/task.py and add labeled data in the generated s1flow/ project.
s1flow cases check ticket-bug
s1flow run ticket-bug
s1flow report ticket-bug
s1flow adopt ticket-bug MODEL --reason "why this candidate" --json   # the new version is current
# open a pull request: the s1flow check Action compares it with the version main ships; merging releases it
```

The first `s1flow run` on a task holds out its test share and writes `tasks/<task>/split.json`; commit it with
`task.py`, because `adopt`, `optimize` and the pull request check read that file and refuse without it. No other
command writes it. Cases added later are placed by a hash of their ID, so the file never moves.

`s1flow init` creates an `s1flow/` project and nothing else. With `--ci` it also writes a pull request check to
`.github/workflows/`; the Skill comes from the plugin or `s1flow skill install` (see
[CLI, agents and CI](cli-and-ci.md#the-agent-skill)). The project's line-up compares three decision models that all work with a single key, `OPENROUTER_API_KEY`
(about $0.02 per 1,000 calls on issue-sized inputs). Cases can come from GitHub issues, app logs or labels you
already have. Fetching cases from GitHub (the Skill's `scripts/github.py`) needs the `gh` CLI, installed and signed in.

A `Task` defines an evaluation: the data, how to read the label, the question, the objective, the constraints
and how to split the cases. Reuse your app's own input-preparation function, or replay the inputs your app
actually sent. Don't deploy `task.py` with your app. Evaluation and the runtime share the question types, answer
validation and decision rules; metrics and optimization live only in `s1flow.eval`.

## Compare candidates

`s1flow report` shows every model and question variant side by side, using only the development cases. The
terminal shows the candidates ordered by the task's objective, with the ranking's pick marked; `--json` adds every
metric of each candidate with the same candidate IDs and numbers, so a person, or an agent acting for them, can
choose based on their own criteria. (It replaces `compare` and `rank`.) The
final test-set result comes only when you adopt a candidate or run `check`.

`adopt --reason` records the choice and makes it current in your working tree; it goes live when the pull request
that carries it merges (see [Policies, evidence and releases](policies.md)).

`s1flow report ticket-bug --out DIR` saves `DIR/comparison.json`, a full snapshot of the development results
including the chart data, and a Markdown report per question (`DIR/questions/base.md`); it writes nothing else unless asked.
`s1flow report --from DIR/comparison.json` reads that
snapshot offline, without rescoring or rechecking anything. The snapshot keeps the source and date, provider and
model, the declared and recorded concurrency, and where latency and cost figures came from: billed, list price,
or shown as estimated, mixed or unknown. Unknown values stay unknown. Text and JSON output both support
`--limit`, `--offset` and exact `--candidate model[:version][/variant]` selectors.

## Charts

To look at the results in a browser, render a local page with the bundled renderer, which needs only the
standard library:

```bash
python <skill>/scripts/charts.py comparison.json --out comparison.html
```

It reads only the saved snapshot, so it doesn't import the evaluation tools, call a model, rescore or adopt
anything. The page opens with the task's objective plotted against API cost. You can switch either axis
to latency or another metric, and add a second chart. The table lists every candidate in model and variant
order, with no recommendations, eligibility filters or adopt buttons. Metric definitions, units and how each was
measured come from the same snapshot that agents read. Target lines don't hide candidates that fall short. You
can export each chart as a self-contained SVG or PNG that includes the source and sample size.

Box questions get the shared metrics and a confidence selection curve. Yes/no questions add precision/recall and
calibration charts. Choice questions get a curve of the selected answer's probability when the model returns a
real distribution. A provider's own confidence score is treated as a separate signal, and no probability curve
is drawn when the signal it needs isn't available.

## Thresholds and intervals

For yes/no questions (and choice questions with a positive option), Accuracy, F1 and ExpectedLoss can pick a threshold on the training side of each
development fold. Reports keep three things apart: raw metrics, cross-validated metrics with a tuned threshold,
and the held-out final result. Tuning a threshold is not the same as calibrating probabilities. Candidates whose
intervals overlap are grouped together, to err on the side of caution. That doesn't prove they are equivalent,
in practice or statistically. An unknown measurement never counts as meeting a cost or latency limit you set.

The ranking only orders candidates with an answer to every case; the JSON `candidates` keep the ones whose
evidence differs or is incomplete, and say where each falls short.

## When old results stop counting

Before reusing a result, s1flow checks the exact input that was sent, the question, the connection actually
used, the model ID and the implementation. Editing an input under the same case ID, or changing the endpoint or
options, means the old response is no longer reused. You can correct a label without asking the model again for an unchanged
input, but earlier evaluation results no longer match.

Changing concurrency also invalidates earlier performance numbers. The raw answers can still be reused, but old
timings aren't reported as if they were measured at the new concurrency; use `run --fresh` to measure again.

A custom provider used in evaluation must declare a `provider_revision` in its trusted ModelSpec or TOML entry,
naming the commit or package version of your implementation. The Client and policies that haven't been evaluated
don't need it. Keeping the revision accurate is up to you; it isn't a signature, and it proves nothing about a
remote model's weights.
