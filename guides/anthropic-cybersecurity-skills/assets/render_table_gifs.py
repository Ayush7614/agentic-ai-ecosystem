#!/usr/bin/env python3
"""Render Part 16 / Part 17 table GIFs from HTML."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FPS = 10
DEVICE_SCALE = 1.5

TABLES = {
    "part16": {
        "html": ROOT / "part16-domains-table.html",
        "gif": ROOT / "part16-domains-table.gif",
        "png": ROOT / "part16-domains-table.png",
        "frames": 30,
        "viewport": {"width": 1080, "height": 920},
    },
    "part17": {
        "html": ROOT / "part17-attck-table.html",
        "gif": ROOT / "part17-attck-table.gif",
        "png": ROOT / "part17-attck-table.png",
        "frames": 18,
        "viewport": {"width": 920, "height": 720},
    },
}


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


def capture_png(spec: dict) -> None:
    from playwright.sync_api import sync_playwright

    url = spec["html"].as_uri() + "?frame=1"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport=spec["viewport"],
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(url, wait_until="networkidle")
        page.wait_for_function("window.__READY === true")
        page.wait_for_timeout(400)
        page.locator("#capture").screenshot(path=str(spec["png"]), type="png")
        browser.close()
    print(f"PNG  {spec['png'].name}")


def capture_gif(spec: dict) -> None:
    from playwright.sync_api import sync_playwright

    frames = spec["frames"]
    frames_dir = ROOT / f".frames-{spec['gif'].stem}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport=spec["viewport"],
            device_scale_factor=DEVICE_SCALE,
        )
        for i in range(frames):
            progress = (i + 1) / frames
            url = spec["html"].as_uri() + f"?frame={progress}"
            page.goto(url, wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.wait_for_timeout(60)
            page.locator("#capture").screenshot(
                path=str(frames_dir / f"frame_{i:04d}.png"), type="png"
            )
        browser.close()

    subprocess.check_call(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-vf", f"fps={FPS},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop", "0",
            str(spec["gif"]),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(frames_dir)
    print(f"GIF  {spec['gif'].name} ({frames} frames)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        choices=["all", "part16", "part17"],
    )
    args = parser.parse_args()
    ensure_playwright()

    names = list(TABLES) if args.target == "all" else [args.target]
    for name in names:
        spec = TABLES[name]
        if not spec["html"].exists():
            sys.exit(f"Missing {spec['html']}")
        capture_png(spec)
        capture_gif(spec)
    print("Done.")


if __name__ == "__main__":
    main()
