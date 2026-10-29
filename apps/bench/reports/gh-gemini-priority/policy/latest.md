# gh-gemini-priority · policy

2026-10-22 · 300 labelled (priority/p2 146, priority/p1 92, priority/p3 62) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**clef/policy** has the highest accuracy (all), 62% [55, 68] (API cost $1.51 per 10k, p99 829ms). Its interval overlaps with kev@openrouter/policy, d1@vercel/policy, jev@vercel/policy, clef-flash/policy, luna@decisions/policy: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **kev@openrouter/policy** (API cost $0.21 per 10k, p99 1432ms). Latency not compared (6 with no concurrency recorded; 6 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-priority --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is clef/policy's, 63% [57, 68].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef/policy | 300 | 62.7% [57, 68] | 0.64 | 0.81 | 0.11 | 3% [1, 5] | 83.3% (41.8%) | 0/300 | 0/300 |
| clef-flash/policy | 300 | 59.3% [54, 65] | 0.61 | 0.80 | 0.12 | 2% [0, 4] | 75.0% (24.9%) | 0/300 | 0/300 |
| d1@vercel/policy | 300 | 54.3% [49, 60] | 0.56 | 0.79 | 0.13 | 1% [0, 3] | 66.7% (13.5%) | 0/300 | 0/300 |
| jev@vercel/policy | 300 | 58.3% [53, 64] | 0.62 | 0.79 | 0.22 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| kev@openrouter/policy | 300 | 54.3% [49, 60] | 0.58 | 0.76 | 0.11 | 0% [0, 1] | 0.0% (0.0%) | 0/300 | 0/300 |
| luna@decisions/policy | 300 | 60.0% [54, 65] | 0.60 | 0.80 | 0.27 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |

Answered by: clef/policy = clef; clef-flash/policy = clef-flash; d1@vercel/policy = liquid/d1; jev@vercel/policy = typesafe-ai/jev; kev@openrouter/policy = jaredpalmer/kev-4b-20260924; luna@decisions/policy = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| kev@openrouter/policy ◎ | 54% [47, 60] | — | met |
| d1@vercel/policy | 54% [47, 60] | — | met |
| jev@vercel/policy | 58% [51, 64] | — | met |
| clef-flash/policy | 58% [51, 64] | — | met |
| luna@decisions/policy | 58% [51, 64] | — | met |
| clef/policy | 62% [55, 68] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef/policy | 300 | 404 ms | 604 ms | 829 ms | 1075 ms | 2.1 | not recorded | unknown | $1.51 | estimated | ○ |
| clef-flash/policy | 300 | 211 ms | 516 ms | 644 ms | 738 ms | 3.0 | not recorded | unknown | $0.57 | estimated | ○ |
| d1@vercel/policy | 300 | 510 ms | 663 ms | 1042 ms | 6235 ms | 2.0 | not recorded | unknown | $0.21 | billed | ○ |
| jev@vercel/policy | 300 | 398 ms | 543 ms | 717 ms | 800 ms | 1.8 | not recorded | unknown | $0.34 | billed | ○ |
| kev@openrouter/policy | 300 | 927 ms | 1125 ms | 1432 ms | 1611 ms | 1.5 | not recorded | unknown | $0.21 | billed | ○ |
| luna@decisions/policy | 300 | 261 ms | 369 ms | 931 ms | 1891 ms | 3.6 | not recorded | unknown | $0.59 | estimated |  |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel/policy, jev@vercel/policy, kev@openrouter/policy; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef/policy (list price of 2026-10-04), clef-flash/policy (list price of 2026-10-04), luna@decisions/policy (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef/policy | $0.05 | 17 s (measured, 300 calls) | 9 min | 8 |
| clef-flash/policy | $0.02 | 11 s (measured, 300 calls) | 6 min | 8 |
| d1@vercel/policy | $0.0063 | 25 s (measured, 300 calls) | 14 min | 8 |
| jev@vercel/policy | $0.01 | 17 s (measured, 300 calls) | 9 min | 8 |
| kev@openrouter/policy | $0.0062 | 36 s (measured, 300 calls) | 20 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef/policy | 90 | 64.4% | 2% | 100.0% | 0.644 |
| clef-flash/policy | 90 | 62.2% | 0% | — | 0.622 |
| d1@vercel/policy | 90 | 55.6% | 2% | 100.0% | 0.556 |
| jev@vercel/policy | 90 | 60.0% | 0% | — | 0.600 |
| kev@openrouter/policy | 90 | 55.6% | 0% | — | 0.556 |
| luna@decisions/policy | 90 | 65.6% | 0% | — | 0.656 |

## Wrong at a high probability (0.9 or more)

**clef/policy** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28445 | priority/p2 | priority/p3 | 0.96 | can i add image generation model configs for nano banana ? |
| #28259 | priority/p2 | priority/p3 | 0.96 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #29012 | priority/p1 | priority/p3 | 0.95 | Docs: six CLI flags missing from the reference table |
| #28260 | priority/p2 | priority/p3 | 0.95 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |
| #28231 | priority/p2 | priority/p3 | 0.93 | Docs: Replace dangerous rm -rf / example in policy engine documentati… |
| #28315 | priority/p2 | priority/p3 | 0.92 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #28263 | priority/p2 | priority/p1 | 0.90 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |

**clef-flash/policy** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28445 | priority/p2 | priority/p3 | 0.92 | can i add image generation model configs for nano banana ? |

**d1@vercel/policy** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28445 | priority/p2 | priority/p3 | 0.97 | can i add image generation model configs for nano banana ? |
| #28263 | priority/p2 | priority/p1 | 0.95 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |
| #28315 | priority/p2 | priority/p3 | 0.95 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #28841 | priority/p2 | priority/p3 | 0.95 | GeminiCLI.com Feedback: [ISSUE] |
| #29012 | priority/p1 | priority/p3 | 0.95 | Docs: six CLI flags missing from the reference table |
| #28550 | priority/p2 | priority/p1 | 0.94 | Heap OOM in non-interactive runs: ignore-matcher (path-scurry + minim… |
| #28259 | priority/p2 | priority/p3 | 0.92 | refactor(cli): clean up profile selector logic and remove legacy conf… |

**jev@vercel/policy** (38)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28445 | priority/p2 | priority/p3 | 1.00 | can i add image generation model configs for nano banana ? |
| #28263 | priority/p2 | priority/p1 | 1.00 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |
| #28550 | priority/p2 | priority/p1 | 1.00 | Heap OOM in non-interactive runs: ignore-matcher (path-scurry + minim… |
| #28841 | priority/p2 | priority/p3 | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28313 | priority/p2 | priority/p1 | 1.00 | MaxListenersExceededWarning and Infinite Loop with gemma-4-31b-it (Ge… |
| #29001 | priority/p2 | priority/p1 | 0.99 | security(a2a-server): HTTP API never enforces authentication, and the… |
| #29306 | priority/p2 | priority/p1 | 0.99 | bug(core): external safety checker inherits full env and unbounded st… |
| #29146 | priority/p2 | priority/p3 | 0.99 | GeminiCLI.com Feedback: [ISSUE] |

**kev@openrouter/policy** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28263 | priority/p2 | priority/p1 | 0.93 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |

**luna@decisions/policy** (44)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #29045 | priority/p1 | priority/p2 | 1.00 | bug: read-many-files treats substring overlap as 'explicitly requeste… |
| #28445 | priority/p2 | priority/p3 | 1.00 | can i add image generation model configs for nano banana ? |
| #28315 | priority/p2 | priority/p3 | 1.00 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #29012 | priority/p1 | priority/p3 | 1.00 | Docs: six CLI flags missing from the reference table |
| #28263 | priority/p2 | priority/p1 | 1.00 | Critical System Failure in LocalAgentExecutor due to Dropped Tool Exe… |
| #28259 | priority/p2 | priority/p3 | 1.00 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #28826 | priority/p1 | priority/p2 | 1.00 | Workspace scan warns when projects.json.lock disappears normally |
| #29031 | priority/p1 | priority/p2 | 0.99 | bug: headless mode reports an untrusted folder as trusted to the rest… |


## Cases the models disagree on (12 of 182)

| id | label | clef | clef-flash | d1@vercel | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|
| #29318 | priority/p2 | priority/p2 (0.67) | priority/p2 (0.46) | priority/p2 (0.61) | priority/p1 (0.64) | priority/p2 (0.44) | priority/p2 (1.00) | bug(cli): @ glob fallback parses LLM text and takes only first match |
| #29290 | priority/p2 | priority/p2 (0.66) | priority/p2 (0.49) | priority/p2 (0.67) | priority/p2 (0.55) | priority/p1 (0.43) | priority/p2 (1.00) | Nested .gitignore: patterns with only a trailing slash (e.g. build/) … |
| #29232 | priority/p3 | priority/p3 (0.72) | priority/p1 (0.69) | priority/p3 (0.83) | priority/p3 (0.88) | priority/p1 (0.56) | priority/p3 (1.00) | Google is a GREAT company but Gemini-cli is NOT |
| #29122 | priority/p2 | priority/p2 (0.55) | priority/p2 (0.46) | priority/p2 (0.68) | priority/p2 (0.79) | priority/p1 (0.50) | priority/p2 (1.00) | hooks: `migrate` copies Claude's `timeout` across a seconds → millise… |
| #29045 | priority/p1 | priority/p2 (0.61) | priority/p1 (0.46) | priority/p2 (0.59) | priority/p2 (0.55) | priority/p1 (0.50) | priority/p2 (1.00) | bug: read-many-files treats substring overlap as 'explicitly requeste… |
| #29044 | priority/p2 | priority/p2 (0.55) | priority/p1 (0.56) | priority/p1 (0.53) | priority/p1 (0.74) | priority/p1 (0.64) | priority/p2 (1.00) | bug: prompt templates built via String.replace corrupt payloads conta… |
| #29012 | priority/p1 | priority/p3 (0.95) | priority/p3 (0.79) | priority/p3 (0.95) | priority/p3 (0.95) | priority/p2 (0.46) | priority/p3 (1.00) | Docs: six CLI flags missing from the reference table |
| #28929 | priority/p3 | priority/p3 (0.78) | priority/p3 (0.60) | priority/p3 (0.93) | priority/p3 (1.00) | priority/p2 (0.41) | priority/p3 (0.87) | GeminiCLI.com Feedback: [ISSUE] |
| #28833 | priority/p3 | priority/p3 (0.94) | priority/p3 (0.75) | priority/p3 (0.94) | priority/p3 (0.99) | priority/p1 (0.46) | priority/p3 (1.00) | Prevent Margin Leaks & Surprise LLM Bills: Add a Hybrid Spend Firewall |
| #28802 | priority/p3 | priority/p3 (0.75) | priority/p1 (0.54) | priority/p3 (0.96) | priority/p3 (0.85) | priority/p3 (0.35) | priority/p3 (1.00) | Latest Gemini models including Flash 3.5, Flash 3.6 and Flash 3.7 are… |
| #28733 | priority/p3 | priority/p3 (0.74) | priority/p3 (0.61) | priority/p3 (0.89) | priority/p3 (1.00) | priority/p2 (0.43) | priority/p3 (0.93) | GeminiCLI.com Feedback: [ISSUE] |
| #28611 | priority/p3 | priority/p3 (0.81) | priority/p3 (0.65) | priority/p3 (0.92) | priority/p3 (1.00) | priority/p2 (0.41) | priority/p3 (0.83) | GeminiCLI.com Feedback: [ISSUE] |
