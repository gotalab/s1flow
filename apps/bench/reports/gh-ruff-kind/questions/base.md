# gh-ruff-kind

2026-11-18 · 210 labelled dev cases (feature 83, question 60, bug 52, documentation 15) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

clef-flash@openrouter has the highest coverage at 90% accuracy, 27% [20, 33] (API cost $0.13 per 10k, p99 780ms). Its interval overlaps with clef-omni@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2-ultra, decider-flash@openrouter, decider@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is clef-omni@openrouter's, 62% [55, 69].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 56.2% [49, 63] | 0.48 | 0.80 | 0.23 | 27% [20, 33] | 85.7% (75.7%) | 0.0% (0/210) | 0/210 |
| clef-omni@openrouter | 210 | 61.9% [55, 69] | 0.55 | 0.84 | 0.18 | 22% [16, 28] | 87.0% (75.9%) | 0.0% (0/210) | 0/210 |
| clef@openrouter | 210 | 58.1% [51, 65] | 0.51 | 0.84 | 0.30 | 8% [5, 12] | 88.2% (67.4%) | 0.0% (0/210) | 0/210 |
| d1-ultra@openrouter | 210 | 59.0% [52, 66] | 0.52 | 0.86 | 0.25 | 16% [11, 21] | 85.3% (71.5%) | 0.0% (0/210) | 0/210 |
| d1.1@openrouter | 210 | 57.1% [50, 64] | 0.52 | 0.86 | 0.29 | 16% [11, 22] | 85.3% (71.5%) | 0.0% (0/210) | 0/210 |
| d1.2 | 210 | 57.6% [51, 64] | 0.52 | 0.85 | 0.28 | 5% [2, 8] | 70.0% (39.3%) | 0.0% (0/210) | 0/210 |
| d1.2-ultra | 210 | 57.6% [51, 64] | 0.52 | 0.87 | 0.25 | 20% [15, 26] | 83.3% (71.0%) | 0.0% (0/210) | 0/210 |
| d1@vercel | 210 | 57.1% [50, 64] | 0.50 | 0.85 | 0.33 | 4% [2, 7] | 66.7% (34.5%) | 0.0% (0/210) | 0/210 |
| decider-flash@openrouter | 210 | 61.0% [54, 68] | 0.54 | 0.85 | 0.27 | 20% [15, 26] | 88.4% (77.1%) | 0.0% (0/210) | 0/210 |
| decider@openrouter | 210 | 59.5% [52, 66] | 0.55 | 0.87 | 0.30 | 17% [12, 22] | 85.7% (72.3%) | 0.0% (0/210) | 0/210 |
| decision-1.1@openrouter | 210 | 61.4% [55, 68] | 0.55 | 0.84 | 0.32 | 5% [2, 8] | 81.8% (53.0%) | 0.0% (0/210) | 0/210 |
| decision-1@openrouter | 210 | 60.5% [54, 67] | 0.54 | 0.87 | 0.33 | 14% [10, 19] | 82.8% (67.1%) | 0.0% (0/210) | 0/210 |
| drex-max@openrouter | 210 | 59.5% [52, 66] | 0.55 | 0.86 | 0.32 | 4% [1, 7] | 75.0% (40.0%) | 0.0% (0/210) | 0/210 |
| elephant@openrouter | 210 | 56.7% [50, 63] | 0.49 | 0.84 | 0.33 | 13% [9, 18] | 89.3% (74.6%) | 0.0% (0/210) | 0/210 |
| gemini-decision@google | 210 | 60.0% [53, 67] | 0.54 | 0.86 | 0.27 | 14% [10, 19] | 86.2% (71.2%) | 0.0% (0/210) | 0/210 |
| jev:1.14 | 210 | 57.6% [51, 64] | 0.52 | 0.79 | 0.35 | 0% [0, 0] | — (0.0%) | 0.0% (0/210) | 0/210 |
| joey@openrouter | 210 | 55.2% [48, 62] | 0.49 | 0.79 | 0.13 | 5% [2, 9] | 72.7% (43.6%) | 0.0% (0/210) | 0/210 |
| kev@openrouter | 210 | 60.5% [53, 67] | 0.56 | 0.82 | 0.05 | 10% [6, 13] | 80.0% (59.9%) | 0.0% (0/210) | 0/210 |
| luna@decisions | 210 | 58.1% [51, 65] | 0.53 | 0.80 | 0.35 | 0% [0, 0] | — (0.0%) | 0.0% (0/210) | 0/210 |
| mammoth@openrouter | 210 | 59.5% [53, 66] | 0.53 | 0.87 | 0.30 | 12% [8, 17] | 84.0% (67.0%) | 0.0% (0/210) | 0/210 |
| reflex@openrouter | 210 | 57.1% [50, 64] | 0.51 | 0.85 | 0.37 | 6% [3, 9] | 91.7% (66.1%) | 0.0% (0/210) | 0/210 |
| span@openrouter | 210 | 60.0% [53, 67] | 0.51 | 0.82 | 0.33 | 21% [16, 27] | 91.1% (80.8%) | 0.0% (0/210) | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 90% accuracy | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 27% [20, 33] | 0.91 | met |
| clef-omni@openrouter = | 22% [16, 28] | 0.92 | met |
| d1-ultra@openrouter = | 16% [11, 21] | 0.97 | met |
| d1.1@openrouter = | 16% [11, 22] | 0.99 | met |
| d1.2-ultra = | 20% [15, 26] | 0.95 | met |
| decider-flash@openrouter = | 20% [15, 26] | 0.98 | met |
| decider@openrouter = | 17% [12, 22] | 0.99 | met |
| span@openrouter = | 21% [16, 27] | 1.00 | met |
| decision-1@openrouter | 14% [10, 19] | 1.00 | met |
| gemini-decision@google | 14% [10, 19] | 0.99 | met |
| elephant@openrouter | 13% [9, 18] | 0.99 | met |
| mammoth@openrouter | 12% [8, 17] | 1.00 | met |
| kev@openrouter | 10% [6, 13] | 0.83 | met |
| clef@openrouter | 8% [5, 12] | 0.97 | met |
| reflex@openrouter | 6% [3, 9] | 1.00 | met |
| decision-1.1@openrouter | 5% [2, 8] | 1.00 | met |
| joey@openrouter | 5% [2, 9] | 0.90 | met |
| d1.2 | 5% [2, 8] | 0.97 | met |
| d1@vercel | 4% [2, 7] | 1.00 | met |
| drex-max@openrouter | 4% [1, 7] | 1.00 | met |
| jev:1.14 | 0% [0, 0] | — | met |
| luna@decisions | 0% [0, 0] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 272 ms | 360 ms | 780 ms | 916 ms | 2.9 | 0 | 4 | $0.13 | billed | ○ |
| clef-omni@openrouter | 210 | 226 ms | 1239 ms | 3654 ms | 4853 ms | 16.2 | 0 | 4 | $0.78 | billed |  |
| clef@openrouter | 210 | 299 ms | 657 ms | 2857 ms | 3983 ms | 9.6 | 0 | 4 | $1.12 | billed |  |
| d1-ultra@openrouter | 210 | 792 ms | 5736 ms | 6194 ms | 6408 ms | 7.8 | 25 | 4 | $0.17 | billed |  |
| d1.1@openrouter | 210 | 311 ms | 473 ms | 672 ms | 709 ms | 2.2 | 0 | 4 | $0.08 | billed |  |
| d1.2 | 210 | 115 ms | 180 ms | 850 ms | 1339 ms | 7.4 | 0 | 4 | $0.08 | billed |  |
| d1.2-ultra | 210 | 118 ms | 157 ms | 510 ms | 3110 ms | 4.3 | 1 | 4 | $0.17 | billed |  |
| d1@vercel | 210 | 645 ms | 4113 ms | 7287 ms | 8365 ms | 11.3 | 7 | 4 | $0.08 | billed |  |
| decider-flash@openrouter | 210 | 130 ms | 147 ms | 253 ms | 413 ms | 1.9 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 211 ms | 315 ms | 1026 ms | 1487 ms | 4.9 | 0 | 4 | $0.09 | billed |  |
| decision-1.1@openrouter | 210 | 224 ms | 249 ms | 385 ms | 543 ms | 1.7 | 0 | 4 | $0.18 | billed |  |
| decision-1@openrouter | 210 | 232 ms | 299 ms | 385 ms | 530 ms | 1.7 | 0 | 4 | $0.17 | billed |  |
| drex-max@openrouter | 210 | 409 ms | 650 ms | 1022 ms | 1260 ms | 2.5 | 0 | 4 | $0.28 | billed |  |
| elephant@openrouter | 210 | 161 ms | 176 ms | 236 ms | 270 ms | 1.5 | 0 | 4 | $0.17 | billed | ○ |
| gemini-decision@google | 210 | 304 ms | 384 ms | 428 ms | 447 ms | 1.4 | 0 | 4 | $0.50 | estimated |  |
| jev:1.14 | 210 | 108 ms | 144 ms | 193 ms | 447 ms | 1.8 | 0 | 4 | $0.29 | estimated | ○ |
| joey@openrouter | 210 | 162 ms | 176 ms | 258 ms | 372 ms | 1.6 | 0 | 4 | $0.05 | billed |  |
| kev@openrouter | 210 | 625 ms | 907 ms | 1154 ms | 1385 ms | 1.8 | 0 | 4 | $0.16 | billed |  |
| luna@decisions | 210 | 190 ms | 352 ms | 524 ms | 572 ms | 2.8 | 0 | 4 | $0.47 | estimated |  |
| mammoth@openrouter | 210 | 178 ms | 199 ms | 234 ms | 330 ms | 1.3 | 0 | 4 | $0.47 | billed | ○ |
| reflex@openrouter | 210 | 249 ms | 288 ms | 345 ms | 387 ms | 1.4 | 0 | 4 | $0.20 | billed |  |
| span@openrouter | 210 | 460 ms | 677 ms | 917 ms | 1010 ms | 2.0 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0027 | 15 s (estimated, 210 calls) | 12 min | 4 |
| clef-omni@openrouter | $0.02 | 27 s (estimated, 210 calls) | 21 min | 4 |
| clef@openrouter | $0.02 | 24 s (estimated, 210 calls) | 19 min | 4 |
| d1-ultra@openrouter | $0.0036 | 2 min (estimated, 210 calls) | 81 min | 4 |
| d1.1@openrouter | $0.0017 | 17 s (estimated, 210 calls) | 13 min | 4 |
| d1.2 | $0.0017 | 8 s (estimated, 210 calls) | 6 min | 4 |
| d1.2-ultra | $0.0036 | 8 s (estimated, 210 calls) | 6 min | 4 |
| d1@vercel | $0.0017 | 70 s (estimated, 210 calls) | 56 min | 4 |
| decider-flash@openrouter | $0.0010 | 7 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0020 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decision-1.1@openrouter | $0.0039 | 12 s (estimated, 210 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0036 | 13 s (estimated, 210 calls) | 10 min | 4 |
| drex-max@openrouter | $0.0059 | 23 s (estimated, 210 calls) | 18 min | 4 |
| elephant@openrouter | $0.0035 | 9 s (estimated, 210 calls) | 7 min | 4 |
| gemini-decision@google | $0.01 | 16 s (estimated, 210 calls) | 12 min | 4 |
| jev:1.14 | $0.0062 | 6 s (estimated, 210 calls) | 5 min | 4 |
| joey@openrouter | $0.0010 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0034 | 35 s (estimated, 210 calls) | 28 min | 4 |
| luna@decisions | $0.0099 | 12 s (estimated, 210 calls) | 9 min | 4 |
| mammoth@openrouter | $0.0100 | 10 s (estimated, 210 calls) | 8 min | 4 |
| reflex@openrouter | $0.0042 | 13 s (estimated, 210 calls) | 11 min | 4 |
| span@openrouter | $0.0010 | 26 s (estimated, 210 calls) | 21 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 90%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26850 | question | feature | 0.94 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #28998 | question | bug | 0.92 | PLW0108 False positive when lambda executes a list element |
| #27775 | question | bug | 0.92 | False positive on TRY203 |
| #24887 | question | bug | 0.91 | F632: false positive |
| #25140 | question | feature | 0.91 | Rule for orphan literals? |
| #27578 | feature | bug | 0.91 | False positive "f-string" message |
| #26951 | feature | bug | 0.90 | RUF052 false negatives for `class`, `def`, and `import` bindings |

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

**clef@openrouter** (41)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26951 | feature | bug | 0.97 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #26522 | feature | bug | 0.97 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28675 | question | bug | 0.97 | ERA001 false positive on "# pytest: foo=bar" |
| #27775 | question | bug | 0.97 | False positive on TRY203 |
| #26850 | question | feature | 0.96 | Include sqlmodel.SQLModel in runtime evaluated base classes |
| #28998 | question | bug | 0.96 | PLW0108 False positive when lambda executes a list element |
| #28519 | question | feature | 0.96 | [Formatter feature request] Config option for trailing comma |

**d1-ultra@openrouter** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #28675 | question | bug | 0.98 | ERA001 false positive on "# pytest: foo=bar" |
| #28998 | question | bug | 0.97 | PLW0108 False positive when lambda executes a list element |
| #28040 | feature | bug | 0.97 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |
| #28519 | question | feature | 0.97 | [Formatter feature request] Config option for trailing comma |
| #26449 | question | bug | 0.97 | ruff format strips mandatory parens from multi-exception except claus… |
| #27775 | question | bug | 0.97 | False positive on TRY203 |
| #27578 | feature | bug | 0.96 | False positive "f-string" message |

**d1.1@openrouter** (34)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 0.99 | False positive Undefined name for self-referential return annotation … |
| #26449 | question | bug | 0.99 | ruff format strips mandatory parens from multi-exception except claus… |
| #28998 | question | bug | 0.99 | PLW0108 False positive when lambda executes a list element |
| #26522 | feature | bug | 0.99 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28675 | question | bug | 0.98 | ERA001 false positive on "# pytest: foo=bar" |
| #27432 | question | bug | 0.98 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #28308 | question | bug | 0.98 | fatal error while checking app.py please open an issue |
| #24827 | question | bug | 0.98 | N805 auto-fix unsafely renames meaningful parameter to `self` |

**d1.2** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 0.98 | PLW0108 False positive when lambda executes a list element |
| #26522 | feature | bug | 0.97 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #26449 | question | bug | 0.97 | ruff format strips mandatory parens from multi-exception except claus… |
| #27369 | feature | bug | 0.97 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #27432 | question | bug | 0.97 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #28675 | question | bug | 0.96 | ERA001 false positive on "# pytest: foo=bar" |
| #28308 | question | bug | 0.96 | fatal error while checking app.py please open an issue |

**d1.2-ultra** (19)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 0.97 | False positive Undefined name for self-referential return annotation … |
| #26646 | question | bug | 0.96 | F722 False Positive (Syntax error in forward annotation) |
| #27775 | question | bug | 0.95 | False positive on TRY203 |
| #28998 | question | bug | 0.95 | PLW0108 False positive when lambda executes a list element |
| #25550 | question | bug | 0.95 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26449 | question | bug | 0.94 | ruff format strips mandatory parens from multi-exception except claus… |
| #27369 | feature | bug | 0.93 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #24563 | feature | bug | 0.93 | PLC2701 false positive for a private name import used in a type param… |

**d1@vercel** (46)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #27369 | feature | bug | 1.00 | TC001/TC002/TC003 false negative when using a type as generic paramet… |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #24827 | question | bug | 1.00 | N805 auto-fix unsafely renames meaningful parameter to `self` |
| #24751 | feature | bug | 1.00 | False positive BLE001 when using structlog's async logger (await logg… |
| #24887 | question | bug | 1.00 | F632: false positive |

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

**decision-1.1@openrouter** (55)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #27432 | question | bug | 1.00 | Ruff reports S604 on creating a shapely.geometry.Polygon |
| #26522 | feature | bug | 1.00 | RUF059 and F841 not detected when calling locals() before unpacking a… |
| #28519 | question | feature | 1.00 | [Formatter feature request] Config option for trailing comma |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |

**decision-1@openrouter** (56)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #27775 | question | bug | 1.00 | False positive on TRY203 |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #28040 | feature | bug | 1.00 | ASYNC240 false positive for `Path.glob()` iterator on offloaded thread |

**drex-max@openrouter** (47)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28998 | question | bug | 1.00 | PLW0108 False positive when lambda executes a list element |
| #27379 | question | bug | 1.00 | False positive Undefined name for self-referential return annotation … |
| #26449 | question | bug | 1.00 | ruff format strips mandatory parens from multi-exception except claus… |
| #26646 | question | bug | 1.00 | F722 False Positive (Syntax error in forward annotation) |
| #26951 | feature | bug | 1.00 | RUF052 false negatives for `class`, `def`, and `import` bindings |
| #28675 | question | bug | 1.00 | ERA001 false positive on "# pytest: foo=bar" |
| #24785 | feature | bug | 1.00 | `unused-async` (`RUF029`) - false negative on methods |
| #25550 | question | bug | 1.00 | ruff format (py314 target) incorrectly rewrites except (A, B): to exc… |

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

**jev:1.14** (62)

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

**reflex@openrouter** (63)

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


## Cases the models disagree on (12 of 69)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28097 | question | feature (0.81) | feature (0.89) | feature (0.93) | feature (0.92) | feature (0.96) | feature (0.91) | feature (0.93) | feature (0.99) | feature (0.97) | feature (0.97) | feature (1.00) | feature (1.00) | feature (0.99) | feature (0.99) | feature (0.99) | feature (1.00) | question (0.49) | feature (0.66) | feature (0.91) | feature (0.97) | feature (1.00) | feature (1.00) | Option to use `code:name` for rules and output |
| #27578 | feature | bug (0.91) | bug (0.89) | bug (0.94) | bug (0.96) | bug (0.86) | bug (0.87) | bug (0.84) | bug (0.98) | bug (0.91) | bug (0.95) | bug (0.97) | bug (0.99) | bug (0.96) | bug (0.98) | feature (0.47) | bug (1.00) | bug (0.72) | bug (0.48) | bug (0.96) | bug (0.93) | bug (1.00) | bug (0.99) | False positive "f-string" message |
| #26879 | feature | feature (0.83) | feature (0.89) | feature (0.85) | feature (0.70) | bug (0.60) | bug (0.59) | feature (0.81) | feature (0.71) | feature (0.85) | feature (0.85) | feature (0.99) | feature (0.93) | feature (0.91) | feature (0.97) | feature (0.86) | feature (0.80) | question (0.35) | feature (0.50) | feature (1.00) | feature (0.90) | feature (0.95) | feature (0.95) | Widen accepted `__all__` and `__slots__` formats to include single-ch… |
| #25296 | feature | feature (0.97) | feature (0.93) | feature (0.97) | feature (0.98) | feature (0.99) | feature (0.97) | feature (0.96) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (1.00) | feature (0.99) | feature (1.00) | bug (0.35) | feature (0.83) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | Rule idea: class-level None can make runtime protocol checks slow |
| #24549 | question | bug (0.55) | bug (0.48) | bug (0.75) | bug (0.89) | bug (0.74) | bug (0.82) | bug (0.86) | bug (0.87) | question (0.57) | bug (0.84) | bug (0.88) | bug (0.68) | bug (0.95) | bug (0.85) | bug (0.84) | bug (0.97) | bug (0.71) | question (0.59) | bug (1.00) | bug (0.93) | bug (1.00) | bug (0.95) | Serious slowdown of jupyter notebooks in vs code |
| #26456 | feature | feature (0.90) | feature (0.92) | feature (0.87) | feature (0.93) | feature (0.94) | feature (0.93) | feature (0.92) | feature (0.99) | feature (0.96) | feature (0.98) | feature (1.00) | feature (1.00) | feature (0.99) | feature (0.97) | feature (0.97) | feature (0.98) | question (0.49) | feature (0.50) | feature (0.98) | feature (0.95) | feature (1.00) | feature (1.00) | Detecting returning exception instead of raising |
| #24545 | feature | feature (0.90) | feature (0.90) | feature (0.74) | feature (0.97) | feature (0.89) | feature (0.89) | feature (0.94) | feature (0.97) | feature (0.86) | feature (0.98) | feature (0.99) | feature (0.98) | feature (0.99) | feature (0.70) | feature (0.99) | feature (0.86) | documentation (0.66) | feature (0.38) | feature (0.87) | feature (0.99) | feature (1.00) | feature (0.99) | Prefer `prefixmatch` over `match` |
| #26656 | feature | feature (0.94) | feature (0.90) | feature (0.91) | feature (0.98) | feature (0.99) | feature (0.96) | feature (0.97) | feature (0.96) | feature (0.99) | feature (1.00) | feature (1.00) | feature (1.00) | feature (1.00) | feature (0.90) | feature (0.99) | feature (0.97) | documentation (0.34) | feature (0.44) | feature (0.53) | feature (0.99) | feature (1.00) | feature (0.95) | Rule suggestion: `functools.partial` call with singular argument |
| #28567 | feature | feature (0.89) | feature (0.90) | feature (0.93) | feature (0.98) | feature (0.96) | feature (0.96) | feature (0.92) | feature (0.99) | feature (0.97) | feature (0.99) | feature (1.00) | feature (0.97) | feature (0.99) | feature (0.90) | feature (0.98) | feature (0.97) | question (0.42) | feature (0.42) | feature (0.90) | feature (0.97) | feature (0.84) | feature (1.00) | Support flake8-if-expr |
| #27777 | feature | feature (0.64) | feature (0.87) | feature (0.79) | feature (0.95) | feature (0.94) | feature (0.91) | feature (0.91) | feature (0.88) | feature (0.93) | feature (0.96) | feature (1.00) | feature (1.00) | feature (0.99) | feature (0.87) | feature (0.94) | feature (0.82) | bug (0.62) | bug (0.35) | feature (0.96) | feature (0.95) | feature (1.00) | feature (0.97) | Flag `classmethod` definition with no arguments |
| #24685 | question | question (0.83) | question (0.91) | question (0.67) | question (0.84) | question (0.77) | question (0.74) | question (0.67) | question (0.69) | question (0.79) | question (0.86) | question (1.00) | question (0.94) | question (0.84) | question (0.81) | question (0.85) | question (0.82) | question (0.58) | question (0.53) | bug (0.53) | question (0.65) | bug (0.53) | bug (0.58) | When using code-server 4.115.0, why are issues shown as warnings with… |
| #25386 | bug | bug (0.67) | bug (0.67) | bug (0.84) | bug (0.89) | bug (0.85) | bug (0.82) | bug (0.89) | bug (0.96) | bug (0.64) | bug (0.98) | bug (0.68) | bug (0.91) | bug (0.98) | bug (0.84) | bug (0.93) | bug (0.95) | bug (0.51) | question (0.42) | bug (0.98) | bug (0.98) | bug (1.00) | bug (0.90) | Schrödinger's comment: it is both commented-out code and a comment th… |
