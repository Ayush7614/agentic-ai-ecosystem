# PulseFeedback — Test Plan

## API
- [ ] POST feedback returns 201 + id
- [ ] GET lists in reverse chronological order
- [ ] PATCH status triaged → done

## UI
- [ ] Submit form clears on success
- [ ] Dashboard status buttons update row
- [ ] Analytics tab shows feedback_submitted

## Stack integration
- [ ] CSAT score 1 creates artifacts/11-csat-loop/new-task.json
- [ ] /api/stack shows 10 tools with live flags
- [ ] n8n webhook hits /api/webhooks/csat (manual curl)
