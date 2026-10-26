"""Night-scene photographs for the "Meet the Vampire Amoeba" blog headers.

The Halloween look of the p18 Reel cover (night gradient, a drawn full moon with
clouds, fungal threads) with the real Vampyrella lateritia micrographs (Hess,
Sausen and Melkonian 2012, PLoS ONE, CC BY 4.0) in eyepiece lenses. One scene per
header size, painted at twice the size the blog-card builder shows it, so the
builder only has to place it.

  python3 tools/wormhole-visuals/vampire_blog.py <out folder>
"""
import os
import sys

from PIL import Image

from collage import gradient, hyphae, round_photo
from posts import plain_moon, spooky_cloud

VB = "/home/user/photos/vampyrella-blog"
A = f"{VB}/vampyrella-A-advancing-cell.jpg"
H_ = f"{VB}/vampyrella-H-emptying-algal-cell.jpg"
NIGHT = [(0, "#101A12"), (0.6, "#1D3020"), (1, "#2C4128")]

# size key: (width, height, layout). Positions are fractions of width / height; diameters of height.
SCENES = {
    "desktop-header-1920x720": (3840, 1440, dict(a=(.62, .50, .82), h=(.82, .64, .52), moon=(.30, .20, .30))),
    "feature-social-1400x1400": (2800, 1726, dict(a=(.40, .55, .74), h=(.70, .64, .48), moon=(.84, .20, .28))),
    "mobile-header-750x1000": (1500, 1322, dict(a=(.36, .58, .62), h=(.74, .70, .40), moon=(.80, .18, .26))),
    "tablet-header-1024x768": (2048, 888, dict(a=(.42, .56, .74), h=(.69, .62, .48), moon=(.88, .20, .30))),
    "thumbnail-1200x800": (2400, 912, dict(a=(.42, .56, .74), h=(.69, .62, .48), moon=(.88, .20, .30))),
}


def lens(src, d):
    return round_photo(src, d, ring=max(12, d // 28), ring_color="#1B1B18")


def scene(w, h, lay):
    im = gradient(w, h, NIGHT, 181).convert("RGBA")
    def put(layer, cx, cy):
        im.alpha_composite(layer, (round(cx - layer.width / 2), round(cy - layer.height / 2)))
    mx, my, md = lay["moon"]
    put(plain_moon(round(md * h)), mx * w, my * h)
    s = h / 1350
    put(spooky_cloud(round(560 * s * 1.6), round(210 * s * 1.6), 4), mx * w, (my + md * .35) * h)
    put(spooky_cloud(round(420 * s * 1.6), round(120 * s * 1.6), 12, opacity=0.8), mx * w + md * h * .25, (my - md * .2) * h)
    th = hyphae(w, round(h * .32), 18, color="#D9D2BE", n=3, width=2.0 * max(1, s))
    im.alpha_composite(th, (0, h - th.height))
    ax, ay, ad = lay["a"]
    put(lens(A, round(ad * h)), ax * w, ay * h)
    hx, hy, hd = lay["h"]
    put(lens(H_, round(hd * h)), hx * w, hy * h)
    return im.convert("RGB")


# ---------------------------------------------------------------- pictures for inside the blog text
INTEXT = [
    ("vampyrella-A-advancing-cell", "A vampire amoeba on the move"),
    ("vampyrella-B-large-trophozoite", "A large feeding cell"),
    ("vampyrella-F-plasmodium", "A large plasmodium"),
    ("vampyrella-G-feeding-on-alga-brightfield", "Latched onto a strand of algae"),
    ("vampyrella-H-emptying-algal-cell", "Draining an algal cell"),
    ("vampyrella-I-becoming-digestive-cyst", "Turning into a digestive cyst"),
    ("vampyrella-N-digestive-cysts-dark-field", "Digestive cysts among algae"),
]


def intext(name, w=1600, h=1067):
    """One real micrograph in a big lens on the night scene, a small moon in the corner."""
    im = gradient(w, h, NIGHT, 300 + len(name)).convert("RGBA")
    def put(layer, cx, cy):
        im.alpha_composite(layer, (round(cx - layer.width / 2), round(cy - layer.height / 2)))
    put(plain_moon(round(h * .2)), w * .88, h * .17)
    put(spooky_cloud(round(w * .26), round(h * .12), 4), w * .88, h * .24)
    th = hyphae(w, round(h * .28), 7 + len(name), color="#D9D2BE", n=3, width=2.2)
    im.alpha_composite(th, (0, h - th.height))
    put(lens(f"{VB}/{name}.jpg", round(h * .86)), w * .46, h * .5)
    return im.convert("RGB")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == "intext":
        for name, _ in INTEXT:
            intext(name).save(os.path.join(out, f"{name}-night.jpg"), quality=92)
        sys.exit()
    for key, (w, h, lay) in SCENES.items():
        scene(w, h, lay).save(os.path.join(out, f"vampire-night-{key}.jpg"), quality=93)
        print(key, w, h)



# ---------------------------------------------------------------- a proper Halloween night (drawn, no generated images)
import math
import random

import numpy as np
from PIL import ImageDraw, ImageFilter

SIL = (6, 10, 7)


def _branch(dr, x, y, ang, length, width, depth, rnd):
    if depth == 0 or length < 6:
        return
    pts = [(x, y)]
    for _ in range(6):
        ang += rnd.uniform(-0.35, 0.35)
        x += length / 6 * math.cos(ang)
        y += length / 6 * math.sin(ang)
        pts.append((x, y))
    dr.line(pts, fill=SIL + (255,), width=max(1, int(width)), joint="curve")
    for _ in range(2 if depth > 2 else rnd.choice((1, 2, 3))):
        _branch(dr, x, y, ang + rnd.uniform(-0.9, 0.9), length * rnd.uniform(0.55, 0.75), width * 0.62, depth - 1, rnd)


def tree(w, h, side, seed):
    """A bare, gnarled tree silhouette growing in from one side."""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    sgn = 1 if side == "left" else -1
    x0 = 0 if side == "left" else w
    # a leaning, twisted trunk: two wavy edges that narrow upwards
    top_y = h * 0.30
    left, right = [], []
    for i in range(31):
        t = i / 30
        y = h - t * (h - top_y)
        m = min(w, h)
        cx = x0 + sgn * (m * .10 + m * .08 * t + m * .02 * math.sin(t * 7))
        half = m * (.08 * (1 - t) + .02)
        left.append((cx - half, y)); right.append((cx + half, y))
    dr.polygon(left + right[::-1], fill=SIL + (255,))
    trunk_top = (x0 + sgn * min(w, h) * .18, top_y)
    for i in range(7):
        a = (-math.pi / 2) + (rnd.uniform(-1.3, 0.3) if side == "left" else rnd.uniform(-0.3, 1.3))
        m = min(w, h)
        _branch(dr, trunk_top[0], trunk_top[1] + rnd.uniform(-h * .05, h * .15), a, m * rnd.uniform(.22, .34),
                m * .016, 6, rnd)
    return im


def bat(size, flap=0.0):
    s = size / 100
    im = Image.new("RGBA", (size, round(size * .55)), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    up = 18 * flap
    pts = [(50, 22), (40, 14 - up), (28, 4 - up), (20, 14 - up), (8, 8 - up), (0, 24), (14, 22), (24, 30), (34, 24),
           (44, 34), (50, 40), (56, 34), (66, 24), (76, 30), (86, 22), (100, 24), (92, 8 - up), (80, 14 - up),
           (72, 4 - up), (60, 14 - up)]
    dr.polygon([(x * s, (y + 18) * s) for x, y in pts], fill=SIL + (255,))
    dr.ellipse(((44) * s, (26) * s, (56) * s, (42) * s), fill=SIL + (255,))
    return im


def halloween_bg(w, h, seed=7, moon_at=(.8, .22), moon_d=.34, tree_side="left"):
    rnd = random.Random(seed)
    im = gradient(w, h, [(0, "#070D09"), (0.55, "#12201A"), (1, "#1E2E22")], seed).convert("RGBA")
    # stars
    st = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    for _ in range(int(w * h / 9000)):
        x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * .6), rnd.choice((1, 1, 1.5, 2)) * h / 1000
        sd.ellipse((x - r, y - r, x + r, y + r), fill=(240, 236, 214, rnd.randint(90, 220)))
    im.alpha_composite(st)
    # moon glow and moon
    mx, my, md = moon_at[0] * w, moon_at[1] * h, round(moon_d * h)
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse((mx - md * 1.1, my - md * 1.1, mx + md * 1.1, my + md * 1.1), fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(md * .45))
    gl = Image.new("RGBA", (w, h), (236, 226, 190, 0)); gl.putalpha(glow)
    im.alpha_composite(gl)
    moon = plain_moon(md)
    im.alpha_composite(moon, (round(mx - moon.width / 2), round(my - moon.height / 2)))
    for dx, dy, cw, ch, sd_, op in ((0, .3, 1.7, .6, 4, .95), (.35, -.25, 1.2, .35, 12, .8), (-.55, .05, 1.0, .3, 21, .7)):
        c = spooky_cloud(round(md * cw), round(md * ch), sd_, opacity=op)
        im.alpha_composite(c, (round(mx + dx * md - c.width / 2), round(my + dy * md - c.height / 2)))
    # bats crossing the moon
    for i in range(4):
        b = bat(round(min(w, h) * rnd.uniform(.06, .1)), flap=rnd.uniform(0, 1))
        b = b.rotate(rnd.uniform(-20, 20), expand=True, resample=Image.BICUBIC)
        bx = mx + rnd.uniform(-1.4, 0.6) * md
        by = my + rnd.uniform(-0.8, 0.5) * md
        im.alpha_composite(b, (round(bx), round(by)))
    # the tree
    im.alpha_composite(tree(w, h, tree_side, seed + 3))
    # rolling ground and mist
    gd = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdr = ImageDraw.Draw(gd)
    pts = [(x, h * .9 + h * .03 * math.sin(x / w * 6.3 + seed)) for x in np.linspace(0, w, 60)]
    gdr.polygon(pts + [(w, h), (0, h)], fill=SIL + (255,))
    im.alpha_composite(gd)
    mist = Image.new("L", (w, h), 0)
    md_ = ImageDraw.Draw(mist)
    for i in range(14):
        x, y = rnd.uniform(-.1, 1.1) * w, rnd.uniform(.78, .96) * h
        md_.ellipse((x - w * .18, y - h * .035, x + w * .18, y + h * .035), fill=rnd.randint(25, 55))
    mist = mist.filter(ImageFilter.GaussianBlur(h * .03))
    ms = Image.new("RGBA", (w, h), (205, 214, 200, 0)); ms.putalpha(mist)
    im.alpha_composite(ms)
    return im


def jack_o_lantern(d, seed=3):
    """A carved pumpkin with a glowing face, flat colours and one dark outline."""
    S = 2
    n = d * S
    im = Image.new("RGBA", (n, int(n * 1.05)), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    o = (40, 24, 12, 255)
    top = int(n * .16)
    body = (n * .04, top, n * .96, n * .98)
    for i, (x0, x1) in enumerate(((.04, .42), (.58, .96), (.18, .62), (.38, .82), (.28, .72))):
        dr.ellipse((n * x0, top, n * x1, n * .98), fill=(214, 110, 32, 255) if i < 2 else (230, 126, 38, 255),
                   outline=o, width=3 * S)
    dr.rectangle((n * .45, n * .04, n * .55, top + n * .04), fill=(70, 86, 40, 255), outline=o, width=3 * S)
    glow = (255, 214, 92, 255)
    dr.polygon([(n * .22, n * .48), (n * .42, n * .48), (n * .32, n * .30)], fill=glow, outline=o)
    dr.polygon([(n * .58, n * .48), (n * .78, n * .48), (n * .68, n * .30)], fill=glow, outline=o)
    dr.polygon([(n * .45, n * .58), (n * .55, n * .58), (n * .50, n * .50)], fill=glow, outline=o)
    mouth = [(n * .20, n * .66), (n * .30, n * .72), (n * .36, n * .66), (n * .44, n * .74), (n * .50, n * .67),
             (n * .56, n * .74), (n * .64, n * .66), (n * .70, n * .72), (n * .80, n * .66), (n * .70, n * .84),
             (n * .30, n * .84)]
    dr.polygon(mouth, fill=glow, outline=o)
    im = im.resize((d, int(d * 1.05)), Image.LANCZOS)
    # a warm glow around it
    pad = d // 2
    out = Image.new("RGBA", (d + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    g = Image.new("L", out.size, 0)
    ImageDraw.Draw(g).ellipse((pad * 1.0, pad * 1.0, out.width - pad * 1.0, out.height - pad * 1.0), fill=150)
    g = g.filter(ImageFilter.GaussianBlur(pad * .28))
    gl = Image.new("RGBA", out.size, (255, 150, 40, 0)); gl.putalpha(g)
    out.alpha_composite(gl)
    out.alpha_composite(im, (pad, pad))
    return out


def spooky_header(w=1920, h=720, seed=7):
    """The agreed-design candidate: night, orange moon, bats, tree, jack-o'-lantern, title, real amoeba lenses."""
    from collage import font
    rnd = random.Random(seed + 1)
    bg = halloween_bg(w, h, seed, moon_at=(.50, .30), moon_d=.46)
    # warm the moon: an orange wash over the moon area for a harvest-moon feel
    wash = Image.new("L", (w, h), 0)
    mx, my, md = .50 * w, .30 * h, .46 * h
    ImageDraw.Draw(wash).ellipse((mx - md * .52, my - md * .52, mx + md * .52, my + md * .52), fill=90)
    wash = wash.filter(ImageFilter.GaussianBlur(md * .08))
    ow = Image.new("RGBA", (w, h), (232, 120, 40, 0)); ow.putalpha(wash)
    bg.alpha_composite(ow)
    for i in range(6):   # more bats
        b = bat(round(h * rnd.uniform(.05, .11)), flap=rnd.uniform(0, 1)).rotate(rnd.uniform(-25, 25), expand=True)
        bg.alpha_composite(b, (round(w * rnd.uniform(.2, .78)), round(h * rnd.uniform(.03, .45))))
    jl = jack_o_lantern(round(h * .22))
    bg.alpha_composite(jl, (round(w * .60 - jl.width / 2), round(h * .93 - jl.height + jl.height * .22)))
    bg.alpha_composite(lens(A, round(h * .74)), (round(w * .655), round(h * .08)))
    bg.alpha_composite(lens(H_, round(h * .42)), (round(w * .825), round(h * .50)))
    # the title, moonlit
    title = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(title)
    f = font("garamond", True, round(h * .17))
    td.text((w * .16, h * .08), "Vampire", font=f, fill=(244, 238, 222, 255))
    td.text((w * .20, h * .08 + h * .17), "amoeba.", font=f, fill=(244, 238, 222, 255))
    sh = title.getchannel("A").filter(ImageFilter.GaussianBlur(h * .012))
    shade = Image.new("RGBA", (w, h), (0, 0, 0, 0)); shade.putalpha(sh.point(lambda v: int(v * .8)))
    bg.alpha_composite(shade, (4, 6))
    bg.alpha_composite(title)
    return bg


def petri_dish(d):
    """A glass Petri dish seen at a low angle: lid, agar, a few colonies, one even outline, flat colours."""
    S = 2
    n = d * S
    hgt = int(n * .5)
    im = Image.new("RGBA", (n, hgt), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    o = (30, 36, 30, 255)
    # base wall
    dr.rectangle((n * .04, hgt * .42, n * .96, hgt * .72), fill=(205, 222, 214, 140))
    dr.ellipse((n * .04, hgt * .56, n * .96, hgt * .92), fill=(205, 222, 214, 160), outline=o, width=3 * S)
    # agar
    dr.ellipse((n * .08, hgt * .30, n * .92, hgt * .66), fill=(222, 196, 120, 235), outline=o, width=2 * S)
    rnd = random.Random(5)
    for _ in range(9):
        x, y, r = rnd.uniform(.2, .8) * n, rnd.uniform(.38, .58) * hgt, rnd.uniform(.015, .035) * n
        dr.ellipse((x - r, y - r * .45, x + r, y + r * .45), fill=rnd.choice(((240, 236, 220, 255), (196, 112, 58, 255))),
                   outline=o, width=S)
    # rim and lid shine
    dr.ellipse((n * .04, hgt * .24, n * .96, hgt * .66), outline=o, width=3 * S)
    dr.line((n * .04, hgt * .45, n * .04, hgt * .74), fill=o, width=3 * S)
    dr.line((n * .96, hgt * .45, n * .96, hgt * .74), fill=o, width=3 * S)
    dr.arc((n * .14, hgt * .28, n * .7, hgt * .5), 190, 250, fill=(255, 255, 255, 200), width=4 * S)
    return im.resize((d, hgt // S), Image.LANCZOS)


def spooky_header2(w=1920, h=720, seed=7):
    """The agreed design: night, a small distant orange moon, bats, the bare tree, mist, the title, real amoeba lenses."""
    from collage import font
    rnd = random.Random(seed + 1)
    mx, my, md = .50, .22, .26
    bg = halloween_bg(w, h, seed, moon_at=(mx, my), moon_d=md)
    wash = Image.new("L", (w, h), 0)
    cx, cy, r = mx * w, my * h, md * h * .52
    ImageDraw.Draw(wash).ellipse((cx - r, cy - r, cx + r, cy + r), fill=90)
    wash = wash.filter(ImageFilter.GaussianBlur(md * h * .08))
    ow = Image.new("RGBA", (w, h), (232, 120, 40, 0)); ow.putalpha(wash)
    bg.alpha_composite(ow)
    for i in range(6):
        b = bat(round(h * rnd.uniform(.04, .08)), flap=rnd.uniform(0, 1)).rotate(rnd.uniform(-25, 25), expand=True)
        bg.alpha_composite(b, (round(w * rnd.uniform(.3, .62)), round(h * rnd.uniform(.03, .4))))
    bg.alpha_composite(lens(A, round(h * .74)), (round(w * .655), round(h * .08)))
    bg.alpha_composite(lens(H_, round(h * .42)), (round(w * .825), round(h * .50)))
    title = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(title)
    f = font("garamond", True, round(h * .17))
    # the title sits in the open sky right of the trunk, low on the left
    td.text((w * .15, h * .48), "Vampire", font=f, fill=(244, 238, 222, 255))
    td.text((w * .19, h * .48 + h * .17), "amoeba", font=f, fill=(244, 238, 222, 255))
    sh = title.getchannel("A").filter(ImageFilter.GaussianBlur(h * .012))
    shade = Image.new("RGBA", (w, h), (0, 0, 0, 0)); shade.putalpha(sh.point(lambda v: int(v * .8)))
    bg.alpha_composite(shade, (4, 6))
    bg.alpha_composite(title)
    return bg


# ---------------------------------------------------------------- the agreed design at any size
# fractions: moon (x, y, diameter of h), lenses (centre x, centre y, diameter of h), title (x, y, size of h)
LAYOUTS = {
    (1920, 720): dict(moon=(.50, .22, .26), a=(.762, .45, .74), hh=(.906, .71, .42), title=(.15, .48, .17)),
    (1080, 1350): dict(moon=(.78, .10, .14), a=(.58, .45, .40), hh=(.80, .60, .23), title=(.19, .70, .095)),
    (750, 1000): dict(moon=(.78, .10, .14), a=(.58, .45, .40), hh=(.80, .60, .23), title=(.19, .70, .095)),
    (1400, 1400): dict(moon=(.80, .13, .16), a=(.62, .48, .44), hh=(.83, .66, .25), title=(.17, .70, .10)),
    (1024, 768): dict(moon=(.42, .17, .21), a=(.72, .50, .56), hh=(.88, .72, .30), title=(.18, .60, .13)),
    (1200, 800): dict(moon=(.42, .17, .21), a=(.72, .50, .56), hh=(.88, .72, .30), title=(.18, .60, .13)),
}


def spooky(w, h, seed=7, title=True):
    from collage import font
    L = LAYOUTS[(w, h)]
    rnd = random.Random(seed + 1)
    mx, my, md = L["moon"]
    bg = halloween_bg(w, h, seed, moon_at=(mx, my), moon_d=md)
    wash = Image.new("L", (w, h), 0)
    cx, cy, r = mx * w, my * h, md * h * .52
    ImageDraw.Draw(wash).ellipse((cx - r, cy - r, cx + r, cy + r), fill=90)
    wash = wash.filter(ImageFilter.GaussianBlur(md * h * .08))
    ow = Image.new("RGBA", (w, h), (232, 120, 40, 0)); ow.putalpha(wash)
    bg.alpha_composite(ow)
    for i in range(6):
        b = bat(round(min(w, h) * rnd.uniform(.035, .065)), flap=rnd.uniform(0, 1)).rotate(rnd.uniform(-25, 25), expand=True)
        bg.alpha_composite(b, (round(cx + rnd.uniform(-1.6, 1.4) * md * h), round(cy + rnd.uniform(-.9, .7) * md * h)))
    for (src, (x, y, d)) in ((A, L["a"]), (H_, L["hh"])):
        l = lens(src, round(d * h))
        bg.alpha_composite(l, (round(x * w - l.width / 2), round(y * h - l.height / 2)))
    if title:
        tx, ty, ts = L["title"]
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        td = ImageDraw.Draw(layer)
        f = font("garamond", True, round(h * ts))
        td.text((w * tx, h * ty), "Vampire", font=f, fill=(244, 238, 222, 255))
        td.text((w * tx + h * ts * .4, h * ty + h * ts), "amoeba", font=f, fill=(244, 238, 222, 255))
        sh = layer.getchannel("A").filter(ImageFilter.GaussianBlur(h * ts * .07))
        shade = Image.new("RGBA", (w, h), (0, 0, 0, 0)); shade.putalpha(sh.point(lambda v: int(v * .8)))
        bg.alpha_composite(shade, (4, 6))
        bg.alpha_composite(layer)
    return bg.convert("RGB")


def intext_night(name, w=1600, h=1067, seed=11):
    """A picture for the blog text: one real micrograph in a big lens in the agreed night scene."""
    bg = halloween_bg(w, h, seed, moon_at=(.86, .16), moon_d=.17)
    l = lens(f"{VB}/{name}.jpg", round(h * .84))
    bg.alpha_composite(l, (round(w * .52 - l.width / 2), round(h * .5 - l.height / 2)))
    return bg.convert("RGB")


def spooky_pptx(w, h, path, seed=7):
    """The agreed design as an editable PowerPoint: night scene, bats, each lens and the title on their own layers."""
    import io
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Emu, Pt
    from collage import font
    L = LAYOUTS[(w, h)]
    rnd = random.Random(seed + 1)
    mx, my, md = L["moon"]
    bg = halloween_bg(w, h, seed, moon_at=(mx, my), moon_d=md)
    wash = Image.new("L", (w, h), 0)
    cx, cy, r = mx * w, my * h, md * h * .52
    ImageDraw.Draw(wash).ellipse((cx - r, cy - r, cx + r, cy + r), fill=90)
    wash = wash.filter(ImageFilter.GaussianBlur(md * h * .08))
    ow = Image.new("RGBA", (w, h), (232, 120, 40, 0)); ow.putalpha(wash)
    bg.alpha_composite(ow)
    bats = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for i in range(6):
        b = bat(round(min(w, h) * rnd.uniform(.035, .065)), flap=rnd.uniform(0, 1)).rotate(rnd.uniform(-25, 25), expand=True)
        bats.alpha_composite(b, (round(cx + rnd.uniform(-1.6, 1.4) * md * h), round(cy + rnd.uniform(-.9, .7) * md * h)))
    layers = [("Night sky, moon, tree and mist", bg.convert("RGB"), 0, 0), ("Bats", bats, 0, 0)]
    for name, (src, (x, y, d)) in (("Lens: vampire amoeba", (A, L["a"])), ("Lens: draining an algal cell", (H_, L["hh"]))):
        l = lens(src, round(d * h))
        layers.append((name, l, round(x * w - l.width / 2), round(y * h - l.height / 2)))
    EMU = 914400 / 96
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(round(w * EMU)), Emu(round(h * EMU))
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    for name, im, x, y in layers:
        buf = io.BytesIO()
        (im.save(buf, "JPEG", quality=92) if im.mode == "RGB" else im.save(buf, "PNG"))
        buf.seek(0)
        pic = sl.shapes.add_picture(buf, Emu(round(x * EMU)), Emu(round(y * EMU)), Emu(round(im.width * EMU)),
                                    Emu(round(im.height * EMU)))
        pic.name = name
    tx, ty, ts = L["title"]
    size = h * ts
    for i, word in enumerate(("Vampire", "amoeba")):
        f = font("garamond", True, round(size))
        tw = f.getlength(word) + size * .3
        tb = sl.shapes.add_textbox(Emu(round((w * tx + i * size * .4) * EMU)), Emu(round((h * ty + i * size - size * .12) * EMU)),
                                   Emu(round(tw * EMU)), Emu(round(size * 1.25 * EMU)))
        tb.name = f"Title: {word}"
        tf = tb.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.word_wrap = False
        run = tf.paragraphs[0].add_run()
        run.text = word
        run.font.name = "EB Garamond"
        run.font.italic = True
        run.font.size = Pt(size * 72 / 96)
        run.font.color.rgb = RGBColor(244, 238, 222)
    prs.save(path)
