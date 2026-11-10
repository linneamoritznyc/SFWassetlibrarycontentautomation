"""Suzanne Shea, Farmer Veteran Coalition (Linnea, 10 Nov: soft visual effects, a fade, a cool background, better text
placement). The photo melts into a blurred, green-graded copy of itself; text sits on the deep soft-green lower third.

  python3 tools/wormhole-visuals/suzanne_soft.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

from bundle_three_styles_v12 import T
from collage import Deck, cover
from nov_fill import DECKS, TILES

W, H = 1080, 1350
CREAM, MINT = "#F4F1EA", "#A8D5B0"
PHOTO = "/home/user/sfwlib/social/veterans/suzanne-fvc-conference.jpg"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"


def build(v):
    ph = ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB")
    # background: the same photo, heavily blurred and graded toward deep green, darker toward the bottom
    bg = cover(ph, W, H, 0.5, 0.4).filter(ImageFilter.GaussianBlur(40))
    a = np.asarray(bg).astype(np.float32)
    deep = np.array([22, 56, 30], np.float32)
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    mix = 0.55 + 0.35 * y
    a = a * (1 - mix) + deep * mix
    bg = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    # foreground photo, full width, fading out softly at the bottom into the background
    fh = 900
    fg = cover(ph, W, fh, 0.45, 0.42).convert("RGBA")
    m = np.ones((fh, W), np.float32)
    ramp = np.linspace(0, 1, fh, dtype=np.float32)
    fade = np.clip((ramp - 0.62) / 0.38, 0, 1) ** 1.3
    m = (1 - fade)[:, None] * m
    fg.putalpha(Image.fromarray((m * 255).astype("uint8")))
    bg.alpha_composite(fg, (0, 0))
    d = Deck("vet20261111", 1, f"veterans-day-{v}", "2026-11-11")
    d.bg(0, bg, name="Background: photo melting into soft green")
    T(d, 0, "Eyebrow", "Farmer Veteran Coalition", 80, 880, 920, 66, 52, bold=False, color=MINT, align="left")
    y2 = T(d, 0, "Headline", "Veteran farmers\nbuilding living soil", 80, 950, 920, 190, 86, color=CREAM, align="left",
           lh=1.02)
    T(d, 0, "Details", "Consultant Suzanne Shea presented\nat the Stakeholders Conference", 80, round(y2) + 24, 900, 140,
      50, bold=False, color=CREAM, align="left", lh=1.2)
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((130, round(lg.height * 130 / lg.width)), Image.LANCZOS)
    d.put(0, "SFW logo", lg, W - 70 - 130, H - 60 - lg.height, shadowed=False, anchor="tl")
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
