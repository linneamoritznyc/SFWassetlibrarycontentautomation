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

# Full answers from the staff (Linnea, 9 Nov: "don't cut out the text"). Spelling typos fixed, wording kept.
FULL = {
"Allison Duck": "I'm thankful for our students' perseverance. In my role in student services, I get the inside perspective on what our students' goals are and I get to help them plan how to map out their pathways to achieve those goals. I'm so impressed by their determination, especially with mastering biologically complete compost creation and using their microscopes to monitor their progress.",
"Kavi Reddy": "I am thankful for all the soil organisms who help make this world so beautiful, for the evergrowing SFW community of people who understand the value of biodiverse soil life, and for my SFW team for sharing this knowledge across the globe!",
"Tommy Tepper": "I am thankful for seasons and how in certain seasons it feels nice and cozy to go dormant and to rest more. Similar to what microbes do, in how they move into dormancy and form cysts or spores during certain periods. I am thankful for rest and how certain times of the year encourage or force us to rest so that we are ready when spring (the busy season) comes.",
"Ayşen Ustunay": "This Thanksgiving, I'm especially grateful for the opportunity to work with many of my students. I want to share the journey about one of my students.\n\nShe is incredibly dedicated, and her journey has truly inspired me. Without land of her own, she faced one difficulty after another, from finding a place to make her compost to losing a farm opportunity just when she was ready to begin her field trial. Yet, she never complained or lost focus. She kept going, found another opportunity through a friend in another country, and even arranged to have part of her compost shipped there!\n\nKnowing that she is now happy and supported by her friends and family, while performing her field trial makes me so happy. I feel genuinely honored to be part of her journey. Students like her remind me how much determination and perseverance people can show when they truly believe in what they are doing.\n\nDr. Elaine would be so proud of her!",
"Casey Williams": "I am grateful simply for being able to be part of the change. I've always wanted to make a positive difference in the field of agriculture, in as large a way as possible. From where I stand in life at the moment, I'm able to do so in an ever expanding way. Additionally, I have the opportunity to continue to learn, gaining a greater depth of knowledge in this field, which fulfills my love of learning and also expands my capacity for helping heal the world's soils through education and direct action.",
"Stephanie McDaniel": "Feeling extreme gratitude for my deepening connection to the earth and all its living creatures, big and microscopic. This soil food web experience has given me even more connection and understanding for interests and hobbies I have even beyond gardening. Cooking, sourdough, fermentation of all sorts, it all has benefitted from understanding what Dr. Elaine taught in the Foundation Courses! I have enjoyed bringing it into the raising of my children. Including conversations that provide a deeper understanding of how it is all connected and how the microscopic world holds it all together has been fun and joyful.",
"Carla Portugal": "I feel blessed to have many reasons to be thankful. This year, I am specially grateful to be part of so many learning and teaching experiences. I am exploring co-adjacent fields of holistic knowledge and integrating it, building a broader view of life. I have been passionate about life since I can remember and this year I am building the best version yet of a life dedicated to learning, teaching, guiding and being guided, working with and being inspired by every person who enters my life. May this be the best year so far!",
"Delvin Solkinson": "I am so thankful for all the extraordinary people I get to learn with from Africa, Asia, Europe, Oceania, North America and South America, truly a global classroom. This diversity of perspectives from farmers, gardeners, homesteaders and people moving toward deeper nature connection creates a rich and vibrant community of practice and learning. What a joy it is to use technology to connect deeper with people around the world and to get support to connect deeper with nature where I live.",
}


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


def frame_cutouts(d, k, x0, y0, x1, y1, seed, sc=1.0):
    """Cut-paper pieces on the frame's edges: a band along the top, a few down the sides, acorns and mushrooms at the
    bottom corners. Same positions on every slide, different pieces, so the set reads as one."""
    rnd = random.Random(seed)
    lv = LEAVES[:]
    rnd.shuffle(lv)
    gr = GROUND[:]
    rnd.shuffle(gr)
    fw, fh = x1 - x0, y1 - y0
    # the pieces sit on the frame's outer edge, never over the middle of the photo (faces)
    top = [(x0 - 0.08 * fw, y0 + 0.02 * fh, 190, -25), (x0 + 0.16 * fw, y0 - 0.1 * fh, 150, 15),
           (x1 - 0.2 * fw, y0 - 0.1 * fh, 160, 22), (x1 + 0.1 * fw, y0 + 0.06 * fh, 185, 35)]
    side = [(x0 - 0.16 * fw, y0 + 0.45 * fh, 150, -40), (x1 + 0.15 * fw, y0 + 0.48 * fh, 120, 50)]
    for i, (cx, cy, w, r) in enumerate(top + side):
        d.put(k, f"Leaf {i + 1}", piece(lv[i % len(lv)], round(w * sc)), cx, cy, rot=r, shadowed=False)
    bottom = [(x0 - 0.12 * fw, y1 - 0.08 * fh, 150, -12), (x0 + 0.08 * fw, y1 + 0.0 * fh, 120, 8),
              (x1 + 0.02 * fw, y1 - 0.04 * fh, 160, 10), (x1 + 0.2 * fw, y1 - 0.2 * fh, 120, -15)]
    for i, (cx, cy, w, r) in enumerate(bottom):
        d.put(k, f"Acorn or mushroom {i + 1}", piece(gr[i % len(gr)], round(w * sc)), cx, cy, rot=r,
              shadowed=False)


def staff_slide(d, k, name, photo, fy, text, seed):
    """Small framed photo at the top so the whole answer fits below it, never under 42 px."""
    d.bg(k, paper(400 + k), name="Background: Organic Cream")
    size, y0 = 300, 60
    x0 = (W - size) // 2
    d.put(k, f"Photo: {name}", framed(photo, fy, size, border=10), x0 - 30, y0 - 30, shadowed=False, anchor="tl")
    frame_cutouts(d, k, x0, y0, x0 + size, y0 + size, seed, sc=0.6)
    T(d, k, "Name", name, 72, y0 + size + 30, 936, 80, 66, color=BROWN)
    top = y0 + size + 30 + 80 + 10
    T(d, k, "Quote", text, 72, top, 936, 1180 - top, 48, bold=False, color=INK, lh=1.2, mn=42)
    logo(d, k, w=140)


def cover(d):
    """"We are thankful for" and words taken from the staff answers (Linnea, 9 Nov), leaves falling across it."""
    from collage import font
    d.bg(0, paper(399), name="Background: Organic Cream")
    T(d, 0, "Headline", "We are thankful for", 72, 150, 936, 110, 86, color=BROWN)
    TAN = "#9C6B4E"
    rows = [[("perseverance", 66, GREEN), ("soil organisms", 52, BROWN)],
            [("seasons", 52, BROWN), ("rest", 66, TAN), ("spring", 52, GREEN)],
            [("biodiverse soil life", 66, BROWN)],
            [("determination", 52, GREEN), ("microbes", 66, BROWN)],
            [("being part of the change", 52, BROWN)],
            [("a global classroom", 66, GREEN)],
            [("sourdough", 52, TAN), ("fermentation", 52, BROWN)],
            [("learning and teaching", 66, BROWN)],
            [("our students", 52, GREEN), ("our team", 52, TAN)]]
    y, gap = 320, 34
    for r, row in enumerate(rows):
        ws = [font("montserrat-bold" if z >= 66 else "source-reg", False, z).getlength(t) + 8 for t, z, _ in row]
        h = max(z for _, z, _ in row) * 1.22
        x = (W - (sum(ws) + gap * (len(row) - 1))) / 2
        for (t, z, c), w in zip(row, ws):
            T(d, 0, f"Word: {t}", t, round(x), round(y + (h - z * 1.22) / 2), round(w) + 4, round(z * 1.3), z,
              bold=z >= 66, color=c, align="left", mn=z)
            x += w + gap
        y += h + 18
    fall = [(90, 80, 150, -30, "leaves-07"), (990, 80, 160, 25, "oak-25"), (60, 520, 120, 40, "leaves-00"),
            (1025, 470, 130, -20, "oak-21"), (80, 900, 110, 60, "oak-23"), (1010, 860, 140, -35, "leaves-04"),
            (520, 1230, 110, 15, "oak-24"), (150, 1215, 150, -10, "acorns-13"), (330, 1250, 120, 30, "mushrooms-small"),
            (760, 1235, 120, 5, "leaves-08")]
    for i, (cx, cy, w, r, n) in enumerate(fall):
        d.put(0, f"Falling leaf {i + 1}", piece(n, w), cx, cy, rot=r, shadowed=False)
    logo(d, 0)


def slides():
    """One slide per person; Ayşen's answer needs two (split at her paragraph break), same frame on both."""
    out = []
    for name, photo, fy, _ in STAFF:
        t = FULL[name]
        if name.startswith("Ayşen"):
            cut = t.index("Yet, she never")   # split mid-story, at a sentence, so both halves fit
            out.append((name, photo, fy, t[:cut].rstrip() + " \u2026"))
            out.append((name, photo, fy, "\u2026 " + t[cut:]))
        else:
            out.append((name, photo, fy, t))
    return out


def build(v, preview=False):
    people = slides()
    d = Deck("thx20261126", 1 + len(people), f"what-we-are-thankful-for-{v}", "2026-11-26")
    cover(d)
    for k, (name, photo, fy, text) in enumerate(people, start=1):
        staff_slide(d, k, name, photo, fy, text, seed=k)
    return d


if __name__ == "__main__":
    v = sys.argv[1]
    d = build(v, preview=len(sys.argv) > 2)
    for k in range(1, d.n + 1):
        assert not os.path.exists(os.path.join(TILES, f"thx20261126-{v}-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
