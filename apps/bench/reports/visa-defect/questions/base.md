# visa-defect

2026-11-11 · 168 labelled dev cases (True 84, False 84) · split: stratified k-fold (no test case among these: CV numbers only) · source: VisA (Amazon, CC BY 4.0), test split: 10 defective and 10 good photos per item, 12 items

**jev** has the highest coverage at 95% accuracy, 24% [17, 30] (API cost $0.65 per 10k, p99 430ms). Its interval overlaps with jev:1.14, d1-ultra@openrouter, luna@decisions, decider-flash@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is gemini-decision@openrouter's, 76% [69, 82].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 168 | 58.9% [52, 66] | 0.30 | 0.76 | 0.22 | 3% [1, 5] | 80.0% (34.3%) | 0/168 | 0/168 |
| clef-omni@openrouter | 168 | 55.4% [48, 63] | 0.27 | 0.69 | 0.27 | 1% [0, 2] | 100.0% (5.0%) | 0/168 | 0/168 |
| clef@openrouter | 168 | 67.3% [60, 74] | 0.55 | 0.75 | 0.12 | 0% [0, 0] | — (0.0%) | 0/168 | 0/168 |
| d1-ultra@openrouter | 168 | 70.8% [64, 77] | 0.60 | 0.86 | 0.06 | 21% [15, 29] | 94.4% (83.5%) | 0/168 | 0/168 |
| d1.1@openrouter | 168 | 57.1% [50, 65] | 0.25 | 0.79 | 0.29 | 7% [3, 11] | 100.0% (76.2%) | 0/168 | 0/168 |
| d1@vercel | 168 | 61.9% [54, 69] | 0.38 | 0.78 | 0.26 | 2% [0, 4] | 66.7% (13.5%) | 0/168 | 0/168 |
| decider-flash@openrouter | 168 | 57.1% [50, 64] | 0.25 | 0.81 | 0.26 | 12% [8, 18] | 85.7% (67.1%) | 0/168 | 0/168 |
| decider@openrouter | 168 | 59.5% [52, 67] | 0.33 | 0.77 | 0.19 | 9% [5, 14] | 93.3% (72.1%) | 0/168 | 0/168 |
| drex-max@openrouter | 168 | 63.1% [56, 70] | 0.47 | 0.76 | 0.19 | 5% [2, 8] | 87.5% (52.9%) | 0/168 | 0/168 |
| elephant@openrouter | 168 | 73.8% [68, 80] | 0.68 | 0.81 | 0.04 | 4% [1, 7] | 100.0% (65.2%) | 0/168 | 0/168 |
| gemini-decision@openrouter | 168 | 75.6% [69, 82] | 0.68 | 0.82 | 0.09 | 8% [4, 12] | 84.6% (59.0%) | 0/168 | 0/168 |
| jev | 168 | 75.0% [68, 81] | 0.77 | 0.82 | 0.13 | 24% [17, 30] | 92.5% (81.7%) | 0/168 | 0/168 |
| jev:1.14 | 168 | 72.0% [65, 79] | 0.75 | 0.81 | 0.11 | 23% [16, 29] | 94.7% (84.3%) | 0/168 | 0/168 |
| joey@openrouter | 168 | 72.0% [65, 79] | 0.61 | 0.86 | 0.10 | 11% [7, 15] | 88.9% (69.0%) | 0/168 | 0/168 |
| luna@decisions | 168 | 61.3% [54, 68] | 0.41 | 0.83 | 0.23 | 22% [16, 29] | 94.6% (83.9%) | 0/168 | 0/168 |
| mammoth@openrouter | 168 | 63.1% [56, 70] | 0.42 | 0.80 | 0.20 | 1% [0, 3] | 100.0% (22.4%) | 0/168 | 0/168 |
| reflex@openrouter | 168 | 63.1% [56, 70] | 0.42 | 0.80 | 0.21 | 2% [1, 5] | 50.0% (9.8%) | 0/168 | 0/168 |
| span@openrouter | 168 | 61.9% [54, 69] | 0.42 | 0.83 | 0.28 | 7% [3, 11] | 81.8% (53.0%) | 0/168 | 0/168 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev = jev-1.14.0; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| jev = | 24% [17, 30] | 75% [68, 81] | 0.79 | met |
| jev:1.14 = | 23% [16, 29] | 72% [65, 79] | 0.82 | met |
| d1-ultra@openrouter = | 21% [15, 29] | 71% [64, 77] | 0.82 | met |
| luna@decisions = | 22% [16, 29] | 61% [54, 68] | 0.92 | met |
| decider-flash@openrouter = | 12% [8, 18] | 57% [50, 64] | 0.91 | met |
| joey@openrouter | 11% [7, 15] | 72% [65, 79] | 0.91 | met |
| decider@openrouter | 9% [5, 14] | 60% [52, 67] | 0.92 | met |
| gemini-decision@openrouter | 8% [4, 12] | 76% [69, 82] | 0.82 | met |
| span@openrouter | 7% [3, 11] | 62% [54, 69] | 0.98 | met |
| d1.1@openrouter | 7% [3, 11] | 57% [50, 65] | 0.96 | met |
| drex-max@openrouter | 5% [2, 8] | 63% [56, 70] | 0.97 | met |
| elephant@openrouter | 4% [1, 7] | 74% [68, 80] | 0.90 | met |
| clef-flash@openrouter | 3% [1, 5] | 59% [52, 66] | 0.94 | met |
| reflex@openrouter | 2% [1, 5] | 63% [56, 70] | — | met |
| d1@vercel | 2% [0, 4] | 62% [54, 69] | — | met |
| mammoth@openrouter | 1% [0, 3] | 63% [56, 70] | 0.97 | met |
| clef-omni@openrouter | 1% [0, 2] | 55% [48, 63] | 0.96 | met |
| clef@openrouter | 0% [0, 0] | 67% [60, 74] | 0.96 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 168 | 385 ms | 616 ms | 1445 ms | 2472 ms | 3.8 | 0 | 4 | $0.24 | billed |  |
| clef-omni@openrouter | 168 | 378 ms | 514 ms | 1682 ms | 4216 ms | 4.4 | 0 | 4 | $0.93 | billed |  |
| clef@openrouter | 168 | 575 ms | 999 ms | 1422 ms | 1840 ms | 2.5 | 0 | 4 | $1.49 | billed |  |
| d1-ultra@openrouter | 168 | 347 ms | 493 ms | 849 ms | 1136 ms | 2.4 | 0 | 4 | $0.32 | billed | ○ |
| d1.1@openrouter | 168 | 351 ms | 630 ms | 1001 ms | 1200 ms | 2.9 | 0 | 4 | $0.15 | billed |  |
| d1@vercel | 168 | 448 ms | 685 ms | 937 ms | 965 ms | 2.1 | 0 | 4 | $0.15 | billed |  |
| decider-flash@openrouter | 168 | 326 ms | 379 ms | 984 ms | 1452 ms | 3.0 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 168 | 359 ms | 512 ms | 970 ms | 1388 ms | 2.7 | 0 | 4 | $0.12 | billed |  |
| drex-max@openrouter | 168 | 360 ms | 663 ms | 1148 ms | 1744 ms | 3.2 | 0 | 4 | $0.35 | billed |  |
| elephant@openrouter | 168 | 260 ms | 374 ms | 488 ms | 586 ms | 1.9 | 0 | 4 | $0.23 | billed | ○ |
| gemini-decision@openrouter | 168 | 777 ms | 1127 ms | 1412 ms | 1774 ms | 1.8 | 0 | 4 | $1.25 | billed |  |
| jev | 168 | 144 ms | 258 ms | 430 ms | 473 ms | 3.0 | 0 | 4 | $0.65 | estimated | ○ |
| jev:1.14 | 168 | 127 ms | 244 ms | 364 ms | 478 ms | 2.9 | 0 | 4 | $0.65 | estimated | ○ |
| joey@openrouter | 168 | 259 ms | 373 ms | 578 ms | 837 ms | 2.2 | 0 | 4 | $0.07 | billed | ○ |
| luna@decisions | 168 | 283 ms | 727 ms | 955 ms | 1202 ms | 3.4 | 0 | 4 | $0.66 | estimated |  |
| mammoth@openrouter | 168 | 299 ms | 418 ms | 533 ms | 659 ms | 1.8 | 0 | 4 | $0.67 | billed |  |
| reflex@openrouter | 168 | 333 ms | 448 ms | 607 ms | 735 ms | 1.8 | 0 | 4 | $0.25 | billed |  |
| span@openrouter | 168 | 330 ms | 562 ms | 856 ms | 1218 ms | 2.6 | 0 | 4 | $0.04 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev (list price of 2026-10-03), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0040 | 19 s (estimated, 168 calls) | 19 min | 4 |
| clef-omni@openrouter | $0.02 | 18 s (estimated, 168 calls) | 18 min | 4 |
| clef@openrouter | $0.03 | 27 s (estimated, 168 calls) | 27 min | 4 |
| d1-ultra@openrouter | $0.0054 | 16 s (estimated, 168 calls) | 15 min | 4 |
| d1.1@openrouter | $0.0026 | 17 s (estimated, 168 calls) | 16 min | 4 |
| d1@vercel | $0.0026 | 20 s (estimated, 168 calls) | 20 min | 4 |
| decider-flash@openrouter | $0.0010 | 15 s (estimated, 168 calls) | 15 min | 4 |
| decider@openrouter | $0.0019 | 16 s (estimated, 168 calls) | 16 min | 4 |
| drex-max@openrouter | $0.0058 | 18 s (estimated, 168 calls) | 18 min | 4 |
| elephant@openrouter | $0.0039 | 12 s (estimated, 168 calls) | 12 min | 4 |
| gemini-decision@openrouter | $0.02 | 35 s (estimated, 168 calls) | 34 min | 4 |
| jev | $0.01 | 8 s (estimated, 168 calls) | 8 min | 4 |
| jev:1.14 | $0.01 | 6 s (estimated, 168 calls) | 6 min | 4 |
| joey@openrouter | $0.0011 | 12 s (estimated, 168 calls) | 12 min | 4 |
| luna@decisions | $0.01 | 16 s (estimated, 168 calls) | 16 min | 4 |
| mammoth@openrouter | $0.01 | 14 s (estimated, 168 calls) | 14 min | 4 |
| reflex@openrouter | $0.0042 | 15 s (estimated, 168 calls) | 15 min | 4 |
| span@openrouter | $0.0007 | 15 s (estimated, 168 calls) | 15 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 58.9% | 73.8% | 23 | 21 | 0.15 | 0.15 |
| clef-omni@openrouter | 55.4% | 64.3% | 38 | 22 | 0.15 | 0.15 |
| clef@openrouter | 67.3% | 70.8% | 39 | 10 | 0.35 | 0.35 |
| d1-ultra@openrouter | 70.8% | 77.4% | 30 | 8 | 0.35 | 0.35 |
| d1.1@openrouter | 57.1% | 73.8% | 38 | 6 | 0.15 | 0.15 |
| d1@vercel | 61.9% | 73.8% | 40 | 4 | 0.20 | 0.20 |
| decider-flash@openrouter | 57.1% | 70.8% | 42 | 7 | 0.20 | 0.20 |
| decider@openrouter | 59.5% | 70.2% | 16 | 34 | 0.15 | 0.15 |
| drex-max@openrouter | 63.1% | 73.2% | 34 | 11 | 0.25 | 0.25 |
| elephant@openrouter | 73.8% | 78.0% | 27 | 10 | 0.35 | 0.35 |
| gemini-decision@openrouter | 75.6% | 80.4% | 32 | 1 | 0.45 | 0.45 |
| jev | 75.0% | 72.6% | 23 | 23 | 0.55 | 0.55 |
| jev:1.14 | 72.0% | 78.0% | 18 | 19 | 0.55 | 0.55 |
| joey@openrouter | 72.0% | 78.6% | 22 | 14 | 0.20 | 0.20 |
| luna@decisions | 61.3% | 71.4% | 30 | 18 | 0.15 | 0.15 |
| mammoth@openrouter | 63.1% | 73.2% | 30 | 15 | 0.20 | 0.15 |
| reflex@openrouter | 63.1% | 74.4% | 34 | 9 | 0.20 | 0.20 |
| span@openrouter | 61.9% | 78.6% | 31 | 5 | 0.10 | 0.10 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 12 (14%) | 56 (67%) |
| 0.15 | 23 (27%) | 21 (25%) |
| 0.20 | 35 (42%) | 17 (20%) |
| 0.30 | 50 (60%) | 5 (6%) |
| 0.40 | 62 (74%) | 1 (1%) |
| 0.50 | 69 (82%) | 0 (0%) |
| 0.60 | 77 (92%) | 0 (0%) |
| 0.70 | 80 (95%) | 0 (0%) |
| 0.80 | 83 (99%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef-omni@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 18 (21%) | 52 (62%) |
| 0.15 | 28 (33%) | 28 (33%) |
| 0.20 | 42 (50%) | 15 (18%) |
| 0.30 | 53 (63%) | 7 (8%) |
| 0.40 | 63 (75%) | 5 (6%) |
| 0.50 | 70 (83%) | 5 (6%) |
| 0.60 | 74 (88%) | 4 (5%) |
| 0.70 | 77 (92%) | 2 (2%) |
| 0.80 | 80 (95%) | 1 (1%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 7 (8%) | 63 (75%) |
| 0.20 | 18 (21%) | 43 (51%) |
| 0.30 | 30 (36%) | 22 (26%) |
| 0.35 | 39 (46%) | 10 (12%) |
| 0.40 | 43 (51%) | 8 (10%) |
| 0.50 | 50 (60%) | 5 (6%) |
| 0.60 | 61 (73%) | 5 (6%) |
| 0.70 | 66 (79%) | 3 (4%) |
| 0.80 | 75 (89%) | 0 (0%) |
| 0.90 | 83 (99%) | 0 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 80 (95%) |
| 0.20 | 8 (10%) | 36 (43%) |
| 0.30 | 27 (32%) | 13 (15%) |
| 0.35 | 30 (36%) | 8 (10%) |
| 0.40 | 35 (42%) | 7 (8%) |
| 0.50 | 47 (56%) | 2 (2%) |
| 0.60 | 56 (67%) | 2 (2%) |
| 0.70 | 63 (75%) | 1 (1%) |
| 0.80 | 75 (89%) | 0 (0%) |
| 0.90 | 80 (95%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (31%) | 26 (31%) |
| 0.15 | 38 (45%) | 6 (7%) |
| 0.20 | 50 (60%) | 1 (1%) |
| 0.30 | 58 (69%) | 0 (0%) |
| 0.40 | 69 (82%) | 0 (0%) |
| 0.50 | 72 (86%) | 0 (0%) |
| 0.60 | 76 (90%) | 0 (0%) |
| 0.70 | 81 (96%) | 0 (0%) |
| 0.80 | 83 (99%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 28 (33%) | 19 (23%) |
| 0.20 | 40 (48%) | 2 (2%) |
| 0.30 | 53 (63%) | 0 (0%) |
| 0.40 | 59 (70%) | 0 (0%) |
| 0.50 | 64 (76%) | 0 (0%) |
| 0.60 | 68 (81%) | 0 (0%) |
| 0.70 | 71 (85%) | 0 (0%) |
| 0.80 | 77 (92%) | 0 (0%) |
| 0.90 | 81 (96%) | 0 (0%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (4%) | 55 (65%) |
| 0.20 | 42 (50%) | 7 (8%) |
| 0.30 | 63 (75%) | 0 (0%) |
| 0.40 | 69 (82%) | 0 (0%) |
| 0.50 | 72 (86%) | 0 (0%) |
| 0.60 | 78 (93%) | 0 (0%) |
| 0.70 | 81 (96%) | 0 (0%) |
| 0.80 | 84 (100%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 5 (6%) | 59 (70%) |
| 0.15 | 16 (19%) | 34 (40%) |
| 0.20 | 31 (37%) | 23 (27%) |
| 0.30 | 52 (62%) | 8 (10%) |
| 0.40 | 58 (69%) | 3 (4%) |
| 0.50 | 67 (80%) | 1 (1%) |
| 0.60 | 73 (87%) | 0 (0%) |
| 0.70 | 79 (94%) | 0 (0%) |
| 0.80 | 83 (99%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 16 (19%) | 47 (56%) |
| 0.20 | 28 (33%) | 20 (24%) |
| 0.25 | 34 (40%) | 11 (13%) |
| 0.30 | 39 (46%) | 9 (11%) |
| 0.40 | 50 (60%) | 7 (8%) |
| 0.50 | 57 (68%) | 5 (6%) |
| 0.60 | 70 (83%) | 2 (2%) |
| 0.70 | 75 (89%) | 1 (1%) |
| 0.80 | 78 (93%) | 0 (0%) |
| 0.90 | 82 (98%) | 0 (0%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (4%) | 78 (93%) |
| 0.20 | 12 (14%) | 40 (48%) |
| 0.30 | 21 (25%) | 18 (21%) |
| 0.35 | 25 (30%) | 10 (12%) |
| 0.40 | 28 (33%) | 9 (11%) |
| 0.50 | 38 (45%) | 6 (7%) |
| 0.60 | 52 (62%) | 4 (5%) |
| 0.70 | 60 (71%) | 1 (1%) |
| 0.80 | 72 (86%) | 1 (1%) |
| 0.90 | 81 (96%) | 0 (0%) |

## Misses and false alarms by threshold (gemini-decision@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 84 (100%) |
| 0.20 | 1 (1%) | 84 (100%) |
| 0.30 | 11 (13%) | 53 (63%) |
| 0.40 | 24 (29%) | 12 (14%) |
| 0.45 | 32 (38%) | 1 (1%) |
| 0.50 | 41 (49%) | 0 (0%) |
| 0.60 | 54 (64%) | 0 (0%) |
| 0.70 | 65 (77%) | 0 (0%) |
| 0.80 | 71 (85%) | 0 (0%) |
| 0.90 | 79 (94%) | 0 (0%) |

## Misses and false alarms by threshold (jev)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 84 (100%) |
| 0.20 | 0 (0%) | 83 (99%) |
| 0.30 | 4 (5%) | 74 (88%) |
| 0.40 | 10 (12%) | 50 (60%) |
| 0.50 | 14 (17%) | 28 (33%) |
| 0.55 | 19 (23%) | 21 (25%) |
| 0.60 | 26 (31%) | 14 (17%) |
| 0.70 | 36 (43%) | 11 (13%) |
| 0.80 | 46 (55%) | 2 (2%) |
| 0.90 | 71 (85%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 84 (100%) |
| 0.20 | 0 (0%) | 83 (99%) |
| 0.30 | 5 (6%) | 74 (88%) |
| 0.40 | 10 (12%) | 51 (61%) |
| 0.50 | 15 (18%) | 32 (38%) |
| 0.55 | 18 (21%) | 19 (23%) |
| 0.60 | 25 (30%) | 15 (18%) |
| 0.70 | 37 (44%) | 12 (14%) |
| 0.80 | 47 (56%) | 3 (4%) |
| 0.90 | 72 (86%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 4 (5%) | 68 (81%) |
| 0.20 | 18 (21%) | 14 (17%) |
| 0.30 | 36 (43%) | 4 (5%) |
| 0.40 | 42 (50%) | 3 (4%) |
| 0.50 | 47 (56%) | 0 (0%) |
| 0.60 | 53 (63%) | 0 (0%) |
| 0.70 | 62 (74%) | 0 (0%) |
| 0.80 | 69 (82%) | 0 (0%) |
| 0.90 | 76 (90%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 54 (64%) |
| 0.15 | 23 (27%) | 21 (25%) |
| 0.20 | 40 (48%) | 8 (10%) |
| 0.30 | 47 (56%) | 5 (6%) |
| 0.40 | 53 (63%) | 4 (5%) |
| 0.50 | 61 (73%) | 4 (5%) |
| 0.60 | 62 (74%) | 3 (4%) |
| 0.70 | 67 (80%) | 3 (4%) |
| 0.80 | 72 (86%) | 2 (2%) |
| 0.90 | 76 (90%) | 0 (0%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 16 (19%) | 32 (38%) |
| 0.15 | 21 (25%) | 19 (23%) |
| 0.20 | 30 (36%) | 11 (13%) |
| 0.30 | 47 (56%) | 6 (7%) |
| 0.40 | 55 (65%) | 3 (4%) |
| 0.50 | 62 (74%) | 0 (0%) |
| 0.60 | 70 (83%) | 0 (0%) |
| 0.70 | 75 (89%) | 0 (0%) |
| 0.80 | 80 (95%) | 0 (0%) |
| 0.90 | 83 (99%) | 0 (0%) |

## Misses and false alarms by threshold (reflex@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 21 (25%) | 30 (36%) |
| 0.20 | 34 (40%) | 9 (11%) |
| 0.30 | 46 (55%) | 3 (4%) |
| 0.40 | 54 (64%) | 0 (0%) |
| 0.50 | 62 (74%) | 0 (0%) |
| 0.60 | 67 (80%) | 0 (0%) |
| 0.70 | 72 (86%) | 0 (0%) |
| 0.80 | 75 (89%) | 0 (0%) |
| 0.90 | 82 (98%) | 0 (0%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 31 (37%) | 5 (6%) |
| 0.20 | 49 (58%) | 3 (4%) |
| 0.30 | 55 (65%) | 3 (4%) |
| 0.40 | 58 (69%) | 3 (4%) |
| 0.50 | 61 (73%) | 3 (4%) |
| 0.60 | 65 (77%) | 2 (2%) |
| 0.70 | 68 (81%) | 2 (2%) |
| 0.80 | 76 (90%) | 2 (2%) |
| 0.90 | 79 (94%) | 0 (0%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-003 | True | False | 0.94 | capsules-anomaly-003 |
| pcb1-anomaly-026 | True | False | 0.94 | pcb1-anomaly-026 |
| capsules-anomaly-089 | True | False | 0.94 | capsules-anomaly-089 |
| pcb1-anomaly-061 | True | False | 0.93 | pcb1-anomaly-061 |
| capsules-anomaly-034 | True | False | 0.93 | capsules-anomaly-034 |
| pcb3-anomaly-035 | True | False | 0.92 | pcb3-anomaly-035 |
| capsules-anomaly-092 | True | False | 0.92 | capsules-anomaly-092 |
| pcb1-anomaly-099 | True | False | 0.92 | pcb1-anomaly-099 |

**clef-omni@openrouter** (18)

| id | label | answer | probability | case |
|---|---|---|---|---|
| cashew-anomaly-086 | True | False | 0.95 | cashew-anomaly-086 |
| pcb1-anomaly-026 | True | False | 0.95 | pcb1-anomaly-026 |
| pcb1-anomaly-061 | True | False | 0.95 | pcb1-anomaly-061 |
| capsules-anomaly-089 | True | False | 0.95 | capsules-anomaly-089 |
| cashew-anomaly-067 | True | False | 0.94 | cashew-anomaly-067 |
| capsules-anomaly-034 | True | False | 0.94 | capsules-anomaly-034 |
| pcb1-anomaly-099 | True | False | 0.94 | pcb1-anomaly-099 |
| macaroni1-anomaly-093 | True | False | 0.93 | macaroni1-anomaly-093 |

**clef@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-075 | True | False | 0.95 | capsules-anomaly-075 |
| capsules-anomaly-034 | True | False | 0.95 | capsules-anomaly-034 |
| capsules-anomaly-092 | True | False | 0.95 | capsules-anomaly-092 |
| capsules-anomaly-089 | True | False | 0.93 | capsules-anomaly-089 |
| capsules-anomaly-003 | True | False | 0.93 | capsules-anomaly-003 |
| pcb3-anomaly-079 | True | False | 0.91 | pcb3-anomaly-079 |
| pcb3-anomaly-014 | True | False | 0.91 | pcb3-anomaly-014 |

**d1.1@openrouter** (26)

| id | label | answer | probability | case |
|---|---|---|---|---|
| cashew-anomaly-086 | True | False | 0.96 | cashew-anomaly-086 |
| pcb3-anomaly-079 | True | False | 0.96 | pcb3-anomaly-079 |
| pcb1-anomaly-026 | True | False | 0.96 | pcb1-anomaly-026 |
| capsules-anomaly-034 | True | False | 0.95 | capsules-anomaly-034 |
| cashew-anomaly-067 | True | False | 0.94 | cashew-anomaly-067 |
| macaroni1-anomaly-093 | True | False | 0.94 | macaroni1-anomaly-093 |
| macaroni1-anomaly-090 | True | False | 0.94 | macaroni1-anomaly-090 |
| capsules-anomaly-075 | True | False | 0.94 | capsules-anomaly-075 |

**d1@vercel** (28)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-089 | True | False | 1.00 | capsules-anomaly-089 |
| capsules-anomaly-003 | True | False | 1.00 | capsules-anomaly-003 |
| capsules-anomaly-075 | True | False | 0.99 | capsules-anomaly-075 |
| capsules-anomaly-092 | True | False | 0.99 | capsules-anomaly-092 |
| capsules-anomaly-034 | True | False | 0.99 | capsules-anomaly-034 |
| pcb3-anomaly-001 | True | False | 0.99 | pcb3-anomaly-001 |
| pcb1-anomaly-061 | True | False | 0.99 | pcb1-anomaly-061 |
| pcb3-anomaly-096 | True | False | 0.99 | pcb3-anomaly-096 |

**decider-flash@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| fryum-anomaly-099 | True | False | 0.91 | fryum-anomaly-099 |
| pcb1-anomaly-026 | True | False | 0.91 | pcb1-anomaly-026 |
| macaroni1-anomaly-090 | True | False | 0.90 | macaroni1-anomaly-090 |

**decider@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-075 | True | False | 0.91 | capsules-anomaly-075 |
| pcb3-anomaly-079 | True | False | 0.91 | pcb3-anomaly-079 |
| pcb1-anomaly-061 | True | False | 0.91 | pcb1-anomaly-061 |
| macaroni1-anomaly-062 | True | False | 0.90 | macaroni1-anomaly-062 |
| capsules-anomaly-092 | True | False | 0.90 | capsules-anomaly-092 |

**drex-max@openrouter** (16)

| id | label | answer | probability | case |
|---|---|---|---|---|
| pcb3-anomaly-079 | True | False | 0.96 | pcb3-anomaly-079 |
| pcb3-anomaly-014 | True | False | 0.96 | pcb3-anomaly-014 |
| capsules-anomaly-034 | True | False | 0.95 | capsules-anomaly-034 |
| capsules-anomaly-092 | True | False | 0.95 | capsules-anomaly-092 |
| pcb3-anomaly-035 | True | False | 0.95 | pcb3-anomaly-035 |
| capsules-anomaly-075 | True | False | 0.95 | capsules-anomaly-075 |
| pcb3-anomaly-001 | True | False | 0.95 | pcb3-anomaly-001 |
| capsules-anomaly-089 | True | False | 0.94 | capsules-anomaly-089 |

**elephant@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| pcb1-anomaly-026 | True | False | 0.90 | pcb1-anomaly-026 |
| pcb1-anomaly-046 | True | False | 0.90 | pcb1-anomaly-046 |
| pcb3-anomaly-079 | True | False | 0.90 | pcb3-anomaly-079 |

**joey@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| pcb1-anomaly-099 | True | False | 0.91 | pcb1-anomaly-099 |
| pcb1-anomaly-026 | True | False | 0.91 | pcb1-anomaly-026 |
| macaroni1-anomaly-093 | True | False | 0.91 | macaroni1-anomaly-093 |
| pcb1-anomaly-046 | True | False | 0.91 | pcb1-anomaly-046 |

**luna@decisions** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| macaroni1-anomaly-062 | True | False | 0.95 | macaroni1-anomaly-062 |
| cashew-anomaly-086 | True | False | 0.91 | cashew-anomaly-086 |
| capsules-anomaly-075 | True | False | 0.90 | capsules-anomaly-075 |
| capsules-anomaly-092 | True | False | 0.90 | capsules-anomaly-092 |
| capsules-anomaly-034 | True | False | 0.90 | capsules-anomaly-034 |

**mammoth@openrouter** (16)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-034 | True | False | 0.96 | capsules-anomaly-034 |
| capsules-anomaly-089 | True | False | 0.96 | capsules-anomaly-089 |
| capsules-anomaly-003 | True | False | 0.96 | capsules-anomaly-003 |
| capsules-anomaly-075 | True | False | 0.96 | capsules-anomaly-075 |
| pcb3-anomaly-014 | True | False | 0.95 | pcb3-anomaly-014 |
| capsules-anomaly-092 | True | False | 0.95 | capsules-anomaly-092 |
| macaroni1-anomaly-090 | True | False | 0.94 | macaroni1-anomaly-090 |
| macaroni1-anomaly-062 | True | False | 0.94 | macaroni1-anomaly-062 |

**reflex@openrouter** (21)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-075 | True | False | 0.98 | capsules-anomaly-075 |
| capsules-anomaly-089 | True | False | 0.97 | capsules-anomaly-089 |
| pcb3-anomaly-079 | True | False | 0.97 | pcb3-anomaly-079 |
| capsules-anomaly-034 | True | False | 0.97 | capsules-anomaly-034 |
| pcb1-anomaly-026 | True | False | 0.97 | pcb1-anomaly-026 |
| pcb3-anomaly-035 | True | False | 0.96 | pcb3-anomaly-035 |
| pcb1-anomaly-099 | True | False | 0.96 | pcb1-anomaly-099 |
| pcb3-anomaly-001 | True | False | 0.96 | pcb3-anomaly-001 |

**span@openrouter** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-075 | True | False | 0.98 | capsules-anomaly-075 |
| pcb1-anomaly-046 | True | False | 0.98 | pcb1-anomaly-046 |
| capsules-anomaly-034 | True | False | 0.98 | capsules-anomaly-034 |
| pcb1-anomaly-026 | True | False | 0.98 | pcb1-anomaly-026 |
| capsules-anomaly-003 | True | False | 0.97 | capsules-anomaly-003 |
| pcb3-anomaly-096 | True | False | 0.97 | pcb3-anomaly-096 |
| macaroni1-anomaly-090 | True | False | 0.97 | macaroni1-anomaly-090 |
| pcb1-anomaly-072 | True | False | 0.97 | pcb1-anomaly-072 |


## Cases the models disagree on (12 of 104)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev | jev:1.14 | joey@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pcb4-normal-0306 | False | False (0.91) | False (0.89) | False (0.90) | False (0.69) | False (0.97) | False (0.99) | False (0.84) | False (0.85) | False (0.94) | False (0.89) | False (0.62) | True (0.56) | True (0.53) | False (0.89) | False (0.90) | False (0.94) | False (0.96) | False (0.92) | pcb4-normal-0306 |
| candle-normal-0545 | False | False (0.90) | False (0.91) | False (0.94) | False (0.84) | False (0.98) | False (0.98) | False (0.90) | False (0.93) | False (0.97) | False (0.83) | False (0.74) | True (0.50) | False (0.51) | False (0.84) | False (0.92) | False (0.94) | False (0.98) | False (0.99) | candle-normal-0545 |
| cashew-normal-384 | False | False (0.92) | False (0.91) | False (0.70) | False (0.86) | False (0.99) | False (0.99) | False (0.86) | False (0.93) | False (0.90) | False (0.83) | False (0.76) | False (0.53) | True (0.52) | False (0.89) | False (0.93) | False (0.91) | False (0.98) | False (0.97) | cashew-normal-384 |
| pcb1-anomaly-061 | True | False (0.93) | False (0.95) | False (0.87) | False (0.81) | False (0.92) | False (0.99) | False (0.86) | False (0.91) | False (0.92) | False (0.88) | False (0.66) | True (0.66) | True (0.66) | False (0.89) | False (0.87) | False (0.92) | False (0.95) | False (0.94) | pcb1-anomaly-061 |
| pcb1-normal-0730 | False | False (0.92) | False (0.92) | False (0.91) | False (0.88) | False (0.93) | False (0.96) | False (0.89) | False (0.90) | False (0.94) | False (0.87) | False (0.71) | True (0.54) | True (0.55) | False (0.86) | False (0.90) | False (0.94) | False (0.97) | False (0.99) | pcb1-normal-0730 |
| pcb3-anomaly-096 | True | False (0.86) | False (0.92) | False (0.90) | False (0.81) | False (0.90) | False (0.99) | False (0.87) | False (0.85) | False (0.93) | False (0.87) | False (0.70) | True (0.51) | False (0.51) | False (0.87) | False (0.87) | False (0.91) | False (0.95) | False (0.97) | pcb3-anomaly-096 |
| pcb4-normal-0400 | False | False (0.89) | False (0.88) | False (0.91) | False (0.84) | False (0.95) | False (0.98) | False (0.84) | False (0.83) | False (0.94) | False (0.86) | False (0.63) | False (0.53) | True (0.50) | False (0.87) | False (0.92) | False (0.94) | False (0.95) | False (0.99) | pcb4-normal-0400 |
| pcb4-normal-0629 | False | False (0.90) | False (0.91) | False (0.89) | False (0.84) | False (0.91) | False (0.99) | False (0.84) | False (0.87) | False (0.94) | False (0.86) | False (0.61) | True (0.63) | True (0.62) | False (0.88) | False (0.86) | False (0.89) | False (0.94) | False (0.93) | pcb4-normal-0629 |
| candle-normal-0552 | False | False (0.87) | False (0.92) | False (0.92) | False (0.88) | False (0.94) | False (0.95) | False (0.89) | False (0.90) | False (0.96) | False (0.79) | False (0.73) | True (0.52) | True (0.53) | False (0.88) | False (0.92) | False (0.86) | False (0.96) | False (0.98) | candle-normal-0552 |
| candle-normal-0985 | False | False (0.89) | False (0.89) | False (0.91) | False (0.86) | False (0.97) | False (0.98) | False (0.91) | False (0.93) | False (0.97) | False (0.85) | False (0.79) | True (0.53) | True (0.51) | False (0.88) | False (0.89) | False (0.94) | False (0.97) | False (0.98) | candle-normal-0985 |
| pcb1-anomaly-026 | True | False (0.94) | False (0.95) | False (0.86) | False (0.81) | False (0.96) | False (0.98) | False (0.91) | False (0.87) | False (0.93) | False (0.90) | True (0.60) | True (0.64) | True (0.60) | False (0.91) | False (0.89) | False (0.92) | False (0.97) | False (0.98) | pcb1-anomaly-026 |
| macaroni2-anomaly-045 | True | False (0.53) | True (0.82) | True (0.72) | True (0.69) | False (0.85) | False (0.73) | False (0.82) | True (0.52) | True (0.58) | True (0.69) | False (0.69) | True (0.57) | True (0.59) | False (0.72) | True (0.98) | True (0.57) | False (0.70) | True (0.55) | macaroni2-anomaly-045 |
