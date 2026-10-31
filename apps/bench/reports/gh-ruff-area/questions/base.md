# gh-ruff-area

2026-10-31 · 361 labelled dev cases (linter 186, configuration 95, formatter 47, server 33) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**d1-ultra@openrouter** has the highest coverage at 95% accuracy, 88% [84, 91] (API cost $0.17 per 10k, p99 5844ms). Its interval overlaps with decider@openrouter, drex-max@openrouter, mammoth@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is mammoth@openrouter's, 91% [88, 93].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 361 | 88.4% [85, 91] | 0.86 | 0.97 | 0.04 | 76% [71, 80] | 94.9% (92.1%) | 0/361 | 0/361 |
| clef@openrouter | 361 | 85.6% [82, 89] | 0.84 | 0.98 | 0.05 | 69% [64, 73] | 94.8% (91.8%) | 0/361 | 0/361 |
| d1-ultra@openrouter | 361 | 90.0% [87, 93] | 0.89 | 0.99 | 0.04 | 88% [84, 91] | 94.0% (91.3%) | 0/361 | 0/361 |
| d1.1@openrouter | 361 | 87.0% [84, 90] | 0.86 | 0.98 | 0.05 | 74% [69, 78] | 95.5% (92.8%) | 0/361 | 0/361 |
| d1@vercel | 361 | 84.8% [81, 88] | 0.83 | 0.98 | 0.06 | 75% [70, 79] | 94.8% (92.0%) | 0/361 | 0/361 |
| decider-flash@openrouter | 361 | 84.2% [80, 88] | 0.82 | 0.97 | 0.06 | 68% [63, 73] | 94.7% (91.8%) | 0/361 | 0/361 |
| decider@openrouter | 361 | 90.3% [87, 93] | 0.89 | 0.98 | 0.02 | 85% [82, 89] | 94.5% (91.8%) | 0/361 | 0/361 |
| decision-1@openrouter | 361 | 86.7% [83, 90] | 0.86 | 0.98 | 0.05 | 75% [70, 79] | 94.8% (92.0%) | 0/361 | 0/361 |
| drex-max@openrouter | 361 | 90.3% [87, 93] | 0.90 | 0.99 | 0.03 | 87% [83, 90] | 95.5% (93.1%) | 0/361 | 0/361 |
| elephant@openrouter | 361 | 86.4% [83, 90] | 0.84 | 0.98 | 0.03 | 75% [70, 80] | 93.7% (90.7%) | 0/361 | 0/361 |
| flash-lite@vercel ※ | 361 | 85.9% [82, 89] | 0.84 | 0.89 | 0.14 | 0% [0, 0] | — (0.0%) | 0/361 | 0/361 |
| haiku@vercel ※ | 361 | 87.8% [84, 91] | 0.88 | 0.91 | 0.12 | 0% [0, 0] | — (0.0%) | 0/361 | 0/361 |
| jev:1.14 | 361 | 85.0% [81, 88] | 0.82 | 0.97 | 0.07 | 75% [71, 80] | 94.9% (92.1%) | 0/361 | 0/361 |
| joey@openrouter | 361 | 78.7% [74, 83] | 0.74 | 0.94 | 0.05 | 44% [39, 50] | 95.0% (91.2%) | 0/361 | 0/361 |
| kev@openrouter | 361 | 80.3% [77, 84] | 0.77 | 0.96 | 0.16 | 64% [59, 69] | 94.4% (91.2%) | 0/361 | 0/361 |
| luna@decisions | 361 | 86.7% [83, 90] | 0.85 | 0.97 | 0.08 | 73% [69, 78] | 94.7% (91.9%) | 0/361 | 0/361 |
| mammoth@openrouter | 361 | 90.9% [88, 93] | 0.90 | 0.99 | 0.02 | 86% [82, 89] | 95.2% (92.6%) | 0/361 | 0/361 |
| mercury@openrouter | 361 | 85.3% [82, 89] | 0.84 | 0.98 | 0.10 | 72% [67, 76] | 95.4% (92.6%) | 0/361 | 0/361 |
| span@openrouter | 361 | 88.4% [85, 91] | 0.87 | 0.98 | 0.06 | 80% [75, 84] | 94.4% (91.7%) | 0/361 | 0/361 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.5-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-5.5; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| d1-ultra@openrouter = | 88% [84, 91] | 0.70 | met |
| decider@openrouter = | 85% [82, 89] | 0.76 | met |
| drex-max@openrouter = | 87% [83, 90] | 0.72 | met |
| mammoth@openrouter = | 86% [82, 89] | 0.75 | met |
| span@openrouter | 80% [75, 84] | 0.90 | met |
| clef-flash@openrouter | 76% [71, 80] | 0.83 | met |
| jev:1.14 | 75% [71, 80] | 0.92 | met |
| elephant@openrouter | 75% [70, 80] | 0.86 | met |
| d1@vercel | 75% [70, 79] | 0.87 | met |
| decision-1@openrouter | 75% [70, 79] | 0.89 | met |
| d1.1@openrouter | 74% [69, 78] | 0.88 | met |
| luna@decisions | 73% [69, 78] | 0.98 | met |
| mercury@openrouter | 72% [67, 76] | 0.97 | met |
| clef@openrouter | 69% [64, 73] | 0.91 | met |
| decider-flash@openrouter | 68% [63, 73] | 0.91 | met |
| kev@openrouter | 64% [59, 69] | 0.59 | met |
| joey@openrouter | 44% [39, 50] | 0.87 | met |
| flash-lite@vercel | 0% [0, 0] | — | met |
| haiku@vercel | 0% [0, 0] | — | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 361 | 386 ms | 530 ms | 812 ms | 893 ms | 2.1 | 0 | 8 | $0.11 | billed | ○ |
| clef@openrouter | 361 | 1480 ms | 2242 ms | 6219 ms | 8795 ms | 4.2 | 0 | 8 | $1.12 | billed |  |
| d1-ultra@openrouter | 361 | 1346 ms | 2308 ms | 5844 ms | 8359 ms | 4.3 | 0 | 8 | $0.17 | billed | ○ |
| d1.1@openrouter | 361 | 1318 ms | 3035 ms | 6542 ms | 11215 ms | 5.0 | 0 | 8 | $0.08 | billed |  |
| d1@vercel | 361 | 211 ms | 285 ms | 524 ms | 1112 ms | 2.5 | 0 | 8 | $0.08 | billed | ○ |
| decider-flash@openrouter | 361 | 1246 ms | 2280 ms | 6436 ms | 11225 ms | 5.2 | 0 | 8 | $0.05 | billed | ○ |
| decider@openrouter | 361 | 1341 ms | 2462 ms | 5871 ms | 8488 ms | 4.4 | 0 | 8 | $0.09 | billed | ○ |
| decision-1@openrouter | 361 | 1434 ms | 2148 ms | 5293 ms | 6788 ms | 3.7 | 0 | 8 | $0.17 | billed |  |
| drex-max@openrouter | 361 | 1566 ms | 2407 ms | 4441 ms | 5807 ms | 2.8 | 4 | 8 | $0.28 | billed | ○ |
| elephant@openrouter | 361 | 1304 ms | 2359 ms | 6314 ms | 8254 ms | 4.8 | 0 | 8 | $0.16 | billed |  |
| flash-lite@vercel | 361 | 1204 ms | 2259 ms | 5388 ms | 8489 ms | 4.5 | 0 | 8 | $1.87 | estimated |  |
| haiku@vercel | 361 | 1297 ms | 2542 ms | 4667 ms | 6873 ms | 3.6 | 0 | 8 | $1.05 | estimated |  |
| jev:1.14 | 361 | 1264 ms | 2186 ms | 6175 ms | 12074 ms | 4.9 | 0 | 8 | $0.29 | estimated |  |
| joey@openrouter | 361 | 1318 ms | 2761 ms | 7095 ms | 11390 ms | 5.4 | 0 | 8 | $0.05 | billed |  |
| kev@openrouter | 361 | 1489 ms | 2486 ms | 6103 ms | 11040 ms | 4.1 | 0 | 8 | $0.16 | billed |  |
| luna@decisions | 361 | 1420 ms | 2495 ms | 6380 ms | 8415 ms | 4.5 | 0 | 8 | $0.47 | estimated |  |
| mammoth@openrouter | 361 | 1366 ms | 2254 ms | 5390 ms | 8277 ms | 3.9 | 0 | 8 | $0.47 | billed |  |
| mercury@openrouter | 361 | 1451 ms | 2259 ms | 5737 ms | 8565 ms | 4.0 | 0 | 8 | $0.09 | billed |  |
| span@openrouter | 361 | 1347 ms | 2359 ms | 5951 ms | 8465 ms | 4.4 | 0 | 8 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): flash-lite@vercel, haiku@vercel, jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0041 | 18 s (estimated, 361 calls) | 8 min | 8 |
| clef@openrouter | $0.04 | 76 s (estimated, 361 calls) | 35 min | 8 |
| d1-ultra@openrouter | $0.0061 | 72 s (estimated, 361 calls) | 33 min | 8 |
| d1.1@openrouter | $0.0029 | 76 s (estimated, 361 calls) | 35 min | 8 |
| d1@vercel | $0.0029 | 10 s (estimated, 361 calls) | 5 min | 8 |
| decider-flash@openrouter | $0.0017 | 72 s (estimated, 361 calls) | 33 min | 8 |
| decider@openrouter | $0.0033 | 74 s (estimated, 361 calls) | 34 min | 8 |
| decision-1@openrouter | $0.0060 | 72 s (estimated, 361 calls) | 33 min | 8 |
| drex-max@openrouter | $0.0100 | 74 s (estimated, 361 calls) | 34 min | 8 |
| elephant@openrouter | $0.0059 | 72 s (estimated, 361 calls) | 33 min | 8 |
| flash-lite@vercel | $0.07 | 66 s (estimated, 361 calls) | 30 min | 8 |
| haiku@vercel | $0.04 | 72 s (estimated, 361 calls) | 33 min | 8 |
| jev:1.14 | $0.01 | 68 s (estimated, 361 calls) | 32 min | 8 |
| joey@openrouter | $0.0017 | 75 s (estimated, 361 calls) | 34 min | 8 |
| kev@openrouter | $0.0057 | 76 s (estimated, 361 calls) | 35 min | 8 |
| luna@decisions | $0.02 | 75 s (estimated, 361 calls) | 35 min | 8 |
| mammoth@openrouter | $0.02 | 72 s (estimated, 361 calls) | 33 min | 8 |
| mercury@openrouter | $0.0032 | 72 s (estimated, 361 calls) | 33 min | 8 |
| span@openrouter | $0.0018 | 73 s (estimated, 361 calls) | 33 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#6847 | configuration | server | 0.99 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| #23855 | formatter | server | 0.96 | Ruff: Format document with an open markdown file results in an error |
| prod:#20280 | configuration | linter | 0.95 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 0.92 | [Infinite loop] TID254 when an import statement has conflicting lazin… |

**clef@openrouter** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #24528 | linter | formatter | 0.98 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #27602 | configuration | formatter | 0.96 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#9132 | configuration | formatter | 0.96 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |
| prod:#13419 | configuration | formatter | 0.96 | {"title": "provide a exit code for `ruff format` (without --check) fo… |
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#17679 | configuration | formatter | 0.96 | {"title": "Allow formatting only changed blocks (git)", "body": "It w… |

**d1-ultra@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.97 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#18310 | configuration | linter | 0.92 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |

**d1.1@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#8248 | linter | configuration | 0.96 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| prod:#17572 | formatter | server | 0.95 | {"title": "Cursor jumps to end of file when formatting files with lar… |
| #24840 | configuration | server | 0.92 | Can the ruff color "All checks passed!" be made consistent with ty pl… |
| prod:#18728 | configuration | linter | 0.91 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |
| #24845 | configuration | linter | 0.91 | Allow configuring some exception types to be ignored by B904 |

**d1@vercel** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #27602 | configuration | formatter | 0.95 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#19196 | configuration | linter | 0.94 | {"title": "EXE003 Configuration of allowable interpreters", "body": "… |
| #24955 | configuration | linter | 0.93 | [pydocstyle] allow configuring indentation level for Google style |
| #28105 | configuration | linter | 0.92 | Stabilize categories |
| #24845 | configuration | linter | 0.91 | Allow configuring some exception types to be ignored by B904 |

**decider-flash@openrouter** (13)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#13419 | configuration | formatter | 0.96 | {"title": "provide a exit code for `ruff format` (without --check) fo… |
| prod:#9132 | configuration | formatter | 0.95 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |
| #27602 | configuration | formatter | 0.95 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #24528 | linter | formatter | 0.95 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#14984 | formatter | linter | 0.94 | {"title": "`docstring-code-line-length = \"dynamic\"` not Working Cor… |

**decider@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#18310 | configuration | linter | 0.97 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#20280 | configuration | linter | 0.96 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#8248 | linter | configuration | 0.93 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |

**decision-1@openrouter** (13)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #23855 | formatter | server | 0.99 | Ruff: Format document with an open markdown file results in an error |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26418 | formatter | linter | 0.97 | Ability to suppress PEP 758 check |
| prod:#6847 | configuration | server | 0.93 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| #26480 | configuration | linter | 0.92 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| prod:#18349 | configuration | linter | 0.92 | {"title": "Warn about error being related to a deprecated rule", "bod… |

**drex-max@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#18310 | configuration | linter | 0.97 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#20280 | configuration | linter | 0.96 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #24528 | linter | formatter | 0.96 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#8248 | linter | configuration | 0.96 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| prod:#17028 | configuration | linter | 0.91 | {"title": "`unconventional-import-alias (ICN001)`: Add `import numpy.… |

**elephant@openrouter** (11)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #27602 | configuration | formatter | 0.98 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#6847 | configuration | server | 0.96 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| #24955 | configuration | linter | 0.92 | [pydocstyle] allow configuring indentation level for Google style |
| prod:#1773 | linter | configuration | 0.92 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| prod:#7804 | configuration | linter | 0.92 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |

**flash-lite@vercel** (51)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28105 | configuration | linter | 1.00 | Stabilize categories |
| #27759 | configuration | linter | 1.00 | ruff check --statistics --fix-only shows all errors, not just fixable… |
| #27647 | configuration | linter | 1.00 | collapsible-if rule obscures conditional structure |
| #27602 | configuration | formatter | 1.00 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26766 | configuration | linter | 1.00 | Open the online doc for a rule from `ruff rule` |
| #26625 | configuration | linter | 1.00 | Improve support for arbitrary functions accepting `TypeForm` arguments |
| #26480 | configuration | linter | 1.00 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |

**haiku@vercel** (44)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #28604 | linter | configuration | 1.00 | Add `import datetime as dt` as a conventional alias |
| #27647 | configuration | linter | 1.00 | collapsible-if rule obscures conditional structure |
| #27602 | configuration | formatter | 1.00 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26625 | configuration | linter | 1.00 | Improve support for arbitrary functions accepting `TypeForm` arguments |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #26480 | configuration | linter | 1.00 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| #26418 | formatter | linter | 1.00 | Ability to suppress PEP 758 check |

**jev:1.14** (17)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#7804 | configuration | linter | 0.99 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| #27602 | configuration | formatter | 0.98 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#1773 | linter | configuration | 0.96 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| #24955 | configuration | linter | 0.96 | [pydocstyle] allow configuring indentation level for Google style |
| prod:#18349 | configuration | linter | 0.96 | {"title": "Warn about error being related to a deprecated rule", "bod… |

**joey@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18449 | configuration | linter | 0.96 | {"title": "Block fixes on a repo with uncommitted files?", "body": "H… |
| prod:#7804 | configuration | linter | 0.95 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| prod:#14984 | formatter | linter | 0.92 | {"title": "`docstring-code-line-length = \"dynamic\"` not Working Cor… |
| #27224 | configuration | linter | 0.92 | SIM118 complains about .keys() even when the object isn't a dict |

**luna@decisions** (22)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#11107 | configuration | linter | 1.00 | {"title": "Ruff should give a nonzero exit code if file linting panic… |
| prod:#9132 | configuration | formatter | 1.00 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |
| prod:#1773 | linter | configuration | 1.00 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| prod:#18449 | configuration | linter | 1.00 | {"title": "Block fixes on a repo with uncommitted files?", "body": "H… |
| prod:#18349 | configuration | linter | 1.00 | {"title": "Warn about error being related to a deprecated rule", "bod… |
| #27647 | configuration | linter | 1.00 | collapsible-if rule obscures conditional structure |

**mammoth@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.96 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #23855 | formatter | server | 0.96 | Ruff: Format document with an open markdown file results in an error |
| prod:#17572 | formatter | server | 0.91 | {"title": "Cursor jumps to end of file when formatting files with lar… |

**mercury@openrouter** (30)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #24528 | linter | formatter | 1.00 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#18310 | configuration | linter | 1.00 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #28105 | configuration | linter | 0.99 | Stabilize categories |
| #24038 | linter | formatter | 0.99 | Add a rule that disallows use of `# fmt` comments |
| prod:#17679 | configuration | formatter | 0.98 | {"title": "Allow formatting only changed blocks (git)", "body": "It w… |

**span@openrouter** (15)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27177 | configuration | linter | 0.98 | Please remove all rules without an automated fix from default rules |
| prod:#1773 | linter | configuration | 0.97 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| prod:#14984 | formatter | linter | 0.95 | {"title": "`docstring-code-line-length = \"dynamic\"` not Working Cor… |
| #23855 | formatter | server | 0.95 | Ruff: Format document with an open markdown file results in an error |
| prod:#18310 | configuration | linter | 0.94 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |


## Cases the models disagree on (12 of 115)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | flash-lite@vercel | haiku@vercel | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28861 | linter | linter (0.80) | linter (0.97) | linter (0.97) | linter (0.97) | linter (1.00) | formatter (0.70) | linter (0.99) | linter (0.99) | linter (0.99) | linter (0.94) | linter (1.00) | linter (1.00) | linter (0.99) | linter (0.77) | formatter (0.39) | linter (0.91) | linter (0.99) | linter (1.00) | linter (0.53) | PLR1711 useless-return removes comments |
| #28604 | linter | linter (0.73) | linter (0.81) | linter (0.71) | linter (0.80) | configuration (0.56) | linter (0.73) | linter (0.81) | linter (0.50) | linter (0.80) | configuration (0.72) | linter (1.00) | configuration (1.00) | configuration (0.72) | linter (0.81) | linter (0.55) | configuration (0.77) | linter (0.60) | linter (0.96) | linter (0.87) | Add `import datetime as dt` as a conventional alias |
| #28519 | formatter | formatter (0.99) | formatter (0.99) | formatter (0.86) | formatter (0.97) | formatter (0.99) | formatter (0.90) | formatter (0.93) | formatter (0.85) | formatter (0.92) | formatter (0.89) | formatter (1.00) | formatter (1.00) | formatter (0.99) | configuration (0.65) | formatter (0.84) | formatter (1.00) | formatter (0.92) | formatter (0.99) | formatter (0.98) | [Formatter feature request] Config option for trailing comma |
| #28273 | configuration | linter (0.58) | configuration (0.66) | configuration (0.60) | linter (0.57) | linter (0.86) | linter (0.66) | configuration (0.84) | linter (0.56) | configuration (0.85) | linter (0.70) | configuration (1.00) | configuration (1.00) | linter (0.75) | linter (0.76) | linter (0.53) | linter (0.83) | configuration (0.65) | configuration (0.53) | linter (0.64) | Please add "is `default` rule" info to the rule json data |
| #28105 | configuration | linter (0.84) | linter (0.61) | linter (0.62) | linter (0.69) | linter (0.92) | linter (0.76) | configuration (0.51) | linter (0.77) | linter (0.53) | linter (0.76) | linter (1.00) | configuration (1.00) | linter (0.94) | linter (0.72) | linter (0.59) | linter (0.93) | configuration (0.59) | linter (0.99) | linter (0.81) | Stabilize categories |
| #27759 | configuration | configuration (0.64) | linter (0.52) | configuration (0.77) | configuration (0.79) | configuration (0.65) | configuration (0.59) | configuration (0.79) | configuration (0.82) | configuration (0.90) | configuration (0.80) | linter (1.00) | configuration (1.00) | linter (0.57) | linter (0.61) | configuration (0.45) | configuration (0.75) | configuration (0.81) | linter (0.78) | configuration (0.97) | ruff check --statistics --fix-only shows all errors, not just fixable… |
| #27647 | configuration | linter (0.69) | linter (0.74) | linter (0.70) | linter (0.89) | linter (0.89) | linter (0.94) | linter (0.84) | linter (0.74) | linter (0.81) | linter (0.60) | linter (1.00) | linter (1.00) | linter (0.91) | linter (0.64) | linter (0.49) | linter (1.00) | linter (0.90) | linter (0.90) | formatter (0.78) | collapsible-if rule obscures conditional structure |
| #27607 | configuration | formatter (0.64) | formatter (0.93) | configuration (0.59) | configuration (0.76) | formatter (0.56) | configuration (0.85) | configuration (0.54) | configuration (0.98) | configuration (0.51) | configuration (0.83) | configuration (1.00) | configuration (1.00) | configuration (0.70) | configuration (0.47) | formatter (0.45) | formatter (0.67) | configuration (0.76) | configuration (0.59) | formatter (0.93) | ruff rejects documented `indent-width` setting |
| #27177 | configuration | configuration (0.86) | linter (0.56) | configuration (0.57) | linter (0.70) | linter (0.62) | linter (0.60) | configuration (0.57) | linter (0.50) | linter (0.69) | linter (0.57) | configuration (1.00) | configuration (1.00) | configuration (0.54) | linter (0.77) | linter (0.52) | linter (0.66) | configuration (0.68) | linter (0.96) | linter (0.98) | Please remove all rules without an automated fix from default rules |
| #27012 | linter | linter (0.78) | linter (0.88) | configuration (0.56) | linter (0.66) | linter (0.97) | linter (0.94) | linter (0.72) | linter (0.81) | linter (0.75) | linter (0.92) | linter (1.00) | linter (1.00) | linter (0.99) | linter (0.80) | linter (0.57) | linter (1.00) | linter (0.87) | linter (0.98) | linter (0.95) | Check for uses of rule codes in warnings |
| #26766 | configuration | configuration (0.74) | configuration (0.93) | configuration (0.80) | configuration (0.89) | configuration (0.88) | configuration (0.51) | configuration (0.94) | configuration (0.92) | configuration (0.98) | configuration (0.81) | linter (1.00) | configuration (1.00) | configuration (0.85) | linter (0.64) | linter (0.38) | configuration (0.92) | configuration (0.96) | configuration (0.92) | configuration (0.93) | Open the online doc for a rule from `ruff rule` |
| #26625 | configuration | linter (0.65) | linter (0.71) | configuration (0.64) | linter (0.78) | linter (0.76) | configuration (0.82) | linter (0.60) | linter (0.59) | configuration (0.62) | configuration (0.69) | linter (1.00) | linter (1.00) | linter (0.61) | linter (0.55) | linter (0.62) | configuration (0.52) | configuration (0.51) | linter (0.92) | linter (0.56) | Improve support for arbitrary functions accepting `TypeForm` arguments |
