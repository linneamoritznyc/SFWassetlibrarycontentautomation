"""Carla at Food as Medicine for All (10 Nov post, talk Sun 15 Nov 7 to 7:45am Pacific). Linnea's brief, 10 Nov:
cream page with the Small Business Saturday frame and logo, eyepiece circles for photos, Montserrat Bold headings,
Source Sans 3 for the rest, three sizes per slide (70 / 50 / 42), Soil Brown text, green accent, everything centred.

  1 conference speaker grid (Linnea uploads; photo space until then)
  2 Carla's session card, unchanged
  3 Plants have a gut microbiome too (4 micrographs from the microbe library, credited)
  4 From soil to plate (3 engraving-style drawings)
  5 Watch Carla live

  python3 tools/wormhole-visuals/carla_fam_v2.py <version>
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import T
from bundle_v6 import H, W
from collage import Deck, cover
from nov_fill import DECKS, TILES
from nov_updates_nov10 import BROWN, CREAM, GREEN, eyepiece, logo, rect

MIC = "/home/user/sfwlib/social/carla-fam"
FLYER = f"{MIC}/session-card.webp"   # Carla's session card from the organisers
PORTRAIT = "/home/user/sfwlib/social/carla-fam/carla-sfw-team.jpg"   # soilfoodweb.com team page
BIG, MED, SMALL = 70, 50, 42


def page(d, k):
    d.bg(k, grain(Image.new("RGB", (W, H), CREAM), 640 + k, 4), name="Background: Organic Cream")
    rect(d, k, "Page frame", 44, 44, W - 88, H - 88, (0, 0, 0, 0), outline=rgb(BROWN) + (255,), width=2)


def sfw(d, k):
    logo(d, k, white=False, w=130, x=W - 80 - 30 - 130, y=H - 80 - 130)


def drawing(name, h):
    la = Image.open(f"/home/user/sfwlib/social/lineart/{name}.png").convert("L")
    al = la.point(lambda v: max(0, min(255, int((v - 40) * 1.6)))).filter(ImageFilter.MaxFilter(3))
    im = Image.new("RGBA", la.size, rgb(BROWN) + (0,))
    im.putalpha(al)
    im = im.crop(al.getbbox())
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def build(v):
    d = Deck("fam20261110", 5, f"carla-food-as-medicine-{v}", "2026-11-10")
    # 1. speaker grid: Linnea uploads the conference graphic; a marked space until then
    page(d, 0)
    rect(d, 0, "Photo space", 80, 80, W - 160, H - 160, rgb("#E2DDD3") + (255,))
    T(d, 0, "Photo space label", "PHOTO: the conference speaker grid,\nunchanged (Linnea uploads)", 72, 600, 936, 150,
      MED, bold=False, color=BROWN)
    # 2. Carla's session card, unchanged, as large as the frame allows, with a heading and the date
    page(d, 1)
    T(d, 1, "Headline", "Carla speaks at\nFood as Medicine for All", 72, 120, 936, 170, BIG, color=BROWN, lh=1.06)
    fl = ImageOps.exif_transpose(Image.open(FLYER)).convert("RGB")
    fw = W - 120
    fl = fl.resize((fw, round(fl.height * fw / fl.width)), Image.LANCZOS)
    d.put(1, "Carla's session card (from the organisers)", fl.convert("RGBA"), 60, 340, shadowed=True, anchor="tl")
    T(d, 1, "Date", "Sunday 15 November, 7 to 7:45am Pacific", 72, 340 + fl.height + 50, 936, 70, MED, bold=False,
      color=BROWN)
    sfw(d, 1)
    # 3. plants have a gut microbiome too (pre-cropped squares around each organism, from the microbe library)
    page(d, 2)
    T(d, 2, "Headline", "Plants have a gut\nmicrobiome too", 72, 96, 936, 170, BIG, color=BROWN, lh=1.06)
    mics = [("crop-bacteria-john-ash.jpg", "Bacteria \u00b7 John Ash"),
            ("crop-fungal-hyphae-tanja-dekker.jpg", "Fungi \u00b7 Tanja Dekker"),
            ("crop-nematode-sid-jensen.jpg", "Nematode \u00b7 Sid Jensen"),
            ("crop-ciliate-gerri-gassert.jpg", "Protozoa \u00b7 Gerri Gassert")]
    D = 320
    for i, (f, cr) in enumerate(mics):
        cx = W // 2 + (-1 if i % 2 == 0 else 1) * 215
        top = 270 + (i // 2) * 405
        d.put(2, "Micrograph: " + cr, eyepiece(f"{MIC}/{f}", D, 0.5, 0.5, 1.0), cx - D // 2, top,
              shadowed=False, anchor="tl")
        T(d, 2, f"Credit {i + 1}", cr, cx - 212, top + D + 8, 424, 60, SMALL, bold=False, color=BROWN, mn=SMALL)
    T(d, 2, "Line", "The soil food web feeds the plant,\nlike gut microbes feed us", 72, 1080, 936, 130, MED,
      bold=False, color=BROWN, lh=1.16)
    sfw(d, 2)
    # 4. from soil to plate
    page(d, 3)
    T(d, 3, "Headline", "From soil to plate", 72, 170, 936, 90, BIG, color=BROWN)
    # real photos in eyepiece circles (Linnea, 10 Nov: no hands or basket drawings). Living soil: mushroom in the
    # soil under grapes; healthy plant: Armonia greenhouse, Costa Rica Jul 2024; food: Costa Rica Oct 2025 kitchen
    steps = [("sq-living-soil.jpg", "Living\nsoil"), ("sq-healthy-plant.jpg", "Healthy\nplant"),
             ("sq-food.jpg", "Nutritious\nfood")]
    CW, DC = 320, 270
    x0 = (W - 3 * CW) // 2
    for i, (f, lab) in enumerate(steps):
        cx = x0 + i * CW + CW // 2
        d.put(3, f"Photo {i + 1}: " + lab.replace("\n", " "), eyepiece(f"{MIC}/{f}", DC, 0.5, 0.5, 1.0), cx - DC // 2,
              400, shadowed=False, anchor="tl")
        T(d, 3, f"Step {i + 1}", lab, cx - 150, 700, 300, 130, MED, bold=False, color=BROWN, lh=1.12)
        if i < 2:
            T(d, 3, f"Arrow {i + 1}", "\u2192", cx + CW // 2 - 45, 480, 90, 100, BIG, color=GREEN)
    T(d, 3, "Line", "Carla explains how soil biology\nshapes the nutrients in our food", 72, 930, 936, 130, MED,
      bold=False, color=BROWN, lh=1.16)
    sfw(d, 3)
    # 5. watch Carla live
    page(d, 4)
    d.put(4, "Photo: Carla Portugal", eyepiece(PORTRAIT, 460, 0.5, 0.4, 1.1), (W - 460) // 2, 190, shadowed=False,
          anchor="tl")
    T(d, 4, "Headline", "Watch Carla live", 72, 730, 936, 90, BIG, color=BROWN)
    T(d, 4, "Date", "Sunday 15 November, 7 to 7:45am Pacific", 72, 840, 936, 70, MED, bold=False, color=BROWN)
    T(d, 4, "Event", "Food as Medicine for All \u00b7 Livestream", 72, 910, 936, 70, MED, bold=False, color=BROWN)
    pill = Image.new("RGBA", (340 * 4, 96 * 4), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, 340 * 4 - 1, 96 * 4 - 1), 192, fill=rgb(GREEN) + (255,))
    d.put(4, "Green pill", pill.resize((340, 96), Image.LANCZOS), (W - 340) // 2, 1040, shadowed=False, anchor="tl")
    T(d, 4, "Link in bio", "Link in bio", 72, 1054, 936, 70, MED, color=CREAM)
    sfw(d, 4)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
