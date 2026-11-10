"""Suzanne Shea, Farmer Veteran Coalition. v10: editorial look. Deep soft-green field with a gentle light bloom,
the photo in a tall arch (softly graded: banner colours calmed, warmth added), a fine cream line echoing the arch,
centred type below. Montserrat Bold + Source Sans 3.

  python3 tools/wormhole-visuals/suzanne_soft.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

from bundle_three_styles_v12 import T
from collage import Deck, cover
from nov_fill import DECKS, TILES

W, H = 1080, 1350
CREAM, MINT = "#F4F1EA", "#B9DCC0"
PHOTO = "/home/user/sfwlib/social/veterans/suzanne-fvc-conference.jpg"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"


def background():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    top, bot = np.array([30, 74, 44], np.float32), np.array([14, 38, 24], np.float32)
    t = (yy / H)[..., None]
    img = top * (1 - t) + bot * t
    r = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.3) / H) ** 2)
    img += (np.clip(1 - r / 0.55, 0, 1) ** 2 * 26)[..., None]          # soft light behind the arch
    img += np.random.default_rng(11).normal(0, 2.2, (H, W, 1)).astype(np.float32)   # fine paper grain
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8")).convert("RGBA")


def arch(img, w, h):
    k = 3
    m = Image.new("L", (w * k, h * k), 0)
    dr = ImageDraw.Draw(m)
    dr.rectangle((0, w * k // 2, w * k, h * k), fill=255)
    dr.ellipse((0, 0, w * k, w * k), fill=255)
    img = img.convert("RGBA")
    img.putalpha(m.resize((w, h), Image.LANCZOS))
    return img


def arch_line(w, h, pad, width=3):
    k = 3
    W2, H2 = (w + 2 * pad) * k, (h + 2 * pad) * k
    im = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    col = (244, 241, 234, 150)
    dr.arc((0, 0, W2 - 1, W2 - 1), 180, 360, fill=col, width=width * k)
    dr.line((width * k / 2, W2 / 2, width * k / 2, H2), fill=col, width=width * k)
    dr.line((W2 - width * k / 2 - 1, W2 / 2, W2 - width * k / 2 - 1, H2), fill=col, width=width * k)
    return im.resize((w + 2 * pad, h + 2 * pad), Image.LANCZOS)


def grade(im):
    im = ImageEnhance.Color(im).enhance(0.78)                         # calm the flag colours
    a = np.asarray(im).astype(np.float32)
    a = a * np.array([1.04, 1.0, 0.94]) + np.array([10, 8, 2])        # warm, lift the shadows
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


HOOP = "/home/user/sfwlib/social/veterans/suzanne-hoop-house.jpg"
WALK = "/home/user/sfwlib/social/veterans/suzanne-conference-walk.jpg"


def soft_fade(img, start, end):
    """Alpha that is solid above `start` and melts to nothing at `end` (fractions of the height), eased."""
    w, h = img.size
    t = np.clip((np.linspace(0, 1, h, dtype=np.float32) - start) / (end - start), 0, 1)
    t = t * t * (3 - 2 * t)
    img = img.convert("RGBA")
    img.putalpha(Image.fromarray(((1 - t)[:, None] * np.ones((h, w), np.float32) * 255).astype("uint8")))
    return img


def logo(d, k, w=96):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, (W - w) // 2, H - 34 - lg.height, shadowed=False, anchor="tl")


def build(v):
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    # 1. hoop house, full width, melting into the green; type centred below
    d.bg(0, background(), name="Background: soft green")
    hp = grade(cover(ImageOps.exif_transpose(Image.open(HOOP)).convert("RGB"), W, 1000, 0.5, 0.3))
    d.put(0, "Photo: Suzanne Shea planting by the hoop house", soft_fade(hp, 0.55, 1.0), 0, 0, shadowed=False,
          anchor="tl")
    T(d, 0, "Eyebrow", "S U Z A N N E   S H E A", 72, 905, 936, 56, 42, bold=False, color=MINT, mn=42)
    T(d, 0, "Headline", "Veteran farmers\nbuilding living soil", 72, 970, 936, 180, 80, color=CREAM, lh=1.04)
    T(d, 0, "Details", "Soil Food Web Consultant", 72, 1165, 936, 64, 46, bold=False, color=CREAM, mn=42)
    logo(d, 0)
    # 2. the conference photo in an arch with a fine cream line around it
    d.bg(1, background(), name="Background: soft green")
    aw, ah = 640, 760
    ph = grade(cover(ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB"), aw, ah, 0.43, 0.55))
    ax, ay = (W - aw) // 2, 96
    d.put(1, "Arch line", arch_line(aw, ah, 22), ax - 22, ay - 22, shadowed=False, anchor="tl")
    d.put(1, "Photo: Suzanne Shea at the Farmer Veteran Coalition conference", arch(ph, aw, ah), ax, ay,
          shadowed=False, anchor="tl")
    T(d, 1, "Eyebrow", "F A R M E R   V E T E R A N   C O A L I T I O N", 72, 925, 936, 56, 42, bold=False,
      color=MINT, mn=42)
    T(d, 1, "Headline", "Scaling Sustainably", 72, 990, 936, 96, 76, color=CREAM)
    T(d, 1, "Details", "Suzanne\u2019s talk at the\nStakeholders Conference", 72, 1095, 936, 130, 46, bold=False,
      color=CREAM, lh=1.2, mn=42)
    logo(d, 1)
    # 3. her selfie on the conference walk, a soft round-cornered window, very little text
    d.bg(2, background(), name="Background: soft green")
    ww, wh = 900, 980
    wp = grade(cover(ImageOps.exif_transpose(Image.open(WALK)).convert("RGB"), ww, wh, 0.15, 0.5)).convert("RGBA")
    m = Image.new("L", (ww * 3, wh * 3), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, ww * 3 - 1, wh * 3 - 1), 60 * 3, fill=255)
    wp.putalpha(m.resize((ww, wh), Image.LANCZOS))
    d.put(2, "Photo: Suzanne Shea on the conference walk", wp, (W - ww) // 2, 90, shadowed=False, anchor="tl")
    T(d, 2, "Headline", "Living soil, shared", 72, 1115, 936, 96, 76, color=CREAM)
    logo(d, 2)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
