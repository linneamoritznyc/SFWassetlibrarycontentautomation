"""Giving Tuesday "Year one" carousel, 10 slides, rebuilt from Linnea's draft (11-11-2026-year-one-achievements.pptx)
with her text. Quiet-luxury look: deep forest ground with a faint soil grain, hairline frame, archival plate numbers,
IM Fell English numerals and headlines, EB Garamond body, tracked small caps, arched photo frames, drawn line icons,
soft fades. Real SFW photos only; gold only on the Donate button. Slide 1 keeps the compost-thermometer dial.

  python3 tools/wormhole-visuals/year_one_luxe.py <version>
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

import collage
from collage import Deck, cover, fit
from nov_fill import DECKS, TILES
from suzanne_frost import grade

W, H = 1080, 1350
ARCH = "/home/user/fonts/dl/arch"
collage.FONT_FILES[("fell", False)] = f"{ARCH}/IMFeENrm28P.ttf"
collage.FONT_FILES[("fell", True)] = f"{ARCH}/IMFeENit28P.ttf"
collage.FONT_FILES[("fellsc", False)] = f"{ARCH}/IMFeENsc28P.ttf"
collage.FONT_FILES[("gara", False)] = "eb-garamond-latin-500-normal.ttf"
collage.PPT_FONT.update({"fell": "IM FELL English", "fellsc": "IM FELL English SC", "gara": "EB Garamond"})

CREAM = "#F4F1EA"
MINT = "#A9D3B2"
SAND = "#D8C3A5"
FOREST = (13, 40, 23)
GOLD = (201, 162, 39)
LINE = (244, 241, 234)
P = "/home/user/photos/new-2026-10"
IND = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/india/raw"
SOIL = "/home/user/sfwlib/social/cic/soil-linnea.jpg"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
LAPTOP = "/home/user/sfwlib/social/lineart/online.png"
COMPOST = "/home/user/sfwlib/social/lineart/compost.png"
MYC = "/home/user/sfwlib/social/merch/mycelium-bloom-print.png"
PH = dict(
    scholar=f"{P}/scholarship-hero-certificate-group.jpg",
    cr="/home/user/sfwlib/social/giving/arms-raised-compost-cr-oct2025-conv.jpg",
    us=f"{P}/learning-outside-santa-fe-2026.jpg",
    uk=f"{P}/community-cheering-compost-cage-jun-2026.jpg",
    india_walk=f"{IND}/6eb1f2b7-ada3-4422-adb2-b2087f35cc66.jpg",
    india_group=f"{IND}/8154d6b2-b029-4ea8-a450-460d233008e8.jpg",
    lab=f"{P}/home-tile-microscopy-lab.jpg",
    hills=f"{IND}/be5ea1aa-fb3a-4480-98e9-fc379364092e.jpg",
)


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def photo(path):
    return grade(ImageOps.exif_transpose(Image.open(path)).convert("RGB"))


# ---------------------------------------------------------------- ground, frame, labels
def ground(seed=0, soil=0.10):
    rng = np.random.default_rng(seed)
    a = np.ones((H, W, 3), np.float32) * np.array(FOREST, np.float32)
    s = np.asarray(cover(Image.open(SOIL).convert("L"), W, H, 0.3 + 0.1 * seed % 1, 0.5)).astype(np.float32) / 255
    a *= (1 - soil + soil * 2 * s)[..., None]
    a += rng.normal(0, 3.0, (H, W, 1))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.45 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    return Image.fromarray((a * v[..., None]).clip(0, 255).astype("uint8")).convert("RGBA")


def frame(d, k, n):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle((36, 36, W - 37, H - 37), outline=LINE + (70,), width=2)
    d.put(k, "Hairline frame", im, 0, 0, shadowed=False, anchor="tl")
    d.text(k, "Plate number", f"Nº {n:02d}", 70, 58, 200, 50, 42, kind="fellsc", italic=False, color=MINT,
           lh=1.0, min_size=42)


def logo(d, k, w=110):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 64 - w, H - 60 - lg.height, shadowed=False, anchor="tl")


def caps(d, k, name, s, x, y, w=900, size=42, color=MINT, align="left"):
    _, lines, _ = fit(s, "montserrat", False, w, 4000, size, size, 1.25, 5)
    return d.text(k, name, s, x, y, w, len(lines) * size * 1.25 + 10, size, kind="montserrat", italic=False,
                  color=color, lh=1.25, align=align, min_size=size, track=5)


def serif(d, k, name, s, x, y, w, size, color=CREAM, italic=False, align="left", lh=1.02, kind="fell"):
    _, lines, _ = fit(s, kind, italic, w, 4000, size, size, lh)
    return d.text(k, name, s, x, y, w, len(lines) * size * lh + 10, size, kind=kind, italic=italic, color=color,
                  lh=lh, align=align, min_size=size)


def body(d, k, name, s, x, y, w, size=52, color=CREAM, align="left", lh=1.22):
    _, lines, _ = fit(s, "gara", False, w, 4000, size, size, lh)
    return d.text(k, name, s, x, y, w, len(lines) * size * lh + 10, size, kind="gara", italic=False, color=color,
                  lh=lh, align=align, min_size=size)


def hair(d, k, x, y, w=None, h=None, a=90, name="Hairline"):
    im = Image.new("RGBA", (w or 2, h or 2), LINE + (a,))
    d.put(k, name, im, x, y, shadowed=False, anchor="tl")


# ---------------------------------------------------------------- photo frames
def arch(path, w, h, fx=0.5, fy=0.5, fade=0.0):
    """Photo in an arched window with a thin cream inner line; optional fade to forest at the bottom."""
    k = 3
    im = cover(photo(path), w, h, fx, fy).convert("RGBA")
    if fade:
        a = np.asarray(im).astype(np.float32)
        y = np.linspace(0, 1, h, dtype=np.float32)
        t = np.clip((y - (1 - fade)) / fade, 0, 1)[:, None, None]
        a[..., :3] = a[..., :3] * (1 - t * 0.9) + np.array(FOREST, np.float32) * t * 0.9
        im = Image.fromarray(a.clip(0, 255).astype("uint8"))
    m = Image.new("L", (w * k, h * k), 0)
    md = ImageDraw.Draw(m)
    md.ellipse((0, 0, w * k - 1, w * k - 1), fill=255)
    md.rectangle((0, w * k // 2, w * k - 1, h * k - 1), fill=255)
    im.putalpha(m.resize((w, h), Image.LANCZOS))
    o = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    od = ImageDraw.Draw(o)
    g = 14 * k
    od.arc((g, g, w * k - g, w * k - g), 180, 360, fill=LINE + (150,), width=2 * k)
    od.line((g, w * k // 2, g, h * k - g), fill=LINE + (150,), width=2 * k)
    od.line((w * k - g, w * k // 2, w * k - g, h * k - g), fill=LINE + (150,), width=2 * k)
    od.line((g, h * k - g, w * k - g, h * k - g), fill=LINE + (150,), width=2 * k)
    im.alpha_composite(o.resize((w, h), Image.LANCZOS))
    return im


def bleed(path, h, fx=0.5, fy=0.5, f0=0.55):
    """Full-width photo of height h that fades into the forest ground."""
    im = cover(photo(path), W, h, fx, fy).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    y = np.linspace(0, 1, h, dtype=np.float32)
    t = np.clip((y - f0) / (1 - f0), 0, 1)
    a[..., 3] = 255 * (1 - t * t * (3 - 2 * t))[:, None]
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


def lineart(path, w, colour=LINE, alpha=1.0):
    """White-on-black line drawing turned into cream lines on transparency."""
    im = Image.open(path).convert("L")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    a = np.clip((a - 40) / 180, 0, 1) * 255 * alpha
    out = np.zeros((im.height, w, 4), np.uint8)
    out[..., :3] = colour
    out[..., 3] = a.astype("uint8")
    return Image.fromarray(out)


# ---------------------------------------------------------------- line icons (drawn)
def icon(kind, s=72, colour=(169, 211, 178)):
    k = 4
    S = s * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = colour + (255,)
    w = 3 * k
    if kind == "phone":
        d.rounded_rectangle((S * .28, S * .06, S * .72, S * .94), S * .08, outline=c, width=w)
        d.line((S * .44, S * .84, S * .56, S * .84), fill=c, width=w)
    elif kind == "microscope":
        d.line((S * .30, S * .90, S * .78, S * .90), fill=c, width=w)
        d.line((S * .50, S * .90, S * .50, S * .74), fill=c, width=w)
        d.arc((S * .30, S * .30, S * .78, S * .82), 270, 90, fill=c, width=w)
        d.line((S * .36, S * .10, S * .54, S * .52), fill=c, width=w * 2)
        d.line((S * .34, S * .60, S * .62, S * .60), fill=c, width=w)
    elif kind == "laptop":
        d.rounded_rectangle((S * .18, S * .22, S * .82, S * .66), S * .03, outline=c, width=w)
        d.line((S * .06, S * .76, S * .94, S * .76), fill=c, width=w)
    elif kind == "people":
        for cx, r in ((.36, .12), (.64, .12)):
            d.ellipse((S * (cx - r), S * .18, S * (cx + r), S * (.18 + 2 * r)), outline=c, width=w)
            d.arc((S * (cx - .22), S * .52, S * (cx + .22), S * .98), 180, 360, fill=c, width=w)
    elif kind == "sprout":
        d.line((S * .5, S * .92, S * .5, S * .42), fill=c, width=w)
        d.chord((S * .14, S * .20, S * .54, S * .56), 300, 120, outline=c, width=w)
        d.chord((S * .46, S * .10, S * .86, S * .46), 60, 240, outline=c, width=w)
        d.line((S * .2, S * .92, S * .8, S * .92), fill=c, width=w)
    return im.resize((s, s), Image.LANCZOS)


def button(d, k, x, y, label="Donate today"):
    from PIL import ImageFont
    f = ImageFont.truetype("/home/user/fonts/Montserrat-Bold.ttf", 52)
    bw, bh = round(f.getlength(label) + 130), 112
    im = Image.new("RGBA", (bw * 3, bh * 3), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, bw * 3 - 1, bh * 3 - 1), bh * 3 // 2, fill=GOLD + (255,))
    d.put(k, "Donate button", im.resize((bw, bh), Image.LANCZOS), x, y, shadowed=False, anchor="tl")
    d.text(k, "Donate button text", label, x, y + 24, bw, 70, 52, kind="montserrat-bold", italic=False,
           color="#173A1F", align="center", lh=1.1, min_size=52)
    return bw, bh


# ---------------------------------------------------------------- slides
def s1(d, k):
    from giving_thermometer import dial, needle
    d.bg(k, ground(1), name="Forest ground")
    frame(d, k, 1)
    caps(d, k, "Eyebrow", "SOIL FOOD WEB FOUNDATION", 90, 150, 900, align="center")
    serif(d, k, "Headline", "Giving Tuesday", 60, 205, 960, 124, italic=True, align="center")
    body(d, k, "Subline", "What we grew together in our first year", 120, 352, 840, 52, MINT, "center")
    D = 590
    x, y = (W - D) // 2, 490
    sw, sh = 28, 150
    st = Image.new("RGBA", (sw * 4, sh * 4), (0, 0, 0, 0))
    ImageDraw.Draw(st).polygon([(0, 0), (sw * 4, 0), (sw * 4, (sh - 30) * 4), (sw * 2, sh * 4), (0, (sh - 30) * 4)],
                               fill=rgb(SAND) + (255,))
    d.put(k, "Thermometer stem", st.resize((sw, sh), Image.LANCZOS), (W - sw) // 2, y + D - 18, shadowed=False,
          anchor="tl")
    d.put(k, "Thermometer dial", dial(D), x, y, shadowed=True, anchor="tl", off=(0, 14), blur=24, alpha=0.4)
    d.put(k, "Needle (rotate around its centre to the current total)", needle(D, 0.0), x, y, shadowed=False,
          anchor="tl")
    logo(d, k)


def s2(d, k):
    d.bg(k, ground(2), name="Forest ground")
    frame(d, k, 2)
    caps(d, k, "Eyebrow", "AT A GLANCE", 90, 150)
    serif(d, k, "Headline", "Our first year\nin numbers", 90, 200, 900, 86)
    hair(d, k, 90, 405, 900, 2)
    serif(d, k, "Number", "$300,000+", 90, 430, 900, 168)
    caps(d, k, "Label", "IN SCHOLARSHIPS AWARDED", 94, 640)
    hair(d, k, 90, 705, 900, 2)
    hair(d, k, 540, 725, 2, 560)
    hair(d, k, 90, 980, 900, 2)
    cells = [("35+", "FREE LIVE\nEVENTS", 90, 720), ("4", "WORKSHOPS", 580, 720),
             ("23", "COUNTRIES IN\nOUR PDC", 90, 995), ("46", "INDIA\nWORKSHOP\nPARTICIPANTS", 580, 995)]
    for n, lab, x, y in cells:
        serif(d, k, f"Number {n}", n, x, y, 420, 112)
        caps(d, k, f"Label {n}", lab, x + 4, y + 135, 430)


def s3(d, k):
    d.bg(k, ground(3), name="Forest ground")
    frame(d, k, 3)
    d.put(k, "Photo in arch", arch(PH["scholar"], 720, 690, 0.5, 0.45), 180, 110, shadowed=True, anchor="tl",
          off=(0, 16), blur=26, alpha=0.45)
    caps(d, k, "Eyebrow", "OPENING THE DOOR", 90, 850, align="center")
    serif(d, k, "Number", "$300,000+", 60, 895, 960, 150, align="center")
    body(d, k, "Text", "in scholarships awarded, through a new official scholarship process", 140, 1100, 800,
         52, CREAM, "center")
    logo(d, k)


def s4(d, k):
    d.bg(k, ground(4), name="Forest ground")
    frame(d, k, 4)
    serif(d, k, "Big 4", "4", 84, 80, 300, 380)
    caps(d, k, "Eyebrow", "IN PERSON", 400, 170, 600)
    serif(d, k, "Headline", "Workshops on\nfour continents", 400, 218, 620, 70)
    places = [("cr", "Costa Rica", "Oct 2025", 0.5, 0.35), ("us", "United\nStates", "Feb 2026", 0.5, 0.45),
              ("uk", "England", "Jun 2026", 0.5, 0.4), ("india_walk", "India", "Oct 2026", 0.45, 0.4)]
    aw, ah, gap = 214, 330, 24
    x0 = (W - (4 * aw + 3 * gap)) // 2
    for i, (key, name, date, fx, fy) in enumerate(places):
        x = x0 + i * (aw + gap)
        d.put(k, f"Photo {name.replace(chr(10), ' ')}", arch(PH[key], aw, ah, fx, fy), x, 520, shadowed=True,
              anchor="tl", off=(0, 10), blur=16, alpha=0.4)
        yy = serif(d, k, f"Place {i + 1}", name, x, 872, aw, 52, CREAM, align="center", lh=1.0)
        body(d, k, f"Date {i + 1}", date, x, 990, aw, 44, MINT, "center")
    hair(d, k, 90, 1080, 900, 2)
    body(d, k, "Text", "Hands-on training with our mentors, on four farms", 90, 1110, 760, 52)
    logo(d, k)


def s5(d, k):
    bg = ground(5)
    bg.alpha_composite(bleed(PH["india_group"], 800, 0.5, 0.55, 0.5), (0, 0))
    d.bg(k, bg, name="India workshop group fading into the forest ground")
    frame(d, k, 5)
    caps(d, k, "Eyebrow", "FIRST IN INDIA", 90, 760)
    serif(d, k, "Number 46", "46", 90, 810, 420, 170)
    body(d, k, "Text 46", "participants from 10 countries", 90, 990, 400, 52)
    hair(d, k, 540, 830, 2, 300)
    serif(d, k, "Number 61", "61", 590, 810, 420, 170)
    body(d, k, "Text 61", "at the Life in the Soils seminar", 590, 990, 400, 52)
    caps(d, k, "Partner line", "WITH ISHA FOUNDATION AND SAVE SOIL", 90, 1190, 760, 42)
    logo(d, k)


def s6(d, k):
    d.bg(k, ground(6), name="Forest ground")
    frame(d, k, 6)
    d.put(k, "Laptop line art", lineart(LAPTOP, 600), 240, 70, shadowed=False, anchor="tl")
    serif(d, k, "Number", "35+", 90, 560, 470, 200)
    serif(d, k, "Headline", "Free live\nevents", 560, 610, 430, 76, italic=True)
    hair(d, k, 90, 800, 900, 2)
    caps(d, k, "Eyebrow", "OUR WEBINAR GUESTS", 90, 840)
    body(d, k, "Guests 1", "Vandana Shiva\nGeoff Lawton\nNicole Masters", 90, 910, 430, 54, lh=1.3)
    body(d, k, "Guests 2", "Mary Reynolds\nDavid Holmgren\nDr. Mary Cole", 560, 910, 430, 54, lh=1.3)
    logo(d, k)


def s7(d, k):
    d.bg(k, ground(7), name="Forest ground")
    frame(d, k, 7)
    caps(d, k, "Eyebrow", "NEW PROGRAMS", 90, 150)
    serif(d, k, "Headline", "Two new ways to learn", 90, 200, 900, 80)
    hair(d, k, 540, 360, 2, 860)
    cols = [(90, icon("sprout", 150), "100", "students from 23 countries", "PERMACULTURE\nDESIGN\nCERTIFICATE",
             "With the Permaculture Association (UK)"),
            (590, lineart(COMPOST, 200, alpha=0.95), "10", "weeks, live online", "COMPOST\nINTENSIVE\nCOURSE",
             "Open to everyone, with Spanish transcriptions")]
    for x, ic, n, sub, title, note in cols:
        d.put(k, f"Icon {n}", ic, x - (25 if ic.height > 160 else 0), 340 if ic.height < 160 else 300, shadowed=False, anchor="tl")
        serif(d, k, f"Number {n}", n, x, 500, 420, 150)
        y = body(d, k, f"Text {n}", sub, x, 660, 400, 52)
        hair(d, k, x, round(y) + 30, 70, 3, 200)
        y = caps(d, k, f"Program {n}", title, x, round(y) + 60, 420, 44, CREAM)
        body(d, k, f"Note {n}", note, x, round(y) + 25, 400, 46, MINT)
    logo(d, k)


def s8(d, k):
    d.bg(k, ground(8), name="Forest ground")
    frame(d, k, 8)
    d.put(k, "Photo in arch", arch(PH["lab"], 400, 1020, 0.45, 0.5), 610, 150, shadowed=True, anchor="tl",
          off=(0, 16), blur=26, alpha=0.45)
    caps(d, k, "Eyebrow", "FOR OUR STUDENTS", 90, 150, 600)
    serif(d, k, "Headline", "A better\nplace to\nlearn", 90, 200, 480, 92)
    items = [("phone", "Student mobile app"), ("microscope", "Updated Microbe Library"),
             ("laptop", "New learning platform"), ("people", "Free public community")]
    y = 610
    for kind, txt in items:
        d.put(k, f"Icon {kind}", icon(kind, 70), 90, y + 6, shadowed=False, anchor="tl")
        yy = body(d, k, f"Item {kind}", txt, 186, y, 380, 50, lh=1.12)
        y = max(round(yy), y + 70) + 44
        hair(d, k, 90, y - 22, 470, 1, 60)
    logo(d, k)


def s9(d, k):
    bg = ground(9)
    bg.alpha_composite(bleed(PH["hills"], 900, 0.5, 0.5, 0.45), (0, 0))
    d.bg(k, bg, name="Hills and palms fading into the forest ground")
    frame(d, k, 9)
    caps(d, k, "Eyebrow", "OUR GOAL FOR 2027", 90, 800)
    serif(d, k, "Number", "100,000", 90, 835, 900, 200)
    caps(d, k, "Label", "ACRES REGENERATED", 94, 1085, 900, 48, CREAM)
    body(d, k, "Text", "by our community of students and graduates", 90, 1150, 760, 52, MINT)
    logo(d, k)


def s10(d, k):
    bg = ground(10, soil=0.16)
    m = Image.open(MYC).convert("RGBA").resize((900, 900), Image.LANCZOS)
    m = m.crop((0, 0, 900, 700))
    a = np.asarray(m).astype(np.float32)
    a[..., 3] *= 0.42
    bg.alpha_composite(Image.fromarray(a.astype("uint8")), (90, 40))
    d.bg(k, bg, name="Forest ground with the mycelium drawing")
    frame(d, k, 10)
    caps(d, k, "Eyebrow", "GIVING TUESDAY", 90, 720, align="center")
    serif(d, k, "Headline", "$100,000 match", 60, 770, 960, 120, align="center")
    body(d, k, "Text", "Every gift is doubled.", 90, 935, 900, 56, CREAM, "center")
    from PIL import ImageFont
    bw = round(ImageFont.truetype("/home/user/fonts/Montserrat-Bold.ttf", 52).getlength("Donate today") + 130)
    button(d, k, (W - bw) // 2, 1060)
    logo(d, k)


def build(v):
    d = Deck("yr20261201", 10, f"year-one-giving-tuesday-{v}", "2026-12-01")
    for k, fn in enumerate((s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)):
        fn(d, k)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
