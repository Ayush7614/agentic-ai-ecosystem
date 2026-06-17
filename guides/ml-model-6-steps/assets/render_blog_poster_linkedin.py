#!/usr/bin/env python3
"""Render LinkedIn article poster — 1200×627 PNG."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "blog-poster-linkedin.html"
OUT = ROOT / "blog-poster-linkedin-1200x627.png"
WIDTH = 1200
HEIGHT = 627


def _python() -> str:
    conda = Path.home() / "miniconda3" / "bin" / "python"
    return str(conda) if conda.exists() else sys.executable


def ensure_playwright() -> None:
    py = _python()
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([py, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py, "-m", "playwright", "install", "chromium"])


def main() -> None:
    from playwright.sync_api import sync_playwright

    if not HTML.exists():
        sys.exit(f"Missing {HTML}")

    ensure_playwright()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=1,
        )
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.locator("#capture").wait_for(state="visible")
        page.wait_for_timeout(300)
        page.locator("#capture").screenshot(path=str(OUT), type="png")
        browser.close()

    print(f"Wrote {OUT} ({WIDTH}×{HEIGHT}, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
