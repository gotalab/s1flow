# enrico-screen

2026-11-11 · 154 labelled dev cases (form 9, gallery 9, menu 9, settings 9, bare 8, chat 8, editor 8, list 8, more) · split: stratified k-fold (no test case among these: CV numbers only) · source: Enrico (labels MIT) on Rico screenshots (CC BY 4.0): up to 12 screens per design topic, mislabelled ones replaced

**elephant@openrouter** has the highest coverage at 95% accuracy, 48% [40, 56] (API cost $0.31 per 10k, p99 629ms). Its interval overlaps with decider@openrouter, gemini-decision@openrouter, drex-max@openrouter, mammoth@openrouter, decider-flash@openrouter, clef@openrouter, d1.1@openrouter, d1-ultra@openrouter, reflex@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is decider@openrouter's, 73% [65, 79].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 68.8% [62, 76] | 0.69 | 0.97 | 0.06 | 26% [19, 33] | 95.0% (85.1%) | 0/154 | 0/154 |
| clef-omni@openrouter | 154 | 66.2% [58, 73] | 0.67 | 0.97 | 0.13 | 21% [14, 28] | 90.6% (77.5%) | 0/154 | 0/154 |
| clef@openrouter | 154 | 70.1% [63, 77] | 0.70 | 0.98 | 0.06 | 34% [27, 42] | 90.6% (81.2%) | 0/154 | 0/154 |
| d1-ultra@openrouter | 154 | 64.9% [57, 73] | 0.67 | 0.97 | 0.08 | 36% [28, 44] | 89.1% (79.6%) | 0/154 | 0/154 |
| d1.1@openrouter | 154 | 67.5% [60, 75] | 0.68 | 0.97 | 0.09 | 34% [27, 41] | 92.3% (83.3%) | 0/154 | 0/154 |
| d1@vercel | 154 | 62.3% [54, 70] | 0.63 | 0.96 | 0.11 | 19% [13, 26] | 86.7% (72.0%) | 0/154 | 0/154 |
| decider-flash@openrouter | 154 | 70.1% [63, 77] | 0.72 | 0.98 | 0.05 | 42% [34, 50] | 92.3% (84.5%) | 0/154 | 0/154 |
| decider@openrouter | 154 | 72.7% [65, 79] | 0.74 | 0.99 | 0.09 | 42% [34, 50] | 96.9% (90.6%) | 0/154 | 0/154 |
| drex-max@openrouter | 154 | 71.4% [64, 78] | 0.71 | 0.98 | 0.09 | 34% [27, 42] | 94.3% (86.0%) | 0/154 | 0/154 |
| elephant@openrouter | 154 | 72.7% [66, 79] | 0.73 | 0.98 | 0.08 | 48% [40, 56] | 91.9% (84.6%) | 0/154 | 0/154 |
| gemini-decision@openrouter | 154 | 71.4% [64, 79] | 0.70 | 0.98 | 0.06 | 36% [28, 43] | 92.7% (84.1%) | 0/154 | 0/154 |
| jev | 154 | 71.4% [64, 78] | 0.71 | 0.96 | 0.09 | 32% [25, 40] | 92.0% (82.6%) | 0/154 | 0/154 |
| jev:1.14 | 154 | 70.8% [64, 77] | 0.70 | 0.96 | 0.07 | 31% [24, 38] | 89.6% (79.3%) | 0/154 | 0/154 |
| joey@openrouter | 154 | 57.8% [49, 66] | 0.59 | 0.95 | 0.15 | 21% [15, 28] | 93.8% (81.6%) | 0/154 | 0/154 |
| luna@decisions | 154 | 69.5% [62, 76] | 0.70 | 0.95 | 0.19 | 14% [8, 20] | 71.4% (51.3%) | 0/154 | 0/154 |
| mammoth@openrouter | 154 | 70.8% [64, 77] | 0.71 | 0.98 | 0.10 | 42% [34, 49] | 93.8% (86.5%) | 0/154 | 0/154 |
| reflex@openrouter | 154 | 64.3% [57, 71] | 0.67 | 0.98 | 0.12 | 34% [27, 42] | 94.3% (86.0%) | 0/154 | 0/154 |
| span@openrouter | 154 | 66.2% [58, 73] | 0.68 | 0.96 | 0.13 | 25% [18, 32] | 97.4% (88.4%) | 0/154 | 0/154 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev = jev-1.14.0; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| elephant@openrouter = | 48% [40, 56] | 73% [66, 79] | 0.84 | met |
| decider@openrouter = | 42% [34, 50] | 73% [65, 79] | 0.77 | met |
| gemini-decision@openrouter = | 36% [28, 43] | 71% [64, 79] | 0.88 | met |
| drex-max@openrouter = | 34% [27, 42] | 71% [64, 78] | 0.94 | met |
| mammoth@openrouter = | 42% [34, 49] | 71% [64, 77] | 0.86 | met |
| decider-flash@openrouter = | 42% [34, 50] | 70% [63, 77] | 0.78 | met |
| clef@openrouter = | 34% [27, 42] | 70% [63, 77] | 0.81 | met |
| d1.1@openrouter = | 34% [27, 41] | 68% [60, 75] | 0.74 | met |
| d1-ultra@openrouter = | 36% [28, 44] | 65% [57, 73] | 0.76 | met |
| reflex@openrouter = | 34% [27, 42] | 64% [57, 71] | 0.95 | met |
| jev | 32% [25, 40] | 71% [64, 78] | 0.97 | met |
| jev:1.14 | 31% [24, 38] | 71% [64, 77] | 0.97 | met |
| clef-flash@openrouter | 26% [19, 33] | 69% [62, 76] | 0.85 | met |
| span@openrouter | 25% [18, 32] | 66% [58, 73] | 0.91 | met |
| clef-omni@openrouter | 21% [14, 28] | 66% [58, 73] | 0.71 | met |
| joey@openrouter | 21% [15, 28] | 58% [49, 66] | 0.94 | met |
| d1@vercel | 19% [13, 26] | 62% [54, 70] | 0.94 | met |
| luna@decisions | 14% [8, 20] | 69% [62, 76] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 435 ms | 657 ms | 1025 ms | 1231 ms | 2.4 | 0 | 4 | $0.38 | billed |  |
| clef-omni@openrouter | 154 | 348 ms | 501 ms | 1483 ms | 2763 ms | 4.3 | 0 | 4 | $1.51 | billed |  |
| clef@openrouter | 154 | 658 ms | 1093 ms | 1502 ms | 1784 ms | 2.3 | 0 | 4 | $2.42 | billed |  |
| d1-ultra@openrouter | 154 | 511 ms | 737 ms | 926 ms | 1017 ms | 1.8 | 0 | 4 | $0.39 | billed |  |
| d1.1@openrouter | 154 | 825 ms | 1158 ms | 1346 ms | 1463 ms | 1.6 | 0 | 4 | $0.19 | billed |  |
| d1@vercel | 154 | 596 ms | 789 ms | 1038 ms | 1201 ms | 1.7 | 0 | 4 | $0.19 | billed |  |
| decider-flash@openrouter | 154 | 295 ms | 351 ms | 442 ms | 583 ms | 1.5 | 0 | 4 | $0.08 | billed | ○ |
| decider@openrouter | 154 | 467 ms | 732 ms | 1204 ms | 1728 ms | 2.6 | 1 | 4 | $0.15 | billed |  |
| drex-max@openrouter | 154 | 523 ms | 821 ms | 1321 ms | 4151 ms | 2.5 | 0 | 4 | $0.46 | billed |  |
| elephant@openrouter | 154 | 282 ms | 447 ms | 629 ms | 1239 ms | 2.2 | 0 | 4 | $0.31 | billed | ○ |
| gemini-decision@openrouter | 154 | 831 ms | 1162 ms | 1555 ms | 1643 ms | 1.9 | 0 | 4 | $1.37 | billed |  |
| jev | 154 | 135 ms | 275 ms | 571 ms | 733 ms | 4.2 | 0 | 4 | $0.84 | estimated |  |
| jev:1.14 | 154 | 235 ms | 292 ms | 711 ms | 773 ms | 3.0 | 0 | 4 | $0.84 | estimated |  |
| joey@openrouter | 154 | 275 ms | 435 ms | 750 ms | 848 ms | 2.7 | 0 | 4 | $0.09 | billed |  |
| luna@decisions | 154 | 372 ms | 746 ms | 1134 ms | 1256 ms | 3.0 | 0 | 4 | $0.80 | estimated |  |
| mammoth@openrouter | 154 | 343 ms | 502 ms | 716 ms | 1108 ms | 2.1 | 0 | 4 | $0.88 | billed |  |
| reflex@openrouter | 154 | 354 ms | 551 ms | 1218 ms | 1884 ms | 3.4 | 0 | 4 | $0.33 | billed |  |
| span@openrouter | 154 | 407 ms | 612 ms | 956 ms | 1217 ms | 2.4 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev (list price of 2026-10-03), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0059 | 18 s (estimated, 154 calls) | 19 min | 4 |
| clef-omni@openrouter | $0.02 | 16 s (estimated, 154 calls) | 17 min | 4 |
| clef@openrouter | $0.04 | 27 s (estimated, 154 calls) | 30 min | 4 |
| d1-ultra@openrouter | $0.0060 | 21 s (estimated, 154 calls) | 22 min | 4 |
| d1.1@openrouter | $0.0029 | 31 s (estimated, 154 calls) | 34 min | 4 |
| d1@vercel | $0.0029 | 23 s (estimated, 154 calls) | 25 min | 4 |
| decider-flash@openrouter | $0.0012 | 11 s (estimated, 154 calls) | 12 min | 4 |
| decider@openrouter | $0.0024 | 19 s (estimated, 154 calls) | 21 min | 4 |
| drex-max@openrouter | $0.0072 | 22 s (estimated, 154 calls) | 24 min | 4 |
| elephant@openrouter | $0.0047 | 13 s (estimated, 154 calls) | 14 min | 4 |
| gemini-decision@openrouter | $0.02 | 34 s (estimated, 154 calls) | 36 min | 4 |
| jev | $0.01 | 7 s (estimated, 154 calls) | 8 min | 4 |
| jev:1.14 | $0.01 | 8 s (estimated, 154 calls) | 9 min | 4 |
| joey@openrouter | $0.0014 | 12 s (estimated, 154 calls) | 13 min | 4 |
| luna@decisions | $0.01 | 17 s (estimated, 154 calls) | 18 min | 4 |
| mammoth@openrouter | $0.01 | 14 s (estimated, 154 calls) | 15 min | 4 |
| reflex@openrouter | $0.0051 | 16 s (estimated, 154 calls) | 17 min | 4 |
| span@openrouter | $0.0008 | 17 s (estimated, 154 calls) | 18 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-omni@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.91 | rico-66373 |

**d1@vercel** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-27717 | other | gallery | 0.98 | rico-27717 |
| rico-35591 | mediaplayer | gallery | 0.97 | rico-35591 |
| rico-30780 | mediaplayer | news | 0.94 | rico-30780 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |
| rico-43798 | menu | list | 0.91 | rico-43798 |
| rico-62574 | settings | list | 0.91 | rico-62574 |

**drex-max@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-35591 | mediaplayer | gallery | 0.96 | rico-35591 |
| rico-66373 | modal | profile | 0.94 | rico-66373 |
| rico-54536 | list | menu | 0.94 | rico-54536 |
| rico-37922 | profile | form | 0.91 | rico-37922 |
| rico-30542 | calculator | other | 0.91 | rico-30542 |

**elephant@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-37922 | profile | form | 0.99 | rico-37922 |
| rico-54536 | list | menu | 0.99 | rico-54536 |
| rico-66373 | modal | profile | 0.97 | rico-66373 |
| rico-35591 | mediaplayer | gallery | 0.96 | rico-35591 |

**gemini-decision@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.93 | rico-54536 |
| rico-37922 | profile | form | 0.93 | rico-37922 |

**jev** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 1.00 | rico-54536 |
| rico-35591 | mediaplayer | gallery | 0.98 | rico-35591 |
| rico-37073 | gallery | form | 0.96 | rico-37073 |
| rico-37922 | profile | form | 0.94 | rico-37922 |
| rico-66373 | modal | profile | 0.93 | rico-66373 |

**jev:1.14** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 1.00 | rico-54536 |
| rico-35591 | mediaplayer | gallery | 0.98 | rico-35591 |
| rico-37922 | profile | form | 0.96 | rico-37922 |
| rico-37073 | gallery | form | 0.96 | rico-37073 |
| rico-12581 | bare | maps | 0.94 | rico-12581 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |

**joey@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-35591 | mediaplayer | gallery | 0.97 | rico-35591 |
| rico-18483 | chat | news | 0.94 | rico-18483 |
| rico-27717 | other | gallery | 0.93 | rico-27717 |
| rico-24196 | editor | gallery | 0.92 | rico-24196 |

**luna@decisions** (21)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-25255 | other | list | 1.00 | rico-25255 |
| rico-18483 | chat | list | 1.00 | rico-18483 |
| rico-54536 | list | menu | 1.00 | rico-54536 |
| rico-68494 | news | list | 1.00 | rico-68494 |
| rico-52658 | other | camera | 0.99 | rico-52658 |
| rico-39118 | other | list | 0.99 | rico-39118 |
| rico-41068 | terms | modal | 0.99 | rico-41068 |
| rico-6918 | search | list | 0.98 | rico-6918 |

**mammoth@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-37922 | profile | form | 0.97 | rico-37922 |

**reflex@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.97 | rico-54536 |
| rico-37922 | profile | form | 0.97 | rico-37922 |
| rico-65338 | profile | other | 0.94 | rico-65338 |
| rico-66373 | modal | profile | 0.90 | rico-66373 |

**span@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.97 | rico-66373 |
| rico-54536 | list | menu | 0.91 | rico-54536 |
| rico-39118 | other | news | 0.90 | rico-39118 |


## Cases the models disagree on (12 of 100)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev | jev:1.14 | joey@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rico-10522 | editor | editor (0.90) | editor (0.82) | editor (0.97) | editor (0.95) | editor (0.92) | editor (0.99) | editor (0.96) | editor (0.97) | editor (0.99) | editor (1.00) | editor (0.99) | editor (1.00) | editor (1.00) | news (0.50) | editor (0.99) | editor (0.99) | editor (0.99) | editor (0.92) | rico-10522 |
| rico-58529 | menu | menu (0.76) | menu (0.75) | menu (0.88) | menu (0.85) | menu (0.69) | menu (0.47) | menu (0.89) | menu (0.90) | menu (0.92) | menu (0.97) | menu (0.94) | menu (0.99) | menu (0.99) | profile (0.35) | menu (1.00) | menu (0.95) | menu (0.97) | menu (0.75) | rico-58529 |
| rico-25255 | other | news (0.58) | list (0.60) | list (0.40) | other (0.32) | news (0.48) | news (0.46) | news (0.29) | list (0.30) | other (0.47) | news (0.57) | news (0.38) | list (0.54) | list (0.54) | gallery (0.35) | list (1.00) | list (0.72) | other (0.49) | news (0.73) | rico-25255 |
| rico-1281 | profile | profile (0.88) | list (0.38) | profile (0.95) | profile (0.89) | profile (0.87) | profile (0.83) | profile (0.92) | profile (0.93) | profile (0.96) | profile (0.98) | profile (0.98) | profile (0.97) | profile (0.97) | news (0.44) | profile (1.00) | profile (0.97) | profile (0.64) | profile (0.95) | rico-1281 |
| rico-63576 | tutorial | search (0.41) | tutorial (0.54) | tutorial (0.72) | tutorial (0.81) | tutorial (0.90) | tutorial (0.91) | search (0.54) | tutorial (0.89) | tutorial (0.87) | tutorial (0.95) | tutorial (0.58) | tutorial (0.88) | tutorial (0.89) | tutorial (0.52) | tutorial (1.00) | tutorial (0.81) | tutorial (0.91) | search (0.69) | rico-63576 |
| rico-18483 | chat | news (0.68) | list (0.49) | news (0.73) | news (0.46) | list (0.38) | news (0.53) | news (0.42) | news (0.50) | news (0.76) | news (0.77) | list (0.50) | list (0.72) | list (0.67) | news (0.94) | list (1.00) | list (0.62) | news (0.80) | news (0.86) | rico-18483 |
| rico-24880 | form | form (0.71) | form (0.68) | form (0.68) | login (0.41) | form (0.71) | form (0.78) | form (0.87) | form (0.79) | form (0.81) | form (0.83) | form (0.89) | form (0.87) | form (0.90) | form (0.73) | form (1.00) | form (0.73) | form (0.89) | form (0.68) | rico-24880 |
| rico-3942 | list | list (0.52) | list (0.58) | list (0.43) | news (0.70) | news (0.52) | news (0.75) | list (0.44) | list (0.62) | list (0.45) | list (0.94) | list (0.69) | list (0.89) | list (0.90) | news (0.36) | list (1.00) | list (0.87) | list (0.86) | news (0.85) | rico-3942 |
| rico-52193 | list | list (0.73) | list (0.71) | list (0.75) | list (0.35) | list (0.49) | list (0.94) | list (0.80) | list (0.75) | list (0.69) | list (0.97) | list (0.75) | list (0.97) | list (0.96) | news (0.53) | list (1.00) | list (0.83) | list (0.80) | list (0.73) | rico-52193 |
| rico-67717 | list | list (0.81) | list (0.72) | list (0.72) | news (0.45) | news (0.41) | list (0.95) | list (0.80) | list (0.85) | list (0.65) | list (1.00) | list (0.78) | list (0.98) | list (0.99) | news (0.29) | list (1.00) | list (0.96) | list (0.84) | news (0.46) | rico-67717 |
| rico-71299 | list | list (0.69) | list (0.71) | list (0.81) | news (0.49) | list (0.34) | list (0.93) | list (0.78) | list (0.90) | list (0.66) | list (0.99) | list (0.82) | list (1.00) | list (0.99) | list (0.35) | list (1.00) | list (0.97) | list (0.95) | news (0.87) | rico-71299 |
| rico-501 | modal | modal (0.74) | modal (0.66) | modal (0.72) | modal (0.81) | modal (0.62) | modal (0.87) | modal (0.89) | modal (0.77) | modal (0.61) | modal (0.87) | modal (0.90) | modal (0.92) | modal (0.91) | modal (0.89) | modal (1.00) | modal (0.88) | login (0.47) | modal (0.82) | rico-501 |
