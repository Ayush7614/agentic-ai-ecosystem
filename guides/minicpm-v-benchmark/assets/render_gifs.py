#!/usr/bin/env python3
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def ensure_pw():
    try:
        import playwright  # noqa
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def render(html: Path, out: Path, w: int, h: int, frames: int = 20) -> None:
    from playwright.sync_api import sync_playwright
    fd = ROOT / f".frames-{out.stem}"
    fd.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        for i in range(frames):
            page.goto(html.as_uri() + f"?frame={(i+1)/frames}", wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.locator("#capture").screenshot(path=str(fd / f"f_{i:04d}.png"))
        browser.close()
    subprocess.check_call(["ffmpeg", "-y", "-framerate", "10", "-i", str(fd / "f_%04d.png"),
        "-vf", "fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-loop", "0", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(fd, ignore_errors=True)
    print(f"Wrote {out}")


def main():
    ensure_pw()
    render(ROOT / "benchmark-terminal.html", ROOT / "step-benchmark-run.gif", 960, 420)
    render(ROOT / "benchmark-table.html", ROOT / "benchmark-comparison.gif", 1000, 560, 16)


if __name__ == "__main__":
    main()
