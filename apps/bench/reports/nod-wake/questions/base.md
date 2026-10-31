# nod-wake

2026-10-31 · 42 labelled dev cases (True 26, False 16) · split: leave-one-out (no test case among these: CV numbers only) · source: cases.json

No model meets the constraints (haiku@vercel: different answered dev cases; automatic comparison refused; d1.1@openrouter: different answered dev cases; automatic comparison refused; d1@vercel: different answered dev cases; automatic comparison refused; mammoth@openrouter: different answered dev cases; automatic comparison refused; elephant@openrouter: different answered dev cases; automatic comparison refused; mercury@openrouter: different answered dev cases; automatic comparison refused; decider@openrouter: different answered dev cases; automatic comparison refused; d1-ultra@openrouter: different answered dev cases; automatic comparison refused; decision-1@openrouter: different answered dev cases; automatic comparison refused; jev:1.14: different answered dev cases; automatic comparison refused; drex-max@openrouter: different answered dev cases; automatic comparison refused; clef@openrouter: different answered dev cases; automatic comparison refused; clef-flash@openrouter: different answered dev cases; automatic comparison refused; luna@decisions: different answered dev cases; automatic comparison refused; decider-flash@openrouter: different answered dev cases; automatic comparison refused; span@openrouter: different answered dev cases; automatic comparison refused; kev@openrouter: different answered dev cases; automatic comparison refused; joey@openrouter: different answered dev cases; automatic comparison refused; flash-lite@vercel: different answered dev cases; automatic comparison refused).

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.97 | 0.12 | 86% [74, 95] | 94.4% (83.5%) | 0/57 | 0/57 |
| clef@openrouter | 42 | 90.5% [81, 98] | 0.93 | 0.99 | 0.09 | 88% [76, 98] | 94.6% (83.9%) | 0/57 | 0/57 |
| d1-ultra@openrouter | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.09 | 98% [93, 100] | 95.1% (85.4%) | 0/57 | 0/57 |
| d1.1@openrouter | 42 | 97.6% [93, 100] | 0.98 | 0.99 | 0.08 | 98% [93, 100] | 97.6% (88.9%) | 0/57 | 0/57 |
| d1@vercel | 42 | 97.6% [93, 100] | 0.98 | 1.00 | 0.11 | 98% [93, 100] | 97.6% (88.9%) | 0/57 | 0/57 |
| decider-flash@openrouter | 42 | 88.1% [76, 98] | 0.90 | 0.97 | 0.06 | 79% [64, 90] | 93.9% (82.1%) | 0/57 | 0/57 |
| decider@openrouter | 42 | 95.2% [88, 100] | 0.96 | 0.99 | 0.05 | 98% [93, 100] | 95.1% (85.4%) | 0/57 | 0/57 |
| decision-1@openrouter | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.04 | 98% [93, 100] | 92.7% (82.2%) | 0/57 | 0/57 |
| drex-max@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.99 | 0.05 | 90% [81, 98] | 92.1% (80.8%) | 0/57 | 0/57 |
| elephant@openrouter | 42 | 95.2% [88, 100] | 0.96 | 1.00 | 0.08 | 98% [93, 100] | 97.6% (88.9%) | 0/57 | 0/57 |
| flash-lite@vercel ※ | 42 | 90.5% [81, 98] | 0.92 | 0.91 | 0.10 | 0% [0, 0] | — (0.0%) | 0/57 | 0/57 |
| haiku@vercel ※ | 42 | 100.0% [100, 100] | 1.00 | 1.00 | 0.00 | 100% [100, 100] | 100.0% (93.1%) | 0/57 | 0/57 |
| jev:1.14 | 42 | 92.9% [83, 100] | 0.95 | 1.00 | 0.05 | 95% [88, 100] | 95.0% (85.1%) | 0/57 | 0/57 |
| joey@openrouter | 42 | 66.7% [52, 81] | 0.68 | 0.85 | 0.08 | 29% [17, 43] | 91.7% (66.1%) | 0/57 | 0/57 |
| kev@openrouter | 42 | 88.1% [79, 95] | 0.89 | 0.98 | 0.20 | 71% [57, 86] | 93.3% (80.5%) | 0/57 | 0/57 |
| luna@decisions | 41 | 90.2% [80, 98] | 0.93 | 0.98 | 0.06 | 83% [71, 93] | 94.1% (82.6%) | 1/57 | 0/57 |
| mammoth@openrouter | 42 | 97.6% [93, 100] | 0.98 | 1.00 | 0.12 | 98% [93, 100] | 100.0% (93.0%) | 0/57 | 0/57 |
| mercury@openrouter | 42 | 95.2% [88, 100] | 0.96 | 1.00 | 0.04 | 98% [93, 100] | 97.6% (88.9%) | 0/57 | 0/57 |
| span@openrouter | 42 | 88.1% [79, 98] | 0.89 | 0.98 | 0.07 | 74% [60, 86] | 93.5% (81.1%) | 0/57 | 0/57 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.5-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-5.5; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 10, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| haiku@vercel | 100% [100, 100] | 0.000 [0.000, 0.000] | 1.00 | different answered dev cases; automatic comparison refused |
| d1.1@openrouter | 98% [93, 100] | 0.024 [0.000, 0.071] | 0.53 | different answered dev cases; automatic comparison refused |
| d1@vercel | 98% [93, 100] | 0.024 [0.000, 0.071] | 0.57 | different answered dev cases; automatic comparison refused |
| mammoth@openrouter | 98% [93, 100] | 0.238 [0.000, 0.714] | 0.60 | different answered dev cases; automatic comparison refused |
| elephant@openrouter | 98% [93, 100] | 0.262 [0.000, 0.786] | 0.51 | different answered dev cases; automatic comparison refused |
| mercury@openrouter | 98% [93, 100] | 0.262 [0.000, 0.762] | 0.91 | different answered dev cases; automatic comparison refused |
| decider@openrouter | 98% [93, 100] | 0.476 [0.000, 1.190] | 0.54 | different answered dev cases; automatic comparison refused |
| d1-ultra@openrouter | 98% [93, 100] | 0.714 [0.000, 1.667] | 0.61 | different answered dev cases; automatic comparison refused |
| decision-1@openrouter | 98% [93, 100] | 0.714 [0.000, 1.667] | 0.76 | different answered dev cases; automatic comparison refused |
| jev:1.14 | 95% [88, 100] | 0.071 [0.000, 0.167] | 0.65 | different answered dev cases; automatic comparison refused |
| drex-max@openrouter | 90% [81, 98] | 0.714 [0.000, 1.667] | 0.74 | different answered dev cases; automatic comparison refused |
| clef@openrouter | 88% [76, 98] | 0.310 [0.024, 0.833] | 0.55 | different answered dev cases; automatic comparison refused |
| clef-flash@openrouter | 86% [74, 95] | 0.524 [0.024, 1.262] | 0.53 | different answered dev cases; automatic comparison refused |
| luna@decisions | 83% [71, 93] | 0.098 [0.024, 0.195] | 0.81 | different answered dev cases; automatic comparison refused |
| decider-flash@openrouter | 79% [64, 90] | 0.762 [0.095, 1.667] | 0.85 | different answered dev cases; automatic comparison refused |
| span@openrouter | 74% [60, 86] | 1.190 [0.238, 2.143] | 0.93 | different answered dev cases; automatic comparison refused |
| kev@openrouter | 71% [57, 86] | 1.190 [0.476, 2.143] | 0.61 | different answered dev cases; automatic comparison refused |
| joey@openrouter | 29% [17, 43] | 2.690 [1.476, 3.932] | 0.82 | different answered dev cases; automatic comparison refused |
| flash-lite@vercel | 0% [0, 0] | 0.738 [0.024, 1.476] | — | different answered dev cases; automatic comparison refused |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 42 | 387 ms | 536 ms | 768 ms | 859 ms | 2.0 | 0 | 8 | $0.09 | billed |  |
| clef@openrouter | 42 | 1501 ms | 2642 ms | 4593 ms | 5388 ms | 3.1 | 0 | 8 | $0.81 | billed |  |
| d1-ultra@openrouter | 42 | 1247 ms | 1978 ms | 4277 ms | 5180 ms | 3.4 | 0 | 8 | $0.13 | billed |  |
| d1.1@openrouter | 42 | 1280 ms | 2113 ms | 5766 ms | 6156 ms | 4.5 | 0 | 8 | $0.06 | billed |  |
| d1@vercel | 42 | 217 ms | 474 ms | 567 ms | 575 ms | 2.6 | 0 | 8 | $0.06 | billed | ○ |
| decider-flash@openrouter | 42 | 1214 ms | 2861 ms | 4665 ms | 5148 ms | 3.8 | 0 | 8 | $0.03 | billed | ○ |
| decider@openrouter | 42 | 1303 ms | 2071 ms | 2940 ms | 2965 ms | 2.3 | 0 | 8 | $0.07 | billed |  |
| decision-1@openrouter | 42 | 1416 ms | 1649 ms | 1948 ms | 2043 ms | 1.4 | 0 | 8 | $0.11 | billed |  |
| drex-max@openrouter | 42 | 1283 ms | 2346 ms | 3443 ms | 4137 ms | 2.7 | 0 | 8 | $0.20 | billed |  |
| elephant@openrouter | 42 | 1199 ms | 2286 ms | 2866 ms | 3098 ms | 2.4 | 0 | 8 | $0.12 | billed |  |
| flash-lite@vercel | 42 | 1199 ms | 2272 ms | 2840 ms | 2867 ms | 2.4 | 0 | 8 | $1.45 | estimated |  |
| haiku@vercel | 42 | 1293 ms | 3346 ms | 4277 ms | 4445 ms | 3.3 | 0 | 8 | $0.95 | estimated | ○ |
| jev:1.14 | 42 | 1200 ms | 2886 ms | 5361 ms | 6148 ms | 4.5 | 0 | 8 | $0.31 | estimated |  |
| joey@openrouter | 42 | 1302 ms | 2198 ms | 3857 ms | 3866 ms | 3.0 | 0 | 8 | $0.03 | billed | ○ |
| kev@openrouter | 42 | 1502 ms | 2026 ms | 2819 ms | 3292 ms | 1.9 | 0 | 8 | $0.11 | billed |  |
| luna@decisions | 41 | 1396 ms | 1751 ms | 4870 ms | 6273 ms | 3.5 | 0 | 8 | $0.45 | estimated |  |
| mammoth@openrouter | 42 | 1256 ms | 2520 ms | 2851 ms | 2890 ms | 2.3 | 0 | 8 | $0.34 | billed |  |
| mercury@openrouter | 42 | 1323 ms | 2002 ms | 2811 ms | 3246 ms | 2.1 | 0 | 8 | $0.06 | billed | ○ |
| span@openrouter | 42 | 1406 ms | 2065 ms | 2958 ms | 3088 ms | 2.1 | 0 | 8 | $0.04 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Under 100 calls, a model's p99 means little more than its max.
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): flash-lite@vercel, haiku@vercel, jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0004 | 2 s (estimated, 42 calls) | 8 min | 8 |
| clef@openrouter | $0.0034 | 8 s (estimated, 42 calls) | 32 min | 8 |
| d1-ultra@openrouter | $0.0006 | 7 s (estimated, 42 calls) | 30 min | 8 |
| d1.1@openrouter | $0.0003 | 8 s (estimated, 42 calls) | 33 min | 8 |
| d1@vercel | $0.0003 | 1 s (estimated, 42 calls) | 5 min | 8 |
| decider-flash@openrouter | $0.0001 | 8 s (estimated, 42 calls) | 31 min | 8 |
| decider@openrouter | $0.0003 | 8 s (estimated, 42 calls) | 30 min | 8 |
| decision-1@openrouter | $0.0005 | 7 s (estimated, 42 calls) | 29 min | 8 |
| drex-max@openrouter | $0.0008 | 8 s (estimated, 42 calls) | 31 min | 8 |
| elephant@openrouter | $0.0005 | 8 s (estimated, 42 calls) | 30 min | 8 |
| flash-lite@vercel | $0.0061 | 7 s (estimated, 42 calls) | 29 min | 8 |
| haiku@vercel | $0.0040 | 9 s (estimated, 42 calls) | 36 min | 8 |
| jev:1.14 | $0.0013 | 8 s (estimated, 42 calls) | 31 min | 8 |
| joey@openrouter | $0.0001 | 8 s (estimated, 42 calls) | 32 min | 8 |
| kev@openrouter | $0.0005 | 8 s (estimated, 42 calls) | 31 min | 8 |
| luna@decisions | $0.0019 | 7 s (estimated, 41 calls) | 30 min | 8 |
| mammoth@openrouter | $0.0014 | 8 s (estimated, 42 calls) | 30 min | 8 |
| mercury@openrouter | $0.0003 | 7 s (estimated, 42 calls) | 29 min | 8 |
| span@openrouter | $0.0002 | 8 s (estimated, 42 calls) | 31 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 10 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 90.5% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| clef@openrouter | 90.5% | 88.1% | 1 | 4 | 0.30 | 0.30 |
| d1-ultra@openrouter | 92.9% | 100.0% | 0 | 0 | 0.30 | 0.30 |
| d1.1@openrouter | 97.6% | 97.6% | 0 | 1 | 0.50 | 0.50 |
| d1@vercel | 97.6% | 97.6% | 0 | 1 | 0.70 | 0.70 |
| decider-flash@openrouter | 88.1% | 92.9% | 1 | 2 | 0.10 | 0.10 |
| decider@openrouter | 95.2% | 88.1% | 1 | 4 | 0.10 | 0.10 |
| decision-1@openrouter | 92.9% | 95.2% | 0 | 2 | 0.10 | 0.10 |
| drex-max@openrouter | 92.9% | 90.5% | 0 | 4 | 0.10 | 0.10 |
| elephant@openrouter | 95.2% | 90.5% | 1 | 3 | 0.30 | 0.30 |
| flash-lite@vercel | 90.5% | 90.5% | 3 | 1 | 0.50 | 0.50 |
| haiku@vercel | 100.0% | 100.0% | 0 | 0 | 0.50 | 0.50 |
| jev:1.14 | 92.9% | 90.5% | 1 | 3 | 0.50 | 0.50 |
| joey@openrouter | 66.7% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| kev@openrouter | 88.1% | 92.9% | 0 | 3 | 0.30 | 0.30 |
| luna@decisions | 90.2% | 87.8% | 1 | 4 | 0.50 | 0.50 |
| mammoth@openrouter | 97.6% | 95.2% | 1 | 1 | 0.30 | 0.30 |
| mercury@openrouter | 95.2% | 95.2% | 1 | 1 | 0.50 | 0.50 |
| span@openrouter | 88.1% | 92.9% | 2 | 1 | 0.10 | 0.10 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 14 (88%) |
| 0.20 | 0 (0%) | 5 (31%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 1 (4%) | 2 (12%) |
| 0.50 | 2 (8%) | 2 (12%) |
| 0.60 | 4 (15%) | 1 (6%) |
| 0.70 | 7 (27%) | 1 (6%) |
| 0.80 | 12 (46%) | 0 (0%) |
| 0.90 | 22 (85%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 14 (88%) |
| 0.20 | 0 (0%) | 5 (31%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 0 (0%) | 4 (25%) |
| 0.50 | 1 (4%) | 3 (19%) |
| 0.60 | 2 (8%) | 1 (6%) |
| 0.70 | 2 (8%) | 1 (6%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 7 (27%) | 0 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 3 (19%) |
| 0.20 | 0 (0%) | 2 (12%) |
| 0.30 | 0 (0%) | 0 (0%) |
| 0.40 | 3 (12%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 6 (23%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 13 (81%) |
| 0.20 | 0 (0%) | 6 (38%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 0 (0%) | 1 (6%) |
| 0.60 | 2 (8%) | 1 (6%) |
| 0.70 | 3 (12%) | 1 (6%) |
| 0.80 | 4 (15%) | 1 (6%) |
| 0.90 | 4 (15%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 15 (94%) |
| 0.20 | 0 (0%) | 8 (50%) |
| 0.30 | 0 (0%) | 3 (19%) |
| 0.40 | 0 (0%) | 3 (19%) |
| 0.50 | 0 (0%) | 1 (6%) |
| 0.60 | 0 (0%) | 1 (6%) |
| 0.70 | 0 (0%) | 0 (0%) |
| 0.80 | 2 (8%) | 0 (0%) |
| 0.90 | 2 (8%) | 0 (0%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 2 (12%) |
| 0.20 | 0 (0%) | 2 (12%) |
| 0.30 | 1 (4%) | 2 (12%) |
| 0.40 | 2 (8%) | 2 (12%) |
| 0.50 | 3 (12%) | 2 (12%) |
| 0.60 | 3 (12%) | 2 (12%) |
| 0.70 | 5 (19%) | 1 (6%) |
| 0.80 | 9 (35%) | 1 (6%) |
| 0.90 | 16 (62%) | 0 (0%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 4 (25%) |
| 0.20 | 0 (0%) | 4 (25%) |
| 0.30 | 1 (4%) | 2 (12%) |
| 0.40 | 2 (8%) | 1 (6%) |
| 0.50 | 2 (8%) | 0 (0%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 2 (12%) |
| 0.20 | 1 (4%) | 0 (0%) |
| 0.30 | 2 (8%) | 0 (0%) |
| 0.40 | 2 (8%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 4 (15%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 4 (25%) |
| 0.20 | 1 (4%) | 2 (12%) |
| 0.30 | 2 (8%) | 1 (6%) |
| 0.40 | 3 (12%) | 1 (6%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 3 (12%) | 0 (0%) |
| 0.80 | 6 (23%) | 0 (0%) |
| 0.90 | 7 (27%) | 0 (0%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 5 (31%) |
| 0.20 | 0 (0%) | 3 (19%) |
| 0.30 | 0 (0%) | 3 (19%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 1 (4%) | 1 (6%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 7 (27%) | 0 (0%) |
| 0.90 | 8 (31%) | 0 (0%) |

## Misses and false alarms by threshold (flash-lite@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (12%) | 1 (6%) |
| 0.20 | 3 (12%) | 1 (6%) |
| 0.30 | 3 (12%) | 1 (6%) |
| 0.40 | 3 (12%) | 1 (6%) |
| 0.50 | 3 (12%) | 1 (6%) |
| 0.60 | 3 (12%) | 1 (6%) |
| 0.70 | 3 (12%) | 1 (6%) |
| 0.80 | 3 (12%) | 1 (6%) |
| 0.90 | 3 (12%) | 1 (6%) |

## Misses and false alarms by threshold (haiku@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 0 (0%) |
| 0.20 | 0 (0%) | 0 (0%) |
| 0.30 | 0 (0%) | 0 (0%) |
| 0.40 | 0 (0%) | 0 (0%) |
| 0.50 | 0 (0%) | 0 (0%) |
| 0.60 | 0 (0%) | 0 (0%) |
| 0.70 | 0 (0%) | 0 (0%) |
| 0.80 | 0 (0%) | 0 (0%) |
| 0.90 | 0 (0%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 7 (44%) |
| 0.20 | 0 (0%) | 4 (25%) |
| 0.30 | 0 (0%) | 3 (19%) |
| 0.40 | 0 (0%) | 3 (19%) |
| 0.50 | 0 (0%) | 3 (19%) |
| 0.60 | 0 (0%) | 3 (19%) |
| 0.70 | 1 (4%) | 2 (12%) |
| 0.80 | 2 (8%) | 0 (0%) |
| 0.90 | 3 (12%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 13 (81%) |
| 0.20 | 0 (0%) | 7 (44%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 3 (12%) | 3 (19%) |
| 0.50 | 11 (42%) | 3 (19%) |
| 0.60 | 16 (62%) | 3 (19%) |
| 0.70 | 20 (77%) | 3 (19%) |
| 0.80 | 23 (88%) | 1 (6%) |
| 0.90 | 26 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 16 (100%) |
| 0.20 | 0 (0%) | 9 (56%) |
| 0.30 | 0 (0%) | 3 (19%) |
| 0.40 | 2 (8%) | 2 (12%) |
| 0.50 | 5 (19%) | 0 (0%) |
| 0.60 | 11 (42%) | 0 (0%) |
| 0.70 | 21 (81%) | 0 (0%) |
| 0.80 | 23 (88%) | 0 (0%) |
| 0.90 | 26 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 10 (62%) |
| 0.20 | 0 (0%) | 7 (44%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 0 (0%) | 4 (25%) |
| 0.50 | 0 (0%) | 4 (25%) |
| 0.60 | 1 (4%) | 4 (25%) |
| 0.70 | 1 (4%) | 3 (19%) |
| 0.80 | 2 (8%) | 1 (6%) |
| 0.90 | 3 (12%) | 0 (0%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 5 (31%) |
| 0.20 | 0 (0%) | 2 (12%) |
| 0.30 | 0 (0%) | 1 (6%) |
| 0.40 | 0 (0%) | 0 (0%) |
| 0.50 | 1 (4%) | 0 (0%) |
| 0.60 | 1 (4%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 6 (23%) | 0 (0%) |
| 0.90 | 8 (31%) | 0 (0%) |

## Misses and false alarms by threshold (mercury@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (4%) | 1 (6%) |
| 0.20 | 1 (4%) | 1 (6%) |
| 0.30 | 1 (4%) | 1 (6%) |
| 0.40 | 1 (4%) | 1 (6%) |
| 0.50 | 1 (4%) | 1 (6%) |
| 0.60 | 1 (4%) | 1 (6%) |
| 0.70 | 1 (4%) | 1 (6%) |
| 0.80 | 1 (4%) | 1 (6%) |
| 0.90 | 1 (4%) | 1 (6%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (8%) | 1 (6%) |
| 0.20 | 4 (15%) | 0 (0%) |
| 0.30 | 4 (15%) | 0 (0%) |
| 0.40 | 4 (15%) | 0 (0%) |
| 0.50 | 5 (19%) | 0 (0%) |
| 0.60 | 6 (23%) | 0 (0%) |
| 0.70 | 7 (27%) | 0 (0%) |
| 0.80 | 7 (27%) | 0 (0%) |
| 0.90 | 10 (38%) | 0 (0%) |

## Wrong at a high probability (0.9 or more)

**flash-lite@vercel** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| email-send-ok | True | False | 1.00 | {"earlier": ["ユーザー: 大家さんに、エアコン壊れたから修理お願いしたいってメール書いて"], "agent": "下書きを… |
| maaiika-accept-20h | True | False | 1.00 | {"earlier": ["ユーザー: 今日19時に2人で「鮨 ひかり」取れる？"], "agent": "19時は満席でした。20時なら… |
| thumbs-to-send-question | True | False | 1.00 | {"agent": "幹事の佐藤さんへ「当日は15分ほど遅れます」と送信しますか？", "user": "👍"} |
| haai-while-working | False | True | 1.00 | {"earlier": ["ユーザー: 近くで土曜に子ども連れで行ける室内の遊び場探して"], "agent": "調べています。少々お待… |

**mercury@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| plan-a-sorede | True | False | 0.93 | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| yappari-iiya-decline-offer | False | True | 0.91 | {"agent": "冷蔵庫にある鶏むね肉と白菜で作れるレシピ、いくつか送りましょうか？", "user": "やっぱりいいや"} |

**span@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| maaiika-accept-20h | True | False | 0.97 | {"earlier": ["ユーザー: 今日19時に2人で「鮨 ひかり」取れる？"], "agent": "19時は満席でした。20時なら… |
| cancel-scheduled-draft | True | False | 0.93 | {"earlier": ["ユーザー: 来週の町内会の議事録、下書き作っといてくれる？"], "agent": "承知しました。明日の朝ま… |


## Cases the models disagree on (12 of 22)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | flash-lite@vercel | haiku@vercel | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| email-send-ok | True | True (0.72) | True (0.78) | True (0.96) | True (0.99) | True (1.00) | False (0.76) | True (0.96) | True (1.00) | True (0.99) | True (0.74) | False (1.00) | True (1.00) | True (0.98) | True (0.84) | False (0.57) | True (0.98) | True (0.75) | True (1.00) | True (0.67) | {"earlier": ["ユーザー: 大家さんに、エアコン壊れたから修理お願いしたいってメール書いて"], "agent": "下書きを… |
| plan-a-sorede | True | False (0.66) | False (0.59) | False (0.60) | True (0.53) | True (0.73) | False (0.55) | False (0.74) | False (0.57) | False (0.85) | True (0.52) | True (1.00) | True (1.00) | True (0.65) | False (0.64) | False (0.57) | True (0.99) | True (0.60) | False (0.93) | True (0.54) | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| restaurant-iine-hold | True | True (0.89) | True (0.93) | True (0.93) | True (0.98) | True (1.00) | True (0.73) | True (0.99) | True (0.95) | True (0.99) | True (0.87) | True (1.00) | True (1.00) | True (0.97) | False (0.57) | True (0.61) | True (0.96) | True (0.89) | True (1.00) | True (0.96) | {"earlier": ["ユーザー: 金曜、大学の友達とご飯行くから店探しといて"], "agent": "金曜19時、渋谷の和食「こも… |
| rain-bbq-musing | True | True (0.86) | True (0.86) | True (0.88) | True (0.97) | True (1.00) | True (0.87) | True (0.91) | True (0.96) | True (0.80) | True (0.97) | True (1.00) | True (1.00) | True (0.99) | False (0.53) | True (0.64) | True (0.99) | True (0.79) | True (0.93) | True (0.84) | {"earlier": ["ユーザー: 明日の河原BBQ、段取りまとめて管理しといて"], "agent": "明日10時集合、多摩川河川… |
| hungry-pending-restaurant | True | True (0.59) | True (0.55) | False (0.63) | True (0.56) | True (0.97) | True (0.72) | False (0.64) | False (0.82) | False (0.78) | False (0.53) | True (1.00) | True (1.00) | True (0.72) | False (0.68) | True (0.52) | True (0.91) | False (0.60) | True (0.96) | False (0.90) | {"earlier": ["ユーザー: 今日の夜ご飯の店、あとで探してほしい。声かけるわ"], "agent": "承知しました。お声がけ… |
| add-milk | True | True (0.73) | True (0.97) | True (0.99) | True (1.00) | True (1.00) | True (0.97) | True (1.00) | True (1.00) | True (1.00) | True (0.97) | True (1.00) | True (1.00) | True (1.00) | False (0.65) | True (0.66) | True (0.99) | True (0.96) | True (1.00) | True (1.00) | {"earlier": ["ユーザー: 卵と食パン切れたからネットスーパーで頼んで"], "agent": "イオンネットスーパーで卵10… |
| sw-fix-tests-un | True | True (0.94) | True (0.97) | True (0.99) | True (1.00) | True (1.00) | True (0.89) | True (1.00) | True (1.00) | True (1.00) | True (0.98) | True (1.00) | True (1.00) | True (1.00) | True (0.62) | False (0.58) | True (1.00) | True (0.92) | True (1.00) | True (0.99) | {"earlier": ["ユーザー: npm test 回して"], "agent": "テストを実行しました。48件中3件が失敗してい… |
| sw-migration-wait | True | True (0.86) | True (0.96) | True (0.99) | True (0.99) | True (1.00) | True (0.95) | True (1.00) | True (1.00) | True (1.00) | True (0.98) | True (1.00) | True (1.00) | True (1.00) | False (0.59) | True (0.73) | True (1.00) | True (0.94) | True (1.00) | True (0.97) | {"earlier": ["ユーザー: usersテーブルにカラム追加するマイグレーション流しといて"], "agent": "マイグレー… |
| sw-naming-change | True | True (0.91) | True (0.97) | True (0.96) | True (0.99) | True (1.00) | False (0.66) | True (0.99) | True (0.99) | True (0.98) | True (0.98) | True (1.00) | True (1.00) | True (1.00) | True (0.75) | True (0.50) | True (0.99) | True (0.91) | True (1.00) | True (0.98) | {"agent": "APIレスポンスのキー名を userId に統一しました。変更は api/handlers 以下の6ファイルです。"… |
| cancel-scheduled-draft | True | False (0.52) | True (0.95) | True (0.93) | True (0.97) | True (0.93) | True (0.91) | True (0.97) | True (0.88) | True (0.98) | True (0.68) | True (1.00) | True (1.00) | True (0.96) | False (0.55) | True (0.58) | True (0.99) | True (0.87) | True (1.00) | False (0.93) | {"earlier": ["ユーザー: 来週の町内会の議事録、下書き作っといてくれる？"], "agent": "承知しました。明日の朝ま… |
| thanks-plus-bus | True | True (0.89) | True (0.98) | True (0.96) | True (0.98) | True (0.99) | True (0.97) | True (0.98) | True (1.00) | True (0.98) | True (0.98) | True (1.00) | True (1.00) | True (1.00) | False (0.56) | True (0.83) | True (0.99) | True (0.92) | True (1.00) | True (0.98) | {"agent": "河口湖行きの高速バス、土曜7:10新宿発で2名分予約しました。", "user": "ありがとう！あと帰りのバスも調… |
| ok-ambiguous-choice | True | True (0.71) | True (0.76) | True (0.64) | True (0.73) | True (0.95) | True (0.61) | True (0.64) | True (0.53) | True (0.74) | True (0.77) | True (1.00) | True (1.00) | True (0.98) | True (0.62) | False (0.64) | True (0.77) | True (0.67) | True (0.99) | False (0.88) | {"agent": "レンタカーは、A: コンパクトカー 1日6,600円、B: ミニバン 1日12,100円 のどちらにしますか？", … |
