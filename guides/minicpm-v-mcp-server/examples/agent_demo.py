#!/usr/bin/env python3
"""End-to-end demo — MiniCPM-V MCP vision tools (works offline with OLLAMA_MOCK=1).

Simulates what Cursor / Claude Desktop sees when the agent calls vision tools.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import vision_backend as vb  # noqa: E402
from server import compare_images, describe_image, ocr_document  # noqa: E402

FIXTURES = ROOT / "fixtures"


def _banner(title: str) -> None:
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")


def _parse(result: str) -> dict:
    return json.loads(result)


def main() -> None:
    os.environ.setdefault("OLLAMA_VISION_MODEL", "minicpm-v4.6")
    if not FIXTURES.exists() or not list(FIXTURES.glob("*.png")):
        from generate_fixtures import main as gen  # noqa: E402

        gen()

    status = vb.health_check()
    _banner("MiniCPM-V 4.6 Vision MCP — Agent Demo")
    print(f"Model: {vb.VISION_MODEL}  ·  Mode: {status.get('mode', '?')}")
    if not status.get("ok") and not vb.MOCK:
        print("\n⚠️  Ollama offline — re-run with OLLAMA_MOCK=1 or start Ollama.\n")

    # Scenario 1 — describe screenshot
    _banner("Scenario 1 — describe_image")
    print('[Tool: describe_image]  path=fixtures/diagram_v2.png')
    r1 = _parse(describe_image(str(FIXTURES / "diagram_v2.png"), "What services are shown?"))
    print("\n## Architecture summary\n")
    print(r1.get("result", r1.get("error", r1)))

    # Scenario 2 — OCR receipt
    _banner("Scenario 2 — ocr_document")
    print('[Tool: ocr_document]  path=fixtures/sample_receipt.png')
    r2 = _parse(ocr_document(str(FIXTURES / "sample_receipt.png")))
    print("\n## Receipt OCR\n")
    print(r2.get("result", r2.get("error", r2)))

    # Scenario 3 — compare before/after
    _banner("Scenario 3 — compare_images")
    print("[Tool: compare_images]  v1 → v2 pipeline diagrams")
    r3 = _parse(
        compare_images(
            str(FIXTURES / "diagram_v1.png"),
            str(FIXTURES / "diagram_v2.png"),
            focus="new components and labels",
        )
    )
    print("\n## Visual diff\n")
    print(r3.get("result", r3.get("error", r3)))

    _banner("Done — wire examples/server.py into Cursor MCP settings")
    print("See examples/cursor_mcp.json.example")


if __name__ == "__main__":
    main()
