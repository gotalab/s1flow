# gh-ruff-area

2026-10-22 · 520 labelled (linter 264, configuration 142, formatter 69, server 45) · split: stratified k-fold (90 test cases of the fixed evaluation set held out) · source: GitHub issues of astral-sh/ruff (labels applied by maintainers)

**d1-ultra@openrouter** has the highest coverage at 95% accuracy, 86% [82, 89] (API cost $0.17 per 10k, p99 1741ms). Its interval overlaps with clef-omni@openrouter, decider@openrouter, span@openrouter: at this many cases the difference is not shown. Of those, compared by p90 latency, then API cost, **clef-omni@openrouter** is chosen (API cost $0.76 per 10k, p99 974ms). The highest accuracy (all cases) is decider@openrouter's, 90% [88, 93].

## Comparison

| model | scored | accuracy | macro-F1 | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |
|---|---|---|---|---|---|---|---|---|---|
| clef ✕ | 300 | 93.3% [90, 96] | 0.86 | 0.97 | 0.01 | 92% [88, 95] | 94.3% (90.7%) | 0/520 | 220/520 |
| clef-flash ✕ | 300 | 92.3% [89, 95] | 0.81 | 0.95 | 0.05 | 95% [92, 98] | 94.5% (91.1%) | 0/520 | 220/520 |
| clef-omni@openrouter | 520 | 87.9% [85, 91] | 0.86 | 0.98 | 0.04 | 81% [77, 85] | 94.2% (91.4%) | 0/520 | 0/520 |
| d1-ultra@openrouter | 520 | 89.8% [87, 92] | 0.89 | 0.99 | 0.03 | 86% [82, 89] | 94.8% (92.3%) | 0/520 | 0/520 |
| d1@vercel | 520 | 83.7% [80, 87] | 0.81 | 0.98 | 0.07 | 73% [68, 78] | 94.7% (91.9%) | 0/520 | 0/520 |
| decider-flash@openrouter | 520 | 82.9% [79, 86] | 0.80 | 0.98 | 0.07 | 67% [62, 71] | 95.4% (92.6%) | 0/520 | 0/520 |
| decider@openrouter | 520 | 90.4% [88, 93] | 0.89 | 0.99 | 0.01 | 86% [82, 89] | 94.8% (92.2%) | 0/520 | 0/520 |
| decision-1@openrouter | 520 | 83.7% [80, 87] | 0.82 | 0.98 | 0.06 | 69% [64, 73] | 94.4% (91.3%) | 0/520 | 0/520 |
| drex@openrouter | 520 | 81.9% [79, 85] | 0.79 | 0.98 | 0.05 | 71% [66, 76] | 95.3% (92.6%) | 0/520 | 0/520 |
| flash-lite@vercel ※ ✕ | 300 | 91.7% [88, 95] | 0.80 | 0.86 | 0.08 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| haiku@vercel ※ ✕ | 300 | 91.3% [88, 94] | 0.83 | 0.92 | 0.09 | 0% [0, 0] | — (0.0%) | 0/300 | 0/300 |
| jev | 520 | 84.2% [81, 87] | 0.81 | 0.98 | 0.08 | 76% [72, 80] | 94.5% (91.7%) | 0/520 | 0/520 |
| jev@vercel ✕ | 300 | 91.7% [88, 94] | 0.79 | 0.96 | 0.06 | 92% [88, 96] | 95.3% (92.0%) | 0/300 | 0/300 |
| kev@openrouter ✕ | 300 | 90.0% [87, 93] | 0.75 | 0.96 | 0.21 | 84% [79, 89] | 94.9% (91.2%) | 0/300 | 0/300 |
| luna@decisions ✕ | 300 | 92.0% [89, 95] | 0.79 | 0.94 | 0.06 | 92% [88, 96] | 95.3% (92.0%) | 0/300 | 0/300 |
| solar-flash@openrouter | 520 | 83.8% [80, 87] | 0.81 | 0.95 | 0.05 | 39% [34, 44] | 93.6% (89.1%) | 0/520 | 0/520 |
| span@openrouter | 520 | 87.9% [85, 91] | 0.87 | 0.98 | 0.07 | 80% [75, 84] | 94.8% (92.1%) | 0/520 | 0/520 |

Not compared: clef (220 cases whose every call failed); clef-flash (220 cases whose every call failed); flash-lite@vercel (220 cases never asked); haiku@vercel (220 cases never asked); jev@vercel (220 cases never asked); kev@openrouter (220 cases never asked); luna@decisions (220 cases never asked). With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered, so it is neither ranked nor chosen. Ask them again: `s1flow run gh-ruff-area --models clef,clef-flash,flash-lite@vercel,haiku@vercel,jev@vercel,kev@openrouter,luna@decisions`

Answered by: clef = clef; clef-flash = clef-flash; clef-omni@openrouter = cloudflare/clef-omni-20261009; d1-ultra@openrouter = liquid/d1-ultra-20261015; d1@vercel = liquid/d1; decider-flash@openrouter = perplexity/pplx-decider-flash-v1.2-20261016; decider@openrouter = perplexity/pplx-decider-v1.2-20261016; decision-1@openrouter = microsoft/microsoft-decision-1-20261009; drex@openrouter = nace-ai/drex-v2.0-20261009; flash-lite@vercel = vercel_ai_gateway/google/gemini-3.1-flash-lite; haiku@vercel = vercel_ai_gateway/anthropic/claude-haiku-4.5; jev = jev-1.13.0 (also jev-1.14.0); jev@vercel = typesafe-ai/jev; kev@openrouter = jaredpalmer/kev-4b-20260924; luna@decisions = gpt-6-luna; solar-flash@openrouter = upstage/solar-decide-flash-20261008; span@openrouter = respan/span-02-20261015. To compare versions, run each by name: `s1flow run <task> --models jev:1.14`.

## Objectives and constraints

| model | coverage at 95% accuracy | rule | constraints |
|---|---|---|---|
| clef-omni@openrouter ◎ | 81% [77, 85] | 0.78 | met |
| d1-ultra@openrouter | 86% [82, 89] | 0.72 | met |
| decider@openrouter | 86% [82, 89] | 0.77 | met |
| span@openrouter | 80% [75, 84] | 0.92 | met |
| jev | 76% [72, 80] | 0.92 | met |
| d1@vercel | 73% [68, 78] | 0.87 | met |
| drex@openrouter | 71% [66, 76] | 0.79 | met |
| decision-1@openrouter | 69% [64, 73] | 0.90 | met |
| decider-flash@openrouter | 67% [62, 71] | 0.91 | met |
| solar-flash@openrouter | 39% [34, 44] | 0.98 | met |

◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost (the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little.

## Calls (latency and API cost)

| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency | API cost per 10k | source | frontier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 300 | 416 ms | 730 ms | 1147 ms | 1216 ms | 2.8 | not recorded | unknown | $1.23 | estimated |  |
| clef-flash | 300 | 203 ms | 381 ms | 548 ms | 1144 ms | 2.7 | not recorded | unknown | $0.46 | estimated |  |
| clef-omni@openrouter | 520 | 338 ms | 448 ms | 974 ms | 1980 ms | 2.9 | 0 | 8 | $0.76 | billed | ○ |
| d1-ultra@openrouter | 520 | 519 ms | 589 ms | 1741 ms | 2273 ms | 3.4 | 0 | 8 | $0.17 | billed | ○ |
| d1@vercel | 520 | 394 ms | 534 ms | 1012 ms | 1165 ms | 2.6 | 0 (300 not recorded) | 8 (300 unknown) | $0.13 | billed | ○ |
| decider-flash@openrouter | 520 | 521 ms | 542 ms | 1703 ms | 2267 ms | 3.3 | 0 | 8 | $0.05 | billed | ○ |
| decider@openrouter | 520 | 544 ms | 647 ms | 1244 ms | 2223 ms | 2.3 | 0 | 8 | $0.09 | billed | ○ |
| decision-1@openrouter | 520 | 522 ms | 549 ms | 1822 ms | 2464 ms | 3.5 | 0 | 8 | $0.16 | billed |  |
| drex@openrouter | 520 | 523 ms | 825 ms | 1709 ms | 2368 ms | 3.3 | 25 | 8 | $0.22 | billed |  |
| flash-lite@vercel | 300 | 1255 ms | 1573 ms | 2459 ms | 8530 ms | 2.0 | not recorded | unknown | $1.50 | estimated |  |
| haiku@vercel | 300 | 987 ms | 1269 ms | 1948 ms | 9369 ms | 2.0 | not recorded | unknown | $7.14 | estimated |  |
| jev | 520 | 175 ms | 229 ms | 339 ms | 418 ms | 1.9 | 0 (300 not recorded) | 8 (300 unknown) | $0.29 | estimated | ○ |
| jev@vercel | 300 | 341 ms | 509 ms | 812 ms | 981 ms | 2.4 | not recorded | unknown | $0.29 | billed |  |
| kev@openrouter | 300 | 985 ms | 1204 ms | 1877 ms | 2150 ms | 1.9 | not recorded | unknown | $0.16 | billed |  |
| luna@decisions | 300 | 256 ms | 297 ms | 454 ms | 696 ms | 1.8 | not recorded | unknown | $0.47 | estimated |  |
| solar-flash@openrouter | 520 | 547 ms | 642 ms | 1540 ms | 2209 ms | 2.8 | 0 | 8 | $0.35 | billed |  |
| span@openrouter | 520 | 520 ms | 904 ms | 2479 ms | 2635 ms | 4.8 | 0 | 8 | $0.05 | billed | ○ |

Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of the primary objective, API cost per 10k and p99.
Latency is the time from sending to receiving one call that answered (the round trip from here included), without retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's connections: to compare models, measure every candidate again at the same concurrency (`s1flow run <task> --fresh --concurrency N`, the same N for all).
Some calls were made at another concurrency, or at one not recorded.
"not recorded": calls made before 2026-10-16, whose time may include a retry's wait.
Where the API costs come from: billed: clef-omni@openrouter, d1-ultra@openrouter, d1@vercel, decider-flash@openrouter, decider@openrouter, decision-1@openrouter, drex@openrouter, jev@vercel, kev@openrouter, solar-flash@openrouter, span@openrouter; estimated (recorded tokens times a list price: s1flow.toml's where dated, else the LLM price table's; not a bill): clef (list price of 2026-10-04), clef-flash (list price of 2026-10-04), flash-lite@vercel, haiku@vercel, jev (list price of 2026-10-03), luna@decisions (list price of 2026-10-09). Billed and estimated API costs sit side by side, so their differences do not compare as they are.

## API cost and time for these cases

| model | API cost, total | time | per 10k (estimate) | concurrency |
|---|---|---|---|---|
| clef | $0.04 | 18 s (measured, 300 calls) | 10 min | 8 |
| clef-flash | $0.01 | 9 s (measured, 300 calls) | 5 min | 8 |
| clef-omni@openrouter | $0.04 | 25 s (measured, 520 calls) | 8 min | 8 |
| d1-ultra@openrouter | $0.0087 | 37 s (measured, 520 calls) | 12 min | 8 |
| d1@vercel | $0.0066 | 18 s (measured, 300 calls) | 10 min | 8 |
| decider-flash@openrouter | $0.0024 | 36 s (measured, 520 calls) | 12 min | 8 |
| decider@openrouter | $0.0047 | 38 s (measured, 520 calls) | 12 min | 8 |
| decision-1@openrouter | $0.0086 | 37 s (measured, 520 calls) | 12 min | 8 |
| drex@openrouter | $0.01 | 43 s (measured, 520 calls) | 14 min | 8 |
| haiku@vercel | $0.21 | 41 s (measured, 300 calls) | 23 min | 8 |
| jev | $0.01 | 5 s (measured, 220 calls) | 4 min | 8 |
| jev@vercel | $0.0087 | 15 s (measured, 300 calls) | 8 min | 8 |
| luna@decisions | $0.01 | 10 s (measured, 300 calls) | 6 min | 8 |
| solar-flash@openrouter | $0.02 | 36 s (measured, 520 calls) | 12 min | 8 |
| span@openrouter | $0.0025 | 43 s (measured, 520 calls) | 14 min | 8 |

Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model.

Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target 95%. The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.
Scored: the cases with an answer, scored (the test share too). Refused / unsupported and failed both count calls.
※ a model that returns no distribution (one answer): its probability is only the agreement of its repeated answers, so with one repeat the coverage is all or nothing.

## Test (read once, at the end)

| model | cases | accuracy | coverage | sure accuracy | primary objective |
|---|---|---|---|---|---|
| clef | 90 | 95.6% | 91% | 95.1% | 0.911 |
| clef-flash | 90 | 91.1% | 97% | 92.0% | 0.967 |
| clef-omni@openrouter | 159 | 86.2% | 70% | 93.8% | 0.704 |
| d1-ultra@openrouter | 159 | 89.9% | 81% | 96.9% | 0.805 |
| d1@vercel | 159 | 82.4% | 71% | 92.0% | 0.711 |
| decider-flash@openrouter | 159 | 81.1% | 64% | 97.1% | 0.642 |
| decider@openrouter | 159 | 91.2% | 84% | 96.3% | 0.843 |
| decision-1@openrouter | 159 | 81.8% | 69% | 92.7% | 0.692 |
| drex@openrouter | 159 | 79.2% | 69% | 92.7% | 0.692 |
| flash-lite@vercel | 90 | 91.1% | 0% | — | 0.000 |
| haiku@vercel | 90 | 95.6% | 0% | — | 0.000 |
| jev | 159 | 81.1% | 71% | 92.0% | 0.711 |
| jev@vercel | 90 | 92.2% | 88% | 96.2% | 0.878 |
| kev@openrouter | 90 | 90.0% | 89% | 91.2% | 0.889 |
| luna@decisions | 90 | 93.3% | 93% | 94.0% | 0.933 |
| solar-flash@openrouter | 159 | 80.5% | 30% | 93.8% | 0.302 |
| span@openrouter | 159 | 86.2% | 75% | 95.0% | 0.755 |

## Wrong at a high probability (0.9 or more)

**clef** (10)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #24528 | linter | formatter | 0.98 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #27602 | configuration | formatter | 0.96 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| #23705 | configuration | linter | 0.95 | BLE001 (blind-except) add option to flag even if logger.exception / e… |
| #23855 | formatter | server | 0.93 | Ruff: Format document with an open markdown file results in an error |
| #28641 | linter | formatter | 0.92 | option to enable lint python codeblocks |
| #27607 | configuration | formatter | 0.92 | ruff rejects documented `indent-width` setting |

**clef-flash** (4)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #23855 | formatter | server | 0.97 | Ruff: Format document with an open markdown file results in an error |
| #23856 | formatter | server | 0.93 | Document editor support for markdown formatting |
| #27224 | configuration | linter | 0.92 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.92 | [Infinite loop] TID254 when an import statement has conflicting lazin… |

**clef-omni@openrouter** (8)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#9984 | configuration | formatter | 0.95 | {"title": "Colorize `format --diff` output", "body": "### Discussed i… |
| prod:#20035 | configuration | formatter | 0.94 | {"title": "`ruff format` can double count formatted files", "body": "… |
| prod:#20280 | configuration | linter | 0.93 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#13607 | configuration | formatter | 0.93 | {"title": "Ruff doesn't seem to respect the maximum line length", "bo… |
| #23855 | formatter | server | 0.93 | Ruff: Format document with an open markdown file results in an error |
| #24409 | linter | formatter | 0.92 | [Fix error] Fix for E502 introduces syntax error |
| prod:#1773 | linter | configuration | 0.90 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |
| #27224 | configuration | linter | 0.90 | SIM118 complains about .keys() even when the object isn't a dict |

**d1-ultra@openrouter** (3)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.96 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#19701 | configuration | linter | 0.95 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |

**d1@vercel** (19)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#19701 | configuration | linter | 1.00 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #23705 | configuration | linter | 0.99 | BLE001 (blind-except) add option to flag even if logger.exception / e… |
| #23856 | formatter | server | 0.98 | Document editor support for markdown formatting |
| #24955 | configuration | linter | 0.97 | [pydocstyle] allow configuring indentation level for Google style |
| #26756 | configuration | linter | 0.97 | [`flake8-async`] Allow configuring safe decorators for `ASYNC119` |

**decider-flash@openrouter** (17)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 0.99 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#9984 | configuration | formatter | 0.97 | {"title": "Colorize `format --diff` output", "body": "### Discussed i… |
| prod:#19701 | configuration | linter | 0.97 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |
| prod:#20035 | configuration | formatter | 0.97 | {"title": "`ruff format` can double count formatted files", "body": "… |
| prod:#13419 | configuration | formatter | 0.96 | {"title": "provide a exit code for `ruff format` (without --check) fo… |
| prod:#9132 | configuration | formatter | 0.95 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |

**decider@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#19701 | configuration | linter | 0.99 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |
| prod:#18310 | configuration | linter | 0.98 | {"title": "Add `torch.nn.functional as F` to flake8-import-convention… |
| prod:#20280 | configuration | linter | 0.97 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#8248 | linter | configuration | 0.92 | {"title": "Proposal: HTML output file", "body": "Would it be possible… |
| #23705 | configuration | linter | 0.90 | BLE001 (blind-except) add option to flag even if logger.exception / e… |

**decision-1@openrouter** (22)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#19701 | configuration | linter | 0.99 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |
| prod:#20280 | configuration | linter | 0.99 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#7804 | configuration | linter | 0.98 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| #26480 | configuration | linter | 0.98 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| prod:#15375 | formatter | linter | 0.97 | {"title": "Implicit concatenated f-string: Trailing end-of-line comme… |
| #23705 | configuration | linter | 0.97 | BLE001 (blind-except) add option to flag even if logger.exception / e… |

**drex@openrouter** (7)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #27224 | configuration | linter | 0.99 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#19701 | configuration | linter | 0.98 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |
| #26221 | linter | server | 0.96 | `PLC2801` gives suggestions differentially for the `__floor__`, `__ce… |
| prod:#20280 | configuration | linter | 0.96 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #27602 | configuration | formatter | 0.92 | `ruff format --check` uses same exit code for syntax errors in files,… |
| prod:#4343 | configuration | linter | 0.90 | {"title": "Expose explanation for a code", "body": "In https://github… |

**flash-lite@vercel** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #24955 | configuration | linter | 1.00 | [pydocstyle] allow configuring indentation level for Google style |
| #24845 | configuration | linter | 1.00 | Allow configuring some exception types to be ignored by B904 |
| #24528 | linter | formatter | 1.00 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #23855 | formatter | server | 1.00 | Ruff: Format document with an open markdown file results in an error |
| #23856 | formatter | server | 1.00 | Document editor support for markdown formatting |
| #23590 | linter | configuration | 1.00 | `ruff` should respect `pyproject.toml` existence for first-party scra… |
| #23705 | configuration | linter | 1.00 | BLE001 (blind-except) add option to flag even if logger.exception / e… |
| #23953 | server | configuration | 1.00 | Option 'extend-select' appears to be ignored. |

**haiku@vercel** (26)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #24955 | configuration | linter | 1.00 | [pydocstyle] allow configuring indentation level for Google style |
| #24840 | configuration | server | 1.00 | Can the ruff color "All checks passed!" be made consistent with ty pl… |
| #25418 | linter | configuration | 1.00 | Conflict (infinite loop) between `lazy-import-mismatch (TID254)` and … |
| #25216 | linter | configuration | 1.00 | D1XX for private code |
| #25652 | linter | configuration | 1.00 | `ASYNC119`: allow some context managers and async context managers to… |
| #24528 | linter | formatter | 1.00 | `ruff format --check` outputs wrong line line/column numbers on synta… |
| #23855 | formatter | server | 1.00 | Ruff: Format document with an open markdown file results in an error |
| #23856 | formatter | server | 1.00 | Document editor support for markdown formatting |

**jev** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #23705 | configuration | linter | 1.00 | BLE001 (blind-except) add option to flag even if logger.exception / e… |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| prod:#19701 | configuration | linter | 1.00 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| prod:#7804 | configuration | linter | 0.99 | {"title": "Bug: `ruff rule` shows `PLR6301` as non-preview", "body": … |
| prod:#9984 | configuration | formatter | 0.98 | {"title": "Colorize `format --diff` output", "body": "### Discussed i… |
| prod:#1773 | linter | configuration | 0.98 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |

**jev@vercel** (12)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #23705 | configuration | linter | 1.00 | BLE001 (blind-except) add option to flag even if logger.exception / e… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #27448 | configuration | linter | 0.98 | Add option to suppress `PLR6301` for custom instance method decorators |
| #27602 | configuration | formatter | 0.97 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #24955 | configuration | linter | 0.97 | [pydocstyle] allow configuring indentation level for Google style |
| #26480 | configuration | linter | 0.95 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| #26418 | formatter | linter | 0.95 | Ability to suppress PEP 758 check |

**luna@decisions** (13)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #23705 | configuration | linter | 1.00 | BLE001 (blind-except) add option to flag even if logger.exception / e… |
| #27647 | configuration | linter | 1.00 | collapsible-if rule obscures conditional structure |
| #27602 | configuration | formatter | 1.00 | `ruff format --check` uses same exit code for syntax errors in files,… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| #27448 | configuration | linter | 1.00 | Add option to suppress `PLR6301` for custom instance method decorators |
| #26480 | configuration | linter | 1.00 | `ruff check --add-noqa` / `--fix` / `ruff format` truncate source fil… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #26756 | configuration | linter | 1.00 | [`flake8-async`] Allow configuring safe decorators for `ASYNC119` |

**solar-flash@openrouter** (25)

| id | label | answer | probability | case |
|---|---|---|---|---|
| #27448 | configuration | linter | 0.99 | Add option to suppress `PLR6301` for custom instance method decorators |
| prod:#9132 | configuration | formatter | 0.99 | {"title": "`ruff format --check` outputs \"files left unchanged\", wh… |
| prod:#18728 | configuration | linter | 0.99 | {"title": "Request: Making `import-outside-top-level (PLC0415)` confi… |
| prod:#20035 | configuration | formatter | 0.99 | {"title": "`ruff format` can double count formatted files", "body": "… |
| prod:#20280 | configuration | linter | 0.98 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 0.98 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #23705 | configuration | linter | 0.98 | BLE001 (blind-except) add option to flag even if logger.exception / e… |
| #24528 | linter | formatter | 0.98 | `ruff format --check` outputs wrong line line/column numbers on synta… |

**span@openrouter** (24)

| id | label | answer | probability | case |
|---|---|---|---|---|
| prod:#19701 | configuration | linter | 1.00 | {"title": "D104: ignore empty files", "body": "`D104 Missing docstrin… |
| #27224 | configuration | linter | 1.00 | SIM118 complains about .keys() even when the object isn't a dict |
| prod:#20280 | configuration | linter | 1.00 | {"title": "Relax DOC rules for private/inner methods", "body": "### S… |
| #26450 | configuration | linter | 1.00 | [Infinite loop] TID254 when an import statement has conflicting lazin… |
| #23856 | formatter | server | 0.98 | Document editor support for markdown formatting |
| #27177 | configuration | linter | 0.98 | Please remove all rules without an automated fix from default rules |
| prod:#9984 | configuration | formatter | 0.97 | {"title": "Colorize `format --diff` output", "body": "### Discussed i… |
| prod:#1773 | linter | configuration | 0.97 | {"title": "Human-friendly rule names", "body": "Pylint, ESLint and Cl… |


## Cases the models disagree on (12 of 65)

| id | label | clef | clef-flash | clef-omni@openrouter | d1-ultra@openrouter | d1@vercel | decider-flash@openrouter | decider@openrouter | decision-1@openrouter | drex@openrouter | flash-lite@vercel | haiku@vercel | jev | jev@vercel | kev@openrouter | luna@decisions | solar-flash@openrouter | span@openrouter | case |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #28945 | linter | linter (0.91) | linter (0.80) | formatter (0.74) | linter (0.88) | linter (1.00) | formatter (0.68) | linter (0.91) | linter (0.99) | linter (0.96) | linter (1.00) | linter (1.00) | linter (0.98) | linter (0.99) | linter (0.41) | linter (0.98) | linter (0.47) | linter (0.70) | RUF031 incorrectly-parenthesized-tuple-in-subscript: false negative |
| #28861 | linter | linter (0.97) | linter (0.81) | formatter (0.72) | linter (0.98) | linter (1.00) | linter (0.57) | linter (0.99) | linter (0.99) | linter (0.79) | linter (1.00) | linter (1.00) | linter (0.97) | linter (0.96) | formatter (0.39) | linter (0.99) | linter (0.86) | linter (0.53) | PLR1711 useless-return removes comments |
| #28857 | linter | linter (0.97) | linter (0.92) | formatter (0.52) | linter (0.96) | linter (0.99) | linter (0.90) | linter (1.00) | linter (0.99) | linter (0.96) | linter (1.00) | linter (1.00) | linter (0.99) | linter (0.98) | linter (0.50) | linter (1.00) | linter (0.50) | linter (0.99) | isort: fixer causes F401 unused-import |
| #28688 | linter | linter (0.90) | linter (0.80) | linter (0.73) | linter (0.79) | linter (0.93) | linter (0.89) | linter (0.93) | linter (0.87) | linter (0.76) | linter (1.00) | configuration (1.00) | linter (0.96) | linter (0.96) | linter (0.67) | linter (0.88) | linter (0.90) | linter (0.95) | `self-assigning-variable` - option to allow reassignment with type an… |
| #28641 | linter | formatter (0.92) | linter (0.52) | formatter (0.81) | linter (0.49) | formatter (0.32) | linter (0.42) | linter (0.43) | linter (0.82) | linter (0.48) | linter (1.00) | linter (1.00) | linter (0.62) | linter (0.65) | linter (0.42) | linter (0.86) | linter (0.61) | linter (0.79) | option to enable lint python codeblocks |
| #28618 | formatter | formatter (0.99) | formatter (0.87) | formatter (0.96) | formatter (0.89) | formatter (0.94) | formatter (0.94) | formatter (0.94) | formatter (0.84) | formatter (0.72) | formatter (1.00) | configuration (1.00) | formatter (0.97) | formatter (0.97) | formatter (0.55) | formatter (1.00) | formatter (0.89) | formatter (0.98) | Support ability to opt out of rewriting exceptions to PEP 758 `except… |
| #28604 | linter | linter (0.79) | linter (0.72) | linter (0.65) | linter (0.78) | configuration (0.59) | linter (0.75) | linter (0.83) | linter (0.80) | linter (0.71) | configuration (1.00) | configuration (1.00) | configuration (0.70) | configuration (0.68) | linter (0.55) | configuration (0.56) | linter (0.56) | linter (0.87) | Add `import datetime as dt` as a conventional alias |
| #28567 | linter | linter (0.74) | linter (0.78) | configuration (0.50) | linter (0.95) | linter (0.99) | linter (0.90) | linter (0.99) | linter (0.97) | linter (0.73) | linter (1.00) | linter (1.00) | linter (0.80) | linter (0.79) | linter (0.72) | linter (0.93) | linter (0.54) | linter (0.99) | Support flake8-if-expr |
| #28273 | configuration | configuration (0.67) | linter (0.56) | configuration (0.82) | configuration (0.61) | linter (0.79) | linter (0.70) | configuration (0.83) | linter (0.70) | linter (0.73) | configuration (1.00) | configuration (1.00) | linter (0.74) | linter (0.72) | linter (0.53) | linter (0.88) | configuration (0.56) | linter (0.65) | Please add "is `default` rule" info to the rule json data |
| #28220 | linter | linter (0.95) | linter (0.95) | linter (0.81) | linter (0.94) | linter (0.93) | linter (0.95) | linter (0.77) | linter (0.98) | linter (0.89) | formatter (1.00) | linter (1.00) | linter (0.99) | linter (0.99) | linter (0.70) | linter (1.00) | linter (0.88) | linter (0.96) | rule for formatting of line-level error suppression comment |
| #28105 | configuration | linter (0.61) | linter (0.83) | linter (0.53) | linter (0.55) | linter (0.92) | linter (0.80) | configuration (0.50) | linter (0.72) | linter (0.82) | linter (1.00) | configuration (1.00) | linter (0.84) | linter (0.86) | linter (0.59) | linter (0.92) | configuration (0.55) | linter (0.81) | Stabilize categories |
| #27759 | configuration | linter (0.57) | configuration (0.64) | configuration (0.86) | configuration (0.75) | configuration (0.68) | configuration (0.60) | configuration (0.80) | configuration (0.78) | configuration (0.50) | linter (1.00) | configuration (1.00) | linter (0.66) | linter (0.61) | configuration (0.45) | configuration (0.73) | configuration (0.62) | configuration (0.97) | ruff check --statistics --fix-only shows all errors, not just fixable… |
