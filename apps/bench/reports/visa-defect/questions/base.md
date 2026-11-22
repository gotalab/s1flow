# visa-defect

2026-11-17 · 168 labelled dev cases (True 84, False 84) · split: stratified k-fold (no test case among these: CV numbers only) · source: VisA (Amazon, CC BY 4.0), test split: 10 defective and 10 good photos per item, 12 items

gemini-decision@google has the highest recall at 10% false alarms or fewer, 69% [59, 79] (false alarms 9.5%) (API cost $1.25 per 10k, p99 1465ms). Its interval overlaps with joey@openrouter, decision-1.1@openrouter, span@openrouter, d1-ultra@openrouter, d1.2-ultra, elephant@openrouter, d1@vercel, d1.1@openrouter, reflex@openrouter, jev:1.14, clef@openrouter, d1.2, jev, decider-flash@openrouter, luna@decisions: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is gemini-decision@google's, 76% [69, 82].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 168 | 58.3% [51, 65] | 0.29 | 0.76 | 0.23 | 2% [0, 4] | 66.7% (13.5%) | 0.0% (0/168) | 0/168 |
| clef-omni@openrouter | 168 | 55.4% [48, 63] | 0.27 | 0.69 | 0.27 | 1% [0, 2] | 100.0% (5.0%) | 0.0% (0/168) | 0/168 |
| clef@openrouter | 168 | 66.1% [59, 73] | 0.53 | 0.74 | 0.11 | 2% [0, 4] | 100.0% (36.8%) | 0.0% (0/168) | 0/168 |
| d1-ultra@openrouter | 168 | 69.0% [62, 76] | 0.57 | 0.84 | 0.07 | 9% [5, 13] | 93.3% (72.1%) | 0.0% (0/168) | 0/168 |
| d1.1@openrouter | 168 | 56.0% [49, 64] | 0.21 | 0.79 | 0.30 | 9% [5, 13] | 93.3% (72.1%) | 0.0% (0/168) | 0/168 |
| d1.2 | 168 | 56.0% [49, 63] | 0.21 | 0.81 | 0.25 | 4% [1, 7] | 85.7% (47.9%) | 0.0% (0/168) | 0/168 |
| d1.2-ultra | 168 | 63.7% [57, 71] | 0.43 | 0.84 | 0.13 | 7% [3, 11] | 90.9% (63.6%) | 0.0% (0/168) | 0/168 |
| d1@vercel | 168 | 61.9% [55, 69] | 0.38 | 0.78 | 0.26 | 1% [0, 2] | 0.0% (0.0%) | 0.0% (0/168) | 0/168 |
| decider-flash@openrouter | 168 | 57.1% [50, 64] | 0.25 | 0.81 | 0.26 | 12% [8, 18] | 85.7% (67.1%) | 0.0% (0/168) | 0/168 |
| decider@openrouter | 168 | 59.5% [52, 67] | 0.32 | 0.78 | 0.20 | 12% [7, 17] | 95.0% (78.4%) | 0.0% (0/168) | 0/168 |
| decision-1.1@openrouter | 168 | 62.5% [55, 70] | 0.42 | 0.82 | 0.13 | 1% [0, 2] | 0.0% (0.0%) | 0.0% (0/168) | 0/168 |
| drex-max@openrouter | 168 | 63.1% [56, 70] | 0.47 | 0.76 | 0.19 | 4% [2, 7] | 85.7% (47.9%) | 0.0% (0/168) | 0/168 |
| elephant@openrouter | 168 | 73.8% [68, 80] | 0.68 | 0.81 | 0.04 | 4% [1, 7] | 100.0% (65.2%) | 0.0% (0/168) | 0/168 |
| gemini-decision@google | 168 | 75.6% [69, 82] | 0.68 | 0.82 | 0.09 | 8% [4, 12] | 84.6% (59.0%) | 0.0% (0/168) | 0/168 |
| jev | 168 | 73.2% [67, 80] | 0.76 | 0.81 | 0.10 | 23% [16, 29] | 92.1% (80.8%) | 0.0% (0/168) | 0/168 |
| jev:1.14 | 168 | 73.8% [67, 80] | 0.76 | 0.82 | 0.15 | 25% [18, 32] | 97.6% (89.2%) | 0.0% (0/168) | 0/168 |
| joey@openrouter | 168 | 72.0% [65, 79] | 0.61 | 0.86 | 0.10 | 10% [5, 14] | 93.8% (73.6%) | 0.0% (0/168) | 0/168 |
| luna@decisions | 168 | 61.3% [54, 68] | 0.41 | 0.83 | 0.23 | 21% [15, 27] | 94.4% (83.5%) | 0.0% (0/168) | 0/168 |
| mammoth@openrouter | 168 | 63.1% [56, 71] | 0.42 | 0.80 | 0.20 | 2% [0, 4] | 66.7% (13.5%) | 0.0% (0/168) | 0/168 |
| reflex@openrouter | 168 | 63.7% [57, 71] | 0.43 | 0.80 | 0.21 | 2% [1, 5] | 75.0% (24.9%) | 0.0% (0/168) | 0/168 |
| span@openrouter | 168 | 61.9% [55, 69] | 0.42 | 0.83 | 0.28 | 7% [3, 11] | 81.8% (53.0%) | 0.0% (0/168) | 0/168 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev = jev-1.14.0; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | recall at 10% false alarms or fewer | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| gemini-decision@google = | 69% [59, 79] (false alarms 9.5%) | 80% [74, 86] | 0.41 | met |
| joey@openrouter = | 68% [58, 78] (false alarms 10.7%) | 79% [73, 84] | 0.24 | met |
| decision-1.1@openrouter = | 64% [53, 74] (false alarms 9.5%) | 77% [71, 83] | 0.31 | met |
| span@openrouter = | 64% [54, 73] (false alarms 9.5%) | 77% [71, 83] | 0.09 | met |
| d1-ultra@openrouter = | 63% [53, 73] (false alarms 10.7%) | 76% [70, 83] | 0.33 | met |
| d1.2-ultra = | 63% [52, 73] (false alarms 10.7%) | 76% [70, 82] | 0.32 | met |
| elephant@openrouter = | 61% [50, 71] (false alarms 8.3%) | 76% [70, 82] | 0.42 | met |
| d1@vercel = | 58% [48, 69] (false alarms 7.1%) | 76% [69, 82] | 0.14 | met |
| d1.1@openrouter = | 60% [49, 69] (false alarms 9.5%) | 75% [68, 82] | 0.14 | met |
| reflex@openrouter = | 57% [47, 67] (false alarms 9.5%) | 74% [67, 80] | 0.22 | met |
| jev:1.14 = | 52% [41, 63] (false alarms 7.1%) | 73% [65, 79] | 0.74 | met |
| clef@openrouter = | 54% [43, 64] (false alarms 9.5%) | 72% [65, 78] | 0.37 | met |
| d1.2 = | 52% [41, 63] (false alarms 8.3%) | 72% [65, 79] | 0.24 | met |
| jev = | 52% [41, 63] (false alarms 8.3%) | 72% [65, 79] | 0.74 | met |
| decider-flash@openrouter = | 52% [40, 63] (false alarms 9.5%) | 71% [64, 78] | 0.19 | met |
| luna@decisions = | 52% [41, 62] (false alarms 10.7%) | 71% [64, 77] | 0.20 | met |
| drex-max@openrouter | 46% [36, 56] (false alarms 8.3%) | 69% [62, 76] | 0.34 | met |
| clef-flash@openrouter | 45% [35, 55] (false alarms 8.3%) | 68% [61, 76] | 0.26 | met |
| mammoth@openrouter | 45% [34, 55] (false alarms 10.7%) | 67% [60, 74] | 0.28 | met |
| decider@openrouter | 38% [28, 48] (false alarms 10.7%) | 64% [57, 71] | 0.29 | met |
| clef-omni@openrouter | 37% [27, 47] (false alarms 10.7%) | 63% [56, 70] | 0.27 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 168 | 392 ms | 760 ms | 1304 ms | 1481 ms | 3.3 | 0 | 4 | $0.16 | billed |  |
| clef-omni@openrouter | 168 | 348 ms | 582 ms | 829 ms | 868 ms | 2.4 | 0 | 4 | $0.93 | billed |  |
| clef@openrouter | 168 | 437 ms | 933 ms | 3684 ms | 5579 ms | 8.4 | 0 | 4 | $1.33 | billed |  |
| d1-ultra@openrouter | 168 | 722 ms | 1062 ms | 1411 ms | 1460 ms | 2.0 | 0 | 4 | $0.32 | billed |  |
| d1.1@openrouter | 168 | 856 ms | 1045 ms | 1419 ms | 1527 ms | 1.7 | 0 | 4 | $0.15 | billed |  |
| d1.2 | 168 | 294 ms | 582 ms | 1281 ms | 3775 ms | 4.4 | 0 | 4 | $0.15 | billed |  |
| d1.2-ultra | 168 | 269 ms | 435 ms | 908 ms | 1353 ms | 3.4 | 0 | 4 | $0.32 | billed |  |
| d1@vercel | 168 | 397 ms | 558 ms | 942 ms | 951 ms | 2.4 | 0 | 4 | $0.15 | billed |  |
| decider-flash@openrouter | 168 | 205 ms | 269 ms | 417 ms | 432 ms | 2.0 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 168 | 332 ms | 487 ms | 855 ms | 3986 ms | 2.6 | 0 | 4 | $0.12 | billed |  |
| decision-1.1@openrouter | 168 | 399 ms | 458 ms | 901 ms | 981 ms | 2.3 | 0 | 4 | $0.15 | billed |  |
| drex-max@openrouter | 168 | 439 ms | 764 ms | 1205 ms | 1889 ms | 2.7 | 0 | 4 | $0.35 | billed |  |
| elephant@openrouter | 168 | 264 ms | 330 ms | 461 ms | 606 ms | 1.7 | 0 | 4 | $0.23 | billed |  |
| gemini-decision@google | 168 | 653 ms | 961 ms | 1465 ms | 1917 ms | 2.2 | 0 | 4 | $1.25 | estimated | ○ |
| jev | 168 | 138 ms | 234 ms | 429 ms | 690 ms | 3.1 | 0 | 4 | $0.65 | estimated |  |
| jev:1.14 | 168 | 134 ms | 198 ms | 418 ms | 872 ms | 3.1 | 0 | 4 | $0.65 | estimated |  |
| joey@openrouter | 168 | 255 ms | 317 ms | 437 ms | 514 ms | 1.7 | 0 | 4 | $0.07 | billed | ○ |
| luna@decisions | 168 | 263 ms | 637 ms | 814 ms | 878 ms | 3.1 | 0 | 4 | $0.66 | estimated |  |
| mammoth@openrouter | 168 | 286 ms | 347 ms | 480 ms | 604 ms | 1.7 | 0 | 4 | $0.67 | billed |  |
| reflex@openrouter | 168 | 689 ms | 877 ms | 951 ms | 1159 ms | 1.4 | 0 | 4 | $0.25 | billed |  |
| span@openrouter | 168 | 650 ms | 879 ms | 1086 ms | 1140 ms | 1.7 | 0 | 4 | $0.04 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev (list price of 2026-10-03), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0027 | 19 s (estimated, 168 calls) | 19 min | 4 |
| clef-omni@openrouter | $0.02 | 17 s (estimated, 168 calls) | 16 min | 4 |
| clef@openrouter | $0.02 | 26 s (estimated, 168 calls) | 25 min | 4 |
| d1-ultra@openrouter | $0.0054 | 32 s (estimated, 168 calls) | 32 min | 4 |
| d1.1@openrouter | $0.0026 | 36 s (estimated, 168 calls) | 36 min | 4 |
| d1.2 | $0.0026 | 14 s (estimated, 168 calls) | 14 min | 4 |
| d1.2-ultra | $0.0054 | 12 s (estimated, 168 calls) | 12 min | 4 |
| d1@vercel | $0.0026 | 18 s (estimated, 168 calls) | 18 min | 4 |
| decider-flash@openrouter | $0.0010 | 9 s (estimated, 168 calls) | 9 min | 4 |
| decider@openrouter | $0.0019 | 16 s (estimated, 168 calls) | 16 min | 4 |
| decision-1.1@openrouter | $0.0025 | 17 s (estimated, 168 calls) | 17 min | 4 |
| drex-max@openrouter | $0.0058 | 21 s (estimated, 168 calls) | 21 min | 4 |
| elephant@openrouter | $0.0039 | 11 s (estimated, 168 calls) | 11 min | 4 |
| gemini-decision@google | $0.02 | 30 s (estimated, 168 calls) | 29 min | 4 |
| jev | $0.01 | 7 s (estimated, 168 calls) | 7 min | 4 |
| jev:1.14 | $0.01 | 6 s (estimated, 168 calls) | 6 min | 4 |
| joey@openrouter | $0.0011 | 11 s (estimated, 168 calls) | 11 min | 4 |
| luna@decisions | $0.01 | 14 s (estimated, 168 calls) | 14 min | 4 |
| mammoth@openrouter | $0.01 | 12 s (estimated, 168 calls) | 12 min | 4 |
| reflex@openrouter | $0.0042 | 29 s (estimated, 168 calls) | 29 min | 4 |
| span@openrouter | $0.0007 | 28 s (estimated, 168 calls) | 28 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 58.3% | 72.0% | 27 | 20 | 0.15 | 0.15 |
| clef-omni@openrouter | 55.4% | 64.3% | 39 | 21 | 0.15 | 0.15 |
| clef@openrouter | 66.1% | 71.4% | 37 | 11 | 0.35 | 0.35 |
| d1-ultra@openrouter | 69.0% | 75.6% | 30 | 11 | 0.30 | 0.30 |
| d1.1@openrouter | 56.0% | 76.2% | 34 | 6 | 0.15 | 0.15 |
| d1.2 | 56.0% | 73.2% | 28 | 17 | 0.20 | 0.20 |
| d1.2-ultra | 63.7% | 78.6% | 27 | 9 | 0.30 | 0.30 |
| d1@vercel | 61.9% | 75.6% | 36 | 5 | 0.15 | 0.15 |
| decider-flash@openrouter | 57.1% | 70.8% | 42 | 7 | 0.20 | 0.20 |
| decider@openrouter | 59.5% | 70.2% | 16 | 34 | 0.15 | 0.15 |
| decision-1.1@openrouter | 62.5% | 72.6% | 32 | 14 | 0.30 | 0.30 |
| drex-max@openrouter | 63.1% | 73.2% | 34 | 11 | 0.25 | 0.25 |
| elephant@openrouter | 73.8% | 78.0% | 27 | 10 | 0.35 | 0.35 |
| gemini-decision@google | 75.6% | 80.4% | 32 | 1 | 0.45 | 0.45 |
| jev | 73.2% | 74.4% | 24 | 19 | 0.60 | 0.60 |
| jev:1.14 | 73.8% | 75.0% | 22 | 20 | 0.55 | 0.55 |
| joey@openrouter | 72.0% | 78.6% | 22 | 14 | 0.20 | 0.20 |
| luna@decisions | 61.3% | 70.8% | 29 | 20 | 0.15 | 0.15 |
| mammoth@openrouter | 63.1% | 73.2% | 30 | 15 | 0.20 | 0.15 |
| reflex@openrouter | 63.7% | 75.6% | 25 | 16 | 0.15 | 0.15 |
| span@openrouter | 61.9% | 78.6% | 31 | 5 | 0.10 | 0.10 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 14 (17%) | 46 (55%) |
| 0.15 | 27 (32%) | 20 (24%) |
| 0.20 | 36 (43%) | 16 (19%) |
| 0.30 | 51 (61%) | 5 (6%) |
| 0.40 | 63 (75%) | 1 (1%) |
| 0.50 | 70 (83%) | 0 (0%) |
| 0.60 | 77 (92%) | 0 (0%) |
| 0.70 | 79 (94%) | 0 (0%) |
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
| 0.10 | 9 (11%) | 63 (75%) |
| 0.20 | 19 (23%) | 43 (51%) |
| 0.30 | 31 (37%) | 21 (25%) |
| 0.35 | 37 (44%) | 11 (13%) |
| 0.40 | 44 (52%) | 8 (10%) |
| 0.50 | 52 (62%) | 5 (6%) |
| 0.60 | 59 (70%) | 5 (6%) |
| 0.70 | 66 (79%) | 3 (4%) |
| 0.80 | 74 (88%) | 0 (0%) |
| 0.90 | 82 (98%) | 0 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 81 (96%) |
| 0.20 | 12 (14%) | 36 (43%) |
| 0.30 | 26 (31%) | 11 (13%) |
| 0.40 | 37 (44%) | 4 (5%) |
| 0.50 | 50 (60%) | 2 (2%) |
| 0.60 | 55 (65%) | 1 (1%) |
| 0.70 | 63 (75%) | 0 (0%) |
| 0.80 | 74 (88%) | 0 (0%) |
| 0.90 | 80 (95%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 24 (29%) | 30 (36%) |
| 0.15 | 34 (40%) | 6 (7%) |
| 0.20 | 47 (56%) | 1 (1%) |
| 0.30 | 59 (70%) | 0 (0%) |
| 0.40 | 73 (87%) | 0 (0%) |
| 0.50 | 74 (88%) | 0 (0%) |
| 0.60 | 75 (89%) | 0 (0%) |
| 0.70 | 79 (94%) | 0 (0%) |
| 0.80 | 83 (99%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (d1.2)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 8 (10%) | 55 (65%) |
| 0.20 | 28 (33%) | 12 (14%) |
| 0.30 | 53 (63%) | 3 (4%) |
| 0.40 | 69 (82%) | 0 (0%) |
| 0.50 | 74 (88%) | 0 (0%) |
| 0.60 | 79 (94%) | 0 (0%) |
| 0.70 | 80 (95%) | 0 (0%) |
| 0.80 | 83 (99%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (d1.2-ultra)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 71 (85%) |
| 0.20 | 13 (15%) | 33 (39%) |
| 0.30 | 27 (32%) | 9 (11%) |
| 0.40 | 48 (57%) | 4 (5%) |
| 0.50 | 61 (73%) | 0 (0%) |
| 0.60 | 67 (80%) | 0 (0%) |
| 0.70 | 76 (90%) | 0 (0%) |
| 0.80 | 78 (93%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 28 (33%) | 20 (24%) |
| 0.15 | 36 (43%) | 5 (6%) |
| 0.20 | 41 (49%) | 3 (4%) |
| 0.30 | 53 (63%) | 0 (0%) |
| 0.40 | 58 (69%) | 0 (0%) |
| 0.50 | 64 (76%) | 0 (0%) |
| 0.60 | 67 (80%) | 0 (0%) |
| 0.70 | 72 (86%) | 0 (0%) |
| 0.80 | 77 (92%) | 0 (0%) |
| 0.90 | 82 (98%) | 0 (0%) |

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
| 0.10 | 5 (6%) | 60 (71%) |
| 0.15 | 16 (19%) | 34 (40%) |
| 0.20 | 32 (38%) | 23 (27%) |
| 0.30 | 52 (62%) | 8 (10%) |
| 0.40 | 57 (68%) | 3 (4%) |
| 0.50 | 68 (81%) | 0 (0%) |
| 0.60 | 73 (87%) | 0 (0%) |
| 0.70 | 79 (94%) | 0 (0%) |
| 0.80 | 83 (99%) | 0 (0%) |
| 0.90 | 84 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 5 (6%) | 60 (71%) |
| 0.20 | 19 (23%) | 26 (31%) |
| 0.30 | 28 (33%) | 11 (13%) |
| 0.40 | 43 (51%) | 2 (2%) |
| 0.50 | 61 (73%) | 2 (2%) |
| 0.60 | 73 (87%) | 0 (0%) |
| 0.70 | 77 (92%) | 0 (0%) |
| 0.80 | 81 (96%) | 0 (0%) |
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

## Misses and false alarms by threshold (gemini-decision@google)

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
| 0.20 | 0 (0%) | 84 (100%) |
| 0.30 | 4 (5%) | 74 (88%) |
| 0.40 | 10 (12%) | 54 (64%) |
| 0.50 | 14 (17%) | 31 (37%) |
| 0.60 | 25 (30%) | 15 (18%) |
| 0.70 | 36 (43%) | 12 (14%) |
| 0.80 | 46 (55%) | 2 (2%) |
| 0.90 | 72 (86%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 84 (100%) |
| 0.20 | 0 (0%) | 83 (99%) |
| 0.30 | 5 (6%) | 73 (87%) |
| 0.40 | 10 (12%) | 49 (58%) |
| 0.50 | 15 (18%) | 29 (35%) |
| 0.55 | 17 (20%) | 22 (26%) |
| 0.60 | 26 (31%) | 14 (17%) |
| 0.70 | 36 (43%) | 12 (14%) |
| 0.80 | 44 (52%) | 1 (1%) |
| 0.90 | 71 (85%) | 0 (0%) |

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
| 0.10 | 23 (27%) | 25 (30%) |
| 0.15 | 25 (30%) | 16 (19%) |
| 0.20 | 36 (43%) | 10 (12%) |
| 0.30 | 48 (57%) | 3 (4%) |
| 0.40 | 54 (64%) | 1 (1%) |
| 0.50 | 61 (73%) | 0 (0%) |
| 0.60 | 67 (80%) | 0 (0%) |
| 0.70 | 71 (85%) | 0 (0%) |
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

**clef-flash@openrouter** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-034 | True | False | 0.94 | capsules-anomaly-034 |
| capsules-anomaly-089 | True | False | 0.94 | capsules-anomaly-089 |
| pcb1-anomaly-026 | True | False | 0.94 | pcb1-anomaly-026 |
| pcb1-anomaly-061 | True | False | 0.94 | pcb1-anomaly-061 |
| capsules-anomaly-003 | True | False | 0.94 | capsules-anomaly-003 |
| pcb1-anomaly-099 | True | False | 0.93 | pcb1-anomaly-099 |
| capsules-anomaly-092 | True | False | 0.93 | capsules-anomaly-092 |
| pcb3-anomaly-035 | True | False | 0.93 | pcb3-anomaly-035 |

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

**clef@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-075 | True | False | 0.95 | capsules-anomaly-075 |
| capsules-anomaly-034 | True | False | 0.95 | capsules-anomaly-034 |
| capsules-anomaly-089 | True | False | 0.95 | capsules-anomaly-089 |
| capsules-anomaly-092 | True | False | 0.93 | capsules-anomaly-092 |
| capsules-anomaly-003 | True | False | 0.93 | capsules-anomaly-003 |
| pcb3-anomaly-035 | True | False | 0.92 | pcb3-anomaly-035 |
| pcb3-anomaly-079 | True | False | 0.92 | pcb3-anomaly-079 |
| pcb3-anomaly-096 | True | False | 0.91 | pcb3-anomaly-096 |

**d1.1@openrouter** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| cashew-anomaly-086 | True | False | 0.96 | cashew-anomaly-086 |
| capsules-anomaly-034 | True | False | 0.95 | capsules-anomaly-034 |
| pcb3-anomaly-079 | True | False | 0.95 | pcb3-anomaly-079 |
| macaroni1-anomaly-090 | True | False | 0.94 | macaroni1-anomaly-090 |
| pcb1-anomaly-061 | True | False | 0.94 | pcb1-anomaly-061 |
| cashew-anomaly-070 | True | False | 0.94 | cashew-anomaly-070 |
| capsules-anomaly-092 | True | False | 0.94 | capsules-anomaly-092 |
| candle-anomaly-008 | True | False | 0.94 | candle-anomaly-008 |

**d1.2** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| cashew-anomaly-086 | True | False | 0.94 | cashew-anomaly-086 |
| pcb1-anomaly-026 | True | False | 0.93 | pcb1-anomaly-026 |
| macaroni1-anomaly-090 | True | False | 0.92 | macaroni1-anomaly-090 |
| cashew-anomaly-067 | True | False | 0.92 | cashew-anomaly-067 |
| capsules-anomaly-089 | True | False | 0.91 | capsules-anomaly-089 |
| capsules-anomaly-034 | True | False | 0.91 | capsules-anomaly-034 |
| pcb3-anomaly-079 | True | False | 0.91 | pcb3-anomaly-079 |
| pcb1-anomaly-061 | True | False | 0.90 | pcb1-anomaly-061 |

**d1.2-ultra** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-075 | True | False | 0.91 | capsules-anomaly-075 |

**d1@vercel** (28)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-034 | True | False | 1.00 | capsules-anomaly-034 |
| capsules-anomaly-003 | True | False | 0.99 | capsules-anomaly-003 |
| capsules-anomaly-075 | True | False | 0.99 | capsules-anomaly-075 |
| pcb1-anomaly-026 | True | False | 0.99 | pcb1-anomaly-026 |
| capsules-anomaly-089 | True | False | 0.99 | capsules-anomaly-089 |
| pcb1-anomaly-061 | True | False | 0.99 | pcb1-anomaly-061 |
| pcb3-anomaly-079 | True | False | 0.99 | pcb3-anomaly-079 |
| pcb3-anomaly-096 | True | False | 0.98 | pcb3-anomaly-096 |

**decider-flash@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| fryum-anomaly-099 | True | False | 0.91 | fryum-anomaly-099 |
| pcb1-anomaly-026 | True | False | 0.91 | pcb1-anomaly-026 |
| macaroni1-anomaly-090 | True | False | 0.90 | macaroni1-anomaly-090 |

**decider@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| pcb3-anomaly-079 | True | False | 0.91 | pcb3-anomaly-079 |
| capsules-anomaly-075 | True | False | 0.91 | capsules-anomaly-075 |
| pcb1-anomaly-061 | True | False | 0.91 | pcb1-anomaly-061 |
| macaroni1-anomaly-062 | True | False | 0.90 | macaroni1-anomaly-062 |
| capsules-anomaly-092 | True | False | 0.90 | capsules-anomaly-092 |

**decision-1.1@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-034 | True | False | 0.95 | capsules-anomaly-034 |
| cashew-anomaly-086 | True | False | 0.94 | cashew-anomaly-086 |
| chewinggum-anomaly-037 | True | False | 0.93 | chewinggum-anomaly-037 |
| capsules-anomaly-075 | True | False | 0.90 | capsules-anomaly-075 |
| pcb1-anomaly-046 | True | False | 0.90 | pcb1-anomaly-046 |

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
| capsules-anomaly-034 | True | False | 0.90 | capsules-anomaly-034 |
| capsules-anomaly-075 | True | False | 0.90 | capsules-anomaly-075 |
| capsules-anomaly-092 | True | False | 0.90 | capsules-anomaly-092 |

**mammoth@openrouter** (16)

| id | label | answer | probability | case |
|---|---|---|---|---|
| capsules-anomaly-034 | True | False | 0.97 | capsules-anomaly-034 |
| capsules-anomaly-089 | True | False | 0.96 | capsules-anomaly-089 |
| capsules-anomaly-003 | True | False | 0.96 | capsules-anomaly-003 |
| capsules-anomaly-075 | True | False | 0.96 | capsules-anomaly-075 |
| pcb3-anomaly-014 | True | False | 0.95 | pcb3-anomaly-014 |
| capsules-anomaly-092 | True | False | 0.95 | capsules-anomaly-092 |
| macaroni1-anomaly-090 | True | False | 0.94 | macaroni1-anomaly-090 |
| macaroni1-anomaly-062 | True | False | 0.94 | macaroni1-anomaly-062 |

**reflex@openrouter** (23)

| id | label | answer | probability | case |
|---|---|---|---|---|
| pcb3-anomaly-079 | True | False | 0.97 | pcb3-anomaly-079 |
| capsules-anomaly-075 | True | False | 0.97 | capsules-anomaly-075 |
| pcb3-anomaly-035 | True | False | 0.97 | pcb3-anomaly-035 |
| pcb3-anomaly-001 | True | False | 0.96 | pcb3-anomaly-001 |
| pcb1-anomaly-026 | True | False | 0.96 | pcb1-anomaly-026 |
| capsules-anomaly-089 | True | False | 0.96 | capsules-anomaly-089 |
| capsules-anomaly-034 | True | False | 0.96 | capsules-anomaly-034 |
| capsules-anomaly-092 | True | False | 0.96 | capsules-anomaly-092 |

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


## Cases the models disagree on (12 of 101)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev | jev:1.14 | joey@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pcb1-anomaly-026 | True | False (0.94) | False (0.95) | False (0.90) | False (0.77) | False (0.93) | False (0.93) | False (0.83) | False (0.99) | False (0.91) | False (0.87) | False (0.80) | False (0.93) | False (0.90) | True (0.60) | True (0.64) | True (0.58) | False (0.91) | False (0.89) | False (0.92) | False (0.96) | False (0.98) | pcb1-anomaly-026 |
| fryum-anomaly-051 | True | True (0.62) | True (0.79) | True (0.88) | True (0.84) | True (0.58) | False (0.51) | True (0.86) | True (0.84) | True (0.70) | True (0.85) | True (0.88) | True (0.96) | True (0.90) | True (0.92) | True (0.92) | True (0.92) | True (0.99) | True (0.91) | True (0.89) | True (0.93) | True (0.94) | fryum-anomaly-051 |
| pcb4-normal-0629 | False | False (0.91) | False (0.91) | False (0.90) | False (0.84) | False (0.92) | False (0.85) | False (0.74) | False (0.99) | False (0.84) | False (0.87) | False (0.65) | False (0.94) | False (0.86) | False (0.61) | True (0.57) | True (0.61) | False (0.88) | False (0.86) | False (0.89) | False (0.94) | False (0.93) | pcb4-normal-0629 |
| pcb4-normal-0400 | False | False (0.91) | False (0.88) | False (0.90) | False (0.84) | False (0.93) | False (0.84) | False (0.72) | False (0.99) | False (0.84) | False (0.83) | False (0.77) | False (0.94) | False (0.86) | False (0.63) | True (0.57) | True (0.52) | False (0.87) | False (0.92) | False (0.94) | False (0.92) | False (0.99) | pcb4-normal-0400 |
| pcb1-normal-0730 | False | False (0.91) | False (0.92) | False (0.85) | False (0.87) | False (0.92) | False (0.92) | False (0.82) | False (0.95) | False (0.89) | False (0.90) | False (0.91) | False (0.94) | False (0.87) | False (0.71) | True (0.56) | True (0.55) | False (0.86) | False (0.90) | False (0.94) | False (0.96) | False (0.99) | pcb1-normal-0730 |
| pcb1-anomaly-061 | True | False (0.94) | False (0.95) | False (0.88) | False (0.83) | False (0.94) | False (0.90) | False (0.81) | False (0.99) | False (0.86) | False (0.91) | False (0.77) | False (0.92) | False (0.88) | False (0.66) | True (0.66) | True (0.67) | False (0.89) | False (0.87) | False (0.92) | False (0.96) | False (0.94) | pcb1-anomaly-061 |
| candle-normal-0552 | False | False (0.90) | False (0.92) | False (0.93) | False (0.86) | False (0.95) | False (0.91) | False (0.88) | False (0.95) | False (0.89) | False (0.90) | False (0.92) | False (0.96) | False (0.79) | False (0.73) | True (0.53) | False (0.52) | False (0.88) | False (0.92) | False (0.86) | False (0.95) | False (0.98) | candle-normal-0552 |
| candle-normal-0985 | False | False (0.91) | False (0.89) | False (0.93) | False (0.89) | False (0.98) | False (0.94) | False (0.92) | False (0.98) | False (0.91) | False (0.93) | False (0.91) | False (0.97) | False (0.85) | False (0.79) | True (0.51) | True (0.50) | False (0.88) | False (0.89) | False (0.94) | False (0.96) | False (0.98) | candle-normal-0985 |
| cashew-normal-384 | False | False (0.92) | False (0.91) | False (0.72) | False (0.87) | False (0.98) | False (0.96) | False (0.95) | False (0.98) | False (0.86) | False (0.93) | False (0.92) | False (0.90) | False (0.83) | False (0.76) | True (0.65) | False (0.54) | False (0.89) | False (0.93) | False (0.91) | False (0.98) | False (0.97) | cashew-normal-384 |
| pcb4-normal-0306 | False | False (0.92) | False (0.89) | False (0.92) | False (0.79) | False (0.97) | False (0.92) | False (0.75) | False (0.98) | False (0.84) | False (0.85) | False (0.69) | False (0.94) | False (0.89) | False (0.62) | True (0.53) | True (0.56) | False (0.89) | False (0.90) | False (0.94) | False (0.97) | False (0.92) | pcb4-normal-0306 |
| pcb4-normal-0174 | False | False (0.91) | False (0.89) | False (0.91) | False (0.74) | False (0.93) | False (0.88) | False (0.78) | False (0.98) | False (0.82) | False (0.86) | False (0.72) | False (0.95) | False (0.81) | False (0.57) | True (0.55) | True (0.59) | False (0.87) | False (0.89) | False (0.93) | False (0.96) | False (0.93) | pcb4-normal-0174 |
| macaroni2-anomaly-045 | True | True (0.51) | True (0.82) | True (0.71) | True (0.71) | False (0.82) | False (0.66) | True (0.65) | False (0.78) | False (0.82) | False (0.52) | False (0.78) | True (0.58) | True (0.69) | False (0.69) | True (0.58) | True (0.57) | False (0.72) | True (0.98) | True (0.57) | False (0.72) | True (0.55) | macaroni2-anomaly-045 |
