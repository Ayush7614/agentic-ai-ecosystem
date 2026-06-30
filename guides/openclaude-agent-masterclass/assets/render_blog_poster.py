#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path(__file__).resolve().parent / "blog-poster-1200x600.png"
html = Path(__file__).resolve().parent / "blog-poster.html"
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1200, "height": 600})
    page.goto(html.as_uri(), wait_until="networkidle")
    page.locator("#capture").screenshot(path=str(out), type="png")
    b.close()
print(out)
