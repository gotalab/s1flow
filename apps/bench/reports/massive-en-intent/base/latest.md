# massive-en-intent

2026-10-22 · 288 labelled (datetime_convert 5, email_addcontact 5, play_podcasts 5, qa_definition 5, transport_ticket 5, takeaway_order 5, social_post 5, play_audiobook 5, more) · split: stratified k-fold (87 test cases of the fixed evaluation set held out) · source: MASSIVE 1.1 en-US test（Amazon, CC BY 4.0）、massive-ja-intent と同じ 288 件

**clef-flash** has the highest accuracy (all), 90% [85, 94] (API cost $1.26 per 10k, p99 852ms). Its interval overlaps with d1@vercel, jev, luna@decisions, clef: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **d1@vercel** (API cost $0.16 per 10k, p99 807ms). Latency not compared (5 with no concurrency recorded; 5 with no retries recorded): measure every candidate again at one concurrency, s1flow run massive-en-intent --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is clef-flash's, 90% [87, 94].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 288 | 88.9% [85, 93] | 0.87 | 1.00 | 0.03 | 82% [77, 88] | 95.2% (91.4%) | 0/288 | 0/288 |
| clef-flash | 288 | 90.3% [87, 94] | 0.89 | 1.00 | 0.03 | 87% [82, 91] | 94.3% (90.4%) | 0/288 | 0/288 |
| d1@vercel | 288 | 86.5% [83, 91] | 0.86 | 0.99 | 0.05 | 67% [61, 74] | 93.3% (88.7%) | 0/288 | 0/288 |
| jev | 288 | 86.1% [82, 90] | 0.85 | 0.98 | 0.07 | 69% [63, 75] | 94.9% (90.7%) | 0/288 | 0/288 |
| luna@decisions | 288 | 84.7% [80, 89] | 0.84 | 0.98 | 0.06 | 73% [66, 79] | 95.2% (91.2%) | 0/288 | 0/288 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; jev = jev-1.14.0 (also jev-1.13.0); luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| d1@vercel ◎ | 86% [81, 91] | — | met |
| jev | 87% [82, 91] | — | met |
| luna@decisions | 85% [79, 90] | — | met |
| clef-flash | 90% [85, 94] | — | met |
| clef | 89% [85, 93] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 288 | 520 ms | 787 ms | 1282 ms | 1605 ms | 2.5 | not recorded | unknown | $3.36 | estimated |  |
| clef-flash | 288 | 258 ms | 522 ms | 852 ms | 1095 ms | 3.3 | not recorded | unknown | $1.26 | estimated | ○ |
| d1@vercel | 288 | 494 ms | 601 ms | 807 ms | 1085 ms | 1.6 | not recorded | unknown | $0.16 | billed | ○ |
| jev | 288 | 163 ms | 224 ms | 273 ms | 440 ms | 1.7 | not recorded | unknown | $0.56 | estimated | ○ |
| luna@decisions | 288 | 272 ms | 403 ms | 3361 ms | 3440 ms | 12.3 | not recorded | unknown | $0.76 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.10 | 20 s (measured, 288 calls) | 12 min | 8 |
| clef-flash | $0.04 | 12 s (measured, 288 calls) | 7 min | 8 |
| d1@vercel | $0.0047 | 18 s (measured, 288 calls) | 10 min | 8 |
| jev | $0.02 | 7 s (measured, 288 calls) | 4 min | 8 |
| luna@decisions | $0.02 | 14 s (measured, 288 calls) | 8 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 87 | 88.5% | 82% | 97.2% | 0.885 |
| clef-flash | 87 | 92.0% | 91% | 93.7% | 0.920 |
| d1@vercel | 87 | 88.5% | 68% | 96.6% | 0.885 |
| jev | 87 | 85.1% | 70% | 96.7% | 0.851 |
| luna@decisions | 87 | 85.1% | 79% | 95.7% | 0.851 |

## Wrong at a high probability (0.9 or more)

**clef** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 0.96 | what is the best chocolate chip cookies recipe |
| m16781 | email_addcontact | email_sendemail | 0.91 | add this email address to my contacts and send an email to |
| m8978 | calendar_set | calendar_query | 0.90 | just let me know the important meetings with my boss over the week |
| m15203 | social_query | news_query | 0.90 | new updates |

**clef-flash** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 0.96 | what is the best chocolate chip cookies recipe |
| m4166 | audio_volume_other | audio_volume_up | 0.96 | change volume level to maximum |
| m286 | iot_hue_lighton | iot_hue_lightup | 0.94 | light up the lights in the kitchen |
| m8978 | calendar_set | calendar_query | 0.94 | just let me know the important meetings with my boss over the week |
| m16225 | email_addcontact | email_querycontact | 0.93 | open contacts |
| m12800 | transport_query | recommendation_locations | 0.93 | where is the public library |
| m50 | datetime_convert | datetime_query | 0.92 | olly tell me the time in g. m. t. plus five |
| m13984 | qa_definition | general_quirky | 0.91 | consequences to actions |

**d1@vercel** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m8978 | calendar_set | calendar_query | 0.99 | just let me know the important meetings with my boss over the week |
| m5911 | music_settings | play_music | 0.98 | replay the musics |
| m8322 | general_quirky | recommendation_events | 0.98 | i want to know more about the fair this weekend |
| m13242 | general_quirky | cooking_recipe | 0.97 | what is the best chocolate chip cookies recipe |
| m4268 | music_settings | play_music | 0.96 | move to the next song in the list |
| m12800 | transport_query | recommendation_locations | 0.95 | where is the public library |
| m5812 | audio_volume_other | music_settings | 0.94 | set the default audio setting |
| m4166 | audio_volume_other | audio_volume_up | 0.94 | change volume level to maximum |

**jev** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 1.00 | what is the best chocolate chip cookies recipe |
| m8978 | calendar_set | calendar_query | 1.00 | just let me know the important meetings with my boss over the week |
| m5911 | music_settings | play_music | 1.00 | replay the musics |
| m4268 | music_settings | play_music | 0.96 | move to the next song in the list |
| m2165 | takeaway_query | cooking_query | 0.94 | is dinner ready yet |
| m16353 | email_query | email_querycontact | 0.93 | check for emails from steve |
| m15203 | social_query | news_query | 0.91 | new updates |
| m8322 | general_quirky | recommendation_events | 0.90 | i want to know more about the fair this weekend |

**luna@decisions** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| m13242 | general_quirky | cooking_recipe | 1.00 | what is the best chocolate chip cookies recipe |
| m2165 | takeaway_query | cooking_query | 1.00 | is dinner ready yet |
| m8978 | calendar_set | calendar_query | 1.00 | just let me know the important meetings with my boss over the week |
| m10931 | lists_query | music_query | 0.99 | what is on my playlist |
| m15203 | social_query | news_query | 0.99 | new updates |
| m50 | datetime_convert | datetime_query | 0.97 | olly tell me the time in g. m. t. plus five |
| m12800 | transport_query | recommendation_locations | 0.93 | where is the public library |
| m5911 | music_settings | play_music | 0.93 | replay the musics |


## Cases the models disagree on (12 of 57)

| id | label | clef | clef-flash | d1@vercel | jev | luna@decisions | case |
|---|---|---|---|---|---|---|---|
| m16353 | email_query | email_query (0.97) | email_query (0.97) | email_query (1.00) | email_querycontact (0.93) | email_query (1.00) | check for emails from steve |
| m5911 | music_settings | music_settings (0.73) | music_settings (0.70) | play_music (0.98) | play_music (1.00) | play_music (0.93) | replay the musics |
| m16317 | email_query | email_query (0.97) | email_query (0.97) | email_query (1.00) | email_querycontact (0.87) | email_query (1.00) | did i get new emails from sarah |
| m31 | iot_cleaning | iot_hue_lightoff (0.43) | iot_cleaning (0.94) | iot_cleaning (1.00) | iot_cleaning (1.00) | iot_cleaning (0.99) | hoover the hallway |
| m5812 | audio_volume_other | audio_volume_other (0.81) | audio_volume_other (0.79) | music_settings (0.94) | music_settings (0.90) | audio_volume_other (0.99) | set the default audio setting |
| m5149 | iot_coffee | iot_coffee (0.96) | iot_coffee (0.95) | iot_coffee (0.98) | iot_coffee (0.90) | iot_wemo_on (0.50) | set the coffee maker to on |
| m15565 | social_post | social_post (0.98) | social_post (0.94) | general_quirky (0.86) | email_sendemail (0.63) | social_post (0.42) | can you let delta know i'm never using them again |
| m12436 | transport_query | transport_traffic (0.63) | transport_query (0.79) | transport_query (0.83) | transport_query (0.72) | transport_query (0.98) | how long will it take to get to the airport |
| m8322 | general_quirky | recommendation_events (0.77) | calendar_query (0.86) | recommendation_events (0.98) | recommendation_events (0.90) | recommendation_events (0.93) | i want to know more about the fair this weekend |
| m10093 | cooking_recipe | cooking_recipe (0.96) | cooking_recipe (0.97) | cooking_recipe (0.91) | cooking_recipe (0.93) | cooking_query (0.76) | how is lasagne made |
| m7232 | calendar_query | calendar_query (0.70) | calendar_query (0.94) | recommendation_events (0.65) | calendar_query (0.87) | calendar_query (0.97) | what are the events next week |
| m50 | datetime_convert | datetime_query (0.75) | datetime_query (0.92) | datetime_query (0.76) | datetime_convert (0.65) | datetime_query (0.97) | olly tell me the time in g. m. t. plus five |
