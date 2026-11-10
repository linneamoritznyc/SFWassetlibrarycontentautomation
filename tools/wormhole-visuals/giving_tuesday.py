"""GivingTuesday, Tue 1 Dec 2026. Family: Soil Brown with one big cream line drawing and the gold donate button (gold
only on donate CTAs, docs/brand.md). Neighbours are cream (Colleen, 28 Nov) and green (Cyber Monday, 30 Nov).
Copy from the Wormhole draft x20261201 (scholarships); confirm with Stephanie that gifts go to scholarships.

  python3 tools/wormhole-visuals/giving_tuesday.py <version>
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import T
from bundle_v6 import H, W
from collage import Deck
from nov_fill import DECKS, TILES

Deck.put_orig = Deck.put
Deck.put = lambda self, k, name, im, cx, cy, **kw: Deck.put_orig(self, k, name, im, round(cx), round(cy), **kw)

BROWN, CREAM, GOLD = "#4F3433", "#F4F1EA", "#C9A227"
WHITE_LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"


def lineart(name, h, color=CREAM, thick=3):
    la = Image.open(f"/home/user/sfwlib/social/lineart/{name}.png").convert("L")
    al = la.point(lambda v: max(0, min(255, int((v - 40) * 1.6)))).filter(ImageFilter.MaxFilter(thick))
    im = Image.new("RGBA", la.size, rgb(color) + (0,))
    im.putalpha(al)
    im = im.crop(al.getbbox())
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def build(v):
    d = Deck("x20261201", 1, f"giving-tuesday-{v}", "2026-12-01")
    d.bg(0, grain(Image.new("RGB", (W, H), BROWN), 801, 4), name="Background: Soil Brown")
    hands = lineart("hands", 470)
    d.put(0, "Drawing: hands holding living soil", hands, (W - hands.width) // 2, 130, shadowed=False, anchor="tl")
    # two fonts, three sizes (86 / 54 / 54), cream text, gold only on the donate button
    T(d, 0, "Headline", "Today is GivingTuesday", 72, 680, 936, 110, 86, color=CREAM)
    T(d, 0, "Details", "Your gift puts a farmer, gardener or student\ninto a Soil Food Web course", 72, 810, 936, 140,
      54, bold=False, color=CREAM, lh=1.2)
    pw = 520
    pill = Image.new("RGBA", (pw * 4, 110 * 4), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, pw * 4 - 1, 110 * 4 - 1), 220, fill=rgb(GOLD) + (255,))
    d.put(0, "Donate button (gold)", pill.resize((pw, 110), Image.LANCZOS), (W - pw) // 2, 1010, shadowed=False,
          anchor="tl")
    T(d, 0, "Donate", "Give today · Link in bio", 72, 1030, 936, 70, 54, color=BROWN)
    lg = Image.open(WHITE_LOGO).convert("RGBA")
    lg = lg.resize((140, round(lg.height * 140 / lg.width)), Image.LANCZOS)
    d.put(0, "SFW logo", lg, W - 70 - 140, H - 60 - lg.height, shadowed=False, anchor="tl")
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
