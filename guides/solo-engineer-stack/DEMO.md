# Live demo script — blog / video walkthrough

Run this **before** recording or presenting. Everything is real — UI, API, artifacts, CSAT loop.

## 5-minute demo

```bash
cd guides/solo-engineer-stack
chmod +x scripts/demo.sh
./scripts/demo.sh
```

Open **http://localhost:8080** and walk through 5 tabs:

| Tab | What to say | What happens |
|-----|-------------|--------------|
| **Submit** | "End users send feedback — built by OpenHands + Aider + Cline" | POST `/api/feedback` |
| **Dashboard** | "Founder triages — new → triaged → done" | PATCH status live |
| **Analytics** | "PostHog captures events — we show the same stream locally" | `/api/events` table |
| **Support** | "Chatwoot CSAT ≤ 2 loops back to Task Master" | Submit score **1** → show `artifacts/11-csat-loop/new-task.json` |
| **10 Tools** | "Every repo has equal weight — green = artifact live" | `/api/stack` board |

## Show artifacts on disk

```bash
cat artifacts/01-task-master/tasks.json    # Task Master (stage 1)
cat artifacts/02-crewai/spec.md              # CrewAI (stage 2)
python orchestrator/graph.py --dry-run       # LangGraph (stage 3)
ls pulsefeedback/                            # OpenHands/Aider/Cline output (stages 4–6)
cat n8n/workflows/csat-loop.json           # n8n (stage 7)
cat pulsefeedback/Dockerfile                 # Coolify (stage 8)
curl localhost:8080/api/events               # PostHog stand-in (stage 9)
curl -X POST localhost:8080/api/webhooks/csat -d '{"score":1}'  # Chatwoot loop (stage 10)
```

## Optional: n8n live

```bash
docker compose up -d
# Import guides/solo-engineer-stack/n8n/workflows/csat-loop.json in n8n UI
```

## Run tests (proof API works)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -q
./scripts/verify-stack.sh    # all 10 stages — 15 checks
```

## Blog recording order

1. **Hook** — "One founder, 10 repos, one product"  
2. **Browser** — PulseFeedback UI (submit + triage)  
3. **Terminal** — `./scripts/demo.sh` CSAT loop + `new-task.json`  
4. **Diagram** — Deca-Loop from README  
5. **CTA** — Full tutorial: `guides/solo-engineer-stack/TUTORIAL.md`  

## Terminal GIFs (blog embeds)

All under `assets/` — regenerate with:

```bash
cd guides/solo-engineer-stack/assets
python3 render_stack_screenshots.py gif
```

| GIF | Use in blog section |
|-----|---------------------|
| `step-00-demo.gif` | Hero / quick start |
| `step-01` … `step-10` | One per tool |
| `step-11-verify-stack.gif` | "It really works" |
| `step-12-csat-loop.gif` | Deca-Loop closer |

## Table visuals (Medium-friendly)

**15 animated table GIFs** — upload these instead of markdown tables:

| GIF | Section |
|-----|---------|
| `table-demo-output.gif` | Demo outputs |
| `table-ui-tabs.gif` | Browser 5 tabs |
| `team-vs-stack-table.gif` | 2022 team → 2026 repos |
| `table-hire-artifacts.gif` | Hire + artifact (3 cols) |
| `table-handoff-summary.gif` | All 10 part handoffs |
| `crewai-agents-table.gif` | brief / spec / test-plan |
| `table-langgraph-nodes.gif` | LangGraph pipeline |
| `table-api-routes.gif` | REST API |
| `table-n8n-workflows.gif` | n8n automations |
| `table-posthog-events.gif` | Analytics events |
| `table-weekly-ritual.gif` | Weekly founder ritual |
| `table-api-reference.gif` | Endpoint reference |
| `table-troubleshooting.gif` | Common fixes |
| `table-whats-next.gif` | Related guides |
| `deca-loop-tools-table.gif` | 10 tools overview |

```bash
cd guides/solo-engineer-stack/assets
python3 render_table_gifs.py all
```

## What is pre-built vs what you extend

| Already runnable in repo | You add with external tools |
|--------------------------|----------------------------|
| PulseFeedback app + UI | Task Master npm CLI (optional) |
| `tasks.json` generator | CrewAI with your LLM API key |
| LangGraph orchestrator | OpenHands / Aider / Cline sessions on your repo |
| n8n workflow JSON | Import + activate in n8n |
| Docker deploy file | Coolify on your VPS |
| Event stream API | Real PostHog project key |
| CSAT webhook | Real Chatwoot widget token |

The **demo app is the reference implementation** of what OpenHands + Aider + Cline produce — you can still run those tools to modify it live on camera.
