# jnli-support

2026-11-23 · 210 labelled dev cases (entailment 70, contradiction 70, neutral 70) · split: stratified k-fold (no test case among these: CV numbers only) · source: JGLUE JNLI v1.3（Yahoo Japan, CC BY-SA 4.0）の validation から各ラベル 100 件

drex-max@openrouter has the highest coverage at 95% accuracy, 96% [93, 99] (API cost $0.10 per 10k, p99 587ms). Its interval overlaps with reflex@openrouter, mammoth@openrouter, decider@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. The highest raw accuracy (dev) is drex-max@openrouter's, 94% [91, 97]. Showing its sure accuracy is 95% or more takes about 4,498 more labels at the same error rate.

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 77.1% [72, 82] | 0.77 | 0.93 | 0.07 | 35% [29, 41] | 89.0% (81.1%) | 0.0% (0/210) | 0/210 |
| clef-omni@openrouter | 210 | 80.5% [75, 85] | 0.81 | 0.94 | 0.05 | 47% [40, 54] | 92.9% (87.1%) | 0.0% (0/210) | 0/210 |
| clef@openrouter | 210 | 86.2% [82, 90] | 0.86 | 0.98 | 0.07 | 76% [70, 81] | 94.3% (90.3%) | 0.0% (0/210) | 0/210 |
| d1-ultra@openrouter | 210 | 91.9% [89, 95] | 0.92 | 0.99 | 0.11 | 88% [84, 92] | 95.1% (91.7%) | 0.0% (0/210) | 0/210 |
| d1.1@openrouter | 210 | 90.0% [86, 94] | 0.90 | 0.99 | 0.11 | 87% [82, 91] | 94.0% (90.2%) | 0.0% (0/210) | 0/210 |
| d1.2-ultra | 210 | 89.0% [85, 93] | 0.89 | 0.99 | 0.10 | 84% [79, 89] | 93.8% (89.9%) | 0.0% (0/210) | 0/210 |
| d1.2 | 210 | 91.4% [87, 95] | 0.91 | 0.99 | 0.13 | 86% [81, 90] | 94.5% (90.8%) | 0.0% (0/210) | 0/210 |
| decider-flash@openrouter | 210 | 91.4% [87, 95] | 0.91 | 0.98 | 0.05 | 84% [80, 89] | 94.9% (91.3%) | 0.0% (0/210) | 0/210 |
| decider@openrouter | 210 | 91.9% [88, 95] | 0.92 | 0.99 | 0.03 | 91% [87, 94] | 95.8% (92.6%) | 0.0% (0/210) | 0/210 |
| decision-1.1@openrouter | 210 | 83.3% [79, 88] | 0.83 | 0.98 | 0.04 | 70% [64, 76] | 93.2% (88.7%) | 0.0% (0/210) | 0/210 |
| decision-1@openrouter | 210 | 85.7% [81, 90] | 0.86 | 0.98 | 0.03 | 83% [78, 89] | 93.1% (89.1%) | 0.0% (0/210) | 0/210 |
| drex-max@openrouter | 210 | 94.3% [91, 97] | 0.94 | 0.99 | 0.03 | 96% [93, 99] | 95.5% (92.4%) | 0.0% (0/210) | 0/210 |
| elephant@openrouter | 210 | 89.0% [85, 93] | 0.89 | 0.98 | 0.04 | 86% [81, 90] | 95.0% (91.4%) | 0.0% (0/210) | 0/210 |
| gemini-decision@google | 210 | 88.1% [84, 92] | 0.88 | 0.98 | 0.06 | 75% [70, 81] | 93.7% (89.5%) | 0.0% (0/210) | 0/210 |
| jev:1.14 | 210 | 82.4% [78, 87] | 0.83 | 0.98 | 0.04 | 62% [56, 69] | 91.6% (86.5%) | 0.0% (0/210) | 0/210 |
| joey@openrouter | 210 | 76.7% [70, 82] | 0.77 | 0.92 | 0.07 | 53% [47, 60] | 95.5% (90.8%) | 0.0% (0/210) | 0/210 |
| kev@openrouter | 210 | 81.9% [77, 87] | 0.82 | 0.94 | 0.07 | 32% [26, 38] | 91.0% (83.1%) | 0.0% (0/210) | 0/210 |
| luna@decisions | 210 | 76.2% [70, 82] | 0.76 | 0.93 | 0.13 | 19% [14, 25] | 92.5% (81.7%) | 0.0% (0/210) | 0/210 |
| mammoth@openrouter | 210 | 92.4% [89, 96] | 0.92 | 0.99 | 0.05 | 94% [91, 97] | 93.9% (90.4%) | 0.0% (0/210) | 0/210 |
| reflex@openrouter | 210 | 94.3% [91, 97] | 0.94 | 0.99 | 0.04 | 96% [93, 98] | 95.0% (91.7%) | 0.0% (0/210) | 0/210 |
| span@openrouter | 210 | 77.1% [71, 82] | 0.77 | 0.95 | 0.05 | 26% [20, 32] | 90.9% (81.8%) | 0.0% (0/210) | 0/210 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2-ultra = d1.2-ultra; d1.2 = d1.2; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | accuracy (all) | rule | constraints |
|---|---|---|---|---|
| drex-max@openrouter = | 96% [93, 99] | 94% [91, 97] | 0.55 | met |
| reflex@openrouter = | 96% [93, 98] | 94% [91, 97] | 0.74 | met |
| mammoth@openrouter = | 94% [91, 97] | 92% [89, 96] | 0.62 | met |
| decider@openrouter = | 91% [87, 94] | 92% [88, 95] | 0.64 | met |
| d1-ultra@openrouter | 88% [84, 92] | 92% [89, 95] | 0.62 | met |
| d1.1@openrouter | 87% [82, 91] | 90% [86, 94] | 0.62 | met |
| d1.2 | 86% [81, 90] | 91% [87, 95] | 0.61 | met |
| elephant@openrouter | 86% [81, 90] | 89% [85, 93] | 0.65 | met |
| decider-flash@openrouter | 84% [80, 89] | 91% [87, 95] | 0.69 | met |
| d1.2-ultra | 84% [79, 89] | 89% [85, 93] | 0.64 | met |
| decision-1@openrouter | 83% [78, 89] | 86% [81, 90] | 0.77 | met |
| clef@openrouter | 76% [70, 81] | 86% [82, 90] | 0.71 | met |
| gemini-decision@google | 75% [70, 81] | 88% [84, 92] | 0.74 | met |
| decision-1.1@openrouter | 70% [64, 76] | 83% [79, 88] | 0.83 | met |
| jev:1.14 | 62% [56, 69] | 82% [78, 87] | 0.88 | met |
| joey@openrouter | 53% [47, 60] | 77% [70, 82] | 0.75 | met |
| clef-omni@openrouter | 47% [40, 54] | 80% [75, 85] | 0.85 | met |
| clef-flash@openrouter | 35% [29, 41] | 77% [72, 82] | 0.86 | met |
| kev@openrouter | 32% [26, 38] | 82% [77, 87] | 0.99 | met |
| span@openrouter | 26% [20, 32] | 77% [71, 82] | 0.94 | met |
| luna@decisions | 19% [14, 25] | 76% [70, 82] | 0.99 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 210 | 270 ms | 447 ms | 912 ms | 1103 ms | 3.4 | 0 | 4 | $0.05 | billed |  |
| clef-omni@openrouter | 210 | 194 ms | 305 ms | 661 ms | 812 ms | 3.4 | 0 | 4 | $0.35 | billed |  |
| clef@openrouter | 210 | 254 ms | 512 ms | 2337 ms | 2866 ms | 9.2 | 0 | 4 | $0.47 | billed |  |
| d1-ultra@openrouter | 210 | 206 ms | 287 ms | 471 ms | 1195 ms | 2.3 | 0 | 4 | $0.06 | billed | ○ |
| d1.1@openrouter | 210 | 176 ms | 242 ms | 560 ms | 771 ms | 3.2 | 12 | 4 | $0.03 | billed | ○ |
| d1.2-ultra | 210 | 150 ms | 376 ms | 795 ms | 1034 ms | 5.3 | 0 | 4 | $0.06 | billed |  |
| d1.2 | 210 | 148 ms | 233 ms | 500 ms | 628 ms | 3.4 | 0 | 4 | $0.03 | billed | ○ |
| decider-flash@openrouter | 0 | — | — | — | — | — | — | — | $0.02 | billed | ○ |
| decider@openrouter | 210 | 212 ms | 322 ms | 537 ms | 553 ms | 2.5 | 57 | 4 | $0.03 | billed | ○ |
| decision-1.1@openrouter | 210 | 225 ms | 324 ms | 509 ms | 589 ms | 2.3 | 0 | 4 | $0.05 | billed |  |
| decision-1@openrouter | 210 | 249 ms | 357 ms | 565 ms | 929 ms | 2.3 | 0 | 4 | $0.05 | billed |  |
| drex-max@openrouter | 210 | 238 ms | 336 ms | 587 ms | 1439 ms | 2.5 | 0 | 4 | $0.10 | billed | ○ |
| elephant@openrouter | 210 | 175 ms | 240 ms | 494 ms | 523 ms | 2.8 | 0 | 4 | $0.06 | billed |  |
| gemini-decision@google | 210 | 242 ms | 376 ms | 486 ms | 491 ms | 2.0 | 0 | 4 | $0.18 | estimated |  |
| jev:1.14 | 210 | 96 ms | 116 ms | 387 ms | 505 ms | 4.0 | 0 | 4 | $0.19 | estimated |  |
| joey@openrouter | 210 | 172 ms | 225 ms | 466 ms | 478 ms | 2.7 | 0 | 4 | $0.02 | billed | ○ |
| kev@openrouter | 210 | 6188 ms | 7728 ms | 8162 ms | 8256 ms | 1.3 | 0 | 4 | $0.04 | billed |  |
| luna@decisions | 210 | 212 ms | 360 ms | 634 ms | 696 ms | 3.0 | 1 | 4 | $0.22 | estimated |  |
| mammoth@openrouter | 210 | 184 ms | 340 ms | 516 ms | 685 ms | 2.8 | 0 | 4 | $0.17 | billed |  |
| reflex@openrouter | 210 | 165 ms | 219 ms | 319 ms | 442 ms | 1.9 | 0 | 4 | $0.07 | billed | ○ |
| span@openrouter | 210 | 560 ms | 707 ms | 918 ms | 964 ms | 1.6 | 0 | 4 | $0.02 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2-ultra, d1.2, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0011 | 16 s (estimated, 210 calls) | 13 min | 4 |
| clef-omni@openrouter | $0.0073 | 12 s (estimated, 210 calls) | 9 min | 4 |
| clef@openrouter | $0.0099 | 19 s (estimated, 210 calls) | 15 min | 4 |
| d1-ultra@openrouter | $0.0012 | 12 s (estimated, 210 calls) | 9 min | 4 |
| d1.1@openrouter | $0.0006 | 10 s (estimated, 210 calls) | 8 min | 4 |
| d1.2-ultra | $0.0012 | 10 s (estimated, 210 calls) | 8 min | 4 |
| d1.2 | $0.0006 | 9 s (estimated, 210 calls) | 7 min | 4 |
| decider@openrouter | $0.0007 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decision-1.1@openrouter | $0.0011 | 13 s (estimated, 210 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0010 | 15 s (estimated, 210 calls) | 12 min | 4 |
| drex-max@openrouter | $0.0021 | 13 s (estimated, 210 calls) | 11 min | 4 |
| elephant@openrouter | $0.0013 | 10 s (estimated, 210 calls) | 8 min | 4 |
| gemini-decision@google | $0.0038 | 14 s (estimated, 210 calls) | 11 min | 4 |
| jev:1.14 | $0.0040 | 5 s (estimated, 210 calls) | 4 min | 4 |
| joey@openrouter | $0.0004 | 10 s (estimated, 210 calls) | 8 min | 4 |
| kev@openrouter | $0.0009 | 5 min (estimated, 210 calls) | 4.0 h | 4 |
| luna@decisions | $0.0047 | 13 s (estimated, 210 calls) | 10 min | 4 |
| mammoth@openrouter | $0.0036 | 11 s (estimated, 210 calls) | 9 min | 4 |
| reflex@openrouter | $0.0015 | 9 s (estimated, 210 calls) | 7 min | 4 |
| span@openrouter | $0.0004 | 29 s (estimated, 210 calls) | 23 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1106 | entailment | neutral | 0.92 | 冬の雪山をスキーヤーが滑っています。 |
| p2094 | contradiction | neutral | 0.92 | 青い靴を履いた男性の集団がいます。 |

**clef-omni@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p57 | contradiction | neutral | 0.91 | バットを振り下ろしたバッターがいます。 |
| p670 | contradiction | neutral | 0.91 | たくさんの人が凧を見上げています。 |
| p1857 | contradiction | neutral | 0.90 | お皿には数種類のフルーツが盛られています。 |

**clef@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p66 | neutral | entailment | 0.91 | 駅のホームに止まった列車の横に人が立っています。 |
| p1851 | contradiction | neutral | 0.90 | 小鳥たちが道に落ちたパンをつついています。 |

**decider-flash@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1852 | contradiction | neutral | 0.92 | 小鳥たちが道に落ちたパンをつついています。 |

**decider@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1392 | contradiction | entailment | 0.92 | 駅のプラットホームに電車が停車するところでず。 |

**decision-1.1@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p108 | contradiction | neutral | 0.99 | 広場のゾウの像に女の子が乗っています。 |
| p1106 | entailment | neutral | 0.99 | 冬の雪山をスキーヤーが滑っています。 |
| p1852 | contradiction | neutral | 0.96 | 小鳥たちが道に落ちたパンをつついています。 |
| p1160 | contradiction | neutral | 0.96 | 帽子 が木の枝の上でぶら下がっています。 |

**decision-1@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1106 | entailment | neutral | 0.99 | 冬の雪山をスキーヤーが滑っています。 |
| p1852 | contradiction | neutral | 0.92 | 小鳥たちが道に落ちたパンをつついています。 |
| p1933 | entailment | neutral | 0.92 | 広い草原の中に２頭の象が歩いている。 |

**drex-max@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1392 | contradiction | entailment | 0.94 | 駅のプラットホームに電車が停車するところでず。 |

**elephant@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1106 | entailment | neutral | 0.98 | 冬の雪山をスキーヤーが滑っています。 |
| p1852 | contradiction | neutral | 0.95 | 小鳥たちが道に落ちたパンをつついています。 |

**gemini-decision@google** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1852 | contradiction | neutral | 0.93 | 小鳥たちが道に落ちたパンをつついています。 |

**jev:1.14** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1852 | contradiction | neutral | 0.99 | 小鳥たちが道に落ちたパンをつついています。 |
| p1106 | entailment | neutral | 0.98 | 冬の雪山をスキーヤーが滑っています。 |
| p2094 | contradiction | neutral | 0.98 | 青い靴を履いた男性の集団がいます。 |
| p108 | contradiction | neutral | 0.96 | 広場のゾウの像に女の子が乗っています。 |
| p224 | entailment | neutral | 0.92 | 机上に携帯電話が四つ置かれています。 |

**kev@openrouter** (11)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1106 | entailment | neutral | 0.99 | 冬の雪山をスキーヤーが滑っています。 |
| p1852 | contradiction | neutral | 0.99 | 小鳥たちが道に落ちたパンをつついています。 |
| p1160 | contradiction | neutral | 0.98 | 帽子 が木の枝の上でぶら下がっています。 |
| p1159 | contradiction | neutral | 0.98 | 傘 が木の枝の上でぶら下がっています。 |
| p224 | entailment | neutral | 0.96 | 机上に携帯電話が四つ置かれています。 |
| p108 | contradiction | neutral | 0.94 | 広場のゾウの像に女の子が乗っています。 |
| p1857 | contradiction | neutral | 0.94 | お皿には数種類のフルーツが盛られています。 |
| p1068 | neutral | entailment | 0.93 | 机の上にパソコンや本などがあります。 |

**luna@decisions** (22)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1119 | contradiction | neutral | 0.99 | １台のバスが停留所を去りました。 |
| p108 | contradiction | neutral | 0.99 | 広場のゾウの像に女の子が乗っています。 |
| p1366 | contradiction | neutral | 0.98 | 2頭のシロクマが水の中であばれています。 |
| p1106 | entailment | neutral | 0.97 | 冬の雪山をスキーヤーが滑っています。 |
| p20 | contradiction | neutral | 0.97 | ソファーに座っている女の子の前で、犬が座っています。 |
| p1852 | contradiction | neutral | 0.97 | 小鳥たちが道に落ちたパンをつついています。 |
| p1857 | contradiction | neutral | 0.97 | お皿には数種類のフルーツが盛られています。 |
| p936 | contradiction | neutral | 0.97 | スキーで雪山を登っている人がいます。 |

**mammoth@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1852 | contradiction | neutral | 0.91 | 小鳥たちが道に落ちたパンをつついています。 |
| p108 | contradiction | neutral | 0.90 | 広場のゾウの像に女の子が乗っています。 |

**reflex@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p1392 | contradiction | entailment | 1.00 | 駅のプラットホームに電車が停車するところでず。 |
| p1106 | entailment | neutral | 0.99 | 冬の雪山をスキーヤーが滑っています。 |
| p909 | contradiction | entailment | 0.99 | 洗面所にバッグを持った女の子がいます。 |
| p1852 | contradiction | neutral | 0.98 | 小鳥たちが道に落ちたパンをつついています。 |
| p825 | neutral | entailment | 0.97 | 女性が３人傘をさしています。 |
| p2238 | neutral | entailment | 0.96 | 野球の選手が、ハイタッチをしています。 |
| p1830 | entailment | neutral | 0.90 | 扉のそばの壁に五つの掛け時計が掛かっています。 |

**span@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| p108 | contradiction | neutral | 0.97 | 広場のゾウの像に女の子が乗っています。 |
| p1106 | entailment | neutral | 0.96 | 冬の雪山をスキーヤーが滑っています。 |
| p1851 | contradiction | neutral | 0.94 | 小鳥たちが道に落ちたパンをつついています。 |
| p2094 | contradiction | neutral | 0.94 | 青い靴を履いた男性の集団がいます。 |
| p1852 | contradiction | neutral | 0.93 | 小鳥たちが道に落ちたパンをつついています。 |


## Cases the models disagree on (12 of 115)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2-ultra | d1.2 | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p1877 | entailment | entailment (0.89) | entailment (0.87) | entailment (0.95) | entailment (0.90) | entailment (0.89) | entailment (0.94) | entailment (0.89) | entailment (0.95) | entailment (0.96) | entailment (0.92) | entailment (0.95) | entailment (0.97) | entailment (0.95) | entailment (0.99) | entailment (0.96) | entailment (0.95) | entailment (0.84) | entailment (1.00) | entailment (0.97) | entailment (1.00) | contradiction (0.46) | テーブルの上にひまわりで飾られた花瓶が置いてあります。 |
| p2227 | neutral | neutral (0.75) | entailment (0.49) | neutral (0.90) | neutral (0.93) | neutral (0.85) | neutral (0.90) | neutral (0.87) | neutral (0.94) | neutral (0.99) | neutral (0.99) | neutral (0.98) | neutral (0.98) | neutral (0.95) | neutral (0.97) | neutral (1.00) | entailment (0.53) | neutral (0.96) | neutral (0.98) | neutral (0.94) | neutral (1.00) | neutral (0.82) | お皿の上に小さく切られたサンドイッチが乗せられています。 |
| p912 | contradiction | contradiction (0.90) | contradiction (0.93) | contradiction (0.98) | contradiction (0.97) | contradiction (0.97) | contradiction (0.98) | contradiction (0.92) | contradiction (0.98) | contradiction (1.00) | contradiction (1.00) | contradiction (1.00) | contradiction (1.00) | contradiction (1.00) | contradiction (1.00) | contradiction (1.00) | neutral (0.72) | contradiction (0.98) | contradiction (0.98) | contradiction (1.00) | contradiction (1.00) | contradiction (0.98) | 洗面所にバッグを持った女の子がいます。 |
| p1480 | entailment | neutral (0.62) | neutral (0.43) | entailment (0.95) | entailment (0.88) | entailment (0.85) | entailment (0.95) | entailment (0.83) | entailment (0.95) | entailment (0.98) | entailment (0.99) | entailment (0.95) | entailment (0.99) | entailment (0.97) | entailment (0.97) | entailment (0.93) | contradiction (0.53) | entailment (0.94) | entailment (0.99) | entailment (0.98) | entailment (1.00) | entailment (0.81) | コートでダブルスのテニスが行われています。 |
| p689 | entailment | entailment (0.70) | entailment (0.87) | entailment (0.96) | entailment (0.91) | entailment (0.78) | entailment (0.97) | entailment (0.87) | entailment (0.95) | entailment (0.99) | entailment (0.50) | entailment (0.96) | entailment (0.99) | entailment (0.93) | entailment (0.98) | entailment (0.84) | contradiction (0.41) | entailment (0.84) | entailment (0.93) | entailment (0.98) | entailment (1.00) | neutral (0.46) | 白熊が、仰向けになって寝ています。 |
| p417 | entailment | entailment (0.87) | entailment (0.90) | entailment (0.84) | neutral (0.56) | entailment (0.62) | entailment (0.93) | entailment (0.63) | entailment (0.98) | entailment (0.99) | entailment (0.87) | entailment (0.98) | entailment (0.99) | entailment (0.98) | entailment (0.70) | entailment (0.73) | entailment (0.89) | entailment (0.89) | entailment (0.53) | entailment (0.99) | entailment (1.00) | neutral (0.67) | 時計台の屋根に風見鶏が付いています。 |
| p639 | contradiction | contradiction (0.85) | contradiction (0.94) | contradiction (0.95) | contradiction (0.88) | contradiction (0.88) | contradiction (0.84) | contradiction (0.84) | contradiction (0.88) | contradiction (1.00) | contradiction (0.92) | contradiction (0.95) | contradiction (0.99) | contradiction (0.71) | contradiction (0.84) | contradiction (0.98) | contradiction (0.70) | contradiction (0.99) | neutral (0.96) | contradiction (0.94) | contradiction (1.00) | contradiction (0.62) | 建物のライトアップが消された。 |
| p1349 | entailment | entailment (0.85) | entailment (0.77) | entailment (0.93) | entailment (0.87) | entailment (0.79) | entailment (0.89) | entailment (0.84) | entailment (0.96) | entailment (0.99) | entailment (0.81) | entailment (0.75) | entailment (0.99) | entailment (0.89) | entailment (0.90) | entailment (0.74) | entailment (0.49) | entailment (0.90) | entailment (0.65) | entailment (0.54) | entailment (1.00) | neutral (0.73) | 海でサーフィンをしているところです。 |
| p1572 | entailment | entailment (0.89) | entailment (0.90) | entailment (0.94) | entailment (0.90) | entailment (0.92) | entailment (0.94) | entailment (0.87) | entailment (0.86) | entailment (0.99) | entailment (0.99) | entailment (0.85) | entailment (0.99) | entailment (0.95) | entailment (0.88) | entailment (0.99) | neutral (0.48) | entailment (0.97) | entailment (0.97) | entailment (0.99) | entailment (1.00) | entailment (0.86) | 消火栓が道端に設置がされています。 |
| p224 | entailment | contradiction (0.48) | entailment (0.43) | entailment (0.76) | entailment (0.65) | neutral (0.49) | entailment (0.74) | neutral (0.37) | neutral (0.82) | entailment (0.97) | entailment (0.44) | neutral (0.55) | entailment (0.99) | contradiction (0.83) | entailment (0.71) | neutral (0.92) | contradiction (0.49) | neutral (0.96) | entailment (0.90) | entailment (0.89) | entailment (1.00) | contradiction (0.65) | 机上に携帯電話が四つ置かれています。 |
| p1735 | entailment | entailment (0.71) | entailment (0.86) | entailment (0.85) | entailment (0.87) | entailment (0.74) | entailment (0.95) | entailment (0.63) | entailment (0.89) | entailment (0.98) | contradiction (0.71) | entailment (0.98) | entailment (0.99) | entailment (0.90) | contradiction (0.50) | entailment (0.63) | contradiction (0.83) | entailment (0.92) | neutral (0.52) | entailment (0.61) | entailment (1.00) | neutral (0.44) | 曇り空の中を戦闘機が飛んでいます。 |
| p1809 | entailment | entailment (0.81) | entailment (0.88) | entailment (0.87) | entailment (0.77) | entailment (0.78) | entailment (0.93) | entailment (0.87) | entailment (0.97) | entailment (0.99) | entailment (0.96) | entailment (0.90) | entailment (0.99) | entailment (0.93) | entailment (0.59) | entailment (0.98) | entailment (0.57) | entailment (0.98) | entailment (0.71) | entailment (0.98) | entailment (1.00) | neutral (0.51) | 草むらの向こうの草原に動物達がいます。 |
