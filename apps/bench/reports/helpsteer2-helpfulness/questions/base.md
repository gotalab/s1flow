# helpsteer2-helpfulness

2026-10-31 · 210 labelled dev cases (2 42, 4 42, 1 42, 3 42, 0 42) · split: stratified k-fold (no test case among these: CV numbers only) · source: NVIDIA HelpSteer2 (CC BY 4.0), validation split: 60 responses per helpfulness level, under 4,000 characters

No model meets the constraints (drex-max@openrouter: different answered dev cases; automatic comparison refused; decision-1@openrouter: different answered dev cases; automatic comparison refused; decider@openrouter: different answered dev cases; automatic comparison refused; mammoth@openrouter: different answered dev cases; automatic comparison refused; mercury@openrouter: different answered dev cases; automatic comparison refused; d1-ultra@openrouter: different answered dev cases; automatic comparison refused; jev:1.14: different answered dev cases; automatic comparison refused; elephant@openrouter: different answered dev cases; automatic comparison refused; luna@decisions: different answered dev cases; automatic comparison refused; clef@openrouter: different answered dev cases; automatic comparison refused; d1.1@openrouter: different answered dev cases; automatic comparison refused; d1@vercel: different answered dev cases; automatic comparison refused; decider-flash@openrouter: different answered dev cases; automatic comparison refused; joey@openrouter: different answered dev cases; automatic comparison refused; span@openrouter: different answered dev cases; automatic comparison refused; kev@openrouter: different answered dev cases; automatic comparison refused; clef-flash@openrouter: different answered dev cases; automatic comparison refused).

## Comparison

| model | scored | accuracy | MAE | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 25.7% [20, 31] | 1.22 | 0.71 | 0.10 | 1% [0, 2] | 0.0% (0.0%) | 0/210 | 0/210 |
| clef@openrouter | 210 | 29.5% [23, 36] | 0.94 | 0.82 | 0.11 | 1% [0, 3] | 66.7% (13.5%) | 0/210 | 0/210 |
| d1-ultra@openrouter | 210 | 31.0% [25, 38] | 0.87 | 0.87 | 0.09 | 1% [0, 2] | 0.0% (0.0%) | 0/210 | 0/210 |
| d1.1@openrouter | 210 | 25.7% [20, 31] | 0.99 | 0.85 | 0.13 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| d1@vercel | 210 | 31.0% [25, 37] | 1.00 | 0.85 | 0.12 | 1% [0, 2] | 50.0% (2.5%) | 0/210 | 0/210 |
| decider-flash@openrouter | 210 | 25.7% [20, 31] | 1.04 | 0.81 | 0.11 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| decider@openrouter | 210 | 36.2% [30, 43] | 0.81 | 0.87 | 0.09 | 1% [0, 3] | 66.7% (13.5%) | 0/210 | 0/210 |
| decision-1@openrouter | 210 | 38.1% [32, 45] | 0.81 | 0.86 | 0.13 | 3% [1, 6] | 85.7% (47.9%) | 0/210 | 0/210 |
| drex-max@openrouter | 210 | 39.5% [33, 46] | 0.75 | 0.88 | 0.05 | 3% [1, 5] | 83.3% (41.8%) | 0/210 | 0/210 |
| elephant@openrouter | 210 | 32.9% [27, 39] | 0.91 | 0.85 | 0.06 | 3% [1, 6] | 85.7% (47.9%) | 0/210 | 0/210 |
| jev:1.14 | 210 | 32.9% [27, 40] | 0.89 | 0.82 | 0.20 | 2% [1, 5] | 80.0% (34.3%) | 0/210 | 0/210 |
| joey@openrouter | 210 | 25.2% [20, 31] | 1.09 | 0.73 | 0.11 | 1% [0, 2] | 50.0% (2.5%) | 0/210 | 0/210 |
| kev@openrouter | 210 | 22.4% [17, 28] | 1.14 | 0.73 | 0.07 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| luna@decisions | 209 | 37.3% [31, 44] | 0.92 | 0.78 | 0.29 | 1% [0, 2] | 50.0% (2.5%) | 1/210 | 0/210 |
| mammoth@openrouter | 210 | 34.8% [29, 41] | 0.81 | 0.88 | 0.04 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |
| mercury@openrouter | 210 | 39.5% [32, 46] | 0.85 | 0.84 | 0.20 | 2% [0, 5] | 80.0% (34.3%) | 0/210 | 0/210 |
| span@openrouter | 210 | 32.4% [26, 39] | 1.13 | 0.80 | 0.35 | 0% [0, 0] | — (0.0%) | 0/210 | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | MAE (levels) | QWK | accuracy (all) | rule | constraints |
|---|---|---|---|---|---|
| drex-max@openrouter | 0.747 [0.667, 0.823] | 0.696 [0.623, 0.759] | 40% [33, 46] | — | different answered dev cases; automatic comparison refused |
| decision-1@openrouter | 0.809 [0.730, 0.894] | 0.674 [0.603, 0.735] | 38% [32, 45] | — | different answered dev cases; automatic comparison refused |
| decider@openrouter | 0.810 [0.733, 0.886] | 0.649 [0.573, 0.719] | 36% [30, 43] | — | different answered dev cases; automatic comparison refused |
| mammoth@openrouter | 0.814 [0.736, 0.897] | 0.624 [0.543, 0.697] | 35% [29, 41] | — | different answered dev cases; automatic comparison refused |
| mercury@openrouter | 0.850 [0.751, 0.942] | 0.636 [0.548, 0.721] | 40% [32, 46] | — | different answered dev cases; automatic comparison refused |
| d1-ultra@openrouter | 0.867 [0.787, 0.942] | 0.583 [0.503, 0.656] | 31% [25, 38] | — | different answered dev cases; automatic comparison refused |
| jev:1.14 | 0.892 [0.802, 0.977] | 0.569 [0.482, 0.656] | 33% [27, 40] | — | different answered dev cases; automatic comparison refused |
| elephant@openrouter | 0.910 [0.816, 1.000] | 0.538 [0.441, 0.627] | 33% [27, 39] | — | different answered dev cases; automatic comparison refused |
| luna@decisions | 0.921 [0.827, 1.021] | 0.535 [0.434, 0.611] | 37% [31, 44] | — | different answered dev cases; automatic comparison refused |
| clef@openrouter | 0.936 [0.850, 1.016] | 0.493 [0.405, 0.578] | 30% [23, 36] | — | different answered dev cases; automatic comparison refused |
| d1.1@openrouter | 0.992 [0.896, 1.088] | 0.463 [0.383, 0.546] | 26% [20, 31] | — | different answered dev cases; automatic comparison refused |
| d1@vercel | 0.999 [0.893, 1.100] | 0.522 [0.443, 0.604] | 31% [25, 37] | — | different answered dev cases; automatic comparison refused |
| decider-flash@openrouter | 1.038 [0.935, 1.142] | 0.380 [0.296, 0.457] | 26% [20, 31] | — | different answered dev cases; automatic comparison refused |
| joey@openrouter | 1.093 [0.992, 1.211] | 0.314 [0.203, 0.414] | 25% [20, 31] | — | different answered dev cases; automatic comparison refused |
| span@openrouter | 1.131 [0.997, 1.275] | 0.438 [0.334, 0.536] | 32% [26, 39] | — | different answered dev cases; automatic comparison refused |
| kev@openrouter | 1.137 [1.031, 1.230] | 0.255 [0.167, 0.337] | 22% [17, 28] | — | different answered dev cases; automatic comparison refused |
| clef-flash@openrouter | 1.223 [1.098, 1.348] | 0.238 [0.153, 0.331] | 26% [20, 31] | — | different answered dev cases; automatic comparison refused |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 1004 ms | 2047 ms | 3097 ms | 4250 ms | 3.1 | 0 | 8 | $0.15 | billed |  |
| clef@openrouter | 210 | 889 ms | 1882 ms | 4636 ms | 7990 ms | 5.2 | 0 | 8 | $1.48 | billed |  |
| d1-ultra@openrouter | 210 | 827 ms | 1889 ms | 4852 ms | 7953 ms | 5.9 | 0 | 8 | $0.24 | billed |  |
| d1.1@openrouter | 210 | 756 ms | 1977 ms | 4984 ms | 7995 ms | 6.6 | 0 | 8 | $0.11 | billed | ○ |
| d1@vercel | 210 | 884 ms | 1167 ms | 3060 ms | 5015 ms | 3.5 | 0 | 8 | $0.11 | billed | ○ |
| decider-flash@openrouter | 210 | 708 ms | 1682 ms | 3675 ms | 3819 ms | 5.2 | 0 | 8 | $0.06 | billed | ○ |
| decider@openrouter | 210 | 818 ms | 1826 ms | 4008 ms | 4922 ms | 4.9 | 0 | 8 | $0.12 | billed | ○ |
| decision-1@openrouter | 210 | 892 ms | 1574 ms | 3873 ms | 4893 ms | 4.3 | 0 | 8 | $0.23 | billed | ○ |
| drex-max@openrouter | 210 | 887 ms | 1973 ms | 4375 ms | 5631 ms | 4.9 | 10 | 8 | $0.36 | billed | ○ |
| elephant@openrouter | 210 | 779 ms | 1779 ms | 3826 ms | 5008 ms | 4.9 | 0 | 8 | $0.22 | billed | ○ |
| jev:1.14 | 210 | 716 ms | 1795 ms | 4673 ms | 4769 ms | 6.5 | 0 | 8 | $0.34 | estimated |  |
| joey@openrouter | 210 | 765 ms | 1898 ms | 4788 ms | 5073 ms | 6.3 | 0 | 8 | $0.06 | billed |  |
| kev@openrouter | 210 | 971 ms | 1827 ms | 3385 ms | 7813 ms | 3.5 | 0 | 8 | $0.22 | billed |  |
| luna@decisions | 209 | 841 ms | 1793 ms | 3747 ms | 4879 ms | 4.5 | 1 | 8 | $0.63 | estimated | ○ |
| mammoth@openrouter | 210 | 1402 ms | 4112 ms | 6053 ms | 9785 ms | 4.3 | 0 | 8 | $0.63 | billed |  |
| mercury@openrouter | 210 | 886 ms | 1893 ms | 4948 ms | 8014 ms | 5.6 | 0 | 8 | $0.12 | billed |  |
| span@openrouter | 210 | 950 ms | 1971 ms | 4916 ms | 8469 ms | 5.2 | 0 | 8 | $0.06 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0032 | 30 s (estimated, 210 calls) | 24 min | 8 |
| clef@openrouter | $0.03 | 29 s (estimated, 210 calls) | 23 min | 8 |
| d1-ultra@openrouter | $0.0050 | 30 s (estimated, 210 calls) | 24 min | 8 |
| d1.1@openrouter | $0.0024 | 29 s (estimated, 210 calls) | 23 min | 8 |
| d1@vercel | $0.0024 | 26 s (estimated, 210 calls) | 21 min | 8 |
| decider-flash@openrouter | $0.0013 | 24 s (estimated, 210 calls) | 19 min | 8 |
| decider@openrouter | $0.0025 | 28 s (estimated, 210 calls) | 22 min | 8 |
| decision-1@openrouter | $0.0047 | 28 s (estimated, 210 calls) | 22 min | 8 |
| drex-max@openrouter | $0.0076 | 27 s (estimated, 210 calls) | 22 min | 8 |
| elephant@openrouter | $0.0047 | 27 s (estimated, 210 calls) | 21 min | 8 |
| jev:1.14 | $0.0072 | 26 s (estimated, 210 calls) | 20 min | 8 |
| joey@openrouter | $0.0013 | 28 s (estimated, 210 calls) | 22 min | 8 |
| kev@openrouter | $0.0046 | 29 s (estimated, 210 calls) | 23 min | 8 |
| luna@decisions | $0.01 | 28 s (estimated, 209 calls) | 22 min | 8 |
| mammoth@openrouter | $0.01 | 49 s (estimated, 210 calls) | 39 min | 8 |
| mercury@openrouter | $0.0025 | 29 s (estimated, 210 calls) | 23 min | 8 |
| span@openrouter | $0.0013 | 31 s (estimated, 210 calls) | 25 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Wrong at a high probability (0.9 or more)

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
| val-328 | 2 | 0 | 0.99 | User: I have a model which is trained with input shape of (5,20) and … |
| val-287 | 1 | 0 | 0.99 | User: Give me 10 different, unique and convincing value propositions … |
| val-24 | 1 | 0 | 0.99 | User: Please provide the equation to calculate the moment of inertia … |
| val-136 | 2 | 1 | 0.97 | User: Write a story about a bald headed technology gremlin called Mat… |
| val-590 | 3 | 4 | 0.96 | User: Im creating a school website otonokizaka national high school c… |
| val-462 | 3 | 1 | 0.95 | User: Taking into account the scientific, psychological, phylosophica… |
| val-317 | 0 | 1 | 0.94 | User: how can I get around Asturias Spain when on vacation?  Assistan… |

**mercury@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| val-777 | 3 | 4 | 0.99 | User: Using the information from the reference text, find the percent… |
| val-82 | 2 | 4 | 0.92 | User: Make up the synopsis for 5 new Seinfeld episodes |
| val-401 | 3 | 4 | 0.90 | User: 1. Pertanyaan #1 What practice involves identifying, defining, … |

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

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| val-272 | 1 | 1 (0.17) | 0 (0.76) | 0 (0.75) | 1 (0.17) | 0 (0.81) | 1 (0.26) | 0 (0.72) | 0 (0.80) | 0 (0.86) | 1 (0.23) | 0 (0.93) | 0 (0.75) | 1 (0.19) | 0 (1.00) | 0 (0.85) | 0 (0.68) | 0 (0.84) | User: I want to make a cell of excel  Calculate the number of Link wo… |
| val-466 | 0 | 1 (0.14) | 1 (0.19) | 1 (0.22) | 0 (0.82) | 0 (0.97) | 0 (0.84) | 0 (0.86) | 0 (0.99) | 0 (0.88) | 0 (0.89) | 0 (0.97) | 0 (0.74) | 2 (0.23) | 0 (1.00) | 0 (0.90) | 0 (0.98) | 0 (0.91) | User: rewrite as a sales flyer:  27 Notch Shopping Center Dr Branson … |
| val-957 | 0 | 1 (0.21) | 0 (0.83) | 0 (0.74) | 1 (0.19) | 0 (0.90) | 1 (0.16) | 0 (0.86) | 0 (0.93) | 0 (0.85) | 1 (0.14) | 0 (0.76) | 0 (0.76) | 1 (0.17) | 0 (1.00) | 0 (0.82) | 0 (0.92) | 0 (0.85) | User: do you know the english word drama  Assistant: Yes, I know the … |
| val-888 | 0 | 0 (0.81) | 0 (0.93) | 0 (0.96) | 0 (0.88) | 0 (0.94) | 1 (0.15) | 0 (0.94) | 0 (1.00) | 0 (0.96) | 0 (0.91) | 0 (0.97) | 1 (0.17) | 1 (0.22) | 0 (0.99) | 0 (0.98) | 0 (0.99) | 0 (0.93) | User: I want to get a shop selling merch based on my artwork online. … |
| val-777 | 3 | 4 (0.78) | 4 (0.78) | 4 (0.76) | 3 (0.37) | 4 (0.75) | 4 (0.73) | 4 (0.87) | 4 (0.88) | 4 (0.82) | 4 (0.84) | 3 (0.38) | 4 (0.70) | 3 (0.24) | 4 (0.94) | 4 (0.87) | 4 (0.99) | 4 (0.99) | User: Using the information from the reference text, find the percent… |
| val-24 | 1 | 3 (0.27) | 1 (0.24) | 1 (0.30) | 1 (0.30) | 1 (0.23) | 2 (0.23) | 1 (0.29) | 0 (0.72) | 1 (0.19) | 1 (0.18) | 0 (0.75) | 2 (0.20) | 2 (0.25) | 0 (0.99) | 1 (0.22) | 0 (0.85) | 1 (0.13) | User: Please provide the equation to calculate the moment of inertia … |
| val-287 | 1 | 2 (0.27) | 1 (0.27) | 1 (0.32) | 1 (0.34) | 0 (0.76) | 2 (0.25) | 1 (0.30) | 0 (0.82) | 1 (0.27) | 1 (0.25) | 1 (0.48) | 2 (0.19) | 2 (0.18) | 0 (0.99) | 1 (0.27) | 0 (0.68) | 0 (0.92) | User: Give me 10 different, unique and convincing value propositions … |
| val-323 | 0 | 1 (0.15) | 0 (0.78) | 0 (0.89) | 0 (0.90) | 0 (0.91) | 1 (0.15) | 0 (0.92) | 0 (0.93) | 0 (0.93) | 0 (0.88) | 0 (0.97) | 0 (0.88) | 1 (0.12) | 0 (0.99) | 0 (0.95) | 0 (0.90) | 0 (0.93) | User: A heated rap battle between Eminem and 2pac. Both artists rap a… |
| val-328 | 2 | 2 (0.26) | 2 (0.36) | 2 (0.34) | 2 (0.33) | 2 (0.25) | 2 (0.24) | 2 (0.37) | 1 (0.35) | 2 (0.33) | 2 (0.32) | 1 (0.57) | 2 (0.25) | 2 (0.21) | 0 (0.99) | 2 (0.27) | 2 (0.46) | 1 (0.25) | User: I have a model which is trained with input shape of (5,20) and … |
| val-663 | 0 | 3 (0.20) | 1 (0.23) | 1 (0.30) | 1 (0.26) | 0 (0.81) | 1 (0.20) | 0 (0.75) | 0 (0.91) | 0 (0.81) | 0 (0.83) | 0 (0.85) | 2 (0.17) | 2 (0.22) | 0 (0.99) | 0 (0.85) | 0 (0.97) | 1 (0.14) | User: which soldier was awarded the param vir chakra after he was mar… |
| val-611 | 2 | 4 (0.76) | 3 (0.54) | 3 (0.42) | 4 (0.67) | 4 (0.74) | 3 (0.34) | 4 (0.66) | 3 (0.59) | 4 (0.68) | 4 (0.65) | 3 (0.62) | 3 (0.32) | 3 (0.32) | 3 (0.47) | 3 (0.30) | 4 (0.87) | 4 (0.99) | User: Does the human body regenerate itself? |
| val-590 | 3 | 3 (0.26) | 3 (0.34) | 3 (0.41) | 4 (0.60) | 4 (0.63) | 3 (0.43) | 4 (0.67) | 3 (0.46) | 4 (0.69) | 4 (0.65) | 3 (0.72) | 3 (0.43) | 3 (0.40) | 4 (0.96) | 4 (0.63) | 4 (0.85) | 4 (0.98) | User: Im creating a school website otonokizaka national high school c… |
