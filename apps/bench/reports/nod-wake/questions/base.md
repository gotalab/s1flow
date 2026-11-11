# nod-wake

2026-11-11 · 42 labelled dev cases (True 26, False 16) · split: leave-one-out (no test case among these: CV numbers only) · source: cases.json

No model meets the constraints (mammoth@openrouter: different answered dev cases; automatic comparison refused; d1@vercel: different answered dev cases; automatic comparison refused; gemini-decision@openrouter: different answered dev cases; automatic comparison refused; d1.1@openrouter: different answered dev cases; automatic comparison refused; d1-ultra@openrouter: different answered dev cases; automatic comparison refused; reflex@openrouter: different answered dev cases; automatic comparison refused; decision-1@openrouter: different answered dev cases; automatic comparison refused; drex-max@openrouter: different answered dev cases; automatic comparison refused; decider@openrouter: different answered dev cases; automatic comparison refused; decider-flash@openrouter: different answered dev cases; automatic comparison refused; elephant@openrouter: different answered dev cases; automatic comparison refused; jev:1.14: different answered dev cases; automatic comparison refused; clef@openrouter: different answered dev cases; automatic comparison refused; clef-flash@openrouter: different answered dev cases; automatic comparison refused; luna@decisions: different answered dev cases; automatic comparison refused; clef-omni@openrouter: different answered dev cases; automatic comparison refused; span@openrouter: different answered dev cases; automatic comparison refused; kev@openrouter: different answered dev cases; automatic comparison refused; joey@openrouter: different answered dev cases; automatic comparison refused).

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.97 | 0.13 | 86% [74, 95] | 91.7% (79.8%) | 0/57 | 0/57 |
| clef-omni@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.95 | 0.12 | 79% [64, 90] | 93.9% (82.1%) | 0/57 | 0/57 |
| clef@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.98 | 0.09 | 88% [79, 98] | 94.6% (83.9%) | 0/57 | 0/57 |
| d1-ultra@openrouter | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.08 | 98% [93, 100] | 95.1% (85.4%) | 0/57 | 0/57 |
| d1.1@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.99 | 0.10 | 98% [93, 100] | 95.1% (85.4%) | 0/57 | 0/57 |
| d1@vercel | 42 | 92.9% [83, 100] | 0.95 | 1.00 | 0.07 | 98% [93, 100] | 95.1% (85.4%) | 0/57 | 0/57 |
| decider-flash@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.95 | 0.06 | 90% [81, 98] | 92.1% (80.8%) | 0/57 | 0/57 |
| decider@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.99 | 0.06 | 93% [86, 100] | 92.3% (81.3%) | 0/57 | 0/57 |
| decision-1@openrouter | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.05 | 95% [88, 100] | 92.5% (81.7%) | 0/57 | 0/57 |
| drex-max@openrouter | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.06 | 95% [88, 100] | 95.0% (85.1%) | 0/57 | 0/57 |
| elephant@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.99 | 0.12 | 90% [81, 98] | 97.4% (88.1%) | 0/57 | 0/57 |
| gemini-decision@openrouter | 42 | 97.6% [93, 100] | 0.98 | 1.00 | 0.04 | 98% [93, 100] | 97.6% (88.9%) | 0/57 | 0/57 |
| jev:1.14 | 42 | 92.9% [86, 100] | 0.95 | 0.99 | 0.08 | 88% [79, 98] | 91.9% (80.4%) | 0/57 | 0/57 |
| joey@openrouter | 42 | 73.8% [60, 86] | 0.77 | 0.85 | 0.09 | 36% [21, 50] | 93.3% (72.1%) | 0/57 | 0/57 |
| kev@openrouter | 42 | 81.0% [69, 90] | 0.82 | 0.98 | 0.15 | 52% [36, 67] | 90.9% (74.1%) | 0/57 | 0/57 |
| luna@decisions | 41 | 90.2% [80, 98] | 0.93 | 0.99 | 0.09 | 85% [73, 95] | 97.1% (87.1%) | 1/57 | 0/57 |
| mammoth@openrouter | 42 | 100.0% [100, 100] | 1.00 | 1.00 | 0.11 | 98% [93, 100] | 100.0% (93.0%) | 0/57 | 0/57 |
| reflex@openrouter | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.07 | 98% [93, 100] | 92.7% (82.2%) | 0/57 | 0/57 |
| span@openrouter | 42 | 83.3% [71, 93] | 0.84 | 0.99 | 0.10 | 69% [55, 83] | 93.1% (79.8%) | 0/57 | 0/57 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 10, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| mammoth@openrouter | 98% [93, 100] | 0.000 [0.000, 0.000] | 0.58 | different answered dev cases; automatic comparison refused |
| d1@vercel | 98% [93, 100] | 0.071 [0.000, 0.167] | 0.56 | different answered dev cases; automatic comparison refused |
| gemini-decision@openrouter | 98% [93, 100] | 0.238 [0.000, 0.714] | 0.64 | different answered dev cases; automatic comparison refused |
| d1.1@openrouter | 98% [93, 100] | 0.286 [0.000, 0.786] | 0.59 | different answered dev cases; automatic comparison refused |
| d1-ultra@openrouter | 98% [93, 100] | 0.714 [0.000, 1.667] | 0.56 | different answered dev cases; automatic comparison refused |
| reflex@openrouter | 98% [93, 100] | 0.714 [0.000, 1.667] | 0.61 | different answered dev cases; automatic comparison refused |
| decision-1@openrouter | 95% [88, 100] | 0.714 [0.000, 1.667] | 0.68 | different answered dev cases; automatic comparison refused |
| drex-max@openrouter | 95% [88, 100] | 0.714 [0.000, 1.667] | 0.62 | different answered dev cases; automatic comparison refused |
| decider@openrouter | 93% [86, 100] | 0.714 [0.000, 1.667] | 0.73 | different answered dev cases; automatic comparison refused |
| decider-flash@openrouter | 90% [81, 98] | 0.524 [0.024, 1.262] | 0.68 | different answered dev cases; automatic comparison refused |
| elephant@openrouter | 90% [81, 98] | 0.738 [0.024, 1.667] | 0.55 | different answered dev cases; automatic comparison refused |
| jev:1.14 | 88% [79, 98] | 0.071 [0.000, 0.143] | 0.84 | different answered dev cases; automatic comparison refused |
| clef@openrouter | 88% [79, 98] | 0.524 [0.024, 1.239] | 0.54 | different answered dev cases; automatic comparison refused |
| clef-flash@openrouter | 86% [74, 95] | 0.500 [0.000, 1.238] | 0.53 | different answered dev cases; automatic comparison refused |
| luna@decisions | 85% [73, 95] | 0.098 [0.024, 0.195] | 0.77 | different answered dev cases; automatic comparison refused |
| clef-omni@openrouter | 79% [64, 90] | 0.738 [0.024, 1.667] | 0.68 | different answered dev cases; automatic comparison refused |
| span@openrouter | 69% [55, 83] | 1.667 [0.714, 2.857] | 0.95 | different answered dev cases; automatic comparison refused |
| kev@openrouter | 52% [36, 67] | 1.905 [0.952, 3.095] | 0.62 | different answered dev cases; automatic comparison refused |
| joey@openrouter | 36% [21, 50] | 1.976 [0.976, 3.190] | 0.76 | different answered dev cases; automatic comparison refused |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 42 | 373 ms | 467 ms | 1079 ms | 1222 ms | 2.9 | 0 | 4 | $0.09 | billed |  |
| clef-omni@openrouter | 42 | 306 ms | 393 ms | 454 ms | 469 ms | 1.5 | 0 | 4 | $0.67 | billed |  |
| clef@openrouter | 42 | 456 ms | 613 ms | 1031 ms | 1138 ms | 2.3 | 0 | 4 | $0.81 | billed |  |
| d1-ultra@openrouter | 42 | 329 ms | 414 ms | 670 ms | 690 ms | 2.0 | 0 | 4 | $0.13 | billed |  |
| d1.1@openrouter | 42 | 290 ms | 456 ms | 1040 ms | 1203 ms | 3.6 | 0 | 4 | $0.06 | billed |  |
| d1@vercel | 42 | 247 ms | 455 ms | 544 ms | 563 ms | 2.2 | 0 | 4 | $0.06 | billed | ○ |
| decider-flash@openrouter | 42 | 144 ms | 265 ms | 291 ms | 297 ms | 2.0 | 0 | 4 | $0.03 | billed | ○ |
| decider@openrouter | 42 | 342 ms | 431 ms | 1000 ms | 1196 ms | 2.9 | 0 | 4 | $0.07 | billed |  |
| decision-1@openrouter | 42 | 307 ms | 400 ms | 532 ms | 552 ms | 1.7 | 0 | 4 | $0.11 | billed | ○ |
| drex-max@openrouter | 42 | 323 ms | 503 ms | 802 ms | 982 ms | 2.5 | 0 | 4 | $0.20 | billed |  |
| elephant@openrouter | 42 | 169 ms | 210 ms | 311 ms | 334 ms | 1.8 | 0 | 4 | $0.12 | billed |  |
| gemini-decision@openrouter | 42 | 326 ms | 443 ms | 496 ms | 513 ms | 1.5 | 0 | 4 | $0.35 | billed |  |
| jev:1.14 | 42 | 103 ms | 226 ms | 287 ms | 309 ms | 2.8 | 0 | 4 | $0.31 | estimated | ○ |
| joey@openrouter | 42 | 172 ms | 281 ms | 327 ms | 329 ms | 1.9 | 0 | 4 | $0.03 | billed |  |
| kev@openrouter | 42 | 604 ms | 844 ms | 1133 ms | 1168 ms | 1.9 | 0 | 4 | $0.11 | billed |  |
| luna@decisions | 41 | 294 ms | 493 ms | 569 ms | 592 ms | 1.9 | 0 | 4 | $0.45 | estimated |  |
| mammoth@openrouter | 42 | 296 ms | 320 ms | 338 ms | 342 ms | 1.1 | 0 | 4 | $0.34 | billed | ○ |
| reflex@openrouter | 42 | 303 ms | 417 ms | 462 ms | 464 ms | 1.5 | 0 | 4 | $0.14 | billed | ○ |
| span@openrouter | 42 | 280 ms | 526 ms | 669 ms | 672 ms | 2.4 | 0 | 4 | $0.04 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Under 100 calls, a model's p99 means little more than its max.
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0004 | 4 s (estimated, 42 calls) | 17 min | 4 |
| clef-omni@openrouter | $0.0028 | 3 s (estimated, 42 calls) | 12 min | 4 |
| clef@openrouter | $0.0034 | 5 s (estimated, 42 calls) | 20 min | 4 |
| d1-ultra@openrouter | $0.0006 | 3 s (estimated, 42 calls) | 13 min | 4 |
| d1.1@openrouter | $0.0003 | 3 s (estimated, 42 calls) | 14 min | 4 |
| d1@vercel | $0.0003 | 3 s (estimated, 42 calls) | 12 min | 4 |
| decider-flash@openrouter | $0.0001 | 2 s (estimated, 42 calls) | 7 min | 4 |
| decider@openrouter | $0.0003 | 4 s (estimated, 42 calls) | 15 min | 4 |
| decision-1@openrouter | $0.0005 | 3 s (estimated, 42 calls) | 13 min | 4 |
| drex-max@openrouter | $0.0008 | 4 s (estimated, 42 calls) | 14 min | 4 |
| elephant@openrouter | $0.0005 | 2 s (estimated, 42 calls) | 7 min | 4 |
| gemini-decision@openrouter | $0.0015 | 4 s (estimated, 42 calls) | 14 min | 4 |
| jev:1.14 | $0.0013 | 1 s (estimated, 42 calls) | 6 min | 4 |
| joey@openrouter | $0.0001 | 2 s (estimated, 42 calls) | 8 min | 4 |
| kev@openrouter | $0.0005 | 7 s (estimated, 42 calls) | 26 min | 4 |
| luna@decisions | $0.0019 | 3 s (estimated, 41 calls) | 13 min | 4 |
| mammoth@openrouter | $0.0014 | 3 s (estimated, 42 calls) | 11 min | 4 |
| reflex@openrouter | $0.0006 | 3 s (estimated, 42 calls) | 13 min | 4 |
| span@openrouter | $0.0002 | 3 s (estimated, 42 calls) | 13 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 10 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 92.9% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| clef-omni@openrouter | 90.5% | 85.7% | 1 | 5 | 0.30 | 0.30 |
| clef@openrouter | 90.5% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| d1-ultra@openrouter | 92.9% | 100.0% | 0 | 0 | 0.30 | 0.30 |
| d1.1@openrouter | 92.9% | 88.1% | 1 | 4 | 0.30 | 0.30 |
| d1@vercel | 92.9% | 100.0% | 0 | 0 | 0.70 | 0.70 |
| decider-flash@openrouter | 90.5% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| decider@openrouter | 92.9% | 88.1% | 1 | 4 | 0.10 | 0.10 |
| decision-1@openrouter | 92.9% | 95.2% | 1 | 1 | 0.10 | 0.10 |
| drex-max@openrouter | 92.9% | 90.5% | 0 | 4 | 0.10 | 0.10 |
| elephant@openrouter | 90.5% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| gemini-decision@openrouter | 97.6% | 95.2% | 1 | 1 | 0.30 | 0.30 |
| jev:1.14 | 92.9% | 92.9% | 0 | 3 | 0.50 | 0.50 |
| joey@openrouter | 73.8% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| kev@openrouter | 81.0% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| luna@decisions | 90.2% | 90.2% | 0 | 4 | 0.50 | 0.50 |
| mammoth@openrouter | 100.0% | 100.0% | 0 | 0 | 0.50 | 0.50 |
| reflex@openrouter | 92.9% | 100.0% | 0 | 0 | 0.30 | 0.30 |
| span@openrouter | 83.3% | 90.5% | 4 | 0 | 0.10 | 0.10 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 14 (88%) |
| 0.20 | 0 (0%) | 4 (25%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 1 (4%) | 2 (12%) |
| 0.50 | 2 (8%) | 1 (6%) |
| 0.60 | 4 (15%) | 1 (6%) |
| 0.70 | 9 (35%) | 1 (6%) |
| 0.80 | 11 (42%) | 0 (0%) |
| 0.90 | 20 (77%) | 0 (0%) |

## Misses and false alarms by threshold (clef-omni@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 16 (100%) |
| 0.20 | 1 (4%) | 12 (75%) |
| 0.30 | 1 (4%) | 5 (31%) |
| 0.40 | 3 (12%) | 1 (6%) |
| 0.50 | 3 (12%) | 1 (6%) |
| 0.60 | 3 (12%) | 1 (6%) |
| 0.70 | 7 (27%) | 0 (0%) |
| 0.80 | 14 (54%) | 0 (0%) |
| 0.90 | 20 (77%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 13 (81%) |
| 0.20 | 0 (0%) | 6 (38%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 1 (4%) | 4 (25%) |
| 0.50 | 2 (8%) | 2 (12%) |
| 0.60 | 2 (8%) | 1 (6%) |
| 0.70 | 2 (8%) | 1 (6%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 6 (23%) | 0 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 4 (25%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 0 (0%) | 0 (0%) |
| 0.40 | 0 (0%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 4 (15%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 6 (23%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 12 (75%) |
| 0.20 | 0 (0%) | 9 (56%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 0 (0%) | 2 (12%) |
| 0.50 | 1 (4%) | 2 (12%) |
| 0.60 | 1 (4%) | 1 (6%) |
| 0.70 | 3 (12%) | 1 (6%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 15 (94%) |
| 0.20 | 0 (0%) | 11 (69%) |
| 0.30 | 0 (0%) | 8 (50%) |
| 0.40 | 0 (0%) | 6 (38%) |
| 0.50 | 0 (0%) | 3 (19%) |
| 0.60 | 0 (0%) | 0 (0%) |
| 0.70 | 0 (0%) | 0 (0%) |
| 0.80 | 1 (4%) | 0 (0%) |
| 0.90 | 2 (8%) | 0 (0%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 3 (19%) |
| 0.20 | 0 (0%) | 2 (12%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 1 (4%) | 2 (12%) |
| 0.50 | 2 (8%) | 2 (12%) |
| 0.60 | 3 (12%) | 2 (12%) |
| 0.70 | 6 (23%) | 1 (6%) |
| 0.80 | 9 (35%) | 1 (6%) |
| 0.90 | 16 (62%) | 1 (6%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 4 (25%) |
| 0.20 | 0 (0%) | 3 (19%) |
| 0.30 | 1 (4%) | 1 (6%) |
| 0.40 | 3 (12%) | 1 (6%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 7 (27%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 1 (6%) |
| 0.20 | 1 (4%) | 0 (0%) |
| 0.30 | 1 (4%) | 0 (0%) |
| 0.40 | 2 (8%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 4 (15%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 4 (25%) |
| 0.20 | 1 (4%) | 1 (6%) |
| 0.30 | 2 (8%) | 1 (6%) |
| 0.40 | 2 (8%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 3 (12%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 6 (38%) |
| 0.20 | 0 (0%) | 3 (19%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 3 (12%) | 1 (6%) |
| 0.60 | 4 (15%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 7 (27%) | 0 (0%) |
| 0.90 | 11 (42%) | 0 (0%) |

## Misses and false alarms by threshold (gemini-decision@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 2 (12%) |
| 0.20 | 0 (0%) | 2 (12%) |
| 0.30 | 0 (0%) | 1 (6%) |
| 0.40 | 1 (4%) | 0 (0%) |
| 0.50 | 1 (4%) | 0 (0%) |
| 0.60 | 1 (4%) | 0 (0%) |
| 0.70 | 2 (8%) | 0 (0%) |
| 0.80 | 2 (8%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 8 (50%) |
| 0.20 | 0 (0%) | 6 (38%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 0 (0%) | 3 (19%) |
| 0.50 | 0 (0%) | 3 (19%) |
| 0.60 | 0 (0%) | 3 (19%) |
| 0.70 | 1 (4%) | 3 (19%) |
| 0.80 | 1 (4%) | 0 (0%) |
| 0.90 | 3 (12%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 14 (88%) |
| 0.20 | 0 (0%) | 8 (50%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 2 (8%) | 3 (19%) |
| 0.50 | 8 (31%) | 3 (19%) |
| 0.60 | 14 (54%) | 3 (19%) |
| 0.70 | 19 (73%) | 3 (19%) |
| 0.80 | 22 (85%) | 0 (0%) |
| 0.90 | 26 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 16 (100%) |
| 0.20 | 0 (0%) | 9 (56%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 2 (8%) | 2 (12%) |
| 0.50 | 8 (31%) | 0 (0%) |
| 0.60 | 17 (65%) | 0 (0%) |
| 0.70 | 23 (88%) | 0 (0%) |
| 0.80 | 25 (96%) | 0 (0%) |
| 0.90 | 26 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 11 (69%) |
| 0.20 | 0 (0%) | 7 (44%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 0 (0%) | 4 (25%) |
| 0.50 | 0 (0%) | 4 (25%) |
| 0.60 | 0 (0%) | 4 (25%) |
| 0.70 | 1 (4%) | 4 (25%) |
| 0.80 | 2 (8%) | 0 (0%) |
| 0.90 | 4 (16%) | 0 (0%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 4 (25%) |
| 0.20 | 0 (0%) | 2 (12%) |
| 0.30 | 0 (0%) | 1 (6%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 0 (0%) | 0 (0%) |
| 0.60 | 0 (0%) | 0 (0%) |
| 0.70 | 2 (8%) | 0 (0%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 11 (42%) | 0 (0%) |

## Misses and false alarms by threshold (reflex@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 5 (31%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 0 (0%) | 0 (0%) |
| 0.40 | 2 (8%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 4 (15%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (12%) | 0 (0%) |
| 0.20 | 4 (15%) | 0 (0%) |
| 0.30 | 4 (15%) | 0 (0%) |
| 0.40 | 6 (23%) | 0 (0%) |
| 0.50 | 7 (27%) | 0 (0%) |
| 0.60 | 8 (31%) | 0 (0%) |
| 0.70 | 8 (31%) | 0 (0%) |
| 0.80 | 9 (35%) | 0 (0%) |
| 0.90 | 12 (46%) | 0 (0%) |

## Wrong at a high probability (0.9 or more)

**decider-flash@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| haai-while-working | False | True | 0.90 | {"earlier": ["ユーザー: 近くで土曜に子ども連れで行ける室内の遊び場探して"], "agent": "調べています。少々お待… |

**span@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| email-send-ok | True | False | 0.95 | {"earlier": ["ユーザー: 大家さんに、エアコン壊れたから修理お願いしたいってメール書いて"], "agent": "下書きを… |
| cancel-scheduled-draft | True | False | 0.94 | {"earlier": ["ユーザー: 来週の町内会の議事録、下書き作っといてくれる？"], "agent": "承知しました。明日の朝ま… |
| maaiika-accept-20h | True | False | 0.91 | {"earlier": ["ユーザー: 今日19時に2人で「鮨 ひかり」取れる？"], "agent": "19時は満席でした。20時なら… |


## Cases the models disagree on (12 of 23)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| book-yes-un | True | True (0.91) | True (0.90) | True (0.96) | True (0.99) | True (0.99) | True (1.00) | True (0.72) | True (1.00) | True (1.00) | True (1.00) | True (0.84) | True (1.00) | True (1.00) | True (0.72) | False (0.50) | True (0.97) | True (0.93) | True (1.00) | True (0.98) | {"earlier": ["ユーザー: 今週末、箱根で一泊できる宿探して。2人で"], "agent": "土曜泊で「箱根湯本 翠の宿」が… |
| hotel-jaa-yasui | True | True (0.86) | True (0.91) | True (0.95) | True (0.99) | True (0.99) | True (1.00) | True (0.93) | True (1.00) | True (1.00) | True (0.99) | True (0.94) | True (1.00) | True (1.00) | False (0.54) | True (0.68) | True (0.99) | True (0.93) | True (1.00) | True (0.80) | {"earlier": ["ユーザー: 大阪出張、10/14泊で梅田近くのビジホ"], "agent": "候補は2つです。\n1. ホテ… |
| add-milk | True | True (0.79) | True (0.90) | True (0.97) | True (1.00) | True (0.99) | True (1.00) | True (0.97) | True (1.00) | True (1.00) | True (1.00) | True (0.94) | True (1.00) | True (1.00) | False (0.62) | True (0.59) | True (0.99) | True (0.94) | True (1.00) | True (1.00) | {"earlier": ["ユーザー: 卵と食パン切れたからネットスーパーで頼んで"], "agent": "イオンネットスーパーで卵10… |
| sw-fix-tests-un | True | True (0.94) | True (0.85) | True (0.97) | True (0.99) | True (0.99) | True (1.00) | True (0.94) | True (1.00) | True (1.00) | True (1.00) | True (0.97) | True (1.00) | True (1.00) | True (0.80) | False (0.62) | True (0.99) | True (0.93) | True (1.00) | True (0.99) | {"earlier": ["ユーザー: npm test 回して"], "agent": "テストを実行しました。48件中3件が失敗してい… |
| sw-naming-change | True | True (0.91) | True (0.60) | True (0.97) | True (0.96) | True (0.99) | True (1.00) | False (0.66) | True (0.99) | True (0.99) | True (0.98) | True (0.98) | True (1.00) | True (1.00) | True (0.76) | True (0.51) | True (0.99) | True (0.90) | True (1.00) | True (0.98) | {"agent": "APIレスポンスのキー名を userId に統一しました。変更は api/handlers 以下の6ファイルです。"… |
| thanks-plus-bus | True | True (0.86) | True (0.85) | True (0.97) | True (0.95) | True (0.99) | True (0.97) | True (0.97) | True (0.98) | True (1.00) | True (0.97) | True (0.98) | True (1.00) | True (1.00) | False (0.58) | True (0.83) | True (0.99) | True (0.94) | True (0.98) | True (0.98) | {"agent": "河口湖行きの高速バス、土曜7:10新宿発で2名分予約しました。", "user": "ありがとう！あと帰りのバスも調… |
| ryokai-to-cancel-fee | True | True (0.68) | True (0.79) | True (0.92) | True (0.93) | True (0.96) | True (0.99) | True (0.68) | True (0.90) | True (0.93) | True (0.93) | True (0.83) | True (0.80) | True (1.00) | True (0.52) | False (0.55) | True (0.84) | True (0.90) | True (0.97) | False (0.61) | {"earlier": ["ユーザー: 来週の美容院、キャンセルしたい"], "agent": "前日以降のキャンセルのため、キャンセル料… |
| tickets-kaatte | True | True (0.62) | True (0.83) | True (0.94) | True (0.99) | True (0.99) | True (1.00) | True (0.85) | True (1.00) | True (0.99) | True (1.00) | True (0.95) | True (1.00) | True (1.00) | False (0.55) | True (0.54) | True (0.99) | True (0.93) | True (1.00) | True (0.94) | {"earlier": ["ユーザー: ミセスのライブ、リセールで出たら教えて"], "agent": "11/22 東京ドーム公演のリセ… |
| sw-dont-touch-file | True | True (0.92) | True (0.92) | True (0.98) | True (0.99) | True (1.00) | True (1.00) | True (0.97) | True (1.00) | True (1.00) | True (1.00) | True (0.92) | True (1.00) | True (1.00) | False (0.52) | True (0.64) | True (1.00) | True (0.94) | True (1.00) | True (0.96) | {"earlier": ["ユーザー: ログイン周りのバグ直して"], "agent": "原因は auth/session.ts のトー… |
| email-send-ok | True | True (0.66) | True (0.64) | True (0.77) | True (0.91) | True (0.99) | True (1.00) | True (0.73) | True (0.88) | True (0.99) | True (0.95) | True (0.75) | True (0.99) | True (0.98) | True (0.81) | True (0.50) | True (0.99) | True (0.85) | False (0.61) | False (0.95) | {"earlier": ["ユーザー: 大家さんに、エアコン壊れたから修理お願いしたいってメール書いて"], "agent": "下書きを… |
| thumbs-to-send-question | True | True (0.92) | True (0.62) | True (0.91) | True (0.92) | True (0.97) | True (1.00) | True (0.89) | True (0.98) | True (1.00) | True (0.98) | True (0.93) | True (0.98) | True (0.99) | False (0.57) | True (0.56) | True (0.97) | True (0.97) | True (0.95) | False (0.51) | {"agent": "幹事の佐藤さんへ「当日は15分ほど遅れます」と送信しますか？", "user": "👍"} |
| yoroshiku-already-agreed | False | False (0.76) | True (0.68) | False (0.77) | False (0.89) | False (0.73) | False (0.56) | False (0.94) | False (0.83) | False (1.00) | False (0.94) | False (0.91) | False (0.97) | False (0.68) | True (0.74) | False (0.74) | True (0.71) | False (0.88) | False (0.95) | False (0.97) | {"earlier": ["ユーザー: 土曜のゴルフ、雨だったら中止にしたい"], "agent": "承知しました。土曜の朝6時に天気を… |
