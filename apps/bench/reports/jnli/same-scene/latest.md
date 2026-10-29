# jnli · same-scene

2026-10-22 · 300 labelled (neutral 100, entailment 100, contradiction 100) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: JGLUE JNLI v1.3 valid（Yahoo Japan, CC BY-SA 4.0）から各ラベル 100 件

**d1@vercel/same-scene** has the highest accuracy (all), 93% [90, 96] (API cost $0.06 per 10k, p99 1646ms). Its interval overlaps with jev@vercel/same-scene, clef/same-scene: at this many cases the difference is not shown. Latency not compared (3 with no concurrency recorded; 3 with no retries recorded): measure every candidate again at one concurrency, s1flow run jnli --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is d1@vercel/same-scene's, 93% [90, 95].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/same-scene | 300 | 88.0% [84, 92] | 0.88 | 0.97 | 0.04 | 64% [57, 71] | 94.8% (90.4%) | 0/300 | 0/300 |
| clef-flash/same-scene | 300 | 84.0% [80, 88] | 0.84 | 0.97 | 0.05 | 54% [47, 60] | 94.7% (89.8%) | 0/300 | 0/300 |
| d1@vercel/same-scene | 300 | 92.7% [90, 95] | 0.93 | 0.99 | 0.04 | 94% [90, 97] | 95.4% (92.2%) | 0/300 | 0/300 |
| jev@vercel/same-scene | 300 | 87.7% [84, 91] | 0.88 | 0.99 | 0.03 | 77% [71, 83] | 94.4% (90.5%) | 0/300 | 0/300 |
| luna@decisions/same-scene | 300 | 77.7% [73, 82] | 0.77 | 0.95 | 0.04 | 33% [27, 39] | 94.2% (87.2%) | 0/300 | 0/300 |

Answered by: clef/same-scene = clef; clef-flash/same-scene = clef-flash; d1@vercel/same-scene = liquid/d1; jev@vercel/same-scene = typesafe-ai/jev; luna@decisions/same-scene = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| d1@vercel/same-scene ◎ | 93% [90, 96] | — | met |
| jev@vercel/same-scene | 87% [82, 91] | — | met |
| clef/same-scene | 87% [83, 91] | — | met |
| clef-flash/same-scene | 84% [80, 89] | — | met |
| luna@decisions/same-scene | 77% [71, 82] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/same-scene | 300 | 419 ms | 685 ms | 1057 ms | 1602 ms | 2.5 | not recorded | unknown | $0.60 | estimated | ○ |
| clef-flash/same-scene | 300 | 179 ms | 340 ms | 522 ms | 524 ms | 2.9 | not recorded | unknown | $0.22 | estimated | ○ |
| d1@vercel/same-scene | 300 | 498 ms | 643 ms | 1646 ms | 6290 ms | 3.3 | not recorded | unknown | $0.06 | billed | ○ |
| jev@vercel/same-scene | 300 | 381 ms | 571 ms | 833 ms | 1425 ms | 2.2 | not recorded | unknown | $0.21 | billed | ○ |
| luna@decisions/same-scene | 300 | 310 ms | 593 ms | 1090 ms | 1498 ms | 3.5 | not recorded | unknown | $0.26 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel/same-scene, jev@vercel/same-scene; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/same-scene (list price of 2026-10-04), clef-flash/same-scene (list price of 2026-10-04), luna@decisions/same-scene (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/same-scene | $0.02 | 18 s (measured, 300 calls) | 10 min | 8 |
| clef-flash/same-scene | $0.0067 | 8 s (measured, 300 calls) | 4 min | 8 |
| d1@vercel/same-scene | $0.0019 | 21 s (measured, 300 calls) | 12 min | 8 |
| jev@vercel/same-scene | $0.0063 | 17 s (measured, 300 calls) | 9 min | 8 |
| luna@decisions/same-scene | $0.0079 | 15 s (measured, 300 calls) | 8 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/same-scene | 90 | 90.0% | 61% | 92.7% | 0.900 |
| clef-flash/same-scene | 90 | 83.3% | 53% | 95.8% | 0.833 |
| d1@vercel/same-scene | 90 | 91.1% | 99% | 91.0% | 0.911 |
| jev@vercel/same-scene | 90 | 90.0% | 73% | 95.5% | 0.900 |
| luna@decisions/same-scene | 90 | 80.0% | 28% | 100.0% | 0.800 |

## Wrong at a high probability (0.9 or more)

**clef/same-scene** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1210 | neutral | entailment | 0.94 | 棚の上にバナナの房がたくさん並んでいます。 ⇒ 商品棚にたくさんのバナナが置かれています。 |
| j1146 | neutral | entailment | 0.94 | 水の入ったガラス容器に、植物が活けられています。 ⇒ 水の入ったコップに植物が入っています。 |
| j263 | contradiction | neutral | 0.94 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j994 | contradiction | neutral | 0.93 | 男性がサーフボードを持って立っている。 ⇒ 男性がサーフボードとパドルを使って波に乗っている。 |
| j771 | entailment | neutral | 0.91 | サーファーが波に乗って立っています。 ⇒ 海にて、サーファーが波に乗っています。 |
| j2232 | contradiction | neutral | 0.90 | 帽子をかぶった子供がバットを持っている。 ⇒ ヘルメットをかぶった子供が野球のバットを持っています。 |

**clef-flash/same-scene** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j263 | contradiction | neutral | 0.93 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j1600 | contradiction | neutral | 0.93 | 草原の木立の中にキリンが一頭います。 ⇒ 草原の木立の中にキリンが二頭います。 |

**d1@vercel/same-scene** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j2242 | contradiction | neutral | 0.98 | 海で水上スキーを履いてロープに掴まっている船があります。 ⇒ 海で水上スキーを履いてロープに掴まっている男性がいます。 |
| j2088 | neutral | contradiction | 0.97 | 黒いソファーベッドの上に猫が寝ています。 ⇒ ソファの上に二匹の猫が丸まっています。 |
| j90 | neutral | contradiction | 0.92 | 部屋に置いてあるトランクの中に猫がいます。 ⇒ 蓋の開いたアタッシュケースの中から猫が顔を出しています。 |
| j1942 | entailment | neutral | 0.91 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |

**jev@vercel/same-scene** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j605 | contradiction | neutral | 0.96 | 歩道で、野菜を販売してる人達がいます。 ⇒ 歩道で、フルーツを販売してる人達がいます。 |
| j1942 | entailment | neutral | 0.95 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j735 | entailment | neutral | 0.95 | 帽子を被った男児が芝生の上で凧を揚げている。 ⇒ 広場で凧を揚げている子どもがいます。 |
| j2232 | contradiction | neutral | 0.92 | 帽子をかぶった子供がバットを持っている。 ⇒ ヘルメットをかぶった子供が野球のバットを持っています。 |

**luna@decisions/same-scene** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j263 | contradiction | neutral | 0.92 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j629 | contradiction | neutral | 0.92 | 男性が傘を差して立っています。 ⇒ 男性がハンモックに座って傘を差しています。 |
| j728 | contradiction | neutral | 0.90 | 椅子の背もたれに太陽電池のパネルが取り付けられています。 ⇒ 机に太陽電池のパネルが取り付けられています。 |


## Cases the models disagree on (12 of 118)

| id | label | clef | clef-flash | d1@vercel | jev@vercel | luna@decisions | case |
|---|---|---|---|---|---|---|---|
| j1652 | neutral | neutral (0.96) | contradiction (0.56) | neutral (0.97) | neutral (1.00) | neutral (0.97) | 個室のトイレには赤い花が活けてあります。 ⇒ ベージュを基調としたトイレットルームです。 |
| j368 | neutral | neutral (0.95) | neutral (0.84) | neutral (0.99) | neutral (1.00) | entailment (0.50) | 雪原の斜面に、スキーを履いた人が２人並び、下方を見ている。 ⇒ 雪の斜面に、黒いウエアを着た2人が立っています。 |
| j1060 | contradiction | contradiction (0.95) | contradiction (0.88) | contradiction (1.00) | contradiction (0.99) | neutral (0.50) | 砂の上にウマを連れた男性が立っています。 ⇒ 砂の上にウマを連れた男性が寝ています。 |
| j1335 | contradiction | contradiction (0.90) | contradiction (0.96) | contradiction (1.00) | contradiction (0.88) | neutral (0.49) | 黒いスキーウェアを着た人がスキーをしています。 ⇒ 赤いスキーウェアを着た人がスキーをしています。 |
| j1727 | contradiction | contradiction (0.78) | contradiction (0.88) | contradiction (1.00) | contradiction (0.84) | neutral (0.83) | 椅子の上に猫と布と枕があります。 ⇒ ベッドの上に猫と布と枕があります。 |
| j865 | contradiction | contradiction (0.52) | contradiction (0.70) | contradiction (1.00) | contradiction (0.73) | neutral (0.62) | 歩道の上に消火栓が設置されています。 ⇒ 芝生の上に消火栓が設置されています。 |
| j1879 | contradiction | contradiction (0.88) | contradiction (0.89) | contradiction (1.00) | contradiction (0.99) | neutral (0.75) | 駅には水色のラッピングがされた列車が停まっています。 ⇒ 列車が走って居ます。 |
| j1341 | contradiction | contradiction (0.91) | contradiction (0.96) | contradiction (0.99) | contradiction (0.90) | neutral (0.65) | 白いスキーウェアを着た人がスキーをしています。 ⇒ 黒いスキーウェアを着た人がスキーをしています。 |
| j1452 | contradiction | contradiction (0.82) | contradiction (0.91) | contradiction (0.99) | contradiction (0.93) | neutral (0.89) | シャッターのまえにひとが立っています。 ⇒ シャッターのまえにひとがすわっています。 |
| j1451 | contradiction | contradiction (0.55) | contradiction (0.79) | contradiction (0.99) | contradiction (0.74) | neutral (0.66) | シャッターのまえにひとがすわっています。 ⇒ シャッターのまえに猫がすわっています。 |
| j1869 | contradiction | contradiction (0.58) | contradiction (0.94) | contradiction (0.99) | contradiction (0.88) | neutral (0.55) | 男性テニスプレイヤーがいます。 ⇒ 黄緑の服を着た女性テニスプレイヤーがテニスをしています。 |
| j1824 | contradiction | contradiction (0.84) | neutral (0.84) | contradiction (0.99) | contradiction (0.97) | neutral (0.53) | トイレの窓にブラインドが設置されています。 ⇒ トイレの窓には通気口があるだけである。 |
