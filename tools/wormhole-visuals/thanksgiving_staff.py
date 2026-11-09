"""Thanksgiving staff carousel, thx20261126 (Thu 26 Nov 2026), rebuilt from scratch (Linnea, 9 Nov).

1 cover + 1 slide per staff member, 1080 x 1350. Same frame on every slide: Organic Cream paper, a square photo in a
thin cream border, and cut-paper fall pieces (maple and oak leaves, acorns, small mushrooms) clustered on the frame's
edges, like Linnea's flower-frame mentor cards (Tommy Tepper) with fall cutouts in place of the flowers. The cover
has the eight staff photos in a group grid and leaves falling across it. Text per docs/slide-rules.md: Montserrat Bold
names and headline, Source Sans 3 quotes, every text box editable (Allison is still editing the quotes), colour logo
bottom right. Cutouts: cut-paper pieces generated on Replicate (flux-1.1-pro) and cut out, in
/home/user/sfwlib/social/fall-cutouts; red and red-spotted pieces left out (brand palette).

  python3 tools/wormhole-visuals/thanksgiving_staff.py <version> [preview]
"""
import os
import random
import sys

from PIL import Image, ImageDraw, ImageOps

from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import T
from bundle_v6 import H, W
from collage import Deck
from nov_fill import DECKS, TILES

_put = Deck.put
Deck.put = lambda self, k, name, im, x, y, **kw: _put(self, k, name, im, round(x), round(y), **kw)

CUT = "/home/user/sfwlib/social/fall-cutouts"
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
CREAM, BROWN, INK, GREEN = "#F4F1EA", "#4F3433", "#333130", "#156826"
NEW = "/home/user/photos/new-2026-10"
SITE = "/home/user/linneamoritznyc/final-sfwsite-linnea/img/w"

STAFF = [  # (name, photo, vertical focus, quote: short version until Allison sends her final text)
    ("Allison Duck", f"{NEW}/team-allison-duck.jpg", 0.35,
     "I'm thankful for our students' perseverance. I'm so impressed by their determination."),
    ("Kavi Reddy", f"{NEW}/team-kavi-reddy.jpg", 0.35,
     "I am thankful for all the soil organisms who help make this world so beautiful, and for the evergrowing SFW "
     "community."),
    ("Tommy Tepper", f"{NEW}/team-tommy-tapper.jpg", 0.3,
     "I am thankful for seasons, and for rest. Like microbes forming cysts and spores, it helps us be ready when "
     "spring comes."),
    ("Ayşen Ustunay", f"{NEW}/team-aysen-ustunay.jpg", 0.3,
     "Students like her remind me how much determination people can show when they truly believe in what they are "
     "doing."),
    ("Casey Williams", f"{NEW}/team-casey-williams.jpg", 0.3,
     "I am grateful simply for being able to be part of the change."),
    ("Stephanie McDaniel", f"{SITE}/stephanie.jpg", 0.35,
     "Feeling extreme gratitude for my deepening connection to the earth and all its living creatures, big and "
     "microscopic."),
    ("Carla Portugal", f"{SITE}/carla.jpg", 0.3,
     "This year, I am especially grateful to be part of so much learning and teaching."),
    ("Delvin Solkinson", f"{NEW}/team-delvin-solkinson.jpg", 0.3,
     "I am so thankful for all the extraordinary people I get to learn with from every continent, truly a global "
     "classroom."),
]

LEAVES = ["leaves-00", "leaves-02", "leaves-04", "leaves-05", "leaves-07", "leaves-08", "leaves-09", "oak-20",
          "oak-21", "oak-22", "oak-23", "oak-24", "oak-25", "oak-19"]
GROUND = ["acorns-10", "acorns-12", "acorns-13", "acorns-14", "acorns-15", "acorns-16", "acorns-18",
          "mushrooms-small", "oak-small-trio"]


def piece(name, w):
    im = Image.open(f"{CUT}/{name}.png").convert("RGBA")
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def paper(seed):
    return grain(Image.new("RGB", (W, H), CREAM), seed, 3)


def framed(path, fy, size, border=14):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    inner = size - 2 * border
    s = max(inner / im.width, inner / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - inner) // 2, max(0, round((im.height - inner) * fy))
    out = Image.new("RGB", (size, size), (251, 248, 241))
    out.paste(im.crop((x, y, x + inner, y + inner)), (border, border))
    sh = Image.new("RGBA", (size + 60, size + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((30, 36, size + 30, size + 36), fill=(60, 40, 30, 70))
    from PIL import ImageFilter
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    sh.alpha_composite(out.convert("RGBA"), (30, 30))
    return sh


def logo(d, k, w=150):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 60 - w, H - 50 - lg.height, shadowed=False, anchor="tl")


def frame_cutouts(d, k, x0, y0, x1, y1, seed):
    """Cut-paper pieces on the frame's edges: a band along the top, a few down the left, acorns and mushrooms at the
    bottom corners. Same positions on every slide, different pieces, so the set reads as one."""
    rnd = random.Random(seed)
    lv = LEAVES[:]
    rnd.shuffle(lv)
    gr = GROUND[:]
    rnd.shuffle(gr)
    top = [(x0 - 10, y0 + 10, 190, -25), (x0 + 120, y0 - 40, 150, 15), (x0 + 330, y0 - 55, 130, -8),
           (x1 - 170, y0 - 45, 160, 22), (x1 + 15, y0 + 30, 185, 35)]
    left = [(x0 - 55, y0 + 230, 150, -40), (x0 - 40, y0 + 420, 130, 20)]
    right = [(x1 + 40, y0 + 250, 120, 50)]
    for i, (cx, cy, w, r) in enumerate(top + left + right):
        d.put(k, f"Leaf {i + 1}", piece(lv[i % len(lv)], w), cx, cy, rot=r, shadowed=False)
    bottom = [(x0 - 20, y1 - 40, 150, -12), (x0 + 110, y1 - 10, 120, 8), (x1 - 30, y1 - 30, 160, 10),
              (x1 + 60, y1 - 100, 120, -15)]
    for i, (cx, cy, w, r) in enumerate(bottom):
        d.put(k, f"Acorn or mushroom {i + 1}", piece(gr[i % len(gr)], w), cx, cy, rot=r, shadowed=False)


def staff_slide(d, k, name, photo, fy, quote):
    d.bg(k, paper(400 + k), name="Background: Organic Cream")
    size, x0, y0 = 600, 240, 96
    fr = framed(photo, fy, size)
    d.put(k, f"Photo: {name}", fr, x0 - 30, y0 - 30, shadowed=False, anchor="tl")
    frame_cutouts(d, k, x0, y0, x0 + size, y0 + size, k)
    T(d, k, "Name", name, 72, 790, 936, 90, 73, color=BROWN)
    T(d, k, "Quote", "“" + quote + "”", 110, 898, 860, 280, 52, bold=False, color=INK, lh=1.25)
    logo(d, k)


def cover(d):
    d.bg(0, paper(399), name="Background: Organic Cream")
    T(d, 0, "Headline", "What we're\nthankful for", 72, 150, 936, 200, 86, color=BROWN)
    T(d, 0, "Details", "Our staff share what they are grateful for this year.", 140, 365, 800, 140, 52, bold=False,
      color=INK, lh=1.25)
    # the eight staff in a 4 x 2 group, same thin cream border as the staff slides
    s, g = 228, 20
    x0 = (W - (4 * s + 3 * g)) // 2
    for i, (name, photo, fy, _) in enumerate(STAFF):
        x, y = x0 + (i % 4) * (s + g), 560 + (i // 4) * (s + g)
        d.put(0, f"Photo: {name}", framed(photo, fy, s, border=7), x - 30, y - 30, shadowed=False, anchor="tl")
    # leaves falling across the slide
    fall = [(90, 80, 150, -30, "leaves-07"), (990, 70, 160, 25, "oak-25"), (55, 470, 120, 40, "leaves-00"),
            (1025, 420, 130, -20, "oak-21"), (330, 545, 110, 60, "oak-23"), (800, 1020, 140, -35, "leaves-04"),
            (500, 1170, 110, 15, "oak-24"), (150, 1210, 150, -10, "acorns-13"), (60, 960, 120, 5, "leaves-08"),
            (330, 1240, 120, 30, "mushrooms-small")]
    for i, (cx, cy, w, r, n) in enumerate(fall):
        d.put(0, f"Falling leaf {i + 1}", piece(n, w), cx, cy, rot=r, shadowed=False)
    logo(d, 0)


def build(v, preview=False):
    people = [STAFF[2]] if preview else STAFF
    d = Deck("thx20261126", 1 + len(people), f"what-we-are-thankful-for-{v}", "2026-11-26")
    cover(d)
    for k, (name, photo, fy, quote) in enumerate(people, start=1):
        staff_slide(d, k, name, photo, fy, quote)
    return d


if __name__ == "__main__":
    v = sys.argv[1]
    d = build(v, preview=len(sys.argv) > 2)
    for k in range(1, d.n + 1):
        assert not os.path.exists(os.path.join(TILES, f"thx20261126-{v}-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
