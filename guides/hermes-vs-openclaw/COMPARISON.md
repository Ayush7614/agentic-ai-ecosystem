# Hermes vs OpenClaw — Feature Matrix

Detailed reference for the [comparison tutorial](https://ayush7614.github.io/agentic-ai-ecosystem/guides/hermes-vs-openclaw/tutorial/). Values reflect upstream docs as of mid-2026; verify with `hermes doctor` and `openclaw doctor` on your machine.

## Core platform

| Feature | Hermes Agent | OpenClaw |
|---------|--------------|----------|
| Maintainer | [Nous Research](https://nousresearch.com/) | OpenClaw community (orig. Peter Steinberger ecosystem) |
| Install | `curl -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash` | `npm install -g openclaw@latest` |
| Primary language | Python | TypeScript |
| CLI entry | `hermes` | `openclaw` |
| Interactive UI | `hermes --tui` | Web dashboard + channel chat |
| Daemon / always-on | `hermes gateway` | `openclaw onboard --install-daemon` (launchd/systemd) |
| Health check | `hermes doctor` | `openclaw doctor` |
| Config home | `~/.hermes/` | `~/.openclaw/` |

## Models & providers

| Feature | Hermes Agent | OpenClaw |
|---------|--------------|----------|
| Cloud APIs | Anthropic, OpenAI, Nous portal, others via `hermes setup` | Anthropic, OpenAI, Google, etc. via onboarding |
| Local / Ollama | Supported via provider configuration | [Ollama provider](https://docs.openclaw.ai/providers/ollama) — e.g. `gemma4:e2b` in [our guide](https://ayush7614.github.io/agentic-ai-ecosystem/guides/openclaw-gemma-rag/) |
| Model switching | `hermes model` | `openclaw.json` + onboarding |
| Recommended quality | Strongest latest-gen cloud model | Same — docs recommend strongest available model |

## Gateway & channels

| Feature | Hermes Agent | OpenClaw |
|---------|--------------|----------|
| Gateway command | `hermes gateway` | `openclaw gateway` (installed as daemon) |
| Channel count | 18+ messaging platforms (docs) | Core channels + bundled/external plugins |
| Named channels | Telegram, WhatsApp, Discord, Slack, … | Telegram, WhatsApp, Discord, Slack, Signal, Teams, Matrix, iMessage, Google Chat, WebChat, Zalo, … |
| DM security | Pairing / allowlists — run `hermes doctor` after changes | Channel-specific pairing; see [Security](https://docs.openclaw.ai/) |
| WebChat | Via gateway / TUI | Built-in WebChat |
| Mobile nodes | Apps in Hermes monorepo | macOS/iOS/Android speak + Canvas |

## Skills & workspace

| Feature | Hermes Agent | OpenClaw |
|---------|--------------|----------|
| Skill format | `SKILL.md` + YAML frontmatter | `SKILL.md` + YAML frontmatter |
| Default path | `~/.hermes/skills/<name>/` | `~/.openclaw/workspace/skills/<name>/` |
| Shared / global skills | Ecosystem + optional dirs | `~/.openclaw/skills` with `--global` install |
| Registry | Community ([awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent)) | [ClawHub](https://clawhub.ai) + `openclaw skills` |
| Install skill | Clone / ecosystem scripts | `openclaw skills install <id>` |
| Skill verification | Ecosystem maturity tags | `openclaw skills verify` (trust envelope) |
| Auto skill creation | **Yes** — learning loop writes skills from sessions | No — author or install skills |
| Skill curation | **Curator** grades/prunes (~7-day cycle, v0.12+) | Manual update via ClawHub / git |
| Injected prompts | Profiles, memory context | `AGENTS.md`, `SOUL.md`, `TOOLS.md` |

## Tools, MCP & automation

| Feature | Hermes Agent | OpenClaw |
|---------|--------------|----------|
| Built-in tools | 60+ (file, shell, browser, search, …) | Tool suite + session tools |
| MCP | First-class optional MCP servers | Supported in agent runtime |
| Plugins | `plugins/` + ecosystem | Channel plugins + skill plugins |
| Cron | `hermes cron` | [Cron jobs](https://docs.openclaw.ai/automation/cron-jobs) |
| Webhooks | Gateway integrations | [Webhooks](https://docs.openclaw.ai/automation/webhook) |
| Email triggers | Ecosystem / custom | [Gmail Pub/Sub](https://docs.openclaw.ai/automation/gmail-pubsub) |
| Remote sandboxes | Modal, Daytona, Vercel Sandbox | Docker sandbox (recommended) |

## Memory & learning

| Feature | Hermes Agent | OpenClaw |
|---------|--------------|----------|
| Session memory | Built-in + ecosystem memory plugins | Session history tools |
| Long-term memory | Memory layer + honcho/hindsight/plur (ecosystem) | Workspace + session stores |
| Self-improvement | **Core feature** — skills evolve from use | Skill updates manual / ClawHub |
| Evaluation loop | Curator + optional self-evolution packs | Operator-driven |

## Multi-agent

| Feature | Hermes Agent | OpenClaw |
|---------|--------------|----------|
| Native multi-agent | Profiles, delegation patterns | Multi-agent routing per docs |
| Ecosystem | oh-my-hermes, ACP skill, mission-control, opencode-hermes | Session tools, agent workspaces |
| Handoff to Codex/Claude | `hermes-agent-acp-skill` | Via agent runtime configuration |

## Migration & interoperability

| Path | Command / resource |
|------|-------------------|
| OpenClaw → Hermes (native) | `hermes claw migrate` |
| OpenClaw → Hermes (community) | [openclaw-to-hermes](https://github.com/0xNyk/openclaw-to-hermes) |
| Shared pattern | Both use `SKILL.md` — port skill folders and adapt tool paths |
| RAG sidecar | Run [Qwen Agentic RAG](https://ayush7614.github.io/agentic-ai-ecosystem/guides/qwen-agentic-rag/) API; call from either skill |

## Security posture

| Topic | Hermes Agent | OpenClaw |
|-------|--------------|----------|
| Untrusted skills | Treat ecosystem skills as untrusted; review `SKILL.md` + scripts | Docs: treat third-party skills as untrusted code |
| Network exposure | Keep gateway local; use pairing until trusted | Local-first gateway; caution on remote exposure |
| Sandboxing | Docker image, remote terminal backends | **Docker sandbox strongly recommended** |
| Audit | `hermes doctor` | `openclaw doctor`, `openclaw skills verify` |

## When to choose (summary)

| Scenario | Recommendation |
|----------|----------------|
| Personal assistant on phone chat apps, Node shop | **OpenClaw** |
| Agent research, skill evolution, Nous stack | **Hermes** |
| Local Gemma + RAG on Telegram | **OpenClaw** ([guide](https://ayush7614.github.io/agentic-ai-ecosystem/guides/openclaw-gemma-rag/)) |
| Leaving OpenClaw, keep channels | **Hermes** + `hermes claw migrate` |
| Maximum skills marketplace (2026) | **OpenClaw** (ClawHub) + **Hermes** (awesome-hermes-agent) — pick primary runtime, borrow skills from the other |
