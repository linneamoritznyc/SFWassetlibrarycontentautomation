"""Fall Enrollment Special, 4 Nov post, 5 slides (Linnea, 4 Nov): the line-art colour-fade look, centred text, the
course badges cut from the course images on our sales pages (no blue boxes), the Compost Intensive badge from the
promo graphic on the bundle page, Dr. Elaine's webinar archive, and Linnea's 01-02-03 steps. No QR codes yet.
Wording from the bundle sales page and Linnea's decks. Never "keep your compost" (Linnea and Allison, 4 Nov).

  python3 tools/wormhole-visuals/bundle_final_nov4.py
"""
import os
import sys

from PIL import Image, ImageDraw

from bundle_three_styles import rgb
from bundle_three_styles_v12 import FY, M, MINT, T, footer, height
from bundle_v6 import H, W, fade, line_art
from collage import Deck
from nov_fill import CREAM, DECKS, TILES

_put = Deck.put
Deck.put = lambda self, k, name, im, x, y, **kw: _put(self, k, name, im, round(x), round(y), **kw)
BADGES = "/home/user/sfwlib/social/course-badges"
ART_ZONE = (50, 450)
HEAD_Y = 500


def art(d, k, name, w, zone=ART_ZONE):
    im = line_art(name, w)
    zh = zone[1] - zone[0]
    if im.height > zh:
        im = line_art(name, round(w * zh / im.height))
    d.put(k, "Line drawing", im, (W - im.width) // 2, zone[0] + (zh - im.height) // 2, shadowed=False, anchor="tl")


def text(d, k, head, det, hs=73, y=HEAD_Y):
    y = T(d, k, "Headline", head, M, y, 936, 300, hs)
    return T(d, k, "Details", det, M, round(y) + 24, 936, FY - round(y) - 50, 52, bold=False)


def badge(n, h):
    im = Image.open(f"{BADGES}/{n}-badge.png").convert("RGBA")
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def below(d, k, ims, ytop):
    gap = (936 - sum(i.width for i in ims)) // max(1, len(ims) - 1) if len(ims) > 1 else 0
    x = M if len(ims) > 1 else (W - ims[0].width) // 2
    y0 = round(ytop + (FY - ytop - max(i.height for i in ims)) / 2)
    for i, im in enumerate(ims):
        d.put(k, f"Badge {i + 1}", im, x, y0 + (max(j.height for j in ims) - im.height) // 2, shadowed=False,
              anchor="tl")
        x += im.width + gap


GAP_ART, GAP_HEAD, GAP_BADGE = 96, 44, 80
HLH, DLH, HW, DW = 1.12, 1.38, 936, 800   # line heights and text widths (Linnea, 4 Nov: more spacing)   # the same gaps on every slide (Linnea, 4 Nov: spacing)


def fit_art(name, w, maxh):
    im = line_art(name, w)
    return im if im.height <= maxh else line_art(name, round(w * maxh / im.height))


def stack(d, k, top_img, head, hs, det, below_imgs=None, area=(72, FY - 40), ds=52):
    """Drawing, headline, details and (optional) a row of badges, centred as one block between the top margin and
    the footer, with fixed gaps."""
    hh = height(head, hs, HW, lh=HLH)
    dh = height(det, ds, DW, bold=False, lh=DLH) if det else 0
    bh = max(i.height for i in below_imgs) if below_imgs else 0
    total = top_img.height + GAP_ART + hh + (GAP_HEAD + dh if det else 0) + (GAP_BADGE + bh if below_imgs else 0)
    y = area[0] + (area[1] - area[0] - total) // 2
    d.put(k, "Line drawing" if top_img.mode == "RGBA" else "Image", top_img, (W - top_img.width) // 2, y,
          shadowed=False, anchor="tl")
    y += top_img.height + GAP_ART
    T(d, k, "Headline", head, (W - HW) // 2, y, HW, hh + 6, hs, lh=HLH)
    y += hh
    if det:
        y += GAP_HEAD
        T(d, k, "Details", det, (W - DW) // 2, y, DW, dh + 6, ds, bold=False, lh=DLH)
        y += dh
    if below_imgs:
        y += GAP_BADGE
        gap = (936 - sum(i.width for i in below_imgs)) // max(1, len(below_imgs) - 1)
        x = M
        for n, im in enumerate(below_imgs):
            d.put(k, f"Badge {n + 1}", im, x, round(y + (bh - im.height) / 2), shadowed=False, anchor="tl")
            x += im.width + gap


def build(v):
    d = Deck("promo-fall-bundle", 6, f"fall-enrollment-bundle-final-{v}", "2026-11-04")
    # 1. cover
    d.bg(0, fade("#1E7A3A", "#0E3B1E", (0.5, 0.24), 40), name="Background fade")
    stack(d, 0, fit_art("online", 520, 250), "Foundation Courses + Compost Intensive", 84,
          "Fall Enrollment Special\nUntil 2 December.", [badge(f"fc{n}", 180) for n in (1, 2, 3, 4)], ds=66)
    footer(d, 0)
    # 2. Foundation Courses
    d.bg(1, fade("#3780B8", "#123B26", (0.5, 0.26), 41), name="Background fade")
    stack(d, 1, fit_art("leaves", 340, 300), "The Foundation Courses teach you to work out what your soil needs.", 73,
          "Four courses, 63 lectures and about 150 hours of study, with 40+ years of Dr. Elaine's knowledge. "
          "Self-paced, start the day you enroll.")
    footer(d, 1)
    # 3. Compost Intensive: the course's own badge is the one image
    d.bg(2, fade("#6B4A3A", "#1E3A22", (0.5, 0.26), 42), name="Background fade")
    stack(d, 2, badge("cic", 300), "The Compost Intensive Course teaches you to make it.", 73,
          "Ten weeks online, with a 90-minute live session with a mentor every week, alongside a global cohort of "
          "peers. You build 2 compost piles right where you live.")
    footer(d, 2)
    # 4. every scale (bundle page: who it's for; CIC FAQ: what it covers)
    d.bg(3, fade("#2F6B5A", "#123B26", (0.5, 0.26), 45), name="Background fade")
    stack(d, 3, fit_art("sunrise", 540, 250), "For farmers, ranchers, agronomists, consultants and gardeners", 73,
          "At any scale. The Compost Intensive covers thermophilic piles, vermicompost, USDA thermal composting "
          "and large-scale windrows.")
    footer(d, 3)
    # 5. Dr. Elaine's webinar archive
    d.bg(4, fade("#8A6A4A", "#1E3A22", (0.5, 0.26), 43), name="Background fade")
    stack(d, 4, fit_art("book", 380, 300), "Plus hundreds of hours\nwith Dr.\u00a0Elaine", 73,
          "Learn directly from the founder of the Soil Food Web School, in our legacy webinar archive recorded live "
          "with Dr.\u00a0Elaine\u00a0Ingham. 40+ years of her knowledge, science and land management practices, "
          "proven across the globe.")
    footer(d, 4)
    # 6. three steps, centred as one block
    d.bg(5, fade("#1E7A3A", "#123B26", (0.5, 0.2), 44), name="Background fade")
    steps = [("01", "Start today", "4 courses, self-paced"), ("02", "Pick your cohort", "January, May or August 2027"),
             ("03", "Build 2 compost piles", "Right where you live")]
    bh, g = 150, 18
    hh = height("Start today.\nPick your season.", 84, 936)
    dh = height("Fall Enrollment Special\nUntil 2 December.", 52, 936)
    total = hh + GAP_ART + 3 * bh + 2 * g + GAP_ART + dh
    y = 72 + (FY - 40 - 72 - total) // 2
    T(d, 5, "Headline", "Start today.\nPick your season.", M, y, 936, hh + 6, 84)
    top = y + hh + GAP_ART
    for i, (n, t1, t2) in enumerate(steps):
        y0 = top + i * (bh + g)
        bar = Image.new("RGBA", (936, bh), (0, 0, 0, 0))
        ImageDraw.Draw(bar).rounded_rectangle((0, 0, 935, bh - 1), 24, fill=(255, 255, 255, 30),
                                              outline=(255, 255, 255, 80), width=2)
        d.put(5, f"Step {n} box", bar, M, y0, shadowed=False, anchor="tl")
        T(d, 5, f"Step {n} number", n, M + 30, y0 + 38, 150, 80, 73, color=MINT, align="left")
        T(d, 5, f"Step {n} title", t1, M + 200, y0 + 18, 700, 62, 52, align="left")
        T(d, 5, f"Step {n} text", t2, M + 200, y0 + 80, 700, 62, 52, bold=False, align="left")
    T(d, 5, "Details", "Fall Enrollment Special\nUntil 2 December.", M, top + 3 * bh + 2 * g + GAP_ART, 936,
      dh + 6, 52)
    footer(d, 5)
    return d


if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "v21"
    d = build(v)
    for it in d.items:   # Linnea, 4 Nov: logo a bit lower on every slide (48 px from the bottom edge)
        if it.get("name") == "SFW logo":
            it["y"] += 24
        elif not str(it.get("name", "")).startswith("Background"):
            it["y"] += 30   # Linnea, 4 Nov: content a bit lower too
    for k in range(1, d.n + 1):
        assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-{v}-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
