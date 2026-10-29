# nod-wake · short

2026-10-22 · 65 labelled (True 40, False 25) · split: leave-one-out (23 test cases of the fixed evaluation set held out) · source: cases.json

**haiku@vercel/short** has the highest coverage at 95% accuracy, 100% [100, 100] (API cost $5.87 per 10k, p99 4447ms). Its interval overlaps with d1@vercel/short, jev@vercel/short: at this many cases the difference is not shown. Of those, compared by loss per case (miss 10, false alarm 1), then API cost, **d1@vercel/short** is chosen (API cost $0.10 per 10k, p99 3681ms). Latency not compared (3 with no concurrency recorded; 3 with no retries recorded): measure every candidate again at one concurrency, s1flow run nod-wake --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is jev@vercel/short's, 97% [92, 100]. Showing its sure accuracy is 95% or more takes about 19 more labels at the same error rate.

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/short | 65 | 92.3% [85, 98] | 0.94 | 0.98 | 0.10 | 90% [81, 98] | 92.1% (80.8%) | 0/80 | 0/80 |
| clef-flash/short | 65 | 81.5% [72, 91] | 0.82 | 0.99 | 0.12 | 55% [40, 69] | 95.7% (81.0%) | 0/80 | 0/80 |
| d1@vercel/short | 65 | 95.4% [89, 100] | 0.96 | 0.99 | 0.06 | 98% [93, 100] | 100.0% (93.0%) | 0/80 | 0/80 |
| flash-lite@vercel/short ※ | 65 | 92.3% [85, 98] | 0.94 | 0.92 | 0.08 | 0% [0, 0] | — (0.0%) | 0/80 | 0/80 |
| haiku@vercel/short ※ | 65 | 95.4% [89, 100] | 0.96 | 0.95 | 0.05 | 100% [100, 100] | 95.2% (85.8%) | 0/80 | 0/80 |
| jev@vercel/short | 65 | 96.9% [92, 100] | 0.98 | 0.98 | 0.03 | 98% [93, 100] | 97.6% (88.9%) | 0/80 | 0/80 |
| laya@vercel/short | 65 | 40.0% [28, 52] | 0.09 | 0.54 | 0.52 | 0% [0, 0] | — (0.0%) | 0/80 | 0/80 |
| luna@decisions/short ✕ | 64 | 92.2% [84, 98] | 0.94 | 0.99 | 0.09 | 95% [88, 100] | 94.9% (84.7%) | 0/80 | 1/80 |

Not compared: luna@decisions/short (1 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is neither ranked nor chosen. Ask them again: `s1flow run nod-wake --models luna@decisions/short`

Answered by: clef/short = clef; clef-flash/short = clef-flash; d1@vercel/short = liquid/d1; flash-lite@vercel/short = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel/short = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev@vercel/short = typesafe-ai/jev; laya@vercel/short = convaiinnovations/laya; luna@decisions/short = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 10, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| d1@vercel/short ◎ | 98% [93, 100] | 0.000 [0.000, 0.000] | 0.54 | met |
| jev@vercel/short | 98% [93, 100] | 0.024 [0.000, 0.071] | 0.69 | met |
| haiku@vercel/short | 100% [100, 100] | 0.262 [0.000, 0.786] | 1.00 | met |
| clef/short | 90% [81, 98] | 0.500 [0.000, 1.214] | 0.66 | met |
| clef-flash/short | 55% [40, 69] | 2.143 [0.952, 3.333] | 0.79 | met |
| flash-lite@vercel/short | 0% [0, 0] | 0.524 [0.024, 1.238] | — | met |
| laya@vercel/short | 0% [0, 0] | 5.738 [4.095, 7.167] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/short | 80 | 430 ms | 776 ms | 1139 ms | 1729 ms | 2.6 | not recorded | unknown | $0.75 | estimated | ○ |
| clef-flash/short | 80 | 170 ms | 351 ms | 469 ms | 519 ms | 2.8 | not recorded | unknown | $0.28 | estimated | ○ |
| d1@vercel/short | 80 | 726 ms | 1258 ms | 3681 ms | 3696 ms | 5.1 | not recorded | unknown | $0.10 | billed | ○ |
| flash-lite@vercel/short | 80 | 1070 ms | 1820 ms | 4509 ms | 5455 ms | 4.2 | not recorded | unknown | $0.97 | estimated |  |
| haiku@vercel/short | 80 | 975 ms | 1594 ms | 4447 ms | 5458 ms | 4.6 | not recorded | unknown | $5.87 | estimated | ○ |
| jev@vercel/short | 80 | 626 ms | 1424 ms | 4335 ms | 6741 ms | 6.9 | not recorded | unknown | $0.26 | billed |  |
| laya@vercel/short | 80 | 623 ms | 1443 ms | 3727 ms | 3741 ms | 6.0 | not recorded | unknown | $0.0000 | billed | ○ |
| luna@decisions/short | 79 | 268 ms | 526 ms | 602 ms | 648 ms | 2.3 | not recorded | unknown | $0.35 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Under 100 calls, a model's p99 means little more than its max.
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel/short, jev@vercel/short, laya@vercel/short; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/short (list price of 2026-10-04), clef-flash/short (list price of 2026-10-04), flash-lite@vercel/short, haiku@vercel/short, luna@decisions/short (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/short | $0.0060 | 14 s (measured, 240 calls) | 10 min | 8 |
| clef-flash/short | $0.0022 | 7 s (measured, 240 calls) | 5 min | 8 |
| luna@decisions/short | $0.0028 | 10 s (measured, 240 calls) | 7 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 10 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold on all data |
|---|---|---|---|---|---|---|
| clef/short | 92.3% | 95.2% | 0 | 2 | 0.30 | 0.30 |
| clef-flash/short | 81.5% | 81.0% | 0 | 8 | 0.10 | 0.10 |
| d1@vercel/short | 95.4% | 100.0% | 0 | 0 | 0.50 | 0.50 |
| flash-lite@vercel/short | 92.3% | 90.5% | 2 | 2 | 0.50 | 0.50 |
| haiku@vercel/short | 95.4% | 95.2% | 1 | 1 | 0.50 | 0.50 |
| jev@vercel/short | 96.9% | 97.6% | 0 | 1 | 0.50 | 0.50 |
| laya@vercel/short | 40.0% | 45.2% | 19 | 4 | 0.10 | 0.10 |
| luna@decisions/short | 92.2% | 90.2% | 1 | 3 | 0.50 | 0.50 |

## Misses and false alarms by threshold (clef/short)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 15 (60%) |
| 0.20 | 0 (0%) | 10 (40%) |
| 0.30 | 0 (0%) | 3 (12%) |
| 0.40 | 1 (2%) | 3 (12%) |
| 0.50 | 3 (8%) | 2 (8%) |
| 0.60 | 3 (8%) | 2 (8%) |
| 0.70 | 5 (12%) | 1 (4%) |
| 0.80 | 8 (20%) | 1 (4%) |
| 0.90 | 15 (38%) | 0 (0%) |

## Misses and false alarms by threshold (clef-flash/short)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 12 (48%) |
| 0.20 | 0 (0%) | 4 (16%) |
| 0.30 | 3 (8%) | 0 (0%) |
| 0.40 | 8 (20%) | 0 (0%) |
| 0.50 | 12 (30%) | 0 (0%) |
| 0.60 | 15 (38%) | 0 (0%) |
| 0.70 | 18 (45%) | 0 (0%) |
| 0.80 | 26 (65%) | 0 (0%) |
| 0.90 | 37 (92%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel/short)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 13 (52%) |
| 0.20 | 0 (0%) | 5 (20%) |
| 0.30 | 0 (0%) | 4 (16%) |
| 0.40 | 0 (0%) | 4 (16%) |
| 0.50 | 1 (2%) | 2 (8%) |
| 0.60 | 1 (2%) | 1 (4%) |
| 0.70 | 2 (5%) | 1 (4%) |
| 0.80 | 3 (8%) | 0 (0%) |
| 0.90 | 10 (25%) | 0 (0%) |

## Misses and false alarms by threshold (flash-lite@vercel/short)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 3 (8%) | 2 (8%) |
| 0.20 | 3 (8%) | 2 (8%) |
| 0.30 | 3 (8%) | 2 (8%) |
| 0.40 | 3 (8%) | 2 (8%) |
| 0.50 | 3 (8%) | 2 (8%) |
| 0.60 | 3 (8%) | 2 (8%) |
| 0.70 | 3 (8%) | 2 (8%) |
| 0.80 | 3 (8%) | 2 (8%) |
| 0.90 | 3 (8%) | 2 (8%) |

## Misses and false alarms by threshold (haiku@vercel/short)

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

## Misses and false alarms by threshold (jev@vercel/short)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 9 (36%) |
| 0.20 | 0 (0%) | 6 (24%) |
| 0.30 | 0 (0%) | 3 (12%) |
| 0.40 | 0 (0%) | 3 (12%) |
| 0.50 | 0 (0%) | 2 (8%) |
| 0.60 | 0 (0%) | 2 (8%) |
| 0.70 | 2 (5%) | 2 (8%) |
| 0.80 | 3 (8%) | 2 (8%) |
| 0.90 | 6 (15%) | 1 (4%) |

## Misses and false alarms by threshold (laya@vercel/short)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 30 (75%) | 5 (20%) |
| 0.20 | 33 (82%) | 4 (16%) |
| 0.30 | 35 (88%) | 1 (4%) |
| 0.40 | 38 (95%) | 1 (4%) |
| 0.50 | 38 (95%) | 1 (4%) |
| 0.60 | 38 (95%) | 1 (4%) |
| 0.70 | 39 (98%) | 1 (4%) |
| 0.80 | 40 (100%) | 1 (4%) |
| 0.90 | 40 (100%) | 1 (4%) |

## Misses and false alarms by threshold (luna@decisions/short)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 16 (64%) |
| 0.20 | 0 (0%) | 9 (36%) |
| 0.30 | 0 (0%) | 7 (28%) |
| 0.40 | 1 (3%) | 4 (16%) |
| 0.50 | 1 (3%) | 4 (16%) |
| 0.60 | 1 (3%) | 2 (8%) |
| 0.70 | 3 (8%) | 0 (0%) |
| 0.80 | 6 (15%) | 0 (0%) |
| 0.90 | 7 (18%) | 0 (0%) |

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/short | 23 | 91.3% | 91% | 100.0% | 0.913 |
| clef-flash/short | 23 | 87.0% | 70% | 100.0% | 0.696 |
| d1@vercel/short | 23 | 87.0% | 96% | 90.9% | 0.957 |
| flash-lite@vercel/short | 23 | 95.7% | 0% | — | 0.000 |
| haiku@vercel/short | 23 | 95.7% | 100% | 95.7% | 1.000 |
| jev@vercel/short | 23 | 95.7% | 91% | 95.2% | 0.913 |
| laya@vercel/short | 23 | 39.1% | 0% | — | 0.000 |
| luna@decisions/short | 23 | 91.3% | 96% | 95.5% | 0.957 |

## Wrong at a high probability (0.9 or more)

**flash-lite@vercel/short** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| thumbs-to-send-question | True | False | 1.00 | {"agent": "幹事の佐藤さんへ「当日は15分ほど遅れます」と送信しますか？", "user": "👍"} |
| digits-nohist | False | True | 1.00 | {"agent": "(なし。ユーザーから話しかけてきた)", "user": "0000000000"} |
| haai-while-working | False | True | 1.00 | {"earlier": ["ユーザー: 近くで土曜に子ども連れで行ける室内の遊び場探して"], "agent": "調べています。少々お待… |
| maaiika-accept-20h | True | False | 1.00 | {"earlier": ["ユーザー: 今日19時に2人で「鮨 ひかり」取れる？"], "agent": "19時は満席でした。20時なら… |
| mouiiyo-angry-while-working | True | False | 1.00 | {"earlier": ["ユーザー: だから禁煙で大浴場あるとこって言ってるじゃん"], "agent": "失礼しました。条件を見直し… |

**haiku@vercel/short** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| digits-nohist | False | True | 1.00 | {"agent": "(なし。ユーザーから話しかけてきた)", "user": "0000000000"} |
| hungry-pending-restaurant | True | False | 1.00 | {"earlier": ["ユーザー: 今日の夜ご飯の店、あとで探してほしい。声かけるわ"], "agent": "承知しました。お声がけ… |
| tashikani-change-sunday | True | False | 1.00 | {"earlier": ["ユーザー: 土曜に子どもたち連れて動物園行く予定にしといて"], "agent": "予定に入れました。ただ、… |

**jev@vercel/short** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| busy-later | False | True | 0.96 | {"agent": "年賀状のデザイン、和風と写真入りのどちらにしますか？締め切りは11月末です。", "user": "今手離せないから… |

**laya@vercel/short** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| allergy-mid-booking | True | False | 1.00 | {"earlier": ["ユーザー: 記念日ディナー、コース料理のお店予約して"], "agent": "恵比寿のフレンチ「ル・シエル」… |
| hotel-jaa-yasui | True | False | 1.00 | {"earlier": ["ユーザー: 大阪出張、10/14泊で梅田近くのビジホ"], "agent": "候補は2つです。\n1. ホテ… |
| change-to-three | True | False | 1.00 | {"earlier": ["ユーザー: 日曜のランチ、4人で予約して"], "agent": "承知しました。「トラットリア・ソーレ」に日… |
| plan-a-sorede | True | False | 0.99 | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| reminder-onegai | True | False | 0.99 | {"agent": "歯医者の予約、10月8日(水)15:30で確定しました。前日の夜にリマインダーも設定しておきましょうか？", "us… |
| wrong-file | True | False | 0.99 | {"earlier": ["ユーザー: 経費精算用に今月の領収書まとめたPDF送って"], "agent": "こちらです：receipt… |
| restaurant-iine-hold | True | False | 0.99 | {"earlier": ["ユーザー: 金曜、大学の友達とご飯行くから店探しといて"], "agent": "金曜19時、渋谷の和食「こも… |
| takai-to-booking-question | True | False | 0.99 | {"earlier": ["ユーザー: 来月の札幌、金曜夜に行って日曜に帰る便"], "agent": "JAL 金曜19:30羽田発・日… |


## Cases the models disagree on (12 of 45)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev@vercel | laya@vercel | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|
| book-yes-un | True | True (0.95) | True (0.66) | True (0.95) | True (1.00) | True (1.00) | True (0.99) | False (0.98) | True (0.98) | {"earlier": ["ユーザー: 今週末、箱根で一泊できる宿探して。2人で"], "agent": "土曜泊で「箱根湯本 翠の宿」が… |
| email-send-ok | True | True (0.81) | True (0.58) | True (0.99) | True (1.00) | True (1.00) | True (0.96) | False (0.91) | True (0.97) | {"earlier": ["ユーザー: 大家さんに、エアコン壊れたから修理お願いしたいってメール書いて"], "agent": "下書きを… |
| plan-a-sorede | True | False (0.70) | False (0.78) | True (0.61) | True (1.00) | True (1.00) | True (0.69) | False (0.99) | True (0.92) | {"agent": "引っ越し業者の見積もりが2社から届きました。A社は9月の平日午前で62,000円、B社は土曜午後で78,000円です… |
| restaurant-iine-hold | True | True (0.89) | False (0.55) | True (0.81) | True (1.00) | True (1.00) | True (0.88) | False (0.99) | True (0.97) | {"earlier": ["ユーザー: 金曜、大学の友達とご飯行くから店探しといて"], "agent": "金曜19時、渋谷の和食「こも… |
| reminder-onegai | True | True (0.95) | True (0.84) | True (0.95) | True (1.00) | True (1.00) | True (0.99) | False (0.99) | True (0.99) | {"agent": "歯医者の予約、10月8日(水)15:30で確定しました。前日の夜にリマインダーも設定しておきましょうか？", "us… |
| hotel-jaa-yasui | True | True (0.94) | True (0.72) | True (0.99) | True (1.00) | True (1.00) | True (1.00) | False (1.00) | True (0.97) | {"earlier": ["ユーザー: 大阪出張、10/14泊で梅田近くのビジホ"], "agent": "候補は2つです。\n1. ホテ… |
| change-to-three | True | True (0.98) | True (0.90) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | False (1.00) | True (0.99) | {"earlier": ["ユーザー: 日曜のランチ、4人で予約して"], "agent": "承知しました。「トラットリア・ソーレ」に日… |
| budget-to-30k | True | True (0.98) | True (0.89) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | False (0.84) | True (1.00) | {"earlier": ["ユーザー: 年末に沖縄行きたい、航空券探して"], "agent": "12/28出発・1/2戻りで、往復5万… |
| stop-unsubscribe | True | True (0.98) | True (0.90) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | False (0.93) | True (1.00) | {"earlier": ["ユーザー: いらないメルマガ全部解除しといて"], "agent": "メルマガの一括解除を進めています（12… |
| self-correct-train-date | True | True (0.97) | True (0.80) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | False (0.99) | True (0.99) | {"earlier": ["ユーザー: 15日の新幹線取って、朝イチで新大阪まで"], "agent": "10月15日(水) 東京→新大… |
| hungry-pending-restaurant | True | False (0.58) | False (0.79) | True (0.86) | True (1.00) | False (1.00) | True (0.79) | False (0.92) | True (0.72) | {"earlier": ["ユーザー: 今日の夜ご飯の店、あとで探してほしい。声かけるわ"], "agent": "承知しました。お声がけ… |
| complaint-wrong-count | True | True (0.98) | True (0.90) | True (1.00) | True (1.00) | True (1.00) | True (1.00) | False (0.97) | True (1.00) | {"earlier": ["ユーザー: 土曜の焼肉、4人で19時ね"], "agent": "予約完了しました。「炭火焼肉 まる」土曜19… |
