# gh-ruff-kind

2026-10-31 · 210 labelled dev cases (feature 83, question 60, bug 52, documentation 15) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**clef-flash@openrouter** has the highest coverage at 95% accuracy, 22% [16, 28] (API cost $0.12 per 10k, p99 748ms). Its interval overlaps with d1-ultra@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is kev@openrouter's, 61% [54, 68].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 55.7% [49, 63] | 0.48 | 0.81 | 0.24 | 22% [16, 28] | 93.5% (84.0%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 58.1% [51, 64] | 0.51 | 0.84 | 0.30 | 3% [1, 6] | 85.7% (47.9%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 60.0% [53, 67] | 0.54 | 0.87 | 0.24 | 17% [12, 22] | 94.3% (83.1%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 56.7% [50, 63] | 0.52 | 0.86 | 0.31 | 6% [3, 9] | 91.7% (66.1%) | 0/210 | 0/210 |
| d1@vercel | 210 | 54.8% [48, 61] | 0.49 | 0.85 | 0.35 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 60.0% [53, 67] | 0.55 | 0.84 | 0.29 | 9% [5, 13] | 88.9% (69.0%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 59.0% [52, 66] | 0.53 | 0.87 | 0.31 | 5% [2, 8] | 90.0% (60.6%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 60.0% [53, 67] | 0.55 | 0.86 | 0.33 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 60.0% [53, 67] | 0.55 | 0.86 | 0.32 | 8% [5, 12] | 88.2% (67.4%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 58.1% [51, 65] | 0.53 | 0.84 | 0.32 | 4% [1, 7] | 87.5% (52.9%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 58.6% [52, 66] | 0.52 | 0.78 | 0.33 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 51.9% [45, 59] | 0.46 | 0.78 | 0.16 | 7% [4, 10] | 64.3% (39.0%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 61.0% [54, 68] | 0.57 | 0.83 | 0.04 | 3% [1, 6] | 85.7% (47.9%) | 0/210 | 0/210 |
| luna@decisions | 210 | 58.1% [51, 64] | 0.52 | 0.83 | 0.36 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 58.1% [51, 65] | 0.52 | 0.87 | 0.32 | 9% [5, 12] | 88.9% (69.0%) | 0/210 | 0/210 |
| mercury@openrouter | 210 | 57.1% [50, 64] | 0.51 | 0.83 | 0.40 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| span@openrouter | 210 | 59.0% [52, 66] | 0.50 | 0.83 | 0.33 | 17% [12, 22] | 94.3% (83.1%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 22% [16, 28] | 0.91 | met |
| d1-ultra@openrouter = | 17% [12, 22] | 0.97 | met |
| span@openrouter = | 17% [12, 22] | 1.00 | met |
| decider-flash@openrouter | 9% [5, 13] | 0.99 | met |
| mammoth@openrouter | 9% [5, 12] | 1.00 | met |
| drex-max@openrouter | 8% [5, 12] | 1.00 | met |
| joey@openrouter | 7% [4, 10] | 0.94 | met |
| d1.1@openrouter | 6% [3, 9] | 0.99 | met |
| decider@openrouter | 5% [2, 8] | 1.00 | met |
| elephant@openrouter | 4% [1, 7] | 1.00 | met |
| clef@openrouter | 3% [1, 6] | 0.98 | met |
| kev@openrouter | 3% [1, 6] | 0.89 | met |
| d1@vercel | 2% [0, 4] | 1.00 | met |
| decision-1@openrouter | 2% [0, 4] | 1.00 | met |
| jev:1.14 | 0% [0, 0] | — | met |
| luna@decisions | 0% [0, 0] | — | met |
| mercury@openrouter | 0% [0, 0] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 401 ms | 540 ms | 748 ms | 1566 ms | 1.9 | 0 | 8 | $0.12 | billed | ○ |
| clef@openrouter | 210 | 1502 ms | 2338 ms | 5019 ms | 6334 ms | 3.3 | 0 | 8 | $1.16 | billed |  |
| d1-ultra@openrouter | 210 | 1379 ms | 2193 ms | 4748 ms | 5250 ms | 3.4 | 0 | 8 | $0.17 | billed |  |
| d1.1@openrouter | 210 | 1321 ms | 2316 ms | 6183 ms | 8328 ms | 4.7 | 0 | 8 | $0.08 | billed |  |
| d1@vercel | 210 | 214 ms | 295 ms | 486 ms | 642 ms | 2.3 | 0 | 8 | $0.08 | billed | ○ |
| decider-flash@openrouter | 210 | 1280 ms | 2931 ms | 6270 ms | 8226 ms | 4.9 | 0 | 8 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 1391 ms | 2507 ms | 5524 ms | 8330 ms | 4.0 | 0 | 8 | $0.09 | billed |  |
| decision-1@openrouter | 210 | 1472 ms | 2329 ms | 4261 ms | 8719 ms | 2.9 | 0 | 8 | $0.17 | billed |  |
| drex-max@openrouter | 210 | 1608 ms | 2362 ms | 5137 ms | 8641 ms | 3.2 | 0 | 8 | $0.28 | billed |  |
| elephant@openrouter | 210 | 1375 ms | 2444 ms | 4960 ms | 6556 ms | 3.6 | 0 | 8 | $0.17 | billed |  |
| jev:1.14 | 210 | 1295 ms | 2435 ms | 5306 ms | 8289 ms | 4.1 | 0 | 8 | $0.29 | estimated |  |
| joey@openrouter | 210 | 1330 ms | 2315 ms | 4166 ms | 6376 ms | 3.1 | 0 | 8 | $0.05 | billed | ○ |
| kev@openrouter | 210 | 1522 ms | 2385 ms | 4644 ms | 6511 ms | 3.1 | 0 | 8 | $0.16 | billed |  |
| luna@decisions | 210 | 1476 ms | 2532 ms | 6341 ms | 8558 ms | 4.3 | 1 | 8 | $0.47 | estimated |  |
| mammoth@openrouter | 210 | 1369 ms | 2441 ms | 6195 ms | 8216 ms | 4.5 | 0 | 8 | $0.47 | billed |  |
| mercury@openrouter | 210 | 1498 ms | 2350 ms | 4543 ms | 5337 ms | 3.0 | 0 | 8 | $0.09 | billed |  |
| span@openrouter | 210 | 1657 ms | 2449 ms | 4670 ms | 5309 ms | 2.8 | 0 | 8 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0026 | 11 s (estimated, 210 calls) | 8 min | 8 |
| clef@openrouter | $0.02 | 44 s (estimated, 210 calls) | 35 min | 8 |
| d1-ultra@openrouter | $0.0036 | 41 s (estimated, 210 calls) | 33 min | 8 |
| d1.1@openrouter | $0.0017 | 42 s (estimated, 210 calls) | 33 min | 8 |
| d1@vercel | $0.0017 | 6 s (estimated, 210 calls) | 5 min | 8 |
| decider-flash@openrouter | $0.0010 | 43 s (estimated, 210 calls) | 34 min | 8 |
| decider@openrouter | $0.0020 | 44 s (estimated, 210 calls) | 35 min | 8 |
| decision-1@openrouter | $0.0036 | 43 s (estimated, 210 calls) | 34 min | 8 |
| drex-max@openrouter | $0.0059 | 45 s (estimated, 210 calls) | 35 min | 8 |
| elephant@openrouter | $0.0035 | 42 s (estimated, 210 calls) | 34 min | 8 |
| jev:1.14 | $0.0062 | 42 s (estimated, 210 calls) | 33 min | 8 |
| joey@openrouter | $0.0010 | 41 s (estimated, 210 calls) | 32 min | 8 |
| kev@openrouter | $0.0034 | 44 s (estimated, 210 calls) | 35 min | 8 |
| luna@decisions | $0.0099 | 44 s (estimated, 210 calls) | 35 min | 8 |
| mammoth@openrouter | $0.0100 | 43 s (estimated, 210 calls) | 34 min | 8 |
| mercury@openrouter | $0.0019 | 43 s (estimated, 210 calls) | 34 min | 8 |
| span@openrouter | $0.0010 | 45 s (estimated, 210 calls) | 35 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26850 | question | feature | 0.94 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #28998 | question | bug | 0.92 | PLW0108 False positive when lambda executes a list element |
| #24887 | question | bug | 0.91 | F632: false positive |
| #27578 | feature | bug | 0.91 | False positive "f-string" message |
| #27775 | question | bug | 0.91 | False positive on TRY203 |
| #25140 | question | feature | 0.91 | Rule for orphan literals? |

**clef@openrouter** (39)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 0.97 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 0.97 | ERA001 false positive on "# pytest: foo=bar" |
| #24887 | question | bug | 0.97 | F632: false positive |
| #26850 | question | feature | 0.97 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #26522 | feature | bug | 0.97 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #27775 | question | bug | 0.97 | False positive on TRY203 |
| #28519 | question | feature | 0.96 | [Formatter feature request] Config option for trailing comma |

**d1-ultra@openrouter** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26646 | question | bug | 0.97 | F722 False Positive (Syntax error in forward annotation) |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 0.97 | ERA001 false positive on "# pytest: foo=bar" |
| #28998 | question | bug | 0.97 | PLW0108 False positive when lambda executes a list element |
| #26449 | question | bug | 0.96 | ruff format strips mandatory parens from multi-exception except claus… |
| #28308 | question | bug | 0.96 | fatal error while checking app.py please open an issue |
| #24887 | question | bug | 0.95 | F632: false positive |
| #28519 | question | feature | 0.95 | [Formatter feature request] Config option for trailing comma |

**d1.1@openrouter** (38)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 0.99 | ruff format strips mandatory parens from multi-exception except claus… |
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #25550 | question | bug | 0.99 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #26951 | feature | bug | 0.98 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28308 | question | bug | 0.98 | fatal error while checking app.py please open an issue |
| #25916 | question | bug | 0.98 | SIM115 open() inside a return statement not reported |
| #26646 | question | bug | 0.98 | F722 False Positive (Syntax error in forward annotation) |

**d1@vercel** (45)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #24785 | feature | bug | 1.00 | `unused-async` (`RUF029`) - false negative on methods |
| #27537 | feature | bug | 1.00 | `unused-function-argument` - false negative when argument is reassign… |

**decider-flash@openrouter** (41)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #28308 | question | bug | 0.99 | fatal error while checking app.py please open an issue |
| #26449 | question | bug | 0.99 | ruff format strips mandatory parens from multi-exception except claus… |
| #26522 | feature | bug | 0.99 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #24827 | question | bug | 0.99 | N805 auto-fix unsafely renames meaningful parameter to `self` |
| #24785 | feature | bug | 0.98 | `unused-async` (`RUF029`) - false negative on methods |
| #27775 | question | bug | 0.98 | False positive on TRY203 |

**decider@openrouter** (43)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #27369 | feature | bug | 0.99 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #25550 | question | bug | 0.99 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #27775 | question | bug | 0.99 | False positive on TRY203 |
| #28675 | question | bug | 0.99 | ERA001 false positive on "# pytest: foo=bar" |
| #24715 | question | bug | 0.99 | PT006 breaks when only one argname |

**decision-1@openrouter** (52)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #26139 | question | bug | 1.00 | Incorrect check_name in report for the rule D421 |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #28097 | question | feature | 1.00 | Option to use `code:name` for rules and output |

**drex-max@openrouter** (50)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #24785 | feature | bug | 1.00 | `unused-async` (`RUF029`) - false negative on methods |

**elephant@openrouter** (51)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #24827 | question | bug | 0.99 | N805 auto-fix unsafely renames meaningful parameter to `self` |
| #24785 | feature | bug | 0.99 | `unused-async` (`RUF029`) - false negative on methods |
| #27369 | feature | bug | 0.99 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #27775 | question | bug | 0.99 | False positive on TRY203 |

**jev:1.14** (60)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28308 | question | bug | 1.00 | fatal error while checking app.py please open an issue |
| #28512 | question | bug | 1.00 | `F821` does not understand the intention of the following code |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28321 | documentation | bug | 1.00 | RUF022 and isort sort_reexports not equal |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #27537 | feature | bug | 1.00 | `unused-function-argument` - false negative when argument is reassign… |

**joey@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28519 | question | feature | 0.93 | [Formatter feature request] Config option for trailing comma |

**luna@decisions** (68)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28248 | documentation | bug | 1.00 | INP001:  does not detect implicit namespace packages containing no mo… |
| #28308 | question | bug | 1.00 | fatal error while checking app.py please open an issue |
| #28483 | question | bug | 1.00 | The Ruff VS Code extension uses the wrong `ruff.toml` file |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #27578 | feature | bug | 1.00 | False positive "f-string" message |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #26783 | feature | question | 1.00 | How to ensure all top-level imports are sorted globally |

**mammoth@openrouter** (40)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #24827 | question | bug | 1.00 | N805 auto-fix unsafely renames meaningful parameter to `self` |

**mercury@openrouter** (78)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #27432 | question | bug | 1.00 | Ruff reports S604 on creating a shapely.geometry.Polygon |

**span@openrouter** (52)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #26139 | question | bug | 1.00 | Incorrect check_name in report for the rule D421 |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26951 | feature | bug | 0.99 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #27246 | question | feature | 0.99 | Add possibility to disable autofixes for certain files |


## Cases the models disagree on (12 of 71)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28604 | feature | feature (0.72) | feature (0.93) | feature (0.95) | feature (0.89) | feature (0.96) | feature (0.98) | feature (0.98) | feature (1.00) | feature (0.98) | feature (0.95) | feature (1.00) | documentation (0.38) | feature (0.72) | feature (1.00) | feature (0.97) | feature (1.00) | feature (0.98) | Add `import datetime as dt` as a conventional alias |
| #28483 | question | bug (0.55) | bug (0.56) | bug (0.71) | bug (0.78) | bug (0.85) | bug (0.55) | question (0.58) | bug (0.65) | bug (0.61) | bug (0.82) | bug (0.93) | bug (0.54) | bug (0.45) | bug (1.00) | bug (0.55) | bug (0.98) | bug (0.91) | The Ruff VS Code extension uses the wrong `ruff.toml` file |
| #28097 | question | feature (0.82) | feature (0.92) | feature (0.93) | feature (0.96) | feature (0.99) | feature (0.98) | feature (0.98) | feature (1.00) | feature (0.99) | feature (0.99) | feature (1.00) | question (0.41) | feature (0.73) | feature (0.93) | feature (0.98) | feature (1.00) | feature (0.98) | Option to use `code:name` for rules and output |
| #27748 | feature | feature (0.96) | feature (0.94) | feature (0.91) | feature (0.93) | feature (0.97) | feature (0.99) | feature (0.96) | feature (1.00) | feature (0.99) | feature (0.97) | feature (0.98) | bug (0.40) | feature (0.49) | feature (1.00) | feature (0.93) | feature (0.99) | feature (0.98) | Default value pop instead of if-else block |
| #27171 | feature | feature (0.92) | feature (0.91) | feature (0.97) | feature (0.92) | feature (0.99) | feature (0.96) | feature (0.99) | feature (0.99) | feature (0.99) | feature (0.99) | feature (0.97) | bug (0.32) | feature (0.48) | feature (1.00) | feature (0.97) | feature (1.00) | feature (0.98) | Rule to flag identifiers that are not NFKC-normalized |
| #26879 | feature | feature (0.83) | feature (0.85) | feature (0.68) | bug (0.67) | bug (0.50) | feature (0.63) | feature (0.71) | feature (0.91) | feature (0.83) | feature (0.91) | feature (0.72) | feature (0.30) | feature (0.49) | feature (1.00) | feature (0.91) | feature (0.98) | feature (0.95) | Widen accepted `__all__` and `__slots__` formats to include single-ch… |
| #26783 | feature | question (0.52) | question (0.72) | question (0.71) | question (0.66) | feature (0.57) | question (0.66) | question (0.89) | question (0.92) | question (0.92) | question (0.61) | feature (0.48) | question (0.49) | question (0.61) | question (1.00) | question (0.58) | feature (0.73) | feature (0.79) | How to ensure all top-level imports are sorted globally |
| #26656 | feature | feature (0.94) | feature (0.91) | feature (0.99) | feature (0.99) | feature (0.99) | feature (0.99) | feature (0.99) | feature (1.00) | feature (1.00) | feature (0.93) | feature (1.00) | question (0.35) | feature (0.56) | feature (0.92) | feature (0.99) | feature (1.00) | feature (1.00) | Rule suggestion: `functools.partial` call with singular argument |
| #26456 | feature | feature (0.90) | feature (0.91) | feature (0.90) | feature (0.94) | feature (0.99) | feature (0.96) | feature (0.97) | feature (1.00) | feature (0.99) | feature (0.96) | feature (0.97) | question (0.43) | feature (0.58) | feature (1.00) | feature (0.95) | feature (1.00) | feature (1.00) | Detecting returning exception instead of raising |
| #26524 | question | bug (0.80) | bug (0.93) | bug (0.95) | bug (0.97) | bug (0.98) | bug (0.90) | bug (0.98) | bug (0.93) | bug (0.99) | bug (0.94) | bug (1.00) | bug (0.53) | question (0.43) | bug (0.99) | bug (0.98) | bug (1.00) | bug (0.98) | Ruff check with --fix removes applicable noqa TRY400 |
| #25296 | feature | feature (0.97) | feature (0.97) | feature (0.98) | feature (0.98) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (1.00) | bug (0.37) | feature (0.80) | feature (1.00) | feature (1.00) | feature (1.00) | feature (1.00) | Rule idea: class-level None can make runtime protocol checks slow |
| #25025 | feature | feature (0.97) | feature (0.93) | feature (0.98) | feature (0.97) | feature (0.99) | feature (0.97) | feature (0.99) | feature (1.00) | feature (1.00) | feature (0.99) | feature (0.99) | bug (0.30) | bug (0.31) | feature (1.00) | feature (0.99) | feature (1.00) | feature (0.98) | new rule - useless `from` clause in `raise` statement |
