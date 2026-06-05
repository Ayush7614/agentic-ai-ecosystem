#!/usr/bin/env python3
"""Render Claude Code guide HTML diagrams to PNG and GIF."""

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
    "anatomy": {
        "html": ROOT / "claude-folder-anatomy.html",
        "png": ROOT / "claude-folder-anatomy.png",
        "gif": ROOT / "claude-folder-anatomy.gif",
    },
    "workflow": {
        "html": ROOT / "claude-code-workflow.html",
        "png": ROOT / "claude-code-workflow.png",
        "gif": ROOT / "claude-code-workflow.gif",
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


def render_one(name: str, png_only: bool = False, gif_only: bool = False) -> None:
    spec = DIAGRAMS[name]
    html = spec["html"]
    if not html.exists():
        sys.exit(f"Missing {html}")

    if not gif_only:
        capture_png(html, spec["png"])
        print(f"Wrote {spec['png']}")

    if not png_only:
        if not shutil.which("ffmpeg"):
            sys.exit("ffmpeg is required for GIF output")
        n = capture_gif(html, spec["gif"])
        print(f"Wrote {spec['gif']} ({n} frames @ {FPS} fps)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "diagram",
        nargs="?",
        choices=["anatomy", "workflow", "all"],
        default="all",
    )
    parser.add_argument("--png-only", action="store_true")
    parser.add_argument("--gif-only", action="store_true")
    args = parser.parse_args()

    ensure_playwright()
    names = list(DIAGRAMS) if args.diagram == "all" else [args.diagram]
    for name in names:
        render_one(name, png_only=args.png_only, gif_only=args.gif_only)


if __name__ == "__main__":
    main()
