"""Today's bundle post (4 Nov) in the line-art colour-fade look Linnea liked (bundle_v6), updated for Stephanie's
notes: centred text, dates kept on one line, a QR code with the platform short link on the last slide. Words from
Linnea's v6 text and the sales page; "and you keep them" dropped (Linnea, 4 Nov). One deck per platform.

  python3 tools/wormhole-visuals/bundle_v6_centered.py
"""
import os

from PIL import Image

from bundle_three_styles_v12 import FY, M, T, footer, height
from bundle_v6 import H, W, fade, line_art
from collage import Deck
from nov_fill import DECKS, TILES

SLIDES = [
    (("#1E7A3A", "#0E3B1E", (0.5, 0.26)), "online", 720, "Foundation Courses + Compost Intensive",
     "Fall Enrollment Special, until 2 December.", 84),
    (("#3780B8", "#123B26", (0.5, 0.26)), "leaves", 440, "The Foundation Courses teach you to work out what your soil "
     "needs.", "Introduction to the Soil Food Web, BioComplete™ Compost, BioComplete™ Liquid Amendments and "
     "Microscopy. Self-paced, start the day you enroll.", 73),
    (("#6B4A3A", "#1E3A22", (0.5, 0.26)), "compost", 520, "The Compost Intensive Course teaches you to make it.",
     "Ten weeks online, with a 90-minute live session with a mentor every week.\nYou build two compost piles right "
     "where you live.", 73),
    (("#1E7A3A", "#123B26", (0.5, 0.26)), "calendar", 400, "Choose your cohort",
     "January, May or August 2027.\nFall Enrollment Special, until 2 December.", 84),
]
ART_ZONE = (50, 450)   # the drawing sits centred in this vertical band on every slide


def build(plat, v, link):
    d = Deck("promo-fall-bundle", len(SLIDES), f"fall-enrollment-bundle-lineart-{plat}-{v}", "2026-11-04")
    last = len(SLIDES) - 1
    for k, ((top, bottom, glow), art, aw, head, det, hs) in enumerate(SLIDES):
        d.bg(k, fade(top, bottom, glow, seed=40 + k), name="Background fade")
        im = line_art(art, aw)
        zh = ART_ZONE[1] - ART_ZONE[0]
        if im.height > zh:
            im = line_art(art, round(aw * zh / im.height))
        d.put(k, "Line drawing", im, (W - im.width) // 2, ART_ZONE[0] + (zh - im.height) // 2, shadowed=False,
              anchor="tl")
        y = T(d, k, "Headline", head, M, 500, 936, 300, hs)
        T(d, k, "Details", det, M, round(y) + 24, 936, FY - round(y) - 50, 52, bold=False)
        if k == last:
            os.environ["QR_LINK"] = link
            import bundle_three_styles_v12 as v12
            v12.QR_LINK = link
            footer(d, k, "Link in bio.", "promo-fall-bundle")
        else:
            footer(d, k)
    return d


if __name__ == "__main__":
    for plat, v, link in (("instagram", "v12", "https://tr.ee/ce6tWIaOx7"),
                          ("facebook", "v13", "https://www.sfw.one/fccicfall2026fb"),
                          ("linkedin", "v14", "https://www.sfw.one/fccicfall2026li")):
        d = build(plat, v, link)
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-{v}-{k}.jpg"))
        print(d.save(TILES, DECKS)[0], d.pptx_name())
