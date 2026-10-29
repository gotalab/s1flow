# gh-ruff-kind

2026-10-22 · 300 labelled (feature 119, question 86, bug 74, documentation 21) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**clef-flash** has the highest coverage at 95% accuracy, 20% [15, 26] (API cost $0.47 per 10k, p99 913ms). The highest accuracy (all cases) is luna@decisions's, 60% [54, 65].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 59.0% [53, 64] | 0.54 | 0.85 | 0.27 | 6% [3, 10] | 84.6% (59.0%) | 0/300 | 0/300 |
| clef-flash | 300 | 56.3% [51, 62] | 0.50 | 0.81 | 0.23 | 20% [15, 26] | 93.0% (82.9%) | 0/300 | 0/300 |
| d1@vercel | 300 | 57.0% [52, 62] | 0.52 | 0.86 | 0.33 | 2% [0, 4] | 75.0% (24.9%) | 0/300 | 0/300 |
| flash-lite@vercel ※ | 300 | 58.0% [52, 63] | 0.52 | 0.71 | 0.42 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| haiku@vercel ※ | 300 | 58.7% [53, 64] | 0.53 | 0.72 | 0.41 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev | 300 | 58.3% [53, 64] | 0.53 | 0.80 | 0.34 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev@vercel | 300 | 58.3% [53, 64] | 0.53 | 0.79 | 0.34 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| kev@openrouter | 300 | 59.3% [54, 65] | 0.55 | 0.83 | 0.02 | 8% [5, 12] | 82.4% (60.4%) | 0/300 | 0/300 |
| luna@decisions | 300 | 59.7% [54, 65] | 0.55 | 0.80 | 0.36 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| clef-flash ◎ | 20% [15, 26] | 0.92 | met |
| kev@openrouter | 8% [5, 12] | 0.89 | met |
| clef | 6% [3, 10] | 0.98 | met |
| d1@vercel | 2% [0, 4] | 1.00 | met |
| jev | 0% [0, 0] | — | met |
| jev@vercel | 0% [0, 0] | — | met |
| luna@decisions | 0% [0, 0] | — | met |
| flash-lite@vercel | 0% [0, 0] | — | met |
| haiku@vercel | 0% [0, 0] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 411 ms | 726 ms | 1385 ms | 4392 ms | 3.4 | not recorded | unknown | $1.26 | estimated |  |
| clef-flash | 300 | 238 ms | 516 ms | 913 ms | 1268 ms | 3.8 | not recorded | unknown | $0.47 | estimated | ○ |
| d1@vercel | 300 | 504 ms | 660 ms | 2084 ms | 2710 ms | 4.1 | not recorded | unknown | $0.17 | billed |  |
| flash-lite@vercel | 300 | 1268 ms | 1595 ms | 2681 ms | 8010 ms | 2.1 | not recorded | unknown | $1.51 | estimated |  |
| haiku@vercel | 300 | 1023 ms | 1280 ms | 2718 ms | 7900 ms | 2.7 | not recorded | unknown | $7.22 | estimated |  |
| jev | 300 | 161 ms | 214 ms | 250 ms | 518 ms | 1.5 | not recorded | unknown | $0.30 | estimated | ○ |
| jev@vercel | 300 | 428 ms | 638 ms | 1199 ms | 6464 ms | 2.8 | not recorded | unknown | $0.30 | billed |  |
| kev@openrouter | 300 | 925 ms | 1192 ms | 1708 ms | 1745 ms | 1.8 | not recorded | unknown | $0.16 | billed | ○ |
| luna@decisions | 300 | 256 ms | 309 ms | 356 ms | 630 ms | 1.4 | not recorded | unknown | $0.48 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.04 | 19 s (measured, 300 calls) | 11 min | 8 |
| clef-flash | $0.01 | 12 s (measured, 300 calls) | 7 min | 8 |
| jev | $0.0089 | 7 s (measured, 300 calls) | 4 min | 8 |
| luna@decisions | $0.01 | 10 s (measured, 300 calls) | 6 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 90 | 62.2% | 3% | 100.0% | 0.033 |
| clef-flash | 90 | 56.7% | 20% | 83.3% | 0.200 |
| d1@vercel | 90 | 57.8% | 1% | 100.0% | 0.011 |
| flash-lite@vercel | 90 | 60.0% | 0% | — | 0.000 |
| haiku@vercel | 90 | 58.9% | 0% | — | 0.000 |
| jev | 90 | 57.8% | 0% | — | 0.000 |
| jev@vercel | 90 | 57.8% | 0% | — | 0.000 |
| kev@openrouter | 90 | 55.6% | 2% | 50.0% | 0.022 |
| luna@decisions | 90 | 61.1% | 0% | — | 0.000 |

## Wrong at a high probability (0.9 or more)

**clef** (52)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 0.97 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #27411 | question | documentation | 0.97 | Docs: F811 (redefined-while-unused) silently skips names matching dum… |
| #26522 | feature | bug | 0.97 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #24559 | question | bug | 0.97 | PYI034 false positive when `Self` is imported from a local re-export … |
| #26850 | question | feature | 0.97 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #28675 | question | bug | 0.97 | ERA001 false positive on "# pytest: foo=bar" |
| #24887 | question | bug | 0.97 | F632: false positive |

**clef-flash** (11)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27411 | question | documentation | 0.95 | Docs: F811 (redefined-while-unused) silently skips names matching dum… |
| #26850 | question | feature | 0.94 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #24784 | question | feature | 0.93 | Looking for a rule catches unused str.replace() |
| #28998 | question | bug | 0.93 | PLW0108 False positive when lambda executes a list element |
| #27982 | question | documentation | 0.92 | offtop: repo / docs section for badges |
| #24887 | question | bug | 0.92 | F632: false positive |
| #27552 | question | bug | 0.91 | RUF075 false-positive with a context manager |
| #27775 | question | bug | 0.91 | False positive on TRY203 |

**d1@vercel** (64)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #24559 | question | bug | 1.00 | PYI034 false positive when `Self` is imported from a local re-export … |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #24887 | question | bug | 1.00 | F632: false positive |
| #28040 | feature | bug | 1.00 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |

**flash-lite@vercel** (126)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25652 | feature | bug | 1.00 | `ASYNC119`: allow some context managers and async context managers to… |
| #25699 | question | feature | 1.00 | `ANN401`: allow `__getattr__` to return `Any` |
| #25809 | question | feature | 1.00 | Eclipse / PyDev integration/setup |
| #25916 | question | bug | 1.00 | SIM115 open() inside a return statement not reported |
| #25588 | feature | bug | 1.00 | `PLR2004` does not care if magic value in comparison is a major versi… |
| #25564 | feature | bug | 1.00 | RUF075 false positive w/ code that should only run without exception |
| #25390 | feature | bug | 1.00 | False positive: `too-many-statements-in-try-clause` triggers on try-f… |
| #25392 | question | bug | 1.00 | SQLAlchemy __mapper_args__: ruff `RUF012` and ty `invalid-attribute-o… |

**haiku@vercel** (124)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25699 | question | feature | 1.00 | `ANN401`: allow `__getattr__` to return `Any` |
| #25809 | question | feature | 1.00 | Eclipse / PyDev integration/setup |
| #25916 | question | bug | 1.00 | SIM115 open() inside a return statement not reported |
| #25588 | feature | bug | 1.00 | `PLR2004` does not care if magic value in comparison is a major versi… |
| #25564 | feature | bug | 1.00 | RUF075 false positive w/ code that should only run without exception |
| #25390 | feature | bug | 1.00 | False positive: `too-many-statements-in-try-clause` triggers on try-f… |
| #25392 | question | bug | 1.00 | SQLAlchemy __mapper_args__: ruff `RUF012` and ty `invalid-attribute-o… |
| #25399 | question | bug | 1.00 | F401 false positive for `import xyz as _` |

**jev** (81)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27552 | question | bug | 1.00 | RUF075 false-positive with a context manager |
| #27537 | feature | bug | 1.00 | `unused-function-argument` - false negative when argument is reassign… |
| #27432 | question | bug | 1.00 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #27369 | feature | bug | 1.00 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #27334 | question | bug | 1.00 | Inconsistent output when `output-prefer-rule-codes = true` |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |

**jev@vercel** (88)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27411 | question | documentation | 1.00 | Docs: F811 (redefined-while-unused) silently skips names matching dum… |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #26850 | question | feature | 1.00 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #27216 | feature | bug | 1.00 | `delete-full-slice` (FURB131) should not apply to `dict`s |
| #27578 | feature | bug | 1.00 | False positive "f-string" message |
| #27552 | question | bug | 1.00 | RUF075 false-positive with a context manager |
| #27537 | feature | bug | 1.00 | `unused-function-argument` - false negative when argument is reassign… |
| #27432 | question | bug | 1.00 | Ruff reports S604 on creating a shapely.geometry.Polygon |

**luna@decisions** (97)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25378 | feature | bug | 1.00 | `fallible-context-manager` (`RUF075`) - false positive when `yield` i… |
| #27432 | question | bug | 1.00 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #28248 | documentation | bug | 1.00 | INP001:  does not detect implicit namespace packages containing no mo… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26153 | feature | question | 1.00 | `D418` should not trigger in .pyi files |
| #27552 | question | bug | 1.00 | RUF075 false-positive with a context manager |
| #27578 | feature | bug | 1.00 | False positive "f-string" message |
| #25916 | question | bug | 1.00 | SIM115 open() inside a return statement not reported |


## Cases the models disagree on (12 of 64)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #29069 | feature | bug (0.59) | bug (0.68) | bug (0.95) | bug (1.00) | bug (1.00) | bug (0.90) | bug (0.90) | feature (0.38) | bug (0.92) | `deprecated-import` - should suggest `typing.TypeForm` instead of `ty… |
| #28945 | feature | bug (0.85) | bug (0.77) | bug (0.53) | feature (1.00) | bug (1.00) | bug (0.80) | bug (0.83) | bug (0.40) | bug (0.97) | RUF031 incorrectly-parenthesized-tuple-in-subscript: false negative |
| #28942 | feature | feature (0.80) | feature (0.49) | bug (0.50) | feature (1.00) | bug (1.00) | bug (0.56) | bug (0.59) | bug (0.40) | bug (0.95) | PLC0414 useless-import-alias: detect in *.pyi files - mypy stubgen ge… |
| #28939 | question | question (0.60) | feature (0.57) | question (0.47) | feature (1.00) | question (1.00) | question (0.60) | question (0.78) | bug (0.30) | question (0.61) | pt HOSP01 |
| #28913 | question | bug (0.38) | question (0.52) | bug (0.79) | bug (1.00) | bug (1.00) | bug (0.64) | bug (0.62) | question (0.51) | bug (0.76) | Current working directory alters check behavior |
| #28893 | question | feature (0.57) | feature (0.55) | feature (0.93) | feature (1.00) | feature (1.00) | feature (0.91) | feature (0.89) | feature (0.44) | question (0.73) | Emit error for "unknown rule selectors" when explicit-preview-rules=t… |
| #28872 | documentation | bug (0.74) | bug (0.72) | bug (0.56) | feature (1.00) | feature (1.00) | feature (0.56) | feature (0.62) | bug (0.37) | bug (0.85) | F841 unused-variable should fix RUF047 needless-else |
| #28868 | question | bug (0.81) | bug (0.68) | bug (0.89) | feature (1.00) | bug (1.00) | bug (0.61) | bug (0.62) | bug (0.43) | bug (0.99) | TC004 runtime-import-in-type-checking-block fixer causes follow up: T… |
| #28777 | feature | feature (0.78) | feature (0.71) | feature (0.81) | feature (1.00) | feature (1.00) | feature (0.71) | feature (0.85) | question (0.40) | feature (0.54) | `too-many-positional-arguments`: dataclasses? |
| #28551 | bug | feature (0.32) | feature (0.35) | bug (0.40) | feature (1.00) | feature (1.00) | feature (0.54) | feature (0.37) | bug (0.32) | question (0.90) | Use rule name with parenthesized rule code in warning messages |
| #28298 | documentation | documentation (0.92) | documentation (0.70) | documentation (0.95) | documentation (1.00) | documentation (1.00) | documentation (0.59) | documentation (0.62) | documentation (0.60) | bug (0.79) | Documentation for any-type (ANN401) |
| #28190 | question | documentation (0.46) | bug (0.40) | documentation (0.84) | documentation (1.00) | bug (1.00) | documentation (0.56) | documentation (0.53) | documentation (0.49) | bug (0.52) | Old rules are now default in 0.16.5 |
