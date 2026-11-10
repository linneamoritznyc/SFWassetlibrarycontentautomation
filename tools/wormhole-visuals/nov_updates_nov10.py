"""November updates (Linnea, 10 Nov): nematodes (p24), Veterans Day (vet20261111), Small Business Saturday with
Colleen Dempster of Rewild Soils (x20261128), Cyber Monday (nmw10rs3la2i). Thanksgiving (thx20261126) is
thanksgiving_staff.py. 1080 x 1350, docs/slide-rules.md: Montserrat Bold headings, Source Sans 3 body, brand
colours, every text box editable, logo on every slide. Missing photos are marked photo boxes until they arrive.

  python3 tools/wormhole-visuals/nov_updates_nov10.py <post|all> <version> [tiles dir] [decks dir]
"""
import math
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
SUZ_PHOTO = os.environ.get("SUZ_PHOTO", "")   # Suzanne planting by the hoop house, blue sky (to come)


def edge_photo(d, k, label, fy=0.4):
    if SUZ_PHOTO and os.path.exists(SUZ_PHOTO):
        ph = ImageOps.exif_transpose(Image.open(SUZ_PHOTO)).convert("RGB")
        d.bg(k, cover(ph, W, H, 0.5, fy).convert("RGBA"), name=f"Photo: {label}")
    else:
        d.bg(k, grain(Image.new("RGB", (W, H), CREAM), 500 + k, 3), name="Background: Organic Cream")
        photo_box(d, k, label, 0, 0, W, H)


def veterans(v):
    """Suzanne presented at the Farmer Veteran Coalition Stakeholders Conference (Williamsburg, Virginia, Oct 2026).
    Warm and respectful, no flags or military imagery. The photo runs edge to edge; text sits in a Soil Brown box."""
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    # 1
    edge_photo(d, 0, "Suzanne Shea planting by the hoop house (edge to edge)")
    hh = height("Happy Veterans Day", 86, 840)
    bh = round(hh + 24 + 70 + 100)
    rect(d, 0, "Brown box", 72, H - 72 - bh, 936, bh, rgb(BROWN) + (255,))
    T(d, 0, "Headline", "Happy Veterans Day", 72, H - 72 - bh + 50, 936, hh + 6, 86, color=CREAM)
    T(d, 0, "Details", "To every veteran who now farms", 72, H - 72 - bh + 50 + round(hh) + 24, 936, 70, 52,
      bold=False, color=CREAM)
    logo(d, 0, w=140, x=W - 72 - 140 - 10, y=60)
    # 2
    edge_photo(d, 1, "Suzanne Shea at the conference", fy=0.3)
    hh = height("Scaling Sustainably", 84, 840)
    dh = height("Suzanne Shea at the Farmer Veteran Coalition Stakeholders Conference", 52, 820, bold=False, lh=1.22)
    bh = round(hh + 24 + dh + 100)
    rect(d, 1, "Brown box", 72, H - 72 - bh, 936, bh, rgb(BROWN) + (255,))
    T(d, 1, "Headline", "Scaling Sustainably", 72, H - 72 - bh + 50, 936, hh + 6, 84, color=CREAM)
    T(d, 1, "Details", "Suzanne Shea at the Farmer Veteran Coalition Stakeholders Conference", 130,
      H - 72 - bh + 50 + round(hh) + 24, 820, dh + 6, 52, bold=False, color=CREAM, lh=1.22)
    logo(d, 1, w=140, x=W - 72 - 140 - 10, y=60)
    # 3: room for more of Suzanne's photos
    d.bg(2, grain(Image.new("RGB", (W, H), CREAM), 503, 3), name="Background: Organic Cream")
    photo_box(d, 2, "More from Suzanne", 72, 72, 936, 560)
    photo_box(d, 2, "More from Suzanne", 72, 660, 936, 480)
    logo(d, 2, white=False, w=150)
    return d


# ---------------- 4. Small Business Saturday: Colleen Dempster, Rewild Soils ----------------
RW = "/home/user/sfwlib/social/rewild"
RW_PHOTO = f"{RW}/compost-toronto-microscope.jpg"   # Compost Toronto event, Toronto community garden (Allison, 10 Nov)


def framed(im, w, h, fx=0.5, fy=0.5, border=14):
    out = Image.new("RGB", (w, h), (251, 248, 241))
    out.paste(cover(im, w - 2 * border, h - 2 * border, fx, fy), (border, border))
    return out.convert("RGBA")


def small_business(v):
    """Facts from rewildsoils.com (10 Nov) and Colleen's note to Allison."""
    d = Deck("x20261128", 3, f"small-business-saturday-rewild-soils-{v}", "2026-11-28")
    ph = ImageOps.exif_transpose(Image.open(RW_PHOTO)).convert("RGB")
    # 1. photo over a green box
    d.bg(0, grain(Image.new("RGB", (W, H), GREEN), 601, 4), name="Background: Food Web Green")
    d.put(0, "Photo: Compost Toronto microscope event", cover(ph, W, 850, 0.5, 0.4).convert("RGBA"), 0, 0,
          shadowed=False, anchor="tl")
    T(d, 0, "Headline", "Happy Small Business Saturday", 72, 890, 936, 200, 84, color=CREAM)
    T(d, 0, "Details", "Meet Colleen Dempster of Rewild Soils", 72, 1090, 760, 140, 52, bold=False, color=CREAM)
    logo(d, 0, w=150)
    # 2. her microscope work
    d.bg(1, grain(Image.new("RGB", (W, H), CREAM), 602, 3), name="Background: Organic Cream")
    d.put(1, "Photo: compost under the microscope", framed(ph, 760, 600, 0.75, 0.55), 160, 90, shadowed=False,
          anchor="tl")
    y = T(d, 1, "Headline", "A Soil Food Web certified microscopy lab since 2022", 72, 740, 936, 230, 66, color=BROWN)
    T(d, 1, "Details", "Colleen has looked at hundreds of soil, compost and compost tea samples. Here she shows "
      "compost on the monitor at a Compost Toronto event.", 110, round(y) + 24, 860, 320, 50, bold=False, color=INK,
      lh=1.22)
    logo(d, 1, white=False, w=150)
    # 3. meet Rewild Soils
    d.bg(2, grain(Image.new("RGB", (W, H), CREAM), 603, 3), name="Background: Organic Cream")
    T(d, 2, "Headline", "Meet Rewild Soils", 72, 130, 936, 110, 86, color=BROWN)
    lg = Image.open(f"{RW}/rewild-soils-logo.png").convert("RGBA")
    lg = lg.resize((800, round(lg.height * 800 / lg.width)), Image.LANCZOS)
    d.put(2, "Rewild Soils logo", lg, (W - lg.width) // 2, 300, shadowed=False, anchor="tl")
    T(d, 2, "Details", "Soil microscopy, consulting, workshops and Biologically Complete compost, from Uxbridge, "
      "Ontario", 120, 300 + lg.height + 60, 840, 220, 52, bold=False, color=INK, lh=1.22)
    rect(d, 2, "Green box", 190, 1040, 700, 110, rgb(GREEN) + (255,), r=55)
    T(d, 2, "Website", "rewildsoils.com", 190, 1060, 700, 72, 58, color=CREAM)
    logo(d, 2, white=False, w=150)
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
