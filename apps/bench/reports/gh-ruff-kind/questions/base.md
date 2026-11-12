# gh-ruff-kind

2026-11-11 · 210 labelled dev cases (feature 83, question 60, bug 52, documentation 15) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**clef-flash@openrouter** has the highest coverage at 95% accuracy, 24% [18, 30] (API cost $0.13 per 10k, p99 1841ms). Its interval overlaps with clef-omni@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is clef-omni@openrouter's, 62% [55, 69].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 56.7% [50, 63] | 0.49 | 0.80 | 0.23 | 24% [18, 30] | 90.0% (80.1%) | 0/210 | 0/210 |
| clef-omni@openrouter | 210 | 61.9% [55, 69] | 0.55 | 0.84 | 0.18 | 16% [11, 22] | 94.1% (82.6%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 58.6% [51, 65] | 0.52 | 0.85 | 0.30 | 6% [3, 9] | 91.7% (66.1%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 60.0% [53, 67] | 0.53 | 0.87 | 0.24 | 4% [2, 7] | 77.8% (45.0%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 57.1% [50, 64] | 0.52 | 0.86 | 0.31 | 1% [0, 3] | 66.7% (13.5%) | 0/210 | 0/210 |
| d1@vercel | 210 | 58.6% [51, 65] | 0.51 | 0.86 | 0.31 | 3% [1, 5] | 83.3% (41.8%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 61.0% [54, 67] | 0.54 | 0.85 | 0.27 | 12% [8, 17] | 92.3% (77.7%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 59.5% [52, 66] | 0.55 | 0.87 | 0.30 | 3% [1, 5] | 83.3% (41.8%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 60.5% [53, 67] | 0.55 | 0.87 | 0.33 | 6% [2, 9] | 83.3% (56.2%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 59.5% [52, 66] | 0.55 | 0.86 | 0.32 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 56.7% [50, 63] | 0.49 | 0.84 | 0.33 | 7% [4, 11] | 80.0% (56.0%) | 0/210 | 0/210 |
| gemini-decision@openrouter | 210 | 59.5% [53, 66] | 0.54 | 0.86 | 0.28 | 1% [0, 2] | 50.0% (2.5%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 57.6% [51, 64] | 0.51 | 0.80 | 0.36 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 55.2% [48, 62] | 0.49 | 0.79 | 0.13 | 2% [0, 5] | 80.0% (34.3%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 60.5% [54, 67] | 0.56 | 0.82 | 0.07 | 1% [0, 2] | 50.0% (2.5%) | 0/210 | 0/210 |
| luna@decisions | 210 | 58.1% [51, 65] | 0.53 | 0.80 | 0.35 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 59.5% [52, 66] | 0.53 | 0.87 | 0.30 | 7% [4, 11] | 73.3% (48.9%) | 0/210 | 0/210 |
| reflex@openrouter | 210 | 57.1% [50, 63] | 0.51 | 0.85 | 0.37 | 5% [2, 8] | 90.9% (63.6%) | 0/210 | 0/210 |
| span@openrouter | 210 | 60.0% [53, 66] | 0.51 | 0.82 | 0.33 | 15% [11, 20] | 93.8% (81.6%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 24% [18, 30] | 0.91 | met |
| clef-omni@openrouter = | 16% [11, 22] | 0.92 | met |
| span@openrouter = | 15% [11, 20] | 1.00 | met |
| decider-flash@openrouter | 12% [8, 17] | 0.99 | met |
| elephant@openrouter | 7% [4, 11] | 1.00 | met |
| mammoth@openrouter | 7% [4, 11] | 1.00 | met |
| clef@openrouter | 6% [3, 9] | 0.97 | met |
| decision-1@openrouter | 6% [2, 9] | 1.00 | met |
| reflex@openrouter | 5% [2, 8] | 1.00 | met |
| d1-ultra@openrouter | 4% [2, 7] | 0.99 | met |
| d1@vercel | 3% [1, 5] | 1.00 | met |
| decider@openrouter | 3% [1, 5] | 1.00 | met |
| joey@openrouter | 2% [0, 5] | 0.93 | met |
| drex-max@openrouter | 2% [0, 4] | 1.00 | met |
| d1.1@openrouter | 1% [0, 3] | 0.99 | met |
| gemini-decision@openrouter | 1% [0, 2] | 1.00 | met |
| kev@openrouter | 1% [0, 2] | 0.95 | met |
| jev:1.14 | 0% [0, 0] | — | met |
| luna@decisions | 0% [0, 0] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 339 ms | 636 ms | 1841 ms | 2567 ms | 5.4 | 0 | 4 | $0.13 | billed | ○ |
| clef-omni@openrouter | 210 | 238 ms | 399 ms | 991 ms | 2857 ms | 4.2 | 0 | 4 | $0.78 | billed | ○ |
| clef@openrouter | 210 | 414 ms | 674 ms | 1226 ms | 2062 ms | 3.0 | 0 | 4 | $1.13 | billed |  |
| d1-ultra@openrouter | 210 | 291 ms | 397 ms | 574 ms | 670 ms | 2.0 | 0 | 4 | $0.17 | billed |  |
| d1.1@openrouter | 210 | 300 ms | 453 ms | 810 ms | 1071 ms | 2.7 | 0 | 4 | $0.08 | billed |  |
| d1@vercel | 210 | 271 ms | 373 ms | 499 ms | 537 ms | 1.8 | 0 | 4 | $0.08 | billed |  |
| decider-flash@openrouter | 210 | 143 ms | 240 ms | 352 ms | 8100 ms | 2.5 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 342 ms | 509 ms | 1049 ms | 1636 ms | 3.1 | 0 | 4 | $0.09 | billed |  |
| decision-1@openrouter | 210 | 272 ms | 388 ms | 481 ms | 783 ms | 1.8 | 0 | 4 | $0.17 | billed |  |
| drex-max@openrouter | 210 | 496 ms | 810 ms | 1386 ms | 1860 ms | 2.8 | 1 | 4 | $0.28 | billed |  |
| elephant@openrouter | 210 | 268 ms | 297 ms | 527 ms | 828 ms | 2.0 | 0 | 4 | $0.17 | billed |  |
| gemini-decision@openrouter | 210 | 428 ms | 560 ms | 736 ms | 882 ms | 1.7 | 1 | 4 | $0.49 | billed |  |
| jev:1.14 | 210 | 114 ms | 227 ms | 258 ms | 349 ms | 2.3 | 0 | 4 | $0.29 | estimated | ○ |
| joey@openrouter | 210 | 267 ms | 296 ms | 321 ms | 336 ms | 1.2 | 0 | 4 | $0.05 | billed | ○ |
| kev@openrouter | 210 | 608 ms | 765 ms | 1141 ms | 1394 ms | 1.9 | 0 | 4 | $0.16 | billed |  |
| luna@decisions | 210 | 306 ms | 463 ms | 635 ms | 705 ms | 2.1 | 0 | 4 | $0.47 | estimated |  |
| mammoth@openrouter | 210 | 272 ms | 846 ms | 2324 ms | 3099 ms | 8.5 | 0 | 4 | $0.47 | billed |  |
| reflex@openrouter | 210 | 270 ms | 372 ms | 437 ms | 545 ms | 1.6 | 0 | 4 | $0.20 | billed |  |
| span@openrouter | 210 | 332 ms | 603 ms | 996 ms | 1029 ms | 3.0 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0027 | 22 s (estimated, 210 calls) | 17 min | 4 |
| clef-omni@openrouter | $0.02 | 16 s (estimated, 210 calls) | 12 min | 4 |
| clef@openrouter | $0.02 | 24 s (estimated, 210 calls) | 19 min | 4 |
| d1-ultra@openrouter | $0.0036 | 16 s (estimated, 210 calls) | 13 min | 4 |
| d1.1@openrouter | $0.0017 | 17 s (estimated, 210 calls) | 13 min | 4 |
| d1@vercel | $0.0017 | 15 s (estimated, 210 calls) | 12 min | 4 |
| decider-flash@openrouter | $0.0010 | 10 s (estimated, 210 calls) | 8 min | 4 |
| decider@openrouter | $0.0020 | 20 s (estimated, 210 calls) | 16 min | 4 |
| decision-1@openrouter | $0.0036 | 15 s (estimated, 210 calls) | 12 min | 4 |
| drex-max@openrouter | $0.0059 | 28 s (estimated, 210 calls) | 22 min | 4 |
| elephant@openrouter | $0.0035 | 13 s (estimated, 210 calls) | 11 min | 4 |
| gemini-decision@openrouter | $0.01 | 22 s (estimated, 210 calls) | 18 min | 4 |
| jev:1.14 | $0.0062 | 8 s (estimated, 210 calls) | 6 min | 4 |
| joey@openrouter | $0.0010 | 13 s (estimated, 210 calls) | 10 min | 4 |
| kev@openrouter | $0.0034 | 33 s (estimated, 210 calls) | 27 min | 4 |
| luna@decisions | $0.0099 | 17 s (estimated, 210 calls) | 13 min | 4 |
| mammoth@openrouter | $0.0100 | 21 s (estimated, 210 calls) | 16 min | 4 |
| reflex@openrouter | $0.0042 | 15 s (estimated, 210 calls) | 12 min | 4 |
| span@openrouter | $0.0010 | 20 s (estimated, 210 calls) | 16 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26850 | question | feature | 0.94 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #27775 | question | bug | 0.92 | False positive on TRY203 |
| #24887 | question | bug | 0.91 | F632: false positive |
| #25140 | question | feature | 0.91 | Rule for orphan literals? |
| #27578 | feature | bug | 0.91 | False positive "f-string" message |
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

**clef@openrouter** (39)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 0.97 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #26522 | feature | bug | 0.97 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28675 | question | bug | 0.97 | ERA001 false positive on "# pytest: foo=bar" |
| #26850 | question | feature | 0.97 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #28998 | question | bug | 0.96 | PLW0108 False positive when lambda executes a list element |
| #24887 | question | bug | 0.96 | F632: false positive |
| #27775 | question | bug | 0.96 | False positive on TRY203 |

**d1-ultra@openrouter** (23)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28675 | question | bug | 0.98 | ERA001 false positive on "# pytest: foo=bar" |
| #28998 | question | bug | 0.98 | PLW0108 False positive when lambda executes a list element |
| #26449 | question | bug | 0.98 | ruff format strips mandatory parens from multi-exception except claus… |
| #27379 | question | bug | 0.98 | False positive Undefined name for self-referential return annotation … |
| #26646 | question | bug | 0.97 | F722 False Positive (Syntax error in forward annotation) |
| #28308 | question | bug | 0.97 | fatal error while checking app.py please open an issue |
| #24887 | question | bug | 0.97 | F632: false positive |
| #28040 | feature | bug | 0.96 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |

**d1.1@openrouter** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 0.99 | ruff format strips mandatory parens from multi-exception except claus… |
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #27775 | question | bug | 0.99 | False positive on TRY203 |
| #26522 | feature | bug | 0.98 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28675 | question | bug | 0.98 | ERA001 false positive on "# pytest: foo=bar" |
| #27432 | question | bug | 0.98 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #24785 | feature | bug | 0.98 | `unused-async` (`RUF029`) - false negative on methods |

**d1@vercel** (44)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28308 | question | bug | 1.00 | fatal error while checking app.py please open an issue |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |

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
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #25550 | question | bug | 0.99 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26449 | question | bug | 0.99 | ruff format strips mandatory parens from multi-exception except claus… |
| #24715 | question | bug | 0.99 | PT006 breaks when only one argname |
| #24785 | feature | bug | 0.99 | `unused-async` (`RUF029`) - false negative on methods |
| #27369 | feature | bug | 0.99 | TC001/TC002/TC003 false negative when using a type as generic paramet… |

**decision-1@openrouter** (57)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #28040 | feature | bug | 1.00 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |
| #28097 | question | feature | 1.00 | Option to use `code:name` for rules and output |

**drex-max@openrouter** (46)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #24785 | feature | bug | 1.00 | `unused-async` (`RUF029`) - false negative on methods |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #27775 | question | bug | 1.00 | False positive on TRY203 |

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

**gemini-decision@openrouter** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28519 | question | feature | 0.99 | [Formatter feature request] Config option for trailing comma |
| #26850 | question | feature | 0.99 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #24785 | feature | bug | 0.99 | `unused-async` (`RUF029`) - false negative on methods |
| #28097 | question | feature | 0.99 | Option to use `code:name` for rules and output |
| #26951 | feature | bug | 0.98 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27246 | question | feature | 0.98 | Add possibility to disable autofixes for certain files |

**jev:1.14** (61)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28308 | question | bug | 1.00 | fatal error while checking app.py please open an issue |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #28512 | question | bug | 1.00 | `F821` does not understand the intention of the following code |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #27537 | feature | bug | 1.00 | `unused-function-argument` - false negative when argument is reassign… |
| #27578 | feature | bug | 1.00 | False positive "f-string" message |

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
| #24887 | question | bug | 1.00 | F632: false positive |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |

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

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28097 | question | feature (0.81) | feature (0.89) | feature (0.93) | feature (0.94) | feature (0.93) | feature (0.97) | feature (0.97) | feature (0.97) | feature (1.00) | feature (0.99) | feature (0.99) | feature (0.99) | feature (1.00) | question (0.49) | feature (0.66) | feature (0.91) | feature (0.97) | feature (1.00) | feature (1.00) | Option to use `code:name` for rules and output |
| #26879 | feature | feature (0.83) | feature (0.89) | feature (0.85) | feature (0.72) | feature (0.58) | feature (0.67) | feature (0.85) | feature (0.85) | feature (0.92) | feature (0.90) | feature (0.97) | feature (0.94) | feature (0.81) | question (0.35) | feature (0.50) | feature (1.00) | feature (0.90) | feature (0.95) | feature (0.95) | Widen accepted `__all__` and `__slots__` formats to include single-ch… |
| #26278 | question | bug (0.78) | bug (0.83) | bug (0.85) | bug (0.54) | bug (0.69) | bug (0.95) | bug (0.82) | bug (0.56) | bug (0.95) | bug (0.53) | bug (0.87) | question (0.54) | bug (1.00) | bug (0.52) | bug (0.58) | bug (0.91) | bug (0.77) | bug (0.92) | bug (0.98) | Ruff 0.15.14 ignores critical bad import in favor of reporting UP031 … |
| #25296 | feature | feature (0.97) | feature (0.93) | feature (0.97) | feature (0.99) | feature (0.99) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | bug (0.35) | feature (0.83) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | Rule idea: class-level None can make runtime protocol checks slow |
| #24549 | question | bug (0.55) | bug (0.48) | bug (0.75) | bug (0.88) | bug (0.74) | bug (0.66) | question (0.57) | bug (0.84) | bug (0.73) | bug (0.95) | bug (0.85) | bug (0.92) | bug (0.96) | bug (0.71) | question (0.59) | bug (1.00) | bug (0.93) | bug (1.00) | bug (0.95) | Serious slowdown of jupyter notebooks in vs code |
| #24545 | feature | feature (0.90) | feature (0.90) | feature (0.80) | feature (0.98) | feature (0.88) | feature (0.99) | feature (0.86) | feature (0.98) | feature (0.98) | feature (0.99) | feature (0.70) | feature (0.99) | feature (0.88) | documentation (0.66) | feature (0.37) | feature (0.87) | feature (0.99) | feature (1.00) | feature (0.99) | Prefer `prefixmatch` over `match` |
| #26456 | feature | feature (0.92) | feature (0.92) | feature (0.89) | feature (0.94) | feature (0.94) | feature (0.99) | feature (0.96) | feature (0.98) | feature (1.00) | feature (0.99) | feature (0.97) | feature (0.96) | feature (0.98) | question (0.49) | feature (0.50) | feature (0.98) | feature (0.95) | feature (1.00) | feature (1.00) | Detecting returning exception instead of raising |
| #26656 | feature | feature (0.94) | feature (0.90) | feature (0.91) | feature (0.97) | feature (0.99) | feature (0.95) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (0.90) | feature (0.99) | feature (0.96) | documentation (0.34) | feature (0.45) | feature (0.53) | feature (0.99) | feature (1.00) | feature (0.95) | Rule suggestion: `functools.partial` call with singular argument |
| #27607 | question | bug (0.70) | bug (0.71) | bug (0.91) | bug (0.80) | bug (0.63) | documentation (0.64) | bug (0.96) | bug (0.73) | bug (1.00) | bug (0.74) | bug (0.95) | bug (0.80) | bug (0.92) | bug (0.76) | bug (0.65) | bug (0.99) | bug (0.90) | bug (0.98) | bug (0.98) | ruff rejects documented `indent-width` setting |
| #25386 | bug | bug (0.67) | bug (0.67) | bug (0.84) | bug (0.82) | bug (0.88) | bug (0.96) | bug (0.64) | bug (0.98) | bug (0.91) | bug (0.98) | bug (0.84) | bug (0.95) | bug (0.96) | bug (0.51) | question (0.43) | bug (0.98) | bug (0.98) | bug (1.00) | bug (0.90) | Schrödinger's comment: it is both commented-out code and a comment th… |
| #28567 | feature | feature (0.89) | feature (0.90) | feature (0.93) | feature (0.97) | feature (0.99) | feature (0.98) | feature (0.97) | feature (0.99) | feature (0.98) | feature (0.98) | feature (0.90) | feature (0.98) | feature (0.97) | question (0.42) | feature (0.42) | feature (0.90) | feature (0.96) | feature (0.84) | feature (1.00) | Support flake8-if-expr |
| #27304 | documentation | feature (0.86) | bug (0.77) | bug (0.92) | bug (0.79) | bug (0.81) | bug (0.91) | bug (0.86) | bug (0.95) | bug (0.98) | bug (0.95) | bug (0.95) | bug (0.80) | bug (0.93) | bug (0.51) | bug (0.42) | bug (0.78) | bug (0.85) | bug (1.00) | bug (0.83) | C417 - map and generator expressions are not equivalent |
