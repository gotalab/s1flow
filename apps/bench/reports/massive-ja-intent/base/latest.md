# massive-ja-intent

2026-10-22 · 288 labelled (datetime_convert 5, email_addcontact 5, play_podcasts 5, qa_definition 5, transport_ticket 5, takeaway_order 5, social_post 5, play_audiobook 5, more) · split: stratified k-fold (87 test cases of the fixed evaluation set held out) · source: MASSIVE 1.1 ja-JP test（Amazon, CC BY 4.0）から各意図 5 件まで

**decider@openrouter** has the highest accuracy (all), 91% [87, 95] (API cost $0.15 per 10k, p99 816ms). Its interval overlaps with span@openrouter, decider-flash@openrouter, d1@vercel, d1-ultra@openrouter, decision-1@openrouter, drex@openrouter, jev@vercel, jev, luna@decisions, clef-flash, clef-omni@openrouter, flash-lite@vercel, clef, haiku@vercel: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **span@openrouter** (API cost $0.05 per 10k, p99 2365ms). Latency not compared (8 with no concurrency recorded; 8 with no retries recorded): measure every candidate again at one concurrency, s1flow run massive-ja-intent --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is clef's, 89% [85, 93].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 288 | 89.2% [85, 93] | 0.86 | 1.00 | 0.04 | 90% [86, 94] | 95.0% (91.5%) | 0/288 | 0/288 |
| clef-flash | 288 | 88.9% [85, 92] | 0.87 | 1.00 | 0.06 | 90% [86, 94] | 94.4% (90.8%) | 0/288 | 0/288 |
| clef-omni@openrouter | 288 | 88.9% [85, 92] | 0.86 | 0.99 | 0.15 | 65% [59, 72] | 93.1% (88.3%) | 0/288 | 0/288 |
| d1-ultra@openrouter | 288 | 86.1% [82, 90] | 0.84 | 0.99 | 0.04 | 75% [69, 81] | 94.7% (90.6%) | 0/288 | 0/288 |
| d1@vercel | 288 | 83.7% [80, 88] | 0.81 | 0.99 | 0.05 | 61% [54, 68] | 94.3% (89.5%) | 0/288 | 0/288 |
| decider-flash@openrouter | 288 | 85.8% [82, 90] | 0.82 | 1.00 | 0.04 | 76% [70, 82] | 95.4% (91.6%) | 0/288 | 0/288 |
| decider@openrouter | 288 | 88.9% [85, 93] | 0.86 | 1.00 | 0.03 | 94% [91, 97] | 94.7% (91.1%) | 0/288 | 0/288 |
| decision-1@openrouter | 288 | 88.2% [84, 92] | 0.87 | 1.00 | 0.02 | 86% [81, 90] | 94.8% (91.0%) | 0/288 | 0/288 |
| drex@openrouter | 288 | 82.3% [77, 87] | 0.80 | 0.99 | 0.06 | 76% [71, 82] | 94.1% (90.0%) | 0/288 | 0/288 |
| flash-lite@vercel ※ | 288 | 86.8% [83, 91] | 0.85 | 0.93 | 0.13 | 0% [0, 0] | — (0.0%) | 0/288 | 0/288 |
| haiku@vercel ※ | 288 | 85.1% [81, 89] | 0.82 | 0.92 | 0.15 | 0% [0, 0] | — (0.0%) | 0/288 | 0/288 |
| jev | 288 | 85.1% [81, 89] | 0.84 | 0.98 | 0.05 | 78% [72, 83] | 92.9% (88.6%) | 0/288 | 0/288 |
| jev@vercel | 288 | 85.8% [82, 90] | 0.85 | 0.97 | 0.05 | 70% [64, 76] | 93.6% (89.1%) | 0/288 | 0/288 |
| kev@openrouter | 288 | 75.7% [71, 81] | 0.73 | 0.99 | 0.23 | 48% [41, 54] | 93.8% (88.0%) | 0/288 | 0/288 |
| laya@vercel | 288 | 39.9% [34, 46] | 0.34 | 0.85 | 0.39 | 0% [0, 0] | — (0.0%) | 0/288 | 0/288 |
| luna@decisions | 288 | 81.9% [77, 86] | 0.80 | 0.98 | 0.05 | 69% [63, 76] | 95.0% (90.7%) | 0/288 | 0/288 |
| mercury@openrouter ✕ | 145 | 91.0% [86, 95] | 0.83 | 1.00 | 0.07 | 88% [81, 94] | 95.5% (89.9%) | 0/288 | 143/288 |
| solar-flash@openrouter | 0 | — | | | | | | 288/288 | 0/288 |
| solar@openrouter | 0 | — | | | | | | 288/288 | 0/288 |
| span@openrouter | 288 | 86.5% [82, 90] | 0.85 | 0.99 | 0.05 | 77% [71, 83] | 95.5% (91.6%) | 0/288 | 0/288 |
| tev1@openrouter | 0 | — | | | | | | 288/288 | 0/288 |

Not compared: mercury@openrouter (143 cases whose every call failed). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is neither ranked nor chosen. Ask them again: `s1flow run massive-ja-intent --models mercury@openrouter`

Answered by: clef = clef; clef-flash = clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex@openrouter = nace-ai/drex-v2.0-20261009; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; laya@vercel = convaiinnovations/laya; luna@decisions = gpt-6-luna; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| span@openrouter ◎ | 87% [83, 92] | — | met |
| decider-flash@openrouter | 86% [81, 90] | — | met |
| decider@openrouter | 91% [87, 95] | — | met |
| d1@vercel | 85% [80, 90] | — | met |
| d1-ultra@openrouter | 87% [82, 92] | — | met |
| decision-1@openrouter | 89% [85, 93] | — | met |
| drex@openrouter | 85% [80, 89] | — | met |
| jev@vercel | 86% [81, 91] | — | met |
| jev | 85% [80, 89] | — | met |
| luna@decisions | 85% [80, 90] | — | met |
| clef-flash | 89% [85, 93] | — | met |
| clef-omni@openrouter | 90% [86, 95] | — | met |
| flash-lite@vercel | 87% [83, 92] | — | met |
| clef | 89% [85, 93] | — | met |
| haiku@vercel | 87% [83, 92] | — | met |
| kev@openrouter | 75% [69, 81] | — | met |
| laya@vercel | 39% [32, 46] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 288 | 539 ms | 906 ms | 1385 ms | 1646 ms | 2.6 | not recorded | unknown | $3.39 | estimated |  |
| clef-flash | 288 | 242 ms | 456 ms | 690 ms | 1020 ms | 2.8 | not recorded | unknown | $1.27 | estimated | ○ |
| clef-omni@openrouter | 288 | 388 ms | 576 ms | 1536 ms | 2219 ms | 4.0 | 0 | 8 | $2.14 | billed |  |
| d1-ultra@openrouter | 288 | 540 ms | 703 ms | 1637 ms | 1742 ms | 3.0 | 0 | 8 | $0.18 | billed |  |
| d1@vercel | 288 | 501 ms | 1138 ms | 2802 ms | 6063 ms | 5.6 | not recorded | unknown | $0.17 | billed |  |
| decider-flash@openrouter | 288 | 522 ms | 585 ms | 1217 ms | 2178 ms | 2.3 | 0 | 8 | $0.07 | billed | ○ |
| decider@openrouter | 288 | 555 ms | 671 ms | 816 ms | 1811 ms | 1.5 | 0 | 8 | $0.15 | billed | ○ |
| decision-1@openrouter | 288 | 522 ms | 625 ms | 1627 ms | 1828 ms | 3.1 | 0 | 8 | $0.24 | billed |  |
| drex@openrouter | 288 | 529 ms | 821 ms | 1432 ms | 2721 ms | 2.7 | 16 | 8 | $0.37 | billed |  |
| flash-lite@vercel | 288 | 1176 ms | 1568 ms | 10749 ms | 11077 ms | 9.1 | not recorded | unknown | $3.11 | estimated |  |
| haiku@vercel | 288 | 1097 ms | 1665 ms | 9272 ms | 10945 ms | 8.5 | not recorded | unknown | $15.50 | estimated |  |
| jev | 288 | 163 ms | 214 ms | 229 ms | 310 ms | 1.4 | not recorded | unknown | $0.58 | estimated | ○ |
| jev@vercel | 288 | 357 ms | 536 ms | 821 ms | 1431 ms | 2.3 | not recorded | unknown | $0.58 | billed |  |
| kev@openrouter | 288 | 731 ms | 903 ms | 1332 ms | 1965 ms | 1.8 | not recorded | unknown | $0.26 | billed |  |
| laya@vercel | 288 | 519 ms | 860 ms | 7954 ms | 8204 ms | 15.3 | not recorded | unknown | $0.0000 | billed | ○ |
| luna@decisions | 288 | 258 ms | 293 ms | 412 ms | 937 ms | 1.6 | not recorded | unknown | $0.79 | estimated |  |
| mercury@openrouter | 145 | 821 ms | 3868 ms | 4065 ms | 4556 ms | 5.0 | not recorded | unknown | $0.0000 | billed |  |
| span@openrouter | 288 | 521 ms | 759 ms | 2365 ms | 2584 ms | 4.5 | 0 | 8 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: clef-omni@openrouter, d1-ultra@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex@openrouter, jev@vercel, kev@openrouter, laya@vercel, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.10 | 22 s (measured, 288 calls) | 13 min | 8 |
| clef-flash | $0.04 | 10 s (measured, 288 calls) | 6 min | 8 |
| clef-omni@openrouter | $0.06 | 16 s (estimated, 288 calls) | 9 min | 8 |
| d1-ultra@openrouter | $0.0051 | 21 s (estimated, 288 calls) | 12 min | 8 |
| d1@vercel | $0.0049 | 26 s (measured, 288 calls) | 15 min | 8 |
| decider-flash@openrouter | $0.0021 | 20 s (estimated, 288 calls) | 11 min | 8 |
| decider@openrouter | $0.0043 | 21 s (estimated, 288 calls) | 12 min | 8 |
| decision-1@openrouter | $0.0069 | 20 s (estimated, 288 calls) | 12 min | 8 |
| drex@openrouter | $0.01 | 22 s (estimated, 288 calls) | 13 min | 8 |
| jev@vercel | $0.02 | 15 s (measured, 288 calls) | 9 min | 8 |
| span@openrouter | $0.0015 | 1 s (measured, 1 calls) | 2.8 h | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 87 | 89.7% | 91% | 93.7% | 0.897 |
| clef-flash | 87 | 88.5% | 86% | 94.7% | 0.885 |
| clef-omni@openrouter | 87 | 86.2% | 78% | 92.6% | 0.862 |
| d1-ultra@openrouter | 87 | 83.9% | 71% | 95.2% | 0.839 |
| d1@vercel | 87 | 81.6% | 54% | 97.9% | 0.816 |
| decider-flash@openrouter | 87 | 86.2% | 68% | 98.3% | 0.862 |
| decider@openrouter | 87 | 85.1% | 87% | 93.4% | 0.851 |
| decision-1@openrouter | 87 | 87.4% | 85% | 94.6% | 0.874 |
| drex@openrouter | 87 | 77.0% | 71% | 91.9% | 0.770 |
| flash-lite@vercel | 87 | 86.2% | 0% | — | 0.862 |
| haiku@vercel | 87 | 80.5% | 0% | — | 0.805 |
| jev | 87 | 86.2% | 77% | 94.0% | 0.862 |
| jev@vercel | 87 | 85.1% | 71% | 95.2% | 0.851 |
| kev@openrouter | 87 | 77.0% | 45% | 100.0% | 0.770 |
| laya@vercel | 87 | 42.5% | 0% | — | 0.425 |
| luna@decisions | 87 | 75.9% | 61% | 100.0% | 0.759 |
| mercury@openrouter | 45 | 88.9% | 78% | 97.1% | 0.889 |
| span@openrouter | 87 | 85.1% | 67% | 98.3% | 0.851 |

## Wrong at a high probability (0.9 or more)

**clef** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.96 | 明かりを消して |
| m4166 | audio_volume_other | audio_volume_up | 0.95 | 音量を最大にする |
| m10931 | lists_query | music_query | 0.95 | 私のプレイリストにある曲は何ですか |
| m13242 | general_quirky | cooking_recipe | 0.94 | 一番美味しい抹茶ケーキのレシピは何 |
| m15203 | social_query | news_query | 0.94 | 最新情報 |
| m16225 | email_addcontact | email_querycontact | 0.91 | 連絡先リストを開く |

**clef-flash** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.97 | 明かりを消して |
| m4166 | audio_volume_other | audio_volume_up | 0.97 | 音量を最大にする |
| m13242 | general_quirky | cooking_recipe | 0.96 | 一番美味しい抹茶ケーキのレシピは何 |
| m16225 | email_addcontact | email_querycontact | 0.94 | 連絡先リストを開く |
| m15203 | social_query | news_query | 0.94 | 最新情報 |

**d1-ultra@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 0.97 | 最新情報 |
| m10349 | play_game | play_music | 0.92 | 透明な世界をかけて |

**d1@vercel** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m8322 | general_quirky | recommendation_events | 0.99 | 今週末のフェアについてもっと知りたい |
| m15203 | social_query | news_query | 0.98 | 最新情報 |
| m4130 | alarm_query | alarm_set | 0.98 | ダンス教室のためにアラームは設定されている |
| m13242 | general_quirky | cooking_recipe | 0.97 | 一番美味しい抹茶ケーキのレシピは何 |
| m2165 | takeaway_query | cooking_query | 0.96 | ディナーはできましたか |
| m4166 | audio_volume_other | audio_volume_up | 0.96 | 音量を最大にする |
| m5911 | music_settings | play_music | 0.95 | 音楽をリプレイ |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.93 | 明かりを消して |

**decider-flash@openrouter** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15333 | social_query | social_post | 0.97 | インスタグラムに何か新しいこと |
| m13242 | general_quirky | cooking_recipe | 0.96 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 0.96 | 音量を最大にする |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.96 | 明かりを消して |
| m16317 | email_query | email_sendemail | 0.94 | 沙羅から新しいメール |
| m15203 | social_query | news_query | 0.93 | 最新情報 |
| m50 | datetime_convert | datetime_query | 0.92 | g. m. t. プラス五の時間を教えて |
| m2165 | takeaway_query | cooking_query | 0.92 | ディナーはできましたか |

**decider@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.98 | 明かりを消して |
| m13372 | general_quirky | calendar_query | 0.96 | 今夜のホッケーゲームは何時ですか |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.95 | 暗くして |
| m4166 | audio_volume_other | audio_volume_up | 0.95 | 音量を最大にする |
| m50 | datetime_convert | datetime_query | 0.94 | g. m. t. プラス五の時間を教えて |
| m15203 | social_query | news_query | 0.91 | 最新情報 |

**decision-1@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 0.99 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 0.98 | 音量を最大にする |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.98 | 明かりを消して |
| m608 | audio_volume_up | audio_volume_mute | 0.95 | ミュートを解除 |
| m5911 | music_settings | play_music | 0.91 | 音楽をリプレイ |

**drex@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.92 | 明かりを消して |
| m15203 | social_query | news_query | 0.91 | 最新情報 |

**flash-lite@vercel** (38)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m944 | datetime_convert | datetime_query | 1.00 | ここと日本の時差はどれくらい |
| m2480 | takeaway_order | takeaway_query | 1.00 | テイクアウトの電話 |
| m10931 | lists_query | music_query | 1.00 | 私のプレイリストにある曲は何ですか |
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 1.00 | 音量を最大にする |
| m2165 | takeaway_query | cooking_query | 1.00 | ディナーはできましたか |
| m9562 | play_radio | play_music | 1.00 | この番組を再生してください |
| m8795 | calendar_query | lists_query | 1.00 | 保留中のリマインダーを表示する |

**haiku@vercel** (43)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m2480 | takeaway_order | takeaway_query | 1.00 | テイクアウトの電話 |
| m10931 | lists_query | music_query | 1.00 | 私のプレイリストにある曲は何ですか |
| m5152 | music_settings | music_query | 1.00 | 二曲スキップして |
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 1.00 | 音量を最大にする |
| m2165 | takeaway_query | cooking_query | 1.00 | ディナーはできましたか |
| m9562 | play_radio | play_music | 1.00 | この番組を再生してください |
| m5919 | news_query | qa_factoid | 1.00 | 江戸川に関わる事業案について最新情報を教えて |

**jev** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 1.00 | 最新情報 |
| m5911 | music_settings | play_music | 1.00 | 音楽をリプレイ |
| m13242 | general_quirky | cooking_recipe | 0.99 | 一番美味しい抹茶ケーキのレシピは何 |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.93 | 明かりを消して |
| m10931 | lists_query | music_query | 0.93 | 私のプレイリストにある曲は何ですか |

**jev@vercel** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 1.00 | 最新情報 |
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m5911 | music_settings | play_music | 1.00 | 音楽をリプレイ |
| m4268 | music_settings | play_music | 0.98 | リストの次の曲に移動 |
| m4130 | alarm_query | alarm_set | 0.97 | ダンス教室のためにアラームは設定されている |
| m10931 | lists_query | music_query | 0.96 | 私のプレイリストにある曲は何ですか |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.96 | 明かりを消して |
| m5691 | music_likeness | play_music | 0.94 | サカナクション |

**laya@vercel** (60)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m16002 | email_query | email_sendemail | 1.00 | 新しいメールを確認する |
| m16317 | email_query | email_sendemail | 1.00 | 沙羅から新しいメール |
| m16470 | email_addcontact | email_sendemail | 1.00 | このメールを私の連絡先に追加してください |
| m16353 | email_query | email_sendemail | 1.00 | 隆雄からのメールを確認 |
| m16178 | email_query | email_sendemail | 1.00 | 今日 amazon から何かメールは |
| m15987 | email_addcontact | email_sendemail | 1.00 | この新着メールを連絡先に追加する |
| m16693 | email_addcontact | email_sendemail | 1.00 | 愛知県名古屋市にある lowes ホームセンターを連絡先メールに追加する |
| m16627 | email_query | email_sendemail | 1.00 | 最新のメールを確認する |

**luna@decisions** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m10931 | lists_query | music_query | 1.00 | 私のプレイリストにある曲は何ですか |
| m3204 | music_likeness | music_dislikeness | 0.98 | ジャズが好きでディスコは嫌い |
| m13242 | general_quirky | cooking_recipe | 0.98 | 一番美味しい抹茶ケーキのレシピは何 |
| m15203 | social_query | news_query | 0.97 | 最新情報 |
| m4166 | audio_volume_other | audio_volume_up | 0.96 | 音量を最大にする |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.91 | 暗くして |

**mercury@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13372 | general_quirky | calendar_query | 1.00 | 今夜のホッケーゲームは何時ですか |
| m4813 | datetime_query | datetime_convert | 1.00 | 他の都市の時間は |
| m10931 | lists_query | music_query | 0.99 | 私のプレイリストにある曲は何ですか |
| m10216 | cooking_recipe | cooking_query | 0.99 | マフィンを焼く道具を探す |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.98 | 暗くして |
| m3364 | general_joke | general_greet | 0.94 | ノックノック |
| m14917 | qa_factoid | music_query | 0.94 | 米津玄師の最新アルバムはいつ発売 |
| m15199 | social_query | news_query | 0.92 | 何が起きているの |

**span@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | 明かりを消して |
| m15203 | social_query | news_query | 0.99 | 最新情報 |
| m4166 | audio_volume_other | audio_volume_up | 0.99 | 音量を最大にする |
| m8322 | general_quirky | recommendation_events | 0.98 | 今週末のフェアについてもっと知りたい |
| m2016 | iot_hue_lightdim | iot_hue_lightoff | 0.97 | キッチンのライトを落とす |
| m5812 | audio_volume_other | music_settings | 0.95 | 既定のオーディオ設定にする |
| m13242 | general_quirky | cooking_recipe | 0.94 | 一番美味しい抹茶ケーキのレシピは何 |
| m2165 | takeaway_query | cooking_query | 0.94 | ディナーはできましたか |


## Cases the models disagree on (12 of 93)

| id | label | clef | clef-flash | clef-omni@openrouter | d1-ultra@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex@openrouter | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | laya@vercel | luna@decisions | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| m944 | datetime_convert | datetime_convert (0.88) | datetime_convert (0.94) | datetime_convert (0.75) | datetime_convert (0.40) | datetime_query (0.51) | datetime_query (0.62) | datetime_convert (0.94) | datetime_convert (0.85) | datetime_convert (0.42) | datetime_query (1.00) | datetime_convert (1.00) | datetime_query (0.61) | datetime_query (0.70) | datetime_query (0.28) | weather_query (0.81) | datetime_convert (0.66) | datetime_convert (1.00) | datetime_convert (0.56) | ここと日本の時差はどれくらい |
| m16781 | email_addcontact | email_sendemail (0.83) | email_sendemail (0.79) | email_sendemail (0.76) | email_addcontact (0.64) | email_addcontact (0.73) | email_sendemail (0.72) | email_sendemail (0.58) | email_addcontact (0.65) | email_addcontact (0.94) | email_addcontact (1.00) | email_addcontact (1.00) | email_addcontact (0.70) | email_addcontact (0.78) | email_addcontact (0.81) | email_sendemail (1.00) | email_sendemail (0.55) | email_addcontact (0.98) | email_addcontact (0.99) | このメールアドレスを連絡先に追加してメールを送る |
| m46 | general_greet | qa_definition (0.38) | general_greet (0.53) | general_quirky (0.44) | general_greet (0.32) | general_quirky (0.22) | qa_definition (0.34) | general_quirky (0.22) | general_greet (0.71) | qa_definition (0.31) | general_greet (1.00) | general_quirky (1.00) | general_greet (0.56) | general_greet (0.70) | qa_factoid (0.07) | qa_definition (0.41) | general_quirky (0.63) | general_quirky (0.38) | general_greet (0.68) | 何ですか、オリ―さん |
| m16693 | email_addcontact | email_addcontact (0.96) | email_addcontact (0.97) | email_addcontact (0.83) | email_addcontact (0.97) | email_addcontact (0.97) | email_addcontact (0.98) | email_addcontact (0.99) | email_addcontact (0.99) | email_addcontact (0.98) | email_addcontact (1.00) | email_addcontact (1.00) | email_addcontact (1.00) | email_addcontact (1.00) | email_addcontact (0.75) | email_sendemail (1.00) | email_addcontact (0.99) | email_addcontact (1.00) | email_addcontact (1.00) | 愛知県名古屋市にある lowes ホームセンターを連絡先メールに追加する |
| m2255 | takeaway_order | takeaway_query (0.80) | takeaway_query (0.85) | takeaway_query (0.63) | takeaway_order (0.48) | takeaway_query (0.77) | takeaway_order (0.99) | takeaway_order (0.96) | takeaway_query (0.62) | takeaway_order (0.58) | takeaway_query (1.00) | takeaway_query (1.00) | takeaway_query (0.63) | takeaway_query (0.85) | takeaway_query (0.57) | takeaway_order (0.98) | takeaway_query (0.82) | takeaway_order (0.97) | takeaway_query (0.90) | 星野珈琲でテイクアウトを注文できますか |
| m6959 | calendar_set | calendar_set (0.94) | calendar_set (0.96) | calendar_set (0.91) | alarm_set (0.46) | calendar_set (0.97) | calendar_set (0.87) | calendar_set (0.99) | calendar_set (0.83) | alarm_set (0.81) | calendar_set (1.00) | alarm_set (1.00) | calendar_set (0.81) | calendar_set (0.82) | calendar_set (0.19) | iot_wemo_off (0.33) | alarm_set (0.36) | calendar_set (0.86) | calendar_set (0.94) | 一時間前に会議についてリマインドしてください |
| m4013 | iot_cleaning | iot_cleaning (0.92) | iot_cleaning (0.85) | iot_cleaning (0.64) | iot_cleaning (0.96) | iot_cleaning (0.92) | iot_cleaning (0.79) | iot_cleaning (1.00) | iot_cleaning (0.99) | iot_cleaning (0.40) | iot_cleaning (1.00) | iot_cleaning (1.00) | iot_cleaning (0.88) | iot_cleaning (0.60) | general_quirky (0.11) | iot_cleaning (0.95) | iot_cleaning (0.93) | iot_cleaning (0.95) | iot_cleaning (0.97) | ほこりを吸いましょう |
| m5318 | play_music | play_music (0.90) | play_music (0.96) | play_music (0.66) | play_music (0.92) | play_music (0.97) | play_music (0.97) | play_music (0.99) | play_music (0.95) | play_music (0.88) | play_music (1.00) | play_music (1.00) | play_music (1.00) | play_music (1.00) | play_music (0.56) | audio_volume_down (0.93) | play_music (1.00) | play_music (1.00) | play_music (0.74) | 福山雅治の歌だけ流して |
| m17123 | email_sendemail | email_sendemail (0.92) | email_sendemail (0.92) | email_sendemail (0.82) | email_sendemail (0.48) | email_sendemail (0.80) | email_sendemail (0.73) | email_sendemail (0.74) | email_sendemail (0.62) | email_sendemail (0.43) | email_sendemail (1.00) | email_query (1.00) | email_sendemail (0.48) | email_sendemail (0.80) | email_query (0.36) | email_sendemail (1.00) | email_sendemail (0.78) | email_sendemail (0.98) | email_sendemail (0.78) | 現地の副社長用のメールフォーム |
| m16353 | email_query | email_query (0.95) | email_query (0.96) | email_query (0.73) | email_query (0.95) | email_query (1.00) | email_query (0.98) | email_query (1.00) | email_query (0.98) | email_query (0.93) | email_query (1.00) | email_query (1.00) | email_query (0.82) | email_query (0.68) | email_query (0.63) | email_sendemail (1.00) | email_query (0.99) | email_query (1.00) | email_query (0.97) | 隆雄からのメールを確認 |
| m4887 | music_likeness | music_likeness (0.92) | music_likeness (0.95) | music_likeness (0.73) | music_likeness (0.81) | music_likeness (0.77) | music_likeness (0.92) | music_likeness (0.92) | music_likeness (0.94) | play_music (0.56) | music_likeness (1.00) | music_likeness (1.00) | music_likeness (0.29) | music_likeness (0.31) | lists_createoradd (0.15) | iot_wemo_off (0.97) | music_likeness (0.23) | music_likeness (0.93) | music_likeness (0.77) | アデルの曲に私の意見をセーブして |
| m6014 | music_query | music_query (0.97) | music_query (0.98) | music_query (0.82) | music_query (0.74) | music_query (0.99) | music_query (0.96) | music_query (0.98) | music_query (0.85) | music_query (0.34) | music_query (1.00) | music_query (1.00) | music_query (0.69) | music_query (0.73) | music_query (0.49) | email_querycontact (0.88) | music_query (0.21) | music_query (1.00) | music_query (0.70) | このアーティストは誰 |
