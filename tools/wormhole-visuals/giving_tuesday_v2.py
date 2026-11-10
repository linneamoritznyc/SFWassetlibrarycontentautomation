"""GivingTuesday carousel, started over (Linnea, 10 Nov: "add the thermometer to the slides", "start over").
Every slide on the Cyber Monday green leaf texture (her 10/10). Cover and close carry the SFW compost thermometer
(code-drawn, needle is its own object: rotate it in Canva to the current total). Story slides: one real photo,
framed straight, text on the green (no boxes). No AI images, no "Link in bio" on slides.

  python3 tools/wormhole-visuals/giving_tuesday_v2.py <version>
"""
import sys

from PIL import Image, ImageDraw, ImageOps

from bundle_three_styles import rgb
from bundle_three_styles_v12 import T, height
from bundle_v6 import H, W
from collage import Deck, cover
from cyber_nov30 import CREAM, MINT, leaf_texture, logo
from giving_thermometer import dial, needle
from nov_fill import DECKS, TILES

Deck.put_orig = getattr(Deck, "put_orig", Deck.put)
GOLD, BROWN, SAND = "#C9A227", "#4F3433", "#D8C3A5"
IND = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/india/raw"
NEW = "/home/user/photos/new-2026-10"
G = "/home/user/sfwlib/social/giving"


def ph(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def framed(path, w, h, fx, fy, r=28):
    im = cover(ph(path), w, h, fx, fy).convert("RGBA")
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), r * 2, fill=255)
    im.putalpha(m.resize((w, h), Image.LANCZOS))
    return im


def button(d, k, text, y, w=520):
    p = Image.new("RGBA", (w * 4, 104 * 4), (0, 0, 0, 0))
    ImageDraw.Draw(p).rounded_rectangle((0, 0, w * 4 - 1, 104 * 4 - 1), 208, fill=rgb(GOLD) + (255,))
    d.put(k, "Donate button (gold)", p.resize((w, 104), Image.LANCZOS), (W - w) // 2, y, shadowed=False, anchor="tl")
    T(d, k, "Button text", text, 72, y + 16, 936, 70, 54, color=BROWN)


def thermometer(d, k, D, y, frac):
    x = (W - D) // 2
    sw, sh = 30, 110
    st = Image.new("RGBA", (sw * 4, sh * 4), (0, 0, 0, 0))
    ImageDraw.Draw(st).polygon([(0, 0), (sw * 4, 0), (sw * 4, (sh - 30) * 4), (sw * 2, sh * 4), (0, (sh - 30) * 4)],
                               fill=rgb(SAND) + (255,))
    d.put(k, "Thermometer stem", st.resize((sw, sh), Image.LANCZOS), (W - sw) // 2, y + D - 16, shadowed=False,
          anchor="tl")
    d.put(k, "Thermometer dial", dial(D), x, y, shadowed=False, anchor="tl")
    d.put(k, "Needle (rotate around its centre to the current total)", needle(D, frac), x, y, shadowed=False,
          anchor="tl")


def story(d, k, path, fx, fy, head, line=None):
    d.bg(k, leaf_texture(780 + k), name="Background: green leaf texture")
    d.put(k, "Photo", framed(path, 940, 720, fx, fy), 70, 80, shadowed=True, anchor="tl")
    hh = height(head, 70, 900, lh=1.08)
    lh = height(line, 52, 900, bold=False, lh=1.2) if line else 0
    top = 800 + (H - 800 - 90 - round(hh) - (round(lh) + 20 if line else 0)) // 2
    y = T(d, k, "Headline", head, 90, top, 900, hh + 8, 70, color=CREAM, align="left", lh=1.08)
    if line:
        T(d, k, "Details", line, 90, round(y) + 20, 900, lh + 8, 52, bold=False, color=MINT, align="left", lh=1.2)
    logo(d, k)


def build(v):
    d = Deck("x20261201", 6, f"giving-tuesday-{v}", "2026-12-01")
    # 1. cover: the thermometer is the hook
    d.bg(0, leaf_texture(779), name="Background: green leaf texture")
    T(d, 0, "Eyebrow", "GivingTuesday · December 1", 72, 80, 936, 66, 52, bold=False, color=MINT)
    T(d, 0, "Headline", "Help us raise $100,000\nto bring soil back to life", 72, 150, 936, 190, 70, color=CREAM, lh=1.06)
    thermometer(d, 0, 620, 370, 0.0)
    button(d, 0, "Give today", 1150, 440)
    logo(d, 0)
    # 2 to 5. the story, one real photo each
    story(d, 1, "/home/user/SFW-SocialMedia/assets/photo/web/fist-of-dry-soil.jpg", 0.5, 0.45,
          "The soil under our feet is alive", "For decades we’ve farmed it\nlike it was dead.")
    story(d, 2, f"{NEW}/card-elaine-ingham-microscope.jpg", 0.5, 0.32,
          "Healthy food comes from healthy soil", "Dr. Elaine Ingham spent\ndecades proving it.")
    story(d, 3, f"{G}/class-live-microscopy-cr-oct2025.jpg", 0.55, 0.45,
          "We teach farmers to restore the living web in their soil")
    story(d, 4, f"{NEW}/students-laughing-at-compost-cage.jpg", 0.6, 0.38,
          "One trained farmer changes a whole farm", "Then the neighbours see\nthe results and ask how.")
    # 6. close: the team line, what gifts fund, the thermometer again and the ask
    d.bg(5, leaf_texture(785), name="Background: green leaf texture")
    T(d, 5, "Headline", "Be the mycelium you want\nto see in the world", 72, 80, 936, 170, 70, color=CREAM, lh=1.06)
    T(d, 5, "Details", "Your gift funds scholarships, educational\nresources and research", 72, 270, 936, 140, 52,
      bold=False, color=MINT, lh=1.2)
    thermometer(d, 5, 560, 450, 0.0)
    button(d, 5, "Donate today", 1150, 480)
    logo(d, 5)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
