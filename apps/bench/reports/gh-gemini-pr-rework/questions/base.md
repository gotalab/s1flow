# gh-gemini-pr-rework

2026-11-23 · 338 labelled dev cases (False 247, True 91) · split: stratified k-fold (no test case among these: CV numbers only) · source: Merged PRs of google-gemini/gemini-cli (review history via the GitHub API)

mammoth@openrouter has the highest AUROC, 0.733 [0.671, 0.790] (API cost $0.61 per 10k, p99 488ms). Its interval overlaps with decider-1.3@vercel, clef-omni@openrouter, heygen-decision@openrouter, drex-max-1.1@vercel, bison@openrouter, reflex@openrouter, decider@openrouter, drex-max@openrouter, mo@vercel, joey@openrouter, span@openrouter, decider-flash@openrouter, groundhog@openrouter, clef-flash@openrouter, kev@openrouter, d1-ultra@openrouter, elephant@openrouter, d1.2-ultra, jev:1.14, gemini-decision@google, d1.1@openrouter, clef@openrouter, d1.2, luna@decisions, decision-1.1@openrouter, decision-1@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. Ordered by task.py's tiebreak (loss per case (miss 1, false alarm 1)), decider-1.3@vercel comes first (API cost $0.12 per 10k, p99 1418ms). The highest raw accuracy (dev) is clef-omni@openrouter's, 76% [72, 81].

## Comparison

| model | scored | accuracy (all) | F1 | AUROC | ECE | refused | failed |
|---|---|---|---|---|---|---|---|
| bison@openrouter | 338 | 75.1% [70, 80] | 0.39 | 0.69 | 0.04 | 0.0% (0/338) | 0/338 |
| clef-flash@openrouter | 338 | 73.4% [68, 78] | 0.12 | 0.69 | 0.13 | 0.0% (0/338) | 0/338 |
| clef-omni@openrouter | 338 | 76.3% [72, 81] | 0.31 | 0.71 | 0.13 | 0.0% (0/338) | 0/338 |
| clef@openrouter | 338 | 69.5% [64, 75] | 0.44 | 0.71 | 0.07 | 0.0% (0/338) | 0/338 |
| d1-ultra@openrouter | 338 | 72.8% [68, 78] | 0.47 | 0.71 | 0.08 | 0.0% (0/338) | 0/338 |
| d1.1@openrouter | 338 | 70.7% [66, 76] | 0.44 | 0.71 | 0.11 | 0.0% (0/338) | 0/338 |
| d1.2 | 338 | 69.2% [64, 74] | 0.40 | 0.70 | 0.07 | 0.0% (0/338) | 0/338 |
| d1.2-ultra | 338 | 72.2% [67, 77] | 0.45 | 0.71 | 0.05 | 0.0% (0/338) | 0/338 |
| decider-1.3@vercel | 338 | 76.3% [72, 81] | 0.39 | 0.71 | 0.13 | 0.0% (0/338) | 0/338 |
| decider-flash@openrouter | 338 | 73.7% [69, 78] | 0.08 | 0.68 | 0.07 | 0.0% (0/338) | 0/338 |
| decider@openrouter | 338 | 74.6% [70, 79] | 0.27 | 0.70 | 0.09 | 0.0% (0/338) | 0/338 |
| decision-1.1@openrouter | 338 | 69.2% [64, 74] | 0.44 | 0.70 | 0.18 | 0.0% (0/338) | 0/338 |
| decision-1@openrouter | 338 | 62.4% [57, 67] | 0.49 | 0.69 | 0.15 | 0.0% (0/338) | 0/338 |
| drex-max-1.1@vercel | 338 | 75.1% [70, 80] | 0.36 | 0.71 | 0.07 | 0.0% (0/338) | 0/338 |
| drex-max@openrouter | 338 | 74.6% [69, 79] | 0.37 | 0.68 | 0.12 | 0.0% (0/338) | 0/338 |
| elephant@openrouter | 338 | 72.5% [68, 78] | 0.44 | 0.69 | 0.06 | 0.0% (0/338) | 0/338 |
| gemini-decision@google | 338 | 71.6% [67, 76] | 0.48 | 0.68 | 0.05 | 0.0% (0/338) | 0/338 |
| groundhog@openrouter | 338 | 73.4% [68, 78] | 0.48 | 0.71 | 0.04 | 0.0% (0/338) | 0/338 |
| heygen-decision@openrouter | 338 | 75.4% [70, 80] | 0.42 | 0.70 | 0.11 | 0.0% (0/338) | 0/338 |
| jev:1.14 | 338 | 71.9% [67, 76] | 0.48 | 0.72 | 0.07 | 0.0% (0/338) | 0/338 |
| joey@openrouter | 338 | 74.0% [69, 78] | 0.27 | 0.70 | 0.04 | 0.0% (0/338) | 0/338 |
| kev@openrouter | 338 | 73.4% [68, 78] | 0.06 | 0.64 | 0.01 | 0.0% (0/338) | 0/338 |
| luna@decisions | 338 | 69.2% [64, 75] | 0.47 | 0.70 | 0.04 | 0.0% (0/338) | 0/338 |
| mammoth@openrouter | 338 | 70.4% [65, 75] | 0.50 | 0.73 | 0.04 | 0.0% (0/338) | 0/338 |
| mo@vercel | 338 | 74.6% [70, 79] | 0.38 | 0.68 | 0.10 | 0.0% (0/338) | 0/338 |
| reflex@openrouter | 338 | 74.9% [70, 80] | 0.37 | 0.73 | 0.14 | 0.0% (0/338) | 0/338 |
| span@openrouter | 338 | 73.7% [69, 78] | 0.33 | 0.70 | 0.18 | 0.0% (0/338) | 0/338 |

Answered by: bison@openrouter = baseten/bison-1-20261120; clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; decider-1.3@vercel = perplexity/pplx-decider-v1.3; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max-1.1@vercel = nace-ai/drex-max-v1.1; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; groundhog@openrouter = baseten/groundhog-1-20261120; heygen-decision@openrouter = heygen/heygen-decision-1-20261112; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mo@vercel = modaic/mo; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | AUROC | loss per case (miss 1, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| decider-1.3@vercel = | 0.713 [0.646, 0.774] | 0.237 [0.192, 0.284] | — | met |
| clef-omni@openrouter = | 0.712 [0.648, 0.770] | 0.237 [0.192, 0.284] | — | met |
| heygen-decision@openrouter = | 0.696 [0.627, 0.759] | 0.246 [0.201, 0.296] | — | met |
| drex-max-1.1@vercel = | 0.713 [0.646, 0.775] | 0.249 [0.201, 0.296] | — | met |
| bison@openrouter = | 0.692 [0.623, 0.754] | 0.249 [0.204, 0.296] | — | met |
| reflex@openrouter = | 0.727 [0.663, 0.785] | 0.251 [0.204, 0.302] | — | met |
| decider@openrouter = | 0.702 [0.635, 0.763] | 0.254 [0.210, 0.302] | — | met |
| drex-max@openrouter = | 0.684 [0.609, 0.748] | 0.254 [0.210, 0.308] | — | met |
| mo@vercel = | 0.675 [0.606, 0.738] | 0.254 [0.207, 0.305] | — | met |
| joey@openrouter = | 0.700 [0.636, 0.762] | 0.260 [0.216, 0.308] | — | met |
| span@openrouter = | 0.696 [0.633, 0.757] | 0.263 [0.216, 0.311] | — | met |
| decider-flash@openrouter = | 0.676 [0.612, 0.737] | 0.263 [0.219, 0.314] | — | met |
| groundhog@openrouter = | 0.714 [0.649, 0.774] | 0.266 [0.219, 0.317] | — | met |
| clef-flash@openrouter = | 0.687 [0.619, 0.750] | 0.266 [0.222, 0.317] | — | met |
| kev@openrouter = | 0.642 [0.573, 0.708] | 0.266 [0.219, 0.317] | — | met |
| d1-ultra@openrouter = | 0.710 [0.651, 0.764] | 0.272 [0.225, 0.322] | — | met |
| elephant@openrouter = | 0.685 [0.619, 0.745] | 0.275 [0.225, 0.322] | — | met |
| d1.2-ultra = | 0.714 [0.648, 0.775] | 0.278 [0.228, 0.328] | — | met |
| jev:1.14 = | 0.715 [0.655, 0.776] | 0.281 [0.237, 0.328] | — | met |
| gemini-decision@google = | 0.681 [0.614, 0.744] | 0.284 [0.237, 0.331] | — | met |
| d1.1@openrouter = | 0.710 [0.647, 0.769] | 0.293 [0.243, 0.340] | — | met |
| mammoth@openrouter = | 0.733 [0.671, 0.790] | 0.296 [0.248, 0.349] | — | met |
| clef@openrouter = | 0.708 [0.643, 0.766] | 0.305 [0.254, 0.358] | — | met |
| d1.2 = | 0.703 [0.639, 0.763] | 0.308 [0.257, 0.358] | — | met |
| luna@decisions = | 0.702 [0.631, 0.765] | 0.308 [0.254, 0.361] | — | met |
| decision-1.1@openrouter = | 0.697 [0.629, 0.757] | 0.308 [0.257, 0.355] | — | met |
| decision-1@openrouter = | 0.692 [0.623, 0.756] | 0.376 [0.325, 0.429] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bison@openrouter | 338 | 245 ms | 285 ms | 527 ms | 588 ms | 2.2 | 0 | 2 | $0.68 | billed |  |
| clef-flash@openrouter | 338 | 274 ms | 389 ms | 792 ms | 1450 ms | 2.9 | 0 | 4 | $0.16 | billed |  |
| clef-omni@openrouter | 338 | 182 ms | 243 ms | 346 ms | 1041 ms | 1.9 | 0 | 4 | $0.95 | billed |  |
| clef@openrouter | 338 | 259 ms | 367 ms | 682 ms | 1064 ms | 2.6 | 0 | 4 | $1.39 | billed |  |
| d1-ultra@openrouter | 338 | 522 ms | 5589 ms | 6151 ms | 8675 ms | 11.8 | 21 | 4 | $0.25 | billed |  |
| d1.1@openrouter | 338 | 325 ms | 533 ms | 798 ms | 838 ms | 2.5 | 0 | 4 | $0.12 | billed | ○ |
| d1.2 | 338 | 117 ms | 166 ms | 396 ms | 469 ms | 3.4 | 0 | 4 | $0.12 | billed | ○ |
| d1.2-ultra | 338 | 126 ms | 191 ms | 408 ms | 555 ms | 3.2 | 1 | 4 | $0.25 | billed | ○ |
| decider-1.3@vercel | 338 | 358 ms | 551 ms | 1418 ms | 2043 ms | 4.0 | 0 | 4 | $0.12 | billed | ○ |
| decider-flash@openrouter | 338 | 141 ms | 258 ms | 421 ms | 1852 ms | 3.0 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 338 | 226 ms | 331 ms | 773 ms | 1135 ms | 3.4 | 0 | 4 | $0.12 | billed |  |
| decision-1.1@openrouter | 338 | 231 ms | 294 ms | 644 ms | 820 ms | 2.8 | 0 | 4 | $0.27 | billed |  |
| decision-1@openrouter | 338 | 251 ms | 316 ms | 450 ms | 2035 ms | 1.8 | 0 | 4 | $0.23 | billed |  |
| drex-max-1.1@vercel | 338 | 357 ms | 482 ms | 819 ms | 1014 ms | 2.3 | 0 | 4 | $0.19 | billed | ○ |
| drex-max@openrouter | 338 | 394 ms | 663 ms | 1149 ms | 1687 ms | 2.9 | 9 | 4 | $0.36 | billed |  |
| elephant@openrouter | 338 | 174 ms | 199 ms | 275 ms | 600 ms | 1.6 | 0 | 4 | $0.21 | billed | ○ |
| gemini-decision@google | 338 | 298 ms | 369 ms | 409 ms | 436 ms | 1.4 | 0 | 4 | $0.72 | estimated |  |
| groundhog@openrouter | 338 | 231 ms | 269 ms | 443 ms | 1274 ms | 1.9 | 0 | 2 | $0.24 | billed | ○ |
| heygen-decision@openrouter | 338 | 313 ms | 590 ms | 2127 ms | 3855 ms | 6.8 | 0 | 4 | $1.01 | billed |  |
| jev:1.14 | 338 | 112 ms | 142 ms | 208 ms | 429 ms | 1.9 | 0 | 4 | $0.35 | estimated | ○ |
| joey@openrouter | 338 | 169 ms | 192 ms | 284 ms | 383 ms | 1.7 | 0 | 4 | $0.06 | billed | ○ |
| kev@openrouter | 338 | 520 ms | 644 ms | 980 ms | 1146 ms | 1.9 | 0 | 4 | $0.22 | billed |  |
| luna@decisions | 338 | 187 ms | 353 ms | 569 ms | 787 ms | 3.0 | 0 | 4 | $0.69 | estimated |  |
| mammoth@openrouter | 338 | 188 ms | 217 ms | 488 ms | 1536 ms | 2.6 | 0 | 4 | $0.61 | billed | ○ |
| mo@vercel | 338 | 339 ms | 439 ms | 945 ms | 1041 ms | 2.8 | 0 | 4 | $0.26 | billed |  |
| reflex@openrouter | 338 | 268 ms | 297 ms | 391 ms | 626 ms | 1.5 | 0 | 4 | $0.26 | billed | ○ |
| span@openrouter | 338 | 561 ms | 890 ms | 1026 ms | 1153 ms | 1.8 | 0 | 4 | $0.07 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: bison@openrouter, clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, decider-1.3@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max-1.1@vercel, drex-max@openrouter, elephant@openrouter, groundhog@openrouter, heygen-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| bison@openrouter | $0.02 | 43 s (estimated, 338 calls) | 21 min | 2 |
| clef-flash@openrouter | $0.0055 | 25 s (estimated, 338 calls) | 12 min | 4 |
| clef-omni@openrouter | $0.03 | 16 s (estimated, 338 calls) | 8 min | 4 |
| clef@openrouter | $0.05 | 24 s (estimated, 338 calls) | 12 min | 4 |
| d1-ultra@openrouter | $0.0083 | 2 min (estimated, 338 calls) | 67 min | 4 |
| d1.1@openrouter | $0.0040 | 29 s (estimated, 338 calls) | 14 min | 4 |
| d1.2 | $0.0040 | 11 s (estimated, 338 calls) | 6 min | 4 |
| d1.2-ultra | $0.0083 | 12 s (estimated, 338 calls) | 6 min | 4 |
| decider-1.3@vercel | $0.0042 | 35 s (estimated, 338 calls) | 17 min | 4 |
| decider-flash@openrouter | $0.0020 | 15 s (estimated, 338 calls) | 8 min | 4 |
| decider@openrouter | $0.0041 | 22 s (estimated, 338 calls) | 11 min | 4 |
| decision-1.1@openrouter | $0.0092 | 21 s (estimated, 338 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0077 | 23 s (estimated, 338 calls) | 11 min | 4 |
| drex-max-1.1@vercel | $0.0064 | 33 s (estimated, 338 calls) | 16 min | 4 |
| drex-max@openrouter | $0.01 | 36 s (estimated, 338 calls) | 18 min | 4 |
| elephant@openrouter | $0.0072 | 15 s (estimated, 338 calls) | 7 min | 4 |
| gemini-decision@google | $0.02 | 24 s (estimated, 338 calls) | 12 min | 4 |
| groundhog@openrouter | $0.0080 | 41 s (estimated, 338 calls) | 20 min | 2 |
| heygen-decision@openrouter | $0.03 | 33 s (estimated, 338 calls) | 16 min | 4 |
| jev:1.14 | $0.01 | 10 s (estimated, 338 calls) | 5 min | 4 |
| joey@openrouter | $0.0021 | 15 s (estimated, 338 calls) | 7 min | 4 |
| kev@openrouter | $0.0074 | 47 s (estimated, 338 calls) | 23 min | 4 |
| luna@decisions | $0.02 | 19 s (estimated, 338 calls) | 9 min | 4 |
| mammoth@openrouter | $0.02 | 17 s (estimated, 338 calls) | 9 min | 4 |
| mo@vercel | $0.0087 | 31 s (estimated, 338 calls) | 15 min | 4 |
| reflex@openrouter | $0.0086 | 23 s (estimated, 338 calls) | 11 min | 4 |
| span@openrouter | $0.0023 | 51 s (estimated, 338 calls) | 25 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

[ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |
|---|---|---|---|---|---|---|
| bison@openrouter | 75.1% | 74.6% | 68 | 18 | 0.50 | 0.60 |
| clef-flash@openrouter | 73.4% | 74.3% | 76 | 11 | 0.35 | 0.35 |
| clef-omni@openrouter | 76.3% | 76.3% | 73 | 7 | 0.50 | 0.50 |
| clef@openrouter | 69.5% | 75.7% | 72 | 10 | 0.80 | 0.80 |
| d1-ultra@openrouter | 72.8% | 75.1% | 73 | 11 | 0.85 | 0.85 |
| d1.1@openrouter | 70.7% | 72.5% | 73 | 20 | 0.80 | 0.80 |
| d1.2 | 69.2% | 72.8% | 78 | 14 | 0.80 | 0.80 |
| d1.2-ultra | 72.2% | 75.7% | 73 | 9 | 0.70 | 0.70 |
| decider-1.3@vercel | 76.3% | 76.0% | 71 | 10 | 0.80 | 0.80 |
| decider-flash@openrouter | 73.7% | 72.5% | 84 | 9 | 0.55 | 0.55 |
| decider@openrouter | 74.6% | 74.3% | 75 | 12 | 0.55 | 0.55 |
| decision-1.1@openrouter | 69.2% | 75.4% | 63 | 20 | 0.85 | 0.85 |
| decision-1@openrouter | 62.4% | 76.0% | 59 | 22 | 0.85 | 0.85 |
| drex-max-1.1@vercel | 75.1% | 75.1% | 74 | 10 | 0.60 | 0.60 |
| drex-max@openrouter | 74.6% | 74.0% | 74 | 14 | 0.60 | 0.60 |
| elephant@openrouter | 72.5% | 72.2% | 71 | 23 | 0.65 | 0.65 |
| gemini-decision@google | 71.6% | 73.7% | 77 | 12 | 0.75 | 0.75 |
| groundhog@openrouter | 73.4% | 74.6% | 65 | 21 | 0.70 | 0.70 |
| heygen-decision@openrouter | 75.4% | 76.3% | 67 | 13 | 0.55 | 0.55 |
| jev:1.14 | 71.9% | 72.2% | 64 | 30 | 0.60 | 0.60 |
| joey@openrouter | 74.0% | 73.1% | 79 | 12 | 0.55 | 0.55 |
| kev@openrouter | 73.4% | 73.4% | 76 | 14 | 0.35 | 0.35 |
| luna@decisions | 69.2% | 75.4% | 64 | 19 | 0.75 | 0.75 |
| mammoth@openrouter | 70.4% | 74.6% | 70 | 16 | 0.75 | 0.75 |
| mo@vercel | 74.6% | 76.3% | 74 | 6 | 0.75 | 0.75 |
| reflex@openrouter | 74.9% | 75.4% | 71 | 12 | 0.70 | 0.70 |
| span@openrouter | 73.7% | 72.2% | 77 | 17 | 0.65 | 0.65 |

## Misses and false alarms by threshold (bison@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 234 (95%) |
| 0.20 | 20 (22%) | 126 (51%) |
| 0.30 | 43 (47%) | 55 (22%) |
| 0.40 | 59 (65%) | 37 (15%) |
| 0.50 | 64 (70%) | 20 (8%) |
| 0.60 | 71 (78%) | 12 (5%) |
| 0.70 | 81 (89%) | 9 (4%) |
| 0.80 | 89 (98%) | 1 (0%) |
| 0.90 | 90 (99%) | 1 (0%) |

## Misses and false alarms by threshold (clef-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (27%) | 107 (43%) |
| 0.20 | 65 (71%) | 31 (13%) |
| 0.30 | 68 (75%) | 18 (7%) |
| 0.35 | 71 (78%) | 11 (4%) |
| 0.40 | 77 (85%) | 7 (3%) |
| 0.50 | 85 (93%) | 5 (2%) |
| 0.60 | 86 (95%) | 3 (1%) |
| 0.70 | 90 (99%) | 2 (1%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef-omni@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 33 (36%) | 95 (38%) |
| 0.20 | 53 (58%) | 44 (18%) |
| 0.30 | 65 (71%) | 25 (10%) |
| 0.40 | 68 (75%) | 15 (6%) |
| 0.50 | 73 (80%) | 7 (3%) |
| 0.60 | 82 (90%) | 6 (2%) |
| 0.70 | 84 (92%) | 3 (1%) |
| 0.80 | 88 (97%) | 1 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (clef@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (3%) | 205 (83%) |
| 0.20 | 15 (16%) | 132 (53%) |
| 0.30 | 34 (37%) | 90 (36%) |
| 0.40 | 43 (47%) | 74 (30%) |
| 0.50 | 50 (55%) | 53 (21%) |
| 0.60 | 57 (63%) | 36 (15%) |
| 0.70 | 65 (71%) | 23 (9%) |
| 0.80 | 72 (79%) | 9 (4%) |
| 0.90 | 90 (99%) | 1 (0%) |

## Misses and false alarms by threshold (d1-ultra@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 6 (7%) | 178 (72%) |
| 0.20 | 22 (24%) | 130 (53%) |
| 0.30 | 37 (41%) | 82 (33%) |
| 0.40 | 46 (51%) | 56 (23%) |
| 0.50 | 50 (55%) | 42 (17%) |
| 0.60 | 59 (65%) | 31 (13%) |
| 0.70 | 64 (70%) | 24 (10%) |
| 0.80 | 71 (78%) | 11 (4%) |
| 0.85 | 75 (82%) | 6 (2%) |
| 0.90 | 84 (92%) | 3 (1%) |

## Misses and false alarms by threshold (d1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 9 (10%) | 166 (67%) |
| 0.20 | 20 (22%) | 110 (45%) |
| 0.30 | 31 (34%) | 78 (32%) |
| 0.40 | 43 (47%) | 58 (23%) |
| 0.50 | 52 (57%) | 47 (19%) |
| 0.60 | 61 (67%) | 40 (16%) |
| 0.70 | 64 (70%) | 30 (12%) |
| 0.80 | 69 (76%) | 19 (8%) |
| 0.90 | 78 (86%) | 13 (5%) |

## Misses and false alarms by threshold (d1.2)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 241 (98%) |
| 0.20 | 4 (4%) | 198 (80%) |
| 0.30 | 16 (18%) | 120 (49%) |
| 0.40 | 39 (43%) | 69 (28%) |
| 0.50 | 57 (63%) | 47 (19%) |
| 0.60 | 67 (74%) | 19 (8%) |
| 0.70 | 75 (82%) | 13 (5%) |
| 0.80 | 80 (88%) | 5 (2%) |
| 0.90 | 89 (98%) | 2 (1%) |

## Misses and false alarms by threshold (d1.2-ultra)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 246 (100%) |
| 0.20 | 1 (1%) | 221 (89%) |
| 0.30 | 13 (14%) | 160 (65%) |
| 0.40 | 34 (37%) | 75 (30%) |
| 0.50 | 53 (58%) | 41 (17%) |
| 0.60 | 67 (74%) | 21 (9%) |
| 0.70 | 73 (80%) | 9 (4%) |
| 0.80 | 86 (95%) | 4 (2%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decider-1.3@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 37 (41%) | 87 (35%) |
| 0.20 | 46 (51%) | 48 (19%) |
| 0.30 | 55 (60%) | 33 (13%) |
| 0.40 | 62 (68%) | 22 (9%) |
| 0.50 | 65 (71%) | 15 (6%) |
| 0.60 | 69 (76%) | 12 (5%) |
| 0.70 | 70 (77%) | 11 (4%) |
| 0.80 | 72 (79%) | 6 (2%) |
| 0.90 | 83 (91%) | 4 (2%) |

## Misses and false alarms by threshold (decider-flash@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (3%) | 223 (90%) |
| 0.20 | 41 (45%) | 71 (29%) |
| 0.30 | 67 (74%) | 22 (9%) |
| 0.40 | 81 (89%) | 8 (3%) |
| 0.50 | 87 (96%) | 2 (1%) |
| 0.55 | 87 (96%) | 1 (0%) |
| 0.60 | 87 (96%) | 1 (0%) |
| 0.70 | 91 (100%) | 0 (0%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decider@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 14 (15%) | 144 (58%) |
| 0.20 | 45 (49%) | 56 (23%) |
| 0.30 | 61 (67%) | 28 (11%) |
| 0.40 | 68 (75%) | 16 (6%) |
| 0.50 | 75 (82%) | 11 (4%) |
| 0.55 | 75 (82%) | 8 (3%) |
| 0.60 | 80 (88%) | 5 (2%) |
| 0.70 | 85 (93%) | 2 (1%) |
| 0.80 | 91 (100%) | 1 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (decision-1.1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (27%) | 116 (47%) |
| 0.20 | 31 (34%) | 94 (38%) |
| 0.30 | 39 (43%) | 78 (32%) |
| 0.40 | 42 (46%) | 65 (26%) |
| 0.50 | 50 (55%) | 54 (22%) |
| 0.60 | 54 (59%) | 40 (16%) |
| 0.70 | 57 (63%) | 32 (13%) |
| 0.80 | 60 (66%) | 26 (11%) |
| 0.85 | 60 (66%) | 21 (9%) |
| 0.90 | 62 (68%) | 20 (8%) |

## Misses and false alarms by threshold (decision-1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 206 (83%) |
| 0.20 | 12 (13%) | 182 (74%) |
| 0.30 | 21 (23%) | 142 (57%) |
| 0.40 | 23 (25%) | 121 (49%) |
| 0.50 | 31 (34%) | 96 (39%) |
| 0.60 | 38 (42%) | 67 (27%) |
| 0.70 | 48 (53%) | 55 (22%) |
| 0.80 | 54 (59%) | 34 (14%) |
| 0.85 | 59 (65%) | 22 (9%) |
| 0.90 | 68 (75%) | 18 (7%) |

## Misses and false alarms by threshold (drex-max-1.1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 7 (8%) | 182 (74%) |
| 0.20 | 39 (43%) | 70 (28%) |
| 0.30 | 51 (56%) | 41 (17%) |
| 0.40 | 60 (66%) | 24 (10%) |
| 0.50 | 67 (74%) | 17 (7%) |
| 0.60 | 71 (78%) | 10 (4%) |
| 0.70 | 76 (84%) | 6 (2%) |
| 0.80 | 84 (92%) | 3 (1%) |
| 0.90 | 91 (100%) | 1 (0%) |

## Misses and false alarms by threshold (drex-max@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 31 (34%) | 118 (48%) |
| 0.20 | 45 (49%) | 49 (20%) |
| 0.30 | 57 (63%) | 35 (14%) |
| 0.40 | 64 (70%) | 27 (11%) |
| 0.50 | 66 (73%) | 20 (8%) |
| 0.60 | 69 (76%) | 14 (6%) |
| 0.70 | 74 (81%) | 12 (5%) |
| 0.80 | 78 (86%) | 9 (4%) |
| 0.90 | 85 (93%) | 2 (1%) |

## Misses and false alarms by threshold (elephant@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 228 (92%) |
| 0.20 | 14 (15%) | 155 (63%) |
| 0.30 | 34 (37%) | 104 (42%) |
| 0.40 | 43 (47%) | 65 (26%) |
| 0.50 | 54 (59%) | 39 (16%) |
| 0.60 | 63 (69%) | 26 (11%) |
| 0.65 | 67 (74%) | 21 (9%) |
| 0.70 | 73 (80%) | 17 (7%) |
| 0.80 | 81 (89%) | 9 (4%) |
| 0.90 | 89 (98%) | 1 (0%) |

## Misses and false alarms by threshold (gemini-decision@google)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (1%) | 245 (99%) |
| 0.20 | 5 (5%) | 204 (83%) |
| 0.30 | 23 (25%) | 142 (57%) |
| 0.40 | 34 (37%) | 86 (35%) |
| 0.50 | 47 (52%) | 49 (20%) |
| 0.60 | 60 (66%) | 30 (12%) |
| 0.70 | 70 (77%) | 16 (6%) |
| 0.75 | 74 (81%) | 10 (4%) |
| 0.80 | 80 (88%) | 5 (2%) |
| 0.90 | 90 (99%) | 0 (0%) |

## Misses and false alarms by threshold (groundhog@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 4 (4%) | 213 (86%) |
| 0.20 | 16 (18%) | 136 (55%) |
| 0.30 | 30 (33%) | 84 (34%) |
| 0.40 | 45 (49%) | 54 (22%) |
| 0.50 | 49 (54%) | 41 (17%) |
| 0.60 | 59 (65%) | 28 (11%) |
| 0.70 | 65 (71%) | 18 (7%) |
| 0.80 | 81 (89%) | 9 (4%) |
| 0.90 | 91 (100%) | 1 (0%) |

## Misses and false alarms by threshold (heygen-decision@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 31 (34%) | 103 (42%) |
| 0.20 | 43 (47%) | 69 (28%) |
| 0.30 | 51 (56%) | 44 (18%) |
| 0.40 | 57 (63%) | 31 (13%) |
| 0.50 | 61 (67%) | 22 (9%) |
| 0.55 | 64 (70%) | 14 (6%) |
| 0.60 | 67 (74%) | 11 (4%) |
| 0.70 | 74 (81%) | 10 (4%) |
| 0.80 | 84 (92%) | 4 (2%) |
| 0.90 | 86 (95%) | 2 (1%) |

## Misses and false alarms by threshold (jev:1.14)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 1 (1%) | 241 (98%) |
| 0.30 | 5 (5%) | 179 (72%) |
| 0.40 | 30 (33%) | 99 (40%) |
| 0.50 | 48 (53%) | 47 (19%) |
| 0.60 | 61 (67%) | 24 (10%) |
| 0.70 | 79 (87%) | 7 (3%) |
| 0.80 | 89 (98%) | 2 (1%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (joey@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 246 (100%) |
| 0.20 | 6 (7%) | 196 (79%) |
| 0.30 | 27 (30%) | 96 (39%) |
| 0.40 | 57 (63%) | 36 (15%) |
| 0.50 | 75 (82%) | 13 (5%) |
| 0.55 | 80 (88%) | 6 (2%) |
| 0.60 | 84 (92%) | 5 (2%) |
| 0.70 | 88 (97%) | 2 (1%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 14 (15%) | 175 (71%) |
| 0.30 | 58 (64%) | 46 (19%) |
| 0.35 | 71 (78%) | 14 (6%) |
| 0.40 | 81 (89%) | 7 (3%) |
| 0.50 | 88 (97%) | 2 (1%) |
| 0.60 | 90 (99%) | 0 (0%) |
| 0.70 | 91 (100%) | 0 (0%) |
| 0.80 | 91 (100%) | 0 (0%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 247 (100%) |
| 0.20 | 2 (2%) | 231 (94%) |
| 0.30 | 16 (18%) | 139 (56%) |
| 0.40 | 41 (45%) | 74 (30%) |
| 0.50 | 45 (49%) | 59 (24%) |
| 0.60 | 49 (54%) | 43 (17%) |
| 0.70 | 60 (66%) | 23 (9%) |
| 0.75 | 65 (71%) | 16 (6%) |
| 0.80 | 78 (86%) | 8 (3%) |
| 0.90 | 86 (95%) | 1 (0%) |

## Misses and false alarms by threshold (mammoth@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (2%) | 234 (95%) |
| 0.20 | 5 (5%) | 165 (67%) |
| 0.30 | 19 (21%) | 119 (48%) |
| 0.40 | 29 (32%) | 83 (34%) |
| 0.50 | 41 (45%) | 59 (24%) |
| 0.60 | 51 (56%) | 43 (17%) |
| 0.70 | 64 (70%) | 19 (8%) |
| 0.75 | 70 (77%) | 12 (5%) |
| 0.80 | 77 (85%) | 7 (3%) |
| 0.90 | 91 (100%) | 0 (0%) |

## Misses and false alarms by threshold (mo@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 15 (16%) | 155 (63%) |
| 0.20 | 45 (49%) | 77 (31%) |
| 0.30 | 55 (60%) | 42 (17%) |
| 0.40 | 61 (67%) | 32 (13%) |
| 0.50 | 65 (71%) | 21 (9%) |
| 0.60 | 68 (75%) | 17 (7%) |
| 0.70 | 71 (78%) | 12 (5%) |
| 0.75 | 74 (81%) | 6 (2%) |
| 0.80 | 77 (85%) | 5 (2%) |
| 0.90 | 85 (93%) | 0 (0%) |

## Misses and false alarms by threshold (reflex@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 34 (37%) | 81 (33%) |
| 0.20 | 46 (51%) | 42 (17%) |
| 0.30 | 55 (60%) | 31 (13%) |
| 0.40 | 60 (66%) | 27 (11%) |
| 0.50 | 66 (73%) | 19 (8%) |
| 0.60 | 68 (75%) | 13 (5%) |
| 0.70 | 71 (78%) | 9 (4%) |
| 0.80 | 74 (81%) | 7 (3%) |
| 0.90 | 83 (91%) | 3 (1%) |

## Misses and false alarms by threshold (span@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 49 (54%) | 48 (19%) |
| 0.20 | 59 (65%) | 34 (14%) |
| 0.30 | 62 (68%) | 27 (11%) |
| 0.40 | 67 (74%) | 23 (9%) |
| 0.50 | 69 (76%) | 20 (8%) |
| 0.60 | 72 (79%) | 18 (7%) |
| 0.65 | 73 (80%) | 14 (6%) |
| 0.70 | 75 (82%) | 12 (5%) |
| 0.80 | 83 (91%) | 7 (3%) |
| 0.90 | 86 (95%) | 2 (1%) |

## Wrong at a high probability (0.9 or more)

**bison@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.94 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.90 | Fix bulk of remaining issues with generalist profile |

**clef-flash@openrouter** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.96 | fix(core): update auth error documentation link to valid anchor and a… |
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #28940 | True | False | 0.95 | fix(a2a-server): clear stale cancellation error on new message turns |
| #27467 | True | False | 0.94 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #27391 | True | False | 0.94 | fix(cli): filter internal session context from history during resumpt… |
| #25324 | True | False | 0.94 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #27698 | True | False | 0.94 | fix(core): Ensure zero-quota limits fail fast to prevent retry loop h… |

**clef-omni@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28216 | True | False | 0.97 | Refactor: exclude transient CI configuration files from workspace con… |
| #25822 | True | False | 0.97 | fix(cli): add missing response key to custom theme text schema |
| #27391 | True | False | 0.96 | fix(cli): filter internal session context from history during resumpt… |
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #25324 | True | False | 0.96 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #29377 | True | False | 0.96 | fix(core): update auth error documentation link to valid anchor and a… |
| #27467 | True | False | 0.95 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #25670 | True | False | 0.95 | fix(core): remove duplicate initialize call on agents refreshed |

**clef@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |
| #29377 | True | False | 0.90 | fix(core): update auth error documentation link to valid anchor and a… |

**d1-ultra@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.95 | fix(cli): add missing response key to custom theme text schema |
| #28470 | False | True | 0.93 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #26073 | False | True | 0.93 | Fix bulk of remaining issues with generalist profile |
| #25324 | True | False | 0.92 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #28530 | False | True | 0.92 | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #25827 | True | False | 0.92 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #29185 | True | False | 0.91 | test(integration): deflake run_shell_command and file-system-interact… |
| #26991 | True | False | 0.91 | fix(ui): clamped table column widths |

**d1.1@openrouter** (22)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #25324 | True | False | 0.97 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #26073 | False | True | 0.96 | Fix bulk of remaining issues with generalist profile |
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #28470 | False | True | 0.96 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #29081 | False | True | 0.95 | fix(core): prevent SSRF in MCP OAuth metadata discovery and authentic… |
| #29450 | False | True | 0.95 | refactor(a2a-server): implement V1 to V2 settings migration logic |
| #26949 | True | False | 0.95 | fix(ci): configure git remote with token for authentication |

**d1.2** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28470 | False | True | 0.95 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #25822 | True | False | 0.92 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |

**decider-1.3@vercel** (41)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #26991 | True | False | 0.98 | fix(ui): clamped table column widths |
| #26073 | False | True | 0.98 | Fix bulk of remaining issues with generalist profile |
| #26270 | True | False | 0.98 | feat(ui): added microphone and updated placeholder for voice mode |
| #29185 | True | False | 0.97 | test(integration): deflake run_shell_command and file-system-interact… |
| #28216 | True | False | 0.97 | Refactor: exclude transient CI configuration files from workspace con… |
| #27619 | True | False | 0.97 | fix(core): implement atomic update in MCP tool discovery |

**decider-flash@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.93 | fix(cli): add missing response key to custom theme text schema |
| #26947 | True | False | 0.92 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #25670 | True | False | 0.91 | fix(core): remove duplicate initialize call on agents refreshed |

**decider@openrouter** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.97 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 0.95 | fix(ui): clamped table column widths |
| #25827 | True | False | 0.95 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26949 | True | False | 0.94 | fix(ci): configure git remote with token for authentication |
| #26947 | True | False | 0.94 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #29377 | True | False | 0.93 | fix(core): update auth error documentation link to valid anchor and a… |
| #27619 | True | False | 0.92 | fix(core): implement atomic update in MCP tool discovery |

**decision-1.1@openrouter** (45)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26073 | False | True | 1.00 | Fix bulk of remaining issues with generalist profile |
| #28530 | False | True | 1.00 | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #28470 | False | True | 1.00 | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #27345 | False | True | 1.00 | feat(context): Complete simplification work. |
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #25827 | True | False | 1.00 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #29377 | True | False | 1.00 | fix(core): update auth error documentation link to valid anchor and a… |
| #28532 | False | True | 1.00 | feat(caretaker-evals): add local golden issue collection and firestor… |

**decision-1@openrouter** (20)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27345 | False | True | 0.99 | feat(context): Complete simplification work. |
| #26073 | False | True | 0.99 | Fix bulk of remaining issues with generalist profile |
| #25822 | True | False | 0.99 | fix(cli): add missing response key to custom theme text schema |
| #25716 | False | True | 0.98 | refactor(memory): replace MemoryManagerAgent with prompt-driven memor… |
| #28530 | False | True | 0.98 | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #26949 | True | False | 0.97 | fix(ci): configure git remote with token for authentication |
| #28532 | False | True | 0.97 | feat(caretaker-evals): add local golden issue collection and firestor… |
| #28470 | False | True | 0.96 | fix(a2a-server): enforce workspace trust and task isolation to preven… |

**drex-max-1.1@vercel** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.94 | fix(cli): add missing response key to custom theme text schema |
| #26270 | True | False | 0.94 | feat(ui): added microphone and updated placeholder for voice mode |
| #26991 | True | False | 0.93 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.92 | fix(core): update auth error documentation link to valid anchor and a… |
| #26947 | True | False | 0.91 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |
| #26949 | True | False | 0.91 | fix(ci): configure git remote with token for authentication |
| #25827 | True | False | 0.91 | fix(cli): prevent duplicate SessionStart systemMessage render |

**drex-max@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #27253 | True | False | 0.97 | fix: robust ripgrep path resolution and 1p hermetic execution support |
| #25324 | True | False | 0.96 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #26646 | True | False | 0.96 | fix(core): resolve parallel tool call streaming ID collision |
| #25827 | True | False | 0.95 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #26949 | True | False | 0.95 | fix(ci): configure git remote with token for authentication |
| #28216 | True | False | 0.95 | Refactor: exclude transient CI configuration files from workspace con… |

**elephant@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.98 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.91 | test(integration): deflake run_shell_command and file-system-interact… |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |

**gemini-decision@google** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.94 | fix(cli): add missing response key to custom theme text schema |

**groundhog@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.97 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.92 | Fix bulk of remaining issues with generalist profile |
| #25324 | True | False | 0.90 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #25827 | True | False | 0.90 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #26991 | True | False | 0.90 | fix(ui): clamped table column widths |

**heygen-decision@openrouter** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #29185 | True | False | 0.98 | test(integration): deflake run_shell_command and file-system-interact… |
| #27041 | True | False | 0.97 | fix(core): resolve EISDIR errors during file processing (#21527) |
| #27467 | True | False | 0.97 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #26073 | False | True | 0.96 | Fix bulk of remaining issues with generalist profile |
| #28940 | True | False | 0.96 | fix(a2a-server): clear stale cancellation error on new message turns |
| #25324 | True | False | 0.96 | fix(cli): prevent spam loop when preferredEditor is invalid |

**luna@decisions** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26073 | False | True | 0.92 | Fix bulk of remaining issues with generalist profile |

**mammoth@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.95 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.91 | test(integration): deflake run_shell_command and file-system-interact… |

**mo@vercel** (15)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25827 | True | False | 0.96 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #26270 | True | False | 0.96 | feat(ui): added microphone and updated placeholder for voice mode |
| #25670 | True | False | 0.95 | fix(core): remove duplicate initialize call on agents refreshed |
| #26947 | True | False | 0.95 | feat(core): add adk.agentSessionSubagentEnabled flag |
| #29377 | True | False | 0.95 | fix(core): update auth error documentation link to valid anchor and a… |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #27619 | True | False | 0.93 | fix(core): implement atomic update in MCP tool discovery |
| #27234 | True | False | 0.93 | fix(core): prevent path traversal in custome command file injection |

**reflex@openrouter** (37)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 0.99 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #29185 | True | False | 0.99 | test(integration): deflake run_shell_command and file-system-interact… |
| #26646 | True | False | 0.99 | fix(core): resolve parallel tool call streaming ID collision |
| #25827 | True | False | 0.98 | fix(cli): prevent duplicate SessionStart systemMessage render |
| #27467 | True | False | 0.98 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #26658 | True | False | 0.98 | fix(routing): fix resolveClassifierModel argument mismatch in Approva… |

**span@openrouter** (51)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 1.00 | fix(ui): clamped table column widths |
| #28940 | True | False | 1.00 | fix(a2a-server): clear stale cancellation error on new message turns |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #28216 | True | False | 0.99 | Refactor: exclude transient CI configuration files from workspace con… |
| #25670 | True | False | 0.99 | fix(core): remove duplicate initialize call on agents refreshed |
| #29185 | True | False | 0.99 | test(integration): deflake run_shell_command and file-system-interact… |
| #27467 | True | False | 0.99 | fix(core): handle multi-line escaped quotes in stripShellWrapper |


## Cases the models disagree on (12 of 193)

| id | label | bison@openrouter | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | decider-1.3@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max-1.1@vercel | drex-max@openrouter | elephant@openrouter | gemini-decision@google | groundhog@openrouter | heygen-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mo@vercel | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #26073 | False | True (0.90) | True (0.72) | True (0.82) | True (0.91) | True (0.93) | True (0.96) | True (0.91) | True (0.80) | True (0.98) | True (0.69) | True (0.80) | True (1.00) | True (0.99) | True (0.91) | True (0.94) | True (0.91) | True (0.89) | True (0.92) | True (0.96) | True (0.76) | True (0.77) | False (0.56) | True (0.92) | True (0.84) | True (0.86) | True (0.97) | True (0.95) | Fix bulk of remaining issues with generalist profile |
| #27232 | True | True (0.88) | True (0.70) | True (0.72) | True (0.90) | True (0.90) | True (0.97) | True (0.93) | True (0.83) | True (0.94) | True (0.65) | True (0.80) | True (1.00) | True (0.98) | True (0.89) | True (0.95) | True (0.84) | True (0.91) | True (0.84) | True (0.93) | True (0.69) | True (0.74) | False (0.55) | True (0.90) | True (0.86) | True (0.90) | True (0.91) | True (0.94) | fix(context): Ensure last message is processed. |
| #28530 | False | True (0.73) | False (0.68) | False (0.63) | True (0.73) | True (0.92) | True (0.87) | True (0.69) | True (0.76) | True (0.90) | False (0.54) | True (0.65) | True (1.00) | True (0.98) | True (0.83) | True (0.88) | True (0.76) | True (0.88) | True (0.82) | True (0.78) | True (0.80) | True (0.51) | False (0.51) | True (0.77) | True (0.73) | True (0.75) | True (0.77) | True (0.84) | feat(caretaker-evals): add triage evaluation framework and judge runn… |
| #26338 | True | True (0.80) | True (0.63) | True (0.78) | True (0.88) | True (0.91) | True (0.96) | True (0.89) | True (0.82) | True (0.96) | False (0.62) | True (0.79) | True (1.00) | True (0.94) | True (0.82) | True (0.98) | True (0.84) | True (0.83) | True (0.87) | True (0.85) | True (0.76) | True (0.62) | False (0.50) | True (0.92) | True (0.88) | True (0.93) | True (0.97) | True (0.72) | feat(memory): add Auto Memory inbox flow with canonical-patch contract |
| #26655 | True | True (0.65) | False (0.55) | True (0.56) | True (0.78) | True (0.88) | True (0.96) | True (0.84) | True (0.76) | True (0.85) | False (0.53) | True (0.59) | True (1.00) | True (0.97) | True (0.78) | True (0.76) | True (0.69) | True (0.84) | True (0.80) | True (0.90) | True (0.62) | True (0.60) | False (0.67) | True (0.79) | True (0.79) | True (0.78) | True (0.87) | True (0.94) | feat(context): Improvements to the snapshotter. |
| #28470 | False | True (0.80) | True (0.57) | True (0.62) | True (0.89) | True (0.93) | True (0.96) | True (0.95) | True (0.86) | True (0.96) | False (0.61) | True (0.75) | True (1.00) | True (0.96) | True (0.87) | True (0.94) | True (0.89) | True (0.74) | True (0.89) | True (0.90) | True (0.78) | False (0.50) | False (0.61) | True (0.89) | True (0.87) | True (0.88) | True (0.93) | True (0.76) | fix(a2a-server): enforce workspace trust and task isolation to preven… |
| #25498 | True | True (0.62) | False (0.51) | True (0.59) | True (0.84) | True (0.90) | True (0.92) | True (0.84) | True (0.82) | True (0.94) | False (0.71) | True (0.71) | True (1.00) | True (0.95) | True (0.84) | True (0.95) | True (0.74) | True (0.82) | True (0.80) | True (0.90) | True (0.72) | False (0.59) | False (0.61) | True (0.85) | True (0.79) | True (0.87) | True (0.92) | True (0.80) | feat(cli): add streamlined `gemini gemma` local model setup |
| #25873 | True | True (0.62) | False (0.69) | True (0.71) | True (0.84) | True (0.86) | True (0.96) | True (0.88) | True (0.77) | True (0.95) | False (0.76) | True (0.59) | True (1.00) | True (0.92) | True (0.78) | True (0.92) | False (0.51) | True (0.67) | True (0.78) | True (0.80) | True (0.62) | False (0.57) | False (0.62) | True (0.82) | True (0.81) | True (0.85) | True (0.92) | True (0.85) | feat(memory): persist auto-memory scratchpad for skill extraction |
| #29214 | True | True (0.73) | False (0.56) | True (0.73) | True (0.85) | True (0.90) | True (0.96) | True (0.82) | True (0.85) | True (0.84) | False (0.59) | True (0.60) | True (1.00) | True (0.97) | True (0.77) | True (0.82) | True (0.89) | True (0.84) | True (0.84) | True (0.91) | True (0.76) | True (0.56) | False (0.55) | True (0.84) | True (0.84) | True (0.82) | True (0.91) | True (0.90) | fix(sandbox): harden filesystem boundaries and isolate runtime state |
| #28532 | False | True (0.62) | False (0.70) | False (0.73) | True (0.67) | True (0.77) | True (0.80) | True (0.57) | True (0.68) | True (0.80) | False (0.51) | True (0.58) | True (1.00) | True (0.97) | True (0.70) | True (0.79) | True (0.77) | True (0.81) | True (0.82) | True (0.71) | True (0.80) | True (0.54) | True (0.57) | True (0.76) | True (0.61) | True (0.67) | True (0.54) | True (0.83) | feat(caretaker-evals): add local golden issue collection and firestor… |
| #26224 | False | False (0.84) | False (0.93) | False (0.95) | False (0.85) | False (0.94) | False (0.96) | False (0.75) | False (0.70) | False (0.98) | False (0.88) | False (0.96) | False (1.00) | True (0.50) | False (0.92) | False (0.96) | False (0.85) | False (0.73) | False (0.82) | False (0.92) | False (0.71) | False (0.75) | False (0.82) | False (0.74) | False (0.83) | False (0.95) | False (0.98) | False (0.99) | fix(cli): use byte length instead of string length for readStdin size… |
| #26888 | True | True (0.68) | True (0.62) | True (0.51) | True (0.86) | True (0.88) | True (0.90) | True (0.78) | True (0.78) | True (0.79) | False (0.61) | True (0.60) | True (1.00) | True (0.97) | True (0.70) | True (0.79) | True (0.66) | True (0.77) | True (0.75) | True (0.84) | True (0.61) | False (0.59) | False (0.63) | True (0.81) | True (0.77) | True (0.71) | True (0.85) | True (0.94) | feat(context): Introduce adaptive token calculator to more accurately… |
