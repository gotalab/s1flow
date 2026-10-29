# nod-wake · gepa-jev

2026-10-22 · 65 labelled (True 40, False 25) · split: leave-one-out (23 test cases of the fixed evaluation set held out) · source: cases.json

**jev@vercel/gepa-jev** has the highest coverage at 95% accuracy, 98% [93, 100] (API cost $0.29 per 10k, p99 829ms). Its interval overlaps with clef/gepa-jev, clef-flash/gepa-jev: at this many cases the difference is not shown. Latency not compared (3 with no concurrency recorded; 3 with no retries recorded): measure every candidate again at one concurrency, s1flow run nod-wake --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is clef/gepa-jev's, 94% [88, 98]. Its sure accuracy is close to the target: showing it is 95% or more takes over 5,000 labels.

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/gepa-jev | 65 | 93.8% [88, 98] | 0.95 | 0.99 | 0.08 | 95% [88, 100] | 95.0% (85.1%) | 0/80 | 0/80 |
| clef-flash/gepa-jev | 65 | 89.2% [82, 95] | 0.91 | 0.99 | 0.11 | 93% [83, 100] | 92.3% (81.3%) | 0/80 | 0/80 |
| jev@vercel/gepa-jev | 65 | 93.8% [88, 98] | 0.95 | 0.99 | 0.04 | 98% [93, 100] | 95.1% (85.4%) | 0/80 | 0/80 |
| luna@decisions/gepa-jev ✕ | 64 | 98.4% [95, 100] | 0.99 | 1.00 | 0.14 | 98% [93, 100] | 97.5% (88.7%) | 0/80 | 1/80 |

Not compared: luna@decisions/gepa-jev (1 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is neither ranked nor chosen. Ask them again: `s1flow run nod-wake --models luna@decisions/gepa-jev`

Answered by: clef/gepa-jev = clef; clef-flash/gepa-jev = clef-flash; jev@vercel/gepa-jev = typesafe-ai/jev; luna@decisions/gepa-jev = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 10, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| jev@vercel/gepa-jev ◎ | 98% [93, 100] | 0.500 [0.000, 1.238] | 0.66 | met |
| clef/gepa-jev | 95% [88, 100] | 0.500 [0.000, 1.214] | 0.56 | met |
| clef-flash/gepa-jev | 93% [83, 100] | 0.738 [0.024, 1.667] | 0.59 | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/gepa-jev | 80 | 389 ms | 649 ms | 939 ms | 979 ms | 2.4 | not recorded | unknown | $0.83 | estimated |  |
| clef-flash/gepa-jev | 80 | 170 ms | 385 ms | 584 ms | 757 ms | 3.4 | not recorded | unknown | $0.31 | estimated | ○ |
| jev@vercel/gepa-jev | 80 | 355 ms | 516 ms | 829 ms | 894 ms | 2.3 | not recorded | unknown | $0.29 | billed | ○ |
| luna@decisions/gepa-jev | 79 | 270 ms | 555 ms | 590 ms | 599 ms | 2.2 | not recorded | unknown | $0.40 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Under 100 calls, a model's p99 means little more than its max.
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: jev@vercel/gepa-jev; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/gepa-jev (list price of 2026-10-04), clef-flash/gepa-jev (list price of 2026-10-04), luna@decisions/gepa-jev (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/gepa-jev | $0.0067 | 13 s (measured, 240 calls) | 9 min | 8 |
| clef-flash/gepa-jev | $0.0025 | 7 s (measured, 240 calls) | 5 min | 8 |
| luna@decisions/gepa-jev | $0.0032 | 10 s (measured, 240 calls) | 7 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 10 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold on all data |
|---|---|---|---|---|---|---|
| clef/gepa-jev | 93.8% | 73.8% | 1 | 10 | 0.10 | 0.10 |
| clef-flash/gepa-jev | 89.2% | 83.3% | 1 | 6 | 0.10 | 0.10 |
| jev@vercel/gepa-jev | 93.8% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| luna@decisions/gepa-jev | 98.4% | 97.6% | 0 | 1 | 0.50 | 0.50 |

## Misses and false alarms by threshold (clef/gepa-jev)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 13 (52%) |
| 0.20 | 0 (0%) | 5 (20%) |
| 0.30 | 2 (5%) | 3 (12%) |
| 0.40 | 2 (5%) | 1 (4%) |
| 0.50 | 3 (8%) | 1 (4%) |
| 0.60 | 4 (10%) | 1 (4%) |
| 0.70 | 6 (15%) | 0 (0%) |
| 0.80 | 7 (18%) | 0 (0%) |
| 0.90 | 14 (35%) | 0 (0%) |

## Misses and false alarms by threshold (clef-flash/gepa-jev)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 7 (28%) |
| 0.20 | 0 (0%) | 3 (12%) |
| 0.30 | 4 (10%) | 2 (8%) |
| 0.40 | 4 (10%) | 2 (8%) |
| 0.50 | 6 (15%) | 1 (4%) |
| 0.60 | 8 (20%) | 0 (0%) |
| 0.70 | 14 (35%) | 0 (0%) |
| 0.80 | 20 (50%) | 0 (0%) |
| 0.90 | 29 (72%) | 0 (0%) |

## Misses and false alarms by threshold (jev@vercel/gepa-jev)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 5 (20%) |
| 0.20 | 0 (0%) | 3 (12%) |
| 0.30 | 0 (0%) | 3 (12%) |
| 0.40 | 1 (2%) | 2 (8%) |
| 0.50 | 2 (5%) | 2 (8%) |
| 0.60 | 3 (8%) | 2 (8%) |
| 0.70 | 5 (12%) | 1 (4%) |
| 0.80 | 9 (22%) | 0 (0%) |
| 0.90 | 10 (25%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions/gepa-jev)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 17 (68%) |
| 0.20 | 0 (0%) | 10 (40%) |
| 0.30 | 0 (0%) | 8 (32%) |
| 0.40 | 0 (0%) | 3 (12%) |
| 0.50 | 0 (0%) | 1 (4%) |
| 0.60 | 2 (5%) | 0 (0%) |
| 0.70 | 8 (21%) | 0 (0%) |
| 0.80 | 9 (23%) | 0 (0%) |
| 0.90 | 13 (33%) | 0 (0%) |

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/gepa-jev | 23 | 95.7% | 100% | 95.7% | 1.000 |
| clef-flash/gepa-jev | 23 | 87.0% | 96% | 86.4% | 0.957 |
| jev@vercel/gepa-jev | 23 | 95.7% | 91% | 100.0% | 0.913 |
| luna@decisions/gepa-jev | 23 | 100.0% | 100% | 100.0% | 1.000 |

## Wrong at a high probability (0.9 or more)

None.

## Cases the models disagree on (12 of 11)

| id | label | clef | clef-flash | jev@vercel | luna@decisions | case |
|---|---|---|---|---|---|---|
| plan-a-sorede | True | False (0.76) | False (0.71) | True (0.67) | True (0.95) | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| ryokai-user-action | False | False (0.83) | False (0.83) | False (0.93) | True (0.52) | {"agent": "ビザ申請の書類はそろいました。残りはパスポート用の証明写真だけなので、明日までに撮ってこのチャットに送ってください。… |
| yappari-iiya-in-progress | True | True (0.93) | False (0.78) | True (0.73) | True (0.85) | {"earlier": ["ユーザー: ドラム式洗濯機、主要な家電量販店で値段比べて"], "agent": "ヨドバシ、ビック、ケーズな… |
| question-mark-only | True | True (0.66) | False (0.70) | True (0.68) | True (0.92) | {"agent": "ご指定の条件では該当がなかったため、SGL→DBLユースでの手配となります。差額はバウチャー精算です。", "use… |
| yappari-iiya-decline-offer | False | True (0.67) | False (0.88) | True (0.74) | False (0.59) | {"agent": "冷蔵庫にある鶏むね肉と白菜で作れるレシピ、いくつか送りましょうか？", "user": "やっぱりいいや"} |
| mouiiyo-angry-while-working | True | True (0.84) | False (0.76) | True (0.55) | True (0.66) | {"earlier": ["ユーザー: だから禁煙で大浴場あるとこって言ってるじゃん"], "agent": "失礼しました。条件を見直し… |
| atode-yomu | False | False (0.84) | True (0.52) | False (0.84) | False (0.63) | {"earlier": ["ユーザー: ふるさと納税、おすすめの返礼品調べて"], "agent": "調査結果をまとめました。\n1. … |
| cancel-scheduled-draft | True | True (0.83) | False (0.54) | False (0.66) | True (0.77) | {"earlier": ["ユーザー: 来週の町内会の議事録、下書き作っといてくれる？"], "agent": "承知しました。明日の朝ま… |
| moving-delivery | True | False (0.74) | True (0.82) | True (0.76) | True (0.58) | {"agent": "Amazon定期おトク便、次回は10月10日にミネラルウォーター2ケースをお届け予定です。", "user": "そ… |
| busy-later | False | False (0.66) | False (0.56) | True (0.61) | False (0.63) | {"agent": "年賀状のデザイン、和風と写真入りのどちらにしますか？締め切りは11月末です。", "user": "今手離せないから… |
| hungry-pending-restaurant | True | False (0.55) | True (0.59) | False (0.58) | True (0.61) | {"earlier": ["ユーザー: 今日の夜ご飯の店、あとで探してほしい。声かけるわ"], "agent": "承知しました。お声がけ… |
