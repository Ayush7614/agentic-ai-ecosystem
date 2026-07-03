# Google agents-cli Agent Masterclass

The **complete guide to Google's agents-cli** — CLI + skills that turn Claude Code, Codex, or Antigravity into experts at building, evaluating, and deploying **ADK agents** on Google Cloud.

**Official:** [github.com/google/agents-cli](https://github.com/google/agents-cli) · **Docs:** [google.github.io/agents-cli](https://google.github.io/agents-cli/) · **PyPI:** `google-agents-cli`

> **Not a coding agent** — a toolchain *for* coding agents. Scaffold → build → eval → deploy → observe.

## What you'll build

- `agents-cli` installed via `uvx google-agents-cli setup`
- A **caveman compressor** agent (official tutorial pattern) — or your own wild idea
- **7 verified terminal GIFs** — recorded with [VHS](https://github.com/charmbracelet/vhs), running real commands (no HTML mockups)
- Skills wired into Cursor / Claude Code for the full ADK lifecycle

![Verified install — real uvx output](./assets/step-01-install-verify.gif)

**One-GIF overview:** [mega-agents-cli-workflow.gif](assets/mega-agents-cli-workflow.gif) — version → scaffold → info → eval metrics.

## Quick start

```bash
# Prerequisites: Python 3.11+, uv, Node.js
uvx google-agents-cli setup

# Or skills only (coding agent does the rest)
npx skills add google/agents-cli

# Standalone CLI — scaffold a prototype agent
uvx google-agents-cli create my-agent --prototype --yes
cd my-agent && uvx google-agents-cli install && uvx google-agents-cli playground
```

## Guide map

- **[Full tutorial](./TUTORIAL.md)** — Parts 1–18 (install → caveman agent → eval → deploy → mind-blowing ideas)
- **[Examples](./examples/)** — caveman `agent.py`, `.agents-cli-spec.md`, OpenClaw-style prompts
- **[Assets](./assets/)** — **verified** VHS terminal GIFs + official Google architecture PNG

## Related guides

- [MCP Visual Guide](../mcp-visual-guide/) · [Harness Engineering](../harness-engineering/)
- [OpenClaude Agent Masterclass](../openclaude-agent-masterclass/) · [OpenCode Agent Masterclass](../opencode-agent-masterclass/)
- [AI Agents Masterclass](../ai-agents-masterclass/)

**Blog header:** `assets/blog-poster-1200x600.png` · Regenerate GIFs: `cd assets/tapes && vhs step-01-install.tape` (see `render_real_gifs.sh`)

## License

Guide: MIT · agents-cli: Apache-2.0 · Community tutorial — not affiliated with Google.
