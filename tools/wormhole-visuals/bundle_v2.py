"""Fall Enrollment Special bundle carousel, rebuilt (Linnea, 4 Nov: her deck looked awful).

Brief (bundle doc, 3 Nov): one idea per slide; lead with "learn what your soil needs, then build it yourself"; sell the
cohort choice (January, May or August); no in-person workshop photos for an online course, real compost without people;
no prices; until 2 December. Course badges from Linnea's deck. Logo straight on the background, no box.

  python3 tools/wormhole-visuals/bundle_v2.py
"""
import os

from PIL import Image, ImageOps

from collage import Deck, cover, paper
from nov_fill import BROWN, COLOR, CREAM, DECKS, GREEN, INK, TILES, WHITE, box

W, H = 1080, 1350
SCR = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad"
BADGES = [f"{SCR}/bundleup/img_0_FC{i}_badge.jpg" for i in (1, 2, 3, 4)]
CIC = f"{SCR}/bundleup/img_0_CIC_badge.jpg"
PILE_GREEN = f"{SCR}/india/raw/2eea3831-7941-4be8-89de-973e3d5d27dd.JPG"
PILE_DARK = f"{SCR}/india/raw/69cdb9ab-191e-4673-abc8-5ae812029c8e.JPG"


def pile(path):
    """The compost pile only: the lower part of the photo, without the people's feet at the top."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return im.crop((0, im.height * 45 // 100, im.width, im.height))


def logo(d, k, path, x, y, w=200):
    lg = Image.open(path).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def build():
    d = Deck("promo-fall-bundle", 5, "fall-enrollment-bundle-v2", "2026-11-04")
    # 1. cover: compost on top, green panel with the promise
    d.bg(0, paper(GREEN, 1, w=W, h=H, grain=6), name="Panel")
    d.put(0, "Photo: compost pile", cover(pile(PILE_GREEN), W, 760, 0.5, 0.5).convert("RGBA"), 0, 0, shadowed=False,
          anchor="tl")
    y = d.text(0, "Headline", "Foundation Courses + Compost Intensive", 72, 810, 936, 200, 86, kind="montserrat-bold", italic=False,
               color=CREAM, lh=1.05, min_size=84)
    d.text(0, "Details", "Fall Enrollment Special, until 2 December.", 72, round(y) + 20,
           700, 220, 52, kind="source-reg", italic=False, color=CREAM, lh=1.2, min_size=50)
    logo(d, 0, WHITE, W - 72 - 200, H - 72 - 175)
    # 2. the four courses
    d.bg(1, paper(CREAM, 2, w=W, h=H, grain=5), name="Background")
    d.text(1, "Headline", "4 Foundation Courses", 72, 90, 936, 200, 84, kind="montserrat-bold", italic=False,
           color=BROWN, lh=1.05, min_size=84)
    bw, bh = 300, 460
    for i, b in enumerate(BADGES):
        im = Image.open(b).convert("RGB").resize((bw, bh), Image.LANCZOS).convert("RGBA")
        x = 72 + (i % 2) * (bw + 40) if False else [90, 400, 710][i] if i < 3 else 0
        d.put(1, f"Badge FC{i + 1}", im, 0, 0, shadowed=False, anchor="tl")
        d.items[-1]["x"] = 1 * W + 72 + i * 236  # four in a row, overlapping slightly like cards
        d.items[-1]["y"] = 330 + (i % 2) * 40
        d.items[-1]["im"] = im.resize((216, 331), Image.LANCZOS)
    d.text(1, "Details", "Introduction to the Soil Food Web, BioComplete™ Compost, BioComplete™ Liquid Amendments "
           "and Microscopy. Self-paced, online.", 72, 760, 860, 300, 52, kind="source-reg", italic=False, color=INK, lh=1.22,
           min_size=50)
    logo(d, 1, COLOR, W - 72 - 200, H - 72 - 175)
    # 3. build it
    d.bg(2, paper(BROWN, 3, w=W, h=H, grain=6), name="Panel")
    d.put(2, "Photo: finished compost", cover(pile(PILE_DARK), W, 760, 0.5, 0.5).convert("RGBA"), 0, 0,
          shadowed=False, anchor="tl")
    y = d.text(2, "Headline", "Compost Intensive Course", 72, 810, 936, 200, 84, kind="montserrat-bold", italic=False,
               color=CREAM, lh=1.05, min_size=84)
    d.text(2, "Details", "10 weeks online. Build 2 compost piles at home, with a weekly live call.", 72,
           round(y) + 20, 700, 220, 52, kind="source-reg", italic=False, color=CREAM, lh=1.2, min_size=50)
    logo(d, 2, WHITE, W - 72 - 200, H - 72 - 175)
    # 4. pick your season
    d.bg(3, paper(GREEN, 4, w=W, h=H, grain=6), name="Background")
    d.text(3, "Headline", "Choose your cohort", 72, 90, 936, 110, 84, kind="montserrat-bold", italic=False,
           color=CREAM, lh=1.05, min_size=84)
    d.text(3, "Details", "Compost Intensive cohorts in 2027:", 72, 210, 900, 140, 52,
           kind="source-reg", italic=False, color=CREAM, lh=1.2, min_size=50)
    for i, m in enumerate(("January", "May", "August")):
        box(d, 3, f"{m} box", CREAM, 72, 400 + i * 240, 936, 200)
        d.text(3, m, m, 120, 432 + i * 240, 840, 140, 110, kind="montserrat-bold", italic=False, color=BROWN, lh=1.0,
               min_size=100)
    logo(d, 3, WHITE, W - 72 - 200, H - 72 - 175)
    # 5. until 2 December
    d.bg(4, paper(CREAM, 5, w=W, h=H, grain=5), name="Background")
    d.text(4, "Eyebrow", "FALL ENROLLMENT SPECIAL", 72, 140, 900, 70, 52, kind="pathway", italic=False, color=GREEN,
           lh=1.0, track=2, min_size=50)
    d.text(4, "Date", "Until 2 December", 72, 230, 936, 300, 130, kind="montserrat-bold", italic=False, color=BROWN,
           lh=1.0, min_size=120)
    cic = Image.open(CIC).convert("RGBA")
    cic = cic.resize((380, round(cic.height * 380 / cic.width)), Image.LANCZOS)
    d.put(4, "CIC badge", cic, 72, 600, shadowed=False, anchor="tl")
    d.text(4, "Details", "Foundation Courses + Compost Intensive bundle. Link in bio.", 500, 640, 508, 330, 52,
           kind="source-reg", italic=False, color=INK, lh=1.22, min_size=50)
    logo(d, 4, COLOR, W - 72 - 200, H - 72 - 175)
    return d


if __name__ == "__main__":
    d = build()
    for k in range(1, 6):
        assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-v2-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
