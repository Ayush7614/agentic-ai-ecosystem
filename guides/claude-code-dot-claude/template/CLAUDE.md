# Project instructions for Claude Code

You are working in the **Agentic AI Ecosystem** sample app. Follow these team defaults unless a `.claude/rules/` file overrides them for a specific path.

## Stack

- Python 3.10+ for backend scripts
- TypeScript for any frontend tooling
- Prefer small, focused diffs — no drive-by refactors

## Workflow

1. Read relevant files before editing.
2. Run tests or linters mentioned in `.claude/rules/testing.md` before claiming work is done.
3. Use `/project:review` before opening a PR.
4. Never commit secrets, `.env` files, or `settings.local.json`.

## Commands you can use

| Slash command | Purpose |
|---------------|---------|
| `/project:review` | Structured code review |
| `/project:fix-issue` | Triage and fix a GitHub issue |
| `/project:deploy` | Run the deploy checklist skill |

## Agents

Delegate when the task fits:

- **code-reviewer** — diff review, style, missing tests
- **security-auditor** — auth, secrets, injection surfaces

## Repo layout

```
src/           # application code
tests/         # pytest suite
.claude/       # Claude Code project config (commit this)
```
