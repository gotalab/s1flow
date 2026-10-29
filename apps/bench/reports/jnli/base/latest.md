# jnli

2026-10-22 · 300 labelled (neutral 100, entailment 100, contradiction 100) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: JGLUE JNLI v1.3 valid（Yahoo Japan, CC BY-SA 4.0）から各ラベル 100 件

**d1@vercel** has the highest accuracy (all), 93% [90, 96] (API cost $0.06 per 10k, p99 1701ms). Its interval overlaps with tev1@openrouter, jev@vercel, clef-flash, clef, flash-lite@vercel, haiku@vercel: at this many cases the difference is not shown. Latency not compared (7 with no concurrency recorded; 7 with no retries recorded): measure every candidate again at one concurrency, s1flow run jnli --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is d1@vercel's, 93% [90, 96].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 87.3% [84, 91] | 0.88 | 0.97 | 0.05 | 60% [53, 67] | 94.4% (89.8%) | 0/300 | 0/300 |
| clef-flash | 300 | 85.3% [81, 89] | 0.86 | 0.97 | 0.05 | 63% [57, 69] | 94.7% (90.3%) | 0/300 | 0/300 |
| d1@vercel | 300 | 93.0% [90, 96] | 0.93 | 0.99 | 0.02 | 97% [94, 99] | 95.1% (91.8%) | 0/300 | 0/300 |
| flash-lite@vercel ※ | 300 | 89.7% [86, 93] | 0.90 | 0.92 | 0.10 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| haiku@vercel ※ | 300 | 89.3% [86, 93] | 0.90 | 0.92 | 0.11 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev | 300 | 84.0% [80, 88] | 0.84 | 0.98 | 0.02 | 61% [54, 67] | 94.5% (90.0%) | 0/300 | 0/300 |
| jev@vercel | 300 | 87.0% [83, 91] | 0.87 | 0.98 | 0.04 | 70% [63, 76] | 94.5% (90.3%) | 0/300 | 0/300 |
| kev@openrouter | 300 | 79.7% [75, 84] | 0.80 | 0.95 | 0.12 | 31% [25, 38] | 92.4% (84.7%) | 0/300 | 0/300 |
| laya@vercel | 300 | 79.3% [75, 84] | 0.79 | 0.91 | 0.12 | 0% [0, 1] | 0.0% (0.0%) | 0/300 | 0/300 |
| luna@decisions | 300 | 80.3% [76, 85] | 0.80 | 0.96 | 0.05 | 29% [22, 34] | 90.0% (81.2%) | 0/300 | 0/300 |
| mercury@openrouter ✕ | 271 | 93.4% [90, 96] | 0.93 | 0.99 | 0.02 | 99% [98, 100] | 95.2% (91.8%) | 0/300 | 29/300 |
| solar@openrouter | 300 | 79.0% [74, 83] | 0.80 | 0.85 | 0.15 | 1% [0, 2] | 50.0% (2.5%) | 0/300 | 0/300 |
| tev1@openrouter | 300 | 86.7% [83, 90] | 0.87 | 0.96 | 0.06 | 82% [78, 87] | 94.8% (91.1%) | 0/300 | 0/300 |

Not compared: mercury@openrouter (29 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is neither ranked nor chosen. Ask them again: `s1flow run jnli --models mercury@openrouter`

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; laya@vercel = convaiinnovations/laya; luna@decisions = gpt-6-luna; mercury@openrouter = inception/mercury-decide-20260930; solar@openrouter = upstage/solar-decide-20260928; tev1@openrouter = togethercomputer/tev1-4b-experimental-20260923. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| d1@vercel ◎ | 93% [90, 96] | — | met |
| tev1@openrouter | 88% [84, 92] | — | met |
| jev@vercel | 86% [81, 90] | — | met |
| clef-flash | 87% [82, 91] | — | met |
| clef | 88% [83, 92] | — | met |
| flash-lite@vercel | 91% [87, 95] | — | met |
| haiku@vercel | 90% [85, 93] | — | met |
| jev | 82% [77, 88] | — | met |
| laya@vercel | 80% [74, 85] | — | met |
| luna@decisions | 79% [73, 84] | — | met |
| kev@openrouter | 78% [72, 83] | — | met |
| solar@openrouter | 76% [70, 81] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 414 ms | 663 ms | 1059 ms | 1451 ms | 2.6 | not recorded | unknown | $0.56 | estimated |  |
| clef-flash | 300 | 275 ms | 437 ms | 562 ms | 848 ms | 2.0 | not recorded | unknown | $0.21 | estimated | ○ |
| d1@vercel | 300 | 654 ms | 1020 ms | 1701 ms | 1837 ms | 2.6 | not recorded | unknown | $0.06 | billed | ○ |
| flash-lite@vercel | 300 | 1134 ms | 1621 ms | 3593 ms | 8172 ms | 3.2 | not recorded | unknown | $0.75 | estimated |  |
| haiku@vercel | 300 | 956 ms | 1364 ms | 3365 ms | 8527 ms | 3.5 | not recorded | unknown | $4.44 | estimated |  |
| jev | 300 | 161 ms | 221 ms | 275 ms | 346 ms | 1.7 | not recorded | unknown | $0.20 | estimated | ○ |
| jev@vercel | 300 | 596 ms | 916 ms | 1600 ms | 6575 ms | 2.7 | not recorded | unknown | $0.20 | billed |  |
| kev@openrouter | 300 | 724 ms | 888 ms | 1405 ms | 2028 ms | 1.9 | not recorded | unknown | $0.05 | billed | ○ |
| laya@vercel | 300 | 616 ms | 1005 ms | 1691 ms | 2136 ms | 2.7 | not recorded | unknown | $0.0000 | billed | ○ |
| luna@decisions | 300 | 258 ms | 299 ms | 352 ms | 420 ms | 1.4 | not recorded | unknown | $0.24 | estimated |  |
| mercury@openrouter | 271 | 359 ms | 986 ms | 3925 ms | 3984 ms | 10.9 | not recorded | unknown | $0.0000 | billed |  |
| solar@openrouter | 300 | 398 ms | 5329 ms | 12897 ms | 16554 ms | 32.4 | not recorded | unknown | $0.22 | billed |  |
| tev1@openrouter | 300 | 429 ms | 518 ms | 947 ms | 1537 ms | 2.2 | not recorded | unknown | $0.08 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter, laya@vercel, mercury@openrouter, solar@openrouter, tev1@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.02 | 17 s (measured, 300 calls) | 9 min | 8 |
| clef-flash | $0.0063 | 11 s (measured, 300 calls) | 6 min | 8 |
| luna@decisions | $0.0072 | 10 s (measured, 300 calls) | 6 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 90 | 86.7% | 51% | 95.7% | 0.867 |
| clef-flash | 90 | 82.2% | 58% | 94.2% | 0.822 |
| d1@vercel | 90 | 92.2% | 99% | 92.1% | 0.922 |
| flash-lite@vercel | 90 | 86.7% | 0% | — | 0.867 |
| haiku@vercel | 90 | 88.9% | 0% | — | 0.889 |
| jev | 90 | 87.8% | 52% | 95.7% | 0.878 |
| jev@vercel | 90 | 90.0% | 53% | 97.9% | 0.900 |
| kev@openrouter | 90 | 84.4% | 34% | 93.5% | 0.844 |
| laya@vercel | 90 | 78.9% | 0% | — | 0.789 |
| luna@decisions | 90 | 83.3% | 30% | 96.3% | 0.833 |
| mercury@openrouter | 82 | 89.0% | 98% | 90.0% | 0.890 |
| solar@openrouter | 90 | 85.6% | 0% | — | 0.856 |
| tev1@openrouter | 90 | 83.3% | 84% | 86.8% | 0.833 |

## Wrong at a high probability (0.9 or more)

**clef** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j263 | contradiction | neutral | 0.96 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j771 | entailment | neutral | 0.95 | サーファーが波に乗って立っています。 ⇒ 海にて、サーファーが波に乗っています。 |
| j994 | contradiction | neutral | 0.94 | 男性がサーフボードを持って立っている。 ⇒ 男性がサーフボードとパドルを使って波に乗っている。 |
| j1210 | neutral | entailment | 0.93 | 棚の上にバナナの房がたくさん並んでいます。 ⇒ 商品棚にたくさんのバナナが置かれています。 |
| j2232 | contradiction | neutral | 0.93 | 帽子をかぶった子供がバットを持っている。 ⇒ ヘルメットをかぶった子供が野球のバットを持っています。 |
| j1236 | neutral | entailment | 0.91 | 道路に二階建てバスが通行しています。 ⇒ 街中をダブルデッカーバスが走っています。 |
| j385 | contradiction | neutral | 0.90 | 海辺を男女が歩いている。 ⇒ 海辺の砂浜を一羽の鳥が歩いています。 |
| j1600 | contradiction | neutral | 0.90 | 草原の木立の中にキリンが一頭います。 ⇒ 草原の木立の中にキリンが二頭います。 |

**clef-flash** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1600 | contradiction | neutral | 0.93 | 草原の木立の中にキリンが一頭います。 ⇒ 草原の木立の中にキリンが二頭います。 |
| j263 | contradiction | neutral | 0.93 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j994 | contradiction | neutral | 0.90 | 男性がサーフボードを持って立っている。 ⇒ 男性がサーフボードとパドルを使って波に乗っている。 |

**d1@vercel** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j2242 | contradiction | neutral | 0.98 | 海で水上スキーを履いてロープに掴まっている船があります。 ⇒ 海で水上スキーを履いてロープに掴まっている男性がいます。 |
| j1942 | entailment | neutral | 0.95 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j2088 | neutral | contradiction | 0.95 | 黒いソファーベッドの上に猫が寝ています。 ⇒ ソファの上に二匹の猫が丸まっています。 |
| j90 | neutral | contradiction | 0.92 | 部屋に置いてあるトランクの中に猫がいます。 ⇒ 蓋の開いたアタッシュケースの中から猫が顔を出しています。 |

**flash-lite@vercel** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j151 | neutral | entailment | 1.00 | グリルの上のプレートに二枚のピザがあります。 ⇒ コンロでピザを2枚焼いています。 |
| j385 | contradiction | neutral | 1.00 | 海辺を男女が歩いている。 ⇒ 海辺の砂浜を一羽の鳥が歩いています。 |
| j2230 | contradiction | neutral | 1.00 | ヘルメットをかぶった子供が野球のバットを持っています。 ⇒ 帽子をかぶった子供がバットを持っている。 |
| j1146 | neutral | entailment | 1.00 | 水の入ったガラス容器に、植物が活けられています。 ⇒ 水の入ったコップに植物が入っています。 |
| j2088 | neutral | contradiction | 1.00 | 黒いソファーベッドの上に猫が寝ています。 ⇒ ソファの上に二匹の猫が丸まっています。 |
| j728 | contradiction | neutral | 1.00 | 椅子の背もたれに太陽電池のパネルが取り付けられています。 ⇒ 机に太陽電池のパネルが取り付けられています。 |
| j1664 | neutral | entailment | 1.00 | 二匹の犬がベッドの上で寝ています。 ⇒ ベッドに敷かれた布団の上に二匹の動物が寝転がっています。 |
| j1451 | contradiction | neutral | 1.00 | シャッターのまえにひとがすわっています。 ⇒ シャッターのまえに猫がすわっています。 |

**haiku@vercel** (32)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1 | entailment | neutral | 1.00 | キリンが、木の中から首を出しています。 ⇒ キリンが木々のあいだから顔を出しています。 |
| j385 | contradiction | neutral | 1.00 | 海辺を男女が歩いている。 ⇒ 海辺の砂浜を一羽の鳥が歩いています。 |
| j2230 | contradiction | entailment | 1.00 | ヘルメットをかぶった子供が野球のバットを持っています。 ⇒ 帽子をかぶった子供がバットを持っている。 |
| j1942 | entailment | neutral | 1.00 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j1146 | neutral | entailment | 1.00 | 水の入ったガラス容器に、植物が活けられています。 ⇒ 水の入ったコップに植物が入っています。 |
| j772 | entailment | neutral | 1.00 | 海の上でサーフィンをしている人がいます。 ⇒ 海の上で、サーファーが波に乗っています。 |
| j1163 | contradiction | neutral | 1.00 | 帽子 が木の枝の上でぶら下がっています。 ⇒ 動物が木の枝の上でぶら下がっています。 |
| j1452 | contradiction | neutral | 1.00 | シャッターのまえにひとが立っています。 ⇒ シャッターのまえにひとがすわっています。 |

**jev** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j605 | contradiction | neutral | 0.98 | 歩道で、野菜を販売してる人達がいます。 ⇒ 歩道で、フルーツを販売してる人達がいます。 |
| j1516 | entailment | neutral | 0.98 | 山の前に蒸気機関の貨物列車がいます。 ⇒ 貨物列車が山の前の線路の上にいます。 |
| j2232 | contradiction | neutral | 0.98 | 帽子をかぶった子供がバットを持っている。 ⇒ ヘルメットをかぶった子供が野球のバットを持っています。 |
| j1942 | entailment | neutral | 0.97 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j1594 | contradiction | neutral | 0.96 | 草原の木立の中にキリンが二頭います。 ⇒ 草原の木立の中にシマウマが二頭います。 |
| j735 | entailment | neutral | 0.93 | 帽子を被った男児が芝生の上で凧を揚げている。 ⇒ 広場で凧を揚げている子どもがいます。 |
| j2242 | contradiction | neutral | 0.92 | 海で水上スキーを履いてロープに掴まっている船があります。 ⇒ 海で水上スキーを履いてロープに掴まっている男性がいます。 |
| j263 | contradiction | neutral | 0.91 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |

**jev@vercel** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j605 | contradiction | neutral | 0.99 | 歩道で、野菜を販売してる人達がいます。 ⇒ 歩道で、フルーツを販売してる人達がいます。 |
| j735 | entailment | neutral | 0.95 | 帽子を被った男児が芝生の上で凧を揚げている。 ⇒ 広場で凧を揚げている子どもがいます。 |
| j1942 | entailment | neutral | 0.95 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j2232 | contradiction | neutral | 0.93 | 帽子をかぶった子供がバットを持っている。 ⇒ ヘルメットをかぶった子供が野球のバットを持っています。 |
| j1516 | entailment | neutral | 0.93 | 山の前に蒸気機関の貨物列車がいます。 ⇒ 貨物列車が山の前の線路の上にいます。 |
| j263 | contradiction | neutral | 0.91 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j1735 | entailment | contradiction | 0.90 | 曇り空の上を一機の戦闘機が飛んでいる。 ⇒ 曇り空の中を戦闘機が飛んでいます。 |
| j728 | contradiction | neutral | 0.90 | 椅子の背もたれに太陽電池のパネルが取り付けられています。 ⇒ 机に太陽電池のパネルが取り付けられています。 |

**kev@openrouter** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1451 | contradiction | neutral | 1.00 | シャッターのまえにひとがすわっています。 ⇒ シャッターのまえに猫がすわっています。 |
| j994 | contradiction | neutral | 1.00 | 男性がサーフボードを持って立っている。 ⇒ 男性がサーフボードとパドルを使って波に乗っている。 |
| j1762 | contradiction | neutral | 1.00 | 屋内でフライングディスクを咥えた犬が走っています。 ⇒ 雪の上をフライングディスクを咥えた犬が走っています。 |
| j1136 | contradiction | neutral | 1.00 | 寝室にソファーがあります。 ⇒ とても広いリビングの真ん中にソファーがあります。 |
| j263 | contradiction | neutral | 1.00 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j1391 | contradiction | neutral | 1.00 | 駅のプラットホームに電車が停車しています。 ⇒ 駅のプラットホームから電車が発車しています。 |
| j2242 | contradiction | neutral | 1.00 | 海で水上スキーを履いてロープに掴まっている船があります。 ⇒ 海で水上スキーを履いてロープに掴まっている男性がいます。 |
| j1942 | entailment | neutral | 0.99 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |

**laya@vercel** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j2258 | neutral | contradiction | 1.00 | 二人の人がフライパンの中を見ています。 ⇒ 老婆と若い娘がキッチンに並んで立っています。 |
| j768 | neutral | contradiction | 1.00 | 港の広場に軍用機が展示されています。 ⇒ 青空の下、広場を背景に、丸いチーズショップの看板があります。 |
| j1307 | neutral | contradiction | 1.00 | 帽子をかぶった男性がウマに股がっています。 ⇒ 人を乗せた馬が１頭歩いています。 |
| j2235 | neutral | contradiction | 1.00 | 大きな袋で荷台がいっぱいのピックアップが、家の前に止まっています。 ⇒ 黒い自動車が野外に駐車されています。 |
| j376 | neutral | contradiction | 1.00 | 草原で2人の人が気球のようなものを持って立っています。 ⇒ パラシュートを広げている男性二人がいます。。 |
| j1652 | neutral | contradiction | 1.00 | 個室のトイレには赤い花が活けてあります。 ⇒ ベージュを基調としたトイレットルームです。 |
| j839 | entailment | neutral | 1.00 | 完熟前ののバナナがたくさん実っています。 ⇒ 緑色のバナナがたくさん実っています。 |
| j955 | neutral | contradiction | 0.99 | 男性が携帯電話で話をしています。 ⇒ 回りに建物がある車が止まっているスペースに複数の人物がいます。 |

**luna@decisions** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j263 | contradiction | neutral | 0.99 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j728 | contradiction | neutral | 0.98 | 椅子の背もたれに太陽電池のパネルが取り付けられています。 ⇒ 机に太陽電池のパネルが取り付けられています。 |
| j605 | contradiction | neutral | 0.98 | 歩道で、野菜を販売してる人達がいます。 ⇒ 歩道で、フルーツを販売してる人達がいます。 |
| j604 | contradiction | neutral | 0.96 | 畑で果物を収穫している人たちがいます。 ⇒ ごみの散乱した路上で、果物を売っている人たちがいます。 |
| j1671 | contradiction | neutral | 0.95 | オリーブなどを乗せた焼かれたピザがあります。 ⇒ オリーブなどを乗せた焼かれたたこ焼きがあります。 |
| j523 | entailment | neutral | 0.94 | 路上に止まるバイクの右側に人が立ち、奥には赤い車があります。 ⇒ 赤い車の前にバイクが停まっています。 |
| j1236 | neutral | entailment | 0.93 | 道路に二階建てバスが通行しています。 ⇒ 街中をダブルデッカーバスが走っています。 |
| j1884 | contradiction | neutral | 0.93 | 針葉樹の枝の上で小さい鳥が鳴いています。 ⇒ 針葉樹の枝の上で小さい鳥が目をつむって寝ています。 |

**mercury@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1942 | entailment | neutral | 0.97 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j1225 | neutral | contradiction | 0.97 | トラックの荷台に車が積まれています。 ⇒ 道を走るトラックにはトラクターが積んであります。 |
| j1111 | entailment | neutral | 0.96 | 料理を前にして、女性が胸の下で両手を握っています。 ⇒ 女性の目の前のテーブルに、料理が置かれています。 |
| j2232 | contradiction | neutral | 0.95 | 帽子をかぶった子供がバットを持っている。 ⇒ ヘルメットをかぶった子供が野球のバットを持っています。 |
| j263 | contradiction | neutral | 0.95 | 象が一頭、草原をゆったりと歩いています。 ⇒ アフリカゾウが食事をしています。 |
| j1933 | entailment | neutral | 0.91 | 木々の生える草原を歩く小さい小象と大きい象がいます。 ⇒ 広い草原の中に２頭の象が歩いている。 |
| j1403 | entailment | neutral | 0.90 | 海の砂浜の柵で区切られた場所で、立体的な凧の様なものを揚げている人々がいます。 ⇒ 浜辺で色々な立体的な凧の様なものを揚げています。 |

**solar@openrouter** (45)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j1528 | contradiction | neutral | 1.00 | スケートボードをしている人がジャンプしています。 ⇒ スキーをしている人がいます。 |
| j1163 | contradiction | neutral | 1.00 | 帽子 が木の枝の上でぶら下がっています。 ⇒ 動物が木の枝の上でぶら下がっています。 |
| j990 | contradiction | neutral | 1.00 | 男性がサーフボードとパドルを使って波に乗っている。 ⇒ 男性がサーフボードを持って立っている。 |
| j16 | entailment | neutral | 1.00 | 窓越しに壁にかけられた時計が見えます。 ⇒ 窓の向こうの部屋に時計が架かっています。 |
| j221 | entailment | neutral | 1.00 | 湖の岸に木のボートが止まっています。 ⇒ 水面に一槽のボートが停止しています。 |
| j1455 | contradiction | neutral | 1.00 | シャッターのまえに猫がすわっています。 ⇒ シャッターのまえにひとがすわっています。 |
| j1451 | contradiction | neutral | 1.00 | シャッターのまえにひとがすわっています。 ⇒ シャッターのまえに猫がすわっています。 |
| j1671 | contradiction | neutral | 1.00 | オリーブなどを乗せた焼かれたピザがあります。 ⇒ オリーブなどを乗せた焼かれたたこ焼きがあります。 |

**tev1@openrouter** (11)

| id | label | answer | probability | case |
|---|---|---|---|---|
| j2242 | contradiction | neutral | 1.00 | 海で水上スキーを履いてロープに掴まっている船があります。 ⇒ 海で水上スキーを履いてロープに掴まっている男性がいます。 |
| j1225 | neutral | contradiction | 1.00 | トラックの荷台に車が積まれています。 ⇒ 道を走るトラックにはトラクターが積んであります。 |
| j1942 | entailment | neutral | 0.99 | 二人の野球選手がハイタッチをしています。 ⇒ 野球の試合で、選手と選手がハイタッチをしています。 |
| j426 | neutral | contradiction | 0.99 | 椅子に座っている女性と子供がいます。 ⇒ ソファーで女性と子供がくつろいでいます。 |
| j1652 | neutral | contradiction | 0.98 | 個室のトイレには赤い花が活けてあります。 ⇒ ベージュを基調としたトイレットルームです。 |
| j768 | neutral | contradiction | 0.98 | 港の広場に軍用機が展示されています。 ⇒ 青空の下、広場を背景に、丸いチーズショップの看板があります。 |
| j2232 | contradiction | neutral | 0.98 | 帽子をかぶった子供がバットを持っている。 ⇒ ヘルメットをかぶった子供が野球のバットを持っています。 |
| j2230 | contradiction | entailment | 0.97 | ヘルメットをかぶった子供が野球のバットを持っています。 ⇒ 帽子をかぶった子供がバットを持っている。 |


## Cases the models disagree on (12 of 150)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | laya@vercel | luna@decisions | mercury@openrouter | solar@openrouter | tev1@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| j977 | neutral | neutral (0.90) | neutral (0.63) | neutral (0.96) | neutral (1.00) | neutral (1.00) | neutral (0.95) | neutral (0.97) | neutral (1.00) | neutral (0.91) | entailment (0.55) | neutral (0.87) | entailment (0.89) | neutral (0.87) | 白いTシャツの女性が赤いハサミを手に持っています。 ⇒ 女性が赤いハサミを持って、見ています。 |
| j79 | entailment | entailment (0.73) | neutral (0.77) | entailment (0.65) | entailment (1.00) | entailment (1.00) | neutral (0.71) | neutral (0.74) | entailment (0.85) | entailment (0.97) | neutral (0.69) | entailment (0.80) | neutral (1.00) | entailment (0.92) | スキー場の斜面に３人のスキーヤーがいます。 ⇒ 雪山に三人の人がスキー姿で立っています。 |
| j1652 | neutral | neutral (0.96) | contradiction (0.50) | neutral (0.98) | neutral (1.00) | neutral (1.00) | neutral (1.00) | neutral (1.00) | contradiction (0.89) | contradiction (1.00) | neutral (1.00) | neutral (0.98) | neutral (0.99) | contradiction (0.98) | 個室のトイレには赤い花が活けてあります。 ⇒ ベージュを基調としたトイレットルームです。 |
| j132 | entailment | entailment (0.85) | entailment (0.80) | entailment (0.93) | entailment (1.00) | entailment (1.00) | entailment (0.52) | neutral (0.57) | entailment (0.97) | entailment (0.99) | entailment (0.97) | entailment (0.91) | entailment (0.94) | entailment (0.98) | 男の子が砂浜で凧あげをしています。 ⇒ 海辺で、男の子が凧をあげています。 |
| j1404 | neutral | neutral (0.94) | neutral (0.88) | neutral (0.98) | neutral (1.00) | neutral (1.00) | neutral (1.00) | neutral (1.00) | neutral (1.00) | contradiction (0.75) | neutral (0.96) | neutral (0.99) | neutral (1.00) | neutral (0.99) | 浜辺で色々な立体的な凧の様なものを揚げています。 ⇒ 海の砂浜の柵で区切られた場所で、立体的な凧の様なものを揚げている人々がいます。 |
| j1532 | entailment | entailment (0.97) | contradiction (0.54) | entailment (0.99) | entailment (1.00) | entailment (1.00) | entailment (0.99) | entailment (0.99) | entailment (1.00) | entailment (1.00) | entailment (0.87) | entailment (1.00) | entailment (0.97) | entailment (1.00) | 白い大型トラックが赤信号で停まっている。 ⇒ 赤信号で大型トラックが停まっています。 |
| j2302 | neutral | neutral (0.90) | neutral (0.90) | neutral (0.84) | neutral (1.00) | neutral (1.00) | neutral (0.98) | neutral (0.98) | neutral (1.00) | contradiction (0.99) | neutral (0.78) | neutral (0.98) | neutral (1.00) | neutral (0.95) | 夜にパラソルを広げて人々が集まっています。 ⇒ 電飾された敷地で傘のしたに人々がいます。 |
| j1735 | entailment | entailment (0.89) | entailment (0.82) | entailment (0.57) | contradiction (1.00) | neutral (1.00) | contradiction (0.73) | contradiction (0.90) | entailment (0.98) | entailment (0.99) | neutral (0.48) | entailment (0.98) | entailment (0.95) | entailment (0.96) | 曇り空の上を一機の戦闘機が飛んでいる。 ⇒ 曇り空の中を戦闘機が飛んでいます。 |
| j1824 | contradiction | contradiction (0.88) | neutral (0.83) | contradiction (0.99) | contradiction (1.00) | contradiction (1.00) | contradiction (0.86) | contradiction (0.94) | contradiction (0.96) | contradiction (0.94) | neutral (0.87) | contradiction (1.00) | contradiction (0.97) | contradiction (1.00) | トイレの窓にブラインドが設置されています。 ⇒ トイレの窓には通気口があるだけである。 |
| j1762 | contradiction | contradiction (0.87) | contradiction (0.73) | contradiction (0.98) | contradiction (1.00) | contradiction (1.00) | contradiction (0.76) | contradiction (0.90) | neutral (1.00) | contradiction (0.93) | contradiction (0.84) | contradiction (1.00) | contradiction (0.94) | contradiction (0.87) | 屋内でフライングディスクを咥えた犬が走っています。 ⇒ 雪の上をフライングディスクを咥えた犬が走っています。 |
| j16 | entailment | entailment (0.54) | entailment (0.75) | entailment (0.68) | entailment (1.00) | neutral (1.00) | neutral (0.58) | neutral (0.54) | neutral (0.49) | entailment (0.74) | entailment (0.51) | entailment (0.88) | neutral (1.00) | entailment (0.73) | 窓越しに壁にかけられた時計が見えます。 ⇒ 窓の向こうの部屋に時計が架かっています。 |
| j1591 | entailment | entailment (0.94) | entailment (0.81) | entailment (0.99) | entailment (1.00) | entailment (1.00) | entailment (0.98) | entailment (0.99) | neutral (0.64) | entailment (1.00) | entailment (0.96) | entailment (0.94) | entailment (0.93) | entailment (0.98) | スキー板を履いた人が、ジャンプしています。 ⇒ スキーを履いてジャンプしている人がいます。 |
