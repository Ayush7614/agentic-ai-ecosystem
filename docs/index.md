# Agentic AI Ecosystem

Hands-on guides for building **local, private agentic AI** systems — RAG, multi-agent crews, MCP tooling, and production-style APIs.

Maintained by [Ayush Kumar](https://github.com/Ayush7614) · [NeuralVerse](https://neural-verse-peach.vercel.app/) · [Portfolio](https://ayushbuilds-dev.vercel.app/)

## Guides

| Guide | What you'll build |
|-------|-------------------|
| [Qwen Agentic RAG](guides/qwen-agentic-rag/index.md) | Private two-agent RAG API with Qwen (Ollama), CrewAI, Qdrant, Firecrawl, LitServe, and Gradio |
| [OpenClaw + Gemma + RAG](guides/openclaw-gemma-rag/index.md) | Messaging assistant on `gemma4:e2b` with a local RAG skill calling the LitServe API |
| [Claude Code `.claude/`](guides/claude-code-dot-claude/index.md) | Team-aware Claude Code layout — `CLAUDE.md`, permissions, rules, skills, and subagents |
| [Awesome Hermes Agent](guides/awesome-hermes-agent/index.md) | Install Hermes Agent and map the skills, plugins, GUIs, and integrations ecosystem |
| [Hermes vs OpenClaw](guides/hermes-vs-openclaw/index.md) | Compare Hermes Agent and OpenClaw — gateways, skills, migration, decision guide |

| [MCP Visual Guide](guides/mcp-visual-guide/index.md) | Model Context Protocol — host/client/server, capability exchange, API vs MCP, App MCP |

| [Anthropic Cybersecurity Skills](guides/anthropic-cybersecurity-skills/index.md) | 754 MITRE-mapped security skills for AI agents — install, frameworks, SOC walkthroughs |

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
