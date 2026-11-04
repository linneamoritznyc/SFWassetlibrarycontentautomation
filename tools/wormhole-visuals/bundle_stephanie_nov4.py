"""4 Nov bundle post, rebuilt on Stephanie's notes (4 Nov): more photos, fewer words and icons; the CIC badge next to
the Foundation Course badges on the cover; Dr. Elaine's slide in her purple with her photo; the live Zoom class on the
Compost Intensive slide; a community slide; the FC webinars; the discount on the slide before the QR code.

  1 cover: Foundation Courses + Compost Intensive, FC1-4 + CIC badges
  2 Dr. Elaine's decades of knowledge in one easy-to-follow online course (purple, photo of her)
  3 Compost Intensive: the live class (Zoom screenshot from Carla)
  4 community (SFW students photo from the CIC page)
  5 FC webinars (purple, photo of her)
  6 over 50% off, until 2 December
  7 QR code (one deck per platform)

  python3 tools/wormhole-visuals/bundle_stephanie_nov4.py <version> <platform> <short link>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageOps

import bundle_final_nov4 as b
from bundle_final_nov4 import badge
from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import FY, M, T, footer, height
from bundle_v6 import H, W, fade
from collage import Deck, cover
from nov_fill import CREAM, DECKS, TILES

PURPLE = "#6B4C7A"   # Legacy Mulberry, Dr. Elaine only (docs/brand.md)
ST = "/home/user/sfwlib/social/students"
ELAINE_BAG = "/home/user/SFW-SocialMedia/assets/photo/web/elaine-with-sample-bag.jpg"
ELAINE_SCOPE = "/home/user/SFW-SocialMedia/assets/photo/web/elaine-flower-shirt-microscope.jpg"
ZOOM = os.environ.get("ZOOM", f"{ST}/cic-zoom-call-blurred.jpg")   # Carla's screenshot, names blurred except hers
PHOTO_H = 620


def photo_slide(d, k, path, fx, fy, panel, head, det, hs=73, fit="cover", ph=None):
    """Photo across the top, a colour panel below with the headline and one short line."""
    PHOTO_H = ph or globals()["PHOTO_H"]
    bg = Image.new("RGB", (W, H), panel)
    d.bg(k, grain(bg, 300 + k, 3), name="Background panel")
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if fit == "cover":
        d.put(k, "Photo", cover(im, W, PHOTO_H, fx, fy).convert("RGBA"), 0, 0, shadowed=False, anchor="tl")
    else:   # screenshot: crop Zoom's dark window frame away, then show the whole grid of faces
        import numpy as np
        g = np.asarray(im.convert("L")) > 60
        rows, cols = np.where(g.sum(1) > im.width * 0.25)[0], np.where(g.sum(0) > im.height * 0.25)[0]
        im = im.crop((cols.min(), rows.min(), cols.max() + 1, rows.max() + 1))
        w = W - 2 * 40
        h = round(im.height * w / im.width)
        d.put(k, "Screenshot", im.resize((w, h), Image.LANCZOS).convert("RGBA"), 40, (PHOTO_H - h) // 2 + 20,
              shadowed=False, anchor="tl")
    hh = height(head, hs, 936)
    dh = height(det, 52, 900, bold=False, lh=1.25)
    y = PHOTO_H + 50 + (FY + 30 - PHOTO_H - 50 - (hh + 24 + dh)) // 2
    assert y >= PHOTO_H + 40, (head, y)
    T(d, k, "Headline", head, M, y, 936, hh + 6, hs)
    T(d, k, "Details", det, (W - 900) // 2, y + hh + 24, 900, dh + 6, 52, bold=False, lh=1.25)
    footer(d, k)


def build(v, plat):
    d = Deck("promo-fall-bundle", 7, f"fall-enrollment-bundle-{plat}-{v}", "2026-11-04")
    # 1. cover: all five course badges
    d.bg(0, fade("#1E7A3A", "#0E3B1E", (0.5, 0.35), 200), name="Background fade")
    hh = height("Foundation Courses + Compost Intensive", 86, 936)
    dh = height("Fall Enrollment Special\nUntil 2 December.", 66, 900, bold=False, lh=1.3)
    fcs = [badge(f"fc{n}", 180) for n in (1, 2, 3, 4)]
    cic = badge("cic", 250)
    G_DATE, G_ROW, G_CIC = 44, 90, 60   # Linnea, 4 Nov: fix the spacing on the cover
    total = hh + G_DATE + dh + G_ROW + 180 + G_CIC + cic.height
    y = 72 + (FY - 30 - 72 - total) // 2
    T(d, 0, "Headline", "Foundation Courses + Compost Intensive", M, y, 936, hh + 6, 86)
    y += hh + G_DATE
    T(d, 0, "Details", "Fall Enrollment Special\nUntil 2 December.", (W - 900) // 2, y, 900, dh + 6, 66, bold=False,
      lh=1.3)
    y += dh + G_ROW
    gap = (900 - sum(i.width for i in fcs)) // 3
    x = (W - 900) // 2
    for n, im in enumerate(fcs):
        d.put(0, f"Badge FC{n + 1}", im, x, y, shadowed=False, anchor="tl")
        x += im.width + gap
    y += 180 + G_CIC
    d.put(0, "Badge Compost Intensive", cic, (W - cic.width) // 2, y, shadowed=False, anchor="tl")
    footer(d, 0)
    # 2. Dr. Elaine: purple, her photo
    photo_slide(d, 1, ELAINE_BAG, 0.45, 0.35, PURPLE,
                "Our 4 flagship Foundation Courses",
                "Dr. Elaine Ingham's seminal lectures on the soil food web and how to restore it. 40+ years of her "
                "knowledge, easy to follow and self-paced.", hs=84)
    # 3. Compost Intensive: the live class
    photo_slide(d, 2, ZOOM, 0.5, 0.5, "#4F3433", "The Compost Intensive Course",
                "Every week, live with Soil Food Web expert mentors who worked extensively alongside "
                "Dr.\u00a0Elaine\u00a0Ingham, and a global cohort of peers.", hs=84, fit="contain")
    # 4. community
    photo_slide(d, 3, f"{ST}/sfw-students-graduation.png", 0.5, 0.45, "#156826", "Join our student community",
                "A community for Foundation Courses students, and your own Compost Intensive cohort.", hs=84)
    # 5. FC webinars: purple, her photo
    photo_slide(d, 4, ELAINE_SCOPE, 0.45, 0.4, PURPLE, "Dr. Elaine's legacy webinar archive",
                "Hundreds of hours recorded live with Dr.\u00a0Elaine and others, going deeper into the Foundation "
                "Courses and beyond, to deepen your learning and put it into\u00a0action.", hs=84, ph=540)
    # 6. the discount, just before the QR code
    d.bg(5, fade("#1E7A3A", "#0E3B1E", (0.5, 0.4), 205), name="Background fade")
    hh2 = height("off the Foundation Courses + Compost Intensive bundle", 73, 936)
    total = 380 + 40 + hh2 + 60 + dh
    y = 60 + (FY - 10 - 60 - total) // 2
    T(d, 5, "Discount", "Over\n50%", M, y, 936, 390, 180, mn=150, lh=1.0, color="#A8D5B0")
    y += 380 + 40
    # $2,700 against the page's $5,900 combined value is 54% off the bundle; against the Foundation Courses alone
    # ($5,000) it is 46%, so "over 50%" is only true for the whole bundle
    T(d, 5, "Headline", "off the Foundation Courses + Compost Intensive bundle", M, y, 936, hh2 + 6, 73)
    y += hh2 + 60
    T(d, 5, "Details", "Fall Enrollment Special\nUntil 2 December.", (W - 900) // 2, y, 900, dh + 6, 66, bold=False,
      lh=1.3)
    footer(d, 5)
    # 7. QR
    b.qr_slide(d, 6)
    return d


if __name__ == "__main__":
    v, plat, link = sys.argv[1], sys.argv[2], sys.argv[3]
    b.QR = link
    import bundle_three_styles_v12 as v12
    v12.QR_LINK = link
    d = build(v, plat)
    for k in range(1, d.n + 1):
        assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-{v}-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
