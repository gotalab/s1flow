# massive-ja-intent · with_none

2026-10-22 · 288 labelled (datetime_convert 5, email_addcontact 5, play_podcasts 5, qa_definition 5, transport_ticket 5, takeaway_order 5, social_post 5, play_audiobook 5, more) · split: stratified k-fold (87 test cases of the fixed evaluation set held out) · source: MASSIVE 1.1 ja-JP test（Amazon, CC BY 4.0）から各意図 5 件まで

**flash-lite@vercel/with_none** has the highest accuracy (all), 87% [83, 92] (API cost $3.15 per 10k, p99 2081ms). Its interval overlaps with d1@vercel/with_none, jev@vercel/with_none, haiku@vercel/with_none: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **d1@vercel/with_none** (API cost $0.17 per 10k, p99 1728ms). Latency not compared (4 with no concurrency recorded; 4 with no retries recorded): measure every candidate again at one concurrency, s1flow run massive-ja-intent --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is flash-lite@vercel/with_none's, 86% [83, 91].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| d1@vercel/with_none | 288 | 84.0% [80, 89] | 0.81 | 0.99 | 0.06 | 59% [52, 67] | 92.4% (87.2%) | 0/288 | 0/288 |
| flash-lite@vercel/with_none ※ | 288 | 86.5% [83, 91] | 0.84 | 0.93 | 0.11 | 0% [0, 0] | — (0.0%) | 0/288 | 0/288 |
| haiku@vercel/with_none ※ | 288 | 85.4% [81, 90] | 0.84 | 0.93 | 0.13 | 0% [0, 0] | — (0.0%) | 0/288 | 0/288 |
| jev@vercel/with_none | 288 | 85.4% [81, 90] | 0.84 | 0.97 | 0.05 | 75% [69, 81] | 93.4% (89.0%) | 0/288 | 0/288 |
| laya@vercel/with_none | 288 | 40.6% [35, 46] | 0.36 | 0.84 | 0.38 | 0% [0, 0] | — (0.0%) | 0/288 | 0/288 |

Answered by: d1@vercel/with_none = liquid/d1; flash-lite@vercel/with_none = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel/with_none = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev@vercel/with_none = typesafe-ai/jev; laya@vercel/with_none = convaiinnovations/laya. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| d1@vercel/with_none ◎ | 85% [80, 90] | — | met |
| jev@vercel/with_none | 86% [81, 90] | — | met |
| flash-lite@vercel/with_none | 87% [83, 92] | — | met |
| haiku@vercel/with_none | 87% [82, 91] | — | met |
| laya@vercel/with_none | 40% [33, 47] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d1@vercel/with_none | 288 | 518 ms | 736 ms | 1728 ms | 2182 ms | 3.3 | not recorded | unknown | $0.17 | billed | ○ |
| flash-lite@vercel/with_none | 288 | 1132 ms | 1542 ms | 2081 ms | 2483 ms | 1.8 | not recorded | unknown | $3.15 | estimated | ○ |
| haiku@vercel/with_none | 288 | 1062 ms | 1401 ms | 2564 ms | 3100 ms | 2.4 | not recorded | unknown | $15.70 | estimated |  |
| jev@vercel/with_none | 288 | 411 ms | 583 ms | 1086 ms | 2086 ms | 2.6 | not recorded | unknown | $0.59 | billed | ○ |
| laya@vercel/with_none | 288 | 456 ms | 696 ms | 1441 ms | 1962 ms | 3.2 | not recorded | unknown | $0.0000 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel/with_none, jev@vercel/with_none, laya@vercel/with_none; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): flash-lite@vercel/with_none, haiku@vercel/with_none. Billed and estimated API costs sit side by side, so their differences do not compare as they are.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| d1@vercel/with_none | 87 | 81.6% | 49% | 100.0% | 0.816 |
| flash-lite@vercel/with_none | 87 | 85.1% | 0% | — | 0.851 |
| haiku@vercel/with_none | 87 | 82.8% | 0% | — | 0.828 |
| jev@vercel/with_none | 87 | 85.1% | 72% | 95.2% | 0.851 |
| laya@vercel/with_none | 87 | 42.5% | 0% | — | 0.425 |

## Wrong at a high probability (0.9 or more)

**d1@vercel/with_none** (13)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 0.99 | 最新情報 |
| m8322 | general_quirky | recommendation_events | 0.99 | 今週末のフェアについてもっと知りたい |
| m4130 | alarm_query | alarm_set | 0.98 | ダンス教室のためにアラームは設定されている |
| m4166 | audio_volume_other | audio_volume_up | 0.97 | 音量を最大にする |
| m5911 | music_settings | play_music | 0.96 | 音楽をリプレイ |
| m13242 | general_quirky | cooking_recipe | 0.96 | 一番美味しい抹茶ケーキのレシピは何 |
| m5812 | audio_volume_other | music_settings | 0.96 | 既定のオーディオ設定にする |
| m2165 | takeaway_query | cooking_query | 0.96 | ディナーはできましたか |

**flash-lite@vercel/with_none** (33)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m944 | datetime_convert | datetime_query | 1.00 | ここと日本の時差はどれくらい |
| m2480 | takeaway_order | takeaway_query | 1.00 | テイクアウトの電話 |
| m10931 | lists_query | music_query | 1.00 | 私のプレイリストにある曲は何ですか |
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 1.00 | 音量を最大にする |
| m2165 | takeaway_query | cooking_query | 1.00 | ディナーはできましたか |
| m8795 | calendar_query | lists_query | 1.00 | 保留中のリマインダーを表示する |
| m9562 | play_radio | play_podcasts | 1.00 | この番組を再生してください |

**haiku@vercel/with_none** (38)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m10931 | lists_query | music_query | 1.00 | 私のプレイリストにある曲は何ですか |
| m2480 | takeaway_order | takeaway_query | 1.00 | テイクアウトの電話 |
| m5152 | music_settings | music_query | 1.00 | 二曲スキップして |
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 1.00 | 音量を最大にする |
| m2165 | takeaway_query | cooking_query | 1.00 | ディナーはできましたか |
| m5919 | news_query | qa_factoid | 1.00 | 江戸川に関わる事業案について最新情報を教えて |
| m8795 | calendar_query | alarm_query | 1.00 | 保留中のリマインダーを表示する |

**jev@vercel/with_none** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 1.00 | 最新情報 |
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m5911 | music_settings | play_music | 1.00 | 音楽をリプレイ |
| m4268 | music_settings | play_music | 0.97 | リストの次の曲に移動 |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.96 | 明かりを消して |
| m10931 | lists_query | music_query | 0.95 | 私のプレイリストにある曲は何ですか |
| m5152 | music_settings | play_music | 0.92 | 二曲スキップして |
| m4130 | alarm_query | alarm_set | 0.92 | ダンス教室のためにアラームは設定されている |

**laya@vercel/with_none** (60)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m16470 | email_addcontact | email_sendemail | 1.00 | このメールを私の連絡先に追加してください |
| m15987 | email_addcontact | email_sendemail | 1.00 | この新着メールを連絡先に追加する |
| m17111 | email_querycontact | email_sendemail | 1.00 | 正人の連絡先の詳細 |
| m3486 | audio_volume_down | iot_hue_lightchange | 1.00 | ちょっと音を下げて下さい |
| m16002 | email_query | email_sendemail | 1.00 | 新しいメールを確認する |
| m16353 | email_query | email_sendemail | 1.00 | 隆雄からのメールを確認 |
| m5611 | audio_volume_down | iot_hue_lightchange | 1.00 | 音量を下げる |
| m16627 | email_query | email_sendemail | 1.00 | 最新のメールを確認する |


## Cases the models disagree on (12 of 173)

| id | label | d1@vercel | flash-lite@vercel | haiku@vercel | jev@vercel | laya@vercel | case |
|---|---|---|---|---|---|---|---|
| m944 | datetime_convert | datetime_query (0.48) | datetime_query (1.00) | datetime_convert (1.00) | datetime_query (0.64) | weather_query (0.54) | ここと日本の時差はどれくらい |
| m16781 | email_addcontact | email_addcontact (0.73) | email_addcontact (1.00) | email_addcontact (1.00) | email_addcontact (0.74) | email_sendemail (1.00) | このメールアドレスを連絡先に追加してメールを送る |
| m46 | general_greet | general_quirky (0.20) | alarm_query (0.00) | general_greet (1.00) | general_greet (0.74) | qa_factoid (0.98) | 何ですか、オリ―さん |
| m16693 | email_addcontact | email_addcontact (0.98) | email_addcontact (1.00) | email_addcontact (1.00) | email_addcontact (1.00) | email_sendemail (1.00) | 愛知県名古屋市にある lowes ホームセンターを連絡先メールに追加する |
| m2255 | takeaway_order | takeaway_query (0.86) | takeaway_query (1.00) | takeaway_query (1.00) | takeaway_query (0.84) | takeaway_order (0.66) | 星野珈琲でテイクアウトを注文できますか |
| m6959 | calendar_set | calendar_set (0.96) | calendar_set (1.00) | alarm_set (1.00) | calendar_set (0.79) | iot_hue_lightdim (0.18) | 一時間前に会議についてリマインドしてください |
| m17123 | email_sendemail | email_sendemail (0.72) | email_sendemail (1.00) | alarm_query (0.00) | email_sendemail (0.84) | email_sendemail (1.00) | 現地の副社長用のメールフォーム |
| m16353 | email_query | email_query (1.00) | email_query (1.00) | email_query (1.00) | email_query (0.70) | email_sendemail (1.00) | 隆雄からのメールを確認 |
| m4887 | music_likeness | music_likeness (0.80) | music_likeness (1.00) | music_likeness (1.00) | lists_createoradd (0.39) | iot_wemo_off (0.99) | アデルの曲に私の意見をセーブして |
| m6014 | music_query | music_query (0.98) | music_query (1.00) | music_query (1.00) | music_query (0.72) | qa_factoid (0.34) | このアーティストは誰 |
| m13372 | general_quirky | recommendation_events (0.55) | recommendation_events (1.00) | datetime_query (1.00) | datetime_query (0.53) | play_game (0.58) | 今夜のホッケーゲームは何時ですか |
| m1076 | music_dislikeness | music_dislikeness (0.87) | music_dislikeness (1.00) | music_dislikeness (1.00) | music_dislikeness (0.79) | audio_volume_down (0.72) | ロックメタルを再生しない |
