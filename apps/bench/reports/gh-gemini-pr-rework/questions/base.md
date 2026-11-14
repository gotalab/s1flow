# gh-gemini-pr-rework

2026-11-12 · 338 labelled dev cases (False 247, True 91) · split: stratified k-fold (no test case among these: CV numbers only) · source: Merged PRs of google-gemini/gemini-cli (review history via the GitHub API)

**clef-omni@openrouter** has the highest coverage at 95% accuracy, 19% [14, 23] (API cost $0.95 per 10k, p99 353ms). Its interval overlaps with decider@openrouter, drex-max@openrouter, d1-ultra@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is clef-omni@openrouter's, 76% [72, 80].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 338 | 73.4% [69, 78] | 0.12 | 0.69 | 0.13 | 0% [0, 0] | — (0.0%) | 0/338 | 0/338 |
| clef-omni@openrouter | 338 | 76.3% [72, 80] | 0.31 | 0.71 | 0.13 | 19% [14, 23] | 93.7% (86.1%) | 0/338 | 0/338 |
| clef@openrouter | 338 | 70.1% [65, 75] | 0.45 | 0.70 | 0.07 | 6% [4, 9] | 85.7% (67.1%) | 0/338 | 0/338 |
| d1-ultra@openrouter | 338 | 73.1% [68, 78] | 0.47 | 0.71 | 0.08 | 17% [14, 22] | 93.2% (85.2%) | 0/338 | 0/338 |
| d1.1@openrouter | 338 | 70.4% [65, 75] | 0.43 | 0.70 | 0.12 | 5% [3, 7] | 75.0% (51.6%) | 0/338 | 0/338 |
| d1@vercel | 338 | 71.6% [66, 76] | 0.40 | 0.69 | 0.14 | 10% [7, 14] | 94.3% (83.1%) | 0/338 | 0/338 |
| decider-flash@openrouter | 338 | 73.7% [69, 78] | 0.08 | 0.68 | 0.07 | 4% [2, 6] | 84.6% (59.0%) | 0/338 | 0/338 |
| decider@openrouter | 338 | 74.9% [70, 79] | 0.27 | 0.70 | 0.09 | 13% [9, 17] | 88.6% (77.6%) | 0/338 | 0/338 |
| decision-1@openrouter | 338 | 61.5% [56, 66] | 0.48 | 0.69 | 0.15 | 0% [0, 0] | — (0.0%) | 0/338 | 0/338 |
| drex-max@openrouter | 338 | 74.6% [70, 79] | 0.38 | 0.69 | 0.12 | 14% [11, 18] | 91.8% (82.3%) | 0/338 | 0/338 |
| elephant@openrouter | 338 | 72.5% [68, 77] | 0.44 | 0.69 | 0.06 | 1% [0, 3] | 80.0% (34.3%) | 0/338 | 0/338 |
| gemini-decision@google | 338 | 71.6% [67, 76] | 0.48 | 0.68 | 0.05 | 1% [0, 2] | 66.7% (13.5%) | 0/338 | 0/338 |
| jev:1.14 | 338 | 71.6% [67, 76] | 0.45 | 0.71 | 0.07 | 2% [1, 3] | 83.3% (41.8%) | 0/338 | 0/338 |
| joey@openrouter | 338 | 74.0% [70, 79] | 0.27 | 0.70 | 0.04 | 1% [0, 3] | 75.0% (24.9%) | 0/338 | 0/338 |
| kev@openrouter | 338 | 73.4% [68, 78] | 0.06 | 0.64 | 0.01 | 2% [1, 3] | 100.0% (60.7%) | 0/338 | 0/338 |
| luna@decisions | 338 | 69.2% [64, 74] | 0.47 | 0.70 | 0.04 | 1% [0, 1] | 50.0% (2.5%) | 0/338 | 0/338 |
| mammoth@openrouter | 338 | 70.4% [65, 75] | 0.50 | 0.73 | 0.04 | 7% [4, 9] | 82.6% (64.5%) | 0/338 | 0/338 |
| reflex@openrouter | 338 | 74.9% [70, 80] | 0.37 | 0.73 | 0.14 | 4% [2, 7] | 85.7% (61.5%) | 0/338 | 0/338 |
| span@openrouter | 338 | 74.6% [70, 79] | 0.33 | 0.70 | 0.18 | 4% [2, 6] | 84.6% (59.0%) | 0/338 | 0/338 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 1, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| clef-omni@openrouter = | 19% [14, 23] | 0.237 [0.195, 0.284] | 0.96 | met |
| decider@openrouter = | 13% [9, 17] | 0.251 [0.207, 0.299] | 0.95 | met |
| drex-max@openrouter = | 14% [11, 18] | 0.254 [0.210, 0.299] | 0.96 | met |
| d1-ultra@openrouter = | 17% [14, 22] | 0.269 [0.222, 0.320] | 0.92 | met |
| d1@vercel | 10% [7, 14] | 0.284 [0.237, 0.337] | 0.99 | met |
| mammoth@openrouter | 7% [4, 9] | 0.296 [0.248, 0.349] | — | met |
| clef@openrouter | 6% [4, 9] | 0.299 [0.254, 0.349] | 0.96 | met |
| d1.1@openrouter | 5% [3, 7] | 0.296 [0.246, 0.349] | 0.99 | met |
| reflex@openrouter | 4% [2, 7] | 0.251 [0.204, 0.299] | 1.00 | met |
| span@openrouter | 4% [2, 6] | 0.254 [0.210, 0.305] | 1.00 | met |
| decider-flash@openrouter | 4% [2, 6] | 0.263 [0.216, 0.311] | 0.93 | met |
| kev@openrouter | 2% [1, 3] | 0.266 [0.219, 0.317] | 0.86 | met |
| jev:1.14 | 2% [1, 3] | 0.284 [0.237, 0.331] | 0.83 | met |
| elephant@openrouter | 1% [0, 3] | 0.275 [0.228, 0.322] | — | met |
| joey@openrouter | 1% [0, 3] | 0.260 [0.213, 0.305] | 0.88 | met |
| gemini-decision@google | 1% [0, 2] | 0.284 [0.237, 0.331] | — | met |
| luna@decisions | 1% [0, 1] | 0.308 [0.257, 0.358] | 0.93 | met |
| clef-flash@openrouter | 0% [0, 0] | 0.266 [0.219, 0.314] | 0.96 | met |
| decision-1@openrouter | 0% [0, 0] | 0.385 [0.337, 0.438] | 0.99 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 338 | 240 ms | 393 ms | 944 ms | 1951 ms | 3.9 | 0 | 4 | $0.16 | billed |  |
| clef-omni@openrouter | 338 | 198 ms | 251 ms | 353 ms | 5266 ms | 1.8 | 0 | 4 | $0.95 | billed | ○ |
| clef@openrouter | 338 | 557 ms | 2445 ms | 5652 ms | 6508 ms | 10.2 | 0 | 4 | $1.40 | billed |  |
| d1-ultra@openrouter | 338 | 472 ms | 879 ms | 1294 ms | 2063 ms | 2.7 | 0 | 4 | $0.25 | billed | ○ |
| d1.1@openrouter | 338 | 211 ms | 357 ms | 545 ms | 940 ms | 2.6 | 9 | 4 | $0.12 | billed | ○ |
| d1@vercel | 338 | 498 ms | 842 ms | 1557 ms | 4540 ms | 3.1 | 0 | 4 | $0.12 | billed | ○ |
| decider-flash@openrouter | 338 | 148 ms | 260 ms | 362 ms | 1432 ms | 2.4 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 338 | 342 ms | 580 ms | 1299 ms | 1656 ms | 3.8 | 1 | 4 | $0.12 | billed | ○ |
| decision-1@openrouter | 338 | 250 ms | 333 ms | 473 ms | 1177 ms | 1.9 | 0 | 4 | $0.23 | billed |  |
| drex-max@openrouter | 338 | 217 ms | 358 ms | 975 ms | 1233 ms | 4.5 | 0 | 4 | $0.36 | billed | ○ |
| elephant@openrouter | 338 | 170 ms | 286 ms | 362 ms | 521 ms | 2.1 | 0 | 4 | $0.21 | billed |  |
| gemini-decision@google | 338 | 230 ms | 384 ms | 688 ms | 780 ms | 3.0 | 0 | 4 | $0.72 | estimated |  |
| jev:1.14 | 338 | 113 ms | 226 ms | 254 ms | 453 ms | 2.2 | 0 | 4 | $0.35 | estimated | ○ |
| joey@openrouter | 338 | 182 ms | 303 ms | 440 ms | 2180 ms | 2.4 | 0 | 4 | $0.06 | billed |  |
| kev@openrouter | 338 | 408 ms | 466 ms | 812 ms | 985 ms | 2.0 | 0 | 4 | $0.22 | billed |  |
| luna@decisions | 338 | 223 ms | 455 ms | 672 ms | 719 ms | 3.0 | 0 | 4 | $0.69 | estimated |  |
| mammoth@openrouter | 338 | 186 ms | 298 ms | 381 ms | 463 ms | 2.0 | 0 | 4 | $0.61 | billed | ○ |
| reflex@openrouter | 338 | 266 ms | 302 ms | 365 ms | 522 ms | 1.4 | 0 | 4 | $0.26 | billed | ○ |
| span@openrouter | 338 | 300 ms | 852 ms | 953 ms | 999 ms | 3.2 | 0 | 4 | $0.07 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0054 | 25 s (estimated, 338 calls) | 12 min | 4 |
| clef-omni@openrouter | $0.03 | 19 s (estimated, 338 calls) | 9 min | 4 |
| clef@openrouter | $0.05 | 81 s (estimated, 338 calls) | 40 min | 4 |
| d1-ultra@openrouter | $0.0083 | 45 s (estimated, 338 calls) | 22 min | 4 |
| d1.1@openrouter | $0.0040 | 20 s (estimated, 338 calls) | 10 min | 4 |
| d1@vercel | $0.0040 | 48 s (estimated, 338 calls) | 23 min | 4 |
| decider-flash@openrouter | $0.0020 | 15 s (estimated, 338 calls) | 8 min | 4 |
| decider@openrouter | $0.0041 | 32 s (estimated, 338 calls) | 16 min | 4 |
| decision-1@openrouter | $0.0077 | 23 s (estimated, 338 calls) | 11 min | 4 |
| drex-max@openrouter | $0.01 | 22 s (estimated, 338 calls) | 11 min | 4 |
| elephant@openrouter | $0.0072 | 16 s (estimated, 338 calls) | 8 min | 4 |
| gemini-decision@google | $0.02 | 22 s (estimated, 338 calls) | 11 min | 4 |
| jev:1.14 | $0.01 | 12 s (estimated, 338 calls) | 6 min | 4 |
| joey@openrouter | $0.0021 | 18 s (estimated, 338 calls) | 9 min | 4 |
| kev@openrouter | $0.0074 | 36 s (estimated, 338 calls) | 18 min | 4 |
| luna@decisions | $0.02 | 23 s (estimated, 338 calls) | 12 min | 4 |
| mammoth@openrouter | $0.02 | 17 s (estimated, 338 calls) | 8 min | 4 |
| reflex@openrouter | $0.0086 | 23 s (estimated, 338 calls) | 11 min | 4 |
| span@openrouter | $0.0023 | 34 s (estimated, 338 calls) | 17 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 73.4% | 75.7% | 71 | 11 | 0.35 | 0.35 |
| clef-omni@openrouter | 76.3% | 76.3% | 73 | 7 | 0.50 | 0.50 |
| clef@openrouter | 70.1% | 74.9% | 73 | 12 | 0.80 | 0.80 |
| d1-ultra@openrouter | 73.1% | 72.5% | 73 | 20 | 0.75 | 0.75 |
| d1.1@openrouter | 70.4% | 74.9% | 70 | 15 | 0.85 | 0.85 |
| d1@vercel | 71.6% | 75.4% | 71 | 12 | 0.80 | 0.80 |
| decider-flash@openrouter | 73.7% | 72.5% | 86 | 7 | 0.55 | 0.55 |
| decider@openrouter | 74.9% | 74.6% | 75 | 11 | 0.45 | 0.45 |
| decision-1@openrouter | 61.5% | 74.6% | 64 | 22 | 0.90 | 0.85 |
| drex-max@openrouter | 74.6% | 73.4% | 74 | 16 | 0.60 | 0.60 |
| elephant@openrouter | 72.5% | 71.9% | 71 | 24 | 0.60 | 0.65 |
| gemini-decision@google | 71.6% | 73.7% | 77 | 12 | 0.75 | 0.75 |
| jev:1.14 | 71.6% | 72.2% | 67 | 27 | 0.65 | 0.70 |
| joey@openrouter | 74.0% | 73.7% | 80 | 9 | 0.55 | 0.55 |
| kev@openrouter | 73.4% | 73.4% | 76 | 14 | 0.35 | 0.35 |
| luna@decisions | 69.2% | 74.9% | 64 | 21 | 0.75 | 0.75 |
| mammoth@openrouter | 70.4% | 74.9% | 69 | 16 | 0.75 | 0.75 |
| reflex@openrouter | 74.9% | 75.4% | 71 | 12 | 0.70 | 0.70 |
| span@openrouter | 74.6% | 75.1% | 68 | 16 | 0.45 | 0.45 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (29%) | 104 (42%) |
| 0.20 | 65 (71%) | 33 (13%) |
| 0.30 | 68 (75%) | 18 (7%) |
| 0.35 | 71 (78%) | 11 (4%) |
| 0.40 | 77 (85%) | 7 (3%) |
| 0.50 | 85 (93%) | 5 (2%) |
| 0.60 | 86 (95%) | 2 (1%) |
| 0.70 | 90 (99%) | 2 (1%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef-omni@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 33 (36%) | 95 (38%) |
| 0.20 | 53 (58%) | 44 (18%) |
| 0.30 | 65 (71%) | 25 (10%) |
| 0.40 | 68 (75%) | 15 (6%) |
| 0.50 | 73 (80%) | 7 (3%) |
| 0.60 | 82 (90%) | 6 (2%) |
| 0.70 | 84 (92%) | 3 (1%) |
| 0.80 | 88 (97%) | 1 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (3%) | 199 (81%) |
| 0.20 | 19 (21%) | 129 (52%) |
| 0.30 | 35 (38%) | 94 (38%) |
| 0.40 | 45 (49%) | 69 (28%) |
| 0.50 | 50 (55%) | 51 (21%) |
| 0.60 | 57 (63%) | 36 (15%) |
| 0.70 | 64 (70%) | 22 (9%) |
| 0.80 | 73 (80%) | 9 (4%) |
| 0.90 | 90 (99%) | 1 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 6 (7%) | 178 (72%) |
| 0.20 | 23 (25%) | 126 (51%) |
| 0.30 | 35 (38%) | 80 (32%) |
| 0.40 | 46 (51%) | 56 (23%) |
| 0.50 | 51 (56%) | 40 (16%) |
| 0.60 | 58 (64%) | 32 (13%) |
| 0.70 | 65 (71%) | 21 (9%) |
| 0.75 | 70 (77%) | 14 (6%) |
| 0.80 | 71 (78%) | 13 (5%) |
| 0.90 | 82 (90%) | 2 (1%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 13 (14%) | 166 (67%) |
| 0.20 | 21 (23%) | 115 (47%) |
| 0.30 | 31 (34%) | 78 (32%) |
| 0.40 | 46 (51%) | 52 (21%) |
| 0.50 | 53 (58%) | 47 (19%) |
| 0.60 | 61 (67%) | 39 (16%) |
| 0.70 | 67 (74%) | 31 (13%) |
| 0.80 | 68 (75%) | 20 (8%) |
| 0.85 | 70 (77%) | 15 (6%) |
| 0.90 | 78 (86%) | 11 (4%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 22 (24%) | 118 (48%) |
| 0.20 | 35 (38%) | 83 (34%) |
| 0.30 | 47 (52%) | 57 (23%) |
| 0.40 | 53 (58%) | 46 (19%) |
| 0.50 | 59 (65%) | 37 (15%) |
| 0.60 | 68 (75%) | 22 (9%) |
| 0.70 | 68 (75%) | 19 (8%) |
| 0.80 | 71 (78%) | 12 (5%) |
| 0.90 | 81 (89%) | 8 (3%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (3%) | 223 (90%) |
| 0.20 | 41 (45%) | 71 (29%) |
| 0.30 | 67 (74%) | 22 (9%) |
| 0.40 | 81 (89%) | 8 (3%) |
| 0.50 | 87 (96%) | 2 (1%) |
| 0.55 | 87 (96%) | 1 (0%) |
| 0.60 | 87 (96%) | 1 (0%) |
| 0.70 | 91 (100%) | 0 (0%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 14 (15%) | 142 (57%) |
| 0.20 | 45 (49%) | 56 (23%) |
| 0.30 | 62 (68%) | 28 (11%) |
| 0.40 | 68 (75%) | 17 (7%) |
| 0.45 | 72 (79%) | 12 (5%) |
| 0.50 | 75 (82%) | 10 (4%) |
| 0.60 | 80 (88%) | 5 (2%) |
| 0.70 | 85 (93%) | 2 (1%) |
| 0.80 | 91 (100%) | 1 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 206 (83%) |
| 0.20 | 11 (12%) | 182 (74%) |
| 0.30 | 21 (23%) | 142 (57%) |
| 0.40 | 25 (27%) | 122 (49%) |
| 0.50 | 31 (34%) | 99 (40%) |
| 0.60 | 38 (42%) | 69 (28%) |
| 0.70 | 48 (53%) | 55 (22%) |
| 0.80 | 54 (59%) | 36 (15%) |
| 0.85 | 59 (65%) | 24 (10%) |
| 0.90 | 66 (73%) | 17 (7%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 29 (32%) | 113 (46%) |
| 0.20 | 46 (51%) | 47 (19%) |
| 0.30 | 57 (63%) | 31 (13%) |
| 0.40 | 62 (68%) | 27 (11%) |
| 0.50 | 65 (71%) | 21 (9%) |
| 0.60 | 68 (75%) | 15 (6%) |
| 0.70 | 73 (80%) | 13 (5%) |
| 0.80 | 78 (86%) | 7 (3%) |
| 0.90 | 85 (93%) | 3 (1%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 228 (92%) |
| 0.20 | 14 (15%) | 155 (63%) |
| 0.30 | 34 (37%) | 104 (42%) |
| 0.40 | 43 (47%) | 65 (26%) |
| 0.50 | 54 (59%) | 39 (16%) |
| 0.60 | 63 (69%) | 26 (11%) |
| 0.65 | 67 (74%) | 21 (9%) |
| 0.70 | 73 (80%) | 17 (7%) |
| 0.80 | 81 (89%) | 9 (4%) |
| 0.90 | 89 (98%) | 1 (0%) |

## Misses and false alarms by threshold (gemini-decision@google)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 245 (99%) |
| 0.20 | 5 (5%) | 204 (83%) |
| 0.30 | 23 (25%) | 142 (57%) |
| 0.40 | 34 (37%) | 86 (35%) |
| 0.50 | 47 (52%) | 49 (20%) |
| 0.60 | 60 (66%) | 30 (12%) |
| 0.70 | 70 (77%) | 16 (6%) |
| 0.75 | 74 (81%) | 10 (4%) |
| 0.80 | 80 (88%) | 5 (2%) |
| 0.90 | 90 (99%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 1 (1%) | 240 (97%) |
| 0.30 | 6 (7%) | 177 (72%) |
| 0.40 | 29 (32%) | 96 (39%) |
| 0.50 | 51 (56%) | 45 (18%) |
| 0.60 | 61 (67%) | 24 (10%) |
| 0.70 | 78 (86%) | 6 (2%) |
| 0.80 | 89 (98%) | 2 (1%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 246 (100%) |
| 0.20 | 6 (7%) | 196 (79%) |
| 0.30 | 27 (30%) | 96 (39%) |
| 0.40 | 57 (63%) | 36 (15%) |
| 0.50 | 75 (82%) | 13 (5%) |
| 0.55 | 80 (88%) | 6 (2%) |
| 0.60 | 84 (92%) | 5 (2%) |
| 0.70 | 88 (97%) | 2 (1%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 14 (15%) | 175 (71%) |
| 0.30 | 58 (64%) | 46 (19%) |
| 0.35 | 71 (78%) | 14 (6%) |
| 0.40 | 81 (89%) | 7 (3%) |
| 0.50 | 88 (97%) | 2 (1%) |
| 0.60 | 90 (99%) | 0 (0%) |
| 0.70 | 91 (100%) | 0 (0%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 2 (2%) | 231 (94%) |
| 0.30 | 16 (18%) | 139 (56%) |
| 0.40 | 41 (45%) | 74 (30%) |
| 0.50 | 45 (49%) | 59 (24%) |
| 0.60 | 49 (54%) | 43 (17%) |
| 0.70 | 60 (66%) | 23 (9%) |
| 0.75 | 65 (71%) | 16 (6%) |
| 0.80 | 78 (86%) | 8 (3%) |
| 0.90 | 86 (95%) | 1 (0%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 234 (95%) |
| 0.20 | 5 (5%) | 165 (67%) |
| 0.30 | 19 (21%) | 119 (48%) |
| 0.40 | 29 (32%) | 82 (33%) |
| 0.50 | 41 (45%) | 59 (24%) |
| 0.60 | 51 (56%) | 43 (17%) |
| 0.70 | 64 (70%) | 19 (8%) |
| 0.75 | 70 (77%) | 12 (5%) |
| 0.80 | 77 (85%) | 7 (3%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (reflex@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 34 (37%) | 81 (33%) |
| 0.20 | 46 (51%) | 42 (17%) |
| 0.30 | 55 (60%) | 31 (13%) |
| 0.40 | 60 (66%) | 27 (11%) |
| 0.50 | 66 (73%) | 19 (8%) |
| 0.60 | 68 (75%) | 13 (5%) |
| 0.70 | 71 (78%) | 9 (4%) |
| 0.80 | 74 (81%) | 7 (3%) |
| 0.90 | 83 (91%) | 3 (1%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 51 (56%) | 41 (17%) |
| 0.20 | 62 (68%) | 27 (11%) |
| 0.30 | 65 (71%) | 23 (9%) |
| 0.40 | 67 (74%) | 20 (8%) |
| 0.45 | 68 (75%) | 16 (6%) |
| 0.50 | 70 (77%) | 16 (6%) |
| 0.60 | 72 (79%) | 13 (5%) |
| 0.70 | 76 (84%) | 12 (5%) |
| 0.80 | 82 (90%) | 8 (3%) |
| 0.90 | 85 (93%) | 2 (1%) |

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

**clef-omni@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28216 | True | False | 0.97 | Refactor: exclude transient CI configuration files from workspace con… |
| #25822 | True | False | 0.97 | fix(cli): add missing response key to custom theme text schema |
| #27391 | True | False | 0.96 | fix(cli): filter internal session context from history during resumpt… |
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #25324 | True | False | 0.96 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #29377 | True | False | 0.96 | fix(core): update auth error documentation link to valid anchor and a… |
| #27467 | True | False | 0.95 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #25670 | True | False | 0.95 | fix(core): remove duplicate initialize call on agents refreshed |

**clef@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26949 | True | False | 0.91 | fix(ci): configure git remote with token for authentication |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |

**d1-ultra@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.95 | fix(cli): add missing response key to custom theme text schema |
| #25324 | True | False | 0.93 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #29185 | True | False | 0.92 | test(integration): deflake run_shell_command and file-system-interact… |
| #26991 | True | False | 0.91 | fix(ui): clamped table column widths |
| #25827 | True | False | 0.91 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #27467 | True | False | 0.91 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #27345 | False | True | 0.91 | feat(context): Complete simplification work. |
| #28470 | False | True | 0.91 | fix(a2a-server): enforce workspace trust and task isolation to preven… |

**d1.1@openrouter** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.98 | Fix bulk of remaining issues with generalist profile |
| #28470 | False | True | 0.97 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #26991 | True | False | 0.97 | fix(ui): clamped table column widths |
| #26270 | True | False | 0.97 | feat(ui): added microphone and updated placeholder for voice mode |
| #29115 | False | True | 0.96 | fix(config): enforce strict permission and ownership checks on system… |
| #28053 | False | True | 0.95 | fix(core-tools): resolve defensive path resolution for at-reference f… |
| #25716 | False | True | 0.95 | refactor(memory): replace MemoryManagerAgent with prompt-driven memor… |

**d1@vercel** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26270 | True | False | 0.99 | feat(ui): added microphone and updated placeholder for voice mode |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.99 | Fix bulk of remaining issues with generalist profile |
| #26947 | True | False | 0.99 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #25324 | True | False | 0.99 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #28216 | True | False | 0.98 | Refactor: exclude transient CI configuration files from workspace con… |
| #26991 | True | False | 0.98 | fix(ui): clamped table column widths |

**decider-flash@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.93 | fix(cli): add missing response key to custom theme text schema |
| #26947 | True | False | 0.92 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #25670 | True | False | 0.91 | fix(core): remove duplicate initialize call on agents refreshed |

**decider@openrouter** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.97 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 0.95 | fix(ui): clamped table column widths |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26949 | True | False | 0.94 | fix(ci): configure git remote with token for authentication |
| #26947 | True | False | 0.94 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #25827 | True | False | 0.94 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #29377 | True | False | 0.93 | fix(core): update auth error documentation link to valid anchor and a… |
| #27619 | True | False | 0.92 | fix(core): implement atomic update in MCP tool discovery |

**decision-1@openrouter** (19)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27345 | False | True | 0.99 | feat(context): Complete simplification work. |
| #26073 | False | True | 0.99 | Fix bulk of remaining issues with generalist profile |
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #25716 | False | True | 0.98 | refactor(memory): replace MemoryManagerAgent with prompt-driven memor… |
| #28530 | False | True | 0.98 | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #26949 | True | False | 0.97 | fix(ci): configure git remote with token for authentication |
| #28470 | False | True | 0.97 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #28532 | False | True | 0.96 | feat(caretaker-evals): add local golden issue collection and firestor… |

**drex-max@openrouter** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #27253 | True | False | 0.97 | fix: robust ripgrep path resolution and 1p hermetic execution support |
| #26658 | True | False | 0.96 | fix(routing): fix resolveClassifierModel argument mismatch in Approva… |
| #26646 | True | False | 0.96 | fix(core): resolve parallel tool call streaming ID collision |
| #28216 | True | False | 0.95 | Refactor: exclude transient CI configuration files from workspace con… |
| #25827 | True | False | 0.95 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #27619 | True | False | 0.95 | fix(core): implement atomic update in MCP tool discovery |
| #26947 | True | False | 0.95 | feat(core): add adk.agentSessionSubagentEnabled flag |

**elephant@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.91 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |

**gemini-decision@google** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.94 | fix(cli): add missing response key to custom theme text schema |

**luna@decisions** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26073 | False | True | 0.92 | Fix bulk of remaining issues with generalist profile |

**mammoth@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.95 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.91 | test(integration): deflake run_shell_command and file-system-interact… |

**reflex@openrouter** (37)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 0.99 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #29185 | True | False | 0.99 | test(integration): deflake run_shell_command and file-system-interact… |
| #26646 | True | False | 0.99 | fix(core): resolve parallel tool call streaming ID collision |
| #25827 | True | False | 0.98 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #27467 | True | False | 0.98 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #26658 | True | False | 0.98 | fix(routing): fix resolveClassifierModel argument mismatch in Approva… |

**span@openrouter** (53)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 1.00 | fix(ui): clamped table column widths |
| #28940 | True | False | 1.00 | fix(a2a-server): clear stale cancellation error on new message turns |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #28216 | True | False | 0.99 | Refactor: exclude transient CI configuration files from workspace con… |
| #25670 | True | False | 0.99 | fix(core): remove duplicate initialize call on agents refreshed |
| #29185 | True | False | 0.99 | test(integration): deflake run_shell_command and file-system-interact… |
| #27467 | True | False | 0.99 | fix(core): handle multi-line escaped quotes in stripShellWrapper |


## Cases the models disagree on (12 of 188)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #26285 | False | False (0.95) | False (0.96) | False (0.91) | False (0.93) | False (0.97) | False (0.99) | False (0.91) | False (0.96) | True (0.50) | False (0.98) | False (0.86) | False (0.77) | False (0.73) | False (0.76) | False (0.85) | False (0.80) | False (0.85) | False (0.99) | False (1.00) | fix(cli): use resolved sandbox state for auto-update check |
| #26446 | False | False (0.92) | False (0.97) | False (0.80) | False (0.84) | False (0.83) | False (0.94) | False (0.88) | False (0.94) | True (0.82) | False (0.82) | False (0.71) | False (0.71) | False (0.64) | False (0.67) | False (0.79) | False (0.75) | False (0.85) | False (0.99) | False (1.00) | refactor(UI): created constants file for ThemeDialog |
| #26128 | False | False (0.96) | False (0.96) | False (0.89) | False (0.93) | False (0.98) | False (0.99) | False (0.86) | False (0.96) | True (0.50) | False (0.95) | False (0.80) | True (0.51) | False (0.69) | False (0.75) | False (0.83) | False (0.80) | False (0.84) | False (0.98) | False (1.00) | fix(ux): added error message for ENOTDIR |
| #28038 | False | False (0.93) | False (0.95) | False (0.92) | False (0.89) | False (0.88) | False (0.80) | False (0.87) | False (0.94) | False (0.53) | False (0.90) | True (0.58) | False (0.60) | False (0.57) | False (0.72) | False (0.75) | False (0.68) | False (0.74) | False (0.96) | False (1.00) | fix(ci): append trailing slash to registry url in npmrc |
| #26532 | False | False (0.95) | False (0.97) | False (0.87) | False (0.92) | False (0.93) | False (0.99) | False (0.83) | False (0.91) | True (0.53) | False (0.95) | False (0.85) | False (0.78) | False (0.69) | False (0.73) | False (0.79) | False (0.77) | False (0.76) | False (0.95) | False (0.99) | fix(core): reject numeric project IDs in GOOGLE_CLOUD_PROJECT (#24695) |
| #27353 | False | False (0.96) | False (0.97) | False (0.87) | False (0.78) | False (0.92) | False (0.99) | False (0.89) | False (0.93) | True (0.68) | False (0.93) | False (0.79) | False (0.70) | False (0.65) | False (0.78) | False (0.81) | False (0.79) | False (0.80) | False (0.99) | False (0.99) | fix(ui): added volta to auto update check |
| #26669 | False | False (0.94) | False (0.96) | False (0.89) | False (0.84) | False (0.93) | False (0.97) | False (0.86) | False (0.94) | True (0.50) | False (0.92) | False (0.72) | False (0.74) | False (0.62) | False (0.73) | False (0.75) | False (0.79) | False (0.82) | False (0.98) | False (0.99) | fix(ui): added quotes around session id in resume tip |
| #28216 | True | False (0.95) | False (0.97) | False (0.83) | False (0.79) | False (0.82) | False (0.98) | False (0.88) | False (0.89) | True (0.56) | False (0.95) | False (0.77) | False (0.59) | False (0.66) | False (0.85) | False (0.86) | False (0.77) | False (0.74) | False (0.96) | False (0.99) | Refactor: exclude transient CI configuration files from workspace con… |
| #27229 | False | False (0.93) | False (0.95) | False (0.86) | False (0.84) | False (0.89) | False (0.95) | False (0.87) | False (0.93) | True (0.78) | False (0.91) | False (0.64) | False (0.69) | False (0.57) | False (0.80) | False (0.83) | False (0.77) | False (0.72) | False (0.98) | False (0.99) | fix(core): add exception handling to migrateFromFileStorage |
| #26289 | False | False (0.89) | False (0.94) | False (0.84) | False (0.85) | False (0.82) | False (0.83) | False (0.79) | False (0.89) | False (0.73) | False (0.91) | False (0.53) | False (0.61) | False (0.60) | False (0.80) | False (0.83) | True (0.52) | False (0.66) | False (0.96) | False (0.99) | fix(ci): checkout PR branch instead of main in bot workflow |
| #26073 | False | True (0.75) | True (0.82) | True (0.91) | True (0.90) | True (0.98) | True (0.99) | True (0.69) | True (0.80) | True (0.99) | True (0.94) | True (0.91) | True (0.89) | True (0.75) | True (0.77) | False (0.56) | True (0.92) | True (0.84) | True (0.97) | True (0.95) | Fix bulk of remaining issues with generalist profile |
| #26705 | False | False (0.95) | False (0.96) | False (0.94) | False (0.62) | False (0.86) | False (0.95) | False (0.78) | False (0.91) | True (0.75) | False (0.73) | False (0.85) | True (0.81) | False (0.57) | False (0.79) | False (0.70) | False (0.65) | False (0.79) | False (0.99) | False (0.98) | skip broken test |
