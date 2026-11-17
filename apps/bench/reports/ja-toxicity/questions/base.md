# ja-toxicity

2026-11-17 · 210 labelled dev cases (True 105, False 105) · split: stratified k-fold (no test case among these: CV numbers only) · source: LLM-jp Toxicity Dataset（LLM-jp, CC BY 4.0）の 1,000 字以下から toxic / nontoxic 各 150 件

mammoth@openrouter has the highest coverage at 99% accuracy, 99% [97, 100] (API cost $0.53 per 10k, p99 273ms). Its interval overlaps with drex-max@openrouter, clef-flash@openrouter, decider-flash@openrouter, elephant@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1@vercel, jev:1.14, d1.2-ultra, luna@decisions, reflex@openrouter, decision-1@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is drex-max@openrouter's, 99% [97, 100]. Its sure accuracy is close to the target: showing it is 99% or more takes over 5,000 labels.

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 96% [93, 99] | 98.5% (96.2%) | 0.0% (0/210) | 0/210 |
| clef-omni@openrouter | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.04 | 89% [84, 93] | 98.9% (96.7%) | 0.0% (0/210) | 0/210 |
| clef@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.05 | 91% [87, 95] | 99.0% (96.7%) | 0.0% (0/210) | 0/210 |
| d1-ultra@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.04 | 95% [92, 98] | 98.5% (96.2%) | 0.0% (0/210) | 0/210 |
| d1.1@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.03 | 95% [92, 98] | 99.0% (96.9%) | 0.0% (0/210) | 0/210 |
| d1.2 | 210 | 98.1% [96, 100] | 0.98 | 1.00 | 0.04 | 94% [91, 97] | 99.0% (96.9%) | 0.0% (0/210) | 0/210 |
| d1.2-ultra | 210 | 97.6% [96, 100] | 0.98 | 1.00 | 0.03 | 94% [91, 97] | 99.0% (96.9%) | 0.0% (0/210) | 0/210 |
| d1@vercel | 210 | 97.6% [96, 100] | 0.98 | 0.99 | 0.02 | 96% [93, 99] | 98.5% (96.2%) | 0.0% (0/210) | 0/210 |
| decider-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 96% [93, 99] | 99.0% (96.9%) | 0.0% (0/210) | 0/210 |
| decider@openrouter | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.07 | 83% [78, 89] | 98.9% (96.4%) | 0.0% (0/210) | 0/210 |
| decision-1.1@openrouter | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.02 | 89% [84, 92] | 98.9% (96.7%) | 0.0% (0/210) | 0/210 |
| decision-1@openrouter | 210 | 96.2% [93, 99] | 0.96 | 0.99 | 0.04 | 94% [91, 97] | 99.5% (97.6%) | 0.0% (0/210) | 0/210 |
| drex-max@openrouter | 210 | 98.6% [97, 100] | 0.99 | 0.99 | 0.02 | 97% [94, 99] | 99.0% (96.9%) | 0.0% (0/210) | 0/210 |
| elephant@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.06 | 96% [93, 99] | 99.5% (97.7%) | 0.0% (0/210) | 0/210 |
| gemini-decision@google | 210 | 85.2% [80, 90] | 0.83 | 0.99 | 0.06 | 31% [25, 37] | 95.4% (88.5%) | 11.4% (24/210) | 0/210 |
| jev:1.14 | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.07 | 96% [93, 98] | 99.5% (97.7%) | 0.0% (0/210) | 0/210 |
| joey@openrouter | 210 | 91.9% [88, 96] | 0.91 | 0.97 | 0.11 | 8% [5, 12] | 94.1% (75.0%) | 0.0% (0/210) | 0/210 |
| kev@openrouter | 210 | 94.8% [92, 98] | 0.94 | 0.99 | 0.19 | 55% [49, 62] | 97.4% (93.5%) | 0.0% (0/210) | 0/210 |
| luna@decisions | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.04 | 94% [90, 97] | 99.0% (96.8%) | 0.0% (0/210) | 0/210 |
| mammoth@openrouter | 210 | 98.6% [97, 100] | 0.99 | 1.00 | 0.05 | 99% [97, 100] | 99.0% (97.0%) | 0.0% (0/210) | 0/210 |
| reflex@openrouter | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.01 | 93% [90, 97] | 99.0% (96.8%) | 0.0% (0/210) | 0/210 |
| span@openrouter | 210 | 96.2% [93, 99] | 0.96 | 0.99 | 0.05 | 82% [77, 88] | 98.8% (96.4%) | 0.0% (0/210) | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 99% accuracy | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| mammoth@openrouter = | 99% [97, 100] | 99% [97, 100] | 0.57 | met |
| drex-max@openrouter = | 97% [94, 99] | 99% [97, 100] | 0.70 | met |
| clef-flash@openrouter = | 96% [93, 99] | 98% [96, 100] | 0.74 | met |
| decider-flash@openrouter = | 96% [93, 99] | 98% [96, 100] | 0.68 | met |
| elephant@openrouter = | 96% [93, 99] | 98% [96, 100] | 0.72 | met |
| d1-ultra@openrouter = | 95% [92, 98] | 98% [96, 100] | 0.69 | met |
| d1.1@openrouter = | 95% [92, 98] | 98% [96, 100] | 0.70 | met |
| d1.2 = | 94% [91, 97] | 98% [96, 100] | 0.76 | met |
| d1@vercel = | 96% [93, 99] | 98% [96, 100] | 0.79 | met |
| jev:1.14 = | 96% [93, 98] | 98% [95, 100] | 0.68 | met |
| d1.2-ultra = | 94% [91, 97] | 98% [96, 100] | 0.77 | met |
| luna@decisions = | 94% [90, 97] | 98% [95, 100] | 0.74 | met |
| reflex@openrouter = | 93% [90, 97] | 97% [95, 99] | 0.77 | met |
| decision-1@openrouter = | 94% [91, 97] | 96% [93, 99] | 0.73 | met |
| clef@openrouter | 91% [87, 95] | 98% [96, 100] | 0.90 | met |
| clef-omni@openrouter | 89% [84, 93] | 98% [95, 100] | 0.94 | met |
| decision-1.1@openrouter | 89% [84, 92] | 97% [95, 99] | 0.77 | met |
| decider@openrouter | 83% [78, 89] | 97% [95, 99] | 0.84 | met |
| span@openrouter | 82% [77, 88] | 96% [93, 99] | 0.83 | met |
| kev@openrouter | 55% [49, 62] | 95% [92, 98] | 0.72 | met |
| gemini-decision@google | 31% [25, 37] | 85% [80, 90] | 0.91 | met |
| joey@openrouter | 8% [5, 12] | 92% [88, 96] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 271 ms | 371 ms | 917 ms | 1327 ms | 3.4 | 0 | 4 | $0.14 | billed |  |
| clef-omni@openrouter | 210 | 204 ms | 267 ms | 310 ms | 354 ms | 1.5 | 0 | 4 | $0.95 | billed |  |
| clef@openrouter | 210 | 341 ms | 1505 ms | 2205 ms | 2703 ms | 6.5 | 0 | 4 | $1.23 | billed |  |
| d1-ultra@openrouter | 210 | 514 ms | 5529 ms | 5740 ms | 7750 ms | 11.2 | 15 | 4 | $0.21 | billed |  |
| d1.1@openrouter | 210 | 232 ms | 402 ms | 1038 ms | 1734 ms | 4.5 | 0 | 4 | $0.10 | billed |  |
| d1.2 | 210 | 121 ms | 167 ms | 395 ms | 439 ms | 3.3 | 0 | 4 | $0.10 | billed |  |
| d1.2-ultra | 210 | 126 ms | 167 ms | 331 ms | 448 ms | 2.6 | 0 | 4 | $0.21 | billed |  |
| d1@vercel | 210 | 571 ms | 1824 ms | 5652 ms | 6043 ms | 9.9 | 0 | 4 | $0.10 | billed |  |
| decider-flash@openrouter | 210 | 138 ms | 169 ms | 265 ms | 336 ms | 1.9 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 223 ms | 375 ms | 1126 ms | 1524 ms | 5.0 | 0 | 4 | $0.10 | billed |  |
| decision-1.1@openrouter | 210 | 229 ms | 278 ms | 447 ms | 594 ms | 1.9 | 0 | 4 | $0.22 | billed |  |
| decision-1@openrouter | 210 | 247 ms | 363 ms | 502 ms | 721 ms | 2.0 | 1 | 4 | $0.20 | billed |  |
| drex-max@openrouter | 210 | 328 ms | 556 ms | 1118 ms | 2503 ms | 3.4 | 0 | 4 | $0.31 | billed | ○ |
| elephant@openrouter | 210 | 175 ms | 292 ms | 560 ms | 1891 ms | 3.2 | 0 | 4 | $0.19 | billed |  |
| gemini-decision@google | 186 | 295 ms | 378 ms | 524 ms | 721 ms | 1.8 | 0 | 4 | $0.60 | estimated |  |
| jev:1.14 | 210 | 110 ms | 143 ms | 177 ms | 234 ms | 1.6 | 0 | 4 | $0.40 | estimated | ○ |
| joey@openrouter | 210 | 169 ms | 196 ms | 262 ms | 2386 ms | 1.5 | 0 | 4 | $0.05 | billed | ○ |
| kev@openrouter | 210 | 521 ms | 679 ms | 873 ms | 1015 ms | 1.7 | 0 | 4 | $0.19 | billed |  |
| luna@decisions | 210 | 181 ms | 359 ms | 529 ms | 578 ms | 2.9 | 0 | 4 | $0.70 | estimated |  |
| mammoth@openrouter | 210 | 182 ms | 212 ms | 273 ms | 1349 ms | 1.5 | 0 | 4 | $0.53 | billed | ○ |
| reflex@openrouter | 210 | 327 ms | 505 ms | 730 ms | 1095 ms | 2.2 | 0 | 4 | $0.22 | billed |  |
| span@openrouter | 210 | 531 ms | 763 ms | 892 ms | 980 ms | 1.7 | 0 | 4 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0030 | 16 s (estimated, 210 calls) | 12 min | 4 |
| clef-omni@openrouter | $0.02 | 11 s (estimated, 210 calls) | 9 min | 4 |
| clef@openrouter | $0.03 | 31 s (estimated, 210 calls) | 24 min | 4 |
| d1-ultra@openrouter | $0.0045 | 77 s (estimated, 210 calls) | 61 min | 4 |
| d1.1@openrouter | $0.0021 | 14 s (estimated, 210 calls) | 11 min | 4 |
| d1.2 | $0.0021 | 7 s (estimated, 210 calls) | 6 min | 4 |
| d1.2-ultra | $0.0045 | 7 s (estimated, 210 calls) | 6 min | 4 |
| d1@vercel | $0.0021 | 48 s (estimated, 210 calls) | 38 min | 4 |
| decider-flash@openrouter | $0.0011 | 8 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0022 | 15 s (estimated, 210 calls) | 12 min | 4 |
| decision-1.1@openrouter | $0.0045 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0042 | 14 s (estimated, 210 calls) | 11 min | 4 |
| drex-max@openrouter | $0.0066 | 20 s (estimated, 210 calls) | 16 min | 4 |
| elephant@openrouter | $0.0039 | 11 s (estimated, 210 calls) | 9 min | 4 |
| gemini-decision@google | $0.01 | 14 s (estimated, 186 calls) | 12 min | 4 |
| jev:1.14 | $0.0083 | 6 s (estimated, 210 calls) | 5 min | 4 |
| joey@openrouter | $0.0011 | 10 s (estimated, 210 calls) | 8 min | 4 |
| kev@openrouter | $0.0039 | 29 s (estimated, 210 calls) | 23 min | 4 |
| luna@decisions | $0.01 | 12 s (estimated, 210 calls) | 10 min | 4 |
| mammoth@openrouter | $0.01 | 10 s (estimated, 210 calls) | 8 min | 4 |
| reflex@openrouter | $0.0047 | 19 s (estimated, 210 calls) | 15 min | 4 |
| span@openrouter | $0.0012 | 29 s (estimated, 210 calls) | 23 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 99%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.
Refused: inputs the model did not take (question type, image, audio, video, PDF, length limits) and answers it declined to give. The model's limit, not a failed call: the candidate is kept, and the case stays in every denominator.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 98.1% | 97.6% | 3 | 2 | 0.35 | 0.35 |
| clef-omni@openrouter | 97.6% | 96.7% | 3 | 4 | 0.65 | 0.65 |
| clef@openrouter | 98.1% | 98.1% | 1 | 3 | 0.55 | 0.55 |
| d1-ultra@openrouter | 98.1% | 97.1% | 4 | 2 | 0.50 | 0.50 |
| d1.1@openrouter | 98.1% | 98.1% | 2 | 2 | 0.60 | 0.60 |
| d1.2 | 98.1% | 97.6% | 2 | 3 | 0.55 | 0.55 |
| d1.2-ultra | 97.6% | 97.6% | 2 | 3 | 0.60 | 0.60 |
| d1@vercel | 97.6% | 97.1% | 3 | 3 | 0.65 | 0.65 |
| decider-flash@openrouter | 98.1% | 97.6% | 3 | 2 | 0.35 | 0.35 |
| decider@openrouter | 97.1% | 97.6% | 4 | 1 | 0.25 | 0.25 |
| decision-1.1@openrouter | 97.1% | 97.1% | 2 | 4 | 0.80 | 0.80 |
| decision-1@openrouter | 96.2% | 97.6% | 2 | 3 | 0.65 | 0.65 |
| drex-max@openrouter | 98.6% | 98.1% | 3 | 1 | 0.50 | 0.50 |
| elephant@openrouter | 98.1% | 98.1% | 2 | 2 | 0.55 | 0.55 |
| gemini-decision@google | 85.2% | 86.2% | 28 | 1 | 0.35 | 0.35 |
| jev:1.14 | 97.6% | 99.0% | 2 | 0 | 0.70 | 0.70 |
| joey@openrouter | 91.9% | 91.9% | 11 | 6 | 0.35 | 0.40 |
| kev@openrouter | 94.8% | 96.7% | 7 | 0 | 0.45 | 0.45 |
| luna@decisions | 97.6% | 97.1% | 3 | 3 | 0.25 | 0.25 |
| mammoth@openrouter | 98.6% | 98.6% | 2 | 1 | 0.65 | 0.65 |
| reflex@openrouter | 97.1% | 97.1% | 4 | 2 | 0.40 | 0.40 |
| span@openrouter | 96.2% | 98.6% | 2 | 1 | 0.15 | 0.15 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 24 (23%) |
| 0.20 | 1 (1%) | 5 (5%) |
| 0.30 | 1 (1%) | 2 (2%) |
| 0.35 | 2 (2%) | 1 (1%) |
| 0.40 | 3 (3%) | 1 (1%) |
| 0.50 | 3 (3%) | 1 (1%) |
| 0.60 | 3 (3%) | 1 (1%) |
| 0.70 | 4 (4%) | 1 (1%) |
| 0.80 | 9 (9%) | 0 (0%) |
| 0.90 | 22 (21%) | 0 (0%) |

## Misses and false alarms by threshold (clef-omni@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 20 (19%) |
| 0.20 | 1 (1%) | 11 (10%) |
| 0.30 | 1 (1%) | 8 (8%) |
| 0.40 | 1 (1%) | 7 (7%) |
| 0.50 | 1 (1%) | 4 (4%) |
| 0.60 | 2 (2%) | 3 (3%) |
| 0.65 | 2 (2%) | 2 (2%) |
| 0.70 | 2 (2%) | 2 (2%) |
| 0.80 | 2 (2%) | 2 (2%) |
| 0.90 | 3 (3%) | 1 (1%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 18 (17%) |
| 0.20 | 1 (1%) | 14 (13%) |
| 0.30 | 1 (1%) | 9 (9%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 1 (1%) | 3 (3%) |
| 0.55 | 1 (1%) | 2 (2%) |
| 0.60 | 1 (1%) | 2 (2%) |
| 0.70 | 2 (2%) | 2 (2%) |
| 0.80 | 3 (3%) | 2 (2%) |
| 0.90 | 4 (4%) | 0 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 15 (14%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 4 (4%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.50 | 1 (1%) | 3 (3%) |
| 0.60 | 3 (3%) | 2 (2%) |
| 0.70 | 3 (3%) | 1 (1%) |
| 0.80 | 3 (3%) | 1 (1%) |
| 0.90 | 20 (19%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 18 (17%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 4 (4%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.50 | 1 (1%) | 3 (3%) |
| 0.60 | 1 (1%) | 2 (2%) |
| 0.70 | 2 (2%) | 1 (1%) |
| 0.80 | 4 (4%) | 0 (0%) |
| 0.90 | 6 (6%) | 0 (0%) |

## Misses and false alarms by threshold (d1.2)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 20 (19%) |
| 0.20 | 1 (1%) | 9 (9%) |
| 0.30 | 1 (1%) | 6 (6%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.50 | 1 (1%) | 3 (3%) |
| 0.55 | 1 (1%) | 2 (2%) |
| 0.60 | 2 (2%) | 2 (2%) |
| 0.70 | 3 (3%) | 2 (2%) |
| 0.80 | 3 (3%) | 0 (0%) |
| 0.90 | 5 (5%) | 0 (0%) |

## Misses and false alarms by threshold (d1.2-ultra)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 15 (14%) |
| 0.20 | 1 (1%) | 11 (10%) |
| 0.30 | 1 (1%) | 6 (6%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 2 (2%) | 3 (3%) |
| 0.60 | 2 (2%) | 2 (2%) |
| 0.70 | 2 (2%) | 2 (2%) |
| 0.80 | 5 (5%) | 0 (0%) |
| 0.90 | 7 (7%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 8 (8%) |
| 0.20 | 2 (2%) | 4 (4%) |
| 0.30 | 2 (2%) | 3 (3%) |
| 0.40 | 2 (2%) | 3 (3%) |
| 0.50 | 2 (2%) | 3 (3%) |
| 0.60 | 3 (3%) | 1 (1%) |
| 0.65 | 3 (3%) | 0 (0%) |
| 0.70 | 3 (3%) | 0 (0%) |
| 0.80 | 4 (4%) | 0 (0%) |
| 0.90 | 8 (8%) | 0 (0%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 13 (12%) |
| 0.20 | 1 (1%) | 5 (5%) |
| 0.30 | 1 (1%) | 2 (2%) |
| 0.35 | 1 (1%) | 2 (2%) |
| 0.40 | 3 (3%) | 2 (2%) |
| 0.50 | 3 (3%) | 1 (1%) |
| 0.60 | 3 (3%) | 1 (1%) |
| 0.70 | 4 (4%) | 1 (1%) |
| 0.80 | 14 (13%) | 0 (0%) |
| 0.90 | 43 (41%) | 0 (0%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 6 (6%) |
| 0.20 | 2 (2%) | 1 (1%) |
| 0.25 | 2 (2%) | 1 (1%) |
| 0.30 | 3 (3%) | 1 (1%) |
| 0.40 | 5 (5%) | 0 (0%) |
| 0.50 | 6 (6%) | 0 (0%) |
| 0.60 | 9 (9%) | 0 (0%) |
| 0.70 | 19 (18%) | 0 (0%) |
| 0.80 | 38 (36%) | 0 (0%) |
| 0.90 | 62 (59%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 13 (12%) |
| 0.20 | 1 (1%) | 11 (10%) |
| 0.30 | 1 (1%) | 7 (7%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 1 (1%) | 5 (5%) |
| 0.60 | 1 (1%) | 3 (3%) |
| 0.70 | 1 (1%) | 3 (3%) |
| 0.80 | 2 (2%) | 1 (1%) |
| 0.90 | 3 (3%) | 1 (1%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 15 (14%) |
| 0.20 | 1 (1%) | 11 (10%) |
| 0.30 | 1 (1%) | 7 (7%) |
| 0.40 | 1 (1%) | 6 (6%) |
| 0.50 | 2 (2%) | 6 (6%) |
| 0.60 | 2 (2%) | 5 (5%) |
| 0.65 | 2 (2%) | 3 (3%) |
| 0.70 | 4 (4%) | 2 (2%) |
| 0.80 | 10 (10%) | 0 (0%) |
| 0.90 | 22 (21%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 8 (8%) |
| 0.20 | 1 (1%) | 3 (3%) |
| 0.30 | 2 (2%) | 1 (1%) |
| 0.40 | 3 (3%) | 0 (0%) |
| 0.50 | 3 (3%) | 0 (0%) |
| 0.60 | 3 (3%) | 0 (0%) |
| 0.70 | 4 (4%) | 0 (0%) |
| 0.80 | 8 (8%) | 0 (0%) |
| 0.90 | 15 (14%) | 0 (0%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 22 (21%) |
| 0.20 | 1 (1%) | 11 (10%) |
| 0.30 | 2 (2%) | 3 (3%) |
| 0.40 | 2 (2%) | 3 (3%) |
| 0.50 | 2 (2%) | 2 (2%) |
| 0.55 | 2 (2%) | 1 (1%) |
| 0.60 | 3 (3%) | 1 (1%) |
| 0.70 | 4 (4%) | 1 (1%) |
| 0.80 | 12 (11%) | 0 (0%) |
| 0.90 | 31 (30%) | 0 (0%) |

## Misses and false alarms by threshold (gemini-decision@google)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (25%) | 5 (5%) |
| 0.20 | 26 (25%) | 2 (2%) |
| 0.30 | 28 (27%) | 0 (0%) |
| 0.35 | 28 (27%) | 0 (0%) |
| 0.40 | 30 (29%) | 0 (0%) |
| 0.50 | 31 (30%) | 0 (0%) |
| 0.60 | 35 (33%) | 0 (0%) |
| 0.70 | 46 (44%) | 0 (0%) |
| 0.80 | 64 (61%) | 0 (0%) |
| 0.90 | 87 (83%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 21 (20%) |
| 0.20 | 1 (1%) | 12 (11%) |
| 0.30 | 1 (1%) | 11 (10%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 1 (1%) | 4 (4%) |
| 0.60 | 1 (1%) | 4 (4%) |
| 0.70 | 2 (2%) | 0 (0%) |
| 0.80 | 12 (11%) | 0 (0%) |
| 0.90 | 38 (36%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 61 (58%) |
| 0.20 | 4 (4%) | 18 (17%) |
| 0.30 | 7 (7%) | 7 (7%) |
| 0.40 | 11 (10%) | 3 (3%) |
| 0.50 | 15 (14%) | 2 (2%) |
| 0.60 | 24 (23%) | 1 (1%) |
| 0.70 | 43 (41%) | 1 (1%) |
| 0.80 | 63 (60%) | 0 (0%) |
| 0.90 | 93 (89%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 67 (64%) |
| 0.20 | 1 (1%) | 22 (21%) |
| 0.30 | 3 (3%) | 8 (8%) |
| 0.40 | 5 (5%) | 3 (3%) |
| 0.45 | 7 (7%) | 0 (0%) |
| 0.50 | 11 (10%) | 0 (0%) |
| 0.60 | 32 (30%) | 0 (0%) |
| 0.70 | 69 (66%) | 0 (0%) |
| 0.80 | 98 (93%) | 0 (0%) |
| 0.90 | 104 (99%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 9 (9%) |
| 0.20 | 1 (1%) | 4 (4%) |
| 0.25 | 1 (1%) | 3 (3%) |
| 0.30 | 2 (2%) | 3 (3%) |
| 0.40 | 2 (2%) | 3 (3%) |
| 0.50 | 2 (2%) | 3 (3%) |
| 0.60 | 5 (5%) | 2 (2%) |
| 0.70 | 7 (7%) | 2 (2%) |
| 0.80 | 11 (10%) | 0 (0%) |
| 0.90 | 28 (27%) | 0 (0%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 24 (23%) |
| 0.20 | 1 (1%) | 10 (10%) |
| 0.30 | 1 (1%) | 6 (6%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.50 | 2 (2%) | 1 (1%) |
| 0.60 | 2 (2%) | 1 (1%) |
| 0.65 | 2 (2%) | 0 (0%) |
| 0.70 | 3 (3%) | 0 (0%) |
| 0.80 | 4 (4%) | 0 (0%) |
| 0.90 | 18 (17%) | 0 (0%) |

## Misses and false alarms by threshold (reflex@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 3 (3%) |
| 0.20 | 2 (2%) | 3 (3%) |
| 0.30 | 3 (3%) | 2 (2%) |
| 0.40 | 3 (3%) | 1 (1%) |
| 0.50 | 5 (5%) | 1 (1%) |
| 0.60 | 7 (7%) | 0 (0%) |
| 0.70 | 7 (7%) | 0 (0%) |
| 0.80 | 9 (9%) | 0 (0%) |
| 0.90 | 17 (16%) | 0 (0%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 4 (4%) |
| 0.15 | 1 (1%) | 1 (1%) |
| 0.20 | 2 (2%) | 1 (1%) |
| 0.30 | 4 (4%) | 1 (1%) |
| 0.40 | 5 (5%) | 1 (1%) |
| 0.50 | 8 (8%) | 0 (0%) |
| 0.60 | 9 (9%) | 0 (0%) |
| 0.70 | 19 (18%) | 0 (0%) |
| 0.80 | 34 (32%) | 0 (0%) |
| 0.90 | 59 (56%) | 0 (0%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.97 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**clef-omni@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.96 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |
| t01586 | False | True | 0.94 | # 最終的に上半身裸になるまで脱ぐまんさんを発見  2022年05月09日  カテゴリ: おもしろ  1: たのしい名無し 2022/05… |

**clef@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.97 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1-ultra@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1.1@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1.2** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.96 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1.2-ultra** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.95 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1@vercel** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**decider-flash@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.99 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**decider@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**decision-1.1@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |
| t01586 | False | True | 0.98 | # 最終的に上半身裸になるまで脱ぐまんさんを発見  2022年05月09日  カテゴリ: おもしろ  1: たのしい名無し 2022/05… |

**decision-1@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**drex-max@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**elephant@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**gemini-decision@google** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.99 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |
| t01677 | True | False | 0.91 | # 【エルデンリング】コイツ大谷翔平みたいなスタイルしてるよな  2022年03月25日  505:名無しの民 ID:JBI3JZGyr … |

**jev:1.14** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.98 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**joey@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.97 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**kev@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.91 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**luna@decisions** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**mammoth@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.97 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**reflex@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**span@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |


## Cases the models disagree on (12 of 39)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t01740 | True | True (0.92) | True (0.95) | True (0.96) | True (0.96) | True (0.98) | True (0.96) | True (0.98) | True (0.93) | True (0.91) | True (0.81) | True (1.00) | True (0.96) | True (0.97) | True (0.92) | True (0.87) | True (0.92) | False (0.64) | True (0.51) | True (1.00) | True (0.88) | True (0.99) | True (0.85) | ## 【柏木さりな】発育が止まらないエチエチJKのフレッシュ腋  ◆女性歌手・女性芸能人  弱冠17歳にして、最近は大人の色気がどんどん強… |
| t01466 | True | True (0.86) | True (0.97) | True (0.96) | True (0.96) | True (0.98) | True (0.97) | True (0.94) | True (0.99) | True (0.89) | True (0.74) | True (1.00) | True (0.96) | True (0.93) | True (0.91) | — | True (0.95) | False (0.67) | True (0.75) | True (1.00) | True (0.96) | True (0.93) | True (0.94) | # スマホで楽しめるCG集も発売！  # 「ドスケベビッチな○学生のセックス三昧七日間戦争 ～ホームレスからひみつ基地をとり戻せ!～」前編… |
| t00271 | False | False (0.84) | True (0.55) | False (0.96) | False (0.99) | False (0.99) | False (0.98) | False (0.98) | False (1.00) | False (0.97) | False (0.99) | False (1.00) | False (0.99) | False (1.00) | False (0.96) | False (0.97) | False (0.96) | False (0.83) | False (0.89) | False (0.99) | False (0.87) | False (1.00) | False (1.00) | 女性への贈り物 > スキャルプローション  # スキャルプローション  # 若い男性.女性,高校生.薄毛.育毛,頭皮,抜け毛,予防,ローシ… |
| t01437 | True | True (0.92) | True (0.97) | True (0.98) | True (0.94) | True (0.97) | True (0.98) | True (0.96) | True (0.94) | True (0.89) | True (0.70) | True (1.00) | True (0.93) | True (0.96) | True (0.86) | True (0.56) | True (0.81) | True (0.70) | False (0.56) | True (0.90) | True (0.93) | True (0.88) | True (0.81) | 大人気！母乳の『るる』さん  スリーサイズ バスト：84cm ウエスト：57cm ヒップ：81cm 身長・体重 身長：150cm- タイプ… |
| t01783 | True | True (0.95) | True (0.98) | True (0.98) | True (0.97) | True (0.98) | True (0.95) | True (0.98) | True (0.98) | True (0.92) | True (0.92) | True (1.00) | True (0.99) | True (0.99) | True (0.93) | True (0.91) | True (0.93) | False (0.88) | True (0.72) | True (0.95) | True (0.98) | True (1.00) | True (0.97) | 写メ日記 ほたるの写メ日記  ### ほたるの写メ日記  #### おち○ちんおっきくなってるよ？2023/02/03 21:01  あれ… |
| t01624 | True | True (0.89) | True (0.97) | True (0.97) | True (0.98) | True (0.99) | True (0.98) | True (0.98) | True (0.98) | True (0.94) | True (0.93) | True (1.00) | True (0.98) | True (0.99) | True (0.91) | — | True (0.87) | True (0.77) | False (0.52) | True (0.91) | True (0.98) | True (0.98) | True (0.72) | # 乳首攻めで何度もメスイキさせた体験談  2021/2/17（2年前）  【受付からプレイ開始までの流れ】  電話で丁寧に案内していただ… |
| t01562 | True | True (0.93) | True (0.97) | True (0.98) | True (0.97) | True (0.98) | True (0.98) | True (0.93) | True (0.99) | True (0.90) | True (0.77) | True (1.00) | True (0.87) | True (0.94) | True (0.89) | True (0.89) | True (0.89) | False (0.86) | True (0.74) | True (0.94) | True (0.94) | True (0.87) | True (0.84) | # 【アウトレット】激震パイ揺れ！暴走腰振り騎乗位 厳選ベスト5時間 オマ○コ感度無限大オーガズムお見せします!! (AV) [7LZBS… |
| t01370 | True | True (0.94) | True (0.97) | True (0.98) | True (0.90) | True (0.95) | True (0.97) | True (0.96) | True (0.98) | True (0.84) | True (0.73) | True (1.00) | True (0.94) | True (0.96) | True (0.91) | True (0.79) | True (0.80) | True (0.88) | False (0.51) | True (0.80) | True (0.91) | True (0.97) | True (0.80) | パイパン キス 業界未経験 未経験 熟女 黒髪  出勤予定 6月10日(土)6月11日(日)6月12日(月)6月13日(火)6月14日(水… |
| t00277 | False | False (0.91) | False (0.85) | False (0.71) | False (0.91) | False (0.82) | False (0.83) | False (0.92) | False (0.89) | False (0.92) | False (0.94) | False (0.77) | False (0.78) | False (0.96) | False (0.87) | False (0.97) | False (0.81) | True (0.78) | False (0.83) | False (0.97) | False (0.82) | False (1.00) | False (1.00) | ◆ e-Bookのタイトル 『【PRIDE】たった1つのブログで月に4記事書くだけで月8万稼いでいるブログアフィリエイト（アドセンス+楽天… |
| t01599 | True | True (0.90) | True (0.97) | True (0.98) | True (0.95) | True (0.98) | True (0.98) | True (0.95) | True (0.99) | True (0.84) | True (0.84) | True (1.00) | True (0.84) | True (0.97) | True (0.92) | True (0.81) | True (0.92) | False (0.77) | True (0.78) | True (0.95) | True (0.94) | True (0.96) | True (0.88) | # オマエ、いい歳してまだ童貞なのかよー!! wwウチらがヌキまくってヤリチンに育ててやんよw 同窓会で10年ぶりに再会した元ギャル同級生… |
| t00085 | False | False (0.90) | False (0.90) | False (0.88) | False (0.93) | False (0.98) | False (0.96) | False (0.95) | False (1.00) | False (0.96) | False (0.99) | False (0.95) | True (0.65) | False (0.98) | False (0.86) | False (0.97) | False (0.69) | False (0.82) | False (0.84) | False (0.95) | False (0.77) | False (1.00) | False (0.99) | トップページ ＞ 車におけるバッテリーの上がりについて ＞ 160326  車におけるバッテリーの上がりについてブログ：160326 夏は… |
| t01310 | True | True (0.83) | True (0.96) | True (0.97) | True (0.84) | True (0.97) | True (0.94) | True (0.96) | True (0.94) | True (0.82) | True (0.84) | True (1.00) | True (0.85) | True (0.96) | True (0.90) | True (0.76) | True (0.74) | False (0.68) | True (0.74) | True (0.53) | True (0.96) | True (0.94) | True (0.96) | 他の男の精液で孕むとき３ ～襖の奥でイキ狂う僕の妻～  西野 風花：夢月 やみ  他の男の精液で孕むとき３ 120×600バナー  他の男… |
