"""v10 of three line-art bundle posts (4 Nov, review of v9): the cohort slide gets a smaller drawing so the long
headline breathes; "Until 2 December" and "Ends tonight" get their own bold line on the last-week and last-day posts.

  python3 tools/wormhole-visuals/bundle_posts_lineart_v10.py
"""
import os

from PIL import Image

from bundle_v6 import H, W, fade, line_art
from collage import Deck
from nov_fill import CREAM, DECKS, TILES, WHITE


def slide(d, k, bg, art, aw, ay, head, hs, ty, sub, det):
    d.bg(k, bg, name="Background fade")
    im = line_art(art, aw)
    d.put(k, "Line drawing", im, (W - im.width) // 2, ay, shadowed=False, anchor="tl")
    y = d.text(k, "Headline", head, 72, ty, 936, 300, hs, kind="montserrat-bold", italic=False, color=CREAM,
               lh=1.08, min_size=66)
    if sub:
        y = d.text(k, "Date line", sub, 72, round(y) + 14, 936, 100, 70, kind="montserrat-bold", italic=False,
                   color=CREAM, lh=1.05, min_size=66)
    d.text(k, "Details", det, 72, round(y) + 24, 700, H - round(y) - 70, 52, kind="source-reg", italic=False,
           color=CREAM, lh=1.2, min_size=50)
    lg = Image.open(WHITE).convert("RGBA")
    lg = lg.resize((200, round(lg.height * 200 / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 72 - 200, H - 72 - lg.height, shadowed=False, anchor="tl")


POSTS = [
    ("x20261125", "2026-11-18", "foundation-courses-lineart-v10", [
        (("#3780B8", "#123B26", (0.5, 0.3)), "microscope", 640, 60, "The Foundation Courses", 84, 700, "",
         "63 lectures and about 150 hours of study, with 40+ years of Dr. Elaine's knowledge. Self-paced."),
        (("#1E7A3A", "#0E3B1E", (0.5, 0.24)), "online", 500, 90, "Plus a seat in a 2027 Compost Intensive cohort",
         70, 640, "", "Fall Enrollment Special, until 2 December. Link in bio.")]),
    ("x20261130", "2026-11-25", "fall-enrollment-last-week-lineart-v10", [
        (("#6B4A3A", "#0E3B1E", (0.5, 0.3)), "sunrise", 700, 80, "Last week", 84, 640, "Until 2 December",
         "Fall Enrollment Special: Foundation Courses + Compost Intensive. Link in bio.")]),
    ("fes20261130", "2026-12-02", "fall-enrollment-last-day-lineart-v10", [
        (("#1E7A3A", "#3A2A22", (0.5, 0.3)), "compost", 500, 80, "Last day", 84, 640, "Ends tonight",
         "Fall Enrollment Special: Foundation Courses + Compost Intensive. Link in bio.")]),
]

if __name__ == "__main__":
    for pid, iso, slug, slides in POSTS:
        d = Deck(pid, len(slides), slug, iso)
        for k, ((top, bottom, glow), *rest) in enumerate(slides):
            slide(d, k, fade(top, bottom, glow, seed=hash(pid) % 100 + k), *rest)
        for k in range(1, len(slides) + 1):
            assert not os.path.exists(os.path.join(TILES, f"{pid}-v10-{k}.jpg"))
        print(d.save(TILES, DECKS)[0], d.pptx_name())
