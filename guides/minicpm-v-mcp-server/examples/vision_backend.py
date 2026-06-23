"""Ollama vision backend for MiniCPM-V 4.6 — shared by MCP server and demos."""
from __future__ import annotations

import base64
import os
from pathlib import Path

import httpx

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
VISION_MODEL = os.environ.get("OLLAMA_VISION_MODEL", "minicpm-v4.6")
MOCK = os.environ.get("OLLAMA_MOCK", "0") == "1"

SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}


class VisionError(Exception):
    pass


def _encode_image(path: Path) -> str:
    if not path.is_file():
        raise VisionError(f"Image not found: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise VisionError(f"Unsupported image type: {path.suffix}")
    return base64.b64encode(path.read_bytes()).decode("ascii")


def _mock_response(prompt: str, image_count: int) -> str:
    return (
        f"[mock {VISION_MODEL}] Processed {image_count} image(s).\n"
        f"Prompt preview: {prompt[:120]}…\n"
        "Set OLLAMA_MOCK=0 and run `ollama pull minicpm-v4.6` for live inference."
    )


def chat_vision(prompt: str, image_paths: list[Path], *, timeout: float = 120.0) -> str:
    """Send a vision chat request to Ollama."""
    if MOCK:
        return _mock_response(prompt, len(image_paths))

    images_b64 = [_encode_image(p) for p in image_paths]
    payload = {
        "model": VISION_MODEL,
        "messages": [{"role": "user", "content": prompt, "images": images_b64}],
        "stream": False,
    }
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(f"{OLLAMA_HOST}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except httpx.ConnectError as exc:
        raise VisionError(
            f"Cannot reach Ollama at {OLLAMA_HOST}. Start Ollama and run: ollama pull {VISION_MODEL}"
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise VisionError(f"Ollama error {exc.response.status_code}: {exc.response.text[:300]}") from exc

    message = data.get("message") or {}
    content = message.get("content", "").strip()
    if not content:
        raise VisionError("Empty response from Ollama")
    return content


def health_check() -> dict:
    """Return model + connectivity status for demos."""
    if MOCK:
        return {"ok": True, "mode": "mock", "model": VISION_MODEL}
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{OLLAMA_HOST}/api/tags")
            resp.raise_for_status()
            tags = {m.get("name", "").split(":")[0] for m in resp.json().get("models", [])}
            base = VISION_MODEL.split(":")[0]
            return {
                "ok": base in tags or VISION_MODEL in tags,
                "mode": "live",
                "model": VISION_MODEL,
                "ollama_host": OLLAMA_HOST,
            }
    except Exception as exc:  # noqa: BLE001 — demo helper
        return {"ok": False, "mode": "offline", "model": VISION_MODEL, "error": str(exc)}
