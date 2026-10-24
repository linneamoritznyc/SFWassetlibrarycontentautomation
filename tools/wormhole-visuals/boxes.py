"""Brand box carousels: flat colour boxes with hard edges over real photos.

The style Linnea approved on d26 (the smell of rain), as a reusable builder. Each slide
picks one of four layouts in turn, so no two neighbouring slides look the same, and a
light green band crosses every slide edge so a carousel joins up when swiped.
Montserrat for headings and labels, Source Sans 3 for body text, all upright, brand
colours only. No gradients, fades, grain, glow, italics, tape, tilts or cutouts.

  BOX_SRC=<photos dir> SFW_FONTS=<dir with the four woff2 files> \
    python3 tools/wormhole-visuals/boxes.py [post ids...]
    -> apps/web/public/wormhole/tiles/<id>-b1-<n>.jpg (1080 x 1350)

Fonts: montserrat-latin-700/800-normal.woff2 and source-sans-3-latin-400/600-normal.woff2
from @fontsource.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
LOGO = os.path.join(REPO, "apps", "web", "public", "wormhole", "sfw-foundation-wordmark-240.png")
SRC = os.environ.get("BOX_SRC", "")
FONTS = os.environ.get("SFW_FONTS", "")

W, H = 1080, 1350
BROWN = (79, 52, 51)
GREEN = (21, 104, 38)
DEEP = (34, 55, 31)
CREAM = (244, 241, 234)
BLUE = (55, 128, 184)
TAN = (200, 155, 123)
LIGHT = (89, 166, 108)
PURPLE = (107, 76, 122)
INK = (51, 49, 48)
SOFT = (200, 210, 195)

BAND_Y, BAND_H = 1040, 70


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def head(s):
    return font("montserrat-latin-800-normal.woff2", s)


def label_font(s):
    return font("montserrat-latin-700-normal.woff2", s)


def body(s):
    return font("source-sans-3-latin-400-normal.woff2", s)


def photo(name, box, focus=(0.5, 0.5)):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    return ImageOps.fit(im, box, Image.LANCZOS, centering=focus)


def wrap(d, text, f, width):
    lines, line = [], ""
    for w in text.split():
        test = f"{line} {w}".strip()
        if d.textlength(test, font=f) <= width or not line:
            line = test
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def fit_heading(d, text, width, max_h, start=92, least=54):
    """The largest heading size whose wrapped lines fit inside width x max_h."""
    size = start
    while size > least:
        f = head(size)
        if len(wrap(d, text, f, width)) * size * 1.12 <= max_h:
            return f
        size -= 4
    return head(least)


def block(d, xy, text, f, fill, width, gap=1.12):
    x, y = xy
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += int(f.size * gap)
    return y


def measure(d, text, f, width, gap=1.12):
    return len(wrap(d, text, f, width)) * int(f.size * gap)


def credit_on(c, d, xy, text):
    """A photo credit on its own small deep green tab, readable on any photo."""
    f = body(26)
    w = int(d.textlength(text, font=f))
    x, y = xy
    d.rectangle((x - 14, y - 8, x + w + 14, y + 36), fill=DEEP)
    d.text((x, y), text, font=f, fill=CREAM)


def logo(c, xy, size=96):
    lg = Image.open(LOGO).convert("RGBA")
    lg.thumbnail((size, size))
    disc = Image.new("RGBA", (size + 20, size + 20), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, size + 19, size + 19), fill=CREAM)
    disc.alpha_composite(lg, ((size + 20 - lg.width) // 2, (size + 20 - lg.height) // 2))
    c.paste(disc, xy, disc)


def band(d, x0, x1):
    d.rectangle((x0, BAND_Y, x1, BAND_Y + BAND_H), fill=LIGHT)


# Each layout takes a slide dict: heading, and optionally label, body, photo, focus,
# credit. `first` and `last` decide whether the band comes in from the left and goes
# out to the right.


def cover(s, first, last):
    """Photo across the top, a deep green box rising from the bottom left."""
    c = Image.new("RGB", (W, H), CREAM)
    if s.get("photo"):
        c.paste(photo(s["photo"], (W, BAND_Y), s.get("focus", (0.5, 0.5))), (0, 0))
    d = ImageDraw.Draw(c)
    f = fit_heading(d, s["heading"], 740, 470)
    need = (60 if s.get("label") else 0) + measure(d, s["heading"], f, 740)
    if s.get("body"):
        need += 16 + measure(d, s["body"], body(38), 740, 1.3)
    box_top = max(560, 1220 - need - 60)
    d.rectangle((0, box_top, 860, H), fill=DEEP)
    y = box_top + 60
    if s.get("label"):
        lf = label_font(34)
        while d.textlength(s["label"].upper(), font=lf) > 740:
            lf = label_font(lf.size - 2)
        d.text((70, y), s["label"].upper(), font=lf, fill=LIGHT)
        y += 60
    y = block(d, (70, y), s["heading"], f, CREAM, 740)
    if s.get("body"):
        block(d, (70, y + 16), s["body"], body(38), CREAM, 740, gap=1.3)
    if not last:
        band(d, 860, W)
    d.rectangle((860, BAND_Y + BAND_H, W, H), fill=BROWN)
    if s.get("credit"):
        d.text((70, 1280), s["credit"], font=body(26), fill=SOFT)
    logo(c, (W - 150, 40))
    return c


def side(s, first, last):
    """Photo on the upper right, a brown box overlapping its lower left corner."""
    c = Image.new("RGB", (W, H), CREAM)
    if s.get("photo"):
        c.paste(photo(s["photo"], (900, 860), s.get("focus", (0.5, 0.5))), (180, 0))
    d = ImageDraw.Draw(c)
    if not first:
        band(d, 0, 180)
    d.rectangle((0, 0, 180, BAND_Y), fill=BLUE)
    f = fit_heading(d, s["heading"], 760, 300 if s.get("body") else 440, start=84)
    need = (60 if s.get("label") else 0) + measure(d, s["heading"], f, 760)
    if s.get("body"):
        need += 16 + measure(d, s["body"], body(38), 740, 1.3)
    box_bottom = max(BAND_Y + BAND_H + 40, 680 + 60 + need + 50)
    d.rectangle((90, 680, 960, box_bottom), fill=BROWN)
    y = 740
    if s.get("label"):
        d.text((150, y), s["label"].upper(), font=label_font(34), fill=TAN)
        y += 60
    y = block(d, (150, y), s["heading"], f, CREAM, 760)
    if s.get("body"):
        block(d, (150, y + 16), s["body"], body(38), CREAM, 740, gap=1.3)
    if not last:
        band(d, 960, W)
    if s.get("credit"):
        credit_on(c, d, (214, 618), s["credit"])
    if last:
        logo(c, (W - 150, BAND_Y + 40))
    return c


def top(s, first, last):
    """Cream box with the heading across the top, the photo below, a deep green foot."""
    c = Image.new("RGB", (W, H), GREEN)
    if s.get("photo"):
        c.paste(photo(s["photo"], (W, 700), s.get("focus", (0.5, 0.5))), (0, 380))
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 390), fill=CREAM)
    d.rectangle((780, 0, W, 450), fill=TAN)
    f = fit_heading(d, s["heading"], 680, 300, start=88)
    h_need = measure(d, s["heading"], f, 680)
    block(d, (70, max(50, (390 - h_need) // 2)), s["heading"], f, DEEP, 680)
    band(d, 0 if not first else 300, W if not last else 780)
    d.rectangle((0, BAND_Y + BAND_H, W, H), fill=DEEP)
    y = BAND_Y + BAND_H + 34
    if s.get("label"):
        d.text((70, y), s["label"].upper(), font=label_font(30), fill=LIGHT)
        y += 52
    if s.get("body"):
        block(d, (70, y), s["body"], body(38), CREAM, 820, gap=1.3)
    if s.get("credit"):
        credit_on(c, d, (84, 996), s["credit"])
    if last:
        logo(c, (W - 150, BAND_Y + BAND_H + 50))
    return c


def split(s, first, last):
    """Photo across the top half, a full-width brown box under it, a deep green corner."""
    c = Image.new("RGB", (W, H), CREAM)
    if s.get("photo"):
        c.paste(photo(s["photo"], (W, 560), s.get("focus", (0.5, 0.5))), (0, 0))
    d = ImageDraw.Draw(c)
    d.rectangle((0, 500, W, BAND_Y), fill=BROWN)
    y = 560
    if s.get("label"):
        d.text((70, y), s["label"].upper(), font=label_font(34), fill=TAN)
        y += 60
    f = fit_heading(d, s["heading"], 920, BAND_Y - y - 40, start=84)
    block(d, (70, y), s["heading"], f, CREAM, 920)
    if not first:
        band(d, 0, 300)
    d.rectangle((300, BAND_Y, W, H), fill=DEEP)
    d.rectangle((0, BAND_Y + BAND_H, 300, H), fill=GREEN)
    if not last:
        band(d, 300 if first else 0, W)
    if s.get("body"):
        block(d, (360, BAND_Y + BAND_H + 30), s["body"], body(36), CREAM, 660, gap=1.3)
    if s.get("credit"):
        d.text((360, 1290), s["credit"], font=body(26), fill=SOFT)
    logo(c, (90, BAND_Y + BAND_H + 50))
    return c


def name(s, first, last):
    """A person without a photo yet: a big tan block with the name, brand boxes around it."""
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 300), fill=GREEN)
    d.rectangle((90, 220, 990, 900), fill=TAN)
    y = 320
    if s.get("label"):
        d.text((160, y), s["label"].upper(), font=label_font(36), fill=BROWN)
        y += 70
    y = block(d, (160, y), s["heading"], head(110), BROWN, 760)
    if s.get("body"):
        block(d, (160, y + 20), s["body"], body(44), BROWN, 760, gap=1.3)
    band(d, 0 if not first else 300, W if not last else 780)
    d.rectangle((0, BAND_Y + BAND_H, W, H), fill=DEEP)
    if last:
        logo(c, (W - 150, BAND_Y + BAND_H + 50))
    return c


ORDER = [cover, side, top, split]


def build(post_id, slides, version="b1"):
    paths = []
    for i, s in enumerate(slides):
        layout = s.get("layout") or ORDER[i % len(ORDER)]
        img = layout(s, i == 0, i == len(slides) - 1)
        path = os.path.join(OUT, f"{post_id}-{version}-{i + 1}.jpg")
        img.save(path, quality=90, optimize=True)
        paths.append(path)
    return paths


POSTS = {
    "p25": [
        dict(
            label="Dr. Elaine Ingham",
            heading="Dr. Elaine's papers, in one place.",
            photo="elaine_cr.jpg",
            focus=(0.45, 0.4),
            credit="Dr. Elaine Ingham in Costa Rica",
        ),
        dict(
            label="Now on our website",
            heading="Four decades of research, open to read.",
            body="77 journal papers, 6 book chapters and 10 EPA and technical reports, each linked to where you can read it.",
            photo="actino_ullens.jpg",
            focus=(0.55, 0.45),
            credit="Actinobacteria, 40x objective. Photo: Rodrigue Ullens",
            layout=top,
        ),
    ],
    "p26": [
        dict(
            label="Certified Soil Food Web Consultants",
            heading="Welcome to our newest consultants.",
            photo="rain_soil.jpg",
            focus=(0.45, 0.55),
        ),
        dict(
            label="United States",
            heading="Kyle Babcock",
            body="Certified Soil Food Web Consultant.",
            photo="kyle.webp",
            focus=(0.6, 0.4),
        ),
        dict(
            label="United States",
            heading="Joshua Stone",
            body="Certified Soil Food Web Consultant.",
            layout=name,
        ),
    ],
    "pl20261114": [
        dict(
            label="Do this weekend",
            heading="Your fallen leaves can become fungal compost.",
            photo="pl20261114-1.jpg",
            credit="Photo: Dan Keck, CC0 1.0",
        ),
        dict(
            heading="Pack wet leaves into a wire cage or a bag with holes.",
            photo="pl20261114-2.jpg",
            credit="Photo: United Diversity, CC BY 2.0",
        ),
        dict(
            heading="Keep them damp. Fungi do the work, slowly.",
            photo="pl20261114-3.jpg",
            credit="Photo: Belbury, CC BY 4.0",
        ),
        dict(
            heading="In 1 to 2 years you get dark, crumbly leaf mold.",
            photo="pl20261114-4.jpg",
            credit="Photo: Andy Wright, CC BY 2.0",
        ),
        dict(
            heading="Use it as mulch or mix it into potting soil.",
            photo="pl20261114-5.jpg",
            credit="Photo: Lance Cheung, USDA, public domain",
            layout=cover,
        ),
    ],
    "pl20261115": [
        dict(
            heading="Imagine a world without earthworms.",
            photo="pl20261115-1.jpg",
            credit="Photo: Nicholas_T, CC BY 2.0",
        ),
        dict(
            label="A thick layer of leaf litter",
            heading="It already exists.",
            photo="pl20261115-2.jpg",
            credit="Photo: Nicholas_T, CC BY 2.0",
        ),
        dict(
            label="Pennsylvania hardwood forest, autumn",
            heading="Many northern North American forests evolved without them after the last Ice Age.",
            photo="pl20261115-3.jpg",
            credit="Photo: Nicholas_T, CC BY 2.0",
        ),
        dict(
            label="Worms on bare, worm-worked soil",
            heading="Introduced worms now eat through the leaf litter those forests depend on.",
            photo="pl20261115-4.jpg",
            credit="Photo: John Abrams, CC BY 4.0",
        ),
        dict(
            label="An introduced earthworm, Minnesota",
            heading="Even a good organism can be the wrong one in the wrong place.",
            photo="pl20261115-5.jpg",
            credit="Photo: Brett Ortler, CC BY 2.0",
            layout=cover,
        ),
    ],
}


if __name__ == "__main__":
    for pid in sys.argv[1:] or POSTS:
        for p in build(pid, POSTS[pid]):
            print(p)
