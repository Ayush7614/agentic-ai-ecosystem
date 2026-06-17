# PulseFeedback — Sample PRD (Task Master input)

Use this file as input for **Claude Task Master** (Part 1). Task Master should emit **10 epics** — one per tool in the Solo Engineer Stack.

---

## Product

**PulseFeedback** — a self-hosted feature-feedback collector for solo founders.

### Goals

1. Collect user feedback via embeddable widget  
2. Triage feedback in a simple dashboard  
3. Route support questions to Chatwoot  
4. Measure conversion with PostHog  
5. Close the loop: bad CSAT → new dev tasks  

### Users

- **End user** — submits feedback (no account)  
- **Founder** — triages, replies, ships fixes  

### MVP scope

| Feature | Priority |
|---------|----------|
| POST `/api/feedback` — title, body, email optional | P0 |
| GET `/api/feedback` — list for dashboard | P0 |
| React dashboard — list + status (new / triaged / done) | P0 |
| PostHog — `feedback_submitted`, `dashboard_viewed` | P0 |
| Chatwoot widget on marketing page | P1 |
| n8n — PR merged → deploy → Slack | P1 |
| LangGraph gate — human approves before deploy | P1 |

### Non-goals (v1)

- Multi-tenant billing  
- Mobile apps  
- Real-time collaboration  

### Success metrics

- Time from PRD to deployed URL < 48 hours (solo + stack)  
- PostHog funnel: widget view → submit > 15%  
- Chatwoot first response < 4 hours (automated draft OK)  

### Stack constraint

**Every epic must map to exactly one Solo Engineer Stack tool:**

1. Task Master — parse this PRD  
2. CrewAI — research + spec + QA plan  
3. LangGraph — orchestration  
4. OpenHands — scaffold  
5. Aider — API  
6. Cline — frontend  
7. n8n — automation  
8. Coolify — deploy  
9. PostHog — analytics  
10. Chatwoot — support  

### Acceptance

- [ ] App live on HTTPS via Coolify  
- [ ] All 10 tools configured and documented in README  
- [ ] CSAT webhook creates Task Master task when score ≤ 2  
