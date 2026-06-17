#!/usr/bin/env python3
"""Render Hermes Masterclass table GIFs."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "tutorial-tables.html"
FPS, SCALE = 10, 1.5
TABLES = {
    "demo-three-agents": ("demo-three-agents.gif", 14, {"width": 1000, "height": 420}),
    "hermes-vs-openclaw": ("table-hermes-vs-openclaw.gif", 16, {"width": 1020, "height": 480}),
    "curator-phases": ("table-curator-phases.gif", 14, {"width": 940, "height": 460}),
    "skills-hub": ("table-skills-hub.gif", 14, {"width": 920, "height": 440}),
    "three-souls": ("table-three-souls.gif", 14, {"width": 1080, "height": 400}),
}

def py():
    c = Path.home() / "miniconda3/bin/python"
    return str(c) if c.exists() else sys.executable

def ensure_pw():
    try:
        import playwright  # noqa
    except ImportError:
        subprocess.check_call([py(), "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py(), "-m", "playwright", "install", "chromium"])

def render(tid, out, frames, vp):
    from playwright.sync_api import sync_playwright
    fd = out.parent / f".frames-{out.stem}"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=vp, device_scale_factor=SCALE)
        for i in range(frames):
            page.goto(HTML.as_uri() + f"?table={tid}&frame={(i+1)/frames}", wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
        browser.close()
    subprocess.check_call(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fd / "frame_%04d.png"),
        "-vf", f"fps={FPS},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-loop", "0", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(fd, ignore_errors=True)

def main():
    ensure_pw()
    t = sys.argv[1] if len(sys.argv) > 1 else "all"
    for tid, (gif, frames, vp) in TABLES.items():
        if t not in ("all", tid): continue
        print(f"GIF {gif} …")
        render(tid, ROOT / gif, frames, vp)
    print("Done.")

if __name__ == "__main__":
    main()
