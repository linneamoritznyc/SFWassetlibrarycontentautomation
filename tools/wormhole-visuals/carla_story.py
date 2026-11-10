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
        # portrait with two micrographs from the carousel overlapping it (bacteria and a nematode)
        D, d2 = 500, 210
        px, py = (W - D) // 2, 290
        d.put(0, "Photo: Carla Portugal", eyepiece(PORTRAIT, D, 0.5, 0.4, 1.1), px, py, shadowed=False, anchor="tl")
        MIC = "/home/user/sfwlib/social/carla-fam"
        d.put(0, "Micrograph: bacteria, John Ash", eyepiece(f"{MIC}/crop-bacteria-john-ash.jpg", d2, 0.5, 0.5, 1.0),
              px - 90, py + D - d2 + 10, shadowed=False, anchor="tl")
        d.put(0, "Micrograph: nematode, Sid Jensen", eyepiece(f"{MIC}/crop-nematode-sid-jensen.jpg", d2, 0.5, 0.5, 1.0),
              px + D - d2 + 90, py + D - d2 + 10, shadowed=False, anchor="tl")
        # three sizes: 54 / 72 / 54 and Montserrat Bold + Source Sans 3
        T(d, 0, "Eyebrow", "Tomorrow, live \u00b7 Carla Portugal", 72, 860, 936, 70, 54, bold=False, color=GREEN)
        y = T(d, 0, "Headline", "Restoring the soil food web to grow nutrition your patients need", 100, 950, 880,
              330, 72, color=BROWN, lh=1.08)
        T(d, 0, "Date", "Sunday 15 November, 7 to 7:45am Pacific\nFood as Medicine for All \u00b7 Livestream", 72,
          round(y) + 40, 936, 140, 54, bold=False, color=BROWN, lh=1.2)
        logo(d, 0, white=False, w=150, x=(W - 150) // 2, y=SH - 300 - 150)
        return d.save(TILES, DECKS)[0]
    finally:
        collage.H = 1350


if __name__ == "__main__":
    print(build(sys.argv[1]))
