# helpsteer2-helpfulness

2026-11-15 · 210 labelled dev cases (2 42, 4 42, 1 42, 3 42, 0 42) · split: stratified k-fold (no test case among these: CV numbers only) · source: NVIDIA HelpSteer2 (CC BY 4.0), validation split: 60 responses per helpfulness level, under 4,000 characters

**drex-max@openrouter** has the lowest MAE (levels), 0.754 [0.679, 0.835] (API cost $0.36 per 10k, p99 1202ms). Its interval overlaps with decision-1@openrouter, reflex@openrouter, decider@openrouter, mammoth@openrouter, gemini-decision@google, d1-ultra@openrouter, jev:1.14, elephant@openrouter, luna@decisions: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is reflex@openrouter's, 47% [40, 54].

## Comparison

| model | scored | accuracy (all) | MAE (levels) | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 25.7% [20, 31] | 1.23 | 0.71 | 0.08 | 1% [0, 3] | 0.0% (0.0%) | 0.0% (0/210) | 0/210 |
| clef-omni@openrouter | 210 | 28.6% [23, 34] | 1.15 | 0.80 | 0.15 | 0% [0, 1] | 0.0% (0.0%) | 0.0% (0/210) | 0/210 |
| clef@openrouter | 210 | 29.0% [23, 36] | 0.94 | 0.82 | 0.12 | 1% [0, 3] | 66.7% (13.5%) | 0.0% (0/210) | 0/210 |
| d1-ultra@openrouter | 210 | 30.0% [24, 36] | 0.87 | 0.87 | 0.09 | 0% [0, 1] | 0.0% (0.0%) | 0.0% (0/210) | 0/210 |
| d1.1@openrouter | 210 | 25.7% [20, 32] | 0.98 | 0.85 | 0.13 | 1% [0, 3] | 66.7% (13.5%) | 0.0% (0/210) | 0/210 |
| d1@vercel | 210 | 33.3% [26, 40] | 0.99 | 0.85 | 0.11 | 2% [0, 4] | 100.0% (47.3%) | 0.0% (0/210) | 0/210 |
| decider-flash@openrouter | 210 | 25.7% [20, 32] | 1.04 | 0.81 | 0.11 | 0% [0, 0] | — (0.0%) | 0.0% (0/210) | 0/210 |
| decider@openrouter | 210 | 36.2% [30, 42] | 0.81 | 0.87 | 0.09 | 2% [0, 4] | 75.0% (24.9%) | 0.0% (0/210) | 0/210 |
| decision-1@openrouter | 210 | 38.1% [31, 44] | 0.81 | 0.86 | 0.13 | 3% [1, 6] | 85.7% (47.9%) | 0.0% (0/210) | 0/210 |
| drex-max@openrouter | 210 | 39.5% [33, 46] | 0.75 | 0.88 | 0.05 | 5% [2, 8] | 80.0% (49.3%) | 0.0% (0/210) | 0/210 |
| elephant@openrouter | 210 | 33.3% [27, 40] | 0.91 | 0.85 | 0.07 | 2% [0, 5] | 80.0% (34.3%) | 0.0% (0/210) | 0/210 |
| gemini-decision@google | 210 | 35.2% [29, 42] | 0.84 | 0.85 | 0.05 | 3% [1, 5] | 66.7% (27.1%) | 0.0% (0/210) | 0/210 |
| jev:1.14 | 210 | 31.4% [25, 38] | 0.89 | 0.82 | 0.21 | 3% [1, 6] | 57.1% (22.5%) | 0.0% (0/210) | 0/210 |
| joey@openrouter | 210 | 26.2% [21, 32] | 1.09 | 0.73 | 0.10 | 1% [0, 2] | 50.0% (2.5%) | 0.0% (0/210) | 0/210 |
| kev@openrouter | 210 | 21.9% [16, 28] | 1.14 | 0.73 | 0.07 | 0% [0, 0] | — (0.0%) | 0.0% (0/210) | 0/210 |
| luna@decisions | 210 | 37.1% [30, 44] | 0.94 | 0.78 | 0.29 | 0% [0, 1] | 0.0% (0.0%) | 0.5% (1/210) | 0/210 |
| mammoth@openrouter | 210 | 34.8% [29, 41] | 0.82 | 0.88 | 0.03 | 1% [0, 2] | 100.0% (22.4%) | 0.0% (0/210) | 0/210 |
| reflex@openrouter | 210 | 46.7% [40, 54] | 0.79 | 0.84 | 0.10 | 3% [1, 5] | 83.3% (41.8%) | 0.0% (0/210) | 0/210 |
| span@openrouter | 210 | 32.4% [26, 40] | 1.16 | 0.80 | 0.33 | 0% [0, 0] | — (0.0%) | 0.0% (0/210) | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | MAE (levels) | QWK | accuracy (all) | rule | constraints |
|---|---|---|---|---|---|
| drex-max@openrouter = | 0.754 [0.679, 0.835] | 0.688 [0.618, 0.748] | 40% [33, 46] | — | met |
| decision-1@openrouter = | 0.806 [0.727, 0.891] | 0.671 [0.600, 0.731] | 38% [31, 44] | — | met |
| reflex@openrouter = | 0.789 [0.693, 0.888] | 0.656 [0.568, 0.731] | 47% [40, 54] | — | met |
| decider@openrouter = | 0.811 [0.734, 0.891] | 0.641 [0.571, 0.711] | 36% [30, 42] | — | met |
| mammoth@openrouter = | 0.818 [0.739, 0.902] | 0.622 [0.543, 0.691] | 35% [29, 41] | — | met |
| gemini-decision@google = | 0.839 [0.759, 0.921] | 0.595 [0.519, 0.671] | 35% [29, 42] | — | met |
| d1-ultra@openrouter = | 0.867 [0.787, 0.942] | 0.565 [0.487, 0.637] | 30% [24, 36] | — | met |
| jev:1.14 = | 0.888 [0.796, 0.974] | 0.558 [0.461, 0.642] | 31% [25, 38] | — | met |
| elephant@openrouter = | 0.909 [0.819, 1.001] | 0.544 [0.455, 0.618] | 33% [27, 40] | — | met |
| luna@decisions = | 0.936 [0.826, 1.047] | 0.519 [0.414, 0.607] | 37% [30, 44] | — | met |
| clef@openrouter | 0.936 [0.844, 1.021] | 0.503 [0.412, 0.580] | 29% [23, 36] | — | met |
| d1.1@openrouter | 0.983 [0.888, 1.085] | 0.456 [0.370, 0.540] | 26% [20, 32] | — | met |
| d1@vercel | 0.987 [0.878, 1.093] | 0.544 [0.461, 0.624] | 33% [26, 40] | — | met |
| decider-flash@openrouter | 1.038 [0.932, 1.147] | 0.380 [0.299, 0.459] | 26% [20, 32] | — | met |
| joey@openrouter | 1.092 [0.988, 1.198] | 0.320 [0.214, 0.425] | 26% [21, 32] | — | met |
| kev@openrouter | 1.137 [1.032, 1.243] | 0.255 [0.171, 0.337] | 22% [16, 28] | — | met |
| clef-omni@openrouter | 1.147 [1.021, 1.271] | 0.409 [0.315, 0.500] | 29% [23, 34] | — | met |
| span@openrouter | 1.158 [1.018, 1.299] | 0.424 [0.322, 0.526] | 32% [26, 40] | — | met |
| clef-flash@openrouter | 1.230 [1.094, 1.363] | 0.231 [0.145, 0.327] | 26% [20, 31] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 284 ms | 485 ms | 893 ms | 1571 ms | 3.1 | 0 | 4 | $0.17 | billed |  |
| clef-omni@openrouter | 210 | 202 ms | 316 ms | 429 ms | 810 ms | 2.1 | 0 | 4 | $1.02 | billed |  |
| clef@openrouter | 210 | 312 ms | 1299 ms | 4610 ms | 6392 ms | 14.8 | 1 | 4 | $1.47 | billed |  |
| d1-ultra@openrouter | 210 | 562 ms | 5595 ms | 8899 ms | 9993 ms | 15.8 | 10 | 4 | $0.24 | billed |  |
| d1.1@openrouter | 210 | 234 ms | 406 ms | 596 ms | 733 ms | 2.6 | 0 | 4 | $0.11 | billed | ○ |
| d1@vercel | 210 | 529 ms | 818 ms | 5051 ms | 5858 ms | 9.5 | 1 | 4 | $0.11 | billed |  |
| decider-flash@openrouter | 210 | 138 ms | 243 ms | 284 ms | 418 ms | 2.1 | 0 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 210 | 223 ms | 341 ms | 746 ms | 1027 ms | 3.3 | 0 | 4 | $0.12 | billed | ○ |
| decision-1@openrouter | 210 | 245 ms | 324 ms | 417 ms | 2467 ms | 1.7 | 0 | 4 | $0.23 | billed | ○ |
| drex-max@openrouter | 210 | 456 ms | 731 ms | 1202 ms | 1608 ms | 2.6 | 2 | 4 | $0.36 | billed | ○ |
| elephant@openrouter | 210 | 173 ms | 205 ms | 290 ms | 442 ms | 1.7 | 0 | 4 | $0.22 | billed | ○ |
| gemini-decision@google | 210 | 245 ms | 380 ms | 431 ms | 494 ms | 1.8 | 1 | 4 | $0.63 | estimated |  |
| jev:1.14 | 210 | 109 ms | 141 ms | 172 ms | 267 ms | 1.6 | 0 | 4 | $0.34 | estimated | ○ |
| joey@openrouter | 210 | 167 ms | 188 ms | 239 ms | 266 ms | 1.4 | 0 | 4 | $0.06 | billed | ○ |
| kev@openrouter | 210 | 524 ms | 652 ms | 974 ms | 1027 ms | 1.9 | 0 | 4 | $0.22 | billed |  |
| luna@decisions | 209 | 182 ms | 341 ms | 549 ms | 577 ms | 3.0 | 0 | 4 | $0.63 | estimated |  |
| mammoth@openrouter | 210 | 184 ms | 226 ms | 311 ms | 1952 ms | 1.7 | 0 | 4 | $0.63 | billed | ○ |
| reflex@openrouter | 210 | 763 ms | 1330 ms | 1594 ms | 1873 ms | 2.1 | 1 | 4 | $0.26 | billed | ○ |
| span@openrouter | 210 | 671 ms | 916 ms | 1039 ms | 1106 ms | 1.5 | 0 | 4 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0035 | 17 s (estimated, 210 calls) | 13 min | 4 |
| clef-omni@openrouter | $0.02 | 12 s (estimated, 210 calls) | 10 min | 4 |
| clef@openrouter | $0.03 | 33 s (estimated, 210 calls) | 26 min | 4 |
| d1-ultra@openrouter | $0.0050 | 2 min (estimated, 210 calls) | 72 min | 4 |
| d1.1@openrouter | $0.0024 | 14 s (estimated, 210 calls) | 11 min | 4 |
| d1@vercel | $0.0024 | 35 s (estimated, 210 calls) | 28 min | 4 |
| decider-flash@openrouter | $0.0013 | 8 s (estimated, 210 calls) | 7 min | 4 |
| decider@openrouter | $0.0025 | 14 s (estimated, 210 calls) | 11 min | 4 |
| decision-1@openrouter | $0.0047 | 14 s (estimated, 210 calls) | 11 min | 4 |
| drex-max@openrouter | $0.0076 | 25 s (estimated, 210 calls) | 20 min | 4 |
| elephant@openrouter | $0.0047 | 9 s (estimated, 210 calls) | 7 min | 4 |
| gemini-decision@google | $0.01 | 14 s (estimated, 210 calls) | 11 min | 4 |
| jev:1.14 | $0.0072 | 6 s (estimated, 210 calls) | 5 min | 4 |
| joey@openrouter | $0.0013 | 9 s (estimated, 210 calls) | 7 min | 4 |
| kev@openrouter | $0.0046 | 29 s (estimated, 210 calls) | 23 min | 4 |
| luna@decisions | $0.01 | 11 s (estimated, 209 calls) | 9 min | 4 |
| mammoth@openrouter | $0.01 | 10 s (estimated, 210 calls) | 8 min | 4 |
| reflex@openrouter | $0.0054 | 45 s (estimated, 210 calls) | 36 min | 4 |
| span@openrouter | $0.0013 | 35 s (estimated, 210 calls) | 28 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results require an explicit final check. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.
Refused: inputs the model did not take (question type, image, audio, video, PDF, length limits) and answers it declined to give. The model's limit, not a failed call: the candidate is kept, and the case stays in every denominator.

## Wrong at a high probability (0.9 or more)

**clef-omni@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-65 | 0 | 4 | 0.91 | User: Can you tell me how to make a Trident cocktail? |

**decision-1@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-774 | 1 | 0 | 0.92 | User: Answer #4's subject, object, and possessive pronouns, then rewr… |

**jev:1.14** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-272 | 1 | 0 | 0.95 | User: I want to make a cell of excel  Calculate the number of Link wo… |

**luna@decisions** (17)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-272 | 1 | 0 | 1.00 | User: I want to make a cell of excel  Calculate the number of Link wo… |
| val-287 | 1 | 0 | 0.99 | User: Give me 10 different, unique and convincing value propositions … |
| val-328 | 2 | 0 | 0.99 | User: I have a model which is trained with input shape of (5,20) and … |
| val-24 | 1 | 0 | 0.99 | User: Please provide the equation to calculate the moment of inertia … |
| val-136 | 2 | 1 | 0.97 | User: Write a story about a bald headed technology gremlin called Mat… |
| val-590 | 3 | 4 | 0.96 | User: Im creating a school website otonokizaka national high school c… |
| val-462 | 3 | 1 | 0.95 | User: Taking into account the scientific, psychological, phylosophica… |
| val-774 | 1 | 0 | 0.94 | User: Answer #4's subject, object, and possessive pronouns, then rewr… |

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

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| val-272 | 1 | 1 (0.17) | 1 (0.17) | 0 (0.74) | 0 (0.71) | 1 (0.21) | 0 (0.77) | 1 (0.26) | 0 (0.75) | 0 (0.82) | 0 (0.86) | 1 (0.24) | 0 (0.62) | 0 (0.95) | 0 (0.76) | 1 (0.19) | 0 (1.00) | 0 (0.86) | 0 (0.95) | 0 (0.80) | User: I want to make a cell of excel  Calculate the number of Link wo… |
| val-466 | 0 | 1 (0.13) | 1 (0.16) | 1 (0.21) | 1 (0.23) | 0 (0.85) | 0 (0.94) | 0 (0.84) | 0 (0.88) | 0 (0.98) | 0 (0.88) | 0 (0.89) | 1 (0.33) | 0 (0.98) | 0 (0.75) | 2 (0.23) | 0 (1.00) | 0 (0.89) | 0 (0.91) | 0 (0.89) | User: rewrite as a sales flyer:  27 Notch Shopping Center Dr Branson … |
| val-957 | 0 | 1 (0.22) | 0 (0.85) | 0 (0.82) | 0 (0.71) | 1 (0.20) | 0 (0.91) | 1 (0.16) | 0 (0.86) | 0 (0.93) | 0 (0.85) | 1 (0.14) | 1 (0.30) | 0 (0.81) | 0 (0.75) | 1 (0.17) | 0 (1.00) | 0 (0.85) | 0 (0.92) | 0 (0.80) | User: do you know the english word drama  Assistant: Yes, I know the … |
| val-888 | 0 | 0 (0.81) | 0 (0.77) | 0 (0.93) | 0 (0.92) | 0 (0.92) | 0 (0.97) | 1 (0.15) | 0 (0.94) | 0 (1.00) | 0 (0.96) | 0 (0.90) | 0 (0.80) | 0 (0.96) | 1 (0.17) | 1 (0.21) | 0 (0.99) | 0 (0.98) | 0 (1.00) | 0 (0.93) | User: I want to get a shop selling merch based on my artwork online. … |
| val-777 | 3 | 4 (0.77) | 4 (0.76) | 4 (0.78) | 4 (0.77) | 3 (0.36) | 4 (0.82) | 4 (0.73) | 4 (0.88) | 4 (0.88) | 4 (0.82) | 4 (0.85) | 4 (0.73) | 3 (0.37) | 4 (0.71) | 3 (0.23) | 4 (0.94) | 4 (0.88) | 4 (0.85) | 4 (0.99) | User: Using the information from the reference text, find the percent… |
| val-24 | 1 | 3 (0.27) | 1 (0.21) | 1 (0.26) | 1 (0.35) | 1 (0.29) | 1 (0.36) | 2 (0.23) | 1 (0.30) | 0 (0.75) | 1 (0.21) | 1 (0.18) | 1 (0.29) | 0 (0.77) | 2 (0.20) | 2 (0.25) | 0 (0.99) | 1 (0.22) | 1 (0.21) | 1 (0.15) | User: Please provide the equation to calculate the moment of inertia … |
| val-287 | 1 | 2 (0.27) | 2 (0.23) | 1 (0.27) | 1 (0.32) | 1 (0.32) | 0 (0.71) | 2 (0.25) | 1 (0.31) | 0 (0.84) | 1 (0.27) | 1 (0.25) | 1 (0.45) | 1 (0.50) | 1 (0.20) | 2 (0.18) | 0 (0.99) | 1 (0.27) | 1 (0.37) | 0 (0.92) | User: Give me 10 different, unique and convincing value propositions … |
| val-323 | 0 | 1 (0.13) | 1 (0.13) | 0 (0.78) | 0 (0.89) | 0 (0.88) | 0 (0.90) | 1 (0.15) | 0 (0.92) | 0 (0.94) | 0 (0.93) | 0 (0.88) | 0 (0.74) | 0 (0.97) | 0 (0.89) | 1 (0.12) | 0 (0.99) | 0 (0.94) | 0 (0.98) | 0 (0.93) | User: A heated rap battle between Eminem and 2pac. Both artists rap a… |
| val-328 | 2 | 2 (0.21) | 2 (0.25) | 1 (0.31) | 2 (0.32) | 2 (0.32) | 2 (0.29) | 2 (0.24) | 2 (0.36) | 1 (0.35) | 2 (0.33) | 2 (0.31) | 1 (0.41) | 1 (0.55) | 2 (0.25) | 2 (0.21) | 0 (0.99) | 2 (0.26) | 2 (0.40) | 1 (0.17) | User: I have a model which is trained with input shape of (5,20) and … |
| val-663 | 0 | 3 (0.21) | 1 (0.16) | 1 (0.22) | 1 (0.24) | 1 (0.25) | 0 (0.78) | 1 (0.20) | 0 (0.74) | 0 (0.90) | 0 (0.76) | 0 (0.83) | 1 (0.33) | 0 (0.86) | 2 (0.17) | 2 (0.23) | 0 (0.99) | 0 (0.85) | 0 (0.88) | 1 (0.17) | User: which soldier was awarded the param vir chakra after he was mar… |
| val-611 | 2 | 4 (0.75) | 4 (0.85) | 3 (0.54) | 3 (0.38) | 4 (0.63) | 4 (0.71) | 3 (0.34) | 4 (0.65) | 3 (0.56) | 4 (0.66) | 4 (0.67) | 3 (0.36) | 3 (0.63) | 3 (0.32) | 3 (0.31) | 3 (0.47) | 3 (0.33) | 4 (0.65) | 4 (0.99) | User: Does the human body regenerate itself? |
| val-759 | 0 | 1 (0.17) | 1 (0.08) | 1 (0.17) | 1 (0.16) | 1 (0.18) | 1 (0.09) | 1 (0.23) | 0 (0.94) | 0 (0.95) | 0 (0.92) | 0 (0.75) | 1 (0.26) | 1 (0.30) | 0 (0.83) | 1 (0.15) | 0 (0.92) | 0 (0.83) | 0 (0.98) | 4 (0.82) | User: Adesewa is a 22-year-old lawyer who has 4 schools on her list o… |
