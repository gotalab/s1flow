# nod-wake

2026-11-23 · 42 labelled dev cases (True 26, False 16) · split: leave-one-out (no test case among these: CV numbers only) · source: cases.json

gemini-decision@google has the lowest loss per case (miss 10, false alarm 1), 0.000 [0.000, 0.000] (API cost $0.36 per 10k, p99 658ms). Its interval overlaps with mammoth@openrouter, reflex@openrouter, bison@openrouter, decision-1.1@openrouter, clef-flash@openrouter, d1.2, decider-flash@openrouter, elephant@openrouter, decision-1@openrouter, heygen-decision@openrouter, mo@vercel, d1.2-ultra: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is gemini-decision@google's, 100% [100, 100].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | refused | failed |
|---|---|---|---|---|---|---|---|
| bison@openrouter | 42 | 97.6% [93, 100] | 0.98 | 0.99 | 0.09 | 0.0% (0/42) | 0/57 |
| clef-flash@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.97 | 0.13 | 0.0% (0/42) | 0/57 |
| clef-omni@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.95 | 0.12 | 0.0% (0/42) | 0/57 |
| clef@openrouter | 42 | 92.9% [86, 100] | 0.94 | 0.99 | 0.10 | 0.0% (0/42) | 0/57 |
| d1-ultra@openrouter | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.07 | 0.0% (0/42) | 0/57 |
| d1.1@openrouter | 42 | 92.9% [86, 100] | 0.94 | 0.99 | 0.07 | 0.0% (0/42) | 0/57 |
| d1.2 | 42 | 95.2% [88, 100] | 0.96 | 1.00 | 0.13 | 0.0% (0/42) | 0/57 |
| d1.2-ultra | 42 | 95.2% [88, 100] | 0.96 | 1.00 | 0.10 | 0.0% (0/42) | 0/57 |
| decider-1.3@vercel | 42 | 97.6% [93, 100] | 0.98 | 1.00 | 0.08 | 0.0% (0/42) | 0/57 |
| decider-flash@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.95 | 0.06 | 0.0% (0/42) | 0/57 |
| decider@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.99 | 0.06 | 0.0% (0/42) | 0/57 |
| decision-1.1@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.99 | 0.07 | 0.0% (0/42) | 0/57 |
| decision-1@openrouter | 42 | 90.5% [81, 98] | 0.92 | 1.00 | 0.07 | 0.0% (0/42) | 0/57 |
| drex-max-1.1@vercel | 42 | 92.9% [83, 100] | 0.94 | 1.00 | 0.11 | 0.0% (0/42) | 0/57 |
| drex-max@openrouter | 42 | 95.2% [88, 100] | 0.96 | 0.99 | 0.06 | 0.0% (0/42) | 0/57 |
| elephant@openrouter | 42 | 90.5% [81, 98] | 0.92 | 0.99 | 0.12 | 0.0% (0/42) | 0/57 |
| gemini-decision@google | 42 | 100.0% [100, 100] | 1.00 | 1.00 | 0.06 | 0.0% (0/42) | 0/57 |
| groundhog@openrouter | 42 | 92.9% [83, 100] | 0.94 | 0.98 | 0.03 | 0.0% (0/42) | 0/57 |
| heygen-decision@openrouter | 42 | 97.6% [93, 100] | 0.98 | 1.00 | 0.08 | 0.0% (0/42) | 0/57 |
| jev:1.14 | 42 | 92.9% [86, 100] | 0.95 | 1.00 | 0.05 | 0.0% (0/42) | 0/57 |
| joey@openrouter | 42 | 73.8% [60, 86] | 0.77 | 0.85 | 0.09 | 0.0% (0/42) | 0/57 |
| kev@openrouter | 42 | 83.3% [71, 93] | 0.84 | 0.98 | 0.17 | 0.0% (0/42) | 0/57 |
| luna@decisions | 42 | 88.1% [76, 98] | 0.91 | 0.98 | 0.09 | 2.4% (1/42) | 0/57 |
| mammoth@openrouter | 42 | 100.0% [100, 100] | 1.00 | 1.00 | 0.11 | 0.0% (0/42) | 0/57 |
| mo@vercel | 42 | 97.6% [93, 100] | 0.98 | 1.00 | 0.07 | 0.0% (0/42) | 0/57 |
| reflex@openrouter | 42 | 92.9% [86, 100] | 0.94 | 1.00 | 0.07 | 0.0% (0/42) | 0/57 |
| span@openrouter | 42 | 83.3% [71, 93] | 0.84 | 0.99 | 0.10 | 0.0% (0/42) | 0/57 |

Answered by: bison@openrouter = baseten/bison-1-20261120; clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; decider-1.3@vercel = perplexity/pplx-decider-v1.3; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max-1.1@vercel = nace-ai/drex-max-v1.1; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; groundhog@openrouter = baseten/groundhog-1-20261120; heygen-decision@openrouter = heygen/heygen-decision-1-20261112; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mo@vercel = modaic/mo; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | loss per case (miss 10, false alarm 1) | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| gemini-decision@google = | 0.000 [0.000, 0.000] | 100% [100, 100] | 0.50 | met |
| mammoth@openrouter = | 0.000 [0.000, 0.000] | 100% [100, 100] | 0.50 | met |
| reflex@openrouter = | 0.000 [0.000, 0.000] | 100% [100, 100] | 0.30 | met |
| bison@openrouter = | 0.024 [0.000, 0.071] | 98% [93, 100] | 0.50 | met |
| decision-1.1@openrouter = | 0.024 [0.000, 0.071] | 98% [93, 100] | 0.10 | met |
| clef-flash@openrouter = | 0.048 [0.000, 0.119] | 95% [88, 100] | 0.30 | met |
| d1.2 = | 0.048 [0.000, 0.119] | 95% [88, 100] | 0.30 | met |
| decider-flash@openrouter = | 0.048 [0.000, 0.119] | 95% [88, 100] | 0.30 | met |
| elephant@openrouter = | 0.048 [0.000, 0.119] | 95% [88, 100] | 0.30 | met |
| decision-1@openrouter = | 0.262 [0.000, 0.762] | 95% [88, 100] | 0.10 | met |
| heygen-decision@openrouter = | 0.262 [0.000, 0.786] | 95% [88, 100] | 0.30 | met |
| mo@vercel = | 0.262 [0.000, 0.762] | 95% [88, 100] | 0.30 | met |
| d1.2-ultra = | 0.286 [0.000, 0.786] | 93% [83, 100] | 0.30 | met |
| joey@openrouter | 0.095 [0.024, 0.190] | 90% [81, 98] | 0.30 | met |
| kev@openrouter | 0.095 [0.024, 0.190] | 90% [81, 98] | 0.30 | met |
| groundhog@openrouter | 0.214 [0.095, 0.357] | 79% [64, 90] | 0.10 | met |
| jev:1.14 | 0.310 [0.024, 0.833] | 90% [81, 98] | 0.50 | met |
| clef@openrouter | 0.333 [0.048, 0.833] | 88% [79, 95] | 0.30 | met |
| d1.1@openrouter | 0.333 [0.024, 0.881] | 88% [76, 98] | 0.30 | met |
| decider@openrouter | 0.333 [0.048, 0.858] | 88% [76, 98] | 0.10 | met |
| drex-max@openrouter | 0.333 [0.024, 0.857] | 88% [79, 98] | 0.10 | met |
| luna@decisions | 0.333 [0.024, 0.857] | 88% [76, 98] | 0.50 | met |
| clef-omni@openrouter | 0.357 [0.048, 0.905] | 86% [74, 95] | 0.30 | met |
| decider-1.3@vercel | 0.357 [0.048, 0.881] | 86% [74, 95] | 0.10 | met |
| drex-max-1.1@vercel | 0.357 [0.048, 0.905] | 86% [74, 95] | 0.10 | met |
| d1-ultra@openrouter | 0.381 [0.071, 0.882] | 83% [71, 93] | 0.10 | met |
| span@openrouter | 0.952 [0.238, 1.905] | 90% [81, 98] | 0.10 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## With other weights

| weights | tied at the top |
|---|---|
| as set: loss per case (miss 10, false alarm 1) | bison@openrouter, clef-flash@openrouter, d1.2, d1.2-ultra, decider-flash@openrouter, decision-1.1@openrouter, decision-1@openrouter, elephant@openrouter, gemini-decision@google, heygen-decision@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter |
| halved: loss per case (miss 5, false alarm 1) | bison@openrouter, clef-flash@openrouter, d1-ultra@openrouter, d1.2, d1.2-ultra, decider-flash@openrouter, decision-1.1@openrouter, decision-1@openrouter, elephant@openrouter, gemini-decision@google, heygen-decision@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter |
| doubled: loss per case (miss 20, false alarm 1) | bison@openrouter, clef-flash@openrouter, d1.2, d1.2-ultra, decider-flash@openrouter, decision-1.1@openrouter, decision-1@openrouter, elephant@openrouter, gemini-decision@google, heygen-decision@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter |

**The candidates tied at the top change: these weights decide the choice.** The weights are the task owner's to set; s1flow has no default. Re-ranked from the recorded answers, nothing asked again.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bison@openrouter | 42 | 225 ms | 264 ms | 694 ms | 782 ms | 3.1 | 0 | 2 | $0.36 | billed |  |
| clef-flash@openrouter | 42 | 334 ms | 726 ms | 1168 ms | 1391 ms | 3.5 | 0 | 4 | $0.10 | billed |  |
| clef-omni@openrouter | 42 | 242 ms | 332 ms | 367 ms | 376 ms | 1.5 | 0 | 4 | $0.67 | billed |  |
| clef@openrouter | 42 | 398 ms | 1435 ms | 2010 ms | 2132 ms | 5.1 | 0 | 4 | $0.84 | billed |  |
| d1-ultra@openrouter | 42 | 636 ms | 3058 ms | 5572 ms | 5574 ms | 8.8 | 0 | 4 | $0.13 | billed |  |
| d1.1@openrouter | 42 | 341 ms | 438 ms | 556 ms | 573 ms | 1.6 | 0 | 4 | $0.06 | billed |  |
| d1.2 | 42 | 119 ms | 253 ms | 526 ms | 526 ms | 4.4 | 0 | 4 | $0.06 | billed |  |
| d1.2-ultra | 42 | 120 ms | 147 ms | 224 ms | 249 ms | 1.9 | 0 | 4 | $0.13 | billed | ○ |
| decider-1.3@vercel | 42 | 437 ms | 844 ms | 2196 ms | 2714 ms | 5.0 | 0 | 4 | $0.07 | billed |  |
| decider-flash@openrouter | 42 | 153 ms | 250 ms | 385 ms | 461 ms | 2.5 | 0 | 4 | $0.03 | billed | ○ |
| decider@openrouter | 42 | 230 ms | 339 ms | 626 ms | 722 ms | 2.7 | 0 | 4 | $0.07 | billed |  |
| decision-1.1@openrouter | 42 | 232 ms | 262 ms | 525 ms | 566 ms | 2.3 | 0 | 4 | $0.13 | billed | ○ |
| decision-1@openrouter | 42 | 270 ms | 367 ms | 428 ms | 432 ms | 1.6 | 0 | 4 | $0.11 | billed |  |
| drex-max-1.1@vercel | 42 | 357 ms | 608 ms | 876 ms | 933 ms | 2.5 | 0 | 4 | $0.10 | billed |  |
| drex-max@openrouter | 42 | 273 ms | 435 ms | 668 ms | 707 ms | 2.4 | 0 | 4 | $0.20 | billed |  |
| elephant@openrouter | 42 | 176 ms | 214 ms | 324 ms | 360 ms | 1.8 | 0 | 4 | $0.12 | billed | ○ |
| gemini-decision@google | 42 | 254 ms | 501 ms | 658 ms | 658 ms | 2.6 | 0 | 4 | $0.36 | estimated |  |
| groundhog@openrouter | 42 | 224 ms | 396 ms | 545 ms | 585 ms | 2.4 | 0 | 2 | $0.12 | billed |  |
| heygen-decision@openrouter | 42 | 552 ms | 1204 ms | 2009 ms | 2066 ms | 3.6 | 0 | 4 | $0.47 | billed |  |
| jev:1.14 | 42 | 128 ms | 254 ms | 593 ms | 596 ms | 4.6 | 0 | 4 | $0.31 | estimated |  |
| joey@openrouter | 42 | 167 ms | 175 ms | 275 ms | 276 ms | 1.6 | 0 | 4 | $0.03 | billed | ○ |
| kev@openrouter | 42 | 1093 ms | 3795 ms | 4385 ms | 4454 ms | 4.0 | 0 | 4 | $0.11 | billed |  |
| luna@decisions | 41 | 266 ms | 354 ms | 530 ms | 537 ms | 2.0 | 0 | 4 | $0.45 | estimated |  |
| mammoth@openrouter | 42 | 384 ms | 760 ms | 1456 ms | 1741 ms | 3.8 | 0 | 4 | $0.34 | billed |  |
| mo@vercel | 42 | 359 ms | 554 ms | 910 ms | 952 ms | 2.5 | 0 | 4 | $0.14 | billed |  |
| reflex@openrouter | 42 | 174 ms | 261 ms | 552 ms | 580 ms | 3.2 | 0 | 4 | $0.14 | billed | ○ |
| span@openrouter | 42 | 471 ms | 611 ms | 789 ms | 794 ms | 1.7 | 0 | 4 | $0.04 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Under 100 calls, a model's p99 means little more than its max.
Where the API costs come from: billed: bison@openrouter, clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, decider-1.3@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max-1.1@vercel, drex-max@openrouter, elephant@openrouter, groundhog@openrouter, heygen-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| bison@openrouter | $0.0015 | 5 s (estimated, 42 calls) | 21 min | 2 |
| clef-flash@openrouter | $0.0004 | 4 s (estimated, 42 calls) | 18 min | 4 |
| clef-omni@openrouter | $0.0028 | 3 s (estimated, 42 calls) | 10 min | 4 |
| clef@openrouter | $0.0035 | 7 s (estimated, 42 calls) | 28 min | 4 |
| d1-ultra@openrouter | $0.0006 | 13 s (estimated, 42 calls) | 52 min | 4 |
| d1.1@openrouter | $0.0003 | 3 s (estimated, 42 calls) | 14 min | 4 |
| d1.2 | $0.0003 | 2 s (estimated, 42 calls) | 7 min | 4 |
| d1.2-ultra | $0.0006 | 1 s (estimated, 42 calls) | 5 min | 4 |
| decider-1.3@vercel | $0.0003 | 6 s (estimated, 42 calls) | 24 min | 4 |
| decider-flash@openrouter | $0.0001 | 2 s (estimated, 42 calls) | 7 min | 4 |
| decider@openrouter | $0.0003 | 3 s (estimated, 42 calls) | 11 min | 4 |
| decision-1.1@openrouter | $0.0005 | 3 s (estimated, 42 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0005 | 3 s (estimated, 42 calls) | 12 min | 4 |
| drex-max-1.1@vercel | $0.0004 | 4 s (estimated, 42 calls) | 17 min | 4 |
| drex-max@openrouter | $0.0008 | 3 s (estimated, 42 calls) | 13 min | 4 |
| elephant@openrouter | $0.0005 | 2 s (estimated, 42 calls) | 8 min | 4 |
| gemini-decision@google | $0.0015 | 3 s (estimated, 42 calls) | 13 min | 4 |
| groundhog@openrouter | $0.0005 | 6 s (estimated, 42 calls) | 22 min | 2 |
| heygen-decision@openrouter | $0.0020 | 7 s (estimated, 42 calls) | 29 min | 4 |
| jev:1.14 | $0.0013 | 2 s (estimated, 42 calls) | 7 min | 4 |
| joey@openrouter | $0.0001 | 2 s (estimated, 42 calls) | 7 min | 4 |
| kev@openrouter | $0.0005 | 19 s (estimated, 42 calls) | 74 min | 4 |
| luna@decisions | $0.0019 | 3 s (estimated, 41 calls) | 11 min | 4 |
| mammoth@openrouter | $0.0014 | 5 s (estimated, 42 calls) | 20 min | 4 |
| mo@vercel | $0.0006 | 4 s (estimated, 42 calls) | 18 min | 4 |
| reflex@openrouter | $0.0006 | 2 s (estimated, 42 calls) | 9 min | 4 |
| span@openrouter | $0.0002 | 5 s (estimated, 42 calls) | 20 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

[ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.
Refused: inputs the model did not take (question type, image, audio, video, PDF, length limits) and answers it declined to give. The model's limit, not a failed call: the candidate is kept, and the case stays in every denominator.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 10 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| bison@openrouter | 97.6% | 97.6% | 0 | 1 | 0.50 | 0.50 |
| clef-flash@openrouter | 92.9% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| clef-omni@openrouter | 90.5% | 85.7% | 1 | 5 | 0.30 | 0.30 |
| clef@openrouter | 92.9% | 88.1% | 1 | 4 | 0.30 | 0.30 |
| d1-ultra@openrouter | 92.9% | 83.3% | 1 | 6 | 0.10 | 0.10 |
| d1.1@openrouter | 92.9% | 88.1% | 1 | 4 | 0.30 | 0.30 |
| d1.2 | 95.2% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| d1.2-ultra | 95.2% | 92.9% | 1 | 2 | 0.30 | 0.30 |
| decider-1.3@vercel | 97.6% | 85.7% | 1 | 5 | 0.10 | 0.10 |
| decider-flash@openrouter | 90.5% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| decider@openrouter | 92.9% | 88.1% | 1 | 4 | 0.10 | 0.10 |
| decision-1.1@openrouter | 92.9% | 97.6% | 0 | 1 | 0.10 | 0.10 |
| decision-1@openrouter | 90.5% | 95.2% | 1 | 1 | 0.10 | 0.10 |
| drex-max-1.1@vercel | 92.9% | 85.7% | 1 | 5 | 0.10 | 0.10 |
| drex-max@openrouter | 95.2% | 88.1% | 1 | 4 | 0.10 | 0.10 |
| elephant@openrouter | 90.5% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| gemini-decision@google | 100.0% | 100.0% | 0 | 0 | 0.50 | 0.50 |
| groundhog@openrouter | 92.9% | 78.6% | 0 | 9 | 0.10 | 0.10 |
| heygen-decision@openrouter | 97.6% | 95.2% | 1 | 1 | 0.30 | 0.30 |
| jev:1.14 | 92.9% | 90.5% | 1 | 3 | 0.50 | 0.50 |
| joey@openrouter | 73.8% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| kev@openrouter | 83.3% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| luna@decisions | 88.1% | 88.1% | 1 | 4 | 0.50 | 0.50 |
| mammoth@openrouter | 100.0% | 100.0% | 0 | 0 | 0.50 | 0.50 |
| mo@vercel | 97.6% | 95.2% | 1 | 1 | 0.30 | 0.30 |
| reflex@openrouter | 92.9% | 100.0% | 0 | 0 | 0.30 | 0.30 |
| span@openrouter | 83.3% | 90.5% | 4 | 0 | 0.10 | 0.10 |

## Misses and false alarms by threshold (bison@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 8 (50%) |
| 0.20 | 0 (0%) | 4 (25%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 0 (0%) | 1 (6%) |
| 0.60 | 2 (8%) | 1 (6%) |
| 0.70 | 5 (19%) | 0 (0%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 6 (23%) | 0 (0%) |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 14 (88%) |
| 0.20 | 0 (0%) | 5 (31%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 1 (4%) | 2 (12%) |
| 0.50 | 2 (8%) | 1 (6%) |
| 0.60 | 4 (15%) | 1 (6%) |
| 0.70 | 7 (27%) | 1 (6%) |
| 0.80 | 12 (46%) | 0 (0%) |
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
| 0.10 | 0 (0%) | 12 (75%) |
| 0.20 | 0 (0%) | 8 (50%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 1 (4%) | 4 (25%) |
| 0.50 | 1 (4%) | 2 (12%) |
| 0.60 | 2 (8%) | 1 (6%) |
| 0.70 | 2 (8%) | 1 (6%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 8 (31%) | 0 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 6 (38%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 1 (4%) | 0 (0%) |
| 0.40 | 2 (8%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 4 (15%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 7 (27%) | 0 (0%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 11 (69%) |
| 0.20 | 0 (0%) | 7 (44%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 0 (0%) | 2 (12%) |
| 0.50 | 1 (4%) | 2 (12%) |
| 0.60 | 2 (8%) | 1 (6%) |
| 0.70 | 2 (8%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

## Misses and false alarms by threshold (d1.2)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 12 (75%) |
| 0.20 | 0 (0%) | 9 (56%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 2 (8%) | 0 (0%) |
| 0.60 | 2 (8%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 7 (27%) | 0 (0%) |

## Misses and false alarms by threshold (d1.2-ultra)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 7 (44%) |
| 0.20 | 0 (0%) | 3 (19%) |
| 0.30 | 0 (0%) | 2 (12%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 1 (4%) | 1 (6%) |
| 0.60 | 2 (8%) | 0 (0%) |
| 0.70 | 5 (19%) | 0 (0%) |
| 0.80 | 6 (23%) | 0 (0%) |
| 0.90 | 7 (27%) | 0 (0%) |

## Misses and false alarms by threshold (decider-1.3@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 5 (31%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 1 (4%) | 1 (6%) |
| 0.40 | 1 (4%) | 1 (6%) |
| 0.50 | 1 (4%) | 0 (0%) |
| 0.60 | 2 (8%) | 0 (0%) |
| 0.70 | 3 (12%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

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

## Misses and false alarms by threshold (decision-1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 1 (6%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 2 (8%) | 1 (6%) |
| 0.40 | 3 (12%) | 1 (6%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 3 (12%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 1 (6%) |
| 0.20 | 1 (4%) | 0 (0%) |
| 0.30 | 1 (4%) | 0 (0%) |
| 0.40 | 2 (8%) | 0 (0%) |
| 0.50 | 4 (15%) | 0 (0%) |
| 0.60 | 4 (15%) | 0 (0%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max-1.1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 5 (31%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 1 (4%) | 1 (6%) |
| 0.40 | 1 (4%) | 0 (0%) |
| 0.50 | 3 (12%) | 0 (0%) |
| 0.60 | 3 (12%) | 0 (0%) |
| 0.70 | 5 (19%) | 0 (0%) |
| 0.80 | 5 (19%) | 0 (0%) |
| 0.90 | 6 (23%) | 0 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 4 (25%) |
| 0.20 | 1 (4%) | 2 (12%) |
| 0.30 | 1 (4%) | 1 (6%) |
| 0.40 | 2 (8%) | 0 (0%) |
| 0.50 | 2 (8%) | 0 (0%) |
| 0.60 | 2 (8%) | 0 (0%) |
| 0.70 | 2 (8%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

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

## Misses and false alarms by threshold (gemini-decision@google)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 2 (12%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 0 (0%) | 1 (6%) |
| 0.40 | 0 (0%) | 0 (0%) |
| 0.50 | 0 (0%) | 0 (0%) |
| 0.60 | 1 (4%) | 0 (0%) |
| 0.70 | 1 (4%) | 0 (0%) |
| 0.80 | 2 (8%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

## Misses and false alarms by threshold (groundhog@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 9 (56%) |
| 0.20 | 1 (4%) | 4 (25%) |
| 0.30 | 2 (8%) | 2 (12%) |
| 0.40 | 2 (8%) | 1 (6%) |
| 0.50 | 2 (8%) | 1 (6%) |
| 0.60 | 2 (8%) | 1 (6%) |
| 0.70 | 4 (15%) | 0 (0%) |
| 0.80 | 4 (15%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (heygen-decision@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 8 (50%) |
| 0.20 | 0 (0%) | 3 (19%) |
| 0.30 | 0 (0%) | 1 (6%) |
| 0.40 | 0 (0%) | 1 (6%) |
| 0.50 | 1 (4%) | 0 (0%) |
| 0.60 | 1 (4%) | 0 (0%) |
| 0.70 | 3 (12%) | 0 (0%) |
| 0.80 | 3 (12%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 8 (50%) |
| 0.20 | 0 (0%) | 5 (31%) |
| 0.30 | 0 (0%) | 4 (25%) |
| 0.40 | 0 (0%) | 3 (19%) |
| 0.50 | 0 (0%) | 3 (19%) |
| 0.60 | 0 (0%) | 3 (19%) |
| 0.70 | 1 (4%) | 1 (6%) |
| 0.80 | 1 (4%) | 0 (0%) |
| 0.90 | 2 (8%) | 0 (0%) |

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
| 0.50 | 7 (27%) | 0 (0%) |
| 0.60 | 17 (65%) | 0 (0%) |
| 0.70 | 23 (88%) | 0 (0%) |
| 0.80 | 25 (96%) | 0 (0%) |
| 0.90 | 26 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (4%) | 11 (69%) |
| 0.20 | 1 (4%) | 7 (44%) |
| 0.30 | 1 (4%) | 4 (25%) |
| 0.40 | 1 (4%) | 4 (25%) |
| 0.50 | 1 (4%) | 4 (25%) |
| 0.60 | 1 (4%) | 4 (25%) |
| 0.70 | 2 (8%) | 4 (25%) |
| 0.80 | 3 (12%) | 0 (0%) |
| 0.90 | 5 (19%) | 0 (0%) |

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
| 0.90 | 10 (38%) | 0 (0%) |

## Misses and false alarms by threshold (mo@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 6 (38%) |
| 0.20 | 0 (0%) | 1 (6%) |
| 0.30 | 0 (0%) | 1 (6%) |
| 0.40 | 1 (4%) | 0 (0%) |
| 0.50 | 1 (4%) | 0 (0%) |
| 0.60 | 2 (8%) | 0 (0%) |
| 0.70 | 2 (8%) | 0 (0%) |
| 0.80 | 3 (12%) | 0 (0%) |
| 0.90 | 4 (15%) | 0 (0%) |

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


## Cases the models disagree on (12 of 22)

| id | label | bison@openrouter | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | decider-1.3@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max-1.1@vercel | drex-max@openrouter | elephant@openrouter | gemini-decision@google | groundhog@openrouter | heygen-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mo@vercel | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotel-jaa-yasui | True | True (0.98) | True (0.86) | True (0.91) | True (0.95) | True (0.99) | True (0.99) | True (0.97) | True (0.97) | True (0.99) | True (0.93) | True (1.00) | True (1.00) | True (1.00) | True (0.99) | True (0.99) | True (0.94) | True (1.00) | True (0.94) | True (0.95) | True (1.00) | False (0.54) | True (0.68) | True (0.99) | True (0.93) | True (0.99) | True (1.00) | True (0.80) | {"earlier": ["ユーザー: 大阪出張、10/14泊で梅田近くのビジホ"], "agent": "候補は2つです。\n1. ホテ… |
| add-milk | True | True (0.98) | True (0.79) | True (0.90) | True (0.97) | True (0.99) | True (0.99) | True (0.97) | True (0.99) | True (1.00) | True (0.97) | True (1.00) | True (1.00) | True (1.00) | True (0.99) | True (1.00) | True (0.94) | True (1.00) | True (1.00) | True (0.98) | True (1.00) | False (0.62) | True (0.58) | True (0.99) | True (0.94) | True (1.00) | True (1.00) | True (1.00) | {"earlier": ["ユーザー: 卵と食パン切れたからネットスーパーで頼んで"], "agent": "イオンネットスーパーで卵10… |
| sw-fix-tests-un | True | True (0.96) | True (0.93) | True (0.85) | True (0.97) | True (0.99) | True (1.00) | True (0.98) | True (0.98) | True (0.99) | True (0.94) | True (1.00) | True (1.00) | True (1.00) | True (0.98) | True (1.00) | True (0.97) | True (1.00) | True (0.99) | True (0.99) | True (1.00) | True (0.80) | False (0.62) | True (0.99) | True (0.93) | True (0.99) | True (1.00) | True (0.99) | {"earlier": ["ユーザー: npm test 回して"], "agent": "テストを実行しました。48件中3件が失敗してい… |
| sw-naming-change | True | True (0.98) | True (0.91) | True (0.60) | True (0.97) | True (0.98) | True (0.99) | True (0.97) | True (0.97) | True (0.98) | False (0.66) | True (0.99) | True (1.00) | True (0.99) | True (0.97) | True (0.98) | True (0.98) | True (1.00) | True (0.99) | True (0.97) | True (1.00) | True (0.76) | True (0.50) | True (0.99) | True (0.90) | True (0.99) | True (1.00) | True (0.98) | {"agent": "APIレスポンスのキー名を userId に統一しました。変更は api/handlers 以下の6ファイルです。"… |
| thanks-plus-bus | True | True (0.97) | True (0.89) | True (0.85) | True (0.98) | True (0.97) | True (0.99) | True (0.96) | True (0.97) | True (0.99) | True (0.97) | True (0.98) | True (1.00) | True (1.00) | True (0.95) | True (0.98) | True (0.98) | True (1.00) | True (0.98) | True (0.96) | True (1.00) | False (0.58) | True (0.84) | True (0.99) | True (0.94) | True (0.98) | True (0.98) | True (0.98) | {"agent": "河口湖行きの高速バス、土曜7:10新宿発で2名分予約しました。", "user": "ありがとう！あと帰りのバスも調… |
| ryokai-to-cancel-fee | True | True (0.58) | True (0.72) | True (0.79) | True (0.91) | True (0.87) | True (0.96) | True (0.96) | True (0.70) | True (0.96) | True (0.68) | True (0.90) | True (0.91) | True (0.93) | True (0.93) | True (0.90) | True (0.83) | True (0.89) | True (0.95) | True (0.97) | True (1.00) | True (0.52) | False (0.55) | True (0.84) | True (0.93) | True (0.97) | True (0.97) | False (0.61) | {"earlier": ["ユーザー: 来週の美容院、キャンセルしたい"], "agent": "前日以降のキャンセルのため、キャンセル料… |
| tickets-kaatte | True | True (0.99) | True (0.66) | True (0.83) | True (0.94) | True (0.99) | True (0.99) | True (0.97) | True (0.98) | True (1.00) | True (0.85) | True (1.00) | True (1.00) | True (0.99) | True (0.99) | True (1.00) | True (0.95) | True (1.00) | True (0.99) | True (0.99) | True (1.00) | False (0.55) | True (0.54) | True (0.99) | True (0.93) | True (1.00) | True (1.00) | True (0.94) | {"earlier": ["ユーザー: ミセスのライブ、リセールで出たら教えて"], "agent": "11/22 東京ドーム公演のリセ… |
| sw-dont-touch-file | True | True (0.99) | True (0.92) | True (0.92) | True (0.98) | True (0.99) | True (1.00) | True (0.99) | True (0.98) | True (1.00) | True (0.97) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | True (0.92) | True (1.00) | True (0.99) | True (0.98) | True (1.00) | False (0.52) | True (0.64) | True (1.00) | True (0.94) | True (1.00) | True (1.00) | True (0.96) | {"earlier": ["ユーザー: ログイン周りのバグ直して"], "agent": "原因は auth/session.ts のトー… |
| oyasumi | False | False (0.90) | False (0.92) | False (0.88) | False (0.56) | False (0.95) | True (0.53) | False (0.84) | False (0.83) | False (0.80) | False (0.96) | False (0.56) | False (1.00) | False (0.99) | False (0.83) | False (0.89) | False (0.89) | False (0.98) | False (0.96) | False (0.87) | False (0.88) | False (0.81) | False (0.78) | False (0.74) | False (0.94) | False (0.85) | False (0.90) | False (0.99) | {"agent": "明日の朝7時に、天気と電車の遅延情報をまとめてお送りします。", "user": "おやすみ"} |
| wait-before-submit | True | True (0.97) | True (0.70) | True (0.78) | True (0.94) | True (0.88) | True (0.97) | True (0.89) | True (0.86) | True (0.97) | True (0.96) | True (0.75) | True (1.00) | True (0.97) | True (0.85) | True (0.93) | False (0.51) | True (0.98) | True (1.00) | True (0.96) | True (0.99) | True (0.60) | True (0.54) | True (0.99) | True (0.95) | True (0.95) | True (0.97) | True (0.88) | {"earlier": ["ユーザー: 区のワクチン接種の予約フォーム埋めといて"], "agent": "必要事項を入力しました。10月… |
| yoroshiku-already-agreed | False | False (0.72) | False (0.76) | True (0.68) | False (0.73) | False (0.89) | False (0.73) | False (0.79) | False (0.88) | False (0.85) | False (0.94) | False (0.83) | False (0.97) | False (1.00) | False (0.84) | False (0.94) | False (0.91) | False (0.96) | False (0.71) | False (0.74) | False (0.68) | True (0.74) | False (0.74) | True (0.71) | False (0.88) | False (0.91) | False (0.95) | False (0.97) | {"earlier": ["ユーザー: 土曜のゴルフ、雨だったら中止にしたい"], "agent": "承知しました。土曜の朝6時に天気を… |
| ok-info | False | False (0.92) | False (0.89) | False (0.81) | False (0.80) | False (0.94) | False (0.91) | False (0.73) | False (0.88) | False (0.93) | False (0.94) | False (0.93) | False (1.00) | False (0.99) | False (0.91) | False (0.95) | False (0.96) | False (0.93) | False (0.96) | False (0.94) | False (0.84) | True (0.73) | False (0.80) | False (0.77) | False (0.93) | False (0.93) | False (0.97) | False (0.99) | {"agent": "お知らせです。明日10/1から、ご利用中の駐輪場の月額料金が2,000円から2,200円に変わります。お手続きは不要… |
