# gh-ruff-pr-rework

2026-10-22 · 434 labelled (False 327, True 107) · split: stratified k-fold (131 test cases of the fixed evaluation set held out) · source: Merged PRs of astral-sh/ruff (review history via the GitHub API)

**d1@vercel** has the highest coverage at 95% accuracy, 31% [26, 37] (API cost $0.20 per 10k, p99 1103ms). Its interval overlaps with clef: at this many cases the difference is not shown. Latency not compared (2 with no concurrency recorded; 2 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-ruff-pr-rework --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is clef-flash's, 76% [72, 80].

## Comparison

| model | scored | accuracy | F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 434 | 75.8% [72, 80] | 0.52 | 0.78 | 0.04 | 24% [19, 29] | 91.7% (84.2%) | 0/434 | 0/434 |
| clef-flash | 434 | 76.3% [72, 80] | 0.34 | 0.74 | 0.06 | 15% [11, 19] | 91.3% (81.2%) | 0/434 | 0/434 |
| d1@vercel | 434 | 76.3% [72, 80] | 0.44 | 0.78 | 0.08 | 31% [26, 37] | 92.6% (86.5%) | 0/434 | 0/434 |
| flash-lite@vercel ※ | 434 | 75.1% [71, 79] | 0.14 | 0.53 | 0.25 | 0% [0, 0] | — (0.0%) | 0/434 | 0/434 |
| haiku@vercel ※ | 434 | 75.3% [71, 79] | 0.18 | 0.54 | 0.25 | 0% [0, 0] | — (0.0%) | 0/434 | 0/434 |
| jev | 434 | 74.4% [70, 79] | 0.43 | 0.74 | 0.08 | 16% [12, 21] | 91.8% (82.3%) | 0/434 | 0/434 |
| jev@vercel | 434 | 72.4% [68, 76] | 0.50 | 0.75 | 0.07 | 5% [3, 8] | 87.5% (65.6%) | 0/434 | 0/434 |
| kev@openrouter | 434 | 75.3% [71, 79] | 0.02 | 0.63 | 0.06 | 10% [7, 14] | 93.5% (81.1%) | 0/434 | 0/434 |
| luna@decisions | 434 | 76.0% [72, 80] | 0.53 | 0.78 | 0.04 | 1% [0, 2] | 50.0% (2.5%) | 0/434 | 0/434 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | loss per case (miss 1, false alarm 1) | rule | constraints |
|---|---|---|---|---|
| d1@vercel ◎ | 31% [26, 37] | 0.231 [0.188, 0.281] | 0.97 | met |
| clef | 24% [19, 29] | 0.254 [0.208, 0.304] | 0.89 | met |
| jev | 16% [12, 21] | 0.248 [0.201, 0.300] | 0.76 | met |
| clef-flash | 15% [11, 19] | 0.241 [0.195, 0.294] | 0.93 | met |
| kev@openrouter | 10% [7, 14] | 0.251 [0.201, 0.300] | 0.80 | met |
| jev@vercel | 5% [3, 8] | 0.274 [0.221, 0.324] | 0.81 | met |
| luna@decisions | 1% [0, 2] | 0.224 [0.178, 0.271] | 0.90 | met |
| flash-lite@vercel | 0% [0, 0] | 0.248 [0.201, 0.297] | — | met |
| haiku@vercel | 0% [0, 0] | 0.251 [0.201, 0.304] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 434 | 418 ms | 782 ms | 1266 ms | 1509 ms | 3.0 | not recorded | unknown | $1.34 | estimated |  |
| clef-flash | 434 | 203 ms | 479 ms | 659 ms | 1361 ms | 3.3 | not recorded | unknown | $0.50 | estimated |  |
| d1@vercel | 434 | 498 ms | 632 ms | 1103 ms | 4439 ms | 2.2 | not recorded | unknown | $0.20 | billed | ○ |
| flash-lite@vercel | 434 | 1255 ms | 1597 ms | 2809 ms | 8633 ms | 2.2 | not recorded | unknown | $1.71 | estimated |  |
| haiku@vercel | 434 | 977 ms | 1217 ms | 1821 ms | 7470 ms | 1.9 | not recorded | unknown | $8.08 | estimated |  |
| jev | 434 | 165 ms | 217 ms | 268 ms | 371 ms | 1.6 | not recorded | unknown | $0.32 | estimated | ○ |
| jev@vercel | 434 | 394 ms | 580 ms | 1059 ms | 6396 ms | 2.7 | not recorded | unknown | $0.32 | billed | ○ |
| kev@openrouter | 434 | 1012 ms | 1241 ms | 1685 ms | 2129 ms | 1.7 | not recorded | unknown | $0.19 | billed | ○ |
| luna@decisions | 434 | 258 ms | 306 ms | 2366 ms | 4760 ms | 9.2 | not recorded | unknown | $0.61 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.06 | 27 s (measured, 434 calls) | 10 min | 8 |
| clef-flash | $0.02 | 14 s (measured, 434 calls) | 5 min | 8 |
| jev | $0.01 | 10 s (measured, 434 calls) | 4 min | 8 |
| luna@decisions | $0.03 | 17 s (measured, 434 calls) | 7 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Threshold

The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing 1 and a false alarm 1.

| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold on all data |
|---|---|---|---|---|---|---|
| clef | 75.8% | 77.6% | 55 | 13 | 0.70 | 0.70 |
| clef-flash | 76.3% | 77.9% | 46 | 21 | 0.40 | 0.40 |
| d1@vercel | 76.3% | 79.9% | 53 | 8 | 0.70 | 0.70 |
| flash-lite@vercel | 75.1% | 75.2% | 69 | 6 | 0.50 | 0.50 |
| haiku@vercel | 75.3% | 74.9% | 68 | 8 | 0.50 | 0.50 |
| jev | 74.4% | 77.9% | 48 | 19 | 0.55 | 0.55 |
| jev@vercel | 72.4% | 77.2% | 50 | 19 | 0.60 | 0.60 |
| kev@openrouter | 75.3% | 74.9% | 73 | 3 | 0.45 | 0.45 |
| luna@decisions | 76.0% | 78.2% | 48 | 18 | 0.70 | 0.70 |

## Misses and false alarms by threshold (clef, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 262 (80%) |
| 0.20 | 9 (8%) | 168 (51%) |
| 0.30 | 26 (24%) | 116 (35%) |
| 0.40 | 37 (35%) | 78 (24%) |
| 0.50 | 51 (48%) | 54 (17%) |
| 0.60 | 60 (56%) | 34 (10%) |
| 0.70 | 77 (72%) | 20 (6%) |
| 0.80 | 90 (84%) | 8 (2%) |
| 0.90 | 106 (99%) | 0 (0%) |

## Misses and false alarms by threshold (clef-flash, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 9 (8%) | 216 (66%) |
| 0.20 | 39 (36%) | 100 (31%) |
| 0.30 | 58 (54%) | 52 (16%) |
| 0.40 | 66 (62%) | 29 (9%) |
| 0.50 | 81 (76%) | 22 (7%) |
| 0.60 | 88 (82%) | 9 (3%) |
| 0.70 | 97 (91%) | 4 (1%) |
| 0.80 | 106 (99%) | 1 (0%) |
| 0.90 | 107 (100%) | 0 (0%) |

## Misses and false alarms by threshold (d1@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 19 (18%) | 141 (43%) |
| 0.20 | 31 (29%) | 97 (30%) |
| 0.30 | 41 (38%) | 67 (20%) |
| 0.40 | 57 (53%) | 48 (15%) |
| 0.50 | 67 (63%) | 36 (11%) |
| 0.60 | 74 (69%) | 24 (7%) |
| 0.70 | 78 (73%) | 16 (5%) |
| 0.80 | 88 (82%) | 10 (3%) |
| 0.90 | 103 (96%) | 3 (1%) |

## Misses and false alarms by threshold (flash-lite@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 98 (92%) | 10 (3%) |
| 0.20 | 98 (92%) | 10 (3%) |
| 0.30 | 98 (92%) | 10 (3%) |
| 0.40 | 98 (92%) | 10 (3%) |
| 0.50 | 98 (92%) | 10 (3%) |
| 0.60 | 98 (92%) | 10 (3%) |
| 0.70 | 98 (92%) | 10 (3%) |
| 0.80 | 98 (92%) | 10 (3%) |
| 0.90 | 98 (92%) | 10 (3%) |

## Misses and false alarms by threshold (haiku@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 95 (89%) | 12 (4%) |
| 0.20 | 95 (89%) | 12 (4%) |
| 0.30 | 95 (89%) | 12 (4%) |
| 0.40 | 95 (89%) | 12 (4%) |
| 0.50 | 95 (89%) | 12 (4%) |
| 0.60 | 95 (89%) | 12 (4%) |
| 0.70 | 95 (89%) | 12 (4%) |
| 0.80 | 95 (89%) | 12 (4%) |
| 0.90 | 95 (89%) | 12 (4%) |

## Misses and false alarms by threshold (jev, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 327 (100%) |
| 0.20 | 1 (1%) | 307 (94%) |
| 0.30 | 17 (16%) | 179 (55%) |
| 0.40 | 34 (32%) | 92 (28%) |
| 0.50 | 65 (61%) | 46 (14%) |
| 0.55 | 69 (64%) | 30 (9%) |
| 0.60 | 83 (78%) | 23 (7%) |
| 0.70 | 98 (92%) | 10 (3%) |
| 0.80 | 106 (99%) | 1 (0%) |
| 0.90 | 107 (100%) | 0 (0%) |

## Misses and false alarms by threshold (jev@vercel, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 327 (100%) |
| 0.20 | 0 (0%) | 312 (95%) |
| 0.30 | 10 (9%) | 210 (64%) |
| 0.40 | 26 (24%) | 124 (38%) |
| 0.50 | 48 (45%) | 72 (22%) |
| 0.60 | 72 (67%) | 31 (9%) |
| 0.70 | 90 (84%) | 17 (5%) |
| 0.80 | 105 (98%) | 1 (0%) |
| 0.90 | 107 (100%) | 0 (0%) |

## Misses and false alarms by threshold (kev@openrouter, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 327 (100%) |
| 0.20 | 1 (1%) | 295 (90%) |
| 0.30 | 39 (36%) | 153 (47%) |
| 0.40 | 91 (85%) | 26 (8%) |
| 0.45 | 102 (95%) | 6 (2%) |
| 0.50 | 106 (99%) | 1 (0%) |
| 0.60 | 107 (100%) | 0 (0%) |
| 0.70 | 107 (100%) | 0 (0%) |
| 0.80 | 107 (100%) | 0 (0%) |
| 0.90 | 107 (100%) | 0 (0%) |

## Misses and false alarms by threshold (luna@decisions, each repeat counted)

| threshold | misses | false alarms |
|---|---|---|
| 0.10 | 0 (0%) | 327 (100%) |
| 0.20 | 0 (0%) | 283 (87%) |
| 0.30 | 19 (18%) | 139 (43%) |
| 0.40 | 38 (36%) | 77 (24%) |
| 0.50 | 49 (46%) | 55 (17%) |
| 0.60 | 58 (54%) | 44 (13%) |
| 0.70 | 74 (69%) | 24 (7%) |
| 0.80 | 88 (82%) | 7 (2%) |
| 0.90 | 105 (98%) | 0 (0%) |

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 131 | 78.6% | 13% | 100.0% | 0.130 |
| clef-flash | 131 | 77.1% | 14% | 100.0% | 0.137 |
| d1@vercel | 131 | 74.8% | 21% | 100.0% | 0.206 |
| flash-lite@vercel | 131 | 74.8% | 0% | — | 0.000 |
| haiku@vercel | 131 | 76.3% | 0% | — | 0.000 |
| jev | 131 | 72.5% | 27% | 94.3% | 0.267 |
| jev@vercel | 131 | 71.8% | 5% | 100.0% | 0.053 |
| kev@openrouter | 131 | 76.3% | 7% | 100.0% | 0.069 |
| luna@decisions | 131 | 72.5% | 0% | — | 0.000 |

## Wrong at a high probability (0.9 or more)

**clef-flash** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28027 | True | False | 0.94 | [`flake8-use-pathlib`] Add display-only fix for `os.listdir` (`PTH208… |
| #29076 | True | False | 0.93 | [`flake8-builtins`] Expand checks in class scopes (`A001`) |
| #28743 | True | False | 0.93 | [ty] Remove unnecessary passthrough methods from the `DocumentSnapsho… |
| #28988 | True | False | 0.92 | [ty] Avoid stale I/O diagnostics when closing deleted files |
| #28196 | True | False | 0.92 | [ty] Avoid repeated inference for literal union call results |
| #28087 | True | False | 0.91 | Add a migration guide for categories |
| #27989 | True | False | 0.90 | [ty] Add a benchmark that has all rules enabled |
| #27981 | True | False | 0.90 | [`flake8-implicit-str-concat`] Mark fix unsafe when it creates a docs… |

**d1@vercel** (22)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29076 | True | False | 1.00 | [`flake8-builtins`] Expand checks in class scopes (`A001`) |
| #27989 | True | False | 0.99 | [ty] Add a benchmark that has all rules enabled |
| #28484 | True | False | 0.97 | use scoped token for release workflow |
| #28027 | True | False | 0.97 | [`flake8-use-pathlib`] Add display-only fix for `os.listdir` (`PTH208… |
| #28698 | True | False | 0.97 | [ty] Allow slots to override abstract properties |
| #28796 | True | False | 0.97 | [ty] Preserve intersections of type guard return types |
| #28246 | True | False | 0.96 | [ty] Preserve generic protocol materialization relations |
| #28196 | True | False | 0.96 | [ty] Avoid repeated inference for literal union call results |

**flash-lite@vercel** (108)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29076 | True | False | 1.00 | [`flake8-builtins`] Expand checks in class scopes (`A001`) |
| #28202 | True | False | 1.00 | [ty] Add namespace package support to import completions. |
| #28207 | True | False | 1.00 | [ty] Fix cached classmethods on generic classes |
| #28210 | True | False | 1.00 | Use `cargo insta`, `cargo nextest`, `cargo codspeed` from toolchain |
| #28226 | True | False | 1.00 | [ty] Defer decorator-call diagnostics to avoid recursive-default cycl… |
| #28246 | True | False | 1.00 | [ty] Preserve generic protocol materialization relations |
| #28250 | True | False | 1.00 | [ty] Report deprecated property accessors on intersections |
| #28258 | True | False | 1.00 | [`pyflakes`] Mark the fix as unsafe when it creates a docstring (`F54… |

**haiku@vercel** (107)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29076 | True | False | 1.00 | [`flake8-builtins`] Expand checks in class scopes (`A001`) |
| #28202 | True | False | 1.00 | [ty] Add namespace package support to import completions. |
| #28207 | True | False | 1.00 | [ty] Fix cached classmethods on generic classes |
| #28210 | True | False | 1.00 | Use `cargo insta`, `cargo nextest`, `cargo codspeed` from toolchain |
| #28226 | True | False | 1.00 | [ty] Defer decorator-call diagnostics to avoid recursive-default cycl… |
| #28246 | True | False | 1.00 | [ty] Preserve generic protocol materialization relations |
| #28250 | True | False | 1.00 | [ty] Report deprecated property accessors on intersections |
| #28252 | False | True | 1.00 | [ty] Resolve dependencies within correlated inference alternatives |


## Cases the models disagree on (12 of 166)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #29045 | False | True (0.59) | False (0.83) | False (0.81) | False (1.00) | False (1.00) | False (0.53) | True (0.52) | False (0.69) | False (0.64) | [ty] Minimize timeouts in py-fuzzer |
| #29021 | True | False (0.53) | False (0.81) | False (0.53) | False (1.00) | False (1.00) | True (0.60) | True (0.69) | False (0.62) | False (0.61) | Check script lockfiles in CI |
| #29018 | True | True (0.60) | False (0.70) | False (0.71) | False (1.00) | False (1.00) | False (0.59) | False (0.52) | False (0.62) | False (0.64) | [ty] Fix member lookup on union-bounded type variables |
| #28999 | False | False (0.61) | False (0.76) | True (0.62) | False (1.00) | False (1.00) | False (0.65) | False (0.63) | False (0.75) | False (0.65) | [ty] Report deprecated overloads in decorator applications |
| #28990 | False | False (0.73) | False (0.86) | False (0.93) | False (1.00) | False (1.00) | False (0.65) | False (0.56) | False (0.74) | True (0.51) | [ty] Improve uv metadata diagnostics |
| #28970 | False | False (0.75) | False (0.76) | False (0.71) | False (1.00) | False (1.00) | False (0.52) | True (0.52) | False (0.73) | False (0.65) | [ty] Move ParamSpec signature metadata to extras |
| #28969 | False | False (0.68) | False (0.63) | False (0.89) | False (1.00) | False (1.00) | False (0.51) | True (0.55) | False (0.63) | False (0.66) | [ty] Compact bound-method receivers |
| #28960 | False | False (0.61) | False (0.64) | False (0.82) | False (1.00) | False (1.00) | False (0.63) | False (0.59) | False (0.69) | True (0.60) | [ty] Narrow later match cases after always-true guards |
| #28959 | True | True (0.59) | False (0.82) | False (0.78) | False (1.00) | False (1.00) | True (0.63) | True (0.66) | False (0.59) | True (0.63) | [ty] Explain outdated uv versions in metadata errors |
| #28950 | False | False (0.64) | False (0.83) | False (0.92) | False (1.00) | False (1.00) | False (0.51) | True (0.53) | False (0.69) | False (0.63) | [ty] Skip independent constraint-pair derivation |
| #28949 | False | False (0.66) | False (0.70) | False (0.84) | False (1.00) | False (1.00) | True (0.50) | True (0.54) | False (0.69) | False (0.65) | [ty] Avoid caching empty sequent maps |
| #28936 | False | False (0.93) | False (0.87) | False (0.98) | False (1.00) | False (1.00) | False (0.54) | True (0.52) | False (0.64) | False (0.78) | [ty] Skip caching trivially assignable types |
