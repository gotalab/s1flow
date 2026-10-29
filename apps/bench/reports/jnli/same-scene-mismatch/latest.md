# jnli · same-scene-mismatch

2026-10-22 · 300 labelled (neutral 100, entailment 100, contradiction 100) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: JGLUE JNLI v1.3 valid（Yahoo Japan, CC BY-SA 4.0）から各ラベル 100 件

**d1@vercel/same-scene-mismatch** has the highest accuracy (all), 93% [89, 96] (API cost $0.07 per 10k, p99 740ms). Its interval overlaps with jev@vercel/same-scene-mismatch, jev/same-scene-mismatch, luna@decisions/same-scene-mismatch, clef/same-scene-mismatch: at this many cases the difference is not shown. Latency not compared (5 with no concurrency recorded; 5 with no retries recorded): measure every candidate again at one concurrency, s1flow run jnli --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is d1@vercel/same-scene-mismatch's, 92% [89, 95].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/same-scene-mismatch | 300 | 89.0% [86, 92] | 0.89 | 0.97 | 0.07 | 82% [77, 88] | 94.8% (91.1%) | 0/300 | 0/300 |
| clef-flash/same-scene-mismatch | 300 | 82.0% [78, 86] | 0.82 | 0.96 | 0.06 | 45% [38, 51] | 92.6% (86.5%) | 0/300 | 0/300 |
| d1@vercel/same-scene-mismatch | 300 | 91.7% [89, 95] | 0.92 | 0.98 | 0.02 | 95% [91, 98] | 94.0% (90.4%) | 0/300 | 0/300 |
| jev/same-scene-mismatch | 300 | 85.3% [81, 89] | 0.85 | 0.98 | 0.04 | 71% [65, 77] | 95.3% (91.4%) | 0/300 | 0/300 |
| jev@vercel/same-scene-mismatch | 300 | 86.0% [82, 90] | 0.86 | 0.98 | 0.03 | 73% [67, 79] | 96.1% (92.4%) | 0/300 | 0/300 |
| luna@decisions/same-scene-mismatch | 300 | 85.3% [81, 89] | 0.85 | 0.97 | 0.10 | 58% [51, 65] | 94.3% (89.5%) | 0/300 | 0/300 |

Answered by: clef/same-scene-mismatch = clef; clef-flash/same-scene-mismatch = clef-flash; d1@vercel/same-scene-mismatch = liquid/d1; jev/same-scene-mismatch = jev-1.14.0 (also jev-1.13.0); jev@vercel/same-scene-mismatch = typesafe-ai/jev; luna@decisions/same-scene-mismatch = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| d1@vercel/same-scene-mismatch ◎ | 93% [89, 96] | — | met |
| jev@vercel/same-scene-mismatch | 86% [81, 90] | — | met |
| jev/same-scene-mismatch | 85% [80, 90] | — | met |
| luna@decisions/same-scene-mismatch | 84% [79, 89] | — | met |
| clef/same-scene-mismatch | 89% [85, 93] | — | met |
| clef-flash/same-scene-mismatch | 83% [78, 88] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/same-scene-mismatch | 300 | 403 ms | 703 ms | 1067 ms | 1264 ms | 2.7 | not recorded | unknown | $0.64 | estimated |  |
| clef-flash/same-scene-mismatch | 300 | 174 ms | 407 ms | 546 ms | 683 ms | 3.1 | not recorded | unknown | $0.24 | estimated |  |
| d1@vercel/same-scene-mismatch | 300 | 457 ms | 567 ms | 740 ms | 1817 ms | 1.6 | not recorded | unknown | $0.07 | billed | ○ |
| jev/same-scene-mismatch | 300 | 156 ms | 226 ms | 494 ms | 516 ms | 3.2 | not recorded | unknown | $0.22 | estimated | ○ |
| jev@vercel/same-scene-mismatch | 300 | 378 ms | 547 ms | 738 ms | 856 ms | 2.0 | not recorded | unknown | $0.22 | billed | ○ |
| luna@decisions/same-scene-mismatch | 300 | 306 ms | 588 ms | 744 ms | 1134 ms | 2.4 | not recorded | unknown | $0.29 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel/same-scene-mismatch, jev@vercel/same-scene-mismatch; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/same-scene-mismatch (list price of 2026-10-04), clef-flash/same-scene-mismatch (list price of 2026-10-04), jev/same-scene-mismatch (list price of 2026-10-03), luna@decisions/same-scene-mismatch (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/same-scene-mismatch | $0.02 | 18 s (measured, 300 calls) | 10 min | 8 |
| clef-flash/same-scene-mismatch | $0.0072 | 8 s (measured, 300 calls) | 4 min | 8 |
| d1@vercel/same-scene-mismatch | $0.0021 | 18 s (measured, 300 calls) | 10 min | 8 |
| jev/same-scene-mismatch | $0.0067 | 7 s (measured, 300 calls) | 4 min | 8 |
| jev@vercel/same-scene-mismatch | $0.0067 | 16 s (measured, 300 calls) | 9 min | 8 |
| luna@decisions/same-scene-mismatch | $0.0086 | 14 s (measured, 300 calls) | 8 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/same-scene-mismatch | 90 | 88.9% | 81% | 93.2% | 0.889 |
| clef-flash/same-scene-mismatch | 90 | 80.0% | 40% | 94.4% | 0.800 |
| d1@vercel/same-scene-mismatch | 90 | 88.9% | 94% | 91.8% | 0.889 |
| jev/same-scene-mismatch | 90 | 85.6% | 77% | 94.2% | 0.856 |
| jev@vercel/same-scene-mismatch | 90 | 86.7% | 74% | 97.0% | 0.867 |
| luna@decisions/same-scene-mismatch | 90 | 88.9% | 51% | 97.8% | 0.889 |

## Wrong at a high probability (0.9 or more)

**d1@vercel/same-scene-mismatch** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j2242 | contradiction | neutral | 0.99 | 海で水上スキーを履いてロープに掴まっている船があります。 ⇒ 海で水上スキーを履いてロープに掴まっている男性がいます。 |
| j90 | neutral | contradiction | 0.97 | 部屋に置いてあるトランクの中に猫がいます。 ⇒ 蓋の開いたアタッシュケースの中から猫が顔を出しています。 |
| j2088 | neutral | contradiction | 0.97 | 黒いソファーベッドの上に猫が寝ています。 ⇒ ソファの上に二匹の猫が丸まっています。 |
| j1942 | entailment | neutral | 0.93 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j768 | neutral | contradiction | 0.91 | 港の広場に軍用機が展示されています。 ⇒ 青空の下、広場を背景に、丸いチーズショップの看板があります。 |

**jev/same-scene-mismatch** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1942 | entailment | neutral | 0.99 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j1516 | entailment | neutral | 0.99 | 山の前に蒸気機関の貨物列車がいます。 ⇒ 貨物列車が山の前の線路の上にいます。 |
| j772 | entailment | neutral | 0.90 | 海の上でサーフィンをしている人がいます。 ⇒ 海の上で、サーファーが波に乗っています。 |

**jev@vercel/same-scene-mismatch** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1942 | entailment | neutral | 0.98 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j1516 | entailment | neutral | 0.96 | 山の前に蒸気機関の貨物列車がいます。 ⇒ 貨物列車が山の前の線路の上にいます。 |
| j1735 | entailment | contradiction | 0.92 | 曇り空の上を一機の戦闘機が飛んでいる。 ⇒ 曇り空の中を戦闘機が飛んでいます。 |
| j2088 | neutral | contradiction | 0.92 | 黒いソファーベッドの上に猫が寝ています。 ⇒ ソファの上に二匹の猫が丸まっています。 |
| j772 | entailment | neutral | 0.92 | 海の上でサーフィンをしている人がいます。 ⇒ 海の上で、サーファーが波に乗っています。 |

**luna@decisions/same-scene-mismatch** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j263 | contradiction | neutral | 0.90 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |


## Cases the models disagree on (12 of 111)

| id | label | clef | clef-flash | d1@vercel | jev | jev@vercel | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|
| j1727 | contradiction | contradiction (0.94) | contradiction (0.89) | contradiction (1.00) | contradiction (0.94) | contradiction (0.96) | neutral (0.58) | 椅子の上に猫と布と枕があります。 ⇒ ベッドの上に猫と布と枕があります。 |
| j604 | contradiction | contradiction (0.77) | contradiction (0.76) | contradiction (1.00) | contradiction (0.91) | contradiction (0.91) | neutral (0.63) | 畑で果物を収穫している人たちがいます。 ⇒ ごみの散乱した路上で、果物を売っている人たちがいます。 |
| j1955 | contradiction | contradiction (0.56) | neutral (0.50) | contradiction (1.00) | contradiction (0.98) | contradiction (0.87) | contradiction (0.60) | タイヤのパンクした赤い車の下に白い猫が座っています。 ⇒ タイヤのパンクした赤い車の下に白い猫が立っています。 |
| j1869 | contradiction | neutral (0.52) | contradiction (0.91) | contradiction (1.00) | contradiction (0.88) | contradiction (0.96) | contradiction (0.62) | 男性テニスプレイヤーがいます。 ⇒ 黄緑の服を着た女性テニスプレイヤーがテニスをしています。 |
| j1879 | contradiction | contradiction (0.85) | contradiction (0.84) | contradiction (1.00) | contradiction (0.98) | contradiction (0.99) | neutral (0.78) | 駅には水色のラッピングがされた列車が停まっています。 ⇒ 列車が走って居ます。 |
| j1451 | contradiction | contradiction (0.83) | contradiction (0.83) | contradiction (1.00) | contradiction (0.84) | contradiction (0.88) | neutral (0.52) | シャッターのまえにひとがすわっています。 ⇒ シャッターのまえに猫がすわっています。 |
| j1600 | contradiction | neutral (0.68) | neutral (0.86) | contradiction (1.00) | contradiction (0.96) | contradiction (0.99) | contradiction (0.62) | 草原の木立の中にキリンが一頭います。 ⇒ 草原の木立の中にキリンが二頭います。 |
| j1824 | contradiction | contradiction (0.77) | neutral (0.83) | contradiction (0.99) | contradiction (0.93) | contradiction (0.97) | contradiction (0.48) | トイレの窓にブラインドが設置されています。 ⇒ トイレの窓には通気口があるだけである。 |
| j1136 | contradiction | contradiction (0.83) | contradiction (0.86) | contradiction (0.99) | contradiction (0.79) | contradiction (0.91) | neutral (0.86) | 寝室にソファーがあります。 ⇒ とても広いリビングの真ん中にソファーがあります。 |
| j1455 | contradiction | contradiction (0.85) | contradiction (0.84) | contradiction (0.99) | contradiction (0.84) | contradiction (0.92) | neutral (0.77) | シャッターのまえに猫がすわっています。 ⇒ シャッターのまえにひとがすわっています。 |
| j2351 | entailment | entailment (0.94) | neutral (0.59) | entailment (0.99) | entailment (0.99) | entailment (0.99) | entailment (0.98) | 芝生の上に座り、女性が携帯電話で話しています。 ⇒ 芝生の上で、女性が座り携帯で電話をしています。 |
| j977 | neutral | neutral (0.80) | neutral (0.78) | neutral (0.93) | neutral (0.97) | neutral (0.99) | entailment (0.52) | 白いTシャツの女性が赤いハサミを手に持っています。 ⇒ 女性が赤いハサミを持って、見ています。 |
