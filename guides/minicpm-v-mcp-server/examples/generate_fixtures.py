#!/usr/bin/env python3
"""Generate sample images for MCP demos (no external assets required)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _font(size: int):
    for name in ("DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def receipt() -> None:
    img = Image.new("RGB", (480, 640), "#fafafa")
    d = ImageDraw.Draw(img)
    f, fs = _font(22), _font(16)
    d.text((40, 40), "COFFEE BEAN Co.", fill="#1a1a1a", font=f)
    d.text((40, 90), "123 Main St · San Francisco", fill="#555", font=fs)
    lines = [
        "Latte (Oat)          $5.50",
        "Croissant            $4.25",
        "Tip                  $1.00",
        "─────────────────────────",
        "TOTAL               $10.75",
        "Card **** 4242",
        "2026-06-23 09:14 AM",
    ]
    y = 150
    for line in lines:
        d.text((40, y), line, fill="#222", font=fs)
        y += 36
    img.save(FIXTURES / "sample_receipt.png")


def diagram_v1() -> None:
    img = Image.new("RGB", (640, 400), "#0f172a")
    d = ImageDraw.Draw(img)
    f = _font(18)
    d.rounded_rectangle((40, 80, 200, 160), radius=12, fill="#1e3a5f", outline="#38bdf8")
    d.text((70, 110), "API", fill="#e2e8f0", font=f)
    d.rounded_rectangle((420, 80, 580, 160), radius=12, fill="#14532d", outline="#4ade80")
    d.text((440, 110), "Qdrant", fill="#e2e8f0", font=f)
    d.line((200, 120, 420, 120), fill="#94a3b8", width=3)
    d.text((250, 200), "v1 — sync pipeline", fill="#94a3b8", font=f)
    img.save(FIXTURES / "diagram_v1.png")


def diagram_v2() -> None:
    img = Image.new("RGB", (640, 400), "#0f172a")
    d = ImageDraw.Draw(img)
    f = _font(18)
    d.rounded_rectangle((40, 80, 200, 160), radius=12, fill="#1e3a5f", outline="#38bdf8")
    d.text((60, 110), "LitServe", fill="#e2e8f0", font=f)
    d.rounded_rectangle((250, 60, 410, 140), radius=12, fill="#4c1d95", outline="#a78bfa")
    d.text((270, 90), "CrewAI", fill="#e2e8f0", font=f)
    d.rounded_rectangle((420, 80, 580, 160), radius=12, fill="#14532d", outline="#4ade80")
    d.text((440, 110), "Qdrant", fill="#e2e8f0", font=f)
    d.line((200, 120, 250, 100), fill="#94a3b8", width=3)
    d.line((410, 100, 420, 120), fill="#94a3b8", width=3)
    d.text((200, 200), "v2 — agentic pipeline", fill="#fbbf24", font=f)
    img.save(FIXTURES / "diagram_v2.png")


def main() -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    receipt()
    diagram_v1()
    diagram_v2()
    print(f"Fixtures written to {FIXTURES}")


if __name__ == "__main__":
    main()
