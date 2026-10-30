"""Diwali (x20261108, 8 Nov), one slide built to docs/slide-rules.md from real flower cutouts (no AI).

A marigold garland (toran) strung across the top of a Soil Brown page, a cream box with the greeting
(86 px Montserrat Bold) and the small text (52 px Source Sans 3) and the logo, a pink lotus and jasmine
breaking out of the bottom-right corner. Every flower, the string, the box, the texts and the logo are
separate named layers.
  python3 tools/wormhole-visuals/diwali.py
"""
import math
import os

from PIL import Image, ImageDraw

from collage import Deck, paper

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
FL = "/home/user/sfwlib/social/cutouts-flowers"
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
W, H = 1080, 1350
BROWN, CREAM, INK = "#4F3433", "#F4F1EA", "#333130"


def cut(name):
    im = Image.open(f"{FL}/{name}.png").convert("RGBA")
    return im.crop(im.getchannel("A").getbbox())


def head(im, frac):
    """The flower head only: the top part of the cutout, trimmed to what is left."""
    im = im.crop((0, 0, im.width, round(im.height * frac)))
    return im.crop(im.getchannel("A").getbbox())


def swag(x0, x1, y, sag, n):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t, y + sag * 4 * t * (1 - t)))
    return pts


def main():
    d = Deck("x20261108", 1, "happy-diwali-v8", "2026-11-08")
    d.bg(0, paper(BROWN, 8, w=W, h=H, grain=6), name="Background")
    mari = head(cut("tamil-nadu-marigold"), 0.47)
    jas = head(cut("tamil-nadu-jasmine"), 0.75)
    # garland: two swags of marigold heads on a thin string, with strands hanging at the edges and centre
    swags = [swag(-40, 540, 50, 250, 8), swag(540, 1120, 50, 250, 8)]
    string = Image.new("RGBA", (W, 460), (0, 0, 0, 0))
    dr = ImageDraw.Draw(string)
    for pts in swags:
        dr.line(pts, fill=(233, 220, 195, 255), width=4, joint="curve")
    d.put(0, "Garland string", string, 0, 0, shadowed=False, anchor="tl")
    k = 0
    for pts in swags:
        for i, (x, y) in enumerate(pts):
            if i == 0 and k:
                continue
            size = 128 if i % 2 == 0 else 108
            m = mari.resize((size, round(mari.height * size / mari.width)), Image.LANCZOS)
            d.put(0, f"Marigold {k + 1}", m, round(x - size / 2), round(y - m.height / 2), shadowed=False,
                  anchor="tl")
            k += 1
    for sx in (40, 540, 1040):
        for j in range(2):
            m = mari.resize((104, round(mari.height * 104 / mari.width)), Image.LANCZOS)
            d.put(0, f"Hanging marigold {sx}-{j + 1}", m, sx - 52, 140 + j * 100, shadowed=False, anchor="tl")
    # cream box with the greeting
    bx0, by0, bx1, by1 = 72, 400, 1008, 880
    d.put(0, "Cream box", Image.new("RGBA", (bx1 - bx0, by1 - by0), CREAM), bx0, by0, shadowed=False, anchor="tl")
    d.text(0, "Headline", "Happy Diwali", bx0 + 64, by0 + 64, 800, 110, 86, kind="montserrat-bold", italic=False,
           color=BROWN, lh=1.05, min_size=84)
    d.text(0, "Details", "To our students, mentors and partners in India, and to everyone celebrating.",
           bx0 + 64, by0 + 200, 600, 260, 52, kind="source-reg", italic=False, color=INK, lh=1.2, min_size=50)
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((150, round(lg.height * 150 / lg.width)), Image.LANCZOS)
    d.put(0, "SFW logo", lg, bx1 - 64 - 150, by1 - 64 - lg.height, shadowed=False, anchor="tl")
    # a flower offering along the bottom, breaking out of both corners
    def place(name, w, x, y, crop=1.0):
        im = cut(name) if crop == 1.0 else head(cut(name), crop)
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        d.put(0, name.split("-", 2)[-1].replace("-", " ").title(), im, x, y, shadowed=False, anchor="tl")
    place("tamil-nadu-gloriosa-lily", 300, -40, 930)
    place("tamil-nadu-jasmine", 340, 210, 1060, crop=0.75)
    place("tamil-nadu-marigold", 230, 500, 1000, crop=0.47)
    place("tamil-nadu-pink-lotus", 460, 680, 930)
    names, _ = d.save(TILES, DECKS)
    print(names, d.pptx_name())


if __name__ == "__main__":
    main()
