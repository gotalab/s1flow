# helpsteer2-helpfulness

2026-11-11 · 210 labelled dev cases (2 42, 4 42, 1 42, 3 42, 0 42) · split: stratified k-fold (no test case among these: CV numbers only) · source: NVIDIA HelpSteer2 (CC BY 4.0), validation split: 60 responses per helpfulness level, under 4,000 characters

No model meets the constraints (drex-max@openrouter: different answered dev cases; automatic comparison refused; reflex@openrouter: different answered dev cases; automatic comparison refused; decision-1@openrouter: different answered dev cases; automatic comparison refused; decider@openrouter: different answered dev cases; automatic comparison refused; mammoth@openrouter: different answered dev cases; automatic comparison refused; gemini-decision@openrouter: different answered dev cases; automatic comparison refused; d1-ultra@openrouter: different answered dev cases; automatic comparison refused; jev:1.14: different answered dev cases; automatic comparison refused; elephant@openrouter: different answered dev cases; automatic comparison refused; luna@decisions: different answered dev cases; automatic comparison refused; clef@openrouter: different answered dev cases; automatic comparison refused; d1@vercel: different answered dev cases; automatic comparison refused; d1.1@openrouter: different answered dev cases; automatic comparison refused; decider-flash@openrouter: different answered dev cases; automatic comparison refused; joey@openrouter: different answered dev cases; automatic comparison refused; kev@openrouter: different answered dev cases; automatic comparison refused; span@openrouter: different answered dev cases; automatic comparison refused; clef-omni@openrouter: different answered dev cases; automatic comparison refused; clef-flash@openrouter: different answered dev cases; automatic comparison refused).

## Comparison

| model | scored | accuracy (all) | MAE (levels) | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 25.7% [20, 31] | 1.23 | 0.71 | 0.08 | 1% [0, 3] | 0.0% (0.0%) | 0/210 | 0/210 |
| clef-omni@openrouter | 210 | 28.6% [22, 34] | 1.15 | 0.80 | 0.15 | 0% [0, 1] | 0.0% (0.0%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 28.1% [22, 34] | 0.94 | 0.82 | 0.12 | 1% [0, 3] | 66.7% (13.5%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 29.5% [23, 36] | 0.87 | 0.87 | 0.10 | 0% [0, 1] | 0.0% (0.0%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 27.6% [21, 34] | 0.99 | 0.85 | 0.12 | 1% [0, 2] | 100.0% (22.4%) | 0/210 | 0/210 |
| d1@vercel | 210 | 32.4% [26, 39] | 0.99 | 0.85 | 0.11 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 25.7% [20, 32] | 1.04 | 0.81 | 0.11 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 36.2% [30, 43] | 0.81 | 0.87 | 0.08 | 2% [0, 4] | 75.0% (24.9%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 38.1% [31, 44] | 0.81 | 0.86 | 0.13 | 2% [0, 5] | 80.0% (34.3%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 41.0% [34, 47] | 0.75 | 0.88 | 0.05 | 2% [0, 5] | 80.0% (34.3%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 33.3% [27, 40] | 0.91 | 0.85 | 0.07 | 2% [0, 5] | 80.0% (34.3%) | 0/210 | 0/210 |
| gemini-decision@openrouter | 210 | 34.3% [28, 40] | 0.85 | 0.85 | 0.06 | 1% [0, 3] | 33.3% (1.7%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 31.4% [25, 38] | 0.89 | 0.82 | 0.22 | 4% [2, 7] | 66.7% (34.5%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 26.2% [21, 32] | 1.09 | 0.73 | 0.10 | 1% [0, 2] | 50.0% (2.5%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 22.9% [17, 29] | 1.14 | 0.73 | 0.07 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| luna@decisions | 209 | 37.3% [31, 44] | 0.92 | 0.78 | 0.29 | 1% [0, 2] | 50.0% (2.5%) | 1/210 | 0/210 |
| mammoth@openrouter | 210 | 34.8% [29, 41] | 0.82 | 0.88 | 0.03 | 1% [0, 2] | 100.0% (22.4%) | 0/210 | 0/210 |
| reflex@openrouter | 210 | 41.0% [34, 47] | 0.79 | 0.85 | 0.14 | 3% [1, 5] | 83.3% (41.8%) | 0/210 | 0/210 |
| span@openrouter | 210 | 32.4% [26, 40] | 1.14 | 0.80 | 0.35 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | MAE (levels) | QWK | accuracy (all) | rule | constraints |
|---|---|---|---|---|---|
| drex-max@openrouter | 0.752 [0.680, 0.827] | 0.694 [0.623, 0.755] | 41% [34, 47] | — | different answered dev cases; automatic comparison refused |
| reflex@openrouter | 0.790 [0.699, 0.883] | 0.643 [0.556, 0.722] | 41% [34, 47] | — | different answered dev cases; automatic comparison refused |
| decision-1@openrouter | 0.808 [0.731, 0.889] | 0.677 [0.606, 0.739] | 38% [31, 44] | — | different answered dev cases; automatic comparison refused |
| decider@openrouter | 0.812 [0.735, 0.891] | 0.641 [0.565, 0.705] | 36% [30, 43] | — | different answered dev cases; automatic comparison refused |
| mammoth@openrouter | 0.818 [0.736, 0.900] | 0.622 [0.541, 0.692] | 35% [29, 41] | — | different answered dev cases; automatic comparison refused |
| gemini-decision@openrouter | 0.846 [0.764, 0.927] | 0.606 [0.529, 0.681] | 34% [28, 40] | — | different answered dev cases; automatic comparison refused |
| d1-ultra@openrouter | 0.868 [0.792, 0.948] | 0.566 [0.490, 0.637] | 30% [23, 36] | — | different answered dev cases; automatic comparison refused |
| jev:1.14 | 0.893 [0.810, 0.977] | 0.563 [0.470, 0.646] | 31% [25, 38] | — | different answered dev cases; automatic comparison refused |
| elephant@openrouter | 0.909 [0.820, 1.000] | 0.544 [0.454, 0.624] | 33% [27, 40] | — | different answered dev cases; automatic comparison refused |
| luna@decisions | 0.921 [0.827, 1.024] | 0.535 [0.432, 0.620] | 37% [31, 44] | — | different answered dev cases; automatic comparison refused |
| clef@openrouter | 0.941 [0.849, 1.029] | 0.483 [0.388, 0.566] | 28% [22, 34] | — | different answered dev cases; automatic comparison refused |
| d1@vercel | 0.987 [0.886, 1.096] | 0.530 [0.440, 0.607] | 32% [26, 39] | — | different answered dev cases; automatic comparison refused |
| d1.1@openrouter | 0.993 [0.893, 1.094] | 0.446 [0.361, 0.531] | 28% [21, 34] | — | different answered dev cases; automatic comparison refused |
| decider-flash@openrouter | 1.038 [0.933, 1.146] | 0.380 [0.294, 0.461] | 26% [20, 32] | — | different answered dev cases; automatic comparison refused |
| joey@openrouter | 1.092 [0.988, 1.199] | 0.320 [0.216, 0.425] | 26% [21, 32] | — | different answered dev cases; automatic comparison refused |
| kev@openrouter | 1.136 [1.025, 1.234] | 0.265 [0.180, 0.350] | 23% [17, 29] | — | different answered dev cases; automatic comparison refused |
| span@openrouter | 1.144 [1.007, 1.277] | 0.428 [0.334, 0.523] | 32% [26, 40] | — | different answered dev cases; automatic comparison refused |
| clef-omni@openrouter | 1.147 [1.023, 1.270] | 0.409 [0.322, 0.498] | 29% [22, 34] | — | different answered dev cases; automatic comparison refused |
| clef-flash@openrouter | 1.226 [1.091, 1.348] | 0.229 [0.145, 0.325] | 26% [20, 31] | — | different answered dev cases; automatic comparison refused |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 350 ms | 503 ms | 1987 ms | 2660 ms | 5.7 | 0 | 4 | $0.16 | billed |  |
| clef-omni@openrouter | 210 | 201 ms | 328 ms | 1002 ms | 1207 ms | 5.0 | 0 | 4 | $1.02 | billed |  |
| clef@openrouter | 210 | 467 ms | 834 ms | 1634 ms | 1703 ms | 3.5 | 0 | 4 | $1.51 | billed |  |
| d1-ultra@openrouter | 210 | 262 ms | 383 ms | 539 ms | 892 ms | 2.1 | 0 | 4 | $0.24 | billed |  |
| d1.1@openrouter | 210 | 321 ms | 473 ms | 592 ms | 667 ms | 1.8 | 0 | 4 | $0.11 | billed | ○ |
| d1@vercel | 210 | 330 ms | 431 ms | 623 ms | 704 ms | 1.9 | 0 | 4 | $0.11 | billed | ○ |
| decider-flash@openrouter | 210 | 240 ms | 275 ms | 498 ms | 770 ms | 2.1 | 2 | 4 | $0.06 | billed | ○ |
| decider@openrouter | 210 | 312 ms | 624 ms | 1548 ms | 3587 ms | 5.0 | 0 | 4 | $0.12 | billed | ○ |
| decision-1@openrouter | 210 | 363 ms | 445 ms | 519 ms | 665 ms | 1.4 | 0 | 4 | $0.23 | billed | ○ |
| drex-max@openrouter | 210 | 346 ms | 539 ms | 1006 ms | 1203 ms | 2.9 | 0 | 4 | $0.36 | billed | ○ |
| elephant@openrouter | 210 | 277 ms | 324 ms | 438 ms | 663 ms | 1.6 | 0 | 4 | $0.22 | billed | ○ |
| gemini-decision@openrouter | 210 | 338 ms | 476 ms | 615 ms | 716 ms | 1.8 | 0 | 4 | $0.62 | billed |  |
| jev:1.14 | 210 | 200 ms | 242 ms | 280 ms | 441 ms | 1.4 | 0 | 4 | $0.34 | estimated | ○ |
| joey@openrouter | 210 | 180 ms | 305 ms | 385 ms | 547 ms | 2.1 | 0 | 4 | $0.06 | billed | ○ |
| kev@openrouter | 210 | 650 ms | 770 ms | 1034 ms | 1123 ms | 1.6 | 3 | 4 | $0.22 | billed |  |
| luna@decisions | 209 | 304 ms | 469 ms | 643 ms | 798 ms | 2.1 | 0 | 4 | $0.63 | estimated |  |
| mammoth@openrouter | 210 | 201 ms | 319 ms | 487 ms | 655 ms | 2.4 | 0 | 4 | $0.63 | billed | ○ |
| reflex@openrouter | 210 | 299 ms | 416 ms | 492 ms | 764 ms | 1.6 | 0 | 4 | $0.26 | billed | ○ |
| span@openrouter | 210 | 550 ms | 989 ms | 1220 ms | 1464 ms | 2.2 | 0 | 4 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0034 | 21 s (estimated, 210 calls) | 17 min | 4 |
| clef-omni@openrouter | $0.02 | 13 s (estimated, 210 calls) | 10 min | 4 |
| clef@openrouter | $0.03 | 28 s (estimated, 210 calls) | 22 min | 4 |
| d1-ultra@openrouter | $0.0050 | 15 s (estimated, 210 calls) | 12 min | 4 |
| d1.1@openrouter | $0.0024 | 17 s (estimated, 210 calls) | 14 min | 4 |
| d1@vercel | $0.0024 | 17 s (estimated, 210 calls) | 14 min | 4 |
| decider-flash@openrouter | $0.0013 | 12 s (estimated, 210 calls) | 9 min | 4 |
| decider@openrouter | $0.0025 | 20 s (estimated, 210 calls) | 16 min | 4 |
| decision-1@openrouter | $0.0047 | 18 s (estimated, 210 calls) | 15 min | 4 |
| drex-max@openrouter | $0.0076 | 20 s (estimated, 210 calls) | 16 min | 4 |
| elephant@openrouter | $0.0047 | 14 s (estimated, 210 calls) | 11 min | 4 |
| gemini-decision@openrouter | $0.01 | 18 s (estimated, 210 calls) | 15 min | 4 |
| jev:1.14 | $0.0072 | 9 s (estimated, 210 calls) | 7 min | 4 |
| joey@openrouter | $0.0013 | 11 s (estimated, 210 calls) | 9 min | 4 |
| kev@openrouter | $0.0046 | 35 s (estimated, 210 calls) | 28 min | 4 |
| luna@decisions | $0.01 | 17 s (estimated, 209 calls) | 13 min | 4 |
| mammoth@openrouter | $0.01 | 13 s (estimated, 210 calls) | 10 min | 4 |
| reflex@openrouter | $0.0054 | 17 s (estimated, 210 calls) | 13 min | 4 |
| span@openrouter | $0.0013 | 33 s (estimated, 210 calls) | 26 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Wrong at a high probability (0.9 or more)

**clef-omni@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-65 | 0 | 4 | 0.91 | User: Can you tell me how to make a Trident cocktail? |

**decision-1@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-774 | 1 | 0 | 0.93 | User: Answer #4's subject, object, and possessive pronouns, then rewr… |

**jev:1.14** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-272 | 1 | 0 | 0.93 | User: I want to make a cell of excel  Calculate the number of Link wo… |

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
| val-777 | 3 | 4 | 0.94 | User: Using the information from the reference text, find the percent… |

**reflex@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-272 | 1 | 0 | 0.96 | User: I want to make a cell of excel  Calculate the number of Link wo… |

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


## Cases the models disagree on (12 of 209)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| val-272 | 1 | 1 (0.17) | 1 (0.17) | 0 (0.74) | 0 (0.70) | 1 (0.20) | 0 (0.85) | 1 (0.26) | 0 (0.76) | 0 (0.82) | 0 (0.86) | 1 (0.24) | 1 (0.33) | 0 (0.93) | 0 (0.76) | 1 (0.19) | 0 (1.00) | 0 (0.86) | 0 (0.96) | 0 (0.80) | User: I want to make a cell of excel  Calculate the number of Link wo… |
| val-466 | 0 | 1 (0.16) | 1 (0.16) | 1 (0.19) | 0 (0.68) | 0 (0.88) | 0 (0.96) | 0 (0.84) | 0 (0.88) | 0 (0.98) | 0 (0.86) | 0 (0.89) | 1 (0.37) | 0 (0.97) | 0 (0.75) | 2 (0.23) | 0 (1.00) | 0 (0.89) | 0 (0.91) | 0 (0.84) | User: rewrite as a sales flyer:  27 Notch Shopping Center Dr Branson … |
| val-957 | 0 | 1 (0.23) | 0 (0.85) | 0 (0.82) | 0 (0.73) | 1 (0.25) | 0 (0.88) | 1 (0.16) | 0 (0.86) | 0 (0.95) | 0 (0.89) | 1 (0.14) | 0 (0.62) | 0 (0.74) | 0 (0.75) | 1 (0.17) | 0 (1.00) | 0 (0.85) | 0 (0.91) | 0 (0.84) | User: do you know the english word drama  Assistant: Yes, I know the … |
| val-888 | 0 | 0 (0.81) | 0 (0.77) | 0 (0.93) | 0 (0.92) | 0 (0.92) | 0 (0.95) | 1 (0.15) | 0 (0.93) | 0 (1.00) | 0 (0.96) | 0 (0.90) | 0 (0.81) | 0 (0.96) | 1 (0.17) | 1 (0.22) | 0 (0.99) | 0 (0.98) | 0 (1.00) | 0 (0.93) | User: I want to get a shop selling merch based on my artwork online. … |
| val-777 | 3 | 4 (0.77) | 4 (0.76) | 4 (0.78) | 4 (0.78) | 3 (0.36) | 4 (0.82) | 4 (0.73) | 4 (0.86) | 4 (0.88) | 4 (0.85) | 4 (0.85) | 4 (0.75) | 3 (0.38) | 4 (0.71) | 3 (0.24) | 4 (0.94) | 4 (0.88) | 4 (0.84) | 4 (0.99) | User: Using the information from the reference text, find the percent… |
| val-24 | 1 | 3 (0.26) | 1 (0.21) | 1 (0.27) | 1 (0.32) | 1 (0.27) | 1 (0.22) | 2 (0.23) | 1 (0.29) | 0 (0.75) | 1 (0.17) | 1 (0.18) | 1 (0.33) | 0 (0.74) | 2 (0.20) | 2 (0.25) | 0 (0.99) | 1 (0.22) | 1 (0.21) | 1 (0.14) | User: Please provide the equation to calculate the moment of inertia … |
| val-287 | 1 | 2 (0.27) | 2 (0.23) | 1 (0.27) | 2 (0.24) | 1 (0.29) | 0 (0.72) | 2 (0.25) | 1 (0.31) | 0 (0.82) | 1 (0.27) | 1 (0.25) | 1 (0.46) | 1 (0.50) | 1 (0.20) | 2 (0.18) | 0 (0.99) | 1 (0.27) | 1 (0.38) | 0 (0.92) | User: Give me 10 different, unique and convincing value propositions … |
| val-323 | 0 | 1 (0.13) | 1 (0.13) | 0 (0.77) | 0 (0.90) | 0 (0.81) | 0 (0.84) | 1 (0.15) | 0 (0.92) | 0 (0.94) | 0 (0.92) | 0 (0.88) | 0 (0.74) | 0 (0.97) | 0 (0.89) | 1 (0.12) | 0 (0.99) | 0 (0.94) | 0 (0.96) | 0 (0.93) | User: A heated rap battle between Eminem and 2pac. Both artists rap a… |
| val-328 | 2 | 2 (0.26) | 2 (0.25) | 1 (0.30) | 2 (0.32) | 2 (0.25) | 2 (0.31) | 2 (0.24) | 2 (0.36) | 1 (0.35) | 2 (0.33) | 2 (0.31) | 1 (0.40) | 1 (0.54) | 2 (0.25) | 2 (0.21) | 0 (0.99) | 2 (0.26) | 3 (0.41) | 1 (0.17) | User: I have a model which is trained with input shape of (5,20) and … |
| val-663 | 0 | 3 (0.21) | 1 (0.16) | 1 (0.23) | 0 (0.64) | 1 (0.25) | 0 (0.73) | 1 (0.20) | 0 (0.74) | 0 (0.90) | 0 (0.83) | 0 (0.83) | 1 (0.36) | 0 (0.85) | 2 (0.17) | 2 (0.23) | 0 (0.99) | 0 (0.85) | 0 (0.90) | 1 (0.17) | User: which soldier was awarded the param vir chakra after he was mar… |
| val-611 | 2 | 4 (0.76) | 4 (0.85) | 3 (0.53) | 3 (0.40) | 4 (0.60) | 4 (0.69) | 3 (0.34) | 4 (0.65) | 3 (0.56) | 4 (0.66) | 4 (0.67) | 3 (0.32) | 3 (0.62) | 3 (0.32) | 3 (0.31) | 3 (0.47) | 3 (0.33) | 3 (0.46) | 4 (0.99) | User: Does the human body regenerate itself? |
| val-759 | 0 | 1 (0.17) | 1 (0.08) | 1 (0.16) | 1 (0.14) | 2 (0.20) | 1 (0.09) | 1 (0.23) | 0 (0.94) | 0 (0.95) | 0 (0.93) | 0 (0.75) | 1 (0.29) | 1 (0.29) | 0 (0.83) | 1 (0.15) | 0 (0.92) | 0 (0.83) | 0 (0.98) | 4 (0.82) | User: Adesewa is a 22-year-old lawyer who has 4 schools on her list o… |
