"""January 2027 rebuilt for variety (Linnea, 27 Oct: "never the same fucking template over and over again").

The photo-and-tag look (jan_a.py, jan_b.py, round2_jan.py) is replaced. Every grid post gets its own
family from docs/feed-guide.md, neighbours never match, the ground colour changes between neighbours,
and no photo appears on two posts (checked with photo_check.py). Brand fonts only: Montserrat,
Pathway Gothic One, Source Sans 3.

  python3 tools/wormhole-visuals/jan_varied.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v5-<n>.jpg   (1080 x 1350; Reels also 1080 x 1920 in out/reels)
"""
import math
import os
import sys

from PIL import Image, ImageDraw

import collage
from collage import cover, draw_layer, hexrgb
from novdec import LOGO, REG, W, build, post

# brand colours
CREAM, DEEP, FWG, BROWN, BLUE = "#F4F1EA", "#22371F", "#156826", "#4F3433", "#3780B8"
TAN, LGREEN, SAND, MIST, INK = "#C89B7B", "#59A66C", "#D8C3A5", "#A7C6D9", "#333130"
LG_T, TAN_T, SAGE = "#D5E9DA", "#EEE1D7", "#DDE5D4"
DARK = {DEEP, FWG, BROWN, BLUE}

SITE = "/home/user/linneamoritznyc/final-sfwsite-linnea/img/w"
NEW = "/home/user/photos/new-2026-10"
MICRO = "/home/user/SFW-SocialMedia/assets/microscopy"
CR = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/cru"  # Costa Rica deck photos
CR = os.environ.get("CR_PHOTOS", CR)
FILM = "/home/user/linneamoritznyc/final-sfwsite-linnea/img/video/790985081.jpg"
SFW = "Photo: Soil Food Web Foundation"
VER = "v5"


def ink(bg):
    return CREAM if bg in DARK else BROWN


def sub(bg):
    return "#E3DDCC" if bg in DARK else INK


def accent(bg):
    return LGREEN if bg in (DEEP, BROWN) else (CREAM if bg in DARK else FWG)


# ------------------------------------------------------------------ text
def eyebrow(p, k, text, bg, y=80, x=90, w=900, color=None):
    return p.d.text(k, "label", text, x, y, w, 60, 40, kind="pathway", italic=False, color=color or accent(bg),
                    lh=1.1, track=2)


def head(p, k, text, bg, y=140, size=80, w=900, x=90, h=420, align="left", color=None):
    p.hb[k] = p.d.text(k, "heading", text, x, y, w, h, size, kind="montserrat-bold", italic=False,
                       color=color or ink(bg), lh=1.1, align=align, min_size=48)
    return p.hb[k]


def body(p, k, text, bg, y, size=40, w=880, x=90, h=300, align="left", color=None):
    return p.d.text(k, "body", text, x, round(y), w, h, size, kind="source-reg", italic=False,
                    color=color or sub(bg), lh=1.3, align=align, min_size=28)


def credit(p, k, text, bg, x=90, y=None, w=640):
    y = p.h - 74 if y is None else y
    p.d.text(k, "credit", text, x, y, w, 50, 22, kind="source-reg", italic=False, color=sub(bg), lh=1.2,
             min_size=18)


def logo(p, k, bg, size=140):
    im = Image.open(LOGO).convert("RGBA")
    im = im.resize((size, round(im.height * size / im.width)), Image.LANCZOS)
    if bg in DARK:  # a cream disc behind the logo on dark grounds
        d = size + 36
        disc = Image.new("RGBA", (d, d), (0, 0, 0, 0))
        ImageDraw.Draw(disc).ellipse((0, 0, d - 1, d - 1), fill=hexrgb(CREAM) + (255,))
        disc.alpha_composite(im, (18, (d - im.height) // 2))
        im = disc
    p.d.put(k, "logo", im, W - 56 - im.width, p.h - 50 - im.height, shadowed=False, anchor="tl")


# ------------------------------------------------------------------ pictures
def framed(p, k, src, x, y, w, h, fx=0.5, fy=0.5, line=BROWN, name="photo"):
    """A real photo in a clean, straight 4 px frame (no hand-drawn wobble, no tilt)."""
    ph = cover(src, w, h, fx, fy).convert("RGBA")
    out = Image.new("RGBA", (w + 8, h + 8), hexrgb(line) + (255,))
    out.alpha_composite(ph, (4, 4))
    return p.put(k, name, out, x - 4, y - 4)


def bleed(p, k, src, fx=0.5, fy=0.5):
    p.put(k, "photo", cover(src, W, p.h, fx, fy).convert("RGBA"), 0, 0)


def band(p, k, color, y, h, x=0, w=W, name="band"):
    p.drawn(k, w, h, lambda dr, s: dr.rectangle((0, 0, w * s, h * s), fill=hexrgb(color) + (255,)), x, y, name=name)


def disc(p, k, src, cx, cy, d, ring=12, ring_color=CREAM, fx=0.5, fy=0.4, name="round photo"):
    im = collage.round_photo(src, d, ring=ring, fx=fx, fy=fy, ring_color=ring_color)
    return p.put(k, name, im, cx - im.width / 2, cy - im.height / 2)


def lens(p, k, src, cx, cy, d, name="micrograph"):
    im = collage.lens(src, d)
    return p.put(k, name, im, cx - im.width / 2, cy - im.height / 2)


def photo_space(p, k, x, y, w, h, what, bg):
    line = hexrgb(ink(bg))

    def fn(dr, s):
        dr.rectangle((0, 0, w * s, h * s), fill=(255, 255, 255, 70), outline=line + (255,), width=round(3 * s))
        for i in range(0, w + h, 44):
            dr.line(((i - h) * s, h * s, i * s, 0), fill=line + (40,), width=round(2 * s))
    p.drawn(k, w, h, fn, x, y, name="photo-placeholder")
    p.d.text(k, "label", "PHOTO: " + what, x + 50, round(y + h / 2 - 40), w - 100, 120, 34, kind="pathway",
             italic=False, color=ink(bg), lh=1.15, align="center", track=1)


# ------------------------------------------------------------------ drawn bits (flat, one even outline)
LINE = (52, 40, 38)


def soil_dots(dr, s, x0, y0, x1, y1, seed, n, r=(3, 7), fill=(122, 92, 70), open_pores=True):
    import random
    rnd = random.Random(seed)
    for _ in range(n):
        x, y, rr = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(*r)
        dr.ellipse(((x - rr) * s, (y - rr) * s, (x + rr) * s, (y + rr) * s),
                   fill=(250, 246, 236, 255) if open_pores else fill + (255,))


# ================================================================== the posts
@post("j20270101", "2027-01-01", "new-year-2027-" + VER, 2, DEEP)
def new_year(p):
    """G, type only."""
    eyebrow(p, 0, "HAPPY NEW YEAR", DEEP)
    y = head(p, 0, "Welcome to 2027.", DEEP, size=120)
    for i, (place, month) in enumerate([("Costa Rica", "January"), ("New Mexico", "May"),
                                        ("United Kingdom", "September")]):
        yy = 620 + i * 150
        band(p, 0, LGREEN, yy, 4, x=90, w=900, name="rule")
        p.d.text(0, "place", place, 90, yy + 24, 600, 80, 58, kind="montserrat-bold", italic=False, color=CREAM,
                 lh=1.1)
        p.d.text(0, "month", month.upper(), 660, yy + 34, 330, 60, 44, kind="pathway", italic=False, color=LGREEN,
                 lh=1.1, align="right", track=2)
    eyebrow(p, 1, "OUR 2027 WORKSHOPS", DEEP)
    head(p, 1, "See you in the field.", DEEP, y=430, size=110)
    body(p, 1, "All 2027 workshops, link in bio.", DEEP, 820, size=44)
    for k in range(2):
        logo(p, k, DEEP)


@post("j20270102", "2027-01-02", "stay-off-wet-beds-" + VER, 1, LG_T)
def wet_beds(p):
    """H, diagram: a footprint presses wet soil flat; a board spreads the weight."""
    eyebrow(p, 0, "DO THIS WEEKEND", LG_T)
    head(p, 0, "Stay off wet beds.", LG_T, size=96)

    def diagram(dr, s):
        for i, x0 in enumerate((0, 470)):
            dr.rectangle(((x0) * s, 140 * s, (x0 + 430) * s, 520 * s), fill=(138, 106, 85, 255),
                         outline=LINE + (255,), width=round(3 * s))
            soil_dots(dr, s, x0 + 20, 160, x0 + 410, 500, 7 + i, 120 if i else 40)
        # left: a boot pressing the surface, a dense band under it
        dr.rectangle((40 * s, 140 * s, 390 * s, 250 * s), fill=(99, 74, 60, 255), outline=LINE + (255,),
                     width=round(3 * s))
        dr.rounded_rectangle((130 * s, 40 * s, 300 * s, 140 * s), radius=30 * s, fill=(51, 49, 48, 255),
                             outline=LINE + (255,), width=round(3 * s))
        # right: a board on the surface, open crumb below
        dr.rectangle((500 * s, 108 * s, 870 * s, 140 * s), fill=(216, 195, 165, 255), outline=LINE + (255,),
                     width=round(3 * s))
        dr.rounded_rectangle((600 * s, 10 * s, 770 * s, 108 * s), radius=30 * s, fill=(51, 49, 48, 255),
                             outline=LINE + (255,), width=round(3 * s))
    p.drawn(0, 900, 530, diagram, 90, 420)
    for x, t in ((90, "Wet soil under a boot: pores pressed shut."), (560, "A board spreads the weight: the crumb stays open.")):
        p.d.text(0, "label", t, x, 980, 430, 160, 34, kind="source-reg", italic=False, color=INK, lh=1.25)
    body(p, 0, "Walk on boards or a mulched path instead.", LG_T, 1140, size=40, w=760, color=BROWN)
    logo(p, 0, LG_T)


@post("j20270103", "2027-01-03", "compost-intensive-january-" + VER, 1, CREAM)
def cic(p):
    """K, one framed photo on flat colour."""
    eyebrow(p, 0, "COMPOST INTENSIVE COURSE", CREAM)
    head(p, 0, "The January cohort starts this month.", CREAM, size=78)
    framed(p, 0, f"{NEW}/R5A_4016.jpg", 90, 470, 900, 620, fy=0.5)
    body(p, 0, "Link in bio.", CREAM, 1130, size=40, color=BROWN)
    credit(p, 0, SFW, CREAM)
    logo(p, 0, CREAM)


@post("j20270104", "2027-01-04", "naked-amoeba-" + VER, 2, DEEP, reel=True)
def naked_amoeba(p):
    """F, specimen."""
    mid = p.h / 2
    eyebrow(p, 0, "READ THE DROP", DEEP)
    head(p, 0, "Meet the naked amoeba.", DEEP, size=84)
    lens(p, 0, f"{NEW}/Naked amoeba, 40x obj, Jimena Fuentes.jpg", W / 2, mid + 120, 700)
    eyebrow(p, 0, "NAKED AMOEBA, 40X OBJECTIVE", DEEP, y=round(mid + 500), x=90, color=CREAM)
    head(p, 1, "It eats bacteria and releases ammonium by the roots.", DEEP, size=70)
    lens(p, 1, f"{NEW}/Naked amoeba (stellate), flagellate, 40x obj, Jimena Fuentes.jpg", W / 2, mid + 160, 640)
    for k in range(2):
        credit(p, k, "Micrograph: Jimena Fuentes", DEEP)
        logo(p, k, DEEP)


@post("j20270105", "2027-01-05", "meet-evan-buckman-" + VER, 1, TAN_T)
def evan(p):
    """I, portrait."""
    eyebrow(p, 0, "MEET THE TEAM", TAN_T)
    disc(p, 0, f"{SITE}/evan.jpg", W / 2, 560, 640, ring=14, ring_color=FWG, fy=0.35)
    p.d.text(0, "name", "Evan Buckman", 90, 930, 900, 110, 84, kind="montserrat-bold", italic=False, color=BROWN,
             lh=1.1, align="center")
    p.d.text(0, "role", "EXECUTIVE DIRECTOR", 90, 1045, 900, 60, 44, kind="pathway", italic=False, color=FWG,
             lh=1.1, align="center", track=3)
    credit(p, 0, SFW, TAN_T)
    logo(p, 0, TAN_T)


@post("j20270106", "2027-01-06", "roberto-silva-peru-" + VER, 1, FWG)
def roberto(p):
    """D, full-bleed photo with one colour strip."""
    bleed(p, 0, FILM, fx=0.42)
    band(p, 0, FWG, 930, 420, name="strip")
    eyebrow(p, 0, "SOIL REGENERATORS IN THE WILD", FWG, y=970, color=LG_T)
    head(p, 0, "Roberto Silva and consultant Miles Sorel", FWG, y=1030, size=62, w=760, h=170)
    body(p, 0, "Piura, Peru", FWG, 1205, size=40)
    credit(p, 0, "Still: Roberto Silva case study film", FWG, y=1280)
    logo(p, 0, FWG, size=120)


@post("j20270107", "2027-01-07", "myth-soil-sleeps-winter-" + VER, 2, MIST)
def winter(p):
    """H, diagram: snow on top, soil life still busy underneath."""
    def scene(dr, s):
        dr.rectangle((0, 0, 900 * s, 150 * s), fill=(250, 250, 248, 255), outline=LINE + (255,), width=round(3 * s))
        dr.rectangle((0, 150 * s, 900 * s, 620 * s), fill=(122, 92, 70, 255), outline=LINE + (255,),
                     width=round(3 * s))
        soil_dots(dr, s, 20, 170, 880, 600, 3, 90)
        import random
        rnd = random.Random(11)
        for _ in range(70):  # bacteria as small green rods, still dividing
            x, y = rnd.uniform(30, 870), rnd.uniform(200, 590)
            dr.rounded_rectangle(((x - 9) * s, (y - 4) * s, (x + 9) * s, (y + 4) * s), radius=4 * s,
                                 fill=(89, 166, 108, 255))
        for x in (180, 520, 760):  # roots
            dr.line((x * s, 150 * s, (x - 30) * s, 420 * s, (x + 10) * s, 600 * s), fill=(233, 220, 195, 255),
                    width=round(7 * s), joint="curve")
    eyebrow(p, 0, "MYTH VS MECHANISM", MIST, color=BROWN)
    head(p, 0, "Myth: soil life sleeps all winter.", MIST, size=82)
    p.drawn(0, 900, 620, scene, 90, 520)
    eyebrow(p, 0, "SNOW", MIST, y=540, x=120, color=BROWN)
    eyebrow(p, 1, "THE MECHANISM", MIST, color=BROWN)
    head(p, 1, "Under the snow, microbes keep growing.", MIST, size=82)
    p.drawn(1, 900, 620, scene, 90, 520)
    p.d.text(1, "label", "bacteria still dividing around the roots", 120, 1160, 800, 60, 34, kind="source-reg",
             italic=False, color=CREAM, lh=1.2)
    for k in range(2):
        logo(p, k, MIST)


@post("j20270108", "2027-01-08", "meet-stephanie-mcdaniel-" + VER, 1, CREAM)
def stephanie(p):
    """K, framed portrait."""
    framed(p, 0, f"{SITE}/stephanie.jpg", 90, 90, 620, 760, fy=0.3)
    eyebrow(p, 0, "MEET THE TEAM", CREAM, y=900)
    y = head(p, 0, "Stephanie McDaniel", CREAM, y=955, size=80, h=110)
    body(p, 0, "Director of Communications", CREAM, y + 12, size=44, color=FWG)
    credit(p, 0, SFW, CREAM)
    logo(p, 0, CREAM)


@post("j20270109a", "2027-01-09", "plan-cover-crops-" + VER, 1, CREAM)
def cover_crops(p):
    """D, full-bleed photo with one colour strip."""
    bleed(p, 0, f"{NEW}/cover-crop-mix-capri.jpg", fx=0.6, fy=0.4)
    band(p, 0, CREAM, 900, 450, name="strip")
    eyebrow(p, 0, "DO THIS WEEKEND", CREAM, y=940)
    head(p, 0, "Plan your cover crops.", CREAM, y=995, size=74, w=760, h=110)
    body(p, 0, "Legumes add nitrogen. Grasses hold on to it. Mix both.", CREAM, 1100, size=38, w=760)
    credit(p, 0, SFW + " (crimson clover)", CREAM, y=1280)
    logo(p, 0, CREAM, size=120)


@post("j20270110a", "2027-01-10", "observe-and-interact-" + VER, 1, SAND)
def observe(p):
    """K, framed photo on flat colour (photo first, heading below)."""
    framed(p, 0, f"{SITE}/erc-panchamana-garden.jpg", 90, 90, 900, 760)
    eyebrow(p, 0, "PERMACULTURE PRINCIPLE 1", SAND, y=900, color=BROWN)
    y = head(p, 0, "Observe and interact.", SAND, y=955, size=80, h=110)
    body(p, 0, "Watch first, then design.", SAND, y + 12, size=42)
    credit(p, 0, SFW + " (Panchamana, Ecosystem Restoration Camps)", SAND, w=760)
    logo(p, 0, SAND)


@post("j20270110c", "2027-01-10", "cic-last-call-" + VER, 1, BROWN)
def last_call(p):
    """G, type only."""
    eyebrow(p, 0, "COMPOST INTENSIVE COURSE", BROWN, y=300)
    head(p, 0, "Last call.", BROWN, y=360, size=190, h=260)
    body(p, 0, "The January cohort starts the week of 18 January. Link in bio.", BROWN, 700, size=46, w=820)
    logo(p, 0, BROWN)


@post("j20270111", "2027-01-11", "costa-rica-one-week-" + VER, 1, CREAM)
def one_week(p):
    """L, photo grid: three photos, straight, even gutters."""
    p.put(0, "photo", cover(f"{CR}/cr24.jpg", 900, 520, 0.5, 0.55).convert("RGBA"), 90, 90)
    p.put(0, "photo", cover(f"{CR}/cr19.jpg", 440, 400, 0.5, 0.5).convert("RGBA"), 90, 630)
    p.put(0, "photo", cover(f"{CR}/cr02.jpg", 440, 400, 0.5, 0.4).convert("RGBA"), 550, 630)
    head(p, 0, "One week to go.", CREAM, y=1065, size=74, h=100)
    body(p, 0, "Accelerator Workshop, Costa Rica, 18 to 29 January at Armonía.", CREAM, 1160, size=34, w=760)
    credit(p, 0, SFW + " (Costa Rica, 2025)", CREAM, y=1290)
    logo(p, 0, CREAM, size=110)


@post("j20270112", "2027-01-12", "protozoa-per-teaspoon-" + VER, 1, LG_T)
def protozoa(p):
    """B, big number."""
    eyebrow(p, 0, "SOIL IN NUMBERS", LG_T)
    p.d.text(0, "number", "1,000,000", 90, 150, 900, 220, 190, kind="montserrat-bold", italic=False, color=FWG,
             lh=1.0, min_size=120)
    body(p, 0, "protozoa can live in one teaspoon of highly fertile soil. Poor soil holds about 1,000.", LG_T, 400,
         size=44, w=880, color=BROWN)
    lens(p, 0, f"{NEW}/Testate amoeba, 40x obj, Cameron Radman.jpg", 540, 880, 520)
    credit(p, 0, "Source: USDA NRCS Soil Biology Primer. Micrograph: Cameron Radman", LG_T, w=780)
    logo(p, 0, LG_T)


@post("j20270113", "2027-01-13", "meet-sammie-bass-" + VER, 1, BLUE)
def sammie(p):
    """I, portrait, set to the left with the name beside it."""
    disc(p, 0, f"{SITE}/sammie.jpg", 400, 640, 620, ring=14, ring_color=CREAM, fy=0.35)
    eyebrow(p, 0, "MEET THE TEAM", BLUE, color=LG_T)
    p.d.text(0, "name", "Sammie Bass", 90, 1030, 900, 110, 88, kind="montserrat-bold", italic=False, color=CREAM,
             lh=1.1)
    p.d.text(0, "role", "MARKETING ASSOCIATE", 90, 1140, 700, 60, 44, kind="pathway", italic=False, color=LG_T,
             lh=1.1, track=3)
    credit(p, 0, SFW, BLUE, y=1290)
    logo(p, 0, BLUE)


@post("j20270114", "2027-01-14", "new-year-webinars-" + VER, 1, FWG)
def webinars(p):
    """M, event card: a cream card on green, a date block on the card."""
    band(p, 0, CREAM, 150, 1000, x=90, w=900, name="card")
    band(p, 0, LGREEN, 150, 16, x=90, w=900, name="card-top")
    eyebrow(p, 0, "FREE WEBINARS", CREAM, y=220, x=150)
    head(p, 0, "New Year Series", CREAM, y=280, x=150, w=780, size=96)
    band(p, 0, BROWN, 560, 260, x=150, w=380, name="date-block")
    p.d.text(0, "date", "JAN TO MAR", 170, 600, 340, 80, 60, kind="pathway", italic=False, color=CREAM, lh=1.0,
             align="center", track=2)
    p.d.text(0, "date2", "2027", 170, 690, 340, 90, 76, kind="montserrat-bold", italic=False, color=CREAM, lh=1.0,
             align="center")
    body(p, 0, "One live hour online, free. Ask your questions live.", CREAM, 870, size=42, x=150, w=780,
         color=INK)
    p.d.text(0, "cta", "LINK IN BIO", 150, 1040, 600, 60, 48, kind="pathway", italic=False, color=FWG, lh=1.0,
             track=3)
    logo(p, 0, FWG, size=120)


@post("j20270115", "2027-01-15", "meet-alex-andreou-" + VER, 1, SAGE)
def alex(p):
    """K, a small framed portrait (the only photo on file is 320 px) on flat colour."""
    eyebrow(p, 0, "MEET THE TEAM", SAGE)
    head(p, 0, "Alex Andreou", SAGE, size=96)
    body(p, 0, "IT Manager", SAGE, 270, size=46, color=FWG)
    framed(p, 0, f"{SITE}/alex.jpg", 290, 420, 500, 500, fy=0.4)
    credit(p, 0, SFW, SAGE)
    logo(p, 0, SAGE)


@post("j20270115b", "2027-01-15", "happy-pongal-" + VER, 1, TAN)
def pongal(p):
    """G, type only, on Natural Tan."""
    eyebrow(p, 0, "15 JANUARY", TAN, y=360, color=BROWN)
    head(p, 0, "Happy Pongal", TAN, y=420, size=150, h=200)
    body(p, 0, "to every farmer in Tamil Nadu, and to the soil that feeds the harvest.", TAN, 640, size=48, w=820,
         color=BROWN)
    logo(p, 0, TAN)


def step(p, k, n, text, bg, art=None, photo=None):
    p.d.text(k, "step", str(n), 90, 70, 400, 360, 330, kind="montserrat-bold", italic=False, color=accent(bg),
             lh=1.0)
    p.d.text(k, "text", text, 90, 470, 880, 330, 64, kind="montserrat-bold", italic=False, color=ink(bg), lh=1.15,
             min_size=44)
    if art:
        p.drawn(k, 600, 380, art, 90, 850)
    if photo:
        framed(p, k, photo, 90, 830, 420, 420, fy=0.45)


def tray(sprouts):
    def fn(dr, s):
        dr.rounded_rectangle((0, 120 * s, 600 * s, 360 * s), radius=18 * s, fill=(122, 92, 70, 255),
                             outline=LINE + (255,), width=round(3 * s))
        for i in range(10):
            for j in range(3):
                x, y = 40 + i * 58, 170 + j * 62
                if sprouts and (i * 3 + j) % 5:
                    dr.line((x * s, y * s, x * s, (y - 60) * s), fill=(89, 166, 108, 255), width=round(5 * s))
                    dr.ellipse(((x - 16) * s, (y - 74) * s, x * s, (y - 58) * s), fill=(89, 166, 108, 255))
                    dr.ellipse((x * s, (y - 74) * s, (x + 16) * s, (y - 58) * s), fill=(89, 166, 108, 255))
                else:
                    dr.ellipse(((x - 6) * s, (y - 6) * s, (x + 6) * s, (y + 6) * s), fill=(216, 195, 165, 255))
    return fn


@post("j20270116", "2027-01-16", "germination-test-" + VER, 3, CREAM)
def germination(p):
    """J, numbered steps."""
    step(p, 0, 1, "Sow 100 radish or cress seeds in moist compost.", CREAM, tray(False))
    step(p, 1, 2, "Keep it moist and in the light for 5 to 10 days.", CREAM)
    step(p, 2, 3, "80 or more sprouts: the compost is likely mature.", CREAM, tray(True))
    credit(p, 1, "Method: Institute for Local Self-Reliance, germination test", CREAM)
    for k in range(3):
        logo(p, k, CREAM)


@post("j20270117", "2027-01-17", "costa-rica-tomorrow-" + VER, 1, DEEP)
def tomorrow(p):
    """D, full-bleed photo, strip on top this time."""
    bleed(p, 0, f"{CR}/cr03.jpg", fy=0.6)
    band(p, 0, DEEP, 0, 400, name="strip")
    eyebrow(p, 0, "ACCELERATOR WORKSHOP, COSTA RICA", DEEP, y=60)
    head(p, 0, "Tomorrow we start.", DEEP, y=115, size=86, h=110)
    body(p, 0, "Week one: compost. Week two: biological liquid amendments.", DEEP, 235, size=38, w=880)
    credit(p, 0, SFW + " (Costa Rica, 2025)", DEEP, y=345, w=800)
    logo(p, 0, DEEP, size=110)


def bacteria_lens(dr, s):
    """No bacteria micrograph on file: a drawn field of rods and cocci in the same round frame."""
    import random
    rnd = random.Random(2)
    dr.ellipse((0, 0, 320 * s, 320 * s), fill=(27, 27, 24, 255))
    dr.ellipse((11 * s, 11 * s, 309 * s, 309 * s), fill=(228, 236, 230, 255))
    for _ in range(80):
        x, y = rnd.uniform(40, 280), rnd.uniform(40, 280)
        if (x - 160) ** 2 + (y - 160) ** 2 > 125 ** 2:
            continue
        if rnd.random() < 0.6:
            a = rnd.uniform(0, math.pi)
            dx, dy = 9 * math.cos(a), 9 * math.sin(a)
            dr.line(((x - dx) * s, (y - dy) * s, (x + dx) * s, (y + dy) * s), fill=(110, 130, 100, 255),
                    width=round(6 * s))
        else:
            dr.ellipse(((x - 4) * s, (y - 4) * s, (x + 4) * s, (y + 4) * s), fill=(110, 130, 100, 255))


@post("j20270118b", "2027-01-18", "foundation-courses-four-groups-" + VER, 1, DEEP)
def four_groups(p):
    """F, specimens: one lens per organism group."""
    eyebrow(p, 0, "FOUNDATION COURSES", DEEP)
    head(p, 0, "Learn to identify the four groups.", DEEP, size=72)
    items = [(None, "BACTERIA (DRAWN)"),
             (f"{SITE}/fungi-in-under-grape-soil.jpg", "FUNGI"),
             (f"{NEW}/Testate amoeba, 40x obj, Tanja Dekker (I5).jpg", "PROTOZOA"),
             (f"{NEW}/Bacterial-feeding nematode (omnivore), 40x obj, Johannes Veith.jpg", "NEMATODES")]
    for i, (src, name) in enumerate(items):
        cx, cy = 300 + (i % 2) * 480, 560 + (i // 2) * 380
        if src:
            lens(p, 0, src, cx, cy, 300)
        else:
            p.drawn(0, 320, 320, bacteria_lens, cx - 160, cy - 160, name="bacteria-drawn")
        p.d.text(0, "label", name, cx - 200, cy + 168, 400, 60, 40, kind="pathway", italic=False, color=CREAM,
                 lh=1.0, align="center", track=3)
    body(p, 0, "Start any time. Link in bio.", DEEP, 1230, size=36, w=600)
    credit(p, 0, "Micrographs: SFW library, Tanja Dekker, Johannes Veith. Bacteria drawn.", DEEP, y=1290, w=780)
    logo(p, 0, DEEP, size=110)


@post("j20270119", "2027-01-19", "meet-leslie-lewis-" + VER, 1, SAND)
def leslie(p):
    """I, portrait, set high with the name below."""
    eyebrow(p, 0, "MEET THE TEAM", SAND, color=BROWN)
    disc(p, 0, f"{SITE}/leslie.jpg", 540, 520, 560, ring=14, ring_color=BROWN, fy=0.3)
    p.d.text(0, "name", "Leslie W. Lewis, Ph.D.", 90, 860, 900, 110, 80, kind="montserrat-bold", italic=False,
             color=BROWN, lh=1.1, align="center")
    p.d.text(0, "role", "EXECUTIVE COMMITTEE", 90, 970, 900, 60, 44, kind="pathway", italic=False, color=FWG,
             lh=1.1, align="center", track=3)
    credit(p, 0, SFW, SAND)
    logo(p, 0, SAND)


@post("j20270119b", "2027-01-19", "intro-to-permaculture-" + VER, 1, CREAM)
def intro_pc(p):
    """K, framed photo, landscape crop, heading above."""
    eyebrow(p, 0, "NEW COURSE", CREAM)
    head(p, 0, "Intro to Permaculture opens 1 February.", CREAM, size=76)
    framed(p, 0, f"{SITE}/erc-panchmana-treeplanting-fb-img-1666270907385.jpg", 90, 480, 900, 600)
    credit(p, 0, SFW + " (Panchamana, Ecosystem Restoration Camps)", CREAM, w=760)
    logo(p, 0, CREAM)


@post("j20270120", "2027-01-20", "trashit-pakistan-" + VER, 1, FWG)
def trashit(p):
    """C, article-style card: cream card on green with the photo, a bar and the headline."""
    band(p, 0, CREAM, 110, 1080, x=90, w=900, name="card")
    p.put(0, "photo", cover(f"{SITE}/screenshot-2025-10-22-212600.jpg", 840, 560, 0.5, 0.45).convert("RGBA"), 120,
          140)
    band(p, 0, FWG, 740, 220, x=120, w=10, name="bar")
    eyebrow(p, 0, "SOIL REGENERATORS IN THE WILD", CREAM, y=740, x=160)
    head(p, 0, "TrashIt, Pakistan", CREAM, y=795, x=160, w=780, size=78, h=110)
    body(p, 0, "Soil Health Week 2025", CREAM, 900, x=160, size=38, color=INK)
    credit(p, 0, SFW, FWG, y=1230, x=90)
    logo(p, 0, FWG, size=110)


def clay_panel(crumb):
    def fn(dr, s):
        dr.rectangle((0, 0, 420 * s, 420 * s), fill=(176, 139, 110, 255), outline=LINE + (255,), width=round(3 * s))
        import random
        rnd = random.Random(5 if crumb else 4)
        if not crumb:  # clay platelets packed flat with sand grains: it sets like brick
            for y in range(20, 410, 22):
                for x in range(10, 410, 70):
                    dr.rectangle(((x + rnd.randint(-8, 8)) * s, y * s, (x + 60) * s, (y + 10) * s),
                                 fill=(142, 123, 110, 255))
            for _ in range(26):
                x, y = rnd.uniform(30, 390), rnd.uniform(30, 390)
                dr.ellipse(((x - 14) * s, (y - 14) * s, (x + 14) * s, (y + 14) * s), fill=(217, 194, 154, 255),
                           outline=LINE + (255,), width=round(2 * s))
        else:  # crumbs held by fungal threads, with pore space between
            for cx, cy in ((90, 100), (260, 90), (130, 260), (320, 280), (220, 360)):
                dr.ellipse(((cx - 70) * s, (cy - 60) * s, (cx + 70) * s, (cy + 60) * s), fill=(122, 92, 70, 255),
                           outline=LINE + (255,), width=round(3 * s))
            for _ in range(14):
                x0, y0 = rnd.uniform(20, 400), rnd.uniform(20, 400)
                dr.line((x0 * s, y0 * s, (x0 + rnd.uniform(-90, 90)) * s, (y0 + rnd.uniform(-90, 90)) * s),
                        fill=(250, 246, 236, 255), width=round(3 * s))
    return fn


@post("j20270121", "2027-01-21", "myth-sand-loosens-clay-" + VER, 2, TAN_T)
def sand_clay(p):
    """H, diagram: two soil panels."""
    eyebrow(p, 0, "MYTH VS MECHANISM", TAN_T)
    head(p, 0, "Myth: add sand to loosen clay soil.", TAN_T, size=80)
    p.drawn(0, 420, 420, clay_panel(False), 330, 520)
    body(p, 0, "Sand in clay packs tight and can set hard.", TAN_T, 980, size=40, w=900, align="center")
    eyebrow(p, 1, "THE MECHANISM", TAN_T)
    head(p, 1, "Add organic matter and let soil life build the crumb.", TAN_T, size=72)
    p.drawn(1, 420, 420, clay_panel(True), 330, 560)
    body(p, 1, "Fungal threads and microbial glues hold crumbs together, with air and water between.", TAN_T, 1010,
         size=36, w=900, align="center")
    for k in range(2):
        logo(p, k, TAN_T)


@post("j20270121b", "2027-01-21", "new-mexico-interest-" + VER, 1, BLUE)
def nm_interest(p):
    """G, type only, on Education Blue."""
    eyebrow(p, 0, "ACCELERATOR WORKSHOP, NEW MEXICO", BLUE, color=LG_T, y=260)
    head(p, 0, "3 to 14 May 2027", BLUE, y=330, size=130, h=330)
    body(p, 0, "Register your interest. Link in bio.", BLUE, 720, size=48)
    logo(p, 0, BLUE)


@post("j20270122", "2027-01-22", "costa-rica-building-piles-" + VER, 1, FWG)
def building(p):
    """D, full-bleed photo, a narrow strip down the left edge."""
    bleed(p, 0, f"{CR}/cr16.jpg", fx=0.6)
    band(p, 0, FWG, 0, p.h, x=0, w=380, name="strip")
    eyebrow(p, 0, "LIVE FROM COSTA RICA", FWG, x=50, y=110, w=300, color=LG_T)
    head(p, 0, "Building the piles.", FWG, x=50, y=170, w=300, size=70, h=400)
    credit(p, 0, SFW + " (Costa Rica, 2025)", FWG, x=50, w=300, y=1240)
    logo(p, 0, FWG, size=110)


@post("j20270123b", "2027-01-23", "squeeze-test-" + VER, 3, LG_T)
def squeeze(p):
    """J, numbered steps."""
    step(p, 0, 1, "Reach into the pile and squeeze a handful tight.", LG_T,
         photo=f"{SITE}/ctpfw-student-squeezing-compost-1.jpg")
    credit(p, 0, SFW, LG_T, x=540, y=1200, w=300)
    step(p, 1, 2, "A wet sheen and no drips: right where you want it.", LG_T)
    step(p, 2, 3, "Drips mean too wet. Dry and dusty means too dry.", LG_T)
    credit(p, 2, "Source: LSU AgCenter, Compost Moisture Content", LG_T)
    for k in range(3):
        logo(p, k, LG_T)


@post("j20270124", "2027-01-24", "field-notes-03-" + VER, 6, CREAM)
def field_notes(p):
    """N, field notebook: ruled lines, a label, a photo space for the graduate's own photos."""
    texts = ["Trial name, place and season.", "The question they tested.", "The method in 3 lines.",
             "The result, one big number.", "What surprised them, including what didn't work.", "Who ran it."]
    for k, t in enumerate(texts):
        for y in range(240, p.h - 120, 64):
            band(p, k, "#D9D2C2", y, 2, x=90, w=900, name="rule")
        band(p, k, "#D98A7B", 0, p.h, x=150, w=3, name="margin")
        p.d.text(k, "label", "FIELD NOTES No. 03", 190, 120, 700, 60, 40, kind="pathway", italic=False,
                 color=FWG, lh=1.0, track=3)
        p.d.text(k, "heading", t, 190, 250, 800, 260, 64, kind="montserrat-bold", italic=False, color=BROWN,
                 lh=1.15, min_size=44)
        photo_space(p, k, 190, 620, 790, 520, "the graduate's own trial photo", CREAM)
        logo(p, k, CREAM, size=110)


@post("j20270125", "2027-01-25", "spores-or-hyphae-" + VER, 2, DEEP, reel=True)
def spores(p):
    """F, specimen: two lenses side by side."""
    mid = p.h / 2
    eyebrow(p, 0, "READ THE DROP", DEEP)
    head(p, 0, "Spores or hyphae?", DEEP, size=96)
    lens(p, 0, f"{SITE}/fungal-spores-in-suspension.jpg", 300, mid + 100, 400)
    lens(p, 0, f"{NEW}/Fungal hypha, 100x obj, Marco Trevisan.jpg", 780, mid + 100, 400)
    for x, t in ((100, "SPORES: FUNGI ON PAUSE"), (580, "HYPHAE: FUNGI AT WORK")):
        p.d.text(0, "label", t, x, round(mid + 330), 400, 60, 36, kind="pathway", italic=False, color=CREAM,
                 lh=1.0, align="center", track=2)
    head(p, 1, "Hyphae on your slide mean fungi growing and working now.", DEEP, size=70)
    lens(p, 1, f"{NEW}/Fungal hypha, 100x obj, Marco Trevisan.jpg", W / 2, mid + 160, 620)
    for k in range(2):
        credit(p, k, "Micrographs: SFW library, Marco Trevisan", DEEP)
        logo(p, k, DEEP)


@post("j20270125b", "2027-01-25", "foundation-courses-10000-" + VER, 2, CREAM)
def ten_thousand(p):
    """B, big number."""
    eyebrow(p, 0, "FOUNDATION COURSES", CREAM)
    p.d.text(0, "number", "10,000+", 90, 150, 900, 240, 220, kind="montserrat-bold", italic=False, color=BROWN,
             lh=1.0)
    body(p, 0, "people in more than 100 countries started here.", CREAM, 420, size=48, w=880, color=INK)
    lens(p, 0, f"{NEW}/Bacterial-feeding nematode, 40x obj, Talbot Armstrong.jpg", 600, 900, 520)
    credit(p, 0, "Micrograph: Talbot Armstrong", CREAM)
    eyebrow(p, 1, "FOUNDATION COURSES", CREAM)
    head(p, 1, "Start any time, at your own pace.", CREAM, y=420, size=96)
    body(p, 1, "Link in bio.", CREAM, 760, size=48, color=FWG)
    for k in range(2):
        logo(p, k, CREAM)


@post("j20270126", "2027-01-26", "costa-rica-microscope-" + VER, 1, SAGE)
def cr_micro(p):
    """K, a frame waiting for the live photo from the day."""
    eyebrow(p, 0, "LIVE FROM COSTA RICA", SAGE)
    head(p, 0, "At the microscope.", SAGE, size=92)
    photo_space(p, 0, 90, 380, 900, 760, "live, from the microscopes on the day (Kavi or the mentors)", SAGE)
    logo(p, 0, SAGE)


@post("j20270127", "2027-01-27", "produce-no-waste-" + VER, 1, CREAM)
def no_waste(p):
    """H, diagram: a loop of four steps."""
    eyebrow(p, 0, "PERMACULTURE PRINCIPLE 6", CREAM)
    head(p, 0, "Produce no waste.", CREAM, size=96)
    cx, cy, r = 540, 800, 300
    names = ["PRUNINGS", "MULCH", "LIVING SOIL", "PLANTS"]
    fills = [LGREEN, TAN, BROWN, FWG]

    def ring(dr, s):
        dr.ellipse((60 * s, 60 * s, 660 * s, 660 * s), outline=LINE + (255,), width=round(4 * s))
        for i in range(4):  # arrow heads on the loop, clockwise
            a = math.radians(-45 + i * 90)
            x, y = 360 + 300 * math.cos(a), 360 + 300 * math.sin(a)
            t = a + math.pi / 2
            pts = [(x + 26 * math.cos(t), y + 26 * math.sin(t)),
                   (x + 18 * math.cos(t + 2.4), y + 18 * math.sin(t + 2.4)),
                   (x + 18 * math.cos(t - 2.4), y + 18 * math.sin(t - 2.4))]
            dr.polygon([(px * s, py * s) for px, py in pts], fill=LINE + (255,))
    p.drawn(0, 720, 720, ring, cx - 360, cy - 360)
    for i, (n, f) in enumerate(zip(names, fills)):
        a = math.radians(-90 + i * 90)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        p.drawn(0, 260, 90, lambda dr, s, f=f: dr.rounded_rectangle((0, 0, 260 * s, 90 * s), radius=45 * s,
                                                                      fill=hexrgb(f) + (255,)), x - 130, y - 45)
        p.d.text(0, "label", n, round(x - 130), round(y - 26), 260, 60, 40, kind="pathway", italic=False,
                 color=CREAM, lh=1.0, align="center", track=2)
    body(p, 0, "Prunings become mulch, scraps become compost.", CREAM, 1210, size=34, w=760, color=INK)
    logo(p, 0, CREAM)


@post("j20270128", "2027-01-28", "95-percent-food-soil-" + VER, 1, DEEP)
def ninety_five(p):
    """B, big number."""
    disc(p, 0, f"{NEW}/R5A_3966.jpg", 760, 980, 460, ring=10, ring_color=LGREEN, fy=0.5)
    eyebrow(p, 0, "SOIL IN NUMBERS", DEEP)
    p.d.text(0, "number", "95%", 90, 150, 900, 340, 330, kind="montserrat-bold", italic=False, color=CREAM, lh=1.0)
    body(p, 0, "of our food is produced in soil.", DEEP, 520, size=56, w=700, color=CREAM)
    credit(p, 0, "Source: FAO, 2017. " + SFW, DEEP, w=440)
    logo(p, 0, DEEP, size=110)


@post("j20270128b", "2027-01-28", "new-mexico-what-you-do-" + VER, 3, TAN_T)
def nm_steps(p):
    """J, numbered steps, no photos (no New Mexico photos on file yet)."""
    step(p, 0, 1, "Build, monitor and maintain your piles with a mentor.", TAN_T)
    step(p, 1, 2, "Brew a variety of liquid amendments.", TAN_T)
    step(p, 2, 3, "Microscopy sessions for beginner and advanced practitioners.", TAN_T)
    for k in range(3):
        eyebrow(p, k, "NEW MEXICO, 3 TO 14 MAY 2027", TAN_T, y=1150)
        logo(p, k, TAN_T)


@post("j20270129", "2027-01-29", "costa-rica-thank-you-" + VER, 1, CREAM)
def thank_you(p):
    """D, full-bleed photo with a cream strip."""
    bleed(p, 0, f"{CR}/cr08.jpg", fy=0.45)
    band(p, 0, CREAM, 960, 390, name="strip")
    eyebrow(p, 0, "COSTA RICA, JANUARY 2027", CREAM, y=1000)
    head(p, 0, "Thank you, Costa Rica, and thank you, Armonía.", CREAM, y=1055, size=60, w=760, h=170)
    credit(p, 0, SFW + " (Costa Rica, 2025)", CREAM, y=1280)
    logo(p, 0, CREAM, size=110)


@post("j20270130", "2027-01-30", "fun-soil-news-january-" + VER, 4, FWG)
def news(p):
    """G, type only: one place name per slide."""
    eyebrow(p, 0, "FUN SOIL NEWS", FWG, color=LG_T)
    y = head(p, 0, "January 2027.", FWG, y=380, size=130, h=330)
    body(p, 0, "Three good stories from the soil this month.", FWG, y + 30, size=46)
    stories = [("BRAZIL", "R$250 million to turn 4,000 hectares of degraded land into cocoa agroforests."),
               ("UNITED STATES", "USDA's Regenerative Pilot Program grows to $1 billion."),
               ("GERMANY", "Forest soils took up about 3% more methane each year.")]
    for k, (place, line) in enumerate(stories, start=1):
        p.d.text(k, "place", place, 90, 160, 900, 150, 130, kind="pathway", italic=False, color=LG_T, lh=1.0,
                 track=3)
        head(p, k, line, FWG, y=380, size=70)
    for k in range(4):
        logo(p, k, FWG)


@post("j20270131", "2027-01-31", "meet-ib-borup-pedersen-" + VER, 1, TAN_T)
def ib(p):
    """K, framed portrait, heading above."""
    eyebrow(p, 0, "MEET THE TEAM", TAN_T)
    head(p, 0, "Ib Borup Pedersen", TAN_T, size=84, h=110)
    body(p, 0, "Farmer, Soil Food Web Consultant and mentor", TAN_T, 245, size=40, color=FWG)
    framed(p, 0, f"{SITE}/ib.jpg", 190, 380, 700, 760, fy=0.35)
    credit(p, 0, SFW, TAN_T)
    logo(p, 0, TAN_T)


FAMILY = {  # family letter and the one-line visual note for each post
    "j20270101": "G, type only", "j20270102": "H, diagram", "j20270103": "K, framed photo",
    "j20270104": "F, specimen", "j20270105": "I, portrait", "j20270106": "D, full-bleed photo",
    "j20270107": "H, diagram", "j20270108": "K, framed photo", "j20270109a": "D, full-bleed photo",
    "j20270110a": "K, framed photo", "j20270110c": "G, type only", "j20270111": "L, photo grid",
    "j20270112": "B, big number", "j20270113": "I, portrait", "j20270114": "M, event card",
    "j20270115": "K, framed photo", "j20270115b": "G, type only", "j20270116": "J, numbered steps",
    "j20270117": "D, full-bleed photo", "j20270118b": "F, specimen", "j20270119": "I, portrait",
    "j20270119b": "K, framed photo", "j20270120": "C, article card", "j20270121": "H, diagram",
    "j20270121b": "G, type only", "j20270122": "D, full-bleed photo", "j20270123b": "J, numbered steps",
    "j20270124": "N, field notebook", "j20270125": "F, specimen", "j20270125b": "B, big number",
    "j20270126": "K, framed photo", "j20270127": "H, diagram", "j20270128": "B, big number",
    "j20270128b": "J, numbered steps", "j20270129": "D, full-bleed photo", "j20270130": "G, type only",
    "j20270131": "K, framed photo",
}

if __name__ == "__main__":
    for pid in sys.argv[1:] or [k for k in REG if k in FAMILY]:
        r = build(pid)
        print(pid, r["tiles"])
