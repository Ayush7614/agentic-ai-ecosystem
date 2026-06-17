#!/usr/bin/env python3
"""Render gif-mix-6-steps.html — all 6 stages in one looping GIF."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "gif-mix-6-steps.html"
PNG = ROOT / "gif-mix-6-steps.png"
GIF = ROOT / "gif-mix-6-steps.gif"

FPS = 15
DURATION_S = 12.0  # 2s per step × 6
DEVICE_SCALE = 2


def _python() -> str:
    conda = Path.home() / "miniconda3" / "bin" / "python"
    return str(conda) if conda.exists() else sys.executable


def ensure_playwright() -> None:
    py = _python()
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([py, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py, "-m", "playwright", "install", "chromium"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Render 6-step mix overview GIF")
    parser.add_argument("--png-only", action="store_true")
    parser.add_argument("--gif-only", action="store_true")
    args = parser.parse_args()

    if not HTML.exists():
        sys.exit(f"Missing {HTML}")
    ensure_playwright()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(HTML.as_uri(), wait_until="networkidle")
        capture = page.locator("#capture")
        capture.wait_for(state="visible")

        if not args.gif_only:
            page.wait_for_timeout(1000)
            capture.screenshot(path=str(PNG), type="png")
            print(f"Wrote {PNG}")

        if not args.png_only:
            if not shutil.which("ffmpeg"):
                sys.exit("ffmpeg required")
            n = int(FPS * DURATION_S)
            frames_dir = ROOT / ".frames-mix-6"
            frames_dir.mkdir(exist_ok=True)
            page.wait_for_timeout(200)
            for i in range(n):
                capture.screenshot(path=str(frames_dir / f"frame_{i:04d}.png"), type="png")
                page.wait_for_timeout(int(1000 / FPS))
            browser.close()

            pal = frames_dir / "palette.png"
            subprocess.check_call(
                ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "frame_%04d.png"),
                 "-vf", f"fps={FPS},palettegen=max_colors=256:stats_mode=full", str(pal)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            subprocess.check_call(
                ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "frame_%04d.png"),
                 "-i", str(pal), "-lavfi", f"fps={FPS}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3",
                 "-loop", "0", str(GIF)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            shutil.rmtree(frames_dir)
            print(f"Wrote {GIF} ({n} frames @ {FPS} fps, {DURATION_S}s loop)")
            return

        browser.close()


if __name__ == "__main__":
    main()
