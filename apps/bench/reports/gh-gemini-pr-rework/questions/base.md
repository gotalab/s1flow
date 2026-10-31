# gh-gemini-pr-rework

2026-10-31 · 338 labelled dev cases (False 247, True 91) · split: stratified k-fold (no test case among these: CV numbers only) · source: Merged PRs of google-gemini/gemini-cli (review history via the GitHub API)

**decider@openrouter** has the highest coverage at 95% accuracy, 16% [12, 19] (API cost $0.12 per 10k, p99 5241ms). Its interval overlaps with drex-max@openrouter, clef@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. Ordered by task.py's tiebreak (loss per case (miss 1, false alarm 1)), **drex-max@openrouter** comes first (API cost $0.36 per 10k, p99 4268ms). The highest raw accuracy (dev) is drex-max@openrouter's, 75% [70, 80].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 338 | 73.4% [68, 78] | 0.12 | 0.69 | 0.14 | 3% [1, 4] | 77.8% (45.0%) | 0/338 | 0/338 |
| clef@openrouter | 338 | 70.4% [65, 75] | 0.46 | 0.70 | 0.08 | 10% [7, 13] | 87.9% (74.4%) | 0/338 | 0/338 |
| d1-ultra@openrouter | 338 | 71.0% [66, 76] | 0.48 | 0.71 | 0.07 | 6% [3, 8] | 89.5% (70.4%) | 0/338 | 0/338 |
| d1.1@openrouter | 338 | 68.9% [64, 74] | 0.44 | 0.71 | 0.11 | 3% [1, 4] | 66.7% (34.5%) | 0/338 | 0/338 |
| d1@vercel | 338 | 72.5% [68, 77] | 0.36 | 0.72 | 0.14 | 3% [1, 5] | 100.0% (76.2%) | 0/338 | 0/338 |
| decider-flash@openrouter | 338 | 73.7% [69, 78] | 0.08 | 0.67 | 0.08 | 5% [3, 7] | 87.5% (65.6%) | 0/338 | 0/338 |
| decider@openrouter | 338 | 74.9% [70, 80] | 0.33 | 0.71 | 0.08 | 16% [12, 19] | 92.5% (83.6%) | 0/338 | 0/338 |
| decision-1@openrouter | 338 | 59.8% [54, 64] | 0.47 | 0.69 | 0.15 | 0% [0, 1] | 0.0% (0.0%) | 0/338 | 0/338 |
| drex-max@openrouter | 338 | 75.1% [70, 80] | 0.39 | 0.69 | 0.10 | 9% [6, 12] | 93.5% (81.1%) | 0/338 | 0/338 |
| elephant@openrouter | 338 | 72.8% [68, 77] | 0.47 | 0.69 | 0.05 | 4% [2, 6] | 78.6% (53.4%) | 0/338 | 0/338 |
| flash-lite@vercel ※ | 338 | 72.8% [68, 78] | 0.10 | 0.52 | 0.27 | 0% [0, 0] | — (0.0%) | 0/338 | 0/338 |
| haiku@vercel ※ | 338 | 64.8% [59, 70] | 0.47 | 0.62 | 0.35 | 0% [0, 0] | — (0.0%) | 0/338 | 0/338 |
| jev:1.14 | 338 | 71.9% [67, 77] | 0.47 | 0.71 | 0.08 | 1% [0, 2] | 66.7% (13.5%) | 0/338 | 0/338 |
| joey@openrouter | 338 | 73.4% [69, 78] | 0.29 | 0.70 | 0.06 | 1% [0, 2] | 66.7% (13.5%) | 0/338 | 0/338 |
| kev@openrouter | 338 | 72.8% [68, 77] | 0.04 | 0.63 | 0.02 | 2% [1, 4] | 100.0% (65.2%) | 0/338 | 0/338 |
| luna@decisions | 338 | 70.1% [65, 75] | 0.48 | 0.72 | 0.06 | 0% [0, 1] | 0.0% (0.0%) | 0/338 | 0/338 |
| mammoth@openrouter | 338 | 69.2% [64, 75] | 0.49 | 0.74 | 0.05 | 7% [4, 11] | 84.0% (67.0%) | 0/338 | 0/338 |
| mercury@openrouter | 338 | 73.7% [69, 78] | 0.39 | 0.70 | 0.16 | 3% [1, 4] | 55.6% (25.1%) | 0/338 | 0/338 |
| span@openrouter | 338 | 74.9% [70, 79] | 0.38 | 0.70 | 0.19 | 8% [5, 11] | 88.9% (73.7%) | 0/338 | 0/338 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.5-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-5.5; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 1, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| drex-max@openrouter = | 9% [6, 12] | 0.249 [0.204, 0.296] | 0.96 | met |
| decider@openrouter = | 16% [12, 19] | 0.251 [0.204, 0.299] | 0.93 | met |
| clef@openrouter = | 10% [7, 13] | 0.296 [0.249, 0.346] | 0.96 | met |
| span@openrouter | 8% [5, 11] | 0.251 [0.207, 0.305] | 1.00 | met |
| mammoth@openrouter | 7% [4, 11] | 0.308 [0.254, 0.358] | 0.87 | met |
| d1-ultra@openrouter | 6% [3, 8] | 0.290 [0.240, 0.343] | 0.93 | met |
| decider-flash@openrouter | 5% [3, 7] | 0.263 [0.216, 0.311] | 0.92 | met |
| elephant@openrouter | 4% [2, 6] | 0.272 [0.228, 0.322] | — | met |
| d1@vercel | 3% [1, 5] | 0.275 [0.228, 0.322] | 1.00 | met |
| mercury@openrouter | 3% [1, 4] | 0.263 [0.219, 0.311] | 1.00 | met |
| clef-flash@openrouter | 3% [1, 4] | 0.266 [0.222, 0.317] | 0.96 | met |
| d1.1@openrouter | 3% [1, 4] | 0.311 [0.260, 0.358] | 0.99 | met |
| kev@openrouter | 2% [1, 4] | 0.272 [0.228, 0.320] | 0.87 | met |
| joey@openrouter | 1% [0, 2] | 0.266 [0.219, 0.314] | 0.89 | met |
| jev:1.14 | 1% [0, 2] | 0.281 [0.231, 0.328] | 0.85 | met |
| luna@decisions | 0% [0, 1] | 0.299 [0.249, 0.352] | 0.93 | met |
| decision-1@openrouter | 0% [0, 1] | 0.402 [0.355, 0.456] | — | met |
| flash-lite@vercel | 0% [0, 0] | 0.272 [0.225, 0.320] | — | met |
| haiku@vercel | 0% [0, 0] | 0.352 [0.302, 0.405] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 338 | 415 ms | 568 ms | 883 ms | 1177 ms | 2.1 | 0 | 8 | $0.14 | billed |  |
| clef@openrouter | 338 | 1520 ms | 2340 ms | 5766 ms | 8420 ms | 3.8 | 0 | 8 | $1.38 | billed |  |
| d1-ultra@openrouter | 338 | 1334 ms | 2197 ms | 5874 ms | 11584 ms | 4.4 | 0 | 8 | $0.25 | billed |  |
| d1.1@openrouter | 338 | 1238 ms | 2103 ms | 4911 ms | 6537 ms | 4.0 | 0 | 8 | $0.12 | billed |  |
| d1@vercel | 338 | 222 ms | 326 ms | 561 ms | 6841 ms | 2.5 | 0 | 8 | $0.12 | billed | ○ |
| decider-flash@openrouter | 338 | 1244 ms | 2424 ms | 5318 ms | 5692 ms | 4.3 | 0 | 8 | $0.06 | billed | ○ |
| decider@openrouter | 338 | 1344 ms | 2174 ms | 5241 ms | 8593 ms | 3.9 | 0 | 8 | $0.12 | billed | ○ |
| decision-1@openrouter | 338 | 1414 ms | 2063 ms | 4324 ms | 6270 ms | 3.1 | 0 | 8 | $0.23 | billed |  |
| drex-max@openrouter | 338 | 1476 ms | 2318 ms | 4268 ms | 4862 ms | 2.9 | 3 | 8 | $0.36 | billed | ○ |
| elephant@openrouter | 338 | 1278 ms | 2236 ms | 5417 ms | 8499 ms | 4.2 | 0 | 8 | $0.21 | billed |  |
| flash-lite@vercel | 338 | 1196 ms | 1792 ms | 3885 ms | 11362 ms | 3.2 | 0 | 8 | $2.40 | estimated |  |
| haiku@vercel | 338 | 1365 ms | 2540 ms | 4767 ms | 10319 ms | 3.5 | 0 | 8 | $1.44 | estimated |  |
| jev:1.14 | 338 | 1242 ms | 2138 ms | 5313 ms | 8237 ms | 4.3 | 0 | 8 | $0.35 | estimated |  |
| joey@openrouter | 338 | 1290 ms | 2204 ms | 4297 ms | 6120 ms | 3.3 | 0 | 8 | $0.06 | billed | ○ |
| kev@openrouter | 338 | 1478 ms | 2355 ms | 5714 ms | 8313 ms | 3.9 | 0 | 8 | $0.22 | billed |  |
| luna@decisions | 338 | 1434 ms | 2195 ms | 4814 ms | 8412 ms | 3.4 | 1 | 8 | $0.69 | estimated |  |
| mammoth@openrouter | 338 | 1381 ms | 2322 ms | 4544 ms | 5898 ms | 3.3 | 0 | 8 | $0.61 | billed |  |
| mercury@openrouter | 338 | 1454 ms | 2267 ms | 3891 ms | 6817 ms | 2.7 | 0 | 8 | $0.11 | billed | ○ |
| span@openrouter | 338 | 1598 ms | 2286 ms | 4077 ms | 5700 ms | 2.6 | 0 | 8 | $0.07 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): flash-lite@vercel, haiku@vercel, jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0047 | 18 s (estimated, 338 calls) | 9 min | 8 |
| clef@openrouter | $0.05 | 68 s (estimated, 338 calls) | 34 min | 8 |
| d1-ultra@openrouter | $0.0083 | 67 s (estimated, 338 calls) | 33 min | 8 |
| d1.1@openrouter | $0.0040 | 60 s (estimated, 338 calls) | 30 min | 8 |
| d1@vercel | $0.0040 | 12 s (estimated, 338 calls) | 6 min | 8 |
| decider-flash@openrouter | $0.0020 | 64 s (estimated, 338 calls) | 31 min | 8 |
| decider@openrouter | $0.0041 | 65 s (estimated, 338 calls) | 32 min | 8 |
| decision-1@openrouter | $0.0077 | 65 s (estimated, 338 calls) | 32 min | 8 |
| drex-max@openrouter | $0.01 | 67 s (estimated, 338 calls) | 33 min | 8 |
| elephant@openrouter | $0.0072 | 64 s (estimated, 338 calls) | 32 min | 8 |
| flash-lite@vercel | $0.08 | 57 s (estimated, 338 calls) | 28 min | 8 |
| haiku@vercel | $0.05 | 69 s (estimated, 338 calls) | 34 min | 8 |
| jev:1.14 | $0.01 | 62 s (estimated, 338 calls) | 31 min | 8 |
| joey@openrouter | $0.0021 | 64 s (estimated, 338 calls) | 31 min | 8 |
| kev@openrouter | $0.0074 | 69 s (estimated, 338 calls) | 34 min | 8 |
| luna@decisions | $0.02 | 65 s (estimated, 338 calls) | 32 min | 8 |
| mammoth@openrouter | $0.02 | 65 s (estimated, 338 calls) | 32 min | 8 |
| mercury@openrouter | $0.0039 | 65 s (estimated, 338 calls) | 32 min | 8 |
| span@openrouter | $0.0023 | 69 s (estimated, 338 calls) | 34 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 73.4% | 74.3% | 75 | 12 | 0.40 | 0.40 |
| clef@openrouter | 70.4% | 74.0% | 73 | 15 | 0.80 | 0.80 |
| d1-ultra@openrouter | 71.0% | 72.2% | 73 | 21 | 0.80 | 0.80 |
| d1.1@openrouter | 68.9% | 72.5% | 78 | 15 | 0.85 | 0.85 |
| d1@vercel | 72.5% | 73.4% | 73 | 17 | 0.70 | 0.70 |
| decider-flash@openrouter | 73.7% | 74.0% | 79 | 9 | 0.40 | 0.35 |
| decider@openrouter | 74.9% | 76.3% | 71 | 9 | 0.55 | 0.55 |
| decision-1@openrouter | 59.8% | 76.3% | 59 | 21 | 0.85 | 0.85 |
| drex-max@openrouter | 75.1% | 75.4% | 65 | 18 | 0.60 | 0.60 |
| elephant@openrouter | 72.8% | 71.9% | 68 | 27 | 0.60 | 0.60 |
| flash-lite@vercel | 72.8% | 72.8% | 86 | 6 | 0.50 | 0.50 |
| haiku@vercel | 64.8% | 64.8% | 39 | 80 | 0.50 | 0.50 |
| jev:1.14 | 71.9% | 74.0% | 59 | 29 | 0.55 | 0.55 |
| joey@openrouter | 73.4% | 72.5% | 75 | 18 | 0.55 | 0.55 |
| kev@openrouter | 72.8% | 72.2% | 80 | 14 | 0.40 | 0.35 |
| luna@decisions | 70.1% | 75.4% | 65 | 18 | 0.75 | 0.75 |
| mammoth@openrouter | 69.2% | 72.5% | 76 | 17 | 0.75 | 0.70 |
| mercury@openrouter | 73.7% | 72.8% | 78 | 14 | 0.95 | 0.95 |
| span@openrouter | 74.9% | 74.3% | 67 | 20 | 0.50 | 0.50 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 28 (31%) | 102 (41%) |
| 0.20 | 65 (71%) | 33 (13%) |
| 0.30 | 68 (75%) | 16 (6%) |
| 0.40 | 75 (82%) | 6 (2%) |
| 0.50 | 85 (93%) | 5 (2%) |
| 0.60 | 86 (95%) | 2 (1%) |
| 0.70 | 89 (98%) | 2 (1%) |
| 0.80 | 90 (99%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 201 (81%) |
| 0.20 | 21 (23%) | 130 (53%) |
| 0.30 | 31 (34%) | 96 (39%) |
| 0.40 | 42 (46%) | 74 (30%) |
| 0.50 | 49 (54%) | 51 (21%) |
| 0.60 | 59 (65%) | 35 (14%) |
| 0.70 | 65 (71%) | 23 (9%) |
| 0.80 | 74 (81%) | 7 (3%) |
| 0.90 | 90 (99%) | 1 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 206 (83%) |
| 0.20 | 13 (14%) | 145 (59%) |
| 0.30 | 28 (31%) | 105 (43%) |
| 0.40 | 35 (38%) | 68 (28%) |
| 0.50 | 46 (51%) | 52 (21%) |
| 0.60 | 56 (62%) | 36 (15%) |
| 0.70 | 65 (71%) | 23 (9%) |
| 0.80 | 69 (76%) | 16 (6%) |
| 0.90 | 86 (95%) | 3 (1%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 7 (8%) | 168 (68%) |
| 0.20 | 19 (21%) | 121 (49%) |
| 0.30 | 29 (32%) | 79 (32%) |
| 0.40 | 39 (43%) | 63 (26%) |
| 0.50 | 49 (54%) | 56 (23%) |
| 0.60 | 61 (67%) | 40 (16%) |
| 0.70 | 65 (71%) | 32 (13%) |
| 0.80 | 69 (76%) | 19 (8%) |
| 0.85 | 71 (78%) | 16 (6%) |
| 0.90 | 78 (86%) | 10 (4%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (27%) | 99 (40%) |
| 0.20 | 40 (44%) | 67 (27%) |
| 0.30 | 50 (55%) | 46 (19%) |
| 0.40 | 58 (64%) | 35 (14%) |
| 0.50 | 65 (71%) | 28 (11%) |
| 0.60 | 72 (79%) | 20 (8%) |
| 0.70 | 72 (79%) | 14 (6%) |
| 0.80 | 80 (88%) | 10 (4%) |
| 0.90 | 85 (93%) | 6 (2%) |

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
| 0.20 | 6 (7%) | 187 (76%) |
| 0.30 | 17 (19%) | 154 (62%) |
| 0.40 | 23 (25%) | 126 (51%) |
| 0.50 | 31 (34%) | 105 (43%) |
| 0.60 | 41 (45%) | 79 (32%) |
| 0.70 | 47 (52%) | 56 (23%) |
| 0.80 | 57 (63%) | 34 (14%) |
| 0.85 | 59 (65%) | 21 (9%) |
| 0.90 | 72 (79%) | 15 (6%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 21 (23%) | 133 (54%) |
| 0.20 | 42 (46%) | 61 (25%) |
| 0.30 | 53 (58%) | 43 (17%) |
| 0.40 | 60 (66%) | 27 (11%) |
| 0.50 | 64 (70%) | 20 (8%) |
| 0.60 | 65 (71%) | 16 (6%) |
| 0.70 | 71 (78%) | 12 (5%) |
| 0.80 | 77 (85%) | 9 (4%) |
| 0.90 | 84 (92%) | 6 (2%) |

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

## Misses and false alarms by threshold (flash-lite@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 86 (95%) | 6 (2%) |
| 0.20 | 86 (95%) | 6 (2%) |
| 0.30 | 86 (95%) | 6 (2%) |
| 0.40 | 86 (95%) | 6 (2%) |
| 0.50 | 86 (95%) | 6 (2%) |
| 0.60 | 86 (95%) | 6 (2%) |
| 0.70 | 86 (95%) | 6 (2%) |
| 0.80 | 86 (95%) | 6 (2%) |
| 0.90 | 86 (95%) | 6 (2%) |

## Misses and false alarms by threshold (haiku@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 39 (43%) | 80 (32%) |
| 0.20 | 39 (43%) | 80 (32%) |
| 0.30 | 39 (43%) | 80 (32%) |
| 0.40 | 39 (43%) | 80 (32%) |
| 0.50 | 39 (43%) | 80 (32%) |
| 0.60 | 39 (43%) | 80 (32%) |
| 0.70 | 39 (43%) | 80 (32%) |
| 0.80 | 39 (43%) | 80 (32%) |
| 0.90 | 39 (43%) | 80 (32%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 1 (1%) | 238 (96%) |
| 0.30 | 6 (7%) | 174 (70%) |
| 0.40 | 27 (30%) | 96 (39%) |
| 0.50 | 49 (54%) | 46 (19%) |
| 0.55 | 52 (57%) | 31 (13%) |
| 0.60 | 63 (69%) | 27 (11%) |
| 0.70 | 79 (87%) | 11 (4%) |
| 0.80 | 89 (98%) | 1 (0%) |
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
| 0.20 | 15 (16%) | 173 (70%) |
| 0.30 | 57 (63%) | 51 (21%) |
| 0.35 | 71 (78%) | 18 (7%) |
| 0.40 | 83 (91%) | 7 (3%) |
| 0.50 | 89 (98%) | 3 (1%) |
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
| 0.10 | 33 (36%) | 88 (36%) |
| 0.20 | 46 (51%) | 56 (23%) |
| 0.30 | 56 (62%) | 41 (17%) |
| 0.40 | 58 (64%) | 31 (13%) |
| 0.50 | 63 (69%) | 26 (11%) |
| 0.60 | 68 (75%) | 22 (9%) |
| 0.70 | 72 (79%) | 20 (8%) |
| 0.80 | 76 (84%) | 15 (6%) |
| 0.90 | 78 (86%) | 11 (4%) |
| 0.95 | 82 (90%) | 4 (2%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 50 (55%) | 52 (21%) |
| 0.20 | 57 (63%) | 36 (15%) |
| 0.30 | 61 (67%) | 29 (12%) |
| 0.40 | 63 (69%) | 28 (11%) |
| 0.50 | 65 (71%) | 20 (8%) |
| 0.60 | 71 (78%) | 17 (7%) |
| 0.70 | 76 (84%) | 15 (6%) |
| 0.80 | 80 (88%) | 11 (4%) |
| 0.90 | 86 (95%) | 5 (2%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (28)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29377 | True | False | 0.96 | fix(core): update auth error documentation link to valid anchor and a… |
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #28940 | True | False | 0.95 | fix(a2a-server): clear stale cancellation error on new message turns |
| #27698 | True | False | 0.94 | fix(core): Ensure zero-quota limits fail fast to prevent retry loop h… |
| #27467 | True | False | 0.94 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #27391 | True | False | 0.94 | fix(cli): filter internal session context from history during resumpt… |
| #28216 | True | False | 0.94 | Refactor: exclude transient CI configuration files from workspace con… |

**clef@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |

**d1-ultra@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.95 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.93 | Fix bulk of remaining issues with generalist profile |
| #29170 | False | True | 0.93 | fix(core): enhance workspace path boundary checks and symlink resolut… |
| #28470 | False | True | 0.92 | fix(a2a-server): enforce workspace trust and task isolation to preven… |

**d1.1@openrouter** (17)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 0.99 | fix(ui): clamped table column widths |
| #26073 | False | True | 0.97 | Fix bulk of remaining issues with generalist profile |
| #29115 | False | True | 0.97 | fix(config): enforce strict permission and ownership checks on system… |
| #26270 | True | False | 0.96 | feat(ui): added microphone and updated placeholder for voice mode |
| #29170 | False | True | 0.96 | fix(core): enhance workspace path boundary checks and symlink resolut… |
| #26949 | True | False | 0.95 | fix(ci): configure git remote with token for authentication |
| #29185 | True | False | 0.95 | test(integration): deflake run_shell_command and file-system-interact… |

**d1@vercel** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29185 | True | False | 1.00 | test(integration): deflake run_shell_command and file-system-interact… |
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #29377 | True | False | 1.00 | fix(core): update auth error documentation link to valid anchor and a… |
| #26991 | True | False | 1.00 | fix(ui): clamped table column widths |
| #26270 | True | False | 0.99 | feat(ui): added microphone and updated placeholder for voice mode |
| #26949 | True | False | 0.99 | fix(ci): configure git remote with token for authentication |
| #28216 | True | False | 0.99 | Refactor: exclude transient CI configuration files from workspace con… |
| #25324 | True | False | 0.99 | fix(cli): prevent spam loop when preferredEditor is invalid |

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
| #28530 | False | True | 0.97 | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #26949 | True | False | 0.97 | fix(ci): configure git remote with token for authentication |
| #28470 | False | True | 0.95 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #26143 | False | True | 0.95 | refactor(acp): modularize monolithic acpClient into specialized files |

**drex-max@openrouter** (27)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.97 | fix(cli): add missing response key to custom theme text schema |
| #28470 | False | True | 0.97 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #25324 | True | False | 0.96 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #28216 | True | False | 0.96 | Refactor: exclude transient CI configuration files from workspace con… |
| #27253 | True | False | 0.95 | fix: robust ripgrep path resolution and 1p hermetic execution support |
| #26991 | True | False | 0.95 | fix(ui): clamped table column widths |
| #27619 | True | False | 0.95 | fix(core): implement atomic update in MCP tool discovery |
| #25827 | True | False | 0.95 | fix(cli): prevent duplicate SessionStart systemMessage render |

**elephant@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #28470 | False | True | 0.94 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #26073 | False | True | 0.92 | Fix bulk of remaining issues with generalist profile |
| #29185 | True | False | 0.90 | test(integration): deflake run_shell_command and file-system-interact… |

**flash-lite@vercel** (92)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29568 | True | False | 1.00 | fix(core): implement append-only delta patching and bounded history w… |
| #29539 | True | False | 1.00 | fix(core): enable autonomous plan execution in non-interactive mode |
| #29506 | True | False | 1.00 | fix(core): align policy redirection gates, path validation, and workf… |
| #29499 | True | False | 1.00 | fix(core): serialize file tool operations and make writes atomic (#29… |
| #29451 | True | False | 1.00 | fix(core): bound tool output size and optimize memory lifecycle in lo… |
| #29437 | True | False | 1.00 | fix(core): clean up temporary directory when background shell executi… |
| #29377 | True | False | 1.00 | fix(core): update auth error documentation link to valid anchor and a… |
| #29214 | True | False | 1.00 | fix(sandbox): harden filesystem boundaries and isolate runtime state |

**haiku@vercel** (119)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29539 | True | False | 1.00 | fix(core): enable autonomous plan execution in non-interactive mode |
| #29520 | False | True | 1.00 | fix(cli): preserve scroll position and partition pending height budget |
| #29487 | False | True | 1.00 | fix(cli): restore paused stdin after capability detection |
| #29450 | False | True | 1.00 | refactor(a2a-server): implement V1 to V2 settings migration logic |
| #29448 | False | True | 1.00 | fix(auth): prevent infinite auth loop from file contention, headless … |
| #29437 | True | False | 1.00 | fix(core): clean up temporary directory when background shell executi… |
| #29377 | True | False | 1.00 | fix(core): update auth error documentation link to valid anchor and a… |
| #29380 | False | True | 1.00 | fix(core,cli): improve terminal buffer memory management and format W… |

**luna@decisions** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26073 | False | True | 0.92 | Fix bulk of remaining issues with generalist profile |

**mammoth@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.93 | fix(cli): add missing response key to custom theme text schema |

**mercury@openrouter** (44)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #27467 | True | False | 0.99 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #26947 | True | False | 0.99 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #26073 | False | True | 0.99 | Fix bulk of remaining issues with generalist profile |
| #28470 | False | True | 0.99 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #28223 | True | False | 0.99 | fix(core-tools): bypass LLM correction for JSON and IPYNB files in wr… |
| #28216 | True | False | 0.99 | Refactor: exclude transient CI configuration files from workspace con… |
| #26270 | True | False | 0.98 | feat(ui): added microphone and updated placeholder for voice mode |

**span@openrouter** (55)

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


## Cases the models disagree on (12 of 211)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | flash-lite@vercel | haiku@vercel | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #29568 | True | False (0.65) | True (0.80) | True (0.88) | True (0.91) | True (0.91) | False (0.66) | True (0.71) | True (0.93) | True (0.89) | True (0.62) | False (1.00) | True (1.00) | True (0.70) | False (0.57) | False (0.66) | True (0.83) | True (0.80) | True (0.92) | True (0.92) | fix(core): implement append-only delta patching and bounded history w… |
| #29558 | False | False (0.90) | True (0.50) | False (0.67) | False (0.74) | False (0.94) | False (0.87) | False (0.87) | False (0.71) | False (0.90) | False (0.69) | False (1.00) | False (1.00) | False (0.67) | False (0.80) | False (0.79) | False (0.66) | False (0.63) | False (0.88) | False (0.93) | fix(cli): persist state atomically and recover from backup on corrupt… |
| #29539 | True | False (0.88) | False (0.82) | False (0.71) | True (0.50) | False (0.62) | False (0.83) | False (0.83) | False (0.75) | False (0.89) | False (0.84) | False (1.00) | False (1.00) | False (0.61) | False (0.54) | False (0.76) | False (0.66) | False (0.68) | False (0.97) | False (0.96) | fix(core): enable autonomous plan execution in non-interactive mode |
| #29520 | False | False (0.79) | True (0.57) | True (0.59) | True (0.75) | False (0.69) | False (0.73) | False (0.73) | False (0.62) | False (0.81) | True (0.50) | False (1.00) | True (1.00) | True (0.50) | True (0.67) | False (0.69) | True (0.70) | True (0.62) | False (0.88) | False (0.92) | fix(cli): preserve scroll position and partition pending height budget |
| #29506 | True | False (0.65) | True (0.84) | True (0.84) | True (0.95) | True (0.59) | False (0.63) | True (0.78) | True (0.93) | True (0.84) | True (0.63) | False (1.00) | True (1.00) | True (0.63) | True (0.66) | False (0.69) | True (0.76) | True (0.84) | False (0.59) | True (0.87) | fix(core): align policy redirection gates, path validation, and workf… |
| #29499 | True | False (0.71) | True (0.81) | True (0.86) | True (0.85) | True (0.58) | False (0.67) | False (0.69) | True (0.88) | False (0.61) | True (0.73) | False (1.00) | True (1.00) | True (0.60) | False (0.53) | False (0.72) | True (0.76) | True (0.71) | False (0.75) | True (0.54) | fix(core): serialize file tool operations and make writes atomic (#29… |
| #29487 | False | False (0.91) | False (0.54) | False (0.79) | False (0.67) | False (0.93) | False (0.78) | False (0.75) | False (0.62) | False (0.87) | False (0.79) | False (1.00) | True (1.00) | False (0.54) | False (0.58) | False (0.75) | False (0.65) | False (0.51) | False (0.93) | False (0.97) | fix(cli): restore paused stdin after capability detection |
| #29463 | False | False (0.90) | False (0.55) | False (0.66) | False (0.74) | False (0.74) | False (0.83) | False (0.87) | True (0.50) | False (0.94) | False (0.79) | False (1.00) | False (1.00) | False (0.62) | False (0.73) | False (0.77) | False (0.60) | False (0.70) | True (0.50) | False (0.89) | fix(acp): resolve session before config initialization and avoid same… |
| #29451 | True | False (0.61) | True (0.74) | True (0.91) | True (0.92) | True (0.85) | False (0.67) | True (0.55) | True (0.75) | True (0.75) | True (0.64) | False (1.00) | True (1.00) | True (0.66) | False (0.51) | False (0.68) | True (0.77) | True (0.79) | False (0.78) | False (0.52) | fix(core): bound tool output size and optimize memory lifecycle in lo… |
| #29450 | False | False (0.68) | True (0.79) | True (0.81) | True (0.92) | True (0.90) | False (0.68) | True (0.52) | True (0.91) | True (0.72) | True (0.53) | False (1.00) | True (1.00) | True (0.64) | True (0.68) | False (0.67) | True (0.80) | True (0.76) | True (0.92) | True (0.81) | refactor(a2a-server): implement V1 to V2 settings migration logic |
| #29446 | False | False (0.94) | False (0.88) | False (0.82) | False (0.92) | False (0.99) | False (0.89) | False (0.95) | False (0.87) | False (0.95) | False (0.94) | False (1.00) | False (1.00) | False (0.77) | False (0.83) | False (0.82) | False (0.71) | False (0.91) | True (0.50) | False (0.99) | fix(cli): distinguish missing MCP enablement config from malformed JS… |
| #29448 | False | False (0.64) | True (0.78) | True (0.85) | True (0.87) | True (0.53) | False (0.68) | False (0.61) | True (0.78) | False (0.62) | True (0.69) | False (1.00) | True (1.00) | True (0.61) | False (0.64) | False (0.71) | True (0.78) | True (0.76) | False (0.56) | False (0.68) | fix(auth): prevent infinite auth loop from file contention, headless … |
