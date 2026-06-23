# MiniCPM-V MCP Server — Give Your Agent Eyes

Build an **MCP server** that exposes `describe_image`, `ocr_document`, and
`compare_images` so **any** MCP host — Cursor, Claude Desktop, Hermes — can
understand screenshots, receipts, and UI diffs through **one protocol**.

Powered by **[MiniCPM-V 4.6](https://ollama.com/library/minicpm-v4.6)** via Ollama:
**1.3B params · 1.6 GB · text + image · 256K context** — the smallest vision model
in the MiniCPM family, tuned for edge and phone deployment.

**The moment:** paste a screenshot into Cursor and ask *"What changed in this UI?"*
The agent calls `compare_images` — no cloud vision API, no API key.

## What you'll learn

- **Vision as MCP tools** — why `describe_image / ocr_document / compare_images` beat one-off scripts
- **One protocol, many hosts** — same server in Cursor, Claude Desktop, and Hermes
- **MiniCPM-V 4.6 on Ollama** — pull, run, and wire the 1.6 GB multimodal model locally
- **Private document OCR** — extract receipt and whiteboard text without sending pixels to the cloud
- **Before/after UI diffs** — compare two screenshots for regression review
- Runnable **Python MCP server** + an end-to-end **agent demo** (works offline with `OLLAMA_MOCK=1`)

![Capability exchange — vision tools over MCP](./assets/diagram-capability-exchange.gif)

![Agent demo terminal — describe_image, ocr_document, compare_images](./assets/step-mcp-vision-demo.gif)

## Quick start

```bash
cd guides/minicpm-v-mcp-server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Pull the vision model (~1.6 GB)
ollama pull minicpm-v4.6

# Generate sample images + run the agent demo
python examples/generate_fixtures.py
python examples/agent_demo.py

# Run the MCP server for Cursor / Claude Desktop
python examples/server.py
# Add examples/cursor_mcp.json.example → Cursor → MCP settings
```

In your host, ask: **"OCR this receipt and tell me the total."** The agent calls
`ocr_document`, MiniCPM-V reads the image locally, and structured text comes back.

## Guide map

- **[Full tutorial](./TUTORIAL.md)** — architecture, the three tools, Ollama wiring, host configs
- **[Examples](./examples/)** — MCP server, vision backend, fixtures, agent demo, host configs
- **[Assets](./assets/)** — capability-exchange diagram + terminal demo GIFs

## The three tools

| MCP tool | What it does | Typical use |
|----------|--------------|-------------|
| `describe_image(path, question?)` | General image Q&A | Screenshot explanation, diagram reading |
| `ocr_document(path)` | Text → markdown | Receipts, invoices, whiteboards |
| `compare_images(path_a, path_b, focus?)` | Visual diff | UI regression, before/after review |

## Hardware notes (16 GB Mac)

- **MiniCPM-V 4.6** uses ~1.6 GB disk and ~2–4 GB RAM at inference — comfortable on 16 GB machines
- First vision call may take 10–30 s while the model loads; later calls are faster
- For text-only chat, keep using [Qwen Agentic RAG](../qwen-agentic-rag/) — this guide adds **eyes**, not a replacement

## Related guides

- [MCP Visual Guide](../mcp-visual-guide/) — host/client/server, capability exchange
- [Stripe Projects MCP](../stripe-projects-mcp/) — same MCP pattern for infra provisioning
- [OpenClaw + MiniCPM-V](../openclaw-minicpm-v/) — photo assistant on Telegram/WhatsApp
- [MiniCPM-V Benchmark](../minicpm-v-benchmark/) — vs Qwen3.5-0.8B and Gemma4-E2B on 16 GB Mac

## License

Guide: MIT · MiniCPM-V weights: Apache-2.0
