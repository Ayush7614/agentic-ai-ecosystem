---
name: fix-issue
description: Triage and implement a fix for a GitHub issue number or URL. Use when the user references an issue ID or asks to fix a bug ticket.
---

# Fix issue workflow

1. Fetch issue context (title, body, labels) if a number or URL was given.
2. Reproduce the bug — identify the failing path or test.
3. Propose a minimal fix; avoid scope creep.
4. Add or update tests that fail without the fix.
5. Summarize: root cause, fix, how to verify.

If reproduction is unclear, ask one focused question before editing.
