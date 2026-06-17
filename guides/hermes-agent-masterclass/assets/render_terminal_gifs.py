#!/usr/bin/env python3
"""Render Hermes Masterclass terminal GIFs."""
from __future__ import annotations
import argparse, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "masterclass-terminal.html"
FPS, SCALE = 10, 2
STEPS = [
    ("01-install-setup", "step-01-install-setup"),
    ("02-gateway-telegram", "step-02-gateway-telegram"),
    ("03-profiles-create", "step-03-profiles-create"),
    ("04-claude-code", "step-04-claude-code"),
    ("05-cron-list", "step-05-cron-list"),
    ("06-install-web", "step-06-install-web"),
    ("07-dashboard", "step-07-dashboard"),
    ("08-researcher-profile", "step-08-researcher-profile"),
    ("09-mcp-skills", "step-09-mcp-skills"),
    ("10-researcher-chat", "step-10-researcher-chat"),
]

def py():
    c = Path.home() / "miniconda3/bin/python"
    return str(c) if c.exists() else sys.executable

def ensure_pw():
    try:
        import playwright  # noqa
    except ImportError:
        subprocess.check_call([py(), "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py(), "-m", "playwright", "install", "chromium"])

def gif(step_id, out, frames=18):
    from playwright.sync_api import sync_playwright
    fd = out.parent / f".frames-{out.stem}"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 980, "height": 560}, device_scale_factor=SCALE)
        for i in range(frames):
            url = HTML.as_uri() + f"?step={step_id}&frame={(i+1)/frames}"
            page.goto(url, wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
        browser.close()
    subprocess.check_call(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fd / "frame_%04d.png"),
        "-vf", f"fps={FPS},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-loop", "0", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(fd, ignore_errors=True)

def main():
    ensure_pw()
    t = (sys.argv[1] if len(sys.argv) > 1 else "all")
    for sid, name in STEPS:
        if t not in ("all", sid): continue
        print(f"GIF {name}.gif …")
        gif(sid, ROOT / f"{name}.gif")
    print("Done.")

if __name__ == "__main__":
    main()
