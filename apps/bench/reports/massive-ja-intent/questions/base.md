# massive-ja-intent

2026-10-31 · 201 labelled dev cases (social_post 5, play_audiobook 5, email_query 5, general_quirky 5, qa_maths 5, iot_hue_lightoff 5, audio_volume_mute 5, datetime_convert 4, more) · split: stratified k-fold (no test case among these: CV numbers only) · source: MASSIVE 1.1 ja-JP test（Amazon, CC BY 4.0）から各意図 5 件まで

**decider@openrouter** has the highest accuracy (all), 92% [88, 95] (API cost $0.15 per 10k, p99 373ms). Its interval overlaps with clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, jev:1.14, joey@openrouter, luna@decisions, mammoth@openrouter, mercury@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is decider@openrouter's, 92% [88, 95].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 0 | — | | | | | | 201/201 | 0/201 |
| clef@openrouter | 201 | 89.6% [86, 94] | 0.85 | 1.00 | 0.04 | 90% [86, 94] | 95.6% (92.2%) | 0/201 | 0/201 |
| d1-ultra@openrouter | 201 | 86.6% [82, 91] | 0.83 | 0.99 | 0.06 | 76% [70, 82] | 94.8% (90.8%) | 0/201 | 0/201 |
| d1.1@openrouter | 201 | 86.6% [82, 92] | 0.82 | 0.99 | 0.05 | 75% [69, 81] | 94.0% (89.8%) | 0/201 | 0/201 |
| d1@vercel | 201 | 85.1% [80, 90] | 0.82 | 0.99 | 0.06 | 66% [59, 72] | 93.9% (89.3%) | 0/201 | 0/201 |
| decider-flash@openrouter | 201 | 86.1% [82, 91] | 0.82 | 1.00 | 0.04 | 78% [73, 84] | 94.3% (90.2%) | 0/201 | 0/201 |
| decider@openrouter | 201 | 91.5% [88, 95] | 0.88 | 1.00 | 0.03 | 94% [91, 97] | 94.7% (91.2%) | 0/201 | 0/201 |
| decision-1@openrouter | 201 | 90.0% [86, 94] | 0.87 | 1.00 | 0.06 | 85% [81, 90] | 94.7% (91.0%) | 0/201 | 0/201 |
| drex-max@openrouter | 201 | 89.1% [85, 94] | 0.85 | 1.00 | 0.07 | 86% [81, 90] | 94.2% (90.3%) | 0/201 | 0/201 |
| elephant@openrouter | 201 | 90.5% [86, 95] | 0.87 | 1.00 | 0.06 | 83% [79, 88] | 93.4% (89.3%) | 0/201 | 0/201 |
| jev:1.14 | 201 | 84.6% [80, 90] | 0.81 | 0.98 | 0.07 | 76% [71, 82] | 94.8% (90.8%) | 0/201 | 0/201 |
| joey@openrouter | 201 | 84.1% [79, 90] | 0.80 | 0.99 | 0.06 | 67% [61, 74] | 94.1% (89.6%) | 0/201 | 0/201 |
| kev@openrouter | 201 | 75.6% [69, 81] | 0.70 | 0.98 | 0.21 | 48% [41, 54] | 94.8% (89.4%) | 0/201 | 0/201 |
| luna@decisions | 201 | 86.1% [81, 91] | 0.82 | 0.98 | 0.06 | 69% [62, 75] | 94.2% (89.8%) | 0/201 | 0/201 |
| mammoth@openrouter | 201 | 89.6% [85, 93] | 0.86 | 1.00 | 0.06 | 91% [87, 95] | 94.0% (90.2%) | 0/201 | 0/201 |
| mercury@openrouter | 201 | 90.0% [86, 94] | 0.85 | 0.99 | 0.09 | 85% [80, 90] | 95.3% (91.7%) | 0/201 | 0/201 |
| span@openrouter | 201 | 87.1% [82, 92] | 0.82 | 0.99 | 0.06 | 78% [72, 83] | 94.2% (90.1%) | 0/201 | 0/201 |

Answered by: clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| clef@openrouter = | 90% [86, 94] | — | met |
| d1-ultra@openrouter = | 87% [82, 91] | — | met |
| d1.1@openrouter = | 87% [82, 92] | — | met |
| d1@vercel = | 85% [80, 90] | — | met |
| decider-flash@openrouter = | 86% [82, 91] | — | met |
| decider@openrouter = | 92% [88, 95] | — | met |
| decision-1@openrouter = | 90% [86, 94] | — | met |
| drex-max@openrouter = | 89% [85, 94] | — | met |
| elephant@openrouter = | 91% [86, 95] | — | met |
| jev:1.14 = | 85% [80, 90] | — | met |
| joey@openrouter = | 84% [79, 90] | — | met |
| luna@decisions = | 86% [81, 91] | — | met |
| mammoth@openrouter = | 90% [85, 93] | — | met |
| mercury@openrouter = | 90% [86, 94] | — | met |
| span@openrouter = | 87% [82, 92] | — | met |
| kev@openrouter | 76% [69, 81] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef@openrouter | 201 | 416 ms | 1032 ms | 2118 ms | 2554 ms | 5.1 | 0 | 4 | $3.06 | billed |  |
| d1-ultra@openrouter | 201 | 217 ms | 295 ms | 1071 ms | 1997 ms | 4.9 | 0 | 4 | $0.18 | billed |  |
| d1.1@openrouter | 201 | 172 ms | 203 ms | 448 ms | 610 ms | 2.6 | 0 | 4 | $0.09 | billed | ○ |
| d1@vercel | 201 | 249 ms | 350 ms | 594 ms | 5035 ms | 2.4 | 0 | 4 | $0.09 | billed |  |
| decider-flash@openrouter | 201 | 143 ms | 155 ms | 176 ms | 240 ms | 1.2 | 0 | 4 | $0.07 | billed | ○ |
| decider@openrouter | 201 | 226 ms | 264 ms | 373 ms | 636 ms | 1.7 | 0 | 4 | $0.15 | billed | ○ |
| decision-1@openrouter | 201 | 296 ms | 410 ms | 796 ms | 1730 ms | 2.7 | 0 | 4 | $0.24 | billed |  |
| drex-max@openrouter | 201 | 389 ms | 764 ms | 1122 ms | 1139 ms | 2.9 | 9 | 4 | $0.45 | billed |  |
| elephant@openrouter | 201 | 193 ms | 216 ms | 390 ms | 470 ms | 2.0 | 0 | 4 | $0.30 | billed |  |
| jev:1.14 | 201 | 150 ms | 180 ms | 294 ms | 488 ms | 2.0 | 1 | 4 | $0.58 | estimated |  |
| joey@openrouter | 201 | 181 ms | 202 ms | 307 ms | 440 ms | 1.7 | 0 | 4 | $0.09 | billed |  |
| kev@openrouter | 201 | 488 ms | 638 ms | 1151 ms | 1322 ms | 2.4 | 0 | 4 | $0.26 | billed |  |
| luna@decisions | 201 | 220 ms | 530 ms | 669 ms | 817 ms | 3.0 | 0 | 4 | $0.79 | estimated |  |
| mammoth@openrouter | 201 | 232 ms | 262 ms | 419 ms | 487 ms | 1.8 | 0 | 4 | $0.86 | billed |  |
| mercury@openrouter | 201 | 336 ms | 440 ms | 597 ms | 628 ms | 1.8 | 0 | 4 | $0.24 | billed |  |
| span@openrouter | 201 | 253 ms | 430 ms | 798 ms | 862 ms | 3.2 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef@openrouter | $0.06 | 28 s (estimated, 201 calls) | 24 min | 4 |
| d1-ultra@openrouter | $0.0036 | 13 s (estimated, 201 calls) | 10 min | 4 |
| d1.1@openrouter | $0.0017 | 9 s (estimated, 201 calls) | 8 min | 4 |
| d1@vercel | $0.0017 | 15 s (estimated, 201 calls) | 12 min | 4 |
| decider-flash@openrouter | $0.0015 | 7 s (estimated, 201 calls) | 6 min | 4 |
| decider@openrouter | $0.0030 | 12 s (estimated, 201 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0048 | 17 s (estimated, 201 calls) | 14 min | 4 |
| drex-max@openrouter | $0.0090 | 23 s (estimated, 201 calls) | 19 min | 4 |
| elephant@openrouter | $0.0061 | 10 s (estimated, 201 calls) | 8 min | 4 |
| jev:1.14 | $0.01 | 8 s (estimated, 201 calls) | 7 min | 4 |
| joey@openrouter | $0.0017 | 9 s (estimated, 201 calls) | 8 min | 4 |
| kev@openrouter | $0.0052 | 21 s (estimated, 201 calls) | 17 min | 4 |
| luna@decisions | $0.02 | 14 s (estimated, 201 calls) | 12 min | 4 |
| mammoth@openrouter | $0.02 | 12 s (estimated, 201 calls) | 10 min | 4 |
| mercury@openrouter | $0.0049 | 18 s (estimated, 201 calls) | 15 min | 4 |
| span@openrouter | $0.0010 | 14 s (estimated, 201 calls) | 12 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Wrong at a high probability (0.9 or more)

**clef@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.95 | 明かりを消して |
| m4166 | audio_volume_other | audio_volume_up | 0.95 | 音量を最大にする |
| m13242 | general_quirky | cooking_recipe | 0.94 | 一番美味しい抹茶ケーキのレシピは何 |
| m10931 | lists_query | music_query | 0.94 | 私のプレイリストにある曲は何ですか |
| m15203 | social_query | news_query | 0.94 | 最新情報 |

**d1-ultra@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 0.98 | 最新情報 |

**d1.1@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 0.96 | 最新情報 |
| m5911 | music_settings | play_music | 0.96 | 音楽をリプレイ |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.94 | 明かりを消して |
| m16317 | email_query | email_sendemail | 0.93 | 沙羅から新しいメール |

**d1@vercel** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m4130 | alarm_query | alarm_set | 0.99 | ダンス教室のためにアラームは設定されている |
| m8322 | general_quirky | recommendation_events | 0.98 | 今週末のフェアについてもっと知りたい |
| m15203 | social_query | news_query | 0.98 | 最新情報 |
| m13242 | general_quirky | cooking_recipe | 0.98 | 一番美味しい抹茶ケーキのレシピは何 |
| m5812 | audio_volume_other | music_settings | 0.96 | 既定のオーディオ設定にする |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.92 | 明かりを消して |
| m12264 | transport_query | weather_query | 0.91 | ニューヨーク |
| m4166 | audio_volume_other | audio_volume_up | 0.90 | 音量を最大にする |

**decider-flash@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 0.97 | 一番美味しい抹茶ケーキのレシピは何 |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.96 | 明かりを消して |
| m4166 | audio_volume_other | audio_volume_up | 0.96 | 音量を最大にする |
| m15333 | social_query | social_post | 0.96 | インスタグラムに何か新しいこと |
| m16317 | email_query | email_sendemail | 0.95 | 沙羅から新しいメール |
| m15203 | social_query | news_query | 0.93 | 最新情報 |
| m10931 | lists_query | music_query | 0.92 | 私のプレイリストにある曲は何ですか |
| m2578 | iot_hue_lightoff | iot_wemo_off | 0.91 | ポーチの電気を消す |

**decider@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.98 | 明かりを消して |
| m13372 | general_quirky | calendar_query | 0.96 | 今夜のホッケーゲームは何時ですか |
| m50 | datetime_convert | datetime_query | 0.96 | g. m. t. プラス五の時間を教えて |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.94 | 暗くして |
| m4166 | audio_volume_other | audio_volume_up | 0.93 | 音量を最大にする |

**decision-1@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 0.99 | 音量を最大にする |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | 明かりを消して |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.97 | 暗くして |
| m15203 | social_query | news_query | 0.94 | 最新情報 |
| m2016 | iot_hue_lightdim | iot_hue_lightoff | 0.94 | キッチンのライトを落とす |
| m50 | datetime_convert | datetime_query | 0.93 | g. m. t. プラス五の時間を教えて |
| m8322 | general_quirky | recommendation_events | 0.92 | 今週末のフェアについてもっと知りたい |

**drex-max@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | 明かりを消して |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.99 | 暗くして |
| m13372 | general_quirky | calendar_query | 0.98 | 今夜のホッケーゲームは何時ですか |
| m13242 | general_quirky | cooking_recipe | 0.98 | 一番美味しい抹茶ケーキのレシピは何 |
| m15203 | social_query | news_query | 0.98 | 最新情報 |
| m4166 | audio_volume_other | audio_volume_up | 0.92 | 音量を最大にする |

**elephant@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 0.99 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 0.99 | 音量を最大にする |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | 明かりを消して |
| m15203 | social_query | news_query | 0.98 | 最新情報 |
| m2255 | takeaway_order | takeaway_query | 0.95 | 星野珈琲でテイクアウトを注文できますか |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.94 | 暗くして |
| m14917 | qa_factoid | music_query | 0.92 | 米津玄師の最新アルバムはいつ発売 |

**jev:1.14** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 1.00 | 最新情報 |
| m13242 | general_quirky | cooking_recipe | 0.99 | 一番美味しい抹茶ケーキのレシピは何 |
| m5911 | music_settings | play_music | 0.99 | 音楽をリプレイ |
| m10931 | lists_query | music_query | 0.94 | 私のプレイリストにある曲は何ですか |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.93 | 明かりを消して |

**joey@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 0.98 | 一番美味しい抹茶ケーキのレシピは何 |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.98 | 明かりを消して |
| m10931 | lists_query | music_query | 0.98 | 私のプレイリストにある曲は何ですか |
| m4166 | audio_volume_other | audio_volume_up | 0.96 | 音量を最大にする |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.96 | 暗くして |
| m9554 | play_radio | play_music | 0.94 | ベイエフエム七八でロマンチックな音楽を再生する |
| m11273 | play_audiobook | play_podcasts | 0.92 | j. k. rowling の harry potter の次の回を再生して |
| m2578 | iot_hue_lightoff | iot_wemo_off | 0.92 | ポーチの電気を消す |

**luna@decisions** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m10931 | lists_query | music_query | 1.00 | 私のプレイリストにある曲は何ですか |
| m13242 | general_quirky | cooking_recipe | 0.99 | 一番美味しい抹茶ケーキのレシピは何 |
| m15203 | social_query | news_query | 0.98 | 最新情報 |
| m3204 | music_likeness | music_dislikeness | 0.97 | ジャズが好きでディスコは嫌い |
| m4166 | audio_volume_other | audio_volume_up | 0.93 | 音量を最大にする |
| m9562 | play_radio | play_music | 0.90 | この番組を再生してください |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.90 | 明かりを消して |

**mammoth@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m4166 | audio_volume_other | audio_volume_up | 0.99 | 音量を最大にする |
| m13242 | general_quirky | cooking_recipe | 0.99 | 一番美味しい抹茶ケーキのレシピは何 |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | 明かりを消して |
| m15203 | social_query | news_query | 0.98 | 最新情報 |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.93 | 暗くして |
| m2255 | takeaway_order | takeaway_query | 0.92 | 星野珈琲でテイクアウトを注文できますか |
| m10931 | lists_query | music_query | 0.90 | 私のプレイリストにある曲は何ですか |

**mercury@openrouter** (17)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m4813 | datetime_query | datetime_convert | 1.00 | 他の都市の時間は |
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m15203 | social_query | news_query | 1.00 | 最新情報 |
| m974 | datetime_query | datetime_convert | 1.00 | ニューヨークは何時ですか |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 1.00 | 明かりを消して |
| m13372 | general_quirky | calendar_query | 1.00 | 今夜のホッケーゲームは何時ですか |
| m9562 | play_radio | play_podcasts | 0.99 | この番組を再生してください |
| m4702 | audio_volume_up | iot_wemo_on | 0.98 | スピーカーをオンにしてください |

**span@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | 明かりを消して |
| m15203 | social_query | news_query | 0.99 | 最新情報 |
| m4166 | audio_volume_other | audio_volume_up | 0.99 | 音量を最大にする |
| m8322 | general_quirky | recommendation_events | 0.98 | 今週末のフェアについてもっと知りたい |
| m2016 | iot_hue_lightdim | iot_hue_lightoff | 0.97 | キッチンのライトを落とす |
| m5812 | audio_volume_other | music_settings | 0.95 | 既定のオーディオ設定にする |
| m13242 | general_quirky | cooking_recipe | 0.94 | 一番美味しい抹茶ケーキのレシピは何 |
| m2255 | takeaway_order | takeaway_query | 0.90 | 星野珈琲でテイクアウトを注文できますか |


## Cases the models disagree on (12 of 62)

| id | label | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| m2578 | iot_hue_lightoff | iot_hue_lightoff (0.95) | iot_hue_lightoff (0.58) | iot_hue_lightoff (0.87) | iot_hue_lightoff (0.86) | iot_wemo_off (0.91) | iot_hue_lightoff (1.00) | iot_hue_lightoff (0.62) | iot_hue_lightoff (0.97) | iot_hue_lightoff (0.74) | iot_hue_lightoff (0.78) | iot_wemo_off (0.92) | iot_wemo_off (0.24) | iot_hue_lightoff (1.00) | iot_hue_lightoff (0.96) | iot_hue_lightoff (1.00) | iot_hue_lightoff (0.99) | ポーチの電気を消す |
| m3205 | play_music | play_music (0.96) | play_music (0.97) | play_music (0.99) | play_music (1.00) | play_music (0.94) | play_music (1.00) | play_music (1.00) | play_music (1.00) | play_music (0.98) | play_music (0.98) | play_music (0.91) | iot_hue_lightchange (0.11) | play_music (1.00) | play_music (0.99) | play_music (1.00) | play_music (0.94) | レディーガガの poker face をかけて |
| m11273 | play_audiobook | play_audiobook (0.90) | play_audiobook (0.89) | play_audiobook (0.89) | play_audiobook (0.96) | play_audiobook (0.95) | play_audiobook (0.93) | play_audiobook (1.00) | play_audiobook (0.99) | play_audiobook (0.94) | play_audiobook (1.00) | play_podcasts (0.92) | recommendation_movies (0.31) | play_audiobook (0.65) | play_audiobook (0.83) | play_audiobook (1.00) | play_audiobook (1.00) | j. k. rowling の harry potter の次の回を再生して |
| m10931 | lists_query | music_query (0.94) | music_query (0.84) | music_query (0.80) | music_query (0.83) | music_query (0.92) | lists_query (0.61) | music_query (0.62) | music_query (0.83) | music_query (0.73) | music_query (0.94) | music_query (0.98) | music_query (0.54) | music_query (1.00) | music_query (0.90) | music_query (0.98) | music_query (0.73) | 私のプレイリストにある曲は何ですか |
| m2201 | news_query | news_query (0.91) | news_query (0.94) | news_query (0.98) | news_query (0.76) | news_query (0.94) | news_query (0.99) | news_query (0.99) | news_query (0.99) | news_query (0.80) | news_query (1.00) | play_radio (0.21) | news_query (0.15) | news_query (0.82) | news_query (0.99) | news_query (1.00) | news_query (0.98) | エヌエッチケーの見出し |
| m6166 | audio_volume_mute | audio_volume_mute (0.95) | audio_volume_mute (0.90) | audio_volume_mute (0.94) | audio_volume_mute (0.98) | audio_volume_mute (0.99) | audio_volume_mute (1.00) | audio_volume_mute (1.00) | audio_volume_mute (1.00) | audio_volume_mute (0.98) | audio_volume_mute (0.99) | audio_volume_mute (0.99) | audio_volume_other (0.12) | audio_volume_mute (1.00) | audio_volume_mute (1.00) | audio_volume_mute (1.00) | audio_volume_mute (0.92) | 五分間ミュートにして |
| m13552 | qa_maths | qa_maths (0.81) | qa_maths (0.99) | qa_maths (0.99) | qa_maths (0.98) | qa_maths (0.94) | qa_maths (0.99) | qa_maths (1.00) | qa_maths (1.00) | qa_maths (1.00) | qa_maths (1.00) | qa_maths (0.46) | datetime_query (0.07) | qa_maths (0.99) | qa_maths (0.99) | qa_maths (0.99) | qa_maths (1.00) | 六わる二は |
| m5593 | play_music | play_music (0.91) | play_music (0.98) | play_music (0.98) | play_music (0.99) | play_radio (0.61) | play_music (0.99) | play_music (1.00) | play_music (1.00) | play_music (0.96) | play_music (0.98) | play_podcasts (0.33) | recommendation_movies (0.10) | play_music (0.97) | play_music (0.98) | play_music (1.00) | play_music (0.95) | バンプオブチキンの天体観測を流して |
| m16317 | email_query | email_query (0.94) | email_query (0.91) | email_sendemail (0.93) | email_query (0.95) | email_sendemail (0.95) | email_query (0.99) | email_query (0.97) | email_query (0.99) | email_query (0.99) | email_query (0.77) | email_query (0.87) | email_query (0.27) | email_query (0.73) | email_query (0.99) | email_query (1.00) | email_query (0.98) | 沙羅から新しいメール |
| m15565 | social_post | social_post (0.96) | transport_ticket (0.41) | email_sendemail (0.63) | general_quirky (0.57) | general_quirky (0.47) | social_post (0.99) | social_post (0.66) | social_post (0.98) | social_post (0.71) | email_sendemail (0.60) | iot_wemo_off (0.25) | transport_query (0.08) | social_query (0.26) | social_post (0.99) | social_post (1.00) | email_sendemail (0.60) | もう絶対使わないと全日空に知らせて |
| m16983 | email_querycontact | email_querycontact (0.91) | email_querycontact (0.78) | email_querycontact (0.79) | email_querycontact (0.75) | email_querycontact (0.92) | email_querycontact (0.98) | email_querycontact (1.00) | email_querycontact (1.00) | email_querycontact (0.98) | social_query (0.37) | email_querycontact (0.99) | email_querycontact (0.12) | qa_factoid (0.36) | email_querycontact (0.98) | email_querycontact (1.00) | email_querycontact (0.93) | 河野さんの事務所の電話番号を知っていますか |
| m944 | datetime_convert | datetime_convert (0.91) | datetime_query (0.50) | datetime_convert (0.50) | datetime_query (0.55) | datetime_query (0.66) | datetime_convert (0.93) | datetime_convert (0.83) | datetime_convert (0.83) | datetime_convert (0.73) | datetime_query (0.63) | datetime_convert (0.68) | datetime_query (0.28) | datetime_convert (0.90) | datetime_convert (0.87) | datetime_convert (1.00) | datetime_convert (0.56) | ここと日本の時差はどれくらい |
