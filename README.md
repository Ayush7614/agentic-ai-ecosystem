# Agentic AI Ecosystem

Hands-on guides for building **local, private agentic AI** systems — RAG, multi-agent crews, MCP tooling, and production-style APIs.

Maintained by [Ayush Kumar](https://github.com/Ayush7614) · [NeuralVerse](https://neural-verse-peach.vercel.app/) · [Portfolio](https://ayushbuilds-dev.vercel.app/)

**Read the guides online:** [ayush7614.github.io/agentic-ai-ecosystem](https://ayush7614.github.io/agentic-ai-ecosystem/)

## Guides

| Guide | Stack | Description |
|-------|--------|-------------|
| [qwen-agentic-rag](./guides/qwen-agentic-rag/) · [blog](https://ayush7614.github.io/agentic-ai-ecosystem/guides/qwen-agentic-rag/) | Qwen (Ollama) · CrewAI · Qdrant · Firecrawl · LitServe · Gradio | Private two-agent RAG API with vector DB + optional web search |
| [openclaw-gemma-rag](./guides/openclaw-gemma-rag/) · [blog](https://ayush7614.github.io/agentic-ai-ecosystem/guides/openclaw-gemma-rag/) | OpenClaw · Gemma 4 E2B · RAG skill | Personal assistant on chat apps backed by local Agentic RAG |
| [claude-code-dot-claude](./guides/claude-code-dot-claude/) · [blog](https://ayush7614.github.io/agentic-ai-ecosystem/guides/claude-code-dot-claude/) | Claude Code · `.claude/` | Anatomy of the `.claude/` folder — skills, rules, agents, permissions |
| [awesome-hermes-agent](./guides/awesome-hermes-agent/) · [blog](https://ayush7614.github.io/agentic-ai-ecosystem/guides/awesome-hermes-agent/) | Hermes Agent · ecosystem | Install Hermes + awesome-hermes-agent skills, tools, and level-up blueprints |
| [hermes-vs-openclaw](./guides/hermes-vs-openclaw/) · [blog](https://ayush7614.github.io/agentic-ai-ecosystem/guides/hermes-vs-openclaw/) | Hermes · OpenClaw | Side-by-side comparison — architecture, skills, migration, when to pick which |
| [minicpm-v-mcp-server](./guides/minicpm-v-mcp-server/) · [blog](https://ayush7614.github.io/agentic-ai-ecosystem/guides/minicpm-v-mcp-server/) | MiniCPM-V 4.6 · Ollama · MCP | Vision MCP tools — describe_image, ocr_document, compare_images for Cursor and Claude Desktop |

## Quick start (any guide)

```bash
git clone https://github.com/Ayush7614/agentic-ai-ecosystem.git
cd agentic-ai-ecosystem/guides/<guide-name>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Follow the guide README
```

## Adding a new guide

1. Create `guides/<your-guide-name>/` with its own `README.md`, `requirements.txt`, and `.env.example`.
2. Add MkDocs pages under `docs/guides/<your-guide-name>/` and an entry in `mkdocs.yml` (see [docs/publishing.md](./docs/publishing.md)).
3. Add a row to the table above.
4. Push to `main` — GitHub Actions publishes the site automatically.

## License

MIT — see [LICENSE](./LICENSE).
