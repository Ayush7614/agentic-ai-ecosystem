#!/usr/bin/env python3
"""Render Ollama Small Models guide GIFs."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIAGRAMS = {
    "ram-tiers": "diagram-ram-tiers.gif",
    "task-picker": "diagram-task-picker.gif",
    "model-families": "diagram-model-families.gif",
    "pull-run-workflow": "diagram-pull-run-workflow.gif",
}
STEPS = [
    ("01-install-verify", "step-01-install-verify"),
    ("02-pull-qwen08b", "step-02-pull-qwen08b"),
    ("03-run-chat-response", "step-03-run-chat-response"),
    ("04-vision-minicpm", "step-04-vision-minicpm"),
    ("05-coding-glm", "step-05-coding-glm"),
    ("06-embed-ps", "step-06-embed-ps"),
]

def py():
    c = Path.home() / "miniconda3/bin/python"
    if c.exists():
        return str(c)
    v = Path(__file__).resolve().parents[2] / "minicpm-v-mcp-server" / ".venv" / "bin" / "python"
    return str(v) if v.exists() else sys.executable

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
            gif(ROOT / "ollama-diagrams.html", ROOT / name, f"?diagram={did}&frame={{p}}")
    if cmd in ("all", "terminal"):
        for sid, name in STEPS:
            print(f"GIF {name}.gif …")
            gif(ROOT / "ollama-terminal.html", ROOT / f"{name}.gif", f"?step={sid}&frame={{p}}", 980, 560, 18, 10)
    if cmd in ("all", "mega"):
        print("GIF mega-ollama-small-models.gif …")
        gif(ROOT / "ollama-mega.html", ROOT / "mega-ollama-small-models.gif", "?frame={p}", 1200, 600, 48, 12)
    print("Done.")

if __name__ == "__main__":
    main()
