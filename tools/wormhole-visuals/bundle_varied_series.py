"""The other Fall Enrollment Special posts, each in its own style (Linnea, 4 Nov: "not all the same visual style").
Centred text, dates on one line, the Instagram QR code on its own last slide in each post's own look. Wording from
the bundle and Compost Intensive pages only. Never "keep your compost", never failing piles, no prices.

  x20261118 v11    Mon 9 Nov    big numbers on soil: the Compost Intensive Course
  x20261125 v18    Wed 18 Nov   dark microscope: look, feel, smell, structure, maturity + Microscopy
  x20261130 v18    Wed 25 Nov   night blue 2027 year ring: one week left
  fes20261130 v17  Wed 2 Dec    cream type poster: last day

  python3 tools/wormhole-visuals/bundle_varied_series.py
"""
import math
import os

import qrcode
from PIL import Image, ImageDraw, ImageFilter

from bundle_final_nov4 import badge
from bundle_from_decks import ICE, NIGHT_BLUE, SOIL, TAN, eyepiece, frost, glow_bg, ring
from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import FY, M, MINT, T, footer, height
from bundle_v6 import H, W, line_art
from collage import Deck
from nov_fill import BROWN, CREAM, DECKS, GREEN, INK, TILES

IG = "https://tr.ee/ce6tWIaOx7"
DARK = "#16110F"


def tint(name, w, color, maxh=None):
    im = line_art(name, w)
    if maxh and im.height > maxh:
        im = line_art(name, round(w * maxh / im.height))
    out = Image.new("RGBA", im.size, rgb(color) + (0,))
    out.putalpha(im.getchannel("A"))
    return out


def qr_end(d, k, bg, head_color, text_color, white_logo, frame_color, det="Fall Enrollment Special\nUntil 2 December."):
    """Last slide: the QR code big and on its own, in the post's own colours."""
    d.bg(k, bg, name="Background")
    q = qrcode.QRCode(border=2, box_size=20)
    q.add_data(IG)
    size = 460
    im = q.make_image(fill_color=INK, back_color=CREAM).convert("RGBA").resize((size, size), Image.NEAREST)
    fr = Image.new("RGBA", (size + 24, size + 24), (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle((0, 0, size + 23, size + 23), 30, fill=rgb(frame_color) + (255,))
    fr.alpha_composite(im, (12, 12))
    hh = height("Foundation Courses + Compost Intensive", 84, 936)
    dh = height(det, 66, 900, bold=False, lh=1.3)
    y = 60 + (FY - 20 - 60 - (hh + 80 + size + 24 + 80 + dh)) // 2
    T(d, k, "Headline", "Foundation Courses + Compost Intensive", M, y, 936, hh + 6, 84, color=head_color)
    y += hh + 80
    d.put(k, "QR code (Instagram link)", fr, (W - size - 24) // 2, y, shadowed=False, anchor="tl")
    y += size + 24 + 80
    T(d, k, "Details", det, (W - 900) // 2, y, 900, dh + 6, 66, bold=False, color=text_color, lh=1.3)
    footer(d, k, white=white_logo)


# ---------- 9 Nov: big numbers on soil ----------
def cic(v):
    d = Deck("x20261118", 4, f"compost-intensive-numbers-{v}", "2026-11-09")
    soil = lambda s: glow_bg(SOIL, [(300, 500, 560, "#156826", 0.45), (800, 520, 560, "#3780B8", 0.4),
                                    (540, 1000, 600, "#6B4A3A", 0.6)], s)
    d.bg(0, soil(90), name="Background: soil")
    cicb = badge("cic", 340)
    hh = height("The Compost Intensive Course", 86, 936)
    dh = height("No prerequisites. All are welcome.", 52, 900, bold=False)
    y = 60 + (FY - 20 - 60 - (cicb.height + 80 + hh + 30 + dh)) // 2
    d.put(0, "Compost Intensive badge", cicb, (W - cicb.width) // 2, y, shadowed=False, anchor="tl")
    y += cicb.height + 80
    T(d, 0, "Headline", "The Compost Intensive Course", M, y, 936, hh + 6, 86)
    T(d, 0, "Details", "No prerequisites. All are welcome.", (W - 900) // 2, y + hh + 30, 900, dh + 6, 52, bold=False)
    footer(d, 0)
    # 2x2 numbers
    d.bg(1, soil(91), name="Background: soil")
    T(d, 1, "Headline", "Ten weeks, online", M, 90, 936, 110, 86)
    tiles = [("10", "weeks, online"), ("90", "minutes live with a mentor every week"),
             ("2", "compost piles you build where you live"), ("3", "2027 cohorts: January, May or August")]
    tw, th, g = 453, 400, 30
    for i, (n, t) in enumerate(tiles):
        x0, y0 = M + (i % 2) * (tw + g), 250 + (i // 2) * (th + g)
        d.put(1, f"Tile {i + 1}", frost(tw, th), x0, y0, shadowed=False, anchor="tl")
        T(d, 1, f"Tile {i + 1} number", n, x0 + 20, y0 + 30, tw - 40, 150, 130, mn=120, lh=1.0)
        T(d, 1, f"Tile {i + 1} text", t, x0 + 30, y0 + 185, tw - 60, 200, 52, bold=False)
    footer(d, 1)
    # one big number with its source on the page
    d.bg(2, soil(92), name="Background: soil")
    n = "80%"
    det = ("More than 80% of the people who took our pilot version of this course walked away with successful "
           "thermophilic piles that achieved BioComplete™ biological potency.")
    dh = height(det, 52, 860, bold=False, lh=1.3)
    y = 60 + (FY - 20 - 60 - (230 + 50 + dh)) // 2
    T(d, 2, "Number", n, M, y, 936, 240, 220, mn=180, lh=1.0, color=MINT)
    T(d, 2, "Details", det, (W - 860) // 2, y + 280, 860, dh + 6, 52, bold=False, lh=1.3)
    footer(d, 2)
    qr_end(d, 3, soil(93), CREAM, CREAM, True, TAN)
    return d


# ---------- 18 Nov: dark, microscope ----------
def micro(v):
    d = Deck("x20261125", 3, f"look-feel-smell-microscopy-{v}", "2026-11-18")
    dark = lambda s, c: glow_bg(DARK, [(540, 420, 560, c, 0.55)], s)
    # 1. by hand
    d.bg(0, dark(100, "#6B4A3A"), name="Background: dark")
    dia = 400
    circ = Image.new("RGBA", (dia, dia), (0, 0, 0, 0))
    ImageDraw.Draw(circ).ellipse((0, 0, dia - 1, dia - 1), fill=rgb("#4F3433") + (255,))
    hands = line_art("hands", 300)
    circ.alpha_composite(hands, ((dia - hands.width) // 2, (dia - hands.height) // 2))
    head = "Look, feel, smell, structure, maturity"
    det = "In the Compost Intensive Course you assess compost quality using practical field observations."
    hh, dh = height(head, 73, 936), height(det, 52, 860, bold=False, lh=1.3)
    y = 60 + (FY - 20 - 60 - (dia + 80 + hh + 30 + dh)) // 2
    d.put(0, "Hands drawing", circ, (W - dia) // 2, y, shadowed=False, anchor="tl")
    r, pad = ring(dia, ticks=False)
    d.put(0, "Ring", r, (W - dia) // 2 - pad, y - pad, shadowed=False, anchor="tl")
    y += dia + 80
    T(d, 0, "Headline", head, M, y, 936, hh + 6, 73)
    T(d, 0, "Details", det, (W - 860) // 2, y + hh + 30, 860, dh + 6, 52, bold=False, lh=1.3)
    footer(d, 0)
    # 2. through the eyepiece
    d.bg(1, dark(101, "#2A5A7A"), name="Background: dark")
    head = "Foundation Course 4: Microscopy"
    det = "Learn to use a compound microscope to identify and quantify bacteria, fungi, protozoa and nematodes."
    hh, dh = height(head, 73, 936), height(det, 52, 860, bold=False, lh=1.3)
    y = 60 + (FY - 20 - 60 - (dia + 80 + hh + 30 + dh + 60)) // 2
    d.put(1, "Micrograph", eyepiece(dia), (W - dia) // 2, y, shadowed=False, anchor="tl")
    r, pad = ring(dia)
    d.put(1, "Eyepiece ring", r, (W - dia) // 2 - pad, y - pad, shadowed=False, anchor="tl")
    y += dia + 80
    T(d, 1, "Headline", head, M, y, 936, hh + 6, 73)
    y2 = T(d, 1, "Details", det, (W - 860) // 2, y + hh + 30, 860, dh + 6, 52, bold=False, lh=1.3)
    T(d, 1, "Photo credit", "Nematode, 40x. Photo: Keisha Wheeler", M, round(y2) + 16, 936, 60, 42,
      bold=False, mn=42, color="#CFC8BC")
    footer(d, 1)
    qr_end(d, 2, dark(102, "#156826"), CREAM, CREAM, True, TAN)
    return d


# ---------- 25 Nov: the 2027 ring ----------
def year_ring(d, k, cx, cy, R):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    dr.ellipse((cx - R, cy - R, cx + R, cy + R), outline=rgb(CREAM) + (90,), width=10)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        dr.line((cx + (R - 16) * math.sin(a), cy - (R - 16) * math.cos(a), cx + (R + 16) * math.sin(a),
                 cy - (R + 16) * math.cos(a)), fill=rgb(CREAM) + (140,), width=3)
    arcs = [(10 / 31, 2 + 26 / 31, ICE, "11 Jan\nto 26 Mar"), (4 + 9 / 30, 6 + 25 / 31, MINT, "10 May\nto 25 Jul"),
            (7 + 29 / 31, 10 + 7 / 30, TAN, "30 Aug\nto 7 Nov")]
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for s, e, col, _ in arcs:
        for dd in (gd, dr):
            dd.arc((cx - R, cy - R, cx + R, cy + R), s / 12 * 360 - 90, e / 12 * 360 - 90, fill=rgb(col) + (255,),
                   width=40)
    d.put(k, "Year ring 2027", Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)), layer), 0, 0,
          shadowed=False, anchor="tl")
    T(d, k, "Year", "2027", round(cx - 200), round(cy - 60), 400, 120, 110, mn=96, lh=1.0)
    for i, m in enumerate("JFMAMJJASOND"):
        a = (i + 0.5) / 12 * 2 * math.pi
        x, y2 = cx + (R + 52) * math.sin(a), cy - (R + 52) * math.cos(a)
        T(d, k, f"Month {i + 1}", m, round(x - 30), round(y2 - 26), 60, 52, 42, mn=42, color="#CFD9E3")
    for (s, e, col, lab), lw in zip(arcs, (240, 260, 220)):
        a = (s + e) / 2 / 12 * 2 * math.pi
        x, y2 = cx + (R + 170) * math.sin(a), cy - (R + 170) * math.cos(a)
        T(d, k, f"Cohort {lab.split()[0]} {lab.split()[1]}", lab, round(x - lw / 2), round(y2 - 50), lw, 110, 42,
          mn=42, color=col, lh=1.15)


def last_week(v):
    d = Deck("x20261130", 2, f"one-week-left-ring-{v}", "2026-11-25")
    night = lambda s: glow_bg(NIGHT_BLUE, [(W / 2, 720, 520, "#1F4E79", 0.7)], s)
    d.bg(0, night(110), name="Background: night blue")
    y = T(d, 0, "Headline", "One week left", M, 80, 936, 110, 86)
    T(d, 0, "Details", "Start the Foundation Courses today.\nPick one 2027 Compost Intensive cohort.", M, round(y) + 20,
      936, 140, 52, bold=False)
    year_ring(d, 0, W / 2, 720, 200)
    footer(d, 0)
    qr_end(d, 1, night(111), CREAM, CREAM, True, ICE)
    return d


# ---------- 2 Dec: cream type poster ----------
def last_day(v):
    d = Deck("fes20261130", 3, f"last-day-poster-{v}", "2026-12-02")
    paper = lambda s: grain(Image.new("RGB", (W, H), CREAM), s, 3)
    d.bg(0, paper(120), name="Background: cream")
    T(d, 0, "Eyebrow", "FALL ENROLLMENT SPECIAL", M, 130, 936, 70, 52, color=GREEN, mn=50)
    y = T(d, 0, "Headline", "Last day", M, 210, 936, 200, 170, color=BROWN, mn=120, lh=1.0)
    y = T(d, 0, "Details", "Foundation Courses + Compost Intensive.\nThe special ends today.", M, round(y) + 20, 936,
          140, 52, bold=False, color=INK)
    sp = tint("sprout", 560, GREEN, FY - round(y) - 110)
    d.put(0, "Line drawing", sp, (W - sp.width) // 2, round(y) + 50 + (FY - round(y) - 90 - sp.height) // 2,
          shadowed=False, anchor="tl")
    footer(d, 0, white=False)
    # what's in it: brown card on cream
    d.bg(1, paper(121), name="Background: cream")
    items = [("4 Foundation Courses", "Self-paced, 63 lectures and about 150 hours of study."),
             ("A seat in a 2027 Compost Intensive cohort", "Ten weeks online, with a 90-minute live session with a "
              "mentor every week."),
             ("Hundreds of hours of webinars", "Our legacy webinar archive, recorded live with Dr. Elaine Ingham.")]
    rows = [(height(t, 52, 820), height(x, 52, 780, bold=False, lh=1.25)) for t, x in items]
    ch = round(70 + sum(a + 8 + b for a, b in rows) + 46 * (len(rows) - 1) + 70)
    top = 60 + (FY - 20 - 60 - ch) // 2
    card = Image.new("RGBA", (936, ch), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, 935, ch - 1), 30, fill=rgb(BROWN) + (255,))
    d.put(1, "Card", card, M, top, shadowed=False, anchor="tl")
    y = top + 70
    for i, ((t, x), (a, b)) in enumerate(zip(items, rows)):
        T(d, 1, f"Item {i + 1}", t, (W - 820) // 2, y, 820, a + 6, 52, color=MINT)
        y += a + 8
        T(d, 1, f"Item {i + 1} text", x, (W - 780) // 2, y, 780, b + 6, 52, bold=False, color=CREAM, lh=1.25)
        y += b + 46
    footer(d, 1, white=False)
    qr_end(d, 2, paper(122), BROWN, INK, False, GREEN, "Fall Enrollment Special\nEnds today.")
    return d


if __name__ == "__main__":
    for fn, v in ((cic, "v11"), (micro, "v18"), (last_week, "v18"), (last_day, "v17")):
        d = fn(v)
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(TILES, f"{d.id}-{v}-{k}.jpg")), d.id
        print(d.save(TILES, DECKS)[0], d.pptx_name())
