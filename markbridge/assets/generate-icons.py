#!/usr/bin/env python3
"""Generate MarkBridge icons from scratch using Pillow."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(os.path.abspath(__file__))

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = size * 0.18
    # Background rounded rect
    d.rounded_rectangle([0, 0, size-1, size-1], radius=int(r), fill="#5B6FFF")
    # White "M" letter
    m = size * 0.2
    pts = [
        (m, size-m),
        (m, m),
        (size/2, size*0.55),
        (size-m, m),
        (size-m, size-m),
    ]
    sw = max(2, int(size * 0.09))
    d.line(pts, fill="white", width=sw, joint="curve")
    return img

for sz in [16, 32, 48, 64, 128, 256, 512]:
    draw_icon(sz).save(f"{OUT}/icon_{sz}.png")

# icon.png (256px — used by Linux + electron-builder)
draw_icon(256).save(f"{OUT}/icon.png")

# tray.png (32px)
draw_icon(32).save(f"{OUT}/tray.png")

# icon.ico (multi-size Windows icon)
imgs = [draw_icon(s) for s in [16, 32, 48, 256]]
imgs[0].save(f"{OUT}/icon.ico", format="ICO", sizes=[(s,s) for s in [16,32,48,256]],
             append_images=imgs[1:])

print(f"Icons generated in {OUT}/")
