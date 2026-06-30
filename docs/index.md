---
template: home.html
title: Agentic AI Ecosystem
hide:
  - navigation
  - toc
---

# Agentic AI Ecosystem

Hands-on guides for building **local, private agentic AI** systems — RAG, multi-agent crews, MCP tooling, and production-style APIs.

Maintained by [Ayush Kumar](https://github.com/Ayush7614) · [NeuralVerse](https://neural-verse-peach.vercel.app/) · [Portfolio](https://ayushbuilds-dev.vercel.app/)

## Guides

| Guide | What you'll build |
|-------|-------------------|
| [Qwen Agentic RAG](guides/qwen-agentic-rag/index.md) | Private two-agent RAG API with Qwen (Ollama), CrewAI, Qdrant, Firecrawl, LitServe, and Gradio |
| [OpenClaw + Gemma + RAG](guides/openclaw-gemma-rag/index.md) | Messaging assistant on `gemma4:e2b` with a local RAG skill calling the LitServe API |
| [OpenClaw + MiniCPM-V](guides/openclaw-minicpm-v/index.md) | Photo assistant on Telegram/WhatsApp with MiniCPM-V 4.6 vision LitServe API |
| [Claude Code `.claude/`](guides/claude-code-dot-claude/index.md) | Team-aware Claude Code layout — `CLAUDE.md`, permissions, rules, skills, and subagents |
| [Awesome Hermes Agent](guides/awesome-hermes-agent/index.md) | Install Hermes Agent and map the skills, plugins, GUIs, and integrations ecosystem |
| [Hermes vs OpenClaw](guides/hermes-vs-openclaw/index.md) | Compare Hermes Agent and OpenClaw — gateways, skills, migration, decision guide |
| [MCP Visual Guide](guides/mcp-visual-guide/index.md) | Model Context Protocol — host/client/server, capability exchange, API vs MCP, App MCP |
| [ML Model in 6 Steps](guides/ml-model-6-steps/index.md) | Visual ML pipeline — problem framing through deploy and monitor with animated GIFs |
| [Solo Engineer Stack](guides/solo-engineer-stack/index.md) | Build PulseFeedback with 10 equal tools — PM to support in one closed loop |
| [Loop Engineering](guides/loop-engineering/index.md) | Act, observe, repeat — eval gates, open vs closed loops, fleet patterns, ReAct |
| [Harness Engineering](guides/harness-engineering/index.md) | Agent = Model + Harness — five subsystems, session lifecycle, verification gates |
| [LLM Fine-Tuning](guides/llm-fine-tuning/index.md) | LoRA, QLoRA, RLHF, DPO, GRPO — when to fine-tune, PEFT math, HuggingFace walkthroughs |
| [AI Agents Masterclass](guides/ai-agents-masterclass/index.md) | **Visual masterclass** — agent anatomy, ReAct/ReWOO, 15+ frameworks, use cases, MCP/A2A, five code examples |
| [Hermes Agent Masterclass](guides/hermes-agent-masterclass/index.md) | **Complete Hermes guide** — learning loop, Profile Builder, memory, Curator, GEPA, three agents |
| [Hermes Profile Builder](guides/hermes-profile-builder/index.md) | Quick index — full Profile Builder walkthrough in Masterclass Parts 11–12 |
| [OpenClaw](guides/openclaw/index.md) | Install and extend the personal AI assistant from openclaw.ai — gateway, channels, skills |
| [Anthropic Cybersecurity Skills](guides/anthropic-cybersecurity-skills/index.md) | 754 MITRE-mapped security skills for AI agents — install, frameworks, SOC walkthroughs |
| [MiniCPM-V MCP Server](guides/minicpm-v-mcp-server/index.md) | Vision MCP server with MiniCPM-V 4.6 — describe_image, ocr_document, compare_images on Ollama |
| [MiniCPM-V Benchmark](guides/minicpm-v-benchmark/index.md) | Compare MiniCPM-V 4.6 vs Qwen3.5-0.8B vs Gemma4-E2B on 16 GB Mac |
| [OpenCode Agent Masterclass](guides/opencode-agent-masterclass/index.md) | **Visual masterclass** — Build vs Plan agents, AGENTS.md, MCP, LSP, 75+ providers |
| [ZeroClaw Agent Masterclass](guides/zeroclaw-agent-masterclass/index.md) | **Visual masterclass** — Rust runtime, config.toml, 30+ channels, security policy, SOP |
| [OpenClaude Agent Masterclass](guides/openclaude-agent-masterclass/index.md) | **Visual masterclass** — GitLawb CLI, 69+ slash commands, /provider, MCP, agent routing |
| [PicoClaw Agent Masterclass](guides/picoclaw-agent-masterclass/index.md) | **Visual masterclass** — Go edge agent, <10MB RAM, WebUI launcher, 19+ channels, MCP |

Each guide is a self-contained project under `guides/<name>/` in the repo. The site pages mirror those READMEs and tutorials so you can read online without cloning.

## Run locally (any guide)

```bash
git clone https://github.com/Ayush7614/agentic-ai-ecosystem.git
cd agentic-ai-ecosystem/guides/<guide-name>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Follow the guide README on GitHub or the tutorial page here
```

## Add a new guide

1. Create `guides/<your-guide-name>/` with `README.md`, `requirements.txt`, and `.env.example`.
2. Add docs pages under `docs/guides/<your-guide-name>/` (see [Publishing](publishing.md)).
3. Add a row to the table above and an entry in `mkdocs.yml` → `nav`.

## License

MIT — see [LICENSE](https://github.com/Ayush7614/agentic-ai-ecosystem/blob/main/LICENSE).
