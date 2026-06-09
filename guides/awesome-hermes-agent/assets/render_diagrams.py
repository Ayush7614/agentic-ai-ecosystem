#!/usr/bin/env python3
"""Render Hermes guide HTML diagrams to PNG and GIF."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FPS = 12
DURATION_S = 3.0
DEVICE_SCALE = 2

DIAGRAMS = {
    "workflow": {
        "html": ROOT / "hermes-ecosystem-workflow.html",
        "png": ROOT / "hermes-ecosystem-workflow.png",
        "gif": ROOT / "hermes-ecosystem-workflow.gif",
    },
}


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


def capture_png(html: Path, out: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 900},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(html.as_uri(), wait_until="networkidle")
        capture = page.locator("#capture")
        capture.wait_for(state="visible")
        page.wait_for_timeout(400)
        capture.screenshot(path=str(out), type="png")
        browser.close()


def capture_gif(html: Path, out: Path) -> int:
    from playwright.sync_api import sync_playwright

    frame_count = int(FPS * DURATION_S)
    frames_dir = out.parent / f".frames-{out.stem}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 900},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(html.as_uri(), wait_until="networkidle")
        capture = page.locator("#capture")
        capture.wait_for(state="visible")
        page.wait_for_timeout(300)

        for i in range(frame_count):
            capture.screenshot(path=str(frames_dir / f"frame_{i:04d}.png"), type="png")
            page.wait_for_timeout(int(1000 / FPS))
        browser.close()

    palette = frames_dir / "palette.png"
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-vf", f"fps={FPS},palettegen",
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
            "-lavfi", f"fps={FPS}[x];[x][1:v]paletteuse",
            "-loop", "0",
            str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(frames_dir)
    return frame_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("diagram", nargs="?", default="workflow", choices=["workflow"])
    parser.add_argument("--png-only", action="store_true")
    parser.add_argument("--gif-only", action="store_true")
    args = parser.parse_args()

    spec = DIAGRAMS[args.diagram]
    if not spec["html"].exists():
        sys.exit(f"Missing {spec['html']}")
    if not shutil.which("ffmpeg") and not args.png_only:
        sys.exit("ffmpeg is required for GIF output")

    ensure_playwright()

    if not args.gif_only:
        capture_png(spec["html"], spec["png"])
        print(f"Wrote {spec['png']}")

    if not args.png_only:
        n = capture_gif(spec["html"], spec["gif"])
        print(f"Wrote {spec['gif']} ({n} frames @ {FPS} fps)")


if __name__ == "__main__":
    main()
