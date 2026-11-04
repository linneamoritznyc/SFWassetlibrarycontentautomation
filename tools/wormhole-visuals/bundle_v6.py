"""Bundle carousel v6 (Linnea, 4 Nov: "cool white line graphics", "cool color fades"). Same words as v4, word for word.

White line illustrations generated once on Replicate (flux-1.1-pro, white lines on black; no people, no photos), stored
in /home/user/sfwlib/social/lineart; black turned transparent. Backgrounds are brand colour fades with a soft glow.

  python3 tools/wormhole-visuals/bundle_v6.py
"""
import os

import numpy as np
from PIL import Image

from collage import Deck
from nov_fill import CREAM, DECKS, TILES, WHITE

W, H = 1080, 1350
ART = "/home/user/sfwlib/social/lineart"


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def fade(top, bottom, glow=(0.5, 0.3), seed=0):
    """Vertical colour fade with a soft light spot behind the drawing and a little grain."""
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    img = hexrgb(top) * (1 - y) + hexrgb(bottom) * y
    img = np.broadcast_to(img, (H, W, 3)).copy()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - glow[0] * W) / W) ** 2 + ((yy - glow[1] * H) / H) ** 2)
    img += (np.clip(1 - r / 0.45, 0, 1) ** 2 * 38)[..., None]
    img += np.random.default_rng(seed).normal(0, 3, (H, W, 1)).astype(np.float32)
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8")).convert("RGBA")


def line_art(name, w):
    im = Image.open(f"{ART}/{name}.png").convert("L")
    a = np.asarray(im).astype(np.float32)
    alpha = np.clip((a - 40) * 1.6, 0, 255).astype("uint8")
    out = Image.new("RGBA", im.size, (255, 255, 255, 0))
    out.putalpha(Image.fromarray(alpha))
    out = out.crop(out.getchannel("A").getbbox())
    return out.resize((w, round(out.height * w / out.width)), Image.LANCZOS)


def slide(d, k, bg, art, art_w, art_y, head, det, hsize, ty=790):
    d.bg(k, bg, name="Background fade")
    im = line_art(art, art_w)
    d.put(k, "Line drawing", im, (W - im.width) // 2, art_y, shadowed=False, anchor="tl")
    y = d.text(k, "Headline", head, 72, ty, 936, 300, hsize, kind="montserrat-bold", italic=False, color=CREAM,
               lh=1.08, min_size=66)
    d.text(k, "Details", det, 72, round(y) + 24, 700, H - round(y) - 70, 52, kind="source-reg", italic=False,
           color=CREAM, lh=1.2, min_size=50)
    lg = Image.open(WHITE).convert("RGBA")
    lg = lg.resize((200, round(lg.height * 200 / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 72 - 200, H - 72 - lg.height, shadowed=False, anchor="tl")


if __name__ == "__main__":
    d = Deck("promo-fall-bundle", 3, "fall-enrollment-bundle-v6", "2026-11-04")
    slide(d, 0, fade("#1E7A3A", "#0E3B1E", (0.5, 0.28), 1), "online", 760, 90,
          "Foundation Courses + Compost Intensive", "Fall Enrollment Special, until 2 December. Link in bio.", 84)
    slide(d, 1, fade("#3780B8", "#123B26", (0.5, 0.3), 2), "leaves", 420, 50,
          "The Foundation Courses teach you to work out what your soil needs.",
          "Introduction to the Soil Food Web, BioComplete™ Compost, BioComplete™ Liquid Amendments and Microscopy. "
          "Self-paced, start the day you enroll.", 70, ty=620)
    slide(d, 2, fade("#6B4A3A", "#1E3A22", (0.45, 0.28), 3), "compost", 500, 50,
          "The Compost Intensive Course teaches you to make it.",
          "Ten weeks online, with a 90-minute live session with a mentor every week. You build two batches of compost "
          "where you live, and you keep them.", 70, ty=620)
    for k in (1, 2, 3):
        assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-v6-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
