#!/usr/bin/env python3
"""Render MiniCPM-V MCP terminal demo GIFs."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "minicpm-terminal.html"
W, H, FPS = 920, 480, 10
STEPS = [("demo", "step-mcp-vision-demo"), ("ollama", "step-ollama-minicpm")]


def ensure_pw():
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def gif(step_id: str, out: Path, frames: int = 24) -> None:
    from playwright.sync_api import sync_playwright

    fd = out.parent / f".frames-{out.stem}"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        for i in range(frames):
            page.goto(HTML.as_uri() + f"?step={step_id}&frame={(i + 1) / frames}", wait_until="networkidle")
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
    t = sys.argv[1] if len(sys.argv) > 1 else "all"
    for sid, name in STEPS:
        if t not in ("all", sid):
            continue
        print(f"GIF {name}.gif …")
        gif(sid, ROOT / f"{name}.gif")
    print("Done.")


if __name__ == "__main__":
    main()
