"""Save Soil shoutouts: article repost cards, the format of the pinned New York Times post.

A white card on a dark grain background: the article's photo with an outlet tab, a
headline beside a green bar, a short line, then "Read More" and the source link below
the card. Carousel slides after the cover carry one fact each on the same card. The
grain runs as one strip across a carousel, so the slides join up when swiped.

  SAVESOIL_SRC=<photos> SFW_FONTS=<fonts> python3 tools/wormhole-visuals/savesoil.py
    -> apps/web/public/wormhole/tiles/ss-0N-v1-<n>.jpg
       (Instagram 1080 x 1350, LinkedIn 1200 x 627)

Photos: Save Soil's own farm photo for post 1; Wikimedia Commons (CC BY, CC BY-SA,
CC0, public domain) for the rest, credited on the card. Fonts: Poppins (OFL).
"""
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.environ.get("SAVESOIL_OUT", os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles"))
LOGO = os.path.join(REPO, "apps", "web", "public", "wormhole", "sfw-foundation-wordmark-240.png")
SRC = os.environ["SAVESOIL_SRC"]
FONTS = os.environ["SFW_FONTS"]

GREEN, DEEP, INK, CREAM = (47, 107, 70), (34, 55, 31), (30, 32, 29), (244, 241, 234)


def font(weight, size, italic=False, subset="latin"):
    f = ImageFont.truetype(os.path.join(FONTS, f"poppins-{subset}-{weight}-{'italic' if italic else 'normal'}.woff2"), size)
    f.spec = (weight, size, italic)
    return f


# The latin file stops at U+00FF; names like Bogušas need the latin-ext file.
PUNCT = set("‘’“”–—…•™")


def ext(ch):
    return ord(ch) > 0xFF and ch not in PUNCT


def draw(d, xy, text, f, fill):
    """Text with a per-letter fallback to latin-ext for the letters latin lacks."""
    if not any(ext(c) for c in text):
        d.text(xy, text, font=f, fill=fill)
        return
    fx = font(*f.spec[:2], italic=f.spec[2], subset="latin-ext")
    x, y = xy
    for c in text:
        g = fx if ext(c) else f
        d.text((x, y), c, font=g, fill=fill)
        x += d.textlength(c, font=g)


def grain(w, h, seed):
    """Dark, uneven grain in the brand's near-black green; no picture, only texture."""
    rng = np.random.default_rng(seed)
    n = np.zeros((h, w), np.float32)
    for cells, amp in [(5, 1.0), (14, 0.55), (40, 0.3), (130, 0.18)]:
        g = rng.random((max(2, h * cells // w + 2), cells + 2)).astype(np.float32)
        n += amp * np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    n = n / 2.03 + rng.normal(0, 0.06, (h, w)).astype(np.float32)
    n = np.clip((n - 0.25) * 1.6, 0, 1) ** 1.6
    lo, hi = np.array([22, 26, 22], np.float32), np.array([96, 102, 94], np.float32)
    rgb = lo + n[..., None] * (hi - lo)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def wrap(d, text, f, width, url=False):
    lines, cur = [], ""
    # A link has no spaces; break it after its slashes instead.
    words = text.replace("/", "/ ").split() if url else text.split()
    joiner = "" if url else " "
    for word in words:
        t = f"{cur}{joiner}{word}".strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def fit(d, text, weight, size, width, max_h, lh=1.18, min_size=26):
    """The biggest size at which the text fits the box."""
    while size > min_size:
        f = font(weight, size)
        lines = wrap(d, text, f, width)
        if len(lines) * size * lh <= max_h:
            return f, lines
        size -= 2
    f = font(weight, min_size)
    return f, wrap(d, text, f, width)


def block(d, x, y, lines, f, fill, lh=1.18):
    for i, ln in enumerate(lines):
        draw(d, (x, y + i * f.size * lh), ln, f, fill)
    return y + len(lines) * f.size * lh


def cover_crop(im, w, h, focus=(0.5, 0.5)):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    x = round((im.width - w) * focus[0])
    y = round((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def photo(name, crop=None):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((round(crop[0] * w), round(crop[1] * h), round(crop[2] * w), round(crop[3] * h)))
    return im


def logo(img, x, y, size):
    lg = Image.open(LOGO).convert("RGBA")
    lg.thumbnail((round(size * 0.8), round(size * 0.8)))
    disc = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, size - 1, size - 1), fill=(255, 255, 255, 255))
    disc.alpha_composite(lg, ((size - lg.width) // 2, (size - lg.height) // 2))
    img.paste(disc, (x, y), disc)


def bar_text(d, x, y, lines, f, bar_h=None):
    d.rectangle((x, y + 6, x + 9, y + (bar_h or len(lines) * f.size * 1.18) - 4), fill=GREEN)
    return block(d, x + 34, y, lines, f, INK)


def read_more(d, x, y, url, right, size=26):
    f = font(500, size)
    d.text((x, y), "Read More", font=f, fill=(235, 235, 230))
    cx = x + d.textlength("Read More", font=f) + 26
    cy = y + size * 0.62
    d.ellipse((cx - 15, cy - 15, cx + 15, cy + 15), fill=(235, 235, 230))
    d.polygon([(cx - 4, cy - 8), (cx + 7, cy), (cx - 4, cy + 8)], fill=INK)
    fs = font(400, size - 4)
    lines = ["Source:"] + wrap(d, url, fs, 520, url=True)
    for i, ln in enumerate(lines):
        d.text((right - d.textlength(ln, font=fs), y + i * (size + 4)), ln, font=fs, fill=(235, 235, 230))


def instagram(pid, post):
    n = 1 + len(post["facts"])
    W, H = 1080, 1350
    strip = grain(W * n, H, post["seed"])
    out = []
    for k in range(n):
        img = strip.crop((k * W, 0, (k + 1) * W, H))
        d = ImageDraw.Draw(img)
        cx0, cx1 = 140, 940
        if k == 0:
            hf, hl = fit(d, post["headline"], 600, 54, cx1 - cx0 - 96, 250)
            bf, bl = fit(d, post["blurb"], 400, 26, cx1 - cx0 - 96, 140, lh=1.35, min_size=20)
            body = 48 + len(hl) * hf.size * 1.18 + 18 + len(bl) * bf.size * 1.35 + 44
            total = 28 + 500 + body + 34 + 120
            cy0 = round((H - total) / 2) + 20
            cy1 = round(cy0 + 28 + 500 + body)
            d.rectangle((cx0, cy0, cx1, cy1), fill=(255, 255, 255))
            px0, py0, px1, py1 = cx0 + 28, cy0 + 28, cx1 - 28, cy0 + 28 + 500
            img.paste(cover_crop(post["photo"], px1 - px0, py1 - py0, post.get("focus", (0.5, 0.5))), (px0, py0))
            tf = font(500, 30, italic=True)
            tw = d.textlength("Save Soil", font=tf)
            d.rectangle((px0, py1 - 58, px0 + tw + 44, py1), fill=GREEN)
            d.text((px0 + 22, py1 - 50), "Save Soil", font=tf, fill=(255, 255, 255))
            cf = font(400, 17)
            d.text((px1 - d.textlength(post["credit"], font=cf), py1 + 8), post["credit"], font=cf, fill=(120, 120, 120))
            y = bar_text(d, px0, py1 + 48, hl, hf)
            block(d, px0 + 34, y + 18, bl, bf, (60, 60, 60), lh=1.35)
            read_more(d, cx0 + 6, cy1 + 34, post["url"], cx1)
        else:
            text = post["facts"][k - 1]
            cite = ""
            if text.endswith(")") and " (" in text:
                text, cite = text[: text.rindex(" (")], text[text.rindex(" (") + 2: -1]
            cy0, cy1 = 290, 1060
            d.rectangle((cx0, cy0, cx1, cy1), fill=(255, 255, 255))
            hf, hl = fit(d, text, 600, 64, cx1 - cx0 - 140, cy1 - cy0 - 200)
            th = len(hl) * hf.size * 1.18
            y = cy0 + (cy1 - cy0 - th - (60 if cite else 0)) / 2
            y = bar_text(d, cx0 + 56, y, hl, hf)
            if cite:
                draw(d, (cx0 + 90, y + 22), cite, font(400, 28), (90, 90, 90))
            if k == n - 1:
                f = font(400, 24)
                line = "From Save Soil (Isha Foundation). Full article: link in bio."
                d.text(((W - d.textlength(line, font=f)) / 2, cy1 + 40), line, font=f, fill=(225, 225, 220))
        logo(img, 46, 42 if k == 0 else 46, 74)
        out.append(img)
    return out


def linkedin(pid, post):
    W, H = 1200, 627
    img = grain(W, H, post["seed"])
    d = ImageDraw.Draw(img)
    cx0, cy0, cx1, cy1 = 40, 40, 1160, 530
    d.rectangle((cx0, cy0, cx1, cy1), fill=(255, 255, 255))
    px0, py0, px1, py1 = cx0 + 22, cy0 + 22, cx0 + 22 + 470, cy1 - 22
    img.paste(cover_crop(post["photo"], px1 - px0, py1 - py0, post.get("focus", (0.5, 0.5))), (px0, py0))
    tf = font(500, 24, italic=True)
    tw = d.textlength("Save Soil", font=tf)
    d.rectangle((px0, py1 - 46, px0 + tw + 36, py1), fill=GREEN)
    d.text((px0 + 18, py1 - 40), "Save Soil", font=tf, fill=(255, 255, 255))
    tx = px1 + 40
    hf, hl = fit(d, post["headline"], 600, 52, cx1 - tx - 70, 260)
    y = bar_text(d, tx, cy0 + 48, hl, hf)
    bf, bl = fit(d, post["blurb"], 400, 22, cx1 - tx - 70, cy1 - y - 70, lh=1.35, min_size=17)
    block(d, tx + 34, y + 18, bl, bf, (60, 60, 60), lh=1.35)
    cf = font(400, 15)
    d.text((cx1 - 26 - d.textlength(post["credit"], font=cf), cy1 - 34), post["credit"], font=cf, fill=(120, 120, 120))
    f = font(500, 20)
    d.text((cx0 + 4, cy1 + 30), "Read More", font=f, fill=(235, 235, 230))
    fs = font(400, 16)
    lines = wrap(d, post["url"].replace("https://", ""), fs, 760, url=True)
    lines[0] = "Source: " + lines[0]
    for i, ln in enumerate(lines[:2]):
        d.text((cx1 - d.textlength(ln, font=fs), cy1 + 22 + i * 22), ln, font=fs, fill=(235, 235, 230))
    return [img]


BASE = "https://consciousplanet.org/en/save-soil/news/"
POSTS = {
    "ss-01": dict(
        kind="ig", seed=301, photo=photo("p1.img"), credit="Photo: Save Soil (Isha Foundation)",
        url=BASE + "save-soil-movement-model-farm-proof-of-concept",
        headline="A coconut farm went from 0.86% to 2.33% soil organic matter",
        blurb="Save Soil's case study of Valluvan's farm in Tamil Nadu, India: \"Model Farm Proof of Concept\".",
        facts=[
            "Coconuts per tree: 90-100 before, 140 now. Nothing changed in the first three years.",
            "Fertiliser spending: under 10% of what it was. Workers: 1, down from 10-20.",
            "2018: over 1,200 mm of rain in a few days, after two years of drought.",
            "His neighbours' open wells stood 6-7 feet lower than his.",
            "What he did: leaf litter trenches between rows, mulch, layered crops, no burning, no summer ploughing.",
        ]),
    "ss-02": dict(
        kind="ig", seed=302, photo=photo("p2.img"), focus=(0.5, 0.55),
        credit="Photo: Donald Hobern, CC BY 2.0",
        url=BASE + "soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga",
        headline="5 numbers that show what soil life does",
        blurb="From Save Soil's paper \"Soil as a Lead Indicator of the Global Goal on Adaptation\".",
        facts=[
            "6x faster: water soaking into regenerative almond orchards (LaCanne et al. 2021)",
            "133% more microbial biomass carbon in regenerative organic soils (Mäder et al. 2025)",
            "2.4 to 13.5x more earthworm biomass in diversified rotations than in rye monoculture (Bogušas et al. 2022)",
            "+24% glomalin, the fungal protein that glues soil crumbs together, under perennial pasture (Abán et al. 2025)",
            "+38-137% maize yield in drought years in legume and manure systems (Lotter et al. 2003)",
        ]),
    "ss-03": dict(
        kind="li", seed=303, photo=photo("p3.img"), focus=(0.5, 0.4),
        credit="Photo: High-Level Champions, COP30 Belém, CC BY 4.0",
        url=BASE + "cop30-a-turning-point-for-climate-action-but-agriculture-and-soils-left-behind",
        headline="USD 1 trillion for energy. USD 9 billion for agriculture.",
        blurb="Save Soil's COP30 analysis: \"A Turning Point for Climate Action, but Agriculture and Soils Still Left Behind\".",
        facts=[]),
    "ss-04": dict(
        kind="li", seed=304, photo=photo("p4.img"), focus=(0.62, 0.5),
        credit="Photo: USDA NRCS South Dakota, public domain",
        url=BASE + "mitigating-climate-change-through-soil-revitalization-using-regenerative-ag",
        headline="Tilled soil released 21% more CO2. In low-carbon soil, 29%.",
        blurb="Meta-analysis of 46 studies, Abdalla et al. 2016. From Save Soil's paper on regenerative agriculture and climate.",
        facts=[]),
    "ss-05": dict(
        kind="ig", seed=305, photo=photo("p5.img"), focus=(0.45, 0.5),
        credit="Springtail on soil. Photo: Lewis Fausak, CC BY-SA 4.0",
        url=BASE + "soil-degradation-and-biodiversity-loss",
        headline="Soil may be home to 59% of all life on Earth",
        blurb="Anthony et al., PNAS 2023, in Save Soil's paper \"Soil Degradation and Biodiversity Loss\".",
        facts=[]),
    "ss-06": dict(
        kind="ig", seed=306, photo=photo("p6.img", crop=(0.04, 0.36, 0.96, 0.72)),
        credit="Mycorrhizal fungus in a maize root. Photo: Marc-André Selosse, CC0",
        url=BASE + "healthy-soil-and-healthy-humans",
        headline="Where you live shapes your gut more than your genes do",
        blurb="From Save Soil's paper \"Healthy Soil and Healthy Humans\".",
        facts=[
            "Baboons: the soil around them shaped their gut microbes 15x more strongly than their genetics",
            "People: under 8% of the gut microbiome is inherited (Rothschild et al. 2018)",
            "Mycorrhizal fungi carry copper, iron, nitrogen, phosphorus and zinc into crops",
            "Rhizobia in legume roots turn nitrogen from the air into plant food",
        ]),
    "ss-07": dict(
        kind="li", seed=307, photo=photo("p7.img"), focus=(0.5, 0.35),
        credit="Soil profile. Photo: Mclund, CC BY 4.0",
        url=BASE + "secure-soil-save-life",
        headline="Soil is becoming security policy.",
        blurb="\"Secure Soil, Save Life\", by the Aroura Soil Security Think Tank, IUCN WCEL and Save Soil.",
        facts=[]),
    "ss-08": dict(
        kind="ig", seed=308, photo=photo("p8.img"), focus=(0.5, 0.55),
        credit="Soil aggregate. Photo: Antonio Jordán, CC BY-SA 3.0",
        url=BASE + "the-soil-carbon-sponge",
        headline="Healthy soil cools the land",
        blurb="From Save Soil's report \"The Soil Carbon Sponge\", built on Walter Jehne's work.",
        facts=[
            "Water in soil evaporates through plants and carries heat away",
            "Bare, degraded soil can't hold that water, so the sun heats the air instead",
            "Cover crops and mulch keep the ground from baking",
            "Fungal threads and bacterial glues hold the sponge's pores open",
        ]),
}


if __name__ == "__main__":
    import sys
    random.seed(1)
    for pid in sys.argv[1:] or POSTS:
        post = POSTS[pid]
        imgs = instagram(pid, post) if post["kind"] == "ig" else linkedin(pid, post)
        for i, im in enumerate(imgs, 1):
            path = os.path.join(TILES, f"{pid}-v1-{i}.jpg")
            assert not os.path.exists(path), f"{path} exists; bump the version"
            im.save(path, quality=88, optimize=True, progressive=True)
        print(pid, len(imgs), "slides")
