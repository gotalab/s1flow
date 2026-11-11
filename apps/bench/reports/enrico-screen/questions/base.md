# enrico-screen

2026-11-11 · 154 labelled dev cases (form 9, gallery 9, menu 9, settings 9, bare 8, chat 8, editor 8, list 8, more) · split: stratified k-fold (no test case among these: CV numbers only) · source: Enrico (labels MIT) on Rico screenshots (CC BY 4.0): up to 12 screens per design topic, mislabelled ones replaced

**decider-flash@openrouter** has the highest coverage at 95% accuracy, 49% [42, 56] (API cost $0.14 per 10k, p99 578ms). Its interval overlaps with elephant@openrouter, mammoth@openrouter, decider@openrouter, d1.1@openrouter, reflex@openrouter, d1-ultra@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. Ordered by task.py's tiebreak (accuracy (all)), **elephant@openrouter** comes first (API cost $0.52 per 10k, p99 847ms). The highest raw accuracy (dev) is elephant@openrouter's, 74% [67, 81].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 70.8% [64, 78] | 0.71 | 0.97 | 0.05 | 28% [21, 34] | 93.0% (82.9%) | 0/154 | 0/154 |
| clef-omni@openrouter | 154 | 66.2% [60, 73] | 0.67 | 0.97 | 0.13 | 23% [16, 29] | 91.4% (79.3%) | 0/154 | 0/154 |
| clef@openrouter | 154 | 70.1% [63, 77] | 0.70 | 0.98 | 0.07 | 33% [26, 41] | 94.1% (85.5%) | 0/154 | 0/154 |
| d1-ultra@openrouter | 154 | 63.0% [55, 71] | 0.64 | 0.97 | 0.08 | 35% [28, 43] | 92.6% (83.8%) | 0/154 | 0/154 |
| d1.1@openrouter | 154 | 66.9% [60, 74] | 0.68 | 0.97 | 0.11 | 36% [29, 44] | 94.5% (86.5%) | 0/154 | 0/154 |
| d1@vercel | 154 | 65.6% [58, 73] | 0.67 | 0.96 | 0.10 | 28% [21, 34] | 93.0% (82.9%) | 0/154 | 0/154 |
| decider-flash@openrouter | 154 | 69.5% [63, 77] | 0.71 | 0.98 | 0.06 | 49% [42, 56] | 94.7% (88.4%) | 0/154 | 0/154 |
| decider@openrouter | 154 | 70.8% [64, 78] | 0.72 | 0.99 | 0.06 | 46% [38, 54] | 94.4% (87.6%) | 0/154 | 0/154 |
| drex-max@openrouter | 154 | 70.8% [64, 78] | 0.71 | 0.98 | 0.06 | 30% [23, 37] | 93.5% (84.0%) | 0/154 | 0/154 |
| elephant@openrouter | 154 | 74.0% [67, 81] | 0.74 | 0.98 | 0.09 | 39% [31, 47] | 93.3% (85.4%) | 0/154 | 0/154 |
| gemini-decision@openrouter | 154 | 70.8% [64, 78] | 0.70 | 0.98 | 0.07 | 33% [25, 40] | 94.1% (85.5%) | 0/154 | 0/154 |
| jev | 154 | 71.4% [65, 79] | 0.71 | 0.97 | 0.07 | 32% [26, 40] | 92.0% (82.6%) | 0/154 | 0/154 |
| jev:1.14 | 154 | 71.4% [64, 78] | 0.71 | 0.97 | 0.08 | 31% [23, 38] | 91.5% (81.6%) | 0/154 | 0/154 |
| joey@openrouter | 154 | 55.8% [48, 64] | 0.56 | 0.96 | 0.12 | 17% [11, 23] | 92.3% (77.7%) | 0/154 | 0/154 |
| luna@decisions | 154 | 70.8% [64, 77] | 0.72 | 0.94 | 0.17 | 0% [0, 0] | — (0.0%) | 0/154 | 0/154 |
| mammoth@openrouter | 154 | 71.4% [64, 79] | 0.72 | 0.98 | 0.07 | 42% [34, 49] | 92.2% (84.3%) | 0/154 | 0/154 |
| reflex@openrouter | 154 | 64.9% [58, 73] | 0.67 | 0.98 | 0.13 | 40% [32, 48] | 93.5% (85.8%) | 0/154 | 0/154 |
| span@openrouter | 154 | 67.5% [61, 75] | 0.69 | 0.96 | 0.13 | 25% [18, 32] | 97.4% (88.1%) | 0/154 | 0/154 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev = jev-1.14.0; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| elephant@openrouter = | 39% [31, 47] | 74% [67, 81] | 0.85 | met |
| mammoth@openrouter = | 42% [34, 49] | 71% [64, 79] | 0.87 | met |
| decider@openrouter = | 46% [38, 54] | 71% [64, 78] | 0.76 | met |
| decider-flash@openrouter = | 49% [42, 56] | 69% [63, 77] | 0.75 | met |
| d1.1@openrouter = | 36% [29, 44] | 67% [60, 74] | 0.70 | met |
| reflex@openrouter = | 40% [32, 48] | 65% [58, 73] | 0.89 | met |
| d1-ultra@openrouter = | 35% [28, 43] | 63% [55, 71] | 0.79 | met |
| gemini-decision@openrouter | 33% [25, 40] | 71% [64, 78] | 0.89 | met |
| clef@openrouter | 33% [26, 41] | 70% [63, 77] | 0.87 | met |
| jev | 32% [26, 40] | 71% [65, 79] | 0.96 | met |
| jev:1.14 | 31% [23, 38] | 71% [64, 78] | 0.98 | met |
| drex-max@openrouter | 30% [23, 37] | 71% [64, 78] | 0.94 | met |
| clef-flash@openrouter | 28% [21, 34] | 71% [64, 78] | 0.85 | met |
| d1@vercel | 28% [21, 34] | 66% [58, 73] | 0.92 | met |
| span@openrouter | 25% [18, 32] | 68% [61, 75] | 0.91 | met |
| clef-omni@openrouter | 23% [16, 29] | 66% [60, 73] | 0.74 | met |
| joey@openrouter | 17% [11, 23] | 56% [48, 64] | 0.96 | met |
| luna@decisions | 0% [0, 0] | 71% [64, 77] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 427 ms | 665 ms | 971 ms | 1031 ms | 2.3 | 0 | 4 | $0.52 | billed |  |
| clef-omni@openrouter | 154 | 497 ms | 742 ms | 1888 ms | 3409 ms | 3.8 | 0 | 4 | $2.04 | billed |  |
| clef@openrouter | 154 | 739 ms | 1096 ms | 1473 ms | 1566 ms | 2.0 | 0 | 4 | $3.27 | billed |  |
| d1-ultra@openrouter | 154 | 494 ms | 673 ms | 835 ms | 932 ms | 1.7 | 0 | 4 | $0.78 | billed |  |
| d1.1@openrouter | 154 | 567 ms | 800 ms | 923 ms | 1194 ms | 1.6 | 0 | 4 | $0.37 | billed |  |
| d1@vercel | 154 | 607 ms | 775 ms | 1269 ms | 1428 ms | 2.1 | 0 | 4 | $0.37 | billed |  |
| decider-flash@openrouter | 154 | 350 ms | 433 ms | 578 ms | 627 ms | 1.7 | 0 | 4 | $0.14 | billed | ○ |
| decider@openrouter | 154 | 566 ms | 735 ms | 948 ms | 1072 ms | 1.7 | 4 | 4 | $0.28 | billed |  |
| drex-max@openrouter | 154 | 603 ms | 1110 ms | 2559 ms | 4151 ms | 4.2 | 0 | 4 | $0.83 | billed |  |
| elephant@openrouter | 154 | 342 ms | 486 ms | 847 ms | 1239 ms | 2.5 | 0 | 4 | $0.52 | billed |  |
| gemini-decision@openrouter | 154 | 890 ms | 1216 ms | 2656 ms | 7650 ms | 3.0 | 0 | 4 | $1.37 | billed |  |
| jev | 154 | 213 ms | 341 ms | 679 ms | 733 ms | 3.2 | 0 | 4 | $1.50 | estimated |  |
| jev:1.14 | 154 | 260 ms | 324 ms | 654 ms | 878 ms | 2.5 | 0 | 4 | $1.50 | estimated |  |
| joey@openrouter | 154 | 310 ms | 406 ms | 674 ms | 848 ms | 2.2 | 0 | 4 | $0.15 | billed |  |
| luna@decisions | 154 | 476 ms | 955 ms | 1203 ms | 1256 ms | 2.5 | 0 | 4 | $1.42 | estimated |  |
| mammoth@openrouter | 154 | 414 ms | 644 ms | 1293 ms | 1493 ms | 3.1 | 0 | 4 | $1.49 | billed |  |
| reflex@openrouter | 154 | 459 ms | 660 ms | 1335 ms | 1884 ms | 2.9 | 0 | 4 | $0.59 | billed |  |
| span@openrouter | 154 | 479 ms | 654 ms | 978 ms | 1109 ms | 2.0 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev (list price of 2026-10-03), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0080 | 18 s (estimated, 154 calls) | 19 min | 4 |
| clef-omni@openrouter | $0.03 | 21 s (estimated, 154 calls) | 23 min | 4 |
| clef@openrouter | $0.05 | 30 s (estimated, 154 calls) | 32 min | 4 |
| d1-ultra@openrouter | $0.01 | 19 s (estimated, 154 calls) | 21 min | 4 |
| d1.1@openrouter | $0.0057 | 22 s (estimated, 154 calls) | 24 min | 4 |
| d1@vercel | $0.0057 | 24 s (estimated, 154 calls) | 26 min | 4 |
| decider-flash@openrouter | $0.0021 | 13 s (estimated, 154 calls) | 14 min | 4 |
| decider@openrouter | $0.0043 | 22 s (estimated, 154 calls) | 24 min | 4 |
| drex-max@openrouter | $0.01 | 29 s (estimated, 154 calls) | 31 min | 4 |
| elephant@openrouter | $0.0081 | 14 s (estimated, 154 calls) | 15 min | 4 |
| gemini-decision@openrouter | $0.02 | 38 s (estimated, 154 calls) | 41 min | 4 |
| jev | $0.02 | 9 s (estimated, 154 calls) | 10 min | 4 |
| jev:1.14 | $0.02 | 9 s (estimated, 154 calls) | 10 min | 4 |
| joey@openrouter | $0.0023 | 12 s (estimated, 154 calls) | 13 min | 4 |
| luna@decisions | $0.02 | 21 s (estimated, 154 calls) | 23 min | 4 |
| mammoth@openrouter | $0.02 | 18 s (estimated, 154 calls) | 19 min | 4 |
| reflex@openrouter | $0.0091 | 19 s (estimated, 154 calls) | 21 min | 4 |
| span@openrouter | $0.0008 | 19 s (estimated, 154 calls) | 20 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-omni@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.91 | rico-66373 |

**d1@vercel** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-35591 | mediaplayer | gallery | 0.96 | rico-35591 |
| rico-43798 | menu | list | 0.93 | rico-43798 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |
| rico-21753 | login | tutorial | 0.91 | rico-21753 |

**drex-max@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-35591 | mediaplayer | gallery | 0.96 | rico-35591 |
| rico-54536 | list | menu | 0.96 | rico-54536 |
| rico-66373 | modal | profile | 0.94 | rico-66373 |
| rico-37922 | profile | form | 0.91 | rico-37922 |

**elephant@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.99 | rico-54536 |
| rico-37922 | profile | form | 0.99 | rico-37922 |
| rico-66373 | modal | profile | 0.97 | rico-66373 |
| rico-35591 | mediaplayer | gallery | 0.96 | rico-35591 |

**gemini-decision@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.95 | rico-54536 |
| rico-37922 | profile | form | 0.93 | rico-37922 |

**jev** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.99 | rico-54536 |
| rico-37073 | gallery | form | 0.98 | rico-37073 |
| rico-35591 | mediaplayer | gallery | 0.95 | rico-35591 |
| rico-37922 | profile | form | 0.94 | rico-37922 |
| rico-66373 | modal | profile | 0.93 | rico-66373 |

**jev:1.14** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.99 | rico-54536 |
| rico-37073 | gallery | form | 0.98 | rico-37073 |
| rico-35591 | mediaplayer | gallery | 0.97 | rico-35591 |
| rico-37922 | profile | form | 0.96 | rico-37922 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |
| rico-41068 | terms | modal | 0.90 | rico-41068 |

**joey@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-35591 | mediaplayer | gallery | 0.97 | rico-35591 |
| rico-27717 | other | gallery | 0.96 | rico-27717 |
| rico-24196 | editor | gallery | 0.91 | rico-24196 |

**luna@decisions** (20)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-18483 | chat | list | 1.00 | rico-18483 |
| rico-54536 | list | menu | 1.00 | rico-54536 |
| rico-6918 | search | list | 1.00 | rico-6918 |
| rico-25255 | other | list | 1.00 | rico-25255 |
| rico-52658 | other | camera | 1.00 | rico-52658 |
| rico-41068 | terms | modal | 1.00 | rico-41068 |
| rico-65259 | chat | tutorial | 0.99 | rico-65259 |
| rico-37073 | gallery | form | 0.99 | rico-37073 |

**mammoth@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-37922 | profile | form | 0.97 | rico-37922 |

**reflex@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-37922 | profile | form | 0.97 | rico-37922 |
| rico-54536 | list | menu | 0.96 | rico-54536 |
| rico-66373 | modal | profile | 0.90 | rico-66373 |

**span@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.97 | rico-66373 |
| rico-71299 | list | news | 0.91 | rico-71299 |
| rico-54536 | list | menu | 0.91 | rico-54536 |


## Cases the models disagree on (12 of 98)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev | jev:1.14 | joey@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rico-17346 | camera | camera (0.66) | camera (0.47) | camera (0.53) | other (0.38) | camera (0.74) | camera (0.56) | other (0.50) | other (0.51) | other (0.46) | camera (0.45) | camera (0.47) | camera (0.48) | camera (0.60) | camera (0.37) | camera (1.00) | other (0.37) | other (0.83) | other (0.38) | rico-17346 |
| rico-18483 | chat | news (0.77) | list (0.44) | news (0.71) | news (0.48) | other (0.40) | news (0.50) | news (0.47) | news (0.51) | news (0.69) | news (0.77) | list (0.58) | list (0.57) | news (0.53) | news (0.89) | list (1.00) | list (0.63) | news (0.76) | news (0.89) | rico-18483 |
| rico-10522 | editor | editor (0.90) | editor (0.82) | editor (0.97) | editor (0.95) | editor (0.92) | editor (0.99) | editor (0.96) | editor (0.97) | editor (0.99) | editor (1.00) | editor (0.99) | editor (1.00) | editor (1.00) | news (0.50) | editor (0.99) | editor (0.99) | editor (0.99) | editor (0.92) | rico-10522 |
| rico-24880 | form | form (0.76) | form (0.75) | form (0.72) | login (0.42) | form (0.64) | form (0.75) | form (0.85) | form (0.84) | form (0.74) | form (0.90) | form (0.91) | form (0.88) | form (0.89) | form (0.79) | form (1.00) | form (0.71) | form (0.89) | form (0.48) | rico-24880 |
| rico-3942 | list | list (0.73) | list (0.56) | list (0.54) | news (0.73) | news (0.47) | news (0.74) | list (0.41) | list (0.64) | list (0.47) | list (0.97) | list (0.67) | list (0.92) | list (0.87) | news (0.31) | list (1.00) | list (0.88) | list (0.76) | news (0.89) | rico-3942 |
| rico-52193 | list | list (0.76) | list (0.70) | list (0.76) | other (0.41) | list (0.50) | list (0.95) | list (0.79) | list (0.79) | list (0.83) | list (0.99) | list (0.68) | list (0.97) | list (0.97) | news (0.55) | list (1.00) | list (0.88) | list (0.91) | list (0.79) | rico-52193 |
| rico-54536 | list | menu (0.78) | menu (0.79) | menu (0.81) | menu (0.68) | menu (0.68) | menu (0.62) | menu (0.65) | menu (0.63) | menu (0.96) | menu (0.99) | menu (0.95) | menu (0.99) | menu (0.99) | modal (0.59) | menu (1.00) | menu (0.69) | menu (0.96) | menu (0.91) | rico-54536 |
| rico-67717 | list | list (0.80) | list (0.67) | list (0.63) | news (0.50) | list (0.37) | list (0.95) | list (0.77) | list (0.85) | list (0.71) | list (1.00) | list (0.72) | list (0.99) | list (0.99) | news (0.39) | list (1.00) | list (0.95) | list (0.86) | list (0.42) | rico-67717 |
| rico-58529 | menu | menu (0.76) | menu (0.75) | menu (0.88) | menu (0.85) | menu (0.69) | menu (0.47) | menu (0.89) | menu (0.90) | menu (0.92) | menu (0.97) | menu (0.94) | menu (0.99) | menu (0.99) | profile (0.35) | menu (1.00) | menu (0.95) | menu (0.97) | menu (0.75) | rico-58529 |
| rico-58958 | news | news (0.76) | news (0.76) | news (0.89) | other (0.56) | other (0.46) | list (0.47) | news (0.95) | news (0.94) | news (0.99) | news (0.99) | news (0.64) | news (0.98) | news (0.98) | news (1.00) | news (1.00) | news (0.99) | news (0.97) | news (0.86) | rico-58958 |
| rico-25255 | other | news (0.58) | list (0.60) | list (0.40) | other (0.32) | news (0.48) | news (0.46) | news (0.29) | list (0.30) | other (0.47) | news (0.57) | news (0.38) | list (0.54) | list (0.54) | gallery (0.35) | list (1.00) | list (0.72) | other (0.49) | news (0.73) | rico-25255 |
| rico-52658 | other | camera (0.75) | camera (0.60) | camera (0.61) | camera (0.44) | camera (0.69) | camera (0.63) | other (0.43) | other (0.35) | other (0.45) | camera (0.58) | camera (0.34) | camera (0.73) | camera (0.70) | camera (0.51) | camera (1.00) | other (0.24) | other (0.69) | other (0.30) | rico-52658 |
