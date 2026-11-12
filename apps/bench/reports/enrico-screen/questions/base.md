# enrico-screen

2026-11-12 · 154 labelled dev cases (form 9, gallery 9, menu 9, settings 9, bare 8, chat 8, editor 8, list 8, more) · split: stratified k-fold (no test case among these: CV numbers only) · source: Enrico (labels MIT) on Rico screenshots (CC BY 4.0): up to 12 screens per design topic, mislabelled ones replaced

**decider-flash@openrouter** has the highest coverage at 95% accuracy, 45% [38, 54] (API cost $0.08 per 10k, p99 486ms). Its interval overlaps with decider@openrouter, elephant@openrouter, gemini-decision@google, drex-max@openrouter, mammoth@openrouter, clef@openrouter, d1.1@openrouter, d1-ultra@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. Ordered by task.py's tiebreak (accuracy (all)), **decider@openrouter** comes first (API cost $0.15 per 10k, p99 945ms). The highest raw accuracy (dev) is decider@openrouter's, 73% [66, 81].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 68.8% [61, 77] | 0.69 | 0.97 | 0.09 | 28% [21, 35] | 93.0% (82.9%) | 0/154 | 0/154 |
| clef-omni@openrouter | 154 | 66.2% [59, 74] | 0.67 | 0.97 | 0.13 | 26% [19, 32] | 92.5% (81.7%) | 0/154 | 0/154 |
| clef@openrouter | 154 | 69.5% [62, 77] | 0.69 | 0.98 | 0.04 | 35% [28, 42] | 92.6% (83.8%) | 0/154 | 0/154 |
| d1-ultra@openrouter | 154 | 63.6% [56, 71] | 0.66 | 0.97 | 0.10 | 39% [31, 47] | 91.7% (83.3%) | 0/154 | 0/154 |
| d1.1@openrouter | 154 | 64.9% [57, 71] | 0.66 | 0.97 | 0.10 | 40% [32, 47] | 95.1% (87.8%) | 0/154 | 0/154 |
| d1@vercel | 154 | 63.0% [56, 70] | 0.63 | 0.96 | 0.10 | 26% [19, 33] | 90.0% (78.6%) | 0/154 | 0/154 |
| decider-flash@openrouter | 154 | 70.1% [63, 77] | 0.72 | 0.98 | 0.05 | 45% [38, 54] | 94.3% (87.4%) | 0/154 | 0/154 |
| decider@openrouter | 154 | 73.4% [66, 81] | 0.74 | 0.99 | 0.11 | 45% [37, 53] | 94.2% (87.2%) | 0/154 | 0/154 |
| drex-max@openrouter | 154 | 71.4% [64, 79] | 0.71 | 0.98 | 0.09 | 33% [25, 40] | 92.2% (82.9%) | 0/154 | 0/154 |
| elephant@openrouter | 154 | 72.7% [66, 80] | 0.73 | 0.98 | 0.08 | 41% [33, 49] | 93.7% (86.1%) | 0/154 | 0/154 |
| gemini-decision@google | 154 | 71.4% [64, 79] | 0.70 | 0.98 | 0.06 | 34% [27, 41] | 94.2% (85.8%) | 0/154 | 0/154 |
| jev | 154 | 70.1% [63, 77] | 0.69 | 0.96 | 0.08 | 25% [18, 32] | 92.1% (80.8%) | 0/154 | 0/154 |
| jev:1.14 | 154 | 69.5% [62, 77] | 0.69 | 0.96 | 0.08 | 17% [11, 23] | 88.5% (72.8%) | 0/154 | 0/154 |
| joey@openrouter | 154 | 57.8% [50, 66] | 0.59 | 0.95 | 0.15 | 21% [16, 28] | 90.9% (78.1%) | 0/154 | 0/154 |
| luna@decisions | 154 | 69.5% [62, 77] | 0.70 | 0.95 | 0.19 | 0% [0, 0] | — (0.0%) | 0/154 | 0/154 |
| mammoth@openrouter | 154 | 70.8% [64, 78] | 0.71 | 0.98 | 0.10 | 44% [36, 51] | 95.5% (88.8%) | 0/154 | 0/154 |
| reflex@openrouter | 154 | 66.2% [58, 73] | 0.69 | 0.98 | 0.11 | 26% [19, 33] | 92.5% (81.7%) | 0/154 | 0/154 |
| span@openrouter | 154 | 66.9% [60, 74] | 0.68 | 0.96 | 0.13 | 27% [21, 34] | 92.9% (82.6%) | 0/154 | 0/154 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev = jev-1.14.0; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| decider@openrouter = | 45% [37, 53] | 73% [66, 81] | 0.77 | met |
| elephant@openrouter = | 41% [33, 49] | 73% [66, 80] | 0.84 | met |
| gemini-decision@google = | 34% [27, 41] | 71% [64, 79] | 0.88 | met |
| drex-max@openrouter = | 33% [25, 40] | 71% [64, 79] | 0.94 | met |
| mammoth@openrouter = | 44% [36, 51] | 71% [64, 78] | 0.86 | met |
| decider-flash@openrouter = | 45% [38, 54] | 70% [63, 77] | 0.78 | met |
| clef@openrouter = | 35% [28, 42] | 69% [62, 77] | 0.86 | met |
| d1.1@openrouter = | 40% [32, 47] | 65% [57, 71] | 0.65 | met |
| d1-ultra@openrouter = | 39% [31, 47] | 64% [56, 71] | 0.70 | met |
| clef-flash@openrouter | 28% [21, 35] | 69% [61, 77] | 0.85 | met |
| span@openrouter | 27% [21, 34] | 67% [60, 74] | 0.91 | met |
| clef-omni@openrouter | 26% [19, 32] | 66% [59, 74] | 0.71 | met |
| reflex@openrouter | 26% [19, 33] | 66% [58, 73] | 0.95 | met |
| d1@vercel | 26% [19, 33] | 63% [56, 70] | 0.92 | met |
| jev | 25% [18, 32] | 70% [63, 77] | 0.97 | met |
| joey@openrouter | 21% [16, 28] | 58% [50, 66] | 0.94 | met |
| jev:1.14 | 17% [11, 23] | 69% [62, 77] | 0.97 | met |
| luna@decisions | 0% [0, 0] | 69% [62, 77] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 390 ms | 576 ms | 1599 ms | 1827 ms | 4.1 | 0 | 4 | $0.26 | billed |  |
| clef-omni@openrouter | 154 | 312 ms | 441 ms | 1562 ms | 2208 ms | 5.0 | 0 | 4 | $1.51 | billed |  |
| clef@openrouter | 154 | 769 ms | 1704 ms | 3134 ms | 3760 ms | 4.1 | 0 | 4 | $2.18 | billed |  |
| d1-ultra@openrouter | 154 | 641 ms | 1350 ms | 2611 ms | 2906 ms | 4.1 | 0 | 4 | $0.39 | billed |  |
| d1.1@openrouter | 154 | 409 ms | 649 ms | 799 ms | 913 ms | 2.0 | 0 | 4 | $0.19 | billed |  |
| d1@vercel | 154 | 862 ms | 1655 ms | 6328 ms | 6684 ms | 7.3 | 0 | 4 | $0.19 | billed |  |
| decider-flash@openrouter | 154 | 215 ms | 342 ms | 486 ms | 611 ms | 2.3 | 0 | 4 | $0.08 | billed | ○ |
| decider@openrouter | 154 | 361 ms | 633 ms | 945 ms | 1145 ms | 2.6 | 0 | 4 | $0.15 | billed |  |
| drex-max@openrouter | 154 | 2334 ms | 4594 ms | 6422 ms | 7153 ms | 2.8 | 0 | 4 | $0.46 | billed |  |
| elephant@openrouter | 154 | 275 ms | 391 ms | 502 ms | 612 ms | 1.8 | 0 | 4 | $0.31 | billed |  |
| gemini-decision@google | 154 | 653 ms | 983 ms | 1417 ms | 1616 ms | 2.2 | 0 | 4 | $1.37 | estimated |  |
| jev | 154 | 246 ms | 293 ms | 667 ms | 681 ms | 2.7 | 0 | 4 | $0.84 | estimated |  |
| jev:1.14 | 154 | 244 ms | 295 ms | 430 ms | 492 ms | 1.8 | 0 | 4 | $0.84 | estimated | ○ |
| joey@openrouter | 154 | 258 ms | 378 ms | 443 ms | 448 ms | 1.7 | 0 | 4 | $0.09 | billed | ○ |
| luna@decisions | 154 | 398 ms | 739 ms | 934 ms | 1058 ms | 2.3 | 0 | 4 | $0.80 | estimated |  |
| mammoth@openrouter | 154 | 323 ms | 485 ms | 723 ms | 1354 ms | 2.2 | 0 | 4 | $0.88 | billed |  |
| reflex@openrouter | 154 | 536 ms | 2357 ms | 3462 ms | 3830 ms | 6.5 | 3 | 4 | $0.33 | billed |  |
| span@openrouter | 154 | 308 ms | 473 ms | 717 ms | 765 ms | 2.3 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev (list price of 2026-10-03), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0039 | 17 s (estimated, 154 calls) | 19 min | 4 |
| clef-omni@openrouter | $0.02 | 14 s (estimated, 154 calls) | 15 min | 4 |
| clef@openrouter | $0.03 | 35 s (estimated, 154 calls) | 38 min | 4 |
| d1-ultra@openrouter | $0.0060 | 31 s (estimated, 154 calls) | 33 min | 4 |
| d1.1@openrouter | $0.0029 | 16 s (estimated, 154 calls) | 18 min | 4 |
| d1@vercel | $0.0029 | 43 s (estimated, 154 calls) | 47 min | 4 |
| decider-flash@openrouter | $0.0012 | 10 s (estimated, 154 calls) | 10 min | 4 |
| decider@openrouter | $0.0024 | 16 s (estimated, 154 calls) | 17 min | 4 |
| drex-max@openrouter | $0.0072 | 2 min (estimated, 154 calls) | 1.9 h | 4 |
| elephant@openrouter | $0.0047 | 11 s (estimated, 154 calls) | 12 min | 4 |
| gemini-decision@google | $0.02 | 27 s (estimated, 154 calls) | 29 min | 4 |
| jev | $0.01 | 10 s (estimated, 154 calls) | 11 min | 4 |
| jev:1.14 | $0.01 | 9 s (estimated, 154 calls) | 10 min | 4 |
| joey@openrouter | $0.0014 | 11 s (estimated, 154 calls) | 12 min | 4 |
| luna@decisions | $0.01 | 17 s (estimated, 154 calls) | 18 min | 4 |
| mammoth@openrouter | $0.01 | 14 s (estimated, 154 calls) | 15 min | 4 |
| reflex@openrouter | $0.0051 | 39 s (estimated, 154 calls) | 43 min | 4 |
| span@openrouter | $0.0008 | 13 s (estimated, 154 calls) | 14 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-omni@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.91 | rico-66373 |

**clef@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-37922 | profile | form | 0.91 | rico-37922 |

**d1@vercel** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-35591 | mediaplayer | gallery | 0.97 | rico-35591 |
| rico-27717 | other | gallery | 0.95 | rico-27717 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |
| rico-43798 | menu | list | 0.91 | rico-43798 |

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

**gemini-decision@google** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.93 | rico-54536 |
| rico-37922 | profile | form | 0.93 | rico-37922 |

**jev** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 1.00 | rico-54536 |
| rico-35591 | mediaplayer | gallery | 0.98 | rico-35591 |
| rico-37922 | profile | form | 0.96 | rico-37922 |
| rico-37073 | gallery | form | 0.96 | rico-37073 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |

**jev:1.14** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 1.00 | rico-54536 |
| rico-35591 | mediaplayer | gallery | 0.99 | rico-35591 |
| rico-37922 | profile | form | 0.96 | rico-37922 |
| rico-37073 | gallery | form | 0.96 | rico-37073 |
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
| rico-18483 | chat | list | 1.00 | rico-18483 |
| rico-54536 | list | menu | 1.00 | rico-54536 |
| rico-68494 | news | list | 1.00 | rico-68494 |
| rico-25255 | other | list | 1.00 | rico-25255 |
| rico-39118 | other | list | 0.99 | rico-39118 |
| rico-52658 | other | camera | 0.99 | rico-52658 |
| rico-41068 | terms | modal | 0.99 | rico-41068 |
| rico-6918 | search | list | 0.98 | rico-6918 |

**mammoth@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-37922 | profile | form | 0.97 | rico-37922 |

**reflex@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.98 | rico-54536 |
| rico-37922 | profile | form | 0.97 | rico-37922 |
| rico-65338 | profile | other | 0.94 | rico-65338 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |
| rico-35591 | mediaplayer | gallery | 0.91 | rico-35591 |

**span@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.97 | rico-66373 |
| rico-54536 | list | menu | 0.91 | rico-54536 |
| rico-39118 | other | news | 0.90 | rico-39118 |


## Cases the models disagree on (12 of 100)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev | jev:1.14 | joey@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rico-18483 | chat | news (0.73) | list (0.49) | news (0.69) | news (0.43) | other (0.36) | list (0.47) | news (0.42) | news (0.51) | news (0.76) | news (0.77) | list (0.50) | list (0.71) | list (0.68) | news (0.94) | list (1.00) | list (0.62) | news (0.80) | news (0.86) | rico-18483 |
| rico-10522 | editor | editor (0.94) | editor (0.82) | editor (0.97) | editor (0.92) | editor (0.94) | editor (0.99) | editor (0.96) | editor (0.97) | editor (0.99) | editor (1.00) | editor (0.99) | editor (1.00) | editor (1.00) | news (0.50) | editor (0.99) | editor (0.99) | editor (0.99) | editor (0.92) | rico-10522 |
| rico-24880 | form | form (0.80) | form (0.68) | form (0.79) | login (0.46) | form (0.56) | form (0.80) | form (0.87) | form (0.79) | form (0.81) | form (0.83) | form (0.89) | form (0.88) | form (0.89) | form (0.73) | form (1.00) | form (0.73) | form (0.92) | form (0.68) | rico-24880 |
| rico-3942 | list | list (0.64) | list (0.58) | list (0.43) | news (0.76) | news (0.63) | news (0.71) | list (0.44) | list (0.62) | list (0.45) | list (0.94) | list (0.69) | list (0.85) | list (0.89) | news (0.36) | list (1.00) | list (0.87) | list (0.88) | news (0.85) | rico-3942 |
| rico-52193 | list | list (0.75) | list (0.71) | list (0.76) | list (0.34) | list (0.54) | list (0.94) | list (0.80) | list (0.75) | list (0.69) | list (0.97) | list (0.75) | list (0.95) | list (0.96) | news (0.53) | list (1.00) | list (0.83) | list (0.58) | list (0.73) | rico-52193 |
| rico-67717 | list | list (0.83) | list (0.72) | list (0.77) | news (0.61) | list (0.37) | list (0.94) | list (0.80) | list (0.83) | list (0.65) | list (1.00) | list (0.78) | list (0.99) | list (0.98) | news (0.29) | list (1.00) | list (0.96) | list (0.76) | news (0.46) | rico-67717 |
| rico-71299 | list | list (0.76) | list (0.71) | list (0.77) | news (0.48) | news (0.37) | list (0.80) | list (0.78) | list (0.90) | list (0.66) | list (0.99) | list (0.82) | list (1.00) | list (1.00) | list (0.35) | list (1.00) | list (0.97) | list (0.95) | news (0.87) | rico-71299 |
| rico-58529 | menu | menu (0.85) | menu (0.75) | menu (0.88) | menu (0.84) | menu (0.70) | profile (0.49) | menu (0.89) | menu (0.90) | menu (0.92) | menu (0.97) | menu (0.94) | menu (0.98) | menu (0.98) | profile (0.35) | menu (1.00) | menu (0.95) | menu (0.97) | menu (0.75) | rico-58529 |
| rico-501 | modal | modal (0.74) | modal (0.66) | modal (0.68) | modal (0.67) | modal (0.65) | modal (0.87) | modal (0.89) | modal (0.77) | modal (0.61) | modal (0.87) | modal (0.90) | modal (0.92) | modal (0.91) | modal (0.89) | modal (1.00) | modal (0.88) | login (0.47) | modal (0.82) | rico-501 |
| rico-68494 | news | news (0.68) | news (0.67) | news (0.58) | news (0.44) | news (0.39) | news (0.57) | news (0.73) | news (0.65) | news (0.82) | news (0.76) | news (0.59) | list (0.59) | list (0.57) | news (0.95) | list (1.00) | list (0.52) | news (0.86) | news (0.91) | rico-68494 |
| rico-25255 | other | news (0.55) | list (0.60) | news (0.40) | news (0.32) | news (0.51) | list (0.49) | news (0.29) | list (0.30) | other (0.47) | news (0.57) | news (0.38) | list (0.55) | list (0.59) | gallery (0.35) | list (1.00) | list (0.72) | other (0.49) | news (0.73) | rico-25255 |
| rico-1281 | profile | profile (0.88) | list (0.38) | profile (0.95) | profile (0.90) | profile (0.83) | profile (0.79) | profile (0.92) | profile (0.92) | profile (0.96) | profile (0.98) | profile (0.98) | profile (0.97) | profile (0.97) | news (0.44) | profile (1.00) | profile (0.97) | profile (0.63) | profile (0.95) | rico-1281 |
