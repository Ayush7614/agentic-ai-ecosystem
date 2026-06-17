#!/usr/bin/env python3
"""Render LLM fine-tuning blog poster 1200x600 PNG."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML, OUT = ROOT / "blog-poster.html", ROOT / "blog-poster-1200x600.png"

def py():
    c = Path.home() / "miniconda3/bin/python"
    return str(c) if c.exists() else sys.executable

def main():
    try:
        import playwright  # noqa
    except ImportError:
        subprocess.check_call([py(), "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py(), "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 600})
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.locator("#capture").screenshot(path=str(OUT), type="png")
        browser.close()
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
