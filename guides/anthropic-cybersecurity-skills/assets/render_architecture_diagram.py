#!/usr/bin/env python3
"""Render Part 3 architecture diagram to PNG and GIF."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "architecture-progressive-disclosure.html"
PNG = ROOT / "architecture-progressive-disclosure.png"
GIF = ROOT / "architecture-progressive-disclosure.gif"
FPS = 8
DURATION_S = 3.0
DEVICE_SCALE = 1.5


def _python() -> str:
    conda = Path.home() / "miniconda3" / "bin" / "python"
    if conda.exists():
        return str(conda)
    return sys.executable


def ensure_playwright() -> None:
    py = _python()
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([py, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py, "-m", "playwright", "install", "chromium"])


def capture_png() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1160, "height": 620},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.wait_for_function("window.__READY === true")
        page.wait_for_timeout(500)
        page.locator("#capture").screenshot(path=str(PNG), type="png")
        browser.close()
    print(f"PNG  {PNG.name}")


def capture_gif() -> int:
    from playwright.sync_api import sync_playwright

    frame_count = int(FPS * DURATION_S)
    frames_dir = ROOT / ".frames-architecture"
    frames_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1160, "height": 620},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.wait_for_function("window.__READY === true")
        page.wait_for_timeout(400)

        for i in range(frame_count):
            page.locator("#capture").screenshot(
                path=str(frames_dir / f"frame_{i:04d}.png"), type="png"
            )
            page.wait_for_timeout(int(1000 / FPS))
        browser.close()

    subprocess.check_call(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-vf", f"fps={FPS},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop", "0",
            str(GIF),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(frames_dir)
    return frame_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--png-only", action="store_true")
    parser.add_argument("--gif-only", action="store_true")
    args = parser.parse_args()

    if not HTML.exists():
        sys.exit(f"Missing {HTML}")

    ensure_playwright()

    if not args.gif_only:
        capture_png()
    if not args.png_only:
        if not shutil.which("ffmpeg"):
            sys.exit("ffmpeg is required for GIF output")
        n = capture_gif()
        print(f"GIF  {GIF.name} ({n} frames @ {FPS} fps)")

    print("Done.")


if __name__ == "__main__":
    main()
