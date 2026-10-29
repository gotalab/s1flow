# gh-gemini-pr-rework

2026-10-22 · 483 labelled (False 353, True 130) · split: stratified k-fold (145 test cases of the fixed evaluation set held out) · source: Merged PRs of google-gemini/gemini-cli (review history via the GitHub API)

**clef** has the highest coverage at 95% accuracy, 6% [4, 8] (API cost $1.54 per 10k, p99 1192ms). Its interval overlaps with d1@vercel: at this many cases the difference is not shown. Of those, compared by loss per case (miss 1, false alarm 1), then API cost, **d1@vercel** is chosen (API cost $0.24 per 10k, p99 2303ms). Latency not compared (2 with no concurrency recorded; 2 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-pr-rework --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is flash-lite@vercel's, 75% [71, 78].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 483 | 70.6% [66, 74] | 0.47 | 0.72 | 0.06 | 6% [4, 8] | 85.0% (65.6%) | 0/483 | 0/483 |
| clef-flash | 483 | 73.9% [70, 78] | 0.14 | 0.71 | 0.13 | 1% [0, 3] | 75.0% (24.9%) | 0/483 | 0/483 |
| d1@vercel | 483 | 73.5% [70, 77] | 0.40 | 0.70 | 0.13 | 3% [1, 5] | 72.7% (43.6%) | 0/483 | 0/483 |
| flash-lite@vercel ※ | 483 | 74.5% [71, 78] | 0.26 | 0.56 | 0.25 | 0% [0, 0] | — (0.0%) | 0/483 | 0/483 |
| haiku@vercel ※ | 483 | 72.0% [68, 76] | 0.17 | 0.53 | 0.28 | 0% [0, 0] | — (0.0%) | 0/483 | 0/483 |
| jev | 483 | 71.0% [67, 75] | 0.47 | 0.71 | 0.06 | 1% [0, 2] | 75.0% (24.9%) | 0/483 | 0/483 |
| jev@vercel | 483 | 67.1% [63, 71] | 0.46 | 0.71 | 0.05 | 1% [0, 3] | 80.0% (34.3%) | 0/483 | 0/483 |
| kev@openrouter | 483 | 73.5% [70, 77] | 0.07 | 0.64 | 0.03 | 2% [1, 3] | 100.0% (60.7%) | 0/483 | 0/483 |
| luna@decisions | 483 | 67.5% [63, 72] | 0.46 | 0.72 | 0.07 | 0% [0, 1] | 0.0% (0.0%) | 0/483 | 0/483 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 1, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| d1@vercel ◎ | 3% [1, 5] | 0.269 [0.222, 0.320] | 1.00 | met |
| clef | 6% [4, 8] | 0.302 [0.254, 0.355] | 0.96 | met |
| kev@openrouter | 2% [1, 3] | 0.269 [0.222, 0.314] | 0.87 | met |
| jev@vercel | 1% [0, 3] | 0.320 [0.272, 0.370] | 0.84 | met |
| clef-flash | 1% [0, 3] | 0.266 [0.222, 0.314] | 0.96 | met |
| jev | 1% [0, 2] | 0.284 [0.240, 0.331] | 0.85 | met |
| luna@decisions | 0% [0, 1] | 0.320 [0.272, 0.370] | — | met |
| flash-lite@vercel | 0% [0, 0] | 0.249 [0.204, 0.290] | — | met |
| haiku@vercel | 0% [0, 0] | 0.272 [0.228, 0.317] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 483 | 406 ms | 666 ms | 1192 ms | 1648 ms | 2.9 | not recorded | unknown | $1.54 | estimated | ○ |
| clef-flash | 483 | 186 ms | 376 ms | 549 ms | 603 ms | 2.9 | not recorded | unknown | $0.58 | estimated | ○ |
| d1@vercel | 483 | 562 ms | 984 ms | 2303 ms | 6268 ms | 4.1 | not recorded | unknown | $0.24 | billed | ○ |
| flash-lite@vercel | 483 | 1230 ms | 1626 ms | 3938 ms | 8725 ms | 3.2 | not recorded | unknown | $1.96 | estimated |  |
| haiku@vercel | 483 | 1044 ms | 1429 ms | 3164 ms | 8426 ms | 3.0 | not recorded | unknown | $9.16 | estimated |  |
| jev | 483 | 164 ms | 238 ms | 911 ms | 1162 ms | 5.6 | not recorded | unknown | $0.36 | estimated | ○ |
| jev@vercel | 483 | 532 ms | 940 ms | 1618 ms | 6901 ms | 3.0 | not recorded | unknown | $0.36 | billed | ○ |
| kev@openrouter | 483 | 1049 ms | 1495 ms | 3352 ms | 4711 ms | 3.2 | not recorded | unknown | $0.22 | billed | ○ |
| luna@decisions | 483 | 258 ms | 304 ms | 479 ms | 562 ms | 1.9 | not recorded | unknown | $0.69 | estimated | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.07 | 28 s (measured, 483 calls) | 10 min | 8 |
| clef-flash | $0.03 | 14 s (measured, 483 calls) | 5 min | 8 |
| jev | $0.02 | 13 s (measured, 483 calls) | 4 min | 8 |
| luna@decisions | $0.03 | 16 s (measured, 483 calls) | 6 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold on all data |
|---|---|---|---|---|---|---|
| clef | 70.6% | 74.6% | 72 | 14 | 0.80 | 0.80 |
| clef-flash | 73.9% | 74.6% | 75 | 11 | 0.40 | 0.40 |
| d1@vercel | 73.5% | 72.8% | 72 | 20 | 0.70 | 0.70 |
| flash-lite@vercel | 74.5% | 75.1% | 73 | 11 | 0.50 | 0.50 |
| haiku@vercel | 72.0% | 72.8% | 79 | 13 | 0.50 | 0.50 |
| jev | 71.0% | 72.2% | 70 | 24 | 0.55 | 0.55 |
| jev@vercel | 67.1% | 71.6% | 71 | 25 | 0.60 | 0.60 |
| kev@openrouter | 73.5% | 72.8% | 85 | 7 | 0.40 | 0.40 |
| luna@decisions | 67.5% | 76.6% | 64 | 15 | 0.75 | 0.75 |

## Misses and false alarms by threshold (clef, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 5 (4%) | 278 (79%) |
| 0.20 | 28 (22%) | 190 (54%) |
| 0.30 | 42 (32%) | 129 (37%) |
| 0.40 | 56 (43%) | 103 (29%) |
| 0.50 | 67 (52%) | 75 (21%) |
| 0.60 | 79 (61%) | 49 (14%) |
| 0.70 | 88 (68%) | 32 (9%) |
| 0.80 | 105 (81%) | 10 (3%) |
| 0.90 | 127 (98%) | 1 (0%) |

## Misses and false alarms by threshold (clef-flash, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 36 (28%) | 145 (41%) |
| 0.20 | 86 (66%) | 43 (12%) |
| 0.30 | 96 (74%) | 23 (7%) |
| 0.40 | 109 (84%) | 8 (2%) |
| 0.50 | 120 (92%) | 6 (2%) |
| 0.60 | 122 (94%) | 3 (1%) |
| 0.70 | 128 (98%) | 2 (1%) |
| 0.80 | 129 (99%) | 0 (0%) |
| 0.90 | 130 (100%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 38 (29%) | 151 (43%) |
| 0.20 | 58 (45%) | 104 (29%) |
| 0.30 | 70 (54%) | 66 (19%) |
| 0.40 | 79 (61%) | 54 (15%) |
| 0.50 | 87 (67%) | 41 (12%) |
| 0.60 | 97 (75%) | 30 (8%) |
| 0.70 | 99 (76%) | 18 (5%) |
| 0.80 | 113 (87%) | 12 (3%) |
| 0.90 | 124 (95%) | 5 (1%) |

## Misses and false alarms by threshold (flash-lite@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 108 (83%) | 15 (4%) |
| 0.20 | 108 (83%) | 15 (4%) |
| 0.30 | 108 (83%) | 15 (4%) |
| 0.40 | 108 (83%) | 15 (4%) |
| 0.50 | 108 (83%) | 15 (4%) |
| 0.60 | 108 (83%) | 15 (4%) |
| 0.70 | 108 (83%) | 15 (4%) |
| 0.80 | 108 (83%) | 15 (4%) |
| 0.90 | 108 (83%) | 15 (4%) |

## Misses and false alarms by threshold (haiku@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 116 (89%) | 19 (5%) |
| 0.20 | 116 (89%) | 19 (5%) |
| 0.30 | 116 (89%) | 19 (5%) |
| 0.40 | 116 (89%) | 19 (5%) |
| 0.50 | 116 (89%) | 19 (5%) |
| 0.60 | 116 (89%) | 19 (5%) |
| 0.70 | 116 (89%) | 19 (5%) |
| 0.80 | 116 (89%) | 19 (5%) |
| 0.90 | 116 (89%) | 19 (5%) |

## Misses and false alarms by threshold (jev, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 353 (100%) |
| 0.20 | 1 (1%) | 338 (96%) |
| 0.30 | 10 (8%) | 243 (69%) |
| 0.40 | 40 (31%) | 145 (41%) |
| 0.50 | 69 (53%) | 71 (20%) |
| 0.55 | 76 (58%) | 49 (14%) |
| 0.60 | 89 (68%) | 36 (10%) |
| 0.70 | 113 (87%) | 12 (3%) |
| 0.80 | 129 (99%) | 1 (0%) |
| 0.90 | 130 (100%) | 0 (0%) |

## Misses and false alarms by threshold (jev@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 353 (100%) |
| 0.20 | 0 (0%) | 344 (97%) |
| 0.30 | 4 (3%) | 272 (77%) |
| 0.40 | 29 (22%) | 183 (52%) |
| 0.50 | 62 (48%) | 97 (27%) |
| 0.60 | 77 (59%) | 50 (14%) |
| 0.70 | 108 (83%) | 21 (6%) |
| 0.80 | 126 (97%) | 2 (1%) |
| 0.90 | 130 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 350 (99%) |
| 0.20 | 17 (13%) | 240 (68%) |
| 0.30 | 81 (62%) | 75 (21%) |
| 0.40 | 115 (88%) | 15 (4%) |
| 0.50 | 125 (96%) | 3 (1%) |
| 0.60 | 129 (99%) | 1 (0%) |
| 0.70 | 130 (100%) | 0 (0%) |
| 0.80 | 130 (100%) | 0 (0%) |
| 0.90 | 130 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 353 (100%) |
| 0.20 | 2 (2%) | 326 (92%) |
| 0.30 | 17 (13%) | 198 (56%) |
| 0.40 | 53 (41%) | 110 (31%) |
| 0.50 | 64 (49%) | 93 (26%) |
| 0.60 | 68 (52%) | 69 (20%) |
| 0.70 | 82 (63%) | 33 (9%) |
| 0.75 | 91 (70%) | 21 (6%) |
| 0.80 | 108 (83%) | 10 (3%) |
| 0.90 | 129 (99%) | 1 (0%) |

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 145 | 72.4% | 1% | 100.0% | 0.014 |
| clef-flash | 145 | 75.2% | 3% | 100.0% | 0.034 |
| d1@vercel | 145 | 74.5% | 1% | 100.0% | 0.014 |
| flash-lite@vercel | 145 | 73.1% | 0% | — | 0.000 |
| haiku@vercel | 145 | 70.3% | 0% | — | 0.000 |
| jev | 145 | 69.7% | 1% | 100.0% | 0.007 |
| jev@vercel | 145 | 64.8% | 1% | 100.0% | 0.007 |
| kev@openrouter | 145 | 74.5% | 3% | 100.0% | 0.034 |
| luna@decisions | 145 | 66.2% | 0% | — | 0.000 |

## Wrong at a high probability (0.9 or more)

**clef** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #29185 | True | False | 0.94 | test(integration): deflake run_shell_command and file-system-interact… |
| #26991 | True | False | 0.92 | fix(ui): clamped table column widths |
| #26073 | False | True | 0.91 | Fix bulk of remaining issues with generalist profile |
| #26949 | True | False | 0.90 | fix(ci): configure git remote with token for authentication |
| #26217 | True | False | 0.90 | test(cleanup): fix temporary directory leaks in test suites |

**clef-flash** (36)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26991 | True | False | 0.96 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.96 | fix(core): update auth error documentation link to valid anchor and a… |
| #25822 | True | False | 0.96 | fix(cli): add missing response key to custom theme text schema |
| #28216 | True | False | 0.95 | Refactor: exclude transient CI configuration files from workspace con… |
| #28940 | True | False | 0.94 | fix(a2a-server): clear stale cancellation error on new message turns |
| #29528 | True | False | 0.94 | fix(cli): propagate resolved folder trust state in headless mode (#29… |
| #27467 | True | False | 0.94 | fix(core): handle multi-line escaped quotes in stripShellWrapper |
| #27391 | True | False | 0.94 | fix(cli): filter internal session context from history during resumpt… |

**d1@vercel** (43)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26270 | True | False | 1.00 | feat(ui): added microphone and updated placeholder for voice mode |
| #25822 | True | False | 1.00 | fix(cli): add missing response key to custom theme text schema |
| #26991 | True | False | 1.00 | fix(ui): clamped table column widths |
| #29377 | True | False | 0.99 | fix(core): update auth error documentation link to valid anchor and a… |
| #28216 | True | False | 0.99 | Refactor: exclude transient CI configuration files from workspace con… |
| #25324 | True | False | 0.99 | fix(cli): prevent spam loop when preferredEditor is invalid |
| #26234 | True | False | 0.99 | Allow non-https proxy urls to support container environments |
| #25753 | True | False | 0.99 | test(e2e): default integration tests to Flash Preview |

**flash-lite@vercel** (123)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26462 | True | False | 1.00 | ci(release): build and attach unsigned macOS binaries to releases |
| #26475 | False | True | 1.00 | fix(ci): respect exempt labels when closing stale items |
| #26479 | True | False | 1.00 | fix(a2a-server): resolve tool approval race condition and improve sta… |
| #26442 | True | False | 1.00 | feat(cli): improve /agents refresh logging |
| #26284 | True | False | 1.00 | feat(ui): added wave animation for voice mode |
| #26290 | False | True | 1.00 | Add Star History section to README |
| #26312 | True | False | 1.00 | fix(core): refresh MCP OAuth token usage after re-auth |
| #26565 | True | False | 1.00 | fix(core): prevent isBinary false-positive on Windows PTY streams |

**haiku@vercel** (135)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26479 | True | False | 1.00 | fix(a2a-server): resolve tool approval race condition and improve sta… |
| #26442 | True | False | 1.00 | feat(cli): improve /agents refresh logging |
| #26284 | True | False | 1.00 | feat(ui): added wave animation for voice mode |
| #26312 | True | False | 1.00 | fix(core): refresh MCP OAuth token usage after re-auth |
| #26333 | False | True | 1.00 | fix(cli): enable daemon relaunch in binary and bundle keytar |
| #26565 | True | False | 1.00 | fix(core): prevent isBinary false-positive on Windows PTY streams |
| #26868 | True | False | 1.00 | fix: add system PATH fallback for ripgrep resolution (#26777) |
| #26888 | True | False | 1.00 | feat(context): Introduce adaptive token calculator to more accurately… |

**luna@decisions** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26073 | False | True | 0.93 | Fix bulk of remaining issues with generalist profile |


## Cases the models disagree on (12 of 205)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #29581 | False | False (0.60) | False (0.89) | False (0.69) | False (1.00) | False (1.00) | False (0.62) | False (0.59) | False (0.77) | True (0.52) | fix(cli): resolve @file:line references and prevent ghost text wrap h… |
| #29580 | False | True (0.66) | False (0.73) | True (0.87) | False (1.00) | False (1.00) | True (0.57) | True (0.60) | False (0.67) | True (0.76) | fix(acp): resolve session by exact id and handle listener cleanup on … |
| #29568 | True | True (0.83) | False (0.64) | True (0.88) | False (1.00) | False (1.00) | True (0.73) | True (0.75) | False (0.66) | True (0.85) | fix(core): implement append-only delta patching and bounded history w… |
| #29560 | False | True (0.61) | False (0.89) | False (0.89) | False (1.00) | False (1.00) | False (0.64) | False (0.62) | False (0.74) | True (0.54) | fix(ui): ensure Windows ConPTY forwards IME cursor position |
| #29520 | False | True (0.68) | False (0.82) | False (0.58) | False (1.00) | False (1.00) | True (0.51) | True (0.58) | False (0.68) | True (0.71) | fix(cli): preserve scroll position and partition pending height budget |
| #29506 | True | True (0.84) | False (0.65) | True (0.84) | False (1.00) | False (1.00) | True (0.62) | True (0.63) | False (0.69) | True (0.77) | fix(core): align policy redirection gates, path validation, and workf… |
| #29502 | False | True (0.54) | False (0.82) | False (0.64) | False (1.00) | False (1.00) | False (0.55) | True (0.53) | False (0.64) | True (0.62) | fix(cli): ensure Enter and Spacebar reliably confirm selection list o… |
| #29499 | True | True (0.81) | False (0.70) | True (0.59) | False (1.00) | False (1.00) | True (0.58) | True (0.62) | False (0.72) | True (0.74) | fix(core): serialize file tool operations and make writes atomic (#29… |
| #29451 | True | True (0.80) | False (0.62) | True (0.88) | False (1.00) | False (1.00) | True (0.69) | True (0.71) | False (0.68) | True (0.75) | fix(core): bound tool output size and optimize memory lifecycle in lo… |
| #29450 | False | True (0.79) | False (0.58) | True (0.93) | False (1.00) | False (1.00) | True (0.63) | True (0.66) | False (0.67) | True (0.78) | refactor(a2a-server): implement V1 to V2 settings migration logic |
| #29448 | False | True (0.78) | False (0.64) | True (0.53) | False (1.00) | False (1.00) | True (0.59) | True (0.66) | False (0.71) | True (0.79) | fix(auth): prevent infinite auth loop from file contention, headless … |
| #29443 | True | True (0.86) | True (0.66) | True (0.89) | False (1.00) | False (1.00) | True (0.71) | True (0.71) | False (0.65) | True (0.85) | Feat/gemini 3.8 flash 3.5 flash lite |
