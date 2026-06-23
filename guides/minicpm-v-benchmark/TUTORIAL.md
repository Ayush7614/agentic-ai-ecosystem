# MiniCPM-V Benchmark — Full Tutorial

Reproducibly compare **MiniCPM-V 4.6**, **Qwen3.5-0.8B**, and **Gemma4-E2B** on your
**16 GB Mac** using local Ollama — the same stack as our agentic guides.

---

## What you'll understand

- What **TTFT** (time to first token) and **tokens/sec** mean for agent UX
- Why **disk size ≠ RAM** at inference time
- When MiniCPM-V's **1.6 GB vision** beats Gemma's **~7 GB** — and when it doesn't
- How to re-run [`scripts/benchmark.py`](./scripts/benchmark.py) after model updates

![Benchmark run](./assets/step-benchmark-run.gif)

---

## Part 1 — Models under test

| Ollama tag | Role in ecosystem |
|------------|-------------------|
| `minicpm-v4.6` | Vision MCP + OpenClaw photos ([guides](../minicpm-v-mcp-server/)) |
| `qwen3.5:0.8b` | Qwen Agentic RAG crew ([guide](../qwen-agentic-rag/)) |
| `gemma4:e2b` | OpenClaw + RAG ([guide](../openclaw-gemma-rag/)) |

```bash
ollama pull minicpm-v4.6
ollama pull qwen3.5:0.8b
ollama pull gemma4:e2b
```

---

## Part 2 — Methodology

### Text benchmark

- **Prompt:** fixed cross-validation explainer (3 sentences)
- **Streaming:** Ollama `/api/chat` with `stream: true`
- **TTFT:** time until first content chunk
- **Throughput:** `eval_count / total_seconds`

### Vision benchmark

- **Image:** `samples/benchmark_card.png` (generated locally)
- **Prompt:** read visible text and list model names
- **Latency:** total non-streaming request time
- **Skipped** for text-only models (Qwen3.5-0.8B)

---

## Part 3 — Run the benchmark

```bash
cd guides/minicpm-v-benchmark
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate_sample.py
python scripts/benchmark.py
```

Outputs:

- `results/benchmark.json` — raw numbers
- `results/report.md` — markdown table + text previews

Options:

```bash
python scripts/benchmark.py --models minicpm-v4.6,qwen3.5:0.8b
SKIP_PULL=0 python scripts/benchmark.py   # auto-pull missing models
```

---

## Part 4 — Reading the results

![Comparison table](./assets/benchmark-comparison.gif)

### MiniCPM-V 4.6

- **Smallest model with vision** in this shootout (~1.6 GB)
- Adds OCR / screenshot understanding without Gemma-scale RAM
- Official claims ~1.5× throughput vs Qwen3.5-0.8B on vision workloads — verify on your hardware

### Qwen3.5-0.8B

- Best when you need **text-only** agentic RAG and minimum footprint
- No vision benchmark row — use MiniCPM-V for images

### Gemma4-E2B

- Strongest **general chat** of the three in most qualitative checks
- ~7 GB — comfortable on 16 GB Mac if you close other apps; tight alongside Qdrant + browsers

---

## Part 5 — Pick a stack

| Your goal | Model | Guide |
|-----------|-------|-------|
| Vision in Cursor (MCP) | minicpm-v4.6 | [MCP server](../minicpm-v-mcp-server/) |
| Photos on Telegram | minicpm-v4.6 | [OpenClaw + MiniCPM-V](../openclaw-minicpm-v/) |
| Text RAG crew | qwen3.5:0.8b or gemma4:e2b | [Qwen RAG](../qwen-agentic-rag/) |
| Best chat quality + vision | gemma4:e2b | [OpenClaw + Gemma](../openclaw-gemma-rag/) |

**Hybrid pattern:** Qwen or Gemma for text agents + MiniCPM-V MCP server for screenshots — only ~1.6 GB extra when vision tools run.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Model not installed | `ollama pull <tag>` or `SKIP_PULL=0` |
| Wildly different second run | First run warms cache; compare run 2 vs run 2 |
| Vision error on Qwen | Expected — text-only model |

---

## License

Guide: MIT · Model weights: respective licenses
