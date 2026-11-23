# enrico-screen

2026-11-23 · 154 labelled dev cases (form 9, gallery 9, menu 9, settings 9, bare 8, chat 8, editor 8, list 8, more) · split: stratified k-fold (no test case among these: CV numbers only) · source: Enrico (labels MIT) on Rico screenshots (CC BY 4.0): up to 12 screens per design topic, mislabelled ones replaced

elephant@openrouter has the highest coverage at 90% accuracy, 62% [55, 71] (API cost $0.31 per 10k, p99 384ms). Its interval overlaps with decider@openrouter, drex-max@openrouter, gemini-decision@google, jev:1.14, jev, clef@openrouter, clef-flash@openrouter, mammoth@openrouter, decider-flash@openrouter, decision-1.1@openrouter, d1-ultra@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is decider@openrouter's, 73% [66, 80].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 70.8% [64, 78] | 0.71 | 0.97 | 0.06 | 49% [41, 56] | 89.3% (81.6%) | 0.0% (0/154) | 0/154 |
| clef-omni@openrouter | 154 | 66.2% [58, 74] | 0.67 | 0.97 | 0.13 | 39% [32, 47] | 90.0% (81.2%) | 0.0% (0/154) | 0/154 |
| clef@openrouter | 154 | 70.8% [64, 78] | 0.71 | 0.98 | 0.06 | 50% [42, 58] | 90.9% (83.6%) | 0.0% (0/154) | 0/154 |
| d1-ultra@openrouter | 154 | 64.9% [57, 73] | 0.66 | 0.97 | 0.12 | 51% [44, 60] | 89.9% (82.5%) | 0.0% (0/154) | 0/154 |
| d1.1@openrouter | 154 | 66.2% [59, 73] | 0.68 | 0.97 | 0.13 | 44% [36, 51] | 89.6% (81.3%) | 0.0% (0/154) | 0/154 |
| d1.2 | 154 | 64.3% [56, 71] | 0.66 | 0.97 | 0.10 | 42% [34, 50] | 89.2% (80.7%) | 0.0% (0/154) | 0/154 |
| d1.2-ultra | 154 | 62.3% [55, 69] | 0.63 | 0.97 | 0.09 | 45% [38, 53] | 88.6% (80.3%) | 0.0% (0/154) | 0/154 |
| decider-flash@openrouter | 154 | 70.1% [63, 77] | 0.72 | 0.98 | 0.05 | 55% [48, 63] | 90.6% (83.7%) | 0.0% (0/154) | 0/154 |
| decider@openrouter | 154 | 72.7% [66, 80] | 0.74 | 0.99 | 0.10 | 56% [48, 64] | 88.4% (81.1%) | 0.0% (0/154) | 0/154 |
| decision-1.1@openrouter | 154 | 68.2% [60, 75] | 0.69 | 0.98 | 0.04 | 49% [41, 57] | 89.3% (81.6%) | 0.0% (0/154) | 0/154 |
| drex-max@openrouter | 154 | 71.4% [64, 79] | 0.71 | 0.98 | 0.09 | 50% [42, 58] | 84.4% (76.0%) | 0.0% (0/154) | 0/154 |
| elephant@openrouter | 154 | 72.7% [66, 80] | 0.73 | 0.98 | 0.07 | 62% [55, 71] | 89.6% (83.0%) | 0.0% (0/154) | 0/154 |
| gemini-decision@google | 154 | 71.4% [65, 79] | 0.70 | 0.98 | 0.06 | 49% [41, 57] | 89.3% (81.6%) | 0.0% (0/154) | 0/154 |
| jev | 154 | 71.4% [64, 79] | 0.71 | 0.96 | 0.07 | 47% [40, 56] | 86.3% (77.9%) | 0.0% (0/154) | 0/154 |
| jev:1.14 | 154 | 71.4% [64, 79] | 0.71 | 0.96 | 0.09 | 49% [41, 56] | 89.3% (81.6%) | 0.0% (0/154) | 0/154 |
| joey@openrouter | 154 | 57.8% [50, 66] | 0.59 | 0.95 | 0.15 | 27% [20, 34] | 90.5% (79.5%) | 0.0% (0/154) | 0/154 |
| luna@decisions | 154 | 69.5% [62, 77] | 0.70 | 0.95 | 0.19 | 25% [18, 32] | 81.6% (68.2%) | 0.0% (0/154) | 0/154 |
| mammoth@openrouter | 154 | 70.8% [64, 78] | 0.71 | 0.98 | 0.10 | 49% [42, 57] | 89.3% (81.6%) | 0.0% (0/154) | 0/154 |
| reflex@openrouter | 154 | 64.9% [58, 73] | 0.66 | 0.98 | 0.12 | 46% [39, 54] | 90.1% (82.3%) | 0.0% (0/154) | 0/154 |
| span@openrouter | 154 | 66.2% [59, 73] | 0.68 | 0.96 | 0.13 | 31% [24, 38] | 91.7% (81.9%) | 0.0% (0/154) | 0/154 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev = jev-1.14.0; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 90% accuracy | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| elephant@openrouter = | 62% [55, 71] | 73% [66, 80] | 0.73 | met |
| decider@openrouter = | 56% [48, 64] | 73% [66, 80] | 0.64 | met |
| drex-max@openrouter = | 50% [42, 58] | 71% [64, 79] | 0.85 | met |
| gemini-decision@google = | 49% [41, 57] | 71% [65, 79] | 0.70 | met |
| jev:1.14 = | 49% [41, 56] | 71% [64, 79] | 0.82 | met |
| jev = | 47% [40, 56] | 71% [64, 79] | 0.82 | met |
| clef@openrouter = | 50% [42, 58] | 71% [64, 78] | 0.73 | met |
| clef-flash@openrouter = | 49% [41, 56] | 71% [64, 78] | 0.77 | met |
| mammoth@openrouter = | 49% [42, 57] | 71% [64, 78] | 0.81 | met |
| decider-flash@openrouter = | 55% [48, 63] | 70% [63, 77] | 0.66 | met |
| decision-1.1@openrouter = | 49% [41, 57] | 68% [60, 75] | 0.75 | met |
| d1-ultra@openrouter = | 51% [44, 60] | 65% [57, 73] | 0.59 | met |
| reflex@openrouter | 46% [39, 54] | 65% [58, 73] | 0.83 | met |
| d1.2-ultra | 45% [38, 53] | 62% [55, 69] | 0.66 | met |
| d1.1@openrouter | 44% [36, 51] | 66% [59, 73] | 0.61 | met |
| d1.2 | 42% [34, 50] | 64% [56, 71] | 0.63 | met |
| clef-omni@openrouter | 39% [32, 47] | 66% [58, 74] | 0.68 | met |
| span@openrouter | 31% [24, 38] | 66% [59, 73] | 0.89 | met |
| joey@openrouter | 27% [20, 34] | 58% [50, 66] | 0.88 | met |
| luna@decisions | 25% [18, 32] | 69% [62, 77] | 1.00 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 154 | 403 ms | 586 ms | 990 ms | 1196 ms | 2.5 | 0 | 4 | $0.27 | billed |  |
| clef-omni@openrouter | 154 | 344 ms | 585 ms | 876 ms | 2387 ms | 2.5 | 0 | 4 | $1.51 | billed |  |
| clef@openrouter | 154 | 405 ms | 711 ms | 1074 ms | 1093 ms | 2.7 | 0 | 4 | $2.19 | billed |  |
| d1-ultra@openrouter | 154 | 2354 ms | 7364 ms | 9577 ms | 9983 ms | 4.1 | 16 | 4 | $0.39 | billed |  |
| d1.1@openrouter | 154 | 281 ms | 482 ms | 618 ms | 680 ms | 2.2 | 0 | 4 | $0.19 | billed |  |
| d1.2 | 154 | 416 ms | 1093 ms | 1871 ms | 2168 ms | 4.5 | 0 | 4 | $0.19 | billed |  |
| d1.2-ultra | 154 | 351 ms | 776 ms | 1503 ms | 1763 ms | 4.3 | 0 | 4 | $0.39 | billed |  |
| decider-flash@openrouter | 154 | 212 ms | 282 ms | 429 ms | 451 ms | 2.0 | 0 | 4 | $0.08 | billed | ○ |
| decider@openrouter | 154 | 323 ms | 500 ms | 962 ms | 1109 ms | 3.0 | 0 | 4 | $0.15 | billed | ○ |
| decision-1.1@openrouter | 154 | 399 ms | 462 ms | 766 ms | 867 ms | 1.9 | 0 | 4 | $0.19 | billed |  |
| drex-max@openrouter | 154 | 534 ms | 782 ms | 1306 ms | 1727 ms | 2.4 | 0 | 4 | $0.46 | billed |  |
| elephant@openrouter | 154 | 249 ms | 320 ms | 384 ms | 457 ms | 1.5 | 0 | 4 | $0.31 | billed | ○ |
| gemini-decision@google | 154 | 693 ms | 1051 ms | 1526 ms | 1774 ms | 2.2 | 0 | 4 | $1.37 | estimated |  |
| jev | 154 | 141 ms | 187 ms | 447 ms | 575 ms | 3.2 | 0 | 4 | $0.84 | estimated |  |
| jev:1.14 | 154 | 139 ms | 184 ms | 311 ms | 341 ms | 2.2 | 0 | 4 | $0.84 | estimated | ○ |
| joey@openrouter | 154 | 259 ms | 321 ms | 451 ms | 1799 ms | 1.7 | 0 | 4 | $0.09 | billed |  |
| luna@decisions | 154 | 299 ms | 603 ms | 865 ms | 884 ms | 2.9 | 0 | 4 | $0.80 | estimated |  |
| mammoth@openrouter | 154 | 280 ms | 337 ms | 395 ms | 448 ms | 1.4 | 0 | 4 | $0.88 | billed |  |
| reflex@openrouter | 154 | 756 ms | 971 ms | 1105 ms | 1121 ms | 1.5 | 0 | 4 | $0.33 | billed |  |
| span@openrouter | 154 | 655 ms | 882 ms | 1062 ms | 1090 ms | 1.6 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev (list price of 2026-10-03), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0041 | 16 s (estimated, 154 calls) | 18 min | 4 |
| clef-omni@openrouter | $0.02 | 15 s (estimated, 154 calls) | 17 min | 4 |
| clef@openrouter | $0.03 | 17 s (estimated, 154 calls) | 19 min | 4 |
| d1-ultra@openrouter | $0.0060 | 2 min (estimated, 154 calls) | 2.5 h | 4 |
| d1.1@openrouter | $0.0029 | 12 s (estimated, 154 calls) | 13 min | 4 |
| d1.2 | $0.0029 | 22 s (estimated, 154 calls) | 23 min | 4 |
| d1.2-ultra | $0.0060 | 16 s (estimated, 154 calls) | 18 min | 4 |
| decider-flash@openrouter | $0.0012 | 9 s (estimated, 154 calls) | 10 min | 4 |
| decider@openrouter | $0.0024 | 14 s (estimated, 154 calls) | 15 min | 4 |
| decision-1.1@openrouter | $0.0029 | 16 s (estimated, 154 calls) | 17 min | 4 |
| drex-max@openrouter | $0.0072 | 22 s (estimated, 154 calls) | 23 min | 4 |
| elephant@openrouter | $0.0047 | 10 s (estimated, 154 calls) | 11 min | 4 |
| gemini-decision@google | $0.02 | 28 s (estimated, 154 calls) | 31 min | 4 |
| jev | $0.01 | 6 s (estimated, 154 calls) | 6 min | 4 |
| jev:1.14 | $0.01 | 6 s (estimated, 154 calls) | 6 min | 4 |
| joey@openrouter | $0.0014 | 11 s (estimated, 154 calls) | 12 min | 4 |
| luna@decisions | $0.01 | 14 s (estimated, 154 calls) | 15 min | 4 |
| mammoth@openrouter | $0.01 | 11 s (estimated, 154 calls) | 12 min | 4 |
| reflex@openrouter | $0.0051 | 29 s (estimated, 154 calls) | 32 min | 4 |
| span@openrouter | $0.0008 | 25 s (estimated, 154 calls) | 28 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 90%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Wrong at a high probability (0.9 or more)

**clef-omni@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.91 | rico-66373 |

**decision-1.1@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.97 | rico-54536 |
| rico-37922 | profile | form | 0.95 | rico-37922 |
| rico-41068 | terms | modal | 0.90 | rico-41068 |

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

**jev** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.99 | rico-54536 |
| rico-35591 | mediaplayer | gallery | 0.97 | rico-35591 |
| rico-37073 | gallery | form | 0.97 | rico-37073 |
| rico-37922 | profile | form | 0.97 | rico-37922 |
| rico-66373 | modal | profile | 0.92 | rico-66373 |
| rico-12581 | bare | maps | 0.91 | rico-12581 |

**jev:1.14** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.99 | rico-54536 |
| rico-35591 | mediaplayer | gallery | 0.98 | rico-35591 |
| rico-37073 | gallery | form | 0.98 | rico-37073 |
| rico-37922 | profile | form | 0.96 | rico-37922 |
| rico-12581 | bare | maps | 0.92 | rico-12581 |
| rico-66373 | modal | profile | 0.91 | rico-66373 |

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

**reflex@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-54536 | list | menu | 0.97 | rico-54536 |
| rico-37922 | profile | form | 0.97 | rico-37922 |
| rico-65338 | profile | other | 0.93 | rico-65338 |
| rico-66373 | modal | profile | 0.91 | rico-66373 |

**span@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| rico-66373 | modal | profile | 0.97 | rico-66373 |
| rico-54536 | list | menu | 0.91 | rico-54536 |
| rico-39118 | other | news | 0.90 | rico-39118 |


## Cases the models disagree on (12 of 99)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev | jev:1.14 | joey@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rico-18483 | chat | news (0.73) | list (0.49) | news (0.69) | news (0.45) | other (0.31) | other (0.46) | news (0.30) | news (0.42) | news (0.50) | list (0.58) | news (0.76) | news (0.77) | list (0.50) | list (0.65) | list (0.62) | news (0.94) | list (1.00) | list (0.62) | news (0.81) | news (0.86) | rico-18483 |
| rico-10522 | editor | editor (0.90) | editor (0.82) | editor (0.98) | editor (0.96) | editor (0.95) | editor (0.90) | editor (0.87) | editor (0.96) | editor (0.97) | editor (0.99) | editor (0.99) | editor (1.00) | editor (0.99) | editor (1.00) | editor (1.00) | news (0.50) | editor (0.99) | editor (0.99) | editor (0.99) | editor (0.92) | rico-10522 |
| rico-24880 | form | form (0.82) | form (0.68) | form (0.79) | login (0.50) | form (0.68) | form (0.55) | form (0.49) | form (0.87) | form (0.79) | form (0.85) | form (0.81) | form (0.83) | form (0.89) | form (0.90) | form (0.89) | form (0.73) | form (1.00) | form (0.73) | form (0.89) | form (0.68) | rico-24880 |
| rico-3942 | list | list (0.52) | list (0.58) | list (0.44) | news (0.73) | news (0.51) | bare (0.38) | news (0.63) | list (0.44) | list (0.62) | list (0.94) | list (0.45) | list (0.94) | list (0.69) | list (0.86) | list (0.89) | news (0.36) | list (1.00) | list (0.87) | list (0.88) | news (0.85) | rico-3942 |
| rico-52193 | list | list (0.75) | list (0.71) | list (0.73) | list (0.42) | list (0.58) | list (0.56) | list (0.46) | list (0.80) | list (0.75) | list (0.94) | list (0.69) | list (0.97) | list (0.75) | list (0.96) | list (0.96) | news (0.53) | list (1.00) | list (0.83) | list (0.60) | list (0.73) | rico-52193 |
| rico-67717 | list | list (0.83) | list (0.72) | list (0.73) | news (0.52) | news (0.33) | list (0.37) | news (0.42) | list (0.80) | list (0.85) | list (0.91) | list (0.65) | list (1.00) | list (0.78) | list (0.98) | list (0.99) | news (0.29) | list (1.00) | list (0.96) | list (0.83) | news (0.46) | rico-67717 |
| rico-71299 | list | list (0.77) | list (0.71) | list (0.77) | news (0.52) | news (0.40) | list (0.41) | news (0.48) | list (0.78) | list (0.90) | list (0.94) | list (0.66) | list (0.99) | list (0.82) | list (0.99) | list (1.00) | list (0.35) | list (1.00) | list (0.97) | list (0.95) | news (0.87) | rico-71299 |
| rico-58529 | menu | menu (0.85) | menu (0.75) | menu (0.88) | menu (0.84) | menu (0.61) | menu (0.77) | menu (0.70) | menu (0.89) | menu (0.90) | menu (0.96) | menu (0.92) | menu (0.97) | menu (0.94) | menu (0.99) | menu (0.99) | profile (0.35) | menu (1.00) | menu (0.95) | menu (0.97) | menu (0.75) | rico-58529 |
| rico-68494 | news | news (0.66) | news (0.67) | news (0.58) | news (0.43) | list (0.31) | news (0.40) | news (0.48) | news (0.73) | news (0.63) | news (0.65) | news (0.82) | news (0.76) | news (0.59) | list (0.58) | list (0.57) | news (0.95) | list (1.00) | list (0.52) | news (0.86) | news (0.91) | rico-68494 |
| rico-25255 | other | news (0.57) | list (0.60) | list (0.40) | other (0.41) | news (0.53) | news (0.28) | news (0.34) | news (0.29) | list (0.30) | news (0.38) | other (0.47) | news (0.57) | news (0.38) | list (0.53) | list (0.55) | gallery (0.35) | list (1.00) | list (0.72) | other (0.55) | news (0.73) | rico-25255 |
| rico-1281 | profile | profile (0.90) | list (0.38) | profile (0.95) | profile (0.92) | profile (0.76) | profile (0.77) | profile (0.72) | profile (0.92) | profile (0.92) | profile (0.97) | profile (0.96) | profile (0.98) | profile (0.98) | profile (0.98) | profile (0.97) | news (0.44) | profile (1.00) | profile (0.97) | other (0.52) | profile (0.95) | rico-1281 |
| rico-21050 | profile | profile (0.77) | list (0.29) | profile (0.95) | profile (0.91) | profile (0.84) | profile (0.59) | profile (0.74) | profile (0.92) | profile (0.95) | profile (0.83) | profile (0.87) | profile (0.94) | profile (0.98) | profile (0.96) | profile (0.97) | news (0.81) | profile (1.00) | profile (0.98) | profile (0.67) | profile (0.78) | rico-21050 |
