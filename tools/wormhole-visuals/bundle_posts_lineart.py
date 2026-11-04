"""The other Fall Enrollment Special posts in the v6 look (Linnea, 4 Nov: "keep going like this"): white line drawings
on colour fades. Words from the sales page only, no slogans; until 2 December (Stephanie, 3 Nov).

  x20261118  Mon 9 Nov   Compost Intensive Course (2 slides)
  x20261125  Wed 18 Nov  Foundation Courses (2 slides)
  x20261130  Wed 25 Nov  last week (1 slide)
  fes20261130 -> Wed 2 Dec  last day (1 slide)

  python3 tools/wormhole-visuals/bundle_posts_lineart.py
"""
import os

from bundle_v6 import fade, slide
from collage import Deck
from nov_fill import DECKS, TILES

POSTS = [
    ("x20261118", "2026-11-09", "compost-intensive-lineart-v9", [
        (("#6B4A3A", "#1E3A22", (0.5, 0.28)), "thermometer", 520, 60, "The Compost Intensive Course",
         "Over ten weeks, you build 2 biological compost piles right where you live.", 84, 700),
        (("#1E7A3A", "#0E3B1E", (0.5, 0.28)), "sprout", 460, 60, "Choose your cohort",
         "January, May or August 2027. Fall Enrollment Special, until 2 December. Link in bio.", 84, 700)]),
    ("x20261125", "2026-11-18", "foundation-courses-lineart-v9", [
        (("#3780B8", "#123B26", (0.5, 0.3)), "microscope", 640, 60, "The Foundation Courses",
         "63 lectures and about 150 hours of study, with 40+ years of Dr. Elaine's knowledge. Self-paced.", 84, 700),
        (("#1E7A3A", "#0E3B1E", (0.5, 0.28)), "online", 640, 80, "Plus a seat in a 2027 Compost Intensive cohort",
         "Fall Enrollment Special, until 2 December. Link in bio.", 73, 700)]),
    ("x20261130", "2026-11-25", "fall-enrollment-last-week-lineart-v9", [
        (("#6B4A3A", "#0E3B1E", (0.5, 0.3)), "sunrise", 760, 80, "Last week",
         "Fall Enrollment Special: Foundation Courses + Compost Intensive, until 2 December. Link in bio.", 84, 760)]),
    ("fes20261130", "2026-12-02", "fall-enrollment-last-day-lineart-v9", [
        (("#1E7A3A", "#3A2A22", (0.5, 0.3)), "compost", 560, 80, "Last day",
         "Fall Enrollment Special: Foundation Courses + Compost Intensive. Link in bio.", 84, 760)]),
]

if __name__ == "__main__":
    for pid, iso, slug, slides in POSTS:
        d = Deck(pid, len(slides), slug, iso)
        for k, ((top, bottom, glow), art, aw, ay, head, det, hs, ty) in enumerate(slides):
            slide(d, k, fade(top, bottom, glow, seed=hash(pid) % 100 + k), art, aw, ay, head, det, hs, ty=ty)
        for k in range(1, len(slides) + 1):
            assert not os.path.exists(os.path.join(TILES, f"{pid}-v9-{k}.jpg"))
        print(d.save(TILES, DECKS)[0], d.pptx_name())
