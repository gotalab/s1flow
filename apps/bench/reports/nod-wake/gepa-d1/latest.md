# nod-wake · gepa-d1

2026-10-22 · 65 labelled (True 40, False 25) · split: leave-one-out (23 test cases of the fixed evaluation set held out) · source: cases.json

**d1@vercel/gepa-d1** has the highest coverage at 95% accuracy, 98% [93, 100] (API cost $0.11 per 10k, p99 6462ms). Its interval overlaps with clef-flash/gepa-d1, clef/gepa-d1: at this many cases the difference is not shown. Latency not compared (3 with no concurrency recorded; 3 with no retries recorded): measure every candidate again at one concurrency, s1flow run nod-wake --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is d1@vercel/gepa-d1's, 94% [88, 98]. Showing its sure accuracy is 95% or more takes about 172 more labels at the same error rate.

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/gepa-d1 | 65 | 90.8% [83, 97] | 0.92 | 1.00 | 0.07 | 93% [83, 100] | 92.3% (81.3%) | 0/80 | 0/80 |
| clef-flash/gepa-d1 | 65 | 89.2% [82, 95] | 0.91 | 0.97 | 0.10 | 83% [71, 93] | 94.3% (83.1%) | 0/80 | 0/80 |
| d1@vercel/gepa-d1 | 65 | 93.8% [88, 98] | 0.95 | 0.99 | 0.05 | 98% [93, 100] | 97.6% (88.9%) | 0/80 | 0/80 |
| luna@decisions/gepa-d1 ✕ | 64 | 95.3% [89, 100] | 0.96 | 0.98 | 0.05 | 98% [93, 100] | 95.0% (85.1%) | 0/80 | 1/80 |

Not compared: luna@decisions/gepa-d1 (1 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is neither ranked nor chosen. Ask them again: `s1flow run nod-wake --models luna@decisions/gepa-d1`

Answered by: clef/gepa-d1 = clef; clef-flash/gepa-d1 = clef-flash; d1@vercel/gepa-d1 = liquid/d1; luna@decisions/gepa-d1 = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 10, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| d1@vercel/gepa-d1 ◎ | 98% [93, 100] | 0.476 [0.000, 1.190] | 0.50 | met |
| clef-flash/gepa-d1 | 83% [71, 93] | 0.524 [0.024, 1.238] | 0.64 | met |
| clef/gepa-d1 | 93% [83, 100] | 0.714 [0.000, 1.667] | 0.70 | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/gepa-d1 | 80 | 412 ms | 646 ms | 1297 ms | 1401 ms | 3.2 | not recorded | unknown | $0.78 | estimated | ○ |
| clef-flash/gepa-d1 | 80 | 189 ms | 583 ms | 1364 ms | 1483 ms | 7.2 | not recorded | unknown | $0.29 | estimated | ○ |
| d1@vercel/gepa-d1 | 80 | 452 ms | 662 ms | 6462 ms | 6482 ms | 14.3 | not recorded | unknown | $0.11 | billed | ○ |
| luna@decisions/gepa-d1 | 79 | 265 ms | 534 ms | 632 ms | 635 ms | 2.4 | not recorded | unknown | $0.38 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Under 100 calls, a model's p99 means little more than its max.
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel/gepa-d1; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/gepa-d1 (list price of 2026-10-04), clef-flash/gepa-d1 (list price of 2026-10-04), luna@decisions/gepa-d1 (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/gepa-d1 | $0.0063 | 15 s (measured, 240 calls) | 10 min | 8 |
| clef-flash/gepa-d1 | $0.0023 | 9 s (measured, 240 calls) | 6 min | 8 |
| luna@decisions/gepa-d1 | $0.0030 | 10 s (measured, 240 calls) | 7 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 10 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold on all data |
|---|---|---|---|---|---|---|
| clef/gepa-d1 | 90.8% | 88.1% | 1 | 4 | 0.10 | 0.10 |
| clef-flash/gepa-d1 | 89.2% | 92.9% | 0 | 3 | 0.30 | 0.30 |
| d1@vercel/gepa-d1 | 93.8% | 100.0% | 0 | 0 | 0.30 | 0.30 |
| luna@decisions/gepa-d1 | 95.3% | 87.8% | 1 | 4 | 0.30 | 0.30 |

## Misses and false alarms by threshold (clef/gepa-d1)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 5 (20%) |
| 0.20 | 0 (0%) | 3 (12%) |
| 0.30 | 2 (5%) | 1 (4%) |
| 0.40 | 5 (12%) | 0 (0%) |
| 0.50 | 6 (15%) | 0 (0%) |
| 0.60 | 8 (20%) | 0 (0%) |
| 0.70 | 10 (25%) | 0 (0%) |
| 0.80 | 14 (35%) | 0 (0%) |
| 0.90 | 20 (50%) | 0 (0%) |

## Misses and false alarms by threshold (clef-flash/gepa-d1)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 14 (56%) |
| 0.20 | 1 (2%) | 7 (28%) |
| 0.30 | 2 (5%) | 4 (16%) |
| 0.40 | 3 (8%) | 3 (12%) |
| 0.50 | 4 (10%) | 3 (12%) |
| 0.60 | 8 (20%) | 1 (4%) |
| 0.70 | 15 (38%) | 0 (0%) |
| 0.80 | 24 (60%) | 0 (0%) |
| 0.90 | 35 (88%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel/gepa-d1)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 1 (2%) | 7 (28%) |
| 0.20 | 1 (2%) | 2 (8%) |
| 0.30 | 1 (2%) | 2 (8%) |
| 0.40 | 1 (2%) | 2 (8%) |
| 0.50 | 3 (8%) | 1 (4%) |
| 0.60 | 3 (8%) | 0 (0%) |
| 0.70 | 6 (15%) | 0 (0%) |
| 0.80 | 8 (20%) | 0 (0%) |
| 0.90 | 11 (28%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions/gepa-d1)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 13 (52%) |
| 0.20 | 0 (0%) | 8 (32%) |
| 0.30 | 0 (0%) | 5 (20%) |
| 0.40 | 0 (0%) | 5 (20%) |
| 0.50 | 1 (3%) | 2 (8%) |
| 0.60 | 1 (3%) | 2 (8%) |
| 0.70 | 5 (13%) | 1 (4%) |
| 0.80 | 8 (21%) | 1 (4%) |
| 0.90 | 9 (23%) | 0 (0%) |

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/gepa-d1 | 23 | 87.0% | 83% | 94.7% | 0.826 |
| clef-flash/gepa-d1 | 23 | 87.0% | 87% | 90.0% | 0.870 |
| d1@vercel/gepa-d1 | 23 | 91.3% | 100% | 91.3% | 1.000 |
| luna@decisions/gepa-d1 | 23 | 95.7% | 100% | 95.7% | 1.000 |

## Wrong at a high probability (0.9 or more)

**d1@vercel/gepa-d1** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| mouiiyo-angry-while-working | True | False | 0.91 | {"earlier": ["ユーザー: だから禁煙で大浴場あるとこって言ってるじゃん"], "agent": "失礼しました。条件を見直し… |


## Cases the models disagree on (12 of 12)

| id | label | clef | clef-flash | d1@vercel | luna@decisions | case |
|---|---|---|---|---|---|---|
| rain-bbq-musing | True | False (0.64) | True (0.72) | True (0.97) | True (0.99) | {"earlier": ["ユーザー: 明日の河原BBQ、段取りまとめて管理しといて"], "agent": "明日10時集合、多摩川河川… |
| yappari-iiya-in-progress | True | True (0.69) | False (0.72) | True (0.80) | True (0.96) | {"earlier": ["ユーザー: ドラム式洗濯機、主要な家電量販店で値段比べて"], "agent": "ヨドバシ、ビック、ケーズな… |
| plan-a-sorede | True | False (0.80) | False (0.64) | True (0.69) | True (0.92) | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| mouiiyo-angry-while-working | True | False (0.71) | False (0.87) | False (0.91) | True (0.64) | {"earlier": ["ユーザー: だから禁煙で大浴場あるとこって言ってるじゃん"], "agent": "失礼しました。条件を見直し… |
| samu | False | False (0.91) | False (0.75) | True (0.51) | False (0.79) | {"agent": "(なし。ユーザーから話しかけてきた)", "user": "寒っ"} |
| haai-while-working | False | False (0.77) | True (0.55) | False (0.90) | False (0.57) | {"earlier": ["ユーザー: 近くで土曜に子ども連れで行ける室内の遊び場探して"], "agent": "調べています。少々お待… |
| ryokai-user-action | False | False (0.70) | True (0.64) | False (0.87) | True (0.85) | {"agent": "ビザ申請の書類はそろいました。残りはパスポート用の証明写真だけなので、明日までに撮ってこのチャットに送ってください。… |
| moving-delivery | True | False (0.53) | True (0.85) | True (0.68) | True (0.78) | {"agent": "Amazon定期おトク便、次回は10月10日にミネラルウォーター2ケースをお届け予定です。", "user": "そ… |
| takai-to-booking-question | True | False (0.67) | True (0.55) | True (0.83) | True (0.65) | {"earlier": ["ユーザー: 来月の札幌、金曜夜に行って日曜に帰る便"], "agent": "JAL 金曜19:30羽田発・日… |
| hungry-pending-restaurant | True | False (0.63) | False (0.53) | False (0.60) | True (0.76) | {"earlier": ["ユーザー: 今日の夜ご飯の店、あとで探してほしい。声かけるわ"], "agent": "承知しました。お声がけ… |
| busy-later | False | False (0.74) | True (0.56) | False (0.55) | True (0.69) | {"agent": "年賀状のデザイン、和風と写真入りのどちらにしますか？締め切りは11月末です。", "user": "今手離せないから… |
| maaiika-accept-20h | True | True (0.54) | True (0.68) | False (0.50) | False (0.60) | {"earlier": ["ユーザー: 今日19時に2人で「鮨 ひかり」取れる？"], "agent": "19時は満席でした。20時なら… |
