# Awesome Hermes Agent — Full Setup Guide

Install **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** (Nous Research), add skills, GUIs, and integrations from the **[awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent)** ecosystem — the self-improving agent with a built-in learning loop.

Part of the [Agentic AI Ecosystem](https://github.com/Ayush7614/agentic-ai-ecosystem).

## Architecture

```mermaid
flowchart LR
    A[You] --> B[Hermes CLI / Gateway]
    B --> C[LLM Provider]
    B --> D[Tools + MCP]
    B --> E[Skills ~/.hermes/skills]
    B --> F[Memory + Curator]
    E --> G[Community ecosystem]
    G --> H[wondelai/skills]
    G --> I[GUI dashboards]
    G --> J[Plugins + bridges]
    F -->|7-day cycle| E
    B --> K[18+ messaging platforms]
```

| Layer | What it is |
|-------|------------|
| **Hermes core** | CLI, gateway, 60+ tools, cron, profiles |
| **Learning loop** | Creates skills from experience; Curator grades/prunes (v0.12+) |
| **Skills** | Procedural memory — `/skill` or auto-invoked |
| **Plugins / MCP** | Extend tools, memory, search, payments |
| **Ecosystem** | Community skills, GUIs, deployment, multi-agent |

## Session workflow

1. Install **Hermes** → configure **LLM provider**  
2. Layer **skills & plugins** → **tools & utilities** → **integrations**  
3. Add **multi-agent** orchestration; **Curator** improves skills every 7 days  

## Workflow diagram

![Hermes ecosystem workflow — animated](./assets/hermes-ecosystem-workflow.gif)

**Maturity tags** (used throughout the [ecosystem catalog](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/ecosystem/)):

| Tag | Meaning |
|-----|---------|
| `production` | Stable, documented — safe to build on |
| `beta` | Works, still evolving |
| `experimental` | Early POC — learn, don't depend |

## Where do I start?

1. **Install Hermes** — one-line installer ([Part 1](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/tutorial/#part-1--install-hermes-agent))
2. **Choose provider** — `hermes setup --portal` or `hermes model` ([Part 2](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/tutorial/#part-2--choose-a-provider))
3. **Skills & plugins** — `./install-ecosystem.sh skills plugins` ([Part 4](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/tutorial/#part-4--skills--plugins))
4. **Tools & utilities** — GUIs, SkillClaw, camofox ([Part 5](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/tutorial/#part-5--tools--utilities))
5. **Integrations & bridges** — MCP, memory, M365 ([Part 6](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/tutorial/#part-6--integrations--bridges))
6. **Multi-agent & swarms** — oh-my-hermes, ACP, mission-control ([Part 7](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/tutorial/#part-7--multi-agent--swarms))

## Quick start

```bash
# 1. Install Hermes (macOS / Linux / WSL)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.zshrc   # or ~/.bashrc

# 2. Provider + Tool Gateway (easiest)
hermes setup --portal

# 3. Verify
cd guides/awesome-hermes-agent
chmod +x verify-install.sh install-starter-pack.sh
./verify-install.sh

# 4. First chat
hermes --tui

# 5. Ecosystem layers (pick one or all)
./install-ecosystem.sh skills
./install-ecosystem.sh plugins
./install-ecosystem.sh tools
./install-ecosystem.sh integrations
./install-ecosystem.sh multiagent
# ./install-ecosystem.sh all
```

Official docs: [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)

## What's in this guide

| File | Purpose |
|------|---------|
| TUTORIAL.md | Full install → skills → GUI → gateway → level-up |
| ECOSYSTEM.md | Curated catalog ([online](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/ecosystem/)) |
| `verify-install.sh` | Health check after install |
| `install-starter-pack.sh` | Lightweight skills only (wondelai + litprog) |
| `install-ecosystem.sh` | Layered installer: skills, plugins, tools, integrations, multiagent |
| `.env.example` | Optional API key reference |
| `assets/hermes-ecosystem-workflow.{html,gif,png}` | Animated ecosystem diagram |
| `assets/render_diagrams.py` | Regenerate workflow GIF/PNG |
| `assets/blog-poster-1200x600.png` | 1200×600 blog header image |
| `assets/render_blog_poster.py` | Regenerate poster from HTML |

## Full tutorial

**[Read the full tutorial →](./TUTORIAL.md)** · [Online](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/tutorial/)

## Related guides in this repo

| Guide | Overlap |
|-------|---------|
| [Hermes vs OpenClaw](../hermes-vs-openclaw/) | Full comparison — architecture, skills, `hermes claw migrate`, when to pick which |
| [OpenClaw + Gemma + RAG](../openclaw-gemma-rag/) | Messaging assistant pattern; Hermes has native gateway + OpenClaw migration |
| [Claude Code `.claude/`](../claude-code-dot-claude/) | Skills standard (agentskills.io) works across Hermes, Claude, Cursor |

## License

MIT — ecosystem list attribution: [awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent) (CC BY 4.0).
