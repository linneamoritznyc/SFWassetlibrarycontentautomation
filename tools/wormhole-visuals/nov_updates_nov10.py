"""November updates (Linnea, 10 Nov): nematodes (p24), Veterans Day (vet20261111), Small Business Saturday with
Colleen Dempster of Rewild Soils (x20261128), Cyber Monday (nmw10rs3la2i). Thanksgiving (thx20261126) is
thanksgiving_staff.py. 1080 x 1350, docs/slide-rules.md: Montserrat Bold headings, Source Sans 3 body, brand
colours, every text box editable, logo on every slide. Missing photos are marked photo boxes until they arrive.

  python3 tools/wormhole-visuals/nov_updates_nov10.py <post|all> <version> [tiles dir] [decks dir]
"""
import math

import numpy as np
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import T, height
from bundle_v6 import H, W, fade
from collage import Deck, cover
from nov_fill import DECKS, TILES

_put = Deck.put
Deck.put = lambda self, k, name, im, x, y, **kw: _put(self, k, name, im, round(x), round(y), **kw)

GREEN, BROWN, CREAM, INK, BLUE, MINT = "#156826", "#4F3433", "#F4F1EA", "#333130", "#3780B8", "#A8D5B0"
WHITE_LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
COLOR_LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
NEW = "/home/user/photos/new-2026-10"


def logo(d, k, white=True, w=160, x=None, y=None):
    lg = Image.open(WHITE_LOGO if white else COLOR_LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 60 - w if x is None else x, H - 50 - lg.height if y is None else y, shadowed=False,
          anchor="tl")


def rect(d, k, name, x, y, w, h, fill, r=0, outline=None, width=0):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    if r:
        dr.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=outline, width=width)
    else:
        dr.rectangle((0, 0, w - 1, h - 1), fill=fill, outline=outline, width=width)
    d.put(k, name, im, x, y, shadowed=False, anchor="tl")


def photo_box(d, k, label, x, y, w, h, dark=False):
    """A clearly marked empty photo box: dashed frame and a label, to be swapped for the real photo."""
    im = Image.new("RGBA", (w, h), rgb("#D9D4C8") + (255,))
    dr = ImageDraw.Draw(im)
    c = rgb("#7C7468") + (255,)
    for i in range(0, 2 * (w + h), 36):   # dashed border
        for a, b in ((0, w), (w, w + h), (w + h, 2 * w + h), (2 * w + h, 2 * (w + h))):
            pass
    for xx in range(12, w - 12, 34):
        dr.line((xx, 12, min(xx + 18, w - 12), 12), fill=c, width=4)
        dr.line((xx, h - 13, min(xx + 18, w - 12), h - 13), fill=c, width=4)
    for yy in range(12, h - 12, 34):
        dr.line((12, yy, 12, min(yy + 18, h - 12)), fill=c, width=4)
        dr.line((w - 13, yy, w - 13, min(yy + 18, h - 12)), fill=c, width=4)
    d.put(k, f"PHOTO BOX: {label}", im, x, y, shadowed=False, anchor="tl")
    T(d, k, "Photo box label", f"PHOTO: {label}", x + 30, y + h // 2 - 40, w - 60, 90, 42, bold=True, color="#7C7468",
      mn=42)


# ---------------- 1. nematodes (p24), Stephanie's comment ----------------
def nematodes(v):
    d = Deck("p24", 3, f"soil-in-numbers-nematodes-{v}", "2026-11-11")
    first = Image.open(os.path.join(TILES, "p24-v2-1.jpg")).convert("RGB")
    black = Image.new("RGB", (W, H), (0, 0, 0))
    black.paste(first.crop((0, 170, W, 860)), (0, 270))
    d.bg(0, black.convert("RGBA"), name="Photo: nematode")
    hh = height("The most common animal on earth", 86, 900)
    T(d, 0, "Headline", "The most common animal on earth", 72, 110, 936, hh + 6, 86, color=CREAM)   # centred
    bh = height("440 quintillion nematodes", 84, 820)
    top = 930
    rect(d, 0, "Green box", 90, top, 900, round(bh) + 80, rgb(GREEN) + (255,))
    T(d, 0, "Details", "440 quintillion nematodes", 72, top + 40, 936, bh + 6, 84, color=CREAM)
    T(d, 0, "Credit", "Photo: Soil Food Web Foundation", 72, top + round(bh) + 100, 936, 56, 42, bold=False,
      color="#CFC8BC", mn=42)
    logo(d, 0, w=140)
    for k, (f, text, credit) in enumerate([
            ("Bacterial-feeding nematode (omnivore), 40x obj, Johannes Veith.jpg", "About 57 billion for every person alive",
             "Photo: Johannes Veith"),
            ("Bacterial-feeding nematode (omnivore), 40x obj, Keisha Wheeler.jpg", "Most feed on bacteria and fungi",
             "Photo: Keisha Wheeler")], start=1):
        ph = ImageOps.exif_transpose(Image.open(f"{NEW}/{f}")).convert("RGB")
        d.bg(k, cover(ph, W, H, 0.5, 0.45).convert("RGBA"), name="Photo: nematode")
        bh = height(text, 84, 820)
        top = H - 230 - round(bh)
        rect(d, k, "Green box", 90, top, 900, round(bh) + 80, rgb(GREEN) + (255,))
        T(d, k, "Headline", text, 72, top + 40, 936, bh + 6, 84, color=CREAM)
        rect(d, k, "Credit box", 290, top + round(bh) + 100, 500, 60, rgb(GREEN) + (255,))
        T(d, k, "Credit", credit, 290, top + round(bh) + 104, 500, 56, 42, bold=False, color=CREAM, mn=42)
        logo(d, k, w=140)
    return d


# ---------------- 2. Veterans Day: Suzanne Shea's talk (Linnea's updated brief, 10 Nov) ----------------
VET = "/home/user/sfwlib/social/veterans"   # Suzanne's own photos, sent by Linnea 10 Nov
SUZ_PHOTO = os.environ.get("SUZ_PHOTO", f"{VET}/suzanne-hoop-house.jpg")
SUZ_FVC = f"{VET}/suzanne-fvc-conference.jpg"
SUZ_WALK = f"{VET}/suzanne-conference-walk.jpg"


def edge_photo(d, k, label, fy=0.4, path=None, fx=0.5):
    path = path or SUZ_PHOTO
    if path and os.path.exists(path):
        ph = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        d.bg(k, cover(ph, W, H, fx, fy).convert("RGBA"), name=f"Photo: {label}")
    else:
        d.bg(k, grain(Image.new("RGB", (W, H), CREAM), 500 + k, 3), name="Background: Organic Cream")
        photo_box(d, k, label, 0, 0, W, H)


def veterans(v):
    """Suzanne Shea's own photos (Linnea, 10 Nov). v6: no boxes. Slide 1 sets the type in the blue sky of the
    hoop-house photo; slide 2 hangs the conference photo like a print in a cream mat with a museum-style label;
    slide 3 is her selfie edge to edge."""
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    # 1. type in the sky
    hh = ImageOps.exif_transpose(Image.open(SUZ_PHOTO)).convert("RGB")
    d.bg(0, cover(hh, W, H, 0.5, 0.0).convert("RGBA"), name="Photo: Suzanne Shea planting by the hoop house")
    # one left edge for both boxes, generous gap between headline and byline, 72 px right margin
    y = T(d, 0, "Headline", "Scaling\nSustainably", 468, 110, 540, 200, 86, color="#FFFFFF", align="left", lh=1.1)
    T(d, 0, "Details", "A talk by Suzanne Shea", 468, round(y) + 40, 540, 70, 52, bold=False,
      color="#FFFFFF", align="left")
    logo(d, 0, w=210)
    # 2. the conference photo as a matted print
    d.bg(1, grain(Image.new("RGB", (W, H), CREAM), 504, 3), name="Background: Organic Cream")
    fvc = ImageOps.exif_transpose(Image.open(SUZ_FVC)).convert("RGB")
    pw, ph_ = 860, 860
    pr = cover(fvc, pw, ph_, 0.5, 0.45).convert("RGBA")
    mat = Image.new("RGBA", (pw + 2, ph_ + 2), rgb(BROWN) + (255,))   # brown hairline round the print
    mat.paste(pr, (1, 1))
    d.put(1, "Photo: Suzanne Shea at the Farmer Veteran Coalition conference", mat, (W - pw) // 2, 80,
          anchor="tl", shadowed=True)
    y = T(d, 1, "Headline", "Suzanne Shea", 72, 80 + ph_ + 50, 936, 86, 73, color=BROWN)
    T(d, 1, "Details", "Farmer Veteran Coalition\nStakeholders Conference", 72, round(y) + 16,
      936, 130, 52, bold=False, color=INK, lh=1.15)
    logo(d, 1, white=False, w=170)
    # 3. her selfie, edge to edge
    edge_photo(d, 2, "Suzanne Shea on the conference walk", fy=0.5, path=SUZ_WALK, fx=0.12)
    logo(d, 2, w=210)
    return d


# ---------------- 4. Small Business Saturday: Colleen Dempster, Rewild Soils ----------------
RW = "/home/user/sfwlib/social/rewild"
RW_PHOTO = f"{RW}/compost-toronto-microscope.jpg"   # Compost Toronto event, Toronto community garden (Allison, 10 Nov)


def framed(im, w, h, fx=0.5, fy=0.5, border=14):
    out = Image.new("RGB", (w, h), (251, 248, 241))
    out.paste(cover(im, w - 2 * border, h - 2 * border, fx, fy), (border, border))
    return out.convert("RGBA")


def scrim(im, start=0.5, strength=0.78):
    """Darken the lower part of a photo with a soft gradient so cream type reads without a box."""
    w, h = im.size
    g = Image.linear_gradient("L").resize((w, h))
    g = g.point(lambda v: 0 if v < start * 255 else int(((v - start * 255) / (255 - start * 255)) ** 1.4 * 255 * strength))
    dark = Image.new("RGB", (w, h), (20, 26, 18))
    return Image.composite(dark, im.convert("RGB"), g)


MIC = "/home/user/photos/new-2026-10"


def eyepiece(path, D, fx=0.5, fy=0.5, zoom=1.0):
    """A round view down the microscope: circle crop, soft dark vignette at the edge, thin dark rim."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    big = cover(im, round(D * zoom), round(D * zoom), fx, fy)
    o = (big.width - D) // 2
    im = big.crop((o, o, o + D, o + D))
    yy, xx = np.mgrid[0:D, 0:D].astype(np.float32)
    r = np.sqrt((xx - D / 2) ** 2 + (yy - D / 2) ** 2) / (D / 2)
    shade = np.clip((r - 0.72) / 0.28, 0, 1) ** 2 * 0.75
    arr = np.asarray(im).astype(np.float32) * (1 - shade[..., None]) + 22 * shade[..., None]
    im = Image.fromarray(arr.clip(0, 255).astype("uint8")).convert("RGBA")
    mask = Image.new("L", (D * 4, D * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, D * 4 - 1, D * 4 - 1), fill=255)
    im.putalpha(mask.resize((D, D), Image.LANCZOS))
    rim = Image.new("RGBA", (D * 4, D * 4), (0, 0, 0, 0))
    ImageDraw.Draw(rim).ellipse((6, 6, D * 4 - 7, D * 4 - 7), outline=(40, 32, 30, 255), width=36)
    im.alpha_composite(rim.resize((D, D), Image.LANCZOS))
    return im


def small_business(v):
    """Colleen Dempster, Rewild Soils (her own answers, sent by Linnea 10 Nov). Linnea: about Colleen and why she
    uses the soil food web, not her services; never tilt a photo. v16: one design system across the carousel, a
    cream naturalist's page with a fine brown frame and one left margin, and real soil micrographs as round
    eyepiece views (Colleen's microscope). Micrograph credits on the slides."""
    d = Deck("x20261128", 6, f"small-business-saturday-rewild-soils-{v}", "2026-11-28")
    ph = ImageOps.exif_transpose(Image.open(RW_PHOTO)).convert("RGB")
    lg = Image.open(f"{RW}/rewild-soils-logo.png").convert("RGBA")
    rr = lg.crop((0, 0, 505, lg.height))
    rr = rr.crop(rr.getchannel("A").point(lambda a: 255 if a > 100 else 0).getbbox())
    fern = lg.crop((386, 15, 462, 330))
    fern = fern.crop(fern.getchannel("A").point(lambda a: 255 if a > 100 else 0).getbbox())
    M = 110          # the one left margin
    TW = W - 2 * M   # text width

    def page(k):
        d.bg(k, grain(Image.new("RGB", (W, H), CREAM), 620 + k, 4), name="Background: Organic Cream")
        rect(d, k, "Page frame", 44, 44, W - 88, H - 88, (0, 0, 0, 0), outline=rgb(BROWN) + (255,), width=2)

    def credit(k, text, x, y, w=TW, align="left"):
        T(d, k, "Photo credit", text, x, y, w, 56 * (text.count("\n") + 1), 42, bold=False, color=BROWN, align=align)

    def sfw(k):
        logo(d, k, white=False, w=140, x=W - 80 - 140, y=H - 80 - 140)

    # 1. cover: the photo, straight, then the name
    page(0)
    d.put(0, "Photo: Colleen at a Compost Toronto microscope event", cover(ph, W - 2 * 80, 700, 0.45, 0.45).convert("RGBA"),
          80, 80, shadowed=False, anchor="tl")
    T(d, 0, "Eyebrow", "Small Business Saturday", M, 840, TW, 66, 52, color=GREEN, align="left")
    y = T(d, 0, "Headline", "Meet Colleen\nDempster", M, 915, 640, 190, 86, color=BROWN, align="left", lh=1.06)
    T(d, 0, "Details", "Rewild Soils, Uxbridge, Ontario", M, round(y) + 22, 700, 70, 52, bold=False, color=INK,
      align="left")
    sfw(0)

    # 2. the lab: an eyepiece view
    page(1)
    D = 700
    d.put(1, "Micrograph: testate amoeba, 40x, Robert Kenyon",
          eyepiece(f"{MIC}/Testate amoeba (reproducing), 40x obj, Robert Kenyon.jpg", D, 0.52, 0.45, 1.25),
          (W - D) // 2, 100, shadowed=False, anchor="tl")
    credit(1, "Testate amoeba, 40x. Robert Kenyon", 0, 100 + D + 14, W, align="center")
    y = T(d, 1, "Headline", "A Soil Food Web certified lab since 2022", M, 900, TW - 40, 170, 70, color=BROWN,
          align="left", lh=1.06)
    T(d, 1, "Details", "Re-certified every year, with more than 300 microbial reports", M, round(y) + 20, 700, 140,
      52, bold=False, color=INK, align="left", lh=1.18)
    sfw(1)

    # 3. her words, with a second eyepiece view
    page(2)
    T(d, 2, "Quote mark", "\u201c", M - 6, 260, 200, 200, 240, color=GREEN, align="left")
    y = T(d, 2, "Quote", "Most people have never seen the microbes that make up the soil food web, so I show "
          "pictures and do live microscope demonstrations", M, 480, TW, 520, 62, color=BROWN, align="left", lh=1.12)
    T(d, 2, "Name", "Colleen Dempster", M, round(y) + 36, TW, 70, 52, bold=False, color=INK, align="left")
    sfw(2)

    # 4. her path into the soil food web
    page(3)
    T(d, 3, "Headline", "Colleen\u2019s path", M, 130, TW, 90, 73, color=BROWN, align="left")
    steps = [("Started slowly", "as a stay-at-home mom, alongside another part-time job"),
             ("2022", "became a Soil Food Web\ncertified lab"),
             ("Now", "finishing the last steps to become a Soil Food Web Consultant")]
    y, xs = 330, M + 90
    tops = []
    for i, (h1, h2) in enumerate(steps):
        tops.append(y)
        hh = height(h1, 66, 700)
        T(d, 3, f"Step {i + 1} title", h1, xs, y, 700, hh + 6, 66, color=GREEN, align="left")
        dh = height(h2, 52, 740, bold=False, lh=1.18)
        T(d, 3, f"Step {i + 1} text", h2, xs, y + round(hh) + 10, 740, dh + 6, 52, bold=False, color=INK,
          align="left", lh=1.18)
        y += round(hh + 10 + dh) + 76
    rect(d, 3, "Path line", M + 21, tops[0] + 40, 3, tops[-1] - tops[0], rgb(BROWN) + (255,))
    for i, ty in enumerate(tops):
        rect(d, 3, f"Path node {i + 1}", M, ty + 18, 44, 44, rgb(CREAM) + (255,), r=22, outline=rgb(BROWN) + (255,),
             width=3)
        rect(d, 3, f"Path node {i + 1} centre", M + 12, ty + 30, 20, 20, rgb(GREEN) + (255,), r=10)
    sfw(3)

    # 5. her words over fungal hyphae, edge to edge inside the frame
    page(4)
    hy = ImageOps.exif_transpose(Image.open(f"{MIC}/Fungal hypha, 100x obj, Marco Trevisan.jpg")).convert("RGB")
    hy = cover(hy, W - 160, H - 160, 0.62, 0.45)
    hy = Image.blend(hy, Image.new("RGB", hy.size, (244, 241, 234)), 0.45)
    d.put(4, "Micrograph: fungal hypha, 100x, Marco Trevisan", hy.convert("RGBA"), 80, 80, shadowed=False, anchor="tl")
    T(d, 4, "Quote mark", "\u201c", M - 6, 150, 200, 200, 240, color=GREEN, align="left")
    y = T(d, 4, "Quote", "Making compost and exploring samples under the microscope will always be something I enjoy",
          M, 380, 800, 420, 66, color=BROWN, align="left", lh=1.1)
    T(d, 4, "Details", "Colleen believes rewilding soils with microbes is about restoring systems and people\u2019s "
      "connection with the Earth", M, round(y) + 50, 860, 300, 52, bold=False, color=INK, align="left", lh=1.18)
    credit(4, "Fungal hypha, 100x. Marco Trevisan", M, H - 80 - 80, 700)
    sfw(4)

    # 6. learn it yourself
    page(5)
    y = T(d, 5, "Headline", "Our Foundation Courses teach you to work out what your soil needs", M, 150, TW, 340, 73,
          color=BROWN, align="left", lh=1.08)
    y = T(d, 5, "Details", "Learn to assess bacteria, fungi, protozoa, and nematodes", M, round(y) + 34, 760, 140, 54,
          bold=False, color=INK, align="left", lh=1.18)
    rect(d, 5, "Green pill", M, round(y) + 56, 440, 104, rgb(GREEN) + (255,), r=52)
    T(d, 5, "Link in bio", "Link in bio", M, round(y) + 56 + 18, 440, 70, 54, color=CREAM)
    rect(d, 5, "Divider", M, 960, TW, 2, rgb(BROWN) + (255,))
    T(d, 5, "Thanks", "With thanks to Colleen Dempster", M, 990, TW, 70, 50, bold=False, color=INK, align="left")
    l6 = lg.resize((300, round(lg.height * 300 / lg.width)), Image.LANCZOS)
    d.put(5, "Rewild Soils logo", l6, M - 10, 1080, shadowed=False, anchor="tl")
    sfw(5)
    return d


# ---------------- 5. Cyber Monday: calm cover, a real photo and a brand-colour box (Linnea: nothing salesy) ----------
def cyber(v):
    d = Deck("nmw10rs3la2i", 3, f"cyber-monday-{v}", "2026-11-30")
    d.bg(0, grain(Image.new("RGB", (W, H), GREEN), 701, 4), name="Background: Food Web Green")
    ph = ImageOps.exif_transpose(Image.open(f"{NEW}/card-classroom-microscope-notebook.jpg")).convert("RGB")
    d.put(0, "Photo: microscopy notes", cover(ph, W, 850, 0.45, 0.5).convert("RGBA"), 0, 0, shadowed=False,
          anchor="tl")
    T(d, 0, "Headline", "Cyber Monday", 72, 900, 936, 110, 86, color=CREAM)
    T(d, 0, "Details", "[DISCOUNT] off online courses\nNov 30 to Dec 4", 72, 1030, 760, 160, 52, bold=False,
      color=CREAM, lh=1.25)
    logo(d, 0, w=150)
    # 2. the programs in the sale (the FC + CIC bundle and the workshops are excluded)
    d.bg(1, grain(Image.new("RGB", (W, H), CREAM), 702, 3), name="Background: Organic Cream")
    T(d, 1, "Headline", "Online courses in the sale", 72, 90, 936, 110, 73, color=BROWN)
    names = ["Foundation Courses", "Compost Intensive", "Permaculture Design Certificate", "Complete Practicum",
             "Advanced Programs", "Intro to the Foundation Courses"]
    tw, th, g = 453, 250, 30
    for n, name in enumerate(names):
        x, y = 72 + (n % 2) * (tw + g), 250 + (n // 2) * (th + g)
        rect(d, 1, f"Badge {n + 1}", x, y, tw, th, rgb(GREEN) + (255,), r=28)
        T(d, 1, f"Badge {n + 1} name", name, x + 12, y + 30, tw - 24, th - 60, 52, color=CREAM, mn=50, lh=1.15)
    T(d, 1, "Details", "[DISCOUNT] off, Nov 30 to Dec 4", 72, 1120, 760, 70, 52, bold=False, color=INK)
    logo(d, 1, white=False, w=150)
    # 3. link in bio
    d.bg(2, grain(Image.new("RGB", (W, H), GREEN), 703, 4), name="Background: Food Web Green")
    T(d, 2, "Headline", "Link in bio", 72, 520, 936, 110, 86, color=CREAM)
    T(d, 2, "Details", "Cyber Monday, Nov 30 to Dec 4", 72, 650, 936, 70, 52, bold=False, color=CREAM)
    lg = Image.open(WHITE_LOGO).convert("RGBA")
    lg = lg.resize((300, round(lg.height * 300 / lg.width)), Image.LANCZOS)
    d.put(2, "SFW logo", lg, (W - 300) // 2, 820, shadowed=False, anchor="tl")
    return d


# ---------------- 6. Carla at Food as Medicine for All (Livestream, 14-15 Nov 2026) ----------------
CARLA = "/home/user/sfwlib/social/carla-portugal-fam-flyer.jpg"   # cropped from the conference flyer (small)


def fam(v):
    """Facts from the conference flyer and Linnea's note (10 Nov): Dr. Carla Portugal speaks Sun 15 Nov, 7 to 7:45am
    Pacific, at the 2026 Food as Medicine for All Livestream Conference (14-15 Nov). Discount code goes in the caption."""
    d = Deck("fam20261110", 2, f"carla-food-as-medicine-{v}", "2026-11-10")
    ph = ImageOps.exif_transpose(Image.open(CARLA)).convert("RGB")
    # 1. speaker card
    d.bg(0, grain(Image.new("RGB", (W, H), CREAM), 801, 3), name="Background: Organic Cream")
    T(d, 0, "Eyebrow", "FOOD AS MEDICINE FOR ALL", 72, 90, 936, 70, 52, color=GREEN, mn=50)
    pw, phh = 400, 530
    pic = Image.new("RGB", (pw, phh), (251, 248, 241))
    pic.paste(cover(ph, pw - 24, phh - 24, 0.5, 0.35), (12, 12))
    d.put(0, "Photo: Dr. Carla Portugal", pic.convert("RGBA"), (W - pw) // 2, 190, shadowed=False, anchor="tl")
    T(d, 0, "Headline", "Dr. Carla Portugal speaks on soil and nutrition", 72, 760, 936, 200, 73, color=BROWN)
    T(d, 0, "Details", "Sunday 15 November, 7 to 7:45am Pacific\nLivestream conference", 72, 960, 936, 140, 52,
      bold=False, color=INK, lh=1.25)
    logo(d, 0, white=False, w=150)
    # 2. her talk
    d.bg(1, grain(Image.new("RGB", (W, H), GREEN), 802, 4), name="Background: Food Web Green")
    T(d, 1, "Eyebrow", "HER TALK", 72, 150, 936, 70, 52, color=MINT, mn=50)
    y = T(d, 1, "Headline", "Restoring the Soil Food Web to Grow Nutrition Your Patients Need", 72, 240, 936, 340,
          73, color=CREAM)
    y = T(d, 1, "Details", "The nutrient density of food is partly a biological property of the soil it grew in. "
          "Carla translates soil biology into clinical language for nutrition specialists.", 110, round(y) + 40, 860,
          340, 52, bold=False, color=CREAM, lh=1.25)
    T(d, 1, "CTA", "2026 Food as Medicine for All, 14 to 15 November. Link in bio", 110, round(y) + 50, 860, 140, 52,
      color=MINT, lh=1.2)
    logo(d, 1, w=150)
    return d


POSTS = {"nematodes": nematodes, "veterans": veterans, "smallbiz": small_business, "cyber": cyber, "fam": fam}

if __name__ == "__main__":
    which, v = sys.argv[1], sys.argv[2]
    tiles = sys.argv[3] if len(sys.argv) > 3 else TILES
    decks = sys.argv[4] if len(sys.argv) > 4 else DECKS
    for name in (POSTS if which == "all" else [which]):
        d = POSTS[name](v)
        print(d.save(tiles, decks)[0], d.pptx_name())
