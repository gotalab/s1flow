# gh-gemini-priority · gepa-jev-from-policy

2026-10-22 · 300 labelled (priority/p2 146, priority/p1 92, priority/p3 62) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**luna@decisions/gepa-jev-from-policy** has the highest accuracy (all), 66% [60, 71] (API cost $0.68 per 10k, p99 618ms). Its interval overlaps with jev@vercel/gepa-jev-from-policy, clef-flash/gepa-jev-from-policy, clef/gepa-jev-from-policy: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **jev@vercel/gepa-jev-from-policy** (API cost $0.38 per 10k, p99 732ms). Latency not compared (4 with no concurrency recorded; 4 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-priority --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is luna@decisions/gepa-jev-from-policy's, 67% [61, 72].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/gepa-jev-from-policy | 300 | 63.0% [57, 68] | 0.63 | 0.82 | 0.05 | 1% [0, 3] | 66.7% (13.5%) | 0/300 | 0/300 |
| clef-flash/gepa-jev-from-policy | 300 | 61.3% [56, 66] | 0.63 | 0.82 | 0.05 | 2% [0, 4] | 100.0% (47.3%) | 0/300 | 0/300 |
| jev@vercel/gepa-jev-from-policy | 300 | 66.0% [61, 71] | 0.67 | 0.83 | 0.15 | 4% [1, 7] | 100.0% (68.8%) | 0/300 | 0/300 |
| luna@decisions/gepa-jev-from-policy | 300 | 66.7% [61, 72] | 0.65 | 0.81 | 0.21 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |

Answered by: clef/gepa-jev-from-policy = clef; clef-flash/gepa-jev-from-policy = clef-flash; jev@vercel/gepa-jev-from-policy = typesafe-ai/jev; luna@decisions/gepa-jev-from-policy = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| jev@vercel/gepa-jev-from-policy ◎ | 64% [57, 70] | — | met |
| clef-flash/gepa-jev-from-policy | 60% [53, 66] | — | met |
| luna@decisions/gepa-jev-from-policy | 66% [60, 71] | — | met |
| clef/gepa-jev-from-policy | 60% [54, 68] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/gepa-jev-from-policy | 300 | 407 ms | 631 ms | 1036 ms | 1360 ms | 2.5 | not recorded | unknown | $1.73 | estimated |  |
| clef-flash/gepa-jev-from-policy | 300 | 200 ms | 507 ms | 577 ms | 675 ms | 2.9 | not recorded | unknown | $0.65 | estimated | ○ |
| jev@vercel/gepa-jev-from-policy | 300 | 404 ms | 547 ms | 732 ms | 1238 ms | 1.8 | not recorded | unknown | $0.38 | billed | ○ |
| luna@decisions/gepa-jev-from-policy | 300 | 263 ms | 352 ms | 618 ms | 684 ms | 2.4 | not recorded | unknown | $0.68 | estimated | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: jev@vercel/gepa-jev-from-policy; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/gepa-jev-from-policy (list price of 2026-10-04), clef-flash/gepa-jev-from-policy (list price of 2026-10-04), luna@decisions/gepa-jev-from-policy (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/gepa-jev-from-policy | $0.05 | 17 s (measured, 300 calls) | 9 min | 8 |
| clef-flash/gepa-jev-from-policy | $0.02 | 10 s (measured, 300 calls) | 6 min | 8 |
| luna@decisions/gepa-jev-from-policy | $0.02 | 11 s (measured, 300 calls) | 6 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/gepa-jev-from-policy | 90 | 68.9% | 0% | — | 0.689 |
| clef-flash/gepa-jev-from-policy | 90 | 65.6% | 4% | 100.0% | 0.656 |
| jev@vercel/gepa-jev-from-policy | 90 | 71.1% | 4% | 100.0% | 0.711 |
| luna@decisions/gepa-jev-from-policy | 90 | 68.9% | 0% | — | 0.689 |

## Wrong at a high probability (0.9 or more)

**clef/gepa-jev-from-policy** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29012 | priority/p1 | priority/p3 | 0.93 | Docs: six CLI flags missing from the reference table |
| #28259 | priority/p2 | priority/p3 | 0.92 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #28841 | priority/p2 | priority/p3 | 0.91 | GeminiCLI.com Feedback: [ISSUE] |

**jev@vercel/gepa-jev-from-policy** (29)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29405 | priority/p2 | priority/p1 | 0.99 | [Bug Report] Background tasks enter indefinite 'Forever Running' hang… |
| #28550 | priority/p2 | priority/p1 | 0.99 | Heap OOM in non-interactive runs: ignore-matcher (path-scurry + minim… |
| #28259 | priority/p2 | priority/p3 | 0.99 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #28841 | priority/p2 | priority/p3 | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #29306 | priority/p2 | priority/p1 | 0.98 | bug(core): external safety checker inherits full env and unbounded st… |
| #28445 | priority/p2 | priority/p3 | 0.98 | can i add image generation model configs for nano banana ? |
| #28263 | priority/p2 | priority/p1 | 0.98 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |
| #28260 | priority/p2 | priority/p3 | 0.96 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |

**luna@decisions/gepa-jev-from-policy** (38)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28445 | priority/p2 | priority/p3 | 1.00 | can i add image generation model configs for nano banana ? |
| #28231 | priority/p2 | priority/p3 | 1.00 | Docs: Replace dangerous rm -rf / example in policy engine documentati… |
| #28259 | priority/p2 | priority/p3 | 1.00 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #29012 | priority/p1 | priority/p3 | 1.00 | Docs: six CLI flags missing from the reference table |
| #29405 | priority/p2 | priority/p1 | 0.99 | [Bug Report] Background tasks enter indefinite 'Forever Running' hang… |
| #28859 | priority/p1 | priority/p2 | 0.99 | v0.55.1: any `--model gemini-<X.Y>-flash` is silently served by gemin… |
| #29465 | priority/p1 | priority/p2 | 0.99 | gemini mcp add in an untrusted folder silently wipes the project's se… |
| #28944 | priority/p3 | priority/p2 | 0.99 | /skills reload reports duplicate warnings when .gemini is symlinked/j… |


## Cases the models disagree on (12 of 127)

| id | label | clef | clef-flash | jev@vercel | luna@decisions | case |
|---|---|---|---|---|---|---|
| #28231 | priority/p2 | priority/p3 (0.87) | priority/p3 (0.79) | priority/p2 (0.42) | priority/p3 (1.00) | Docs: Replace dangerous rm -rf / example in policy engine documentati… |
| #29465 | priority/p1 | priority/p1 (0.55) | priority/p1 (0.49) | priority/p2 (0.66) | priority/p2 (0.99) | gemini mcp add in an untrusted folder silently wipes the project's se… |
| #29003 | priority/p1 | priority/p1 (0.69) | priority/p1 (0.62) | priority/p1 (0.98) | priority/p2 (0.67) | security(core): project .env can inject execution-affecting GIT_* var… |
| #28265 | priority/p2 | priority/p3 (0.51) | priority/p2 (0.51) | priority/p2 (0.93) | priority/p2 (0.98) | Unhandled PTY Lifecycle Race Conditions Masked by Silent EBADF/ESRCH … |
| #28263 | priority/p2 | priority/p1 (0.76) | priority/p1 (0.65) | priority/p1 (0.98) | priority/p2 (0.59) | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |
| #29044 | priority/p2 | priority/p2 (0.64) | priority/p1 (0.42) | priority/p2 (0.62) | priority/p2 (0.97) | bug: prompt templates built via String.replace corrupt payloads conta… |
| #28646 | priority/p2 | priority/p2 (0.51) | priority/p1 (0.41) | priority/p2 (0.54) | priority/p2 (0.97) | bug: malformed GitHub API JSON can crash extension operations |
| #29204 | priority/p2 | priority/p2 (0.68) | priority/p1 (0.49) | priority/p2 (0.96) | priority/p2 (0.92) | MCP prompt responses are submitted as JSON-encoded text |
| #29133 | priority/p2 | priority/p2 (0.51) | priority/p1 (0.45) | priority/p1 (0.75) | priority/p2 (0.96) | Bug: --list-sessions never marks the current session, so --delete-ses… |
| #28575 | priority/p2 | priority/p2 (0.75) | priority/p2 (0.51) | priority/p1 (0.60) | priority/p2 (0.96) | CLI crashes on startup when GEMINI_API_KEY contains special characters |
| #28314 | priority/p2 | priority/p2 (0.49) | priority/p1 (0.42) | priority/p2 (0.96) | priority/p2 (0.93) | GeminiCLI.com Feedback: [ISSUE] |
| #29308 | priority/p2 | priority/p1 (0.47) | priority/p1 (0.48) | priority/p1 (0.51) | priority/p2 (0.95) | bug(sdk): unguarded JSON.parse on tool-call args kills sendStream (se… |
