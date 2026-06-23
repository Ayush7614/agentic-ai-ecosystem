#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

out = Path(__file__).resolve().parent / "samples"
out.mkdir(exist_ok=True)
img = Image.new("RGB", (480, 640), "#fafafa")
d = ImageDraw.Draw(img)
try:
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
except OSError:
    f = ImageFont.load_default()
d.text((40, 40), "COFFEE BEAN Co.", fill="#111", font=f)
d.text((40, 100), "TOTAL  $10.75", fill="#222", font=f)
d.text((40, 140), "2026-06-23", fill="#555", font=f)
img.save(out / "receipt.png")
print(f"Wrote {out / 'receipt.png'}")
