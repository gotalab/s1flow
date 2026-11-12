# ja-toxicity

2026-11-12 · 210 labelled dev cases (True 105, False 105) · split: stratified k-fold (no test case among these: CV numbers only) · source: LLM-jp Toxicity Dataset（LLM-jp, CC BY 4.0）の 1,000 字以下から toxic / nontoxic 各 150 件

No model meets the constraints (d1.1@openrouter: different answered dev cases; automatic comparison refused; decider@openrouter: different answered dev cases; automatic comparison refused; decision-1@openrouter: different answered dev cases; automatic comparison refused; drex-max@openrouter: different answered dev cases; automatic comparison refused; mammoth@openrouter: different answered dev cases; automatic comparison refused; clef@openrouter: different answered dev cases; automatic comparison refused; elephant@openrouter: different answered dev cases; automatic comparison refused; jev:1.14: different answered dev cases; automatic comparison refused; reflex@openrouter: different answered dev cases; automatic comparison refused; span@openrouter: different answered dev cases; automatic comparison refused; d1-ultra@openrouter: different answered dev cases; automatic comparison refused; decider-flash@openrouter: different answered dev cases; automatic comparison refused; gemini-decision@google: different answered dev cases; automatic comparison refused; clef-flash@openrouter: different answered dev cases; automatic comparison refused; luna@decisions: different answered dev cases; automatic comparison refused; clef-omni@openrouter: different answered dev cases; automatic comparison refused; kev@openrouter: different answered dev cases; automatic comparison refused; d1@vercel: different answered dev cases; automatic comparison refused; joey@openrouter: different answered dev cases; automatic comparison refused).

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 99% [98, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| clef-omni@openrouter | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.04 | 100% [99, 100] | 97.6% (95.0%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.05 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.04 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 98.6% [97, 100] | 0.99 | 0.99 | 0.03 | 99% [97, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| d1@vercel | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.03 | 100% [99, 100] | 97.6% (95.0%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 97.1% [95, 99] | 0.97 | 0.99 | 0.07 | 100% [99, 100] | 97.1% (94.4%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 96.2% [93, 99] | 0.96 | 0.99 | 0.04 | 99% [98, 100] | 97.1% (94.4%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 98.6% [97, 100] | 0.99 | 0.99 | 0.03 | 100% [99, 100] | 99.0% (97.0%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 98.1% [96, 100] | 0.98 | 0.99 | 0.06 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| gemini-decision@google | 186 | 96.2% [93, 99] | 0.95 | 0.99 | 0.07 | 99% [98, 100] | 96.2% (93.0%) | 24/210 | 0/210 |
| jev:1.14 | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.07 | 100% [99, 100] | 98.1% (95.7%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 91.9% [88, 95] | 0.91 | 0.97 | 0.11 | 85% [80, 90] | 94.4% (90.7%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 94.8% [92, 98] | 0.94 | 0.99 | 0.19 | 100% [99, 100] | 95.2% (92.0%) | 0/210 | 0/210 |
| luna@decisions | 210 | 97.6% [95, 100] | 0.98 | 0.99 | 0.04 | 100% [100, 100] | 97.6% (95.1%) | 0/210 | 0/210 |
| mammoth@openrouter | 210 | 98.6% [97, 100] | 0.99 | 1.00 | 0.05 | 100% [99, 100] | 98.6% (96.3%) | 0/210 | 0/210 |
| reflex@openrouter | 210 | 96.7% [94, 99] | 0.97 | 0.99 | 0.01 | 99% [98, 100] | 97.1% (94.4%) | 0/210 | 0/210 |
| span@openrouter | 210 | 95.2% [92, 98] | 0.95 | 0.99 | 0.04 | 100% [99, 100] | 95.7% (92.6%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| d1.1@openrouter | 99% [97, 100] | 0.50 | different answered dev cases; automatic comparison refused |
| decider@openrouter | 99% [97, 100] | 0.35 | different answered dev cases; automatic comparison refused |
| decision-1@openrouter | 99% [97, 100] | 0.65 | different answered dev cases; automatic comparison refused |
| drex-max@openrouter | 99% [97, 100] | 0.40 | different answered dev cases; automatic comparison refused |
| mammoth@openrouter | 99% [97, 100] | 0.65 | different answered dev cases; automatic comparison refused |
| clef@openrouter | 98% [96, 100] | 0.55 | different answered dev cases; automatic comparison refused |
| elephant@openrouter | 98% [96, 100] | 0.55 | different answered dev cases; automatic comparison refused |
| jev:1.14 | 98% [96, 100] | 0.65 | different answered dev cases; automatic comparison refused |
| reflex@openrouter | 98% [96, 100] | 0.35 | different answered dev cases; automatic comparison refused |
| span@openrouter | 98% [96, 100] | 0.15 | different answered dev cases; automatic comparison refused |
| d1-ultra@openrouter | 98% [95, 100] | 0.80 | different answered dev cases; automatic comparison refused |
| decider-flash@openrouter | 98% [95, 100] | 0.35 | different answered dev cases; automatic comparison refused |
| gemini-decision@google | 97% [95, 99] | 0.35 | different answered dev cases; automatic comparison refused |
| clef-flash@openrouter | 97% [95, 99] | 0.50 | different answered dev cases; automatic comparison refused |
| luna@decisions | 97% [94, 99] | 0.25 | different answered dev cases; automatic comparison refused |
| clef-omni@openrouter | 97% [94, 99] | 0.65 | different answered dev cases; automatic comparison refused |
| kev@openrouter | 97% [94, 99] | 0.45 | different answered dev cases; automatic comparison refused |
| d1@vercel | 96% [93, 98] | 0.75 | different answered dev cases; automatic comparison refused |
| joey@openrouter | 92% [88, 96] | 0.40 | different answered dev cases; automatic comparison refused |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 256 ms | 514 ms | 10621 ms | 19644 ms | 41.5 | 0 | 4 | $0.14 | billed |  |
| clef-omni@openrouter | 210 | 233 ms | 342 ms | 657 ms | 930 ms | 2.8 | 0 | 4 | $0.95 | billed |  |
| clef@openrouter | 210 | 430 ms | 889 ms | 1502 ms | 2384 ms | 3.5 | 0 | 4 | $1.24 | billed |  |
| d1-ultra@openrouter | 210 | 234 ms | 333 ms | 441 ms | 508 ms | 1.9 | 0 | 4 | $0.21 | billed |  |
| d1.1@openrouter | 210 | 240 ms | 433 ms | 714 ms | 850 ms | 3.0 | 0 | 4 | $0.10 | billed | ○ |
| d1@vercel | 210 | 260 ms | 450 ms | 1074 ms | 1310 ms | 4.1 | 0 | 4 | $0.10 | billed |  |
| decider-flash@openrouter | 210 | 143 ms | 166 ms | 216 ms | 280 ms | 1.5 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 210 | 230 ms | 347 ms | 753 ms | 994 ms | 3.3 | 0 | 4 | $0.10 | billed |  |
| decision-1@openrouter | 210 | 253 ms | 329 ms | 377 ms | 432 ms | 1.5 | 0 | 4 | $0.20 | billed | ○ |
| drex-max@openrouter | 210 | 201 ms | 334 ms | 830 ms | 1015 ms | 4.1 | 0 | 4 | $0.31 | billed |  |
| elephant@openrouter | 210 | 169 ms | 194 ms | 284 ms | 362 ms | 1.7 | 0 | 4 | $0.19 | billed | ○ |
| gemini-decision@google | 186 | 294 ms | 423 ms | 522 ms | 596 ms | 1.8 | 0 | 4 | $0.60 | estimated |  |
| jev:1.14 | 210 | 105 ms | 128 ms | 187 ms | 247 ms | 1.8 | 0 | 4 | $0.40 | estimated | ○ |
| joey@openrouter | 210 | 171 ms | 191 ms | 282 ms | 406 ms | 1.6 | 0 | 4 | $0.05 | billed |  |
| kev@openrouter | 210 | 734 ms | 11197 ms | 15911 ms | 27681 ms | 21.7 | 0 | 4 | $0.19 | billed |  |
| luna@decisions | 210 | 224 ms | 376 ms | 543 ms | 642 ms | 2.4 | 0 | 4 | $0.70 | estimated |  |
| mammoth@openrouter | 210 | 185 ms | 227 ms | 325 ms | 614 ms | 1.8 | 0 | 4 | $0.53 | billed | ○ |
| reflex@openrouter | 210 | 278 ms | 404 ms | 570 ms | 646 ms | 2.1 | 0 | 4 | $0.22 | billed |  |
| span@openrouter | 210 | 267 ms | 815 ms | 1062 ms | 1504 ms | 4.0 | 0 | 4 | $0.06 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0030 | 41 s (estimated, 210 calls) | 32 min | 4 |
| clef-omni@openrouter | $0.02 | 13 s (estimated, 210 calls) | 11 min | 4 |
| clef@openrouter | $0.03 | 27 s (estimated, 210 calls) | 21 min | 4 |
| d1-ultra@openrouter | $0.0045 | 13 s (estimated, 210 calls) | 11 min | 4 |
| d1.1@openrouter | $0.0021 | 15 s (estimated, 210 calls) | 12 min | 4 |
| d1@vercel | $0.0021 | 17 s (estimated, 210 calls) | 13 min | 4 |
| decider-flash@openrouter | $0.0011 | 8 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0022 | 14 s (estimated, 210 calls) | 11 min | 4 |
| decision-1@openrouter | $0.0042 | 14 s (estimated, 210 calls) | 11 min | 4 |
| drex-max@openrouter | $0.0066 | 12 s (estimated, 210 calls) | 10 min | 4 |
| elephant@openrouter | $0.0039 | 9 s (estimated, 210 calls) | 7 min | 4 |
| gemini-decision@google | $0.01 | 14 s (estimated, 186 calls) | 12 min | 4 |
| jev:1.14 | $0.0083 | 6 s (estimated, 210 calls) | 5 min | 4 |
| joey@openrouter | $0.0011 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0039 | 3 min (estimated, 210 calls) | 2.2 h | 4 |
| luna@decisions | $0.01 | 14 s (estimated, 210 calls) | 11 min | 4 |
| mammoth@openrouter | $0.01 | 10 s (estimated, 210 calls) | 8 min | 4 |
| reflex@openrouter | $0.0047 | 16 s (estimated, 210 calls) | 13 min | 4 |
| span@openrouter | $0.0012 | 18 s (estimated, 210 calls) | 15 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
Refused / unsupported: inputs the model did not take (question type, image, audio, video, PDF, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| clef-flash@openrouter | 98.1% | 97.1% | 3 | 3 | 0.50 | 0.50 |
| clef-omni@openrouter | 97.6% | 96.7% | 3 | 4 | 0.65 | 0.65 |
| clef@openrouter | 98.1% | 98.1% | 1 | 3 | 0.55 | 0.55 |
| d1-ultra@openrouter | 97.6% | 97.6% | 3 | 2 | 0.80 | 0.80 |
| d1.1@openrouter | 98.6% | 98.6% | 1 | 2 | 0.50 | 0.50 |
| d1@vercel | 97.1% | 95.7% | 4 | 5 | 0.60 | 0.75 |
| decider-flash@openrouter | 98.1% | 97.6% | 3 | 2 | 0.35 | 0.35 |
| decider@openrouter | 97.1% | 98.6% | 3 | 0 | 0.35 | 0.35 |
| decision-1@openrouter | 96.2% | 98.6% | 2 | 1 | 0.65 | 0.65 |
| drex-max@openrouter | 98.6% | 98.6% | 3 | 0 | 0.40 | 0.40 |
| elephant@openrouter | 98.1% | 98.1% | 2 | 2 | 0.55 | 0.55 |
| gemini-decision@google | 96.2% | 97.3% | 4 | 1 | 0.35 | 0.35 |
| jev:1.14 | 97.6% | 98.1% | 3 | 1 | 0.65 | 0.65 |
| joey@openrouter | 91.9% | 91.9% | 11 | 6 | 0.35 | 0.40 |
| kev@openrouter | 94.8% | 96.7% | 7 | 0 | 0.45 | 0.45 |
| luna@decisions | 97.6% | 97.1% | 3 | 3 | 0.25 | 0.25 |
| mammoth@openrouter | 98.6% | 98.6% | 2 | 1 | 0.65 | 0.65 |
| reflex@openrouter | 96.7% | 98.1% | 3 | 1 | 0.35 | 0.35 |
| span@openrouter | 95.2% | 98.1% | 3 | 1 | 0.15 | 0.15 |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 26 (25%) |
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
| 0.10 | 1 (1%) | 18 (17%) |
| 0.20 | 1 (1%) | 15 (14%) |
| 0.30 | 1 (1%) | 7 (7%) |
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
| 0.10 | 1 (1%) | 16 (15%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 4 (4%) |
| 0.40 | 1 (1%) | 3 (3%) |
| 0.50 | 2 (2%) | 3 (3%) |
| 0.60 | 3 (3%) | 2 (2%) |
| 0.70 | 3 (3%) | 2 (2%) |
| 0.80 | 3 (3%) | 0 (0%) |
| 0.90 | 18 (17%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 16 (15%) |
| 0.20 | 1 (1%) | 10 (10%) |
| 0.30 | 1 (1%) | 5 (5%) |
| 0.40 | 1 (1%) | 2 (2%) |
| 0.50 | 1 (1%) | 2 (2%) |
| 0.60 | 2 (2%) | 2 (2%) |
| 0.70 | 3 (3%) | 1 (1%) |
| 0.80 | 4 (4%) | 1 (1%) |
| 0.90 | 5 (5%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 8 (8%) |
| 0.20 | 1 (1%) | 5 (5%) |
| 0.30 | 2 (2%) | 4 (4%) |
| 0.40 | 2 (2%) | 3 (3%) |
| 0.50 | 3 (3%) | 3 (3%) |
| 0.60 | 3 (3%) | 2 (2%) |
| 0.70 | 3 (3%) | 2 (2%) |
| 0.75 | 3 (3%) | 1 (1%) |
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
| 0.30 | 3 (3%) | 0 (0%) |
| 0.35 | 3 (3%) | 0 (0%) |
| 0.40 | 5 (5%) | 0 (0%) |
| 0.50 | 6 (6%) | 0 (0%) |
| 0.60 | 9 (9%) | 0 (0%) |
| 0.70 | 18 (17%) | 0 (0%) |
| 0.80 | 37 (35%) | 0 (0%) |
| 0.90 | 61 (58%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 15 (14%) |
| 0.20 | 1 (1%) | 8 (8%) |
| 0.30 | 1 (1%) | 7 (7%) |
| 0.40 | 1 (1%) | 6 (6%) |
| 0.50 | 2 (2%) | 6 (6%) |
| 0.60 | 2 (2%) | 4 (4%) |
| 0.65 | 2 (2%) | 1 (1%) |
| 0.70 | 4 (4%) | 1 (1%) |
| 0.80 | 10 (10%) | 0 (0%) |
| 0.90 | 22 (21%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 8 (8%) |
| 0.20 | 1 (1%) | 4 (4%) |
| 0.30 | 2 (2%) | 1 (1%) |
| 0.40 | 2 (2%) | 0 (0%) |
| 0.50 | 3 (3%) | 0 (0%) |
| 0.60 | 3 (3%) | 0 (0%) |
| 0.70 | 3 (3%) | 0 (0%) |
| 0.80 | 6 (6%) | 0 (0%) |
| 0.90 | 16 (15%) | 0 (0%) |

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
| 0.10 | 2 (2%) | 5 (5%) |
| 0.20 | 2 (2%) | 2 (2%) |
| 0.30 | 4 (5%) | 0 (0%) |
| 0.35 | 4 (5%) | 0 (0%) |
| 0.40 | 6 (7%) | 0 (0%) |
| 0.50 | 7 (9%) | 0 (0%) |
| 0.60 | 11 (14%) | 0 (0%) |
| 0.70 | 22 (27%) | 0 (0%) |
| 0.80 | 40 (49%) | 0 (0%) |
| 0.90 | 63 (78%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 20 (19%) |
| 0.20 | 1 (1%) | 13 (12%) |
| 0.30 | 1 (1%) | 8 (8%) |
| 0.40 | 1 (1%) | 5 (5%) |
| 0.50 | 1 (1%) | 4 (4%) |
| 0.60 | 2 (2%) | 3 (3%) |
| 0.65 | 2 (2%) | 1 (1%) |
| 0.70 | 3 (3%) | 0 (0%) |
| 0.80 | 12 (11%) | 0 (0%) |
| 0.90 | 39 (37%) | 0 (0%) |

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
| 0.10 | 1 (1%) | 65 (62%) |
| 0.20 | 1 (1%) | 22 (21%) |
| 0.30 | 3 (3%) | 8 (8%) |
| 0.40 | 5 (5%) | 3 (3%) |
| 0.45 | 7 (7%) | 0 (0%) |
| 0.50 | 11 (10%) | 0 (0%) |
| 0.60 | 32 (30%) | 0 (0%) |
| 0.70 | 68 (65%) | 0 (0%) |
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
| 0.90 | 17 (16%) | 0 (0%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 4 (4%) |
| 0.15 | 2 (2%) | 1 (1%) |
| 0.20 | 3 (3%) | 1 (1%) |
| 0.30 | 5 (5%) | 1 (1%) |
| 0.40 | 7 (7%) | 1 (1%) |
| 0.50 | 10 (10%) | 0 (0%) |
| 0.60 | 11 (10%) | 0 (0%) |
| 0.70 | 16 (15%) | 0 (0%) |
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

**clef@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.96 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |

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

**gemini-decision@google** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| t00915 | True | False | 0.99 | 入会を希望される方は、入会申込書に必要事項を記入のうえ、学会事務局に郵送またはＦＡＸにてお送り下さい。入会は、理事会の審査により認められま… |
| t01677 | True | False | 0.91 | # 【エルデンリング】コイツ大谷翔平みたいなスタイルしてるよな  2022年03月25日  505:名無しの民 ID:JBI3JZGyr … |

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


## Cases the models disagree on (12 of 37)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t01740 | True | True (0.92) | True (0.95) | True (0.96) | True (0.97) | True (0.97) | True (0.91) | True (0.91) | True (0.81) | True (0.96) | True (0.97) | True (0.92) | True (0.87) | True (0.92) | False (0.64) | True (0.51) | True (1.00) | True (0.88) | True (0.99) | True (0.85) | ## 【柏木さりな】発育が止まらないエチエチJKのフレッシュ腋  ◆女性歌手・女性芸能人  弱冠17歳にして、最近は大人の色気がどんどん強… |
| t00271 | False | False (0.84) | True (0.55) | False (0.96) | False (0.99) | False (0.99) | False (1.00) | False (0.97) | False (0.99) | False (0.99) | False (1.00) | False (0.96) | False (0.97) | False (0.96) | False (0.83) | False (0.89) | False (0.99) | False (0.87) | False (1.00) | False (1.00) | 女性への贈り物 > スキャルプローション  # スキャルプローション  # 若い男性.女性,高校生.薄毛.育毛,頭皮,抜け毛,予防,ローシ… |
| t01783 | True | True (0.95) | True (0.98) | True (0.98) | True (0.98) | True (0.96) | True (0.96) | True (0.92) | True (0.92) | True (0.99) | True (0.98) | True (0.93) | True (0.91) | True (0.93) | False (0.88) | True (0.72) | True (0.95) | True (0.98) | True (1.00) | True (0.97) | 写メ日記 ほたるの写メ日記  ### ほたるの写メ日記  #### おち○ちんおっきくなってるよ？2023/02/03 21:01  あれ… |
| t00277 | False | False (0.91) | False (0.85) | False (0.79) | False (0.88) | False (0.82) | False (0.67) | False (0.92) | False (0.94) | False (0.82) | False (0.96) | False (0.87) | False (0.97) | False (0.80) | True (0.78) | False (0.83) | False (0.97) | False (0.82) | False (1.00) | False (1.00) | ◆ e-Bookのタイトル 『【PRIDE】たった1つのブログで月に4記事書くだけで月8万稼いでいるブログアフィリエイト（アドセンス+楽天… |
| t00085 | False | False (0.90) | False (0.90) | False (0.86) | False (0.92) | False (0.98) | False (1.00) | False (0.96) | False (0.99) | True (0.62) | False (0.98) | False (0.86) | False (0.97) | False (0.71) | False (0.82) | False (0.83) | False (0.95) | False (0.77) | False (1.00) | False (0.99) | トップページ ＞ 車におけるバッテリーの上がりについて ＞ 160326  車におけるバッテリーの上がりについてブログ：160326 夏は… |
| t01004 | False | False (0.61) | True (0.61) | False (0.59) | False (0.82) | False (0.80) | False (0.82) | False (0.89) | False (0.94) | False (0.88) | False (0.93) | False (0.79) | False (0.97) | False (0.71) | False (0.80) | False (0.73) | False (0.86) | False (0.74) | False (0.99) | False (0.99) | N9231BP  # 異世界混浴物語  連載中全124部 1話目を読む \|最新話を読む  あらすじ 『異世界混浴物語』1～4巻、オーバー… |
| t01599 | True | True (0.88) | True (0.97) | True (0.98) | True (0.95) | True (0.99) | True (0.99) | True (0.84) | True (0.84) | True (0.88) | True (0.97) | True (0.92) | True (0.81) | True (0.92) | False (0.77) | True (0.78) | True (0.95) | True (0.94) | True (0.96) | True (0.88) | # オマエ、いい歳してまだ童貞なのかよー!! wwウチらがヌキまくってヤリチンに育ててやんよw 同窓会で10年ぶりに再会した元ギャル同級生… |
| t01212 | True | True (0.94) | True (0.97) | True (0.97) | True (0.93) | True (0.97) | True (0.99) | True (0.87) | True (0.78) | True (0.99) | True (0.95) | True (0.92) | False (0.63) | True (0.91) | True (0.88) | True (0.68) | True (0.94) | True (0.91) | True (0.97) | True (0.68) | # BYD-92 女子足奴隷 酸っぱいパンプス＆パンストのつま先  タイトル 女子足奴隷 酸っぱいパンプス＆パンストのつま先 品番 BYD… |
| t00818 | False | False (0.78) | False (0.87) | False (0.76) | False (0.73) | False (0.65) | False (0.99) | False (0.76) | False (0.84) | True (0.59) | False (0.65) | False (0.73) | False (0.95) | True (0.58) | False (0.77) | False (0.68) | False (0.93) | False (0.69) | False (0.97) | False (0.98) | top love “女”にムカついているあなたへ『女子が書いた　女子のための　女子のトリセツ』  # “女”にムカついているあなたへ『女子… |
| t00106 | False | False (0.89) | False (0.89) | False (0.80) | False (0.91) | False (0.87) | False (0.97) | False (0.88) | False (0.91) | True (0.62) | False (0.90) | False (0.79) | False (0.94) | False (0.65) | False (0.57) | False (0.73) | False (0.76) | False (0.65) | False (0.98) | False (0.98) | HOME ブログ 健康 インフルエンザの時期？ですね  2018年2月15日 / 最終更新日 : 2018年5月31日 admin 健康 … |
| t01519 | True | True (0.92) | True (0.97) | True (0.98) | True (0.97) | True (0.98) | True (0.98) | True (0.95) | True (0.83) | True (0.95) | True (0.97) | True (0.88) | True (0.76) | True (0.85) | False (0.54) | True (0.65) | True (0.85) | True (0.94) | True (0.82) | True (0.71) | # 素人娘尻アナル大全　※サンプル動画あり  トップページ ＞ アナル・菊門・尻穴 作品 一覧 ＞ 素人娘尻アナル大全　※サンプル動画あり… |
| t01562 | True | True (0.93) | True (0.97) | True (0.98) | True (0.92) | True (0.98) | True (0.97) | True (0.90) | True (0.77) | True (0.88) | True (0.94) | True (0.89) | True (0.89) | True (0.89) | False (0.86) | True (0.74) | True (0.94) | True (0.94) | True (0.87) | True (0.84) | # 【アウトレット】激震パイ揺れ！暴走腰振り騎乗位 厳選ベスト5時間 オマ○コ感度無限大オーガズムお見せします!! (AV) [7LZBS… |
