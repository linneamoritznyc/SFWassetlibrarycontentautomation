"""International Women's Day 2027 (wd20270308): watch the all-woman panel "Women Seeding Regenerative Futures".

Family I, portrait. Deep green ground, four round portraits, Montserrat headings, Pathway Gothic One labels,
Source Sans 3 body. A real photo only where it shows that person; Clea and Kelda get labelled photo spaces
until their portraits come in.

  python3 tools/wormhole-visuals/iwd.py
    -> apps/web/public/wormhole/tiles/wd20270308-v1-<n>.jpg
"""
from PIL import Image, ImageDraw

import collage
from collage import draw_layer, hexrgb
from novdec import CREAMT, DEEP, REG, W, build, post

KAVI = "/home/user/photos/new-2026-10/team-kavi-reddy.jpg"
CARLA = "/home/user/linneamoritznyc/final-sfwsite-linnea/img/carla.jpg"
LGREEN = "#59A66C"

PANEL = [  # (name, one line from the September planning doc, photo or None)
    ("Clea Chandmal", "Permaculture science rooted in plant molecular physiology.", None),
    ("Kelda Lorax", "30 years of permaculture education and a deep commitment to justice in land relationships.",
     None),
    ("Dr. Carla Portugal", "Research across Brazil and the United States. Instructor, mentor and translator at the "
     "Soil Food Web School.", CARLA),
    ("Kavi Reddy", "Systems thinking across soil fertility, food systems and global partnerships.", KAVI),
]


def heading(p, k, text, y, size=78, w=900, x=90, align="left"):
    p.hb[k] = p.d.text(k, "heading", text, x, y, w, 330, size, kind="montserrat-bold", italic=False,
                       color=CREAMT, lh=1.12, align=align, min_size=56)
    return p.hb[k]


def label(p, k, text, x, y, w=900, size=40, color=LGREEN, align="left"):
    return p.d.text(k, f"label {text[:20]}", text, x, y, w, 70, size, kind="pathway", italic=False, color=color,
                    lh=1.1, align=align, track=2)


def body(p, k, text, x, y, w, size=34, h=150):
    return p.d.text(k, "body", text, x, y, w, h, size, kind="source-reg", italic=False, color="#E3DDCC", lh=1.25,
                    min_size=26)


def portrait(p, k, src, name, cx, cy, dia):
    """A round portrait with a light green ring, or a labelled empty circle for a photo still to come."""
    if src:
        disc = collage.round_photo(src, dia, ring=10, fx=0.5, fy=0.35, ring_color=LGREEN)
    else:
        def fn(dr, s):
            r = dia + 20
            dr.ellipse((0, 0, r * s, r * s), fill=hexrgb(LGREEN) + (255,))
            dr.ellipse((10 * s, 10 * s, (r - 10) * s, (r - 10) * s), fill=(255, 255, 255, 40))
        disc = draw_layer(dia + 20, dia + 20, fn)
        hatch = Image.new("L", disc.size, 0)
        ImageDraw.Draw(hatch).ellipse((10, 10, disc.width - 11, disc.height - 11), fill=255)
        lines = Image.new("RGBA", disc.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lines)
        for i in range(-disc.height, disc.width, 26):
            ld.line((i, disc.height, i + disc.height, 0), fill=(244, 241, 234, 50), width=2)
        clipped = Image.new("RGBA", disc.size, (0, 0, 0, 0))
        clipped.paste(lines, (0, 0), Image.composite(lines.getchannel("A"), Image.new("L", disc.size, 0), hatch))
        disc.alpha_composite(clipped)
    x, y = round(cx - disc.width / 2), round(cy - disc.height / 2)
    p.put(k, "portrait " + name if src else "photo-placeholder " + name, disc, x, y)
    if not src:
        label(p, k, "PHOTO: " + name.split()[0].upper(), x + 20, cy - 22, w=disc.width - 40, size=34,
              color=CREAMT, align="center")
    label(p, k, name.upper(), cx - 230, y + disc.height + 14, w=460, size=40, color=CREAMT, align="center")


@post("wd20270308", "2027-03-08", "iwd-women-seeding-regenerative-futures-v1", 3, DEEP)
def iwd(p):
    # 1. cover: who is on the panel
    label(p, 0, "INTERNATIONAL WOMEN'S DAY", 90, 80)
    heading(p, 0, "Four women on permaculture, soil and community", 140, size=70)
    for i, (name, _, src) in enumerate(PANEL):
        cx = 290 + (i % 2) * 420
        cy = 590 + (i // 2) * 380
        portrait(p, 0, src, name, cx, cy, 290)
    # 2. one line each, from the September planning doc
    label(p, 1, "THE PANEL", 90, 80)
    heading(p, 1, "Women Seeding Regenerative Futures", 140, size=66)
    y = 360
    for name, line, _ in PANEL:
        label(p, 1, name.upper(), 90, y, size=44, color=LGREEN)
        body(p, 1, line, 90, y + 56, 740)
        y += 222
    # 3. the ask
    label(p, 2, "WATCH THE FULL PANEL", 90, 80)
    heading(p, 2, "Learn and grow together with four extraordinary forces of nature.", 140, size=72)
    body(p, 2, "An all-woman panel of experts in permaculture and regenerative design, recorded live on "
         "2 September 2026. Free to watch.", 90, 560, 880, size=40, h=200)
    label(p, 2, "LINK IN BIO", 90, 800, size=56, color=LGREEN)
    body(p, 2, "webinar.soilfoodweb.com", 90, 875, 880, size=38)
    for k in range(3):
        p.logo(k)


if __name__ == "__main__":
    print(build("wd20270308"))
