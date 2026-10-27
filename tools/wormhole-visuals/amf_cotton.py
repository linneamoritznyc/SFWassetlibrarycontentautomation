"""k20261030: Carla's paper pick, AM fungi extend cotton's phosphorus reach 15-fold
(Mai et al. 2019, European Journal of Soil Biology 90: 31-35). Drawn diagrams, no photos.

  SFW_FONTS=<fonts dir> python3 tools/wormhole-visuals/amf_cotton.py
    -> apps/web/public/wormhole/tiles/k20261030-v1-<n>.jpg
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "apps", "web", "public", "wormhole", "tiles")
LOGO = os.path.join(HERE, "..", "..", "apps", "web", "public", "wormhole", "sfw-foundation-wordmark-240.png")
F = os.environ["SFW_FONTS"]
W, H = 1080, 1350
GREEN, DEEP, CREAM, BROWN, TAN, SAND, LIGHT = "#156826", "#22371F", "#F4F1EA", "#4F3433", "#C89B7B", "#D8C3A5", "#59A66C"


def font(n, s):
    return ImageFont.truetype(os.path.join(F, n), s)


MONT = lambda s: font("montserrat-latin-800-normal.woff2", s)
GOTH = lambda s: font("pathway-gothic-one-latin-400-normal.woff2", s)
SANS = lambda s: font("source-sans-3-latin-400-normal.woff2", s)


def wash(c, box, color, seed, alpha=210):
    """A soft watercolor blot: a few jittered translucent layers, blurred edges."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r, g, b = Image.new("RGB", (1, 1), color).getpixel((0, 0))
    for k in range(5):
        j = 18 + k * 6
        pts = []
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
        for t in range(36):
            a = t / 36 * 2 * math.pi
            m = 1 + rnd.uniform(-0.06, 0.06)
            pts.append((cx + math.cos(a) * (rx + rnd.uniform(-j, j)) * m, cy + math.sin(a) * (ry + rnd.uniform(-j, j)) * m))
        d.polygon(pts, fill=(r, g, b, alpha // 5))
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    c.alpha_composite(layer)


def hyphae(d, cx, cy, r0, r1, seed, color=CREAM, n=46, width=3):
    rnd = random.Random(seed)
    for i in range(n):
        a = i / n * 2 * math.pi + rnd.uniform(-0.05, 0.05)
        x, y = cx + math.cos(a) * r0, cy + math.sin(a) * r0
        length = rnd.uniform(0.75, 1.0) * (r1 - r0)
        steps = 18
        for s in range(steps):
            a += rnd.uniform(-0.12, 0.12)
            nx, ny = x + math.cos(a) * length / steps, y + math.sin(a) * length / steps
            d.line((x, y, nx, ny), fill=color, width=width)
            if rnd.random() < 0.10:
                b = a + rnd.choice((-1, 1)) * rnd.uniform(0.4, 0.9)
                bx, by = nx, ny
                for _ in range(5):
                    ex, ey = bx + math.cos(b) * length / steps, by + math.sin(b) * length / steps
                    d.line((bx, by, ex, ey), fill=color, width=max(1, width - 1))
                    bx, by = ex, ey
            x, y = nx, ny


def text(d, xy, rows, f, fill, lh):
    x, y = xy
    for r in rows:
        top = d.textbbox((0, 0), r, font=f)[1]
        d.text((x, y - top), r, font=f, fill=fill)
        y += lh
    return y


def logo(c):
    lg = Image.open(LOGO).convert("RGBA")
    lg.thumbnail((110, 110))
    disc = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, 129, 129), fill=CREAM)
    disc.alpha_composite(lg, ((130 - lg.width) // 2, (130 - lg.height) // 2))
    c.alpha_composite(disc, (W - 170, 40))


def slide1():
    c = Image.new("RGBA", (W, H), DEEP)
    cx, cy = 540, 640
    wash(c, (cx - 430, cy - 430, cx + 430, cy + 430), SAND, 3, 170)
    d = ImageDraw.Draw(c)
    hyphae(d, cx, cy, 40, 400, 7, color=CREAM, n=54, width=3)
    wash(c, (cx - 60, cy - 60, cx + 60, cy + 60), TAN, 5, 255)
    d = ImageDraw.Draw(c)
    d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=BROWN)
    # scale: root reach vs hyphal reach
    d.line((cx, cy + 470, cx + 400, cy + 470), fill=CREAM, width=4)
    d.line((cx, cy + 455, cx, cy + 485), fill=CREAM, width=4)
    d.line((cx + 400, cy + 455, cx + 400, cy + 485), fill=CREAM, width=4)
    text(d, (cx + 120, cy + 500), ["HYPHAE: ABOUT 30 MM"], GOTH(44), CREAM, 50)
    text(d, (cx - 430, cy + 470), ["COTTON ROOT AT THE CENTER"], GOTH(38), CREAM, 44)
    d.rectangle((60, 70, 860, 300), fill=CREAM)
    y = text(d, (100, 108), ["Fungi reach 15 times", "more soil than the root."], MONT(54), BROWN, 66)
    text(d, (100, y + 14), ["Field study on cotton, Mai et al. 2019"], SANS(30), BROWN, 36)
    logo(c)
    return c


def slide2():
    c = Image.new("RGBA", (W, H), CREAM)
    wash(c, (120, 260, 960, 1000), LIGHT, 11, 120)
    d = ImageDraw.Draw(c)
    text(d, (140, 330), ["15x"], MONT(330), GREEN, 340)
    d.rectangle((0, 1010, W, H), fill=GREEN)
    y = text(d, (90, 1060), ["MORE SOIL FOR PHOSPHORUS"], GOTH(56), CREAM, 66)
    text(d, (90, y + 10), ["Mycorrhizal hyphae carried phosphorus to cotton", "roots from up to 30 mm away in the field."],
         SANS(38), CREAM, 48)
    return c


def slide3():
    c = Image.new("RGBA", (W, H), DEEP)
    d = ImageDraw.Draw(c)
    # two soils side by side: low P with many hyphae, high P with few
    for i, (n, label) in enumerate([(54, "LOW SOLUBLE P"), (12, "HIGH SOLUBLE P")]):
        cx = 290 + i * 500
        cy = 640
        wash(c, (cx - 230, cy - 230, cx + 230, cy + 230), SAND, 20 + i, 150)
        d = ImageDraw.Draw(c)
        hyphae(d, cx, cy, 26, 215, 30 + i, color=CREAM, n=n, width=3)
        d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), fill=BROWN)
        w = d.textlength(label, font=GOTH(44))
        text(d, (cx - w / 2, cy + 280), [label], GOTH(44), CREAM, 50)
    d.rectangle((60, 90, 880, 300), fill=CREAM)
    y = text(d, (100, 128), ["More soluble P,", "fewer hyphae."], MONT(58), BROWN, 70)
    d.rectangle((60, 1080, 1020, 1250), fill=GREEN)
    text(d, (100, 1110), ["Cotton took up the most P at a moderate rate,", "150 kg P2O5 per hectare. The authors say balance", "fertilizer with the fungal pathway."],
         SANS(34), CREAM, 44)
    return c


if __name__ == "__main__":
    for n, make in [(1, slide1), (2, slide3)]:
        p = os.path.join(OUT, f"k20261030-v1-{n}.jpg")
        assert not os.path.exists(p), p
        make().convert("RGB").save(p, quality=90)
        print(p)
