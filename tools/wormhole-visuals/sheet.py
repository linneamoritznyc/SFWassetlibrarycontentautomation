import sys, os, json
from PIL import Image, ImageDraw
tiles = sys.argv[2:]; out = sys.argv[1]
T = 360; Hh = 450
rows = [t.split(',') for t in tiles]
n = max(len(r) for r in rows)
im = Image.new('RGB', (n * (T + 8), len(rows) * (Hh + 8)), (40, 40, 40))
for j, r in enumerate(rows):
    for i, f in enumerate(r):
        if f: im.paste(Image.open(f).convert('RGB').resize((T, Hh)), (i * (T + 8), j * (Hh + 8)))
im.save(out, quality=85)
