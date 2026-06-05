---
name: code-review
description: Run a structured code review on the current diff or specified files. Use before opening a PR or when the user asks for review.
---

# Code review

Review the changed code against team standards in `.claude/rules/`.

## Checklist

1. **Correctness** — logic bugs, edge cases, error handling
2. **Security** — secrets, injection, unsafe shell commands
3. **Tests** — new behavior covered; existing tests still pass
4. **Style** — matches `code-style.md`
5. **Scope** — no unrelated refactors

## Output format

```markdown
## Summary
<1–2 sentences>

## Findings
### Critical
- ...

### Suggestions
- ...

## Verdict
APPROVE | REQUEST_CHANGES
```

Run `git diff` if no files were specified. Suggest `pytest -q` when tests exist.
