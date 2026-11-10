"""Suzanne Shea / Veterans Day, Linnea's final text (10 Nov screenshots), text unchanged. Soft look: full-bleed
photos with a frosted, green-tinted fade where the text sits (bottom on slide 1, top on slide 2); slide 3 photo only.

  python3 tools/wormhole-visuals/suzanne_final.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

from bundle_three_styles_v12 import T, height
from collage import Deck, cover
from nov_fill import DECKS, TILES
from suzanne_frost import grade

W, H = 1080, 1350
CREAM = "#F4F1EA"
V = "/home/user/sfwlib/social/veterans"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"


def frost(path, fx, fy, a0, a1, top=False):
    sharp = grade(cover(ImageOps.exif_transpose(Image.open(path)).convert("RGB"), W, H, fx, fy))
    blur = np.asarray(sharp.filter(ImageFilter.GaussianBlur(30))).astype(np.float32)
    deep = np.array([20, 50, 30], np.float32)
    frost_ = blur * 0.38 + deep * 0.62
    y = np.linspace(0, 1, H, dtype=np.float32)
    if top:
        y = 1 - y
    t = np.clip((y - a0) / (a1 - a0), 0, 1)
    t = (t * t * (3 - 2 * t))[:, None, None]
    out = np.asarray(sharp).astype(np.float32) * (1 - t) + frost_ * t
    return Image.fromarray(out.clip(0, 255).astype("uint8")).convert("RGBA")


def logo(d, k, x, y, w=120):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def build(v):
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    # 1
    d.bg(0, frost(f"{V}/suzanne-fvc-conference.jpg", 0.45, 0.62, 0.55, 0.8), name="Photo with soft frosted fade")
    head = "We salute our veteran farmers and soil food web practicioners!"
    det = "Consultant Suzanne Shea presented at the Farmer Veteran Coalition Stakeholders Conference"
    hh = height(head, 66, 920, lh=1.06)
    dh = height(det, 48, 780, bold=False, lh=1.2)
    y = H - 70 - round(dh) - 22 - round(hh)
    y = T(d, 0, "Headline", head, 80, y, 920, hh + 8, 66, color=CREAM, align="left", lh=1.06)
    T(d, 0, "Details", det, 80, round(y) + 22, 780, dh + 8, 48, bold=False, color=CREAM, align="left", lh=1.2)
    logo(d, 0, W - 70 - 120, H - 60 - 120)
    # 2
    d.bg(1, frost(f"{V}/suzanne-hoop-house.jpg", 0.55, 0.7, 0.55, 0.8, top=True), name="Photo with soft frosted fade")
    t2 = "Her presentation taught veteran farmers about scalable sustainability through the Soil Food Web Approach."
    T(d, 1, "Text", t2, 80, 90, 900, 330, 56, bold=False, color=CREAM, align="left", lh=1.22)
    logo(d, 1, W - 70 - 120, H - 60 - 120)
    # 3 photo only
    d.bg(2, grade(cover(ImageOps.exif_transpose(Image.open(f"{V}/suzanne-conference-walk.jpg")).convert("RGB"), W, H,
                        0.3, 0.5)).convert("RGBA"), name="Photo")
    logo(d, 2, W - 70 - 120, H - 60 - 120)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
