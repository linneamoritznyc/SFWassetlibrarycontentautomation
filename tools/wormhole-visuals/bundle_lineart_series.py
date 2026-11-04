"""The other Fall Enrollment Special posts in the look Linnea approved on 4 Nov (bundle_final_nov4.py): line art on
colour fades, one centred block per slide, course badges cut from our sales pages, the Instagram QR code on its own
last slide. Wording from the bundle and Compost Intensive pages only (checked 4 Nov). Never "keep your compost", never
failing piles, no prices.

  x20261118 v10   Mon 9 Nov    The Compost Intensive Course
  x20261125 v17   Wed 18 Nov   Look, feel, smell, structure, maturity + Microscopy
  x20261130 v17   Wed 25 Nov   One week left: choose your 2027 cohort
  fes20261130 v16 Wed 2 Dec    Last day

  python3 tools/wormhole-visuals/bundle_lineart_series.py
"""
import os

from PIL import Image, ImageDraw

import bundle_final_nov4 as b
from bundle_final_nov4 import GAP_ART, badge, fit_art, stack
from bundle_three_styles_v12 import FY, M, MINT, T, footer, height
from bundle_v6 import W, fade
from collage import Deck
from nov_fill import DECKS, TILES

b.QR = "https://tr.ee/ce6tWIaOx7"   # Instagram short link; Facebook and LinkedIn versions come later
FCS = lambda h=180: [badge(f"fc{n}", h) for n in (1, 2, 3, 4)]


def bars(d, k, head, rows, foot, seed, colors=("#1E7A3A", "#123B26")):
    """Headline, a list of frosted rows (title, text), and a closing line, centred as one block."""
    d.bg(k, fade(colors[0], colors[1], (0.5, 0.22), seed), name="Background fade")
    hh = height(head, 84, 936)
    bh, g = 150, 18
    fh = height(foot, 52, 936)
    total = hh + GAP_ART + len(rows) * bh + (len(rows) - 1) * g + GAP_ART + fh
    y = 72 + (FY - 40 - 72 - total) // 2 + 30
    T(d, k, "Headline", head, M, y, 936, hh + 6, 84)
    top = y + hh + GAP_ART
    for i, (t1, t2) in enumerate(rows):
        y0 = top + i * (bh + g)
        bar = Image.new("RGBA", (936, bh), (0, 0, 0, 0))
        ImageDraw.Draw(bar).rounded_rectangle((0, 0, 935, bh - 1), 24, fill=(255, 255, 255, 30),
                                              outline=(255, 255, 255, 80), width=2)
        d.put(k, f"Row {i + 1} box", bar, M, y0, shadowed=False, anchor="tl")
        T(d, k, f"Row {i + 1} title", t1, M + 40, y0 + 18, 856, 62, 52, align="left")
        T(d, k, f"Row {i + 1} text", t2, M + 40, y0 + 80, 856, 62, 52, bold=False, align="left", color=MINT)
    T(d, k, "Details", foot, M, top + len(rows) * bh + (len(rows) - 1) * g + GAP_ART, 936, fh + 6, 52)
    footer(d, k)


def lift(d):
    for it in d.items:   # same offsets as the 4 Nov post: logo and content a bit lower
        if it.get("name") == "SFW logo":
            it["y"] += 24


def cic(v):
    d = Deck("x20261118", 5, f"compost-intensive-lineart-{v}", "2026-11-09")
    d.bg(0, fade("#6B4A3A", "#1E3A22", (0.5, 0.26), 50), name="Background fade")
    stack(d, 0, badge("cic", 300), "The Compost Intensive Course", 84,
          "A hands-on, 10-week online training, alongside a global cohort of peers.")
    footer(d, 0)
    d.bg(1, fade("#1E7A3A", "#0E3B1E", (0.5, 0.26), 51), name="Background fade")
    stack(d, 1, fit_art("thermometer", 300, 300), "Build 2 compost piles right where you live", 73,
          "Over ten weeks you learn to choose feedstocks, balance recipes, manage temperature and moisture, "
          "with a 90-minute live session with a mentor every week.")
    footer(d, 1)
    d.bg(2, fade("#2F6B5A", "#123B26", (0.5, 0.26), 52), name="Background fade")
    stack(d, 2, fit_art("sprout", 320, 300), "No prerequisites", 84,
          "All are welcome. You don't need to finish the Foundation Courses before the Intensive begins.")
    footer(d, 2)
    bars(d, 3, "Choose your 2027 cohort", [("January", "11 January to 26 March"), ("May", "10 May to 25 July"),
                                          ("August", "30 August to 7 November")],
         "Part of the Fall Enrollment Special,\nuntil 2 December.", 53)
    b.qr_slide(d, 4)
    return d


def by_hand(v):
    d = Deck("x20261125", 4, f"look-feel-smell-microscopy-lineart-{v}", "2026-11-18")
    d.bg(0, fade("#6B4A3A", "#1E3A22", (0.5, 0.26), 60), name="Background fade")
    stack(d, 0, fit_art("hands", 360, 300), "Look, feel, smell, structure, maturity", 73,
          "In the Compost Intensive Course you assess compost quality using practical field observations.")
    footer(d, 0)
    d.bg(1, fade("#3780B8", "#123B26", (0.5, 0.26), 61), name="Background fade")
    stack(d, 1, fit_art("microscope", 460, 300), "Foundation Course 4: Microscopy", 73,
          "Learn to use a compound microscope to identify and quantify bacteria, fungi, protozoa and nematodes.")
    footer(d, 1)
    d.bg(2, fade("#1E7A3A", "#0E3B1E", (0.5, 0.24), 62), name="Background fade")
    stack(d, 2, fit_art("online", 520, 250), "Foundation Courses + Compost Intensive", 84,
          "Fall Enrollment Special\nUntil 2 December.", FCS(), ds=66)
    footer(d, 2)
    b.qr_slide(d, 3)
    return d


def last_week(v):
    d = Deck("x20261130", 4, f"one-week-left-lineart-{v}", "2026-11-25")
    d.bg(0, fade("#6B4A3A", "#0E3B1E", (0.5, 0.26), 70), name="Background fade")
    stack(d, 0, fit_art("sunrise", 560, 280), "One week left", 86,
          "Fall Enrollment Special\nUntil 2 December.", ds=66)
    footer(d, 0)
    bars(d, 1, "Start today.\nPick your season.", [("January", "11 January to 26 March"),
                                                    ("May", "10 May to 25 July"),
                                                    ("August", "30 August to 7 November")],
         "Start the Foundation Courses today.\nPick one 2027 cohort.", 71, ("#3780B8", "#123B26"))
    d.bg(2, fade("#1E7A3A", "#0E3B1E", (0.5, 0.24), 72), name="Background fade")
    stack(d, 2, badge("cic", 260), "Foundation Courses + Compost Intensive", 84,
          "Four self-paced courses, a seat in a 2027 Compost Intensive cohort, and hundreds of hours of webinars "
          "with Dr. Elaine.")
    footer(d, 2)
    b.qr_slide(d, 3)
    return d


def last_day(v):
    d = Deck("fes20261130", 3, f"last-day-lineart-{v}", "2026-12-02")
    d.bg(0, fade("#1E7A3A", "#3A2A22", (0.5, 0.26), 80), name="Background fade")
    stack(d, 0, fit_art("compost", 440, 300), "Last day", 86,
          "The Fall Enrollment Special ends today.", ds=66)
    footer(d, 0)
    d.bg(1, fade("#3780B8", "#123B26", (0.5, 0.24), 81), name="Background fade")
    stack(d, 1, fit_art("online", 520, 250), "Foundation Courses + Compost Intensive", 84,
          "Four self-paced courses, a seat in a 2027 Compost Intensive cohort, and hundreds of hours of webinars "
          "with Dr. Elaine.", FCS(170))
    footer(d, 1)
    b.qr_slide(d, 2)
    return d


if __name__ == "__main__":
    for fn, v in ((cic, "v10"), (by_hand, "v17"), (last_week, "v17"), (last_day, "v16")):
        d = fn(v)
        lift(d)
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(TILES, f"{d.id}-{v}-{k}.jpg")), d.id
        print(d.save(TILES, DECKS)[0], d.pptx_name())
