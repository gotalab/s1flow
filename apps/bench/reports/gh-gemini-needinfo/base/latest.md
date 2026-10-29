# gh-gemini-needinfo

2026-10-22 · 300 labelled (False 236, True 64) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**clef-flash** has the highest accuracy (all), 80% [75, 86] (API cost $0.54 per 10k, p99 511ms). Its interval overlaps with kev@openrouter, d1@vercel, jev@vercel, jev, luna@decisions, clef, flash-lite@vercel, haiku@vercel: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **kev@openrouter** (API cost $0.20 per 10k, p99 4101ms). Latency not compared (9 with no concurrency recorded; 9 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-needinfo --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is kev@openrouter's, 78% [73, 82].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 77.3% [73, 82] | 0.36 | 0.60 | 0.15 | 3% [1, 5] | 66.7% (27.1%) | 0/300 | 0/300 |
| clef-flash | 300 | 76.0% [71, 81] | 0.36 | 0.60 | 0.10 | 4% [1, 7] | 75.0% (40.0%) | 0/300 | 0/300 |
| d1@vercel | 300 | 74.3% [70, 79] | 0.35 | 0.61 | 0.18 | 3% [1, 5] | 83.3% (41.8%) | 0/300 | 0/300 |
| flash-lite@vercel ※ | 300 | 77.0% [72, 82] | 0.37 | 0.60 | 0.23 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| haiku@vercel ※ | 300 | 76.7% [72, 81] | 0.39 | 0.61 | 0.23 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev | 300 | 71.3% [66, 76] | 0.35 | 0.61 | 0.14 | 1% [0, 2] | 0.0% (0.0%) | 0/300 | 0/300 |
| jev@vercel | 300 | 69.7% [64, 75] | 0.35 | 0.61 | 0.17 | 1% [0, 3] | 33.3% (1.7%) | 0/300 | 0/300 |
| kev@openrouter | 300 | 77.7% [73, 82] | 0.31 | 0.61 | 0.05 | 0% [0, 1] | 0.0% (0.0%) | 0/300 | 0/300 |
| luna@decisions | 300 | 72.7% [68, 77] | 0.33 | 0.61 | 0.18 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| kev@openrouter ◎ | 80% [74, 85] | 0.70 | met |
| d1@vercel | 77% [72, 82] | 0.95 | met |
| jev@vercel | 78% [72, 83] | 0.95 | met |
| jev | 77% [71, 82] | 0.75 | met |
| clef-flash | 80% [75, 86] | 0.85 | met |
| luna@decisions | 77% [72, 82] | 0.90 | met |
| clef | 80% [75, 85] | 0.85 | met |
| flash-lite@vercel | 78% [72, 83] | 0.50 | met |
| haiku@vercel | 77% [71, 82] | 0.50 | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 406 ms | 674 ms | 1103 ms | 1421 ms | 2.7 | not recorded | unknown | $1.44 | estimated |  |
| clef-flash | 300 | 154 ms | 301 ms | 511 ms | 545 ms | 3.3 | not recorded | unknown | $0.54 | estimated | ○ |
| d1@vercel | 300 | 666 ms | 1203 ms | 2571 ms | 4897 ms | 3.9 | not recorded | unknown | $0.21 | billed | ○ |
| flash-lite@vercel | 300 | 1300 ms | 1828 ms | 4198 ms | 8832 ms | 3.2 | not recorded | unknown | $1.73 | estimated |  |
| haiku@vercel | 300 | 1110 ms | 1484 ms | 4161 ms | 7989 ms | 3.8 | not recorded | unknown | $8.17 | estimated |  |
| jev | 300 | 165 ms | 208 ms | 238 ms | 306 ms | 1.4 | not recorded | unknown | $0.33 | estimated | ○ |
| jev@vercel | 300 | 592 ms | 1146 ms | 2816 ms | 4722 ms | 4.8 | not recorded | unknown | $0.33 | billed | ○ |
| kev@openrouter | 300 | 1004 ms | 1427 ms | 4101 ms | 4133 ms | 4.1 | not recorded | unknown | $0.20 | billed | ○ |
| luna@decisions | 300 | 258 ms | 302 ms | 518 ms | 724 ms | 2.0 | not recorded | unknown | $0.63 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.04 | 17 s (measured, 300 calls) | 9 min | 8 |
| clef-flash | $0.02 | 7 s (measured, 300 calls) | 4 min | 8 |
| jev | $0.0098 | 7 s (measured, 300 calls) | 4 min | 8 |
| luna@decisions | $0.02 | 10 s (measured, 300 calls) | 6 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold on all data |
|---|---|---|---|---|---|---|
| clef | 77.3% | 80.0% | 35 | 7 | 0.85 | 0.85 |
| clef-flash | 76.0% | 80.5% | 34 | 7 | 0.85 | 0.85 |
| d1@vercel | 74.3% | 77.1% | 36 | 12 | 0.95 | 0.95 |
| flash-lite@vercel | 77.0% | 77.6% | 31 | 16 | 0.50 | 0.50 |
| haiku@vercel | 76.7% | 77.1% | 30 | 18 | 0.50 | 0.50 |
| jev | 71.3% | 76.7% | 34 | 15 | 0.85 | 0.75 |
| jev@vercel | 69.7% | 77.6% | 34 | 13 | 0.95 | 0.95 |
| kev@openrouter | 77.7% | 79.5% | 36 | 7 | 0.70 | 0.70 |
| luna@decisions | 72.7% | 77.1% | 34 | 14 | 0.90 | 0.90 |

## Misses and false alarms by threshold (clef)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 42 (66%) | 59 (25%) |
| 0.20 | 42 (66%) | 38 (16%) |
| 0.30 | 43 (67%) | 29 (12%) |
| 0.40 | 43 (67%) | 25 (11%) |
| 0.50 | 45 (70%) | 23 (10%) |
| 0.60 | 47 (73%) | 21 (9%) |
| 0.70 | 48 (75%) | 14 (6%) |
| 0.80 | 50 (78%) | 8 (3%) |
| 0.85 | 50 (78%) | 6 (3%) |
| 0.90 | 52 (81%) | 5 (2%) |

## Misses and false alarms by threshold (clef-flash)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 25 (39%) | 144 (61%) |
| 0.20 | 39 (61%) | 57 (24%) |
| 0.30 | 42 (66%) | 44 (19%) |
| 0.40 | 43 (67%) | 34 (14%) |
| 0.50 | 44 (69%) | 28 (12%) |
| 0.60 | 45 (70%) | 23 (10%) |
| 0.70 | 47 (73%) | 19 (8%) |
| 0.80 | 50 (78%) | 12 (5%) |
| 0.85 | 51 (80%) | 7 (3%) |
| 0.90 | 58 (91%) | 5 (2%) |

## Misses and false alarms by threshold (d1@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 30 (47%) | 89 (38%) |
| 0.20 | 38 (59%) | 68 (29%) |
| 0.30 | 40 (62%) | 55 (23%) |
| 0.40 | 41 (64%) | 42 (18%) |
| 0.50 | 43 (67%) | 34 (14%) |
| 0.60 | 43 (67%) | 26 (11%) |
| 0.70 | 44 (69%) | 25 (11%) |
| 0.80 | 45 (70%) | 20 (8%) |
| 0.90 | 49 (77%) | 15 (6%) |
| 0.95 | 53 (83%) | 11 (5%) |

## Misses and false alarms by threshold (flash-lite@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 44 (69%) | 25 (11%) |
| 0.20 | 44 (69%) | 25 (11%) |
| 0.30 | 44 (69%) | 25 (11%) |
| 0.40 | 44 (69%) | 25 (11%) |
| 0.50 | 44 (69%) | 25 (11%) |
| 0.60 | 44 (69%) | 25 (11%) |
| 0.70 | 44 (69%) | 25 (11%) |
| 0.80 | 44 (69%) | 25 (11%) |
| 0.90 | 44 (69%) | 25 (11%) |

## Misses and false alarms by threshold (haiku@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 42 (66%) | 28 (12%) |
| 0.20 | 42 (66%) | 28 (12%) |
| 0.30 | 42 (66%) | 28 (12%) |
| 0.40 | 42 (66%) | 28 (12%) |
| 0.50 | 42 (66%) | 28 (12%) |
| 0.60 | 42 (66%) | 28 (12%) |
| 0.70 | 42 (66%) | 28 (12%) |
| 0.80 | 42 (66%) | 28 (12%) |
| 0.90 | 42 (66%) | 28 (12%) |

## Misses and false alarms by threshold (jev)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 6 (9%) | 187 (79%) |
| 0.20 | 29 (45%) | 110 (47%) |
| 0.30 | 37 (58%) | 80 (34%) |
| 0.40 | 39 (61%) | 58 (25%) |
| 0.50 | 41 (64%) | 45 (19%) |
| 0.60 | 42 (66%) | 38 (16%) |
| 0.70 | 42 (66%) | 33 (14%) |
| 0.75 | 42 (66%) | 26 (11%) |
| 0.80 | 44 (69%) | 25 (11%) |
| 0.90 | 45 (70%) | 20 (8%) |

## Misses and false alarms by threshold (jev@vercel)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 4 (6%) | 193 (82%) |
| 0.20 | 27 (42%) | 108 (46%) |
| 0.30 | 34 (53%) | 90 (38%) |
| 0.40 | 39 (61%) | 69 (29%) |
| 0.50 | 40 (62%) | 51 (22%) |
| 0.60 | 40 (62%) | 41 (17%) |
| 0.70 | 42 (66%) | 40 (17%) |
| 0.80 | 43 (67%) | 28 (12%) |
| 0.90 | 47 (73%) | 21 (9%) |
| 0.95 | 50 (78%) | 12 (5%) |

## Misses and false alarms by threshold (kev@openrouter)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 4 (6%) | 220 (93%) |
| 0.20 | 30 (47%) | 99 (42%) |
| 0.30 | 41 (64%) | 50 (21%) |
| 0.40 | 46 (72%) | 30 (13%) |
| 0.50 | 49 (77%) | 18 (8%) |
| 0.60 | 53 (83%) | 12 (5%) |
| 0.70 | 54 (84%) | 3 (1%) |
| 0.80 | 59 (92%) | 2 (1%) |
| 0.90 | 62 (97%) | 1 (0%) |

## Misses and false alarms by threshold (luna@decisions)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 26 (41%) | 114 (48%) |
| 0.20 | 39 (61%) | 65 (28%) |
| 0.30 | 42 (66%) | 51 (22%) |
| 0.40 | 42 (66%) | 41 (17%) |
| 0.50 | 44 (69%) | 38 (16%) |
| 0.60 | 46 (72%) | 35 (15%) |
| 0.70 | 47 (73%) | 31 (13%) |
| 0.80 | 47 (73%) | 26 (11%) |
| 0.90 | 49 (77%) | 18 (8%) |

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 90 | 75.6% | 1% | 100.0% | 0.822 |
| clef-flash | 90 | 73.3% | 0% | — | 0.811 |
| d1@vercel | 90 | 73.3% | 1% | 100.0% | 0.778 |
| flash-lite@vercel | 90 | 75.6% | 0% | — | 0.756 |
| haiku@vercel | 90 | 75.6% | 0% | — | 0.756 |
| jev | 90 | 71.1% | 0% | — | 0.756 |
| jev@vercel | 90 | 66.7% | 0% | — | 0.811 |
| kev@openrouter | 90 | 74.4% | 0% | — | 0.811 |
| luna@decisions | 90 | 66.7% | 0% | — | 0.756 |

## Wrong at a high probability (0.9 or more)

**clef** (47)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 0.98 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #28846 | True | False | 0.98 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29316 | True | False | 0.98 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #28761 | True | False | 0.97 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29012 | True | False | 0.97 | Docs: six CLI flags missing from the reference table |
| #29290 | True | False | 0.97 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29306 | True | False | 0.97 | bug(core): external safety checker inherits full env and unbounded st… |
| #29133 | True | False | 0.97 | Bug: --list-sessions never marks the current session, so --delete-ses… |

**clef-flash** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 0.94 | Docs: six CLI flags missing from the reference table |
| #29424 | True | False | 0.94 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #28713 | True | False | 0.93 | Caretaker agent completion |
| #28761 | True | False | 0.93 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29290 | True | False | 0.93 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29144 | True | False | 0.93 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29204 | True | False | 0.92 | MCP prompt responses are submitted as JSON-encoded text |
| #28846 | True | False | 0.92 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |

**d1@vercel** (45)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29388 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29390 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29424 | True | False | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #28846 | True | False | 1.00 | OAuth personal on 0.46.0 fails with UNSUPPORTED_CLIENT and Antigravit… |
| #29311 | True | False | 1.00 | bug(core): insecure user/workspace policy dirs skip permission checks… |
| #29391 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29392 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |

**flash-lite@vercel** (69)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29033 | True | False | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29001 | True | False | 1.00 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29080 | True | False | 1.00 | perf(core): chat history O(n^2) re-serialization on every turn causes… |
| #29100 | False | True | 1.00 | Gemini lolo |
| #29107 | False | True | 1.00 | "The caller does not have permission  #25306 - still persists |
| #29111 | False | True | 1.00 | ejecucion lenta |

**haiku@vercel** (70)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29033 | True | False | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29001 | True | False | 1.00 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29012 | True | False | 1.00 | Docs: six CLI flags missing from the reference table |
| #29046 | True | False | 1.00 | bug(cli): impure state updater in useInputHistoryStore schedules nest… |
| #29080 | True | False | 1.00 | perf(core): chat history O(n^2) re-serialization on every turn causes… |
| #29100 | False | True | 1.00 | Gemini lolo |
| #29107 | False | True | 1.00 | "The caller does not have permission  #25306 - still persists |
| #29111 | False | True | 1.00 | ejecucion lenta |

**jev** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29100 | False | True | 0.98 | Gemini lolo |
| #28783 | False | True | 0.98 | cutealexamartha |
| #29147 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29228 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29220 | False | True | 0.97 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #29146 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29390 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] Post-analysis helper uses a stale imp… |
| #29391 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |

**jev@vercel** (29)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29147 | False | True | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29100 | False | True | 0.98 | Gemini lolo |
| #29391 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29392 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] Generated files change automated exte… |
| #29220 | False | True | 0.97 | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
| #28783 | False | True | 0.97 | cutealexamartha |
| #29146 | False | True | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29355 | False | True | 0.96 | GeminiCLI.com Feedback: [ISSUE] |

**kev@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | True | False | 0.94 | Docs: six CLI flags missing from the reference table |
| #29316 | True | False | 0.93 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29317 | True | False | 0.91 | bug(a2a-server): logger ignores LOG_LEVEL and logs request bodies wit… |
| #29147 | False | True | 0.91 | GeminiCLI.com Feedback: [ISSUE] |
| #29306 | True | False | 0.90 | bug(core): external safety checker inherits full env and unbounded st… |

**luna@decisions** (47)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29144 | True | False | 1.00 | sanitizeToolArgs redacts non-secret keys like max_tokens and author v… |
| #29290 | True | False | 1.00 | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29146 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29308 | True | False | 1.00 | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
| #29316 | True | False | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29207 | True | False | 1.00 | Corrupt agents.json (valid JSON, wrong shape) crashes acknowledgment |
| #29147 | False | True | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29355 | False | True | 0.99 | GeminiCLI.com Feedback: [ISSUE] |


## Cases the models disagree on (12 of 58)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #29594 | False | False (0.95) | False (0.75) | False (0.61) | False (1.00) | False (1.00) | False (0.59) | True (0.52) | False (0.79) | False (0.71) | bug(tools): GoogleSearch tool hangs indefinitely in "Thinking..." sta… |
| #29576 | False | False (0.92) | False (0.75) | False (0.62) | False (1.00) | False (1.00) | True (0.50) | True (0.59) | False (0.63) | False (0.83) | Appeal submitted but TOS_VIOLATION suspension persists (request for p… |
| #29555 | False | True (0.65) | True (0.56) | True (0.59) | True (1.00) | True (1.00) | True (0.87) | True (0.85) | False (0.62) | True (0.79) | Unresponsive / Performance Issue |
| #29533 | False | True (0.81) | True (0.68) | True (0.90) | True (1.00) | True (1.00) | True (0.95) | True (0.94) | False (0.51) | True (0.91) | As a user i can't transfer money to others |
| #29529 | False | True (0.74) | True (0.72) | True (0.99) | True (1.00) | True (1.00) | True (0.94) | True (0.94) | False (0.52) | True (0.90) | error you do not have a valid license of this product |
| #29524 | True | False (0.93) | False (0.85) | True (0.65) | False (1.00) | False (1.00) | True (0.57) | True (0.67) | False (0.75) | False (0.74) | Paid Google AI account showing “not eligible” in Antigravity |
| #29504 | False | False (0.87) | False (0.78) | False (0.77) | False (1.00) | False (1.00) | True (0.74) | True (0.76) | False (0.63) | False (0.68) | TUI hides 400/429 spend cap error behind 'high demand' infinite loop … |
| #29500 | False | False (0.81) | True (0.55) | True (0.75) | True (1.00) | False (1.00) | True (0.90) | True (0.90) | False (0.81) | True (0.84) | Docs: typo in README installation section |
| #29430 | False | False (0.69) | False (0.64) | True (0.71) | False (1.00) | True (1.00) | True (0.73) | True (0.80) | False (0.67) | True (0.62) | Access Blocked: Authorization Error |
| #29416 | False | False (0.75) | True (0.62) | True (0.65) | False (1.00) | False (1.00) | True (0.70) | True (0.78) | True (0.52) | True (0.93) | gemini --help exits with code 5 after winget install on Windows 11 |
| #29414 | False | False (0.62) | False (0.83) | True (0.53) | False (1.00) | False (1.00) | False (0.68) | False (0.71) | False (0.76) | True (0.98) | Issue classifier pipeline verification probe |
| #29410 | False | False (0.71) | False (0.68) | True (0.82) | False (1.00) | False (1.00) | True (0.70) | True (0.73) | False (0.76) | False (0.77) | resume latest reopens most recently started session, not most recentl… |
