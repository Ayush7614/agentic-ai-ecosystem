---
name: deploy
description: Run the pre-deploy checklist. Use when the user says deploy, release, or ship to production.
disable-model-invocation: true
---

# Deploy checklist

Walk through each step. Stop and ask if any step fails.

1. `git status` — working tree clean
2. `pytest -q` — all tests green
3. Bump version in `pyproject.toml` or `package.json` if needed
4. Update `CHANGELOG.md` with user-facing notes
5. Create annotated tag: `git tag -a vX.Y.Z -m "..."`
6. Push branch and tags (user confirms remote)

Do **not** run deploy commands against production without explicit user confirmation.
