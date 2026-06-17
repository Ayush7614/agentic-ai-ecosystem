# Solo Engineer Stack — equal reference (10 tools)

Each section has the same structure: **role · install · config · PulseFeedback task · artifact · handoff**.

Use with [Tutorial](./TUTORIAL.md) Parts 1–10.

---

## 1. OpenHands — autonomous junior developer

| | |
|---|---|
| **Repo** | [github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) |
| **Role** | Scaffold repos, run tests, open PRs from issues |
| **PulseFeedback** | Create repo structure + CI + stub routes |
| **Artifact** | `artifacts/04-openhands/scaffold-pr-url.txt` |
| **Handoff to** | Aider |

```bash
git clone https://github.com/OpenHands/OpenHands.git && cd OpenHands
export LLM_MODEL=gpt-4o LLM_API_KEY=$OPENAI_API_KEY LLM_BASE_URL=$OPENAI_API_BASE
docker compose up
```

---

## 2. Aider — mid-level pair programmer

| | |
|---|---|
| **Repo** | [github.com/Aider-AI/aider](https://github.com/Aider-AI/aider) |
| **Role** | Multi-file edits with git commits from terminal |
| **PulseFeedback** | Implement FastAPI routes + pytest |
| **Artifact** | `artifacts/05-aider/git-log.txt` |
| **Handoff to** | Cline |

```bash
pip install aider-chat
aider --model openai/gpt-4o --openai-api-base $OPENAI_API_BASE --openai-api-key $OPENAI_API_KEY
```

---

## 3. Cline — AI teammate in Cursor

| | |
|---|---|
| **Repo** | [github.com/cline/cline](https://github.com/cline/cline) |
| **Role** | IDE agent — files, terminal, browser |
| **PulseFeedback** | React dashboard + browser verification |
| **Artifact** | `artifacts/06-cline/screenshot-dashboard.png` |
| **Handoff to** | n8n |

Cursor → Settings → Cline → OpenAI Compatible → `OPENAI_API_BASE` + model ID.

---

## 4. Claude Task Master — project manager

| | |
|---|---|
| **Repo** | [github.com/eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master) |
| **Role** | PRD → tasks, dependencies, agent prompts |
| **PulseFeedback** | Parse PRD → 10 tool-tagged epics |
| **Artifact** | `artifacts/01-task-master/tasks.json` |
| **Handoff to** | CrewAI |

```bash
npx task-master parse-prd examples/prd-pulsefeedback.md
npx task-master list
```

---

## 5. CrewAI — tech lead

| | |
|---|---|
| **Repo** | [github.com/crewAIInc/crewai](https://github.com/crewAIInc/crewai) |
| **Role** | Multi-agent crews with roles |
| **PulseFeedback** | brief.md + spec.md + test-plan.md |
| **Artifact** | `artifacts/02-crewai/*.md` |
| **Handoff to** | LangGraph |

```python
from crewai import Agent, Crew, LLM, Task
llm = LLM(model="gpt-4o")
# See TUTORIAL Part 2 for full crew
```

---

## 6. LangGraph — system architect

| | |
|---|---|
| **Repo** | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| **Role** | Stateful workflows, durable execution |
| **PulseFeedback** | Deca-Loop graph + human approval gate |
| **Artifact** | `artifacts/03-langgraph/state-approved.json` |
| **Handoff to** | OpenHands |

```bash
python orchestrator/graph.py --dry-run
```

---

## 7. n8n — operations team

| | |
|---|---|
| **Repo** | [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n) |
| **Role** | 400+ integrations, visual automation |
| **PulseFeedback** | Deploy + notify + CSAT loop workflows |
| **Artifact** | `artifacts/07-n8n/workflow-ids.txt` |
| **Handoff to** | Coolify |

```bash
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

---

## 8. Coolify — DevOps engineer

| | |
|---|---|
| **Repo** | [github.com/coollabsio/coolify](https://github.com/coollabsio/coolify) |
| **Role** | Self-hosted PaaS — git push deploy, SSL |
| **PulseFeedback** | HTTPS for app + services |
| **Artifact** | `artifacts/08-coolify/urls.txt` |
| **Handoff to** | PostHog |

Install on VPS → connect GitHub → enable auto-deploy on `main`.

---

## 9. PostHog — QA + data team

| | |
|---|---|
| **Repo** | [github.com/posthog/posthog](https://github.com/posthog/posthog) |
| **Role** | Analytics, replay, flags, experiments |
| **PulseFeedback** | Funnel + `feedback_submitted` events |
| **Artifact** | `artifacts/09-posthog/funnel-screenshot.png` |
| **Handoff to** | Chatwoot |

```javascript
posthog.capture('feedback_submitted')
```

---

## 10. Chatwoot — customer support

| | |
|---|---|
| **Repo** | [github.com/chatwoot/chatwoot](https://github.com/chatwoot/chatwoot) |
| **Role** | Omnichannel inbox + AI Captain |
| **PulseFeedback** | Widget + CSAT → n8n → Task Master loop |
| **Artifact** | `artifacts/10-chatwoot/widget-screenshot.png` |
| **Handoff to** | Task Master (loop) |

Embed widget → connect n8n CSAT webhook → close Deca-Loop.

---

## Equal time budget

Spend **~30 minutes per tool** on first run. If one tool takes 3 hours and another 5 minutes, rebalance — the stack only works when all ten lanes stay warm.

| Tool | Weekly touch |
|------|----------------|
| Task Master | Monday planning |
| CrewAI | Spec refresh |
| LangGraph | Gate reviews |
| OpenHands | New epics |
| Aider | Daily commits |
| Cline | UI polish |
| n8n | Workflow fixes |
| Coolify | Deploy health |
| PostHog | Metrics review |
| Chatwoot | Support triage |

Back to [Tutorial](./TUTORIAL.md)
