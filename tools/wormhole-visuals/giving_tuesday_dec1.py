"""Giving Tuesday (Dec 1) donation post, 3 slides. Slide lines come straight from Linnea's caption; slide 3 is her
slide text. India workshop photos, soft dark fades where the text sits, gold only on the Donate button.

  python3 tools/wormhole-visuals/giving_tuesday_dec1.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageOps

from bundle_three_styles_v12 import T, height
from collage import Deck, cover
from nov_fill import DECKS, TILES
from suzanne_frost import grade

W, H = 1080, 1350
CREAM = "#F4F1EA"
MINT = "#A9D3B2"
GOLD = (201, 162, 39)
DEEP = (10, 40, 20)
IND = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/india/raw"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
AERIAL = f"{IND}/0094eea0-fa85-4200-91fe-dba96bce14ec.jpg"     # farm plots from above, Tamil Nadu
FIELD = f"{IND}/1311e3fb-ba0c-4512-97eb-40de356c4da0.jpg"      # thriving field
GROUP = f"{IND}/99696ef1-0bb4-4626-b0c8-cf77fd2e04c7.JPG"      # workshop group, waving


def photo(path, fx=0.5, fy=0.5):
    return grade(cover(ImageOps.exif_transpose(Image.open(path)).convert("RGB"), W, H, fx, fy))


def fade(im, y0, y1, strength=0.88, top=False, colour=DEEP):
    """Dark green fade from y0 (clear) to y1 (strength), smoothstep."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    y = np.arange(H, dtype=np.float32)
    t = np.clip((y - y0) / (y1 - y0), 0, 1) if not top else np.clip((y1 - y) / (y1 - y0), 0, 1)
    t = (t * t * (3 - 2 * t) * strength)[:, None, None]
    a = a * (1 - t) + np.array(colour, np.float32) * t
    return Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")


def logo(d, k, x, y, w=150):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def button(d, k, x, y, label="Donate today"):
    from PIL import ImageFont
    f = ImageFont.truetype("/home/user/fonts/Montserrat-Bold.ttf", 54)
    tw = f.getlength(label)
    bw, bh = round(tw + 120), 116
    im = Image.new("RGBA", (bw * 2, bh * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, bw * 2 - 1, bh * 2 - 1), bh, fill=GOLD + (255,))
    im = im.resize((bw, bh), Image.LANCZOS)
    d.put(k, "Donate button", im, x, y, shadowed=True, anchor="tl", off=(0, 8), blur=14, alpha=0.35)
    T(d, k, "Donate button text", label, x, y + (bh - 66) // 2, bw, 70, 54, color="#173A1F", align="center", lh=1.1)
    return bh


def build(v):
    d = Deck("gt20261201", 3, f"giving-tuesday-dec1-{v}", "2026-12-01")
    # 1. the hook, over farmland seen from above
    bg = fade(photo(AERIAL, 0.55, 0.5), H * 0.38, H * 0.78, 0.9)
    d.bg(0, bg, name="Farmland from above with dark fade")
    head = "There is a farmer somewhere right now watching their soil fail."
    hh = height(head, 84, 920, lh=1.08)
    T(d, 0, "Headline", head, 80, H - 120 - round(hh), 920, hh + 8, 84, color=CREAM, align="left", lh=1.08)
    # 2. recovery, the match and the ask
    bg = fade(photo(FIELD, 0.5, 0.6), H * 0.30, H * 0.70, 0.92)
    d.bg(1, bg, name="Thriving field with dark fade")
    head = "The soil can recover.\nIt wants to."
    small = "A generous donor is matching every gift through the end of the year, so your donation goes twice as far."
    hh = height(head, 86, 920, lh=1.06)
    sh = height(small, 52, 900, bold=False, lh=1.2)
    y = H - 110 - 116 - 60 - round(sh) - 40 - round(hh)
    y = T(d, 1, "Headline", head, 80, y, 920, hh + 8, 86, color=CREAM, align="left", lh=1.06)
    y = T(d, 1, "Small text", small, 80, round(y) + 40, 900, sh + 8, 52, bold=False, color=CREAM, align="left", lh=1.2)
    button(d, 1, 80, round(y) + 60)
    # 3. India workshop
    ph = 880
    g = grade(cover(ImageOps.exif_transpose(Image.open(GROUP)).convert("RGB"), W, ph, 0.5, 0.62))
    bg = Image.new("RGB", (W, H), DEEP)
    bg.paste(g, (0, 0))
    bg = fade(bg, ph - 230, ph, 1.0)
    d.bg(2, bg, name="India workshop group with dark fade")
    txt = ("We partnered with the Isha Foundation to host our first in-person Accelerator Workshop in India! "
           "This group featured 46 students from 10 countries")
    th = height(txt, 54, 920, bold=False, lh=1.2)
    T(d, 2, "Text", txt, 80, 900 + (H - 900 - 170 - round(th)) // 2, 920, th + 8, 54, bold=False, color=CREAM, align="left", lh=1.2)
    logo(d, 2, W - 60 - 150, H - 40 - 150)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
