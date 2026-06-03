---
name: agentic-rag
description: Query the local Agentic RAG API (CrewAI + Qdrant + optional Firecrawl) for ML FAQ and research-heavy answers.
user-invocable: true
metadata:
  {"openclaw":{"emoji":"📚","requires":{"bins":["curl","jq"],"env":["RAG_API_URL"]},"primaryEnv":"RAG_API_URL"}}
---

# Agentic RAG (local LitServe API)

Use this skill when the user asks about **machine learning concepts**, **FAQ-style knowledge** stored in the vector DB, or wants a **researched answer** that should combine local retrieval with optional web search (if Firecrawl is configured on the RAG server).

Do **not** use this skill for casual chat, scheduling, or channel meta — answer those directly.

## When to invoke

- ML / data-science questions (cross-validation, overfitting, embeddings, etc.)
- User explicitly asks to "search the knowledge base", "use RAG", or "ask the research crew"
- Questions that need grounded answers from the project's Qdrant FAQ collection

## How to invoke

1. Confirm the RAG API is reachable (optional quick check):

```bash
curl -sS -o /dev/null -w "%{http_code}" "${RAG_API_URL:-http://127.0.0.1:8001}/predict" -X POST -H 'Content-Type: application/json' -d '{"query":"ping"}' || true
```

A `200` or `422` means the server is up; connection errors mean the user must start `python server.py` in `guides/qwen-agentic-rag`.

2. Run the bundled script with the **full user question** as one argument:

```bash
"{baseDir}/scripts/rag_query.sh" "USER_QUESTION_HERE"
```

3. Return the script output to the user. If the script errors, explain that the RAG stack may be offline and list: Ollama, Qdrant, `setup_vectordb.py`, and `server.py`.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `RAG_API_URL` | `http://127.0.0.1:8001` | LitServe base URL (no trailing slash) |

Set in `~/.openclaw/openclaw.json` under `skills.entries.agentic-rag.env` or export before starting the gateway.

## Notes for the agent

- RAG calls can take **1–10+ minutes** on a laptop (CrewAI + local LLM). Do not retry aggressively.
- After RAG returns, you may **shorten or reformat** the answer for the channel (Telegram/WhatsApp) but preserve factual content.
- OpenClaw chat and the RAG crew both use `gemma4:e2b` via `guides/qwen-agentic-rag/.env` (`env.rag.example`).
