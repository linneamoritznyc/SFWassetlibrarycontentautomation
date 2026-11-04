"""v12 of the three bundle posts (Linnea, 4 Nov: "better layout, this is all over the place"). One fixed grid on every
slide: drawing in a fixed zone at the top, text centred below it at the same height on every slide of a post, and one
footer row (QR left, footer line centred, logo right) on the same baseline. Centred text, dates on one line and UTM QR
codes per Stephanie (4 Nov). Words from the bundle sales page.

  python3 tools/wormhole-visuals/bundle_three_styles_v12.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import news_cards as nc
from bundle_three_styles import (BLUE_D, COLOR_LOGO, NIGHT, T, UTM, URL, blueprint, glow_layer, grain, keep_dates,
                                 rgb, speckle, tinted)
from bundle_v6 import H, W, line_art
from collage import Deck, fit
import qrcode
from nov_fill import BROWN, CREAM, DECKS, GREEN, INK, LGREEN, TILES, WHITE

V = "v12"
M = 72                 # outer margin
FOOT = 170             # footer row height (QR and logo)
FY = H - M - FOOT      # footer row top: 1108
MINT = "#A8D5B0"


def height(t, size, w, bold=True, lh=None):
    lh = lh or (1.06 if bold else 1.22)
    _, lines, s = fit(keep_dates(t), "montserrat-bold" if bold else "source-reg", False, w, 2000, size, size, lh)
    return len(lines) * s * lh


def art_fit(name, maxw, maxh, color=None):
    im = line_art(name, maxw)
    if im.height > maxh:
        im = line_art(name, round(maxw * maxh / im.height))
    if color:
        out = Image.new("RGBA", im.size, rgb(color) + (0,))
        out.putalpha(im.getchannel("A"))
        im = out
    return im


def put_art(d, k, name, cx, cy, maxw, maxh, color=None):
    im = art_fit(name, maxw, maxh, color)
    d.put(k, "Line drawing", im, round(cx - im.width / 2), round(cy - im.height / 2), shadowed=False, anchor="tl")


def footer(d, k, line=None, qr_pid=None, white=True, color=CREAM):
    lg = Image.open(WHITE if white else COLOR_LOGO).convert("RGBA")
    lg = lg.resize((FOOT, round(lg.height * FOOT / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - M - FOOT, FY + (FOOT - lg.height) // 2, shadowed=False, anchor="tl")
    if qr_pid:
        q = qrcode.QRCode(border=2, box_size=10)
        q.add_data(URL + UTM.format(qr_pid))
        im = q.make_image(fill_color=INK, back_color=CREAM).convert("RGBA").resize((FOOT, FOOT), Image.NEAREST)
        m = Image.new("L", (FOOT, FOOT), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, FOOT - 1, FOOT - 1), 16, fill=255)
        im.putalpha(m)
        d.put(k, "QR code (UTM link)", im, M, FY, shadowed=False, anchor="tl")
    if line:
        w = W - 2 * (M + FOOT + 24)
        h = height(line, 52, w)
        T(d, k, "Footer line", line, M + FOOT + 24, round(FY + FOOT / 2 - h / 2), w, h + 4, 52, color=color)


def text_block(d, k, y, head, det, hsize=73, hcolor=CREAM, dcolor=CREAM, w=900, dw=820):
    y = T(d, k, "Headline", head, M, y, w, 400, hsize, color=hcolor)
    if det:
        y = T(d, k, "Details", det, M, round(y) + 26, dw, 400, 52, bold=False, color=dcolor)
    return y


# ---------- post 1: split screen ----------
def two_courses():
    d = Deck("x20261125", 3, f"two-courses-one-bundle-{V}", "2026-11-18")
    half = W // 2
    bg = Image.new("RGBA", (W, H))
    bg.paste(blueprint(half, H, 1), (0, 0))
    bg.paste(speckle(W - half, H, 2), (half, 0))
    ImageDraw.Draw(bg).line((half, 0, half, H), fill=rgb(CREAM) + (255,), width=6)
    d.bg(0, bg, name="Background: blueprint | soil")
    put_art(d, 0, "microscope", half / 2, 290, 400, 330)
    put_art(d, 0, "thermometer", half + half / 2, 290, 300, 330)
    T(d, 0, "Label left", "Foundation Courses", 40, 490, half - 80, 130, 52)
    T(d, 0, "Label right", "Compost Intensive", half + 40, 490, half - 80, 130, 52)
    cw, top = 800, 660
    hh = height("Two courses, one bundle", 84, cw - 100)
    dh = height("Fall Enrollment Special, until 2 December. Link in bio.", 52, cw - 100, bold=False)
    ch = 56 + hh + 22 + dh + 56
    card = Image.new("RGBA", (cw, round(ch)), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, cw - 1, round(ch) - 1), 28, fill=rgb(CREAM) + (255,))
    d.put(0, "Card", card, (W - cw) // 2, top, shadowed=False, anchor="tl")
    y = T(d, 0, "Headline", "Two courses, one bundle", (W - cw) // 2 + 50, top + 56, cw - 100, hh + 4, 84,
          color=BROWN)
    T(d, 0, "Details", "Fall Enrollment Special, until 2 December. Link in bio.", (W - cw) // 2 + 50, round(y) + 22, cw - 100,
      dh + 4, 52, bold=False, color=INK)
    footer(d, 0)
    for k, (bgim, art, aw, head, det) in enumerate((
            (blueprint(W, H, 3), "microscope", 700, "The Foundation Courses teach you to work out what your soil needs.",
             "63 lectures and about 150 hours of study, with 40+ years of Dr. Elaine's knowledge."),
            (speckle(W, H, 4), "thermometer", 520, "The Compost Intensive Course teaches you to make it.",
             "No prerequisites. Start the Foundation Courses today and build with the cohort as early as January.")),
            start=1):
        d.bg(k, bgim, name="Background")
        put_art(d, k, art, W / 2, 330, aw, 440)
        text_block(d, k, 620, head, det)
        footer(d, k, "Link in bio." if k == 2 else None, "x20261125" if k == 2 else None)
    return d


# ---------- post 2: night timeline ----------
def pick_season():
    d = Deck("x20261130", 1, f"pick-your-season-{V}", "2026-11-25")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - 200) / H * 1.6) ** 2)
    a = np.zeros((H, W, 3), np.float32) + np.array(rgb(NIGHT), np.float32)
    a += (np.clip(1 - r / 0.5, 0, 1) ** 2)[..., None] * np.array([40, 70, 45], np.float32)
    d.bg(0, grain(Image.fromarray(np.clip(a, 0, 255).astype("uint8")), 5, 3), name="Background: night")
    put_art(d, 0, "sunrise", W / 2, 230, 600, 300)
    y = text_block(d, 0, 430, "Pick your season", "Start the Foundation Courses this winter. Then build with a "
                   "ten-week 2027 cohort, with a live mentor every week.", hsize=84)
    x0, x1, ty = M + 20, W - M - 20, round(y) + 150
    mw = (x1 - x0) / 12
    blocks = [(10 / 31, 2 + 26 / 31), (4 + 9 / 30, 6 + 25 / 31), (7 + 29 / 31, 10 + 7 / 30)]

    def draw(dr):
        dr.line((x0, ty, x1, ty), fill=rgb(CREAM) + (110,), width=4)
        for i in range(13):
            dr.line((x0 + i * mw, ty - 12, x0 + i * mw, ty + 12), fill=rgb(CREAM) + (110,), width=3)
        for s, e in blocks:
            dr.rounded_rectangle((x0 + s * mw, ty - 30, x0 + e * mw, ty + 30), 30, fill=rgb(LGREEN) + (255,))
    d.put(0, "Timeline 2027", glow_layer(draw, 14), 0, 0, shadowed=False, anchor="tl")
    for i, m in enumerate("JFMAMJJASOND"):
        T(d, 0, f"Month {i + 1}", m, round(x0 + (i + 0.5) * mw - 35), ty - 92, 70, 52, 42, mn=42)
    for (s, e), lab in zip(blocks, ("11 Jan\nto 26 Mar", "10 May\nto 25 Jul", "30 Aug\nto 7 Nov")):
        cx = x0 + (s + e) / 2 * mw
        T(d, 0, f"Cohort {lab.split()[0]} {lab.split()[1]}", lab, round(cx - 140), ty + 50, 280, 110, 42,
          bold=False, mn=42, lh=1.15)
    footer(d, 0, "One week left,\nuntil 2 December.", "x20261130", color=MINT)
    return d


# ---------- post 3: ends today ----------
def ends_today():
    d = Deck("fes20261130", 3, f"bundle-ends-today-{V}", "2026-12-02")
    d.bg(0, grain(Image.new("RGB", (W, H), CREAM), 7, 3), name="Background: cream")
    T(d, 0, "Eyebrow", "FALL ENROLLMENT SPECIAL", M, 130, 936, 70, 52, color=GREEN, mn=50)
    y = T(d, 0, "Headline", "Ends today", M, 210, 936, 200, 160, color=BROWN, mn=120, lh=1.0)
    y = T(d, 0, "Details", "Foundation Courses + Compost Intensive.", M, round(y) + 20, 900, 140, 52, bold=False,
          color=INK)
    put_art(d, 0, "sprout", W / 2, (y + FY) / 2, 560, FY - y - 80, color=GREEN)
    footer(d, 0, "Link in bio.", white=False, color=GREEN)
    # quote
    d.bg(1, grain(Image.new("RGB", (W, H), "#3A2A22"), 8, 4), name="Background: brown")
    quote = ("The extraordinary body of knowledge Soil Food Web's Foundation Courses has to offer can certainly "
             "empower me with the required knowledge and experience to drive the work I have been developing "
             "further.")
    q = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    ImageDraw.Draw(q).text((0, -60), "“", font=ImageFont.truetype(
        os.path.join(nc.FONTS, "Montserrat-Bold.ttf"), 400), fill=rgb(LGREEN) + (255,))
    q = q.crop(q.getchannel("A").getbbox())
    qh = height(quote, 56, 900, bold=False, lh=1.25)
    total = q.height + 50 + qh + 40 + 62
    top = round((FY - 40 - total) / 2) + 20
    d.put(1, "Quote mark", q, (W - q.width) // 2, top, shadowed=False, anchor="tl")
    y = T(d, 1, "Quote", quote, M, top + q.height + 50, 900, qh + 4, 56, bold=False, lh=1.25)
    T(d, 1, "Name", "Clara Santiago, Portugal", M, round(y) + 40, 900, 70, 52, color=MINT)
    footer(d, 1)
    # consultant fact on a cream card
    d.bg(2, grain(Image.new("RGB", (W, H), CREAM), 9, 3), name="Background: cream")
    cw = 936
    eh = 62
    hh = height("The Compost Intensive counts toward the Consultant Pathway.", 73, cw - 120)
    dh = height("It can be used to satisfy the BioComplete™ Compost Production requirement.", 52, 760, bold=False)
    ch = round(60 + eh + 24 + hh + 26 + dh + 64)
    top = round((FY - 40 - ch) / 2) + 20
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, cw - 1, ch - 1), 28, fill=rgb(BROWN) + (255,))
    d.put(2, "Card", card, M, top, shadowed=False, anchor="tl")
    T(d, 2, "Eyebrow", "FOR CONSULTANTS", M + 60, top + 60, cw - 120, eh, 52, color=MINT, mn=50)
    y = T(d, 2, "Headline", "The Compost Intensive counts toward the Consultant Pathway.", M + 60, top + 60 + eh + 24,
          cw - 120, hh + 4, 73, color=CREAM)
    T(d, 2, "Details", "It can be used to satisfy the BioComplete™ Compost Production requirement.",
      (W - 760) // 2, round(y) + 26, 760, dh + 4, 52, bold=False, color=CREAM)
    footer(d, 2, "Ends today.\nLink in bio.", "fes20261130", white=False, color=BROWN)
    return d


if __name__ == "__main__":
    for fn in (two_courses, pick_season, ends_today):
        d = fn()
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(TILES, f"{d.id}-{V}-{k}.jpg")), d.id
        print(d.save(TILES, DECKS)[0], d.pptx_name())
