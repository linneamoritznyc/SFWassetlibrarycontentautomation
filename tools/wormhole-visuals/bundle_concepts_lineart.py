"""Fall Enrollment Special, more slides in the line-art look (Linnea, 4 Nov: "more stuff like this... with white
vectors", from her 10 concepts). Facts and wording from the bundle sales page only; no prices, no slogans.
Frosted panels are white at low opacity, so the fade shows through.

  python3 tools/wormhole-visuals/bundle_concepts_lineart.py
"""
import os

from PIL import Image, ImageDraw

from bundle_v6 import H, W, fade, line_art
from collage import Deck
from nov_fill import CREAM, DECKS, TILES, WHITE


def frost(d, k, name, x, y, w, h, a=34):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(255, 255, 255, a),
                                         outline=(255, 255, 255, 90), width=2)
    d.put(k, name, im, x, y, shadowed=False, anchor="tl")


def art(d, k, name, w, y, x=None):
    im = line_art(name, w)
    d.put(k, "Line drawing", im, (W - im.width) // 2 if x is None else x, y, shadowed=False, anchor="tl")


def logo(d, k):
    lg = Image.open(WHITE).convert("RGBA")
    lg = lg.resize((200, round(lg.height * 200 / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 72 - 200, H - 72 - lg.height, shadowed=False, anchor="tl")


def head(d, k, t, y, size=84):
    return d.text(k, "Headline", t, 72, y, 936, 300, size, kind="montserrat-bold", italic=False, color=CREAM,
                  lh=1.08, min_size=66)


def small(d, k, name, t, x, y, w, h=200, bold=False, size=52):
    return d.text(k, name, t, x, y, w, h, size, kind="montserrat-bold" if bold else "source-reg", italic=False,
                  color=CREAM, lh=1.2, min_size=50)


def build():
    d = Deck("promo-fall-bundle", 4, "fall-enrollment-bundle-concepts-v7", "2026-11-04")
    # 1. 4 + 1
    d.bg(0, fade("#1E7A3A", "#0E3B1E", (0.5, 0.3), 11), name="Background fade")
    art(d, 0, "book", 520, 70)
    d.text(0, "Number", "4 + 1", 72, 560, 936, 230, 210, kind="montserrat-bold", italic=False, color=CREAM, lh=1.0,
           min_size=180)
    y = small(d, 0, "Details", "4 Foundation Courses, plus a seat in a 2027 Compost Intensive cohort. "
              "Fall Enrollment Special, until 2 December.", 72, 800, 760, 300)
    logo(d, 0)
    # 2. what's in the bundle
    d.bg(1, fade("#3780B8", "#123B26", (0.8, 0.12), 12), name="Background fade")
    art(d, 1, "microscope", 330, 70, x=W - 72 - 330)
    head(d, 1, "What's in the bundle", 90, 84)
    rows = ["4 Foundation Courses, self-paced", "A seat in a 2027 Compost Intensive cohort",
            "A 90-minute live session with a mentor every week", "Foundation Courses webinar archive and community"]
    for i, r in enumerate(rows):
        y0 = 360 + i * 200
        frost(d, 1, f"Panel {i + 1}", 72, y0, 936, 172)
        d.text(1, f"Tick {i + 1}", "✓", 104, y0 + 46, 60, 80, 66, kind="montserrat-bold", italic=False, color=CREAM,
               lh=1.0, min_size=60)
        small(d, 1, f"Item {i + 1}", r, 184, y0 + 24, 790, 130)
    logo(d, 1)
    # 3. your 2027 cohort
    d.bg(2, fade("#6B4A3A", "#1E3A22", (0.5, 0.2), 13), name="Background fade")
    art(d, 2, "calendar", 380, 60)
    head(d, 2, "Pick your 2027 cohort", 470, 84)
    for i, (m, dates) in enumerate((("January", "11 Jan to 26 Mar"), ("May", "10 May to 25 Jul"),
                                    ("August", "30 Aug to 7 Nov"))):
        y0 = 600 + i * 170
        frost(d, 2, f"{m} panel", 72, y0, 936, 146)
        d.text(2, m, m, 108, y0 + 38, 380, 80, 66, kind="montserrat-bold", italic=False, color=CREAM, lh=1.0,
               min_size=66)
        small(d, 2, f"{m} dates", dates, 500, y0 + 44, 480, 80)
    small(d, 2, "Details", "Ten weeks online. Link in bio.", 72, 1120, 900, 80)
    logo(d, 2)
    # 4. judge it by hand
    d.bg(3, fade("#1E7A3A", "#3A2A22", (0.5, 0.25), 14), name="Background fade")
    art(d, 3, "thermometer", 380, 60)
    head(d, 3, "Judge compost by hand", 520, 84)
    for i, w in enumerate(("Look", "Feel", "Smell", "Structure", "Maturity")):
        x0, y0 = 72 + (i % 3) * 316, 640 + (i // 3) * 130
        frost(d, 3, f"{w} chip", x0, y0, 300, 108, a=28)
        d.text(3, w, w, x0 + 24, y0 + 28, 260, 60, 52, kind="montserrat-bold", italic=False, color=CREAM, lh=1.0,
               min_size=50)
    small(d, 3, "Details", "In the Compost Intensive Course. No microscopy skills needed.", 72, 930, 760, 160)
    logo(d, 3)
    return d


if __name__ == "__main__":
    d = build()
    for k in range(1, d.n + 1):
        assert not os.path.exists(os.path.join(TILES, f"promo-fall-bundle-v7-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
