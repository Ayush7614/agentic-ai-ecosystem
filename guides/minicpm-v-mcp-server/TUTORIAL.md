# MiniCPM-V MCP Server — Full Tutorial

Give your coding agent **eyes.** Instead of uploading screenshots to a cloud
vision API, you run a small **MCP server** backed by **MiniCPM-V 4.6** on Ollama
and expose three tools — `describe_image`, `ocr_document`, `compare_images` — so
Cursor, Claude Desktop, and Hermes all see images the same way.

Format matches our [Stripe Projects MCP](../stripe-projects-mcp/TUTORIAL.md)
and [MCP Visual Guide](../mcp-visual-guide/TUTORIAL.md) guides: prose, runnable
Python, terminal screenshots, and animated diagrams.

---

## What you'll understand at the end

- Why **vision belongs in MCP** — reusable tools vs one-off `ollama run` commands
- How **MiniCPM-V 4.6** fits a 16 GB Mac (~1.6 GB model, text + image input)
- The three tools and when to use each
- Wiring the server into **Cursor** and **Claude Desktop**
- Running the **agent demo** offline (`OLLAMA_MOCK=1`) or live with Ollama

![Capability exchange — vision tools over MCP](./assets/diagram-capability-exchange.gif)

**Terminal demo:** [step-mcp-vision-demo.gif](./assets/step-mcp-vision-demo.gif)

---

## Introduction — agents without eyes

Your agent can grep code, run tests, and provision infra — but the moment someone
pastes a **screenshot**, a **receipt**, or a **Figma export**, the loop breaks unless
you bolt on a vision API. That means API keys, cloud latency, and pixels leaving your
machine.

MiniCPM-V 4.6 is built for the opposite: **1.3B parameters**, **~1.6 GB** on disk,
**256K context**, and native **text + image** input via Ollama. Wrap it in MCP and
every host discovers the same three vision tools at connect time.

---

## Part 1 — MiniCPM-V 4.6 on Ollama

From the [Ollama model page](https://ollama.com/library/minicpm-v4.6):

| Tag | Size | Context | Input |
|-----|------|---------|-------|
| `minicpm-v4.6:latest` | 1.6 GB | 256K | Text, Image |
| `minicpm-v4.6:1b` | 1.6 GB | 256K | Text, Image |

```bash
ollama pull minicpm-v4.6
ollama run minicpm-v4.6 "Describe this image" --image ./photo.jpg
```

This guide uses the same model through Ollama's **HTTP API** so the MCP server can
batch tool calls without spawning a CLI per request.

---

## Part 2 — Why MCP for vision

You could write a Python script that calls Ollama and paste output into chat. But
then Cursor, Claude Desktop, and Hermes each need their own glue.

MCP collapses that. You write **one server**; hosts discover tools at **capability
exchange**. Add a fourth tool later and every host sees it on reconnect — no
host-side changes.

| Role | Here |
|------|------|
| **Host** | Cursor / Claude Desktop / Hermes |
| **Client** | MCP client inside the host |
| **Server** | `minicpm-vision` — vision tools backed by Ollama |

---

## Part 3 — The vision backend

[`examples/vision_backend.py`](./examples/vision_backend.py) encodes images as
base64 and POSTs to `OLLAMA_HOST/api/chat`:

```python
payload = {
    "model": VISION_MODEL,  # minicpm-v4.6
    "messages": [{"role": "user", "content": prompt, "images": images_b64}],
    "stream": False,
}
```

Environment variables (see [`.env.example`](./.env.example)):

| Variable | Default | Purpose |
|----------|---------|---------|
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Ollama base URL |
| `OLLAMA_VISION_MODEL` | `minicpm-v4.6` | Vision model tag |
| `OLLAMA_MOCK` | `0` | Set `1` for offline demo without Ollama |

---

## Part 4 — The three tools

[`examples/server.py`](./examples/server.py) is a `FastMCP` server.

### `describe_image`

General-purpose image Q&A. Default prompt asks for objects, visible text, layout,
and developer-relevant details. Pass a custom `question` for targeted queries.

### `ocr_document`

Uses a structured OCR prompt — markdown headings, bullet lists, tables. Ideal for
receipts, invoices, and whiteboard photos.

### `compare_images`

Accepts two paths and an optional `focus` string (e.g. `"navigation bar"`). Returns
similarities, differences, and UI change notes.

Each tool returns **JSON** with `result`, `tool`, paths, and `model` — easy for the
host to parse and display.

---

## Part 5 — Agent demo

[`examples/agent_demo.py`](./examples/agent_demo.py) runs all three scenarios against
generated fixtures:

```bash
python examples/generate_fixtures.py   # receipt + two diagram PNGs
python examples/agent_demo.py
```

Output mirrors what you see when an agent chains tools:

```
[Tool: describe_image]  path=fixtures/diagram_v2.png
[Tool: ocr_document]    path=fixtures/sample_receipt.png
[Tool: compare_images]  v1 → v2 pipeline diagrams
```

Offline smoke test:

```bash
OLLAMA_MOCK=1 python examples/agent_demo.py
```

---

## Part 6 — Wire into Cursor

Copy [`examples/cursor_mcp.json.example`](./examples/cursor_mcp.json.example) into
Cursor → Settings → MCP. Use **absolute paths** for `cwd`.

Restart Cursor, open MCP tool list — you should see `describe_image`, `ocr_document`,
`compare_images`.

Try: *"Use ocr_document on /path/to/receipt.png and summarize the total."*

---

## Part 7 — Wire into Claude Desktop

Add the server block from
[`examples/claude_desktop_config.json.example`](./examples/claude_desktop_config.json.example)
to `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS.

Restart Claude Desktop. Vision tools appear alongside your other MCP servers.

---

## Part 8 — Sample fixtures

[`examples/generate_fixtures.py`](./examples/generate_fixtures.py) creates:

| File | Purpose |
|------|---------|
| `sample_receipt.png` | OCR demo — coffee shop receipt |
| `diagram_v1.png` | Compare demo — simple API → Qdrant |
| `diagram_v2.png` | Compare demo — adds CrewAI + LitServe |

No external downloads required — the guide is self-contained.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Cannot reach Ollama` | Start Ollama app; verify `curl http://127.0.0.1:11434/api/tags` |
| `model not found` | `ollama pull minicpm-v4.6` |
| Slow first call | Normal — model loads into RAM; subsequent calls faster |
| MCP host shows no tools | Check absolute `cwd` in config; restart host |

---

## Next steps

- **[OpenClaw + MiniCPM-V](../openclaw-minicpm-v/)** — send photos on Telegram/WhatsApp
- **[MiniCPM-V Benchmark](../minicpm-v-benchmark/)** — compare vs Qwen3.5-0.8B and Gemma4-E2B
- **[Qwen Agentic RAG](../qwen-agentic-rag/)** — text RAG crew; pair with this guide for multimodal agents

---

## License

Guide: MIT · MiniCPM-V: Apache-2.0
