# gh-gemini-pr-rework

2026-11-11 · 338 labelled dev cases (False 247, True 91) · split: stratified k-fold (no test case among these: CV numbers only) · source: Merged PRs of google-gemini/gemini-cli (review history via the GitHub API)

**clef-omni@openrouter** has the highest coverage at 95% accuracy, 19% [15, 23] (API cost $0.95 per 10k, p99 424ms). Its interval overlaps with decider@openrouter, d1-ultra@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is clef-omni@openrouter's, 76% [72, 81].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter ✕ | 337 | 73.3% [69, 78] | 0.12 | 0.69 | 0.14 | 1% [0, 2] | 66.7% (13.5%) | 0/338 | 1/338 |
| clef-omni@openrouter | 338 | 76.3% [72, 81] | 0.31 | 0.71 | 0.13 | 19% [15, 23] | 93.8% (86.3%) | 0/338 | 0/338 |
| clef@openrouter | 338 | 70.4% [65, 75] | 0.44 | 0.71 | 0.07 | 4% [2, 7] | 86.7% (63.7%) | 0/338 | 0/338 |
| d1-ultra@openrouter | 338 | 71.9% [67, 77] | 0.44 | 0.70 | 0.07 | 18% [14, 22] | 91.8% (83.5%) | 0/338 | 0/338 |
| d1.1@openrouter | 338 | 69.8% [64, 75] | 0.42 | 0.70 | 0.12 | 3% [1, 5] | 90.9% (63.6%) | 0/338 | 0/338 |
| d1@vercel | 338 | 70.4% [65, 75] | 0.37 | 0.69 | 0.14 | 5% [2, 7] | 81.2% (58.3%) | 0/338 | 0/338 |
| decider-flash@openrouter | 338 | 73.7% [69, 78] | 0.08 | 0.68 | 0.07 | 4% [2, 6] | 83.3% (56.2%) | 0/338 | 0/338 |
| decider@openrouter | 338 | 74.9% [70, 80] | 0.27 | 0.70 | 0.09 | 12% [9, 16] | 90.5% (79.5%) | 0/338 | 0/338 |
| decision-1@openrouter | 338 | 61.5% [57, 67] | 0.48 | 0.69 | 0.15 | 0% [0, 1] | 0.0% (0.0%) | 0/338 | 0/338 |
| drex-max@openrouter | 338 | 74.9% [70, 79] | 0.38 | 0.69 | 0.12 | 11% [8, 14] | 94.6% (83.9%) | 0/338 | 0/338 |
| elephant@openrouter | 338 | 72.5% [68, 78] | 0.44 | 0.69 | 0.06 | 1% [0, 3] | 80.0% (34.3%) | 0/338 | 0/338 |
| gemini-decision@openrouter | 338 | 68.6% [64, 73] | 0.48 | 0.68 | 0.01 | 1% [0, 3] | 60.0% (18.9%) | 0/338 | 0/338 |
| jev:1.14 | 338 | 71.3% [66, 76] | 0.46 | 0.72 | 0.07 | 1% [0, 3] | 100.0% (54.9%) | 0/338 | 0/338 |
| joey@openrouter | 338 | 74.0% [69, 78] | 0.27 | 0.70 | 0.04 | 1% [0, 2] | 75.0% (24.9%) | 0/338 | 0/338 |
| kev@openrouter | 338 | 73.4% [69, 78] | 0.06 | 0.64 | 0.02 | 1% [0, 2] | 75.0% (24.9%) | 0/338 | 0/338 |
| luna@decisions | 338 | 69.2% [64, 74] | 0.47 | 0.70 | 0.04 | 1% [0, 2] | 75.0% (24.9%) | 0/338 | 0/338 |
| mammoth@openrouter | 338 | 70.4% [65, 75] | 0.50 | 0.73 | 0.04 | 7% [4, 9] | 82.6% (64.5%) | 0/338 | 0/338 |
| reflex@openrouter | 338 | 74.9% [70, 80] | 0.37 | 0.73 | 0.14 | 4% [2, 7] | 85.7% (61.5%) | 0/338 | 0/338 |
| span@openrouter | 338 | 72.8% [68, 78] | 0.31 | 0.70 | 0.19 | 6% [4, 9] | 85.0% (65.6%) | 0/338 | 0/338 |

Not compared: clef-flash@openrouter (1 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is not ranked. Ask them again: `s1flow run gh-gemini-pr-rework --models clef-flash@openrouter`

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 1, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| clef-omni@openrouter = | 19% [15, 23] | 0.237 [0.192, 0.284] | 0.96 | met |
| decider@openrouter = | 12% [9, 16] | 0.251 [0.204, 0.302] | 0.95 | met |
| d1-ultra@openrouter = | 18% [14, 22] | 0.281 [0.234, 0.331] | 0.92 | met |
| drex-max@openrouter | 11% [8, 14] | 0.251 [0.207, 0.299] | 0.97 | met |
| mammoth@openrouter | 7% [4, 9] | 0.296 [0.246, 0.349] | — | met |
| span@openrouter | 6% [4, 9] | 0.272 [0.225, 0.322] | 1.00 | met |
| d1@vercel | 5% [2, 7] | 0.296 [0.249, 0.346] | 1.00 | met |
| clef@openrouter | 4% [2, 7] | 0.296 [0.251, 0.346] | 0.96 | met |
| reflex@openrouter | 4% [2, 7] | 0.251 [0.204, 0.299] | 1.00 | met |
| decider-flash@openrouter | 4% [2, 6] | 0.263 [0.216, 0.311] | 0.93 | met |
| d1.1@openrouter | 3% [1, 5] | 0.302 [0.251, 0.355] | 0.98 | met |
| elephant@openrouter | 1% [0, 3] | 0.275 [0.225, 0.322] | — | met |
| jev:1.14 | 1% [0, 3] | 0.287 [0.243, 0.337] | 0.82 | met |
| gemini-decision@openrouter | 1% [0, 3] | 0.314 [0.266, 0.361] | 0.94 | met |
| joey@openrouter | 1% [0, 2] | 0.260 [0.216, 0.308] | 0.88 | met |
| kev@openrouter | 1% [0, 2] | 0.266 [0.219, 0.314] | 0.87 | met |
| luna@decisions | 1% [0, 2] | 0.308 [0.257, 0.358] | 0.93 | met |
| decision-1@openrouter | 0% [0, 1] | 0.385 [0.334, 0.435] | 1.00 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 337 | 351 ms | 792 ms | 2619 ms | 3623 ms | 7.5 | 0 | 4 | $0.16 | billed |  |
| clef-omni@openrouter | 338 | 193 ms | 253 ms | 424 ms | 953 ms | 2.2 | 0 | 4 | $0.95 | billed | ○ |
| clef@openrouter | 338 | 400 ms | 767 ms | 1616 ms | 2646 ms | 4.0 | 0 | 4 | $1.39 | billed |  |
| d1-ultra@openrouter | 338 | 250 ms | 345 ms | 562 ms | 825 ms | 2.3 | 0 | 4 | $0.25 | billed | ○ |
| d1.1@openrouter | 338 | 494 ms | 741 ms | 834 ms | 965 ms | 1.7 | 0 | 4 | $0.12 | billed |  |
| d1@vercel | 338 | 221 ms | 283 ms | 368 ms | 474 ms | 1.7 | 0 | 4 | $0.12 | billed | ○ |
| decider-flash@openrouter | 338 | 142 ms | 170 ms | 236 ms | 300 ms | 1.7 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 338 | 240 ms | 556 ms | 1852 ms | 2809 ms | 7.7 | 0 | 4 | $0.12 | billed | ○ |
| decision-1@openrouter | 338 | 245 ms | 312 ms | 416 ms | 445 ms | 1.7 | 0 | 4 | $0.23 | billed |  |
| drex-max@openrouter | 338 | 244 ms | 325 ms | 1046 ms | 2257 ms | 4.3 | 0 | 4 | $0.36 | billed |  |
| elephant@openrouter | 338 | 174 ms | 209 ms | 377 ms | 694 ms | 2.2 | 0 | 4 | $0.21 | billed |  |
| gemini-decision@openrouter | 338 | 336 ms | 469 ms | 556 ms | 896 ms | 1.7 | 0 | 4 | $0.69 | billed |  |
| jev:1.14 | 338 | 101 ms | 128 ms | 200 ms | 326 ms | 2.0 | 0 | 4 | $0.35 | estimated | ○ |
| joey@openrouter | 338 | 167 ms | 191 ms | 349 ms | 611 ms | 2.1 | 0 | 4 | $0.06 | billed |  |
| kev@openrouter | 338 | 517 ms | 721 ms | 889 ms | 1180 ms | 1.7 | 3 | 4 | $0.22 | billed |  |
| luna@decisions | 338 | 228 ms | 416 ms | 617 ms | 768 ms | 2.7 | 0 | 4 | $0.69 | estimated |  |
| mammoth@openrouter | 338 | 191 ms | 226 ms | 421 ms | 613 ms | 2.2 | 0 | 4 | $0.61 | billed | ○ |
| reflex@openrouter | 338 | 265 ms | 297 ms | 360 ms | 577 ms | 1.4 | 0 | 4 | $0.26 | billed | ○ |
| span@openrouter | 338 | 300 ms | 853 ms | 1028 ms | 1172 ms | 3.4 | 0 | 4 | $0.07 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0053 | 39 s (estimated, 337 calls) | 19 min | 4 |
| clef-omni@openrouter | $0.03 | 17 s (estimated, 338 calls) | 9 min | 4 |
| clef@openrouter | $0.05 | 40 s (estimated, 338 calls) | 20 min | 4 |
| d1-ultra@openrouter | $0.0083 | 23 s (estimated, 338 calls) | 11 min | 4 |
| d1.1@openrouter | $0.0040 | 42 s (estimated, 338 calls) | 21 min | 4 |
| d1@vercel | $0.0040 | 20 s (estimated, 338 calls) | 10 min | 4 |
| decider-flash@openrouter | $0.0020 | 12 s (estimated, 338 calls) | 6 min | 4 |
| decider@openrouter | $0.0041 | 29 s (estimated, 338 calls) | 14 min | 4 |
| decision-1@openrouter | $0.0077 | 22 s (estimated, 338 calls) | 11 min | 4 |
| drex-max@openrouter | $0.01 | 23 s (estimated, 338 calls) | 11 min | 4 |
| elephant@openrouter | $0.0072 | 16 s (estimated, 338 calls) | 8 min | 4 |
| gemini-decision@openrouter | $0.02 | 29 s (estimated, 338 calls) | 14 min | 4 |
| jev:1.14 | $0.01 | 9 s (estimated, 338 calls) | 4 min | 4 |
| joey@openrouter | $0.0021 | 15 s (estimated, 338 calls) | 7 min | 4 |
| kev@openrouter | $0.0074 | 48 s (estimated, 338 calls) | 24 min | 4 |
| luna@decisions | $0.02 | 23 s (estimated, 338 calls) | 11 min | 4 |
| mammoth@openrouter | $0.02 | 17 s (estimated, 338 calls) | 8 min | 4 |
| reflex@openrouter | $0.0086 | 23 s (estimated, 338 calls) | 11 min | 4 |
| span@openrouter | $0.0023 | 35 s (estimated, 338 calls) | 17 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 73.3% | 74.5% | 76 | 10 | 0.35 | 0.35 |
| clef-omni@openrouter | 76.3% | 75.7% | 73 | 9 | 0.50 | 0.50 |
| clef@openrouter | 70.4% | 75.1% | 73 | 11 | 0.80 | 0.80 |
| d1-ultra@openrouter | 71.9% | 75.4% | 73 | 10 | 0.85 | 0.85 |
| d1.1@openrouter | 69.8% | 73.1% | 73 | 18 | 0.85 | 0.85 |
| d1@vercel | 70.4% | 74.3% | 75 | 12 | 0.80 | 0.80 |
| decider-flash@openrouter | 73.7% | 72.5% | 86 | 7 | 0.55 | 0.55 |
| decider@openrouter | 74.9% | 73.7% | 76 | 13 | 0.55 | 0.55 |
| decision-1@openrouter | 61.5% | 74.6% | 56 | 30 | 0.80 | 0.85 |
| drex-max@openrouter | 74.9% | 73.4% | 74 | 16 | 0.60 | 0.60 |
| elephant@openrouter | 72.5% | 71.9% | 71 | 24 | 0.60 | 0.65 |
| gemini-decision@openrouter | 68.6% | 75.4% | 67 | 16 | 0.75 | 0.75 |
| jev:1.14 | 71.3% | 72.8% | 64 | 28 | 0.60 | 0.60 |
| joey@openrouter | 74.0% | 73.1% | 79 | 12 | 0.55 | 0.55 |
| kev@openrouter | 73.4% | 74.0% | 74 | 14 | 0.35 | 0.35 |
| luna@decisions | 69.2% | 74.9% | 64 | 21 | 0.75 | 0.75 |
| mammoth@openrouter | 70.4% | 74.9% | 69 | 16 | 0.75 | 0.75 |
| reflex@openrouter | 74.9% | 75.4% | 71 | 12 | 0.70 | 0.70 |
| span@openrouter | 72.8% | 73.1% | 71 | 20 | 0.35 | 0.75 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 29 (32%) | 100 (41%) |
| 0.20 | 65 (71%) | 31 (13%) |
| 0.30 | 68 (75%) | 16 (7%) |
| 0.35 | 71 (78%) | 11 (4%) |
| 0.40 | 77 (85%) | 6 (2%) |
| 0.50 | 85 (93%) | 5 (2%) |
| 0.60 | 85 (93%) | 3 (1%) |
| 0.70 | 89 (98%) | 2 (1%) |
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
| 0.10 | 4 (4%) | 205 (83%) |
| 0.20 | 17 (19%) | 126 (51%) |
| 0.30 | 30 (33%) | 92 (37%) |
| 0.40 | 41 (45%) | 72 (29%) |
| 0.50 | 52 (57%) | 48 (19%) |
| 0.60 | 58 (64%) | 36 (15%) |
| 0.70 | 65 (71%) | 23 (9%) |
| 0.80 | 73 (80%) | 8 (3%) |
| 0.90 | 90 (99%) | 1 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 5 (5%) | 179 (72%) |
| 0.20 | 24 (26%) | 122 (49%) |
| 0.30 | 40 (44%) | 77 (31%) |
| 0.40 | 47 (52%) | 54 (22%) |
| 0.50 | 53 (58%) | 42 (17%) |
| 0.60 | 60 (66%) | 32 (13%) |
| 0.70 | 64 (70%) | 23 (9%) |
| 0.80 | 71 (78%) | 12 (5%) |
| 0.85 | 73 (80%) | 8 (3%) |
| 0.90 | 83 (91%) | 4 (2%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 11 (12%) | 166 (67%) |
| 0.20 | 19 (21%) | 109 (44%) |
| 0.30 | 35 (38%) | 76 (31%) |
| 0.40 | 44 (48%) | 52 (21%) |
| 0.50 | 54 (59%) | 48 (19%) |
| 0.60 | 63 (69%) | 38 (15%) |
| 0.70 | 66 (73%) | 32 (13%) |
| 0.80 | 69 (76%) | 22 (9%) |
| 0.85 | 73 (80%) | 16 (6%) |
| 0.90 | 79 (87%) | 12 (5%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (21%) | 123 (50%) |
| 0.20 | 37 (41%) | 87 (35%) |
| 0.30 | 41 (45%) | 58 (23%) |
| 0.40 | 52 (57%) | 44 (18%) |
| 0.50 | 62 (68%) | 38 (15%) |
| 0.60 | 69 (76%) | 31 (13%) |
| 0.70 | 69 (76%) | 22 (9%) |
| 0.80 | 72 (79%) | 13 (5%) |
| 0.90 | 81 (89%) | 7 (3%) |

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
| 0.10 | 14 (15%) | 143 (58%) |
| 0.20 | 45 (49%) | 56 (23%) |
| 0.30 | 61 (67%) | 27 (11%) |
| 0.40 | 68 (75%) | 16 (6%) |
| 0.50 | 75 (82%) | 10 (4%) |
| 0.55 | 76 (84%) | 8 (3%) |
| 0.60 | 79 (87%) | 5 (2%) |
| 0.70 | 85 (93%) | 2 (1%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 206 (83%) |
| 0.20 | 11 (12%) | 182 (74%) |
| 0.30 | 19 (21%) | 144 (58%) |
| 0.40 | 24 (26%) | 121 (49%) |
| 0.50 | 31 (34%) | 99 (40%) |
| 0.60 | 38 (42%) | 70 (28%) |
| 0.70 | 48 (53%) | 55 (22%) |
| 0.80 | 52 (57%) | 31 (13%) |
| 0.85 | 59 (65%) | 23 (9%) |
| 0.90 | 69 (76%) | 18 (7%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 32 (35%) | 115 (47%) |
| 0.20 | 45 (49%) | 46 (19%) |
| 0.30 | 56 (62%) | 32 (13%) |
| 0.40 | 62 (68%) | 26 (11%) |
| 0.50 | 65 (71%) | 20 (8%) |
| 0.60 | 69 (76%) | 15 (6%) |
| 0.70 | 73 (80%) | 13 (5%) |
| 0.80 | 78 (86%) | 7 (3%) |
| 0.90 | 86 (95%) | 3 (1%) |

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

## Misses and false alarms by threshold (gemini-decision@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 243 (98%) |
| 0.20 | 5 (5%) | 207 (84%) |
| 0.30 | 18 (20%) | 149 (60%) |
| 0.40 | 33 (36%) | 98 (40%) |
| 0.50 | 43 (47%) | 63 (26%) |
| 0.60 | 55 (60%) | 36 (15%) |
| 0.70 | 62 (68%) | 19 (8%) |
| 0.75 | 70 (77%) | 10 (4%) |
| 0.80 | 76 (84%) | 6 (2%) |
| 0.90 | 89 (98%) | 1 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 1 (1%) | 240 (97%) |
| 0.30 | 5 (5%) | 180 (73%) |
| 0.40 | 28 (31%) | 95 (38%) |
| 0.50 | 50 (55%) | 47 (19%) |
| 0.60 | 61 (67%) | 24 (10%) |
| 0.70 | 79 (87%) | 8 (3%) |
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
| 0.20 | 14 (15%) | 177 (72%) |
| 0.30 | 57 (63%) | 42 (17%) |
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
| 0.10 | 51 (56%) | 46 (19%) |
| 0.20 | 59 (65%) | 31 (13%) |
| 0.30 | 63 (69%) | 24 (10%) |
| 0.40 | 66 (73%) | 22 (9%) |
| 0.50 | 70 (77%) | 22 (9%) |
| 0.60 | 71 (78%) | 19 (8%) |
| 0.70 | 74 (81%) | 17 (7%) |
| 0.75 | 76 (84%) | 10 (4%) |
| 0.80 | 82 (90%) | 8 (3%) |
| 0.90 | 85 (93%) | 3 (1%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (29)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.95 | fix(core): update auth error documentation link to valid anchor and a… |
| #25822 | True | False | 0.95 | fix(cli): add missing response key to custom theme text schema |
| #28216 | True | False | 0.95 | Refactor: exclude transient CI configuration files from workspace con… |
| #28940 | True | False | 0.95 | fix(a2a-server): clear stale cancellation error on new message turns |
| #27391 | True | False | 0.94 | fix(cli): filter internal session context from history during resumpt… |
| #27467 | True | False | 0.94 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #25324 | True | False | 0.94 | fix(cli): prevent spam loop when preferredEditor is invalid |

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

**clef@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26949 | True | False | 0.91 | fix(ci): configure git remote with token for authentication |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |
| #26991 | True | False | 0.90 | fix(ui): clamped table column widths |

**d1-ultra@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.97 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.93 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.93 | Fix bulk of remaining issues with generalist profile |
| #25827 | True | False | 0.92 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #28470 | False | True | 0.92 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #25324 | True | False | 0.91 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #27619 | True | False | 0.91 | fix(core): implement atomic update in MCP tool discovery |
| #27345 | False | True | 0.91 | feat(context): Complete simplification work. |

**d1.1@openrouter** (23)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26991 | True | False | 0.98 | fix(ui): clamped table column widths |
| #28470 | False | True | 0.98 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #29081 | False | True | 0.96 | fix(core): prevent SSRF in MCP OAuth metadata discovery and authentic… |
| #26270 | True | False | 0.96 | feat(ui): added microphone and updated placeholder for voice mode |
| #29115 | False | True | 0.96 | fix(config): enforce strict permission and ownership checks on system… |
| #28053 | False | True | 0.96 | fix(core-tools): resolve defensive path resolution for at-reference f… |
| #26073 | False | True | 0.96 | Fix bulk of remaining issues with generalist profile |

**d1@vercel** (26)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26991 | True | False | 1.00 | fix(ui): clamped table column widths |
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #26270 | True | False | 0.99 | feat(ui): added microphone and updated placeholder for voice mode |
| #26949 | True | False | 0.98 | fix(ci): configure git remote with token for authentication |
| #29185 | True | False | 0.98 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.98 | Fix bulk of remaining issues with generalist profile |
| #26947 | True | False | 0.98 | feat(core): add adk.agentSessionSubagentEnabled flag |

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
| #25827 | True | False | 0.95 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26949 | True | False | 0.94 | fix(ci): configure git remote with token for authentication |
| #26947 | True | False | 0.94 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #29377 | True | False | 0.93 | fix(core): update auth error documentation link to valid anchor and a… |
| #27467 | True | False | 0.93 | fix(core): handle multi-line escaped quotes in stripShellWrapper |

**decision-1@openrouter** (20)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27345 | False | True | 0.99 | feat(context): Complete simplification work. |
| #26073 | False | True | 0.99 | Fix bulk of remaining issues with generalist profile |
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #25716 | False | True | 0.98 | refactor(memory): replace MemoryManagerAgent with prompt-driven memor… |
| #28530 | False | True | 0.98 | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #26949 | True | False | 0.97 | fix(ci): configure git remote with token for authentication |
| #28470 | False | True | 0.96 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #28532 | False | True | 0.96 | feat(caretaker-evals): add local golden issue collection and firestor… |

**drex-max@openrouter** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #27253 | True | False | 0.97 | fix: robust ripgrep path resolution and 1p hermetic execution support |
| #25324 | True | False | 0.96 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #28216 | True | False | 0.96 | Refactor: exclude transient CI configuration files from workspace con… |
| #26646 | True | False | 0.96 | fix(core): resolve parallel tool call streaming ID collision |
| #26658 | True | False | 0.96 | fix(routing): fix resolveClassifierModel argument mismatch in Approva… |
| #25827 | True | False | 0.95 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #27619 | True | False | 0.95 | fix(core): implement atomic update in MCP tool discovery |

**elephant@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.91 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |

**gemini-decision@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.94 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.90 | Fix bulk of remaining issues with generalist profile |

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

**span@openrouter** (54)

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


## Cases the models disagree on (12 of 191)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #26774 | False | False (0.96) | False (0.98) | False (0.95) | False (0.97) | False (0.95) | False (0.98) | False (0.89) | False (0.96) | True (0.50) | False (0.98) | False (0.87) | False (0.82) | False (0.82) | False (0.85) | False (0.80) | False (0.80) | False (0.93) | False (1.00) | False (1.00) | docs: update sandbox image command |
| #26446 | False | False (0.94) | False (0.97) | False (0.80) | False (0.86) | False (0.79) | False (0.90) | False (0.88) | False (0.94) | True (0.82) | False (0.88) | False (0.71) | False (0.67) | False (0.67) | False (0.67) | False (0.79) | False (0.75) | False (0.85) | False (0.99) | False (1.00) | refactor(UI): created constants file for ThemeDialog |
| #26128 | False | False (0.96) | False (0.96) | False (0.89) | False (0.94) | False (0.98) | False (0.98) | False (0.86) | False (0.96) | True (0.53) | False (0.95) | False (0.80) | False (0.56) | False (0.68) | False (0.75) | False (0.83) | False (0.80) | False (0.84) | False (0.98) | False (1.00) | fix(ux): added error message for ENOTDIR |
| #28038 | False | False (0.93) | False (0.95) | False (0.84) | False (0.89) | False (0.89) | False (0.78) | False (0.87) | False (0.94) | False (0.56) | False (0.90) | True (0.58) | False (0.67) | False (0.57) | False (0.72) | False (0.75) | False (0.68) | False (0.74) | False (0.96) | False (1.00) | fix(ci): append trailing slash to registry url in npmrc |
| #27353 | False | False (0.96) | False (0.97) | False (0.86) | False (0.81) | False (0.95) | False (0.99) | False (0.89) | False (0.93) | True (0.68) | False (0.93) | False (0.79) | False (0.71) | False (0.67) | False (0.78) | False (0.81) | False (0.79) | False (0.80) | False (0.99) | False (0.99) | fix(ui): added volta to auto update check |
| #26669 | False | False (0.94) | False (0.96) | False (0.89) | False (0.89) | False (0.93) | False (0.98) | False (0.86) | False (0.94) | True (0.50) | False (0.92) | False (0.72) | False (0.67) | False (0.62) | False (0.73) | False (0.74) | False (0.79) | False (0.82) | False (0.98) | False (0.99) | fix(ui): added quotes around session id in resume tip |
| #28216 | True | False (0.95) | False (0.97) | False (0.84) | False (0.79) | False (0.80) | False (0.97) | False (0.88) | False (0.89) | True (0.56) | False (0.96) | False (0.77) | False (0.72) | False (0.65) | False (0.85) | False (0.85) | False (0.77) | False (0.74) | False (0.96) | False (0.99) | Refactor: exclude transient CI configuration files from workspace con… |
| #26073 | False | True (0.75) | True (0.82) | True (0.91) | True (0.93) | True (0.96) | True (0.98) | True (0.69) | True (0.79) | True (0.99) | True (0.94) | True (0.91) | True (0.90) | True (0.75) | True (0.77) | False (0.56) | True (0.92) | True (0.84) | True (0.97) | True (0.95) | Fix bulk of remaining issues with generalist profile |
| #27229 | False | False (0.93) | False (0.95) | False (0.86) | False (0.85) | False (0.86) | False (0.94) | False (0.87) | False (0.93) | True (0.78) | False (0.91) | False (0.64) | False (0.63) | False (0.57) | False (0.80) | False (0.83) | False (0.77) | False (0.72) | False (0.98) | False (0.99) | fix(core): add exception handling to migrateFromFileStorage |
| #26289 | False | False (0.89) | False (0.94) | False (0.86) | False (0.77) | False (0.81) | False (0.80) | False (0.79) | False (0.91) | False (0.73) | False (0.91) | False (0.53) | False (0.62) | False (0.59) | False (0.80) | False (0.83) | True (0.52) | False (0.66) | False (0.96) | False (0.99) | fix(ci): checkout PR branch instead of main in bot workflow |
| #26705 | False | False (0.95) | False (0.96) | False (0.94) | False (0.59) | False (0.89) | False (0.96) | False (0.78) | False (0.91) | True (0.75) | False (0.83) | False (0.85) | True (0.81) | False (0.56) | False (0.79) | False (0.70) | False (0.65) | False (0.79) | False (0.99) | False (0.98) | skip broken test |
| #26506 | False | False (0.87) | False (0.77) | False (0.64) | False (0.60) | False (0.83) | False (0.74) | False (0.83) | False (0.92) | True (0.62) | False (0.88) | False (0.55) | False (0.74) | False (0.64) | False (0.72) | False (0.74) | False (0.57) | False (0.71) | False (0.95) | False (0.99) | feat: allow queuing messages during compression (#24071) |
