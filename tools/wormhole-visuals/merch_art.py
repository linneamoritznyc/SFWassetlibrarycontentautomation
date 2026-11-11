"""SFW merch artwork, drawn in code (no AI images, no stock): print-ready transparent PNGs at 3000 px plus a preview
of each on its garment colour.

  1. mycelium-bloom  - a radial mycelium network fading from mint to cream, line from the team culture deck
  2. soil-horizon    - a sunrise fade over sprouts, roots and hyphae reaching down into the soil, the brand tagline
  3. look-closer     - a microscope field of view: hyphae, bacteria, a nematode and a protozoan in a soft vignette

  python3 tools/wormhole-visuals/merch_art.py <outdir>
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = "/home/user/fonts"
ARCH = "/home/user/fonts/dl/arch"
FELL, FELLI, FELLSC, TYPE = (f"{ARCH}/IMFeENrm28P.ttf", f"{ARCH}/IMFeENit28P.ttf", f"{ARCH}/IMFeENsc28P.ttf",
                             f"{ARCH}/CourierPrime-Regular.ttf")
GREEN = (21, 104, 38)
DEEP = (12, 52, 24)
MINT = (169, 211, 178)
LEAF = (89, 166, 108)
CREAM = (244, 241, 234)
SAND = (216, 195, 165)
BROWN = (79, 52, 51)
S = 3000          # print size
K = 2             # supersample


def font(name, size):
    return ImageFont.truetype(name if name.startswith('/') else os.path.join(FONTS, name), size)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


# ---------------------------------------------------------------- growth
def grow(seeds, rng, steps=420, step=7.0, branch=0.035, wander=0.16, pull=None, limit=None, maxw=7.0, die=0.0):
    """Hyphae / roots: tips walk with a little wander, branch now and then, and get thinner each generation.
    Returns segments (x0, y0, x1, y1, width, generation, distance-travelled)."""
    tips = [dict(x=x, y=y, a=a, w=maxw, g=0, d=0.0) for x, y, a in seeds]
    segs = []
    for _ in range(steps):
        new = []
        for t in tips:
            a = t["a"] + rng.gauss(0, wander)
            if pull:
                a = pull(t, a)
            x1, y1 = t["x"] + math.cos(a) * step, t["y"] + math.sin(a) * step
            if limit and not limit(x1, y1):
                continue
            if die and rng.random() < die * (1 + t['g'] * 0.6):
                continue
            segs.append((t["x"], t["y"], x1, y1, t["w"], t["g"], t["d"]))
            t.update(x=x1, y=y1, a=a, w=max(1.2, t["w"] * 0.996), d=t["d"] + step)
            new.append(t)
            if rng.random() < branch and t["w"] > 1.6:
                new.append(dict(x=x1, y=y1, a=a + rng.choice((-1, 1)) * rng.uniform(0.45, 0.95),
                                w=t["w"] * 0.72, g=t["g"] + 1, d=t["d"]))
        tips = new[:900]
        if not tips:
            break
    return segs


def stroke(dr, segs, colour, k=K, alpha=None):
    for x0, y0, x1, y1, w, g, d in segs:
        c = colour(x0, y0, w, g, d)
        dr.line((x0 * k, y0 * k, x1 * k, y1 * k), fill=c, width=max(1, round(w * k)))
        dr.ellipse((x1 * k - w * k / 2, y1 * k - w * k / 2, x1 * k + w * k / 2, y1 * k + w * k / 2), fill=c)


def canvas(n=S):
    im = Image.new("RGBA", (n * K, n * K), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def down(im, n=S):
    return im.resize((n, n), Image.LANCZOS)


def text_c(dr, cx, y, s, f, fill, k=K, track=0):
    if track:
        ws = [dr.textlength(ch, font=f) for ch in s]
        tw = sum(ws) + track * k * (len(s) - 1)
        x = cx * k - tw / 2
        for ch, w in zip(s, ws):
            dr.text((x, y * k), ch, font=f, fill=fill)
            x += w + track * k
        return
    tw = dr.textlength(s, font=f)
    dr.text((cx * k - tw / 2, y * k), s, font=f, fill=fill)


# ---------------------------------------------------------------- vector botanicals
def leaf(dr, bx, by, ang, ln, wd, fill, vein=None, k=K):
    """Pointed leaf from two curves, base at (bx, by) pointing along ang."""
    pts_l, pts_r = [], []
    for i in range(41):
        t = i / 40
        half = math.sin(math.pi * t) ** 0.85 * wd * (1 - 0.35 * t)
        px, py = t * ln, half
        for side, arr in ((1, pts_l), (-1, pts_r)):
            x = bx + px * math.cos(ang) - side * py * math.sin(ang)
            y = by + px * math.sin(ang) + side * py * math.cos(ang)
            arr.append((x * k, y * k))
    dr.polygon(pts_l + pts_r[::-1], fill=fill)
    if vein:
        ex, ey = bx + ln * 0.92 * math.cos(ang), by + ln * 0.92 * math.sin(ang)
        dr.line((bx * k, by * k, ex * k, ey * k), fill=vein, width=max(1, round(2.2 * k)))


def stem(dr, pts, w, fill, k=K):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dr.line((x0 * k, y0 * k, x1 * k, y1 * k), fill=fill, width=round(w * k))
        dr.ellipse((x1 * k - w * k / 2, y1 * k - w * k / 2, x1 * k + w * k / 2, y1 * k + w * k / 2), fill=fill)


def curve(x0, y0, x1, y1, bend, n=40):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1,
             (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1) for t in (i / n for i in range(n + 1))]


def flower(dr, cx, cy, r, petals, fill, centre, rot=0.0, k=K):
    for i in range(petals):
        a = rot + 2 * math.pi * i / petals
        leaf(dr, cx, cy, a, r, r * 0.42, fill)
    dr.ellipse(((cx - r * 0.22) * k, (cy - r * 0.22) * k, (cx + r * 0.22) * k, (cy + r * 0.22) * k), fill=centre)


# ---------------------------------------------------------------- 1. mycelium bloom
def mycelium_bloom():
    rng = random.Random(7)
    im, dr = canvas()
    cx, cy, R = S / 2, S * 0.43, S * 0.42
    ph = [rng.uniform(0, 6.28) for _ in range(3)]

    def edge(a):  # uneven, organic outline instead of a fade
        return 0.86 + 0.07 * math.sin(3 * a + ph[0]) + 0.05 * math.sin(5 * a + ph[1]) + 0.03 * math.sin(9 * a + ph[2])

    seeds = [(cx + rng.uniform(-30, 30), cy + rng.uniform(-30, 30), 2 * math.pi * i / 24 + rng.uniform(-.1, .1))
             for i in range(24)]

    def pull(t, a):  # keep heading outward
        out = math.atan2(t["y"] - cy, t["x"] - cx)
        return a + 0.06 * math.sin(out - a)

    segs = grow(seeds, rng, steps=175, step=7, branch=0.04, wander=0.22, pull=pull,
                limit=lambda x, y: math.hypot(x - cx, y - cy) < R * 1.3, maxw=8, die=0.0025)

    def col(x, y, w, g, d):
        t = min(1, math.hypot(x - cx, y - cy) / R)
        c = lerp(MINT, CREAM, t ** 0.8)
        return c + (255,)

    stroke(dr, sorted(segs, key=lambda s: -s[4]), col)
    # spores glowing at the tips
    for x0, y0, x1, y1, w, g, d in segs[-1200::3]:
        t = math.hypot(x1 - cx, y1 - cy) / R
        if t > 0.55:
            r = rng.uniform(3, 7)
            dr.ellipse(((x1 - r) * K, (y1 - r) * K, (x1 + r) * K, (y1 + r) * K), fill=CREAM + (255,))
    glow = im.filter(ImageFilter.GaussianBlur(10 * K))
    glow.putalpha(glow.getchannel('A').point(lambda v: v // 3))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(glow)
    base.alpha_composite(im)
    dr = ImageDraw.Draw(base)
    f1 = font(FELLI, 270 * K)
    text_c(dr, S / 2, S * 0.81, "Be the mycelium", f1, CREAM + (255,))
    f2 = font(FELLSC, 120 * K)
    text_c(dr, S / 2, S * 0.81 + 310, "you want to see in the world", f2, MINT + (255,), track=8)
    f3 = font(TYPE, 58 * K)
    text_c(dr, S / 2, S * 0.81 + 520, "FIG. 1 \u2014 FUNGAL HYPHAE", f3, MINT + (255,), track=10)
    return down(base)


# ---------------------------------------------------------------- 2. soil horizon
def soil_horizon():
    rng = random.Random(3)
    cx, R = S / 2, S * 0.33
    hy = S * 0.40                      # horizon
    # sunrise disc: cream to sand to soft green, fading at its edge
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    d = np.hypot(xx - cx, yy - hy)
    disc = np.clip(1 - (d - R * 0.96) / (R * 0.04), 0, 1)
    up = np.clip((hy - yy) / R, 0, 1)
    sky = np.stack([np.interp(up, [0, 0.45, 1], [a, b, c]) for a, b, c in zip(SAND, (232, 220, 196), CREAM)], -1)
    below = np.clip((yy - hy) / R, 0, 1)
    soil = np.stack([np.interp(below, [0, 1], [a, b]) for a, b in zip(BROWN, (38, 26, 24))], -1)
    rgb = np.where((yy < hy)[..., None], sky, soil)
    a = disc * np.where(yy < hy, 1.0, np.clip(1 - below ** 1.6 * 0.9, 0, 1))
    art = Image.fromarray(np.dstack([rgb, a * 255]).astype("uint8"), "RGBA").resize((S * K, S * K), Image.LANCZOS)
    dr = ImageDraw.Draw(art)
    m = Image.new("L", art.size, 0)
    ImageDraw.Draw(m).ellipse(((cx - R) * K, (hy - R) * K, (cx + R) * K, (hy + R) * K), fill=255)

    # roots and hyphae under the horizon
    layer, ldr = canvas()
    for px in np.linspace(cx - R * 0.62, cx + R * 0.62, 7):
        seeds = [(px, hy + 4, math.pi / 2 + rng.uniform(-.2, .2))]
        segs = grow(seeds, rng, steps=150, step=6, branch=0.035, wander=0.22,
                    pull=lambda t, a: a + 0.05 * math.sin(math.pi / 2 - a),
                    limit=lambda x, y: math.hypot(x - cx, y - hy) < R * 0.97 and y > hy, maxw=8)
        stroke(ldr, segs, lambda x, y, w, g, d: CREAM + (round(235 * max(0, 1 - (y - hy) / (R * 0.8)) ** 1.5),))
    hy_segs = grow([(rng.uniform(cx - R * .7, cx + R * .7), rng.uniform(hy + 80, hy + R * .7), rng.uniform(0, 6.28))
                    for _ in range(14)], rng, steps=80, step=5, branch=0.04, wander=0.35,
                   limit=lambda x, y: math.hypot(x - cx, y - hy) < R * 0.95 and y > hy + 10, maxw=2.4)
    stroke(ldr, hy_segs, lambda x, y, w, g, d: MINT + (round(200 * max(0, 1 - (y - hy) / (R * 0.95))),))

    # sprouts and small plants on the horizon
    for i, px in enumerate(np.linspace(cx - R * 0.62, cx + R * 0.62, 7)):
        h = [190, 280, 360, 440, 340, 260, 180][i] * rng.uniform(0.9, 1.1)
        top = (px + rng.uniform(-40, 40), hy - h)
        pts = curve(px, hy, top[0], top[1], rng.uniform(-60, 60))
        stem(ldr, pts, 9, GREEN + (255,))
        for j, t in enumerate((0.35, 0.55, 0.75)):
            x, y = pts[int(t * 40)]
            side = 1 if j % 2 else -1
            leaf(ldr, x, y, -math.pi / 2 + side * 0.95, h * 0.33, h * 0.11, LEAF + (255,), vein=GREEN + (255,))
        if i in (1, 3, 5):
            flower(ldr, top[0], top[1], h * 0.16, 7 if i != 3 else 9, CREAM + (255,), (201, 162, 39, 255) if False
                   else SAND + (255,), rot=rng.uniform(0, 1))
        else:
            leaf(ldr, top[0], top[1], -math.pi / 2 - 0.5, h * 0.25, h * 0.09, LEAF + (255,), vein=GREEN + (255,))
            leaf(ldr, top[0], top[1], -math.pi / 2 + 0.5, h * 0.25, h * 0.09, LEAF + (255,), vein=GREEN + (255,))
    ldr.line(((cx - R) * K, hy * K, (cx + R) * K, hy * K), fill=CREAM + (200,), width=4 * K)
    la = np.asarray(layer).copy()
    la[..., 3] = (la[..., 3].astype(np.float32) * (np.asarray(m) / 255)).astype("uint8")
    art.alpha_composite(Image.fromarray(la))
    dr = ImageDraw.Draw(art)
    f1 = font(FELLSC, 190 * K)
    f2 = font(FELLI, 160 * K)
    y0 = hy + R + 110
    text_c(dr, cx, y0, "healing soil", f1, CREAM + (255,), track=14)
    text_c(dr, cx, y0 + 210, "Feeding Humanity.", f2, MINT + (255,))
    text_c(dr, cx, y0 + 390, "Restoring the Living World.", f2, MINT + (255,))
    return down(art)


# ---------------------------------------------------------------- 3. look closer
def look_closer():
    rng = random.Random(11)
    cx, cy, R = S / 2, S * 0.38, S * 0.34
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy) / R
    light = np.clip(1 - d ** 3, 0, 1)                         # bright field, vignette to the rim
    rgb = np.stack([np.interp(light, [0, 1], [a, b]) for a, b in zip(DEEP, (236, 240, 222))], -1)
    a = np.clip((1.0 - d) / 0.012, 0, 1)
    art = Image.fromarray(np.dstack([rgb, a * 255]).astype("uint8"), "RGBA").resize((S * K, S * K), Image.LANCZOS)
    layer, dr = canvas()
    inside = lambda x, y: math.hypot(x - cx, y - cy) < R * 0.97
    # fungal hyphae
    segs = grow([(cx - R, cy + rng.uniform(-R * .5, R * .5), rng.uniform(-.4, .4)) for _ in range(2)] +
                [(cx + rng.uniform(-R * .3, R * .3), cy - R, math.pi / 2 + rng.uniform(-.4, .4)) for _ in range(1)],
                rng, steps=300, step=7, branch=0.018, wander=0.08, maxw=10)
    segs = [s for s in segs if inside(s[2], s[3])]
    stroke(dr, segs, lambda x, y, w, g, d: (52, 98, 60, 245))
    # bacteria: rods and cocci
    for _ in range(70):
        x, y = cx + rng.uniform(-R, R), cy + rng.uniform(-R, R)
        if not inside(x, y):
            continue
        ang, ln = rng.uniform(0, math.pi), rng.uniform(18, 34)
        c = rng.choice([(89, 166, 108, 230), (55, 128, 184, 210), (79, 52, 51, 220)])
        if rng.random() < 0.6:
            stem(dr, [(x, y), (x + math.cos(ang) * ln, y + math.sin(ang) * ln)], 13, c)
        else:
            r = rng.uniform(6, 9)
            dr.ellipse(((x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K), fill=c)
    # nematode: tapered sine body
    pts = []
    for i in range(200):
        t = i / 199
        x = cx - R * 0.6 + t * R * 1.0
        y = cy + R * 0.5 - t * R * 0.75 + math.sin(t * 2.2 * math.pi) * 90
        pts.append((x, y))
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(pts, pts[1:])):
        t = i / 198
        w = 34 * (math.sin(math.pi * min(1, t * 1.08)) ** 0.5) + 3
        dr.line((x0 * K, y0 * K, x1 * K, y1 * K), fill=(150, 122, 96, 245), width=round(w * K))
        dr.ellipse(((x1 - w / 2) * K, (y1 - w / 2) * K, (x1 + w / 2) * K, (y1 + w / 2) * K), fill=(150, 122, 96, 245))
    for i in range(30, 170, 9):  # gut line
        x0, y0 = pts[i]
        x1, y1 = pts[i + 5]
        dr.line((x0 * K, y0 * K, x1 * K, y1 * K), fill=(110, 86, 68, 255), width=4 * K)
    # protozoan (ciliate)
    px, py, pr = cx - R * 0.35, cy - R * 0.38, 110
    dr.ellipse(((px - pr) * K, (py - pr * .7) * K, (px + pr) * K, (py + pr * .7) * K), fill=(196, 221, 200, 235),
               outline=(64, 110, 70, 255), width=5 * K)
    for i in range(46):
        a = 2 * math.pi * i / 46
        x0, y0 = px + math.cos(a) * pr, py + math.sin(a) * pr * .7
        dr.line((x0 * K, y0 * K, (x0 + math.cos(a) * 22) * K, (y0 + math.sin(a) * 16) * K), fill=(64, 110, 70, 255),
                width=3 * K)
    dr.ellipse(((px - 26) * K, (py - 20) * K, (px + 26) * K, (py + 20) * K), fill=(64, 110, 70, 255))
    la = np.asarray(layer).copy()
    m = (np.hypot(*np.mgrid[0:S * K, 0:S * K][::-1] - np.array([cx * K, cy * K])[:, None, None]) < R * K * 0.985)
    la[..., 3] = (la[..., 3] * m).astype("uint8")
    art.alpha_composite(Image.fromarray(la))
    dr = ImageDraw.Draw(art)
    dr.ellipse(((cx - R) * K, (cy - R) * K, (cx + R) * K, (cy + R) * K), outline=CREAM + (255,), width=10 * K)
    f1 = font(FELLI, 290 * K)
    f2 = font(TYPE, 100 * K)
    text_c(dr, cx, cy + R + 110, "Look closer.", f1, CREAM + (255,))
    text_c(dr, cx, cy + R + 450, "THERE'S LIFE", f2, MINT + (255,), track=22)
    return down(art)


def preview(art, garment, path, scale=1100):
    bg = Image.new("RGBA", (1600, 1600), garment + (255,))
    a = art.resize((scale, scale), Image.LANCZOS)
    bg.alpha_composite(a, ((1600 - scale) // 2, (1600 - scale) // 2 - 20))
    bg.convert("RGB").save(path, quality=92)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, fn, garment in (("mycelium-bloom", mycelium_bloom, DEEP), ("soil-horizon", soil_horizon, GREEN),
                              ("look-closer", look_closer, (30, 36, 30))):
        art = fn()
        art.save(f"{out}/{name}-print.png")
        preview(art, garment, f"{out}/{name}-preview.jpg")
        print(name)
