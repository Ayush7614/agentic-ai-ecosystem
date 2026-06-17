#!/usr/bin/env python3
"""Render LLM fine-tuning mega overview GIF — 1200x600, full story in one loop."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "mega-finetune.html"
OUT = ROOT / "mega-finetune-everything.gif"
W, H, FPS, DUR, SCALE = 1200, 600, 15, 12.0, 1

def py():
    c = Path.home() / "miniconda3/bin/python"
    return str(c) if c.exists() else sys.executable

def ensure_pw():
    try:
        import playwright  # noqa
    except ImportError:
        subprocess.check_call([py(), "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py(), "-m", "playwright", "install", "chromium"])

def main():
    ensure_pw()
    from playwright.sync_api import sync_playwright
    frames = int(FPS * DUR)
    fd = ROOT / ".frames-mega-finetune"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for i in range(frames):
            prog = (i + 1) / frames
            page.goto(HTML.as_uri() + f"?frame={prog}", wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
        browser.close()
    subprocess.check_call(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fd / "frame_%04d.png"),
        "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=full[p];[s1][p]paletteuse",
        "-loop", "0", str(OUT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(fd, ignore_errors=True)
    print(f"Wrote {OUT} ({W}x{H}, {frames} frames)")

if __name__ == "__main__":
    main()
