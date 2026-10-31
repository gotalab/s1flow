# gh-gemini-needinfo

2026-10-31 · 210 labelled dev cases (False 165, True 45) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**clef@openrouter** has the highest accuracy (all), 81% [76, 86] (API cost $1.32 per 10k, p99 965ms). Its interval overlaps with clef-flash@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, jev:1.14, joey@openrouter, kev@openrouter, luna@decisions, mammoth@openrouter, mercury@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is kev@openrouter's, 79% [73, 85].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 76.7% [71, 82] | 0.38 | 0.60 | 0.12 | 5% [2, 9] | 72.7% (43.6%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 78.1% [73, 84] | 0.38 | 0.59 | 0.14 | 3% [1, 6] | 42.9% (12.9%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 73.3% [67, 79] | 0.36 | 0.59 | 0.15 | 2% [0, 5] | 100.0% (54.9%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 71.4% [65, 77] | 0.35 | 0.60 | 0.17 | 4% [1, 7] | 87.5% (52.9%) | 0/210 | 0/210 |
| d1@vercel | 210 | 74.3% [69, 80] | 0.36 | 0.60 | 0.19 | 4% [2, 7] | 88.9% (57.1%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 78.1% [72, 84] | 0.36 | 0.61 | 0.15 | 2% [0, 4] | 50.0% (9.8%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 78.1% [73, 83] | 0.39 | 0.61 | 0.18 | 11% [7, 15] | 95.8% (81.7%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 71.4% [65, 77] | 0.36 | 0.59 | 0.24 | 1% [0, 2] | 100.0% (22.4%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 76.7% [71, 82] | 0.38 | 0.56 | 0.19 | 4% [1, 7] | 87.5% (52.9%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 71.0% [65, 77] | 0.33 | 0.59 | 0.15 | 4% [1, 6] | 87.5% (52.9%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 72.4% [66, 79] | 0.34 | 0.60 | 0.13 | 2% [0, 4] | 25.0% (1.3%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 78.1% [72, 83] | 0.34 | 0.58 | 0.07 | 1% [0, 3] | 66.7% (13.5%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 79.0% [73, 85] | 0.35 | 0.62 | 0.04 | 0% [0, 1] | 0.0% (0.0%) | 0/210 | 0/210 |
| luna@decisions | 210 | 75.7% [70, 81] | 0.37 | 0.62 | 0.19 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 76.7% [71, 82] | 0.38 | 0.59 | 0.17 | 7% [4, 10] | 85.7% (61.5%) | 0/210 | 0/210 |
| mercury@openrouter | 210 | 74.8% [69, 81] | 0.29 | 0.55 | 0.23 | 3% [1, 5] | 66.7% (27.1%) | 0/210 | 0/210 |
| span@openrouter | 210 | 75.2% [70, 81] | 0.35 | 0.65 | 0.19 | 13% [9, 18] | 85.7% (70.2%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 80% [75, 86] | 0.85 | met |
| clef@openrouter = | 81% [76, 86] | 0.85 | met |
| d1-ultra@openrouter = | 80% [75, 86] | 0.95 | met |
| d1.1@openrouter = | 78% [71, 83] | 0.95 | met |
| d1@vercel = | 80% [74, 85] | 0.95 | met |
| decider-flash@openrouter = | 77% [71, 82] | 0.80 | met |
| decider@openrouter = | 79% [74, 84] | 0.90 | met |
| decision-1@openrouter = | 77% [72, 83] | 0.95 | met |
| drex-max@openrouter = | 77% [71, 83] | 0.90 | met |
| elephant@openrouter = | 79% [72, 84] | 0.95 | met |
| jev:1.14 = | 78% [72, 83] | 0.90 | met |
| joey@openrouter = | 77% [71, 82] | 0.80 | met |
| kev@openrouter = | 80% [74, 85] | 0.70 | met |
| luna@decisions = | 76% [70, 82] | 0.90 | met |
| mammoth@openrouter = | 79% [73, 84] | 0.70 | met |
| mercury@openrouter = | 78% [72, 83] | 0.95 | met |
| span@openrouter = | 80% [75, 86] | 0.95 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 427 ms | 643 ms | 1212 ms | 1573 ms | 2.8 | 0 | 4 | $0.13 | billed |  |
| clef@openrouter | 210 | 358 ms | 594 ms | 965 ms | 1014 ms | 2.7 | 0 | 4 | $1.32 | billed | ○ |
| d1-ultra@openrouter | 210 | 219 ms | 342 ms | 601 ms | 705 ms | 2.7 | 0 | 4 | $0.22 | billed | ○ |
| d1.1@openrouter | 210 | 188 ms | 258 ms | 455 ms | 608 ms | 2.4 | 0 | 4 | $0.10 | billed | ○ |
| d1@vercel | 210 | 258 ms | 351 ms | 666 ms | 5005 ms | 2.6 | 0 | 4 | $0.10 | billed | ○ |
| decider-flash@openrouter | 210 | 146 ms | 167 ms | 248 ms | 359 ms | 1.7 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 210 | 229 ms | 267 ms | 479 ms | 965 ms | 2.1 | 0 | 4 | $0.11 | billed | ○ |
| decision-1@openrouter | 210 | 288 ms | 390 ms | 522 ms | 747 ms | 1.8 | 0 | 4 | $0.21 | billed |  |
| drex-max@openrouter | 210 | 363 ms | 506 ms | 773 ms | 1719 ms | 2.1 | 0 | 4 | $0.33 | billed |  |
| elephant@openrouter | 210 | 196 ms | 218 ms | 337 ms | 1209 ms | 1.7 | 0 | 4 | $0.20 | billed | ○ |
| jev:1.14 | 210 | 139 ms | 172 ms | 251 ms | 351 ms | 1.8 | 0 | 4 | $0.32 | estimated | ○ |
| joey@openrouter | 210 | 181 ms | 200 ms | 304 ms | 538 ms | 1.7 | 0 | 4 | $0.06 | billed |  |
| kev@openrouter | 210 | 468 ms | 739 ms | 953 ms | 975 ms | 2.0 | 0 | 4 | $0.20 | billed |  |
| luna@decisions | 210 | 216 ms | 414 ms | 977 ms | 1870 ms | 4.5 | 0 | 4 | $0.63 | estimated |  |
| mammoth@openrouter | 210 | 261 ms | 388 ms | 779 ms | 975 ms | 3.0 | 0 | 4 | $0.56 | billed |  |
| mercury@openrouter | 210 | 305 ms | 388 ms | 472 ms | 791 ms | 1.5 | 0 | 4 | $0.10 | billed |  |
| span@openrouter | 210 | 199 ms | 828 ms | 938 ms | 988 ms | 4.7 | 0 | 4 | $0.06 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0027 | 24 s (estimated, 210 calls) | 19 min | 4 |
| clef@openrouter | $0.03 | 21 s (estimated, 210 calls) | 16 min | 4 |
| d1-ultra@openrouter | $0.0046 | 13 s (estimated, 210 calls) | 11 min | 4 |
| d1.1@openrouter | $0.0022 | 11 s (estimated, 210 calls) | 9 min | 4 |
| d1@vercel | $0.0022 | 15 s (estimated, 210 calls) | 12 min | 4 |
| decider-flash@openrouter | $0.0012 | 8 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0023 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0044 | 16 s (estimated, 210 calls) | 13 min | 4 |
| drex-max@openrouter | $0.0070 | 20 s (estimated, 210 calls) | 16 min | 4 |
| elephant@openrouter | $0.0041 | 11 s (estimated, 210 calls) | 9 min | 4 |
| jev:1.14 | $0.0068 | 8 s (estimated, 210 calls) | 6 min | 4 |
| joey@openrouter | $0.0012 | 10 s (estimated, 210 calls) | 8 min | 4 |
| kev@openrouter | $0.0042 | 22 s (estimated, 210 calls) | 18 min | 4 |
| luna@decisions | $0.01 | 14 s (estimated, 210 calls) | 11 min | 4 |
| mammoth@openrouter | $0.01 | 15 s (estimated, 210 calls) | 12 min | 4 |
| mercury@openrouter | $0.0022 | 17 s (estimated, 210 calls) | 13 min | 4 |
| span@openrouter | $0.0013 | 17 s (estimated, 210 calls) | 13 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 76.7% | 80.5% | 34 | 7 | 0.85 | 0.85 |
| clef@openrouter | 78.1% | 81.0% | 35 | 5 | 0.85 | 0.85 |
| d1-ultra@openrouter | 73.3% | 80.5% | 34 | 7 | 0.95 | 0.95 |
| d1.1@openrouter | 71.4% | 77.6% | 32 | 15 | 0.95 | 0.95 |
| d1@vercel | 74.3% | 79.5% | 35 | 8 | 0.95 | 0.95 |
| decider-flash@openrouter | 78.1% | 76.7% | 36 | 13 | 0.80 | 0.80 |
| decider@openrouter | 78.1% | 79.0% | 33 | 11 | 0.90 | 0.90 |
| decision-1@openrouter | 71.4% | 77.1% | 32 | 16 | 0.95 | 0.95 |
| drex-max@openrouter | 76.7% | 77.1% | 32 | 16 | 0.90 | 0.90 |
| elephant@openrouter | 71.0% | 78.6% | 38 | 7 | 0.95 | 0.95 |
| jev:1.14 | 72.4% | 77.6% | 32 | 15 | 0.90 | 0.90 |
| joey@openrouter | 78.1% | 76.7% | 40 | 9 | 0.80 | 0.80 |
| kev@openrouter | 79.0% | 79.5% | 36 | 7 | 0.70 | 0.70 |
| luna@decisions | 75.7% | 76.2% | 35 | 15 | 0.90 | 0.90 |
| mammoth@openrouter | 76.7% | 78.6% | 31 | 14 | 0.70 | 0.70 |
| mercury@openrouter | 74.8% | 77.6% | 35 | 12 | 0.95 | 0.95 |
| span@openrouter | 75.2% | 80.5% | 35 | 6 | 0.95 | 0.95 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 18 (40%) | 94 (57%) |
| 0.20 | 27 (60%) | 38 (23%) |
| 0.30 | 30 (67%) | 29 (18%) |
| 0.40 | 30 (67%) | 22 (13%) |
| 0.50 | 30 (67%) | 19 (12%) |
| 0.60 | 31 (69%) | 14 (8%) |
| 0.70 | 32 (71%) | 14 (8%) |
| 0.80 | 34 (76%) | 10 (6%) |
| 0.85 | 34 (76%) | 7 (4%) |
| 0.90 | 40 (89%) | 3 (2%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 29 (64%) | 37 (22%) |
| 0.20 | 30 (67%) | 24 (15%) |
| 0.30 | 30 (67%) | 19 (12%) |
| 0.40 | 30 (67%) | 17 (10%) |
| 0.50 | 31 (69%) | 15 (9%) |
| 0.60 | 33 (73%) | 13 (8%) |
| 0.70 | 33 (73%) | 10 (6%) |
| 0.80 | 34 (76%) | 8 (5%) |
| 0.85 | 35 (78%) | 5 (3%) |
| 0.90 | 36 (80%) | 5 (3%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 20 (44%) | 75 (45%) |
| 0.20 | 23 (51%) | 51 (31%) |
| 0.30 | 28 (62%) | 37 (22%) |
| 0.40 | 29 (64%) | 32 (19%) |
| 0.50 | 29 (64%) | 27 (16%) |
| 0.60 | 30 (67%) | 17 (10%) |
| 0.70 | 31 (69%) | 15 (9%) |
| 0.80 | 32 (71%) | 13 (8%) |
| 0.90 | 33 (73%) | 12 (7%) |
| 0.95 | 34 (76%) | 7 (4%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (42%) | 79 (48%) |
| 0.20 | 24 (53%) | 62 (38%) |
| 0.30 | 28 (62%) | 44 (27%) |
| 0.40 | 29 (64%) | 37 (22%) |
| 0.50 | 29 (64%) | 31 (19%) |
| 0.60 | 29 (64%) | 22 (13%) |
| 0.70 | 29 (64%) | 20 (12%) |
| 0.80 | 31 (69%) | 15 (9%) |
| 0.90 | 32 (71%) | 13 (8%) |
| 0.95 | 32 (71%) | 12 (7%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 23 (51%) | 58 (35%) |
| 0.20 | 26 (58%) | 42 (25%) |
| 0.30 | 29 (64%) | 30 (18%) |
| 0.40 | 30 (67%) | 26 (16%) |
| 0.50 | 30 (67%) | 24 (15%) |
| 0.60 | 31 (69%) | 21 (13%) |
| 0.70 | 32 (71%) | 17 (10%) |
| 0.80 | 33 (73%) | 16 (10%) |
| 0.90 | 34 (76%) | 13 (8%) |
| 0.95 | 35 (78%) | 8 (5%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (56%) | 51 (31%) |
| 0.20 | 28 (62%) | 23 (14%) |
| 0.30 | 31 (69%) | 18 (11%) |
| 0.40 | 31 (69%) | 15 (9%) |
| 0.50 | 32 (71%) | 14 (8%) |
| 0.60 | 32 (71%) | 13 (8%) |
| 0.70 | 33 (73%) | 12 (7%) |
| 0.80 | 35 (78%) | 8 (5%) |
| 0.90 | 38 (84%) | 7 (4%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (58%) | 44 (27%) |
| 0.20 | 28 (62%) | 30 (18%) |
| 0.30 | 29 (64%) | 22 (13%) |
| 0.40 | 29 (64%) | 18 (11%) |
| 0.50 | 30 (67%) | 16 (10%) |
| 0.60 | 31 (69%) | 15 (9%) |
| 0.70 | 31 (69%) | 15 (9%) |
| 0.80 | 31 (69%) | 15 (9%) |
| 0.90 | 32 (71%) | 11 (7%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 27 (60%) | 58 (35%) |
| 0.20 | 28 (62%) | 49 (30%) |
| 0.30 | 28 (62%) | 41 (25%) |
| 0.40 | 28 (62%) | 37 (22%) |
| 0.50 | 28 (62%) | 32 (19%) |
| 0.60 | 29 (64%) | 28 (17%) |
| 0.70 | 30 (67%) | 28 (17%) |
| 0.80 | 30 (67%) | 22 (13%) |
| 0.90 | 32 (71%) | 16 (10%) |
| 0.95 | 32 (71%) | 15 (9%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (56%) | 51 (31%) |
| 0.20 | 28 (62%) | 35 (21%) |
| 0.30 | 30 (67%) | 28 (17%) |
| 0.40 | 30 (67%) | 23 (14%) |
| 0.50 | 30 (67%) | 19 (12%) |
| 0.60 | 30 (67%) | 16 (10%) |
| 0.70 | 31 (69%) | 16 (10%) |
| 0.80 | 31 (69%) | 16 (10%) |
| 0.90 | 31 (69%) | 14 (8%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 18 (40%) | 94 (57%) |
| 0.20 | 24 (53%) | 64 (39%) |
| 0.30 | 26 (58%) | 48 (29%) |
| 0.40 | 29 (64%) | 37 (22%) |
| 0.50 | 30 (67%) | 31 (19%) |
| 0.60 | 30 (67%) | 24 (15%) |
| 0.70 | 31 (69%) | 18 (11%) |
| 0.80 | 33 (73%) | 15 (9%) |
| 0.90 | 34 (76%) | 11 (7%) |
| 0.95 | 38 (84%) | 4 (2%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 6 (13%) | 130 (79%) |
| 0.20 | 22 (49%) | 67 (41%) |
| 0.30 | 24 (53%) | 49 (30%) |
| 0.40 | 28 (62%) | 38 (23%) |
| 0.50 | 30 (67%) | 28 (17%) |
| 0.60 | 30 (67%) | 24 (15%) |
| 0.70 | 30 (67%) | 20 (12%) |
| 0.80 | 31 (69%) | 16 (10%) |
| 0.90 | 31 (69%) | 14 (8%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (4%) | 155 (94%) |
| 0.20 | 22 (49%) | 77 (47%) |
| 0.30 | 27 (60%) | 46 (28%) |
| 0.40 | 31 (69%) | 25 (15%) |
| 0.50 | 33 (73%) | 13 (8%) |
| 0.60 | 39 (87%) | 7 (4%) |
| 0.70 | 42 (93%) | 4 (2%) |
| 0.80 | 44 (98%) | 0 (0%) |
| 0.90 | 45 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 4 (9%) | 153 (93%) |
| 0.20 | 20 (44%) | 64 (39%) |
| 0.30 | 29 (64%) | 31 (19%) |
| 0.40 | 31 (69%) | 19 (12%) |
| 0.50 | 33 (73%) | 11 (7%) |
| 0.60 | 37 (82%) | 8 (5%) |
| 0.70 | 37 (82%) | 4 (2%) |
| 0.80 | 41 (91%) | 2 (1%) |
| 0.90 | 43 (96%) | 1 (1%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 21 (47%) | 69 (42%) |
| 0.20 | 28 (62%) | 41 (25%) |
| 0.30 | 29 (64%) | 29 (18%) |
| 0.40 | 30 (67%) | 25 (15%) |
| 0.50 | 30 (67%) | 21 (13%) |
| 0.60 | 30 (67%) | 19 (12%) |
| 0.70 | 31 (69%) | 17 (10%) |
| 0.80 | 31 (69%) | 17 (10%) |
| 0.90 | 33 (73%) | 13 (8%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 21 (47%) | 65 (39%) |
| 0.20 | 27 (60%) | 42 (25%) |
| 0.30 | 28 (62%) | 29 (18%) |
| 0.40 | 29 (64%) | 24 (15%) |
| 0.50 | 30 (67%) | 19 (12%) |
| 0.60 | 30 (67%) | 16 (10%) |
| 0.70 | 31 (69%) | 13 (8%) |
| 0.80 | 32 (71%) | 13 (8%) |
| 0.90 | 33 (73%) | 13 (8%) |

## Misses and false alarms by threshold (mercury@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 29 (64%) | 25 (15%) |
| 0.20 | 31 (69%) | 24 (15%) |
| 0.30 | 32 (71%) | 20 (12%) |
| 0.40 | 34 (76%) | 19 (12%) |
| 0.50 | 34 (76%) | 19 (12%) |
| 0.60 | 34 (76%) | 19 (12%) |
| 0.70 | 34 (76%) | 18 (11%) |
| 0.80 | 34 (76%) | 18 (11%) |
| 0.90 | 34 (76%) | 17 (10%) |
| 0.95 | 35 (78%) | 12 (7%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (58%) | 40 (24%) |
| 0.20 | 29 (64%) | 26 (16%) |
| 0.30 | 30 (67%) | 23 (14%) |
| 0.40 | 31 (69%) | 22 (13%) |
| 0.50 | 31 (69%) | 21 (13%) |
| 0.60 | 31 (69%) | 20 (12%) |
| 0.70 | 31 (69%) | 14 (8%) |
| 0.80 | 31 (69%) | 13 (8%) |
| 0.90 | 34 (76%) | 11 (7%) |
| 0.95 | 35 (78%) | 6 (4%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (21)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29424 | True | False | 0.94 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #28761 | True | False | 0.93 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29012 | True | False | 0.93 | Docs: six CLI flags missing from the reference table |
| #29144 | True | False | 0.93 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 0.93 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29204 | True | False | 0.92 | MCP prompt responses are submitted as JSON-encoded text |
| #29316 | True | False | 0.92 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29220 | False | True | 0.92 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |

**clef@openrouter** (34)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #28846 | True | False | 0.98 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #28761 | True | False | 0.98 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29316 | True | False | 0.97 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29068 | True | False | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29424 | True | False | 0.97 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29308 | True | False | 0.97 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |

**d1-ultra@openrouter** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29317 | True | False | 0.99 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.99 | Gemini lolo |
| #29392 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29388 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |

**d1.1@openrouter** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29012 | True | False | 0.99 | Docs: six CLI flags missing from the reference table |
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29392 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #28783 | False | True | 0.99 | cutealexamartha |
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.99 | Gemini lolo |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |

**d1@vercel** (36)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29424 | True | False | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29305 | True | False | 1.00 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29392 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29388 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29311 | True | False | 1.00 | bug(core): insecure user/workspace policy dirs skip permission checks… |
| #29068 | True | False | 1.00 | GeminiCLI.com Feedback: [ISSUE] |

**decider-flash@openrouter** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29100 | False | True | 0.99 | Gemini lolo |
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28783 | False | True | 0.99 | cutealexamartha |
| #29146 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29046 | True | False | 0.98 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29392 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29012 | True | False | 0.98 | Docs: six CLI flags missing from the reference table |
| #29317 | True | False | 0.97 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |

**decider@openrouter** (37)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29290 | True | False | 0.99 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29424 | True | False | 0.99 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |

**decision-1@openrouter** (43)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 1.00 | Gemini lolo |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28783 | False | True | 1.00 | cutealexamartha |
| #29221 | False | True | 1.00 | Leeres.blaat_A4-DIN |
| #29220 | False | True | 1.00 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |

**drex-max@openrouter** (39)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29388 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29100 | False | True | 1.00 | Gemini lolo |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29290 | True | False | 0.99 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29392 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |

**elephant@openrouter** (29)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28846 | True | False | 0.98 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29012 | True | False | 0.97 | Docs: six CLI flags missing from the reference table |
| #29311 | True | False | 0.97 | bug(core): insecure user/workspace policy dirs skip permission checks… |
| #29001 | True | False | 0.97 | security(a2a-server): HTTP API never enforces authentication, and the… |

**jev:1.14** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.98 | Gemini lolo |
| #28783 | False | True | 0.98 | cutealexamartha |
| #29111 | False | True | 0.97 | ejecucion lenta |
| #29146 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29220 | False | True | 0.97 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #29392 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29388 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |

**joey@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29415 | True | False | 0.92 | gemini --help exits with code 5 after winget install on Windows 11 |
| #29305 | True | False | 0.91 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |

**kev@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 0.94 | Docs: six CLI flags missing from the reference table |
| #29316 | True | False | 0.93 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29147 | False | True | 0.91 | GeminiCLI.com Feedback: [ISSUE] |
| #29317 | True | False | 0.91 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29308 | True | False | 0.90 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |

**luna@decisions** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29207 | True | False | 1.00 | Corrupt agents.json (valid JSON, wrong shape) crashes acknowledgment |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29100 | False | True | 0.99 | Gemini lolo |
| #29221 | False | True | 0.99 | Leeres.blaat_A4-DIN |

**mammoth@openrouter** (34)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29207 | True | False | 1.00 | Corrupt agents.json (valid JSON, wrong shape) crashes acknowledgment |
| #29392 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29012 | True | False | 0.99 | Docs: six CLI flags missing from the reference table |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |

**mercury@openrouter** (46)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29204 | True | False | 1.00 | MCP prompt responses are submitted as JSON-encoded text |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29610 | True | False | 1.00 | Gemini CLI extension gallery has not indexed suhaib81/url-shortener-b… |
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |

**span@openrouter** (37)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29424 | True | False | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |


## Cases the models disagree on (12 of 52)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #29418 | True | True (0.90) | True (0.91) | True (0.97) | True (0.97) | True (0.91) | True (0.81) | True (0.94) | True (1.00) | True (0.92) | True (0.97) | True (0.97) | True (0.63) | True (0.74) | True (0.99) | True (0.88) | False (0.65) | True (0.99) | GeminiCLI.com Feedback: [ISSUE] |
| #28809 | False | False (0.92) | False (0.97) | False (0.95) | False (0.86) | False (0.95) | False (0.95) | False (0.98) | False (0.85) | False (0.98) | False (0.82) | False (0.86) | False (0.86) | False (0.90) | False (0.97) | False (0.95) | True (0.92) | False (1.00) | GeminiCLI.com Feedback: kyisaiah47/kynth-gemini-extension missing fro… |
| #29390 | False | True (0.77) | True (0.66) | True (0.98) | True (0.96) | True (1.00) | True (0.95) | True (0.99) | True (1.00) | True (0.99) | True (0.92) | True (0.97) | True (0.56) | False (0.63) | True (0.87) | True (0.94) | True (1.00) | True (0.87) | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29388 | False | True (0.77) | True (0.62) | True (0.99) | True (0.98) | True (1.00) | True (0.95) | True (0.99) | True (1.00) | True (1.00) | True (0.92) | True (0.97) | True (0.56) | False (0.63) | True (0.87) | True (0.94) | True (1.00) | True (0.87) | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29135 | True | True (0.87) | True (0.52) | True (0.91) | True (0.96) | True (0.56) | True (0.77) | True (0.95) | True (1.00) | True (0.92) | True (0.82) | True (0.91) | True (0.58) | False (0.50) | False (0.69) | True (0.95) | False (0.65) | True (0.84) | Features |
| #29221 | False | True (0.88) | True (0.75) | True (0.85) | True (0.99) | True (0.86) | True (0.76) | True (0.94) | True (1.00) | True (0.97) | True (0.82) | True (0.95) | False (0.55) | True (0.57) | True (0.99) | True (0.95) | True (0.96) | True (0.95) | Leeres.blaat_A4-DIN |
| #28923 | True | True (0.92) | True (0.92) | True (0.87) | True (0.98) | True (0.97) | True (0.65) | True (0.98) | True (1.00) | True (0.99) | True (0.90) | True (0.97) | False (0.54) | True (0.81) | True (0.94) | True (0.96) | True (0.99) | True (0.98) | GeminiCLI.com Feedback: [ISSUE] |
| #29107 | False | True (0.73) | True (0.69) | True (0.94) | True (0.94) | True (0.99) | True (0.62) | True (0.88) | True (1.00) | True (0.92) | True (0.85) | True (0.94) | True (0.64) | False (0.55) | True (0.93) | True (0.93) | True (0.95) | True (0.93) | "The caller does not have permission  #25306 - still persists |
| #28717 | False | False (0.93) | False (0.97) | False (0.87) | False (0.70) | False (1.00) | False (0.89) | False (0.93) | True (0.85) | False (0.93) | False (0.90) | False (0.84) | False (0.85) | False (0.84) | False (0.88) | False (0.96) | False (0.99) | False (1.00) | [Bug]: Google AI Pro sign-in silently falls back to API key onboardin… |
| #29128 | False | False (0.87) | False (0.92) | False (0.67) | False (0.82) | False (0.85) | False (0.80) | False (0.97) | True (0.73) | False (0.93) | False (0.72) | True (0.55) | False (0.66) | False (0.81) | False (0.70) | False (0.83) | False (1.00) | False (0.89) | Add agy cli to docker sbx |
| #29224 | True | True (0.75) | True (0.57) | True (0.96) | True (0.96) | True (0.96) | True (0.95) | True (0.98) | True (1.00) | True (0.98) | True (0.77) | True (0.95) | False (0.64) | False (0.62) | True (0.86) | True (0.95) | True (1.00) | True (0.89) | npm install -g @google/gemini-cli@preview |
| #29381 | False | False (0.52) | False (0.51) | False (0.84) | True (0.73) | False (0.84) | False (0.87) | False (0.81) | False (1.00) | False (0.61) | True (0.71) | False (0.74) | False (0.86) | False (0.81) | False (0.98) | False (0.77) | False (0.98) | False (0.53) | Created in error — please disregard |
