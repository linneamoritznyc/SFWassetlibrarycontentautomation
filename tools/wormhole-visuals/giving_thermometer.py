"""GivingTuesday progress Story (1080 x 1920): an SFW compost thermometer with dollars where the degrees go.
Drawn in code (no AI images). The needle is its own square object centred on the dial, so in Canva you rotate it
around the dial centre to the current total. Default: pointing at $0 (straight to the 225 degree start).

  python3 tools/wormhole-visuals/giving_thermometer.py <version> [fraction 0..1]
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

import collage
from bundle_three_styles import rgb
from bundle_three_styles_v12 import T
from collage import Deck
from cyber_nov30 import CREAM, MINT, leaf_texture, logo
from nov_fill import DECKS, TILES

W, SH = 1080, 1920
BROWN, GREEN, GOLD = "#4F3433", "#156826", "#C9A227"
FONT = "/home/user/fonts/Montserrat-Bold.ttf"
A0, A1 = 225, -45   # dial sweep, degrees (0 at 3 o'clock, counter-clockwise positive)


def ang(f):
    return math.radians(A0 + (A1 - A0) * f)


def dial(D):
    k = 3
    S = D * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = S / 2
    dr.ellipse((0, 0, S - 1, S - 1), fill=rgb("#D8C3A5") + (255,))            # sand bezel
    dr.ellipse((26 * k, 26 * k, S - 26 * k, S - 26 * k), fill=rgb(CREAM) + (255,))
    f_lab = ImageFont.truetype(FONT, 34 * k)
    for i in range(0, 21):
        f = i / 20
        a = ang(f)
        r1 = c - 50 * k
        r0 = r1 - (44 * k if i % 5 == 0 else 22 * k)
        dr.line((c + r0 * math.cos(a), c - r0 * math.sin(a), c + r1 * math.cos(a), c - r1 * math.sin(a)),
                fill=rgb(BROWN) + (255,), width=(7 if i % 5 == 0 else 4) * k)
        if i % 5 == 0:
            lab = "$0" if i == 0 else f"${i * 5}k"
            rl = r0 - 52 * k
            tw = dr.textlength(lab, font=f_lab)
            dr.text((c + rl * math.cos(a) - tw / 2, c - rl * math.sin(a) - 22 * k), lab, font=f_lab,
                    fill=rgb(BROWN) + (255,))
    # green arc for the goal zone
    dr.arc((60 * k, 60 * k, S - 60 * k, S - 60 * k), start=-A0, end=-A1, fill=rgb(GREEN) + (255,), width=6 * k)
    f_small = ImageFont.truetype(FONT, 30 * k)
    t = "GOAL $100,000"
    dr.text((c - dr.textlength(t, font=f_small) / 2, c + 120 * k), t, font=f_small, fill=rgb(GREEN) + (255,))
    return im.resize((D, D), Image.LANCZOS)


def needle(D, f):
    k = 3
    S = D * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = S / 2
    a = ang(f)
    L = c - 110 * k
    tip = (c + L * math.cos(a), c - L * math.sin(a))
    w = 16 * k
    p1 = (c + w * math.cos(a + math.pi / 2), c - w * math.sin(a + math.pi / 2))
    p2 = (c + w * math.cos(a - math.pi / 2), c - w * math.sin(a - math.pi / 2))
    dr.polygon([tip, p1, p2], fill=rgb(BROWN) + (255,))
    dr.ellipse((c - 34 * k, c - 34 * k, c + 34 * k, c + 34 * k), fill=rgb(BROWN) + (255,))
    dr.ellipse((c - 12 * k, c - 12 * k, c + 12 * k, c + 12 * k), fill=rgb(GOLD) + (255,))
    return im.resize((D, D), Image.LANCZOS)


def build(v, fracs):
    collage.H = SH
    try:
        d = Deck("st20261201give", len(fracs), f"giving-tuesday-thermometer-story-{v}", "2026-12-01")
        for k, f in enumerate(fracs):
            one(d, k, f)
        return d.save(TILES, DECKS)[0]
    finally:
        collage.H = 1350


def one(d, k, f):
    if True:
        d.bg(k, leaf_texture(770).resize((W, SH)), name="Background: green leaf texture")
        T(d, k, "Eyebrow", "GivingTuesday · December 1", 72, 300, 936, 70, 54, bold=False, color=MINT)
        T(d, k, "Headline", "We did it.\nThank you!" if f >= 1 else "Help us reach\nour goal", 72, 380, 936, 200, 86, color=CREAM, lh=1.04)
        D = 760
        x, y = (W - D) // 2, 620
        stem_w, stem_h = 34, 200
        stem = Image.new("RGBA", (stem_w * 4, stem_h * 4), (0, 0, 0, 0))   # the long compost-thermometer stem, pointed
        ImageDraw.Draw(stem).polygon([(0, 0), (stem_w * 4, 0), (stem_w * 4, (stem_h - 40) * 4), (stem_w * 2, stem_h * 4),
                                      (0, (stem_h - 40) * 4)], fill=rgb("#D8C3A5") + (255,))
        d.put(k, "Thermometer stem", stem.resize((stem_w, stem_h), Image.LANCZOS), (W - stem_w) // 2, y + D - 20,
              shadowed=False, anchor="tl")
        d.put(k, "Thermometer dial", dial(D), x, y, shadowed=False, anchor="tl")
        d.put(k, "Needle (rotate around its centre to the current total)", needle(D, f), x, y, shadowed=False,
              anchor="tl")
        pw = 600
        pill = Image.new("RGBA", (pw * 4, 110 * 4), (0, 0, 0, 0))
        ImageDraw.Draw(pill).rounded_rectangle((0, 0, pw * 4 - 1, 110 * 4 - 1), 220, fill=rgb(GOLD) + (255,))
        d.put(k, "Give button (gold)", pill.resize((pw, 110), Image.LANCZOS), (W - pw) // 2, 1590, shadowed=False,
              anchor="tl")
        T(d, k, "Give", "Give today", 72, 1608, 936, 70, 54, color=BROWN)
        lg = Image.open("/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png").convert("RGBA")
        lg = lg.resize((130, round(lg.height * 130 / lg.width)), Image.LANCZOS)
        d.put(k, "SFW logo", lg, (W - 130) // 2, 120, shadowed=False, anchor="tl")


if __name__ == "__main__":
    print(build(sys.argv[1], [0.1, 0.25, 0.5, 0.75, 1.0]))
