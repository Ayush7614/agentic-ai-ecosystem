#!/usr/bin/env python3
"""Render Loop Engineering terminal GIFs."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "loop-terminal.html"
W, H, FPS, SCALE = 1200, 600, 10, 1  # blog/Medium hero size
STEPS = [
    ("01-loop-scaffold", "step-01-loop-scaffold"),
    ("02-test-gate", "step-02-test-gate"),
    ("03-eval-yaml", "step-03-eval-yaml"),
    ("04-max-iterations", "step-04-max-iterations"),
    ("05-multi-agent", "step-05-multi-agent"),
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
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for i in range(frames):
            page.goto(HTML.as_uri() + f"?step={step_id}&frame={(i+1)/frames}", wait_until="networkidle")
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
    for sid, name in STEPS:
        if t not in ("all", sid):
            continue
        print(f"GIF {name}.gif …")
        gif(sid, ROOT / f"{name}.gif")
    print("Done.")

if __name__ == "__main__":
    main()
