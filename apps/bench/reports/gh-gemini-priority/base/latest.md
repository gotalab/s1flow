# gh-gemini-priority

2026-10-22 · 300 labelled (priority/p2 146, priority/p1 92, priority/p3 62) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**flash-lite@vercel** has the highest accuracy (all), 58% [51, 64] (API cost $1.62 per 10k, p99 4018ms). Its interval overlaps with jev@vercel, jev, clef-flash, luna@decisions, clef, haiku@vercel: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **jev@vercel** (API cost $0.30 per 10k, p99 2382ms). Latency not compared (7 with no concurrency recorded; 7 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-priority --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is flash-lite@vercel's, 60% [55, 66].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 55.3% [50, 61] | 0.58 | 0.80 | 0.11 | 2% [0, 4] | 100.0% (47.3%) | 0/300 | 0/300 |
| clef-flash | 300 | 46.0% [40, 52] | 0.45 | 0.76 | 0.20 | 0% [0, 1] | 100.0% (5.0%) | 0/300 | 0/300 |
| d1@vercel | 300 | 42.7% [37, 48] | 0.40 | 0.75 | 0.20 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| flash-lite@vercel ※ | 300 | 60.0% [55, 66] | 0.62 | 0.71 | 0.40 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| haiku@vercel ※ | 300 | 56.3% [51, 62] | 0.59 | 0.70 | 0.44 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev | 300 | 50.3% [45, 56] | 0.52 | 0.75 | 0.23 | 1% [0, 3] | 66.7% (13.5%) | 0/300 | 0/300 |
| jev@vercel | 300 | 52.3% [47, 58] | 0.55 | 0.75 | 0.26 | 3% [1, 5] | 100.0% (60.7%) | 0/300 | 0/300 |
| kev@openrouter | 300 | 43.0% [38, 48] | 0.43 | 0.71 | 0.11 | 1% [0, 3] | 66.7% (13.5%) | 0/300 | 0/300 |
| luna@decisions | 300 | 56.7% [51, 62] | 0.58 | 0.77 | 0.25 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| jev@vercel ◎ | 51% [44, 58] | — | met |
| jev | 49% [42, 56] | — | met |
| clef-flash | 46% [39, 53] | — | met |
| luna@decisions | 55% [48, 62] | — | met |
| clef | 55% [48, 61] | — | met |
| flash-lite@vercel | 58% [51, 64] | — | met |
| haiku@vercel | 53% [46, 60] | — | met |
| kev@openrouter | 42% [35, 50] | — | met |
| d1@vercel | 42% [36, 49] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 402 ms | 662 ms | 975 ms | 1116 ms | 2.4 | not recorded | unknown | $1.28 | estimated |  |
| clef-flash | 300 | 232 ms | 512 ms | 699 ms | 4296 ms | 3.0 | not recorded | unknown | $0.48 | estimated |  |
| d1@vercel | 300 | 545 ms | 903 ms | 2956 ms | 3645 ms | 5.4 | not recorded | unknown | $0.17 | billed | ○ |
| flash-lite@vercel | 300 | 1261 ms | 1580 ms | 4018 ms | 7101 ms | 3.2 | not recorded | unknown | $1.62 | estimated | ○ |
| haiku@vercel | 300 | 1056 ms | 1323 ms | 3325 ms | 4021 ms | 3.1 | not recorded | unknown | $7.71 | estimated |  |
| jev | 300 | 148 ms | 228 ms | 278 ms | 351 ms | 1.9 | not recorded | unknown | $0.30 | estimated | ○ |
| jev@vercel | 300 | 535 ms | 820 ms | 2382 ms | 2818 ms | 4.5 | not recorded | unknown | $0.30 | billed | ○ |
| kev@openrouter | 300 | 953 ms | 1217 ms | 4016 ms | 4018 ms | 4.2 | not recorded | unknown | $0.17 | billed | ○ |
| luna@decisions | 300 | 257 ms | 291 ms | 331 ms | 515 ms | 1.3 | not recorded | unknown | $0.50 | estimated | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.04 | 17 s (measured, 300 calls) | 9 min | 8 |
| clef-flash | $0.01 | 11 s (measured, 300 calls) | 6 min | 8 |
| jev | $0.0091 | 7 s (measured, 300 calls) | 4 min | 8 |
| luna@decisions | $0.01 | 10 s (measured, 300 calls) | 6 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 90 | 56.7% | 1% | 100.0% | 0.567 |
| clef-flash | 90 | 45.6% | 2% | 100.0% | 0.456 |
| d1@vercel | 90 | 43.3% | 0% | — | 0.433 |
| flash-lite@vercel | 90 | 65.6% | 0% | — | 0.656 |
| haiku@vercel | 90 | 64.4% | 0% | — | 0.644 |
| jev | 90 | 53.3% | 2% | 100.0% | 0.533 |
| jev@vercel | 90 | 55.6% | 4% | 100.0% | 0.556 |
| kev@openrouter | 90 | 44.4% | 0% | — | 0.444 |
| luna@decisions | 90 | 60.0% | 0% | — | 0.600 |

## Wrong at a high probability (0.9 or more)

**d1@vercel** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28395 | priority/p2 | priority/p1 | 0.96 | Blocking Synchronous I/O on the Main Thread Causes UI Stutter |

**flash-lite@vercel** (120)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28593 | priority/p3 | priority/p1 | 1.00 | Среда автономной разработки оптимизации тестирования  через ИИ агенто… |
| #28600 | priority/p2 | priority/p1 | 1.00 | 404 errors for gemini-3.1pro-preview |
| #28605 | priority/p2 | priority/p1 | 1.00 | Nightly Release Failed for  on 2026-07-31 |
| #28620 | priority/p1 | priority/p2 | 1.00 | formatTruncatedToolOutput: negative maxChars silently inflates output… |
| #28621 | priority/p2 | priority/p1 | 1.00 | [Bug] Model generates a synthetic next user turn instead of answering… |
| #28625 | priority/p2 | priority/p1 | 1.00 | Enterprise Gemini CLI users were promised access to the latest models… |
| #28579 | priority/p2 | priority/p1 | 1.00 | bug(core): 400 Bad Request: "Function call is missing a thought_signa… |
| #28575 | priority/p2 | priority/p1 | 1.00 | CLI crashes on startup when GEMINI_API_KEY contains special characters |

**haiku@vercel** (131)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28600 | priority/p2 | priority/p1 | 1.00 | 404 errors for gemini-3.1pro-preview |
| #28605 | priority/p2 | priority/p1 | 1.00 | Nightly Release Failed for  on 2026-07-31 |
| #28621 | priority/p2 | priority/p1 | 1.00 | [Bug] Model generates a synthetic next user turn instead of answering… |
| #28625 | priority/p2 | priority/p1 | 1.00 | Enterprise Gemini CLI users were promised access to the latest models… |
| #28579 | priority/p2 | priority/p1 | 1.00 | bug(core): 400 Bad Request: "Function call is missing a thought_signa… |
| #28537 | priority/p1 | priority/p2 | 1.00 | Possible bug |
| #28550 | priority/p2 | priority/p1 | 1.00 | Heap OOM in non-interactive runs: ignore-matcher (path-scurry + minim… |
| #28553 | priority/p2 | priority/p3 | 1.00 | VNN LOGICLAB |

**jev** (28)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28263 | priority/p2 | priority/p1 | 0.98 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |
| #29306 | priority/p2 | priority/p1 | 0.98 | bug(core): external safety checker inherits full env and unbounded st… |
| #28841 | priority/p2 | priority/p3 | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29305 | priority/p2 | priority/p1 | 0.97 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29001 | priority/p2 | priority/p1 | 0.97 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29202 | priority/p2 | priority/p1 | 0.96 | Policy bypass: shell-wrapper flags skip inner command re-check |
| #29146 | priority/p2 | priority/p3 | 0.96 | GeminiCLI.com Feedback: [ISSUE] |
| #29073 | priority/p2 | priority/p1 | 0.96 | bug(a2a-server): express.json() mounted after A2A SDK routes breaks J… |

**jev@vercel** (42)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29306 | priority/p2 | priority/p1 | 0.99 | bug(core): external safety checker inherits full env and unbounded st… |
| #28841 | priority/p2 | priority/p3 | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28550 | priority/p2 | priority/p1 | 0.99 | Heap OOM in non-interactive runs: ignore-matcher (path-scurry + minim… |
| #28448 | priority/p1 | priority/p3 | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28263 | priority/p2 | priority/p1 | 0.99 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |
| #29146 | priority/p2 | priority/p3 | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29145 | priority/p2 | priority/p3 | 0.99 | Recalibrate trick |
| #28571 | priority/p2 | priority/p3 | 0.98 | Open Copilot в VS Code  codespace  |

**luna@decisions** (44)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29306 | priority/p2 | priority/p1 | 1.00 | bug(core): external safety checker inherits full env and unbounded st… |
| #29405 | priority/p2 | priority/p1 | 1.00 | [Bug Report] Background tasks enter indefinite 'Forever Running' hang… |
| #29202 | priority/p2 | priority/p1 | 1.00 | Policy bypass: shell-wrapper flags skip inner command re-check |
| #28395 | priority/p2 | priority/p1 | 1.00 | Blocking Synchronous I/O on the Main Thread Causes UI Stutter |
| #28259 | priority/p2 | priority/p3 | 1.00 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #29007 | priority/p2 | priority/p1 | 1.00 | Docs: env var redaction section uses setting keys that do not exist |
| #29305 | priority/p2 | priority/p1 | 0.99 | bug(core): client-initiated tool calls silently bypass ASK_USER confi… |
| #29073 | priority/p2 | priority/p1 | 0.99 | bug(a2a-server): express.json() mounted after A2A SDK routes breaks J… |


## Cases the models disagree on (12 of 186)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #29610 | priority/p2 | priority/p2 (0.46) | priority/p3 (0.49) | priority/p1 (0.54) | priority/p2 (1.00) | priority/p2 (1.00) | priority/p2 (0.47) | priority/p2 (0.54) | priority/p2 (0.37) | priority/p2 (0.73) | Gemini CLI extension gallery has not indexed suhaib81/url-shortener-b… |
| #29605 | priority/p3 | priority/p3 (0.77) | priority/p3 (0.41) | priority/p1 (0.59) | priority/p3 (1.00) | priority/p2 (1.00) | priority/p3 (0.66) | priority/p3 (0.65) | priority/p3 (0.35) | priority/p3 (0.64) | Pull request 29482 is waiting for a review |
| #29600 | priority/p3 | priority/p3 (0.56) | priority/p3 (0.50) | priority/p1 (0.51) | priority/p3 (1.00) | priority/p3 (1.00) | priority/p2 (0.54) | priority/p2 (0.65) | priority/p2 (0.38) | priority/p2 (0.52) | bug(cli): formatDuration shows "1000ms" and "60.0s" just below a unit… |
| #29526 | priority/p2 | priority/p1 (0.58) | priority/p1 (0.63) | priority/p1 (0.58) | priority/p2 (1.00) | priority/p1 (1.00) | priority/p1 (0.86) | priority/p1 (0.94) | priority/p1 (0.48) | priority/p1 (0.87) | MCP tool answering in `structuredContent` is a success with an empty … |
| #29524 | priority/p2 | priority/p1 (0.68) | priority/p1 (0.78) | priority/p1 (0.67) | priority/p1 (1.00) | priority/p1 (1.00) | priority/p1 (0.70) | priority/p1 (0.58) | priority/p1 (0.48) | priority/p2 (0.60) | Paid Google AI account showing “not eligible” in Antigravity |
| #29514 | priority/p3 | priority/p3 (0.71) | priority/p1 (0.45) | priority/p1 (0.50) | priority/p3 (1.00) | priority/p3 (1.00) | priority/p3 (0.52) | priority/p2 (0.58) | priority/p2 (0.41) | priority/p2 (0.58) | cache-transcript-turn-indexes |
| #29513 | priority/p3 | priority/p3 (0.52) | priority/p1 (0.39) | priority/p1 (0.57) | priority/p2 (1.00) | priority/p2 (1.00) | priority/p2 (0.59) | priority/p2 (0.70) | priority/p1 (0.55) | priority/p2 (0.60) | linearize-state-snapshot-id-lookups |
| #29504 | priority/p2 | priority/p1 (0.70) | priority/p1 (0.76) | priority/p1 (0.61) | priority/p2 (1.00) | priority/p1 (1.00) | priority/p1 (0.84) | priority/p1 (0.89) | priority/p1 (0.55) | priority/p1 (0.65) | TUI hides 400/429 spend cap error behind 'high demand' infinite loop … |
| #29478 | priority/p3 | priority/p2 (0.43) | priority/p2 (0.38) | priority/p1 (0.48) | priority/p2 (1.00) | priority/p2 (1.00) | priority/p2 (0.39) | priority/p1 (0.43) | priority/p2 (0.46) | priority/p3 (0.61) | Feature Request: Add PkgDiet dependency guardrail skill |
| #29464 | priority/p2 | priority/p2 (0.41) | priority/p3 (0.39) | priority/p3 (0.44) | priority/p3 (1.00) | priority/p3 (1.00) | priority/p3 (0.79) | priority/p3 (0.79) | priority/p3 (0.43) | priority/p3 (0.93) | Overthinking and overtime consuming |
| #29453 | priority/p3 | priority/p3 (0.46) | priority/p3 (0.56) | priority/p2 (0.37) | priority/p3 (1.00) | priority/p3 (1.00) | priority/p3 (0.92) | priority/p3 (0.94) | priority/p2 (0.44) | priority/p3 (1.00) | Feature Request: Add interactive file path autocomplete (tab-completi… |
| #29417 | priority/p2 | priority/p1 (0.53) | priority/p1 (0.62) | priority/p1 (0.71) | priority/p2 (1.00) | priority/p1 (1.00) | priority/p1 (0.79) | priority/p1 (0.82) | priority/p1 (0.60) | priority/p1 (0.99) | bug(core): explicit `--model gemini-3-pro-preview` silently rewritten… |
