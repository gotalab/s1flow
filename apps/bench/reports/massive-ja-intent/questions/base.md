# massive-ja-intent

2026-11-11 · 201 labelled dev cases (social_post 5, play_audiobook 5, email_query 5, general_quirky 5, qa_maths 5, iot_hue_lightoff 5, audio_volume_mute 5, datetime_convert 4, more) · split: stratified k-fold (no test case among these: CV numbers only) · source: MASSIVE 1.1 ja-JP test（Amazon, CC BY 4.0）から各意図 5 件まで

**decider@openrouter** has the highest accuracy (all), 91% [87, 95] (API cost $0.15 per 10k, p99 1694ms). Its interval overlaps with clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, jev:1.14, joey@openrouter, luna@decisions, mammoth@openrouter, reflex@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is decider@openrouter's, 91% [87, 95].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 0 | — | | | | | | 201/201 | 0/201 |
| clef-omni@openrouter | 201 | 90.0% [86, 94] | 0.87 | 0.99 | 0.16 | 78% [72, 84] | 94.9% (91.0%) | 0/201 | 0/201 |
| clef@openrouter | 201 | 89.6% [86, 94] | 0.85 | 1.00 | 0.05 | 89% [85, 93] | 95.5% (92.1%) | 0/201 | 0/201 |
| d1-ultra@openrouter | 201 | 85.6% [81, 91] | 0.82 | 0.99 | 0.06 | 75% [69, 81] | 94.7% (90.6%) | 0/201 | 0/201 |
| d1.1@openrouter | 201 | 87.1% [82, 92] | 0.83 | 0.99 | 0.03 | 77% [71, 83] | 93.5% (89.2%) | 0/201 | 0/201 |
| d1@vercel | 201 | 87.1% [83, 92] | 0.83 | 0.99 | 0.06 | 62% [55, 68] | 93.5% (88.7%) | 0/201 | 0/201 |
| decider-flash@openrouter | 201 | 86.1% [81, 91] | 0.82 | 1.00 | 0.04 | 78% [72, 84] | 94.9% (91.0%) | 0/201 | 0/201 |
| decider@openrouter | 201 | 91.0% [87, 95] | 0.88 | 1.00 | 0.03 | 93% [89, 96] | 94.6% (91.1%) | 0/201 | 0/201 |
| decision-1@openrouter | 201 | 89.1% [85, 93] | 0.86 | 1.00 | 0.07 | 90% [86, 94] | 95.0% (91.4%) | 0/201 | 0/201 |
| drex-max@openrouter | 201 | 89.1% [85, 94] | 0.85 | 1.00 | 0.05 | 87% [82, 92] | 94.3% (90.5%) | 0/201 | 0/201 |
| elephant@openrouter | 201 | 90.5% [87, 95] | 0.87 | 1.00 | 0.06 | 84% [79, 89] | 94.1% (90.2%) | 0/201 | 0/201 |
| gemini-decision@openrouter | 201 | 88.1% [84, 93] | 0.85 | 0.99 | 0.03 | 74% [67, 80] | 95.3% (91.3%) | 0/201 | 0/201 |
| jev:1.14 | 201 | 85.1% [80, 90] | 0.81 | 0.98 | 0.05 | 78% [73, 84] | 93.0% (88.7%) | 0/201 | 0/201 |
| joey@openrouter | 201 | 84.1% [79, 89] | 0.80 | 0.99 | 0.06 | 65% [59, 72] | 93.9% (89.3%) | 0/201 | 0/201 |
| kev@openrouter | 201 | 75.1% [70, 81] | 0.70 | 0.98 | 0.21 | 50% [43, 56] | 93.0% (87.3%) | 0/201 | 0/201 |
| luna@decisions | 201 | 86.1% [81, 91] | 0.82 | 0.98 | 0.06 | 68% [61, 74] | 94.1% (89.6%) | 0/201 | 0/201 |
| mammoth@openrouter | 201 | 89.6% [85, 94] | 0.86 | 1.00 | 0.05 | 89% [85, 93] | 93.9% (90.0%) | 0/201 | 0/201 |
| reflex@openrouter | 201 | 85.6% [81, 91] | 0.82 | 0.99 | 0.08 | 74% [68, 80] | 95.3% (91.3%) | 0/201 | 0/201 |
| span@openrouter | 201 | 87.1% [82, 92] | 0.82 | 0.99 | 0.06 | 78% [72, 83] | 94.9% (90.9%) | 0/201 | 0/201 |

Answered by: clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@openrouter = google/gemini-decision-1-20261111; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| clef-omni@openrouter = | 90% [86, 94] | — | met |
| clef@openrouter = | 90% [86, 94] | — | met |
| d1-ultra@openrouter = | 86% [81, 91] | — | met |
| d1.1@openrouter = | 87% [82, 92] | — | met |
| d1@vercel = | 87% [83, 92] | — | met |
| decider-flash@openrouter = | 86% [81, 91] | — | met |
| decider@openrouter = | 91% [87, 95] | — | met |
| decision-1@openrouter = | 89% [85, 93] | — | met |
| drex-max@openrouter = | 89% [85, 94] | — | met |
| elephant@openrouter = | 91% [87, 95] | — | met |
| gemini-decision@openrouter = | 88% [84, 93] | — | met |
| jev:1.14 = | 85% [80, 90] | — | met |
| joey@openrouter = | 84% [79, 89] | — | met |
| luna@decisions = | 86% [81, 91] | — | met |
| mammoth@openrouter = | 90% [85, 94] | — | met |
| reflex@openrouter = | 86% [81, 91] | — | met |
| span@openrouter = | 87% [82, 92] | — | met |
| kev@openrouter | 75% [70, 81] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-omni@openrouter | 201 | 331 ms | 438 ms | 2112 ms | 3370 ms | 6.4 | 0 | 4 | $2.14 | billed |  |
| clef@openrouter | 201 | 438 ms | 751 ms | 1221 ms | 1656 ms | 2.8 | 0 | 4 | $3.08 | billed |  |
| d1-ultra@openrouter | 201 | 384 ms | 475 ms | 1090 ms | 1132 ms | 2.8 | 0 | 4 | $0.18 | billed |  |
| d1.1@openrouter | 201 | 394 ms | 604 ms | 738 ms | 768 ms | 1.9 | 0 | 4 | $0.09 | billed |  |
| d1@vercel | 201 | 351 ms | 421 ms | 627 ms | 814 ms | 1.8 | 0 | 4 | $0.09 | billed | ○ |
| decider-flash@openrouter | 201 | 268 ms | 307 ms | 521 ms | 539 ms | 1.9 | 0 | 4 | $0.07 | billed | ○ |
| decider@openrouter | 201 | 362 ms | 585 ms | 1694 ms | 1826 ms | 4.7 | 0 | 4 | $0.15 | billed | ○ |
| decision-1@openrouter | 201 | 360 ms | 472 ms | 638 ms | 797 ms | 1.8 | 0 | 4 | $0.24 | billed | ○ |
| drex-max@openrouter | 201 | 375 ms | 1154 ms | 1531 ms | 1655 ms | 4.1 | 0 | 4 | $0.45 | billed |  |
| elephant@openrouter | 201 | 297 ms | 326 ms | 516 ms | 746 ms | 1.7 | 0 | 4 | $0.30 | billed | ○ |
| gemini-decision@openrouter | 201 | 352 ms | 511 ms | 1501 ms | 1728 ms | 4.3 | 0 | 4 | $0.78 | billed |  |
| jev:1.14 | 201 | 235 ms | 257 ms | 322 ms | 436 ms | 1.4 | 0 | 4 | $0.58 | estimated | ○ |
| joey@openrouter | 201 | 294 ms | 325 ms | 494 ms | 530 ms | 1.7 | 0 | 4 | $0.09 | billed | ○ |
| kev@openrouter | 201 | 631 ms | 773 ms | 1233 ms | 1299 ms | 2.0 | 4 | 4 | $0.26 | billed |  |
| luna@decisions | 201 | 308 ms | 496 ms | 732 ms | 1081 ms | 2.4 | 0 | 4 | $0.79 | estimated |  |
| mammoth@openrouter | 201 | 322 ms | 362 ms | 543 ms | 614 ms | 1.7 | 0 | 4 | $0.86 | billed |  |
| reflex@openrouter | 201 | 397 ms | 446 ms | 619 ms | 754 ms | 1.6 | 0 | 4 | $0.32 | billed |  |
| span@openrouter | 201 | 360 ms | 588 ms | 888 ms | 938 ms | 2.5 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, gemini-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-omni@openrouter | $0.04 | 19 s (estimated, 201 calls) | 16 min | 4 |
| clef@openrouter | $0.06 | 25 s (estimated, 201 calls) | 20 min | 4 |
| d1-ultra@openrouter | $0.0036 | 21 s (estimated, 201 calls) | 17 min | 4 |
| d1.1@openrouter | $0.0017 | 20 s (estimated, 201 calls) | 17 min | 4 |
| d1@vercel | $0.0017 | 18 s (estimated, 201 calls) | 15 min | 4 |
| decider-flash@openrouter | $0.0015 | 13 s (estimated, 201 calls) | 10 min | 4 |
| decider@openrouter | $0.0030 | 21 s (estimated, 201 calls) | 17 min | 4 |
| decision-1@openrouter | $0.0048 | 18 s (estimated, 201 calls) | 15 min | 4 |
| drex-max@openrouter | $0.0090 | 25 s (estimated, 201 calls) | 21 min | 4 |
| elephant@openrouter | $0.0061 | 15 s (estimated, 201 calls) | 13 min | 4 |
| gemini-decision@openrouter | $0.02 | 19 s (estimated, 201 calls) | 16 min | 4 |
| jev:1.14 | $0.01 | 12 s (estimated, 201 calls) | 10 min | 4 |
| joey@openrouter | $0.0017 | 15 s (estimated, 201 calls) | 12 min | 4 |
| kev@openrouter | $0.0052 | 33 s (estimated, 201 calls) | 27 min | 4 |
| luna@decisions | $0.02 | 17 s (estimated, 201 calls) | 14 min | 4 |
| mammoth@openrouter | $0.02 | 16 s (estimated, 201 calls) | 14 min | 4 |
| reflex@openrouter | $0.0063 | 19 s (estimated, 201 calls) | 16 min | 4 |
| span@openrouter | $0.0010 | 20 s (estimated, 201 calls) | 16 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.
Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, not a failed call: left out of the denominator, the candidate kept.

## Wrong at a high probability (0.9 or more)

**clef@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.96 | 明かりを消して |
| m10931 | lists_query | music_query | 0.95 | 私のプレイリストにある曲は何ですか |
| m4166 | audio_volume_other | audio_volume_up | 0.94 | 音量を最大にする |
| m15203 | social_query | news_query | 0.94 | 最新情報 |
| m13242 | general_quirky | cooking_recipe | 0.94 | 一番美味しい抹茶ケーキのレシピは何 |

**d1-ultra@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 0.97 | 最新情報 |

**d1.1@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m15203 | social_query | news_query | 0.96 | 最新情報 |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.95 | 明かりを消して |
| m5911 | music_settings | play_music | 0.93 | 音楽をリプレイ |

**d1@vercel** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m4130 | alarm_query | alarm_set | 0.99 | ダンス教室のためにアラームは設定されている |
| m8322 | general_quirky | recommendation_events | 0.98 | 今週末のフェアについてもっと知りたい |
| m15203 | social_query | news_query | 0.98 | 最新情報 |
| m13242 | general_quirky | cooking_recipe | 0.97 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 0.96 | 音量を最大にする |
| m5812 | audio_volume_other | music_settings | 0.96 | 既定のオーディオ設定にする |
| m5911 | music_settings | play_music | 0.95 | 音楽をリプレイ |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.91 | 明かりを消して |

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

**decider@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.98 | 明かりを消して |
| m13372 | general_quirky | calendar_query | 0.96 | 今夜のホッケーゲームは何時ですか |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.95 | 暗くして |
| m4166 | audio_volume_other | audio_volume_up | 0.94 | 音量を最大にする |
| m50 | datetime_convert | datetime_query | 0.93 | g. m. t. プラス五の時間を教えて |
| m15203 | social_query | news_query | 0.90 | 最新情報 |

**decision-1@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 1.00 | 一番美味しい抹茶ケーキのレシピは何 |
| m4166 | audio_volume_other | audio_volume_up | 0.99 | 音量を最大にする |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | 明かりを消して |
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.97 | 暗くして |
| m15203 | social_query | news_query | 0.93 | 最新情報 |
| m13372 | general_quirky | calendar_query | 0.93 | 今夜のホッケーゲームは何時ですか |
| m50 | datetime_convert | datetime_query | 0.92 | g. m. t. プラス五の時間を教えて |
| m8322 | general_quirky | recommendation_events | 0.92 | 今週末のフェアについてもっと知りたい |

**drex-max@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 1.00 | 明かりを消して |
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

**gemini-decision@openrouter** (2)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m8978 | calendar_set | calendar_query | 0.99 | 私の上司との重要な会議を一週間後教えてください |
| m8322 | general_quirky | recommendation_events | 0.94 | 今週末のフェアについてもっと知りたい |

**jev:1.14** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m5911 | music_settings | play_music | 1.00 | 音楽をリプレイ |
| m15203 | social_query | news_query | 1.00 | 最新情報 |
| m13242 | general_quirky | cooking_recipe | 0.99 | 一番美味しい抹茶ケーキのレシピは何 |
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 0.93 | 明かりを消して |
| m10931 | lists_query | music_query | 0.93 | 私のプレイリストにある曲は何ですか |

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
| m14 | iot_hue_lighton | iot_hue_lightdim | 0.94 | 暗くして |
| m2255 | takeaway_order | takeaway_query | 0.93 | 星野珈琲でテイクアウトを注文できますか |
| m10931 | lists_query | music_query | 0.90 | 私のプレイリストにある曲は何ですか |

**reflex@openrouter** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m3834 | iot_hue_lightdim | iot_hue_lightoff | 1.00 | 明かりを消して |
| m4166 | audio_volume_other | audio_volume_up | 0.99 | 音量を最大にする |
| m15203 | social_query | news_query | 0.99 | 最新情報 |
| m2016 | iot_hue_lightdim | iot_hue_lightoff | 0.99 | キッチンのライトを落とす |
| m50 | datetime_convert | datetime_query | 0.98 | g. m. t. プラス五の時間を教えて |
| m10931 | lists_query | music_query | 0.97 | 私のプレイリストにある曲は何ですか |
| m13242 | general_quirky | cooking_recipe | 0.97 | 一番美味しい抹茶ケーキのレシピは何 |
| m4702 | audio_volume_up | iot_wemo_on | 0.94 | スピーカーをオンにしてください |

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


## Cases the models disagree on (12 of 63)

| id | label | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| m5911 | music_settings | music_settings (0.77) | music_settings (0.85) | play_music (0.82) | play_music (0.93) | play_music (0.95) | play_music (0.88) | music_settings (0.81) | music_settings (0.61) | music_settings (0.74) | play_music (0.88) | music_settings (0.82) | play_music (1.00) | music_settings (0.62) | play_music (0.29) | play_music (0.51) | music_settings (0.54) | play_music (0.71) | play_music (0.88) | 音楽をリプレイ |
| m2578 | iot_hue_lightoff | iot_wemo_off (0.53) | iot_hue_lightoff (0.95) | iot_hue_lightoff (0.59) | iot_hue_lightoff (0.87) | iot_hue_lightoff (0.89) | iot_wemo_off (0.91) | iot_hue_lightoff (0.99) | iot_hue_lightoff (0.62) | iot_hue_lightoff (0.97) | iot_hue_lightoff (0.74) | iot_hue_lightoff (0.84) | iot_hue_lightoff (0.78) | iot_wemo_off (0.92) | iot_wemo_off (0.24) | iot_hue_lightoff (1.00) | iot_hue_lightoff (0.96) | iot_hue_lightoff (0.99) | iot_hue_lightoff (0.99) | ポーチの電気を消す |
| m3205 | play_music | play_music (0.70) | play_music (0.96) | play_music (0.98) | play_music (0.99) | play_music (1.00) | play_music (0.94) | play_music (1.00) | play_music (1.00) | play_music (1.00) | play_music (0.98) | play_music (0.99) | play_music (0.98) | play_music (0.91) | iot_hue_lightchange (0.12) | play_music (1.00) | play_music (0.99) | play_music (1.00) | play_music (0.94) | レディーガガの poker face をかけて |
| m11273 | play_audiobook | play_audiobook (0.73) | play_audiobook (0.89) | play_audiobook (0.91) | play_audiobook (0.94) | play_audiobook (0.95) | play_audiobook (0.95) | play_audiobook (0.92) | play_audiobook (1.00) | play_audiobook (0.99) | play_audiobook (0.94) | play_audiobook (0.68) | play_audiobook (1.00) | play_podcasts (0.92) | recommendation_movies (0.30) | play_audiobook (0.65) | play_audiobook (0.85) | play_audiobook (1.00) | play_audiobook (1.00) | j. k. rowling の harry potter の次の回を再生して |
| m10931 | lists_query | lists_query (0.84) | music_query (0.95) | music_query (0.88) | music_query (0.78) | music_query (0.76) | music_query (0.92) | lists_query (0.55) | music_query (0.62) | music_query (0.83) | music_query (0.73) | music_query (0.86) | music_query (0.93) | music_query (0.98) | music_query (0.54) | music_query (1.00) | music_query (0.90) | music_query (0.97) | music_query (0.77) | 私のプレイリストにある曲は何ですか |
| m2201 | news_query | news_query (0.82) | news_query (0.91) | news_query (0.96) | news_query (0.97) | news_query (0.94) | news_query (0.94) | news_query (0.98) | news_query (0.99) | news_query (0.99) | news_query (0.80) | news_query (1.00) | news_query (1.00) | play_radio (0.21) | news_query (0.14) | news_query (0.82) | news_query (0.99) | news_query (0.98) | news_query (0.98) | エヌエッチケーの見出し |
| m6166 | audio_volume_mute | audio_volume_mute (0.73) | audio_volume_mute (0.95) | audio_volume_mute (0.91) | audio_volume_mute (0.94) | audio_volume_mute (0.92) | audio_volume_mute (0.99) | audio_volume_mute (0.99) | audio_volume_mute (1.00) | audio_volume_mute (1.00) | audio_volume_mute (0.98) | audio_volume_mute (0.93) | audio_volume_mute (0.99) | audio_volume_mute (0.99) | audio_volume_other (0.13) | audio_volume_mute (1.00) | audio_volume_mute (1.00) | audio_volume_mute (1.00) | audio_volume_mute (0.92) | 五分間ミュートにして |
| m13552 | qa_maths | qa_maths (0.84) | qa_maths (0.83) | qa_maths (0.99) | qa_maths (0.99) | qa_maths (0.98) | qa_maths (0.94) | qa_maths (0.99) | qa_maths (1.00) | qa_maths (1.00) | qa_maths (1.00) | qa_maths (0.99) | qa_maths (1.00) | qa_maths (0.46) | datetime_query (0.07) | qa_maths (0.99) | qa_maths (0.99) | qa_maths (1.00) | qa_maths (1.00) | 六わる二は |
| m5593 | play_music | play_music (0.69) | play_music (0.95) | play_music (0.97) | play_music (0.98) | play_music (0.98) | play_radio (0.61) | play_music (0.99) | play_music (1.00) | play_music (1.00) | play_music (0.96) | play_music (0.99) | play_music (0.88) | play_podcasts (0.33) | recommendation_movies (0.10) | play_music (0.97) | play_music (0.98) | play_music (1.00) | play_music (0.95) | バンプオブチキンの天体観測を流して |
| m15333 | social_query | social_query (0.73) | social_query (0.63) | social_query (0.93) | social_query (0.65) | social_post (0.62) | social_post (0.96) | social_query (1.00) | social_query (1.00) | social_query (0.98) | social_query (0.82) | social_query (0.94) | social_post (0.77) | social_query (0.96) | social_post (0.50) | social_query (0.62) | social_query (0.98) | social_post (0.88) | social_query (0.70) | インスタグラムに何か新しいこと |
| m1630 | audio_volume_up | audio_volume_up (0.79) | audio_volume_up (0.93) | audio_volume_up (0.87) | audio_volume_up (0.97) | audio_volume_up (0.98) | audio_volume_up (0.98) | audio_volume_up (0.99) | audio_volume_up (0.99) | audio_volume_up (1.00) | audio_volume_up (0.93) | audio_volume_up (0.96) | audio_volume_up (0.98) | audio_volume_up (0.66) | audio_volume_up (0.92) | audio_volume_up (0.96) | audio_volume_up (0.98) | audio_volume_down (0.88) | audio_volume_up (0.97) | 音楽の音を上げて |
| m9718 | play_audiobook | play_audiobook (0.74) | play_audiobook (0.87) | play_audiobook (0.86) | play_audiobook (0.85) | play_audiobook (0.88) | play_audiobook (0.97) | play_audiobook (0.99) | play_audiobook (0.99) | play_audiobook (0.98) | play_audiobook (0.93) | play_audiobook (0.76) | play_audiobook (0.70) | play_audiobook (0.70) | recommendation_movies (0.10) | play_audiobook (0.35) | play_audiobook (0.95) | play_audiobook (1.00) | play_audiobook (0.85) | 夢をかなえるゾウを再開して |
