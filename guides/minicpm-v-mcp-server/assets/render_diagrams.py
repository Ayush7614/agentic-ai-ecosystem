#!/usr/bin/env python3
"""Render MiniCPM-V MCP diagram GIFs — 1200x600."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "minicpm-diagrams.html"
W, H, FPS = 1200, 600, 12

DIAGRAMS = {"capability-exchange": ("diagram-capability-exchange.gif", 3.0)}


def ensure_pw():
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def gif(did: str, out: Path, dur: float) -> None:
    from playwright.sync_api import sync_playwright

    frames = int(FPS * dur)
    fd = out.parent / f".frames-{out.stem}"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H})
        for i in range(frames):
            prog = (i + 1) / frames
            page.goto(HTML.as_uri() + f"?diagram={did}&frame={prog}", wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
        browser.close()
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fd / "frame_%04d.png"),
            "-vf", f"fps={FPS},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop", "0", str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(fd, ignore_errors=True)


def main() -> None:
    ensure_pw()
    for did, (name, dur) in DIAGRAMS.items():
        print(f"GIF {name} …")
        gif(did, ROOT / name, dur)
    print("Done.")


if __name__ == "__main__":
    main()
