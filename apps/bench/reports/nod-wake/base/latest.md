# nod-wake

2026-10-22 · 65 labelled (True 40, False 25) · split: leave-one-out (23 test cases of the fixed evaluation set held out) · source: cases.json

**jev@vercel** has the highest coverage at 95% accuracy, 98% [93, 100] (API cost $0.31 per 10k, p99 1509ms). Its interval overlaps with d1@vercel, jev, mercury@openrouter, clef-flash, clef: at this many cases the difference is not shown. Of those, compared by loss per case (miss 10, false alarm 1), then API cost, **d1@vercel** is chosen (API cost $0.06 per 10k, p99 458ms). Latency not compared (1 with no concurrency recorded; 1 with no retries recorded): measure every candidate again at one concurrency, s1flow run nod-wake --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is mercury@openrouter's, 97% [92, 100].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 65 | 93.8% [88, 98] | 0.95 | 0.99 | 0.09 | 88% [79, 98] | 91.9% (80.4%) | 0/80 | 0/80 |
| clef-flash | 65 | 92.3% [86, 98] | 0.94 | 0.97 | 0.12 | 90% [81, 98] | 92.1% (80.8%) | 0/80 | 0/80 |
| d1@vercel | 65 | 90.8% [83, 97] | 0.93 | 1.00 | 0.06 | 95% [88, 100] | 95.0% (85.1%) | 0/80 | 0/80 |
| flash-lite@vercel ※ | 65 | 90.8% [83, 97] | 0.93 | 0.90 | 0.09 | 0% [0, 0] | — (0.0%) | 0/80 | 0/80 |
| haiku@vercel ※ | 65 | 95.4% [89, 100] | 0.96 | 0.95 | 0.05 | 7% [0, 17] | 0.0% (0.0%) | 0/80 | 0/80 |
| jev | 65 | 92.3% [85, 98] | 0.94 | 0.99 | 0.09 | 98% [93, 100] | 95.1% (85.4%) | 0/80 | 0/80 |
| jev@vercel | 65 | 93.8% [88, 100] | 0.95 | 0.99 | 0.03 | 98% [93, 100] | 95.1% (85.4%) | 0/80 | 0/80 |
| kev@openrouter | 65 | 87.7% [78, 95] | 0.89 | 0.97 | 0.18 | 69% [55, 81] | 96.6% (84.7%) | 0/80 | 0/80 |
| laya@vercel | 0 | — | | | | | | 80/80 | 0/80 |
| luna@decisions ✕ | 64 | 92.2% [84, 98] | 0.94 | 0.98 | 0.05 | 83% [71, 93] | 94.1% (82.6%) | 0/80 | 1/80 |
| mercury@openrouter | 65 | 96.9% [92, 100] | 0.97 | 1.00 | 0.02 | 98% [93, 100] | 97.6% (88.9%) | 0/80 | 0/80 |
| solar@openrouter | 65 | 78.5% [68, 89] | 0.85 | 0.73 | 0.13 | 21% [10, 36] | 100.0% (71.7%) | 0/80 | 0/80 |
| tev1@openrouter | 65 | 76.9% [66, 86] | 0.78 | 0.92 | 0.06 | 57% [43, 71] | 91.7% (76.0%) | 0/80 | 0/80 |

Not compared: luna@decisions (1 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is neither ranked nor chosen. Ask them again: `s1flow run nod-wake --models luna@decisions`

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.13.0 (also jev-1.14.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mercury@openrouter = inception/mercury-decide-20260930; solar@openrouter = upstage/solar-decide-20260928; tev1@openrouter = togethercomputer/tev1-4b-experimental-20260923. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 10, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| d1@vercel ◎ | 95% [88, 100] | 0.071 [0.000, 0.143] | 0.55 | met |
| jev@vercel | 98% [93, 100] | 0.071 [0.000, 0.167] | 0.58 | met |
| jev | 98% [93, 100] | 0.071 [0.000, 0.167] | 0.55 | met |
| mercury@openrouter | 98% [93, 100] | 0.262 [0.000, 0.762] | 0.89 | met |
| clef-flash | 90% [81, 98] | 0.500 [0.000, 1.215] | 0.68 | met |
| clef | 88% [79, 98] | 0.524 [0.024, 1.238] | 0.70 | met |
| kev@openrouter | 69% [55, 81] | 1.190 [0.238, 2.143] | 0.61 | met |
| tev1@openrouter | 57% [43, 71] | 1.714 [0.714, 2.979] | 0.83 | met |
| solar@openrouter | 21% [10, 36] | 0.238 [0.119, 0.381] | 0.98 | met |
| haiku@vercel | 7% [0, 17] | 0.500 [0.000, 1.214] | — | met |
| flash-lite@vercel | 0% [0, 0] | 0.524 [0.024, 1.238] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 80 | 441 ms | 1030 ms | 1960 ms | 2065 ms | 4.4 | 0 | 1 | $0.90 | estimated |  |
| clef-flash | 80 | 226 ms | 399 ms | 522 ms | 544 ms | 2.3 | not recorded | unknown | $0.34 | estimated |  |
| d1@vercel | 80 | 331 ms | 405 ms | 458 ms | 471 ms | 1.4 | 0 | 1 | $0.06 | billed | ○ |
| flash-lite@vercel | 80 | 1078 ms | 1619 ms | 9251 ms | 9895 ms | 8.6 | not recorded | unknown | $1.14 | estimated |  |
| haiku@vercel | 80 | 906 ms | 1380 ms | 2810 ms | 2830 ms | 3.1 | not recorded | unknown | $6.99 | estimated |  |
| jev | 80 | 147 ms | 228 ms | 256 ms | 257 ms | 1.7 | 0 | 1 | $0.31 | estimated | ○ |
| jev@vercel | 80 | 258 ms | 332 ms | 1509 ms | 4983 ms | 5.8 | 0 | 1 | $0.31 | billed |  |
| kev@openrouter | 80 | 720 ms | 870 ms | 1468 ms | 1677 ms | 2.0 | 0 | 1 | $0.11 | billed |  |
| luna@decisions | 79 | 188 ms | 260 ms | 326 ms | 450 ms | 1.7 | 0 | 1 | $0.45 | estimated |  |
| mercury@openrouter | 80 | 286 ms | 425 ms | 643 ms | 676 ms | 2.3 | 0 | 1 | $0.0000 | billed | ○ |
| solar@openrouter | 80 | 661 ms | 10688 ms | 13550 ms | 13785 ms | 20.5 | not recorded | unknown | $0.30 | billed |  |
| tev1@openrouter | 80 | 541 ms | 1260 ms | 2261 ms | 2298 ms | 4.2 | not recorded | unknown | $0.14 | billed |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Under 100 calls, a model's p99 means little more than its max.
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter, mercury@openrouter, solar@openrouter, tev1@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.0072 | 2 min (measured, 240 calls) | 1.6 h | 1 |
| clef-flash | $0.0027 | 8 s (measured, 240 calls) | 6 min | 8 |
| d1@vercel | $0.0005 | 82 s (measured, 240 calls) | 57 min | 1 |
| jev | $0.0025 | 41 s (measured, 240 calls) | 28 min | 1 |
| jev@vercel | $0.0025 | 72 s (measured, 240 calls) | 50 min | 1 |
| kev@openrouter | $0.0009 | 3 min (measured, 240 calls) | 2.0 h | 1 |
| luna@decisions | $0.0035 | 51 s (measured, 237 calls) | 36 min | 1 |
| mercury@openrouter | $0.0000 | 13 min (measured, 240 calls) | 9.2 h | 1 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 10 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold on all data |
|---|---|---|---|---|---|---|
| clef | 93.8% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| clef-flash | 92.3% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| d1@vercel | 90.8% | 100.0% | 0 | 0 | 0.70 | 0.70 |
| flash-lite@vercel | 90.8% | 90.5% | 2 | 2 | 0.50 | 0.50 |
| haiku@vercel | 95.4% | 92.9% | 2 | 1 | 0.50 | 0.50 |
| jev | 92.3% | 90.5% | 1 | 3 | 0.50 | 0.50 |
| jev@vercel | 93.8% | 90.5% | 1 | 3 | 0.50 | 0.50 |
| kev@openrouter | 87.7% | 90.5% | 0 | 4 | 0.30 | 0.30 |
| luna@decisions | 92.2% | 87.8% | 1 | 4 | 0.50 | 0.50 |
| mercury@openrouter | 96.9% | 95.2% | 1 | 1 | 0.90 | 0.90 |
| solar@openrouter | 78.5% | 76.2% | 0 | 10 | 0.50 | 0.50 |
| tev1@openrouter | 76.9% | 85.7% | 1 | 5 | 0.10 | 0.10 |

## Misses and false alarms by threshold (clef)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 23 (92%) |
| 0.20 | 0 (0%) | 8 (32%) |
| 0.30 | 0 (0%) | 6 (24%) |
| 0.40 | 1 (2%) | 4 (16%) |
| 0.50 | 2 (5%) | 2 (8%) |
| 0.60 | 3 (8%) | 2 (8%) |
| 0.70 | 5 (12%) | 1 (4%) |
| 0.80 | 8 (20%) | 0 (0%) |
| 0.90 | 12 (30%) | 0 (0%) |

## Misses and false alarms by threshold (clef-flash)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 21 (84%) |
| 0.20 | 0 (0%) | 9 (36%) |
| 0.30 | 1 (2%) | 3 (12%) |
| 0.40 | 2 (5%) | 3 (12%) |
| 0.50 | 4 (10%) | 1 (4%) |
| 0.60 | 7 (18%) | 1 (4%) |
| 0.70 | 12 (30%) | 1 (4%) |
| 0.80 | 17 (42%) | 0 (0%) |
| 0.90 | 30 (75%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 21 (84%) |
| 0.20 | 0 (0%) | 16 (64%) |
| 0.30 | 0 (0%) | 11 (44%) |
| 0.40 | 0 (0%) | 8 (32%) |
| 0.50 | 0 (0%) | 6 (24%) |
| 0.60 | 0 (0%) | 3 (12%) |
| 0.70 | 0 (0%) | 1 (4%) |
| 0.80 | 1 (2%) | 0 (0%) |
| 0.90 | 4 (10%) | 0 (0%) |

## Misses and false alarms by threshold (flash-lite@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (8%) | 3 (12%) |
| 0.20 | 3 (8%) | 3 (12%) |
| 0.30 | 3 (8%) | 3 (12%) |
| 0.40 | 3 (8%) | 3 (12%) |
| 0.50 | 3 (8%) | 3 (12%) |
| 0.60 | 3 (8%) | 3 (12%) |
| 0.70 | 3 (8%) | 3 (12%) |
| 0.80 | 3 (8%) | 3 (12%) |
| 0.90 | 3 (8%) | 3 (12%) |

## Misses and false alarms by threshold (haiku@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (5%) | 1 (4%) |
| 0.20 | 2 (5%) | 1 (4%) |
| 0.30 | 2 (5%) | 1 (4%) |
| 0.40 | 2 (5%) | 1 (4%) |
| 0.50 | 2 (5%) | 1 (4%) |
| 0.60 | 2 (5%) | 1 (4%) |
| 0.70 | 2 (5%) | 1 (4%) |
| 0.80 | 2 (5%) | 1 (4%) |
| 0.90 | 2 (5%) | 1 (4%) |

## Misses and false alarms by threshold (jev)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 12 (48%) |
| 0.20 | 0 (0%) | 5 (20%) |
| 0.30 | 0 (0%) | 5 (20%) |
| 0.40 | 0 (0%) | 5 (20%) |
| 0.50 | 0 (0%) | 5 (20%) |
| 0.60 | 0 (0%) | 2 (8%) |
| 0.70 | 2 (5%) | 2 (8%) |
| 0.80 | 3 (8%) | 1 (4%) |
| 0.90 | 4 (10%) | 0 (0%) |

## Misses and false alarms by threshold (jev@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 9 (36%) |
| 0.20 | 0 (0%) | 5 (20%) |
| 0.30 | 0 (0%) | 5 (20%) |
| 0.40 | 0 (0%) | 5 (20%) |
| 0.50 | 0 (0%) | 4 (16%) |
| 0.60 | 1 (2%) | 2 (8%) |
| 0.70 | 2 (5%) | 2 (8%) |
| 0.80 | 3 (8%) | 1 (4%) |
| 0.90 | 4 (10%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 25 (100%) |
| 0.20 | 0 (0%) | 15 (60%) |
| 0.30 | 1 (2%) | 6 (24%) |
| 0.40 | 4 (10%) | 3 (12%) |
| 0.50 | 8 (20%) | 0 (0%) |
| 0.60 | 16 (40%) | 0 (0%) |
| 0.70 | 27 (68%) | 0 (0%) |
| 0.80 | 36 (90%) | 0 (0%) |
| 0.90 | 40 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 17 (68%) |
| 0.20 | 0 (0%) | 12 (48%) |
| 0.30 | 0 (0%) | 8 (32%) |
| 0.40 | 0 (0%) | 5 (20%) |
| 0.50 | 0 (0%) | 5 (20%) |
| 0.60 | 2 (5%) | 5 (20%) |
| 0.70 | 2 (5%) | 4 (16%) |
| 0.80 | 4 (10%) | 1 (4%) |
| 0.90 | 5 (13%) | 0 (0%) |

## Misses and false alarms by threshold (mercury@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (2%) | 1 (4%) |
| 0.20 | 1 (2%) | 1 (4%) |
| 0.30 | 1 (2%) | 1 (4%) |
| 0.40 | 1 (2%) | 1 (4%) |
| 0.50 | 1 (2%) | 1 (4%) |
| 0.60 | 1 (2%) | 1 (4%) |
| 0.70 | 1 (2%) | 1 (4%) |
| 0.80 | 1 (2%) | 1 (4%) |
| 0.90 | 1 (2%) | 0 (0%) |

## Misses and false alarms by threshold (solar@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 15 (60%) |
| 0.20 | 0 (0%) | 14 (56%) |
| 0.30 | 0 (0%) | 14 (56%) |
| 0.40 | 0 (0%) | 14 (56%) |
| 0.50 | 0 (0%) | 14 (56%) |
| 0.60 | 0 (0%) | 14 (56%) |
| 0.70 | 1 (2%) | 14 (56%) |
| 0.80 | 1 (2%) | 14 (56%) |
| 0.90 | 22 (55%) | 7 (28%) |

## Misses and false alarms by threshold (tev1@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 2 (5%) | 8 (32%) |
| 0.20 | 4 (10%) | 4 (16%) |
| 0.30 | 7 (18%) | 4 (16%) |
| 0.40 | 11 (28%) | 3 (12%) |
| 0.50 | 13 (32%) | 2 (8%) |
| 0.60 | 14 (35%) | 2 (8%) |
| 0.70 | 19 (48%) | 2 (8%) |
| 0.80 | 24 (60%) | 1 (4%) |
| 0.90 | 30 (75%) | 0 (0%) |

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 23 | 100.0% | 83% | 100.0% | 0.826 |
| clef-flash | 23 | 91.3% | 83% | 94.7% | 0.826 |
| d1@vercel | 23 | 87.0% | 96% | 90.9% | 0.957 |
| flash-lite@vercel | 23 | 91.3% | 0% | — | 0.000 |
| haiku@vercel | 23 | 100.0% | 0% | — | 0.000 |
| jev | 23 | 91.3% | 100% | 91.3% | 1.000 |
| jev@vercel | 23 | 95.7% | 96% | 95.5% | 0.957 |
| kev@openrouter | 23 | 87.0% | 83% | 84.2% | 0.826 |
| luna@decisions | 23 | 95.7% | 70% | 100.0% | 0.696 |
| mercury@openrouter | 23 | 100.0% | 100% | 100.0% | 1.000 |
| solar@openrouter | 23 | 82.6% | 22% | 100.0% | 0.217 |
| tev1@openrouter | 23 | 73.9% | 57% | 92.3% | 0.565 |

## Wrong at a high probability (0.9 or more)

**flash-lite@vercel** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| thumbs-to-send-question | True | False | 1.00 | {"agent": "幹事の佐藤さんへ「当日は15分ほど遅れます」と送信しますか？", "user": "👍"} |
| samu | False | True | 1.00 | {"agent": "(なし。ユーザーから話しかけてきた)", "user": "寒っ"} |
| digits-nohist | False | True | 1.00 | {"agent": "(なし。ユーザーから話しかけてきた)", "user": "0000000000"} |
| haai-while-working | False | True | 1.00 | {"earlier": ["ユーザー: 近くで土曜に子ども連れで行ける室内の遊び場探して"], "agent": "調べています。少々お待… |
| maaiika-accept-20h | True | False | 1.00 | {"earlier": ["ユーザー: 今日19時に2人で「鮨 ひかり」取れる？"], "agent": "19時は満席でした。20時なら… |
| mouiiyo-angry-while-working | True | False | 1.00 | {"earlier": ["ユーザー: だから禁煙で大浴場あるとこって言ってるじゃん"], "agent": "失礼しました。条件を見直し… |

**haiku@vercel** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| digits-nohist | False | True | 1.00 | {"agent": "(なし。ユーザーから話しかけてきた)", "user": "0000000000"} |
| plan-a-sorede | True | False | 1.00 | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| hungry-pending-restaurant | True | False | 1.00 | {"earlier": ["ユーザー: 今日の夜ご飯の店、あとで探してほしい。声かけるわ"], "agent": "承知しました。お声がけ… |

**mercury@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| plan-a-sorede | True | False | 0.92 | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |

**solar@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| ryokai-user-action | False | True | 0.95 | {"agent": "ビザ申請の書類はそろいました。残りはパスポート用の証明写真だけなので、明日までに撮ってこのチャットに送ってください。… |
| yappari-iiya-decline-offer | False | True | 0.95 | {"agent": "冷蔵庫にある鶏むね肉と白菜で作れるレシピ、いくつか送りましょうか？", "user": "やっぱりいいや"} |
| yoroshiku-already-agreed | False | True | 0.94 | {"earlier": ["ユーザー: 土曜のゴルフ、雨だったら中止にしたい"], "agent": "承知しました。土曜の朝6時に天気を… |
| ryokai-finished-report | False | True | 0.94 | {"earlier": ["ユーザー: 来週の出張、全部手配しといて"], "agent": "手配完了しました。往路：10/7 のぞみ1… |
| ok-info | False | True | 0.92 | {"agent": "お知らせです。明日10/1から、ご利用中の駐輪場の月額料金が2,000円から2,200円に変わります。お手続きは不要… |
| sw-yattoka | False | True | 0.91 | {"earlier": ["ユーザー: 型エラー全部潰して"], "agent": "tsc の型エラーが0件になりました。テストも全件通… |
| sw-deploy-thanks | False | True | 0.91 | {"earlier": ["ユーザー: さっきの修正、本番にデプロイして"], "agent": "デプロイ完了しました。本番でログイン〜… |

**tev1@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| tashikani-change-sunday | True | False | 0.93 | {"earlier": ["ユーザー: 土曜に子どもたち連れて動物園行く予定にしといて"], "agent": "予定に入れました。ただ、… |
| maaiika-accept-20h | True | False | 0.92 | {"earlier": ["ユーザー: 今日19時に2人で「鮨 ひかり」取れる？"], "agent": "19時は満席でした。20時なら… |


## Cases the models disagree on (12 of 36)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | mercury@openrouter | solar@openrouter | tev1@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| book-yes-un | True | True (0.96) | True (0.89) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | True (0.65) | True (0.99) | True (1.00) | True (0.88) | False (0.63) | {"earlier": ["ユーザー: 今週末、箱根で一泊できる宿探して。2人で"], "agent": "土曜泊で「箱根湯本 翠の宿」が… |
| email-send-ok | True | True (0.57) | True (0.71) | True (1.00) | True (1.00) | True (1.00) | True (0.99) | True (0.99) | False (0.57) | True (0.98) | True (1.00) | True (0.92) | True (0.83) | {"earlier": ["ユーザー: 大家さんに、エアコン壊れたから修理お願いしたいってメール書いて"], "agent": "下書きを… |
| plan-a-sorede | True | False (0.64) | False (0.64) | True (0.72) | True (1.00) | False (1.00) | True (0.62) | True (0.61) | False (0.57) | True (0.99) | False (0.92) | True (0.90) | False (0.81) | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| restaurant-iine-hold | True | True (0.87) | True (0.90) | True (1.00) | True (1.00) | True (1.00) | True (0.98) | True (0.99) | True (0.61) | True (0.96) | True (1.00) | True (0.91) | False (0.73) | {"earlier": ["ユーザー: 金曜、大学の友達とご飯行くから店探しといて"], "agent": "金曜19時、渋谷の和食「こも… |
| hungry-pending-restaurant | True | False (0.51) | True (0.59) | True (0.94) | True (1.00) | False (1.00) | True (0.74) | True (0.76) | True (0.52) | True (0.91) | True (0.97) | True (0.87) | True (0.71) | {"earlier": ["ユーザー: 今日の夜ご飯の店、あとで探してほしい。声かけるわ"], "agent": "承知しました。お声がけ… |
| mouiiyo-angry-while-working | True | True (0.71) | False (0.71) | True (0.86) | False (1.00) | True (1.00) | True (0.66) | True (0.59) | True (0.58) | True (0.50) | True (1.00) | True (0.64) | False (0.79) | {"earlier": ["ユーザー: だから禁煙で大浴場あるとこって言ってるじゃん"], "agent": "失礼しました。条件を見直し… |
| sw-fix-tests-un | True | True (0.96) | True (0.93) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | False (0.59) | True (1.00) | True (1.00) | True (0.93) | True (0.77) | {"earlier": ["ユーザー: npm test 回して"], "agent": "テストを実行しました。48件中3件が失敗してい… |
| cancel-scheduled-draft | True | True (0.96) | False (0.55) | True (0.97) | True (1.00) | True (1.00) | True (0.93) | True (0.96) | True (0.58) | True (0.99) | True (1.00) | True (1.00) | False (0.83) | {"earlier": ["ユーザー: 来週の町内会の議事録、下書き作っといてくれる？"], "agent": "承知しました。明日の朝ま… |
| tashikani-change-sunday | True | True (0.85) | True (0.65) | True (0.97) | True (1.00) | True (1.00) | True (0.88) | True (0.82) | False (0.70) | True (0.74) | True (0.95) | True (0.92) | False (0.93) | {"earlier": ["ユーザー: 土曜に子どもたち連れて動物園行く予定にしといて"], "agent": "予定に入れました。ただ、… |
| ok-ambiguous-choice | True | True (0.76) | True (0.69) | True (0.83) | True (1.00) | True (1.00) | True (0.98) | True (0.98) | False (0.64) | True (0.77) | True (0.99) | True (0.89) | False (0.74) | {"agent": "レンタカーは、A: コンパクトカー 1日6,600円、B: ミニバン 1日12,100円 のどちらにしますか？", … |
| yappari-iiya-in-progress | True | True (0.90) | False (0.56) | True (1.00) | True (1.00) | True (1.00) | True (0.90) | True (0.90) | False (0.62) | True (0.96) | True (1.00) | True (0.89) | False (0.57) | {"earlier": ["ユーザー: ドラム式洗濯機、主要な家電量販店で値段比べて"], "agent": "ヨドバシ、ビック、ケーズな… |
| moving-delivery | True | True (0.68) | True (0.86) | True (0.98) | True (1.00) | True (1.00) | True (0.98) | True (0.97) | True (0.61) | True (0.92) | True (0.98) | True (0.82) | False (0.64) | {"agent": "Amazon定期おトク便、次回は10月10日にミネラルウォーター2ケースをお届け予定です。", "user": "そ… |
