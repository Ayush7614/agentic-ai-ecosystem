#!/usr/bin/env python3
"""Shared renderer for ML blog GIFs 05–07."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SPECS = {
    "05": {"html": "gif-05-train-loop.html", "png_wait_ms": 4200, "duration_s": 5.0},
    "06": {"html": "gif-06-evaluation-dashboard.html", "png_wait_ms": 3200, "duration_s": 5.0},
    "07": {"html": "gif-07-deploy-monitor.html", "png_wait_ms": 2800, "duration_s": 4.0},
}

FPS = 15
DEVICE_SCALE = 2
VIEWPORT_W = 1280
VIEWPORT_H = 960


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


def render(num: str, png_only: bool = False, gif_only: bool = False) -> None:
    spec = SPECS[num]
    html = ROOT / spec["html"]
    stem = html.stem
    png = ROOT / f"{stem}.png"
    gif = ROOT / f"{stem}.gif"
    duration = spec["duration_s"]

    if not html.exists():
        sys.exit(f"Missing {html}")

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(html.as_uri(), wait_until="networkidle")
        capture = page.locator("#capture")
        capture.wait_for(state="visible")

        if not gif_only:
            page.wait_for_timeout(spec["png_wait_ms"])
            capture.screenshot(path=str(png), type="png")
            print(f"Wrote {png}")

        if not png_only:
            if not shutil.which("ffmpeg"):
                sys.exit("ffmpeg is required for GIF output")
            frame_count = int(FPS * duration)
            frames_dir = ROOT / f".frames-{stem}"
            frames_dir.mkdir(parents=True, exist_ok=True)
            page.wait_for_timeout(300)
            for i in range(frame_count):
                capture.screenshot(path=str(frames_dir / f"frame_{i:04d}.png"), type="png")
                page.wait_for_timeout(int(1000 / FPS))
            browser.close()

            palette = frames_dir / "palette.png"
            subprocess.check_call(
                ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "frame_%04d.png"),
                 "-vf", f"fps={FPS},palettegen=max_colors=256:stats_mode=full", str(palette)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            subprocess.check_call(
                ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "frame_%04d.png"),
                 "-i", str(palette),
                 "-lavfi", f"fps={FPS}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3",
                 "-loop", "0", str(gif)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            shutil.rmtree(frames_dir)
            print(f"Wrote {gif} ({frame_count} frames @ {FPS} fps)")
            return

        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("gif", choices=["05", "06", "07", "all"], nargs="?", default="all")
    parser.add_argument("--png-only", action="store_true")
    parser.add_argument("--gif-only", action="store_true")
    args = parser.parse_args()

    ensure_playwright()
    nums = list(SPECS) if args.gif == "all" else [args.gif]
    for n in nums:
        render(n, png_only=args.png_only, gif_only=args.gif_only)


if __name__ == "__main__":
    main()
