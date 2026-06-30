# PicoClaw Agent Masterclass

The **complete PicoClaw guide** — WebUI launcher, `config.json`, 30+ providers, 19+ channels, MCP, skills, cron, and edge deployment.

**Official:** [docs.picoclaw.io](https://docs.picoclaw.io/) · **Website:** [picoclaw.io](https://picoclaw.io/) · **Source:** [github.com/sipeed/picoclaw](https://github.com/sipeed/picoclaw)

> Ultra-efficient AI assistant in **Go** — <10MB RAM, <1s boot, runs on **$10 hardware** (RISC-V, ARM, x86). Not a fork of OpenClaw.

## What you'll build

- PicoClaw via **picoclaw-launcher** WebUI at `http://localhost:18800`
- Provider + channel (Telegram) + **gateway** running
- CLI path: `picoclaw onboard` → `config.json` + `.security.yml`
- **MCP** server, **ClawHub skills**, web search, and **cron** reminders
- Understanding of workspace harness files (`AGENTS.md`, `SOUL.md`, `HEARTBEAT.md`)

![PicoClaw stack — launcher to gateway](./assets/diagram-picoclaw-stack.gif)

**One-GIF overview (blog hero):** [mega-picoclaw-everything.gif](assets/mega-picoclaw-everything.gif) — download → WebUI → provider → channel → chat in ~12s.

## Quick start

```bash
# Download from picoclaw.io (auto-detects platform) or:
wget https://github.com/sipeed/picoclaw/releases/latest/download/picoclaw_Linux_x86_64.tar.gz
picoclaw-launcher
# Open http://localhost:18800 → Provider → Channel → Start Gateway
```

## Guide map

- **[Full tutorial](./TUTORIAL.md)** — Parts 1–18 (edge hardware → MCP → OpenClaw comparison)
- **[Examples](./examples/)** — `config.minimal.json`, Telegram channel, MCP block
- **[Assets](./assets/)** — diagram + terminal GIFs, blog poster

## Related guides

- [OpenClaw](../openclaw/) · [ZeroClaw Agent Masterclass](../zeroclaw-agent-masterclass/)
- [OpenCode Agent Masterclass](../opencode-agent-masterclass/) · [MCP Visual Guide](../mcp-visual-guide/)
- [Harness Engineering](../harness-engineering/)

**Blog header:** `assets/blog-poster-1200x600.png` · Regenerate: `cd assets && python3 render_gifs.py all && python3 render_blog_poster.py`

## License

Guide: MIT · PicoClaw: upstream MIT · Community tutorial — not affiliated with Sipeed.
