# MiniCPM-V vs Qwen3.5-0.8B vs Gemma4-E2B — 16 GB Mac Benchmark

Compare **edge models** on a typical **16 GB Mac**: disk size, text **TTFT**, **tokens/sec**, and **vision latency** — with **MiniCPM-V 4.6** as the pocket-sized vision baseline.

Part of the [Agentic AI Ecosystem](https://github.com/Ayush7614/agentic-ai-ecosystem).

## What you'll learn

- How **MiniCPM-V 4.6** (1.6 GB) compares to **Qwen3.5-0.8B** (text) and **Gemma4-E2B** (~7 GB) on the same machine
- Measuring **TTFT** and **throughput** with Ollama's streaming API
- When to pick **vision** vs **text-only** vs **larger edge** models for agentic stacks
- Reproducible benchmark script you can re-run after Ollama updates

![Benchmark terminal demo](./assets/step-benchmark-run.gif)

**Results table GIF:** [benchmark-comparison.gif](./assets/benchmark-comparison.gif)

## Quick start

```bash
cd guides/minicpm-v-benchmark
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Pull models you want to compare
ollama pull minicpm-v4.6
ollama pull qwen3.5:0.8b      # optional — text-only baseline
ollama pull gemma4:e2b      # optional — larger vision model

python generate_sample.py
python scripts/benchmark.py

cat results/report.md
```

## Models compared

| Model | Params | Ollama size | Vision | Best for |
|-------|--------|-------------|--------|----------|
| **minicpm-v4.6** | 1.3B | ~1.6 GB | ✅ | Photos, OCR, UI screenshots on 16 GB Mac |
| **qwen3.5:0.8b** | 0.8B | ~0.5 GB | ❌ | Fastest text-only RAG / agents |
| **gemma4:e2b** | ~2B effective | ~7 GB | ✅ | Stronger chat + vision when RAM allows |

## Sample results (16 GB Mac, local Ollama)

See [results/report.md](./results/report.md) for the latest run. Typical patterns:

- **MiniCPM-V 4.6** — smallest **vision** model; adds eyes without Gemma's ~7 GB footprint
- **Qwen3.5-0.8B** — fastest **text** TTFT; pair with [Qwen Agentic RAG](../qwen-agentic-rag/) for pure text crews
- **Gemma4-E2B** — highest quality of the three for chat; use when you have RAM headroom ([OpenClaw + Gemma](../openclaw-gemma-rag/))

## Project layout

| Path | Purpose |
|------|---------|
| `scripts/benchmark.py` | TTFT, tok/s, vision latency per model |
| `generate_sample.py` | Benchmark card PNG for vision tests |
| `results/benchmark.json` | Machine-readable scores |
| `results/report.md` | Markdown summary table |
| `TUTORIAL.md` | Methodology, interpretation, hardware notes |

## Hardware notes (16 GB Mac)

- Run benchmarks with **other heavy apps closed** for stable numbers
- Ollama loads one model at a time by default — benchmark script runs sequentially
- First run after pull includes download time; re-run for steady-state TTFT

## Related guides

| Guide | Use case |
|-------|----------|
| [MiniCPM-V MCP Server](../minicpm-v-mcp-server/) | Vision tools in Cursor |
| [OpenClaw + MiniCPM-V](../openclaw-minicpm-v/) | Photo assistant on messaging |
| [Qwen Agentic RAG](../qwen-agentic-rag/) | Text-only agentic RAG |

## Full tutorial

See [TUTORIAL.md](./TUTORIAL.md).
