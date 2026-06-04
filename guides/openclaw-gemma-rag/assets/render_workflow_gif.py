#!/usr/bin/env python3
"""Render openclaw-gemma-rag-workflow.html to an animated GIF (same style as qwen guide)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "openclaw-gemma-rag-workflow.html"
DEFAULT_OUT = ROOT / "openclaw-gemma-rag-workflow.gif"
FPS = 12
DURATION_S = 3.0
DEVICE_SCALE = 2


def _python() -> str:
    conda = Path.home() / "miniconda3" / "bin" / "python"
    if conda.exists():
        return str(conda)
    return sys.executable


def ensure_playwright():
    py = _python()
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([py, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py, "-m", "playwright", "install", "chromium"])


def capture_frames(frames_dir: Path) -> int:
    from playwright.sync_api import sync_playwright

    frame_count = int(FPS * DURATION_S)
    url = HTML.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 900},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(url, wait_until="networkidle")
        capture = page.locator("#capture")
        capture.wait_for(state="visible")
        page.wait_for_timeout(300)

        for i in range(frame_count):
            capture.screenshot(path=str(frames_dir / f"frame_{i:04d}.png"), type="png")
            page.wait_for_timeout(int(1000 / FPS))

        browser.close()

    return frame_count


def build_gif(frames_dir: Path, out: Path, frame_count: int) -> None:
    palette = frames_dir / "palette.png"
    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(frames_dir / "frame_%04d.png"),
            "-vf",
            f"fps={FPS},palettegen",
            str(palette),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(frames_dir / "frame_%04d.png"),
            "-i",
            str(palette),
            "-lavfi",
            f"fps={FPS}[x];[x][1:v]paletteuse",
            "-loop",
            "0",
            str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    if not HTML.exists():
        sys.exit(f"Missing {HTML}")
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is required")

    ensure_playwright()
    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        frames_dir = Path(tmp)
        n = capture_frames(frames_dir)
        build_gif(frames_dir, out, n)

    subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(out)],
        check=False,
        capture_output=True,
        text=True,
    )
    print(f"Wrote {out} ({n} frames @ {FPS} fps, cropped to #capture)")


if __name__ == "__main__":
    main()
