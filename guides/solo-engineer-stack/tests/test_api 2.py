import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pulsefeedback" / "backend"))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["product"] == "PulseFeedback"


def test_feedback_crud():
    r = client.post("/api/feedback", json={"title": "Test", "body": "Hello world"})
    assert r.status_code == 200
    fid = r.json()["id"]

    r = client.get("/api/feedback")
    assert any(x["id"] == fid for x in r.json())

    r = client.patch(f"/api/feedback/{fid}", json={"status": "triaged"})
    assert r.json()["status"] == "triaged"


def test_csat_loop():
    r = client.post("/api/webhooks/csat", json={"score": 1, "comment": "bad"})
    assert r.json()["loop_triggered"] is True


def test_stack_endpoint():
    r = client.get("/api/stack")
    assert r.status_code == 200
    assert len(r.json()) == 10
