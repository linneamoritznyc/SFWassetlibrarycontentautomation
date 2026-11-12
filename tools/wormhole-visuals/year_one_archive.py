"""Giving Tuesday "Year one", archival edition. Allison's final text.

A natural-history field journal: aged paper and Food Web Green plates, Ernst Haeckel's engravings from Kunstformen
der Natur (1904, public domain, Wikimedia Commons) printed in as ink, IM Fell English for headlines and numbers,
Montserrat caps labels, Source Sans body. Real SFW photos as mounted prints (white border, soft shadow, never cut
through a person). No slide numbers, no gold, logo large and in the same place on every slide.

  python3 tools/wormhole-visuals/year_one_archive.py <version>
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

import year_one_luxe  # noqa: F401  registers the IM Fell fonts with collage
from collage import Deck, cover, fit
from nov_fill import DECKS, TILES
from suzanne_frost import grade
from year_one_v5 import BROWN, COMPOSTP, CREAM, CREAMC, FWG, GREEN, MINT, PH, SOIL, body, caps, duo, icon

W, H = 1080, 1350
M = 90
HK = "/home/user/sfwlib/social/haeckel"
INKG = (21, 104, 38)
LOGO_W = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
LOGO_C = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-colour.png"
FELL = "/home/user/fonts/dl/arch/IMFeENrm28P.ttf"
FELLI = "/home/user/fonts/dl/arch/IMFeENit28P.ttf"

PLATES = {  # file, crop box (fractions), light background?
    "cage": ("Haeckel_Basimycetes.jpg", (0.28, 0.36, 0.74, 0.80), False),
    "stinkhorn": ("Haeckel_Basimycetes.jpg", (0.0, 0.40, 0.28, 0.97), False),
    "fern": ("Haeckel_Filicinae.jpg", (0.12, 0.12, 0.88, 0.82), True),
    "ciliate": ("Haeckel_Ciliata.jpg", (0.30, 0.28, 0.70, 0.56), True),
    "slime": ("Haeckel_Mycetozoa.jpg", (0.33, 0.22, 0.64, 0.86), False),
    "diatom": ("Haeckel_Diatomea.jpg", (0.30, 0.24, 0.70, 0.54), False),
    "lichen": ("Haeckel_Lichenes.jpg", (0, 0, 1, 1), False),
    "fungi": ("Haeckel_Basimycetes.jpg", (0, 0, 1, 1), False),
    "ascomycetes": ("Haeckel_Ascomycetes.jpg", (0, 0, 1, 1), False),
}


# ------------------------------------------------------------------ materials
def ink(key, w, colour, alpha=1.0, gamma=1.0):
    """A Haeckel engraving turned into ink of one colour on transparency."""
    f, b, light = PLATES[key]
    im = Image.open(f"{HK}/{f}").convert("L")
    im = im.crop((int(b[0] * im.width), int(b[1] * im.height), int(b[2] * im.width), int(b[3] * im.height)))
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    if light:
        a = 1 - a
    lo, hi = np.percentile(a, 8), np.percentile(a, 99.5)
    a = np.clip((a - lo) / (hi - lo + 1e-6), 0, 1) ** gamma
    out = np.zeros((im.height, w, 4), np.uint8)
    out[..., :3] = colour
    if b != (0, 0, 1, 1):   # single figure: let the edges of the crop melt away
        hh, ww = a.shape
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        r = np.hypot((xx - ww / 2) / (ww / 2), (yy - hh / 2) / (hh / 2))
        a = a * np.clip((1.0 - r) / 0.25, 0, 1)
    out[..., 3] = (a * 255 * alpha).astype("uint8")
    return Image.fromarray(out)


def paper(seed=0):
    """Aged paper: cream with fibres, faint foxing and darker edges."""
    rng = np.random.default_rng(seed)
    base = np.array((241, 235, 221), np.float32)
    lo = rng.normal(0, 1, (H // 30 + 2, W // 30 + 2)).astype(np.float32)
    lo = np.asarray(Image.fromarray(((lo * 40) + 128).clip(0, 255).astype("uint8")).resize((W, H), Image.BICUBIC)
                    .filter(ImageFilter.GaussianBlur(30))).astype(np.float32) / 128 - 1
    fib = rng.normal(0, 1, (H, W)).astype(np.float32)
    fib = np.asarray(Image.fromarray(((fib * 50) + 128).clip(0, 255).astype("uint8")).filter(
        ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 128 - 1
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    edge = np.clip(np.minimum(np.minimum(xx, W - xx), np.minimum(yy, H - yy)) / 140, 0, 1)
    tone = 1 + 0.025 * lo + 0.02 * fib - 0.06 * (1 - edge) ** 2
    a = base * tone[..., None]
    a[..., 2] -= 6 * (1 - edge) ** 2      # warmer at the edges
    straw = np.asarray(cover(Image.open("/home/user/sfwlib/social/cic/straw-linnea.jpg").convert("L"), W, H, 0.5,
                             0.3 + 0.1 * seed)).astype(np.float32) / 255
    a *= (0.97 + 0.05 * straw)[..., None]
    return Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")


def green_plate(src=COMPOSTP, fy=0.4, plate=None, plate_alpha=0.16, plate_w=1200, px=-60, py=-40):
    g = duo(src, (14, 74, 29), (30, 112, 50), 0.5, fy, 0.8)
    if plate:
        g.alpha_composite(ink(plate, plate_w, (244, 241, 234), plate_alpha), (px, py))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.25 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 2
    a = np.asarray(g).astype(np.float32)
    a[..., :3] *= v[..., None]
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


def print_photo(path, w, h, fx=0.5, fy=0.5, border=16):
    """A mounted photographic print: cream border, photo inside."""
    im = cover(grade(ImageOps.exif_transpose(Image.open(path)).convert("RGB")), w - 2 * border, h - 2 * border,
               fx, fy)
    out = Image.new("RGBA", (w, h), (250, 248, 242, 255))
    out.paste(im, (border, border))
    return out


def photo_full(path, h, fx, fy):
    """Full-width photo of height h, keeping the full width of the frame (no one cut at the sides)."""
    return cover(grade(ImageOps.exif_transpose(Image.open(path)).convert("RGB")), W, h, fx, fy).convert("RGBA")


def fade_into(bg, im, y0, fade=0.28):
    a = np.asarray(im).astype(np.float32)
    h = im.height
    y = np.linspace(0, 1, h, dtype=np.float32)
    t = np.clip((y - (1 - fade)) / fade, 0, 1)
    a[..., 3] = 255 * (1 - t * t * (3 - 2 * t))[:, None]
    bg.alpha_composite(Image.fromarray(a.astype("uint8")), (0, y0))
    return bg


# ------------------------------------------------------------------ type
def serif(d, k, name, s, x, y, w, size, colour, italic=False, align="left", lh=1.02):
    _, lines, _ = fit(s, "fell", italic, w, 5000, size, size, lh)
    return d.text(k, name, s, x, y, w, len(lines) * size * lh + 12, size, kind="fell", italic=italic, color=colour,
                  lh=lh, align=align, min_size=size)


def logo(d, k, dark, w=190):
    lg = Image.open(LOGO_W if dark else LOGO_C).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 70 - w, H - 60 - lg.height, shadowed=False, anchor="tl")


def button(d, k, x, y, on_dark=True):
    f = ImageFont.truetype("/home/user/fonts/Montserrat-Bold.ttf", 52)
    bw, bh = round(f.getlength("Donate today") + 140), 116
    im = Image.new("RGBA", (bw * 3, bh * 3), (0, 0, 0, 0))
    fill = CREAMC if on_dark else INKG
    ImageDraw.Draw(im).rounded_rectangle((0, 0, bw * 3 - 1, bh * 3 - 1), bh * 3 // 2, fill=fill + (255,))
    d.put(k, "Donate button", im.resize((bw, bh), Image.LANCZOS), x, y, shadowed=True, anchor="tl")
    d.text(k, "Donate button text", "Donate today", x, y + 26, bw, 70, 52, kind="montserrat-bold", italic=False,
           color=FWG if on_dark else CREAM, align="center", lh=1.1, min_size=52)


# ------------------------------------------------------------------ the thermometer, redrawn as an instrument
def instrument(D, f=0.0):
    k = 3
    S = D * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = S / 2
    dr.ellipse((0, 0, S - 1, S - 1), fill=(236, 226, 205, 255))
    dr.ellipse((10 * k, 10 * k, S - 10 * k, S - 10 * k), outline=INKG + (255,), width=3 * k)
    dr.ellipse((22 * k, 22 * k, S - 22 * k, S - 22 * k), fill=(248, 245, 236, 255), outline=INKG + (255,),
               width=1 * k)
    A0, A1 = 225, -45
    lab = ImageFont.truetype(FELL, int(S * 0.062))
    for i in range(41):
        t = i / 40
        a = math.radians(A0 + (A1 - A0) * t)
        r1 = c - 44 * k
        r0 = r1 - (40 * k if i % 10 == 0 else 22 * k if i % 5 == 0 else 12 * k)
        dr.line((c + r0 * math.cos(a), c - r0 * math.sin(a), c + r1 * math.cos(a), c - r1 * math.sin(a)),
                fill=INKG + (255,), width=(4 if i % 10 == 0 else 2) * k)
        if i % 10 == 0:
            s = "$0" if i == 0 else f"${i * 25 // 10}k" if i < 40 else "$100k"
            rl = r0 - S * 0.085
            tw = dr.textlength(s, font=lab)
            dr.text((c + rl * math.cos(a) - tw / 2, c - rl * math.sin(a) - S * 0.04), s, font=lab,
                    fill=(79, 52, 51, 255))
    cap = ImageFont.truetype("/home/user/fonts/Montserrat-SemiBold.ttf", int(S * 0.036))
    t = "GOAL  $100,000"
    dr.text((c - dr.textlength(t, font=cap) / 2, c + S * 0.24), t, font=cap, fill=INKG + (255,))
    a = math.radians(A0 + (A1 - A0) * f)
    L = c - 90 * k
    tip = (c + L * math.cos(a), c - L * math.sin(a))
    tail = (c - 40 * k * math.cos(a), c + 40 * k * math.sin(a))
    dr.line((tail, tip), fill=(79, 52, 51, 255), width=5 * k)
    dr.ellipse((c - 22 * k, c - 22 * k, c + 22 * k, c + 22 * k), fill=(79, 52, 51, 255))
    dr.ellipse((c - 8 * k, c - 8 * k, c + 8 * k, c + 8 * k), fill=(248, 245, 236, 255))
    return im.resize((D, D), Image.LANCZOS)


# ------------------------------------------------------------------ slides
def s1(d, k):
    d.bg(k, green_plate(COMPOSTP, 0.35, "fungi", 0.13, 1240, -80, -60), name="Green plate with Haeckel fungi")
    caps(d, k, "Eyebrow", "SOIL FOOD WEB FOUNDATION", M, 110, 900, 44, MINT, "center", 6)
    serif(d, k, "Headline", "Giving Tuesday", 40, 170, 1000, 150, CREAM, True, "center")
    body(d, k, "Subline", "What we grew together in our first year", 40, 352, 1000, 56, CREAM, "center")
    D = 620
    x, y = (W - D) // 2, 500
    d.put(k, "Thermometer dial", instrument(D), x, y, shadowed=True, anchor="tl")
    sw, sh = 26, 110
    st = Image.new("RGBA", (sw * 4, sh * 4), (0, 0, 0, 0))
    ImageDraw.Draw(st).polygon([(0, 0), (sw * 4, 0), (sw * 4, (sh - 26) * 4), (sw * 2, sh * 4), (0, (sh - 26) * 4)],
                               fill=(236, 226, 205, 255))
    d.put(k, "Thermometer stem", st.resize((sw, sh), Image.LANCZOS), (W - sw) // 2, y + D - 6, shadowed=False,
          anchor="tl")
    logo(d, k, True)


def s2(d, k):
    bg = paper(2)
    bg.alpha_composite(ink("diatom", 380, INKG, 0.9), (W - 380 - 50, 30))
    d.bg(k, bg, name="Aged paper with Haeckel diatom")
    caps(d, k, "Eyebrow", "AT A GLANCE", M, 120, 600, 44, "#59A66C")
    serif(d, k, "Headline", "Our first year\nin numbers", M, 175, 600, 96, BROWN, True)
    serif(d, k, "Number", "$300,000+", M - 4, 420, 900, 168, FWG)
    caps(d, k, "Label", "IN SCHOLARSHIPS AWARDED", M, 632, 900, 44, BROWN, "left", 3)
    cells = [("35+", "FREE LIVE EVENTS", M, 715), ("4", "WORKSHOPS", 560, 715),
             ("23", "NUMBER OF COUNTRIES\nREPRESENTED IN OUR PDC", M, 950),
             ("46", "INDIA WORKSHOP\nPARTICIPANTS", 560, 950)]
    for n, lab, x, y in cells:
        serif(d, k, f"Number {n}", n, x - 4, y, 440, 130, FWG)
        caps(d, k, f"Label {n}", lab, x, y + 165, 440, 42, BROWN, "left", 1)


def s3(d, k):
    bg = paper(3)
    d.bg(k, bg, name="Aged paper")
    d.put(k, "Photo print", print_photo(PH["scholar"], 900, 600, 0.5, 0.45), M, 90, shadowed=True, anchor="tl")
    caps(d, k, "Eyebrow", "OPENING THE DOOR", M, 760, 900, 44, "#59A66C")
    serif(d, k, "Number", "$300,000+", M - 4, 812, 900, 168, FWG)
    body(d, k, "Text", "in scholarships awarded for our various courses and workshops", M, 1010, 700, 56, BROWN)
    logo(d, k, False)


def s4(d, k):
    bg = paper(4)
    d.bg(k, bg, name="Aged paper")
    serif(d, k, "Big 4", "4", M - 10, 60, 380, 400, FWG)
    caps(d, k, "Eyebrow", "IN PERSON", 470, 150, 520, 44, "#59A66C")
    serif(d, k, "Headline", "Workshops\non 4\ncontinents", 470, 200, 520, 84, BROWN, True)
    places = [("cr", "COSTA\nRICA", "Oct 2025", 0.5, 0.35), ("us", "UNITED\nSTATES", "Feb 2026", 0.55, 0.45),
              ("uk", "ENGLAND", "Jun 2026", 0.5, 0.4), ("india_walk", "INDIA", "Oct 2026", 0.45, 0.4)]
    gap = 16
    pw, ph = (W - 2 * M - 3 * gap) // 4, 330
    for i, (key, name, date, fx, fy) in enumerate(places):
        x = M + i * (pw + gap)
        d.put(k, f"Photo print {i + 1}", print_photo(PH[key], pw, ph, fx, fy, 10), x, 560, shadowed=True,
              anchor="tl")
        caps(d, k, f"Place {i + 1}", name, x, 916 + (0 if "\n" in name else 52), pw + 12, 40, FWG, "left", 0)
        serif(d, k, f"Date {i + 1}", date, x, 1022, pw + 10, 46, BROWN, True)
    body(d, k, "Text", "Hands-on training with our mentors, on four farms", M, 1130, 680, 54, BROWN)
    logo(d, k, False)


def s5(d, k):
    bg = green_plate(SOIL, 0.3)
    bg = fade_into(bg, photo_full(PH["india_group"], 760, 0.5, 0.3), 0, 0.3)
    d.bg(k, bg, name="India photo fading into the green plate")
    caps(d, k, "Eyebrow", "FIRST WORKSHOP IN INDIA", M, 745, 900, 44, MINT)
    serif(d, k, "Number 46", "46", M - 4, 790, 430, 160, CREAM)
    body(d, k, "Text 46", "participants from 10 countries", M, 978, 400, 54, CREAM)
    serif(d, k, "Number 61", "61", 560, 790, 430, 160, CREAM)
    body(d, k, "Text 61", "at the Life in the Soils seminar", 560, 978, 400, 54, CREAM)
    body(d, k, "Partner line", "We partnered with Isha Foundation and Save Soil", M, 1180, 620, 46, MINT)
    logo(d, k, True)


def s6(d, k):
    bg = green_plate(COMPOSTP, 0.3, "lichen", 0.12, 1240, -80, -40)
    d.bg(k, bg, name="Green plate with Haeckel lichens")
    serif(d, k, "Number", "35+", M - 6, 90, 520, 300, CREAM)
    caps(d, k, "Label", "FREE\nLIVE\nEVENTS", 600, 160, 400, 62, MINT, "left", 6)
    d.put(k, "Haeckel slime mould", ink("slime", 220, (244, 241, 234), 0.9), W - 80 - 220, 560, shadowed=False,
          anchor="tl")
    caps(d, k, "Eyebrow", "SOME OF OUR WEBINAR GUESTS:", M, 500, 900, 44, MINT, "left", 2)
    body(d, k, "Guests", "Vandana Shiva\nGeoff Lawton\nNicole Masters\nMary Reynolds\nDavid Holmgren\nDr. Mary Cole",
         M, 585, 600, 62, CREAM)
    logo(d, k, True)


def s7(d, k):
    bg = paper(7)
    d.bg(k, bg, name="Aged paper")
    caps(d, k, "Eyebrow", "NEW PROGRAMS", M, 110, 900, 44, "#59A66C")
    serif(d, k, "Headline", "Two new ways to learn", M, 160, 900, 96, BROWN, True)
    cols = [(M, "fern", "100", "students from 23 countries", "PERMACULTURE\nDESIGN\nCERTIFICATE",
             "With the Permaculture Association (UK)"),
            (560, "cage", "10", "weeks, live online", "COMPOST\nINTENSIVE COURSE",
             "No prerequisites, with Spanish transcriptions")]
    for x, plate, n, sub, title, note in cols:
        art = ink(plate, 230, INKG, 0.95)
        art = art.crop((0, 0, 230, min(art.height, 260)))
        d.put(k, f"Haeckel {plate}", art, x, 300, shadowed=False, anchor="tl")
        serif(d, k, f"Number {n}", n, x - 4, 570, 420, 150, FWG)
        y = body(d, k, f"Text {n}", sub, x, 735, 400, 52)
        y = caps(d, k, f"Program {n}", title, x, round(y) + 30, 420, 42, FWG, "left", 1)
        body(d, k, f"Note {n}", note, x, round(y) + 16, 400, 46)


def s8(d, k):
    bg = green_plate(SOIL, 0.5)
    bg = fade_into(bg, photo_full(PH["lab"], 720, 0.5, 0.28), 0, 0.3)
    d.bg(k, bg, name="Microscopy class photo fading into the green plate")
    caps(d, k, "Eyebrow", "FOR OUR STUDENTS", M, 740, 900, 44, MINT)
    serif(d, k, "Headline", "A better place to learn", M, 790, 900, 92, CREAM, True)
    items = [("phone", "Student mobile app"), ("microscope", "Updated Microbe Library"),
             ("laptop", "New learning platform"), ("people", "Free public community")]
    for i, (kind, t) in enumerate(items):
        x, y = (M, 560)[i % 2], 935 + (i // 2) * 150
        d.put(k, f"Icon {kind}", icon(kind, 54, (207, 230, 211)), x, y + 2, shadowed=False, anchor="tl")
        body(d, k, f"Item {kind}", t, x + 76, y, 380, 50, CREAM)


def s9(d, k):
    bg = green_plate(SOIL, 0.8)
    bg = fade_into(bg, photo_full(PH["hills"], 900, 0.5, 0.5), 0, 0.32)
    d.bg(k, bg, name="Hills photo fading into the green plate")
    caps(d, k, "Eyebrow", "OUR GOAL FOR 2027", M, 790, 900, 44, MINT)
    serif(d, k, "Number", "100,000", M - 6, 835, 900, 190, CREAM)
    caps(d, k, "Label", "ACRES REGENERATED", M, 1075, 900, 54, CREAM, "left", 5)
    body(d, k, "Text", "by our community of students and graduates", M, 1150, 620, 50, MINT)
    logo(d, k, True)


def s10(d, k):
    bg = green_plate(COMPOSTP, 0.75, "ascomycetes", 0.13, 1240, -80, -60)
    d.bg(k, bg, name="Green plate with Haeckel cup fungi")
    caps(d, k, "Eyebrow", "GIVING TUESDAY", M, 200, 900, 46, MINT, "left", 6)
    serif(d, k, "Headline", "$100,000\nmatch", M - 6, 260, 900, 200, CREAM)
    body(d, k, "Text", "Every gift is doubled.", M, 700, 900, 64, CREAM)
    button(d, k, M, 820)
    logo(d, k, True, 220)


def build(v):
    d = Deck("yar20261201", 10, f"year-one-giving-tuesday-archive-{v}", "2026-12-01")
    for k, fn in enumerate((s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)):
        fn(d, k)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
