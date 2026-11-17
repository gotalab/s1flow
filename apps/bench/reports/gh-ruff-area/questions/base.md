# gh-ruff-area

2026-11-17 · 361 labelled dev cases (linter 186, configuration 95, formatter 47, server 33) · split: stratified k-fold (no test case among these: CV numbers only) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

drex-max@openrouter has the highest coverage at 95% accuracy, 89% [85, 92] (API cost $0.28 per 10k, p99 1240ms). Its interval overlaps with d1-ultra@openrouter, d1.2-ultra, decider@openrouter, mammoth@openrouter, span@openrouter: the objective cannot tell them apart; interval overlap does not establish equivalence. task.py names no tiebreak, so they are listed by name, unordered. The highest raw accuracy (dev) is decider@openrouter's, 92% [89, 94].

## Comparison

| model | scored | accuracy (all) | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 361 | 87.8% [84, 91] | 0.86 | 0.97 | 0.03 | 76% [72, 80] | 94.2% (91.3%) | 0.0% (0/361) | 0/361 |
| clef-omni@openrouter | 361 | 88.6% [85, 92] | 0.87 | 0.98 | 0.05 | 79% [75, 83] | 94.7% (92.0%) | 0.0% (0/361) | 0/361 |
| clef@openrouter | 361 | 86.4% [83, 90] | 0.85 | 0.98 | 0.05 | 66% [61, 70] | 95.4% (92.4%) | 0.0% (0/361) | 0/361 |
| d1-ultra@openrouter | 361 | 90.0% [87, 93] | 0.89 | 0.99 | 0.04 | 86% [82, 90] | 94.9% (92.3%) | 0.0% (0/361) | 0/361 |
| d1.1@openrouter | 361 | 87.3% [84, 90] | 0.87 | 0.98 | 0.03 | 75% [70, 79] | 95.2% (92.5%) | 0.0% (0/361) | 0/361 |
| d1.2 | 361 | 86.1% [83, 89] | 0.85 | 0.98 | 0.05 | 70% [66, 75] | 95.3% (92.5%) | 0.0% (0/361) | 0/361 |
| d1.2-ultra | 361 | 91.1% [88, 94] | 0.90 | 0.99 | 0.06 | 88% [85, 92] | 95.0% (92.5%) | 0.0% (0/361) | 0/361 |
| d1@vercel | 361 | 84.5% [81, 88] | 0.82 | 0.98 | 0.06 | 73% [68, 77] | 94.3% (91.4%) | 0.0% (0/361) | 0/361 |
| decider-flash@openrouter | 361 | 85.9% [83, 89] | 0.85 | 0.98 | 0.06 | 67% [63, 72] | 95.5% (92.6%) | 0.0% (0/361) | 0/361 |
| decider@openrouter | 361 | 91.7% [89, 94] | 0.91 | 0.99 | 0.02 | 88% [85, 91] | 94.3% (91.7%) | 0.0% (0/361) | 0/361 |
| decision-1.1@openrouter | 361 | 90.6% [88, 94] | 0.91 | 0.98 | 0.05 | 76% [72, 80] | 95.3% (92.6%) | 0.0% (0/361) | 0/361 |
| decision-1@openrouter | 361 | 87.3% [84, 91] | 0.86 | 0.98 | 0.05 | 72% [68, 77] | 95.4% (92.7%) | 0.0% (0/361) | 0/361 |
| drex-max@openrouter | 361 | 90.6% [88, 93] | 0.90 | 0.99 | 0.04 | 89% [85, 92] | 94.7% (92.2%) | 0.0% (0/361) | 0/361 |
| elephant@openrouter | 361 | 86.1% [83, 89] | 0.84 | 0.98 | 0.04 | 72% [67, 76] | 94.6% (91.7%) | 0.0% (0/361) | 0/361 |
| gemini-decision@google | 361 | 86.4% [83, 90] | 0.86 | 0.99 | 0.03 | 76% [72, 81] | 94.9% (92.2%) | 0.0% (0/361) | 0/361 |
| jev:1.14 | 361 | 85.3% [82, 89] | 0.83 | 0.98 | 0.07 | 76% [72, 80] | 94.2% (91.3%) | 0.0% (0/361) | 0/361 |
| joey@openrouter | 361 | 77.6% [73, 82] | 0.72 | 0.94 | 0.03 | 38% [34, 43] | 94.2% (89.8%) | 0.0% (0/361) | 0/361 |
| kev@openrouter | 361 | 81.4% [77, 85] | 0.78 | 0.97 | 0.16 | 68% [64, 73] | 94.3% (91.3%) | 0.0% (0/361) | 0/361 |
| luna@decisions | 361 | 88.4% [85, 91] | 0.88 | 0.98 | 0.07 | 73% [68, 77] | 95.1% (92.3%) | 0.0% (0/361) | 0/361 |
| mammoth@openrouter | 361 | 90.3% [87, 93] | 0.90 | 0.99 | 0.02 | 87% [83, 90] | 94.9% (92.3%) | 0.0% (0/361) | 0/361 |
| reflex@openrouter | 361 | 91.1% [88, 94] | 0.91 | 0.99 | 0.06 | 81% [77, 85] | 95.2% (92.6%) | 0.0% (0/361) | 0/361 |
| span@openrouter | 361 | 88.6% [85, 92] | 0.87 | 0.98 | 0.05 | 84% [80, 87] | 94.7% (92.1%) | 0.0% (0/361) | 0/361 |

Answered by: clef-flash@openrouter = cloudflare/clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; clef@openrouter = cloudflare/clef; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1.1@openrouter = liquid/d1.1-20261027; d1.2 = d1.2; d1.2-ultra = d1.2-ultra; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1.1@openrouter = microsoft/microsoft-decision-1.1-20261117; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex-max@openrouter = nace-ai/drex-max-20261016; elephant@openrouter = baseten/elephant-1-20261021; gemini-decision@google = gemini-decision-1; jev:1.14 = jev-1.14.0; joey@openrouter = baseten/joey-1-20261029; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; mammoth@openrouter = baseten/mammoth-1-20261021; reflex@openrouter = morph/reflex-20261103; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| d1-ultra@openrouter = | 86% [82, 90] | 0.67 | met |
| d1.2-ultra = | 88% [85, 92] | 0.65 | met |
| decider@openrouter = | 88% [85, 91] | 0.78 | met |
| drex-max@openrouter = | 89% [85, 92] | 0.71 | met |
| mammoth@openrouter = | 87% [83, 90] | 0.76 | met |
| span@openrouter = | 84% [80, 87] | 0.84 | met |
| reflex@openrouter | 81% [77, 85] | 0.92 | met |
| clef-omni@openrouter | 79% [75, 83] | 0.78 | met |
| gemini-decision@google | 76% [72, 81] | 0.77 | met |
| clef-flash@openrouter | 76% [72, 80] | 0.82 | met |
| decision-1.1@openrouter | 76% [72, 80] | 0.89 | met |
| jev:1.14 | 76% [72, 80] | 0.87 | met |
| d1.1@openrouter | 75% [70, 79] | 0.86 | met |
| d1@vercel | 73% [68, 77] | 0.88 | met |
| luna@decisions | 73% [68, 77] | 0.99 | met |
| decision-1@openrouter | 72% [68, 77] | 0.91 | met |
| elephant@openrouter | 72% [67, 76] | 0.87 | met |
| d1.2 | 70% [66, 75] | 0.82 | met |
| kev@openrouter | 68% [64, 73] | 0.58 | met |
| decider-flash@openrouter | 67% [63, 72] | 0.91 | met |
| clef@openrouter | 66% [61, 70] | 0.90 | met |
| joey@openrouter | 38% [34, 43] | 0.91 | met |

= marks the models whose interval on the primary objective (leftmost) overlaps the best one's; task.py's tiebreak orders them (its objectives read the way the primary sets; latency is p90, compared only when all were measured alike; API cost per 10k, the Calls section), and without one they are listed by name. Every objective is measured on the answers. The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef-flash@openrouter | 361 | 277 ms | 524 ms | 1229 ms | 1598 ms | 4.4 | 0 | 4 | $0.13 | billed |  |
| clef-omni@openrouter | 361 | 181 ms | 217 ms | 321 ms | 882 ms | 1.8 | 0 | 4 | $0.76 | billed |  |
| clef@openrouter | 361 | 298 ms | 729 ms | 4400 ms | 9104 ms | 14.8 | 0 | 4 | $1.10 | billed |  |
| d1-ultra@openrouter | 361 | 687 ms | 2325 ms | 5672 ms | 7114 ms | 8.3 | 0 | 4 | $0.17 | billed |  |
| d1.1@openrouter | 361 | 297 ms | 503 ms | 689 ms | 3162 ms | 2.3 | 0 | 4 | $0.08 | billed | ○ |
| d1.2 | 361 | 112 ms | 168 ms | 611 ms | 1127 ms | 5.5 | 0 | 4 | $0.08 | billed | ○ |
| d1.2-ultra | 361 | 114 ms | 155 ms | 326 ms | 395 ms | 2.8 | 0 | 4 | $0.17 | billed | ○ |
| d1@vercel | 361 | 508 ms | 852 ms | 1933 ms | 6090 ms | 3.8 | 0 | 4 | $0.08 | billed |  |
| decider-flash@openrouter | 361 | 137 ms | 166 ms | 410 ms | 481 ms | 3.0 | 0 | 4 | $0.05 | billed | ○ |
| decider@openrouter | 361 | 219 ms | 314 ms | 628 ms | 1006 ms | 2.9 | 0 | 4 | $0.09 | billed | ○ |
| decision-1.1@openrouter | 361 | 223 ms | 255 ms | 325 ms | 514 ms | 1.5 | 0 | 4 | $0.18 | billed | ○ |
| decision-1@openrouter | 361 | 232 ms | 301 ms | 380 ms | 457 ms | 1.6 | 0 | 4 | $0.17 | billed | ○ |
| drex-max@openrouter | 361 | 439 ms | 790 ms | 1240 ms | 1390 ms | 2.8 | 0 | 4 | $0.28 | billed | ○ |
| elephant@openrouter | 361 | 167 ms | 189 ms | 255 ms | 369 ms | 1.5 | 0 | 4 | $0.16 | billed | ○ |
| gemini-decision@google | 361 | 265 ms | 375 ms | 409 ms | 593 ms | 1.5 | 0 | 4 | $0.49 | estimated |  |
| jev:1.14 | 361 | 110 ms | 140 ms | 206 ms | 416 ms | 1.9 | 0 | 4 | $0.29 | estimated | ○ |
| joey@openrouter | 361 | 165 ms | 189 ms | 238 ms | 377 ms | 1.4 | 0 | 4 | $0.05 | billed | ○ |
| kev@openrouter | 361 | 644 ms | 920 ms | 1292 ms | 1535 ms | 2.0 | 0 | 4 | $0.16 | billed |  |
| luna@decisions | 361 | 185 ms | 350 ms | 502 ms | 687 ms | 2.7 | 0 | 4 | $0.47 | estimated |  |
| mammoth@openrouter | 361 | 178 ms | 206 ms | 287 ms | 466 ms | 1.6 | 0 | 4 | $0.47 | billed | ○ |
| reflex@openrouter | 361 | 249 ms | 286 ms | 345 ms | 494 ms | 1.4 | 0 | 4 | $0.20 | billed |  |
| span@openrouter | 361 | 528 ms | 772 ms | 912 ms | 1086 ms | 1.7 | 0 | 4 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Where the API costs come from: billed: clef-flash@openrouter, clef-omni@openrouter, clef@openrouter, d1-ultra@openrouter, d1.1@openrouter, d1.2, d1.2-ultra, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1.1@openrouter, decision-1@openrouter, drex-max@openrouter, elephant@openrouter, joey@openrouter, kev@openrouter, mammoth@openrouter, reflex@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): gemini-decision@google (list price of 2026-11-12), jev:1.14 (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef-flash@openrouter | $0.0045 | 30 s (estimated, 361 calls) | 14 min | 4 |
| clef-omni@openrouter | $0.03 | 17 s (estimated, 361 calls) | 8 min | 4 |
| clef@openrouter | $0.04 | 48 s (estimated, 361 calls) | 22 min | 4 |
| d1-ultra@openrouter | $0.0061 | 2 min (estimated, 361 calls) | 44 min | 4 |
| d1.1@openrouter | $0.0029 | 30 s (estimated, 361 calls) | 14 min | 4 |
| d1.2 | $0.0029 | 13 s (estimated, 361 calls) | 6 min | 4 |
| d1.2-ultra | $0.0061 | 11 s (estimated, 361 calls) | 5 min | 4 |
| d1@vercel | $0.0029 | 53 s (estimated, 361 calls) | 24 min | 4 |
| decider-flash@openrouter | $0.0017 | 13 s (estimated, 361 calls) | 6 min | 4 |
| decider@openrouter | $0.0033 | 22 s (estimated, 361 calls) | 10 min | 4 |
| decision-1.1@openrouter | $0.0065 | 21 s (estimated, 361 calls) | 10 min | 4 |
| decision-1@openrouter | $0.0060 | 22 s (estimated, 361 calls) | 10 min | 4 |
| drex-max@openrouter | $0.0100 | 42 s (estimated, 361 calls) | 20 min | 4 |
| elephant@openrouter | $0.0059 | 15 s (estimated, 361 calls) | 7 min | 4 |
| gemini-decision@google | $0.02 | 25 s (estimated, 361 calls) | 12 min | 4 |
| jev:1.14 | $0.01 | 10 s (estimated, 361 calls) | 5 min | 4 |
| joey@openrouter | $0.0017 | 15 s (estimated, 361 calls) | 7 min | 4 |
| kev@openrouter | $0.0057 | 62 s (estimated, 361 calls) | 29 min | 4 |
| luna@decisions | $0.02 | 21 s (estimated, 361 calls) | 9 min | 4 |
| mammoth@openrouter | $0.02 | 16 s (estimated, 361 calls) | 8 min | 4 |
| reflex@openrouter | $0.0071 | 23 s (estimated, 361 calls) | 11 min | 4 |
| span@openrouter | $0.0018 | 50 s (estimated, 361 calls) | 23 min | 4 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: every labelled dev case the model answered or refused; held-out test results come only when a candidate is adopted. Refused: the share of the scored cases the model refused or does not support, each counted as no answer (wrong, and never sure). Failed counts calls.

## Wrong at a high probability (0.9 or more)

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
| #26450 | configuration | linter | 0.97 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#18310 | configuration | linter | 0.95 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #27224 | configuration | linter | 0.93 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.92 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |

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

**d1.2** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.97 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.97 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.95 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18728 | configuration | linter | 0.92 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |

**d1.2-ultra** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.96 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#8248 | linter | configuration | 0.91 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |

**d1@vercel** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18310 | configuration | linter | 0.98 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| #24528 | linter | formatter | 0.96 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| prod:#14813 | configuration | linter | 0.96 | {"title": "F821 not recognizing `requires-python` in `pyproject.toml`… |
| prod:#18728 | configuration | linter | 0.95 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |
| #27647 | configuration | linter | 0.94 | collapsible-if rule obscures conditional structure |

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

**drex-max@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#18310 | configuration | linter | 0.97 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#8248 | linter | configuration | 0.97 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| #24528 | linter | formatter | 0.95 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #26418 | formatter | linter | 0.91 | Ability to suppress PEP 758 check |
| prod:#1773 | linter | configuration | 0.90 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |

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
| prod:#7804 | configuration | linter | 0.95 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |

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
| prod:#18349 | configuration | linter | 1.00 | {"title": "Warn about error being related to a deprecated rule", "bod… |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #26480 | configuration | linter | 1.00 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #27647 | configuration | linter | 1.00 | collapsible-if rule obscures conditional structure |
| #27602 | configuration | formatter | 1.00 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#18449 | configuration | linter | 0.99 | {"title": "Block fixes on a repo with uncommitted files?", "body": "H… |

**mammoth@openrouter** (5)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #23855 | formatter | server | 0.97 | Ruff: Format document with an open markdown file results in an error |
| #24955 | configuration | linter | 0.90 | [pydocstyle] allow configuring indentation level for Google style |

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
| prod:#15155 | server | linter | 0.94 | {"title": "Incorrect import removal with \"todo:\" in Neovim/LSP", "b… |
| prod:#1773 | linter | configuration | 0.93 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |


## Cases the models disagree on (12 of 116)

| id | label | clef-flash@openrouter | clef-omni@openrouter | clef@openrouter | d1-ultra@openrouter | d1.1@openrouter | d1.2 | d1.2-ultra | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1.1@openrouter | decision-1@openrouter | drex-max@openrouter | elephant@openrouter | gemini-decision@google | jev:1.14 | joey@openrouter | kev@openrouter | luna@decisions | mammoth@openrouter | reflex@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28861 | linter | linter (0.67) | formatter (0.72) | linter (0.97) | linter (0.96) | linter (0.96) | linter (0.93) | linter (0.94) | linter (1.00) | linter (0.87) | linter (0.99) | linter (1.00) | linter (0.99) | linter (0.98) | linter (0.96) | linter (0.99) | linter (0.99) | linter (0.81) | linter (0.44) | linter (1.00) | linter (0.99) | linter (1.00) | linter (0.68) | PLR1711 useless-return removes comments |
| #28857 | linter | linter (0.92) | formatter (0.52) | linter (0.97) | linter (0.94) | linter (0.97) | linter (0.96) | linter (0.90) | linter (0.98) | linter (0.87) | linter (0.99) | linter (1.00) | linter (0.98) | linter (0.99) | linter (0.95) | linter (0.98) | linter (0.92) | linter (0.93) | linter (0.44) | linter (1.00) | linter (0.98) | linter (1.00) | linter (0.98) | isort: fixer causes F401 unused-import |
| #28519 | formatter | formatter (0.99) | formatter (0.95) | formatter (0.99) | formatter (0.94) | formatter (0.94) | formatter (0.93) | formatter (0.87) | formatter (0.98) | formatter (0.72) | formatter (0.93) | formatter (0.75) | formatter (0.73) | formatter (0.96) | formatter (0.88) | formatter (0.86) | formatter (1.00) | configuration (0.69) | formatter (0.78) | formatter (0.99) | formatter (0.90) | formatter (0.99) | formatter (0.99) | [Formatter feature request] Config option for trailing comma |
| #27647 | configuration | linter (0.62) | formatter (0.87) | linter (0.74) | linter (0.62) | linter (0.85) | linter (0.88) | linter (0.60) | linter (0.94) | linter (0.94) | linter (0.60) | linter (0.89) | linter (0.41) | linter (0.67) | linter (0.54) | linter (0.75) | linter (0.98) | linter (0.64) | linter (0.53) | linter (1.00) | linter (0.87) | linter (0.83) | formatter (0.75) | collapsible-if rule obscures conditional structure |
| #27602 | configuration | formatter (0.82) | formatter (0.79) | formatter (0.97) | formatter (0.61) | formatter (0.76) | formatter (0.82) | formatter (0.69) | formatter (0.93) | formatter (0.96) | formatter (0.66) | configuration (0.87) | formatter (0.80) | formatter (0.88) | formatter (0.99) | formatter (0.77) | formatter (0.99) | formatter (0.83) | formatter (0.65) | formatter (1.00) | formatter (0.57) | formatter (0.80) | formatter (0.68) | `ruff format --check` uses same exit code for syntax errors in files,… |
| #26866 | formatter | formatter (0.86) | formatter (0.85) | formatter (0.99) | formatter (0.86) | formatter (0.92) | formatter (0.90) | formatter (0.93) | formatter (0.99) | formatter (0.77) | formatter (0.99) | formatter (0.71) | formatter (0.71) | formatter (1.00) | linter (0.45) | formatter (0.92) | formatter (0.99) | formatter (0.91) | formatter (0.48) | formatter (1.00) | formatter (0.97) | formatter (1.00) | formatter (0.88) | Stabilize Markdown formatting |
| #26480 | configuration | linter (0.46) | formatter (0.54) | linter (0.77) | linter (0.49) | linter (0.56) | linter (0.50) | configuration (0.48) | linter (0.78) | linter (0.78) | configuration (0.52) | linter (0.61) | linter (0.96) | configuration (0.53) | linter (0.61) | linter (0.62) | linter (0.83) | linter (0.87) | formatter (0.49) | linter (1.00) | linter (0.71) | configuration (0.41) | linter (0.84) | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| #26451 | linter | linter (0.85) | configuration (0.43) | linter (0.89) | linter (0.85) | linter (0.92) | linter (0.89) | linter (0.82) | linter (0.97) | linter (0.87) | linter (0.95) | linter (0.99) | linter (0.99) | linter (0.89) | linter (0.87) | linter (0.91) | linter (0.96) | formatter (0.69) | linter (0.38) | linter (1.00) | linter (0.89) | linter (0.99) | linter (0.87) | TD004: Support additional TODO comment formats |
| #26320 | linter | linter (0.89) | linter (0.74) | linter (0.67) | configuration (0.59) | linter (0.66) | linter (0.85) | configuration (0.69) | linter (0.84) | linter (0.95) | linter (0.67) | linter (0.58) | linter (0.89) | configuration (0.60) | linter (0.84) | linter (0.83) | linter (0.93) | linter (0.84) | linter (0.60) | linter (1.00) | linter (0.53) | linter (0.87) | configuration (0.67) | Option to opt in to showing error codes or show error codes in additi… |
| #25281 | formatter | formatter (0.90) | formatter (0.94) | formatter (0.96) | formatter (0.76) | formatter (0.82) | formatter (0.82) | formatter (0.89) | formatter (0.78) | formatter (0.84) | formatter (0.96) | formatter (0.73) | formatter (0.90) | formatter (0.98) | formatter (0.87) | formatter (0.63) | formatter (0.89) | linter (0.61) | formatter (0.63) | formatter (1.00) | formatter (0.95) | formatter (0.99) | formatter (0.97) | Support pycon formatting in docstrings |
| #25114 | configuration | configuration (0.83) | configuration (0.86) | configuration (0.83) | configuration (0.92) | configuration (0.89) | configuration (0.81) | configuration (0.88) | configuration (0.97) | configuration (0.86) | configuration (0.98) | configuration (0.79) | configuration (0.96) | configuration (0.98) | configuration (0.96) | configuration (0.88) | configuration (1.00) | linter (0.73) | configuration (0.60) | configuration (1.00) | configuration (0.98) | configuration (1.00) | configuration (0.96) | `requires-python` discovery is inconsistent with config file discovery |
| #25105 | linter | linter (0.74) | formatter (0.47) | linter (0.92) | linter (0.99) | linter (0.99) | linter (0.96) | linter (0.95) | linter (0.99) | linter (0.88) | linter (1.00) | linter (1.00) | linter (0.98) | linter (1.00) | linter (0.94) | linter (0.99) | linter (0.99) | linter (0.67) | linter (0.59) | linter (1.00) | linter (0.98) | linter (1.00) | linter (1.00) | `pyupgrade` should rewrite `abc.{abstractclassmethod, abstractstaticm… |
