"""Watercolor science-book redo (Stephanie, 28 Oct: less flat empty space, more texture and depth, editable in Canva).

Warm white paper with a faint cold-press grain, one big watercolor illustration per slide filling the page
(wc_redo_prompts.py, FLUX on Replicate, no text in the image), the slide words as a Montserrat Bold heading
in Soil Brown, thin brown hand-drawn arrows with short Montserrat labels, the logo bottom right in clear paper.

  python3 tools/wormhole-visuals/wc_redo.py p20
    -> apps/web/public/wormhole/tiles/<id>-wc-<n>.jpg   (never overwrites)
    -> apps/web/public/wormhole/decks/DD-MM-YYYY-<slug>-wc.pptx  (every picture, arrow, logo and text its own layer)
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

import collage
from collage import Deck, H, W
from watercolor_posts import arrow_layer, wc

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
PAPER, BROWN, BODY = "#FBF9F4", "#4F3433", "#5C4636"
LOGO_W = 150
LOGO_BOX = (W - 60 - LOGO_W, H - 60 - 130, W - 40, H - 40)  # where the logo sits; kept clear of paint


def wc_paper(seed, w=W, h=H):
    """Warm white watercolor paper: soft uneven wash plus a fine embossed cold-press tooth."""
    rng = np.random.default_rng(seed)
    base = np.array(collage.hexrgb(PAPER), np.float32)[None, None, :]
    low = rng.normal(0, 1, (h // 60 + 2, w // 60 + 2)).astype(np.float32)
    low = np.array(Image.fromarray(((low - low.min()) / np.ptp(low) * 255).astype(np.uint8))
                   .resize((w, h), Image.BICUBIC), np.float32) / 255 - 0.5
    tooth = Image.fromarray((rng.random((h // 2, w // 2)) * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)
    tooth = np.array(tooth.filter(ImageFilter.GaussianBlur(1.2)).filter(ImageFilter.EMBOSS), np.float32) - 128
    img = base + low[..., None] * 7 + tooth[..., None] * 0.10
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")


class Slide:
    def __init__(self, d, k):
        self.d, self.k = d, k
        self.box = None

    def heading(self, text, size=74, y=70, x=80, w=920):
        self.bottom = self.d.text(self.k, "heading", text, x, y, w, 330, size, kind="montserrat-bold", italic=False,
                                  color=BROWN, lh=1.12, min_size=52)
        return self.bottom

    def body(self, text, y, size=36, x=82, w=900):
        return self.d.text(self.k, "body", text, x, round(y), w, 200, size, kind="mont", italic=False, color=BODY,
                           lh=1.3, min_size=28)

    def art(self, name, top=None, bottom=H - 30, left=30, right=W - 30, dx=0):
        """The watercolor, as big as fits between the heading and the bottom edge, clear of the logo."""
        top = round(self.bottom + 24) if top is None else top
        im = wc(name, w=right - left, h=bottom - top)
        for _ in range(30):
            x = left + (right - left - im.width) // 2 + dx
            y = bottom - im.height
            a = im.getchannel("A")
            lx0, ly0, lx1, ly1 = LOGO_BOX
            cx0, cy0, cx1, cy1 = max(lx0 - x, 0), max(ly0 - y, 0), min(lx1 - x, im.width), min(ly1 - y, im.height)
            if cx1 <= cx0 or cy1 <= cy0 or np.asarray(a.crop((cx0, cy0, cx1, cy1))).mean() < 6:
                break
            dx -= 14  # slide left first, then shrink
            if x <= left - 40:
                im = im.resize((round(im.width * 0.96), round(im.height * 0.96)), Image.LANCZOS)
                dx = 0
        self.d.put(self.k, "illustration", im, x, y, shadowed=False, anchor="tl")
        self.box = (x, y, im.width, im.height)
        return self.box

    def at(self, fx, fy):
        x, y, w, h = self.box
        return x + w * fx, y + h * fy

    def label(self, text, x, y, w=300, align="left", size=30):
        self.d.text(self.k, f"label {text[:20]}", text, round(x), round(y), w, 120, size, kind="mont-medium",
                    italic=False, color=BROWN, lh=1.2, align=align)

    def arrow(self, p0, p1, bend=0.25, seed=0):
        lay, x, y = arrow_layer(p0, p1, bend, seed)
        self.d.put(self.k, "arrow", lay, x, y, shadowed=False, anchor="tl")

    def logo(self):
        im = Image.open(LOGO).convert("RGBA")
        im = im.resize((LOGO_W, round(im.height * LOGO_W / im.width)), Image.LANCZOS)
        self.d.put(self.k, "logo", im, LOGO_BOX[0], H - 50 - im.height, shadowed=False, anchor="tl")


def build(pid, iso, slug, n, fn, seed=0):
    d = Deck(pid, n, slug, iso)
    for k in range(n):
        d.bg(k, wc_paper(seed + k), name=f"paper-{k + 1}")
    fn([Slide(d, k) for k in range(n)])
    names = []
    for k, im in enumerate(d.render()):
        name = f"{pid}-wc-{k + 1}.jpg"
        path = os.path.join(TILES, name)
        if os.path.exists(path) and os.environ.get("WC_OVERWRITE_DRAFT") != name.split("-wc-")[0]:
            raise SystemExit(f"{name} exists: never overwrite a tile")
        im.save(path, quality=86, optimize=True, progressive=True)
        names.append(name)
    deck = os.path.join(DECKS, d.pptx_name())
    d.pptx(deck)
    return names, deck


# ================================================================== p20
def p20(s):
    a = s[0]
    a.heading("What happens inside a compost pile?", size=80)
    a.art("p20-pile-a")
    a.logo()

    b = s[1]
    b.heading("Days 1 to 3: bacteria wake up and the pile heats up.")
    b.art("p20-bacteria-b")
    b.logo()

    c = s[2]
    c.heading("The hot phase kills weed seeds and pathogens.")
    c.art("p20-seeds-b")
    c.logo()

    e = s[3]
    e.heading("You turn it to bring air back in.", size=80)
    e.art("p20-turn-c")
    e.logo()

    f = s[4]
    f.heading("As it cools, fungi and protozoa move in.")
    f.art("p20-fungi-b")
    f.logo()

    g = s[5]
    g.heading("Learn it properly in the Compost Intensive, starts 18 January.")
    g.art("p20-hands-a")
    g.logo()


POSTS = {"p20": ("2026-11-02", "inside-a-compost-pile-wc", 6, p20)}

if __name__ == "__main__":
    for pid in sys.argv[1:]:
        iso, slug, n, fn = POSTS[pid]
        print(build(pid, iso, slug, n, fn, seed=sum(map(ord, pid))))
