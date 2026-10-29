The repository's triage bot assigns priorities with these rules (from .github/workflows/gemini-scheduled-issue-triage.yml, 2026-10-03):

- P0, urgent blocking: critical failures breaking core functionality for a large portion of users (CLI fails to launch globally, core commands crash on valid input, unhandled promise rejections on boot, critical security vulnerability). The bot never applies P0: it applies P1 and asks for manual triage instead.
- P1, critical but workable: severe issues without a reasonable workaround, significantly degrading the developer experience but not globally blocking (specific tools failing consistently, e.g. web_search returning 500s; persistent PTY streaming hangs; memory leaks leading to OOM after short use).
- P2, significant: affect some workflows but a clear workaround exists, or non-critical bugs (theme flickering, confusing error messages, minor UI misalignment, failing to read deeply nested config files).
- P3, minor or enhancements: trivial bugs, typos, documentation requests, or feature requests.
- If the issue is highly ambiguous, lacks a description, or sits between two lower priorities (P2 vs P3), the bot keeps an existing priority instead of changing it.
- The bot assigns the true priority by impact and does not downgrade for missing information.
- The bot reads the issue title, body, current labels and comments.
