#!/usr/bin/env python3
"""Render installation terminal screenshots (PNG + optional GIF) for the cybersec skills guide."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "install-terminal.html"
DEVICE_SCALE = 2
FPS = 10

STEPS = [
    ("01-npx", "install-step-01-npx"),
    ("02-clone", "install-step-02-clone"),
    ("03-script", "install-step-03-script"),
    ("04-claude", "install-step-04-claude"),
    ("05-cursor", "install-step-05-cursor"),
    ("06-hermes", "install-step-06-hermes"),
    ("07-codex", "install-step-07-codex"),
    ("08-gemini", "install-step-08-gemini"),
    ("09-skill-anatomy", "part11-skill-anatomy"),
    ("10-part13", "part13-credential-dump"),
]

STEP_IDS = {s[0] for s in STEPS}


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


def capture_png(step_id: str, out: Path, frame: float | None = None) -> None:
    from playwright.sync_api import sync_playwright

    url = HTML.as_uri() + f"?step={step_id}"
    if frame is not None:
        url += f"&frame={frame}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 980, "height": 520},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(url, wait_until="networkidle")
        page.wait_for_function("window.__READY === true")
        page.wait_for_timeout(350)
        page.locator("#capture").screenshot(path=str(out), type="png")
        browser.close()


def capture_step_gif(step_id: str, out: Path, frames: int = 18) -> None:
    from playwright.sync_api import sync_playwright

    frames_dir = out.parent / f".frames-{out.stem}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 980, "height": 520},
            device_scale_factor=DEVICE_SCALE,
        )
        for i in range(frames):
            progress = (i + 1) / frames
            url = HTML.as_uri() + f"?step={step_id}&frame={progress}"
            page.goto(url, wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.wait_for_timeout(80)
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


def _selected_steps(only: str | None) -> list[tuple[str, str]]:
    if not only:
        return STEPS
    ids = [x.strip() for x in only.split(",") if x.strip()]
    bad = [i for i in ids if i not in STEP_IDS]
    if bad:
        sys.exit(f"Unknown step id(s): {', '.join(bad)}. Choose from: {', '.join(sorted(STEP_IDS))}")
    return [(sid, name) for sid, name in STEPS if sid in ids]


def render_pngs(only: str | None = None) -> None:
    for step_id, name in _selected_steps(only):
        out = ROOT / f"{name}.png"
        print(f"PNG  {name}.png")
        capture_png(step_id, out)


def render_gifs(only: str | None = None) -> None:
    for step_id, name in _selected_steps(only):
        out = ROOT / f"{name}.gif"
        print(f"GIF  {name}.gif")
        capture_step_gif(step_id, out)


def render_all_gif() -> None:
    """Single GIF cycling through all install steps."""
    out = ROOT / "install-steps-all.gif"
    frames_dir = ROOT / ".frames-install-all"
    frames_dir.mkdir(parents=True, exist_ok=True)
    idx = 0

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 980, "height": 520},
            device_scale_factor=DEVICE_SCALE,
        )
        for step_id, _ in STEPS:
            for i in range(14):
                progress = (i + 1) / 14
                url = HTML.as_uri() + f"?step={step_id}&frame={progress}"
                page.goto(url, wait_until="networkidle")
                page.wait_for_function("window.__READY === true")
                page.wait_for_timeout(60)
                page.locator("#capture").screenshot(
                    path=str(frames_dir / f"frame_{idx:04d}.png"), type="png"
                )
                idx += 1
            page.wait_for_timeout(400)
        browser.close()

    palette = frames_dir / "palette.png"
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-framerate", "8",
            "-i", str(frames_dir / "frame_%04d.png"),
            "-vf", "fps=8,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop", "0",
            str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(frames_dir)
    print(f"GIF  install-steps-all.gif ({idx} frames)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="all", choices=["all", "png", "gif", "combo"])
    parser.add_argument(
        "--only",
        help="Comma-separated step ids (e.g. 07-codex,08-gemini)",
    )
    args = parser.parse_args()

    if not HTML.exists():
        sys.exit(f"Missing {HTML}")

    ensure_playwright()

    if args.target in ("all", "png"):
        render_pngs(args.only)
    if args.target in ("all", "gif"):
        render_gifs(args.only)
    if args.target == "combo":
        render_pngs(args.only)
        render_all_gif()

    print("Done.")


if __name__ == "__main__":
    main()
