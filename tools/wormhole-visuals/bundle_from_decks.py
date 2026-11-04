"""Linnea's three bundle decks (4 Nov), rebuilt to look finished: her slide ideas and words, one grid, centred text,
dates on one line, a UTM QR code on each post's last slide (Stephanie, 4 Nov), no flat green backgrounds.

  promo-fall-bundle v8  Wed 4 Nov   4-slide carousel: badges cover, above/below ground, 01-02-03 steps, number tiles
  x20261125 v13         Wed 18 Nov  Judge it by hand. Then see the life in it. (hands drawing | micrograph eyepiece)
  x20261130 v13         Wed 25 Nov  Start today. Pick your season. (2027 year ring with the three cohorts)

Badges from Linnea's deck (scratchpad/bundleup). Micrograph: bacterial-feeding nematode (omnivore), 40x objective,
Keisha Wheeler (photo_check: unused). Line drawings from Replicate (sfwlib/social/lineart).

  python3 tools/wormhole-visuals/bundle_from_decks.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from bundle_three_styles import blueprint, grain, keep_dates, rgb, speckle
from bundle_three_styles_v12 import FOOT, FY, M, MINT, T, art_fit, footer, height, put_art
from bundle_v6 import H, W, line_art
from collage import Deck
from nov_fill import BROWN, CREAM, DECKS, INK, LGREEN, TILES

_put = Deck.put


def _put_int(self, k, name, im, x, y, **kw):
    return _put(self, k, name, im, round(x), round(y), **kw)


Deck.put = _put_int
SCR = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad"
BADGES = [f"{SCR}/bundleup/img_0_FC{i}_badge.jpg" for i in (1, 2, 3, 4)]
CIC = f"{SCR}/bundleup/img_0_CIC_badge.jpg"
MICRO = "/home/user/photos/new-2026-10/Bacterial-feeding nematode (omnivore), 40x obj, Keisha Wheeler.jpg"
SOIL, NIGHT_BLUE = "#2E211F", "#0E2233"
TAN, ICE = "#D8B48A", "#9CC9E8"


def glow_bg(base, glows, seed):
    """Flat base colour with soft coloured light pools and grain."""
    a = np.zeros((H, W, 3), np.float32) + np.array(rgb(base), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for (gx, gy, rad, col, k) in glows:
        r = np.sqrt((xx - gx) ** 2 + (yy - gy) ** 2) / rad
        a += (np.clip(1 - r, 0, 1) ** 2)[..., None] * (np.array(rgb(col), np.float32) - a) * k
    return grain(Image.fromarray(np.clip(a, 0, 255).astype("uint8")), seed, 3)


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = im.convert("RGBA")
    out.putalpha(m)
    return out


def shadowed(im, blur=18, off=10, alpha=110):
    pad = blur * 2
    sh = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2 + off), (0, 0, 0, 0))
    a = Image.new("L", sh.size, 0)
    a.paste(im.getchannel("A").point(lambda v: v * alpha // 255), (pad, pad + off))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(blur)))
    sh.alpha_composite(im, (pad, pad))
    return sh, pad


def put_shadowed(d, k, name, im, x, y):
    s, pad = shadowed(im)
    d.put(k, name, s, x - pad, y - pad, shadowed=False, anchor="tl")


def frost(w, h, r=26, a=30, line=80):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=(255, 255, 255, a),
                                         outline=(255, 255, 255, line), width=2)
    return im


# ---------------- carousel ----------------
def carousel():
    d = Deck("promo-fall-bundle", 4, "fall-enrollment-bundle-v8", "2026-11-04")
    # 1. cover: soil top, cream bottom, the four badges across the seam
    seam = 600
    bg = Image.new("RGBA", (W, H))
    bg.paste(glow_bg(SOIL, [(W / 2, 120, 700, "#6B4A3A", 0.6)], 1).crop((0, 0, W, seam)), (0, 0))
    bg.paste(grain(Image.new("RGB", (W, H - seam), CREAM), 2, 3), (0, seam))
    d.bg(0, bg, name="Background: soil | cream")
    y = T(d, 0, "Headline", "Foundation Courses + Compost Intensive", M, 80, 936, 200, 84)
    T(d, 0, "Details", "Fall Enrollment Special, until 2 December.", M, round(y) + 20, 936, 70, 52, bold=False)
    bw = 204
    bh = round(bw * 426 / 278)
    gap = (936 - 4 * bw) // 3
    for i, b in enumerate(BADGES):
        im = rounded(Image.open(b).convert("RGB").resize((bw, bh), Image.LANCZOS), 18)
        put_shadowed(d, 0, f"Badge FC{i + 1}", im, M + i * (bw + gap), seam - bh // 2 + 30)
    cy = seam + bh // 2 + 30 + 40
    cic = Image.open(CIC).convert("RGB")
    cw = 190
    cic = rounded(cic.resize((cw, round(cic.height * cw / cic.width)), Image.LANCZOS), 18)
    tw = 560
    gx = (W - (cw + 36 + tw)) // 2
    th = height("+ a seat in a 2027 Compost Intensive cohort", 52, tw) + 14 + height("10 weeks, live and online", 52, tw,
                                                                                     bold=False)
    gy = cy + (FY - 30 - cy - max(cic.height, th)) // 2
    put_shadowed(d, 0, "CIC badge", cic, gx, gy + (max(cic.height, th) - cic.height) // 2)
    ty = gy + (max(cic.height, th) - th) // 2
    y = T(d, 0, "CIC headline", "+ a seat in a 2027 Compost Intensive cohort", gx + cw + 36, ty, tw, 200, 52,
          color=BROWN)
    T(d, 0, "CIC details", "10 weeks, live and online", gx + cw + 36, round(y) + 14, tw, 70, 52, bold=False,
      color=INK)
    footer(d, 0, white=False)
    # 2. above ground / below ground
    hz = 650
    bg = Image.new("RGBA", (W, H))
    bg.paste(grain(Image.new("RGB", (W, hz), CREAM), 3, 3), (0, 0))
    bg.paste(speckle(W, H - hz, 5).crop((0, 0, W, H - hz)), (0, hz))
    sh = Image.new("RGBA", (W, H - hz), rgb(SOIL) + (150,))
    bg.alpha_composite(sh, (0, hz))
    ImageDraw.Draw(bg).rectangle((0, hz - 4, W, hz + 4), fill=rgb(LGREEN) + (255,))
    d.bg(1, bg, name="Background: above | below ground")
    T(d, 1, "Headline", "Learn what your\nsoil needs. Then build\nit yourself.", M, 70, 936, 300, 84, color=BROWN)
    sp = line_art("sprout", 470)            # soil line sits at 327/540 of the drawing's height
    soil_y = round(sp.height * 327 / 540)
    sx, sy = (W - sp.width) // 2, hz - soil_y
    top = Image.new("RGBA", sp.size, rgb("#156826") + (0,))
    top.putalpha(sp.getchannel("A").point(lambda v: v))
    top = top.crop((0, 0, sp.width, soil_y))
    bot = Image.new("RGBA", sp.size, rgb(CREAM) + (0,))
    bot.putalpha(sp.getchannel("A").point(lambda v: v * 70 // 255))
    bot = bot.crop((0, soil_y, sp.width, sp.height))
    d.put(1, "Seedling", top, sx, sy, shadowed=False, anchor="tl")
    d.put(1, "Roots", bot, sx, hz, shadowed=False, anchor="tl")
    y = T(d, 1, "Course list", "The Soil Food Web\nBioComplete™ Compost\nBioComplete™ Liquid Amendments\nMicroscopy",
          M, hz + 50, 936, 340, 52, lh=1.2)
    T(d, 1, "Course note", "Self-paced. Start today.", M, round(y) + 24, 936, 70, 52, bold=False, color=MINT)
    footer(d, 1, "Until 2 December.")
    # 3. three steps
    bg = blueprint(W, H, 6)
    tint = Image.new("RGBA", (W, H), rgb(NIGHT_BLUE) + (150,))
    bg.alpha_composite(tint)
    d.bg(2, bg, name="Background: blueprint")
    T(d, 2, "Headline", "From soil science to compost you made yourself.", M, 80, 936, 280, 73)
    cols = [("book", "Start today", "4 courses, self-paced"), ("calendar", "Pick your cohort", "January, May or August"),
            ("hands", "Keep your compost", "Two batches, at home")]
    cw3 = 300
    cxs = [M + cw3 / 2 + i * (cw3 + 18) for i in range(3)]
    cyc = 690
    line = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(line)
    for x in range(round(cxs[0]), round(cxs[2]), 22):
        dr.ellipse((x - 3, cyc - 3, x + 3, cyc + 3), fill=rgb(MINT) + (200,))
    d.put(2, "Path", line, 0, 0, shadowed=False, anchor="tl")
    for i, (art, t1, t2) in enumerate(cols):
        cx = cxs[i]
        put_art(d, 2, art, cx, 480, 230, 200)
        c = Image.new("RGBA", (112, 112), (0, 0, 0, 0))
        ImageDraw.Draw(c).ellipse((0, 0, 111, 111), fill=rgb(NIGHT_BLUE) + (255,), outline=rgb(MINT) + (255,),
                                  width=4)
        d.put(2, f"Step 0{i + 1} circle", c, round(cx - 56), cyc - 56, shadowed=False, anchor="tl")
        T(d, 2, f"Step 0{i + 1} number", f"0{i + 1}", round(cx - 56), cyc - 30, 112, 62, 52, color=MINT)
        y = T(d, 2, f"Step 0{i + 1} title", t1, round(cx - cw3 / 2) + (1 if i == 0 else 0), cyc + 90, cw3, 140, 52)
        T(d, 2, f"Step 0{i + 1} text", t2, round(cx - cw3 / 2) + (1 if i == 0 else 0), round(y) + 10, cw3, 140, 50, bold=False)
    footer(d, 2, "Until 2 December.")
    # 4. number tiles on soil with coloured light
    d.bg(3, glow_bg(SOIL, [(300, 520, 520, "#156826", 0.55), (800, 520, 520, "#3780B8", 0.5),
                           (300, 900, 520, "#6B4A3A", 0.6), (800, 900, 520, TAN, 0.35)], 7),
         name="Background: soil with light")
    T(d, 3, "Headline", "Everything in one bundle", M, 80, 936, 200, 84)
    tiles = [("4", "Foundation Courses"), ("10", "weeks live with a mentor"), ("2", "batches of compost you keep"),
             ("100s", "of hours of Dr. Elaine's webinars")]
    tw2, th2, g = 453, 380, 30
    for i, (n, t) in enumerate(tiles):
        x0, y0 = M + (i % 2) * (tw2 + g), 290 + (i // 2) * (th2 + g)
        d.put(3, f"Tile {i + 1}", frost(tw2, th2), x0, y0, shadowed=False, anchor="tl")
        T(d, 3, f"Tile {i + 1} number", n, x0 + 20, y0 + 40, tw2 - 40, 170, 150, mn=120, lh=1.0)
        T(d, 3, f"Tile {i + 1} text", t, x0 + 30, y0 + 220, tw2 - 60, 130, 52, bold=False)
    footer(d, 3, "Until 2 December.\nLink in bio.", "promo-fall-bundle")
    return d


# ---------------- by hand, then the microscope ----------------
def eyepiece(d_px):
    im = ImageOps.exif_transpose(Image.open(MICRO)).convert("RGB")
    s = min(im.size)
    cx = min(max(im.width * 0.45, s / 2), im.width - s / 2)
    cy = min(max(im.height * 0.42, s / 2), im.height - s / 2)
    im = im.crop((round(cx - s / 2), round(cy - s / 2), round(cx + s / 2), round(cy + s / 2))).resize((d_px, d_px),
                                                                                                         Image.LANCZOS)
    m = Image.new("L", (d_px * 2, d_px * 2), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d_px * 2 - 1, d_px * 2 - 1), fill=255)
    out = im.convert("RGBA")
    out.putalpha(m.resize((d_px, d_px), Image.LANCZOS))
    # dark vignette like looking down an eyepiece
    yy, xx = np.mgrid[0:d_px, 0:d_px].astype(np.float32)
    r = np.sqrt((xx - d_px / 2) ** 2 + (yy - d_px / 2) ** 2) / (d_px / 2)
    v = (np.clip((r - 0.72) / 0.28, 0, 1) ** 1.6 * 170).astype("uint8")
    shade = Image.new("RGBA", (d_px, d_px), (0, 0, 0, 0))
    shade.putalpha(Image.fromarray(v))
    out.alpha_composite(Image.composite(shade, Image.new("RGBA", shade.size, (0, 0, 0, 0)), out.getchannel("A")))
    return out


def ring(d_px, ticks=True):
    pad = 18
    im = Image.new("RGBA", (d_px + pad * 2, d_px + pad * 2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.ellipse((pad - 8, pad - 8, pad + d_px + 7, pad + d_px + 7), outline=rgb(CREAM) + (230,), width=3)
    if ticks:
        c = pad + d_px / 2
        for i in range(60):
            a = i / 60 * 2 * math.pi
            r0, r1 = d_px / 2 + 8, d_px / 2 + (18 if i % 5 == 0 else 13)
            dr.line((c + r0 * math.sin(a), c - r0 * math.cos(a), c + r1 * math.sin(a), c - r1 * math.cos(a)),
                    fill=rgb(CREAM) + (200,), width=2)
    return im, pad


def by_hand():
    d = Deck("x20261125", 1, "by-hand-then-microscope-v13", "2026-11-18")
    d.bg(0, glow_bg("#16110F", [(285, 520, 420, "#6B4A3A", 0.55), (795, 520, 420, "#2A5A7A", 0.55)], 11),
         name="Background: dark")
    T(d, 0, "Headline", "Judge it by hand.\nThen see the life in it.", M, 70, 936, 200, 84)
    dia, cy = 340, 290
    xs = [M + 20, W - M - 20 - dia]
    left = Image.new("RGBA", (dia, dia), (0, 0, 0, 0))
    ImageDraw.Draw(left).ellipse((0, 0, dia - 1, dia - 1), fill=rgb("#4F3433") + (255,))
    hands = art_fit("hands", 250, 250)
    left.alpha_composite(hands, ((dia - hands.width) // 2, (dia - hands.height) // 2))
    d.put(0, "Hands drawing", left, xs[0], cy, shadowed=False, anchor="tl")
    r, pad = ring(dia, ticks=False)
    d.put(0, "Ring left", r, xs[0] - pad, cy - pad, shadowed=False, anchor="tl")
    d.put(0, "Micrograph", eyepiece(dia), xs[1], cy, shadowed=False, anchor="tl")
    r, pad = ring(dia)
    d.put(0, "Eyepiece ring", r, xs[1] - pad, cy - pad, shadowed=False, anchor="tl")
    lw = 460
    ly = cy + dia + 30
    yl = T(d, 0, "Left label", "In the Compost Intensive", xs[0] + dia // 2 - lw // 2, ly, lw, 200, 52)
    y = T(d, 0, "Right label", "Microscopy, in the Foundation Courses", xs[1] + dia // 2 - lw // 2, ly, lw, 200, 52)
    yc = T(d, 0, "Photo credit", "Photo: Keisha Wheeler", xs[1] + dia // 2 - lw // 2, round(y) + 4, lw, 60,
      42, bold=False, mn=42, color="#CFC8BC")
    # the five senses as pills, two rows, centred
    words = [["Look", "Feel", "Smell"], ["Structure", "Maturity"]]
    from collage import font
    f = font("montserrat-bold", False, 50)
    py = round(max(yl, yc)) + 26
    for row in words:
        ws = [round(f.getlength(w)) + 64 for w in row]
        x = (W - (sum(ws) + 20 * (len(row) - 1))) // 2
        for w, word in zip(ws, row):
            pill = Image.new("RGBA", (w, 84), (0, 0, 0, 0))
            ImageDraw.Draw(pill).rounded_rectangle((0, 0, w - 1, 83), 42, fill=rgb(TAN) + (40,),
                                                   outline=rgb(TAN) + (255,), width=3)
            d.put(0, f"Pill {word}", pill, x, py, shadowed=False, anchor="tl")
            T(d, 0, word, word, x, py + 13, w, 62, 50, color=CREAM, mn=50)
            x += w + 20
        py += 96
    footer(d, 0, "Until 2 December.\nLink in bio.", "x20261125")
    return d


# ---------------- pick your season: the 2027 ring ----------------
def season():
    d = Deck("x20261130", 1, "pick-your-season-ring-v13", "2026-11-25")
    d.bg(0, glow_bg(NIGHT_BLUE, [(W / 2, 720, 520, "#1F4E79", 0.7)], 13), name="Background: night blue")
    y = T(d, 0, "Headline", "Start today.\nPick your season.", M, 70, 936, 200, 84)
    T(d, 0, "Details", "Start the Foundation Courses any day. One 2027 Compost Intensive cohort is included.", M,
      round(y) + 20, 936, 140, 52, bold=False)
    cx, cy, R = W / 2, 700, 200
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    dr.ellipse((cx - R, cy - R, cx + R, cy + R), outline=rgb(CREAM) + (90,), width=10)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        dr.line((cx + (R - 16) * math.sin(a), cy - (R - 16) * math.cos(a), cx + (R + 16) * math.sin(a),
                 cy - (R + 16) * math.cos(a)), fill=rgb(CREAM) + (140,), width=3)
    arcs = [((10 / 31), 2 + 26 / 31, ICE, "11 Jan\nto 26 Mar"), (4 + 9 / 30, 6 + 25 / 31, MINT, "10 May\nto 25 Jul"),
            (7 + 29 / 31, 10 + 7 / 30, TAN, "30 Aug\nto 7 Nov")]
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for s, e, col, _ in arcs:
        for dd in (gd, dr):
            dd.arc((cx - R, cy - R, cx + R, cy + R), s / 12 * 360 - 90, e / 12 * 360 - 90, fill=rgb(col) + (255,),
                   width=40)
    layer = Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)), layer)
    d.put(0, "Year ring 2027", layer, 0, 0, shadowed=False, anchor="tl")
    T(d, 0, "Year", "2027", round(cx - 200), round(cy - 60), 400, 120, 110, mn=96, lh=1.0)
    for i, m in enumerate("JFMAMJJASOND"):
        a = (i + 0.5) / 12 * 2 * math.pi
        x, y2 = cx + (R + 52) * math.sin(a), cy - (R + 52) * math.cos(a)
        T(d, 0, f"Month {i + 1}", m, round(x - 30), round(y2 - 26), 60, 52, 42, mn=42, color="#CFD9E3")
    for (s, e, col, lab), lw in zip(arcs, (240, 260, 220)):
        a = (s + e) / 2 / 12 * 2 * math.pi
        rr = R + 170
        x, y2 = cx + rr * math.sin(a), cy - rr * math.cos(a)
        T(d, 0, f"Cohort {lab.split()[0]} {lab.split()[1]}", lab, round(x - lw / 2), round(y2 - 50), lw, 110, 42,
          mn=42, color=col, lh=1.15)
    footer(d, 0, "One week left,\nuntil 2 December.", "x20261130")
    return d


if __name__ == "__main__":
    for fn, v in ((carousel, "v8"), (by_hand, "v13"), (season, "v13")):
        d = fn()
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(TILES, f"{d.id}-{v}-{k}.jpg")), d.id
        print(d.save(TILES, DECKS)[0], d.pptx_name())
