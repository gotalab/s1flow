# helpsteer2-helpfulness

2026-11-23 · 210 labelled dev cases (2 42, 4 42, 1 42, 3 42, 0 42) · split: stratified k-fold (no test case among these: CV numbers only) · source: NVIDIA HelpSteer2 (CC BY 4.0), validation split: 60 responses per helpfulness level, under 4,000 characters

drex-max@openrouter has the lowest MAE (levels), 0.754 [0.682, 0.829] (API cost $0.36 per 10k, p99 1202ms). Its interval overlaps with mo@vercel, decision-1.1@openrouter, drex-max-1.1@vercel, decision-1@openrouter, reflex@openrouter, decider@openrouter, decider-1.3@vercel, bison@openrouter, mammoth@openrouter, d1.2-ultra, gemini-decision@google, d1-ultra@openrouter, heygen-decision@openrouter, jev:1.14, elephant@openrouter, d1.2, groundhog@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. Ordered by task.py's tiebreak (QWK, then accuracy (all)), mo@vercel comes first (API cost $0.25 per 10k, p99 580ms). The highest raw accuracy (dev) is reflex@openrouter's, 47% [40, 53].

## Comparison

| model | scored | accuracy (all) | MAE (levels) | AUROC | ECE | refused | failed |
|---|---|---|---|---|---|---|---|
| bison@openrouter | 210 | 37.1% [31, 44] | 0.82 | 0.87 | 0.08 | 0.0% (0/210) | 0/210 |
| clef-flash@openrouter | 210 | 25.7% [20, 32] | 1.23 | 0.71 | 0.08 | 0.0% (0/210) | 0/210 |
| clef-omni@openrouter | 210 | 28.6% [23, 35] | 1.15 | 0.80 | 0.15 | 0.0% (0/210) | 0/210 |
| clef@openrouter | 210 | 29.0% [23, 35] | 0.94 | 0.82 | 0.12 | 0.0% (0/210) | 0/210 |
| d1-ultra@openrouter | 210 | 30.0% [24, 36] | 0.87 | 0.87 | 0.09 | 0.0% (0/210) | 0/210 |
| d1.1@openrouter | 210 | 25.7% [20, 32] | 0.98 | 0.85 | 0.13 | 0.0% (0/210) | 0/210 |
| d1.2-ultra | 210 | 33.3% [27, 40] | 0.83 | 0.87 | 0.03 | 0.0% (0/210) | 0/210 |
| d1.2 | 210 | 29.5% [23, 36] | 0.90 | 0.87 | 0.06 | 0.0% (0/210) | 0/210 |
| decider-1.3@vercel | 210 | 35.7% [29, 42] | 0.83 | 0.87 | 0.18 | 0.0% (0/210) | 0/210 |
| decider-flash@openrouter | 210 | 25.7% [20, 32] | 1.04 | 0.81 | 0.11 | 0.0% (0/210) | 0/210 |
| decider@openrouter | 210 | 36.2% [30, 43] | 0.81 | 0.87 | 0.09 | 0.0% (0/210) | 0/210 |
| decision-1.1@openrouter | 210 | 41.0% [34, 47] | 0.79 | 0.86 | 0.12 | 0.0% (0/210) | 0/210 |
| decision-1@openrouter | 210 | 38.1% [31, 45] | 0.81 | 0.86 | 0.13 | 0.0% (0/210) | 0/210 |
| drex-max-1.1@vercel | 210 | 35.2% [29, 41] | 0.80 | 0.88 | 0.06 | 0.0% (0/210) | 0/210 |
| drex-max@openrouter | 210 | 39.5% [33, 46] | 0.75 | 0.88 | 0.05 | 0.0% (0/210) | 0/210 |
| elephant@openrouter | 210 | 33.3% [27, 40] | 0.91 | 0.85 | 0.07 | 0.0% (0/210) | 0/210 |
| gemini-decision@google | 210 | 35.2% [29, 42] | 0.84 | 0.85 | 0.05 | 0.0% (0/210) | 0/210 |
| groundhog@openrouter | 210 | 31.0% [24, 38] | 0.88 | 0.86 | 0.06 | 0.0% (0/210) | 0/210 |
| heygen-decision@openrouter | 210 | 33.3% [27, 40] | 0.92 | 0.87 | 0.18 | 0.0% (0/210) | 0/210 |
| jev:1.14 | 210 | 31.4% [25, 38] | 0.89 | 0.82 | 0.21 | 0.0% (0/210) | 0/210 |
| joey@openrouter | 210 | 26.2% [20, 32] | 1.09 | 0.73 | 0.10 | 0.0% (0/210) | 0/210 |
| kev@openrouter | 210 | 21.9% [17, 28] | 1.14 | 0.73 | 0.07 | 0.0% (0/210) | 0/210 |
| luna@decisions | 210 | 37.1% [31, 43] | 0.94 | 0.78 | 0.29 | 0.5% (1/210) | 0/210 |
| mammoth@openrouter | 210 | 34.8% [29, 41] | 0.82 | 0.88 | 0.03 | 0.0% (0/210) | 0/210 |
| mo@vercel | 210 | 39.5% [33, 46] | 0.77 | 0.88 | 0.14 | 0.0% (0/210) | 0/210 |
| reflex@openrouter | 210 | 46.7% [40, 53] | 0.79 | 0.84 | 0.10 | 0.0% (0/210) | 0/210 |
| span@openrouter | 210 | 32.4% [26, 39] | 1.16 | 0.80 | 0.33 | 0.0% (0/210) | 0/210 |

Answered by: bison@openrouter = baseten/bison-1-20261120; clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2-ultra = d1.2-ultra; d1.2 = d1.2; decider-1.3@vercel = perplexity/pplx-decider-v1.3; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max-1.1@vercel = nace-ai/drex-max-v1.1; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; groundhog@openrouter = baseten/groundhog-1-20261120; heygen-decision@openrouter = heygen/heygen-decision-1-20261112; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mo@vercel = modaic/mo; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | MAE (levels) | QWK | accuracy (all) | rule | constraints |
|---|---|---|---|---|---|
| mo@vercel = | 0.767 [0.689, 0.845] | 0.710 [0.641, 0.771] | 40% [33, 46] | — | met |
| drex-max@openrouter = | 0.754 [0.682, 0.829] | 0.688 [0.610, 0.752] | 40% [33, 46] | — | met |
| decision-1.1@openrouter = | 0.793 [0.709, 0.877] | 0.678 [0.593, 0.753] | 41% [34, 47] | — | met |
| drex-max-1.1@vercel = | 0.797 [0.720, 0.873] | 0.673 [0.611, 0.731] | 35% [29, 41] | — | met |
| decision-1@openrouter = | 0.806 [0.726, 0.887] | 0.671 [0.603, 0.733] | 38% [31, 45] | — | met |
| reflex@openrouter = | 0.789 [0.703, 0.884] | 0.656 [0.573, 0.728] | 47% [40, 53] | — | met |
| decider@openrouter = | 0.811 [0.731, 0.885] | 0.641 [0.562, 0.713] | 36% [30, 43] | — | met |
| decider-1.3@vercel = | 0.833 [0.754, 0.915] | 0.640 [0.562, 0.707] | 36% [29, 42] | — | met |
| bison@openrouter = | 0.824 [0.742, 0.906] | 0.639 [0.560, 0.710] | 37% [31, 44] | — | met |
| mammoth@openrouter = | 0.818 [0.740, 0.893] | 0.622 [0.545, 0.692] | 35% [29, 41] | — | met |
| d1.2-ultra = | 0.827 [0.741, 0.902] | 0.612 [0.531, 0.682] | 33% [27, 40] | — | met |
| gemini-decision@google = | 0.839 [0.761, 0.920] | 0.595 [0.509, 0.671] | 35% [29, 42] | — | met |
| d1-ultra@openrouter = | 0.867 [0.794, 0.942] | 0.565 [0.487, 0.638] | 30% [24, 36] | — | met |
| heygen-decision@openrouter = | 0.920 [0.820, 1.015] | 0.562 [0.467, 0.643] | 33% [27, 40] | — | met |
| jev:1.14 = | 0.888 [0.807, 0.970] | 0.558 [0.474, 0.637] | 31% [25, 38] | — | met |
| elephant@openrouter = | 0.909 [0.823, 0.992] | 0.544 [0.455, 0.629] | 33% [27, 40] | — | met |
| d1.2 = | 0.903 [0.816, 0.991] | 0.544 [0.464, 0.613] | 30% [23, 36] | — | met |
| groundhog@openrouter = | 0.881 [0.800, 0.959] | 0.527 [0.441, 0.607] | 31% [24, 38] | — | met |
| luna@decisions | 0.936 [0.833, 1.038] | 0.519 [0.424, 0.612] | 37% [31, 43] | — | met |
| clef@openrouter | 0.936 [0.852, 1.016] | 0.503 [0.412, 0.585] | 29% [23, 35] | — | met |
| d1.1@openrouter | 0.983 [0.892, 1.077] | 0.456 [0.382, 0.533] | 26% [20, 32] | — | met |
| decider-flash@openrouter | 1.038 [0.936, 1.137] | 0.380 [0.303, 0.459] | 26% [20, 32] | — | met |
| joey@openrouter | 1.092 [0.989, 1.195] | 0.320 [0.213, 0.428] | 26% [20, 32] | — | met |
| kev@openrouter | 1.137 [1.038, 1.236] | 0.255 [0.165, 0.342] | 22% [17, 28] | — | met |
| clef-omni@openrouter | 1.147 [1.036, 1.262] | 0.409 [0.318, 0.495] | 29% [23, 35] | — | met |
| span@openrouter | 1.158 [1.033, 1.289] | 0.424 [0.324, 0.518] | 32% [26, 39] | — | met |
| clef-flash@openrouter | 1.230 [1.107, 1.359] | 0.231 [0.149, 0.313] | 26% [20, 32] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bison@openrouter | 210 | 246 ms | 407 ms | 562 ms | 798 ms | 2.3 | 0 | 2 | $0.65 | billed |  |
| clef-flash@openrouter | 210 | 284 ms | 485 ms | 893 ms | 1571 ms | 3.1 | 0 | 4 | $0.17 | billed |  |
| clef-omni@openrouter | 210 | 202 ms | 316 ms | 429 ms | 810 ms | 2.1 | 0 | 4 | $1.02 | billed |  |
| clef@openrouter | 210 | 312 ms | 1299 ms | 4610 ms | 6392 ms | 14.8 | 1 | 4 | $1.47 | billed |  |
| d1-ultra@openrouter | 210 | 562 ms | 5595 ms | 8899 ms | 9993 ms | 15.8 | 10 | 4 | $0.24 | billed |  |
| d1.1@openrouter | 210 | 234 ms | 406 ms | 596 ms | 733 ms | 2.6 | 0 | 4 | $0.11 | billed |  |
| d1.2-ultra | 210 | 121 ms | 182 ms | 425 ms | 449 ms | 3.5 | 0 | 4 | $0.24 | billed |  |
| d1.2 | 210 | 117 ms | 197 ms | 394 ms | 439 ms | 3.4 | 0 | 4 | $0.11 | billed | ○ |
| decider-1.3@vercel | 210 | 354 ms | 444 ms | 814 ms | 1096 ms | 2.3 | 0 | 4 | $0.12 | billed |  |
| decider-flash@openrouter | 210 | 138 ms | 243 ms | 284 ms | 418 ms | 2.1 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 210 | 223 ms | 341 ms | 746 ms | 1027 ms | 3.3 | 0 | 4 | $0.12 | billed | ○ |
| decision-1.1@openrouter | 210 | 227 ms | 284 ms | 625 ms | 820 ms | 2.8 | 0 | 4 | $0.24 | billed | ○ |
| decision-1@openrouter | 210 | 245 ms | 324 ms | 417 ms | 2467 ms | 1.7 | 0 | 4 | $0.23 | billed | ○ |
| drex-max-1.1@vercel | 210 | 371 ms | 523 ms | 923 ms | 1460 ms | 2.5 | 0 | 4 | $0.19 | billed | ○ |
| drex-max@openrouter | 210 | 456 ms | 731 ms | 1202 ms | 1608 ms | 2.6 | 2 | 4 | $0.36 | billed | ○ |
| elephant@openrouter | 210 | 173 ms | 205 ms | 290 ms | 442 ms | 1.7 | 0 | 4 | $0.22 | billed | ○ |
| gemini-decision@google | 210 | 245 ms | 380 ms | 431 ms | 494 ms | 1.8 | 1 | 4 | $0.63 | estimated |  |
| groundhog@openrouter | 210 | 240 ms | 428 ms | 501 ms | 574 ms | 2.1 | 0 | 2 | $0.23 | billed |  |
| heygen-decision@openrouter | 210 | 373 ms | 740 ms | 1362 ms | 1520 ms | 3.6 | 0 | 4 | $1.31 | billed |  |
| jev:1.14 | 210 | 109 ms | 141 ms | 172 ms | 267 ms | 1.6 | 0 | 4 | $0.34 | estimated | ○ |
| joey@openrouter | 210 | 167 ms | 188 ms | 239 ms | 266 ms | 1.4 | 0 | 4 | $0.06 | billed | ○ |
| kev@openrouter | 210 | 524 ms | 652 ms | 974 ms | 1027 ms | 1.9 | 0 | 4 | $0.22 | billed |  |
| luna@decisions | 209 | 182 ms | 341 ms | 549 ms | 577 ms | 3.0 | 0 | 4 | $0.63 | estimated |  |
| mammoth@openrouter | 210 | 184 ms | 226 ms | 311 ms | 1952 ms | 1.7 | 0 | 4 | $0.63 | billed | ○ |
| mo@vercel | 210 | 338 ms | 437 ms | 580 ms | 803 ms | 1.7 | 0 | 4 | $0.25 | billed | ○ |
| reflex@openrouter | 210 | 763 ms | 1330 ms | 1594 ms | 1873 ms | 2.1 | 1 | 4 | $0.26 | billed |  |
| span@openrouter | 210 | 671 ms | 916 ms | 1039 ms | 1106 ms | 1.5 | 0 | 4 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: bison@openrouter, clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2-ultra, d1.2, decider-1.3@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max-1.1@vercel, drex-max@openrouter, elephant@openrouter, groundhog@openrouter, heygen-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| bison@openrouter | $0.01 | 29 s (estimated, 210 calls) | 23 min | 2 |
| clef-flash@openrouter | $0.0035 | 17 s (estimated, 210 calls) | 13 min | 4 |
| clef-omni@openrouter | $0.02 | 12 s (estimated, 210 calls) | 10 min | 4 |
| clef@openrouter | $0.03 | 33 s (estimated, 210 calls) | 26 min | 4 |
| d1-ultra@openrouter | $0.0050 | 2 min (estimated, 210 calls) | 72 min | 4 |
| d1.1@openrouter | $0.0024 | 14 s (estimated, 210 calls) | 11 min | 4 |
| d1.2-ultra | $0.0050 | 7 s (estimated, 210 calls) | 6 min | 4 |
| d1.2 | $0.0024 | 7 s (estimated, 210 calls) | 6 min | 4 |
| decider-1.3@vercel | $0.0026 | 19 s (estimated, 210 calls) | 15 min | 4 |
| decider-flash@openrouter | $0.0013 | 8 s (estimated, 210 calls) | 7 min | 4 |
| decider@openrouter | $0.0025 | 14 s (estimated, 210 calls) | 11 min | 4 |
| decision-1.1@openrouter | $0.0050 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0047 | 14 s (estimated, 210 calls) | 11 min | 4 |
| drex-max-1.1@vercel | $0.0039 | 22 s (estimated, 210 calls) | 17 min | 4 |
| drex-max@openrouter | $0.0076 | 25 s (estimated, 210 calls) | 20 min | 4 |
| elephant@openrouter | $0.0047 | 9 s (estimated, 210 calls) | 7 min | 4 |
| gemini-decision@google | $0.01 | 14 s (estimated, 210 calls) | 11 min | 4 |
| groundhog@openrouter | $0.0047 | 29 s (estimated, 210 calls) | 23 min | 2 |
| heygen-decision@openrouter | $0.03 | 24 s (estimated, 210 calls) | 19 min | 4 |
| jev:1.14 | $0.0072 | 6 s (estimated, 210 calls) | 5 min | 4 |
| joey@openrouter | $0.0013 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0046 | 29 s (estimated, 210 calls) | 23 min | 4 |
| luna@decisions | $0.01 | 11 s (estimated, 209 calls) | 9 min | 4 |
| mammoth@openrouter | $0.01 | 10 s (estimated, 210 calls) | 8 min | 4 |
| mo@vercel | $0.0053 | 19 s (estimated, 210 calls) | 15 min | 4 |
| reflex@openrouter | $0.0054 | 45 s (estimated, 210 calls) | 36 min | 4 |
| span@openrouter | $0.0013 | 35 s (estimated, 210 calls) | 28 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

[ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.
Refused: inputs the model did not take (question type, image, audio, video, PDF, length limits) and answers it declined to give. The model's limit, not a failed call: the candidate is kept, and the case stays in every denominator.

## Wrong at a high probability (0.9 or more)

**bison@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-777 | 3 | 4 | 0.90 | User: Using the information from the reference text, find the percent… |

**clef-omni@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-65 | 0 | 4 | 0.91 | User: Can you tell me how to make a Trident cocktail? |

**decider-1.3@vercel** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-777 | 3 | 4 | 0.97 | User: Using the information from the reference text, find the percent… |

**decision-1.1@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-777 | 3 | 4 | 0.97 | User: Using the information from the reference text, find the percent… |
| val-606 | 2 | 0 | 0.90 | User: What neighborhoods outside Greenville SC, but within 20 mile ra… |

**decision-1@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-774 | 1 | 0 | 0.92 | User: Answer #4's subject, object, and possessive pronouns, then rewr… |

**heygen-decision@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-777 | 3 | 4 | 0.96 | User: Using the information from the reference text, find the percent… |

**jev:1.14** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-272 | 1 | 0 | 0.95 | User: I want to make a cell of excel  Calculate the number of Link wo… |

**luna@decisions** (17)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-272 | 1 | 0 | 1.00 | User: I want to make a cell of excel  Calculate the number of Link wo… |
| val-328 | 2 | 0 | 0.99 | User: I have a model which is trained with input shape of (5,20) and … |
| val-287 | 1 | 0 | 0.99 | User: Give me 10 different, unique and convincing value propositions … |
| val-24 | 1 | 0 | 0.99 | User: Please provide the equation to calculate the moment of inertia … |
| val-136 | 2 | 1 | 0.97 | User: Write a story about a bald headed technology gremlin called Mat… |
| val-590 | 3 | 4 | 0.96 | User: Im creating a school website otonokizaka national high school c… |
| val-462 | 3 | 1 | 0.95 | User: Taking into account the scientific, psychological, phylosophica… |
| val-777 | 3 | 4 | 0.94 | User: Using the information from the reference text, find the percent… |

**mo@vercel** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-777 | 3 | 4 | 0.96 | User: Using the information from the reference text, find the percent… |
| val-272 | 1 | 0 | 0.96 | User: I want to make a cell of excel  Calculate the number of Link wo… |

**reflex@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-272 | 1 | 0 | 0.95 | User: I want to make a cell of excel  Calculate the number of Link wo… |

**span@openrouter** (23)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-777 | 3 | 4 | 0.99 | User: Using the information from the reference text, find the percent… |
| val-611 | 2 | 4 | 0.99 | User: Does the human body regenerate itself? |
| val-590 | 3 | 4 | 0.98 | User: Im creating a school website otonokizaka national high school c… |
| val-107 | 3 | 4 | 0.98 | User: What is recommder system? |
| val-130 | 3 | 4 | 0.98 | User: can i feed you a pdf file and ask questions about it |
| val-65 | 0 | 4 | 0.98 | User: Can you tell me how to make a Trident cocktail? |
| val-696 | 3 | 4 | 0.98 | User: What are the core concepts of emergence theory? |
| val-408 | 3 | 4 | 0.97 | User: What are the pros and cons of biogas |


## Cases the models disagree on (12 of 210)

| id | label | bison@openrouter | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2-ultra | d1.2 | decider-1.3@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max-1.1@vercel | drex-max@openrouter | elephant@openrouter | gemini-decision@google | groundhog@openrouter | heygen-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mo@vercel | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| val-272 | 1 | 0 (0.87) | 1 (0.17) | 1 (0.17) | 0 (0.74) | 0 (0.71) | 1 (0.21) | 0 (0.70) | 0 (0.69) | 0 (0.80) | 1 (0.26) | 0 (0.75) | 0 (0.87) | 0 (0.82) | 0 (0.78) | 0 (0.86) | 1 (0.24) | 0 (0.62) | 1 (0.10) | 0 (0.88) | 0 (0.95) | 0 (0.76) | 1 (0.19) | 0 (1.00) | 0 (0.86) | 0 (0.96) | 0 (0.95) | 0 (0.80) | User: I want to make a cell of excel  Calculate the number of Link wo… |
| val-466 | 0 | 0 (0.84) | 1 (0.13) | 1 (0.16) | 1 (0.21) | 1 (0.23) | 0 (0.85) | 0 (0.87) | 0 (0.88) | 0 (0.80) | 0 (0.84) | 0 (0.88) | 0 (0.95) | 0 (0.98) | 0 (0.85) | 0 (0.88) | 0 (0.89) | 1 (0.33) | 0 (0.91) | 0 (0.89) | 0 (0.98) | 0 (0.75) | 2 (0.23) | 0 (1.00) | 0 (0.89) | 0 (0.91) | 0 (0.91) | 0 (0.89) | User: rewrite as a sales flyer:  27 Notch Shopping Center Dr Branson … |
| val-957 | 0 | 0 (0.86) | 1 (0.22) | 0 (0.85) | 0 (0.82) | 0 (0.71) | 1 (0.20) | 1 (0.18) | 1 (0.18) | 0 (0.88) | 1 (0.16) | 0 (0.86) | 0 (0.96) | 0 (0.93) | 0 (0.86) | 0 (0.85) | 1 (0.14) | 1 (0.30) | 1 (0.14) | 0 (0.90) | 0 (0.81) | 0 (0.75) | 1 (0.17) | 0 (1.00) | 0 (0.85) | 0 (0.95) | 0 (0.92) | 0 (0.80) | User: do you know the english word drama  Assistant: Yes, I know the … |
| val-888 | 0 | 0 (0.96) | 0 (0.81) | 0 (0.77) | 0 (0.93) | 0 (0.92) | 0 (0.92) | 0 (0.91) | 0 (0.93) | 0 (0.97) | 1 (0.15) | 0 (0.94) | 0 (1.00) | 0 (1.00) | 0 (0.93) | 0 (0.96) | 0 (0.90) | 0 (0.80) | 0 (0.95) | 0 (0.99) | 0 (0.96) | 1 (0.17) | 1 (0.21) | 0 (0.99) | 0 (0.98) | 0 (0.99) | 0 (1.00) | 0 (0.93) | User: I want to get a shop selling merch based on my artwork online. … |
| val-777 | 3 | 4 (0.90) | 4 (0.77) | 4 (0.76) | 4 (0.78) | 4 (0.77) | 3 (0.36) | 4 (0.73) | 3 (0.31) | 4 (0.97) | 4 (0.73) | 4 (0.88) | 4 (0.97) | 4 (0.88) | 4 (0.84) | 4 (0.82) | 4 (0.85) | 4 (0.73) | 4 (0.87) | 4 (0.96) | 3 (0.37) | 4 (0.71) | 3 (0.23) | 4 (0.94) | 4 (0.88) | 4 (0.96) | 4 (0.85) | 4 (0.99) | User: Using the information from the reference text, find the percent… |
| val-729 | 0 | 1 (0.07) | 2 (0.41) | 0 (0.82) | 1 (0.10) | 1 (0.23) | 1 (0.18) | 1 (0.16) | 1 (0.16) | 1 (0.34) | 2 (0.42) | 1 (0.20) | 0 (0.99) | 0 (0.80) | 1 (0.21) | 0 (0.75) | 1 (0.08) | 1 (0.22) | 0 (0.74) | 0 (0.85) | 1 (0.09) | 3 (0.23) | 3 (0.22) | 0 (0.92) | 1 (0.09) | 0 (0.87) | 0 (0.91) | 0 (0.92) | User: The paper should serve any one, or any combination, of the foll… |
| val-24 | 1 | 1 (0.21) | 3 (0.27) | 1 (0.21) | 1 (0.26) | 1 (0.35) | 1 (0.29) | 1 (0.24) | 1 (0.23) | 1 (0.30) | 2 (0.23) | 1 (0.30) | 0 (0.90) | 0 (0.75) | 1 (0.25) | 1 (0.21) | 1 (0.18) | 1 (0.29) | 1 (0.21) | 2 (0.25) | 0 (0.77) | 2 (0.20) | 2 (0.25) | 0 (0.99) | 1 (0.22) | 0 (0.71) | 1 (0.21) | 1 (0.15) | User: Please provide the equation to calculate the moment of inertia … |
| val-287 | 1 | 1 (0.29) | 2 (0.27) | 2 (0.23) | 1 (0.27) | 1 (0.32) | 1 (0.32) | 1 (0.26) | 1 (0.31) | 1 (0.45) | 2 (0.25) | 1 (0.31) | 0 (0.86) | 0 (0.84) | 1 (0.28) | 1 (0.27) | 1 (0.25) | 1 (0.45) | 1 (0.17) | 1 (0.20) | 1 (0.50) | 1 (0.20) | 2 (0.18) | 0 (0.99) | 1 (0.27) | 1 (0.23) | 1 (0.37) | 0 (0.92) | User: Give me 10 different, unique and convincing value propositions … |
| val-323 | 0 | 0 (0.94) | 1 (0.13) | 1 (0.13) | 0 (0.78) | 0 (0.89) | 0 (0.88) | 0 (0.82) | 0 (0.89) | 0 (0.93) | 1 (0.15) | 0 (0.92) | 0 (0.99) | 0 (0.94) | 0 (0.88) | 0 (0.93) | 0 (0.88) | 0 (0.74) | 0 (0.93) | 0 (0.98) | 0 (0.97) | 0 (0.89) | 1 (0.12) | 0 (0.99) | 0 (0.94) | 0 (0.96) | 0 (0.98) | 0 (0.93) | User: A heated rap battle between Eminem and 2pac. Both artists rap a… |
| val-328 | 2 | 2 (0.29) | 2 (0.21) | 2 (0.25) | 1 (0.31) | 2 (0.32) | 2 (0.32) | 2 (0.27) | 2 (0.26) | 2 (0.46) | 2 (0.24) | 2 (0.36) | 1 (0.33) | 1 (0.35) | 3 (0.33) | 2 (0.33) | 2 (0.31) | 1 (0.41) | 1 (0.29) | 2 (0.41) | 1 (0.55) | 2 (0.25) | 2 (0.21) | 0 (0.99) | 2 (0.26) | 3 (0.43) | 2 (0.40) | 1 (0.17) | User: I have a model which is trained with input shape of (5,20) and … |
| val-663 | 0 | 0 (0.75) | 3 (0.21) | 1 (0.16) | 1 (0.22) | 1 (0.24) | 1 (0.25) | 0 (0.72) | 0 (0.73) | 0 (0.75) | 1 (0.20) | 0 (0.74) | 0 (0.86) | 0 (0.90) | 0 (0.74) | 0 (0.76) | 0 (0.83) | 1 (0.33) | 1 (0.13) | 1 (0.24) | 0 (0.86) | 2 (0.17) | 2 (0.23) | 0 (0.99) | 0 (0.85) | 0 (0.86) | 0 (0.88) | 1 (0.17) | User: which soldier was awarded the param vir chakra after he was mar… |
| val-611 | 2 | 3 (0.40) | 4 (0.75) | 4 (0.85) | 3 (0.54) | 3 (0.38) | 4 (0.63) | 4 (0.64) | 4 (0.64) | 4 (0.78) | 3 (0.34) | 4 (0.65) | 3 (0.52) | 3 (0.56) | 4 (0.65) | 4 (0.66) | 4 (0.67) | 3 (0.36) | 3 (0.32) | 4 (0.86) | 3 (0.63) | 3 (0.32) | 3 (0.31) | 3 (0.47) | 3 (0.33) | 4 (0.60) | 4 (0.65) | 4 (0.99) | User: Does the human body regenerate itself? |
