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
PORTRAIT = "/home/user/sfwlib/social/carla-portugal-fam-flyer.jpg"


def build(v):
    collage.H = SH
    try:
        d = Deck("st20261114carla", 1, f"carla-food-as-medicine-story-{v}", "2026-11-14")
        d.bg(0, grain(Image.new("RGB", (W, SH), CREAM), 661, 4), name="Background: Organic Cream")
        rect(d, 0, "Page frame", 44, 44, W - 88, SH - 88, (0, 0, 0, 0), outline=rgb(BROWN) + (255,), width=2)
        D = 520
        d.put(0, "Photo: Carla Portugal", eyepiece(PORTRAIT, D, 0.5, 0.42, 1.25), (W - D) // 2, 290, shadowed=False,
              anchor="tl")
        T(d, 0, "Eyebrow", "Tomorrow", 72, 870, 936, 70, 54, bold=False, color=GREEN)
        T(d, 0, "Headline", "Watch Carla live", 72, 950, 936, 100, 86, color=BROWN)
        T(d, 0, "Date", "Sunday 15 November\n7 to 7:45am Pacific", 72, 1080, 936, 140, 54, bold=False, color=BROWN,
          lh=1.18)
        T(d, 0, "Event", "Food as Medicine for All · Livestream", 72, 1240, 936, 70, 54, bold=False, color=BROWN)
        # space for Instagram's link sticker, placed in the app
        rect(d, 0, "Link sticker space", (W - 560) // 2, 1380, 560, 110, (0, 0, 0, 0), r=55,
             outline=rgb(GREEN) + (255,), width=3)
        T(d, 0, "Link sticker label", "LINK STICKER HERE", 72, 1400, 936, 70, 42, bold=False, color=GREEN, mn=42)
        logo(d, 0, white=False, w=150, x=(W - 150) // 2, y=SH - 300 - 20)
        return d.save(TILES, DECKS)[0]
    finally:
        collage.H = 1350


if __name__ == "__main__":
    print(build(sys.argv[1]))
