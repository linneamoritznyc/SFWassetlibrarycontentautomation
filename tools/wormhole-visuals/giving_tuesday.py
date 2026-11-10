"""GivingTuesday carousel, Tue 1 Dec 2026 (Linnea, 10 Nov): sister to the Cyber Monday visual. Food Web Green leaf
texture, white (cream) line illustrations, Montserrat Bold + Source Sans 3, one reason per slide.
Facts from Linnea's brief: 40+ years (Foundation facts), India seminar and workshop numbers, the 100,000 acres goal
(bundle sales page). Confirm with Stephanie what the gifts fund before posting (slide 5).

  python3 tools/wormhole-visuals/giving_tuesday.py <version>
"""
import sys

from PIL import Image

from cyber_nov30 import CREAM, MINT, leaf_texture, lineart, logo
from bundle_three_styles_v12 import T, height
from bundle_v6 import H, W
from collage import Deck
from nov_fill import DECKS, TILES

SLIDES = [
    ("seedling-fungi", "Why give on Giving Tuesday?", None),
    ("microscope", "We carry Dr. Elaine Ingham’s science forward",
     "40+ years of soil food web research, taught by her team."),
    ("globe-sprouts", "We teach farmers around the world",
     "This year in India: 61 farmers at our Life in the Soil seminar, 46 participants from 10 countries at our workshop."),
    ("sunrise", "Our goal: 100,000 acres regenerated in 2027", None),
    ("hands", "Your gift helps a student learn to restore soil", "Link in bio"),
]


def build(v):
    d = Deck("x20261201", len(SLIDES), f"giving-tuesday-{v}", "2026-12-01")
    for k, (art, head, line) in enumerate(SLIDES):
        d.bg(k, leaf_texture(740 + k), name="Background: green fade with leaf texture")
        im = lineart(art, 420 if k else 480, thick=5 if art in ("microscope", "sunrise", "hands") else 3)
        if im.width > 760:
            im = im.resize((760, round(im.height * 760 / im.width)), Image.LANCZOS)
        hs = 86 if k == 0 else 70
        hh = height(head, hs, 900)
        lh = height(line, 54, 860, bold=False, lh=1.22) if line else 0
        total = im.height + 70 + hh + (34 + lh if line else 0)
        y = round((H - 150 - total) / 2) + 40
        d.put(k, f"Drawing: {art}", im, (W - im.width) // 2, y, shadowed=False, anchor="tl")
        y += im.height + 70
        T(d, k, "Headline", head, 90, y, 900, hh + 8, hs, color=CREAM)
        if line:
            T(d, k, "Details", line, 110, y + round(hh) + 34, 860, lh + 8, 54, bold=False,
              color=MINT if line == "Link in bio" else CREAM, lh=1.22)
        logo(d, k)
    return d


if __name__ == "__main__":
    from PIL import Image  # noqa: F401
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
