"""Cyber Monday (30 Nov), in the look of the 4 Nov Fall Enrollment bundle post: the green fade, the round course
badges, Montserrat Bold and Source Sans 3. Online sale, so no workshop photos. Linnea, 10 Nov.

  python3 tools/wormhole-visuals/cyber_nov30.py <version>
"""
import random
import sys

from PIL import Image

from bundle_three_styles import rgb
from bundle_three_styles_v12 import T
from bundle_v6 import H, W, fade
from collage import Deck
from nov_fill import DECKS, TILES

Deck.put_orig = Deck.put
Deck.put = lambda self, k, name, im, cx, cy, **kw: Deck.put_orig(self, k, name, im, round(cx), round(cy), **kw)

CREAM, MINT = "#F4F1EA", "#A8D5B0"
WHITE_LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
LEAVES = "/home/user/sfwlib/social/fall-cutouts"


def leaf_texture(seed):
    """Tone-on-tone leaf pattern: the fall leaf cut-outs as faint lighter-green silhouettes on the fade."""
    bg = fade("#1E7A3A", "#0E3B1E", (0.5, 0.38), seed)
    rnd = random.Random(seed)
    tex = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    leaves = [Image.open(f"{LEAVES}/leaves-0{n}.png").convert("RGBA") for n in range(10)]
    for gy in range(-1, 9):
        for gx in range(-1, 7):
            lf = rnd.choice(leaves)
            s = rnd.uniform(0.38, 0.55)
            lf = lf.resize((round(lf.width * s), round(lf.height * s)), Image.LANCZOS).rotate(rnd.uniform(0, 360), expand=True)
            sil = Image.new("RGBA", lf.size, (255, 255, 255, 0))
            sil.putalpha(lf.getchannel("A").point(lambda a: 20 if a > 100 else 0))
            x = gx * 175 + (gy % 2) * 88 + rnd.randint(-20, 20)
            y = gy * 165 + rnd.randint(-20, 20)
            tex.alpha_composite(sil, (max(0, x), max(0, y)) if x >= 0 and y >= 0 else (0, 0)) if x >= 0 and y >= 0 else None
    bg.alpha_composite(tex)
    return bg


def logo(d, k, w=150):
    lg = Image.open(WHITE_LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 70 - w, H - 60 - lg.height, shadowed=False, anchor="tl")


def build(v):
    d = Deck("nmw10rs3la2i", 1, f"cyber-monday-{v}", "2026-11-30")
    d.bg(0, leaf_texture(731), name="Background: green fade with leaf texture")
    # two fonts (Montserrat Bold, Source Sans 3), three sizes (54 / 300 / 54), cream text, mint accent
    T(d, 0, "Eyebrow", "Cyber Monday · Online courses", 72, 300, 936, 70, 54, bold=False, color=MINT)
    T(d, 0, "Discount", "[X]%\nOFF", 72, 400, 936, 600, 300, color=CREAM, lh=0.95, mn=200)
    T(d, 0, "Details", "Nov 30 to Dec 4 · Link in bio", 72, 1030, 936, 70, 54, bold=False, color=CREAM)
    logo(d, 0)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS))
