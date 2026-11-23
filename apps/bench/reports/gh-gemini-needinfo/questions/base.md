# gh-gemini-needinfo

2026-11-23 · 210 labelled dev cases (False 165, True 45) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

heygen-decision@openrouter has the highest recall at 5% false alarms or fewer, 27% [15, 41] (false alarms 3.6%) (API cost $0.64 per 10k, p99 885ms). Its interval overlaps with decider-flash@openrouter, decision-1@openrouter, clef@openrouter, decision-1.1@openrouter, joey@openrouter, span@openrouter, d1.2, d1.2-ultra, clef-flash@openrouter, decider-1.3@vercel, gemini-decision@google, d1.1@openrouter, groundhog@openrouter, clef-omni@openrouter, drex-max-1.1@vercel, reflex@openrouter, elephant@openrouter, d1-ultra@openrouter, drex-max@openrouter, kev@openrouter, mammoth@openrouter, mo@vercel, luna@decisions, jev:1.14, decider@openrouter, bison@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is joey@openrouter's, 80% [75, 85].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | refused | failed |
|---|---|---|---|---|---|---|---|
| bison@openrouter | 210 | 75.2% [70, 81] | 0.38 | 0.61 | 0.16 | 0.0% (0/210) | 0/210 |
| clef-flash@openrouter | 210 | 77.1% [71, 83] | 0.38 | 0.63 | 0.11 | 0.0% (0/210) | 0/210 |
| clef-omni@openrouter | 210 | 78.1% [73, 84] | 0.38 | 0.60 | 0.13 | 0.0% (0/210) | 0/210 |
| clef@openrouter | 210 | 77.1% [72, 83] | 0.35 | 0.59 | 0.15 | 0.0% (0/210) | 0/210 |
| d1-ultra@openrouter | 210 | 75.2% [70, 81] | 0.37 | 0.56 | 0.16 | 0.0% (0/210) | 0/210 |
| d1.1@openrouter | 210 | 71.9% [66, 78] | 0.35 | 0.60 | 0.18 | 0.0% (0/210) | 0/210 |
| d1.2 | 210 | 74.3% [68, 80] | 0.34 | 0.62 | 0.11 | 0.0% (0/210) | 0/210 |
| d1.2-ultra | 210 | 75.7% [70, 82] | 0.37 | 0.58 | 0.16 | 0.0% (0/210) | 0/210 |
| decider-1.3@vercel | 210 | 78.1% [73, 84] | 0.39 | 0.60 | 0.20 | 0.0% (0/210) | 0/210 |
| decider-flash@openrouter | 210 | 78.6% [73, 84] | 0.35 | 0.62 | 0.14 | 0.0% (0/210) | 0/210 |
| decider@openrouter | 210 | 77.6% [72, 83] | 0.39 | 0.60 | 0.18 | 0.0% (0/210) | 0/210 |
| decision-1.1@openrouter | 210 | 71.9% [66, 79] | 0.35 | 0.59 | 0.21 | 0.0% (0/210) | 0/210 |
| decision-1@openrouter | 210 | 71.4% [65, 78] | 0.35 | 0.58 | 0.24 | 0.0% (0/210) | 0/210 |
| drex-max-1.1@vercel | 210 | 78.1% [72, 84] | 0.38 | 0.59 | 0.18 | 0.0% (0/210) | 0/210 |
| drex-max@openrouter | 210 | 75.2% [70, 81] | 0.37 | 0.57 | 0.20 | 0.0% (0/210) | 0/210 |
| elephant@openrouter | 210 | 72.4% [66, 79] | 0.34 | 0.58 | 0.17 | 0.0% (0/210) | 0/210 |
| gemini-decision@google | 210 | 73.8% [68, 80] | 0.35 | 0.60 | 0.17 | 0.0% (0/210) | 0/210 |
| groundhog@openrouter | 210 | 72.9% [67, 79] | 0.37 | 0.66 | 0.15 | 0.0% (0/210) | 0/210 |
| heygen-decision@openrouter | 210 | 74.3% [68, 80] | 0.37 | 0.63 | 0.16 | 0.0% (0/210) | 0/210 |
| jev:1.14 | 210 | 71.9% [66, 78] | 0.34 | 0.61 | 0.13 | 0.0% (0/210) | 0/210 |
| joey@openrouter | 210 | 80.0% [75, 85] | 0.34 | 0.58 | 0.07 | 0.0% (0/210) | 0/210 |
| kev@openrouter | 210 | 78.1% [72, 83] | 0.30 | 0.58 | 0.05 | 0.0% (0/210) | 0/210 |
| luna@decisions | 210 | 75.7% [70, 82] | 0.37 | 0.63 | 0.19 | 0.0% (0/210) | 0/210 |
| mammoth@openrouter | 210 | 76.7% [71, 83] | 0.38 | 0.61 | 0.18 | 0.0% (0/210) | 0/210 |
| mo@vercel | 210 | 77.1% [72, 83] | 0.38 | 0.60 | 0.20 | 0.0% (0/210) | 0/210 |
| reflex@openrouter | 210 | 78.1% [73, 84] | 0.39 | 0.63 | 0.19 | 0.0% (0/210) | 0/210 |
| span@openrouter | 210 | 76.7% [71, 83] | 0.38 | 0.63 | 0.17 | 0.0% (0/210) | 0/210 |

Answered by: bison@openrouter = baseten/bison-1-20261120; clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; decider-1.3@vercel = perplexity/pplx-decider-v1.3; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max-1.1@vercel = nace-ai/drex-max-v1.1; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; groundhog@openrouter = baseten/groundhog-1-20261120; heygen-decision@openrouter = heygen/heygen-decision-1-20261112; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mo@vercel = modaic/mo; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | recall at 5% false alarms or fewer | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| heygen-decision@openrouter = | 27% [15, 41] (false alarms 3.6%) | 81% [76, 87] | 0.92 | met |
| decider-flash@openrouter = | 24% [13, 38] (false alarms 3.6%) | 81% [76, 87] | 0.77 | met |
| decision-1@openrouter = | 27% [15, 40] (false alarms 4.8%) | 80% [75, 86] | 1.00 | met |
| clef@openrouter = | 24% [12, 38] (false alarms 4.2%) | 80% [76, 86] | 0.81 | met |
| decision-1.1@openrouter = | 24% [13, 38] (false alarms 4.2%) | 80% [75, 86] | 1.00 | met |
| joey@openrouter = | 24% [12, 38] (false alarms 4.8%) | 80% [75, 85] | 0.50 | met |
| span@openrouter = | 24% [13, 39] (false alarms 4.8%) | 80% [75, 86] | 0.92 | met |
| d1.2 = | 22% [12, 35] (false alarms 4.2%) | 80% [74, 85] | 0.93 | met |
| d1.2-ultra = | 22% [11, 36] (false alarms 4.2%) | 80% [74, 86] | 0.95 | met |
| clef-flash@openrouter = | 22% [11, 35] (false alarms 4.8%) | 80% [74, 85] | 0.84 | met |
| decider-1.3@vercel = | 22% [11, 37] (false alarms 4.8%) | 80% [74, 85] | 0.99 | met |
| gemini-decision@google = | 22% [11, 36] (false alarms 4.8%) | 80% [74, 85] | 0.97 | met |
| d1.1@openrouter = | 20% [9, 33] (false alarms 4.2%) | 80% [74, 85] | 0.97 | met |
| groundhog@openrouter = | 20% [9, 33] (false alarms 4.2%) | 80% [74, 85] | 0.94 | met |
| clef-omni@openrouter = | 22% [11, 35] (false alarms 5.5%) | 79% [73, 85] | 0.86 | met |
| drex-max-1.1@vercel = | 20% [9, 33] (false alarms 4.8%) | 79% [73, 85] | 0.95 | met |
| reflex@openrouter = | 20% [9, 33] (false alarms 4.8%) | 79% [74, 84] | 1.00 | met |
| elephant@openrouter = | 16% [6, 27] (false alarms 3.6%) | 79% [73, 85] | 0.93 | met |
| d1-ultra@openrouter = | 20% [9, 32] (false alarms 5.5%) | 79% [73, 84] | 0.95 | met |
| drex-max@openrouter = | 18% [7, 29] (false alarms 4.8%) | 79% [73, 84] | 0.99 | met |
| kev@openrouter = | 18% [7, 29] (false alarms 4.8%) | 79% [73, 84] | 0.57 | met |
| mammoth@openrouter = | 18% [8, 30] (false alarms 4.8%) | 79% [73, 84] | 0.96 | met |
| mo@vercel = | 16% [5, 27] (false alarms 4.2%) | 79% [73, 84] | 0.99 | met |
| luna@decisions = | 18% [8, 31] (false alarms 5.5%) | 78% [73, 84] | 0.96 | met |
| jev:1.14 = | 16% [5, 27] (false alarms 4.8%) | 78% [73, 84] | 0.97 | met |
| decider@openrouter = | 16% [5, 27] (false alarms 5.5%) | 78% [72, 83] | 0.98 | met |
| bison@openrouter = | 11% [2, 21] (false alarms 4.8%) | 77% [71, 83] | 0.95 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bison@openrouter | 210 | 245 ms | 274 ms | 348 ms | 402 ms | 1.4 | 0 | 2 | $0.60 | billed |  |
| clef-flash@openrouter | 210 | 260 ms | 335 ms | 687 ms | 755 ms | 2.6 | 0 | 4 | $0.15 | billed |  |
| clef-omni@openrouter | 210 | 166 ms | 212 ms | 308 ms | 576 ms | 1.9 | 0 | 4 | $0.89 | billed |  |
| clef@openrouter | 210 | 319 ms | 880 ms | 2452 ms | 5621 ms | 7.7 | 0 | 4 | $1.30 | billed |  |
| d1-ultra@openrouter | 210 | 605 ms | 5635 ms | 6150 ms | 7202 ms | 10.2 | 15 | 4 | $0.22 | billed |  |
| d1.1@openrouter | 210 | 207 ms | 348 ms | 445 ms | 468 ms | 2.1 | 0 | 4 | $0.10 | billed |  |
| d1.2 | 210 | 117 ms | 178 ms | 637 ms | 700 ms | 5.4 | 1 | 4 | $0.10 | billed |  |
| d1.2-ultra | 210 | 119 ms | 164 ms | 407 ms | 484 ms | 3.4 | 0 | 4 | $0.22 | billed |  |
| decider-1.3@vercel | 210 | 354 ms | 435 ms | 802 ms | 1245 ms | 2.3 | 0 | 4 | $0.11 | billed |  |
| decider-flash@openrouter | 210 | 134 ms | 151 ms | 203 ms | 457 ms | 1.5 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 210 | 218 ms | 297 ms | 800 ms | 1323 ms | 3.7 | 0 | 4 | $0.11 | billed |  |
| decision-1.1@openrouter | 210 | 231 ms | 265 ms | 322 ms | 350 ms | 1.4 | 0 | 4 | $0.23 | billed |  |
| decision-1@openrouter | 210 | 238 ms | 301 ms | 359 ms | 423 ms | 1.5 | 0 | 4 | $0.21 | billed | ○ |
| drex-max-1.1@vercel | 210 | 350 ms | 522 ms | 760 ms | 1412 ms | 2.2 | 0 | 4 | $0.17 | billed |  |
| drex-max@openrouter | 210 | 256 ms | 357 ms | 764 ms | 851 ms | 3.0 | 0 | 4 | $0.33 | billed |  |
| elephant@openrouter | 210 | 172 ms | 272 ms | 316 ms | 457 ms | 1.8 | 0 | 4 | $0.20 | billed |  |
| gemini-decision@google | 210 | 299 ms | 379 ms | 433 ms | 501 ms | 1.4 | 0 | 4 | $0.62 | estimated |  |
| groundhog@openrouter | 210 | 228 ms | 255 ms | 436 ms | 562 ms | 1.9 | 0 | 2 | $0.21 | billed |  |
| heygen-decision@openrouter | 210 | 291 ms | 490 ms | 885 ms | 1217 ms | 3.0 | 0 | 4 | $0.64 | billed |  |
| jev:1.14 | 210 | 102 ms | 133 ms | 204 ms | 435 ms | 2.0 | 0 | 4 | $0.32 | estimated |  |
| joey@openrouter | 210 | 167 ms | 198 ms | 278 ms | 944 ms | 1.7 | 0 | 4 | $0.06 | billed |  |
| kev@openrouter | 210 | 528 ms | 646 ms | 1094 ms | 1355 ms | 2.1 | 0 | 4 | $0.20 | billed |  |
| luna@decisions | 210 | 184 ms | 342 ms | 551 ms | 687 ms | 3.0 | 0 | 4 | $0.63 | estimated |  |
| mammoth@openrouter | 210 | 180 ms | 206 ms | 356 ms | 509 ms | 2.0 | 0 | 4 | $0.56 | billed |  |
| mo@vercel | 210 | 348 ms | 431 ms | 732 ms | 890 ms | 2.1 | 0 | 4 | $0.23 | billed |  |
| reflex@openrouter | 210 | 258 ms | 282 ms | 358 ms | 435 ms | 1.4 | 0 | 4 | $0.24 | billed |  |
| span@openrouter | 210 | 523 ms | 801 ms | 947 ms | 1276 ms | 1.8 | 0 | 4 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: bison@openrouter, clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, decider-1.3@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max-1.1@vercel, drex-max@openrouter, elephant@openrouter, groundhog@openrouter, heygen-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| bison@openrouter | $0.01 | 26 s (estimated, 210 calls) | 21 min | 2 |
| clef-flash@openrouter | $0.0032 | 14 s (estimated, 210 calls) | 11 min | 4 |
| clef-omni@openrouter | $0.02 | 9 s (estimated, 210 calls) | 7 min | 4 |
| clef@openrouter | $0.03 | 25 s (estimated, 210 calls) | 20 min | 4 |
| d1-ultra@openrouter | $0.0046 | 2 min (estimated, 210 calls) | 72 min | 4 |
| d1.1@openrouter | $0.0022 | 12 s (estimated, 210 calls) | 10 min | 4 |
| d1.2 | $0.0022 | 8 s (estimated, 210 calls) | 6 min | 4 |
| d1.2-ultra | $0.0046 | 7 s (estimated, 210 calls) | 6 min | 4 |
| decider-1.3@vercel | $0.0023 | 19 s (estimated, 210 calls) | 15 min | 4 |
| decider-flash@openrouter | $0.0012 | 7 s (estimated, 210 calls) | 6 min | 4 |
| decider@openrouter | $0.0023 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decision-1.1@openrouter | $0.0048 | 12 s (estimated, 210 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0044 | 13 s (estimated, 210 calls) | 10 min | 4 |
| drex-max-1.1@vercel | $0.0036 | 21 s (estimated, 210 calls) | 16 min | 4 |
| drex-max@openrouter | $0.0070 | 14 s (estimated, 210 calls) | 11 min | 4 |
| elephant@openrouter | $0.0041 | 10 s (estimated, 210 calls) | 8 min | 4 |
| gemini-decision@google | $0.01 | 15 s (estimated, 210 calls) | 12 min | 4 |
| groundhog@openrouter | $0.0044 | 25 s (estimated, 210 calls) | 20 min | 2 |
| heygen-decision@openrouter | $0.01 | 17 s (estimated, 210 calls) | 14 min | 4 |
| jev:1.14 | $0.0068 | 6 s (estimated, 210 calls) | 4 min | 4 |
| joey@openrouter | $0.0012 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0042 | 30 s (estimated, 210 calls) | 24 min | 4 |
| luna@decisions | $0.01 | 12 s (estimated, 210 calls) | 9 min | 4 |
| mammoth@openrouter | $0.01 | 10 s (estimated, 210 calls) | 8 min | 4 |
| mo@vercel | $0.0049 | 19 s (estimated, 210 calls) | 15 min | 4 |
| reflex@openrouter | $0.0049 | 14 s (estimated, 210 calls) | 11 min | 4 |
| span@openrouter | $0.0013 | 29 s (estimated, 210 calls) | 23 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

[ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| bison@openrouter | 75.2% | 77.6% | 33 | 14 | 0.70 | 0.70 |
| clef-flash@openrouter | 77.1% | 80.5% | 34 | 7 | 0.85 | 0.85 |
| clef-omni@openrouter | 78.1% | 80.0% | 33 | 9 | 0.80 | 0.80 |
| clef@openrouter | 77.1% | 79.5% | 38 | 5 | 0.85 | 0.85 |
| d1-ultra@openrouter | 75.2% | 78.6% | 35 | 10 | 0.95 | 0.95 |
| d1.1@openrouter | 71.9% | 79.5% | 33 | 10 | 0.95 | 0.95 |
| d1.2 | 74.3% | 79.5% | 34 | 9 | 0.90 | 0.90 |
| d1.2-ultra | 75.7% | 78.6% | 33 | 12 | 0.90 | 0.90 |
| decider-1.3@vercel | 78.1% | 79.5% | 32 | 11 | 0.95 | 0.95 |
| decider-flash@openrouter | 78.6% | 80.0% | 34 | 8 | 0.80 | 0.80 |
| decider@openrouter | 77.6% | 79.5% | 32 | 11 | 0.90 | 0.90 |
| decision-1.1@openrouter | 71.9% | 77.1% | 30 | 18 | 0.85 | 0.85 |
| decision-1@openrouter | 71.4% | 78.1% | 32 | 14 | 0.95 | 0.95 |
| drex-max-1.1@vercel | 78.1% | 81.0% | 36 | 4 | 0.95 | 0.95 |
| drex-max@openrouter | 75.2% | 78.1% | 31 | 15 | 0.90 | 0.90 |
| elephant@openrouter | 72.4% | 80.5% | 38 | 3 | 0.95 | 0.95 |
| gemini-decision@google | 73.8% | 78.1% | 34 | 12 | 0.95 | 0.95 |
| groundhog@openrouter | 72.9% | 77.1% | 36 | 12 | 0.90 | 0.90 |
| heygen-decision@openrouter | 74.3% | 79.0% | 38 | 6 | 0.95 | 0.95 |
| jev:1.14 | 71.9% | 76.7% | 34 | 15 | 0.85 | 0.85 |
| joey@openrouter | 80.0% | 80.0% | 34 | 8 | 0.50 | 0.50 |
| kev@openrouter | 78.1% | 78.6% | 41 | 4 | 0.70 | 0.70 |
| luna@decisions | 75.7% | 75.2% | 35 | 17 | 0.90 | 0.95 |
| mammoth@openrouter | 76.7% | 78.1% | 31 | 15 | 0.75 | 0.75 |
| mo@vercel | 77.1% | 78.1% | 31 | 15 | 0.80 | 0.80 |
| reflex@openrouter | 78.1% | 78.6% | 31 | 14 | 0.90 | 0.90 |
| span@openrouter | 76.7% | 78.1% | 36 | 10 | 0.95 | 0.95 |

## Misses and false alarms by threshold (bison@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 20 (44%) | 70 (42%) |
| 0.20 | 25 (56%) | 54 (33%) |
| 0.30 | 27 (60%) | 36 (22%) |
| 0.40 | 27 (60%) | 26 (16%) |
| 0.50 | 29 (64%) | 23 (14%) |
| 0.60 | 31 (69%) | 18 (11%) |
| 0.70 | 32 (71%) | 14 (8%) |
| 0.80 | 32 (71%) | 14 (8%) |
| 0.90 | 36 (80%) | 12 (7%) |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 15 (33%) | 102 (62%) |
| 0.20 | 26 (58%) | 38 (23%) |
| 0.30 | 30 (67%) | 29 (18%) |
| 0.40 | 30 (67%) | 22 (13%) |
| 0.50 | 30 (67%) | 18 (11%) |
| 0.60 | 32 (71%) | 16 (10%) |
| 0.70 | 32 (71%) | 14 (8%) |
| 0.80 | 34 (76%) | 10 (6%) |
| 0.85 | 34 (76%) | 7 (4%) |
| 0.90 | 40 (89%) | 5 (3%) |

## Misses and false alarms by threshold (clef-omni@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 22 (49%) | 55 (33%) |
| 0.20 | 29 (64%) | 31 (19%) |
| 0.30 | 30 (67%) | 25 (15%) |
| 0.40 | 31 (69%) | 19 (12%) |
| 0.50 | 31 (69%) | 15 (9%) |
| 0.60 | 33 (73%) | 12 (7%) |
| 0.70 | 33 (73%) | 11 (7%) |
| 0.80 | 33 (73%) | 9 (5%) |
| 0.90 | 40 (89%) | 7 (4%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 30 (67%) | 38 (23%) |
| 0.20 | 30 (67%) | 23 (14%) |
| 0.30 | 30 (67%) | 21 (13%) |
| 0.40 | 30 (67%) | 17 (10%) |
| 0.50 | 32 (71%) | 16 (10%) |
| 0.60 | 32 (71%) | 13 (8%) |
| 0.70 | 33 (73%) | 10 (6%) |
| 0.80 | 34 (76%) | 8 (5%) |
| 0.85 | 35 (78%) | 6 (4%) |
| 0.90 | 38 (84%) | 5 (3%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 20 (44%) | 74 (45%) |
| 0.20 | 23 (51%) | 53 (32%) |
| 0.30 | 28 (62%) | 36 (22%) |
| 0.40 | 30 (67%) | 30 (18%) |
| 0.50 | 30 (67%) | 22 (13%) |
| 0.60 | 30 (67%) | 20 (12%) |
| 0.70 | 31 (69%) | 16 (10%) |
| 0.80 | 33 (73%) | 14 (8%) |
| 0.90 | 34 (76%) | 13 (8%) |
| 0.95 | 35 (78%) | 8 (5%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (42%) | 71 (43%) |
| 0.20 | 23 (51%) | 58 (35%) |
| 0.30 | 28 (62%) | 44 (27%) |
| 0.40 | 28 (62%) | 38 (23%) |
| 0.50 | 29 (64%) | 30 (18%) |
| 0.60 | 30 (67%) | 26 (16%) |
| 0.70 | 30 (67%) | 18 (11%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 32 (71%) | 14 (8%) |
| 0.95 | 33 (73%) | 10 (6%) |

## Misses and false alarms by threshold (d1.2)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 13 (29%) | 98 (59%) |
| 0.20 | 18 (40%) | 61 (37%) |
| 0.30 | 28 (62%) | 39 (24%) |
| 0.40 | 30 (67%) | 27 (16%) |
| 0.50 | 31 (69%) | 23 (14%) |
| 0.60 | 32 (71%) | 19 (12%) |
| 0.70 | 32 (71%) | 15 (9%) |
| 0.80 | 32 (71%) | 13 (8%) |
| 0.90 | 34 (76%) | 9 (5%) |

## Misses and false alarms by threshold (d1.2-ultra)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (42%) | 81 (49%) |
| 0.20 | 24 (53%) | 57 (35%) |
| 0.30 | 25 (56%) | 39 (24%) |
| 0.40 | 29 (64%) | 27 (16%) |
| 0.50 | 30 (67%) | 21 (13%) |
| 0.60 | 30 (67%) | 19 (12%) |
| 0.70 | 31 (69%) | 15 (9%) |
| 0.80 | 32 (71%) | 14 (8%) |
| 0.90 | 32 (71%) | 12 (7%) |

## Misses and false alarms by threshold (decider-1.3@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 28 (62%) | 34 (21%) |
| 0.20 | 28 (62%) | 27 (16%) |
| 0.30 | 29 (64%) | 20 (12%) |
| 0.40 | 30 (67%) | 18 (11%) |
| 0.50 | 30 (67%) | 16 (10%) |
| 0.60 | 30 (67%) | 16 (10%) |
| 0.70 | 30 (67%) | 15 (9%) |
| 0.80 | 31 (69%) | 15 (9%) |
| 0.90 | 31 (69%) | 14 (8%) |
| 0.95 | 32 (71%) | 11 (7%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (58%) | 46 (28%) |
| 0.20 | 30 (67%) | 25 (15%) |
| 0.30 | 31 (69%) | 19 (12%) |
| 0.40 | 32 (71%) | 15 (9%) |
| 0.50 | 33 (73%) | 12 (7%) |
| 0.60 | 33 (73%) | 12 (7%) |
| 0.70 | 33 (73%) | 11 (7%) |
| 0.80 | 34 (76%) | 6 (4%) |
| 0.90 | 38 (84%) | 5 (3%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (58%) | 48 (29%) |
| 0.20 | 28 (62%) | 32 (19%) |
| 0.30 | 30 (67%) | 22 (13%) |
| 0.40 | 30 (67%) | 18 (11%) |
| 0.50 | 30 (67%) | 17 (10%) |
| 0.60 | 31 (69%) | 15 (9%) |
| 0.70 | 31 (69%) | 15 (9%) |
| 0.80 | 31 (69%) | 15 (9%) |
| 0.90 | 32 (71%) | 11 (7%) |

## Misses and false alarms by threshold (decision-1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 23 (51%) | 58 (35%) |
| 0.20 | 25 (56%) | 44 (27%) |
| 0.30 | 27 (60%) | 38 (23%) |
| 0.40 | 28 (62%) | 36 (22%) |
| 0.50 | 29 (64%) | 30 (18%) |
| 0.60 | 29 (64%) | 26 (16%) |
| 0.70 | 29 (64%) | 22 (13%) |
| 0.80 | 29 (64%) | 21 (13%) |
| 0.85 | 29 (64%) | 18 (11%) |
| 0.90 | 30 (67%) | 18 (11%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 27 (60%) | 59 (36%) |
| 0.20 | 28 (62%) | 49 (30%) |
| 0.30 | 29 (64%) | 43 (26%) |
| 0.40 | 29 (64%) | 38 (23%) |
| 0.50 | 29 (64%) | 31 (19%) |
| 0.60 | 29 (64%) | 27 (16%) |
| 0.70 | 29 (64%) | 26 (16%) |
| 0.80 | 31 (69%) | 23 (14%) |
| 0.90 | 31 (69%) | 19 (12%) |
| 0.95 | 32 (71%) | 14 (8%) |

## Misses and false alarms by threshold (drex-max-1.1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (56%) | 48 (29%) |
| 0.20 | 29 (64%) | 30 (18%) |
| 0.30 | 30 (67%) | 23 (14%) |
| 0.40 | 30 (67%) | 18 (11%) |
| 0.50 | 31 (69%) | 15 (9%) |
| 0.60 | 31 (69%) | 15 (9%) |
| 0.70 | 31 (69%) | 15 (9%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 34 (76%) | 10 (6%) |
| 0.95 | 36 (80%) | 4 (2%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (56%) | 52 (32%) |
| 0.20 | 29 (64%) | 37 (22%) |
| 0.30 | 30 (67%) | 27 (16%) |
| 0.40 | 30 (67%) | 24 (15%) |
| 0.50 | 30 (67%) | 22 (13%) |
| 0.60 | 30 (67%) | 17 (10%) |
| 0.70 | 31 (69%) | 16 (10%) |
| 0.80 | 31 (69%) | 16 (10%) |
| 0.90 | 31 (69%) | 14 (8%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (42%) | 87 (53%) |
| 0.20 | 26 (58%) | 64 (39%) |
| 0.30 | 27 (60%) | 47 (28%) |
| 0.40 | 29 (64%) | 36 (22%) |
| 0.50 | 30 (67%) | 28 (17%) |
| 0.60 | 30 (67%) | 23 (14%) |
| 0.70 | 30 (67%) | 15 (9%) |
| 0.80 | 34 (76%) | 13 (8%) |
| 0.90 | 36 (80%) | 11 (7%) |
| 0.95 | 38 (84%) | 3 (2%) |

## Misses and false alarms by threshold (gemini-decision@google)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 21 (47%) | 68 (41%) |
| 0.20 | 26 (58%) | 57 (35%) |
| 0.30 | 27 (60%) | 41 (25%) |
| 0.40 | 29 (64%) | 30 (18%) |
| 0.50 | 30 (67%) | 25 (15%) |
| 0.60 | 30 (67%) | 21 (13%) |
| 0.70 | 30 (67%) | 20 (12%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 33 (73%) | 12 (7%) |
| 0.95 | 34 (76%) | 10 (6%) |

## Misses and false alarms by threshold (groundhog@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 11 (24%) | 91 (55%) |
| 0.20 | 20 (44%) | 67 (41%) |
| 0.30 | 26 (58%) | 47 (28%) |
| 0.40 | 27 (60%) | 34 (21%) |
| 0.50 | 28 (62%) | 29 (18%) |
| 0.60 | 29 (64%) | 19 (12%) |
| 0.70 | 31 (69%) | 17 (10%) |
| 0.80 | 32 (71%) | 13 (8%) |
| 0.90 | 33 (73%) | 10 (6%) |

## Misses and false alarms by threshold (heygen-decision@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (56%) | 60 (36%) |
| 0.20 | 26 (58%) | 45 (27%) |
| 0.30 | 26 (58%) | 35 (21%) |
| 0.40 | 29 (64%) | 30 (18%) |
| 0.50 | 29 (64%) | 25 (15%) |
| 0.60 | 30 (67%) | 19 (12%) |
| 0.70 | 30 (67%) | 17 (10%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 33 (73%) | 11 (7%) |
| 0.95 | 39 (87%) | 3 (2%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 8 (18%) | 120 (73%) |
| 0.20 | 22 (49%) | 69 (42%) |
| 0.30 | 28 (62%) | 47 (28%) |
| 0.40 | 28 (62%) | 35 (21%) |
| 0.50 | 30 (67%) | 29 (18%) |
| 0.60 | 30 (67%) | 23 (14%) |
| 0.70 | 30 (67%) | 19 (12%) |
| 0.80 | 31 (69%) | 15 (9%) |
| 0.85 | 31 (69%) | 14 (8%) |
| 0.90 | 31 (69%) | 14 (8%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (4%) | 156 (95%) |
| 0.20 | 20 (44%) | 74 (45%) |
| 0.30 | 27 (60%) | 44 (27%) |
| 0.40 | 31 (69%) | 23 (14%) |
| 0.50 | 34 (76%) | 8 (5%) |
| 0.60 | 42 (93%) | 4 (2%) |
| 0.70 | 44 (98%) | 1 (1%) |
| 0.80 | 45 (100%) | 0 (0%) |
| 0.90 | 45 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 6 (13%) | 146 (88%) |
| 0.20 | 24 (53%) | 59 (36%) |
| 0.30 | 29 (64%) | 29 (18%) |
| 0.40 | 31 (69%) | 17 (10%) |
| 0.50 | 35 (78%) | 11 (7%) |
| 0.60 | 38 (84%) | 8 (5%) |
| 0.70 | 39 (87%) | 4 (2%) |
| 0.80 | 42 (93%) | 1 (1%) |
| 0.90 | 44 (98%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 22 (49%) | 66 (40%) |
| 0.20 | 30 (67%) | 37 (22%) |
| 0.30 | 30 (67%) | 26 (16%) |
| 0.40 | 30 (67%) | 23 (14%) |
| 0.50 | 30 (67%) | 21 (13%) |
| 0.60 | 30 (67%) | 21 (13%) |
| 0.70 | 30 (67%) | 17 (10%) |
| 0.80 | 32 (71%) | 15 (9%) |
| 0.90 | 33 (73%) | 13 (8%) |
| 0.95 | 36 (80%) | 9 (5%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 20 (44%) | 63 (38%) |
| 0.20 | 27 (60%) | 45 (27%) |
| 0.30 | 28 (62%) | 29 (18%) |
| 0.40 | 29 (64%) | 22 (13%) |
| 0.50 | 30 (67%) | 19 (12%) |
| 0.60 | 30 (67%) | 15 (9%) |
| 0.70 | 31 (69%) | 14 (8%) |
| 0.75 | 31 (69%) | 13 (8%) |
| 0.80 | 31 (69%) | 13 (8%) |
| 0.90 | 32 (71%) | 13 (8%) |

## Misses and false alarms by threshold (mo@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 28 (62%) | 44 (27%) |
| 0.20 | 28 (62%) | 29 (18%) |
| 0.30 | 30 (67%) | 21 (13%) |
| 0.40 | 30 (67%) | 18 (11%) |
| 0.50 | 30 (67%) | 18 (11%) |
| 0.60 | 30 (67%) | 18 (11%) |
| 0.70 | 31 (69%) | 15 (9%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 32 (71%) | 14 (8%) |

## Misses and false alarms by threshold (reflex@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 28 (62%) | 36 (22%) |
| 0.20 | 28 (62%) | 23 (14%) |
| 0.30 | 30 (67%) | 21 (13%) |
| 0.40 | 30 (67%) | 19 (12%) |
| 0.50 | 30 (67%) | 16 (10%) |
| 0.60 | 30 (67%) | 16 (10%) |
| 0.70 | 30 (67%) | 14 (8%) |
| 0.80 | 31 (69%) | 14 (8%) |
| 0.90 | 31 (69%) | 12 (7%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 27 (60%) | 38 (23%) |
| 0.20 | 29 (64%) | 29 (18%) |
| 0.30 | 29 (64%) | 26 (16%) |
| 0.40 | 29 (64%) | 23 (14%) |
| 0.50 | 30 (67%) | 19 (12%) |
| 0.60 | 31 (69%) | 17 (10%) |
| 0.70 | 32 (71%) | 13 (8%) |
| 0.80 | 33 (73%) | 11 (7%) |
| 0.90 | 34 (76%) | 9 (5%) |
| 0.95 | 37 (82%) | 5 (3%) |

## Wrong at a high probability (0.9 or more)

**bison@openrouter** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29100 | False | True | 0.98 | Gemini lolo |
| #29290 | True | False | 0.98 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29392 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #28783 | False | True | 0.96 | cutealexamartha |
| #29390 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29388 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29316 | True | False | 0.96 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |

**clef-flash@openrouter** (20)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28761 | True | False | 0.93 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29290 | True | False | 0.93 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29424 | True | False | 0.92 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29144 | True | False | 0.92 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29220 | False | True | 0.92 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #28783 | False | True | 0.92 | cutealexamartha |
| #29311 | True | False | 0.92 | bug(core): insecure user/workspace policy dirs skip permission checks… |
| #29309 | True | False | 0.92 | bug(core): unbounded _execute recursion on sandbox_expansion_required… |

**clef-omni@openrouter** (29)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 0.97 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29424 | True | False | 0.97 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29146 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #28761 | True | False | 0.97 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #28846 | True | False | 0.96 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29204 | True | False | 0.96 | MCP prompt responses are submitted as JSON-encoded text |
| #29317 | True | False | 0.96 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |

**clef@openrouter** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28846 | True | False | 0.98 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29316 | True | False | 0.98 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29424 | True | False | 0.98 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #28761 | True | False | 0.97 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29308 | True | False | 0.97 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29012 | True | False | 0.97 | Docs: six CLI flags missing from the reference table |

**d1-ultra@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29317 | True | False | 0.99 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #28783 | False | True | 0.99 | cutealexamartha |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29100 | False | True | 0.99 | Gemini lolo |
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29392 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29309 | True | False | 0.99 | bug(core): unbounded _execute recursion on sandbox_expansion_required… |

**d1.1@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.99 | Gemini lolo |
| #28783 | False | True | 0.99 | cutealexamartha |
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29012 | True | False | 0.99 | Docs: six CLI flags missing from the reference table |
| #29204 | True | False | 0.99 | MCP prompt responses are submitted as JSON-encoded text |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |

**d1.2** (22)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29100 | False | True | 0.98 | Gemini lolo |
| #29146 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29147 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29316 | True | False | 0.97 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #28783 | False | True | 0.97 | cutealexamartha |
| #29392 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29012 | True | False | 0.96 | Docs: six CLI flags missing from the reference table |

**d1.2-ultra** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29204 | True | False | 0.99 | MCP prompt responses are submitted as JSON-encoded text |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29012 | True | False | 0.99 | Docs: six CLI flags missing from the reference table |
| #29046 | True | False | 0.99 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29316 | True | False | 0.98 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29308 | True | False | 0.98 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29290 | True | False | 0.98 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |

**decider-1.3@vercel** (42)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29317 | True | False | 1.00 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29314 | True | False | 1.00 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |

**decider-flash@openrouter** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.99 | Gemini lolo |
| #28783 | False | True | 0.98 | cutealexamartha |
| #28846 | True | False | 0.97 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29424 | True | False | 0.97 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29144 | True | False | 0.97 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29012 | True | False | 0.97 | Docs: six CLI flags missing from the reference table |

**decider@openrouter** (37)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29046 | True | False | 0.99 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29424 | True | False | 0.99 | bug: Node process hangs on session exit, preventing terminal from ret… |

**decision-1.1@openrouter** (41)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29100 | False | True | 1.00 | Gemini lolo |
| #28783 | False | True | 1.00 | cutealexamartha |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29220 | False | True | 1.00 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |

**decision-1@openrouter** (46)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 1.00 | Gemini lolo |
| #28783 | False | True | 1.00 | cutealexamartha |
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29221 | False | True | 1.00 | Leeres.blaat_A4-DIN |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |

**drex-max-1.1@vercel** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29046 | True | False | 0.99 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29305 | True | False | 0.99 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29144 | True | False | 0.99 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29290 | True | False | 0.99 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29311 | True | False | 0.99 | bug(core): insecure user/workspace policy dirs skip permission checks… |

**drex-max@openrouter** (39)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29392 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29100 | False | True | 1.00 | Gemini lolo |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29388 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29390 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |

**elephant@openrouter** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29146 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29147 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28846 | True | False | 0.99 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29290 | True | False | 0.99 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29316 | True | False | 0.97 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29100 | False | True | 0.97 | Gemini lolo |
| #29012 | True | False | 0.97 | Docs: six CLI flags missing from the reference table |

**gemini-decision@google** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29100 | False | True | 0.99 | Gemini lolo |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29305 | True | False | 0.98 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29317 | True | False | 0.98 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29046 | True | False | 0.98 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29012 | True | False | 0.98 | Docs: six CLI flags missing from the reference table |

**groundhog@openrouter** (21)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29146 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #28783 | False | True | 0.98 | cutealexamartha |
| #29100 | False | True | 0.98 | Gemini lolo |
| #29111 | False | True | 0.97 | ejecucion lenta |
| #29012 | True | False | 0.96 | Docs: six CLI flags missing from the reference table |
| #29147 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] |
| #29355 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] |

**heygen-decision@openrouter** (36)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28783 | False | True | 0.98 | cutealexamartha |
| #29012 | True | False | 0.98 | Docs: six CLI flags missing from the reference table |
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29305 | True | False | 0.98 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29424 | True | False | 0.97 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29100 | False | True | 0.97 | Gemini lolo |
| #29314 | True | False | 0.97 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |

**jev:1.14** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29228 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29355 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.97 | Gemini lolo |
| #29220 | False | True | 0.97 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #29146 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #28783 | False | True | 0.97 | cutealexamartha |
| #29392 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |

**joey@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29415 | True | False | 0.92 | gemini --help exits with code 5 after winget install on Windows 11 |
| #29305 | True | False | 0.91 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |

**kev@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | True | False | 0.93 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29012 | True | False | 0.93 | Docs: six CLI flags missing from the reference table |
| #29001 | True | False | 0.92 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29144 | True | False | 0.91 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29317 | True | False | 0.91 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29308 | True | False | 0.91 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |

**luna@decisions** (35)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29305 | True | False | 1.00 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29221 | False | True | 1.00 | Leeres.blaat_A4-DIN |
| #29220 | False | True | 0.99 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |

**mammoth@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29207 | True | False | 0.99 | Corrupt agents.json (valid JSON, wrong shape) crashes acknowledgment |
| #29392 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29316 | True | False | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29305 | True | False | 0.99 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29314 | True | False | 0.99 | bug(cli): ShellProcessor ignores abort signal, hung custom command bl… |
| #29046 | True | False | 0.99 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |

**mo@vercel** (42)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29392 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29202 | True | False | 1.00 | Policy bypass: shell-wrapper flags skip inner command re-check |
| #29308 | True | False | 0.99 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |

**reflex@openrouter** (40)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29355 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29388 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |

**span@openrouter** (36)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29424 | True | False | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29305 | True | False | 1.00 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |


## Cases the models disagree on (12 of 51)

| id | label | bison@openrouter | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | decider-1.3@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max-1.1@vercel | drex-max@openrouter | elephant@openrouter | gemini-decision@google | groundhog@openrouter | heygen-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mo@vercel | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #29442 | False | False (0.90) | False (0.88) | False (0.87) | False (0.95) | False (0.94) | False (0.58) | False (0.79) | False (0.78) | False (0.98) | False (0.95) | False (0.94) | False (0.56) | True (0.80) | False (0.93) | False (0.84) | True (0.56) | False (0.91) | False (0.68) | False (0.85) | False (0.80) | False (0.74) | False (0.82) | False (1.00) | False (0.90) | False (0.87) | False (0.98) | False (0.95) | Create a kitten illustration with a lion-shaped shadow |
| #29221 | False | True (0.93) | True (0.87) | True (0.79) | True (0.78) | True (0.91) | True (0.97) | True (0.94) | True (0.95) | True (0.96) | True (0.79) | True (0.96) | True (1.00) | True (1.00) | True (0.92) | True (0.98) | True (0.79) | True (0.97) | True (0.95) | True (0.91) | True (0.93) | False (0.56) | False (0.54) | True (1.00) | True (0.96) | True (0.99) | True (0.98) | True (0.88) | Leeres.blaat_A4-DIN |
| #28686 | False | False (0.87) | False (0.88) | False (0.83) | False (0.94) | False (0.88) | True (0.63) | True (0.65) | False (0.77) | False (1.00) | False (0.96) | False (0.93) | False (0.77) | False (0.68) | False (0.96) | False (0.96) | False (0.58) | False (0.67) | False (0.84) | False (0.93) | False (0.80) | False (0.76) | False (0.85) | False (1.00) | False (0.88) | False (0.97) | False (0.99) | False (0.83) | ## Code Review |
| #29135 | True | True (0.89) | True (0.85) | True (0.60) | False (0.52) | True (0.77) | True (0.97) | True (0.91) | True (0.95) | True (0.97) | True (0.94) | True (0.96) | True (1.00) | True (1.00) | True (0.87) | True (0.92) | True (0.78) | True (0.90) | True (0.88) | True (0.93) | True (0.90) | True (0.58) | False (0.51) | True (0.73) | True (0.95) | True (0.96) | True (0.93) | False (0.59) | Features |
| #28783 | False | True (0.96) | True (0.92) | True (0.95) | True (0.81) | True (0.99) | True (0.99) | True (0.97) | True (0.97) | True (0.93) | True (0.98) | True (0.98) | True (1.00) | True (1.00) | True (0.93) | True (0.99) | True (0.93) | True (0.98) | True (0.98) | True (0.98) | True (0.97) | False (0.56) | True (0.51) | True (0.97) | True (0.97) | True (0.99) | True (0.99) | True (0.90) | cutealexamartha |
| #29136 | True | True (0.90) | True (0.88) | True (0.83) | True (0.89) | True (0.99) | True (0.99) | True (0.96) | True (0.96) | True (0.99) | True (0.92) | True (0.96) | True (1.00) | True (1.00) | True (0.92) | True (0.97) | True (0.93) | True (0.98) | True (0.98) | True (0.95) | True (0.98) | False (0.59) | True (0.52) | True (0.98) | True (0.95) | True (0.98) | True (1.00) | True (0.99) | GeminiCLI.com Feedback: [ISSUE] |
| #29224 | True | True (0.90) | True (0.76) | True (0.83) | True (0.62) | True (0.98) | True (0.98) | True (0.96) | True (0.98) | True (0.99) | True (0.86) | True (0.97) | True (1.00) | True (1.00) | True (0.96) | True (0.97) | True (0.79) | True (0.98) | True (0.94) | True (0.89) | True (0.94) | False (0.53) | False (0.65) | True (0.70) | True (0.96) | True (0.91) | True (0.98) | True (0.70) | npm install -g @google/gemini-cli@preview |
| #29145 | True | True (0.95) | True (0.88) | True (0.94) | True (0.94) | True (0.98) | True (1.00) | True (0.97) | True (0.95) | True (1.00) | True (0.94) | True (1.00) | True (1.00) | True (1.00) | True (0.97) | True (1.00) | True (0.97) | True (0.98) | True (0.97) | True (0.97) | True (0.97) | True (0.71) | False (0.52) | True (0.99) | True (0.95) | True (1.00) | True (1.00) | True (0.99) | Recalibrate trick |
| #28923 | True | True (0.90) | True (0.91) | True (0.86) | True (0.90) | True (0.86) | True (0.96) | True (0.90) | True (0.98) | True (0.99) | True (0.71) | True (0.99) | True (1.00) | True (1.00) | True (0.98) | True (0.99) | True (0.91) | True (0.92) | True (0.96) | True (0.94) | True (0.96) | False (0.63) | True (0.71) | True (0.96) | True (0.96) | True (0.99) | True (1.00) | True (0.95) | GeminiCLI.com Feedback: [ISSUE] |
| #29392 | False | True (0.97) | True (0.84) | True (0.80) | True (0.75) | True (0.99) | True (0.98) | True (0.96) | True (0.98) | True (0.99) | True (0.91) | True (0.98) | True (1.00) | True (1.00) | True (0.96) | True (1.00) | True (0.95) | True (0.97) | True (0.87) | True (0.93) | True (0.96) | False (0.56) | True (0.66) | True (0.91) | True (0.99) | True (1.00) | True (1.00) | True (0.81) | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #28777 | True | True (0.88) | True (0.79) | True (0.87) | True (0.88) | True (0.98) | True (0.96) | True (0.89) | True (0.95) | True (1.00) | False (0.66) | True (0.97) | True (1.00) | True (1.00) | True (0.93) | True (0.98) | True (0.89) | True (0.97) | True (0.91) | True (0.88) | True (0.95) | True (0.59) | False (0.56) | True (0.89) | True (0.91) | True (0.98) | True (0.99) | True (0.92) | ticket IT support |
| #29390 | False | True (0.96) | True (0.77) | True (0.59) | True (0.66) | True (0.98) | True (0.91) | True (0.86) | True (0.95) | True (0.99) | True (0.73) | True (0.98) | True (1.00) | True (1.00) | True (0.95) | True (1.00) | True (0.93) | True (0.91) | True (0.89) | True (0.92) | True (0.95) | False (0.59) | False (0.66) | True (0.88) | True (0.96) | True (0.99) | True (1.00) | False (0.53) | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
