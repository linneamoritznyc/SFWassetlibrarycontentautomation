"""Suzanne Shea / Farmer Veteran Coalition, v12: media-company quality, not a news layout (Linnea, 10 Nov).
Full-bleed graded photo; the lower part melts into a frosted, green-tinted blur of the same photo (smooth eased mask);
big cream Montserrat headline with a short mint accent line; small Source Sans line. White logo.

  python3 tools/wormhole-visuals/suzanne_frost.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from bundle_three_styles_v12 import T, height
from collage import Deck, cover
from nov_fill import DECKS, TILES

W, H = 1080, 1350
CREAM, MINT = "#F4F1EA", "#A8D5B0"
V = "/home/user/sfwlib/social/veterans"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"


def grade(im):
    im = ImageEnhance.Color(im).enhance(0.86)
    a = np.asarray(im).astype(np.float32) * np.array([1.03, 1.0, 0.95]) + np.array([4, 3, 0])
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


def frosted(path, fx, fy, start, end=None):
    """Sharp photo on top; below `start` it eases into a blurred, deep-green-tinted copy (frosted glass)."""
    end = end or min(1.0, start + 0.28)
    sharp = grade(cover(ImageOps.exif_transpose(Image.open(path)).convert("RGB"), W, H, fx, fy))
    blur = np.asarray(sharp.filter(ImageFilter.GaussianBlur(34))).astype(np.float32)
    deep = np.array([18, 46, 26], np.float32)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    tint = 0.55 + 0.25 * np.clip((yy - start) / (1 - start), 0, 1)
    frost = blur * (1 - tint) + deep * tint
    t = np.clip((yy - start) / (end - start), 0, 1)
    t = t * t * (3 - 2 * t)
    out = np.asarray(sharp).astype(np.float32) * (1 - t) + frost * t
    return Image.fromarray(out.clip(0, 255).astype("uint8")).convert("RGBA")


def accent(d, k, x, y, w=90):
    c = tuple(int(MINT[i:i + 2], 16) for i in (1, 3, 5))
    d.put(k, "Accent line", Image.new("RGBA", (w, 6), c + (255,)), x, y, shadowed=False, anchor="tl")


def logo(d, k, w=110):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 70 - w, H - 60 - lg.height, shadowed=False, anchor="tl")


def text_block(d, k, kicker, head, line, bottom=1250, hs=80):
    hh = height(head, hs, 900, lh=1.04)
    lh = height(line, 48, 760, bold=False, lh=1.22) if line else 0
    y = bottom - round(lh) - (24 if line else 0) - round(hh) - 30 - 52
    T(d, k, "Kicker", kicker, 80, y, 900, 56, 42, bold=False, color=MINT, align="left", mn=42)
    accent(d, k, 80, y + 52)
    y = T(d, k, "Headline", head, 80, y + 82, 900, hh + 8, hs, color=CREAM, align="left", lh=1.04)
    if line:
        T(d, k, "Details", line, 80, round(y) + 24, 760, lh + 8, 48, bold=False, color=CREAM, align="left", lh=1.22,
          mn=42)


import math
from PIL import ImageDraw, ImageFont

BOLD = "/home/user/fonts/Montserrat-Bold.ttf"


def furrow_grid(start_y, horizon_y, seed=0):
    """An endless field: crop rows running to a vanishing point plus cross lines that bunch up toward the horizon.
    Thin mint lines, fading out toward the horizon."""
    k = 2
    im = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    vx, vy = W / 2 * k, horizon_y * k
    col = (168, 213, 176)
    for i in range(-14, 15):                      # rows
        x_bottom = (W / 2 + i * 120) * k
        steps = 40
        for s_ in range(steps):
            t0, t1 = s_ / steps, (s_ + 1) / steps
            ya, yb = H * k + (vy - H * k) * t0, H * k + (vy - H * k) * t1
            xa, xb = x_bottom + (vx - x_bottom) * t0, x_bottom + (vx - x_bottom) * t1
            if yb < start_y * k:
                continue
            alpha = int(80 * (1 - t0) ** 1.2)
            dr.line((xa, ya, xb, yb), fill=col + (alpha,), width=2 * k)
    for j in range(1, 16):                        # cross lines, closer together near the horizon
        t = 1 - (1 / (1 + j * 0.45))
        y = H * k + (vy - H * k) * t
        if y < start_y * k:
            continue
        dr.line((0, y, W * k, y), fill=col + (int(70 * (1 - t)),), width=2 * k)
    return im.resize((W, H), Image.LANCZOS)


def badge(text, D=230, fill=(244, 241, 234), ink=(21, 104, 38)):
    """A round stamp: cream disc, text running round the edge, a small sprout drawn in the middle."""
    k = 3
    S = D * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.ellipse((0, 0, S - 1, S - 1), fill=fill + (255,))
    dr.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), outline=ink + (255,), width=int(S * 0.012))
    dr.ellipse((S * 0.27, S * 0.27, S * 0.73, S * 0.73), outline=ink + (255,), width=int(S * 0.01))
    f = ImageFont.truetype(BOLD, int(S * 0.085))
    text = text.upper() + "  \u2022  "
    total = sum(dr.textlength(ch, font=f) for ch in text)
    r = S * 0.37
    circ = 2 * math.pi * r
    scale = circ / total
    a = -math.pi / 2
    for ch in text:
        cw = dr.textlength(ch, font=f) * scale
        a_mid = a + (cw / 2) / r
        g = Image.new("RGBA", (int(S * 0.12), int(S * 0.12)), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((g.width / 2, g.height / 2), ch, font=f, fill=ink + (255,), anchor="mm")
        g = g.rotate(-math.degrees(a_mid) - 90, resample=Image.BICUBIC)
        im.alpha_composite(g, (int(S / 2 + r * math.cos(a_mid) - g.width / 2), int(S / 2 + r * math.sin(a_mid) - g.height / 2)))
        a += cw / r
    c = S / 2                                   # sprout: a stem and two leaves
    w_ = int(S * 0.018)
    dr.line((c, c + S * 0.13, c, c - S * 0.06), fill=ink + (255,), width=w_)
    dr.chord((c - S * 0.13, c - S * 0.12, c + S * 0.01, c + S * 0.02), 180, 360, fill=ink + (255,))
    dr.chord((c - S * 0.01, c - S * 0.16, c + S * 0.13, c - S * 0.02), 180, 360, fill=ink + (255,))
    dr.line((c - S * 0.12, c + S * 0.13, c + S * 0.12, c + S * 0.13), fill=ink + (255,), width=w_)
    return im.resize((D, D), Image.LANCZOS)


FIELD = "/home/user/photos/new-2026-10/card-field-walk-crop-rows.jpg"


def wheat(rnd, h):
    """One code-drawn wheat stalk: a gently curved stem and an ear of paired grains."""
    k = 3
    w = 70
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    lean = rnd.uniform(-14, 14)
    col = (60, 52, 30, 255)
    pts = [(w / 2 + lean * (1 - t) ** 2, h * t) for t in [i / 30 for i in range(31)]]
    dr.line([(x * k, (h - y) * k) for x, y in pts], fill=col, width=3 * k)
    tx, ty = pts[-1][0], h - pts[-1][1]
    ear = int(h * 0.22)
    for i in range(9):
        yy = ty + 4 + i * ear / 9
        for side in (-1, 1):
            cx = tx + side * 7
            dr.ellipse(((cx - 6) * k, (yy - 9) * k, (cx + 6) * k, (yy + 9) * k), fill=col)
        dr.line(((tx) * k, (yy - 4) * k, (tx + side * 22) * k, (yy - 30) * k), fill=col, width=1 * k)
    return im.resize((w, h), Image.LANCZOS)


def field_bg(fx, seed):
    """Code-drawn harvest scene: warm golden sky, a deep green field of rows running to the horizon, and a band of
    wheat stalks silhouetted along the horizon. No photo, so no stray faces."""
    import random
    hz = int(H * 0.47)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    sky_top, sky_low = np.array([238, 214, 160], np.float32), np.array([246, 232, 196], np.float32)
    fld_top, fld_bot = np.array([58, 92, 52], np.float32), np.array([16, 38, 22], np.float32)
    t_s = np.clip(yy / (hz / H), 0, 1)
    t_f = np.clip((yy - hz / H) / (1 - hz / H), 0, 1)
    sky = sky_top * (1 - t_s) + sky_low * t_s
    fld = fld_top * (1 - t_f) + fld_bot * t_f
    a = np.where(yy < hz / H, sky, fld) * np.ones((H, W, 1), np.float32)
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    r = np.sqrt((xx - 0.5) ** 2 + ((yy - hz / H) * 1.6) ** 2)
    a += (np.clip(1 - r / 0.5, 0, 1) ** 2 * 30) * (yy < hz / H)          # low sun glow on the horizon
    a += np.random.default_rng(seed).normal(0, 2.2, (H, W, 1)).astype(np.float32)
    im = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    im.alpha_composite(furrow_grid(hz + 6, hz))
    return im


def card(path, w, h, fx, fy, border=10, r=34):
    ph = grade(cover(ImageOps.exif_transpose(Image.open(path)).convert("RGB"), w, h, fx, fy)).convert("RGBA")
    k = 3
    out = Image.new("RGBA", ((w + 2 * border) * k, (h + 2 * border) * k), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle((0, 0, out.width - 1, out.height - 1), (r + border) * k,
                                          fill=(244, 241, 234, 255))
    out = out.resize((w + 2 * border, h + 2 * border), Image.LANCZOS)
    m = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * k - 1, h * k - 1), r * k, fill=255)
    ph.putalpha(m.resize((w, h), Image.LANCZOS))
    out.alpha_composite(ph, (border, border))
    return out


def slide(d, k, path, fx, fy, cw, ch, cx, kicker, head, line, stamp, bx, by):
    d.bg(k, field_bg(0.3 + 0.2 * k, 920 + k), name="Background: crop-row field, harvest gold")
    c = card(path, cw, ch, fx, fy)
    d.put(k, "Photo card", c, cx, 80, shadowed=False, anchor="tl")
    b = badge(stamp, 220)
    d.put(k, "Badge", b, bx, by, shadowed=False, anchor="tl")
    text_block(d, k, kicker, head, line)
    logo(d, k)


def build(v):
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    slide(d, 0, f"{V}/suzanne-hoop-house.jpg", 0.62, 0.3, 820, 700, 70, "Farmer Veteran Coalition",
          "Veteran farmers\nbuilding living soil", "With Soil Food Web Consultant\nSuzanne Shea",
          "Soil Food Web Consultant", 790, 640)
    slide(d, 1, f"{V}/suzanne-fvc-conference.jpg", 0.45, 0.55, 760, 680, 230, "Stakeholders Conference",
          "\u201cScaling Sustainably\u201d", "Suzanne Shea\u2019s talk at the\nFarmer Veteran Coalition",
          "Farmer Veteran Coalition", 80, 610)
    slide(d, 2, f"{V}/suzanne-conference-walk.jpg", 0.2, 0.45, 900, 760, 80, "Soil Food Web Consultants",
          "Find one\nnear you", None, "Living soil, local hands", 790, 700)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
