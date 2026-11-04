"""Bundle carousel v5: same words as v4 (Linnea's, word for word), more designed: the cover shows the four Foundation
Course badges + the Compost Intensive badge on the badge blue, like the sales page hero; slide 2 puts the badges on a
clean blue band; slide 3 overlaps the CIC badge on the compost photo.

  python3 tools/wormhole-visuals/bundle_v5.py
"""
import os

from PIL import Image, ImageDraw

from bundle_v2 import BADGES, CIC, PILE_DARK, logo, pile
from collage import Deck, cover, paper
from nov_fill import BROWN, COLOR, CREAM, DECKS, GREEN, INK, TILES, WHITE, box

W, H = 1080, 1350
BLUE = "#A7C6DA"


def fc_tile(i, w):
    im = Image.open(BADGES[i]).convert("RGB").crop((0, 18, 278, 330))
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).convert("RGBA")


def cic_disc(d_):
    im = Image.open(CIC).convert("RGBA")
    im = im.resize((round(d_ * 0.78), round(im.height * d_ * 0.78 / im.width)), Image.LANCZOS)
    disc = Image.new("RGBA", (d_, d_), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, d_ - 1, d_ - 1), fill=CREAM)
    disc.alpha_composite(im, ((d_ - im.width) // 2, (d_ - im.height) // 2))
    return disc


if __name__ == "__main__":
    d = Deck("promo-fall-bundle", 3, "fall-enrollment-bundle-v5", "2026-11-04")
    # 1. cover
    d.bg(0, paper(GREEN, 21, w=W, h=H, grain=6), name="Panel")
    box(d, 0, "Badge band", BLUE, 0, 0, W, 760)
    tw = 250
    for i in range(4):
        t = fc_tile(i, tw)
        d.put(0, f"Badge FC{i + 1}", t, 60 + (i % 2) * (tw + 20), 90 + (i // 2) * (t.height + 20), shadowed=False,
              anchor="tl")
    d.text(0, "Plus", "+", 610, 270, 90, 160, 150, kind="montserrat-bold", italic=False, color=BROWN, lh=1.0,
           min_size=140)
    d.put(0, "CIC badge", cic_disc(330), 700, 210, shadowed=False, anchor="tl")
    y = d.text(0, "Headline", "Foundation Courses + Compost Intensive", 72, 810, 936, 200, 84, kind="montserrat-bold",
               italic=False, color=CREAM, lh=1.05, min_size=84)
    d.text(0, "Details", "Fall Enrollment Special, until 2 December. Link in bio.", 72, round(y) + 24, 700, 200, 52,
           kind="source-reg", italic=False, color=CREAM, lh=1.2, min_size=50)
    logo(d, 0, WHITE, W - 72 - 200, H - 72 - 175)
    # 2. the Foundation Courses
    d.bg(1, paper(CREAM, 22, w=W, h=H, grain=5), name="Background")
    y = d.text(1, "Headline", "The Foundation Courses teach you to work out what your soil needs.", 72, 90, 936, 330,
               73, kind="montserrat-bold", italic=False, color=BROWN, lh=1.08, min_size=66)
    band_y = round(y) + 40
    box(d, 1, "Badge band", BLUE, 0, band_y, W, 300)
    for i in range(4):
        d.put(1, f"Badge FC{i + 1}", fc_tile(i, 236), 40 + i * 252, band_y + 20, shadowed=False, anchor="tl")
    d.text(1, "Details", "Introduction to the Soil Food Web, BioComplete™ Compost, BioComplete™ Liquid Amendments and "
           "Microscopy. Self-paced, start the day you enroll.", 72, band_y + 350, 760, 330, 52, kind="source-reg",
           italic=False, color=INK, lh=1.2, min_size=50)
    logo(d, 1, COLOR, W - 72 - 200, H - 72 - 175)
    # 3. the Compost Intensive Course
    d.bg(2, paper(BROWN, 23, w=W, h=H, grain=6), name="Panel")
    d.put(2, "Photo: compost", cover(pile(PILE_DARK), W, 620, 0.5, 0.5).convert("RGBA"), 0, 0, shadowed=False,
          anchor="tl")
    d.put(2, "CIC badge", cic_disc(250), W - 72 - 250, 620 - 150, shadowed=False, anchor="tl")
    y = d.text(2, "Headline", "The Compost Intensive Course teaches you to make it.", 72, 668, 700, 300, 73,
               kind="montserrat-bold", italic=False, color=CREAM, lh=1.08, min_size=66)
    d.text(2, "Details", "Ten weeks online, with a 90-minute live session with a mentor every week. You build two "
           "batches of compost where you live, and you keep them.", 72, round(y) + 24, 700, H - round(y) - 70, 52,
           kind="source-reg", italic=False, color=CREAM, lh=1.2, min_size=50)
    logo(d, 2, WHITE, W - 72 - 200, H - 72 - 175)
    for k in (1, 2, 3):
        assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-v5-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
