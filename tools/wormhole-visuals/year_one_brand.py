"""Giving Tuesday "Year one" carousel, on brand (docs/brand.md): Food Web Green leaf texture (the Cyber Monday ground
Linnea rated 10/10), cream cards as shapes, Montserrat headlines, Pathway Gothic One labels, Source Sans body, Soil
Brown on cream, real photos in arches and soft fades, line art, gold only on the Donate button. Allison's final text
(11-11-2026-year-one-achievements.pptx_1). Slide 1 keeps the compost thermometer.

  python3 tools/wormhole-visuals/year_one_brand.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from collage import Deck, cover, fit
from cyber_nov30 import leaf_texture
from nov_fill import DECKS, TILES
from year_one_luxe import PH, MYC, LAPTOP, COMPOST, arch, bleed, icon, lineart

W, H = 1080, 1350
GREEN = "#156826"
LEAFG = "#59A66C"
BROWN = "#4F3433"
CREAM = "#F4F1EA"
MINT = "#CFE6D3"
GOLD = (201, 162, 39)
LOGO_W = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
LOGO_C = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-colour.png"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


_LEAF = None


def leaf():
    global _LEAF
    if _LEAF is None:
        _LEAF = leaf_texture(770).resize((W, H)).convert("RGBA")
    return _LEAF.copy()


def card(d, k, x, y, w, h, name="Cream card", r=30, colour=CREAM):
    im = Image.new("RGBA", (w * 3, h * 3), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), r * 3, fill=rgb(colour) + (255,))
    d.put(k, name, im.resize((w, h), Image.LANCZOS), x, y, shadowed=True, anchor="tl")


def logo(d, k, x=None, y=None, w=140, colour=False):
    lg = Image.open(LOGO_C if colour else LOGO_W).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    x = W - 56 - w if x is None else x
    y = H - 50 - lg.height if y is None else y
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def tx(d, k, name, s, x, y, w, size, kind, colour, align="left", lh=None, track=0):
    lh = lh or {"montserrat-bold": 1.04, "pathway": 1.1, "source-reg": 1.22}[kind]
    _, lines, _ = fit(s, kind, False, w, 5000, size, size, lh, track)
    return d.text(k, name, s, x, y, w, len(lines) * size * lh + 10, size, kind=kind, italic=False, color=colour,
                  lh=lh, align=align, min_size=size, track=track)


def head(d, k, name, s, x, y, w, size, colour, align="left"):
    return tx(d, k, name, s, x, y, w, size, "montserrat-bold", colour, align)


def label(d, k, name, s, x, y, w, size=50, colour=LEAFG, align="left"):
    return tx(d, k, name, s, x, y, w, size, "pathway", colour, align, track=3)


def body(d, k, name, s, x, y, w, size=52, colour=BROWN, align="left"):
    return tx(d, k, name, s, x, y, w, size, "source-reg", colour, align)


def rule(d, k, x, y, w, colour=LEAFG, h=4, name="Rule"):
    d.put(k, name, Image.new("RGBA", (w, h), rgb(colour) + (255,)), x, y, shadowed=False, anchor="tl")


def tint(im, colour):
    a = np.asarray(im).copy()
    a[..., :3] = rgb(colour)
    return Image.fromarray(a)


# ------------------------------------------------------------------ slides
def s1(d, k):
    from giving_thermometer import dial, needle
    d.bg(k, leaf(), name="Background: green leaf texture")
    logo(d, k, (W - 150) // 2, 70, 150)
    label(d, k, "Eyebrow", "SOIL FOOD WEB FOUNDATION", 60, 250, 960, 52, MINT, "center")
    head(d, k, "Headline", "GIVING TUESDAY", 40, 315, 1000, 100, CREAM, "center")
    body(d, k, "Subline", "What we grew together in our first year", 100, 440, 880, 52, CREAM, "center")
    D = 600
    x, y = (W - D) // 2, 560
    sw, sh = 30, 130
    st = Image.new("RGBA", (sw * 4, sh * 4), (0, 0, 0, 0))
    ImageDraw.Draw(st).polygon([(0, 0), (sw * 4, 0), (sw * 4, (sh - 30) * 4), (sw * 2, sh * 4), (0, (sh - 30) * 4)],
                               fill=(216, 195, 165, 255))
    d.put(k, "Thermometer stem", st.resize((sw, sh), Image.LANCZOS), (W - sw) // 2, y + D - 18, shadowed=False,
          anchor="tl")
    d.put(k, "Thermometer dial", dial(D), x, y, shadowed=True, anchor="tl")
    d.put(k, "Needle (rotate around its centre to the current total)", needle(D, 0.0), x, y, shadowed=False,
          anchor="tl")


def s2(d, k):
    d.bg(k, leaf(), name="Background: green leaf texture")
    card(d, k, 56, 56, 968, 1238)
    x = 120
    label(d, k, "Eyebrow", "AT A GLANCE", x, 110, 840)
    head(d, k, "Headline", "OUR FIRST YEAR\nIN NUMBERS", x, 165, 840, 72, BROWN)
    head(d, k, "Number", "$300,000+", x, 365, 840, 128, GREEN)
    label(d, k, "Label", "IN SCHOLARSHIPS AWARDED", x, 510, 840, 50, BROWN)
    cells = [("35+", "FREE LIVE EVENTS", x, 630), ("4", "WORKSHOPS", 580, 630),
             ("23", "NUMBER OF COUNTRIES\nREPRESENTED IN OUR PDC", x, 930),
             ("46", "INDIA WORKSHOP\nPARTICIPANTS", 580, 930)]
    for n, lab, cx, cy in cells:
        head(d, k, f"Number {n}", n, cx, cy, 400, 110, GREEN)
        label(d, k, f"Label {n}", lab, cx, cy + 128, 400, 46, BROWN)
    logo(d, k, W - 120 - 140, 110, 140, colour=True)


def s3(d, k):
    d.bg(k, leaf(), name="Background: green leaf texture")
    d.put(k, "Photo in arch", arch(PH["scholar"], 760, 660, 0.5, 0.45), 160, 80, shadowed=True, anchor="tl")
    card(d, k, 56, 790, 968, 504)
    label(d, k, "Eyebrow", "OPENING THE DOOR", 120, 840, 840, 52)
    head(d, k, "Number", "$300,000+", 120, 905, 840, 136, GREEN)
    body(d, k, "Text", "in scholarships awarded for our various courses and workshops", 120, 1065, 760, 52)


def s4(d, k):
    d.bg(k, leaf(), name="Background: green leaf texture")
    card(d, k, 56, 56, 968, 1238)
    head(d, k, "Big 4", "4", 110, 70, 300, 330, GREEN)
    label(d, k, "Eyebrow", "IN PERSON", 420, 130, 560, 52)
    head(d, k, "Headline", "WORKSHOPS\nON 4\nCONTINENTS", 420, 185, 560, 68, BROWN)
    places = [("cr", "COSTA RICA", "Oct 2025", 0.5, 0.35), ("us", "UNITED\nSTATES", "Feb 2026", 0.5, 0.45),
              ("uk", "ENGLAND", "Jun 2026", 0.5, 0.4), ("india_walk", "INDIA", "Oct 2026", 0.45, 0.4)]
    aw, ah, gap = 200, 320, 20
    x0 = (W - (4 * aw + 3 * gap)) // 2
    for i, (key, name, date, fx, fy) in enumerate(places):
        x = x0 + i * (aw + gap)
        d.put(k, f"Photo {i + 1}", arch(PH[key], aw, ah, fx, fy), x, 470, shadowed=False, anchor="tl")
        label(d, k, f"Place {i + 1}", name, x, 812, aw, 46, GREEN, "center")
        body(d, k, f"Date {i + 1}", date, x, 920, aw, 44, BROWN, "center")
    body(d, k, "Text", "Hands-on training with our mentors, on four farms", 120, 1055, 700, 52)
    logo(d, k, W - 120 - 140, 1130, 140, colour=True)


def s5(d, k):
    bg = leaf()
    bg.alpha_composite(bleed(PH["india_group"], 760, 0.5, 0.55, 0.55), (0, 0))
    d.bg(k, bg, name="India workshop photo fading into the leaf texture")
    card(d, k, 56, 640, 968, 654)
    label(d, k, "Eyebrow", "FIRST WORKSHOP IN INDIA", 120, 690, 840, 52)
    head(d, k, "Number 46", "46", 120, 755, 380, 140, GREEN)
    body(d, k, "Text 46", "participants from 10 countries", 120, 915, 380, 52)
    head(d, k, "Number 61", "61", 580, 755, 380, 140, GREEN)
    body(d, k, "Text 61", "at the Life in the Soils seminar", 580, 915, 380, 52)
    label(d, k, "Partner line", "We partnered with Isha Foundation and Save Soil", 120, 1135, 840, 48, BROWN)


def s6(d, k):
    d.bg(k, leaf(), name="Background: green leaf texture")
    d.put(k, "Laptop line art", lineart(LAPTOP, 560), 260, 50, shadowed=False, anchor="tl")
    head(d, k, "Number", "35+", 90, 480, 520, 210, CREAM)
    label(d, k, "Label", "FREE\nLIVE\nEVENTS", 640, 500, 380, 66, MINT)
    card(d, k, 56, 830, 968, 400)
    label(d, k, "Eyebrow", "SOME OF OUR WEBINAR GUESTS:", 120, 875, 840, 50)
    body(d, k, "Guests 1", "Vandana Shiva\nGeoff Lawton\nNicole Masters", 120, 950, 400, 54)
    body(d, k, "Guests 2", "Mary Reynolds\nDavid Holmgren\nDr. Mary Cole", 560, 950, 400, 54)


def s7(d, k):
    d.bg(k, leaf(), name="Background: green leaf texture")
    label(d, k, "Eyebrow", "NEW PROGRAMS", 70, 80, 940, 52, MINT)
    head(d, k, "Headline", "TWO NEW WAYS TO LEARN", 70, 140, 940, 62, CREAM)
    cols = [(56, "sprout", "100", "students from 23 countries", "PERMACULTURE\nDESIGN\nCERTIFICATE",
             "With the Permaculture Association (UK)"),
            (550, "compost", "10", "weeks, live online", "COMPOST\nINTENSIVE COURSE",
             "No prerequisites, with Spanish transcriptions")]
    for x, ic, n, sub, title, note in cols:
        card(d, k, x, 260, 474, 1034, name=f"Card {n}")
        art = icon("sprout", 130, rgb(GREEN)) if ic == "sprout" else tint(lineart(COMPOST, 190), GREEN)
        d.put(k, f"Line art {n}", art, x + 50 - (30 if ic != "sprout" else 0), 300, shadowed=False, anchor="tl")
        head(d, k, f"Number {n}", n, x + 50, 470, 380, 130, GREEN)
        y = body(d, k, f"Text {n}", sub, x + 50, 615, 380, 52)
        y = label(d, k, f"Program {n}", title, x + 50, round(y) + 45, 380, 52, GREEN)
        body(d, k, f"Note {n}", note, x + 50, round(y) + 25, 380, 46)


def s8(d, k):
    d.bg(k, leaf(), name="Background: green leaf texture")
    d.put(k, "Photo in arch", arch(PH["lab"], 420, 1060, 0.45, 0.5), 604, 150, shadowed=True, anchor="tl")
    card(d, k, 56, 150, 520, 1060)
    label(d, k, "Eyebrow", "FOR OUR STUDENTS", 104, 195, 440, 50)
    head(d, k, "Headline", "A BETTER\nPLACE TO\nLEARN", 104, 255, 440, 74, BROWN)
    items = [("phone", "Student mobile app"), ("microscope", "Updated Microbe Library"),
             ("laptop", "New learning platform"), ("people", "Free public community")]
    y = 560
    for kind, t in items:
        d.put(k, f"Icon {kind}", icon(kind, 68, rgb(GREEN)), 104, y + 4, shadowed=False, anchor="tl")
        yy = body(d, k, f"Item {kind}", t, 196, y, 340, 50)
        y = max(round(yy), y + 70) + 40


def s9(d, k):
    bg = leaf()
    bg.alpha_composite(bleed(PH["hills"], 860, 0.5, 0.5, 0.55), (0, 0))
    d.bg(k, bg, name="Hills photo fading into the leaf texture")
    card(d, k, 56, 760, 968, 534)
    label(d, k, "Eyebrow", "OUR GOAL FOR 2027", 120, 810, 840, 52)
    head(d, k, "Number", "100,000", 120, 870, 840, 160, GREEN)
    label(d, k, "Label", "ACRES REGENERATED", 120, 1045, 840, 60, BROWN)
    body(d, k, "Text", "by our community of students and graduates", 120, 1125, 760, 52)


def s10(d, k):
    bg = leaf()
    m = Image.open(MYC).convert("RGBA").resize((860, 860), Image.LANCZOS).crop((0, 0, 860, 690))
    a = np.asarray(m).astype(np.float32)
    a[..., 3] *= 0.5
    bg.alpha_composite(Image.fromarray(a.astype("uint8")), (110, 30))
    d.bg(k, bg, name="Leaf texture with the mycelium drawing")
    label(d, k, "Eyebrow", "GIVING TUESDAY", 60, 650, 960, 54, MINT, "center")
    head(d, k, "Headline", "$100,000\nMATCH", 60, 720, 960, 120, CREAM, "center")
    body(d, k, "Text", "Every gift is doubled.", 60, 1005, 960, 56, CREAM, "center")
    f = ImageFont.truetype("/home/user/fonts/Montserrat-Bold.ttf", 52)
    bw, bh = round(f.getlength("Donate today") + 130), 112
    im = Image.new("RGBA", (bw * 3, bh * 3), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, bw * 3 - 1, bh * 3 - 1), bh * 3 // 2, fill=GOLD + (255,))
    x = (W - bw) // 2
    d.put(k, "Donate button", im.resize((bw, bh), Image.LANCZOS), x, 1115, shadowed=True, anchor="tl")
    d.text(k, "Donate button text", "Donate today", x, 1139, bw, 70, 52, kind="montserrat-bold", italic=False,
           color=BROWN, align="center", lh=1.1, min_size=52)


def build(v):
    d = Deck("yb20261201", 10, f"year-one-giving-tuesday-brand-{v}", "2026-12-01")
    for k, fn in enumerate((s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)):
        fn(d, k)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
