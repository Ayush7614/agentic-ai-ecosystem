#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
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
    out = ROOT / "blog-poster-1200x600.png"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 600})
        page.goto((ROOT / "blog-poster.html").as_uri(), wait_until="networkidle")
        page.locator("#capture").screenshot(path=str(out), type="png")
        browser.close()
    print(f"Wrote {out}")
if __name__ == "__main__":
    main()
