"""New Mexico Accelerator Workshop posts for November 2026 (Linnea, 3 Nov: the November doc never mentions New Mexico).

Facts from the live event page and calendar (www.soilfoodweb.com/calendar-event/aw-new-mexico-usa-2027/,
/calendar/): 3 to 14 May 2027, Synergia Ranch Retreat Center, 10 days in person, small groups each guided by a
mentor, build, monitor and maintain compost piles, brew liquid amendments, microscopy by level. Waitlist via the
workshop interest form. No price published, so none on the slides.

Photos: Synergia Ranch, February 2026 workshop (/home/user/photos/new-2026-10), each used on no other post.
Layout: photo on top, a flat colour panel below with the words (Education Blue for post 1, sand for post 2, so
neither looks like the green Costa Rica posts). Text at docs/slide-rules.md sizes.

  python3 tools/wormhole-visuals/nm_posts.py
"""
import os

from PIL import Image, ImageOps

from collage import Deck, cover, paper
from nov_fill import BLUE, BROWN, COLOR, CREAM, DECKS, INK, TILES, WHITE, logo

W, H = 1080, 1350
PH = "/home/user/photos/new-2026-10"
SAND = "#D8C3A5"
SPLIT = 760


def photo(name):
    return ImageOps.exif_transpose(Image.open(f"{PH}/{name}.jpg")).convert("RGB")


def slide(d, k, img, head, det, panel, ink, logo_path, fy=0.5, credit="Synergia Ranch, February 2026"):
    d.bg(k, paper(panel, 90 + k, w=W, h=H, grain=5), name="Panel")
    d.put(k, "Photo", cover(img, W, SPLIT, 0.5, fy).convert("RGBA"), 0, 0, shadowed=False, anchor="tl")
    y = d.text(k, "Headline", head, 72, SPLIT + 48, 936, 200, 84, kind="montserrat-bold", italic=False, color=ink,
               lh=1.05, min_size=84)
    d.text(k, "Details", det, 72, round(y) + 20, 680, H - round(y) - 60, 52, kind="source-reg", italic=False,
           color=ink, lh=1.2, min_size=50)
    d.text(k, "Credit", credit, 72, SPLIT - 62, 700, 50, 42, kind="source-reg", italic=False, color=CREAM, lh=1.0,
           shade=True, min_size=42)
    logo(d, k, logo_path, W - 72 - 220, H - 170, w=220)


def post1():
    d = Deck("nm20261119", 3, "new-mexico-may-2027-v1", "2026-11-19")
    slide(d, 0, photo("learning-outside-2-synergia"), "New Mexico, May 2027",
          "Our Accelerator Workshop, 3 to 14 May, at Synergia Ranch.", BLUE, CREAM, WHITE, fy=0.5)
    slide(d, 1, photo("mentors-purple-shirts-santa-fe"), "Learn with our mentors",
          "Ten days in person, in small groups, each guided by a mentor.", BLUE, CREAM, WHITE, fy=0.3,
          credit="Our mentors, Santa Fe, February 2026")
    slide(d, 2, photo("fire-pit-synergia"), "Join the waitlist",
          "Choose New Mexico on the workshop interest form. Link in bio.", BLUE, CREAM, WHITE, fy=0.55)
    return d


def post2():
    d = Deck("nm20261124", 3, "new-mexico-what-you-learn-v1", "2026-11-24")
    slide(d, 0, photo("reviewing-feedstock-synergia"), "Build the pile",
          "Choose feedstocks, then build, monitor and maintain your compost piles.", SAND, BROWN, COLOR, fy=0.45)
    slide(d, 1, photo("learning-outside-synergia"), "Learn in small groups",
          "Each group works with a mentor on compost, extracts and teas.", SAND, BROWN, COLOR, fy=0.5)
    slide(d, 2, photo("community-laughing-at-microscope"), "Read it under the scope",
          "Microscopy for beginners and advanced students. 3 to 14 May 2027.", SAND, BROWN, COLOR, fy=0.5,
          credit="Photo: Soil Food Web Foundation")
    return d


if __name__ == "__main__":
    for d in (post1(), post2()):
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(TILES, f"{d.id}-v1-{k}.jpg")), d.id
        print(d.save(TILES, DECKS)[0], d.pptx_name())
