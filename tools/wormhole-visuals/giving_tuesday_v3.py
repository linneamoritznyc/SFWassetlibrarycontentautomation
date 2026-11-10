"""GivingTuesday 2026 from zero (Linnea's brief, 10 Nov). Trifold style: flat full-colour boxes with hard edges over
real photos; no gradients, fades, shadows, pills, gold, italics or leaf background; no "Link in bio".
A code-drawn compost thermometer (dial and needle separate, needle rotates around the dial centre in Canva) and one
cream mycelium thread that runs across all 7 carousel slides and ends in a mushroom on slide 7. No AI images.

  python3 tools/wormhole-visuals/giving_tuesday_v3.py
    -> decks/01-12-2026-giving-tuesday-carousel.pptx, decks/01-12-2026-giving-tuesday-stories.pptx
"""
import math
import os
import random
import shutil

from PIL import Image, ImageDraw, ImageFont, ImageOps

import collage
from bundle_three_styles_v12 import T, height
from collage import Deck, cover
from nov_fill import DECKS, TILES

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

W = 1080
GREEN, BROWN, CREAM, BLUE, INK = "#156826", "#4F3433", "#F4F1EA", "#3780B8", "#333130"
STEEL = "#B9B7AF"
FONT = "/home/user/fonts/Montserrat-Bold.ttf"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
GIV = "/home/user/sfwlib/social/giving"
IND = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/india/raw"
NEW = "/home/user/photos/new-2026-10"
A0, A1 = 225, -45


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def put(d, k, name, im, x, y):
    d.put(k, name, im, round(x), round(y), shadowed=False, anchor="tl")


def box(d, k, name, x, y, w, h, color):
    put(d, k, name, Image.new("RGBA", (round(w), round(h)), hexrgb(color) + (255,)), x, y)


def photo(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


# ---------------- the thermometer ----------------
def ang(f):
    return math.radians(A0 + (A1 - A0) * f)


def dial(D):
    k = 3
    S = D * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = S / 2
    dr.ellipse((0, 0, S - 1, S - 1), fill=hexrgb(BROWN) + (255,))                     # soil brown rim
    rim = S * 0.055
    dr.ellipse((rim, rim, S - rim, S - rim), fill=hexrgb(CREAM) + (255,))           # cream face
    f_lab = ImageFont.truetype(FONT, int(S * 0.062))
    for i in range(0, 21):
        f = i / 20
        a = ang(f)
        r1 = c - rim - S * 0.035
        r0 = r1 - (S * 0.07 if i % 5 == 0 else S * 0.035)
        dr.line((c + r0 * math.cos(a), c - r0 * math.sin(a), c + r1 * math.cos(a), c - r1 * math.sin(a)),
                fill=hexrgb(BROWN) + (255,), width=int(S * (0.012 if i % 5 == 0 else 0.006)))
        if i % 5 == 0:
            lab = "$0" if i == 0 else ("$100k" if i == 20 else f"${i * 5}k")
            rl = r0 - S * 0.1
            if i in (0, 20):   # nudge the end labels off the needle's rest positions
                a = ang(f + (0.06 if i == 0 else -0.06))
            tw = dr.textlength(lab, font=f_lab)
            dr.text((c + rl * math.cos(a) - tw / 2, c - rl * math.sin(a) - S * 0.035), lab, font=f_lab,
                    fill=hexrgb(INK) + (255,))
    return im.resize((D, D), Image.LANCZOS)


def needle(D, f):
    k = 3
    S = D * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = S / 2
    a = ang(f)
    L = S * 0.36
    w = S * 0.022
    tip = (c + L * math.cos(a), c - L * math.sin(a))
    tail = (c - S * 0.07 * math.cos(a), c + S * 0.07 * math.sin(a))
    p1 = (c + w * math.cos(a + math.pi / 2), c - w * math.sin(a + math.pi / 2))
    p2 = (c + w * math.cos(a - math.pi / 2), c - w * math.sin(a - math.pi / 2))
    dr.polygon([tip, p1, tail, p2], fill=hexrgb(GREEN) + (255,))
    r = S * 0.045
    dr.ellipse((c - r, c - r, c + r, c + r), fill=hexrgb(GREEN) + (255,))
    return im.resize((D, D), Image.LANCZOS)


def stem(length, w=26):
    k = 4
    im = Image.new("RGBA", (w * k, length * k), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon([(0, 0), (w * k, 0), (w * k, (length - 36) * k), (w * k / 2, length * k),
                                (0, (length - 36) * k)], fill=hexrgb(STEEL) + (255,))
    return im.resize((w, length), Image.LANCZOS)


def thermometer(d, k, cx, top, D, f, stem_len):
    st = stem(stem_len, max(18, round(D * 0.045)))
    put(d, k, "Thermometer stem", st, cx - st.width / 2, top + D - D * 0.04)
    put(d, k, "Thermometer", dial(D), cx - D / 2, top)
    put(d, k, "Needle", needle(D, f), cx - D / 2, top)


# ---------------- the mycelium thread ----------------
def mycelium(n, H, pts, seed=7):
    """One hand-drawn cream thread across n slides: a wobbly main line through the waypoints, with short side
    branches, ending in a small mushroom. Returns one RGBA image per slide."""
    k = 2
    WW = W * n
    im = Image.new("RGBA", (WW * k, H * k), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    rnd = random.Random(seed)
    col = hexrgb(CREAM) + (255,)
    line = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        steps = max(8, int(abs(x1 - x0) / 12))
        for s in range(steps):
            t = s / steps
            tt = t * t * (3 - 2 * t)
            line.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * tt + rnd.uniform(-2.5, 2.5)))
    line.append(pts[-1])
    dr.line([(x * k, y * k) for x, y in line], fill=col, width=5 * k, joint="curve")

    def branch(x, y, a, length, width, depth):
        pts_ = [(x, y)]
        for _ in range(int(length / 10)):
            a += rnd.uniform(-0.35, 0.35)
            x += 10 * math.cos(a)
            y += 10 * math.sin(a)
            pts_.append((x, y))
        dr.line([(px * k, py * k) for px, py in pts_], fill=col, width=max(1, int(width * k)), joint="curve")
        if depth and rnd.random() < 0.8:
            i = rnd.randrange(1, len(pts_))
            branch(*pts_[i], a + rnd.choice((-1, 1)) * rnd.uniform(0.5, 1.0), length * 0.55, width * 0.7, depth - 1)

    for i in range(20, len(line) - 30, 22):
        x, y = line[i]
        if x > WW - 260:
            break
        a = rnd.choice((-1, 1)) * rnd.uniform(0.6, 1.4) + (0 if rnd.random() < 0.5 else math.pi)
        branch(x, y, a, rnd.uniform(40, 110), 2.6, 2)
    # mushroom at the end: stem rising from the thread, a rounded cap
    ex, ey = pts[-1]
    dr.rectangle(((ex - 9) * k, (ey - 62) * k, (ex + 9) * k, ey * k), fill=col)
    dr.pieslice(((ex - 52) * k, (ey - 104) * k, (ex + 52) * k, (ey - 24) * k), 180, 360, fill=col)
    big = im.resize((WW, H), Image.LANCZOS)
    return [big.crop((i * W, 0, (i + 1) * W, H)) for i in range(n)]


# ---------------- carousel ----------------
def carousel():
    H = 1350
    d = Deck("x20261201", 7, "giving-tuesday-carousel-v28", "2026-12-01")
    # 1. cover: the thermometer pushed into the compost
    d.bg(0, cover(photo(f"{GIV}/compost-r5a-4028.jpg"), W, H, 0.5, 0.6).convert("RGBA"), name="Photo")
    thermometer(d, 0, 650, 110, 520, 0.0, 420)
    box(d, 0, "Green box", 0, 1000, 760, 350, GREEN)
    T(d, 0, "Headline", "$100,000 for\nliving soil", 70, 1040, 640, 190, 86, color=CREAM, align="left", lh=1.0)
    T(d, 0, "Details", "Giving Tuesday · 1 December", 70, 1240, 660, 64, 50, bold=False, color=CREAM,
      align="left")
    # 2. the farmer in India, cream box in the bottom-right corner
    d.bg(1, cover(photo(f"{IND}/40c702d3-e6e9-4387-b187-2a1798fef626.jpg"), W, H, 0.42, 0.35).convert("RGBA"),
         name="Photo")
    box(d, 1, "Cream box", 290, 930, 790, 420, CREAM)
    T(d, 1, "Headline", "Healing soil.\nFeeding humanity.\nRestoring the\nliving world.", 340, 965, 720, 340, 66,
      color=INK, align="left", lh=1.06)
    # 3. the class at live microscopy, brown box bottom left
    d.bg(2, cover(photo(f"{GIV}/class-live-microscopy-cr-oct2025.jpg"), W, H, 0.6, 0.5).convert("RGBA"),
         name="Photo")
    box(d, 2, "Brown box", 0, 880, 860, 470, BROWN)
    T(d, 2, "Headline", "We teach farmers, agronomists and consultants to bring their soil back to life.", 70, 920,
      740, 400, 66, color=CREAM, align="left", lh=1.06)
    # 4 and 5. full-bleed, no text
    d.bg(3, cover(photo(f"{GIV}/extraction-demo-cr-mar2025.jpg"), W, H, 0.5, 0.5).convert("RGBA"), name="Photo")
    d.bg(4, cover(photo(f"{NEW}/students-laughing-at-compost-cage.jpg"), W, H, 0.62, 0.4).convert("RGBA"),
         name="Photo")
    # 6. aerial farm, small green band
    d.bg(5, cover(photo(f"{IND}/17c01e4d-cbfa-4f9c-8058-9e225aa30c5f.jpg"), W, H, 0.5, 0.5).convert("RGBA"),
         name="Photo")
    box(d, 5, "Green box", 0, 1100, W, 170, GREEN)
    T(d, 5, "Details", "Costa Rica · New Mexico · England\nCyprus · India", 72, 1118, 936, 140, 50,
      bold=False, color=CREAM, lh=1.15)
    # 7. pink tree top 55% (photo space until the file arrives), green box below
    tree = os.environ.get("PINK_TREE", f"{GIV}/pink-tree-cr-mar2025.jpg")
    TOP = 740
    if os.path.exists(tree):
        put(d, 6, "Photo", cover(photo(tree), W, TOP, 0.5, 0.45).convert("RGBA"), 0, 0)
    else:
        box(d, 6, "Photo space: pink tree in bloom, Costa Rica Mar 2025 (800DA1A4)", 0, 0, W, TOP, BLUE)
        T(d, 6, "Photo space label", "PHOTO: pink tree in bloom\n(800DA1A4, Costa Rica 2025)", 72, 300, 936, 140, 50,
          bold=False, color=CREAM, lh=1.15)
    box(d, 6, "Green box", 0, TOP, W, H - TOP, GREEN)
    thermometer(d, 6, 190, 790, 250, 0.0, 120)
    T(d, 6, "Headline", "Be the mycelium you want to see in the world.", 360, 790, 660, 240, 66, color=CREAM,
      align="left", lh=1.06)
    T(d, 6, "Details", "$100,000 for scholarships, educational resources and research. Donate today.", 360, 1040,
      660, 200, 50, bold=False, color=CREAM, align="left", lh=1.18)
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((120, round(lg.height * 120 / lg.width)), Image.LANCZOS)
    put(d, 6, "SFW logo", lg, 130, H - 40 - lg.height)
    # the thread across all 7, over the seams, ending in a mushroom on slide 7 at the box edge
    pts = [(0, 900), (540, 880), (1080, 880), (1620, 860), (2160, 780), (2700, 760), (3200, 900), (3500, 1220),
           (3780, 1235), (4320, 1220), (4860, 1200), (5250, 1000), (5940, 990), (6480, 760), (6900, 720), (7380, TOP)]
    for k, piece in enumerate(mycelium(7, H, pts)):
        put(d, k, "Mycelium line", piece, 0, 0)
    return d


# ---------------- stories ----------------
def stories():
    collage.H = 1920
    try:
        H = 1920
        d = Deck("st20261201give", 5, "giving-tuesday-stories-v6", "2026-12-01")
        shots = [(f"{NEW}/students-high-five-at-compost.jpg", 0.5, 0.35),
                 (f"{NEW}/students-laughing-together.jpg", 0.5, 0.4),
                 (f"{NEW}/workshop-july-2024-compost-cage-team.jpg", 0.5, 0.3),
                 (f"{NEW}/card-students-building-compost-pile.jpg", 0.45, 0.4),
                 (f"{NEW}/workshop-group-around-compost-pile.jpg", 0.5, 0.5)]
        lines = ["$10,000 raised.\nHelp us reach $100,000.", "$25,000 raised.\nHelp us reach $100,000.",
                 "$50,000 raised.\nHelp us reach $100,000.", "$75,000 raised.\nHelp us reach $100,000.",
                 "We did it.\nThank you."]
        fr = [0.1, 0.25, 0.5, 0.75, 1.0]
        TOP = 864
        for k in range(5):
            d.bg(k, Image.new("RGBA", (W, H), hexrgb(GREEN) + (255,)), name="Green box")
            p, fx, fy = shots[k]
            put(d, k, "Photo", cover(photo(p), W, TOP, fx, fy).convert("RGBA"), 0, 0)
            thermometer(d, k, W // 2, 800, 560, fr[k], 120)
            T(d, k, "Headline", lines[k], 72, 1500, 936, 170, 70, color=CREAM, lh=1.08)
        return d
    finally:
        collage.H = 1350


if __name__ == "__main__":
    for build, final in ((carousel, "01-12-2026-giving-tuesday-carousel.pptx"),
                         (stories, "01-12-2026-giving-tuesday-stories.pptx")):
        d = build()
        if build is stories:
            collage.H = 1920
        try:
            names, _ = d.save(TILES, DECKS)
        finally:
            collage.H = 1350
        src = os.path.join(DECKS, d.pptx_name())
        shutil.move(src, os.path.join(DECKS, final))
        print(names, final)
