# gh-gemini-area

2026-10-22 · 300 labelled (area/core 93, area/agent 84, area/security 41, area/extensions 20, area/documentation 18, area/enterprise 18, area/platform 13, area/non-interactive 13) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**flash-lite@vercel** has the highest accuracy (all), 60% [53, 67] (API cost $2.13 per 10k, p99 6400ms). Its interval overlaps with kev@openrouter, d1@vercel, jev@vercel, jev, luna@decisions, clef-flash, clef, haiku@vercel: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **kev@openrouter** (API cost $0.24 per 10k, p99 5884ms). Latency not compared (9 with no concurrency recorded; 9 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-area --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is clef's, 60% [54, 66].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 60.0% [54, 66] | 0.56 | 0.89 | 0.12 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| clef-flash | 300 | 52.7% [47, 58] | 0.50 | 0.84 | 0.15 | 1% [0, 2] | 50.0% (2.5%) | 0/300 | 0/300 |
| d1@vercel | 300 | 50.7% [45, 56] | 0.46 | 0.84 | 0.18 | 1% [0, 2] | 50.0% (2.5%) | 0/300 | 0/300 |
| flash-lite@vercel ※ | 300 | 58.7% [53, 64] | 0.53 | 0.74 | 0.41 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| haiku@vercel ※ | 300 | 56.0% [50, 61] | 0.54 | 0.75 | 0.44 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev | 300 | 52.3% [47, 58] | 0.49 | 0.87 | 0.27 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev@vercel | 300 | 54.3% [49, 60] | 0.52 | 0.86 | 0.25 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| kev@openrouter | 300 | 51.0% [45, 57] | 0.46 | 0.86 | 0.08 | 1% [0, 3] | 66.7% (13.5%) | 0/300 | 0/300 |
| luna@decisions | 300 | 57.3% [52, 63] | 0.53 | 0.81 | 0.26 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| kev@openrouter ◎ | 52% [45, 59] | — | met |
| d1@vercel | 50% [43, 57] | — | met |
| jev@vercel | 55% [48, 62] | — | met |
| jev | 53% [46, 60] | — | met |
| luna@decisions | 59% [51, 66] | — | met |
| clef-flash | 52% [44, 59] | — | met |
| clef | 60% [52, 66] | — | met |
| flash-lite@vercel | 60% [53, 67] | — | met |
| haiku@vercel | 57% [50, 64] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 435 ms | 712 ms | 1068 ms | 1329 ms | 2.5 | not recorded | unknown | $1.86 | estimated | ○ |
| clef-flash | 300 | 247 ms | 502 ms | 667 ms | 789 ms | 2.7 | not recorded | unknown | $0.70 | estimated |  |
| d1@vercel | 300 | 718 ms | 1262 ms | 4423 ms | 4466 ms | 6.2 | not recorded | unknown | $0.24 | billed | ○ |
| flash-lite@vercel | 300 | 1307 ms | 1778 ms | 6400 ms | 7987 ms | 4.9 | not recorded | unknown | $2.13 | estimated | ○ |
| haiku@vercel | 300 | 1150 ms | 1495 ms | 5961 ms | 5984 ms | 5.2 | not recorded | unknown | $10.04 | estimated |  |
| jev | 300 | 163 ms | 218 ms | 239 ms | 636 ms | 1.5 | not recorded | unknown | $0.39 | estimated | ○ |
| jev@vercel | 300 | 628 ms | 1217 ms | 4802 ms | 8333 ms | 7.6 | not recorded | unknown | $0.39 | billed | ○ |
| kev@openrouter | 300 | 1005 ms | 1494 ms | 5884 ms | 5903 ms | 5.9 | not recorded | unknown | $0.24 | billed | ○ |
| luna@decisions | 300 | 257 ms | 386 ms | 606 ms | 1025 ms | 2.4 | not recorded | unknown | $0.68 | estimated | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.06 | 18 s (measured, 300 calls) | 10 min | 8 |
| clef-flash | $0.02 | 11 s (measured, 300 calls) | 6 min | 8 |
| jev | $0.01 | 7 s (measured, 300 calls) | 4 min | 8 |
| luna@decisions | $0.02 | 11 s (measured, 300 calls) | 6 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 90 | 60.0% | 0% | — | 0.600 |
| clef-flash | 90 | 54.4% | 0% | — | 0.544 |
| d1@vercel | 90 | 52.2% | 0% | — | 0.522 |
| flash-lite@vercel | 90 | 54.4% | 0% | — | 0.544 |
| haiku@vercel | 90 | 53.3% | 0% | — | 0.533 |
| jev | 90 | 51.1% | 0% | — | 0.511 |
| jev@vercel | 90 | 52.2% | 0% | — | 0.522 |
| kev@openrouter | 90 | 48.9% | 0% | — | 0.489 |
| luna@decisions | 90 | 54.4% | 0% | — | 0.544 |

## Wrong at a high probability (0.9 or more)

**clef** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29033 | area/platform | area/extensions | 0.98 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29012 | area/core | area/documentation | 0.98 | Docs: six CLI flags missing from the reference table |
| #28841 | area/core | area/documentation | 0.96 | GeminiCLI.com Feedback: [ISSUE] |
| #29316 | area/agent | area/non-interactive | 0.95 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29555 | area/core | area/extensions | 0.95 | Unresponsive / Performance Issue |
| #29001 | area/extensions | area/security | 0.94 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29064 | area/platform | area/enterprise | 0.93 | Gemini 2.5 Pro quota stuck at 100% / limit reached for several days |
| #29415 | area/agent | area/core | 0.91 | gemini --help exits with code 5 after winget install on Windows 11 |

**clef-flash** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | area/core | area/documentation | 0.99 | Docs: six CLI flags missing from the reference table |
| #29001 | area/extensions | area/security | 0.98 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29021 | area/core | area/agent | 0.95 | ask_user tool should retain question in chat history for human contex… |
| #29078 | area/core | area/agent | 0.95 | bug(tools): concurrent file writes suffer lost-update race (no atomic… |
| #29033 | area/platform | area/extensions | 0.94 | bug: extension update rollback copies an empty temp dir - restores no… |
| #28841 | area/core | area/documentation | 0.93 | GeminiCLI.com Feedback: [ISSUE] |
| #28692 | area/non-interactive | area/platform | 0.92 | Nightly Release Failed for v0.55.0-nightly.20260805.gac42fb0a2 on 202… |
| #28675 | area/non-interactive | area/platform | 0.91 | Nightly Release Failed for v0.55.0-nightly.20260804.gac42fb0a2 on 202… |

**d1@vercel** (19)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29078 | area/core | area/agent | 1.00 | bug(tools): concurrent file writes suffer lost-update race (no atomic… |
| #29012 | area/core | area/documentation | 0.99 | Docs: six CLI flags missing from the reference table |
| #28841 | area/core | area/documentation | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29045 | area/core | area/agent | 0.99 | bug: read-many-files treats substring overlap as 'explicitly requeste… |
| #29033 | area/platform | area/extensions | 0.98 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29064 | area/platform | area/enterprise | 0.98 | Gemini 2.5 Pro quota stuck at 100% / limit reached for several days |
| #29130 | area/core | area/agent | 0.97 | fix(core): getDiffContextSnippet produces full-file diff on CRLF line… |
| #29574 | area/core | area/agent | 0.96 | bug(core): 400 Bad Request "Requests ending with a model turn are not… |

**flash-lite@vercel** (124)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | area/core | area/documentation | 1.00 | Docs: six CLI flags missing from the reference table |
| #29021 | area/core | area/agent | 1.00 | ask_user tool should retain question in chat history for human contex… |
| #29025 | area/agent | area/core | 1.00 | bug: auto-compression summarizer failure aborts the entire user turn … |
| #29026 | area/agent | area/core | 1.00 | bug: context-management history dedupe silently drops consecutive ide… |
| #29027 | area/agent | area/core | 1.00 | bug: mid-stream retry backoff is not abort-aware and retries content … |
| #29031 | area/core | area/security | 1.00 | bug: headless mode reports an untrusted folder as trusted to the rest… |
| #29033 | area/platform | area/extensions | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29028 | area/agent | area/core | 1.00 | bug: abort-time history rollback becomes a silent no-op after mid-pro… |

**haiku@vercel** (132)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | area/core | area/documentation | 1.00 | Docs: six CLI flags missing from the reference table |
| #29021 | area/core | area/agent | 1.00 | ask_user tool should retain question in chat history for human contex… |
| #29025 | area/agent | area/core | 1.00 | bug: auto-compression summarizer failure aborts the entire user turn … |
| #29026 | area/agent | area/core | 1.00 | bug: context-management history dedupe silently drops consecutive ide… |
| #29027 | area/agent | area/core | 1.00 | bug: mid-stream retry backoff is not abort-aware and retries content … |
| #29029 | area/agent | area/core | 1.00 | bug: MCP progress events publish NaN/negative progressPercent to the … |
| #29030 | area/agent | area/core | 1.00 | bug: CoreToolScheduler.dispose() leaves queued schedule() callers pen… |
| #29033 | area/platform | area/extensions | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |

**jev** (26)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28841 | area/core | area/documentation | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29001 | area/extensions | area/security | 1.00 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29033 | area/platform | area/extensions | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29012 | area/core | area/documentation | 1.00 | Docs: six CLI flags missing from the reference table |
| #29417 | area/agent | area/core | 0.99 | bug(core): explicit `--model gemini-3-pro-preview` silently rewritten… |
| #28912 | area/agent | area/enterprise | 0.99 | You do not have a valid license of this product. |
| #29316 | area/agent | area/non-interactive | 0.99 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #28826 | area/agent | area/core | 0.97 | Workspace scan warns when projects.json.lock disappears normally |

**jev@vercel** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | area/agent | area/non-interactive | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #28841 | area/core | area/documentation | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29033 | area/platform | area/extensions | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29012 | area/core | area/documentation | 1.00 | Docs: six CLI flags missing from the reference table |
| #29001 | area/extensions | area/security | 1.00 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #28692 | area/non-interactive | area/platform | 0.99 | Nightly Release Failed for v0.55.0-nightly.20260805.gac42fb0a2 on 202… |
| #29417 | area/agent | area/core | 0.99 | bug(core): explicit `--model gemini-3-pro-preview` silently rewritten… |
| #28675 | area/non-interactive | area/platform | 0.99 | Nightly Release Failed for v0.55.0-nightly.20260804.gac42fb0a2 on 202… |

**luna@decisions** (52)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29033 | area/platform | area/extensions | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29012 | area/core | area/documentation | 1.00 | Docs: six CLI flags missing from the reference table |
| #29001 | area/extensions | area/security | 1.00 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29417 | area/agent | area/core | 1.00 | bug(core): explicit `--model gemini-3-pro-preview` silently rewritten… |
| #29424 | area/agent | area/core | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #28929 | area/documentation | area/core | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29316 | area/agent | area/non-interactive | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29174 | area/non-interactive | area/platform | 1.00 | Nightly Release Failed for  on 2026-09-03 |


## Cases the models disagree on (12 of 183)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #29614 | area/core | area/core (0.68) | area/non-interactive (0.56) | area/non-interactive (0.49) | area/core (1.00) | area/core (1.00) | area/core (0.73) | area/core (0.71) | area/core (0.37) | area/core (0.90) | [Windows] Hardcoded GIT_CONFIG_GLOBAL=NUL causes Git for Windows to f… |
| #29602 | area/core | area/core (0.81) | area/core (0.75) | area/agent (0.37) | area/core (1.00) | area/core (1.00) | area/core (1.00) | area/core (1.00) | area/core (0.56) | area/core (0.87) | bug(core): GEMINI_CLI_CUSTOM_HEADERS splits header values that contai… |
| #29598 | area/platform | area/platform (0.88) | area/platform (0.78) | area/platform (0.75) | area/platform (1.00) | area/platform (1.00) | area/platform (0.79) | area/platform (0.93) | area/non-interactive (0.53) | area/non-interactive (0.57) | Nightly evals: summary job reads green when no eval reports exist |
| #29595 | area/non-interactive | area/non-interactive (0.34) | area/security (0.48) | area/security (0.47) | area/security (1.00) | area/security (1.00) | area/security (0.65) | area/security (0.80) | area/security (0.32) | area/non-interactive (0.84) | ACP: an MCP tool permission request doesn't say which server or tool … |
| #29592 | area/core | area/core (0.66) | area/core (0.87) | area/non-interactive (0.55) | area/core (1.00) | area/core (1.00) | area/core (0.76) | area/core (0.72) | area/core (0.52) | area/core (0.85) | macOS PTY master leak persists in 0.62.0 after completed shell comman… |
| #29591 | area/core | area/agent (0.57) | area/agent (0.60) | area/agent (0.80) | area/core (1.00) | area/core (1.00) | area/agent (0.86) | area/agent (0.65) | area/core (0.28) | area/agent (0.69) | ⚠  High memory usage detected: 7.28 GB. If you experience a crash, pl… |
| #29589 | area/core | area/agent (0.52) | area/core (0.54) | area/agent (0.92) | area/core (1.00) | area/core (1.00) | area/core (0.85) | area/core (0.82) | area/core (0.51) | area/core (0.50) | bug(core): stripToolCallIdPrefixes drops functionResponse.parts, so i… |
| #29579 | area/security | area/security (0.81) | area/agent (0.40) | area/agent (0.71) | area/security (1.00) | area/security (1.00) | area/core (0.60) | area/core (0.52) | area/core (0.43) | area/security (0.42) | bug(core): massive false positives with "Untrusted Command Flags Dete… |
| #29576 | area/security | area/enterprise (0.58) | area/core (0.37) | area/enterprise (0.40) | area/enterprise (1.00) | area/security (1.00) | area/enterprise (0.71) | area/enterprise (0.58) | area/non-interactive (0.22) | area/enterprise (0.41) | Appeal submitted but TOS_VIOLATION suspension persists (request for p… |
| #29574 | area/core | area/agent (0.87) | area/agent (0.44) | area/agent (0.96) | area/agent (1.00) | area/agent (1.00) | area/core (0.55) | area/agent (0.63) | area/core (0.39) | area/agent (0.69) | bug(core): 400 Bad Request "Requests ending with a model turn are not… |
| #29572 | area/platform | area/core (0.51) | area/core (0.89) | area/non-interactive (0.48) | area/core (1.00) | area/core (1.00) | area/core (0.84) | area/core (0.84) | area/core (0.41) | area/core (0.99) | parseImageName misparses a sandbox image reference whose registry car… |
| #29562 | area/core | area/core (0.66) | area/core (0.49) | area/agent (0.65) | area/core (1.00) | area/core (1.00) | area/core (0.94) | area/core (0.91) | area/core (0.43) | area/core (0.88) | truncateString() drops every line terminator and does not charge them… |
