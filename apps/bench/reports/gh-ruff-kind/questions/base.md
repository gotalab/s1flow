# gh-ruff-kind

2026-10-31 · 210 labelled dev cases (feature 83, question 60, bug 52, documentation 15) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**clef-flash@openrouter** has the highest coverage at 95% accuracy, 22% [17, 29] (API cost $0.12 per 10k, p99 874ms). Its interval overlaps with d1.1@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is kev@openrouter's, 61% [54, 68].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 56.2% [49, 63] | 0.48 | 0.80 | 0.23 | 22% [17, 29] | 93.6% (84.3%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 57.1% [50, 63] | 0.51 | 0.84 | 0.29 | 4% [2, 7] | 88.9% (57.1%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 60.5% [54, 67] | 0.56 | 0.87 | 0.23 | 8% [4, 11] | 81.2% (58.3%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 56.7% [50, 63] | 0.52 | 0.86 | 0.31 | 13% [9, 17] | 92.6% (78.5%) | 0/210 | 0/210 |
| d1@vercel | 210 | 58.1% [51, 65] | 0.52 | 0.86 | 0.32 | 1% [0, 3] | 66.7% (13.5%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 60.0% [53, 67] | 0.55 | 0.84 | 0.29 | 9% [5, 13] | 88.9% (69.0%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 59.0% [52, 66] | 0.53 | 0.87 | 0.31 | 5% [2, 8] | 90.0% (60.6%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 60.0% [53, 67] | 0.55 | 0.86 | 0.33 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 59.0% [52, 65] | 0.54 | 0.86 | 0.32 | 7% [4, 11] | 80.0% (56.0%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 58.1% [51, 65] | 0.53 | 0.84 | 0.32 | 4% [1, 7] | 87.5% (52.9%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 58.1% [51, 65] | 0.52 | 0.78 | 0.34 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 51.9% [45, 59] | 0.46 | 0.78 | 0.16 | 7% [4, 10] | 64.3% (39.0%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 61.0% [54, 68] | 0.57 | 0.83 | 0.05 | 3% [1, 6] | 85.7% (47.9%) | 0/210 | 0/210 |
| luna@decisions | 210 | 58.1% [51, 64] | 0.52 | 0.83 | 0.36 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 58.1% [51, 65] | 0.52 | 0.87 | 0.32 | 9% [5, 12] | 88.9% (69.0%) | 0/210 | 0/210 |
| mercury@openrouter | 210 | 57.1% [50, 64] | 0.51 | 0.83 | 0.40 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| span@openrouter | 210 | 59.0% [52, 66] | 0.51 | 0.83 | 0.34 | 17% [12, 22] | 94.3% (83.1%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 22% [17, 29] | 0.92 | met |
| d1.1@openrouter = | 13% [9, 17] | 0.99 | met |
| span@openrouter = | 17% [12, 22] | 1.00 | met |
| decider-flash@openrouter | 9% [5, 13] | 0.99 | met |
| mammoth@openrouter | 9% [5, 12] | 1.00 | met |
| d1-ultra@openrouter | 8% [4, 11] | 0.99 | met |
| drex-max@openrouter | 7% [4, 11] | 1.00 | met |
| joey@openrouter | 7% [4, 10] | 0.94 | met |
| decider@openrouter | 5% [2, 8] | 1.00 | met |
| clef@openrouter | 4% [2, 7] | 0.98 | met |
| elephant@openrouter | 4% [1, 7] | 1.00 | met |
| kev@openrouter | 3% [1, 6] | 0.89 | met |
| decision-1@openrouter | 2% [0, 4] | 1.00 | met |
| d1@vercel | 1% [0, 3] | 1.00 | met |
| jev:1.14 | 0% [0, 0] | — | met |
| luna@decisions | 0% [0, 0] | — | met |
| mercury@openrouter | 0% [0, 0] | 1.00 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 378 ms | 571 ms | 874 ms | 1056 ms | 2.3 | 0 | 4 | $0.12 | billed | ○ |
| clef@openrouter | 210 | 338 ms | 430 ms | 790 ms | 871 ms | 2.3 | 0 | 4 | $1.15 | billed |  |
| d1-ultra@openrouter | 210 | 225 ms | 332 ms | 556 ms | 599 ms | 2.5 | 0 | 4 | $0.17 | billed |  |
| d1.1@openrouter | 210 | 176 ms | 263 ms | 340 ms | 475 ms | 1.9 | 0 | 4 | $0.08 | billed | ○ |
| d1@vercel | 210 | 227 ms | 310 ms | 519 ms | 549 ms | 2.3 | 0 | 4 | $0.08 | billed |  |
| decider-flash@openrouter | 210 | 142 ms | 159 ms | 257 ms | 307 ms | 1.8 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 218 ms | 250 ms | 353 ms | 1234 ms | 1.6 | 0 | 4 | $0.09 | billed |  |
| decision-1@openrouter | 210 | 266 ms | 344 ms | 426 ms | 497 ms | 1.6 | 0 | 4 | $0.17 | billed |  |
| drex-max@openrouter | 210 | 314 ms | 414 ms | 718 ms | 985 ms | 2.3 | 0 | 4 | $0.28 | billed |  |
| elephant@openrouter | 210 | 184 ms | 202 ms | 322 ms | 416 ms | 1.7 | 0 | 4 | $0.17 | billed |  |
| jev:1.14 | 210 | 142 ms | 168 ms | 224 ms | 292 ms | 1.6 | 0 | 4 | $0.29 | estimated | ○ |
| joey@openrouter | 210 | 175 ms | 193 ms | 256 ms | 399 ms | 1.5 | 0 | 4 | $0.05 | billed | ○ |
| kev@openrouter | 210 | 476 ms | 808 ms | 1235 ms | 1308 ms | 2.6 | 0 | 4 | $0.16 | billed |  |
| luna@decisions | 210 | 197 ms | 346 ms | 526 ms | 583 ms | 2.7 | 1 | 4 | $0.47 | estimated |  |
| mammoth@openrouter | 210 | 214 ms | 243 ms | 396 ms | 848 ms | 1.8 | 0 | 4 | $0.47 | billed |  |
| mercury@openrouter | 210 | 301 ms | 385 ms | 537 ms | 1105 ms | 1.8 | 0 | 4 | $0.09 | billed |  |
| span@openrouter | 210 | 192 ms | 469 ms | 880 ms | 952 ms | 4.6 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0025 | 21 s (estimated, 210 calls) | 16 min | 4 |
| clef@openrouter | $0.02 | 18 s (estimated, 210 calls) | 14 min | 4 |
| d1-ultra@openrouter | $0.0036 | 13 s (estimated, 210 calls) | 10 min | 4 |
| d1.1@openrouter | $0.0017 | 10 s (estimated, 210 calls) | 8 min | 4 |
| d1@vercel | $0.0017 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decider-flash@openrouter | $0.0010 | 8 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0020 | 12 s (estimated, 210 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0036 | 15 s (estimated, 210 calls) | 12 min | 4 |
| drex-max@openrouter | $0.0059 | 16 s (estimated, 210 calls) | 13 min | 4 |
| elephant@openrouter | $0.0035 | 10 s (estimated, 210 calls) | 8 min | 4 |
| jev:1.14 | $0.0062 | 8 s (estimated, 210 calls) | 6 min | 4 |
| joey@openrouter | $0.0010 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0034 | 23 s (estimated, 210 calls) | 18 min | 4 |
| luna@decisions | $0.0099 | 12 s (estimated, 210 calls) | 9 min | 4 |
| mammoth@openrouter | $0.0100 | 12 s (estimated, 210 calls) | 9 min | 4 |
| mercury@openrouter | $0.0019 | 17 s (estimated, 210 calls) | 13 min | 4 |
| span@openrouter | $0.0010 | 14 s (estimated, 210 calls) | 12 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26850 | question | feature | 0.94 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #28998 | question | bug | 0.92 | PLW0108 False positive when lambda executes a list element |
| #24887 | question | bug | 0.91 | F632: false positive |
| #28922 | feature | documentation | 0.91 | B018: useless-expression one more example to document |
| #27578 | feature | bug | 0.91 | False positive "f-string" message |
| #27775 | question | bug | 0.91 | False positive on TRY203 |
| #25140 | question | feature | 0.90 | Rule for orphan literals? |
| #26951 | feature | bug | 0.90 | RUF052 false negatives for `class`, `def`, and `import` bindings |

**clef@openrouter** (39)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 0.97 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 0.97 | ERA001 false positive on "# pytest: foo=bar" |
| #26522 | feature | bug | 0.97 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #26850 | question | feature | 0.96 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #24887 | question | bug | 0.96 | F632: false positive |
| #27775 | question | bug | 0.96 | False positive on TRY203 |
| #28519 | question | feature | 0.96 | [Formatter feature request] Config option for trailing comma |

**d1-ultra@openrouter** (21)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #26449 | question | bug | 0.98 | ruff format strips mandatory parens from multi-exception except claus… |
| #28675 | question | bug | 0.98 | ERA001 false positive on "# pytest: foo=bar" |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #25550 | question | bug | 0.97 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26646 | question | bug | 0.97 | F722 False Positive (Syntax error in forward annotation) |
| #28308 | question | bug | 0.97 | fatal error while checking app.py please open an issue |
| #28040 | feature | bug | 0.96 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |

**d1.1@openrouter** (37)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26522 | feature | bug | 0.99 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #27537 | feature | bug | 0.99 | `unused-function-argument` - false negative when argument is reassign… |
| #26449 | question | bug | 0.98 | ruff format strips mandatory parens from multi-exception except claus… |
| #27379 | question | bug | 0.98 | False positive Undefined name for self-referential return annotation … |
| #25550 | question | bug | 0.98 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #28675 | question | bug | 0.98 | ERA001 false positive on "# pytest: foo=bar" |
| #28998 | question | bug | 0.98 | PLW0108 False positive when lambda executes a list element |
| #24563 | feature | bug | 0.98 | PLC2701 false positive for a private name import used in a type param… |

**d1@vercel** (45)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #24563 | feature | bug | 1.00 | PLC2701 false positive for a private name import used in a type param… |
| #27775 | question | bug | 1.00 | False positive on TRY203 |

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

**decision-1@openrouter** (51)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26139 | question | bug | 1.00 | Incorrect check_name in report for the rule D421 |
| #28308 | question | bug | 1.00 | fatal error while checking app.py please open an issue |

**drex-max@openrouter** (50)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #27369 | feature | bug | 1.00 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |

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

**jev:1.14** (59)

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

**mercury@openrouter** (79)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #27432 | question | bug | 1.00 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |

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


## Cases the models disagree on (12 of 69)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28604 | feature | feature (0.70) | feature (0.93) | feature (0.91) | feature (0.92) | feature (0.97) | feature (0.98) | feature (0.98) | feature (1.00) | feature (0.98) | feature (0.95) | feature (1.00) | documentation (0.38) | feature (0.72) | feature (1.00) | feature (0.97) | feature (1.00) | feature (0.98) | Add `import datetime as dt` as a conventional alias |
| #28483 | question | bug (0.55) | bug (0.58) | bug (0.66) | bug (0.78) | bug (0.89) | bug (0.55) | question (0.58) | bug (0.65) | bug (0.61) | bug (0.82) | bug (0.93) | bug (0.54) | bug (0.45) | bug (1.00) | bug (0.55) | bug (0.97) | bug (0.91) | The Ruff VS Code extension uses the wrong `ruff.toml` file |
| #28097 | question | feature (0.81) | feature (0.92) | feature (0.93) | feature (0.94) | feature (0.99) | feature (0.98) | feature (0.98) | feature (1.00) | feature (0.99) | feature (0.99) | feature (1.00) | question (0.41) | feature (0.73) | feature (0.93) | feature (0.98) | feature (1.00) | feature (0.98) | Option to use `code:name` for rules and output |
| #27748 | feature | feature (0.96) | feature (0.92) | feature (0.93) | feature (0.92) | feature (0.98) | feature (0.99) | feature (0.96) | feature (1.00) | feature (0.99) | feature (0.97) | feature (0.97) | bug (0.40) | feature (0.49) | feature (1.00) | feature (0.93) | feature (0.99) | feature (0.98) | Default value pop instead of if-else block |
| #27171 | feature | feature (0.92) | feature (0.91) | feature (0.95) | feature (0.92) | feature (0.97) | feature (0.96) | feature (0.99) | feature (0.99) | feature (0.99) | feature (0.99) | feature (0.97) | bug (0.32) | feature (0.48) | feature (1.00) | feature (0.97) | feature (1.00) | feature (0.98) | Rule to flag identifiers that are not NFKC-normalized |
| #26879 | feature | feature (0.84) | feature (0.85) | feature (0.65) | feature (0.58) | bug (0.63) | feature (0.63) | feature (0.71) | feature (0.90) | feature (0.83) | feature (0.91) | feature (0.72) | feature (0.30) | feature (0.49) | feature (1.00) | feature (0.91) | feature (0.98) | feature (0.95) | Widen accepted `__all__` and `__slots__` formats to include single-ch… |
| #26783 | feature | question (0.51) | question (0.73) | question (0.65) | question (0.64) | feature (0.71) | question (0.66) | question (0.89) | question (0.92) | question (0.92) | question (0.61) | feature (0.51) | question (0.49) | question (0.61) | question (1.00) | question (0.58) | feature (0.75) | feature (0.79) | How to ensure all top-level imports are sorted globally |
| #26656 | feature | feature (0.94) | feature (0.91) | feature (0.98) | feature (0.99) | feature (0.99) | feature (0.99) | feature (0.99) | feature (1.00) | feature (1.00) | feature (0.93) | feature (1.00) | question (0.35) | feature (0.55) | feature (0.92) | feature (0.99) | feature (1.00) | feature (1.00) | Rule suggestion: `functools.partial` call with singular argument |
| #26456 | feature | feature (0.92) | feature (0.91) | feature (0.89) | feature (0.94) | feature (0.99) | feature (0.96) | feature (0.97) | feature (1.00) | feature (0.99) | feature (0.96) | feature (0.98) | question (0.43) | feature (0.58) | feature (1.00) | feature (0.95) | feature (1.00) | feature (1.00) | Detecting returning exception instead of raising |
| #26524 | question | bug (0.82) | bug (0.92) | bug (0.93) | bug (0.97) | bug (0.99) | bug (0.90) | bug (0.98) | bug (0.92) | bug (0.99) | bug (0.94) | bug (1.00) | bug (0.53) | question (0.43) | bug (0.99) | bug (0.98) | bug (1.00) | bug (0.98) | Ruff check with --fix removes applicable noqa TRY400 |
| #25296 | feature | feature (0.97) | feature (0.97) | feature (0.98) | feature (0.99) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (1.00) | bug (0.37) | feature (0.80) | feature (1.00) | feature (1.00) | feature (1.00) | feature (1.00) | Rule idea: class-level None can make runtime protocol checks slow |
| #25025 | feature | feature (0.97) | feature (0.93) | feature (0.98) | feature (0.97) | feature (0.99) | feature (0.97) | feature (0.99) | feature (1.00) | feature (1.00) | feature (0.99) | feature (0.99) | bug (0.30) | bug (0.31) | feature (1.00) | feature (0.99) | feature (1.00) | feature (0.98) | new rule - useless `from` clause in `raise` statement |
