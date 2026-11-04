"""Bundle carousel v4: Linnea's own slide text, word for word (4 Nov), only sales-page wording. Three slides.

  python3 tools/wormhole-visuals/bundle_v3.py
"""
import os

from PIL import Image

from bundle_v2 import BADGES, PILE_DARK, PILE_GREEN, logo, pile
from collage import Deck, cover, paper
from nov_fill import BROWN, COLOR, CREAM, DECKS, GREEN, INK, TILES, WHITE

W, H = 1080, 1350
SPLIT = 620


def photo_slide(d, k, img, panel, head, det):
    d.bg(k, paper(panel, 10 + k, w=W, h=H, grain=6), name="Panel")
    d.put(k, "Photo: compost", cover(img, W, SPLIT, 0.5, 0.5).convert("RGBA"), 0, 0, shadowed=False, anchor="tl")
    y = d.text(k, "Headline", head, 72, SPLIT + 48, 936, 300, 73, kind="montserrat-bold", italic=False, color=CREAM,
               lh=1.08, min_size=66)
    d.text(k, "Details", det, 72, round(y) + 24, 700, H - round(y) - 70, 52, kind="source-reg", italic=False,
           color=CREAM, lh=1.2, min_size=50)
    logo(d, k, WHITE, W - 72 - 200, H - 72 - 175)


if __name__ == "__main__":
    d = Deck("promo-fall-bundle", 3, "fall-enrollment-bundle-v4", "2026-11-04")
    photo_slide(d, 0, pile(PILE_GREEN), GREEN, "Foundation Courses + Compost Intensive",
                "Fall Enrollment Special, until 2 December. Link in bio.")
    d.bg(1, paper(CREAM, 12, w=W, h=H, grain=5), name="Background")
    y = d.text(1, "Headline", "The Foundation Courses teach you to work out what your soil needs.", 72, 90, 936, 330,
               73, kind="montserrat-bold", italic=False, color=BROWN, lh=1.08, min_size=66)
    for i, b in enumerate(BADGES):
        im = Image.open(b).convert("RGB").resize((216, 331), Image.LANCZOS).convert("RGBA")
        d.put(1, f"Badge FC{i + 1}", im, 72 + i * 236, round(y) + 40 + (i % 2) * 30, shadowed=False, anchor="tl")
    d.text(1, "Details", "Introduction to the Soil Food Web, BioComplete™ Compost, BioComplete™ Liquid Amendments and "
           "Microscopy. Self-paced, start the day you enroll.", 72, round(y) + 450, 760, 330, 52, kind="source-reg",
           italic=False, color=INK, lh=1.2, min_size=50)
    logo(d, 1, COLOR, W - 72 - 200, H - 72 - 175)
    photo_slide(d, 2, pile(PILE_DARK), BROWN, "The Compost Intensive Course teaches you to make it.",
                "Ten weeks online, with a 90-minute live session with a mentor every week. You build two batches of "
                "compost where you live, and you keep them.")
    for k in (1, 2, 3):
        assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-v4-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
