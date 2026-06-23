"""Ollama vision backend for MiniCPM-V 4.6."""
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


def chat_vision(prompt: str, image_paths: list[Path], *, timeout: float = 120.0) -> str:
    if MOCK:
        return f"[mock {VISION_MODEL}] {prompt[:80]}… ({len(image_paths)} image(s))"
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
        raise VisionError(f"Cannot reach Ollama at {OLLAMA_HOST}") from exc
    content = (data.get("message") or {}).get("content", "").strip()
    if not content:
        raise VisionError("Empty response from Ollama")
    return content
