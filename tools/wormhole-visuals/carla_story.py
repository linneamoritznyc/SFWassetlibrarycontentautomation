"""Carla's talk, Instagram Story for Sat 14 Nov, the day before (1080 x 1920). Same cream page, frame, eyepiece photo
and type as the Carla carousel. Text kept out of the top 250 and bottom 300 px; a marked space for the link sticker.

  python3 tools/wormhole-visuals/carla_story.py <version>
"""
import sys

from PIL import Image

import collage
from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import T
from collage import Deck
from nov_fill import DECKS, TILES
from nov_updates_nov10 import BROWN, CREAM, GREEN, eyepiece, logo, rect

W, SH = 1080, 1920
PORTRAIT = "/home/user/sfwlib/social/carla-fam/carla-sfw-team.jpg"   # soilfoodweb.com team page


def build(v):
    collage.H = SH
    try:
        d = Deck("st20261114carla", 1, f"carla-food-as-medicine-story-{v}", "2026-11-14")
        d.bg(0, grain(Image.new("RGB", (W, SH), CREAM), 661, 4), name="Background: Organic Cream")
        rect(d, 0, "Page frame", 44, 44, W - 88, SH - 88, (0, 0, 0, 0), outline=rgb(BROWN) + (255,), width=2)
        # just her photo and the talk (Linnea, 10 Nov: no microbes, more text). Sizes 54 / 70 / 50.
        D = 400
        d.put(0, "Photo: Carla Portugal", eyepiece(PORTRAIT, D, 0.5, 0.4, 1.1), (W - D) // 2, 230, shadowed=False,
              anchor="tl")
        T(d, 0, "Eyebrow", "Tomorrow, live \u00b7 Carla Portugal", 72, 670, 936, 70, 54, bold=False, color=GREEN)
        y = T(d, 0, "Headline", "Restoring the soil food web to grow nutrition your patients need", 100, 745, 880,
              330, 70, color=BROWN, lh=1.08)
        # from her session card
        y = T(d, 0, "Talk", "How soil microbes shape our food\nWhat the evidence does and doesn\u2019t "
              "support\nA sourcing checklist for food pantries\nand community farms", 72, round(y) + 36, 936, 420, 50,
              bold=False, color=BROWN, lh=1.3)
        rect(d, 0, "Rule", (W - 120) // 2, round(y) + 30, 120, 2, rgb(BROWN) + (255,))
        T(d, 0, "Date", "Sunday 15 November, 7 to 7:45am Pacific\nFood as Medicine for All \u00b7 Livestream", 72,
          round(y) + 60, 936, 140, 54, bold=False, color=BROWN, lh=1.2)
        logo(d, 0, white=False, w=120, x=(W - 120) // 2, y=SH - 60 - 140)   # low, leaving room for the link sticker
        return d.save(TILES, DECKS)[0]
    finally:
        collage.H = 1350


if __name__ == "__main__":
    print(build(sys.argv[1]))
