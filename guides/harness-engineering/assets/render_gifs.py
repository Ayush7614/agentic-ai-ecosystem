#!/usr/bin/env python3
"""Render harness engineering GIFs at 1200x600."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
W, H, FPS, SCALE = 1200, 600, 15, 1

def py():
    c = Path.home() / "miniconda3/bin/python"
    return str(c) if c.exists() else sys.executable

def ensure_pw():
    try:
        import playwright  # noqa
    except ImportError:
        subprocess.check_call([py(), "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([py(), "-m", "playwright", "install", "chromium"])

def gif(html, out, frames, extra=""):
    from playwright.sync_api import sync_playwright
    fd = ROOT / f".frames-{out.stem}"
    fd.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for i in range(frames):
            prog = (i + 1) / frames
            page.goto(html.as_uri() + extra.replace("{p}", str(prog)), wait_until="networkidle")
            page.wait_for_function("window.__READY === true")
            page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
        browser.close()
    subprocess.check_call(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fd / "frame_%04d.png"),
        "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=full[p];[s1][p]paletteuse",
        "-loop", "0", str(out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(fd, ignore_errors=True)

def main():
    ensure_pw()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"

    previews = [
        ("home", "preview-course-home.gif", 4.0),
        ("lecture", "preview-lecture.gif", 4.0),
        ("resources", "preview-resource-library.gif", 4.5),
    ]
    if cmd in ("all", "previews"):
        for scene, name, dur in previews:
            print(f"GIF {name} …")
            gif(ROOT / "harness-previews.html", ROOT / name, int(FPS * dur), f"?scene={scene}&frame={{p}}")

    diagrams = {
        "harness-pattern": "diagram-harness-pattern.gif",
        "five-subsystems": "diagram-five-subsystems.gif",
        "agents-map": "diagram-agents-map.gif",
        "session-lifecycle": "diagram-session-lifecycle.gif",
        "planner-eval": "diagram-planner-eval.gif",
    }
    if cmd in ("all", "diagrams"):
        for did, name in diagrams.items():
            print(f"GIF {name} …")
            frames = int(FPS * 3.5)
            fd = ROOT / f".frames-{Path(name).stem}"
            fd.mkdir(parents=True, exist_ok=True)
            from playwright.sync_api import sync_playwright
            html = ROOT / "harness-diagrams.html"
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
                for i in range(frames):
                    page.goto(html.as_uri() + f"?diagram={did}&frame={(i+1)/frames}", wait_until="networkidle")
                    page.wait_for_function("window.__READY === true")
                    page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
                browser.close()
            subprocess.check_call(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fd / "frame_%04d.png"),
                "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=full[p];[s1][p]paletteuse",
                "-loop", "0", str(ROOT / name)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            shutil.rmtree(fd, ignore_errors=True)

    steps = [
        ("01-drop-templates", "step-01-drop-templates.gif"),
        ("02-init-session", "step-02-init-session.gif"),
        ("03-verify-gate", "step-03-verify-gate.gif"),
        ("04-handoff", "step-04-handoff.gif"),
    ]
    if cmd in ("all", "terminal"):
        for sid, name in steps:
            print(f"GIF {name} …")
            frames = 20
            fd = ROOT / f".frames-{Path(name).stem}"
            fd.mkdir(parents=True, exist_ok=True)
            from playwright.sync_api import sync_playwright
            html = ROOT / "harness-terminal.html"
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
                for i in range(frames):
                    page.goto(html.as_uri() + f"?step={sid}&frame={(i+1)/frames}", wait_until="networkidle")
                    page.wait_for_function("window.__READY === true")
                    page.locator("#capture").screenshot(path=str(fd / f"frame_{i:04d}.png"))
                browser.close()
            subprocess.check_call(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fd / "frame_%04d.png"),
                "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=full[p];[s1][p]paletteuse",
                "-loop", "0", str(ROOT / name)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            shutil.rmtree(fd, ignore_errors=True)

    if cmd in ("all", "mega"):
        print("GIF mega-harness-everything.gif …")
        gif(ROOT / "harness-mega.html", ROOT / "mega-harness-everything.gif", int(FPS * 12), "?frame={p}")

    print("Done.")

if __name__ == "__main__":
    main()
