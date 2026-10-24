"""d26, "Read the drop: the smell of rain": four slides, flat colour boxes over real photos.

Built like the trifold: full-colour boxes with hard edges overlapping the photos, and
one green band that runs out of each slide and into the next, so the carousel joins up
when swiped. Upright Montserrat and Source Sans 3, brand colours only.

Photos come from the SFW microbe library and workshop photos on Linnea's Drive:
  rain_soil.jpg       Moist healthy no-till soil after 2 inches of rain
  actino_ullens.jpg   Actinobacteria, 40x obj, Rodrigue Ullens
  collembola.jpg      Microarthropod (Collembola), 40x obj, Cameron Radman

  D26_SRC=<photos> SFW_FONTS=<@fontsource files dir> python3 tools/wormhole-visuals/d26_rain.py
    -> apps/web/public/wormhole/tiles/d26-v2-<n>.jpg (1080 x 1350)
"""
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
LOGO = os.path.join(REPO, "apps", "web", "public", "wormhole", "sfw-foundation-wordmark-240.png")
SRC = os.environ["D26_SRC"]
FONTS = os.environ["SFW_FONTS"]

W, H = 1080, 1350
BROWN = (79, 52, 51)
GREEN = (21, 104, 38)
DEEP = (34, 55, 31)
CREAM = (244, 241, 234)
BLUE = (55, 128, 184)
TAN = (200, 155, 123)
LIGHT = (89, 166, 108)
INK = (51, 49, 48)

BAND_Y, BAND_H = 1040, 70  # the green band that crosses every slide edge


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


HEAD = lambda s: font("montserrat-latin-800-normal.woff2", s)  # noqa: E731
LABEL = lambda s: font("montserrat-latin-700-normal.woff2", s)  # noqa: E731
BODY = lambda s: font("source-sans-3-latin-400-normal.woff2", s)  # noqa: E731


def photo(name, box, focus=(0.5, 0.5)):
    """The photo cropped to fill box (w, h) around a focus point, true colour."""
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    return ImageOps.fit(im, box, Image.LANCZOS, centering=focus)


def wrap(d, text, f, width):
    words, lines, line = text.split(), [], ""
    for w in words:
        test = f"{line} {w}".strip()
        if d.textlength(test, font=f) <= width:
            line = test
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def text_block(d, xy, text, f, fill, width, gap=1.12):
    x, y = xy
    size = f.size
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += int(size * gap)
    return y


def logo(canvas, xy, size=96):
    lg = Image.open(LOGO).convert("RGBA")
    lg.thumbnail((size, size))
    disc = Image.new("RGBA", (size + 20, size + 20), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, size + 19, size + 19), fill=CREAM)
    disc.alpha_composite(lg, ((size + 20 - lg.width) // 2, (size + 20 - lg.height) // 2))
    canvas.paste(disc, xy, disc)


def credit(d, xy, text, fill=CREAM):
    d.text(xy, text, font=BODY(26), fill=fill)


def band(d, x0, x1):
    d.rectangle((x0, BAND_Y, x1, BAND_Y + BAND_H), fill=LIGHT)


def slide1():
    c = Image.new("RGB", (W, H), CREAM)
    c.paste(photo("rain_soil.jpg", (W, BAND_Y), (0.45, 0.55)), (0, 0))
    d = ImageDraw.Draw(c)
    # Deep green box rising out of the bottom, over the soil.
    d.rectangle((0, 640, 860, H), fill=DEEP)
    d.text((70, 700), "AFTER RAIN", font=LABEL(34), fill=LIGHT)
    text_block(d, (70, 760), "The smell of rain is a chemical signal.", HEAD(86), CREAM, 740)
    band(d, 860, W)  # runs out to the right, into slide 2
    d.rectangle((860, BAND_Y + BAND_H, W, H), fill=BROWN)
    credit(d, (70, 1270), "No-till soil after 2 inches of rain", (200, 210, 195))
    logo(c, (W - 150, 40))
    return c


def slide2():
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    # Microscope photo in the upper right, a brown box overlapping its lower left corner.
    c.paste(photo("actino_ullens.jpg", (900, 860), (0.55, 0.45)), (180, 0))
    d = ImageDraw.Draw(c)
    band(d, 0, 180)  # arrives from slide 1
    d.rectangle((0, 0, 180, BAND_Y), fill=BLUE)
    d.rectangle((90, 700, 960, 1250), fill=BROWN)
    d.text((150, 760), "THE SMELL HAS A NAME", font=LABEL(34), fill=TAN)
    y = text_block(d, (150, 820), "Geosmin, made by Streptomyces bacteria.", HEAD(78), CREAM, 760)
    text_block(
        d,
        (150, y + 20),
        "They grow as long threads through the soil and release it as they form spores.",
        BODY(40),
        CREAM,
        740,
        gap=1.3,
    )
    band(d, 960, W)  # leaves to the right, into slide 3
    credit(d, (220, 650), "Actinobacteria, 40x objective. Photo: Rodrigue Ullens", INK)
    return c


def slide3():
    c = Image.new("RGB", (W, H), GREEN)
    c.paste(photo("collembola.jpg", (W, 800), (0.42, 0.45)), (0, 380))
    d = ImageDraw.Draw(c)
    # Cream box across the top, a tan block cut into its right side.
    d.rectangle((0, 0, W, 390), fill=CREAM)
    d.rectangle((780, 0, W, 450), fill=TAN)
    d.text((70, 70), "WHO SMELLS IT", font=LABEL(34), fill=GREEN)
    text_block(d, (70, 125), "It attracts springtails.", HEAD(90), DEEP, 680)
    band(d, 0, W)  # crosses the whole slide, from 2 into 4
    d.rectangle((0, BAND_Y + BAND_H, W, H), fill=DEEP)
    text_block(
        d,
        (70, BAND_Y + BAND_H + 40),
        "Tiny six-legged soil animals that find geosmin and walk toward it.",
        BODY(40),
        CREAM,
        940,
        gap=1.3,
    )
    credit(d, (70, 990), "Collembola, 40x objective. Photo: Cameron Radman")
    return c


def slide4():
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    # Two photos side by side under a full-width brown box: the colony and its visitor.
    c.paste(photo("actino_ullens.jpg", (540, 560), (0.6, 0.4)), (0, 0))
    c.paste(photo("collembola.jpg", (540, 560), (0.45, 0.5)), (540, 0))
    d = ImageDraw.Draw(c)
    band(d, 0, 300)  # arrives from slide 3 and stops
    d.rectangle((0, 500, W, BAND_Y), fill=BROWN)
    d.text((70, 560), "THE TRADE", font=LABEL(34), fill=TAN)
    text_block(d, (70, 620), "They eat the colony and carry its spores away.", HEAD(80), CREAM, 920)
    d.rectangle((300, BAND_Y, W, H), fill=DEEP)
    text_block(
        d,
        (360, BAND_Y + 50),
        "The smell after rain is a dispersal system, older than us.",
        BODY(40),
        CREAM,
        660,
        gap=1.3,
    )
    credit(d, (360, 1270), "Becher et al. 2020, Nature Microbiology", (200, 210, 195))
    d.rectangle((0, BAND_Y + BAND_H, 300, H), fill=GREEN)
    logo(c, (90, BAND_Y + BAND_H + 50))
    return c


if __name__ == "__main__":
    for i, make in enumerate([slide1, slide2, slide3, slide4], 1):
        path = os.path.join(OUT, f"d26-v2-{i}.jpg")
        make().save(path, quality=90, optimize=True)
        print(path)
