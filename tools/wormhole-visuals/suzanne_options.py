"""Three looks for the Suzanne slide, Linnea's exact text (her screenshot, 10 Nov):
  Headline: "Veteran farmers building living soil"
  Details:  "Consultant Suzanne Shea presented at the Farmer Veteran Coalition Stakeholders Conference"
A: full-bleed photo melting into a frosted deep green, centred type.
B: deep green field with a soft light bloom, photo in an arch with a fine cream line, centred type.
C: the photo blurred and green-tinted as the whole background, the sharp photo as a soft-edged card, centred type.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from bundle_three_styles_v12 import T
from collage import Deck, cover
from nov_fill import DECKS, TILES
from suzanne_frost import frosted, grade
from suzanne_soft import arch, arch_line, background

W, H = 1080, 1350
CREAM = "#F4F1EA"
PHOTO = "/home/user/sfwlib/social/veterans/suzanne-fvc-conference.jpg"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"
HEAD = "Veteran farmers\nbuilding living soil"
DET = "Consultant Suzanne Shea presented\nat the Farmer Veteran Coalition\nStakeholders Conference"


def words(d, k, y):
    y = T(d, k, "Headline", HEAD, 72, y, 936, 180, 80, color=CREAM, lh=1.04)
    T(d, k, "Details", DET, 72, round(y) + 22, 936, 200, 48, bold=False, color=CREAM, lh=1.2, mn=42)


def logo(d, k):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((100, round(lg.height * 100 / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 60 - 100, 50, shadowed=False, anchor="tl")


def build():
    d = Deck("vetopt", 3, "veterans-day-options-v1", "2026-11-11")
    # A
    d.bg(0, frosted(PHOTO, 0.45, 0.32, 0.5, 0.82), name="Photo melting into frosted green")
    words(d, 0, 900)
    logo(d, 0)
    # B
    d.bg(1, background(), name="Background: soft green with light bloom")
    aw, ah = 620, 700
    ph = grade(cover(ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB"), aw, ah, 0.43, 0.55))
    ax, ay = (W - aw) // 2, 110
    d.put(1, "Arch line", arch_line(aw, ah, 22), ax - 22, ay - 22, shadowed=False, anchor="tl")
    d.put(1, "Photo (arch)", arch(ph, aw, ah), ax, ay, shadowed=False, anchor="tl")
    words(d, 1, 870)
    logo(d, 1)
    # C
    src = ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB")
    bg = np.asarray(cover(src, W, H, 0.5, 0.5).filter(ImageFilter.GaussianBlur(45))).astype(np.float32)
    bg = bg * 0.35 + np.array([24, 60, 34], np.float32) * 0.65
    d.bg(2, Image.fromarray(bg.clip(0, 255).astype("uint8")).convert("RGBA"), name="Background: blurred photo, green")
    cw, ch = 860, 700
    card = grade(cover(src, cw, ch, 0.45, 0.5)).convert("RGBA")
    m = Image.new("L", (cw * 3, ch * 3), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cw * 3 - 1, ch * 3 - 1), 40 * 3, fill=255)
    card.putalpha(m.resize((cw, ch), Image.LANCZOS))
    glow = Image.new("RGBA", (cw + 120, ch + 120), (0, 0, 0, 0))
    gm = Image.new("L", glow.size, 0)
    ImageDraw.Draw(gm).rounded_rectangle((60, 70, cw + 60, ch + 70), 40, fill=110)
    glow.putalpha(gm.filter(ImageFilter.GaussianBlur(30)))
    d.put(2, "Soft shadow", glow, (W - cw) // 2 - 60, 110 - 60, shadowed=False, anchor="tl")
    d.put(2, "Photo (card)", card, (W - cw) // 2, 110, shadowed=False, anchor="tl")
    words(d, 2, 870)
    logo(d, 2)
    return d


if __name__ == "__main__":
    print(build().save(TILES, DECKS)[0])
