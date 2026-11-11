# ja-toxicity

2026-11-11 · 210 labelled dev cases (True 105, False 105) · split: stratified k-fold (no test case among these: CV numbers only) · source: LLM-jp Toxicity Dataset（LLM-jp, CC BY 4.0）の 1,000 字以下から toxic / nontoxic 各 150 件

**decider@openrouter** has the highest accuracy (all), 99% [97, 100] (API cost $0.10 per 10k, p99 1038ms). Its interval overlaps with clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, jev:1.14, kev@openrouter, luna@decisions, mammoth@openrouter, reflex@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is drex-max@openrouter's, 99% [97, 100].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| clef-omni@openrouter | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.04 | 100% [99, 100] | 97.6% (95.0%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.04 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.03 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.02 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| d1@vercel | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.02 | 99% [98, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.07 | 100% [99, 100] | 97.1% (94.4%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 96.7% [94, 99] | 0.97 | 0.99 | 0.03 | 100% [99, 100] | 96.7% (93.8%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 98.6% [97, 100] | 0.99 | 0.99 | 0.03 | 100% [99, 100] | 99.0% (97.0%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.06 | 100% [98, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| gemini-decision@openrouter ✕ | 187 | 96.8% [94, 99] | 0.96 | 0.99 | 0.08 | 99% [98, 100] | 96.8% (93.7%) | 0/210 | 23/210 |
| jev:1.14 | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 91.9% [88, 96] | 0.91 | 0.97 | 0.11 | 85% [80, 90] | 94.4% (90.7%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 94.8% [92, 98] | 0.94 | 0.99 | 0.19 | 100% [99, 100] | 95.2% (92.0%) | 0/210 | 0/210 |
| luna@decisions | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.04 | 100% [100, 100] | 97.6% (95.1%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 98.6% [97, 100] | 0.99 | 1.00 | 0.05 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| reflex@openrouter | 210 | 96.7% [94, 99] | 0.97 | 0.99 | 0.01 | 99% [98, 100] | 97.1% (94.4%) | 0/210 | 0/210 |
| span@openrouter | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.05 | 100% [99, 100] | 97.1% (94.4%) | 0/210 | 0/210 |

Not compared: gemini-decision@openrouter (23 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is not ranked. Ask them again: `s1flow run ja-toxicity --models gemini-decision@openrouter`

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| clef-flash@openrouter = | 98% [96, 100] | 0.50 | met |
| clef-omni@openrouter = | 97% [94, 99] | 0.65 | met |
| clef@openrouter = | 98% [96, 100] | 0.55 | met |
| d1-ultra@openrouter = | 98% [96, 100] | 0.45 | met |
| d1.1@openrouter = | 98% [96, 100] | 0.55 | met |
| d1@vercel = | 98% [96, 100] | 0.80 | met |
| decider-flash@openrouter = | 98% [95, 100] | 0.35 | met |
| decider@openrouter = | 99% [97, 100] | 0.35 | met |
| decision-1@openrouter = | 97% [95, 99] | 0.65 | met |
| drex-max@openrouter = | 99% [97, 100] | 0.40 | met |
| elephant@openrouter = | 98% [96, 100] | 0.55 | met |
| jev:1.14 = | 98% [96, 100] | 0.65 | met |
| kev@openrouter = | 96% [93, 98] | 0.45 | met |
| luna@decisions = | 97% [95, 99] | 0.25 | met |
| mammoth@openrouter = | 99% [97, 100] | 0.65 | met |
| reflex@openrouter = | 98% [95, 100] | 0.35 | met |
| span@openrouter = | 98% [95, 100] | 0.20 | met |
| joey@openrouter | 92% [88, 95] | 0.40 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 350 ms | 522 ms | 2243 ms | 2381 ms | 6.4 | 0 | 4 | $0.13 | billed |  |
| clef-omni@openrouter | 210 | 296 ms | 452 ms | 895 ms | 965 ms | 3.0 | 0 | 4 | $0.95 | billed |  |
| clef@openrouter | 210 | 448 ms | 841 ms | 1757 ms | 2118 ms | 3.9 | 0 | 4 | $1.25 | billed |  |
| d1-ultra@openrouter | 210 | 259 ms | 378 ms | 448 ms | 577 ms | 1.7 | 0 | 4 | $0.21 | billed |  |
| d1.1@openrouter | 210 | 509 ms | 702 ms | 875 ms | 993 ms | 1.7 | 0 | 4 | $0.10 | billed |  |
| d1@vercel | 210 | 325 ms | 403 ms | 552 ms | 689 ms | 1.7 | 0 | 4 | $0.10 | billed | ○ |
| decider-flash@openrouter | 210 | 247 ms | 276 ms | 372 ms | 519 ms | 1.5 | 2 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 334 ms | 633 ms | 1038 ms | 1245 ms | 3.1 | 0 | 4 | $0.10 | billed | ○ |
| decision-1@openrouter | 210 | 354 ms | 425 ms | 579 ms | 649 ms | 1.6 | 0 | 4 | $0.20 | billed |  |
| drex-max@openrouter | 210 | 482 ms | 1181 ms | 1651 ms | 1898 ms | 3.4 | 0 | 4 | $0.31 | billed |  |
| elephant@openrouter | 210 | 279 ms | 301 ms | 357 ms | 410 ms | 1.3 | 0 | 4 | $0.19 | billed | ○ |
| gemini-decision@openrouter | 187 | 364 ms | 466 ms | 597 ms | 790 ms | 1.6 | 0 | 4 | $0.59 | billed |  |
| jev:1.14 | 210 | 190 ms | 222 ms | 253 ms | 257 ms | 1.3 | 0 | 4 | $0.40 | estimated | ○ |
| joey@openrouter | 210 | 278 ms | 319 ms | 427 ms | 654 ms | 1.5 | 0 | 4 | $0.05 | billed |  |
| kev@openrouter | 210 | 2088 ms | 5816 ms | 7096 ms | 7137 ms | 3.4 | 6 | 4 | $0.19 | billed |  |
| luna@decisions | 210 | 257 ms | 395 ms | 626 ms | 803 ms | 2.4 | 0 | 4 | $0.70 | estimated |  |
| mammoth@openrouter | 210 | 214 ms | 308 ms | 403 ms | 656 ms | 1.9 | 0 | 4 | $0.53 | billed | ○ |
| reflex@openrouter | 210 | 284 ms | 416 ms | 501 ms | 544 ms | 1.8 | 0 | 4 | $0.22 | billed |  |
| span@openrouter | 210 | 446 ms | 883 ms | 1054 ms | 1115 ms | 2.4 | 0 | 4 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0028 | 22 s (estimated, 210 calls) | 18 min | 4 |
| clef-omni@openrouter | $0.02 | 17 s (estimated, 210 calls) | 14 min | 4 |
| clef@openrouter | $0.03 | 28 s (estimated, 210 calls) | 22 min | 4 |
| d1-ultra@openrouter | $0.0045 | 15 s (estimated, 210 calls) | 12 min | 4 |
| d1.1@openrouter | $0.0021 | 27 s (estimated, 210 calls) | 21 min | 4 |
| d1@vercel | $0.0021 | 17 s (estimated, 210 calls) | 13 min | 4 |
| decider-flash@openrouter | $0.0011 | 12 s (estimated, 210 calls) | 9 min | 4 |
| decider@openrouter | $0.0022 | 19 s (estimated, 210 calls) | 15 min | 4 |
| decision-1@openrouter | $0.0042 | 18 s (estimated, 210 calls) | 14 min | 4 |
| drex-max@openrouter | $0.0066 | 32 s (estimated, 210 calls) | 25 min | 4 |
| elephant@openrouter | $0.0039 | 13 s (estimated, 210 calls) | 10 min | 4 |
| gemini-decision@openrouter | $0.01 | 17 s (estimated, 187 calls) | 15 min | 4 |
| jev:1.14 | $0.0083 | 9 s (estimated, 210 calls) | 7 min | 4 |
| joey@openrouter | $0.0011 | 14 s (estimated, 210 calls) | 11 min | 4 |
| kev@openrouter | $0.0039 | 2 min (estimated, 210 calls) | 1.9 h | 4 |
| luna@decisions | $0.01 | 14 s (estimated, 210 calls) | 11 min | 4 |
| mammoth@openrouter | $0.01 | 13 s (estimated, 210 calls) | 10 min | 4 |
| reflex@openrouter | $0.0047 | 17 s (estimated, 210 calls) | 13 min | 4 |
| span@openrouter | $0.0012 | 25 s (estimated, 210 calls) | 20 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 98.1% | 97.6% | 3 | 2 | 0.50 | 0.50 |
| clef-omni@openrouter | 97.6% | 97.1% | 3 | 3 | 0.65 | 0.65 |
| clef@openrouter | 98.1% | 98.1% | 1 | 3 | 0.55 | 0.55 |
| d1-ultra@openrouter | 98.1% | 98.1% | 2 | 2 | 0.45 | 0.45 |
| d1.1@openrouter | 98.1% | 98.1% | 1 | 3 | 0.55 | 0.55 |
| d1@vercel | 97.6% | 98.1% | 3 | 1 | 0.80 | 0.80 |
| decider-flash@openrouter | 98.1% | 97.6% | 3 | 2 | 0.35 | 0.35 |
| decider@openrouter | 97.1% | 98.6% | 3 | 0 | 0.35 | 0.35 |
| decision-1@openrouter | 96.7% | 97.1% | 3 | 3 | 0.65 | 0.65 |
| drex-max@openrouter | 98.6% | 98.6% | 3 | 0 | 0.40 | 0.40 |
| elephant@openrouter | 98.1% | 98.1% | 2 | 2 | 0.55 | 0.55 |
| gemini-decision@openrouter | 96.8% | 95.7% | 5 | 3 | 0.30 | 0.45 |
| jev:1.14 | 97.6% | 98.1% | 3 | 1 | 0.65 | 0.65 |
| joey@openrouter | 91.9% | 91.9% | 11 | 6 | 0.35 | 0.40 |
| kev@openrouter | 94.8% | 95.7% | 7 | 2 | 0.45 | 0.45 |
| luna@decisions | 97.6% | 97.1% | 3 | 3 | 0.25 | 0.25 |
| mammoth@openrouter | 98.6% | 98.6% | 2 | 1 | 0.65 | 0.65 |
| reflex@openrouter | 96.7% | 97.6% | 3 | 2 | 0.35 | 0.35 |
| span@openrouter | 97.1% | 97.6% | 3 | 2 | 0.20 | 0.20 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 28 (27%) |
| 0.20 | 1 (1%) | 5 (5%) |
| 0.30 | 1 (1%) | 3 (3%) |
| 0.40 | 3 (3%) | 1 (1%) |
| 0.50 | 3 (3%) | 1 (1%) |
| 0.60 | 3 (3%) | 1 (1%) |
| 0.70 | 4 (4%) | 1 (1%) |
| 0.80 | 9 (9%) | 0 (0%) |
| 0.90 | 24 (23%) | 0 (0%) |

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
| 0.10 | 1 (1%) | 17 (16%) |
| 0.20 | 1 (1%) | 14 (13%) |
| 0.30 | 1 (1%) | 9 (9%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 1 (1%) | 3 (3%) |
| 0.55 | 1 (1%) | 2 (2%) |
| 0.60 | 1 (1%) | 2 (2%) |
| 0.70 | 2 (2%) | 2 (2%) |
| 0.80 | 3 (3%) | 2 (2%) |
| 0.90 | 4 (4%) | 1 (1%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 15 (14%) |
| 0.20 | 1 (1%) | 9 (9%) |
| 0.30 | 1 (1%) | 4 (4%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.45 | 1 (1%) | 2 (2%) |
| 0.50 | 2 (2%) | 2 (2%) |
| 0.60 | 3 (3%) | 2 (2%) |
| 0.70 | 3 (3%) | 2 (2%) |
| 0.80 | 4 (4%) | 1 (1%) |
| 0.90 | 14 (13%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 17 (16%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 4 (4%) |
| 0.40 | 1 (1%) | 4 (4%) |
| 0.50 | 1 (1%) | 3 (3%) |
| 0.55 | 1 (1%) | 2 (2%) |
| 0.60 | 1 (1%) | 2 (2%) |
| 0.70 | 2 (2%) | 2 (2%) |
| 0.80 | 3 (3%) | 1 (1%) |
| 0.90 | 6 (6%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 7 (7%) |
| 0.20 | 1 (1%) | 5 (5%) |
| 0.30 | 2 (2%) | 3 (3%) |
| 0.40 | 2 (2%) | 2 (2%) |
| 0.50 | 3 (3%) | 2 (2%) |
| 0.60 | 3 (3%) | 1 (1%) |
| 0.70 | 3 (3%) | 1 (1%) |
| 0.80 | 3 (3%) | 0 (0%) |
| 0.90 | 7 (7%) | 0 (0%) |

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
| 0.30 | 3 (3%) | 0 (0%) |
| 0.35 | 3 (3%) | 0 (0%) |
| 0.40 | 5 (5%) | 0 (0%) |
| 0.50 | 6 (6%) | 0 (0%) |
| 0.60 | 9 (9%) | 0 (0%) |
| 0.70 | 19 (18%) | 0 (0%) |
| 0.80 | 37 (35%) | 0 (0%) |
| 0.90 | 61 (58%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 15 (14%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 7 (7%) |
| 0.40 | 1 (1%) | 6 (6%) |
| 0.50 | 1 (1%) | 6 (6%) |
| 0.60 | 2 (2%) | 5 (5%) |
| 0.65 | 2 (2%) | 3 (3%) |
| 0.70 | 3 (3%) | 2 (2%) |
| 0.80 | 10 (10%) | 0 (0%) |
| 0.90 | 21 (20%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 8 (8%) |
| 0.20 | 1 (1%) | 3 (3%) |
| 0.30 | 2 (2%) | 1 (1%) |
| 0.40 | 2 (2%) | 0 (0%) |
| 0.50 | 3 (3%) | 0 (0%) |
| 0.60 | 3 (3%) | 0 (0%) |
| 0.70 | 4 (4%) | 0 (0%) |
| 0.80 | 6 (6%) | 0 (0%) |
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

## Misses and false alarms by threshold (gemini-decision@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 3 (3%) |
| 0.20 | 3 (4%) | 2 (2%) |
| 0.30 | 4 (5%) | 1 (1%) |
| 0.40 | 5 (6%) | 0 (0%) |
| 0.45 | 5 (6%) | 0 (0%) |
| 0.50 | 6 (7%) | 0 (0%) |
| 0.60 | 13 (16%) | 0 (0%) |
| 0.70 | 23 (28%) | 0 (0%) |
| 0.80 | 36 (44%) | 0 (0%) |
| 0.90 | 65 (79%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 20 (19%) |
| 0.20 | 1 (1%) | 12 (11%) |
| 0.30 | 1 (1%) | 8 (8%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 1 (1%) | 4 (4%) |
| 0.60 | 2 (2%) | 3 (3%) |
| 0.65 | 2 (2%) | 1 (1%) |
| 0.70 | 3 (3%) | 0 (0%) |
| 0.80 | 13 (12%) | 0 (0%) |
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
| 0.10 | 1 (1%) | 66 (63%) |
| 0.20 | 1 (1%) | 22 (21%) |
| 0.30 | 3 (3%) | 8 (8%) |
| 0.40 | 5 (5%) | 3 (3%) |
| 0.45 | 7 (7%) | 0 (0%) |
| 0.50 | 11 (10%) | 0 (0%) |
| 0.60 | 33 (31%) | 0 (0%) |
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
| 0.35 | 3 (3%) | 1 (1%) |
| 0.40 | 5 (5%) | 1 (1%) |
| 0.50 | 6 (6%) | 1 (1%) |
| 0.60 | 7 (7%) | 0 (0%) |
| 0.70 | 8 (8%) | 0 (0%) |
| 0.80 | 9 (9%) | 0 (0%) |
| 0.90 | 16 (15%) | 0 (0%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 4 (4%) |
| 0.20 | 1 (1%) | 2 (2%) |
| 0.30 | 5 (5%) | 1 (1%) |
| 0.40 | 5 (5%) | 0 (0%) |
| 0.50 | 6 (6%) | 0 (0%) |
| 0.60 | 12 (11%) | 0 (0%) |
| 0.70 | 21 (20%) | 0 (0%) |
| 0.80 | 33 (31%) | 0 (0%) |
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

**clef@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.97 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |
| t00740 | False | True | 0.90 | この作品 「【C85】ガッチャマンクラウズ18禁本サンプル」 は 「兄弟(意味深)」「ガッチャマン500users入り」 等のタグがつけら… |

**d1-ultra@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**d1.1@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

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

**gemini-decision@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.98 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |
| t01859 | True | False | 0.91 | 天使のゆびさき岡山店 亜希子(あきこ)  極上のマッサージ技術とエロさを兼ね備えた巨乳セラピスト！  とってもフレンドリーでノリが良く愛嬌… |

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

**reflex@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

**span@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 1.00 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |


## Cases the models disagree on (12 of 35)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t01740 | True | True (0.92) | True (0.95) | True (0.96) | True (0.96) | True (0.95) | True (0.92) | True (0.91) | True (0.80) | True (0.96) | True (0.98) | True (0.92) | True (0.77) | True (0.93) | False (0.64) | True (0.51) | True (1.00) | True (0.88) | True (0.99) | True (0.85) | ## 【柏木さりな】発育が止まらないエチエチJKのフレッシュ腋  ◆女性歌手・女性芸能人  弱冠17歳にして、最近は大人の色気がどんどん強… |
| t00271 | False | False (0.84) | True (0.55) | False (0.96) | False (0.99) | False (0.99) | False (1.00) | False (0.97) | False (0.99) | False (0.99) | False (1.00) | False (0.96) | False (0.98) | False (0.95) | False (0.83) | False (0.89) | False (0.99) | False (0.87) | False (1.00) | False (1.00) | 女性への贈り物 > スキャルプローション  # スキャルプローション  # 若い男性.女性,高校生.薄毛.育毛,頭皮,抜け毛,予防,ローシ… |
| t01783 | True | True (0.95) | True (0.98) | True (0.98) | True (0.98) | True (0.98) | True (0.98) | True (0.92) | True (0.92) | True (0.99) | True (0.99) | True (0.93) | True (0.77) | True (0.93) | False (0.88) | True (0.72) | True (0.95) | True (0.98) | True (1.00) | True (0.97) | 写メ日記 ほたるの写メ日記  ### ほたるの写メ日記  #### おち○ちんおっきくなってるよ？2023/02/03 21:01  あれ… |
| t00277 | False | False (0.91) | False (0.85) | False (0.71) | False (0.92) | False (0.83) | False (0.93) | False (0.92) | False (0.93) | False (0.84) | False (0.97) | False (0.87) | False (0.96) | False (0.81) | True (0.78) | False (0.84) | False (0.97) | False (0.82) | False (1.00) | False (1.00) | ◆ e-Bookのタイトル 『【PRIDE】たった1つのブログで月に4記事書くだけで月8万稼いでいるブログアフィリエイト（アドセンス+楽天… |
| t00085 | False | False (0.90) | False (0.90) | False (0.85) | False (0.91) | False (0.97) | False (1.00) | False (0.96) | False (0.99) | True (0.68) | False (0.98) | False (0.86) | False (0.97) | False (0.74) | False (0.82) | False (0.84) | False (0.95) | False (0.77) | False (1.00) | False (0.99) | トップページ ＞ 車におけるバッテリーの上がりについて ＞ 160326  車におけるバッテリーの上がりについてブログ：160326 夏は… |
| t01562 | True | True (0.93) | True (0.97) | True (0.98) | True (0.95) | True (0.97) | True (0.99) | True (0.90) | True (0.77) | True (0.88) | True (0.94) | True (0.89) | True (0.82) | True (0.89) | False (0.86) | True (0.73) | True (0.94) | True (0.94) | True (0.87) | True (0.84) | # 【アウトレット】激震パイ揺れ！暴走腰振り騎乗位 厳選ベスト5時間 オマ○コ感度無限大オーガズムお見せします!! (AV) [7LZBS… |
| t00577 | False | False (0.90) | False (0.60) | True (0.53) | False (0.78) | False (0.86) | False (0.99) | False (0.80) | False (0.86) | False (0.89) | False (0.82) | False (0.73) | False (0.79) | True (0.64) | False (0.75) | False (0.79) | False (0.95) | False (0.66) | False (0.97) | False (0.87) | # 神谷明の給料は1本10万円  声優の神谷明（かみやあきら＝53歳）が関西テレビ系番組「マルコポロリ」に出演して、給料を暴露しました。 … |
| t01004 | False | False (0.61) | True (0.61) | False (0.55) | False (0.85) | False (0.74) | False (0.75) | False (0.89) | False (0.93) | False (0.88) | False (0.94) | False (0.79) | False (0.95) | False (0.71) | False (0.80) | False (0.73) | False (0.86) | False (0.74) | False (0.99) | False (0.99) | N9231BP  # 異世界混浴物語  連載中全124部 1話目を読む \|最新話を読む  あらすじ 『異世界混浴物語』1～4巻、オーバー… |
| t01599 | True | True (0.88) | True (0.97) | True (0.98) | True (0.96) | True (0.98) | True (0.99) | True (0.84) | True (0.84) | True (0.84) | True (0.97) | True (0.92) | True (0.78) | True (0.92) | False (0.77) | True (0.78) | True (0.95) | True (0.94) | True (0.96) | True (0.88) | # オマエ、いい歳してまだ童貞なのかよー!! wwウチらがヌキまくってヤリチンに育ててやんよw 同窓会で10年ぶりに再会した元ギャル同級生… |
| t01519 | True | True (0.92) | True (0.97) | True (0.97) | True (0.97) | True (0.98) | True (0.99) | True (0.95) | True (0.83) | True (0.96) | True (0.97) | True (0.88) | True (0.58) | True (0.85) | False (0.54) | True (0.64) | True (0.85) | True (0.94) | True (0.82) | True (0.71) | # 素人娘尻アナル大全　※サンプル動画あり  トップページ ＞ アナル・菊門・尻穴 作品 一覧 ＞ 素人娘尻アナル大全　※サンプル動画あり… |
| t00106 | False | False (0.89) | False (0.89) | False (0.84) | False (0.89) | False (0.89) | False (0.96) | False (0.88) | False (0.91) | True (0.62) | False (0.85) | False (0.79) | False (0.91) | False (0.69) | False (0.57) | False (0.73) | False (0.76) | False (0.65) | False (0.98) | False (0.98) | HOME ブログ 健康 インフルエンザの時期？ですね  2018年2月15日 / 最終更新日 : 2018年5月31日 admin 健康 … |
| t01215 | True | True (0.88) | True (0.95) | True (0.97) | True (0.95) | True (0.95) | True (0.98) | True (0.78) | True (0.85) | True (0.84) | True (0.96) | True (0.75) | True (0.57) | True (0.79) | True (0.73) | False (0.72) | True (0.58) | True (0.91) | True (0.98) | True (0.68) | 06月11日 20名出勤  ### まこさんボディデータ  ◆ボディーデータ◆ ・性感帯は？：『背中♪』 ・濡れやすい体質ですか？：『濡れ… |
