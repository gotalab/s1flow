# Changelog

## Unreleased

### Added

- A built-in `gemini` provider for Google's own Decisions API on the Gemini API (`GEMINI_API_KEY`): Gemini
  Decision 1 without OpenRouter in between, with text, images, audio, video and PDFs. An input Google's safety
  filters block counts as refused for that case.
- `s1flow init`'s line-up adds Gemini Decision 1 (through OpenRouter, the same key), so a new project has a model
  that hears audio, watches video and reads PDFs. The line-up is now four models.
- Audio, video and PDFs as input: `{"type": "audio" | "video" | "pdf", "path" | "url"}` as top-level items of a
  list state, like images, and `decide --audio`, `--video`, `--pdf`. They are sent as the file's own bytes
  (WAV or MP3, MP4, PDF), the same to every model. How many and how large is each model's own limit: a model
  that refuses an input counts as refused for that case.
  A model declares `capabilities.audio`, `video`, `pdf`, and `s1flow models --verify` checks each with an input
  only a model that hears, watches or reads it can answer. Through OpenRouter, Gemini Decision 1 takes all three,
  Clef Omni audio and video, ScaleDown Classify 1 PDFs (the Skill's setup reference has their entries).

### Changed

- `ImageRef` is now `MediaRef`, and state preparation moved from `s1flow.client.images` to `s1flow.client.media`
  (`media.materialize`, `media.prepare(kind, data)`).
- s1flow no longer caps a state at 4 images; a model that takes fewer refuses the case, which counts as refused.

## 0.1.0a5 (2026-11-12)

### Added

- `policy.decide(state, timeout=SECONDS)` (and `adecide`) caps how long one decision may take, retries and their
  waits included. Past it the call is cancelled and `TimedOut`, a `ProviderError`, is raised and logged as
  `failed`. Without a limit, a throttled provider could hold one decision for minutes.

### Fixed

- An `llm` model on the AI Gateway fetched the gateway's price list on the event loop, holding every other call
  on it (and a timeout) until the fetch ended. It is fetched off the loop now.

## 0.1.0a4 (2026-11-12)

### Changed

- Every model call sends the state with the keys of each JSON object sorted, at any depth; lists keep their order.
  The request identity already ignored key order, so an evaluation case and a production call that differed only in
  key order counted as the same request while the model read different text. As after every release, `run` calls
  the models again instead of reusing answers recorded by an earlier one.

## 0.1.0a3 (2026-11-10)

### Changed

- The chart page (`scripts/charts.py`) opens on a table of every compared candidate across the task's objectives,
  the question type's metrics, API cost and latency, with the best per column highlighted and a ◆ on candidates no
  other matches or beats on every measure shown. Candidates never run and the details are folded away.
- `feedback record` calls no model, so it takes no `--connections` (passing one is a usage error).
- `init --ci` outside a Git repository exits 2 and says why, instead of writing the project without the workflow.
  A bad `--task` id is also refused before anything is written.

### Added

- `doctor --policy TASK --path policies.json --connections FILE` checks a policy from an exported file, outside an
  s1flow project.

### Fixed

- The `policies.load(...)` line `export` prints names `client=`.
- `report` on a task whose cases file is missing, and `feedback measure` on a log that is missing, print one error
  line (exit 2) instead of a traceback.
- `doctor` names a project's Skill copy written by an earlier alpha (0.1.0a2 under 0.1.0a3); the alpha number was
  ignored. Its hint is `s1flow init --skill`, which already updates the files s1flow wrote, without `--force`.
- `init` adds `.write.lock` (the policy store's lock file) to the project's `.gitignore`.
- A `.env` value in quotes followed by a comment (`KEY="value" # note`) is read without the quotes and the comment.
- `adopt` records no `git_sha` in a repository without a commit; it recorded the word `HEAD`.
- The Skill's `scripts/github.py`: the day after a labelling is 24 hours in every time zone (it was 23 where summer
  time applies), and a call that keeps hitting GitHub's secondary rate limit stops with that reason.
- The generated check workflow's comment gives the `doctor --policy` command with the `--connections` it needs.

## 0.1.0a2 (2026-11-01)

### Breaking changes

0.1.0a1 had almost no users, so these come with no migration path: a file in an older format is refused.

- The CLI has 12 commands. `compare` and `rank` are `report`; `tasks` is `report` with no task; `policy create`
  and `policy validate` are `adopt --spec` (with `--check` to validate only); `policy export` is `export`;
  `skill install` is `init --skill`; `optimize prompt` is `optimize`. `promote`, `guide`, `skill path` and
  `github` are gone (the Skill's `scripts/github.py` fetches from GitHub).
- Merging the pull request is the release: `adopt` saves the next version and makes it current. A policy is
  `TASK` or `TASK@vN`; the `next` and named channels are gone. Each switch appends to `policies/<task>/history.jsonl`.
- `adopt` refuses a candidate below on the held-out test unless `--force`. `optimize` writes a candidate and
  makes nothing current. Only `s1flow run` writes `split.json`.
- `check` asks both versions again and compares current with `--against vN`. The Action fails a pending check
  by default, and a pull request that rewrites, renames or removes a saved version.
- `report` marks no pick: `=` marks the candidates tied at the top, ordered only by task.py's `tiebreak`.
- `feedback measure` only measures; `--add` also adds the cases.
- `optimize` runs the optimizer task.py names (`Gepa` by default).
- Files now read only as `s1flow/policy-evaluation@3`, `s1flow/split@2`, `s1flow/optimized@2` and `s1flow/run@2`.
- Evaluation records, runs and cached answers written before retries, case counts and evidence digests were
  recorded are no longer read.
- `S1FLOW_CONNECTIONS` is gone: pass `--connections PATH`, else the project's `s1flow.toml` is read.
- `s1flow init` inside a project adds to it. The Agent Skill is one `SKILL.md` and six references by stage.

### Added

- A task can ask a `Score` question (levels 0 to L-1): `MAE()` is its default objective, with `QWK()` and
  `Accuracy()` of the rounded level; comparison, report and charts read it. A policy still holds a boolean or
  choice question.
- `s1flow models` runs on the base install. `s1flow models --verify` needs only `s1flow[images]`; before, both
  needed `s1flow[eval]` and `s1flow[images]`.
- `tiebreak` takes `"latency"` and `"cost"` beside objectives, in the order that ranks the tied candidates
  (`tiebreak=["cost", "latency"]` puts API cost first).
- `s1flow init --task` writes every default into task.py: `split=Split(test=0.3, k=5, seed=1)`,
  `objective=Accuracy()`, `tiebreak=["latency", "cost"]`, `constraints=Constraints()`. The task measures as it
  did with them left out, and orders tied candidates as 0.1.0a1 did.
