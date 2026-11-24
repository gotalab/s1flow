# gh-ruff-area

2026-11-23 · 361 labelled dev cases (linter 186, configuration 95, formatter 47, server 33) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

d1.2-ultra has the highest coverage at 95% accuracy, 89% [86, 92] (API cost $0.17 per 10k, p99 1062ms). Its interval overlaps with bison@openrouter, d1-ultra@openrouter, decider-1.3@vercel, decider@openrouter, drex-max-1.1@vercel, drex-max@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is drex-max-1.1@vercel's, 92% [89, 95].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| bison@openrouter | 361 | 88.6% [85, 92] | 0.88 | 0.99 | 0.02 | 85% [81, 88] | 94.8% (92.2%) | 0.0% (0/361) | 0/361 |
| clef-flash@openrouter | 361 | 87.8% [84, 91] | 0.86 | 0.97 | 0.03 | 75% [70, 79] | 93.3% (90.2%) | 0.0% (0/361) | 0/361 |
| clef-omni@openrouter | 361 | 88.6% [85, 92] | 0.87 | 0.98 | 0.05 | 77% [72, 81] | 94.2% (91.4%) | 0.0% (0/361) | 0/361 |
| clef@openrouter | 361 | 86.4% [83, 90] | 0.85 | 0.98 | 0.05 | 69% [65, 74] | 94.8% (91.8%) | 0.0% (0/361) | 0/361 |
| d1-ultra@openrouter | 361 | 89.8% [87, 93] | 0.90 | 0.99 | 0.03 | 85% [81, 89] | 95.5% (93.0%) | 0.0% (0/361) | 0/361 |
| d1.1@openrouter | 361 | 87.3% [84, 91] | 0.87 | 0.98 | 0.03 | 75% [71, 80] | 95.2% (92.5%) | 0.0% (0/361) | 0/361 |
| d1.2-ultra | 361 | 91.1% [88, 94] | 0.90 | 0.99 | 0.06 | 89% [86, 92] | 94.1% (91.5%) | 0.0% (0/361) | 0/361 |
| d1.2 | 361 | 86.1% [82, 90] | 0.85 | 0.98 | 0.05 | 70% [66, 75] | 95.7% (92.9%) | 0.0% (0/361) | 0/361 |
| decider-1.3@vercel | 361 | 90.6% [87, 93] | 0.90 | 0.99 | 0.03 | 89% [86, 93] | 93.8% (91.1%) | 0.0% (0/361) | 0/361 |
| decider-flash@openrouter | 361 | 85.9% [82, 89] | 0.85 | 0.98 | 0.06 | 68% [63, 73] | 94.7% (91.7%) | 0.0% (0/361) | 0/361 |
| decider@openrouter | 361 | 91.7% [89, 94] | 0.91 | 0.99 | 0.02 | 87% [83, 90] | 94.2% (91.6%) | 0.0% (0/361) | 0/361 |
| decision-1.1@openrouter | 361 | 90.6% [87, 93] | 0.91 | 0.98 | 0.05 | 76% [71, 80] | 94.9% (92.1%) | 0.0% (0/361) | 0/361 |
| decision-1@openrouter | 361 | 87.3% [84, 90] | 0.86 | 0.98 | 0.05 | 74% [70, 79] | 95.5% (92.8%) | 0.0% (0/361) | 0/361 |
| drex-max-1.1@vercel | 361 | 92.0% [89, 95] | 0.92 | 0.99 | 0.02 | 89% [86, 92] | 94.7% (92.2%) | 0.0% (0/361) | 0/361 |
| drex-max@openrouter | 361 | 90.6% [88, 93] | 0.90 | 0.99 | 0.03 | 88% [84, 91] | 95.0% (92.4%) | 0.0% (0/361) | 0/361 |
| elephant@openrouter | 361 | 86.1% [82, 89] | 0.84 | 0.98 | 0.04 | 71% [66, 76] | 95.3% (92.5%) | 0.0% (0/361) | 0/361 |
| gemini-decision@google | 361 | 86.4% [83, 90] | 0.86 | 0.99 | 0.03 | 76% [72, 81] | 95.3% (92.6%) | 0.0% (0/361) | 0/361 |
| groundhog@openrouter | 361 | 85.0% [81, 89] | 0.83 | 0.98 | 0.04 | 73% [68, 77] | 94.7% (91.8%) | 0.0% (0/361) | 0/361 |
| heygen-decision@openrouter | 361 | 85.0% [81, 89] | 0.84 | 0.98 | 0.07 | 71% [66, 76] | 94.2% (91.2%) | 0.0% (0/361) | 0/361 |
| jev:1.14 | 361 | 85.3% [82, 89] | 0.83 | 0.98 | 0.07 | 76% [72, 81] | 94.9% (92.2%) | 0.0% (0/361) | 0/361 |
| joey@openrouter | 361 | 77.6% [73, 82] | 0.72 | 0.94 | 0.03 | 36% [31, 41] | 92.3% (87.3%) | 0.0% (0/361) | 0/361 |
| kev@openrouter | 361 | 81.4% [77, 85] | 0.78 | 0.97 | 0.16 | 70% [65, 75] | 94.0% (91.0%) | 0.0% (0/361) | 0/361 |
| luna@decisions | 361 | 88.4% [85, 91] | 0.88 | 0.98 | 0.07 | 73% [69, 78] | 94.7% (91.9%) | 0.0% (0/361) | 0/361 |
| mammoth@openrouter | 361 | 90.3% [87, 93] | 0.90 | 0.99 | 0.02 | 87% [83, 90] | 94.6% (92.0%) | 0.0% (0/361) | 0/361 |
| mo@vercel | 361 | 90.0% [87, 93] | 0.90 | 0.99 | 0.04 | 87% [83, 90] | 94.6% (92.0%) | 0.0% (0/361) | 0/361 |
| reflex@openrouter | 361 | 91.1% [88, 94] | 0.91 | 0.99 | 0.06 | 82% [78, 86] | 95.3% (92.7%) | 0.0% (0/361) | 0/361 |
| span@openrouter | 361 | 88.9% [86, 92] | 0.88 | 0.98 | 0.05 | 83% [79, 87] | 95.0% (92.4%) | 0.0% (0/361) | 0/361 |

Answered by: bison@openrouter = baseten/bison-1-20261120; clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2-ultra = d1.2-ultra; d1.2 = d1.2; decider-1.3@vercel = perplexity/pplx-decider-v1.3; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max-1.1@vercel = nace-ai/drex-max-v1.1; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; groundhog@openrouter = baseten/groundhog-1-20261120; heygen-decision@openrouter = heygen/heygen-decision-1-20261112; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mo@vercel = modaic/mo; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| bison@openrouter = | 85% [81, 88] | 0.71 | met |
| d1-ultra@openrouter = | 85% [81, 89] | 0.69 | met |
| d1.2-ultra = | 89% [86, 92] | 0.65 | met |
| decider-1.3@vercel = | 89% [86, 93] | 0.81 | met |
| decider@openrouter = | 87% [83, 90] | 0.78 | met |
| drex-max-1.1@vercel = | 89% [86, 92] | 0.70 | met |
| drex-max@openrouter = | 88% [84, 91] | 0.72 | met |
| mammoth@openrouter = | 87% [83, 90] | 0.76 | met |
| mo@vercel = | 87% [83, 90] | 0.84 | met |
| reflex@openrouter = | 82% [78, 86] | 0.92 | met |
| span@openrouter = | 83% [79, 87] | 0.86 | met |
| clef-omni@openrouter | 77% [72, 81] | 0.78 | met |
| gemini-decision@google | 76% [72, 81] | 0.77 | met |
| jev:1.14 | 76% [72, 81] | 0.87 | met |
| decision-1.1@openrouter | 76% [71, 80] | 0.89 | met |
| d1.1@openrouter | 75% [71, 80] | 0.86 | met |
| clef-flash@openrouter | 75% [70, 79] | 0.82 | met |
| decision-1@openrouter | 74% [70, 79] | 0.91 | met |
| luna@decisions | 73% [69, 78] | 0.99 | met |
| groundhog@openrouter | 73% [68, 77] | 0.80 | met |
| elephant@openrouter | 71% [66, 76] | 0.87 | met |
| heygen-decision@openrouter | 71% [66, 76] | 0.93 | met |
| d1.2 | 70% [66, 75] | 0.82 | met |
| kev@openrouter | 70% [65, 75] | 0.58 | met |
| clef@openrouter | 69% [65, 74] | 0.90 | met |
| decider-flash@openrouter | 68% [63, 73] | 0.91 | met |
| joey@openrouter | 36% [31, 41] | 0.91 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bison@openrouter | 361 | 238 ms | 397 ms | 493 ms | 536 ms | 2.1 | 0 | 2 | $0.49 | billed |  |
| clef-flash@openrouter | 361 | 277 ms | 524 ms | 1229 ms | 1598 ms | 4.4 | 0 | 4 | $0.13 | billed |  |
| clef-omni@openrouter | 361 | 181 ms | 217 ms | 321 ms | 882 ms | 1.8 | 0 | 4 | $0.76 | billed | ○ |
| clef@openrouter | 361 | 298 ms | 729 ms | 4400 ms | 9104 ms | 14.8 | 0 | 4 | $1.10 | billed |  |
| d1-ultra@openrouter | 361 | 232 ms | 386 ms | 1041 ms | 1954 ms | 4.5 | 0 | 4 | $0.17 | billed |  |
| d1.1@openrouter | 361 | 297 ms | 503 ms | 689 ms | 3162 ms | 2.3 | 0 | 4 | $0.08 | billed |  |
| d1.2-ultra | 361 | 145 ms | 389 ms | 1062 ms | 3753 ms | 7.3 | 0 | 4 | $0.17 | billed |  |
| d1.2 | 361 | 112 ms | 168 ms | 611 ms | 1127 ms | 5.5 | 0 | 4 | $0.08 | billed |  |
| decider-1.3@vercel | 361 | 369 ms | 507 ms | 1071 ms | 1860 ms | 2.9 | 0 | 4 | $0.09 | billed | ○ |
| decider-flash@openrouter | 361 | 137 ms | 166 ms | 410 ms | 481 ms | 3.0 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 0 | — | — | — | — | — | — | — | $0.09 | billed |  |
| decision-1.1@openrouter | 361 | 223 ms | 255 ms | 325 ms | 514 ms | 1.5 | 0 | 4 | $0.18 | billed | ○ |
| decision-1@openrouter | 361 | 232 ms | 301 ms | 380 ms | 457 ms | 1.6 | 0 | 4 | $0.17 | billed |  |
| drex-max-1.1@vercel | 361 | 338 ms | 425 ms | 807 ms | 1276 ms | 2.4 | 0 | 4 | $0.14 | billed | ○ |
| drex-max@openrouter | 361 | 230 ms | 324 ms | 562 ms | 864 ms | 2.4 | 0 | 4 | $0.28 | billed | ○ |
| elephant@openrouter | 361 | 167 ms | 189 ms | 255 ms | 369 ms | 1.5 | 0 | 4 | $0.16 | billed | ○ |
| gemini-decision@google | 361 | 265 ms | 375 ms | 409 ms | 593 ms | 1.5 | 0 | 4 | $0.49 | estimated |  |
| groundhog@openrouter | 361 | 228 ms | 313 ms | 514 ms | 674 ms | 2.3 | 0 | 2 | $0.17 | billed |  |
| heygen-decision@openrouter | 361 | 312 ms | 617 ms | 2792 ms | 3520 ms | 8.9 | 0 | 4 | $0.50 | billed |  |
| jev:1.14 | 361 | 110 ms | 140 ms | 206 ms | 416 ms | 1.9 | 0 | 4 | $0.29 | estimated | ○ |
| joey@openrouter | 361 | 165 ms | 189 ms | 238 ms | 377 ms | 1.4 | 0 | 4 | $0.05 | billed | ○ |
| kev@openrouter | 361 | 644 ms | 920 ms | 1292 ms | 1535 ms | 2.0 | 0 | 4 | $0.16 | billed |  |
| luna@decisions | 361 | 185 ms | 350 ms | 502 ms | 687 ms | 2.7 | 0 | 4 | $0.47 | estimated |  |
| mammoth@openrouter | 361 | 187 ms | 241 ms | 492 ms | 546 ms | 2.6 | 81 | 4 | $0.47 | billed | ○ |
| mo@vercel | 361 | 337 ms | 422 ms | 599 ms | 895 ms | 1.8 | 0 | 4 | $0.19 | billed | ○ |
| reflex@openrouter | 361 | 249 ms | 286 ms | 345 ms | 494 ms | 1.4 | 0 | 4 | $0.20 | billed | ○ |
| span@openrouter | 361 | 194 ms | 267 ms | 372 ms | 516 ms | 1.9 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: bison@openrouter, clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2-ultra, d1.2, decider-1.3@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max-1.1@vercel, drex-max@openrouter, elephant@openrouter, groundhog@openrouter, heygen-decision@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mo@vercel, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| bison@openrouter | $0.02 | 47 s (estimated, 361 calls) | 22 min | 2 |
| clef-flash@openrouter | $0.0045 | 30 s (estimated, 361 calls) | 14 min | 4 |
| clef-omni@openrouter | $0.03 | 17 s (estimated, 361 calls) | 8 min | 4 |
| clef@openrouter | $0.04 | 48 s (estimated, 361 calls) | 22 min | 4 |
| d1-ultra@openrouter | $0.0061 | 25 s (estimated, 361 calls) | 11 min | 4 |
| d1.1@openrouter | $0.0029 | 30 s (estimated, 361 calls) | 14 min | 4 |
| d1.2-ultra | $0.0061 | 20 s (estimated, 361 calls) | 9 min | 4 |
| d1.2 | $0.0029 | 13 s (estimated, 361 calls) | 6 min | 4 |
| decider-1.3@vercel | $0.0032 | 36 s (estimated, 361 calls) | 17 min | 4 |
| decider-flash@openrouter | $0.0017 | 13 s (estimated, 361 calls) | 6 min | 4 |
| decision-1.1@openrouter | $0.0065 | 21 s (estimated, 361 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0060 | 22 s (estimated, 361 calls) | 10 min | 4 |
| drex-max-1.1@vercel | $0.0050 | 33 s (estimated, 361 calls) | 15 min | 4 |
| drex-max@openrouter | $0.0100 | 22 s (estimated, 361 calls) | 10 min | 4 |
| elephant@openrouter | $0.0059 | 15 s (estimated, 361 calls) | 7 min | 4 |
| gemini-decision@google | $0.02 | 25 s (estimated, 361 calls) | 12 min | 4 |
| groundhog@openrouter | $0.0062 | 45 s (estimated, 361 calls) | 21 min | 2 |
| heygen-decision@openrouter | $0.02 | 38 s (estimated, 361 calls) | 17 min | 4 |
| jev:1.14 | $0.01 | 10 s (estimated, 361 calls) | 5 min | 4 |
| joey@openrouter | $0.0017 | 15 s (estimated, 361 calls) | 7 min | 4 |
| kev@openrouter | $0.0057 | 62 s (estimated, 361 calls) | 29 min | 4 |
| luna@decisions | $0.02 | 21 s (estimated, 361 calls) | 9 min | 4 |
| mammoth@openrouter | $0.02 | 18 s (estimated, 361 calls) | 8 min | 4 |
| mo@vercel | $0.0068 | 32 s (estimated, 361 calls) | 15 min | 4 |
| reflex@openrouter | $0.0071 | 23 s (estimated, 361 calls) | 11 min | 4 |
| span@openrouter | $0.0018 | 19 s (estimated, 361 calls) | 9 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Wrong at a high probability (0.9 or more)

**bison@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |

**clef-flash@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#6847 | configuration | server | 0.99 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| #23855 | formatter | server | 0.96 | Ruff: Format document with an open markdown file results in an error |
| prod:#20280 | configuration | linter | 0.94 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 0.92 | [Infinite loop] TID254 when an import statement has conflicting lazin… |

**clef-omni@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 0.93 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #23855 | formatter | server | 0.93 | Ruff: Format document with an open markdown file results in an error |
| #24409 | linter | formatter | 0.92 | [Fix error] Fix for E502 introduces syntax error |
| prod:#1773 | linter | configuration | 0.90 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| #27224 | configuration | linter | 0.90 | SIM118 complains about .keys() even when the object isn't a dict |

**clef@openrouter** (13)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #24528 | linter | formatter | 0.98 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #27602 | configuration | formatter | 0.97 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#9132 | configuration | formatter | 0.96 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |
| prod:#13419 | configuration | formatter | 0.96 | {"title": "provide a exit code for `ruff format` (without --check) fo… |
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#17679 | configuration | formatter | 0.96 | {"title": "Allow formatting only changed blocks (git)", "body": "It w… |

**d1-ultra@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.96 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#18310 | configuration | linter | 0.92 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#20280 | configuration | linter | 0.91 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |

**d1.1@openrouter** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#8248 | linter | configuration | 0.97 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| prod:#20280 | configuration | linter | 0.96 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18310 | configuration | linter | 0.95 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #23855 | formatter | server | 0.92 | Ruff: Format document with an open markdown file results in an error |
| prod:#18728 | configuration | linter | 0.92 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |
| #24845 | configuration | linter | 0.91 | Allow configuring some exception types to be ignored by B904 |

**d1.2-ultra** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.96 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#8248 | linter | configuration | 0.91 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |

**d1.2** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.97 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.97 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.95 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18728 | configuration | linter | 0.92 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |

**decider-1.3@vercel** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#8248 | linter | configuration | 0.99 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| prod:#18310 | configuration | linter | 0.98 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#14984 | formatter | linter | 0.96 | {"title": "`docstring-code-line-length = \"dynamic\"` not Working Cor… |

**decider-flash@openrouter** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#7804 | configuration | linter | 0.96 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| prod:#9132 | configuration | formatter | 0.96 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |
| #27602 | configuration | formatter | 0.96 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#13419 | configuration | formatter | 0.95 | {"title": "provide a exit code for `ruff format` (without --check) fo… |
| #27647 | configuration | linter | 0.94 | collapsible-if rule obscures conditional structure |

**decider@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#18310 | configuration | linter | 0.98 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#8248 | linter | configuration | 0.94 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |

**decision-1.1@openrouter** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18310 | configuration | linter | 1.00 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #26418 | formatter | linter | 0.98 | Ability to suppress PEP 758 check |
| prod:#17028 | configuration | linter | 0.97 | {"title": "`unconventional-import-alias (ICN001)`: Add `import numpy.… |
| #24955 | configuration | linter | 0.97 | [pydocstyle] allow configuring indentation level for Google style |
| prod:#17572 | formatter | server | 0.95 | {"title": "Cursor jumps to end of file when formatting files with lar… |

**decision-1@openrouter** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #23855 | formatter | server | 0.99 | Ruff: Format document with an open markdown file results in an error |
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#7804 | configuration | linter | 0.97 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| prod:#6847 | configuration | server | 0.96 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| #26480 | configuration | linter | 0.96 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| prod:#19421 | configuration | linter | 0.94 | {"title": "Failure to create cache key on invalid symlink", "body": "… |

**drex-max-1.1@vercel** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#18310 | configuration | linter | 0.97 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#20280 | configuration | linter | 0.96 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#8248 | linter | configuration | 0.96 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| #23855 | formatter | server | 0.93 | Ruff: Format document with an open markdown file results in an error |

**drex-max@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#18310 | configuration | linter | 0.97 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #24528 | linter | formatter | 0.97 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#8248 | linter | configuration | 0.97 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| prod:#20280 | configuration | linter | 0.96 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#1773 | linter | configuration | 0.91 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |

**elephant@openrouter** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27602 | configuration | formatter | 0.99 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #24528 | linter | formatter | 0.95 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#6847 | configuration | server | 0.95 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| prod:#7804 | configuration | linter | 0.95 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| prod:#17679 | configuration | formatter | 0.91 | {"title": "Allow formatting only changed blocks (git)", "body": "It w… |

**gemini-decision@google** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #23855 | formatter | server | 0.92 | Ruff: Format document with an open markdown file results in an error |

**groundhog@openrouter** (6)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#15911 | configuration | linter | 0.96 | {"title": "Import alias settings of I002 and ICN001 conflict even whe… |
| #24528 | linter | formatter | 0.93 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #27602 | configuration | formatter | 0.91 | `ruff format --check` uses same exit code for syntax errors in files,… |

**heygen-decision@openrouter** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18310 | configuration | linter | 0.98 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #27602 | configuration | formatter | 0.95 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#18728 | configuration | linter | 0.95 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |
| prod:#17028 | configuration | linter | 0.95 | {"title": "`unconventional-import-alias (ICN001)`: Add `import numpy.… |
| prod:#14984 | formatter | linter | 0.94 | {"title": "`docstring-code-line-length = \"dynamic\"` not Working Cor… |

**jev:1.14** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #27602 | configuration | formatter | 0.99 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #27647 | configuration | linter | 0.98 | collapsible-if rule obscures conditional structure |
| prod:#17679 | configuration | formatter | 0.97 | {"title": "Allow formatting only changed blocks (git)", "body": "It w… |
| prod:#18349 | configuration | linter | 0.95 | {"title": "Warn about error being related to a deprecated rule", "bod… |
| #24528 | linter | formatter | 0.95 | `ruff format --check` outputs wrong line line/column numbers on synta… |

**joey@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18449 | configuration | linter | 0.95 | {"title": "Block fixes on a repo with uncommitted files?", "body": "H… |
| prod:#7804 | configuration | linter | 0.95 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| prod:#14984 | formatter | linter | 0.94 | {"title": "`docstring-code-line-length = \"dynamic\"` not Working Cor… |
| #27224 | configuration | linter | 0.93 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#11789 | formatter | linter | 0.91 | {"title": "(🎁) format `type: ignore` and other pragmas", "body": "```… |
| prod:#11107 | configuration | linter | 0.90 | {"title": "Ruff should give a nonzero exit code if file linting panic… |
| #26450 | configuration | linter | 0.90 | [Infinite loop] TID254 when an import statement has conflicting lazin… |

**luna@decisions** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26480 | configuration | linter | 1.00 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| #27602 | configuration | formatter | 1.00 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #27647 | configuration | linter | 1.00 | collapsible-if rule obscures conditional structure |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18349 | configuration | linter | 1.00 | {"title": "Warn about error being related to a deprecated rule", "bod… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#9132 | configuration | formatter | 0.99 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |

**mammoth@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #23855 | formatter | server | 0.97 | Ruff: Format document with an open markdown file results in an error |
| #24955 | configuration | linter | 0.90 | [pydocstyle] allow configuring indentation level for Google style |

**mo@vercel** (9)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18310 | configuration | linter | 0.98 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#8248 | linter | configuration | 0.96 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| prod:#17028 | configuration | linter | 0.95 | {"title": "`unconventional-import-alias (ICN001)`: Add `import numpy.… |
| prod:#18728 | configuration | linter | 0.94 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |
| #23855 | formatter | server | 0.92 | Ruff: Format document with an open markdown file results in an error |

**reflex@openrouter** (16)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #24528 | linter | formatter | 0.99 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#8248 | linter | configuration | 0.99 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| #23855 | formatter | server | 0.97 | Ruff: Format document with an open markdown file results in an error |
| prod:#1773 | linter | configuration | 0.97 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| prod:#18310 | configuration | linter | 0.97 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |

**span@openrouter** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #27177 | configuration | linter | 0.98 | Please remove all rules without an automated fix from default rules |
| #23855 | formatter | server | 0.96 | Ruff: Format document with an open markdown file results in an error |
| prod:#14984 | formatter | linter | 0.94 | {"title": "`docstring-code-line-length = \"dynamic\"` not Working Cor… |
| prod:#1773 | linter | configuration | 0.93 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| prod:#15911 | configuration | linter | 0.92 | {"title": "Import alias settings of I002 and ICN001 conflict even whe… |


## Cases the models disagree on (12 of 116)

| id | label | bison@openrouter | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2-ultra | d1.2 | decider-1.3@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max-1.1@vercel | drex-max@openrouter | elephant@openrouter | gemini-decision@google | groundhog@openrouter | heygen-decision@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mo@vercel | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #23530 | linter | linter (0.93) | linter (0.75) | formatter (0.60) | linter (0.95) | linter (0.92) | linter (0.87) | linter (0.92) | linter (0.87) | linter (0.96) | linter (0.96) | linter (0.98) | linter (0.99) | linter (0.94) | linter (0.95) | linter (0.98) | linter (0.92) | linter (0.98) | linter (0.86) | linter (0.86) | linter (0.92) | formatter (0.60) | formatter (0.44) | linter (1.00) | linter (0.97) | linter (0.97) | linter (0.97) | linter (0.95) | `RET` autofixers should introduce newlines to preserve readability |
| #23590 | linter | configuration (0.55) | linter (0.62) | configuration (0.47) | linter (0.94) | linter (0.65) | linter (0.80) | linter (0.54) | linter (0.83) | linter (0.60) | configuration (0.53) | linter (0.63) | linter (0.88) | linter (0.96) | linter (0.54) | configuration (0.54) | linter (0.71) | linter (0.72) | linter (0.77) | linter (0.59) | configuration (0.79) | linter (0.48) | formatter (0.33) | linter (1.00) | linter (0.80) | linter (0.81) | linter (0.84) | linter (0.84) | `ruff` should respect `pyproject.toml` existence for first-party scra… |
| #24031 | linter | linter (0.96) | linter (0.84) | linter (0.85) | linter (0.91) | linter (0.97) | linter (0.99) | linter (0.94) | linter (0.95) | linter (1.00) | linter (0.97) | linter (0.99) | linter (1.00) | linter (0.99) | linter (0.98) | linter (1.00) | linter (0.99) | linter (1.00) | linter (0.92) | linter (0.99) | linter (1.00) | formatter (0.48) | linter (0.65) | linter (1.00) | linter (0.98) | linter (1.00) | linter (1.00) | linter (0.99) | Mismatching number of %-placeholders in string formatting |
| #24409 | linter | linter (0.95) | formatter (0.56) | formatter (0.92) | linter (0.97) | linter (0.96) | linter (0.97) | linter (0.91) | linter (0.89) | linter (0.99) | linter (0.94) | linter (0.98) | linter (1.00) | linter (0.98) | linter (0.98) | linter (0.99) | linter (0.90) | linter (1.00) | linter (0.96) | linter (0.99) | linter (0.85) | linter (0.73) | formatter (0.40) | linter (1.00) | linter (0.99) | linter (0.99) | linter (1.00) | linter (0.98) | [Fix error] Fix for E502 introduces syntax error |
| #24420 | server | server (0.89) | server (0.99) | server (0.98) | server (0.99) | server (0.94) | server (0.95) | server (0.92) | server (0.91) | server (0.96) | server (0.97) | server (0.96) | server (1.00) | server (0.99) | server (0.91) | server (0.95) | server (0.96) | server (0.94) | server (0.89) | server (0.96) | server (0.98) | configuration (0.47) | server (0.64) | server (1.00) | server (0.88) | server (0.98) | server (0.99) | server (0.99) | [LSP] `"settings.configurationPreference: "filesystemFirst"` doesn't … |
| #24548 | linter | linter (0.81) | linter (0.71) | linter (0.56) | linter (0.67) | linter (0.86) | linter (0.82) | configuration (0.48) | linter (0.80) | linter (0.68) | linter (0.92) | linter (0.73) | linter (0.80) | linter (0.98) | linter (0.68) | linter (0.66) | linter (0.97) | linter (0.90) | linter (0.82) | linter (0.99) | linter (0.98) | linter (0.83) | linter (0.51) | linter (1.00) | linter (0.89) | linter (0.88) | linter (0.84) | linter (0.97) | Default ruff check output is extremely slow on large E303-heavy files |
| #24829 | configuration | configuration (0.96) | configuration (0.82) | configuration (0.91) | configuration (0.79) | configuration (0.88) | configuration (0.87) | configuration (0.88) | configuration (0.78) | configuration (0.97) | configuration (0.96) | configuration (0.95) | configuration (0.54) | configuration (0.85) | configuration (0.96) | configuration (0.97) | configuration (0.97) | configuration (0.82) | configuration (0.70) | configuration (0.97) | configuration (0.96) | linter (0.55) | configuration (0.71) | configuration (1.00) | configuration (0.93) | configuration (0.94) | configuration (0.97) | configuration (0.94) | ruff ignoring `requires-python` in `pyproject.toml` when missing `[to… |
| #25105 | linter | linter (0.95) | linter (0.74) | formatter (0.47) | linter (0.92) | linter (0.98) | linter (0.99) | linter (0.95) | linter (0.96) | linter (1.00) | linter (0.88) | linter (1.00) | linter (1.00) | linter (0.98) | linter (0.99) | linter (1.00) | linter (0.94) | linter (0.99) | linter (0.95) | linter (0.97) | linter (0.99) | linter (0.67) | linter (0.59) | linter (1.00) | linter (0.98) | linter (0.99) | linter (1.00) | linter (1.00) | `pyupgrade` should rewrite `abc.{abstractclassmethod, abstractstaticm… |
| #25114 | configuration | configuration (0.96) | configuration (0.83) | configuration (0.86) | configuration (0.83) | configuration (0.89) | configuration (0.89) | configuration (0.88) | configuration (0.81) | configuration (0.99) | configuration (0.86) | configuration (0.98) | configuration (0.79) | configuration (0.96) | configuration (0.97) | configuration (0.98) | configuration (0.96) | configuration (0.88) | configuration (0.78) | configuration (0.94) | configuration (1.00) | linter (0.73) | configuration (0.60) | configuration (1.00) | configuration (0.98) | configuration (0.99) | configuration (1.00) | configuration (0.96) | `requires-python` discovery is inconsistent with config file discovery |
| #25281 | formatter | formatter (0.89) | formatter (0.90) | formatter (0.94) | formatter (0.96) | formatter (0.83) | formatter (0.82) | formatter (0.89) | formatter (0.82) | formatter (0.97) | formatter (0.84) | formatter (0.96) | formatter (0.73) | formatter (0.90) | formatter (0.93) | formatter (0.98) | formatter (0.87) | formatter (0.63) | formatter (0.88) | formatter (0.97) | formatter (0.89) | linter (0.61) | formatter (0.63) | formatter (1.00) | formatter (0.95) | formatter (0.98) | formatter (0.99) | formatter (0.97) | Support pycon formatting in docstrings |
| #26320 | linter | linter (0.64) | linter (0.89) | linter (0.74) | linter (0.67) | configuration (0.53) | linter (0.66) | configuration (0.69) | linter (0.85) | linter (0.56) | linter (0.95) | linter (0.67) | linter (0.58) | linter (0.89) | linter (0.57) | configuration (0.60) | linter (0.84) | linter (0.83) | linter (0.72) | linter (0.93) | linter (0.93) | linter (0.84) | linter (0.60) | linter (1.00) | linter (0.53) | linter (0.51) | linter (0.87) | configuration (0.67) | Option to opt in to showing error codes or show error codes in additi… |
| #26451 | linter | linter (0.87) | linter (0.85) | configuration (0.43) | linter (0.89) | linter (0.80) | linter (0.92) | linter (0.82) | linter (0.89) | linter (0.96) | linter (0.87) | linter (0.95) | linter (0.99) | linter (0.99) | linter (0.96) | linter (0.91) | linter (0.87) | linter (0.91) | linter (0.73) | linter (0.94) | linter (0.96) | formatter (0.69) | linter (0.38) | linter (1.00) | linter (0.89) | linter (0.99) | linter (0.99) | linter (0.83) | TD004: Support additional TODO comment formats |
