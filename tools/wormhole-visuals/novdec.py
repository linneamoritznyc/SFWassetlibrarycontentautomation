"""November and December 2026 posts (the pl2026 drafts).

One flat brand colour per post (never white, never the same colour two posts in a
row), a rounded Soil Brown heading, Montserrat body text, real photos in a thin ink
frame, real micrographs in round lenses, simple flat diagrams drawn in code with one
even outline, thin hand-drawn arrows with labels, the logo in clear space bottom right.
No generated pictures. No purple, no gold.

  python3 tools/wormhole-visuals/novdec.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v1-<n>.jpg   (1080 x 1350)
    -> apps/web/public/wormhole/decks/DD-MM-YYYY-<slug>.pptx
       (Reels: the deck and tools/wormhole-visuals/out/reels/<id>-v1-<n>.jpg are 1080 x 1920)
"""
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw

import collage
from collage import Deck, cover, draw_layer, hexrgb, paper
from watercolor_posts import arrow_layer, wobble_rect

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
REELS = os.path.join(HERE, "out", "reels")
MANIFEST = os.path.join(HERE, "out", "novdec.json")
W = 1080

NEW = "/home/user/photos/new-2026-10"
MICRO = "/home/user/SFW-SocialMedia/assets/microscopy"
CC = "/home/user/photos/cc"
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
FLOWERS = "/home/user/sfwlib/social/cutouts-flowers"
SOILC = "/home/user/sfwlib/social/cutouts-soil"

BROWN, BODY, CREAMT = "#4F3433", "#5C4636", "#F4F1EA"
# brand colours as flat backgrounds (Light Green at 25%, Natural Tan at 35%, over white)
CREAM, LGREEN, TAN, SAGE, DEEP = "#F4F1EA", "#D5E9DA", "#EEE1D7", "#DDE5D4", "#22371F"
# flat washes for drawn diagrams
WASH = {"soil": "#8A6A55", "soil2": "#B08B6E", "sand": "#D9C29A", "silt": "#B9A58C", "clay": "#8E7B6E",
        "water": "#CFE0E3", "leaf": "#7FA36B", "leaf2": "#C98B4E", "root": "#E9DCC3", "fungi": "#FFFFFF",
        "green": "#59A66C", "deep": "#22371F", "tan": "#C89B7B", "rock": "#9C978E", "sky": "#E7EEF0"}
LINE = (52, 40, 38)


class Theme:
    def __init__(self, bg):
        self.bg = bg
        dark = bg == DEEP
        self.head = CREAMT if dark else BROWN
        self.body = "#E3DDCC" if dark else BODY
        self.label = CREAMT if dark else BROWN
        self.arrow = CREAMT if dark else BROWN
        self.ink = (233, 226, 207) if dark else LINE


# ------------------------------------------------------------------ registry and build
REG = {}


def post(pid, iso, slug, n, bg, reel=False):
    def wrap(fn):
        REG[pid] = dict(iso=iso, slug=slug, n=n, bg=bg, reel=reel, fn=fn)
        return fn
    return wrap


class Page:
    """Slide helpers bound to one deck, one theme and one slide height."""

    def __init__(self, d, t, h):
        self.d, self.t, self.h = d, t, h
        self.credits = []

    # text ------------------------------------------------------------
    def heading(self, k, text, y=110, size=84, w=900, x=90, h=420, align="left", color=None):
        return self.d.text(k, "heading", text, x, round(y), w, h, size, kind="fredoka", italic=False,
                           color=color or self.t.head, lh=1.12, align=align, min_size=64)

    def body(self, k, text, y, size=40, w=880, x=92, h=320, align="left"):
        return self.d.text(k, "body", text, x, round(y), w, h, size, kind="mont", italic=False, color=self.t.body,
                           lh=1.38, align=align, min_size=30)

    def label(self, k, text, x, y, w=300, size=31, align="left", color=None):
        return self.d.text(k, f"label {text[:24]}", text, round(x), round(y), w, 160, size, kind="mont-medium",
                           italic=False, color=color or self.t.label, lh=1.22, align=align, min_size=26)

    def small(self, k, text, y=None, x=92, w=700, size=22):
        y = self.h - 70 if y is None else y
        return self.d.text(k, "credit", text, x, round(y), w, 80, size, kind="mont", italic=False, color=self.t.body,
                           lh=1.25, min_size=18)

    # pictures ----------------------------------------------------------
    def put(self, k, name, im, x, y):
        self.d.put(k, name, im, round(x), round(y), shadowed=False, anchor="tl")
        return (round(x), round(y), im.width, im.height)

    def photo(self, k, src, x, y, w, h, fx=0.5, fy=0.5, seed=1, name="photo"):
        """A real photo set into the page in a thin hand-drawn ink frame."""
        pad = 10
        ph = cover(src, w, h, fx, fy).convert("RGBA")
        out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
        out.alpha_composite(ph, (pad, pad))
        ink = self.t.ink

        def fn(dr, s):
            rnd = random.Random(seed)
            x0, y0, x1, y1 = pad - 3, pad - 3, pad + w + 3, pad + h + 3
            pts = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)),
                                       ((x0, y1), (x0, y0))):
                for i in range(24):
                    t = i / 24
                    pts.append((ax + (bx - ax) * t + rnd.uniform(-1.1, 1.1), ay + (by - ay) * t + rnd.uniform(-1.1, 1.1)))
            pts.append(pts[0])
            dr.line([(a * s, b * s) for a, b in pts], fill=ink + (255,), width=round(2.6 * s), joint="curve")
        out.alpha_composite(draw_layer(out.width, out.height, fn))
        return self.put(k, name, out, x - pad, y - pad)

    def lens(self, k, src, cx, cy, dia, center=(0.5, 0.5), zoom=1.0, name="micrograph"):
        """A real micrograph in a round eyepiece with a dark rim; center is the point of the image to show."""
        im = Image.open(src).convert("RGB")
        side = min(im.width, im.height) / zoom
        px, py = center[0] * im.width, center[1] * im.height
        x0 = min(max(0, px - side / 2), im.width - side)
        y0 = min(max(0, py - side / 2), im.height - side)
        im = im.crop((round(x0), round(y0), round(x0 + side), round(y0 + side)))
        disc = collage.round_photo(im, dia, ring=max(10, dia // 30), ring_color="#1B1B18")
        return self.put(k, name, disc, cx - disc.width / 2, cy - disc.height / 2)

    def cut(self, k, path, x, y, w=None, h=None, name=None):
        im = Image.open(path).convert("RGBA")
        bb = im.getchannel("A").getbbox()
        im = im.crop(bb)
        s = (w / im.width) if w else (h / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        return self.put(k, name or os.path.basename(path).split(".")[0], im, x, y)

    def drawn(self, k, w, h, fn, x, y, name="diagram"):
        return self.put(k, name, draw_layer(w, h, fn), x, y)

    def arrow(self, k, p0, p1, bend=0.25, seed=0):
        lay, x, y = arrow_layer(p0, p1, bend, seed)
        if self.t.arrow != BROWN:  # recolour for dark pages
            r, g, b = hexrgb(self.t.arrow)
            a = lay.getchannel("A")
            lay = Image.new("RGBA", lay.size, (r, g, b, 0))
            lay.putalpha(a)
        self.d.put(k, "arrow", lay, x, y, shadowed=False, anchor="tl")

    def logo(self, k, size=150):
        im = Image.open(LOGO).convert("RGBA")
        im = im.resize((size, round(im.height * size / im.width)), Image.LANCZOS)
        if self.t.bg == DEEP:  # the logo sits on a small cream disc on dark pages
            disc = Image.new("RGBA", (size + 36, size + 36), (0, 0, 0, 0))
            ImageDraw.Draw(disc).ellipse((0, 0, size + 35, size + 35), fill=hexrgb(CREAMT) + (255,))
            disc.alpha_composite(im, (18, (size + 36 - im.height) // 2))
            im = disc
        self.d.put(k, "logo", im, W - 56 - im.width, self.h - 50 - im.height, shadowed=False, anchor="tl")

    def credit(self, text):
        if text not in self.credits:
            self.credits.append(text)


def build(pid):
    spec = REG[pid]
    iso, slug, n, bg, reel = spec["iso"], spec["slug"], spec["n"], spec["bg"], spec["reel"]
    result = {}
    for h in ((1350, 1920) if reel else (1350,)):
        collage.H = h
        d = Deck(pid, n, slug, iso)
        t = Theme(bg)
        pg = Page(d, t, h)
        for k in range(n):
            d.bg(k, paper(bg, sum(map(ord, pid)) + k, w=W, h=h, grain=5), name=f"background-{k + 1}")
        spec["fn"](pg)
        if h == 1350:
            names, _ = d.save(TILES, None if reel else DECKS)
            result.update(tiles=names, texts=d.slide_texts(), credits=pg.credits,
                          pptx=None if reel else d.pptx_name())
        else:
            os.makedirs(REELS, exist_ok=True)
            d.save(REELS, DECKS)
            result["pptx"] = d.pptx_name()
    collage.H = 1350
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    man[pid] = dict(iso=iso, **result)
    json.dump(man, open(MANIFEST, "w"), indent=1)
    return result


# ------------------------------------------------------------------ drawing helpers
def outline(dr, s, shape, xy, fill, width=2.6, **kw):
    getattr(dr, shape)([v * s for v in xy], fill=hexrgb(fill) + (255,) if fill else None, outline=LINE + (255,),
                       width=round(width * s), **kw)


def poly(dr, s, pts, fill, width=2.6):
    dr.polygon([(x * s, y * s) for x, y in pts], fill=hexrgb(fill) + (255,) if fill else None, outline=LINE + (255,),
               width=round(width * s))


def wavy(x0, x1, y, amp, seed, n=24):
    rnd = random.Random(seed)
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(i * 0.9 + seed) + rnd.uniform(-amp / 3, amp / 3))
            for i in range(n + 1)]


def threads(dr, s, x, y, ang, length, seed, color="#FFFFFF", width=2.0, depth=0, alpha=235):
    rnd = random.Random(seed * 7 + depth)
    pts = [(x, y)]
    for _ in range(int(length / 6)):
        ang += rnd.uniform(-0.25, 0.25)
        x += 6 * math.cos(ang)
        y += 6 * math.sin(ang)
        pts.append((x, y))
        if depth < 2 and rnd.random() < 0.06:
            threads(dr, s, x, y, ang + rnd.choice((-1, 1)) * rnd.uniform(0.5, 1.0), length * 0.45,
                    seed + len(pts), color, width * 0.75, depth + 1, alpha)
    dr.line([(a * s, b * s) for a, b in pts], fill=hexrgb(color) + (alpha,), width=max(1, round(width * s)),
            joint="curve")


# ================================================================== Read the drop: ciliates (Reel)
CILIATE = f"{NEW}/Ciliate, 60x obj, Patricia J Coppola.jpg"
CIL_AT = (0.548, 0.497)
TEA = f"{NEW}/sfw-inc-geo-tea-brewer.jpg"


@post("pl20261130", "2026-11-30", "read-the-drop-ciliates-v1", 4, DEEP, reel=True)
def ciliates(p):
    h = p.h
    mid = h * 0.56
    p.heading(0, "This is a ciliate.", y=120, size=100)
    x, y, w, hh = p.lens(0, CILIATE, 520, mid - 20, 680, center=CIL_AT, zoom=2.0)
    p.label(0, "a ciliate, seen at 60x", 80, y + hh + 20, w=420)
    p.arrow(0, (320, y + hh + 14), (450, y + hh * 0.72), bend=-0.2, seed=1)

    p.heading(1, "Hair-like cilia cover its body.", y=120, size=92)
    d1 = 700
    x, y, w, hh = p.lens(1, CILIATE, 520, mid, d1, center=CIL_AT, zoom=2.2)
    cx, cy = 520, mid
    p.label(1, "cilia", 880, cy - 330, w=180)
    p.arrow(1, (905, cy - 280), (cx + 0.29 * d1, cy - 0.05 * d1), bend=0.3, seed=2)
    p.label(1, "cilia", 70, cy + 0.42 * d1, w=180)
    p.arrow(1, (120, cy + 0.42 * d1 - 8), (cx - 0.2 * d1, cy + 0.3 * d1), bend=-0.3, seed=3)

    p.heading(2, "Lots of them in compost or tea?", y=120, size=92)
    top = mid - 260
    p.photo(2, TEA, 90, top, 560, 400, fx=0.55, seed=4)
    p.label(2, "compost tea brewing", 90, top + 420, w=420)
    lx, ly, lw, lh_ = p.lens(2, CILIATE, 820, top + 330, 360, center=CIL_AT, zoom=1.8)
    p.label(2, "one ciliate is normal, a slide full is a warning", 90, top + 560, w=520)
    p.arrow(2, (560, top + 575), (lx + 40, ly + lh_ - 70), bend=0.25, seed=5)

    p.heading(3, "Oxygen has run low. Fix it before you apply.", y=120, size=88)
    top = mid - 160
    p.photo(3, TEA, 90, top, 900, 520, fx=0.55, seed=6)
    p.label(3, "aerate the brew, turn the pile, add structure", 90, top + 550, w=640)
    for k in range(4):
        p.logo(k)
    p.credit("Micrograph: Patricia J Coppola. Tea brewer photo: SFW library.")
    p.small(0, "Micrograph: Patricia J Coppola, 60x objective")


# ================================================================== Myth vs mechanism: organic matter and water
def drop(dr, s, cx, cy, r, fill):
    pts = []
    for i in range(61):
        a = -math.pi / 2 + 2 * math.pi * i / 60
        rr = r * (1 - 0.0 * math.sin(a))
        x = cx + rr * math.cos(a)
        y = cy + rr * math.sin(a)
        if a < -math.pi / 2 + 0.9 or a > 3 * math.pi / 2 - 0.9:
            t = abs(((a + math.pi / 2) % (2 * math.pi)))
            t = min(t, 2 * math.pi - t) / 0.9
            x = cx + (x - cx) * t
            y = cy - r * 1.7 + (y - (cy - r * 1.7)) * t
        pts.append((x, y))
    poly(dr, s, pts, fill)


@post("pl20261207", "2026-12-07", "myth-organic-matter-and-water-v1", 6, SAGE)
def om_water(p):
    p.heading(0, "Myth: “Add 1% organic matter and your soil holds 20,000 more gallons of water per acre.”",
              y=110, size=78, h=520)
    p.drawn(0, 700, 560, lambda dr, s: drop(dr, s, 350, 360, 190, WASH["water"]), 60, 600, name="drawn-drop")
    p.label(0, "the claim everyone repeats", 660, 820, w=300)
    p.arrow(0, (700, 900), (610, 990), bend=-0.25, seed=1)

    p.heading(1, "A 2018 review of about 60 studies tested that claim.", y=110, size=80)
    def papers(dr, s):
        for i in range(6):
            x, y = 60 + i * 26, 40 + i * 22
            outline(dr, s, "rectangle", (x, y, x + 380, y + 470), "#FBF8F1")
            for j in range(9):
                dr.line(((x + 40) * s, (y + 70 + j * 42) * s, (x + 340 - (j % 3) * 40) * s, (y + 70 + j * 42) * s),
                        fill=LINE + (120,), width=round(3 * s))
    p.drawn(1, 640, 600, papers, 230, 470, name="drawn-papers")
    p.label(1, "Minasny and McBratney, European Journal of Soil Science", 120, 1110, w=620, size=28)

    p.heading(2, "A 1% rise in soil organic carbon raised available water only slightly, on average about 1 mm per "
              "10 cm of soil.", y=110, size=72, h=560)
    def two_drops(dr, s):
        drop(dr, s, 210, 330, 170, WASH["water"])
        drop(dr, s, 640, 420, 60, WASH["water"])
    p.drawn(2, 860, 520, two_drops, 110, 640, name="drawn-drops")
    p.label(2, "the claim", 220, 1170, w=260)
    p.label(2, "what the studies measured", 640, 820, w=300)
    p.arrow(2, (700, 900), (750, 1010), bend=0.3, seed=2)
    p.small(2, "Drops are not to scale.", y=1250, w=400)

    p.heading(3, "The effect was larger in sandy soils and smaller in clays.", y=110, size=80)
    def soils(dr, s):
        rnd = random.Random(3)
        outline(dr, s, "rounded_rectangle", (20, 20, 400, 420), WASH["sand"], radius=round(30 * s))
        for _ in range(70):
            x, y, r = rnd.uniform(50, 370), rnd.uniform(50, 390), rnd.uniform(9, 16)
            outline(dr, s, "ellipse", (x - r, y - r, x + r, y + r), "#E8D6B0", width=1.6)
        outline(dr, s, "rounded_rectangle", (480, 20, 860, 420), WASH["clay"], radius=round(30 * s))
        for i in range(14):
            yy = 50 + i * 26
            dr.line((500 * s, yy * s, 840 * s, (yy + rnd.uniform(-4, 4)) * s), fill=LINE + (140,), width=round(2 * s))
    p.drawn(3, 880, 440, soils, 100, 560, name="drawn-sand-and-clay")
    p.label(3, "sand: more effect", 120, 1010, w=380)
    p.label(3, "clay: less effect", 580, 1010, w=380)

    p.heading(4, "Where biology really helps water: aggregates and pores that let rain soak in instead of running off.",
              y=110, size=74, h=520)
    def infil(dr, s):
        rnd = random.Random(5)
        outline(dr, s, "rectangle", (20, 160, 860, 560), WASH["soil"])
        for _ in range(26):
            x, y, r = rnd.uniform(60, 820), rnd.uniform(200, 520), rnd.uniform(22, 40)
            outline(dr, s, "ellipse", (x - r, y - r * 0.8, x + r, y + r * 0.8), WASH["soil2"], width=2)
        for i in range(9):
            x = 70 + i * 92
            dr.line((x * s, 10 * s, (x - 14) * s, 120 * s), fill=hexrgb("#6E9FB0") + (255,), width=round(4 * s))
            pts = [(x - 14 + 8 * math.sin(j / 2), 180 + j * 14) for j in range(rnd.randint(10, 24))]
            dr.line([(a * s, b * s) for a, b in pts], fill=hexrgb("#6E9FB0") + (220,), width=round(5 * s))
    p.drawn(4, 880, 580, infil, 100, 600, name="drawn-infiltration")
    p.label(4, "rain soaks in between the crumbs", 110, 1200, w=600)

    p.heading(5, "Honest numbers build trust. Source on the slide.", y=110, size=84)
    p.body(5, "Minasny, B. and McBratney, A. B. (2018). Limited effect of organic matter on soil available water "
              "capacity. European Journal of Soil Science 69: 39–47.", 460, size=36, w=860)
    for k in range(6):
        p.logo(k)


# ================================================================== drawn kit: jar, crumbs, leaf
def jar(dr, s, x, y, w, h, layers, top_water=None, murky=None, lid=True, marks=()):
    """A glass jar, bottom at y + h. layers: [(fraction_of_height, colour), ...] from the bottom up."""
    r = 34
    inner_top = y + 70
    by = y + h
    cur = by - 6
    for frac, col in layers:
        lh = (h - 76) * frac
        dr.rectangle(((x + 8) * s, (cur - lh) * s, (x + w - 8) * s, cur * s), fill=hexrgb(col) + (255,))
        cur -= lh
    if murky:
        dr.rectangle(((x + 8) * s, (inner_top + 30) * s, (x + w - 8) * s, cur * s), fill=hexrgb(murky) + (255,))
        cur = inner_top + 30
    elif top_water:
        dr.rectangle(((x + 8) * s, (inner_top + 30) * s, (x + w - 8) * s, cur * s), fill=hexrgb(top_water) + (255,))
    for my in marks:
        dr.line(((x - 18) * s, my * s, (x + 26) * s, my * s), fill=hexrgb("#B23A2E") + (255,), width=round(5 * s))
    # glass outline and shine
    dr.rounded_rectangle((x * s, inner_top * s, (x + w) * s, by * s), radius=round(r * s), outline=LINE + (255,),
                         width=round(3 * s))
    dr.line(((x + 26) * s, (inner_top + 40) * s, (x + 26) * s, (by - 60) * s), fill=(255, 255, 255, 150),
            width=round(10 * s))
    if lid:
        outline(dr, s, "rounded_rectangle", (x + 18, y, x + w - 18, inner_top + 4), "#B9A58C", radius=round(10 * s))


def crumb(dr, s, cx, cy, r, seed, fill=None, pores=True):
    rnd = random.Random(seed)
    pts = [(cx + r * (0.82 + rnd.uniform(0, 0.22)) * math.cos(a), cy + r * (0.82 + rnd.uniform(0, 0.22)) * math.sin(a))
           for a in [i * 2 * math.pi / 22 for i in range(22)]]
    poly(dr, s, pts, fill or WASH["soil"])
    if pores:
        for _ in range(int(r / 9)):
            a, d = rnd.uniform(0, 6.28), rnd.uniform(0, r * 0.7)
            rr = rnd.uniform(r * 0.06, r * 0.13)
            px, py = cx + d * math.cos(a), cy + d * math.sin(a)
            dr.ellipse(((px - rr) * s, (py - rr * 0.7) * s, (px + rr) * s, (py + rr * 0.7) * s),
                       fill=hexrgb(WASH["soil2"]) + (255,))


def leaf_shape(dr, s, cx, cy, L, ang, fill, seed=0, bite=0.0):
    rnd = random.Random(seed)
    pts = []
    for i in range(41):
        t = i / 40
        wdt = math.sin(math.pi * t) * L * 0.32
        pts.append((t * L - L / 2, -wdt))
    for i in range(40, -1, -1):
        t = i / 40
        wdt = math.sin(math.pi * t) * L * 0.32
        pts.append((t * L - L / 2, wdt * (1 - bite * (rnd.random() > 0.6))))
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(cx + px * ca - py * sa, cy + px * sa + py * ca) for px, py in pts]
    poly(dr, s, pts, fill)
    dr.line(((cx - L / 2 * ca) * s, (cy - L / 2 * sa) * s, (cx + L / 2 * ca) * s, (cy + L / 2 * sa) * s),
            fill=LINE + (200,), width=round(2 * s))


# ================================================================== Do this weekend: the jar test
@post("pl20261219", "2026-12-19", "do-this-weekend-jar-test-v1", 5, SAGE)
def jar_test(p):
    S, SI, CL, WA, MU = WASH["sand"], WASH["silt"], WASH["clay"], WASH["water"], "#9C8670"
    p.heading(0, "What is your soil made of? Find out with a jar.", y=110, size=88)
    p.drawn(0, 420, 640, lambda dr, s: jar(dr, s, 40, 0, 340, 620, [], murky=MU), 330, 470, name="drawn-jar")
    p.cut(0, f"{SOILC}/dark-soil-clump.png", 110, 900, w=260)
    p.label(0, "a jar, water and a handful of your soil", 740, 560, w=280)
    p.arrow(0, (790, 680), (700, 780), bend=0.3, seed=1)

    p.heading(1, "Fill a jar one third with soil, top up with water and a pinch of dish soap. Shake hard.", y=110,
              size=74, h=420)
    def shake(dr, s):
        jar(dr, s, 60, 0, 340, 620, [(0.33, "#7A5E48")], top_water=WA)
        for i in range(3):
            dr.arc(((0 - i * 22) * s, (200 - i * 30) * s, (60 - i * 22) * s, (420 + i * 30) * s), 120, 240,
                   fill=LINE + (200,), width=round(3 * s))
            dr.arc(((400 + i * 22) * s, (200 - i * 30) * s, (460 + i * 22) * s, (420 + i * 30) * s), -60, 60,
                   fill=LINE + (200,), width=round(3 * s))
    p.drawn(1, 470, 640, shake, 290, 520, name="drawn-jar")
    p.label(1, "one third soil", 70, 1000, w=230)
    p.arrow(1, (180, 995), (380, 1000), bend=-0.2, seed=2)
    p.label(1, "water", 800, 700, w=200)
    p.arrow(1, (820, 750), (640, 800), bend=0.2, seed=3)
    p.label(1, "a pinch of dish soap", 760, 520, w=240)
    p.arrow(1, (800, 600), (640, 680), bend=0.25, seed=4)

    p.heading(2, "Sand settles in about a minute. Mark the line.", y=110, size=88)
    sand_top = 470 + 620 - 6 - (620 - 76) * 0.2
    p.drawn(2, 420, 640, lambda dr, s: jar(dr, s, 40, 0, 340, 620, [(0.2, S)], murky=MU,
                                            marks=(sand_top - 470,)), 330, 470, name="drawn-jar")
    p.label(2, "sand", 790, 1000, w=200)
    p.arrow(2, (800, 1030), (660, 1040), bend=0.2, seed=5)
    p.label(2, "mark the line", 80, 860, w=230)
    p.arrow(2, (160, 930), (340, sand_top - 6), bend=-0.25, seed=6)

    p.heading(3, "Silt settles over a few hours. Mark it. Clay can take a day or more.", y=110, size=80)
    p.drawn(3, 420, 640, lambda dr, s: jar(dr, s, 40, 0, 340, 620, [(0.2, S), (0.18, SI), (0.12, CL)], top_water=WA),
            330, 470, name="drawn-jar")
    base = 470 + 620 - 6
    unit = 620 - 76
    for nm, y0, y1, side in (("sand", 0, 0.2, 0), ("silt", 0.2, 0.38, 1), ("clay", 0.38, 0.5, 0), ("water", 0.5, 0.9, 1)):
        yc = base - unit * (y0 + y1) / 2
        if side:
            p.label(3, nm, 820, yc - 20, w=180)
            p.arrow(3, (815, yc), (690, yc), bend=0.1, seed=int(yc))
        else:
            p.label(3, nm, 120, yc - 20, w=180)
            p.arrow(3, (230, yc), (360, yc), bend=-0.1, seed=int(yc))

    p.heading(4, "Compare the layers to find your texture.", y=110, size=88)
    def triangle(dr, s):
        A, B, C = (40, 520), (580, 520), (310, 52)
        poly(dr, s, [A, B, C], "#F4F1EA")
        for i in range(1, 5):
            t = i / 5
            for P, Q, R in ((A, B, C), (B, C, A), (C, A, B)):
                p1 = (P[0] + (R[0] - P[0]) * t, P[1] + (R[1] - P[1]) * t)
                p2 = (Q[0] + (R[0] - Q[0]) * t, Q[1] + (R[1] - Q[1]) * t)
                dr.line((p1[0] * s, p1[1] * s, p2[0] * s, p2[1] * s), fill=LINE + (70,), width=round(1.5 * s))
        outline(dr, s, "ellipse", (300, 330, 336, 366), "#B23A2E")
    p.drawn(4, 620, 560, triangle, 380, 520, name="drawn-texture-triangle")
    p.drawn(4, 260, 520, lambda dr, s: jar(dr, s, 20, 0, 220, 500, [(0.2, S), (0.18, SI), (0.12, CL)], top_water=WA),
            80, 560, name="drawn-jar")
    p.label(4, "sand", 360, 1065, w=150)
    p.label(4, "silt", 860, 780, w=150)
    p.label(4, "clay", 650, 470, w=150)
    p.label(4, "your soil", 620, 1070, w=200)
    p.arrow(4, (690, 1065), (700, 890), bend=0.25, seed=9)
    for k in range(5):
        p.logo(k)


# ================================================================== Two levels: soil aggregates
def pill(p, k, text, x, y, fill):
    def fn(dr, s):
        outline(dr, s, "rounded_rectangle", (2, 2, 238, 62), fill, radius=round(30 * s))
    p.drawn(k, 240, 64, fn, x, y, name="level-pill")
    p.label(k, text, x, y + 14, w=240, size=30, align="center", color=CREAMT if fill == DEEP else BROWN)


def macro(dr, s, cx, cy, r, seed, hyphae=True, roots=True, cut=False):
    rnd = random.Random(seed)
    subs = []
    for _ in range(60):
        a, d = rnd.uniform(0, 6.28), r * math.sqrt(rnd.random()) * 0.78
        subs.append((cx + d * math.cos(a), cy + d * math.sin(a), rnd.uniform(r * 0.12, r * 0.2)))
    for x, y, rr in subs:
        crumb(dr, s, x, y, rr, int(x * 7 + y), fill=rnd.choice((WASH["soil"], "#7B5D49", "#94735C")), pores=False)
    if roots:
        pts = [(cx - r * 1.3 + i * 12, cy - r * 0.9 + i * 9 + 14 * math.sin(i / 3)) for i in range(int(r * 2.6 / 12))]
        dr.line([(a * s, b * s) for a, b in pts], fill=hexrgb(WASH["root"]) + (255,), width=round(9 * s), joint="curve")
        dr.line([(a * s, b * s) for a, b in pts], fill=LINE + (160,), width=round(1.5 * s), joint="curve")
    if hyphae:
        for i in range(9):
            a = i * 0.7
            sx, sy = cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a)
            threads(dr, s, sx, sy, a + math.pi + rnd.uniform(-0.6, 0.6), r * 1.5, seed + i, color="#FFFFFF", width=2.2)
    if cut:
        dr.line(((cx - r * 1.4) * s, (cy + r * 0.15) * s, (cx + r * 1.4) * s, (cy - r * 0.1) * s),
                fill=hexrgb("#B23A2E") + (255,), width=round(5 * s))


@post("pl20261123", "2026-11-23", "two-levels-soil-aggregates-v1", 7, TAN)
def aggregates(p):
    p.heading(0, "Soil aggregates, explained twice. Level 1 for new gardeners, level 2 for consultants.", y=110,
              size=80, h=460)
    p.cut(0, f"{SOILC}/dark-soil-clump.png", 250, 640, w=580)
    pill(p, 0, "Level 1", 120, 1110, "#F4F1EA")
    pill(p, 0, "Level 2", 400, 1110, DEEP)

    for k in (1, 2, 3):
        pill(p, k, "Level 1", 90, 90, "#F4F1EA")
    for k in (4, 5):
        pill(p, k, "Level 2", 90, 90, DEEP)

    p.heading(1, "Level 1: Healthy soil clumps into crumbs. Those crumbs are aggregates.", y=200, size=74)
    def crumbs(dr, s):
        rnd = random.Random(11)
        for i in range(9):
            crumb(dr, s, 120 + (i % 3) * 300 + rnd.uniform(-30, 30), 120 + (i // 3) * 190 + rnd.uniform(-20, 20),
                  rnd.uniform(70, 100), i)
    p.drawn(1, 900, 600, crumbs, 80, 580, name="drawn-crumbs")
    p.label(1, "one crumb, one aggregate", 600, 1160, w=280)
    p.arrow(1, (640, 1150), (700, 1030), bend=0.25, seed=1)

    p.heading(2, "Level 1: Roots, fungi and bacteria glue them together.", y=200, size=80)
    def glued(dr, s):
        macro(dr, s, 420, 320, 240, 3)
        rnd = random.Random(4)
        for _ in range(40):
            x, y = 420 + rnd.uniform(-200, 200), 320 + rnd.uniform(-200, 200)
            dr.ellipse(((x - 5) * s, (y - 3) * s, (x + 5) * s, (y + 3) * s), fill=hexrgb("#E8C547") + (255,))
    p.drawn(2, 860, 660, glued, 110, 520, name="drawn-glued-crumb")
    p.label(2, "a root", 80, 520, w=200)
    p.arrow(2, (140, 570), (260, 640), bend=-0.25, seed=2)
    p.label(2, "fungal threads", 760, 560, w=240)
    p.arrow(2, (800, 640), (760, 760), bend=0.25, seed=3)
    p.label(2, "bacteria", 760, 1080, w=200)
    p.arrow(2, (780, 1075), (640, 960), bend=0.25, seed=4)

    p.heading(3, "Level 1: Crumbs leave spaces for air, water and roots.", y=200, size=80)
    def spaces(dr, s):
        rnd = random.Random(21)
        outline(dr, s, "rectangle", (10, 10, 870, 560), "#E7EEF0")
        for i in range(12):
            crumb(dr, s, 90 + (i % 4) * 230 + rnd.uniform(-20, 20), 110 + (i // 4) * 175 + rnd.uniform(-15, 15),
                  rnd.uniform(70, 88), 40 + i)
        dr.ellipse((420 * s, 240 * s, 470 * s, 290 * s), fill=hexrgb(WASH["water"]) + (255,), outline=LINE + (255,),
                   width=round(2 * s))
        pts = [(330 + 6 * math.sin(i / 2), 0 + i * 14) for i in range(40)]
        dr.line([(a * s, b * s) for a, b in pts], fill=hexrgb(WASH["root"]) + (255,), width=round(10 * s))
    p.drawn(3, 880, 570, spaces, 100, 540, name="drawn-pores")
    p.label(3, "air", 90, 1150, w=120)
    p.arrow(3, (130, 1145), (190, 1000), bend=-0.2, seed=5)
    p.label(3, "water", 600, 1140, w=160)
    p.arrow(3, (620, 1135), (560, 830), bend=0.2, seed=6)
    p.label(3, "a root", 280, 1150, w=160)
    p.arrow(3, (330, 1145), (440, 1060), bend=-0.2, seed=7)

    p.heading(4, "Level 2: Microaggregates are bound by persistent organic compounds and bacterial glues.", y=200,
              size=74, h=380)
    def micro_agg(dr, s):
        rnd = random.Random(8)
        dr.ellipse((60 * s, 20 * s, 620 * s, 580 * s), fill=hexrgb("#FBF8F1") + (255,), outline=LINE + (255,),
                   width=round(3 * s))
        for _ in range(26):
            x, y = 340 + rnd.uniform(-170, 170), 300 + rnd.uniform(-170, 170)
            outline(dr, s, "ellipse", (x - 40, y - 26, x + 40, y + 26), "#B9A58C", width=2)
        for _ in range(18):
            x, y = 340 + rnd.uniform(-150, 150), 300 + rnd.uniform(-150, 150)
            dr.ellipse(((x - 28) * s, (y - 18) * s, (x + 28) * s, (y + 18) * s), fill=(92, 70, 54, 150))
        for _ in range(16):
            x, y = 340 + rnd.uniform(-160, 160), 300 + rnd.uniform(-160, 160)
            dr.ellipse(((x - 7) * s, (y - 4) * s, (x + 7) * s, (y + 4) * s), fill=hexrgb("#E8C547") + (255,),
                       outline=LINE + (255,), width=round(1 * s))
    p.drawn(4, 680, 600, micro_agg, 200, 560, name="drawn-microaggregate")
    p.label(4, "mineral particles", 60, 600, w=220)
    p.arrow(4, (130, 680), (380, 760), bend=-0.25, seed=8)
    p.label(4, "organic compounds", 800, 600, w=220)
    p.arrow(4, (830, 690), (640, 800), bend=0.25, seed=9)
    p.label(4, "bacteria and their glues", 60, 1120, w=300)
    p.arrow(4, (200, 1115), (420, 1000), bend=0.25, seed=10)

    p.heading(5, "Level 2: Macroaggregates are held by roots and fungal hyphae, so they break down when tillage cuts "
              "those networks.", y=200, size=70, h=420)
    p.drawn(5, 900, 560, lambda dr, s: macro(dr, s, 450, 290, 220, 12, cut=True), 90, 640, name="drawn-macroaggregate")
    p.label(5, "tillage cuts here", 760, 1120, w=240)
    p.arrow(5, (800, 1115), (760, 930), bend=0.25, seed=11)
    p.label(5, "made of microaggregates", 70, 1120, w=320)
    p.arrow(5, (200, 1115), (420, 1000), bend=-0.25, seed=12)

    p.heading(6, "Source: Tisdall and Oades, 1982.", y=200, size=84)
    p.body(6, "Tisdall, J. M. and Oades, J. M. (1982). Organic matter and water-stable aggregates in soils. "
              "Journal of Soil Science 33: 141–163.", 420, size=36, w=860)
    p.drawn(6, 600, 480, lambda dr, s: macro(dr, s, 300, 240, 180, 5), 240, 660, name="drawn-aggregate")
    for k in range(7):
        p.logo(k)


# ================================================================== Myth vs mechanism: humus
@post("pl20261228", "2026-12-28", "myth-humus-v1", 6, LGREEN)
def humus(p):
    p.heading(0, "Myth: “Humus is a special, stable substance in soil.”", y=110, size=88)
    def blob(dr, s):
        rnd = random.Random(2)
        pts = [(300 + 230 * (0.8 + rnd.uniform(0, 0.25)) * math.cos(a), 280 + 200 * (0.8 + rnd.uniform(0, 0.25)) *
                math.sin(a)) for a in [i * 6.283 / 30 for i in range(30)]]
        poly(dr, s, pts, "#5A4334")
    p.drawn(0, 600, 560, blob, 240, 560, name="drawn-humus-blob")
    p.label(0, "the textbook picture", 700, 1100, w=260)
    p.arrow(0, (720, 1095), (700, 980), bend=0.25, seed=1)

    p.heading(1, "For a century, textbooks described humic substances as large, unique molecules.", y=110, size=78)
    def book(dr, s):
        poly(dr, s, [(40, 80), (420, 40), (420, 520), (40, 560)], "#FBF8F1")
        poly(dr, s, [(420, 40), (800, 80), (800, 560), (420, 520)], "#FBF8F1")
        rnd = random.Random(3)
        nodes = [(560 + rnd.uniform(-90, 90), 280 + rnd.uniform(-130, 130)) for _ in range(16)]
        for i, a in enumerate(nodes):
            b = nodes[(i * 5 + 3) % len(nodes)]
            dr.line((a[0] * s, a[1] * s, b[0] * s, b[1] * s), fill=LINE + (220,), width=round(3 * s))
        for x, y in nodes:
            outline(dr, s, "ellipse", (x - 12, y - 12, x + 12, y + 12), "#8A6A55", width=2)
        for j in range(8):
            dr.line((90 * s, (140 + j * 44) * s, 370 * s, (130 + j * 44) * s), fill=LINE + (110,), width=round(3 * s))
    p.drawn(1, 840, 600, book, 120, 560, name="drawn-textbook")
    p.label(1, "a giant “humic molecule”", 620, 1170, w=330)

    p.heading(2, "Modern imaging found little of that in intact soil. Much of it came from the harsh extraction method.",
              y=110, size=72, h=460)
    def flask(dr, s):
        poly(dr, s, [(250, 40), (370, 40), (370, 220), (560, 520), (60, 520), (250, 220)], "#E7EEF0")
        poly(dr, s, [(160, 380), (460, 380), (560, 520), (60, 520)], "#3D2B22")
        for i in range(6):
            dr.ellipse(((230 + i * 30) * s, (340 - i * 18) * s, (244 + i * 30) * s, (354 - i * 18) * s),
                       outline=LINE + (200,), width=round(2 * s))
    p.drawn(2, 620, 560, flask, 230, 600, name="drawn-flask")
    p.label(2, "strong alkali pulls out dark extracts", 60, 640, w=260)
    p.arrow(2, (150, 780), (380, 1050), bend=-0.25, seed=2)

    p.heading(3, "The current view: organic matter is a continuum of compounds being broken down by microbes.",
              y=110, size=74, h=460)
    def continuum(dr, s):
        leaf_shape(dr, s, 120, 220, 200, -0.5, WASH["leaf2"])
        rnd = random.Random(5)
        for i in range(5):
            leaf_shape(dr, s, 330 + rnd.uniform(-30, 30), 150 + i * 50, 60, rnd.uniform(0, 6), WASH["leaf2"])
        for i in range(14):
            x, y = 520 + rnd.uniform(-40, 40), 120 + rnd.uniform(0, 220)
            outline(dr, s, "ellipse", (x - 10, y - 8, x + 10, y + 8), "#B77B45", width=1.6)
        for i in range(40):
            x, y = 700 + rnd.uniform(-50, 50), 100 + rnd.uniform(0, 260)
            dr.ellipse(((x - 4) * s, (y - 4) * s, (x + 4) * s, (y + 4) * s), fill=hexrgb("#8A5A32") + (255,))
        dr.line((40 * s, 420 * s, 820 * s, 420 * s), fill=LINE + (255,), width=round(3 * s))
        poly(dr, s, [(820, 405), (850, 420), (820, 435)], "#4F3433")
    p.drawn(3, 880, 470, continuum, 100, 600, name="drawn-continuum")
    p.label(3, "a leaf", 110, 1100, w=200)
    p.label(3, "smaller and smaller pieces, eaten by microbes", 380, 1100, w=440)

    p.heading(4, "Carbon stays in soil mainly when it's protected in aggregates or bound to minerals.", y=110, size=78)
    def protected(dr, s):
        crumb(dr, s, 220, 260, 200, 9)
        rnd = random.Random(6)
        for _ in range(8):
            x, y = 220 + rnd.uniform(-110, 110), 260 + rnd.uniform(-110, 110)
            dr.ellipse(((x - 9) * s, (y - 9) * s, (x + 9) * s, (y + 9) * s), fill=hexrgb("#2F1E14") + (255,))
        poly(dr, s, [(520, 120), (800, 160), (760, 420), (500, 380)], "#C9BFB0")
        for _ in range(14):
            x, y = 520 + rnd.uniform(0, 250), 150 + rnd.uniform(0, 250)
            if 500 < x < 790:
                dr.ellipse(((x - 8) * s, (y - 8) * s, (x + 8) * s, (y + 8) * s), fill=hexrgb("#2F1E14") + (255,))
    p.drawn(4, 860, 500, protected, 110, 560, name="drawn-protected-carbon")
    p.label(4, "inside an aggregate", 110, 1100, w=300)
    p.label(4, "stuck to a mineral surface", 600, 1060, w=300)

    p.heading(5, "Microbes are part of the answer. Source on the slide.", y=110, size=84)
    p.body(5, "Lehmann, J. and Kleber, M. (2015). The contentious nature of soil organic matter. Nature 528: 60–68.",
           420, size=36, w=860)
    p.lens(5, f"{NEW}/Fungal hypha, 100x obj, Marco Trevisan.jpg", 330, 880, 460, center=(0.55, 0.5), zoom=1.6)
    p.label(5, "a fungal hypha at 100x, by Marco Trevisan", 600, 720, w=300)
    p.arrow(5, (640, 840), (480, 900), bend=0.25, seed=3)
    for k in range(6):
        p.logo(k)


# ================================================================== globe (Natural Earth 1:110m land, public domain)
_LAND = None


def land_mask():
    global _LAND
    if _LAND is None:
        import numpy as np
        geo = json.load(open("/home/user/photos/ne/land.geojson"))
        m = Image.new("L", (2048, 1024), 0)
        dr = ImageDraw.Draw(m)
        for f in geo["features"]:
            g = f["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            for pg in polys:
                for i, ring in enumerate(pg):
                    pts = [((lon + 180) / 360 * 2048, (90 - lat) / 180 * 1024) for lon, lat in ring]
                    dr.polygon(pts, fill=0 if i else 255)
        _LAND = np.asarray(m) > 127
    return _LAND


def globe(dia, lon0=-25, lat0=12, pins=(), sea="#CFE0E3", land="#7FA36B", pin="#B23A2E"):
    """A flat drawn globe (orthographic) with an even dark outline and optional pins [(lat, lon)]."""
    import numpy as np
    from PIL import ImageFilter
    mask = land_mask()
    S = 2
    n = dia * S
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float64)
    x = (xx - n / 2) / (n / 2)
    y = -(yy - n / 2) / (n / 2)
    rho = np.sqrt(x * x + y * y)
    inside = rho <= 1
    c = np.arcsin(np.clip(rho, 0, 1))
    la0, lo0 = math.radians(lat0), math.radians(lon0)
    with np.errstate(invalid="ignore", divide="ignore"):
        lat = np.arcsin(np.cos(c) * math.sin(la0) + np.where(rho > 0, y * np.sin(c) * math.cos(la0) / rho, 0))
        lon = lo0 + np.arctan2(x * np.sin(c), rho * np.cos(c) * math.cos(la0) - y * np.sin(c) * math.sin(la0))
    lon = (np.degrees(lon) + 180) % 360
    lat = np.degrees(lat)
    mx = np.clip((lon / 360 * 2048).astype(int), 0, 2047)
    my = np.clip(((90 - lat) / 180 * 1024).astype(int), 0, 1023)
    is_land = mask[my, mx] & inside
    rgb = np.zeros((n, n, 4), np.uint8)
    rgb[inside] = hexrgb(sea) + (255,)
    rgb[is_land] = hexrgb(land) + (255,)
    im = Image.fromarray(rgb, "RGBA")
    edge = Image.fromarray((is_land * 255).astype(np.uint8))
    edge = Image.fromarray(((np.asarray(edge.filter(ImageFilter.MaxFilter(5))) > 0) & ~is_land & inside).astype(np.uint8) * 255)
    ink = Image.new("RGBA", (n, n), LINE + (0,))
    ink.putalpha(edge.point(lambda v: 200 if v else 0))
    im.alpha_composite(ink)
    dr = ImageDraw.Draw(im)
    dr.ellipse((2, 2, n - 3, n - 3), outline=LINE + (255,), width=3 * S)
    for plat, plon in pins:
        a, b = math.radians(plat), math.radians(plon) - lo0
        cosc = math.sin(la0) * math.sin(a) + math.cos(la0) * math.cos(a) * math.cos(b)
        if cosc < 0:
            continue
        px = math.cos(a) * math.sin(b)
        py = math.cos(la0) * math.sin(a) - math.sin(la0) * math.cos(a) * math.cos(b)
        cx, cy = n / 2 + px * n / 2, n / 2 - py * n / 2
        r = 11 * S
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=hexrgb(pin) + (255,), outline=(255, 255, 255, 255),
                   width=3 * S)
    return im.resize((dia, dia), Image.LANCZOS)


def placeholder(w, h, text="PHOTO"):
    """A clearly labelled empty frame for a photo still to come."""
    def fn(dr, s):
        dr.rectangle((0, 0, w * s, h * s), fill=(255, 255, 255, 120))
        for i in range(0, w + h, 40):
            dr.line((i * s, 0, (i - h) * s, h * s), fill=LINE + (40,), width=round(2 * s))
    return draw_layer(w, h, fn)


# ================================================================== World Soil Day
GRADS = [  # (slide text, pin, photo or None) - a photo only where it really shows that person
    ("Boubacar, Guinea. Coffee grown in a syntropic agroforest.", (10.4, -11.0), "boubacar"),
    ("Christina, Tennessee. From advertising to a soil business.", (35.05, -85.3), None),
    ("Ibrahim, Turkey. More than 80 growers going regenerative.", (39.0, 35.0), None),
    ("Arthur, Brazil. A prize-winning farm school.", (-14.2, -51.9), None),
    ("Joseph, Kenya. Teaching his whole community.", (0.0, 37.9), None),
]
BOUBACAR = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles", "d02-w1.jpg")


@post("pl20261205", "2026-12-05", "world-soil-day-v1", 7, LGREEN)
def world_soil_day(p):
    pins = [g[1] for g in GRADS]
    p.heading(0, "Happy World Soil Day. Here's a year of living soil.", y=110, size=88)
    p.put(0, "globe", globe(660, lon0=-18, lat0=14, pins=pins), 210, 470)
    p.label(0, "World Soil Day 2026: Our future is rooted in soil", 90, 1170, w=640, size=30)

    boub = Image.open(BOUBACAR).convert("RGB")
    boub = boub.crop((0, 0, round(boub.width * 0.86), boub.height))  # leave out the old logo corner
    for k, (text, pin, photo) in enumerate(GRADS, start=1):
        p.heading(k, text, y=110, size=80)
        top = 470
        if photo == "boubacar":
            p.photo(k, boub, 90, top, 900, 560, fx=0.35, fy=0.3, seed=k)
        else:
            x, y, w, h = p.put(k, "photo-placeholder", placeholder(900, 560), 90, top)
            p.drawn(k, 920, 580, lambda dr, s: dr.rectangle((10 * s, 10 * s, 910 * s, 570 * s), outline=LINE + (255,),
                                                            width=round(3 * s)), 80, top - 10, name="placeholder-frame")
            p.label(k, "PHOTO: add a photo of " + text.split(",")[0] + " from their own post", 150, top + 240,
                    w=780, size=34, align="center")
        p.put(k, "globe", globe(230, lon0=pin[1], lat0=pin[0], pins=[pin]), 90, 1080)
    p.heading(6, "Thank you for protecting the ground we all stand on.", y=110, size=88)
    p.put(6, "globe", globe(620, lon0=-18, lat0=14, pins=pins), 230, 520)
    for k in range(7):
        p.logo(k)


# ================================================================== templates still waiting for content
def eyebrow(p, k, text, color=None):
    p.d.text(k, "eyebrow", text, 92, 70, 880, 50, 26, kind="mont-medium", italic=False,
             color=color or p.t.label, lh=1.2, track=3)


def photo_space(p, k, x, y, w, h, what):
    p.put(k, "photo-placeholder", placeholder(w, h), x, y)
    p.drawn(k, w + 20, h + 20, lambda dr, s: dr.rectangle((10 * s, 10 * s, (w + 10) * s, (h + 10) * s),
                                                          outline=hexrgb(p.t.label) + (255,), width=round(3 * s)),
            x - 10, y - 10, name="placeholder-frame")
    p.label(k, "PHOTO: " + what, x + 40, y + h / 2 - 30, w=w - 80, size=32, align="center")


@post("pl20261206", "2026-12-06", "field-notes-02-v1", 6, DEEP)
def field_notes_2(p):
    texts = ["Trial name, place and season.", "The question they tested.", "The method in 3 lines.",
             "The result, one big number.", "What surprised them, including what didn't work.", "Who ran it."]
    for k, t in enumerate(texts):
        eyebrow(p, k, "FIELD NOTES No. 02")
        p.heading(k, t, y=150, size=84)
        p.logo(k)
    photo_space(p, 0, 90, 480, 900, 600, "the trial plot, from the graduate")
    p.drawn(3, 900, 420, lambda dr, s: outline(dr, s, "rounded_rectangle", (0, 0, 900, 420), "#2E4A2A",
                                               radius=round(30 * s)), 90, 520, name="number-box")
    p.label(3, "[the number]", 90, 680, w=900, size=64, align="center")
    photo_space(p, 5, 90, 440, 600, 600, "the graduate who ran the trial")


@post("pl20261209", "2026-12-09", "free-webinar-december-v1", 5, CREAM)
def webinar_dec(p):
    p.heading(0, "FREE WEBINAR", y=140, size=120)
    p.lens(0, f"{NEW}/Bacterial-feeding nematode, 40x obj, Casey Williams.jpg", 540, 800, 620, center=(0.5, 0.45),
           zoom=1.6)
    p.small(0, "Micrograph: Casey Williams, 40x objective", y=1270)
    p.heading(1, "[Webinar title]", y=140, size=96)
    p.heading(2, "[Date and time, three time zones]", y=140, size=96)
    p.heading(3, "[Host name]", y=140, size=96)
    photo_space(p, 3, 240, 420, 600, 640, "the host's headshot")
    p.heading(4, "Free. Link in bio.", y=140, size=110)
    p.cut(4, f"{FLOWERS}/norfolk-common-poppy.png", 160, 640, h=480)
    p.cut(4, f"{FLOWERS}/tamil-nadu-marigold.png", 520, 760, h=360)
    for k in range(5):
        p.logo(k)


@post("pl20261218", "2026-12-18", "fun-soil-news-december-v1", 6, TAN)
def fun_news_dec(p):
    p.heading(0, "Fun Soil News: December 2026.", y=150, size=100)
    p.cut(0, f"{FLOWERS}/costa-rica-heliconia.png", 90, 640, h=560)
    p.cut(0, f"{FLOWERS}/costa-rica-hibiscus.png", 380, 860, h=300)
    p.cut(0, f"{FLOWERS}/costa-rica-torch-ginger.png", 620, 600, h=560)
    for k in range(1, 6):
        p.drawn(k, W, 110, lambda dr, s: dr.rectangle((0, 0, W * s, 110 * s), fill=hexrgb("#156826") + (255,)),
                0, 0, name="top-bar")
        p.d.text(k, "eyebrow", "FUN SOIL NEWS · DECEMBER 2026", 92, 40, 880, 50, 26, kind="mont-medium",
                 italic=False, color=CREAMT, lh=1.2, track=2)
        p.heading(k, f"Story {k}. Country in big type, one sentence, source.", y=200, size=80)
        p.cut(k, f"{FLOWERS}/" + ["tamil-nadu-marigold", "costa-rica-hibiscus", "costa-rica-poro-flower",
                                  "tamil-nadu-pink-lotus", "santa-fe-globemallow"][k - 1] + ".png", 700, 820, h=300)
    for k in range(6):
        p.logo(k)


@post("pl20261223", "2026-12-23", "partner-share-december-v1", 3, TAN)
def partner_dec(p):
    p.heading(0, "FROM OUR PARTNERS", y=140, size=110)
    photo_space(p, 0, 140, 470, 800, 640, "the partner's own post")
    p.heading(1, "[Partner name]", y=140, size=100)
    p.heading(2, "[One line on their work]", y=140, size=100)
    p.cut(1, f"{SOILC}/fern-fiddlehead.png", 640, 700, h=420)
    p.cut(2, f"{SOILC}/moss-clump.png", 520, 880, w=360)
    for k in range(3):
        p.logo(k)


@post("pl20261230", "2026-12-30", "soil-regenerators-sumatra-v1", 5, SAGE)
def sumatra(p):
    texts = ["Soil Regenerators in the wild. [Name], Simalungun Regency, Sumatra, Indonesia",
             "Farming the way their parents did. Then they looked under a microscope.",
             "Regenerative compost, checked under the microscope.",
             "Fields mapped, companion plants and ground cover planted.",
             "“It has enriched the people, plants and animals in the Simalungun regency where I call home.”"]
    whats = ["the farmer, from their own photos", "the farm, from the farmer's photos",
             "their compost or microscope, from their photos", "their fields and ground cover, from their photos",
             "the farmer, from their own photos"]
    for k, t in enumerate(texts):
        bottom = p.heading(k, t, y=110, size=76 if k in (0, 4) else 80)
        photo_space(p, k, 90, max(470, bottom + 60), 900, 560, whats[k])
        p.logo(k)
    p.put(0, "globe", globe(220, lon0=99.0, lat0=2.9, pins=[(2.9, 99.0)]), 90, 1100)


# ================================================================== Myth vs mechanism: the wood wide web
def tree_roots(dr, s, cx, ground, h, seed, trunk="#7A5B44", crown="#7FA36B", small=False):
    rnd = random.Random(seed)
    tw = 26 if small else 46
    poly(dr, s, [(cx - tw / 2, ground), (cx - tw / 2 + 6, ground - h * 0.45), (cx + tw / 2 - 6, ground - h * 0.45),
                 (cx + tw / 2, ground)], trunk)
    r = h * (0.28 if small else 0.34)
    for dx, dy, rr in ((0, -h * 0.62, r), (-r * 0.6, -h * 0.5, r * 0.75), (r * 0.6, -h * 0.5, r * 0.75)):
        outline(dr, s, "ellipse", (cx + dx - rr, ground + dy - rr * 0.8, cx + dx + rr, ground + dy + rr * 0.8), crown)
    for i in range(7 if not small else 4):
        ang = math.pi / 2 + rnd.uniform(-1.1, 1.1)
        pts = [(cx, ground)]
        x, y = cx, ground
        for _ in range(16):
            ang += rnd.uniform(-0.2, 0.2)
            x += 12 * math.cos(ang)
            y += 12 * math.sin(ang)
            pts.append((x, y))
        dr.line([(a * s, b * s) for a, b in pts], fill=hexrgb("#E9DCC3") + (255,), width=round((7 if not small else 5) * s),
                joint="curve")


@post("pl20261116", "2026-11-16", "myth-wood-wide-web-v1", 6, CREAM)
def wood_wide_web(p):
    G = 330

    def forest(dr, s, links=True, solid_links=False):
        outline(dr, s, "rectangle", (0, G, 860, 580), WASH["soil"])
        tree_roots(dr, s, 230, G, 300, 1)
        tree_roots(dr, s, 690, G, 230, 2, small=True)
        if links:
            rnd = random.Random(4)
            for i in range(10):
                y = G + 60 + i * 22
                pts = [(300 + j * 30, y + 12 * math.sin(j / 2 + i) + rnd.uniform(-4, 4)) for j in range(13)]
                dr.line([(a * s, b * s) for a, b in pts], fill=(255, 255, 255, 230 if solid_links else 200),
                        width=round(2 * s))

    p.heading(0, "Myth: “Mother trees feed their seedlings through a fungal internet.”", y=110, size=84)
    p.drawn(0, 900, 600, forest, 110, 540, name="drawn-trees")

    p.heading(1, "Mycorrhizal fungi do connect the roots of different trees. That part is real.", y=110, size=80)
    p.drawn(1, 900, 600, forest, 110, 540, name="drawn-trees")
    p.label(1, "fungal threads between the roots", 110, 1170, w=560)
    p.arrow(1, (560, 1165), (520, 1060), bend=0.25, seed=1)

    p.heading(2, "But field evidence that trees send meaningful resources to each other through them is thin.",
              y=110, size=76, h=460)
    def unsure(dr, s):
        forest(dr, s)
        for x in (360, 470, 580):
            dr.text((x * s, (G + 110) * s), "?", fill=hexrgb(CREAMT) + (255,),
                    font=collage.font("fredoka", False, round(60 * s)))
    p.drawn(2, 900, 600, unsure, 110, 540, name="drawn-trees")

    p.heading(3, "A 2023 review found positive citation bias: papers cited the dramatic claims more than the data "
              "supported.", y=110, size=74, h=460)
    def citations(dr, s):
        outline(dr, s, "rectangle", (330, 60, 560, 340), "#FBF8F1")
        for j in range(6):
            dr.line((360 * s, (110 + j * 36) * s, 530 * s, (110 + j * 36) * s), fill=LINE + (120,), width=round(3 * s))
        rnd = random.Random(7)
        for i in range(12):
            a = i / 12 * 6.283
            x, y = 445 + 330 * math.cos(a), 200 + 170 * math.sin(a)
            outline(dr, s, "rectangle", (x - 40, y - 50, x + 40, y + 50), "#F4F1EA", width=2)
            dr.line(((x - 40 * math.cos(a)) * s, (y - 50 * math.sin(a)) * s, (445 + 115 * math.cos(a)) * s,
                     (200 + 140 * math.sin(a)) * s), fill=LINE + (110,), width=round(2 * s))
    p.drawn(3, 900, 420, citations, 90, 620, name="drawn-citations")
    p.label(3, "Karst et al. 2023, Nature Ecology and Evolution", 90, 1110, w=640, size=28)

    p.heading(4, "What is solid: mycorrhizal fungi trade nutrients and water for plant sugars, one plant at a time.",
              y=110, size=74, h=460)
    def trade(dr, s):
        pts = [(450 + 10 * math.sin(i / 3), i * 14) for i in range(46)]
        dr.line([(a * s, b * s) for a, b in pts], fill=hexrgb("#E9DCC3") + (255,), width=round(38 * s), joint="curve")
        dr.line([(a * s, b * s) for a, b in pts], fill=LINE + (255,), width=round(2 * s), joint="curve")
        for i in range(14):
            threads(dr, s, 450 + (18 if i % 2 else -18), 200 + i * 28, 0 if i % 2 else math.pi, 330, 30 + i,
                    color="#8A6A55", width=2.2)
    p.drawn(4, 900, 650, trade, 90, 560, name="drawn-root-tip")
    p.label(4, "sugars go to the fungus", 100, 620, w=280)
    p.arrow(4, (180, 700), (480, 780), bend=-0.2, seed=2)
    p.label(4, "nutrients and water come back", 700, 960, w=300)
    p.arrow(4, (720, 955), (590, 880), bend=0.25, seed=3)

    p.heading(5, "Real science is exciting enough. Source on the slide.", y=110, size=84)
    p.body(5, "Karst, J., Jones, M. D. and Hoeksema, J. D. (2023). Positive citation bias and overinterpreted results "
              "lead to misinformation on common mycorrhizal networks in forests. Nature Ecology and Evolution 7: "
              "501–511.", 440, size=34, w=860)
    p.drawn(5, 900, 380, lambda dr, s: tree_roots(dr, s, 450, 300, 280, 9), 90, 800, name="drawn-tree")
    for k in range(6):
        p.logo(k)


# ================================================================== Soil in numbers: a third degraded
def cause_icon(dr, s, kind, x, y, r=78):
    outline(dr, s, "ellipse", (x - r, y - r, x + r, y + r), "#F4F1EA")
    if kind == "erosion":
        poly(dr, s, [(x - 50, y + 10), (x - 10, y + 10), (x, y + 40), (x + 10, y + 10), (x + 50, y + 10), (x + 50, y + 40),
                     (x - 50, y + 40)], WASH["soil"])
        for i in range(4):
            dr.line(((x - 40 + i * 25) * s, (y - 45) * s, (x - 48 + i * 25) * s, (y - 15) * s),
                    fill=hexrgb("#6E9FB0") + (255,), width=round(4 * s))
    elif kind == "carbon":
        crumb(dr, s, x, y + 5, 45, 3, fill="#B9A58C", pores=False)
        dr.line(((x + 20) * s, (y - 50) * s, (x + 20) * s, (y - 10) * s), fill=LINE + (255,), width=round(4 * s))
        poly(dr, s, [(x + 8, y - 48), (x + 20, y - 62), (x + 32, y - 48)], "#4F3433")
    elif kind == "salt":
        rnd = random.Random(2)
        for _ in range(7):
            cx, cy = x + rnd.uniform(-40, 40), y + rnd.uniform(-35, 35)
            outline(dr, s, "rectangle", (cx - 9, cy - 9, cx + 9, cy + 9), "#FFFFFF", width=2)
    elif kind == "compaction":
        outline(dr, s, "rectangle", (x - 45, y + 5, x + 45, y + 40), WASH["clay"])
        for dx in (-25, 25):
            dr.line(((x + dx) * s, (y - 50) * s, (x + dx) * s, (y - 8) * s), fill=LINE + (255,), width=round(4 * s))
            poly(dr, s, [(x + dx - 10, y - 18), (x + dx, y - 4), (x + dx + 10, y - 18)], "#4F3433")
    elif kind == "acid":
        drop(dr, s, x, y + 18, 36, "#C9D96B")
    elif kind == "pollution":
        outline(dr, s, "rectangle", (x - 30, y - 30, x + 30, y + 40), "#9C978E")
        outline(dr, s, "ellipse", (x - 30, y - 42, x + 30, y - 18), "#B5B0A6")
        poly(dr, s, [(x + 30, y + 25), (x + 55, y + 45), (x + 25, y + 45)], "#3D2B22")


@post("pl20261214", "2026-12-14", "soil-in-numbers-degraded-v1", 4, DEEP)
def degraded(p):
    p.heading(0, "33% of the world's soils are moderately to highly degraded.", y=110, size=88)
    def pie(dr, s):
        box = (40, 40, 600, 600)
        dr.pieslice([v * s for v in box], -90, 30, fill=hexrgb("#C89B7B") + (255,), outline=hexrgb(CREAMT) + (255,),
                    width=round(4 * s))
        dr.pieslice([v * s for v in box], 30, 270, fill=hexrgb("#59A66C") + (255,), outline=hexrgb(CREAMT) + (255,),
                    width=round(4 * s))
    p.drawn(0, 640, 640, pie, 220, 500, name="drawn-pie")
    p.label(0, "one in three", 790, 560, w=220, size=34)
    p.arrow(0, (820, 610), (720, 700), bend=0.25, seed=1)
    p.small(0, "Source: FAO and ITPS (2015), Status of the World's Soil Resources", y=1170, w=640)

    p.heading(1, "The causes: erosion, loss of organic carbon, salinization, compaction, acidification and pollution.",
              y=110, size=74, h=460)
    kinds = ["erosion", "carbon", "salt", "compaction", "acid", "pollution"]
    names = ["erosion", "carbon loss", "salinization", "compaction", "acidification", "pollution"]
    def icons(dr, s):
        for i, kd in enumerate(kinds):
            cause_icon(dr, s, kd, 130 + (i % 3) * 300, 110 + (i // 3) * 270)
    p.drawn(1, 900, 520, icons, 90, 540, name="drawn-causes")
    for i, nm in enumerate(names):
        p.label(1, nm, 90 + (i % 3) * 300 - 30, 540 + 110 + (i // 3) * 270 + 90, w=300, size=28, align="center")

    p.heading(2, "Forming a few centimeters of new soil can take centuries.", y=110, size=88)
    def profile(dr, s):
        outline(dr, s, "rectangle", (40, 40, 520, 90), "#4A3426")
        outline(dr, s, "rectangle", (40, 90, 520, 300), "#9C7B5E")
        outline(dr, s, "rectangle", (40, 300, 520, 560), "#9C978E")
        rnd = random.Random(3)
        for _ in range(16):
            x, y, r = rnd.uniform(70, 490), rnd.uniform(330, 540), rnd.uniform(12, 30)
            outline(dr, s, "ellipse", (x - r, y - r * 0.7, x + r, y + r * 0.7), "#B5B0A6", width=2)
    p.drawn(2, 560, 600, profile, 120, 540, name="drawn-soil-profile")
    p.label(2, "a few centimeters of topsoil", 700, 520, w=300, size=31)
    p.arrow(2, (720, 600), (650, 610), bend=0.2, seed=2)
    p.label(2, "rock that weathers slowly", 700, 920, w=300, size=31)
    p.arrow(2, (720, 960), (650, 990), bend=0.2, seed=3)

    p.heading(3, "Restoring soil biology is one of the fastest ways to rebuild it.", y=110, size=88)
    p.lens(3, f"{NEW}/Fungal hypha, 100x obj, Marco Trevisan.jpg", 400, 800, 520, center=(0.55, 0.5), zoom=1.6)
    p.cut(3, f"{SOILC}/compost-white-fungal-threads.png", 640, 700, w=300)
    p.label(3, "a fungal hypha at 100x, by Marco Trevisan", 90, 1110, w=560, size=28)
    for k in range(4):
        p.logo(k)


# ================================================================== Do this weekend: worm bin in winter
WORM = f"{SOILC}/earthworm.png"
SCARF_AT, SCARF_ANG = (267, 100), 2.06


def scarf(dr, s, x, y, ang=-0.5, k=1.0):
    """A little knitted scarf: a wrapped band and two hanging tails, flat colours, one outline."""
    ca, sa = math.cos(ang), math.sin(ang)
    def rot(pts):
        return [(x + k * (px * ca - py * sa), y + k * (px * sa + py * ca)) for px, py in pts]
    poly(dr, s, rot([(-46, -16), (46, -16), (46, 16), (-46, 16)]), "#B23A2E")
    for i in (-24, 0, 24):
        a, b = rot([(i, -16), (i, 16)])
        dr.line((a[0] * s, a[1] * s, b[0] * s, b[1] * s), fill=hexrgb("#F4F1EA") + (255,), width=round(6 * s))
    tx, ty = rot([(30, 0)])[0]
    poly(dr, s, [(tx - 12 * k, ty), (tx + 8 * k, ty), (tx + 14 * k, ty + 80 * k), (tx - 6 * k, ty + 82 * k)], "#B23A2E")
    poly(dr, s, [(tx + 4 * k, ty + 4 * k), (tx + 22 * k, ty), (tx + 40 * k, ty + 70 * k), (tx + 22 * k, ty + 76 * k)],
         "#2E6B3A")


@post("pl20261212", "2026-12-12", "do-this-weekend-worm-bin-winter-v1", 5, CREAM)
def worm_winter(p):
    p.heading(0, "Your worms get cold too.", y=120, size=110)
    x, y, w, h = p.cut(0, WORM, 300, 480, h=640, name="earthworm")
    sc = 640 / 427
    hx, hy = SCARF_AT
    p.drawn(0, 400, 400, lambda dr, s: scarf(dr, s, 200, 200, ang=SCARF_ANG, k=1.8), x + hx * sc - 200,
            y + hy * sc - 200, name="drawn-scarf")
    p.label(0, "a red wiggler, ready for winter", 90, 1150, w=600)

    p.heading(1, "Red wigglers slow down below about 10°C and die if the bin freezes.", y=110, size=80)
    def thermo(dr, s):
        outline(dr, s, "rounded_rectangle", (120, 20, 200, 520), "#FFFFFF", radius=round(40 * s))
        outline(dr, s, "ellipse", (90, 480, 230, 620), "#B23A2E")
        dr.rectangle((145 * s, 300 * s, 175 * s, 540 * s), fill=hexrgb("#B23A2E") + (255,))
        for i in range(9):
            yy = 60 + i * 50
            dr.line((200 * s, yy * s, 230 * s, yy * s), fill=LINE + (255,), width=round(3 * s))
        dr.line((90 * s, 300 * s, 260 * s, 300 * s), fill=hexrgb("#2E6B3A") + (255,), width=round(5 * s))
    p.drawn(1, 300, 640, thermo, 200, 520, name="drawn-thermometer")
    p.cut(1, WORM, 560, 700, h=380, name="earthworm")
    p.label(1, "about 10°C: worms slow down", 520, 560, w=360)
    p.arrow(1, (540, 640), (470, 815), bend=0.25, seed=1)

    p.heading(2, "Move the bin to a shed, garage or basement.", y=110, size=88)
    def shed(dr, s):
        poly(dr, s, [(40, 260), (420, 60), (800, 260)], "#8A6A55")
        outline(dr, s, "rectangle", (90, 260, 750, 620), "#C9B79C")
        outline(dr, s, "rectangle", (330, 380, 520, 620), "#6E5543")
        outline(dr, s, "rounded_rectangle", (560, 470, 720, 620), "#2E6B3A", radius=round(12 * s))
        outline(dr, s, "rectangle", (550, 450, 730, 485), "#24502D")
    p.drawn(2, 840, 640, shed, 120, 520, name="drawn-shed")
    p.label(2, "the worm bin, out of the frost", 560, 1180, w=300)
    p.arrow(2, (640, 1175), (750, 1110), bend=-0.25, seed=2)

    p.heading(3, "Add extra shredded cardboard as insulation, and feed less.", y=110, size=88)
    def cardboard(dr, s):
        rnd = random.Random(5)
        outline(dr, s, "rounded_rectangle", (60, 320, 840, 640), "#2E6B3A", radius=round(16 * s))
        for _ in range(60):
            x, y = rnd.uniform(90, 800), rnd.uniform(200, 360)
            a = rnd.uniform(-0.6, 0.6)
            pts = [(x, y), (x + 70 * math.cos(a), y + 70 * math.sin(a)), (x + 70 * math.cos(a) - 8, y + 70 * math.sin(a) + 14),
                   (x - 8, y + 14)]
            poly(dr, s, pts, rnd.choice(("#C8A675", "#B8935F", "#D7B98A")), width=1.6)
    p.drawn(3, 900, 660, cardboard, 90, 480, name="drawn-cardboard")
    p.label(3, "a thick layer of shredded cardboard", 90, 1160, w=600)

    p.heading(4, "Keep the bedding damp, like a wrung-out sponge.", y=110, size=88)
    def sponge(dr, s):
        rnd = random.Random(8)
        poly(dr, s, [(120, 220), (560, 160), (620, 360), (170, 430)], "#E8C547")
        for _ in range(26):
            x, y = rnd.uniform(200, 560), rnd.uniform(220, 380)
            dr.ellipse(((x - 9) * s, (y - 7) * s, (x + 9) * s, (y + 7) * s), fill=hexrgb("#C9A52F") + (255,))
        for i in range(3):
            drop(dr, s, 300 + i * 90, 560 + (i % 2) * 40, 18, WASH["water"])
    p.drawn(4, 760, 680, sponge, 160, 460, name="drawn-sponge")
    p.label(4, "a few drops, not a stream", 600, 1100, w=280)
    p.arrow(4, (640, 1095), (560, 1060), bend=0.2, seed=4)
    for k in range(5):
        p.logo(k)


# ================================================================== more templates
def field_notes(p, number):
    texts = ["Trial name, place and season.", "The question they tested.", "The method in 3 lines.",
             "The result, one big number.", "What surprised them, including what didn't work.", "Who ran it."]
    for k, t in enumerate(texts):
        eyebrow(p, k, f"FIELD NOTES No. {number}")
        p.heading(k, t, y=150, size=84)
        p.logo(k)
    photo_space(p, 0, 90, 480, 900, 600, "the trial plot, from the graduate")
    p.drawn(3, 900, 420, lambda dr, s: outline(dr, s, "rounded_rectangle", (0, 0, 900, 420),
                                               "#2E4A2A" if p.t.bg == DEEP else "#FBF8F1", radius=round(30 * s)),
            90, 520, name="number-box")
    p.label(3, "[the number]", 90, 680, w=900, size=64, align="center")
    photo_space(p, 5, 90, 440, 600, 600, "the graduate who ran the trial")


@post("pl20261107", "2026-11-07", "field-notes-01-v1", 6, CREAM)
def field_notes_1(p):
    field_notes(p, "01")


@post("pl20261125", "2026-11-25", "mentor-spotlight-november-v1", 2, SAGE)
def mentor_nov(p):
    p.heading(0, "Meet our mentors. [Name], [role].", y=110, size=96)
    photo_space(p, 0, 190, 460, 700, 700, "the mentor's website headshot")
    p.heading(1, "[Their one line of advice, in their words.]", y=110, size=96)
    p.cut(1, f"{FLOWERS}/norfolk-common-poppy.png", 200, 640, h=520)
    p.cut(1, f"{SOILC}/fern-fiddlehead.png", 560, 820, h=340)
    for k in range(2):
        p.logo(k)


@post("pl20261127", "2026-11-27", "fun-soil-news-november-v1", 6, LGREEN)
def fun_news_nov(p):
    p.heading(0, "Fun Soil News: November 2026.", y=150, size=100)
    p.cut(0, f"{FLOWERS}/tamil-nadu-marigold.png", 120, 700, h=420)
    p.cut(0, f"{FLOWERS}/norfolk-common-poppy.png", 420, 620, h=540)
    p.cut(0, f"{FLOWERS}/santa-fe-globemallow.png", 700, 720, h=420)
    flowers = ["costa-rica-hibiscus", "tamil-nadu-jasmine", "costa-rica-poro-flower", "tamil-nadu-marigold",
               "santa-fe-chamisa"]
    for k in range(1, 6):
        p.drawn(k, W, 110, lambda dr, s: dr.rectangle((0, 0, W * s, 110 * s), fill=hexrgb("#156826") + (255,)),
                0, 0, name="top-bar")
        p.d.text(k, "eyebrow", "FUN SOIL NEWS · NOVEMBER 2026", 92, 40, 880, 50, 26, kind="mont-medium",
                 italic=False, color=CREAMT, lh=1.2, track=2)
        p.heading(k, f"Story {k}. Country in big type, one sentence, source.", y=200, size=80)
        p.cut(k, f"{FLOWERS}/{flowers[k - 1]}.png", 700, 820, h=300)
    for k in range(6):
        p.logo(k)


@post("d10", "2026-10-15", "what-does-regenerative-mean-v1", 1, TAN)
def regenerative(p):
    p.heading(0, "What does “regenerative” actually mean, and who gets to decide?", y=120, size=92)
    p.cut(0, f"{SOILC}/dark-soil-clump.png", 140, 760, w=420)
    p.cut(0, f"{SOILC}/fern-fiddlehead.png", 560, 640, h=520)
    p.logo(0)


# ================================================================== Read the drop: nematode mouthparts (Reel)
NEMS = [  # (slide text, file, lens center, zoom, short label, credit)
    ("Bacterial feeder: open, tube-shaped mouth", f"{CC}/bacterial-feeding-nematode-2-crop.jpg", (0.48, 0.42), 1.35,
     "bacterial feeder", "Tandingan De Ley et al. 2023, PLOS ONE"),
    ("Fungal feeder: a thin stylet to pierce hyphae", f"{CC}/fungal-feeding-nematode-1-crop.jpg", (0.47, 0.45), 1.0,
     "fungal feeder", "Munawar et al. 2024, Microorganisms"),
    ("Root feeder: a heavy stylet to pierce roots", f"{CC}/plant-parasitic-nematode-1-crop.jpg", (0.5, 0.29), 1.0,
     "root feeder", "Handoo et al. 2021, Plants"),
    ("Predator: teeth or a wide mouth", f"{CC}/predatory-nematode-2-crop.jpg", (0.44, 0.5), 1.15,
     "predator", "Altash et al. 2024, ZooKeys"),
]
NEM_POINT = [("the open mouth tube", (0.5, 0.3)), ("the thin stylet", (0.5, 0.45)), ("the heavy stylet with knobs", (0.47, 0.42)),
             ("a wide mouth with a tooth", (0.55, 0.42))]


@post("pl20261102", "2026-11-02", "read-the-drop-nematode-mouths-v1", 5, DEEP, reel=True)
def nematode_mouths(p):
    h = p.h
    mid = h * 0.5
    for k, (text, src, c, z, short, cred) in enumerate(NEMS):
        p.heading(k, text, y=120, size=86)
        dia = 580
        x, y, w, hh = p.lens(k, src, 540, mid, dia, center=c, zoom=z)
        lab, (fx, fy) = NEM_POINT[k]
        p.label(k, lab, 760, y - 40, w=280)
        p.arrow(k, (800, y + 40), (x + w * fx + 30, y + hh * fy), bend=0.3, seed=k + 1)
        row_y = y + hh + 30
        for j, (_, s2, c2, z2, _, _) in enumerate(NEMS):
            cx = 150 + j * 170
            p.lens(k, s2, cx, row_y + 75, 140 if j != k else 160, center=c2, zoom=z2, name=f"small-{j + 1}")
            if j == k:
                p.drawn(k, 190, 190, lambda dr, s: dr.ellipse((4 * s, 4 * s, 186 * s, 186 * s),
                                                               outline=hexrgb(CREAMT) + (255,), width=round(5 * s)),
                        cx - 95, row_y - 20, name="ring")
        p.small(k, f"Micrograph: {cred}, CC BY 4.0 (cropped)", y=h - 70, w=640)
    p.heading(4, "Read the mouth, know the job.", y=120, size=96)
    top = mid - 330
    for j, (_, s2, c2, z2, short, _) in enumerate(NEMS):
        cx, cy = 270 + (j % 2) * 420, top + 150 + (j // 2) * 390
        p.lens(4, s2, cx, cy, 290, center=c2, zoom=z2)
        p.label(4, short, cx - 160, cy + 158, w=320, align="center")
    p.small(4, "Micrographs: Tandingan De Ley 2023, Munawar 2024, Handoo 2021, Altash 2024; CC BY 4.0", y=h - 70, w=680)
    for k in range(5):
        p.logo(k)


# ================================================================== Read the drop: hyphae or debris? (Reel)
HYPHA = f"{CC}/fungal-hypha-1.jpg"
DEBRIS = f"{CC}/organic-matter-debris-1.jpg"
ACTINO = f"{CC}/actinomycetes-1-crop.jpg"


@post("pl20261221", "2026-12-21", "read-the-drop-hyphae-or-debris-v1", 4, DEEP, reel=True)
def hyphae_or_debris(p):
    h = p.h
    mid = h * 0.53
    dia = 600

    def pt(box, fx, fy):
        x, y, w, hh = box
        return (x + w * fx, y + hh * fy)

    hb = p.heading(0, "Fungal hypha: same width along its whole length.", y=120, size=86)
    cy = max(mid, hb + 120 + dia / 2)
    b = p.lens(0, HYPHA, 540, cy, dia, center=(0.45, 0.35), zoom=1.2)
    p.label(0, "same width here", 80, b[1] - 60, w=300)
    p.arrow(0, (200, b[1] + 10), pt(b, 0.22, 0.37), bend=-0.25, seed=1)
    p.label(0, "and here", 800, b[1] - 60, w=220)
    p.arrow(0, (840, b[1] + 10), pt(b, 0.8, 0.37), bend=0.25, seed=2)
    p.small(0, "Micrograph: Gondal, Rauf and Naz 2019, Scientific Reports, CC BY 4.0 (cropped)", y=h - 70, w=680)

    hb = p.heading(1, "Parallel walls, often branching.", y=120, size=92)
    cy = max(mid, hb + 120 + dia / 2)
    b = p.lens(1, HYPHA, 540, cy, dia, center=(0.45, 0.35), zoom=1.2)
    p.label(1, "a branch", 790, b[1] + b[3] - 140, w=220)
    p.arrow(1, (820, b[1] + b[3] - 150), pt(b, 0.47, 0.3), bend=0.3, seed=3)
    p.label(1, "parallel walls", 70, b[1] + b[3] - 110, w=260)
    p.arrow(1, (150, b[1] + b[3] - 120), pt(b, 0.44, 0.62), bend=-0.3, seed=4)
    p.small(1, "Micrograph: Gondal, Rauf and Naz 2019, Scientific Reports, CC BY 4.0 (cropped)", y=h - 70, w=680)

    hb = p.heading(2, "Debris: irregular edges, changing width.", y=120, size=92)
    cy = max(mid, hb + 120 + dia / 2)
    b = p.lens(2, DEBRIS, 540, cy, dia, center=(0.45, 0.55), zoom=1.3)
    p.label(2, "debris", 850, b[1] + b[3] - 120, w=180)
    p.arrow(2, (880, b[1] + b[3] - 125), pt(b, 0.66, 0.7), bend=0.3, seed=5)
    p.label(2, "a hypha, for comparison", 60, b[1] - 70, w=300)
    p.arrow(2, (160, b[1] + 20), pt(b, 0.4, 0.5), bend=-0.25, seed=6)
    p.small(2, "Photo: Matthew Rozanoff / iNaturalist, CC BY 4.0 (cropped)", y=h - 70, w=680)

    hb = p.heading(3, "Actinomycetes: much thinner threads.", y=120, size=92)
    cy = max(mid, hb + 120 + dia / 2)
    b = p.lens(3, ACTINO, 540, cy, dia, center=(0.6, 0.5), zoom=1.0)
    p.label(3, "thin, branching threads", 760, b[1] - 60, w=280)
    p.arrow(3, (820, b[1] + 20), pt(b, 0.62, 0.35), bend=0.25, seed=7)
    p.small(3, "Micrograph: Du et al. 2025, PLOS ONE, CC BY 4.0 (cropped)", y=h - 70, w=680)
    for k in range(4):
        p.logo(k)


# ================================================================== Holiday card: tardigrades in Santa hats
TARD1 = "/home/user/sfwlib/cuts/tardigrade-1.png"   # Jan Ebr & Ivana Ebrova / iNaturalist, CC BY 4.0
TARD3 = "/home/user/sfwlib/cuts/tardigrade-3.png"   # Stec, Arakawa & Michalczyk 2018, PLOS ONE, CC BY 4.0


def santa_hat(size, ang=0.0):
    """A drawn Santa hat: red cone with a bent tip, white band and pompom, one even outline."""
    def fn(dr, s):
        poly(dr, s, [(30, 170), (95, 40), (150, 25), (205, 70), (170, 75), (130, 70), (190, 170)], "#B23A2E")
        outline(dr, s, "rounded_rectangle", (14, 158, 206, 200), "#FBF8F1", radius=round(20 * s))
        outline(dr, s, "ellipse", (190, 52, 236, 98), "#FBF8F1")
    im = draw_layer(250, 220, fn)
    im = im.resize((size, round(size * 220 / 250)), Image.LANCZOS)
    return im.rotate(ang, expand=True, resample=Image.BICUBIC) if ang else im


def leaves(n, seed):
    def fn(dr, s):
        rnd = random.Random(seed)
        for i in range(n):
            leaf_shape(dr, s, 60 + i * 70 + rnd.uniform(-10, 10), 90 + rnd.uniform(-30, 30), 120, rnd.uniform(-1, 1),
                       rnd.choice(("#59A66C", "#2E6B3A", "#7FA36B")))
    return draw_layer(60 + n * 70 + 60, 200, fn)


@post("pl20261225", "2026-12-25", "holiday-card-tardigrades-v1", 2, CREAM)
def tardigrades(p):
    p.heading(0, "Happy holidays", y=130, size=120)
    x, y, w, h = p.cut(0, TARD3, 90, 560, w=560, name="tardigrade-1")
    p.put(0, "santa-hat-1", santa_hat(190, ang=20), x - 40, y - 120)
    x2, y2, w2, h2 = p.cut(0, TARD1, 640, 520, w=330, name="tardigrade-2")
    p.put(0, "santa-hat-2", santa_hat(170, ang=35), x2 - 50, y2 - 110)
    p.put(0, "leaves", leaves(8, 3), 60, 1000)
    p.small(0, "Tardigrades: Stec et al. 2018, PLOS ONE; Jan Ebr and Ivana Ebrová / iNaturalist. CC BY 4.0", y=1240,
            w=700)

    p.heading(1, "from all of us at the Soil Food Web School.", y=130, size=96)
    x, y, w, h = p.cut(1, TARD3, 260, 640, w=620, name="tardigrade")
    p.put(1, "santa-hat", santa_hat(200, ang=20), x - 45, y - 125)
    p.put(1, "leaves", leaves(7, 9), 100, 960)
    p.small(1, "Tardigrade: Stec et al. 2018, PLOS ONE, CC BY 4.0", y=1240, w=700)
    for k in range(2):
        p.logo(k)
