#!/usr/bin/env python3
"""Generate a small test image for vision benchmarks."""
from pathlib import Path
from PIL import Image, ImageDraw

out = Path(__file__).resolve().parent / "samples" / "benchmark_card.png"
out.parent.mkdir(exist_ok=True)
img = Image.new("RGB", (512, 320), "#0f172a")
d = ImageDraw.Draw(img)
d.rounded_rectangle((40, 40, 472, 280), radius=16, outline="#38bdf8", width=3)
d.text((60, 80), "Edge Model Benchmark", fill="#e2e8f0")
d.text((60, 130), "MiniCPM-V 4.6 · Qwen3.5 · Gemma4", fill="#94a3b8")
d.text((60, 180), "16 GB Mac · Local Ollama", fill="#4ade80")
img.save(out)
print(out)
