import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database import get_db, init_db, utc_now
from schemas import (
    AnalyticsEvent,
    CSATWebhook,
    FeedbackCreate,
    FeedbackOut,
    FeedbackUpdate,
    StackToolStatus,
)

load_dotenv()

ROOT = Path(os.environ.get("STACK_ROOT", str(Path(__file__).resolve().parents[2])))
ARTIFACTS = ROOT / "artifacts"
STATIC = Path(__file__).resolve().parents[1] / "frontend"

app = FastAPI(title="PulseFeedback", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ARTIFACTS.mkdir(parents=True, exist_ok=True)
init_db()


@app.on_event("startup")
def startup():
    init_db()


def _row_to_feedback(row) -> FeedbackOut:
    return FeedbackOut(
        id=row["id"],
        title=row["title"],
        body=row["body"],
        email=row["email"],
        status=row["status"],
        created_at=row["created_at"],
    )


@app.get("/health")
def health():
    return {"status": "ok", "product": "PulseFeedback", "stack": "solo-engineer-stack"}


@app.post("/api/feedback", response_model=FeedbackOut)
def create_feedback(payload: FeedbackCreate):
    with get_db() as conn:
        cur = conn.execute(
            """
            INSERT INTO feedback (title, body, email, status, created_at)
            VALUES (?, ?, ?, 'new', ?)
            """,
            (payload.title, payload.body, payload.email, utc_now()),
        )
        row = conn.execute("SELECT * FROM feedback WHERE id = ?", (cur.lastrowid,)).fetchone()
    _log_event("feedback_submitted", {"title": payload.title[:80]})
    return _row_to_feedback(row)


@app.get("/api/feedback", response_model=list[FeedbackOut])
def list_feedback(status: str | None = Query(default=None)):
    with get_db() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM feedback WHERE status = ? ORDER BY id DESC",
                (status,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
    return [_row_to_feedback(r) for r in rows]


@app.patch("/api/feedback/{feedback_id}", response_model=FeedbackOut)
def update_feedback(feedback_id: int, payload: FeedbackUpdate):
    with get_db() as conn:
        conn.execute(
            "UPDATE feedback SET status = ? WHERE id = ?",
            (payload.status, feedback_id),
        )
        row = conn.execute("SELECT * FROM feedback WHERE id = ?", (feedback_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Feedback not found")
    _log_event("feedback_status_changed", {"id": feedback_id, "status": payload.status})
    return _row_to_feedback(row)


@app.post("/api/events")
def track_event(payload: AnalyticsEvent):
    """PostHog-style event capture (demo + real PostHog can mirror this)."""
    _log_event(payload.event, payload.properties or {})
    return {"ok": True}


@app.get("/api/events")
def list_events(limit: int = Query(default=50, le=200)):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT event, properties, created_at FROM analytics_events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {
            "event": r["event"],
            "properties": json.loads(r["properties"]) if r["properties"] else {},
            "created_at": r["created_at"],
        }
        for r in rows
    ]


@app.post("/api/webhooks/csat")
def csat_webhook(payload: CSATWebhook):
    """n8n / Chatwoot CSAT loop — score ≤ 2 creates a new task artifact."""
    with get_db() as conn:
        conn.execute(
            "INSERT INTO csat_responses (score, comment, created_at) VALUES (?, ?, ?)",
            (payload.score, payload.comment, utc_now()),
        )

    loop_dir = ARTIFACTS / "11-csat-loop"
    loop_dir.mkdir(parents=True, exist_ok=True)
    event_file = loop_dir / "events.jsonl"
    with event_file.open("a") as f:
        f.write(json.dumps({"score": payload.score, "comment": payload.comment, "at": utc_now()}) + "\n")

    loop_triggered = payload.score <= 2
    if loop_triggered:
        task = {
            "source": "chatwoot_csat",
            "title": "Fix support issue from low CSAT",
            "score": payload.score,
            "comment": payload.comment,
            "next_tool": "task_master",
            "created_at": utc_now(),
        }
        (loop_dir / "new-task.json").write_text(json.dumps(task, indent=2))

    _log_event("csat_received", {"score": payload.score, "loop_triggered": loop_triggered})
    return {"ok": True, "loop_triggered": loop_triggered}


@app.get("/api/stack", response_model=list[StackToolStatus])
def stack_status():
    """Live demo: which of the 10 stack tools are reachable."""
    n8n_live = _probe("http://localhost:5678/healthz")
    return [
        StackToolStatus(id=1, name="Task Master", role="PM", artifact="artifacts/01-task-master/tasks.json", live=ARTIFACTS.joinpath("01-task-master/tasks.json").exists()),
        StackToolStatus(id=2, name="CrewAI", role="Tech lead", artifact="artifacts/02-crewai/", live=ARTIFACTS.joinpath("02-crewai/spec.md").exists()),
        StackToolStatus(id=3, name="LangGraph", role="Architect", artifact="orchestrator/graph.py", demo_url="/docs", live=True),
        StackToolStatus(id=4, name="OpenHands", role="Junior dev", artifact="pulsefeedback/", live=True),
        StackToolStatus(id=5, name="Aider", role="Mid-level dev", artifact="pulsefeedback/backend/main.py", live=True),
        StackToolStatus(id=6, name="Cline", role="IDE teammate", artifact="pulsefeedback/frontend/", live=True),
        StackToolStatus(id=7, name="n8n", role="Ops", artifact="n8n/workflows/", demo_url="http://localhost:5678", live=n8n_live),
        StackToolStatus(id=8, name="Coolify", role="DevOps", artifact="pulsefeedback/Dockerfile", live=Path(__file__).joinpath("..", "..", "Dockerfile").resolve().exists()),
        StackToolStatus(id=9, name="PostHog", role="QA + data", artifact="/api/events", demo_url="/api/events", live=True),
        StackToolStatus(id=10, name="Chatwoot", role="Support", artifact="/api/webhooks/csat", demo_url="http://localhost:3000", live=_probe("http://localhost:3000")),
    ]


def _log_event(event: str, properties: dict | None = None) -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT INTO analytics_events (event, properties, created_at) VALUES (?, ?, ?)",
            (event, json.dumps(properties or {}), utc_now()),
        )


def _probe(url: str) -> bool:
    try:
        import httpx

        r = httpx.get(url, timeout=1.5)
        return r.status_code < 500
    except Exception:
        return False


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
