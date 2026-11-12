# gh-ruff-kind

2026-11-12 · 210 labelled dev cases (feature 83, question 60, bug 52, documentation 15) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**clef-flash@openrouter** has the highest coverage at 95% accuracy, 22% [17, 29] (API cost $0.14 per 10k, p99 738ms). Its interval overlaps with clef-omni@openrouter, d1.1@openrouter, decider-flash@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is clef-omni@openrouter's, 62% [55, 69].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 56.2% [49, 63] | 0.48 | 0.81 | 0.23 | 22% [17, 29] | 91.5% (81.6%) | 0/210 | 0/210 |
| clef-omni@openrouter | 210 | 61.9% [55, 69] | 0.55 | 0.84 | 0.18 | 16% [11, 21] | 94.1% (82.6%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 57.6% [51, 64] | 0.52 | 0.85 | 0.29 | 5% [2, 9] | 90.9% (63.6%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 59.5% [53, 66] | 0.52 | 0.85 | 0.24 | 8% [4, 11] | 87.5% (65.6%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 56.2% [49, 63] | 0.51 | 0.86 | 0.31 | 12% [8, 17] | 88.0% (71.8%) | 0/210 | 0/210 |
| d1@vercel | 210 | 58.6% [51, 65] | 0.52 | 0.86 | 0.31 | 3% [1, 5] | 100.0% (60.7%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 61.0% [54, 68] | 0.54 | 0.85 | 0.27 | 12% [8, 17] | 92.3% (77.7%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 59.5% [52, 66] | 0.55 | 0.87 | 0.30 | 1% [0, 3] | 100.0% (36.8%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 60.5% [54, 67] | 0.54 | 0.87 | 0.34 | 6% [3, 10] | 84.6% (59.0%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 60.0% [52, 67] | 0.57 | 0.86 | 0.32 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 56.7% [50, 63] | 0.49 | 0.84 | 0.33 | 7% [4, 11] | 80.0% (56.0%) | 0/210 | 0/210 |
| gemini-decision@google | 210 | 60.0% [53, 66] | 0.54 | 0.86 | 0.27 | 7% [4, 10] | 93.3% (72.1%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 58.1% [51, 65] | 0.52 | 0.80 | 0.35 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 55.2% [48, 62] | 0.49 | 0.79 | 0.13 | 2% [0, 5] | 80.0% (34.3%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 60.5% [54, 67] | 0.56 | 0.82 | 0.05 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| luna@decisions | 210 | 58.1% [51, 64] | 0.53 | 0.80 | 0.35 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 59.5% [53, 66] | 0.53 | 0.87 | 0.30 | 7% [4, 11] | 73.3% (48.9%) | 0/210 | 0/210 |
| reflex@openrouter | 210 | 57.1% [50, 63] | 0.51 | 0.85 | 0.37 | 5% [2, 8] | 90.9% (63.6%) | 0/210 | 0/210 |
| span@openrouter | 210 | 60.0% [53, 67] | 0.51 | 0.82 | 0.33 | 15% [10, 20] | 93.8% (81.6%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 22% [17, 29] | 0.91 | met |
| clef-omni@openrouter = | 16% [11, 21] | 0.92 | met |
| d1.1@openrouter = | 12% [8, 17] | 0.99 | met |
| decider-flash@openrouter = | 12% [8, 17] | 0.99 | met |
| span@openrouter = | 15% [10, 20] | 1.00 | met |
| d1-ultra@openrouter | 8% [4, 11] | 0.99 | met |
| elephant@openrouter | 7% [4, 11] | 1.00 | met |
| gemini-decision@google | 7% [4, 10] | 0.99 | met |
| mammoth@openrouter | 7% [4, 11] | 1.00 | met |
| decision-1@openrouter | 6% [3, 10] | 1.00 | met |
| clef@openrouter | 5% [2, 9] | 0.98 | met |
| reflex@openrouter | 5% [2, 8] | 1.00 | met |
| d1@vercel | 3% [1, 5] | 1.00 | met |
| joey@openrouter | 2% [0, 5] | 0.93 | met |
| drex-max@openrouter | 2% [0, 4] | 1.00 | met |
| kev@openrouter | 2% [0, 4] | 0.91 | met |
| decider@openrouter | 1% [0, 3] | 1.00 | met |
| jev:1.14 | 0% [0, 0] | — | met |
| luna@decisions | 0% [0, 0] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 274 ms | 451 ms | 738 ms | 850 ms | 2.7 | 0 | 4 | $0.14 | billed | ○ |
| clef-omni@openrouter | 210 | 205 ms | 339 ms | 662 ms | 717 ms | 3.2 | 0 | 4 | $0.78 | billed | ○ |
| clef@openrouter | 210 | 384 ms | 800 ms | 2743 ms | 4545 ms | 7.1 | 1 | 4 | $1.16 | billed |  |
| d1-ultra@openrouter | 210 | 220 ms | 265 ms | 332 ms | 348 ms | 1.5 | 0 | 4 | $0.17 | billed |  |
| d1.1@openrouter | 210 | 239 ms | 404 ms | 583 ms | 635 ms | 2.4 | 0 | 4 | $0.08 | billed |  |
| d1@vercel | 210 | 266 ms | 358 ms | 552 ms | 667 ms | 2.1 | 0 | 4 | $0.08 | billed |  |
| decider-flash@openrouter | 210 | 136 ms | 163 ms | 200 ms | 348 ms | 1.5 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 221 ms | 416 ms | 1169 ms | 1474 ms | 5.3 | 0 | 4 | $0.09 | billed |  |
| decision-1@openrouter | 210 | 250 ms | 339 ms | 428 ms | 454 ms | 1.7 | 0 | 4 | $0.17 | billed |  |
| drex-max@openrouter | 210 | 382 ms | 3078 ms | 4405 ms | 4905 ms | 11.5 | 1 | 4 | $0.28 | billed |  |
| elephant@openrouter | 210 | 162 ms | 186 ms | 300 ms | 399 ms | 1.8 | 0 | 4 | $0.17 | billed |  |
| gemini-decision@google | 210 | 200 ms | 390 ms | 530 ms | 638 ms | 2.6 | 0 | 4 | $0.50 | estimated |  |
| jev:1.14 | 210 | 103 ms | 122 ms | 209 ms | 260 ms | 2.0 | 0 | 4 | $0.29 | estimated |  |
| joey@openrouter | 210 | 166 ms | 186 ms | 217 ms | 371 ms | 1.3 | 0 | 4 | $0.05 | billed |  |
| kev@openrouter | 210 | 544 ms | 3252 ms | 3981 ms | 4204 ms | 7.3 | 0 | 4 | $0.16 | billed |  |
| luna@decisions | 210 | 220 ms | 411 ms | 583 ms | 3135 ms | 2.6 | 0 | 4 | $0.47 | estimated |  |
| mammoth@openrouter | 210 | 180 ms | 214 ms | 301 ms | 416 ms | 1.7 | 0 | 4 | $0.47 | billed |  |
| reflex@openrouter | 210 | 268 ms | 398 ms | 450 ms | 784 ms | 1.7 | 0 | 4 | $0.20 | billed |  |
| span@openrouter | 210 | 438 ms | 721 ms | 990 ms | 1176 ms | 2.3 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0028 | 16 s (estimated, 210 calls) | 13 min | 4 |
| clef-omni@openrouter | $0.02 | 13 s (estimated, 210 calls) | 10 min | 4 |
| clef@openrouter | $0.02 | 27 s (estimated, 210 calls) | 21 min | 4 |
| d1-ultra@openrouter | $0.0036 | 12 s (estimated, 210 calls) | 9 min | 4 |
| d1.1@openrouter | $0.0017 | 14 s (estimated, 210 calls) | 11 min | 4 |
| d1@vercel | $0.0017 | 15 s (estimated, 210 calls) | 12 min | 4 |
| decider-flash@openrouter | $0.0010 | 7 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0020 | 14 s (estimated, 210 calls) | 11 min | 4 |
| decision-1@openrouter | $0.0036 | 14 s (estimated, 210 calls) | 11 min | 4 |
| drex-max@openrouter | $0.0059 | 59 s (estimated, 210 calls) | 47 min | 4 |
| elephant@openrouter | $0.0035 | 9 s (estimated, 210 calls) | 7 min | 4 |
| gemini-decision@google | $0.01 | 12 s (estimated, 210 calls) | 10 min | 4 |
| jev:1.14 | $0.0062 | 6 s (estimated, 210 calls) | 4 min | 4 |
| joey@openrouter | $0.0010 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0034 | 62 s (estimated, 210 calls) | 49 min | 4 |
| luna@decisions | $0.0099 | 14 s (estimated, 210 calls) | 11 min | 4 |
| mammoth@openrouter | $0.0100 | 10 s (estimated, 210 calls) | 8 min | 4 |
| reflex@openrouter | $0.0041 | 16 s (estimated, 210 calls) | 13 min | 4 |
| span@openrouter | $0.0010 | 25 s (estimated, 210 calls) | 20 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26850 | question | feature | 0.94 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #24887 | question | bug | 0.91 | F632: false positive |
| #27578 | feature | bug | 0.91 | False positive "f-string" message |
| #25140 | question | feature | 0.91 | Rule for orphan literals? |
| #26951 | feature | bug | 0.90 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28998 | question | bug | 0.90 | PLW0108 False positive when lambda executes a list element |

**clef-omni@openrouter** (11)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28308 | question | bug | 0.92 | fatal error while checking app.py please open an issue |
| #24887 | question | bug | 0.92 | F632: false positive |
| #28519 | question | feature | 0.92 | [Formatter feature request] Config option for trailing comma |
| #26850 | question | feature | 0.92 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #26522 | feature | bug | 0.92 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #26449 | question | bug | 0.91 | ruff format strips mandatory parens from multi-exception except claus… |
| #27775 | question | bug | 0.91 | False positive on TRY203 |
| #28675 | question | bug | 0.91 | ERA001 false positive on "# pytest: foo=bar" |

**clef@openrouter** (40)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 0.98 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 0.97 | ERA001 false positive on "# pytest: foo=bar" |
| #26850 | question | feature | 0.97 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #26522 | feature | bug | 0.97 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #24887 | question | bug | 0.96 | F632: false positive |
| #27775 | question | bug | 0.96 | False positive on TRY203 |
| #28998 | question | bug | 0.96 | PLW0108 False positive when lambda executes a list element |

**d1-ultra@openrouter** (22)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #28040 | feature | bug | 0.98 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |
| #26646 | question | bug | 0.97 | F722 False Positive (Syntax error in forward annotation) |
| #28519 | question | feature | 0.97 | [Formatter feature request] Config option for trailing comma |
| #26449 | question | bug | 0.97 | ruff format strips mandatory parens from multi-exception except claus… |
| #26524 | question | bug | 0.97 | Ruff check with --fix removes applicable noqa TRY400 |
| #28998 | question | bug | 0.96 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 0.96 | ERA001 false positive on "# pytest: foo=bar" |

**d1.1@openrouter** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #26449 | question | bug | 0.98 | ruff format strips mandatory parens from multi-exception except claus… |
| #26522 | feature | bug | 0.98 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28998 | question | bug | 0.98 | PLW0108 False positive when lambda executes a list element |
| #28308 | question | bug | 0.98 | fatal error while checking app.py please open an issue |
| #24785 | feature | bug | 0.98 | `unused-async` (`RUF029`) - false negative on methods |
| #28040 | feature | bug | 0.98 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |
| #28675 | question | bug | 0.98 | ERA001 false positive on "# pytest: foo=bar" |

**d1@vercel** (44)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28040 | feature | bug | 1.00 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #27369 | feature | bug | 1.00 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #24785 | feature | bug | 1.00 | `unused-async` (`RUF029`) - false negative on methods |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |

**decider-flash@openrouter** (38)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #24827 | question | bug | 0.99 | N805 auto-fix unsafely renames meaningful parameter to `self` |
| #27537 | feature | bug | 0.98 | `unused-function-argument` - false negative when argument is reassign… |
| #28308 | question | bug | 0.98 | fatal error while checking app.py please open an issue |
| #26522 | feature | bug | 0.98 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #24563 | feature | bug | 0.98 | PLC2701 false positive for a private name import used in a type param… |
| #26449 | question | bug | 0.98 | ruff format strips mandatory parens from multi-exception except claus… |

**decider@openrouter** (40)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #25550 | question | bug | 0.99 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26449 | question | bug | 0.99 | ruff format strips mandatory parens from multi-exception except claus… |
| #24715 | question | bug | 0.99 | PT006 breaks when only one argname |
| #24785 | feature | bug | 0.99 | `unused-async` (`RUF029`) - false negative on methods |
| #27369 | feature | bug | 0.99 | TC001/TC002/TC003 false negative when using a type as generic paramet… |

**decision-1@openrouter** (56)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28040 | feature | bug | 1.00 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |

**drex-max@openrouter** (47)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #24785 | feature | bug | 1.00 | `unused-async` (`RUF029`) - false negative on methods |

**elephant@openrouter** (52)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 0.99 | ERA001 false positive on "# pytest: foo=bar" |
| #24827 | question | bug | 0.99 | N805 auto-fix unsafely renames meaningful parameter to `self` |
| #26951 | feature | bug | 0.99 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28040 | feature | bug | 0.99 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |

**gemini-decision@google** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28519 | question | feature | 0.99 | [Formatter feature request] Config option for trailing comma |
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #27246 | question | feature | 0.99 | Add possibility to disable autofixes for certain files |
| #28097 | question | feature | 0.99 | Option to use `code:name` for rules and output |
| #26850 | question | feature | 0.99 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #26522 | feature | bug | 0.99 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28308 | question | bug | 0.98 | fatal error while checking app.py please open an issue |

**jev:1.14** (61)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28308 | question | bug | 1.00 | fatal error while checking app.py please open an issue |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #28512 | question | bug | 1.00 | `F821` does not understand the intention of the following code |
| #27578 | feature | bug | 1.00 | False positive "f-string" message |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #27537 | feature | bug | 1.00 | `unused-function-argument` - false negative when argument is reassign… |

**joey@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28519 | question | feature | 0.91 | [Formatter feature request] Config option for trailing comma |

**kev@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28519 | question | feature | 0.91 | [Formatter feature request] Config option for trailing comma |

**luna@decisions** (64)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28308 | question | bug | 1.00 | fatal error while checking app.py please open an issue |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #28040 | feature | bug | 1.00 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |

**mammoth@openrouter** (41)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #24827 | question | bug | 1.00 | N805 auto-fix unsafely renames meaningful parameter to `self` |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #24887 | question | bug | 1.00 | F632: false positive |

**reflex@openrouter** (64)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #26524 | question | bug | 1.00 | Ruff check with --fix removes applicable noqa TRY400 |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #27432 | question | bug | 1.00 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #24715 | question | bug | 1.00 | PT006 breaks when only one argname |
| #27775 | question | bug | 1.00 | False positive on TRY203 |

**span@openrouter** (57)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #27246 | question | feature | 1.00 | Add possibility to disable autofixes for certain files |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28097 | question | feature | 1.00 | Option to use `code:name` for rules and output |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #26449 | question | bug | 0.99 | ruff format strips mandatory parens from multi-exception except claus… |
| #28675 | question | bug | 0.99 | ERA001 false positive on "# pytest: foo=bar" |
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |


## Cases the models disagree on (12 of 70)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28097 | question | feature (0.81) | feature (0.89) | feature (0.92) | feature (0.94) | feature (0.97) | feature (0.99) | feature (0.97) | feature (0.97) | feature (1.00) | feature (0.99) | feature (0.99) | feature (0.99) | feature (1.00) | question (0.49) | feature (0.66) | feature (0.91) | feature (0.97) | feature (1.00) | feature (1.00) | Option to use `code:name` for rules and output |
| #27578 | feature | bug (0.91) | bug (0.89) | bug (0.94) | bug (0.96) | bug (0.87) | bug (0.98) | bug (0.91) | bug (0.95) | bug (0.99) | bug (0.97) | bug (0.98) | feature (0.47) | bug (1.00) | bug (0.72) | bug (0.48) | bug (0.96) | bug (0.93) | bug (1.00) | bug (0.99) | False positive "f-string" message |
| #26879 | feature | feature (0.83) | feature (0.89) | feature (0.85) | feature (0.76) | bug (0.46) | feature (0.77) | feature (0.85) | feature (0.82) | feature (0.93) | feature (0.90) | feature (0.97) | feature (0.86) | feature (0.79) | question (0.35) | feature (0.50) | feature (1.00) | feature (0.90) | feature (0.95) | feature (0.95) | Widen accepted `__all__` and `__slots__` formats to include single-ch… |
| #25296 | feature | feature (0.97) | feature (0.93) | feature (0.97) | feature (0.98) | feature (0.99) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | bug (0.35) | feature (0.83) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | Rule idea: class-level None can make runtime protocol checks slow |
| #24549 | question | bug (0.55) | bug (0.48) | bug (0.76) | bug (0.82) | bug (0.79) | bug (0.82) | question (0.57) | bug (0.84) | bug (0.68) | bug (0.94) | bug (0.85) | bug (0.84) | bug (0.96) | bug (0.71) | question (0.59) | bug (1.00) | bug (0.93) | bug (1.00) | bug (0.95) | Serious slowdown of jupyter notebooks in vs code |
| #24545 | feature | feature (0.90) | feature (0.90) | feature (0.73) | feature (0.97) | feature (0.90) | feature (0.98) | feature (0.86) | feature (0.98) | feature (0.98) | feature (0.99) | feature (0.70) | feature (0.99) | feature (0.85) | documentation (0.66) | feature (0.38) | feature (0.87) | feature (0.99) | feature (1.00) | feature (0.99) | Prefer `prefixmatch` over `match` |
| #26456 | feature | feature (0.90) | feature (0.92) | feature (0.91) | feature (0.93) | feature (0.94) | feature (0.98) | feature (0.96) | feature (0.98) | feature (1.00) | feature (0.99) | feature (0.97) | feature (0.97) | feature (0.98) | question (0.49) | feature (0.49) | feature (0.98) | feature (0.95) | feature (1.00) | feature (1.00) | Detecting returning exception instead of raising |
| #26656 | feature | feature (0.94) | feature (0.90) | feature (0.89) | feature (0.98) | feature (0.99) | feature (0.94) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (0.90) | feature (0.99) | feature (0.97) | documentation (0.34) | feature (0.44) | feature (0.53) | feature (0.99) | feature (1.00) | feature (0.95) | Rule suggestion: `functools.partial` call with singular argument |
| #27607 | question | bug (0.70) | bug (0.71) | bug (0.91) | bug (0.78) | bug (0.68) | documentation (0.62) | bug (0.96) | bug (0.73) | bug (1.00) | bug (0.83) | bug (0.95) | bug (0.79) | bug (0.91) | bug (0.76) | bug (0.65) | bug (0.99) | bug (0.90) | bug (0.98) | bug (0.98) | ruff rejects documented `indent-width` setting |
| #25386 | bug | bug (0.67) | bug (0.67) | bug (0.88) | bug (0.84) | bug (0.85) | bug (0.94) | bug (0.64) | bug (0.98) | bug (0.92) | bug (0.98) | bug (0.84) | bug (0.93) | bug (0.96) | bug (0.51) | question (0.42) | bug (0.98) | bug (0.98) | bug (1.00) | bug (0.90) | Schrödinger's comment: it is both commented-out code and a comment th… |
| #25105 | feature | feature (0.89) | feature (0.86) | feature (0.96) | feature (0.92) | feature (0.93) | feature (0.97) | feature (0.94) | feature (0.98) | feature (1.00) | feature (0.99) | feature (0.98) | feature (0.99) | feature (0.99) | question (0.58) | feature (0.68) | feature (0.97) | feature (0.99) | feature (1.00) | feature (1.00) | `pyupgrade` should rewrite `abc.{abstractclassmethod, abstractstaticm… |
| #28567 | feature | feature (0.87) | feature (0.90) | feature (0.93) | feature (0.98) | feature (0.98) | feature (0.97) | feature (0.97) | feature (0.99) | feature (0.98) | feature (0.98) | feature (0.90) | feature (0.98) | feature (0.96) | question (0.42) | feature (0.42) | feature (0.90) | feature (0.97) | feature (0.84) | feature (1.00) | Support flake8-if-expr |
