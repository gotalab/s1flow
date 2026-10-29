# gh-gemini-area · policy

2026-10-22 · 300 labelled (area/core 93, area/agent 84, area/security 41, area/extensions 20, area/documentation 18, area/enterprise 18, area/platform 13, area/non-interactive 13) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**luna@decisions/policy** has the highest accuracy (all), 65% [59, 71] (API cost $0.68 per 10k, p99 719ms). Its interval overlaps with d1@vercel/policy, kev@openrouter/policy, jev@vercel/policy, clef-flash/policy, clef/policy: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **d1@vercel/policy** (API cost $0.24 per 10k, p99 954ms). Latency not compared (6 with no concurrency recorded; 6 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-area --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is luna@decisions/policy's, 65% [60, 71].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/policy | 300 | 61.7% [56, 67] | 0.58 | 0.89 | 0.10 | 0% [0, 1] | 0.0% (0.0%) | 0/300 | 0/300 |
| clef-flash/policy | 300 | 58.7% [53, 64] | 0.54 | 0.88 | 0.10 | 9% [5, 13] | 89.5% (70.4%) | 0/300 | 0/300 |
| d1@vercel/policy | 300 | 56.7% [51, 62] | 0.54 | 0.86 | 0.20 | 2% [0, 4] | 75.0% (24.9%) | 0/300 | 0/300 |
| jev@vercel/policy | 300 | 61.7% [56, 67] | 0.57 | 0.89 | 0.20 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| kev@openrouter/policy | 300 | 58.7% [53, 64] | 0.55 | 0.88 | 0.18 | 3% [1, 5] | 83.3% (41.8%) | 0/300 | 0/300 |
| luna@decisions/policy | 300 | 65.3% [60, 71] | 0.61 | 0.89 | 0.18 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |

Answered by: clef/policy = clef; clef-flash/policy = clef-flash; d1@vercel/policy = liquid/d1; jev@vercel/policy = typesafe-ai/jev; kev@openrouter/policy = jaredpalmer/kev-4b-20260924; luna@decisions/policy = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| d1@vercel/policy ◎ | 57% [50, 64] | — | met |
| kev@openrouter/policy | 60% [54, 67] | — | met |
| jev@vercel/policy | 64% [58, 70] | — | met |
| luna@decisions/policy | 65% [59, 71] | — | met |
| clef-flash/policy | 59% [52, 66] | — | met |
| clef/policy | 62% [56, 69] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/policy | 300 | 422 ms | 644 ms | 1092 ms | 1237 ms | 2.6 | not recorded | unknown | $1.87 | estimated |  |
| clef-flash/policy | 300 | 206 ms | 488 ms | 612 ms | 702 ms | 3.0 | not recorded | unknown | $0.70 | estimated | ○ |
| d1@vercel/policy | 300 | 492 ms | 646 ms | 954 ms | 6788 ms | 1.9 | not recorded | unknown | $0.24 | billed | ○ |
| jev@vercel/policy | 300 | 422 ms | 574 ms | 719 ms | 942 ms | 1.7 | not recorded | unknown | $0.40 | billed | ○ |
| kev@openrouter/policy | 300 | 940 ms | 1259 ms | 1691 ms | 2018 ms | 1.8 | not recorded | unknown | $0.24 | billed | ○ |
| luna@decisions/policy | 300 | 267 ms | 394 ms | 719 ms | 1048 ms | 2.7 | not recorded | unknown | $0.68 | estimated | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel/policy, jev@vercel/policy, kev@openrouter/policy; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/policy (list price of 2026-10-04), clef-flash/policy (list price of 2026-10-04), luna@decisions/policy (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/policy | $0.06 | 17 s (measured, 300 calls) | 9 min | 8 |
| clef-flash/policy | $0.02 | 10 s (measured, 300 calls) | 6 min | 8 |
| d1@vercel/policy | $0.0073 | 22 s (measured, 300 calls) | 12 min | 8 |
| jev@vercel/policy | $0.01 | 17 s (measured, 300 calls) | 9 min | 8 |
| kev@openrouter/policy | $0.0073 | 36 s (measured, 300 calls) | 20 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/policy | 90 | 60.0% | 0% | — | 0.600 |
| clef-flash/policy | 90 | 57.8% | 8% | 85.7% | 0.578 |
| d1@vercel/policy | 90 | 56.7% | 0% | — | 0.567 |
| jev@vercel/policy | 90 | 55.6% | 0% | — | 0.556 |
| kev@openrouter/policy | 90 | 54.4% | 0% | — | 0.544 |
| luna@decisions/policy | 90 | 65.6% | 0% | — | 0.656 |

## Wrong at a high probability (0.9 or more)

**clef/policy** (13)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29033 | area/platform | area/extensions | 0.98 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29012 | area/core | area/documentation | 0.97 | Docs: six CLI flags missing from the reference table |
| #29068 | area/agent | area/security | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #29101 | area/enterprise | area/security | 0.96 | Authentication failure blocking Enterprise Workspace accounts |
| #29316 | area/agent | area/non-interactive | 0.96 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29069 | area/core | area/security | 0.95 | invalid_grant |
| #29598 | area/platform | area/non-interactive | 0.95 | Nightly evals: summary job reads green when no eval reports exist |
| #28798 | area/platform | area/non-interactive | 0.95 | unassign-inactive-assignees treats any open PR as progress, so stale … |

**clef-flash/policy** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29033 | area/platform | area/extensions | 0.94 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29461 | area/platform | area/security | 0.94 | Sandboxed Gemini CLI loses login and session information since v0.60.0 |
| #29598 | area/platform | area/non-interactive | 0.92 | Nightly evals: summary job reads green when no eval reports exist |
| #29316 | area/agent | area/non-interactive | 0.92 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29069 | area/core | area/security | 0.91 | invalid_grant |
| #29012 | area/core | area/documentation | 0.91 | Docs: six CLI flags missing from the reference table |
| #29064 | area/platform | area/enterprise | 0.91 | Gemini 2.5 Pro quota stuck at 100% / limit reached for several days |
| #29101 | area/enterprise | area/security | 0.91 | Authentication failure blocking Enterprise Workspace accounts |

**d1@vercel/policy** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29033 | area/platform | area/extensions | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29589 | area/core | area/agent | 1.00 | bug(core): stripToolCallIdPrefixes drops functionResponse.parts, so i… |
| #29598 | area/platform | area/non-interactive | 0.99 | Nightly evals: summary job reads green when no eval reports exist |
| #29064 | area/platform | area/enterprise | 0.99 | Gemini 2.5 Pro quota stuck at 100% / limit reached for several days |
| #29069 | area/core | area/security | 0.99 | invalid_grant |
| #29038 | area/security | area/extensions | 0.99 | bug: extension trust gate evaluates process.cwd() but prompts/writes … |
| #29309 | area/core | area/agent | 0.99 | bug(core): unbounded _execute recursion on sandbox_expansion_required… |
| #29501 | area/security | area/non-interactive | 0.99 | ci: template injection risk in release-patch-0-from-comment workflow |

**jev@vercel/policy** (26)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29316 | area/agent | area/non-interactive | 1.00 | bug(sdk): AgentShellOptions env/timeoutSeconds silently ignored (shel… |
| #29069 | area/core | area/security | 1.00 | invalid_grant |
| #29068 | area/agent | area/security | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #29001 | area/extensions | area/security | 1.00 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29064 | area/platform | area/enterprise | 1.00 | Gemini 2.5 Pro quota stuck at 100% / limit reached for several days |
| #29012 | area/core | area/documentation | 1.00 | Docs: six CLI flags missing from the reference table |
| #29033 | area/platform | area/extensions | 1.00 | bug: extension update rollback copies an empty temp dir - restores no… |
| #29598 | area/platform | area/non-interactive | 1.00 | Nightly evals: summary job reads green when no eval reports exist |

**luna@decisions/policy** (31)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29001 | area/extensions | area/security | 1.00 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #28998 | area/core | area/platform | 1.00 | bug(ide): Windows IDE detection fallback invokes Unix-only 'ps' comma… |
| #29424 | area/agent | area/core | 1.00 | bug: Node process hangs on session exit, preventing terminal from ret… |
| #29012 | area/core | area/documentation | 1.00 | Docs: six CLI flags missing from the reference table |
| #28761 | area/core | area/enterprise | 1.00 | [Bug] Usage limit reached despite 1–8% usage on Gemini Code Assist St… |
| #29076 | area/security | area/extensions | 1.00 | security(extensions): extension name path traversal allows write outs… |
| #29598 | area/platform | area/non-interactive | 1.00 | Nightly evals: summary job reads green when no eval reports exist |
| #29069 | area/core | area/security | 1.00 | invalid_grant |


## Cases the models disagree on (12 of 152)

| id | label | clef | clef-flash | d1@vercel | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|
| #29297 | area/core | area/core (0.79) | area/enterprise (0.53) | area/core (0.74) | area/core (0.88) | area/core (0.32) | area/core (1.00) | Feature: /stats heatmap — calendar heatmap of daily token usage |
| #29079 | area/security | area/security (0.68) | area/security (0.54) | area/extensions (0.79) | area/security (1.00) | area/security (0.36) | area/security (0.88) | security(mcp): MCP server command not validated - malicious settings/… |
| #29003 | area/security | area/security (0.77) | area/security (0.46) | area/agent (0.26) | area/security (0.98) | area/security (0.33) | area/security (1.00) | security(core): project .env can inject execution-affecting GIT_* var… |
| #28998 | area/core | area/platform (0.66) | area/core (0.49) | area/platform (0.55) | area/core (0.60) | area/platform (0.39) | area/platform (1.00) | bug(ide): Windows IDE detection fallback invokes Unix-only 'ps' comma… |
| #29548 | area/documentation | area/documentation (0.78) | area/extensions (0.45) | area/documentation (0.59) | area/documentation (0.97) | area/documentation (0.50) | area/documentation (0.99) | `.gemini/skills/behavioral-evals/SKILL.md` links to a contributor's l… |
| #29410 | area/core | area/core (0.61) | area/core (0.51) | area/core (0.80) | area/core (0.85) | area/agent (0.41) | area/core (0.99) | resume latest reopens most recently started session, not most recentl… |
| #29306 | area/security | area/security (0.76) | area/security (0.52) | area/agent (0.60) | area/security (0.76) | area/security (0.36) | area/security (0.99) | bug(core): external safety checker inherits full env and unbounded st… |
| #29189 | area/security | area/security (0.70) | area/security (0.54) | area/platform (0.39) | area/security (0.99) | area/security (0.33) | area/security (0.99) | Security: `git diff --output` bypasses permission prompt, silently ov… |
| #29107 | area/security | area/security (0.55) | area/security (0.48) | area/security (0.83) | area/security (0.99) | area/extensions (0.22) | area/security (0.99) | "The caller does not have permission  #25306 - still persists |
| #29074 | area/security | area/security (0.71) | area/security (0.41) | area/agent (0.89) | area/security (0.97) | area/security (0.36) | area/security (0.99) | security(web-fetch): SSRF via redirect to private IP bypasses isPriva… |
| #29070 | area/security | area/security (0.61) | area/security (0.24) | area/non-interactive (0.40) | area/security (0.99) | area/security (0.35) | area/security (0.95) | security(sandbox): host shell injection via BUILD_SANDBOX path interp… |
| #29053 | area/enterprise | area/enterprise (0.88) | area/enterprise (0.73) | area/enterprise (0.84) | area/security (0.52) | area/core (0.23) | area/enterprise (0.99) | bug: commandRegex policy patterns are unanchored and can match across… |
