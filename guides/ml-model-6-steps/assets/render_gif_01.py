#!/usr/bin/env python3
"""Render gif-01-pipeline-overview.html to high-quality PNG and GIF."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "gif-01-pipeline-overview.html"
PNG = ROOT / "gif-01-pipeline-overview.png"
GIF = ROOT / "gif-01-pipeline-overview.gif"

# High quality: retina capture, smooth loop aligned with 5.5s CSS animations
FPS = 15
DURATION_S = 5.5
DEVICE_SCALE = 3
VIEWPORT_W = 1280
VIEWPORT_H = 960


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


def capture_png(out: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(HTML.as_uri(), wait_until="networkidle")
        capture = page.locator("#capture")
        capture.wait_for(state="visible")
        page.wait_for_timeout(600)
        capture.screenshot(path=str(out), type="png")
        browser.close()


def capture_gif(out: Path) -> int:
    from playwright.sync_api import sync_playwright

    frame_count = int(FPS * DURATION_S)
    frames_dir = out.parent / f".frames-{out.stem}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(HTML.as_uri(), wait_until="networkidle")
        capture = page.locator("#capture")
        capture.wait_for(state="visible")
        page.wait_for_timeout(400)

        for i in range(frame_count):
            capture.screenshot(path=str(frames_dir / f"frame_{i:04d}.png"), type="png")
            page.wait_for_timeout(int(1000 / FPS))
        browser.close()

    palette = frames_dir / "palette.png"
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-vf", f"fps={FPS},palettegen=max_colors=256:stats_mode=full",
            str(palette),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-i", str(palette),
            "-lavfi", f"fps={FPS}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3",
            "-loop", "0",
            str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(frames_dir)
    return frame_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Render ML pipeline overview GIF 1")
    parser.add_argument("--png-only", action="store_true")
    parser.add_argument("--gif-only", action="store_true")
    args = parser.parse_args()

    if not HTML.exists():
        sys.exit(f"Missing {HTML}")
    if not shutil.which("ffmpeg") and not args.png_only:
        sys.exit("ffmpeg is required for GIF output")

    ensure_playwright()

    if not args.gif_only:
        capture_png(PNG)
        print(f"Wrote {PNG}")

    if not args.png_only:
        n = capture_gif(GIF)
        print(f"Wrote {GIF} ({n} frames @ {FPS} fps, scale={DEVICE_SCALE}x)")


if __name__ == "__main__":
    main()
