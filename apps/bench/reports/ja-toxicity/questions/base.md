# ja-toxicity

2026-10-31 · 210 labelled dev cases (True 105, False 105) · split: stratified k-fold (no test case among these: CV numbers only) · source: LLM-jp Toxicity Dataset（LLM-jp, CC BY 4.0）の 1,000 字以下から toxic / nontoxic 各 150 件

**clef@openrouter** has the highest accuracy (all), 99% [97, 100] (API cost $1.23 per 10k, p99 5593ms). Its interval overlaps with clef-flash@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, jev:1.14, kev@openrouter, luna@decisions, mammoth@openrouter, mercury@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is clef@openrouter's, 99% [97, 100].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 98.6% [97, 100] | 0.99 | 0.99 | 0.05 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.04 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.03 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| d1@vercel | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.01 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.07 | 100% [99, 100] | 97.1% (94.4%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 96.2% [93, 99] | 0.96 | 0.99 | 0.03 | 100% [99, 100] | 96.7% (93.8%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 98.6% [97, 100] | 0.99 | 0.99 | 0.03 | 100% [99, 100] | 99.0% (97.0%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.06 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 97.6% [96, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 91.9% [88, 96] | 0.91 | 0.97 | 0.11 | 82% [77, 87] | 94.8% (91.0%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 94.8% [92, 98] | 0.94 | 0.99 | 0.19 | 99% [98, 100] | 95.2% (92.0%) | 0/210 | 0/210 |
| luna@decisions | 210 | 97.6% [96, 100] | 0.98 | 0.99 | 0.04 | 100% [100, 100] | 97.6% (95.1%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 98.1% [96, 100] | 0.98 | 1.00 | 0.05 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| mercury@openrouter | 210 | 95.7% [93, 98] | 0.96 | 0.99 | 0.02 | 100% [99, 100] | 95.7% (92.6%) | 0/210 | 0/210 |
| span@openrouter | 210 | 95.2% [92, 98] | 0.95 | 0.99 | 0.04 | 100% [99, 100] | 95.7% (92.6%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 98% [95, 100] | 0.35 | met |
| clef@openrouter = | 99% [97, 100] | 0.50 | met |
| d1-ultra@openrouter = | 98% [96, 100] | 0.75 | met |
| d1.1@openrouter = | 98% [96, 100] | 0.45 | met |
| d1@vercel = | 97% [94, 99] | 0.70 | met |
| decider-flash@openrouter = | 98% [95, 100] | 0.35 | met |
| decider@openrouter = | 99% [97, 100] | 0.15 | met |
| decision-1@openrouter = | 96% [93, 99] | 0.65 | met |
| drex-max@openrouter = | 99% [97, 100] | 0.45 | met |
| elephant@openrouter = | 98% [96, 100] | 0.55 | met |
| jev:1.14 = | 97% [95, 99] | 0.65 | met |
| kev@openrouter = | 96% [93, 99] | 0.45 | met |
| luna@decisions = | 97% [95, 99] | 0.25 | met |
| mammoth@openrouter = | 98% [96, 100] | 0.55 | met |
| mercury@openrouter = | 96% [93, 98] | 0.15 | met |
| span@openrouter = | 99% [97, 100] | 0.15 | met |
| joey@openrouter | 92% [89, 96] | 0.40 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 421 ms | 578 ms | 983 ms | 1025 ms | 2.3 | 0 | 8 | $0.12 | billed | ○ |
| clef@openrouter | 210 | 1491 ms | 1960 ms | 5593 ms | 8331 ms | 3.8 | 0 | 8 | $1.23 | billed |  |
| d1-ultra@openrouter | 210 | 1312 ms | 2135 ms | 5505 ms | 8408 ms | 4.2 | 0 | 8 | $0.21 | billed |  |
| d1.1@openrouter | 210 | 1275 ms | 2024 ms | 3854 ms | 5354 ms | 3.0 | 0 | 8 | $0.10 | billed | ○ |
| d1@vercel | 210 | 221 ms | 293 ms | 514 ms | 580 ms | 2.3 | 0 | 8 | $0.10 | billed | ○ |
| decider-flash@openrouter | 210 | 1229 ms | 1875 ms | 4055 ms | 5547 ms | 3.3 | 0 | 8 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 1300 ms | 2182 ms | 5397 ms | 6307 ms | 4.2 | 0 | 8 | $0.10 | billed |  |
| decision-1@openrouter | 210 | 1417 ms | 2176 ms | 5457 ms | 8101 ms | 3.9 | 0 | 8 | $0.20 | billed |  |
| drex-max@openrouter | 210 | 1495 ms | 2293 ms | 4009 ms | 4243 ms | 2.7 | 0 | 8 | $0.31 | billed | ○ |
| elephant@openrouter | 210 | 1294 ms | 2146 ms | 4968 ms | 5399 ms | 3.8 | 0 | 8 | $0.19 | billed |  |
| jev:1.14 | 210 | 1232 ms | 2002 ms | 5467 ms | 6364 ms | 4.4 | 0 | 8 | $0.40 | estimated |  |
| joey@openrouter | 210 | 1258 ms | 2129 ms | 5361 ms | 5489 ms | 4.3 | 0 | 8 | $0.05 | billed |  |
| kev@openrouter | 210 | 1496 ms | 2177 ms | 4379 ms | 6600 ms | 2.9 | 0 | 8 | $0.19 | billed |  |
| luna@decisions | 210 | 1372 ms | 2212 ms | 3048 ms | 3380 ms | 2.2 | 0 | 8 | $0.70 | estimated |  |
| mammoth@openrouter | 210 | 1354 ms | 2112 ms | 5399 ms | 8189 ms | 4.0 | 0 | 8 | $0.53 | billed |  |
| mercury@openrouter | 210 | 1392 ms | 2075 ms | 7740 ms | 8112 ms | 5.6 | 1 | 8 | $0.10 | billed |  |
| span@openrouter | 210 | 1426 ms | 1991 ms | 4277 ms | 6426 ms | 3.0 | 0 | 8 | $0.06 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0026 | 11 s (estimated, 210 calls) | 9 min | 8 |
| clef@openrouter | $0.03 | 41 s (estimated, 210 calls) | 32 min | 8 |
| d1-ultra@openrouter | $0.0045 | 41 s (estimated, 210 calls) | 32 min | 8 |
| d1.1@openrouter | $0.0021 | 37 s (estimated, 210 calls) | 29 min | 8 |
| d1@vercel | $0.0021 | 6 s (estimated, 210 calls) | 5 min | 8 |
| decider-flash@openrouter | $0.0011 | 35 s (estimated, 210 calls) | 28 min | 8 |
| decider@openrouter | $0.0022 | 39 s (estimated, 210 calls) | 31 min | 8 |
| decision-1@openrouter | $0.0042 | 40 s (estimated, 210 calls) | 32 min | 8 |
| drex-max@openrouter | $0.0066 | 40 s (estimated, 210 calls) | 32 min | 8 |
| elephant@openrouter | $0.0039 | 38 s (estimated, 210 calls) | 30 min | 8 |
| jev:1.14 | $0.0083 | 37 s (estimated, 210 calls) | 30 min | 8 |
| joey@openrouter | $0.0011 | 38 s (estimated, 210 calls) | 30 min | 8 |
| kev@openrouter | $0.0039 | 41 s (estimated, 210 calls) | 32 min | 8 |
| luna@decisions | $0.01 | 39 s (estimated, 210 calls) | 31 min | 8 |
| mammoth@openrouter | $0.01 | 39 s (estimated, 210 calls) | 31 min | 8 |
| mercury@openrouter | $0.0021 | 40 s (estimated, 210 calls) | 32 min | 8 |
| span@openrouter | $0.0012 | 40 s (estimated, 210 calls) | 32 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 98.1% | 97.6% | 3 | 2 | 0.35 | 0.35 |
| clef@openrouter | 98.6% | 98.6% | 1 | 2 | 0.50 | 0.50 |
| d1-ultra@openrouter | 98.1% | 98.1% | 3 | 1 | 0.75 | 0.75 |
| d1.1@openrouter | 98.1% | 98.1% | 2 | 2 | 0.45 | 0.45 |
| d1@vercel | 97.6% | 96.7% | 4 | 3 | 0.70 | 0.70 |
| decider-flash@openrouter | 98.1% | 97.6% | 3 | 2 | 0.35 | 0.35 |
| decider@openrouter | 97.1% | 98.6% | 2 | 1 | 0.15 | 0.15 |
| decision-1@openrouter | 96.2% | 96.2% | 2 | 6 | 0.65 | 0.65 |
| drex-max@openrouter | 98.6% | 98.6% | 3 | 0 | 0.45 | 0.45 |
| elephant@openrouter | 98.1% | 98.1% | 2 | 2 | 0.55 | 0.55 |
| jev:1.14 | 97.6% | 97.1% | 2 | 4 | 0.65 | 0.65 |
| joey@openrouter | 91.9% | 92.4% | 11 | 5 | 0.40 | 0.40 |
| kev@openrouter | 94.8% | 96.2% | 7 | 1 | 0.45 | 0.45 |
| luna@decisions | 97.6% | 97.1% | 3 | 3 | 0.25 | 0.25 |
| mammoth@openrouter | 98.1% | 98.1% | 3 | 1 | 0.55 | 0.55 |
| mercury@openrouter | 95.7% | 95.7% | 7 | 2 | 0.15 | 0.15 |
| span@openrouter | 95.2% | 98.6% | 2 | 1 | 0.15 | 0.15 |

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
| 0.90 | 21 (20%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 19 (18%) |
| 0.20 | 1 (1%) | 13 (12%) |
| 0.30 | 1 (1%) | 7 (7%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 1 (1%) | 2 (2%) |
| 0.60 | 1 (1%) | 2 (2%) |
| 0.70 | 2 (2%) | 2 (2%) |
| 0.80 | 2 (2%) | 2 (2%) |
| 0.90 | 4 (4%) | 0 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 16 (15%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 5 (5%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.50 | 1 (1%) | 3 (3%) |
| 0.60 | 3 (3%) | 3 (3%) |
| 0.70 | 3 (3%) | 2 (2%) |
| 0.75 | 3 (3%) | 0 (0%) |
| 0.80 | 3 (3%) | 0 (0%) |
| 0.90 | 16 (15%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 16 (15%) |
| 0.20 | 1 (1%) | 9 (9%) |
| 0.30 | 1 (1%) | 3 (3%) |
| 0.40 | 1 (1%) | 2 (2%) |
| 0.45 | 1 (1%) | 2 (2%) |
| 0.50 | 2 (2%) | 2 (2%) |
| 0.60 | 2 (2%) | 2 (2%) |
| 0.70 | 2 (2%) | 2 (2%) |
| 0.80 | 4 (4%) | 0 (0%) |
| 0.90 | 8 (8%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 7 (7%) |
| 0.20 | 2 (2%) | 4 (4%) |
| 0.30 | 2 (2%) | 3 (3%) |
| 0.40 | 2 (2%) | 3 (3%) |
| 0.50 | 3 (3%) | 2 (2%) |
| 0.60 | 3 (3%) | 2 (2%) |
| 0.70 | 3 (3%) | 1 (1%) |
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
| 0.15 | 1 (1%) | 1 (1%) |
| 0.20 | 2 (2%) | 1 (1%) |
| 0.30 | 3 (3%) | 1 (1%) |
| 0.40 | 5 (5%) | 0 (0%) |
| 0.50 | 6 (6%) | 0 (0%) |
| 0.60 | 9 (9%) | 0 (0%) |
| 0.70 | 18 (17%) | 0 (0%) |
| 0.80 | 39 (37%) | 0 (0%) |
| 0.90 | 62 (59%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 15 (14%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 7 (7%) |
| 0.40 | 1 (1%) | 7 (7%) |
| 0.50 | 2 (2%) | 6 (6%) |
| 0.60 | 2 (2%) | 5 (5%) |
| 0.65 | 2 (2%) | 4 (4%) |
| 0.70 | 5 (5%) | 2 (2%) |
| 0.80 | 10 (10%) | 0 (0%) |
| 0.90 | 24 (23%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 8 (8%) |
| 0.20 | 1 (1%) | 3 (3%) |
| 0.30 | 2 (2%) | 1 (1%) |
| 0.40 | 2 (2%) | 0 (0%) |
| 0.45 | 2 (2%) | 0 (0%) |
| 0.50 | 3 (3%) | 0 (0%) |
| 0.60 | 3 (3%) | 0 (0%) |
| 0.70 | 4 (4%) | 0 (0%) |
| 0.80 | 7 (7%) | 0 (0%) |
| 0.90 | 16 (15%) | 0 (0%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 20 (19%) |
| 0.20 | 1 (1%) | 11 (10%) |
| 0.30 | 2 (2%) | 3 (3%) |
| 0.40 | 2 (2%) | 3 (3%) |
| 0.50 | 2 (2%) | 2 (2%) |
| 0.55 | 2 (2%) | 1 (1%) |
| 0.60 | 2 (2%) | 1 (1%) |
| 0.70 | 4 (4%) | 1 (1%) |
| 0.80 | 10 (10%) | 0 (0%) |
| 0.90 | 29 (28%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 20 (19%) |
| 0.20 | 1 (1%) | 14 (13%) |
| 0.30 | 1 (1%) | 11 (10%) |
| 0.40 | 1 (1%) | 4 (4%) |
| 0.50 | 1 (1%) | 4 (4%) |
| 0.60 | 2 (2%) | 3 (3%) |
| 0.65 | 2 (2%) | 2 (2%) |
| 0.70 | 4 (4%) | 1 (1%) |
| 0.80 | 12 (11%) | 0 (0%) |
| 0.90 | 37 (35%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 62 (59%) |
| 0.20 | 4 (4%) | 18 (17%) |
| 0.30 | 7 (7%) | 7 (7%) |
| 0.40 | 11 (10%) | 3 (3%) |
| 0.50 | 15 (14%) | 2 (2%) |
| 0.60 | 22 (21%) | 1 (1%) |
| 0.70 | 40 (38%) | 1 (1%) |
| 0.80 | 62 (59%) | 0 (0%) |
| 0.90 | 93 (89%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 67 (64%) |
| 0.20 | 1 (1%) | 22 (21%) |
| 0.30 | 3 (3%) | 8 (8%) |
| 0.40 | 5 (5%) | 2 (2%) |
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
| 0.10 | 1 (1%) | 23 (22%) |
| 0.20 | 1 (1%) | 10 (10%) |
| 0.30 | 1 (1%) | 5 (5%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.50 | 2 (2%) | 2 (2%) |
| 0.55 | 2 (2%) | 1 (1%) |
| 0.60 | 2 (2%) | 1 (1%) |
| 0.70 | 3 (3%) | 0 (0%) |
| 0.80 | 4 (4%) | 0 (0%) |
| 0.90 | 17 (16%) | 0 (0%) |

## Misses and false alarms by threshold (mercury@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 4 (4%) | 2 (2%) |
| 0.15 | 4 (4%) | 2 (2%) |
| 0.20 | 6 (6%) | 2 (2%) |
| 0.30 | 6 (6%) | 2 (2%) |
| 0.40 | 7 (7%) | 2 (2%) |
| 0.50 | 8 (8%) | 1 (1%) |
| 0.60 | 11 (10%) | 0 (0%) |
| 0.70 | 12 (11%) | 0 (0%) |
| 0.80 | 18 (17%) | 0 (0%) |
| 0.90 | 26 (25%) | 0 (0%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 4 (4%) |
| 0.15 | 1 (1%) | 1 (1%) |
| 0.20 | 2 (2%) | 1 (1%) |
| 0.30 | 4 (4%) | 1 (1%) |
| 0.40 | 5 (5%) | 0 (0%) |
| 0.50 | 10 (10%) | 0 (0%) |
| 0.60 | 14 (13%) | 0 (0%) |
| 0.70 | 20 (19%) | 0 (0%) |
| 0.80 | 34 (32%) | 0 (0%) |
| 0.90 | 59 (56%) | 0 (0%) |

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.97 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**clef@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.97 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1-ultra@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.99 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1.1@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.99 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

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

**jev:1.14** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.99 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

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

**mercury@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |
| t01769 | True | False | 0.96 | ▽ あ～ちんさんの書き込み 【SM交際】  上げ上げのノリノリ～ヽ(^o^)丿  #### メールを返信  新規エントリー＆メッセージ送信… |
| t01677 | True | False | 0.95 | # 【エルデンリング】コイツ大谷翔平みたいなスタイルしてるよな  2022年03月25日  505:名無しの民 ID:JBI3JZGyr … |
| t00953 | True | False | 0.93 | 公開日： 2014/07/16 : 最終更新日：2014/08/02 未分類  まだまだ被害が続いているLINEの不正アクセス。不正アクセ… |

**span@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |


## Cases the models disagree on (12 of 36)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t01740 | True | True (0.90) | True (0.96) | True (0.95) | True (0.97) | True (0.90) | True (0.91) | True (0.79) | True (0.97) | True (0.97) | True (0.92) | True (0.93) | False (0.65) | True (0.51) | True (1.00) | True (0.88) | True (0.90) | True (0.85) | ## 【柏木さりな】発育が止まらないエチエチJKのフレッシュ腋  ◆女性歌手・女性芸能人  弱冠17歳にして、最近は大人の色気がどんどん強… |
| t01466 | True | True (0.86) | True (0.97) | True (0.95) | True (0.98) | True (0.98) | True (0.89) | True (0.74) | True (0.94) | True (0.93) | True (0.91) | True (0.95) | False (0.66) | True (0.75) | True (1.00) | True (0.95) | True (0.99) | True (0.94) | # スマホで楽しめるCG集も発売！  # 「ドスケベビッチな○学生のセックス三昧七日間戦争 ～ホームレスからひみつ基地をとり戻せ!～」前編… |
| t00277 | False | False (0.91) | False (0.76) | False (0.89) | False (0.85) | False (0.89) | False (0.92) | False (0.93) | False (0.84) | False (0.96) | False (0.87) | False (0.80) | True (0.79) | False (0.83) | False (0.97) | False (0.82) | False (1.00) | False (1.00) | ◆ e-Bookのタイトル 『【PRIDE】たった1つのブログで月に4記事書くだけで月8万稼いでいるブログアフィリエイト（アドセンス+楽天… |
| t00577 | False | False (0.92) | False (0.51) | False (0.81) | False (0.90) | False (0.98) | False (0.80) | False (0.86) | False (0.88) | False (0.82) | False (0.72) | True (0.61) | False (0.75) | False (0.79) | False (0.95) | False (0.73) | False (0.99) | False (0.87) | # 神谷明の給料は1本10万円  声優の神谷明（かみやあきら＝53歳）が関西テレビ系番組「マルコポロリ」に出演して、給料を暴露しました。 … |
| t00085 | False | False (0.90) | False (0.87) | False (0.89) | False (0.98) | False (0.99) | False (0.96) | False (0.99) | True (0.65) | False (0.98) | False (0.87) | False (0.69) | False (0.82) | False (0.84) | False (0.95) | False (0.77) | False (0.98) | False (0.99) | トップページ ＞ 車におけるバッテリーの上がりについて ＞ 160326  車におけるバッテリーの上がりについてブログ：160326 夏は… |
| t01783 | True | True (0.95) | True (0.98) | True (0.98) | True (0.98) | True (0.98) | True (0.92) | True (0.92) | True (0.99) | True (0.99) | True (0.94) | True (0.93) | False (0.88) | True (0.72) | True (0.95) | True (0.98) | True (0.99) | True (0.97) | 写メ日記 ほたるの写メ日記  ### ほたるの写メ日記  #### おち○ちんおっきくなってるよ？2023/02/03 21:01  あれ… |
| t01599 | True | True (0.89) | True (0.98) | True (0.96) | True (0.98) | True (0.99) | True (0.84) | True (0.84) | True (0.88) | True (0.97) | True (0.93) | True (0.92) | False (0.77) | True (0.77) | True (0.95) | True (0.93) | True (0.99) | True (0.88) | # オマエ、いい歳してまだ童貞なのかよー!! wwウチらがヌキまくってヤリチンに育ててやんよw 同窓会で10年ぶりに再会した元ギャル同級生… |
| t01624 | True | True (0.91) | True (0.97) | True (0.99) | True (0.98) | True (0.98) | True (0.94) | True (0.93) | True (0.98) | True (0.99) | True (0.91) | True (0.88) | True (0.77) | False (0.52) | True (0.91) | True (0.97) | True (0.98) | True (0.62) | # 乳首攻めで何度もメスイキさせた体験談  2021/2/17（2年前）  【受付からプレイ開始までの流れ】  電話で丁寧に案内していただ… |
| t01519 | True | True (0.92) | True (0.97) | True (0.98) | True (0.99) | True (0.98) | True (0.95) | True (0.84) | True (0.96) | True (0.97) | True (0.88) | True (0.83) | False (0.53) | True (0.64) | True (0.85) | True (0.94) | True (0.95) | True (0.71) | # 素人娘尻アナル大全　※サンプル動画あり  トップページ ＞ アナル・菊門・尻穴 作品 一覧 ＞ 素人娘尻アナル大全　※サンプル動画あり… |
| t01562 | True | True (0.93) | True (0.98) | True (0.96) | True (0.99) | True (0.98) | True (0.90) | True (0.77) | True (0.88) | True (0.94) | True (0.90) | True (0.90) | False (0.86) | True (0.73) | True (0.94) | True (0.94) | True (0.95) | True (0.84) | # 【アウトレット】激震パイ揺れ！暴走腰振り騎乗位 厳選ベスト5時間 オマ○コ感度無限大オーガズムお見せします!! (AV) [7LZBS… |
| t00106 | False | False (0.89) | False (0.80) | False (0.90) | False (0.80) | False (0.97) | False (0.88) | False (0.91) | True (0.62) | False (0.90) | False (0.79) | False (0.65) | False (0.57) | False (0.73) | False (0.76) | False (0.66) | False (0.97) | False (0.98) | HOME ブログ 健康 インフルエンザの時期？ですね  2018年2月15日 / 最終更新日 : 2018年5月31日 admin 健康 … |
| t00818 | False | False (0.78) | False (0.76) | False (0.63) | False (0.72) | False (0.98) | False (0.76) | False (0.85) | True (0.59) | False (0.65) | False (0.73) | True (0.57) | False (0.77) | False (0.69) | False (0.93) | False (0.66) | False (0.98) | False (0.98) | top love “女”にムカついているあなたへ『女子が書いた　女子のための　女子のトリセツ』  # “女”にムカついているあなたへ『女子… |
