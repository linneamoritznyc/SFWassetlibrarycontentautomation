"""More style families from FEED-GUIDE.md, so neighbouring posts never look alike.

  I  portrait        a person's photo large and round, name, country and role
  J  numbered steps  a big step number, one short instruction, a square photo
  G  type only       one statement set big on a flat brand colour, no photo

  BOX_SRC=<photos> SFW_FONTS=<dir with the woff2 files> \
    python3 tools/wormhole-visuals/families.py [post ids...]
    -> apps/web/public/wormhole/tiles/<id>-f1-<n>.jpg (1080 x 1350)

Fonts: montserrat-latin-700/800-normal, source-sans-3-latin-400-normal and
eb-garamond-latin-500-normal woff2 files from @fontsource. All upright.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageOps

import boxes as B

W, H = B.W, B.H
OUT = B.OUT


def garamond(size):
    return B.font("eb-garamond-latin-500-normal.woff2", size)


def round_photo(path, d, focus=(0.5, 0.5), ring=None, ring_w=14):
    im = ImageOps.fit(Image.open(path).convert("RGB"), (d, d), Image.LANCZOS, centering=focus)
    mask = Image.new("L", (d * 4, d * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d * 4 - 1, d * 4 - 1), fill=255)
    mask = mask.resize((d, d), Image.LANCZOS)
    out = Image.new("RGBA", (d + 2 * ring_w, d + 2 * ring_w), (0, 0, 0, 0))
    if ring:
        ImageDraw.Draw(out).ellipse((0, 0, d + 2 * ring_w - 1, d + 2 * ring_w - 1), fill=ring)
    out.paste(im, (ring_w, ring_w), mask)
    return out


def initials_disc(text, d, fill, ink):
    out = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    dr = ImageDraw.Draw(out)
    dr.ellipse((0, 0, d - 1, d - 1), fill=fill)
    f = B.head(d // 3)
    w = dr.textlength(text, font=f)
    dr.text(((d - w) / 2, d / 2 - f.size * 0.62), text, font=f, fill=ink)
    return out


# ---------------------------------------------------------------- I, portrait


def portrait_cover(heading, people):
    """Soil brown ground, the heading in EB Garamond, a round face for each person."""
    c = Image.new("RGB", (W, H), B.BROWN)
    d = ImageDraw.Draw(c)
    d.text((90, 110), "CERTIFIED SOIL FOOD WEB CONSULTANTS", font=B.label_font(32), fill=B.TAN)
    B.block(d, (90, 170), heading, garamond(104), B.CREAM, 900, gap=1.08)
    x = 90
    for p in people:
        disc = (
            round_photo(os.path.join(B.SRC, p["photo"]), 380, p.get("focus", (0.5, 0.5)), B.CREAM)
            if p.get("photo")
            else initials_disc(p["initials"], 408, B.TAN, B.BROWN)
        )
        c.paste(disc, (x, 640), disc)
        d.text((x + 10, 1080), p["name"], font=B.head(46), fill=B.CREAM)
        d.text((x + 10, 1140), p["country"], font=B.body(36), fill=B.TAN)
        x += 480
    B.logo(c, (W - 150, H - 150))
    return c


def portrait_slide(p, ground, ink, accent):
    """One person: a large round portrait (or their initials) and their name under it."""
    c = Image.new("RGB", (W, H), ground)
    d = ImageDraw.Draw(c)
    disc = (
        round_photo(os.path.join(B.SRC, p["photo"]), 640, p.get("focus", (0.5, 0.5)), accent, 18)
        if p.get("photo")
        else initials_disc(p["initials"], 676, accent, ground)
    )
    c.paste(disc, ((W - disc.width) // 2, 120), disc)
    y = 880
    nf = B.head(88)
    w = d.textlength(p["name"], font=nf)
    d.text(((W - w) / 2, y), p["name"], font=nf, fill=ink)
    for line, f in ((p["country"], B.body(44)), ("Certified Soil Food Web Consultant", garamond(48))):
        y += 110 if f is not None else 0
        w = d.textlength(line, font=f)
        d.text(((W - w) / 2, y), line, font=f, fill=ink)
    return c


# ---------------------------------------------------------- J, numbered steps


def step_slide(n, text, photo, credit, ground, ink, num_ink, focus=(0.5, 0.5), kicker=None):
    """A big EB Garamond step number, a short instruction, a square photo set flush right.

    Laid out from measured glyph boxes, top to bottom, so the number, the text and the
    photo never touch: at least GAP between each, and the photo shrinks (never below
    MIN_PHOTO) rather than run into the text.
    """
    GAP, MARGIN, BOTTOM, MIN_PHOTO, MAX_PHOTO = 56, 90, 110, 440, 540
    c = Image.new("RGB", (W, H), ground)
    d = ImageDraw.Draw(c)
    y = MARGIN
    if kicker:
        kf = B.label_font(32)
        d.text((MARGIN, y), kicker.upper(), font=kf, fill=num_ink)
        y = d.textbbox((MARGIN, y), kicker.upper(), font=kf)[3] + 28
    if n is not None:
        nf = garamond(260)
        top = d.textbbox((0, 0), str(n), font=nf)[1]
        d.text((MARGIN - 8, y - top), str(n), font=nf, fill=num_ink)
        y = d.textbbox((MARGIN - 8, y - top), str(n), font=nf)[3] + 36
    room = H - BOTTOM - MIN_PHOTO - GAP - y
    f = B.fit_heading(d, text, 900, room, start=80, least=52)
    last = B.block(d, (MARGIN, y), text, f, ink, 900)
    lines = B.wrap(d, text, f, 900)
    text_bottom = d.textbbox((MARGIN, last - int(f.size * 1.12)), lines[-1], font=f)[3]
    if photo:
        size = max(MIN_PHOTO, min(MAX_PHOTO, H - BOTTOM - (text_bottom + GAP)))
        c.paste(B.photo(photo, (size, size), focus), (W - size, H - BOTTOM - size))
        if credit:
            d.text((W - size, H - BOTTOM + 22), credit, font=B.body(26), fill=ink)
    return c


# -------------------------------------------------------------- G, type only


def type_slide(text, ground, ink, kicker=None, kicker_ink=None, size=None, logo=False):
    """One statement set big on a flat colour. Nothing else competes with it."""
    c = Image.new("RGB", (W, H), ground)
    d = ImageDraw.Draw(c)
    f = B.head(size) if size else B.fit_heading(d, text, 900, 760, start=120, least=70)
    h = B.measure(d, text, f, 900)
    y = (H - h) // 2
    if kicker:
        d.text((90, y - 90), kicker.upper(), font=B.label_font(34), fill=kicker_ink or ink)
    B.block(d, (90, y), text, f, ink, 900)
    if logo:
        B.logo(c, (W - 150, H - 150))
    return c


def p26():
    kyle = dict(name="Kyle Babcock", country="United States", photo="kyle.webp", focus=(0.62, 0.4))
    josh = dict(name="Joshua Stone", country="United States", initials="JS")
    return [
        portrait_cover("Welcome to our newest consultants.", [kyle, josh]),
        portrait_slide(kyle, B.CREAM, B.BROWN, B.TAN),
        portrait_slide(josh, B.GREEN, B.CREAM, B.TAN),
    ]


def pl20261114():
    steps = [
        (None, "Your fallen leaves can become fungal compost.", "pl20261114-1.jpg",
         "Photo: Dan Keck, CC0 1.0", B.TAN, B.BROWN, B.CREAM, "Do this weekend"),
        (1, "Pack wet leaves into a wire cage or a bag with holes.", "pl20261114-2.jpg",
         "Photo: United Diversity, CC BY 2.0", B.CREAM, B.BROWN, B.TAN, None),
        (2, "Keep them damp. Fungi do the work, slowly.", "pl20261114-3.jpg",
         "Photo: Belbury, CC BY 4.0", B.CREAM, B.BROWN, B.LIGHT, None),
        (3, "In 1 to 2 years you get dark, crumbly leaf mold.", "pl20261114-4.jpg",
         "Photo: Andy Wright, CC BY 2.0", B.CREAM, B.BROWN, B.TAN, None),
        (4, "Use it as mulch or mix it into potting soil.", "pl20261114-5.jpg",
         "Photo: Lance Cheung, USDA, public domain", B.TAN, B.BROWN, B.CREAM, None),
    ]
    return [step_slide(n, t, p, cr, g, ink, num, kicker=k) for n, t, p, cr, g, ink, num, k in steps]


def pl20261115():
    return [
        type_slide("Imagine a world without earthworms.", B.DEEP, B.CREAM, size=118),
        type_slide("It already exists.", B.CREAM, B.BROWN, size=130),
        type_slide(
            "Many northern North American forests evolved without them after the last Ice Age.",
            B.BLUE, B.CREAM, kicker="After the glaciers", kicker_ink=B.CREAM,
        ),
        type_slide(
            "Introduced worms now eat through the leaf litter those forests depend on.",
            B.TAN, B.BROWN, kicker="Fishing bait, gardens, moved soil", kicker_ink=B.BROWN,
        ),
        type_slide(
            "Even a good organism can be the wrong one in the wrong place.",
            B.BROWN, B.CREAM, logo=True,
        ),
    ]


# f2: pl20261114 re-spaced (24 Oct); bump this for any re-render, never overwrite.
VERSION = os.environ.get("FAMILIES_VERSION", "f1")
POSTS = {"p26": p26, "pl20261114": pl20261114, "pl20261115": pl20261115}


if __name__ == "__main__":
    for pid in sys.argv[1:] or POSTS:
        for i, img in enumerate(POSTS[pid](), 1):
            path = os.path.join(OUT, f"{pid}-{VERSION}-{i}.jpg")
            img.save(path, quality=90, optimize=True)
            print(path)
