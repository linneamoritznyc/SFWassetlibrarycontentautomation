"""Giving Tuesday "Year one" carousel, take 5. Allison's final text. Built on Linnea's own textures (straw, soil,
compost photos she sent) toned into brand colours: Food Web Green duotone for green slides, cream/sand duotone for
light slides. Montserrat Light display type with wide tracking, Montserrat SemiBold small caps, Source Sans body,
Soil Brown on cream. Real photos full-bleed with soft fades. No boxes, no rules. Thermometer on slide 1. Gold only
on the Donate button.

  python3 tools/wormhole-visuals/year_one_v5.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import collage
from collage import Deck, cover, fit
from nov_fill import DECKS, TILES
from year_one_luxe import PH, LAPTOP, COMPOST, icon, lineart
from suzanne_frost import grade
from PIL import ImageOps

collage.FONT_FILES[("mont-light", False)] = "Montserrat-Light.ttf"
collage.PPT_FONT["mont-light"] = "Montserrat Light"

W, H = 1080, 1350
GREEN = (21, 104, 38)
CREAMC = (244, 241, 234)
BROWN = "#4F3433"
FWG = "#156826"
LEAFG = "#59A66C"
CREAM = "#F4F1EA"
MINT = "#CFE6D3"
GOLD = (201, 162, 39)
T = "/home/user/sfwlib/social/cic"
STRAW, SOIL, COMPOSTP = f"{T}/straw-linnea.jpg", f"{T}/soil-linnea.jpg", f"{T}/compost-linnea.jpg"
LOGO_W = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
LOGO_C = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-colour.png"


def duo(path, dark, light, fx=0.5, fy=0.5, contrast=1.0):
    g = np.asarray(cover(Image.open(path).convert("L"), W, H, fx, fy)).astype(np.float32) / 255
    g = np.clip((g - g.mean()) * contrast + 0.5, 0, 1)[..., None]
    a = np.array(dark, np.float32) * (1 - g) + np.array(light, np.float32) * g
    return Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")


def green_ground(src=COMPOSTP, fy=0.5):
    return duo(src, (12, 74, 28), (40, 132, 62), 0.5, fy, 1.3)


def cream_ground(fy=0.5):
    return duo(STRAW, (226, 214, 192), (247, 244, 237), 0.5, fy, 0.9)


def photo_fade(path, fx, fy, f0, f1, colour=(12, 60, 26), strength=0.9):
    im = cover(grade(ImageOps.exif_transpose(Image.open(path)).convert("RGB")), W, H, fx, fy)
    a = np.asarray(im).astype(np.float32)
    y = np.linspace(0, 1, H, dtype=np.float32)
    t = np.clip((y - f0) / (f1 - f0), 0, 1)
    t = (t * t * (3 - 2 * t) * strength)[:, None, None]
    a = a * (1 - t) + np.array(colour, np.float32) * t
    return Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")


def tx(d, k, name, s, x, y, w, size, kind, colour, align="left", lh=None, track=0):
    lh = lh or {"mont-light": 1.02, "montserrat": 1.2, "source-reg": 1.24, "montserrat-bold": 1.02}[kind]
    _, lines, _ = fit(s, kind, False, w, 5000, size, size, lh, track)
    return d.text(k, name, s, x, y, w, len(lines) * size * lh + 12, size, kind=kind, italic=False, color=colour,
                  lh=lh, align=align, min_size=size, track=track)


def display(d, k, name, s, x, y, w, size, colour, align="left", track=2):
    return tx(d, k, name, s, x, y, w, size, "mont-light", colour, align, track=track)


def caps(d, k, name, s, x, y, w, size=42, colour=LEAFG, align="left", track=4):
    return tx(d, k, name, s, x, y, w, size, "montserrat", colour, align, track=track)


def body(d, k, name, s, x, y, w, size=52, colour=BROWN, align="left"):
    return tx(d, k, name, s, x, y, w, size, "source-reg", colour, align)


def logo(d, k, x, y, w=140, colour=False):
    lg = Image.open(LOGO_C if colour else LOGO_W).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def tint(im, colour):
    a = np.asarray(im).copy()
    a[..., :3] = colour
    return Image.fromarray(a)


MICRO = "/home/user/photos/new-2026-10"
SPEC = dict(hypha=f"{MICRO}/Fungal hypha, 100x obj, Marco Trevisan.jpg",
            nema=f"{MICRO}/Bacterial-feeding nematode, 40x obj, Talbot Armstrong.jpg",
            amoeba=f"{MICRO}/Naked amoeba (stellate), flagellate, 40x obj, Jimena Fuentes.jpg",
            testate=f"{MICRO}/Testate amoeba, 40x obj, Joy Kaluf.jpg",
            omni=f"{MICRO}/Bacterial-feeding nematode (omnivore), 40x obj, Keisha Wheeler.jpg")


def specimen(key, D, ring=CREAMC, zoom=1.0):
    """A microscope field of view: the student's micrograph in a circle with a thin ring."""
    k = 3
    im = ImageOps.exif_transpose(Image.open(SPEC[key])).convert("RGB")
    s = int(min(im.size) / zoom)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
    im = im.resize((D * k, D * k), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (D * k, D * k), 0)
    ImageDraw.Draw(m).ellipse((0, 0, D * k - 1, D * k - 1), fill=255)
    im.putalpha(m)
    ImageDraw.Draw(im).ellipse((4 * k, 4 * k, D * k - 4 * k, D * k - 4 * k), outline=ring + (255,), width=5 * k)
    return im.resize((D, D), Image.LANCZOS)


def rect_photo(path, w, h, fx=0.5, fy=0.5):
    return cover(grade(ImageOps.exif_transpose(Image.open(path)).convert("RGB")), w, h, fx, fy).convert("RGBA")


# ------------------------------------------------------------------ slides
def s1(d, k):
    from giving_thermometer import dial, needle
    d.bg(k, green_ground(COMPOSTP, 0.35), name="Background: compost texture in Food Web Green")
    logo(d, k, (W - 150) // 2, 70, 150)
    caps(d, k, "Eyebrow", "SOIL FOOD WEB FOUNDATION", 60, 268, 960, 42, MINT, "center", 6)
    display(d, k, "Headline", "GIVING TUESDAY", 40, 322, 1000, 100, CREAM, "center", 6)
    body(d, k, "Subline", "What we grew together in our first year", 100, 448, 880, 54, CREAM, "center")
    D = 600
    x, y = (W - D) // 2, 578
    sw, sh = 30, 120
    st = Image.new("RGBA", (sw * 4, sh * 4), (0, 0, 0, 0))
    ImageDraw.Draw(st).polygon([(0, 0), (sw * 4, 0), (sw * 4, (sh - 30) * 4), (sw * 2, sh * 4), (0, (sh - 30) * 4)],
                               fill=(216, 195, 165, 255))
    d.put(k, "Thermometer stem", st.resize((sw, sh), Image.LANCZOS), (W - sw) // 2, y + D - 18, shadowed=False,
          anchor="tl")
    d.put(k, "Thermometer dial", dial(D), x, y, shadowed=True, anchor="tl")
    d.put(k, "Needle (rotate around its centre to the current total)", needle(D, 0.0), x, y, shadowed=False,
          anchor="tl")


def s2(d, k):
    d.bg(k, cream_ground(0.6), name="Background: straw texture in cream")
    caps(d, k, "Eyebrow", "AT A GLANCE", 100, 110, 880)
    display(d, k, "Headline", "OUR FIRST YEAR\nIN NUMBERS", 100, 160, 880, 70, BROWN, track=4)
    d.put(k, "Specimen: fungal hypha", specimen("testate", 210, GREEN, 1.2), 810, 70, shadowed=True, anchor="tl")
    display(d, k, "Number", "$300,000+", 92, 360, 900, 150, FWG, track=0)
    caps(d, k, "Label", "IN SCHOLARSHIPS AWARDED", 100, 535, 880, 42, BROWN)
    cells = [("35+", "FREE LIVE EVENTS", 100, 680), ("4", "WORKSHOPS", 580, 680),
             ("23", "NUMBER OF COUNTRIES\nREPRESENTED IN OUR PDC", 100, 960),
             ("46", "INDIA WORKSHOP\nPARTICIPANTS", 580, 960)]
    for n, lab, x, y in cells:
        display(d, k, f"Number {n}", n, x - 6, y, 440, 120, FWG, track=0)
        caps(d, k, f"Label {n}", lab, x, y + 140, 460, 42, BROWN, track=1)


def s3(d, k):
    """Whole group in frame: the photo runs the full width at the top (no one cut), fading into green."""
    bg = green_ground(SOIL, 0.6)
    ph = 760
    im = cover(grade(ImageOps.exif_transpose(Image.open(PH["scholar"])).convert("RGB")), W, ph, 0.5, 0.45)
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    y = np.linspace(0, 1, ph, dtype=np.float32)
    t = np.clip((y - 0.72) / 0.28, 0, 1)
    a[..., 3] = 255 * (1 - t * t * (3 - 2 * t))[:, None]
    bg.alpha_composite(Image.fromarray(a.astype("uint8")), (0, 0))
    d.bg(k, bg, name="Scholarship photo fading into the soil texture")
    caps(d, k, "Eyebrow", "OPENING THE DOOR", 90, 820, 900, 44, MINT)
    display(d, k, "Number", "$300,000+", 82, 878, 920, 150, CREAM, track=0)
    body(d, k, "Text", "in scholarships awarded for our various courses and workshops", 90, 1068, 820, 54, CREAM)


def s4(d, k):
    d.bg(k, cream_ground(0.2), name="Background: straw texture in cream")
    display(d, k, "Big 4", "4", 80, 40, 320, 420, FWG, track=0)
    caps(d, k, "Eyebrow", "IN PERSON", 420, 140, 600, 42, LEAFG)
    display(d, k, "Headline", "WORKSHOPS\nON 4\nCONTINENTS", 420, 190, 600, 66, BROWN, track=4)
    places = [("cr", "COSTA\nRICA", "Oct 2025", 0.5, 0.35), ("us", "UNITED\nSTATES", "Feb 2026", 0.55, 0.45),
              ("uk", "ENGLAND", "Jun 2026", 0.5, 0.4), ("india_walk", "INDIA", "Oct 2026", 0.45, 0.4)]
    pw, ph, gap = 214, 410, 14
    x0 = (W - (4 * pw + 3 * gap)) // 2
    for i, (key, name, date, fx, fy) in enumerate(places):
        x = x0 + i * (pw + gap)
        d.put(k, f"Photo {i + 1}", rect_photo(PH[key], pw, ph, fx, fy), x, 500, shadowed=True, anchor="tl")
        caps(d, k, f"Place {i + 1}", name, x - 6, 945 + (0 if "\n" in name else 52), pw + 12, 42, FWG, "center",
             track=0)
        body(d, k, f"Date {i + 1}", date, x, 1050, pw, 44, BROWN, "center")
    body(d, k, "Text", "Hands-on training with our mentors, on four farms", 100, 1160, 820, 52, BROWN)


def s5(d, k):
    d.bg(k, photo_fade(PH["india_group"], 0.5, 0.25, 0.5, 0.74, strength=0.96), name="India photo with soft fade")
    caps(d, k, "Eyebrow", "FIRST WORKSHOP IN INDIA", 90, 850, 900, 44, MINT)
    display(d, k, "Number 46", "46", 84, 900, 420, 150, CREAM, track=0)
    body(d, k, "Text 46", "participants from 10 countries", 90, 1065, 400, 52, CREAM)
    display(d, k, "Number 61", "61", 574, 900, 420, 150, CREAM, track=0)
    body(d, k, "Text 61", "at the Life in the Soils seminar", 580, 1065, 420, 52, CREAM)
    body(d, k, "Partner line", "We partnered with Isha Foundation and Save Soil", 90, 1225, 960, 44, MINT)


def s6(d, k):
    """Number band on a deepened texture, the laptop drawing on a soft glow, the guests on a cream card."""
    bg = duo(COMPOSTP, (14, 78, 30), (34, 122, 54), 0.5, 0.3, 1.0)
    a = np.asarray(bg).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dark = 0.62 + 0.38 * np.clip(np.hypot((xx - W / 2) / (W * 0.55), (yy - 640) / (H * 0.42)), 0, 1) ** 1.5
    a[..., :3] *= (1.0 - 0.45 * (1 - np.clip(dark, 0, 1)) - 0.25)[..., None] if False else 1.0
    band = np.clip(1 - np.abs(yy - 270) / 260, 0, 1) ** 1.2
    a[..., :3] = a[..., :3] * (1 - 0.35 * band[..., None]) + np.array((8, 40, 18), np.float32) * 0.35 * band[..., None]
    glow = np.exp(-(((xx - W / 2) / 380) ** 2 + ((yy - 660) / 190) ** 2))
    a[..., :3] = a[..., :3] * (1 - 0.30 * glow[..., None]) + np.array((10, 48, 22), np.float32) * 0.30 * glow[..., None]
    d.bg(k, Image.fromarray(a.clip(0, 255).astype("uint8")), name="Compost texture, deepened behind the text")
    display(d, k, "Number", "35+", 80, 40, 470, 270, CREAM, "left", 0)
    caps(d, k, "Label", "FREE\nLIVE\nEVENTS", 560, 102, 430, 60, MINT, "left", 6)
    line = Image.new("RGBA", (900, 3), (207, 230, 211, 200))
    d.put(k, "Mint line", line, 90, 440, shadowed=False, anchor="tl")
    art = lineart(LAPTOP, 900)
    art = art.crop(art.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox())
    art = art.resize((560, round(art.height * 560 / art.width)), Image.LANCZOS)
    d.put(k, "Laptop line art", art, (W - art.width) // 2, 645 - art.height // 2, shadowed=False, anchor="tl")
    cw, ch, cx, cy = 900, 410, 90, 850
    card = Image.new("RGBA", (cw * 3, ch * 3), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, cw * 3 - 1, ch * 3 - 1), 84, fill=CREAMC + (255,))
    d.put(k, "Cream card", card.resize((cw, ch), Image.LANCZOS), cx, cy, shadowed=True, anchor="tl")
    caps(d, k, "Eyebrow", "SOME OF OUR WEBINAR GUESTS:", cx + 50, cy + 52, cw - 80, 42, FWG, "left", 1)
    d.put(k, "Green line", Image.new("RGBA", (90, 4), GREEN + (255,)), cx + 50, cy + 117, shadowed=False, anchor="tl")
    body(d, k, "Guests 1", "Vandana Shiva\nGeoff Lawton\nNicole Masters", cx + 50, cy + 150, 420, 54, BROWN)
    body(d, k, "Guests 2", "Mary Reynolds\nDavid Holmgren\nDr. Mary Cole", 560, cy + 150, 400, 54, BROWN)


def s7(d, k):
    d.bg(k, cream_ground(0.8), name="Background: straw texture in cream")
    d.put(k, "Specimen: testate amoeba", specimen("hypha", 190, GREEN, 1.6), 850, 1110, shadowed=True, anchor="tl")
    caps(d, k, "Eyebrow", "NEW PROGRAMS", 90, 110, 900)
    display(d, k, "Headline", "TWO NEW WAYS TO LEARN", 84, 170, 940, 58, BROWN, track=1)
    cols = [(90, "sprout", "100", "students from 23 countries", "PERMACULTURE\nDESIGN\nCERTIFICATE",
             "With the Permaculture Association (UK)"),
            (580, "compost", "10", "weeks, live online", "COMPOST\nINTENSIVE COURSE",
             "No prerequisites, with Spanish transcriptions")]
    for x, ic, n, sub, title, note in cols:
        art = icon("sprout", 150, GREEN) if ic == "sprout" else tint(lineart(COMPOST, 220), GREEN)
        d.put(k, f"Line art {n}", art, x - (34 if ic != "sprout" else 0), 300 if ic == "sprout" else 270,
              shadowed=False, anchor="tl")
        display(d, k, f"Number {n}", n, x - 6, 480, 420, 150, FWG, track=0)
        y = body(d, k, f"Text {n}", sub, x, 650, 400, 52)
        y = caps(d, k, f"Program {n}", title, x, round(y) + 40, 420, 42, FWG, track=2)
        body(d, k, f"Note {n}", note, x, round(y) + 20, 400, 46)


def s8(d, k):
    """All five people in frame: photo across the top, fading into green; headline left, list right."""
    bg = green_ground(SOIL, 0.5)
    ph = 820
    im = cover(grade(ImageOps.exif_transpose(Image.open(PH["lab"])).convert("RGB")), W, ph, 0.5, 0.3)
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    y = np.linspace(0, 1, ph, dtype=np.float32)
    t = np.clip((y - 0.7) / 0.3, 0, 1)
    a[..., 3] = 255 * (1 - t * t * (3 - 2 * t))[:, None]
    bg.alpha_composite(Image.fromarray(a.astype("uint8")), (0, 0))
    d.bg(k, bg, name="Microscopy class photo fading into the soil texture")
    caps(d, k, "Eyebrow", "FOR OUR STUDENTS", 80, 770, 920, 42, MINT, track=2)
    display(d, k, "Headline", "A BETTER PLACE\nTO LEARN", 76, 822, 920, 70, CREAM, track=3)
    items = [("phone", "Student mobile app"), ("microscope", "Updated Microbe Library"),
             ("laptop", "New learning platform"), ("people", "Free public community")]
    for i, (kind, t) in enumerate(items):
        x, y = 80 + (i % 2) * 480, 1010 + (i // 2) * 150
        d.put(k, f"Icon {kind}", icon(kind, 60, (207, 230, 211)), x, y + 2, shadowed=False, anchor="tl")
        body(d, k, f"Item {kind}", t, x + 82, y, 360, 48, CREAM)


def s9(d, k):
    d.bg(k, photo_fade(PH["hills"], 0.5, 0.5, 0.42, 0.72, strength=0.95), name="Hills photo with soft fade")
    caps(d, k, "Eyebrow", "OUR GOAL FOR 2027", 90, 820, 900, 44, MINT)
    display(d, k, "Number", "100,000", 82, 875, 920, 180, CREAM, track=0)
    caps(d, k, "Label", "ACRES REGENERATED", 90, 1085, 900, 52, CREAM)
    body(d, k, "Text", "by our community of students and graduates", 90, 1165, 820, 52, MINT)


def s10(d, k):
    d.bg(k, green_ground(COMPOSTP, 0.75), name="Background: compost texture in Food Web Green")
    d.put(k, "Specimen: nematode", specimen("nema", 360, CREAMC, 1.1), -90, 1060, shadowed=True, anchor="tl")
    d.put(k, "Specimen: amoeba", specimen("amoeba", 300, CREAMC, 1.2), 860, -60, shadowed=True, anchor="tl")
    logo(d, k, (W - 160) // 2, 150, 160)
    caps(d, k, "Eyebrow", "GIVING TUESDAY", 60, 470, 960, 46, MINT, "center")
    display(d, k, "Headline", "$100,000\nMATCH", 60, 535, 960, 140, CREAM, "center", 4)
    body(d, k, "Text", "Every gift is doubled.", 60, 850, 960, 58, CREAM, "center")
    f = ImageFont.truetype("/home/user/fonts/Montserrat-Bold.ttf", 52)
    bw, bh = round(f.getlength("Donate today") + 140), 116
    im = Image.new("RGBA", (bw * 3, bh * 3), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, bw * 3 - 1, bh * 3 - 1), bh * 3 // 2, fill=GOLD + (255,))
    x = (W - bw) // 2
    d.put(k, "Donate button", im.resize((bw, bh), Image.LANCZOS), x, 980, shadowed=True, anchor="tl")
    d.text(k, "Donate button text", "Donate today", x, 1006, bw, 70, 52, kind="montserrat-bold", italic=False,
           color=BROWN, align="center", lh=1.1, min_size=52)


def build(v):
    d = Deck("y5c20261201", 10, f"year-one-giving-tuesday-v5-{v}", "2026-12-01")
    for k, fn in enumerate((s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)):
        fn(d, k)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
