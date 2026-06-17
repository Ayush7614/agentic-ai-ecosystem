#!/usr/bin/env python3
"""Render ALL tutorial table GIFs from tutorial-tables.html (?table=id&frame=)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "tutorial-tables.html"
FPS = 10
DEVICE_SCALE = 1.5

# table_id → output gif filename, frames, viewport
TABLES: dict[str, dict] = {
    "demo-output": {
        "gif": "table-demo-output.gif",
        "frames": 14,
        "viewport": {"width": 920, "height": 480},
    },
    "ui-tabs": {
        "gif": "table-ui-tabs.gif",
        "frames": 14,
        "viewport": {"width": 980, "height": 520},
    },
    "hire-artifacts": {
        "gif": "table-hire-artifacts.gif",
        "frames": 22,
        "viewport": {"width": 1080, "height": 680},
    },
    "team-vs-stack": {
        "gif": "team-vs-stack-table.gif",
        "frames": 22,
        "viewport": {"width": 960, "height": 720},
    },
    "crewai-agents": {
        "gif": "crewai-agents-table.gif",
        "frames": 14,
        "viewport": {"width": 920, "height": 520},
    },
    "langgraph-nodes": {
        "gif": "table-langgraph-nodes.gif",
        "frames": 14,
        "viewport": {"width": 920, "height": 480},
    },
    "handoff-summary": {
        "gif": "table-handoff-summary.gif",
        "frames": 22,
        "viewport": {"width": 1040, "height": 720},
    },
    "api-routes": {
        "gif": "table-api-routes.gif",
        "frames": 16,
        "viewport": {"width": 920, "height": 560},
    },
    "n8n-workflows": {
        "gif": "table-n8n-workflows.gif",
        "frames": 12,
        "viewport": {"width": 960, "height": 420},
    },
    "posthog-events": {
        "gif": "table-posthog-events.gif",
        "frames": 12,
        "viewport": {"width": 860, "height": 400},
    },
    "weekly-ritual": {
        "gif": "table-weekly-ritual.gif",
        "frames": 14,
        "viewport": {"width": 900, "height": 480},
    },
    "api-reference": {
        "gif": "table-api-reference.gif",
        "frames": 16,
        "viewport": {"width": 920, "height": 560},
    },
    "troubleshooting": {
        "gif": "table-troubleshooting.gif",
        "frames": 20,
        "viewport": {"width": 1040, "height": 640},
    },
    "whats-next": {
        "gif": "table-whats-next.gif",
        "frames": 14,
        "viewport": {"width": 900, "height": 480},
    },
    "deca-loop": {
        "gif": "deca-loop-tools-table.gif",
        "frames": 24,
        "viewport": {"width": 1080, "height": 680},
    },
}


def ensure_playwright() -> None:
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def _url(table_id: str, frame: float | None = None) -> str:
    u = HTML.as_uri() + f"?table={table_id}"
    if frame is not None:
        u += f"&frame={frame}"
    return u


def capture_png(table_id: str, out: Path, viewport: dict) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=viewport, device_scale_factor=DEVICE_SCALE)
        page.goto(_url(table_id, 1.0), wait_until="networkidle")
        page.wait_for_function("window.__READY === true")
        page.wait_for_timeout(400)
        page.locator("#capture").screenshot(path=str(out), type="png")
        browser.close()


def capture_gif(table_id: str, out: Path, viewport: dict, frames: int) -> None:
    from playwright.sync_api import sync_playwright

    frames_dir = ROOT / f".frames-{out.stem}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=viewport, device_scale_factor=DEVICE_SCALE)
        for i in range(frames):
            progress = (i + 1) / frames
            page.goto(_url(table_id, progress), wait_until="networkidle")
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
            str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(frames_dir)


def render_one(table_id: str, spec: dict) -> None:
    gif_path = ROOT / spec["gif"]
    png_path = gif_path.with_suffix(".png")
    print(f"PNG  {png_path.name}")
    capture_png(table_id, png_path, spec["viewport"])
    print(f"GIF  {gif_path.name} ({spec['frames']} frames)")
    capture_gif(table_id, gif_path, spec["viewport"], spec["frames"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        choices=["all", *TABLES.keys()],
    )
    args = parser.parse_args()

    if not HTML.exists():
        sys.exit(f"Missing {HTML}")

    ensure_playwright()
    names = list(TABLES) if args.target == "all" else [args.target]

    for table_id in names:
        render_one(table_id, TABLES[table_id])

    print(f"Done. {len(names)} table GIF(s).")


if __name__ == "__main__":
    main()
