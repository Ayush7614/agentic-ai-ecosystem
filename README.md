# Agentic AI Ecosystem

Hands-on guides for building **local, private agentic AI** systems — RAG, multi-agent crews, MCP tooling, and production-style APIs.

Maintained by [Ayush Kumar](https://github.com/Ayush7614) · [NeuralVerse](https://neural-verse-peach.vercel.app/) · [Portfolio](https://ayushbuilds-dev.vercel.app/)

## Guides

| Guide | Stack | Description |
|-------|--------|-------------|
| [qwen-agentic-rag](./guides/qwen-agentic-rag/) | Qwen (Ollama) · CrewAI · Qdrant · Firecrawl · LitServe · Gradio | Private two-agent RAG API with vector DB + optional web search |

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
2. Add a row to the table above.
3. Open a PR or push to `main`.

## License

MIT — see [LICENSE](./LICENSE).
