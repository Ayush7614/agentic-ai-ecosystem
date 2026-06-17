# PulseFeedback — Technical Spec

## Stack
- Backend: FastAPI + SQLite (Postgres in production)
- Frontend: Static HTML/JS served by FastAPI
- Deploy: Coolify + Docker

## API
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/feedback | Create feedback |
| GET | /api/feedback | List feedback (?status=) |
| PATCH | /api/feedback/{id} | Update status |
| POST | /api/events | Analytics capture |
| POST | /api/webhooks/csat | CSAT loop trigger |
| GET | /api/stack | 10-tool status board |

## Schema
- feedback: id, title, body, email, status (new|triaged|done), created_at
