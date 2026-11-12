# gh-gemini-needinfo

2026-11-12 · 210 labelled dev cases (False 165, True 45) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**clef-flash@openrouter** has the highest accuracy (all), 80% [75, 86] (API cost $0.15 per 10k, p99 760ms). Its interval overlaps with clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@google, jev:1.14, joey@openrouter, kev@openrouter, luna@decisions, mammoth@openrouter, reflex@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is joey@openrouter's, 80% [74, 85].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 76.7% [71, 83] | 0.36 | 0.60 | 0.11 | 4% [1, 6] | 75.0% (40.0%) | 0/210 | 0/210 |
| clef-omni@openrouter | 210 | 78.1% [73, 84] | 0.38 | 0.60 | 0.13 | 2% [0, 4] | 50.0% (9.8%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 78.6% [73, 84] | 0.38 | 0.60 | 0.15 | 8% [4, 11] | 75.0% (51.6%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 75.2% [70, 81] | 0.37 | 0.57 | 0.14 | 3% [1, 6] | 71.4% (34.1%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 71.4% [65, 78] | 0.35 | 0.62 | 0.17 | 8% [5, 12] | 82.4% (60.4%) | 0/210 | 0/210 |
| d1@vercel | 210 | 74.8% [69, 81] | 0.35 | 0.60 | 0.19 | 10% [7, 14] | 85.7% (67.1%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 78.6% [73, 84] | 0.35 | 0.62 | 0.14 | 4% [2, 7] | 66.7% (34.5%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 77.6% [72, 83] | 0.39 | 0.60 | 0.18 | 11% [7, 15] | 95.7% (81.0%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 71.0% [64, 78] | 0.34 | 0.58 | 0.24 | 0% [0, 1] | 0.0% (0.0%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 75.2% [70, 81] | 0.37 | 0.58 | 0.21 | 3% [1, 5] | 83.3% (41.8%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 72.4% [66, 79] | 0.34 | 0.58 | 0.17 | 4% [1, 7] | 100.0% (68.8%) | 0/210 | 0/210 |
| gemini-decision@google | 210 | 73.8% [68, 80] | 0.35 | 0.60 | 0.17 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 72.4% [66, 79] | 0.36 | 0.61 | 0.13 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 80.0% [74, 85] | 0.34 | 0.58 | 0.07 | 1% [0, 2] | 50.0% (2.5%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 78.1% [73, 84] | 0.30 | 0.58 | 0.05 | 1% [0, 2] | 50.0% (2.5%) | 0/210 | 0/210 |
| luna@decisions | 210 | 75.7% [70, 81] | 0.37 | 0.63 | 0.19 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 76.7% [71, 83] | 0.38 | 0.61 | 0.18 | 16% [11, 20] | 93.9% (82.1%) | 0/210 | 0/210 |
| reflex@openrouter | 210 | 78.1% [73, 84] | 0.39 | 0.63 | 0.19 | 6% [3, 9] | 91.7% (66.1%) | 0/210 | 0/210 |
| span@openrouter | 210 | 75.7% [70, 82] | 0.37 | 0.63 | 0.18 | 4% [2, 8] | 66.7% (34.5%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 80% [75, 86] | 0.85 | met |
| clef-omni@openrouter = | 80% [75, 86] | 0.80 | met |
| clef@openrouter = | 80% [75, 86] | 0.85 | met |
| d1-ultra@openrouter = | 80% [74, 86] | 0.95 | met |
| d1.1@openrouter = | 80% [75, 86] | 0.95 | met |
| d1@vercel = | 79% [74, 85] | 0.90 | met |
| decider-flash@openrouter = | 80% [74, 86] | 0.80 | met |
| decider@openrouter = | 80% [74, 85] | 0.90 | met |
| decision-1@openrouter = | 78% [72, 83] | 0.95 | met |
| drex-max@openrouter = | 78% [73, 84] | 0.90 | met |
| elephant@openrouter = | 80% [75, 86] | 0.95 | met |
| gemini-decision@google = | 78% [72, 83] | 0.95 | met |
| jev:1.14 = | 78% [73, 84] | 0.85 | met |
| joey@openrouter = | 80% [74, 85] | 0.50 | met |
| kev@openrouter = | 79% [73, 84] | 0.70 | met |
| luna@decisions = | 75% [70, 81] | 0.95 | met |
| mammoth@openrouter = | 78% [72, 84] | 0.75 | met |
| reflex@openrouter = | 79% [73, 84] | 0.90 | met |
| span@openrouter = | 79% [73, 84] | 0.95 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 266 ms | 377 ms | 760 ms | 895 ms | 2.9 | 0 | 4 | $0.15 | billed | ○ |
| clef-omni@openrouter | 210 | 210 ms | 309 ms | 493 ms | 982 ms | 2.4 | 0 | 4 | $0.89 | billed |  |
| clef@openrouter | 210 | 355 ms | 753 ms | 1252 ms | 3190 ms | 3.5 | 0 | 4 | $1.30 | billed |  |
| d1-ultra@openrouter | 210 | 229 ms | 314 ms | 767 ms | 1261 ms | 3.4 | 0 | 4 | $0.22 | billed |  |
| d1.1@openrouter | 210 | 470 ms | 844 ms | 972 ms | 1044 ms | 2.1 | 0 | 4 | $0.10 | billed |  |
| d1@vercel | 210 | 280 ms | 414 ms | 531 ms | 856 ms | 1.9 | 0 | 4 | $0.10 | billed |  |
| decider-flash@openrouter | 210 | 140 ms | 189 ms | 230 ms | 255 ms | 1.6 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 210 | 232 ms | 452 ms | 1137 ms | 1325 ms | 4.9 | 0 | 4 | $0.11 | billed |  |
| decision-1@openrouter | 210 | 245 ms | 325 ms | 399 ms | 424 ms | 1.6 | 0 | 4 | $0.21 | billed |  |
| drex-max@openrouter | 210 | 268 ms | 504 ms | 894 ms | 1497 ms | 3.3 | 7 | 4 | $0.33 | billed |  |
| elephant@openrouter | 210 | 165 ms | 192 ms | 244 ms | 290 ms | 1.5 | 0 | 4 | $0.20 | billed | ○ |
| gemini-decision@google | 210 | 187 ms | 328 ms | 534 ms | 594 ms | 2.9 | 0 | 4 | $0.62 | estimated |  |
| jev:1.14 | 210 | 107 ms | 216 ms | 252 ms | 293 ms | 2.4 | 0 | 4 | $0.32 | estimated |  |
| joey@openrouter | 210 | 166 ms | 190 ms | 245 ms | 1389 ms | 1.5 | 0 | 4 | $0.06 | billed |  |
| kev@openrouter | 210 | 414 ms | 542 ms | 841 ms | 1088 ms | 2.0 | 0 | 4 | $0.20 | billed |  |
| luna@decisions | 210 | 218 ms | 428 ms | 627 ms | 754 ms | 2.9 | 0 | 4 | $0.63 | estimated |  |
| mammoth@openrouter | 210 | 187 ms | 216 ms | 587 ms | 2040 ms | 3.1 | 0 | 4 | $0.56 | billed |  |
| reflex@openrouter | 210 | 263 ms | 407 ms | 1059 ms | 1488 ms | 4.0 | 0 | 4 | $0.24 | billed |  |
| span@openrouter | 210 | 206 ms | 781 ms | 937 ms | 973 ms | 4.6 | 0 | 4 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0031 | 15 s (estimated, 210 calls) | 12 min | 4 |
| clef-omni@openrouter | $0.02 | 12 s (estimated, 210 calls) | 10 min | 4 |
| clef@openrouter | $0.03 | 23 s (estimated, 210 calls) | 19 min | 4 |
| d1-ultra@openrouter | $0.0046 | 13 s (estimated, 210 calls) | 11 min | 4 |
| d1.1@openrouter | $0.0022 | 26 s (estimated, 210 calls) | 21 min | 4 |
| d1@vercel | $0.0022 | 16 s (estimated, 210 calls) | 13 min | 4 |
| decider-flash@openrouter | $0.0012 | 8 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0023 | 16 s (estimated, 210 calls) | 13 min | 4 |
| decision-1@openrouter | $0.0044 | 14 s (estimated, 210 calls) | 11 min | 4 |
| drex-max@openrouter | $0.0070 | 17 s (estimated, 210 calls) | 13 min | 4 |
| elephant@openrouter | $0.0041 | 9 s (estimated, 210 calls) | 7 min | 4 |
| gemini-decision@google | $0.01 | 11 s (estimated, 210 calls) | 9 min | 4 |
| jev:1.14 | $0.0068 | 7 s (estimated, 210 calls) | 6 min | 4 |
| joey@openrouter | $0.0012 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0042 | 23 s (estimated, 210 calls) | 18 min | 4 |
| luna@decisions | $0.01 | 14 s (estimated, 210 calls) | 11 min | 4 |
| mammoth@openrouter | $0.01 | 11 s (estimated, 210 calls) | 9 min | 4 |
| reflex@openrouter | $0.0049 | 16 s (estimated, 210 calls) | 13 min | 4 |
| span@openrouter | $0.0013 | 16 s (estimated, 210 calls) | 13 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 76.7% | 80.5% | 34 | 7 | 0.85 | 0.85 |
| clef-omni@openrouter | 78.1% | 80.0% | 33 | 9 | 0.80 | 0.80 |
| clef@openrouter | 78.6% | 80.0% | 35 | 7 | 0.85 | 0.85 |
| d1-ultra@openrouter | 75.2% | 80.0% | 35 | 7 | 0.95 | 0.95 |
| d1.1@openrouter | 71.4% | 80.0% | 32 | 10 | 0.95 | 0.95 |
| d1@vercel | 74.8% | 79.0% | 35 | 9 | 0.90 | 0.90 |
| decider-flash@openrouter | 78.6% | 80.0% | 34 | 8 | 0.80 | 0.80 |
| decider@openrouter | 77.6% | 79.5% | 32 | 11 | 0.90 | 0.90 |
| decision-1@openrouter | 71.0% | 77.6% | 32 | 15 | 0.95 | 0.95 |
| drex-max@openrouter | 75.2% | 78.1% | 31 | 15 | 0.90 | 0.90 |
| elephant@openrouter | 72.4% | 80.5% | 38 | 3 | 0.95 | 0.95 |
| gemini-decision@google | 73.8% | 77.6% | 33 | 14 | 0.85 | 0.95 |
| jev:1.14 | 72.4% | 78.1% | 31 | 15 | 0.85 | 0.85 |
| joey@openrouter | 80.0% | 80.0% | 34 | 8 | 0.50 | 0.50 |
| kev@openrouter | 78.1% | 78.6% | 41 | 4 | 0.70 | 0.70 |
| luna@decisions | 75.7% | 75.2% | 36 | 16 | 0.90 | 0.95 |
| mammoth@openrouter | 76.7% | 78.1% | 31 | 15 | 0.75 | 0.75 |
| reflex@openrouter | 78.1% | 78.6% | 31 | 14 | 0.90 | 0.90 |
| span@openrouter | 75.7% | 78.6% | 36 | 9 | 0.95 | 0.95 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 17 (38%) | 98 (59%) |
| 0.20 | 26 (58%) | 39 (24%) |
| 0.30 | 30 (67%) | 29 (18%) |
| 0.40 | 30 (67%) | 22 (13%) |
| 0.50 | 31 (69%) | 18 (11%) |
| 0.60 | 32 (71%) | 16 (10%) |
| 0.70 | 33 (73%) | 14 (8%) |
| 0.80 | 33 (73%) | 10 (6%) |
| 0.85 | 34 (76%) | 7 (4%) |
| 0.90 | 40 (89%) | 4 (2%) |

## Misses and false alarms by threshold (clef-omni@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 22 (49%) | 55 (33%) |
| 0.20 | 29 (64%) | 31 (19%) |
| 0.30 | 30 (67%) | 25 (15%) |
| 0.40 | 31 (69%) | 19 (12%) |
| 0.50 | 31 (69%) | 15 (9%) |
| 0.60 | 33 (73%) | 12 (7%) |
| 0.70 | 33 (73%) | 11 (7%) |
| 0.80 | 33 (73%) | 9 (5%) |
| 0.90 | 40 (89%) | 7 (4%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 30 (67%) | 37 (22%) |
| 0.20 | 30 (67%) | 24 (15%) |
| 0.30 | 30 (67%) | 19 (12%) |
| 0.40 | 30 (67%) | 15 (9%) |
| 0.50 | 31 (69%) | 14 (8%) |
| 0.60 | 32 (71%) | 12 (7%) |
| 0.70 | 33 (73%) | 10 (6%) |
| 0.80 | 34 (76%) | 7 (4%) |
| 0.85 | 35 (78%) | 5 (3%) |
| 0.90 | 37 (82%) | 5 (3%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 20 (44%) | 81 (49%) |
| 0.20 | 22 (49%) | 51 (31%) |
| 0.30 | 28 (62%) | 33 (20%) |
| 0.40 | 29 (64%) | 29 (18%) |
| 0.50 | 30 (67%) | 22 (13%) |
| 0.60 | 30 (67%) | 17 (10%) |
| 0.70 | 31 (69%) | 14 (8%) |
| 0.80 | 32 (71%) | 14 (8%) |
| 0.90 | 33 (73%) | 12 (7%) |
| 0.95 | 35 (78%) | 7 (4%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (42%) | 77 (47%) |
| 0.20 | 23 (51%) | 57 (35%) |
| 0.30 | 27 (60%) | 43 (26%) |
| 0.40 | 29 (64%) | 35 (21%) |
| 0.50 | 29 (64%) | 31 (19%) |
| 0.60 | 30 (67%) | 23 (14%) |
| 0.70 | 30 (67%) | 19 (12%) |
| 0.80 | 30 (67%) | 15 (9%) |
| 0.90 | 32 (71%) | 14 (8%) |
| 0.95 | 32 (71%) | 10 (6%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 24 (53%) | 56 (34%) |
| 0.20 | 28 (62%) | 39 (24%) |
| 0.30 | 29 (64%) | 30 (18%) |
| 0.40 | 29 (64%) | 24 (15%) |
| 0.50 | 31 (69%) | 22 (13%) |
| 0.60 | 32 (71%) | 17 (10%) |
| 0.70 | 32 (71%) | 16 (10%) |
| 0.80 | 33 (73%) | 15 (9%) |
| 0.90 | 34 (76%) | 9 (5%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (58%) | 46 (28%) |
| 0.20 | 30 (67%) | 25 (15%) |
| 0.30 | 31 (69%) | 19 (12%) |
| 0.40 | 32 (71%) | 15 (9%) |
| 0.50 | 33 (73%) | 12 (7%) |
| 0.60 | 33 (73%) | 12 (7%) |
| 0.70 | 33 (73%) | 11 (7%) |
| 0.80 | 34 (76%) | 6 (4%) |
| 0.90 | 38 (84%) | 5 (3%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (58%) | 48 (29%) |
| 0.20 | 28 (62%) | 31 (19%) |
| 0.30 | 30 (67%) | 23 (14%) |
| 0.40 | 30 (67%) | 18 (11%) |
| 0.50 | 30 (67%) | 17 (10%) |
| 0.60 | 31 (69%) | 15 (9%) |
| 0.70 | 31 (69%) | 15 (9%) |
| 0.80 | 31 (69%) | 15 (9%) |
| 0.90 | 32 (71%) | 11 (7%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (58%) | 61 (37%) |
| 0.20 | 28 (62%) | 51 (31%) |
| 0.30 | 29 (64%) | 43 (26%) |
| 0.40 | 29 (64%) | 40 (24%) |
| 0.50 | 29 (64%) | 32 (19%) |
| 0.60 | 29 (64%) | 28 (17%) |
| 0.70 | 30 (67%) | 27 (16%) |
| 0.80 | 31 (69%) | 22 (13%) |
| 0.90 | 32 (71%) | 19 (12%) |
| 0.95 | 32 (71%) | 15 (9%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (56%) | 52 (32%) |
| 0.20 | 29 (64%) | 37 (22%) |
| 0.30 | 30 (67%) | 29 (18%) |
| 0.40 | 30 (67%) | 23 (14%) |
| 0.50 | 30 (67%) | 22 (13%) |
| 0.60 | 30 (67%) | 17 (10%) |
| 0.70 | 31 (69%) | 16 (10%) |
| 0.80 | 31 (69%) | 16 (10%) |
| 0.90 | 31 (69%) | 14 (8%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (42%) | 87 (53%) |
| 0.20 | 26 (58%) | 64 (39%) |
| 0.30 | 27 (60%) | 47 (28%) |
| 0.40 | 29 (64%) | 36 (22%) |
| 0.50 | 30 (67%) | 28 (17%) |
| 0.60 | 30 (67%) | 23 (14%) |
| 0.70 | 30 (67%) | 15 (9%) |
| 0.80 | 34 (76%) | 13 (8%) |
| 0.90 | 36 (80%) | 11 (7%) |
| 0.95 | 38 (84%) | 3 (2%) |

## Misses and false alarms by threshold (gemini-decision@google)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 21 (47%) | 68 (41%) |
| 0.20 | 26 (58%) | 57 (35%) |
| 0.30 | 27 (60%) | 41 (25%) |
| 0.40 | 29 (64%) | 30 (18%) |
| 0.50 | 30 (67%) | 25 (15%) |
| 0.60 | 30 (67%) | 21 (13%) |
| 0.70 | 30 (67%) | 20 (12%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 33 (73%) | 12 (7%) |
| 0.95 | 34 (76%) | 10 (6%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 6 (13%) | 120 (73%) |
| 0.20 | 22 (49%) | 69 (42%) |
| 0.30 | 27 (60%) | 48 (29%) |
| 0.40 | 28 (62%) | 36 (22%) |
| 0.50 | 29 (64%) | 29 (18%) |
| 0.60 | 30 (67%) | 24 (15%) |
| 0.70 | 30 (67%) | 20 (12%) |
| 0.80 | 31 (69%) | 16 (10%) |
| 0.85 | 31 (69%) | 14 (8%) |
| 0.90 | 31 (69%) | 14 (8%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (4%) | 156 (95%) |
| 0.20 | 20 (44%) | 74 (45%) |
| 0.30 | 27 (60%) | 44 (27%) |
| 0.40 | 31 (69%) | 23 (14%) |
| 0.50 | 34 (76%) | 8 (5%) |
| 0.60 | 42 (93%) | 4 (2%) |
| 0.70 | 44 (98%) | 1 (1%) |
| 0.80 | 45 (100%) | 0 (0%) |
| 0.90 | 45 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 6 (13%) | 146 (88%) |
| 0.20 | 24 (53%) | 59 (36%) |
| 0.30 | 29 (64%) | 29 (18%) |
| 0.40 | 31 (69%) | 17 (10%) |
| 0.50 | 35 (78%) | 11 (7%) |
| 0.60 | 38 (84%) | 8 (5%) |
| 0.70 | 39 (87%) | 4 (2%) |
| 0.80 | 42 (93%) | 1 (1%) |
| 0.90 | 44 (98%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 22 (49%) | 66 (40%) |
| 0.20 | 30 (67%) | 37 (22%) |
| 0.30 | 30 (67%) | 26 (16%) |
| 0.40 | 30 (67%) | 23 (14%) |
| 0.50 | 30 (67%) | 21 (13%) |
| 0.60 | 30 (67%) | 21 (13%) |
| 0.70 | 30 (67%) | 17 (10%) |
| 0.80 | 32 (71%) | 15 (9%) |
| 0.90 | 33 (73%) | 13 (8%) |
| 0.95 | 36 (80%) | 9 (5%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 20 (44%) | 63 (38%) |
| 0.20 | 27 (60%) | 45 (27%) |
| 0.30 | 28 (62%) | 29 (18%) |
| 0.40 | 29 (64%) | 22 (13%) |
| 0.50 | 30 (67%) | 19 (12%) |
| 0.60 | 30 (67%) | 15 (9%) |
| 0.70 | 31 (69%) | 14 (8%) |
| 0.75 | 31 (69%) | 13 (8%) |
| 0.80 | 31 (69%) | 13 (8%) |
| 0.90 | 32 (71%) | 13 (8%) |

## Misses and false alarms by threshold (reflex@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 28 (62%) | 36 (22%) |
| 0.20 | 28 (62%) | 23 (14%) |
| 0.30 | 30 (67%) | 21 (13%) |
| 0.40 | 30 (67%) | 19 (12%) |
| 0.50 | 30 (67%) | 16 (10%) |
| 0.60 | 30 (67%) | 16 (10%) |
| 0.70 | 30 (67%) | 14 (8%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 31 (69%) | 12 (7%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 27 (60%) | 38 (23%) |
| 0.20 | 29 (64%) | 28 (17%) |
| 0.30 | 29 (64%) | 26 (16%) |
| 0.40 | 29 (64%) | 23 (14%) |
| 0.50 | 30 (67%) | 21 (13%) |
| 0.60 | 30 (67%) | 20 (12%) |
| 0.70 | 30 (67%) | 13 (8%) |
| 0.80 | 33 (73%) | 11 (7%) |
| 0.90 | 34 (76%) | 9 (5%) |
| 0.95 | 37 (82%) | 5 (3%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (21)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 0.95 | Docs: six CLI flags missing from the reference table |
| #29424 | True | False | 0.93 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29290 | True | False | 0.93 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #28761 | True | False | 0.93 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29311 | True | False | 0.93 | bug(core): insecure user/workspace policy dirs skip permission checks… |
| #29316 | True | False | 0.93 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29204 | True | False | 0.92 | MCP prompt responses are submitted as JSON-encoded text |
| #29144 | True | False | 0.92 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |

**clef-omni@openrouter** (29)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 0.97 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29424 | True | False | 0.97 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29146 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #28761 | True | False | 0.97 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #28846 | True | False | 0.96 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29204 | True | False | 0.96 | MCP prompt responses are submitted as JSON-encoded text |
| #29317 | True | False | 0.96 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |

**clef@openrouter** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28846 | True | False | 0.98 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 0.98 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #28761 | True | False | 0.97 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29316 | True | False | 0.97 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29308 | True | False | 0.97 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29317 | True | False | 0.97 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29424 | True | False | 0.97 | bug: Node process hangs on session exit, preventing terminal from ret… |

**d1-ultra@openrouter** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29317 | True | False | 0.99 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28783 | False | True | 0.99 | cutealexamartha |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29309 | True | False | 0.99 | bug(core): unbounded _execute recursion on sandbox_expansion_required… |
| #29046 | True | False | 0.99 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |

**d1.1@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28783 | False | True | 0.99 | cutealexamartha |
| #29100 | False | True | 0.99 | Gemini lolo |
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29012 | True | False | 0.99 | Docs: six CLI flags missing from the reference table |
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29290 | True | False | 0.99 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |

**d1@vercel** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #28761 | True | False | 1.00 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29068 | True | False | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29424 | True | False | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29100 | False | True | 1.00 | Gemini lolo |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |

**decider-flash@openrouter** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.99 | Gemini lolo |
| #28783 | False | True | 0.98 | cutealexamartha |
| #28846 | True | False | 0.97 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29424 | True | False | 0.97 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29144 | True | False | 0.97 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29012 | True | False | 0.97 | Docs: six CLI flags missing from the reference table |

**decider@openrouter** (37)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29046 | True | False | 0.99 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29424 | True | False | 0.99 | bug: Node process hangs on session exit, preventing terminal from ret… |

**decision-1@openrouter** (45)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 1.00 | Gemini lolo |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28783 | False | True | 1.00 | cutealexamartha |
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29220 | False | True | 1.00 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #29221 | False | True | 1.00 | Leeres.blaat_A4-DIN |
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |

**drex-max@openrouter** (39)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29392 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29100 | False | True | 1.00 | Gemini lolo |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29388 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29390 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |

**elephant@openrouter** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29290 | True | False | 0.99 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29316 | True | False | 0.97 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29100 | False | True | 0.97 | Gemini lolo |
| #29012 | True | False | 0.97 | Docs: six CLI flags missing from the reference table |

**gemini-decision@google** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29100 | False | True | 0.99 | Gemini lolo |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29305 | True | False | 0.98 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29317 | True | False | 0.98 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29046 | True | False | 0.98 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29012 | True | False | 0.98 | Docs: six CLI flags missing from the reference table |

**jev:1.14** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29355 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29147 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29228 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.97 | Gemini lolo |
| #29220 | False | True | 0.97 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #28783 | False | True | 0.97 | cutealexamartha |
| #29146 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29392 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |

**joey@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29415 | True | False | 0.92 | gemini --help exits with code 5 after winget install on Windows 11 |
| #29305 | True | False | 0.91 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |

**kev@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | True | False | 0.93 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29012 | True | False | 0.93 | Docs: six CLI flags missing from the reference table |
| #29001 | True | False | 0.92 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29144 | True | False | 0.91 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29317 | True | False | 0.91 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29308 | True | False | 0.91 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |

**luna@decisions** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29305 | True | False | 1.00 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29221 | False | True | 1.00 | Leeres.blaat_A4-DIN |
| #29220 | False | True | 0.99 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |

**mammoth@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29207 | True | False | 0.99 | Corrupt agents.json (valid JSON, wrong shape) crashes acknowledgment |
| #29392 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29305 | True | False | 0.99 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29046 | True | False | 0.99 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |

**reflex@openrouter** (40)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29388 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |

**span@openrouter** (36)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29424 | True | False | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29305 | True | False | 1.00 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |


## Cases the models disagree on (12 of 50)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #29442 | False | False (0.88) | False (0.87) | False (0.97) | False (0.93) | True (0.55) | False (0.93) | False (0.95) | False (0.94) | True (0.80) | False (0.87) | True (0.56) | False (0.91) | False (0.80) | False (0.74) | False (0.82) | False (1.00) | False (0.90) | False (0.98) | False (0.95) | Create a kitten illustration with a lion-shaped shadow |
| #29221 | False | True (0.87) | True (0.79) | True (0.78) | True (0.89) | True (0.97) | True (0.72) | True (0.79) | True (0.96) | True (1.00) | True (0.98) | True (0.79) | True (0.97) | True (0.92) | False (0.56) | False (0.54) | True (1.00) | True (0.96) | True (0.98) | True (0.88) | Leeres.blaat_A4-DIN |
| #28686 | False | False (0.90) | False (0.83) | False (0.94) | False (0.90) | True (0.58) | False (0.90) | False (0.96) | False (0.94) | False (0.59) | False (0.96) | False (0.58) | False (0.67) | False (0.80) | False (0.76) | False (0.85) | False (1.00) | False (0.88) | False (0.99) | False (0.83) | ## Code Review |
| #29145 | True | True (0.90) | True (0.94) | True (0.95) | True (0.98) | True (1.00) | True (0.97) | True (0.94) | True (1.00) | True (1.00) | True (1.00) | True (0.97) | True (0.98) | True (0.97) | True (0.71) | False (0.52) | True (0.99) | True (0.95) | True (1.00) | True (0.99) | Recalibrate trick |
| #29136 | True | True (0.88) | True (0.83) | True (0.90) | True (0.99) | True (0.98) | True (0.98) | True (0.92) | True (0.96) | True (1.00) | True (0.97) | True (0.93) | True (0.98) | True (0.98) | False (0.59) | True (0.52) | True (0.98) | True (0.95) | True (1.00) | True (0.99) | GeminiCLI.com Feedback: [ISSUE] |
| #28777 | True | True (0.80) | True (0.87) | True (0.88) | True (0.98) | True (0.97) | True (0.53) | False (0.66) | True (0.97) | True (1.00) | True (0.98) | True (0.89) | True (0.97) | True (0.94) | True (0.59) | False (0.56) | True (0.89) | True (0.91) | True (0.99) | True (0.92) | ticket IT support |
| #28783 | False | True (0.92) | True (0.95) | True (0.78) | True (0.99) | True (0.99) | True (1.00) | True (0.98) | True (0.98) | True (1.00) | True (0.99) | True (0.93) | True (0.98) | True (0.97) | False (0.56) | True (0.51) | True (0.97) | True (0.97) | True (0.99) | True (0.90) | cutealexamartha |
| #29135 | True | True (0.88) | True (0.60) | True (0.56) | True (0.83) | True (0.97) | False (0.53) | True (0.94) | True (0.96) | True (1.00) | True (0.93) | True (0.78) | True (0.90) | True (0.90) | True (0.58) | False (0.51) | True (0.73) | True (0.95) | True (0.93) | False (0.59) | Features |
| #28923 | True | True (0.91) | True (0.86) | True (0.91) | True (0.91) | True (0.95) | True (0.96) | True (0.71) | True (0.99) | True (1.00) | True (0.99) | True (0.91) | True (0.92) | True (0.97) | False (0.63) | True (0.71) | True (0.96) | True (0.96) | True (1.00) | True (0.95) | GeminiCLI.com Feedback: [ISSUE] |
| #28717 | False | False (0.93) | False (0.97) | False (0.97) | False (0.90) | False (0.84) | False (0.98) | False (0.89) | False (0.92) | True (0.88) | False (0.91) | False (0.81) | False (0.69) | False (0.85) | False (0.83) | False (0.89) | False (0.91) | False (0.96) | False (1.00) | False (1.00) | [Bug]: Google AI Pro sign-in silently falls back to API key onboardin… |
| #29390 | False | True (0.79) | True (0.59) | True (0.60) | True (0.97) | True (0.97) | True (0.97) | True (0.73) | True (0.98) | True (1.00) | True (1.00) | True (0.93) | True (0.91) | True (0.95) | False (0.59) | False (0.66) | True (0.88) | True (0.96) | True (1.00) | True (0.70) | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29388 | False | True (0.77) | True (0.59) | True (0.66) | True (0.98) | True (0.96) | True (0.96) | True (0.73) | True (0.98) | True (1.00) | True (1.00) | True (0.93) | True (0.91) | True (0.95) | False (0.59) | False (0.66) | True (0.88) | True (0.96) | True (1.00) | True (0.69) | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
