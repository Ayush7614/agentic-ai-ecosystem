#!/usr/bin/env python3
"""Render AI Agents Masterclass terminal GIFs."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "agent-terminal.html"
W, H, FPS, SCALE = 1200, 600, 10, 1
STEPS = [
    ("01-setup", "step-01-setup"),
    ("02-react-agent", "step-02-react-agent"),
    ("03-langgraph", "step-03-langgraph"),
    ("04-crewai", "step-04-crewai"),
    ("05-openai-sdk", "step-05-openai-sdk"),
    ("06-pydantic-ai", "step-06-pydantic-ai"),
    ("07-run-test", "step-07-run-test"),
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

def gif(step_id, out, frames=20):
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
