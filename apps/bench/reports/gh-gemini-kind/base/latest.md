# gh-gemini-kind

2026-10-22 · 300 labelled (kind/bug 247, kind/enhancement 28, kind/question 25) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of google-gemini/gemini-cli (labels applied by the repository's Gemini triage bot; see gh-audit)

**flash-lite@vercel** has the highest accuracy (all), 91% [88, 95] (API cost $1.65 per 10k, p99 6295ms). Its interval overlaps with kev@openrouter, d1@vercel, jev, jev@vercel, clef-flash, luna@decisions, clef, haiku@vercel: at this many cases the difference is not shown. Of those, the lowest API cost is chosen: **kev@openrouter** (API cost $0.18 per 10k, p99 5128ms). Latency not compared (9 with no concurrency recorded; 9 with no retries recorded): measure every candidate again at one concurrency, s1flow run gh-gemini-kind --fresh --concurrency N (the same N for all). The highest accuracy (all cases) is haiku@vercel's, 92% [88, 95].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 89.0% [86, 93] | 0.69 | 0.96 | 0.04 | 85% [80, 90] | 95.0% (91.4%) | 0/300 | 0/300 |
| clef-flash | 300 | 90.0% [87, 93] | 0.75 | 0.96 | 0.05 | 85% [80, 90] | 93.8% (90.0%) | 0/300 | 0/300 |
| d1@vercel | 300 | 88.0% [84, 92] | 0.68 | 0.96 | 0.03 | 84% [79, 89] | 95.5% (92.0%) | 0/300 | 0/300 |
| flash-lite@vercel ※ | 300 | 90.7% [87, 94] | 0.77 | 0.86 | 0.09 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| haiku@vercel ※ | 300 | 91.7% [88, 95] | 0.84 | 0.93 | 0.08 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev | 300 | 89.7% [86, 93] | 0.68 | 0.96 | 0.05 | 87% [82, 91] | 95.1% (91.5%) | 0/300 | 0/300 |
| jev@vercel | 300 | 90.0% [86, 93] | 0.72 | 0.95 | 0.07 | 89% [85, 93] | 95.2% (91.8%) | 0/300 | 0/300 |
| kev@openrouter | 300 | 87.0% [83, 91] | 0.67 | 0.95 | 0.12 | 79% [73, 84] | 95.2% (91.4%) | 0/300 | 0/300 |
| luna@decisions | 300 | 90.3% [87, 93] | 0.77 | 0.95 | 0.06 | 86% [81, 90] | 95.0% (91.4%) | 0/300 | 0/300 |

Answered by: clef = clef; clef-flash = clef-flash; d1@vercel = liquid/d1; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.14.0 (also jev-1.13.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | accuracy (all) | rule | constraints |
|---|---|---|---|
| kev@openrouter ◎ | 87% [82, 91] | — | met |
| d1@vercel | 89% [84, 93] | — | met |
| jev | 90% [86, 94] | — | met |
| jev@vercel | 90% [86, 94] | — | met |
| clef-flash | 90% [85, 93] | — | met |
| luna@decisions | 90% [86, 94] | — | met |
| clef | 90% [86, 94] | — | met |
| flash-lite@vercel | 91% [88, 95] | — | met |
| haiku@vercel | 91% [87, 95] | — | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 425 ms | 692 ms | 1027 ms | 1177 ms | 2.4 | not recorded | unknown | $1.33 | estimated |  |
| clef-flash | 300 | 222 ms | 506 ms | 636 ms | 685 ms | 2.9 | not recorded | unknown | $0.50 | estimated |  |
| d1@vercel | 300 | 708 ms | 1226 ms | 3864 ms | 4017 ms | 5.5 | not recorded | unknown | $0.18 | billed | ○ |
| flash-lite@vercel | 300 | 1367 ms | 1819 ms | 6295 ms | 7893 ms | 4.6 | not recorded | unknown | $1.65 | estimated | ○ |
| haiku@vercel | 300 | 1132 ms | 1527 ms | 4924 ms | 8881 ms | 4.4 | not recorded | unknown | $7.76 | estimated | ○ |
| jev | 300 | 165 ms | 209 ms | 240 ms | 365 ms | 1.5 | not recorded | unknown | $0.31 | estimated | ○ |
| jev@vercel | 300 | 644 ms | 1095 ms | 3755 ms | 4399 ms | 5.8 | not recorded | unknown | $0.31 | billed |  |
| kev@openrouter | 300 | 1129 ms | 1546 ms | 5128 ms | 6310 ms | 4.5 | not recorded | unknown | $0.18 | billed | ○ |
| luna@decisions | 300 | 257 ms | 302 ms | 633 ms | 3104 ms | 2.5 | not recorded | unknown | $0.52 | estimated | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: d1@vercel, jev@vercel, kev@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.04 | 18 s (measured, 300 calls) | 10 min | 8 |
| clef-flash | $0.01 | 11 s (measured, 300 calls) | 6 min | 8 |
| jev | $0.0093 | 7 s (measured, 300 calls) | 4 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 90 | 86.7% | 86% | 94.8% | 0.867 |
| clef-flash | 90 | 91.1% | 89% | 93.8% | 0.911 |
| d1@vercel | 90 | 86.7% | 90% | 90.1% | 0.867 |
| flash-lite@vercel | 90 | 88.9% | 0% | — | 0.889 |
| haiku@vercel | 90 | 92.2% | 0% | — | 0.922 |
| jev | 90 | 88.9% | 92% | 92.8% | 0.889 |
| jev@vercel | 90 | 90.0% | 92% | 91.6% | 0.900 |
| kev@openrouter | 90 | 86.7% | 84% | 94.7% | 0.867 |
| luna@decisions | 90 | 90.0% | 82% | 95.9% | 0.900 |

## Wrong at a high probability (0.9 or more)

**clef** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28315 | kind/bug | kind/enhancement | 0.98 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #28260 | kind/bug | kind/enhancement | 0.94 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |
| #28745 | kind/question | kind/bug | 0.93 | GeminiCLI.com Feedback: [ISSUE] |
| #28713 | kind/bug | kind/enhancement | 0.93 | Caretaker agent completion |
| #28393 | kind/question | kind/bug | 0.91 | GeminiCLI.com Feedback: [ISSUE] |
| #28259 | kind/bug | kind/enhancement | 0.90 | refactor(cli): clean up profile selector logic and remove legacy conf… |

**clef-flash** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28259 | kind/bug | kind/enhancement | 0.97 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #28315 | kind/bug | kind/enhancement | 0.96 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #28260 | kind/bug | kind/enhancement | 0.96 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |
| #28713 | kind/bug | kind/enhancement | 0.94 | Caretaker agent completion |
| #28261 | kind/bug | kind/enhancement | 0.91 | refactor(a2a-server): implement V1 to V2 settings migration logic |

**d1@vercel** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28315 | kind/bug | kind/enhancement | 1.00 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #29605 | kind/question | kind/enhancement | 0.97 | Pull request 29482 is waiting for a review |
| #28713 | kind/bug | kind/enhancement | 0.97 | Caretaker agent completion |
| #28777 | kind/question | kind/enhancement | 0.97 | ticket IT support |
| #28258 | kind/bug | kind/enhancement | 0.94 | refactor(cli): decouple useGeminiStream from lookahead logic for para… |
| #28260 | kind/bug | kind/enhancement | 0.93 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |
| #28745 | kind/question | kind/bug | 0.92 | GeminiCLI.com Feedback: [ISSUE] |
| #28259 | kind/bug | kind/enhancement | 0.92 | refactor(cli): clean up profile selector logic and remove legacy conf… |

**flash-lite@vercel** (28)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28611 | kind/question | kind/bug | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28614 | kind/bug | kind/question | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28571 | kind/bug | kind/question | 1.00 | Open Copilot в VS Code  codespace  |
| #28582 | kind/enhancement | kind/question | 1.00 | genkit |
| #28585 | kind/question | kind/bug | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28845 | kind/question | kind/enhancement | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28713 | kind/bug | kind/enhancement | 1.00 | Caretaker agent completion |
| #28733 | kind/question | kind/bug | 1.00 | GeminiCLI.com Feedback: [ISSUE] |

**haiku@vercel** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28614 | kind/bug | kind/question | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28593 | kind/enhancement | kind/question | 1.00 | Среда автономной разработки оптимизации тестирования  через ИИ агенто… |
| #28571 | kind/bug | kind/question | 1.00 | Open Copilot в VS Code  codespace  |
| #28582 | kind/enhancement | kind/question | 1.00 | genkit |
| #28841 | kind/bug | kind/question | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28713 | kind/bug | kind/enhancement | 1.00 | Caretaker agent completion |
| #28745 | kind/question | kind/bug | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28315 | kind/bug | kind/enhancement | 1.00 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |

**jev** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28315 | kind/bug | kind/enhancement | 1.00 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #28259 | kind/bug | kind/enhancement | 0.99 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #28260 | kind/bug | kind/enhancement | 0.99 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |
| #28393 | kind/question | kind/bug | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #28745 | kind/question | kind/bug | 0.98 | GeminiCLI.com Feedback: [ISSUE] |
| #29136 | kind/question | kind/bug | 0.97 | GeminiCLI.com Feedback: [ISSUE] |
| #28258 | kind/bug | kind/enhancement | 0.97 | refactor(cli): decouple useGeminiStream from lookahead logic for para… |
| #28713 | kind/bug | kind/enhancement | 0.96 | Caretaker agent completion |

**jev@vercel** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28745 | kind/question | kind/bug | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28315 | kind/bug | kind/enhancement | 1.00 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #28260 | kind/bug | kind/enhancement | 1.00 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |
| #28259 | kind/bug | kind/enhancement | 1.00 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #29136 | kind/question | kind/bug | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28258 | kind/bug | kind/enhancement | 0.99 | refactor(cli): decouple useGeminiStream from lookahead logic for para… |
| #28713 | kind/bug | kind/enhancement | 0.98 | Caretaker agent completion |
| #28777 | kind/question | kind/enhancement | 0.96 | ticket IT support |

**kev@openrouter** (1)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28315 | kind/bug | kind/enhancement | 0.94 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |

**luna@decisions** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28745 | kind/question | kind/bug | 1.00 | GeminiCLI.com Feedback: [ISSUE] |
| #28713 | kind/bug | kind/enhancement | 1.00 | Caretaker agent completion |
| #28315 | kind/bug | kind/enhancement | 1.00 | Feature Request: Enhancing  Prompt as Code with Structured Templating… |
| #28258 | kind/bug | kind/enhancement | 1.00 | refactor(cli): decouple useGeminiStream from lookahead logic for para… |
| #28393 | kind/question | kind/bug | 0.99 | GeminiCLI.com Feedback: [ISSUE] |
| #28259 | kind/bug | kind/enhancement | 0.99 | refactor(cli): clean up profile selector logic and remove legacy conf… |
| #28260 | kind/bug | kind/enhancement | 0.99 | refactor(cli): decouple ToolGroupMessage from internal type guards an… |
| #28777 | kind/question | kind/enhancement | 0.97 | ticket IT support |


## Cases the models disagree on (12 of 46)

| id | label | clef | clef-flash | d1@vercel | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | case |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #29605 | kind/question | kind/enhancement (0.53) | kind/enhancement (0.81) | kind/enhancement (0.97) | kind/question (1.00) | kind/question (1.00) | kind/question (0.86) | kind/question (0.93) | kind/question (0.41) | kind/question (0.94) | Pull request 29482 is waiting for a review |
| #29603 | kind/question | kind/enhancement (0.83) | kind/enhancement (0.62) | kind/question (0.53) | kind/question (1.00) | kind/question (1.00) | kind/enhancement (0.73) | kind/enhancement (0.78) | kind/enhancement (0.60) | kind/enhancement (0.69) | 邀请 gemini-cli 加入 GithubStarMate，让更多人发现你的作品 |
| #29514 | kind/enhancement | kind/enhancement (0.95) | kind/enhancement (0.81) | kind/enhancement (0.73) | kind/enhancement (1.00) | kind/enhancement (1.00) | kind/enhancement (0.95) | kind/enhancement (0.95) | kind/enhancement (0.81) | kind/bug (0.77) | cache-transcript-turn-indexes |
| #29418 | kind/question | kind/enhancement (0.65) | kind/bug (0.39) | kind/bug (0.41) | kind/question (1.00) | kind/question (1.00) | kind/bug (0.44) | kind/bug (0.53) | kind/bug (0.46) | kind/enhancement (0.84) | GeminiCLI.com Feedback: [ISSUE] |
| #29389 | kind/bug | kind/enhancement (0.50) | kind/bug (0.58) | kind/enhancement (0.75) | kind/bug (1.00) | kind/bug (1.00) | kind/bug (0.84) | kind/bug (0.83) | kind/enhancement (0.57) | kind/bug (0.76) | ACP: token usage is still only in _meta.quota; PromptResponse.usage a… |
| #29356 | kind/question | kind/question (0.51) | kind/bug (0.54) | kind/bug (0.48) | kind/bug (1.00) | kind/question (1.00) | kind/bug (0.72) | kind/bug (0.63) | kind/question (0.46) | kind/question (0.62) | Extension gallery has not indexed jgs-magic-sysmlv1-read-skills (topi… |
| #29355 | kind/bug | kind/bug (0.73) | kind/bug (0.70) | kind/bug (0.82) | kind/bug (1.00) | kind/question (1.00) | kind/bug (0.95) | kind/bug (0.96) | kind/bug (0.66) | kind/bug (0.60) | GeminiCLI.com Feedback: [ISSUE] |
| #29245 | kind/question | kind/bug (0.72) | kind/question (0.42) | kind/bug (0.63) | kind/question (1.00) | kind/question (1.00) | kind/bug (0.79) | kind/bug (0.80) | kind/bug (0.54) | kind/question (0.96) | GeminiCLI.com Feedback: [ISSUE] |
| #29228 | kind/question | kind/enhancement (0.64) | kind/question (0.59) | kind/enhancement (0.64) | kind/enhancement (1.00) | kind/question (1.00) | kind/enhancement (0.77) | kind/question (0.55) | kind/enhancement (0.45) | kind/enhancement (0.94) | GeminiCLI.com Feedback: [ISSUE] |
| #29224 | kind/question | kind/question (0.40) | kind/question (0.75) | kind/question (0.76) | kind/question (1.00) | kind/question (1.00) | kind/question (0.85) | kind/question (0.85) | kind/question (0.67) | kind/enhancement (0.65) | npm install -g @google/gemini-cli@preview |
| #29221 | kind/bug | kind/bug (0.41) | kind/bug (0.39) | kind/bug (0.72) | kind/question (1.00) | kind/question (1.00) | kind/bug (0.97) | kind/bug (0.91) | kind/bug (0.48) | kind/question (0.77) | Leeres.blaat_A4-DIN |
| #29220 | kind/question | kind/bug (0.64) | kind/question (0.45) | kind/bug (0.83) | kind/question (1.00) | kind/question (1.00) | kind/bug (0.85) | kind/bug (0.71) | kind/bug (0.40) | kind/question (0.67) | 𓂀 = Wahrnehmung 👁️ ⌁ = Schwankung ⟁ = Spannung ☍ = Kontrast / Gegensp… |
