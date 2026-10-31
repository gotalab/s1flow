# gh-ruff-area

2026-10-31 · 361 labelled dev cases (linter 186, configuration 95, formatter 47, server 33) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**drex-max@openrouter** has the highest coverage at 95% accuracy, 87% [84, 91] (API cost $0.28 per 10k, p99 1000ms). Its interval overlaps with d1-ultra@openrouter, decider@openrouter, mammoth@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is d1-ultra@openrouter's, 91% [88, 94]. Showing its sure accuracy is 95% or more takes about 4,586 more labels at the same error rate.

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 361 | 88.1% [84, 91] | 0.86 | 0.97 | 0.04 | 75% [71, 80] | 94.8% (92.0%) | 0/361 | 0/361 |
| clef@openrouter | 361 | 86.4% [83, 90] | 0.85 | 0.98 | 0.04 | 70% [66, 75] | 94.9% (92.0%) | 0/361 | 0/361 |
| d1-ultra@openrouter | 361 | 90.9% [88, 94] | 0.91 | 0.99 | 0.03 | 86% [82, 89] | 95.5% (93.0%) | 0/361 | 0/361 |
| d1.1@openrouter | 361 | 87.5% [84, 91] | 0.87 | 0.98 | 0.03 | 74% [70, 78] | 95.1% (92.4%) | 0/361 | 0/361 |
| d1@vercel | 361 | 85.0% [81, 89] | 0.83 | 0.98 | 0.06 | 71% [66, 76] | 94.9% (92.0%) | 0/361 | 0/361 |
| decider-flash@openrouter | 361 | 84.2% [80, 88] | 0.82 | 0.97 | 0.06 | 68% [63, 73] | 94.7% (91.8%) | 0/361 | 0/361 |
| decider@openrouter | 361 | 90.3% [87, 93] | 0.89 | 0.98 | 0.02 | 85% [82, 89] | 94.5% (91.8%) | 0/361 | 0/361 |
| decision-1@openrouter | 361 | 86.7% [83, 90] | 0.86 | 0.98 | 0.05 | 75% [70, 79] | 94.8% (92.0%) | 0/361 | 0/361 |
| drex-max@openrouter | 361 | 90.6% [88, 93] | 0.90 | 0.99 | 0.03 | 87% [84, 91] | 95.6% (93.1%) | 0/361 | 0/361 |
| elephant@openrouter | 361 | 86.4% [83, 90] | 0.84 | 0.98 | 0.03 | 75% [70, 80] | 93.7% (90.7%) | 0/361 | 0/361 |
| jev:1.14 | 361 | 85.3% [82, 89] | 0.83 | 0.97 | 0.06 | 76% [72, 80] | 94.2% (91.3%) | 0/361 | 0/361 |
| joey@openrouter | 361 | 78.7% [74, 83] | 0.74 | 0.94 | 0.05 | 44% [39, 50] | 95.0% (91.2%) | 0/361 | 0/361 |
| kev@openrouter | 361 | 80.3% [77, 84] | 0.77 | 0.96 | 0.16 | 65% [60, 70] | 94.4% (91.3%) | 0/361 | 0/361 |
| luna@decisions | 361 | 86.7% [83, 90] | 0.85 | 0.97 | 0.08 | 73% [69, 78] | 94.7% (91.9%) | 0/361 | 0/361 |
| mammoth@openrouter | 361 | 90.9% [88, 93] | 0.90 | 0.99 | 0.02 | 86% [82, 89] | 95.2% (92.6%) | 0/361 | 0/361 |
| mercury@openrouter | 361 | 85.3% [82, 89] | 0.84 | 0.98 | 0.10 | 71% [67, 76] | 95.7% (93.0%) | 0/361 | 0/361 |
| span@openrouter | 361 | 88.6% [85, 92] | 0.87 | 0.98 | 0.06 | 79% [75, 83] | 94.4% (91.6%) | 0/361 | 0/361 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; mercury@openrouter = inception/mercury-decide-20260930; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| d1-ultra@openrouter = | 86% [82, 89] | 0.70 | met |
| decider@openrouter = | 85% [82, 89] | 0.76 | met |
| drex-max@openrouter = | 87% [84, 91] | 0.73 | met |
| mammoth@openrouter = | 86% [82, 89] | 0.75 | met |
| span@openrouter | 79% [75, 83] | 0.92 | met |
| jev:1.14 | 76% [72, 80] | 0.93 | met |
| clef-flash@openrouter | 75% [71, 80] | 0.83 | met |
| elephant@openrouter | 75% [70, 80] | 0.86 | met |
| decision-1@openrouter | 75% [70, 79] | 0.89 | met |
| d1.1@openrouter | 74% [70, 78] | 0.87 | met |
| luna@decisions | 73% [69, 78] | 0.98 | met |
| mercury@openrouter | 71% [67, 76] | 0.97 | met |
| d1@vercel | 71% [66, 76] | 0.85 | met |
| clef@openrouter | 70% [66, 75] | 0.91 | met |
| decider-flash@openrouter | 68% [63, 73] | 0.91 | met |
| kev@openrouter | 65% [60, 70] | 0.59 | met |
| joey@openrouter | 44% [39, 50] | 0.87 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 361 | 406 ms | 568 ms | 787 ms | 1085 ms | 1.9 | 0 | 4 | $0.12 | billed |  |
| clef@openrouter | 361 | 345 ms | 489 ms | 1180 ms | 1573 ms | 3.4 | 0 | 4 | $1.11 | billed |  |
| d1-ultra@openrouter | 361 | 212 ms | 292 ms | 422 ms | 541 ms | 2.0 | 0 | 4 | $0.17 | billed | ○ |
| d1.1@openrouter | 361 | 172 ms | 249 ms | 333 ms | 480 ms | 1.9 | 0 | 4 | $0.08 | billed | ○ |
| d1@vercel | 361 | 214 ms | 303 ms | 431 ms | 728 ms | 2.0 | 0 | 4 | $0.08 | billed |  |
| decider-flash@openrouter | 361 | 146 ms | 162 ms | 197 ms | 370 ms | 1.3 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 361 | 218 ms | 250 ms | 378 ms | 5322 ms | 1.7 | 0 | 4 | $0.09 | billed | ○ |
| decision-1@openrouter | 361 | 266 ms | 331 ms | 471 ms | 674 ms | 1.8 | 0 | 4 | $0.17 | billed |  |
| drex-max@openrouter | 361 | 298 ms | 404 ms | 1000 ms | 1604 ms | 3.4 | 0 | 4 | $0.28 | billed | ○ |
| elephant@openrouter | 361 | 185 ms | 205 ms | 300 ms | 546 ms | 1.6 | 0 | 4 | $0.16 | billed | ○ |
| jev:1.14 | 361 | 143 ms | 168 ms | 311 ms | 678 ms | 2.2 | 0 | 4 | $0.29 | estimated | ○ |
| joey@openrouter | 361 | 181 ms | 202 ms | 356 ms | 607 ms | 2.0 | 0 | 4 | $0.05 | billed |  |
| kev@openrouter | 361 | 459 ms | 720 ms | 1187 ms | 1315 ms | 2.6 | 0 | 4 | $0.16 | billed |  |
| luna@decisions | 361 | 204 ms | 354 ms | 682 ms | 928 ms | 3.3 | 1 | 4 | $0.47 | estimated |  |
| mammoth@openrouter | 361 | 222 ms | 244 ms | 419 ms | 872 ms | 1.9 | 0 | 4 | $0.47 | billed | ○ |
| mercury@openrouter | 361 | 306 ms | 404 ms | 626 ms | 736 ms | 2.0 | 0 | 4 | $0.09 | billed |  |
| span@openrouter | 361 | 176 ms | 425 ms | 892 ms | 1119 ms | 5.1 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, mercury@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0042 | 36 s (estimated, 361 calls) | 16 min | 4 |
| clef@openrouter | $0.04 | 33 s (estimated, 361 calls) | 15 min | 4 |
| d1-ultra@openrouter | $0.0061 | 21 s (estimated, 361 calls) | 10 min | 4 |
| d1.1@openrouter | $0.0029 | 17 s (estimated, 361 calls) | 8 min | 4 |
| d1@vercel | $0.0029 | 21 s (estimated, 361 calls) | 10 min | 4 |
| decider-flash@openrouter | $0.0017 | 13 s (estimated, 361 calls) | 6 min | 4 |
| decider@openrouter | $0.0033 | 22 s (estimated, 361 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0060 | 25 s (estimated, 361 calls) | 12 min | 4 |
| drex-max@openrouter | $0.0100 | 28 s (estimated, 361 calls) | 13 min | 4 |
| elephant@openrouter | $0.0059 | 17 s (estimated, 361 calls) | 8 min | 4 |
| jev:1.14 | $0.01 | 14 s (estimated, 361 calls) | 6 min | 4 |
| joey@openrouter | $0.0017 | 17 s (estimated, 361 calls) | 8 min | 4 |
| kev@openrouter | $0.0057 | 37 s (estimated, 361 calls) | 17 min | 4 |
| luna@decisions | $0.02 | 22 s (estimated, 361 calls) | 10 min | 4 |
| mammoth@openrouter | $0.02 | 21 s (estimated, 361 calls) | 10 min | 4 |
| mercury@openrouter | $0.0032 | 29 s (estimated, 361 calls) | 14 min | 4 |
| span@openrouter | $0.0018 | 23 s (estimated, 361 calls) | 11 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.

## Wrong at a high probability (0.9 or more)

**clef-flash@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#6847 | configuration | server | 0.99 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| #23855 | formatter | server | 0.96 | Ruff: Format document with an open markdown file results in an error |
| prod:#20280 | configuration | linter | 0.95 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #27224 | configuration | linter | 0.92 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.92 | [Infinite loop] TID254 when an import statement has conflicting lazin… |

**clef@openrouter** (14)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #24528 | linter | formatter | 0.98 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#9132 | configuration | formatter | 0.97 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |
| #27602 | configuration | formatter | 0.96 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#13419 | configuration | formatter | 0.96 | {"title": "provide a exit code for `ruff format` (without --check) fo… |
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#17679 | configuration | formatter | 0.96 | {"title": "Allow formatting only changed blocks (git)", "body": "It w… |

**d1-ultra@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| #23855 | formatter | server | 0.90 | Ruff: Format document with an open markdown file results in an error |

**d1.1@openrouter** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#8248 | linter | configuration | 0.97 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| #24840 | configuration | server | 0.96 | Can the ruff color "All checks passed!" be made consistent with ty pl… |
| prod:#17572 | formatter | server | 0.94 | {"title": "Cursor jumps to end of file when formatting files with lar… |
| #27647 | configuration | linter | 0.94 | collapsible-if rule obscures conditional structure |
| #23855 | formatter | server | 0.91 | Ruff: Format document with an open markdown file results in an error |

**d1@vercel** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #23855 | formatter | server | 0.97 | Ruff: Format document with an open markdown file results in an error |
| #24528 | linter | formatter | 0.96 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #24955 | configuration | linter | 0.95 | [pydocstyle] allow configuring indentation level for Google style |
| prod:#18728 | configuration | linter | 0.95 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |
| #27602 | configuration | formatter | 0.94 | `ruff format --check` uses same exit code for syntax errors in files,… |

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

**decision-1@openrouter** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #23855 | formatter | server | 0.99 | Ruff: Format document with an open markdown file results in an error |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26418 | formatter | linter | 0.97 | Ability to suppress PEP 758 check |
| #26480 | configuration | linter | 0.94 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| prod:#6847 | configuration | server | 0.92 | {"title": "Break in compatibility with jupyterlab-lsp + python-lsp-ru… |
| prod:#18349 | configuration | linter | 0.92 | {"title": "Warn about error being related to a deprecated rule", "bod… |

**drex-max@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18310 | configuration | linter | 0.97 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#8248 | linter | configuration | 0.97 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| #24528 | linter | formatter | 0.96 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#17028 | configuration | linter | 0.92 | {"title": "`unconventional-import-alias (ICN001)`: Add `import numpy.… |

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

**jev:1.14** (16)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#7804 | configuration | linter | 0.99 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| #27602 | configuration | formatter | 0.97 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#17679 | configuration | formatter | 0.96 | {"title": "Allow formatting only changed blocks (git)", "body": "It w… |
| prod:#18349 | configuration | linter | 0.96 | {"title": "Warn about error being related to a deprecated rule", "bod… |
| #24955 | configuration | linter | 0.96 | [pydocstyle] allow configuring indentation level for Google style |

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

**mercury@openrouter** (27)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #24528 | linter | formatter | 1.00 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#18310 | configuration | linter | 1.00 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #28105 | configuration | linter | 0.99 | Stabilize categories |
| #24038 | linter | formatter | 0.98 | Add a rule that disallows use of `# fmt` comments |
| prod:#19196 | configuration | linter | 0.98 | {"title": "EXE003 Configuration of allowable interpreters", "body": "… |

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


## Cases the models disagree on (12 of 113)

| id | label | clef-flash@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | mercury@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28519 | formatter | formatter (0.99) | formatter (0.99) | formatter (0.85) | formatter (0.97) | formatter (0.98) | formatter (0.90) | formatter (0.93) | formatter (0.85) | formatter (0.92) | formatter (0.89) | formatter (0.99) | configuration (0.65) | formatter (0.83) | formatter (1.00) | formatter (0.92) | formatter (0.99) | formatter (0.98) | [Formatter feature request] Config option for trailing comma |
| #27647 | configuration | linter (0.68) | linter (0.77) | linter (0.73) | linter (0.94) | linter (0.94) | linter (0.94) | linter (0.84) | linter (0.65) | linter (0.90) | linter (0.60) | linter (0.92) | linter (0.64) | linter (0.49) | linter (1.00) | linter (0.90) | linter (0.90) | formatter (0.53) | collapsible-if rule obscures conditional structure |
| #27012 | linter | linter (0.78) | linter (0.89) | configuration (0.54) | linter (0.73) | linter (0.96) | linter (0.94) | linter (0.72) | linter (0.82) | linter (0.75) | linter (0.92) | linter (1.00) | linter (0.80) | linter (0.57) | linter (1.00) | linter (0.87) | linter (0.99) | linter (0.95) | Check for uses of rule codes in warnings |
| #26320 | linter | linter (0.90) | linter (0.80) | configuration (0.61) | linter (0.64) | linter (0.85) | linter (0.93) | linter (0.53) | linter (0.75) | configuration (0.64) | linter (0.74) | linter (0.93) | linter (0.84) | linter (0.59) | linter (1.00) | configuration (0.50) | linter (0.95) | configuration (0.62) | Option to opt in to showing error codes or show error codes in additi… |
| #26221 | linter | linter (0.64) | linter (0.96) | linter (0.97) | linter (0.97) | server (0.92) | server (0.77) | linter (1.00) | linter (1.00) | linter (1.00) | linter (0.98) | server (0.82) | linter (0.62) | linter (0.41) | linter (1.00) | linter (1.00) | linter (1.00) | linter (0.94) | `PLC2801` gives suggestions differentially for the `__floor__`, `__ce… |
| #25281 | formatter | formatter (0.88) | formatter (0.96) | formatter (0.71) | formatter (0.78) | formatter (0.90) | formatter (0.77) | formatter (0.95) | formatter (0.85) | formatter (0.97) | formatter (0.86) | formatter (0.95) | linter (0.55) | formatter (0.64) | formatter (1.00) | formatter (0.92) | formatter (1.00) | formatter (0.99) | Support pycon formatting in docstrings |
| #25114 | configuration | configuration (0.84) | configuration (0.84) | configuration (0.86) | configuration (0.92) | configuration (0.95) | configuration (0.94) | configuration (0.98) | configuration (0.93) | configuration (0.99) | configuration (0.96) | configuration (0.99) | linter (0.72) | configuration (0.57) | configuration (1.00) | configuration (0.98) | configuration (0.99) | configuration (0.96) | `requires-python` discovery is inconsistent with config file discovery |
| #24829 | configuration | configuration (0.81) | configuration (0.79) | configuration (0.89) | configuration (0.97) | configuration (0.88) | configuration (0.96) | configuration (0.97) | configuration (0.88) | configuration (0.98) | configuration (0.97) | configuration (0.98) | linter (0.56) | configuration (0.64) | configuration (1.00) | configuration (0.95) | configuration (0.94) | configuration (0.93) | ruff ignoring `requires-python` in `pyproject.toml` when missing `[to… |
| #24420 | server | server (0.99) | server (0.99) | server (0.92) | server (0.97) | server (0.98) | server (0.97) | server (0.95) | server (0.99) | server (0.93) | server (0.95) | server (0.96) | configuration (0.50) | server (0.51) | server (1.00) | server (0.90) | server (0.99) | server (0.98) | [LSP] `"settings.configurationPreference: "filesystemFirst"` doesn't … |
| #24389 | linter | linter (0.73) | linter (0.82) | linter (0.95) | linter (0.98) | linter (0.99) | formatter (0.72) | linter (0.97) | linter (0.95) | linter (0.98) | linter (0.76) | linter (0.98) | linter (0.48) | linter (0.44) | linter (1.00) | linter (0.90) | linter (0.98) | linter (0.94) | String ending with octal causes panic when `UP012` selected |
| #24323 | linter | linter (0.77) | linter (0.94) | linter (0.81) | linter (0.90) | linter (0.97) | linter (0.79) | linter (0.91) | linter (0.91) | linter (0.92) | linter (0.64) | linter (0.94) | linter (0.70) | formatter (0.40) | linter (1.00) | linter (0.81) | linter (1.00) | linter (0.98) | `isort` options for profile compatibility |
| #24031 | linter | linter (0.85) | linter (0.91) | linter (0.98) | linter (0.98) | linter (0.99) | linter (0.98) | linter (0.99) | linter (1.00) | linter (0.99) | linter (0.99) | linter (1.00) | formatter (0.54) | linter (0.68) | linter (1.00) | linter (0.98) | linter (1.00) | linter (0.99) | Mismatching number of %-placeholders in string formatting |
