# OpenClaw + Gemma 4 E2B + Agentic RAG — Full Integration

Build a **personal AI assistant** that answers on Telegram/WhatsApp/CLI using **Gemma 4 E2B**, and delegates research-heavy questions to your **local Agentic RAG API**.

## What you end up with

1. **OpenClaw Gateway** — always-on control plane (daemon)
2. **gemma4:e2b** — conversational model with tools + optional vision
3. **agentic-rag skill** — shells out to `rag_query.sh` → `POST /predict` on LitServe
4. **qwen-agentic-rag** — CrewAI Researcher + Writer + Qdrant (and optional Firecrawl)

This integration uses **one Ollama model everywhere**: `gemma4:e2b` for OpenClaw chat and for the CrewAI RAG agents.

---

## Prerequisites

| Requirement | Check |
|-------------|--------|
| Node **22.12+** or **24** (OpenClaw will not run on Node 20) | `node -v` |
| Ollama | `ollama -v` |
| Python 3.10+ | `python3 --version` |
| curl + jq | `curl --version` && `jq --version` |
| Completed [qwen-agentic-rag](https://ayush7614.github.io/agentic-ai-ecosystem/guides/qwen-agentic-rag/) once | vector DB built |

---

## Part 1 — Agentic RAG API

If you already finished the [Qwen Agentic RAG tutorial](https://ayush7614.github.io/agentic-ai-ecosystem/guides/qwen-agentic-rag/tutorial/), start the server only:

```bash
ollama pull gemma4:e2b
cd guides/qwen-agentic-rag
source .venv/bin/activate
cp ../openclaw-gemma-rag/env.rag.example .env   # sets OLLAMA_MODEL=ollama/gemma4:e2b
# First time only:
# pip install -r requirements.txt && python setup_vectordb.py
python server.py
```

Default URL: **http://127.0.0.1:8001** (`PORT` in `.env`).

Verify:

```bash
python client.py --query "What is cross-validation?"
# or
curl -sS -X POST http://127.0.0.1:8001/predict \
  -H 'Content-Type: application/json' \
  -d '{"query":"What is cross-validation?"}' | jq -r .output
```

Keep this terminal open. First crew run may take several minutes.

---

## Part 2 — Pull Gemma 4 E2B

```bash
ollama pull gemma4:e2b
ollama run gemma4:e2b "Reply in one sentence: what is Gemma 4?"
```

Recommended sampling (Ollama may already apply defaults): `temperature=1`, `top_p=0.95`, `top_k=64`.

---

## Part 3 — Install OpenClaw

### Node version (required)

OpenClaw needs **Node >= 22.12**. If `node -v` shows v20, switch with nvm (you may already have 22 installed):

```bash
cd guides/openclaw-gemma-rag
source ./use-node22.sh   # uses .nvmrc → 22.22.3
node -v                # must be v22.12.0 or higher
```

Optional — make Node 22 the default in new terminals:

```bash
nvm alias default 22
```

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Follow prompts for workspace, auth, and optional channels. See [Getting started](https://docs.openclaw.ai/).

Set the primary model:

```bash
export OLLAMA_API_KEY="ollama-local"
openclaw models list --provider ollama
openclaw models set ollama/gemma4:e2b
```

### Config snippet

Copy fields from `config/openclaw.snippet.json5` in this guide into `~/.openclaw/openclaw.json`.

Critical points:

- `baseUrl`: `http://127.0.0.1:11434` — **no** `/v1` suffix
- `api`: `"ollama"` — native tool calling
- `agents.defaults.model.primary`: `"ollama/gemma4:e2b"`

Restart:

```bash
openclaw gateway restart
openclaw gateway status
```

---

## Part 4 — Install the agentic-rag skill

From this guide directory:

```bash
cd guides/openclaw-gemma-rag
chmod +x install-skill.sh skills/agentic-rag/scripts/*.sh
./install-skill.sh
```

This copies to `~/.openclaw/workspace/skills/agentic-rag/`.

Alternative (if your CLI supports it):

```bash
openclaw skills install ./guides/openclaw-gemma-rag/skills/agentic-rag --global
```

Enable in config:

```json5
{
  skills: {
    entries: {
      "agentic-rag": {
        enabled: true,
        env: { RAG_API_URL: "http://127.0.0.1:8001" },
      },
    },
  },
}
```

Optional allowlist so only this skill is injected:

```json5
{
  agents: {
    defaults: {
      skills: ["agentic-rag"],
    },
  },
}
```

Restart the gateway after skill or config changes.

### Skill behavior

The skill teaches OpenClaw to run:

```bash
~/.openclaw/workspace/skills/agentic-rag/scripts/rag_query.sh "user question"
```

That POSTs to LitServe and prints the crew answer. The **Gemma** model decides *when* to use the skill; the **RAG crew** uses the same `OLLAMA_MODEL=ollama/gemma4:e2b` from `guides/qwen-agentic-rag/.env` (see `env.rag.example`).

---

## Part 5 — End-to-end test

### CLI (no channel)

```bash
openclaw agent --message "Using the agentic RAG knowledge base: explain cross-validation in 3 bullets." --thinking low
```

Watch the gateway logs — you should see an `exec` invoking `rag_query.sh`.

### Manual script test

```bash
export RAG_API_URL=http://127.0.0.1:8001
./skills/agentic-rag/scripts/rag_query.sh "What is regularization?"
```

### Health check

```bash
./skills/agentic-rag/scripts/rag_health.sh
```

---

## Part 6 — Connect a channel (optional)

Example: **Telegram**

1. Create a bot via [@BotFather](https://t.me/BotFather)
2. During `openclaw onboard` or `openclaw configure`, add the Telegram channel token
3. Keep **DM pairing** enabled (`dmPolicy: "pairing"`) until you trust exposure
4. Approve yourself: `openclaw pairing approve telegram <code>`

Send: *"Search the ML FAQ: what is gradient descent?"*

Flow: Telegram → Gateway → Gemma → `agentic-rag` skill → RAG API → reply on Telegram.

Channel docs: [OpenClaw Channels](https://docs.openclaw.ai/).

---

## Security checklist

- Treat inbound DMs as **untrusted** — keep pairing on for production-adjacent setups
- `exec` (used by the RAG skill) is powerful — do not expose the gateway to the public internet without [Security](https://docs.openclaw.ai/security) and [Exposure runbook](https://docs.openclaw.ai/)
- Run `openclaw doctor` after config changes
- RAG API binds to localhost by default — keep it that way

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `connection refused` on :8001 | Start `python server.py` in qwen-agentic-rag |
| RAG very slow | Normal on laptop; reduce parallel Ollama loads |
| OpenClaw ignores RAG | Confirm skill installed, `enabled: true`, gateway restarted; ask explicitly to "use agentic RAG" |
| `ollama/gemma4:e2b` not found | `ollama pull gemma4:e2b`; check `openclaw models list` |
| Tool calling errors | Ensure `api: "ollama"` and no `/v1` on baseUrl |
| `openclaw requires Node >=22.12.0` | Run `source guides/openclaw-gemma-rag/use-node22.sh` or `nvm use 22` before any `openclaw` command |
| OOM on 16GB Mac | Only run `gemma4:e2b`; quit other Ollama models (`ollama ps`) |
| Skill `curl` fails | `brew install jq` or apt install jq |

---

## What's next

- Add your own documents in `guides/qwen-agentic-rag/rag_code.py` and re-run `setup_vectordb.py`
- Publish a second OpenClaw skill for Gradio (`ui.py`) health checks
- Route work vs personal agents with [multi-agent routing](https://docs.openclaw.ai/)
- Share this guide on the [ecosystem docs site](https://ayush7614.github.io/agentic-ai-ecosystem/)

---

## Summary

| Component | You run |
|-----------|---------|
| Ollama | `gemma4:e2b` (chat + RAG) |
| RAG | `guides/qwen-agentic-rag/server.py` |
| OpenClaw | `openclaw gateway` (daemon) |
| Skill | `agentic-rag` → `rag_query.sh` → `/predict` |

You now have a **local-first assistant**: Gemma for conversation, CrewAI RAG for grounded ML research — no cloud LLM required for either layer.
