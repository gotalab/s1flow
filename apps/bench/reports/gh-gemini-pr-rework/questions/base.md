# gh-gemini-pr-rework

2026-10-31 · 338 labelled dev cases (False 247, True 91) · split: stratified k-fold (no test case among these: CV numbers only) · source: Merged PRs of google-gemini/gemini-cli (review history via the GitHub API)

**decider@openrouter** has the highest coverage at 95% accuracy, 16% [12, 19] (API cost $0.12 per 10k, p99 454ms). Its interval overlaps with drex-max@openrouter, clef@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is decider@openrouter's, 75% [70, 80].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 338 | 73.4% [68, 78] | 0.12 | 0.69 | 0.13 | 1% [0, 2] | 100.0% (36.8%) | 0/338 | 0/338 |
| clef@openrouter | 338 | 68.3% [63, 73] | 0.42 | 0.70 | 0.08 | 10% [7, 13] | 88.2% (75.1%) | 0/338 | 0/338 |
| d1-ultra@openrouter | 338 | 71.0% [66, 76] | 0.49 | 0.72 | 0.05 | 5% [3, 8] | 100.0% (84.7%) | 0/338 | 0/338 |
| d1.1@openrouter | 338 | 69.2% [64, 75] | 0.41 | 0.70 | 0.11 | 0% [0, 1] | 0.0% (0.0%) | 0/338 | 0/338 |
| d1@vercel | 338 | 72.5% [68, 78] | 0.34 | 0.70 | 0.14 | 5% [3, 8] | 82.4% (60.4%) | 0/338 | 0/338 |
| decider-flash@openrouter | 338 | 73.7% [69, 78] | 0.08 | 0.67 | 0.08 | 5% [3, 7] | 87.5% (65.6%) | 0/338 | 0/338 |
| decider@openrouter | 338 | 74.9% [70, 80] | 0.33 | 0.71 | 0.08 | 16% [12, 19] | 92.5% (83.6%) | 0/338 | 0/338 |
| decision-1@openrouter | 338 | 60.1% [55, 65] | 0.48 | 0.68 | 0.15 | 0% [0, 1] | 0.0% (0.0%) | 0/338 | 0/338 |
| drex-max@openrouter | 338 | 74.9% [70, 79] | 0.39 | 0.70 | 0.11 | 10% [7, 14] | 88.6% (75.7%) | 0/338 | 0/338 |
| elephant@openrouter | 338 | 72.8% [68, 77] | 0.47 | 0.69 | 0.05 | 4% [2, 6] | 78.6% (53.4%) | 0/338 | 0/338 |
| jev:1.14 | 338 | 71.3% [67, 76] | 0.46 | 0.71 | 0.06 | 1% [0, 2] | 75.0% (24.9%) | 0/338 | 0/338 |
| joey@openrouter | 338 | 73.4% [69, 78] | 0.29 | 0.70 | 0.06 | 1% [0, 2] | 66.7% (13.5%) | 0/338 | 0/338 |
| kev@openrouter | 338 | 73.1% [68, 78] | 0.06 | 0.63 | 0.02 | 2% [1, 4] | 100.0% (65.2%) | 0/338 | 0/338 |
| luna@decisions | 338 | 70.1% [65, 75] | 0.48 | 0.72 | 0.06 | 0% [0, 1] | 0.0% (0.0%) | 0/338 | 0/338 |
| mammoth@openrouter | 338 | 69.2% [64, 75] | 0.49 | 0.74 | 0.05 | 7% [4, 11] | 84.0% (67.0%) | 0/338 | 0/338 |
| mercury@openrouter | 338 | 72.5% [68, 78] | 0.36 | 0.69 | 0.17 | 5% [3, 8] | 77.8% (56.1%) | 0/338 | 0/338 |
| span@openrouter | 338 | 74.3% [69, 79] | 0.38 | 0.70 | 0.18 | 8% [5, 11] | 88.9% (73.7%) | 0/338 | 0/338 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 1, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| decider@openrouter = | 16% [12, 19] | 0.251 [0.204, 0.299] | 0.93 | met |
| drex-max@openrouter = | 10% [7, 14] | 0.251 [0.207, 0.302] | 0.97 | met |
| clef@openrouter = | 10% [7, 13] | 0.317 [0.269, 0.367] | 0.91 | met |
| span@openrouter | 8% [5, 11] | 0.257 [0.210, 0.308] | 1.00 | met |
| mammoth@openrouter | 7% [4, 11] | 0.308 [0.254, 0.358] | 0.87 | met |
| mercury@openrouter | 5% [3, 8] | 0.275 [0.225, 0.320] | 0.99 | met |
| d1-ultra@openrouter | 5% [3, 8] | 0.290 [0.240, 0.343] | 0.93 | met |
| d1@vercel | 5% [3, 8] | 0.275 [0.225, 0.322] | 1.00 | met |
| decider-flash@openrouter | 5% [3, 7] | 0.263 [0.216, 0.311] | 0.92 | met |
| elephant@openrouter | 4% [2, 6] | 0.272 [0.228, 0.322] | — | met |
| kev@openrouter | 2% [1, 4] | 0.269 [0.225, 0.317] | 0.87 | met |
| jev:1.14 | 1% [0, 2] | 0.287 [0.237, 0.334] | 0.85 | met |
| clef-flash@openrouter | 1% [0, 2] | 0.266 [0.222, 0.317] | 0.96 | met |
| joey@openrouter | 1% [0, 2] | 0.266 [0.219, 0.314] | 0.89 | met |
| luna@decisions | 0% [0, 1] | 0.299 [0.249, 0.352] | 0.93 | met |
| d1.1@openrouter | 0% [0, 1] | 0.308 [0.254, 0.358] | — | met |
| decision-1@openrouter | 0% [0, 1] | 0.399 [0.349, 0.453] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 338 | 425 ms | 532 ms | 1433 ms | 2296 ms | 3.4 | 0 | 4 | $0.14 | billed |  |
| clef@openrouter | 338 | 344 ms | 472 ms | 941 ms | 1395 ms | 2.7 | 0 | 4 | $1.39 | billed |  |
| d1-ultra@openrouter | 338 | 228 ms | 333 ms | 562 ms | 732 ms | 2.5 | 0 | 4 | $0.25 | billed |  |
| d1.1@openrouter | 338 | 173 ms | 251 ms | 391 ms | 828 ms | 2.3 | 0 | 4 | $0.12 | billed |  |
| d1@vercel | 338 | 266 ms | 383 ms | 557 ms | 752 ms | 2.1 | 0 | 4 | $0.12 | billed |  |
| decider-flash@openrouter | 338 | 147 ms | 166 ms | 274 ms | 523 ms | 1.9 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 338 | 227 ms | 264 ms | 454 ms | 550 ms | 2.0 | 0 | 4 | $0.12 | billed | ○ |
| decision-1@openrouter | 338 | 278 ms | 352 ms | 526 ms | 861 ms | 1.9 | 0 | 4 | $0.23 | billed |  |
| drex-max@openrouter | 338 | 323 ms | 617 ms | 1162 ms | 2434 ms | 3.6 | 7 | 4 | $0.36 | billed |  |
| elephant@openrouter | 338 | 192 ms | 215 ms | 319 ms | 540 ms | 1.7 | 0 | 4 | $0.21 | billed |  |
| jev:1.14 | 338 | 146 ms | 178 ms | 219 ms | 317 ms | 1.5 | 0 | 4 | $0.35 | estimated | ○ |
| joey@openrouter | 338 | 178 ms | 204 ms | 270 ms | 414 ms | 1.5 | 0 | 4 | $0.06 | billed | ○ |
| kev@openrouter | 338 | 315 ms | 721 ms | 1016 ms | 1367 ms | 3.2 | 0 | 4 | $0.22 | billed |  |
| luna@decisions | 338 | 224 ms | 394 ms | 606 ms | 968 ms | 2.7 | 4 | 4 | $0.69 | estimated |  |
| mammoth@openrouter | 338 | 226 ms | 263 ms | 500 ms | 633 ms | 2.2 | 0 | 4 | $0.61 | billed |  |
| mercury@openrouter | 338 | 311 ms | 379 ms | 487 ms | 637 ms | 1.6 | 0 | 4 | $0.11 | billed | ○ |
| span@openrouter | 338 | 341 ms | 879 ms | 964 ms | 1211 ms | 2.8 | 0 | 4 | $0.07 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0048 | 36 s (estimated, 338 calls) | 18 min | 4 |
| clef@openrouter | $0.05 | 31 s (estimated, 338 calls) | 15 min | 4 |
| d1-ultra@openrouter | $0.0083 | 21 s (estimated, 338 calls) | 11 min | 4 |
| d1.1@openrouter | $0.0040 | 16 s (estimated, 338 calls) | 8 min | 4 |
| d1@vercel | $0.0040 | 24 s (estimated, 338 calls) | 12 min | 4 |
| decider-flash@openrouter | $0.0020 | 13 s (estimated, 338 calls) | 6 min | 4 |
| decider@openrouter | $0.0041 | 20 s (estimated, 338 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0077 | 25 s (estimated, 338 calls) | 12 min | 4 |
| drex-max@openrouter | $0.01 | 31 s (estimated, 338 calls) | 16 min | 4 |
| elephant@openrouter | $0.0072 | 17 s (estimated, 338 calls) | 8 min | 4 |
| jev:1.14 | $0.01 | 13 s (estimated, 338 calls) | 6 min | 4 |
| joey@openrouter | $0.0021 | 16 s (estimated, 338 calls) | 8 min | 4 |
| kev@openrouter | $0.0074 | 34 s (estimated, 338 calls) | 17 min | 4 |
| luna@decisions | $0.02 | 22 s (estimated, 338 calls) | 11 min | 4 |
| mammoth@openrouter | $0.02 | 20 s (estimated, 338 calls) | 10 min | 4 |
| mercury@openrouter | $0.0039 | 27 s (estimated, 338 calls) | 13 min | 4 |
| span@openrouter | $0.0023 | 40 s (estimated, 338 calls) | 20 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 73.4% | 74.9% | 75 | 10 | 0.40 | 0.40 |
| clef@openrouter | 68.3% | 76.3% | 67 | 13 | 0.75 | 0.75 |
| d1-ultra@openrouter | 71.0% | 73.4% | 70 | 20 | 0.75 | 0.75 |
| d1.1@openrouter | 69.2% | 72.8% | 77 | 15 | 0.85 | 0.85 |
| d1@vercel | 72.5% | 75.1% | 69 | 15 | 0.70 | 0.70 |
| decider-flash@openrouter | 73.7% | 74.0% | 79 | 9 | 0.40 | 0.35 |
| decider@openrouter | 74.9% | 76.3% | 71 | 9 | 0.55 | 0.55 |
| decision-1@openrouter | 60.1% | 76.0% | 59 | 22 | 0.85 | 0.85 |
| drex-max@openrouter | 74.9% | 74.0% | 65 | 23 | 0.55 | 0.55 |
| elephant@openrouter | 72.8% | 71.9% | 68 | 27 | 0.60 | 0.60 |
| jev:1.14 | 71.3% | 74.0% | 63 | 25 | 0.55 | 0.55 |
| joey@openrouter | 73.4% | 72.5% | 75 | 18 | 0.55 | 0.55 |
| kev@openrouter | 73.1% | 72.2% | 80 | 14 | 0.40 | 0.45 |
| luna@decisions | 70.1% | 75.4% | 65 | 18 | 0.75 | 0.75 |
| mammoth@openrouter | 69.2% | 72.5% | 76 | 17 | 0.75 | 0.70 |
| mercury@openrouter | 72.5% | 74.3% | 81 | 6 | 0.95 | 0.95 |
| span@openrouter | 74.3% | 72.5% | 69 | 24 | 0.50 | 0.50 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (29%) | 105 (43%) |
| 0.20 | 64 (70%) | 32 (13%) |
| 0.30 | 68 (75%) | 18 (7%) |
| 0.40 | 75 (82%) | 8 (3%) |
| 0.50 | 85 (93%) | 5 (2%) |
| 0.60 | 86 (95%) | 3 (1%) |
| 0.70 | 90 (99%) | 2 (1%) |
| 0.80 | 90 (99%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (3%) | 196 (79%) |
| 0.20 | 17 (19%) | 135 (55%) |
| 0.30 | 31 (34%) | 95 (38%) |
| 0.40 | 43 (47%) | 73 (30%) |
| 0.50 | 53 (58%) | 54 (22%) |
| 0.60 | 57 (63%) | 38 (15%) |
| 0.70 | 65 (71%) | 20 (8%) |
| 0.75 | 67 (74%) | 13 (5%) |
| 0.80 | 74 (81%) | 9 (4%) |
| 0.90 | 90 (99%) | 1 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 210 (85%) |
| 0.20 | 14 (15%) | 141 (57%) |
| 0.30 | 26 (29%) | 102 (41%) |
| 0.40 | 37 (41%) | 69 (28%) |
| 0.50 | 43 (47%) | 55 (22%) |
| 0.60 | 56 (62%) | 37 (15%) |
| 0.70 | 62 (68%) | 26 (11%) |
| 0.75 | 64 (70%) | 20 (8%) |
| 0.80 | 71 (78%) | 13 (5%) |
| 0.90 | 85 (93%) | 4 (2%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 8 (9%) | 170 (69%) |
| 0.20 | 16 (18%) | 124 (50%) |
| 0.30 | 32 (35%) | 84 (34%) |
| 0.40 | 41 (45%) | 60 (24%) |
| 0.50 | 55 (60%) | 49 (20%) |
| 0.60 | 62 (68%) | 42 (17%) |
| 0.70 | 67 (74%) | 35 (14%) |
| 0.80 | 70 (77%) | 21 (9%) |
| 0.85 | 71 (78%) | 16 (6%) |
| 0.90 | 81 (89%) | 12 (5%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 24 (26%) | 97 (39%) |
| 0.20 | 41 (45%) | 68 (28%) |
| 0.30 | 54 (59%) | 46 (19%) |
| 0.40 | 60 (66%) | 36 (15%) |
| 0.50 | 67 (74%) | 26 (11%) |
| 0.60 | 69 (76%) | 22 (9%) |
| 0.70 | 69 (76%) | 15 (6%) |
| 0.80 | 79 (87%) | 10 (4%) |
| 0.90 | 86 (95%) | 5 (2%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 8 (9%) | 199 (81%) |
| 0.20 | 46 (51%) | 55 (22%) |
| 0.30 | 68 (75%) | 24 (10%) |
| 0.35 | 75 (82%) | 10 (4%) |
| 0.40 | 80 (88%) | 6 (2%) |
| 0.50 | 87 (96%) | 2 (1%) |
| 0.60 | 88 (97%) | 1 (0%) |
| 0.70 | 90 (99%) | 1 (0%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 13 (14%) | 157 (64%) |
| 0.20 | 43 (47%) | 70 (28%) |
| 0.30 | 53 (58%) | 36 (15%) |
| 0.40 | 67 (74%) | 22 (9%) |
| 0.50 | 70 (77%) | 15 (6%) |
| 0.55 | 71 (78%) | 9 (4%) |
| 0.60 | 75 (82%) | 7 (3%) |
| 0.70 | 83 (91%) | 3 (1%) |
| 0.80 | 90 (99%) | 2 (1%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 217 (88%) |
| 0.20 | 7 (8%) | 191 (77%) |
| 0.30 | 16 (18%) | 156 (63%) |
| 0.40 | 26 (29%) | 126 (51%) |
| 0.50 | 29 (32%) | 106 (43%) |
| 0.60 | 40 (44%) | 80 (32%) |
| 0.70 | 46 (51%) | 58 (23%) |
| 0.80 | 57 (63%) | 34 (14%) |
| 0.85 | 59 (65%) | 22 (9%) |
| 0.90 | 71 (78%) | 15 (6%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 20 (22%) | 132 (53%) |
| 0.20 | 45 (49%) | 58 (23%) |
| 0.30 | 53 (58%) | 45 (18%) |
| 0.40 | 59 (65%) | 27 (11%) |
| 0.50 | 64 (70%) | 21 (9%) |
| 0.55 | 65 (71%) | 18 (7%) |
| 0.60 | 67 (74%) | 16 (6%) |
| 0.70 | 70 (77%) | 13 (5%) |
| 0.80 | 78 (86%) | 8 (3%) |
| 0.90 | 83 (91%) | 6 (2%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 226 (91%) |
| 0.20 | 12 (13%) | 152 (62%) |
| 0.30 | 33 (36%) | 95 (38%) |
| 0.40 | 43 (47%) | 67 (27%) |
| 0.50 | 51 (56%) | 41 (17%) |
| 0.60 | 63 (69%) | 23 (9%) |
| 0.70 | 74 (81%) | 17 (7%) |
| 0.80 | 83 (91%) | 8 (3%) |
| 0.90 | 88 (97%) | 2 (1%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 1 (1%) | 238 (96%) |
| 0.30 | 7 (8%) | 172 (70%) |
| 0.40 | 30 (33%) | 97 (39%) |
| 0.50 | 49 (54%) | 48 (19%) |
| 0.55 | 52 (57%) | 31 (13%) |
| 0.60 | 61 (67%) | 25 (10%) |
| 0.70 | 79 (87%) | 11 (4%) |
| 0.80 | 90 (99%) | 1 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 5 (5%) | 201 (81%) |
| 0.30 | 24 (26%) | 108 (44%) |
| 0.40 | 47 (52%) | 47 (19%) |
| 0.50 | 73 (80%) | 17 (7%) |
| 0.55 | 79 (87%) | 8 (3%) |
| 0.60 | 81 (89%) | 6 (2%) |
| 0.70 | 88 (97%) | 2 (1%) |
| 0.80 | 90 (99%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 246 (100%) |
| 0.20 | 15 (16%) | 175 (71%) |
| 0.30 | 58 (64%) | 52 (21%) |
| 0.40 | 82 (90%) | 8 (3%) |
| 0.45 | 86 (95%) | 4 (2%) |
| 0.50 | 88 (97%) | 3 (1%) |
| 0.60 | 91 (100%) | 1 (0%) |
| 0.70 | 91 (100%) | 0 (0%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 1 (1%) | 230 (93%) |
| 0.30 | 12 (13%) | 137 (55%) |
| 0.40 | 37 (41%) | 76 (31%) |
| 0.50 | 45 (49%) | 56 (23%) |
| 0.60 | 48 (53%) | 45 (18%) |
| 0.70 | 60 (66%) | 23 (9%) |
| 0.75 | 65 (71%) | 15 (6%) |
| 0.80 | 76 (84%) | 9 (4%) |
| 0.90 | 89 (98%) | 1 (0%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 234 (95%) |
| 0.20 | 5 (5%) | 166 (67%) |
| 0.30 | 16 (18%) | 122 (49%) |
| 0.40 | 30 (33%) | 85 (34%) |
| 0.50 | 41 (45%) | 63 (26%) |
| 0.60 | 50 (55%) | 40 (16%) |
| 0.70 | 65 (71%) | 18 (7%) |
| 0.80 | 78 (86%) | 7 (3%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (mercury@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 33 (36%) | 83 (34%) |
| 0.20 | 48 (53%) | 56 (23%) |
| 0.30 | 57 (63%) | 39 (16%) |
| 0.40 | 60 (66%) | 31 (13%) |
| 0.50 | 65 (71%) | 28 (11%) |
| 0.60 | 68 (75%) | 23 (9%) |
| 0.70 | 72 (79%) | 21 (9%) |
| 0.80 | 76 (84%) | 13 (5%) |
| 0.90 | 78 (86%) | 9 (4%) |
| 0.95 | 81 (89%) | 3 (1%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 52 (57%) | 52 (21%) |
| 0.20 | 56 (62%) | 33 (13%) |
| 0.30 | 60 (66%) | 29 (12%) |
| 0.40 | 62 (68%) | 28 (11%) |
| 0.50 | 64 (70%) | 23 (9%) |
| 0.60 | 69 (76%) | 20 (8%) |
| 0.70 | 75 (82%) | 18 (7%) |
| 0.80 | 77 (85%) | 12 (5%) |
| 0.90 | 85 (93%) | 5 (2%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (26)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.96 | fix(core): update auth error documentation link to valid anchor and a… |
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #28216 | True | False | 0.95 | Refactor: exclude transient CI configuration files from workspace con… |
| #28940 | True | False | 0.94 | fix(a2a-server): clear stale cancellation error on new message turns |
| #27391 | True | False | 0.94 | fix(cli): filter internal session context from history during resumpt… |
| #27467 | True | False | 0.94 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #27698 | True | False | 0.94 | fix(core): Ensure zero-quota limits fail fast to prevent retry loop h… |

**clef@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |
| #26991 | True | False | 0.90 | fix(ui): clamped table column widths |

**d1-ultra@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29115 | False | True | 0.93 | fix(config): enforce strict permission and ownership checks on system… |
| #25822 | True | False | 0.93 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.93 | Fix bulk of remaining issues with generalist profile |
| #28470 | False | True | 0.92 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #28530 | False | True | 0.92 | feat(caretaker-evals): add triage evaluation framework and judge runn… |

**d1.1@openrouter** (20)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #28470 | False | True | 0.98 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #29185 | True | False | 0.98 | test(integration): deflake run_shell_command and file-system-interact… |
| #26991 | True | False | 0.98 | fix(ui): clamped table column widths |
| #26073 | False | True | 0.97 | Fix bulk of remaining issues with generalist profile |
| #25324 | True | False | 0.97 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #29120 | False | True | 0.96 | fix(core): improve destination validation and connection routing in w… |
| #26949 | True | False | 0.95 | fix(ci): configure git remote with token for authentication |

**d1@vercel** (29)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #29377 | True | False | 1.00 | fix(core): update auth error documentation link to valid anchor and a… |
| #26991 | True | False | 0.99 | fix(ui): clamped table column widths |
| #28216 | True | False | 0.99 | Refactor: exclude transient CI configuration files from workspace con… |
| #25324 | True | False | 0.99 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #29185 | True | False | 0.99 | test(integration): deflake run_shell_command and file-system-interact… |
| #26949 | True | False | 0.99 | fix(ci): configure git remote with token for authentication |
| #27467 | True | False | 0.99 | fix(core): handle multi-line escaped quotes in stripShellWrapper |

**decider-flash@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #26947 | True | False | 0.92 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #27007 | True | False | 0.91 | fix(core): add aliases and thinking config for gemini-3.1 models |
| #25670 | True | False | 0.91 | fix(core): remove duplicate initialize call on agents refreshed |
| #28940 | True | False | 0.91 | fix(a2a-server): clear stale cancellation error on new message turns |
| #29377 | True | False | 0.91 | fix(core): update auth error documentation link to valid anchor and a… |
| #27391 | True | False | 0.90 | fix(cli): filter internal session context from history during resumpt… |
| #28216 | True | False | 0.90 | Refactor: exclude transient CI configuration files from workspace con… |

**decider@openrouter** (13)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #26949 | True | False | 0.94 | fix(ci): configure git remote with token for authentication |
| #29377 | True | False | 0.93 | fix(core): update auth error documentation link to valid anchor and a… |
| #26947 | True | False | 0.93 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #29185 | True | False | 0.93 | test(integration): deflake run_shell_command and file-system-interact… |
| #27619 | True | False | 0.93 | fix(core): implement atomic update in MCP tool discovery |
| #25827 | True | False | 0.93 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #27234 | True | False | 0.91 | fix(core): prevent path traversal in custome command file injection |

**decision-1@openrouter** (17)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26073 | False | True | 1.00 | Fix bulk of remaining issues with generalist profile |
| #27345 | False | True | 0.98 | feat(context): Complete simplification work. |
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #25716 | False | True | 0.98 | refactor(memory): replace MemoryManagerAgent with prompt-driven memor… |
| #28470 | False | True | 0.98 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #28530 | False | True | 0.97 | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #26949 | True | False | 0.97 | fix(ci): configure git remote with token for authentication |
| #26143 | False | True | 0.96 | refactor(acp): modularize monolithic acpClient into specialized files |

**drex-max@openrouter** (26)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #28216 | True | False | 0.97 | Refactor: exclude transient CI configuration files from workspace con… |
| #28470 | False | True | 0.97 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #27253 | True | False | 0.95 | fix: robust ripgrep path resolution and 1p hermetic execution support |
| #25324 | True | False | 0.95 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #25827 | True | False | 0.95 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #27619 | True | False | 0.95 | fix(core): implement atomic update in MCP tool discovery |

**elephant@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #28470 | False | True | 0.94 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #26073 | False | True | 0.92 | Fix bulk of remaining issues with generalist profile |
| #29185 | True | False | 0.90 | test(integration): deflake run_shell_command and file-system-interact… |

**luna@decisions** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26073 | False | True | 0.92 | Fix bulk of remaining issues with generalist profile |

**mammoth@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.93 | fix(cli): add missing response key to custom theme text schema |

**mercury@openrouter** (42)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #28470 | False | True | 0.99 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #26073 | False | True | 0.99 | Fix bulk of remaining issues with generalist profile |
| #26947 | True | False | 0.99 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #28223 | True | False | 0.99 | fix(core-tools): bypass LLM correction for JSON and IPYNB files in wr… |
| #27467 | True | False | 0.99 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #28216 | True | False | 0.99 | Refactor: exclude transient CI configuration files from workspace con… |
| #27619 | True | False | 0.99 | fix(core): implement atomic update in MCP tool discovery |

**span@openrouter** (57)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28216 | True | False | 1.00 | Refactor: exclude transient CI configuration files from workspace con… |
| #26991 | True | False | 1.00 | fix(ui): clamped table column widths |
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #28940 | True | False | 0.99 | fix(a2a-server): clear stale cancellation error on new message turns |
| #26270 | True | False | 0.99 | feat(ui): added microphone and updated placeholder for voice mode |
| #25324 | True | False | 0.99 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #25670 | True | False | 0.99 | fix(core): remove duplicate initialize call on agents refreshed |


## Cases the models disagree on (12 of 197)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #26285 | False | False (0.95) | False (0.91) | False (0.93) | False (0.97) | False (1.00) | False (0.92) | False (0.95) | True (0.53) | False (0.98) | False (0.83) | False (0.75) | False (0.77) | False (0.83) | False (0.80) | False (0.85) | False (0.93) | False (1.00) | fix(cli): use resolved sandbox state for auto-update check |
| #26453 | False | False (0.95) | False (0.95) | False (0.89) | False (0.99) | False (1.00) | False (0.91) | False (0.96) | False (0.93) | False (0.99) | False (0.90) | False (0.77) | False (0.86) | False (0.85) | False (0.83) | False (0.89) | True (0.50) | False (1.00) | fix(cli): allow early stdout when config is undefined |
| #28216 | True | False (0.95) | False (0.83) | False (0.81) | False (0.82) | False (0.99) | False (0.90) | False (0.91) | True (0.56) | False (0.97) | False (0.77) | False (0.69) | False (0.85) | False (0.86) | False (0.77) | False (0.75) | False (0.99) | False (1.00) | Refactor: exclude transient CI configuration files from workspace con… |
| #27353 | False | False (0.94) | False (0.87) | False (0.83) | False (0.94) | False (1.00) | False (0.88) | False (0.91) | True (0.59) | False (0.90) | False (0.79) | False (0.66) | False (0.78) | False (0.80) | False (0.79) | False (0.81) | False (0.96) | False (1.00) | fix(ui): added volta to auto update check |
| #26128 | False | False (0.95) | False (0.87) | False (0.84) | False (0.96) | False (0.99) | False (0.87) | False (0.93) | True (0.56) | False (0.89) | False (0.76) | False (0.72) | False (0.75) | False (0.82) | False (0.80) | False (0.83) | False (0.97) | False (1.00) | fix(ux): added error message for ENOTDIR |
| #26446 | False | False (0.93) | False (0.74) | False (0.78) | False (0.82) | False (0.98) | False (0.87) | False (0.90) | True (0.75) | False (0.86) | False (0.63) | False (0.68) | False (0.70) | False (0.80) | False (0.74) | False (0.86) | False (0.98) | False (1.00) | refactor(UI): created constants file for ThemeDialog |
| #26125 | False | False (0.93) | False (0.83) | False (0.88) | False (0.91) | False (0.93) | False (0.86) | False (0.91) | True (0.56) | False (0.94) | False (0.90) | False (0.67) | False (0.88) | False (0.82) | False (0.68) | False (0.73) | False (0.84) | False (1.00) | fix(cli): prevent ACP stdout pollution from SessionEnd hooks |
| #26191 | False | False (0.93) | False (0.86) | False (0.81) | False (0.91) | False (1.00) | False (0.88) | False (0.93) | True (0.53) | False (0.95) | False (0.67) | False (0.68) | False (0.74) | False (0.81) | False (0.75) | False (0.76) | False (0.97) | False (0.98) | fix(core): reduce default API timeout to 60s and enable retries for u… |
| #26229 | False | False (0.94) | False (0.88) | False (0.75) | False (0.89) | False (0.99) | False (0.84) | False (0.89) | True (0.71) | False (0.94) | False (0.77) | False (0.71) | False (0.67) | False (0.79) | False (0.74) | False (0.84) | False (0.96) | False (1.00) | fix(ui): made shell tool header wrap on Ctrl+O |
| #28038 | False | False (0.93) | False (0.93) | False (0.79) | False (0.93) | False (0.91) | False (0.85) | False (0.94) | False (0.59) | False (0.92) | True (0.58) | False (0.61) | False (0.70) | False (0.78) | False (0.79) | False (0.72) | False (0.97) | False (0.99) | fix(ci): append trailing slash to registry url in npmrc |
| #28467 | False | False (0.92) | False (0.85) | False (0.87) | False (0.96) | False (0.99) | False (0.86) | False (0.93) | True (0.65) | False (0.94) | False (0.76) | False (0.65) | False (0.70) | False (0.78) | False (0.67) | False (0.68) | False (0.97) | False (0.98) | feat(caretaker): update Firestore schema with error, and pr_number fi… |
| #28940 | True | False (0.94) | False (0.75) | False (0.76) | False (0.83) | False (0.96) | False (0.91) | False (0.87) | True (0.65) | False (0.90) | False (0.58) | False (0.70) | False (0.78) | False (0.85) | False (0.65) | False (0.70) | False (0.93) | False (0.99) | fix(a2a-server): clear stale cancellation error on new message turns |
