"""Giving Tuesday "Year one", final direction (brand fonts only, no slide numbers, no gold, big logo in one place,
Unsplash photos as design elements, credits in sfwlib/social/unsplash/credits.txt). Built from the Swiss edition. Allison's final text, one system on all 10 slides:
- grid: 90 px margins, two columns (90-520, 560-990), baseline steps of 8 px
- section label top left on most slides; no slide numbers, no rules
- type scale: display 300 / 150 / 72 (Montserrat Light), labels 42-60 (Montserrat SemiBold caps), body 52-56 (Source Sans)
- grounds: Linnea's textures in brand colours (straw in cream, compost and soil in Food Web Green), real photos
  full width across the top so no one is cropped
- thermometer on slide 1; no gold anywhere (cream Donate button)

  python3 tools/wormhole-visuals/year_one_swiss.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from collage import Deck, cover
from nov_fill import DECKS, TILES
from suzanne_frost import grade
from year_one_v5 import (BROWN, COMPOSTP, CREAM, CREAMC, FWG, GOLD, GREEN, LAPTOP, COMPOST, LEAFG, MINT, PH, SOIL,
                         body, caps, cream_ground, display, duo, icon, lineart, tint)

W, H = 1080, 1350
M, C2, R = 90, 560, 990          # margin, second column, right edge
LOGO_W = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
US = "/home/user/sfwlib/social/unsplash"
LOGO_C = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-colour.png"


def green(src=COMPOSTP, fy=0.4):
    return duo(src, (14, 78, 30), (34, 122, 54), 0.5, fy, 1.0)


def header(d, k, label, dark):
    if label:
        caps(d, k, "Section label", label, M, 96, 900, 44, MINT if dark else FWG, "left", 3)


def photo_top(bg, path, h, fx, fy, top_shade=False, y0=180):
    im = cover(grade(ImageOps.exif_transpose(Image.open(path)).convert("RGB")), W, h, fx, fy)
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    y = np.linspace(0, 1, h, dtype=np.float32)
    t = np.clip((y - 0.72) / 0.28, 0, 1)
    a[..., 3] = 255 * (1 - t * t * (3 - 2 * t))[:, None]
    if top_shade:  # soft darkening under the header so it reads
        s = np.clip(1 - y / 0.22, 0, 1)[:, None, None] * 0.45
        a[..., :3] = a[..., :3] * (1 - s) + np.array((10, 40, 18), np.float32) * s
    bg.alpha_composite(Image.fromarray(a.clip(0, 255).astype("uint8")), (0, y0))
    return bg


def logo(d, k, x=None, y=None, w=170, colour=False):
    """Same size, same place on every slide: bottom right, 70 px in."""
    lg = Image.open(LOGO_C if colour else LOGO_W).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 70 - w, H - 60 - lg.height, shadowed=False, anchor="tl")


def us(name, w, h, fx=0.5, fy=0.5):
    return cover(grade(Image.open(f"{US}/{name}.jpg").convert("RGB")), w, h, fx, fy).convert("RGBA")


def melt(im, left=0.0, bottom=0.0, top=0.0):
    """Fade an image's edges to transparent (fractions of its size)."""
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    m = np.ones((h, w), np.float32)
    if left:
        m *= np.clip(xx / (w * left), 0, 1)
    if bottom:
        m *= np.clip((h - yy) / (h * bottom), 0, 1)
    if top:
        m *= np.clip(yy / (h * top), 0, 1)
    m = m * m * (3 - 2 * m)
    a[..., 3] *= m
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


def card(d, k, x, y, w, h):
    im = Image.new("RGBA", (w * 3, h * 3), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), 72, fill=CREAMC + (255,))
    d.put(k, "Cream card", im.resize((w, h), Image.LANCZOS), x, y, shadowed=True, anchor="tl")


def accent(d, k, x, y, colour=GREEN, w=90):
    d.put(k, "Accent line", Image.new("RGBA", (w, 4), colour + (255,)), x, y, shadowed=False, anchor="tl")


# ------------------------------------------------------------------ slides
def s1(d, k):
    from giving_thermometer import dial, needle
    d.bg(k, green(COMPOSTP, 0.35), name="Compost texture in Food Web Green")
    header(d, k, "SOIL FOOD WEB FOUNDATION", True)
    display(d, k, "Headline", "GIVING\nTUESDAY", M - 6, 196, 900, 124, CREAM, "left", 4)
    body(d, k, "Subline", "What we grew together in our first year", M, 470, 660, 54, CREAM)
    D = 560
    x, y = (W - D) // 2, 610
    sw, sh = 30, 110
    st = Image.new("RGBA", (sw * 4, sh * 4), (0, 0, 0, 0))
    ImageDraw.Draw(st).polygon([(0, 0), (sw * 4, 0), (sw * 4, (sh - 26) * 4), (sw * 2, sh * 4), (0, (sh - 26) * 4)],
                               fill=(216, 195, 165, 255))
    d.put(k, "Thermometer stem", st.resize((sw, sh), Image.LANCZOS), x + D // 2 - sw // 2, y + D - 18,
          shadowed=False, anchor="tl")
    d.put(k, "Thermometer dial", dial(D), x, y, shadowed=True, anchor="tl")
    d.put(k, "Needle (rotate around its centre to the current total)", needle(D, 0.0), x, y, shadowed=False,
          anchor="tl")


def s2(d, k):
    bg = cream_ground(0.6)
    bg.alpha_composite(melt(us("wUqiaRLZDiY", 400, 520, 0.6, 0.6), left=0.5, bottom=0.45), (W - 400, 0))
    d.bg(k, bg, name="Straw texture in cream with Unsplash hand-in-soil photo melting in")
    header(d, k, "AT A GLANCE", False)
    display(d, k, "Headline", "OUR FIRST YEAR\nIN NUMBERS", M - 4, 160, 620, 66, BROWN, "left", 2)
    display(d, k, "Number", "$300,000+", M - 8, 360, 920, 150, FWG, "left", 0)
    caps(d, k, "Label", "IN SCHOLARSHIPS AWARDED", M, 536, 900, 42, BROWN, "left", 3)
    cells = [("35+", "FREE LIVE EVENTS", M, 640), ("4", "WORKSHOPS", C2, 640),
             ("23", "NUMBER OF COUNTRIES\nREPRESENTED IN OUR PDC", M, 870), ("46", "INDIA WORKSHOP\nPARTICIPANTS", C2, 870)]
    for n, lab, x, y in cells:
        display(d, k, f"Number {n}", n, x - 6, y, 430, 120, FWG, "left", 0)
        caps(d, k, f"Label {n}", lab, x, y + 140, 430, 42, BROWN, "left", 1)


def s3(d, k):
    bg = photo_top(green(SOIL, 0.6), PH["scholar"], 700, 0.5, 0.45)
    d.bg(k, bg, name="Scholarship photo fading into the soil texture")
    header(d, k, "OPENING THE DOOR", True)
    display(d, k, "Number", "$300,000+", M - 8, 860, 920, 150, CREAM, "left", 0)
    accent(d, k, M, 1046, (207, 230, 211))
    body(d, k, "Text", "in scholarships awarded for our various courses and workshops", M, 1076, 700, 54, CREAM)


def s4(d, k):
    d.bg(k, cream_ground(0.2), name="Straw texture in cream")
    header(d, k, "IN PERSON", False)
    display(d, k, "Big 4", "4", M - 10, 150, 400, 330, FWG, "left", 0)
    display(d, k, "Headline", "WORKSHOPS\nON 4\nCONTINENTS", C2 - 4, 200, 430, 66, BROWN, "left", 4)
    places = [("cr", "COSTA\nRICA", "Oct 2025", 0.5, 0.35), ("us", "UNITED\nSTATES", "Feb 2026", 0.55, 0.45),
              ("uk", "ENGLAND", "Jun 2026", 0.5, 0.4), ("india_walk", "INDIA", "Oct 2026", 0.45, 0.4)]
    gap = 20
    pw, ph = (R - M - 3 * gap) // 4, 400
    for i, (key, name, date, fx, fy) in enumerate(places):
        x = M + i * (pw + gap)
        im = cover(grade(ImageOps.exif_transpose(Image.open(PH[key])).convert("RGB")), pw, ph, fx, fy).convert("RGBA")
        d.put(k, f"Photo {i + 1}", im, x, 520, shadowed=False, anchor="tl")
        caps(d, k, f"Place {i + 1}", name, x, 944 + (0 if "\n" in name else 52), pw + 10, 40, FWG, "left", 0)
        body(d, k, f"Date {i + 1}", date, x, 1050, pw, 44, BROWN)
    d.put(k, "Rule", Image.new("RGBA", (R - M, 2), (89, 166, 108, 255)), M, 1140, shadowed=False, anchor="tl")
    body(d, k, "Text", "Hands-on training with our mentors, on four farms", M, 1150, 690, 52)


def s5(d, k):
    bg = photo_top(green(SOIL, 0.3), PH["india_group"], 720, 0.5, 0.3)
    d.bg(k, bg, name="India photo fading into the soil texture")
    header(d, k, "FIRST WORKSHOP IN INDIA", True)
    display(d, k, "Number 46", "46", M - 6, 820, 430, 150, CREAM, "left", 0)
    body(d, k, "Text 46", "participants from 10 countries", M, 986, 420, 52, CREAM)
    display(d, k, "Number 61", "61", C2 - 6, 820, 430, 150, CREAM, "left", 0)
    body(d, k, "Text 61", "at the Life in the Soils seminar", C2, 986, 400, 52, CREAM)
    accent(d, k, M, 1190, (207, 230, 211))
    body(d, k, "Partner line", "We partnered with Isha Foundation and Save Soil", M, 1190, 690, 44, MINT)


def s6(d, k):
    bg = green(COMPOSTP, 0.3)
    bg.alpha_composite(melt(us("PuzohkVDJDY", 420, 520, 0.5, 0.55), left=0.55, top=0.25, bottom=0.35), (W - 420, 380))
    d.bg(k, bg, name="Compost texture in green with Unsplash mushrooms melting in")
    display(d, k, "Number", "35+", M - 10, 170, 470, 270, CREAM, "left", 0)
    caps(d, k, "Label", "FREE\nLIVE\nEVENTS", C2, 226, 430, 60, MINT, "left", 6)
    art = lineart(LAPTOP, 900)
    art = art.crop(art.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox())
    art = art.resize((460, round(art.height * 460 / art.width)), Image.LANCZOS)
    d.put(k, "Laptop line art", art, M, 600 - art.height // 2, shadowed=False, anchor="tl")
    cx, cy, cw, ch = M, 760, R - M, 370
    card(d, k, cx, cy, cw, ch)
    caps(d, k, "Eyebrow", "SOME OF OUR WEBINAR GUESTS:", cx + 50, cy + 48, cw - 80, 42, FWG, "left", 1)
    accent(d, k, cx + 50, cy + 112)
    body(d, k, "Guests 1", "Vandana Shiva\nGeoff Lawton\nNicole Masters", cx + 50, cy + 136, 420, 54, BROWN)
    body(d, k, "Guests 2", "Mary Reynolds\nDavid Holmgren\nDr. Mary Cole", C2, cy + 136, 400, 54, BROWN)


def s7(d, k):
    d.bg(k, cream_ground(0.8), name="Straw texture in cream")
    header(d, k, "NEW PROGRAMS", False)
    display(d, k, "Headline", "TWO NEW WAYS TO LEARN", M - 4, 160, 920, 60, BROWN, "left", 2)
    cols = [(M, "TBjNbj1sdAE", 0.5, 0.6, "100", "students from 23 countries", "PERMACULTURE\nDESIGN\nCERTIFICATE",
             "With the Permaculture Association (UK)"),
            (C2, "j4fV6dKT9tw", 0.5, 0.75, "10", "weeks, live online", "COMPOST\nINTENSIVE COURSE",
             "No prerequisites, with Spanish transcriptions")]
    for x, ph, fx, fy, n, sub, title, note in cols:
        d.put(k, f"Photo {n}", us(ph, 430, 280, fx, fy), x, 250, shadowed=True, anchor="tl")
        display(d, k, f"Number {n}", n, x - 6, 550, 420, 140, FWG, "left", 0)
        y = body(d, k, f"Text {n}", sub, x, 700, 400, 52)
        y = caps(d, k, f"Program {n}", title, x, round(y) + 34, 410, 42, FWG, "left", 1)
        body(d, k, f"Note {n}", note, x, round(y) + 16, 390, 46)


def s8(d, k):
    bg = photo_top(green(SOIL, 0.5), PH["lab"], 700, 0.5, 0.28)
    d.bg(k, bg, name="Microscopy class photo fading into the soil texture")
    header(d, k, "FOR OUR STUDENTS", True)
    display(d, k, "Headline", "A BETTER PLACE\nTO LEARN", M - 4, 780, 920, 72, CREAM, "left", 3)
    items = [("phone", "Student mobile app"), ("microscope", "Updated Microbe Library"),
             ("laptop", "New learning platform"), ("people", "Free public community")]
    for i, (kind, t) in enumerate(items):
        x, y = M, 960 + i * 72
        d.put(k, f"Icon {kind}", icon(kind, 56, (207, 230, 211)), x, y + 4, shadowed=False, anchor="tl")
        body(d, k, f"Item {kind}", t, x + 76, y, 640, 48, CREAM)


def s9(d, k):
    bg = photo_top(green(SOIL, 0.8), PH["hills"], 880, 0.5, 0.5, True, 0)
    d.bg(k, bg, name="Hills photo fading into the soil texture")
    header(d, k, "OUR GOAL FOR 2027", True)
    display(d, k, "Number", "100,000", M - 8, 860, 920, 180, CREAM, "left", 0)
    caps(d, k, "Label", "ACRES REGENERATED", M, 1070, 900, 52, CREAM, "left", 4)
    body(d, k, "Text", "by our community of students and graduates", M, 1150, 680, 52, MINT)


def s10(d, k):
    bg = green(COMPOSTP, 0.75)
    sp = us("iXjKR1-v-nQ", W, H, 0.5, 0.6)
    a = np.asarray(sp).astype(np.float32)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    t = np.clip((0.62 - yy) / 0.5, 0, 1)
    a[..., 3] = 255 * (1 - t * t * (3 - 2 * t))
    bg.alpha_composite(Image.fromarray(a.astype("uint8")))
    d.bg(k, bg, name="Unsplash seedling rising out of the green")
    header(d, k, "GIVING TUESDAY", True)
    display(d, k, "Headline", "$100,000\nMATCH", M - 8, 170, 920, 170, CREAM, "left", 2)
    body(d, k, "Text", "Every gift is doubled.", M, 560, 900, 60, CREAM)
    f = ImageFont.truetype("/home/user/fonts/Montserrat-Bold.ttf", 52)
    bw, bh = round(f.getlength("Donate today") + 140), 116
    im = Image.new("RGBA", (bw * 3, bh * 3), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, bw * 3 - 1, bh * 3 - 1), bh * 3 // 2, fill=CREAMC + (255,))
    d.put(k, "Donate button (cream)", im.resize((bw, bh), Image.LANCZOS), M, 680, shadowed=True, anchor="tl")
    d.text(k, "Donate button text", "Donate today", M, 706, bw, 70, 52, kind="montserrat-bold", italic=False,
           color=FWG, align="center", lh=1.1, min_size=52)


def build(v):
    d = Deck("yfin20261201", 10, f"year-one-giving-tuesday-{v}", "2026-12-01")
    for k, fn in enumerate((s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)):
        fn(d, k)
        logo(d, k, colour=k in (1, 3, 6))
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
