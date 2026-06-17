#!/usr/bin/env python3
"""Render MCP Visual Guide diagram GIFs — 1200x600."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "mcp-diagrams.html"
W, H, FPS, SCALE, DUR = 1200, 600, 12, 1, 3.0

DIAGRAMS = {
    "usbc-hub": "diagram-usbc-hub.gif",
    "host-stack": "diagram-host-stack.gif",
    "server-primitives": "diagram-server-primitives.gif",
    "transport": "diagram-transport.gif",
    "handshake": "diagram-handshake.gif",
    "api-rigid": "diagram-api-rigid.gif",
    "api-break": "diagram-api-break.gif",
    "mcp-dynamic": "diagram-mcp-dynamic.gif",
    "text-vs-ui": "diagram-text-vs-ui.gif",
    "visuals-flow": "diagram-visuals-flow.gif",
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

def gif(did, out):
    from playwright.sync_api import sync_playwright
    frames = int(FPS * DUR)
    fd = out.parent / f".frames-{out.stem}"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for i in range(frames):
            page.goto(HTML.as_uri() + f"?diagram={did}&frame={(i+1)/frames}", wait_until="networkidle")
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
    for did, name in DIAGRAMS.items():
        if t not in ("all", did):
            continue
        print(f"GIF {name} …")
        gif(did, ROOT / name)
    print("Done.")

if __name__ == "__main__":
    main()
