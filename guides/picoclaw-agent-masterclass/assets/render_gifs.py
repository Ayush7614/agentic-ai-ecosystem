#!/usr/bin/env python3
"""Render PicoClaw Masterclass GIFs."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIAGRAMS = {
    "picoclaw-stack": "diagram-picoclaw-stack.gif",
    "workspace-anatomy": "diagram-workspace-anatomy.gif",
    "channels-map": "diagram-channels-map.gif",
    "edge-hardware": "diagram-edge-hardware.gif",
}
STEPS = [
    ("01-launcher-webui", "step-01-launcher-webui"),
    ("02-onboard-cli", "step-02-onboard-cli"),
    ("03-telegram-gateway", "step-03-telegram-gateway"),
    ("04-mcp-skills", "step-04-mcp-skills"),
    ("05-cron-heartbeat", "step-05-cron-heartbeat"),
]

def py():
    v = Path(__file__).resolve().parents[2] / "minicpm-v-mcp-server" / ".venv" / "bin" / "python"
    if v.exists():
        return str(v)
    c = Path.home() / "miniconda3/bin/python"
    return str(c) if c.exists() else sys.executable

def ensure_pw():
    try:
        import playwright  # noqa
    except ImportError:
        subprocess.check_call([py(), "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py(), "-m", "playwright", "install", "chromium"])

def gif(html, out, extra="", vw=1160, vh=380, frames=36, fps=12):
    from playwright.sync_api import sync_playwright
    fd = out.parent / f".frames-{out.stem}"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=2)
        for i in range(frames):
            prog = (i + 1) / frames
            page.goto(html.as_uri() + extra.replace("{p}", str(prog)), wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
        browser.close()
    subprocess.check_call(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(fd / "frame_%04d.png"),
        "-vf", f"fps={fps},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-loop", "0", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(fd, ignore_errors=True)

def main():
    ensure_pw()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("all", "diagrams"):
        for did, name in DIAGRAMS.items():
            print(f"GIF {name} …")
            gif(ROOT / "picoclaw-diagrams.html", ROOT / name, f"?diagram={did}&frame={{p}}")
    if cmd in ("all", "terminal"):
        for sid, name in STEPS:
            print(f"GIF {name}.gif …")
            gif(ROOT / "picoclaw-terminal.html", ROOT / f"{name}.gif", f"?step={sid}&frame={{p}}", 980, 560, 18, 10)
    if cmd in ("all", "mega"):
        print("GIF mega-picoclaw-everything.gif …")
        gif(ROOT / "picoclaw-mega.html", ROOT / "mega-picoclaw-everything.gif", "?frame={p}", 1200, 600, 48, 12)
    print("Done.")

if __name__ == "__main__":
    main()
