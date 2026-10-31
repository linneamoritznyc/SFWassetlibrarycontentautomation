"""27 Oct fixes from Linnea's notes, seven posts (worker redos).

No AI pictures anywhere. Photos are real SFW photos from the catalog. Everything else is drawn here in
code: watercolor-style washes (layered, multiplied glazes with soft edges, darker rims and pigment
variation, made with numpy and PIL), Natural Earth maps (public domain, 1:50m countries and 1:10m
provinces) painted the same way, and simple diagrams. Brand fonts only: Montserrat, Pathway Gothic One,
Source Sans 3. No gradients, no gold, no purple, no slide counters.

  BOX_SRC=<catalog photos> SFW_FONTS=<woff2 dir> GEO_DIR=<natural earth geojson dir> \
    python3 tools/wormhole-visuals/fix_1027.py [post ids...]
    -> apps/web/public/wormhole/tiles/<id>-f1-<n>.jpg   (never overwrites; FIX_REDO=1 to rebuild)

Posts: j20270103 (new slide 1 photo), j20270124 (Field Notes No. 03, Josh Cheng), j20270125 (slide 2
micrograph), j20270127 (watercolor loop), j20270128b (New Mexico, educational copy), j20270130 (Fun Soil
News, maps and watercolor), st20261201 (Costa Rica stories, new crops and box).
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.environ.get("FIX_OUT") or os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
BRAND = os.path.join(REPO, "apps", "web", "public", "wormhole", "brand")
SRC = os.environ.get("BOX_SRC", "")
FONTS = os.environ.get("SFW_FONTS", "")
GEO = os.environ.get("GEO_DIR", "")

W, H = 1080, 1350
CREAM, DEEP, FWG, BROWN, BLUE = "#F4F1EA", "#22371F", "#156826", "#4F3433", "#3780B8"
TAN, LGREEN, SAND, MIST, INK = "#C89B7B", "#59A66C", "#D8C3A5", "#A7C6D9", "#333130"
TAN_T, LG_T = "#EEE1D7", "#D5E9DA"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ------------------------------------------------------------------ type
FONT_FILES = {
    "mont8": "montserrat-latin-800-normal.woff2",
    "mont7": "montserrat-latin-700-normal.woff2",
    "path": "pathway-gothic-one-latin-400-normal.woff2",
    "sans": "source-sans-3-latin-400-normal.woff2",
    "sans6": "source-sans-3-latin-600-normal.woff2",
}
_fc = {}


def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONTS, FONT_FILES[kind]), size)
    return _fc[k]


def _tw(d, s, f, track):
    return d.textlength(s, font=f) + track * max(0, len(s) - 1)


def wrap(d, text, f, width, track=0):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if _tw(d, t, f, track) <= width or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text(im, s, x, y, w, size, kind="mont7", color=BROWN, lh=1.12, align="left", track=0, h=None, min_size=None):
    """Draws wrapped text with its cap top at y; shrinks to fit h. Returns the bottom y."""
    d = ImageDraw.Draw(im)
    min_size = min_size or int(size * 0.6)
    while True:
        f = font(kind, size)
        lines = wrap(d, s, f, w, track)
        tot = round(size * lh) * len(lines)
        if h is None or tot <= h or size <= min_size:
            break
        size -= 2
    cy = y
    top = f.getbbox("H")[1]
    for ln in lines:
        lw = _tw(d, ln, f, track)
        lx = x if align == "left" else (x + (w - lw) / 2 if align == "center" else x + w - lw)
        if track:
            tx = lx
            for ch in ln:
                d.text((tx, cy - top), ch, font=f, fill=color)
                tx += d.textlength(ch, font=f) + track
        else:
            d.text((lx, cy - top), ln, font=f, fill=color)
        cy += round(size * lh)
    return cy - round(size * (lh - 1)) - top * 0  # bottom of the last line box


def label(im, s, x, y, size=40, color=FWG, track=2, w=900, align="left"):
    return text(im, s, x, y, w, size, kind="path", color=color, lh=1.1, track=track, align=align)


# ------------------------------------------------------------------ logo and photos
def logo(im, dark=False, size=140, x=None, y=None):
    f = "sfw-foundation-logo-white.png" if dark else "sfw-foundation-logo-colour.png"
    lg = Image.open(os.path.join(BRAND, f)).convert("RGBA")
    box = lg.getchannel("A").getbbox()
    lg = lg.crop(box)
    lg = lg.resize((size, round(lg.height * size / lg.width)), Image.LANCZOS)
    x = im.width - 56 - lg.width if x is None else x
    y = im.height - 50 - lg.height if y is None else y
    im.paste(lg, (round(x), round(y)), lg)
    return lg.size


def load(name):
    return ImageOps.exif_transpose(Image.open(os.path.join(SRC, name))).convert("RGB")


def cover(name, w, h, fx=0.5, fy=0.5, zoom=1.0, rect=None):
    """Crop to w x h. rect=(x0, y0, x1, y1) in source pixels picks an exact window (aspect is fixed to w/h,
    centred on the rect)."""
    im = load(name)
    if rect:
        x0, y0, x1, y1 = rect
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rw, rh = x1 - x0, y1 - y0
        if rw / rh > w / h:
            rh = rw * h / w
        else:
            rw = rh * w / h
        x0 = min(max(0, cx - rw / 2), im.width - rw)
        y0 = min(max(0, cy - rh / 2), im.height - rh)
        assert rw <= im.width + 1 and rh <= im.height + 1, (name, rect)
        return im.crop((round(x0), round(y0), round(x0 + rw), round(y0 + rh))).resize((w, h), Image.LANCZOS)
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx)
    y = round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def framed(im, name, x, y, w, h, line=BROWN, **kw):
    ph = cover(name, w, h, **kw)
    d = ImageDraw.Draw(im)
    d.rectangle((x - 4, y - 4, x + w + 3, y + h + 3), fill=line)
    im.paste(ph, (x, y))


def lens(im, name, cx, cy, d, fx=0.5, fy=0.5, zoom=1.0):
    """A micrograph seen through the eyepiece: round field, dark rim (as collage.lens)."""
    ring = max(10, d // 28)
    ph = cover(name, d - 2 * ring, d - 2 * ring, fx, fy, zoom)
    out = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    m = Image.new("L", (d * 3, d * 3), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d * 3 - 1, d * 3 - 1), fill=255)
    rim = Image.new("RGBA", (d, d), rgb("#1B1B18") + (255,))
    rim.putalpha(m.resize((d, d), Image.LANCZOS))
    out.alpha_composite(rim)
    pd = d - 2 * ring
    m2 = Image.new("L", (pd * 3, pd * 3), 0)
    ImageDraw.Draw(m2).ellipse((0, 0, pd * 3 - 1, pd * 3 - 1), fill=255)
    ph = ph.convert("RGBA")
    ph.putalpha(m2.resize((pd, pd), Image.LANCZOS))
    out.alpha_composite(ph, (ring, ring))
    im.paste(out, (round(cx - d / 2), round(cy - d / 2)), out)


# ------------------------------------------------------------------ watercolor, drawn in code
def smooth_noise(h, w, cell, seed, lo=0.0, hi=1.0):
    r = np.random.default_rng(seed)
    g = r.random((max(2, h // cell + 2), max(2, w // cell + 2)))
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    a = np.asarray(im).astype(np.float32) / 255
    return lo + (hi - lo) * a


def blur(a, r):
    if r <= 0:
        return a
    im = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255


def jitter_poly(pts, amp, seed, step=6.0, freq=0.035):
    """Subdivides a closed polygon and moves each point along its normal by smooth noise."""
    r = random.Random(seed)
    ph = [r.uniform(0, 6.3) for _ in range(4)]
    fr = [freq, freq * 2.3, freq * 5.1, freq * 11.0]
    am = [1.0, 0.5, 0.25, 0.12]
    out, s = [], 0.0
    n = len(pts)
    for i in range(n):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
        L = math.hypot(bx - ax, by - ay)
        k = max(1, int(L / step))
        nx, ny = (-(by - ay) / L, (bx - ax) / L) if L else (0, 0)
        for j in range(k):
            t = j / k
            off = amp * sum(a * math.sin(s * f + p) for a, f, p in zip(am, fr, ph)) / 1.87
            out.append((ax + (bx - ax) * t + nx * off, ay + (by - ay) * t + ny * off))
            s += L / k
    return out


class Paper:
    """A flat paper colour; paint is glazed on with a multiply blend, like transparent watercolor."""

    def __init__(self, w, h, color=CREAM):
        self.w, self.h = w, h
        self.a = np.ones((h, w, 3), np.float32) * (np.array(rgb(color), np.float32) / 255)

    def poly_mask(self, polys, ss=2):
        m = Image.new("L", (self.w * ss, self.h * ss), 0)
        d = ImageDraw.Draw(m)
        for p in polys:
            if len(p) >= 3:
                d.polygon([(x * ss, y * ss) for x, y in p], fill=255)
        return np.asarray(m.resize((self.w, self.h), Image.LANCZOS)).astype(np.float32) / 255

    def wash(self, polys, color, opacity=0.75, seed=1, amp=4.0, layers=3, rim=0.55, mottle=0.25, cell=60,
             jitter=True, soft=1.2, freq=0.035):
        """One watercolor wash over one or more polygons: soft uneven edges, darker rim, mottled pigment."""
        acc = np.zeros((self.h, self.w), np.float32)
        for l in range(layers):
            ps = [jitter_poly(p, amp, seed * 31 + l * 7 + i, freq=freq) if jitter else p for i, p in enumerate(polys)]
            acc += self.poly_mask(ps)
        m = blur(acc / layers, soft)
        self.glaze_mask(m, color, opacity, seed, rim, mottle, cell)
        return m

    def glaze_mask(self, m, color, opacity=0.75, seed=1, rim=0.55, mottle=0.25, cell=60):
        edge = np.clip(m - blur(m, 7), 0, 1) * 2.2
        n = smooth_noise(self.h, self.w, cell, seed, 1 - mottle, 1 + mottle * 0.4)
        fine = smooth_noise(self.h, self.w, 9, seed + 5, 0.9, 1.05)
        dens = np.clip((m * n * fine) * (1 - rim * 0.35) + edge * rim, 0, 1) * opacity
        c = np.array(rgb(color), np.float32) / 255
        self.a *= 1 - dens[..., None] * (1 - c)

    def lines(self, paths, color, width=3.0, opacity=0.8, mode="glaze", seed=3):
        """Brush lines (roots, stems, hyphae). mode 'gouache' paints opaque light colour over dark washes."""
        ss = 2
        m = Image.new("L", (self.w * ss, self.h * ss), 0)
        d = ImageDraw.Draw(m)
        for p in paths:
            wv = p[1] if isinstance(p, tuple) else width
            pts = p[0] if isinstance(p, tuple) else p
            d.line([(x * ss, y * ss) for x, y in pts], fill=255, width=max(1, round(wv * ss)), joint="curve")
        a = np.asarray(m.resize((self.w, self.h), Image.LANCZOS)).astype(np.float32) / 255
        a = blur(a, 0.6) * smooth_noise(self.h, self.w, 14, seed, 0.75, 1.0) * opacity
        c = np.array(rgb(color), np.float32) / 255
        if mode == "gouache":
            self.a = self.a * (1 - a[..., None]) + c * a[..., None]
        else:
            self.a *= 1 - a[..., None] * (1 - c)

    def dots(self, pts, color, opacity=0.8, seed=4, mode="glaze"):
        """Small soft blobs: soil crumbs, bacteria, markers. pts = [(x, y, rx, ry, angle)]."""
        polys = []
        for x, y, rx, ry, ang in pts:
            ca, sa = math.cos(ang), math.sin(ang)
            n = max(10, int((rx + ry) * 1.2))
            polys.append([(x + rx * math.cos(t) * ca - ry * math.sin(t) * sa,
                           y + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
                          for t in (2 * math.pi * i / n for i in range(n))])
        m = blur(self.poly_mask(polys), 0.7)
        if mode == "gouache":
            c = np.array(rgb(color), np.float32) / 255
            a = m * opacity
            self.a = self.a * (1 - a[..., None]) + c * a[..., None]
        else:
            self.glaze_mask(m, color, opacity, seed, rim=0.4, mottle=0.15, cell=20)

    def image(self):
        return Image.fromarray(np.clip(self.a * 255, 0, 255).astype(np.uint8), "RGB")


def ellipse_poly(cx, cy, rx, ry, ang=0.0, n=64):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(t) * ca - ry * math.sin(t) * sa, cy + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
            for t in (2 * math.pi * i / n for i in range(n))]


def leaf_poly(x, y, length, width, ang, n=40):
    """A pointed leaf from its base point (x, y) along angle ang."""
    pts = []
    for i in range(n + 1):
        t = i / n
        r = width * math.sin(math.pi * t) ** 0.85
        pts.append((t * length, r))
    pts += [(t, -r) for t, r in reversed(pts[1:-1])]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]


def branch(x, y, ang, length, seed, steps=14, spread=0.35, kids=2, depth=0, maxd=3, droop=0.0):
    """Random-walk branching paths (roots, hyphae). Returns [(points, width)]."""
    r = random.Random(seed)
    out = []
    pts = [(x, y)]
    a = ang
    seg = length / steps
    for i in range(steps):
        a += r.uniform(-spread, spread) + droop
        x, y = x + seg * math.cos(a), y + seg * math.sin(a)
        pts.append((x, y))
        if depth < maxd and i > 2 and r.random() < kids / steps:
            out += branch(x, y, a + r.choice((-1, 1)) * r.uniform(0.5, 1.0), length * 0.55, seed * 7 + i,
                          max(5, steps // 2), spread, kids, depth + 1, maxd, droop)
    out.insert(0, (pts, max(1.2, 3.4 - depth * 0.9)))
    return out


def arrow(p, p0, p1, bend=0.25, color=BROWN, width=3.0, head=18):
    """A thin curved arrow drawn as a brush line."""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)
           for t in (i / 40 for i in range(41))]
    tx, ty = pts[-1][0] - pts[-4][0], pts[-1][1] - pts[-4][1]
    a = math.atan2(ty, tx)
    h1 = [(x1 - head * math.cos(a - 0.45), y1 - head * math.sin(a - 0.45)), (x1, y1),
          (x1 - head * math.cos(a + 0.45), y1 - head * math.sin(a + 0.45))]
    p.lines([pts, h1], color, width=width, opacity=0.9)


# ------------------------------------------------------------------ maps (Natural Earth, public domain)
_geo = {}


def geo(name):
    if name not in _geo:
        _geo[name] = json.load(open(os.path.join(GEO, name + ".geojson")))
    return _geo[name]


def rings(feature):
    g = feature["geometry"]
    if g is None:
        return []
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return [p[0] for p in polys]


def country(name):
    for f in geo("ne_50m_admin_0_countries")["features"]:
        pr = f["properties"]
        if name in (pr.get("ADMIN"), pr.get("NAME"), pr.get("NAME_LONG")):
            return rings(f)
    raise KeyError(name)


def province(name, adm0):
    for f in geo("ne_10m_admin_1_states_provinces")["features"]:
        pr = f["properties"]
        if pr.get("name") == name and pr.get("admin") == adm0:
            return rings(f)
    raise KeyError(name)


class Proj:
    """Equirectangular, scaled by cos(mid latitude), fitted into a pixel box."""

    def __init__(self, lon0, lon1, lat0, lat1, box):
        self.lon0, self.lat1 = lon0, lat1
        self.k = math.cos(math.radians((lat0 + lat1) / 2))
        x0, y0, x1, y1 = box
        sx = (x1 - x0) / ((lon1 - lon0) * self.k)
        sy = (y1 - y0) / (lat1 - lat0)
        self.s = min(sx, sy)
        self.ox = x0 + ((x1 - x0) - (lon1 - lon0) * self.k * self.s) / 2
        self.oy = y0 + ((y1 - y0) - (lat1 - lat0) * self.s) / 2

    def __call__(self, lon, lat):
        return self.ox + (lon - self.lon0) * self.k * self.s, self.oy + (self.lat1 - lat) * self.s

    def ring(self, r):
        return [self(lon, lat) for lon, lat in r]


def paint_map(p, pr, shapes, color, opacity=0.7, seed=1, amp=0.0):
    polys = [pr.ring(r) for r in shapes]
    polys = [q for q in polys if len(q) > 2]
    return p.wash(polys, color, opacity, seed=seed, amp=amp, layers=2, rim=0.5, mottle=0.22, cell=45,
                  jitter=amp > 0, soft=0.8)


def marker(p, x, y, r=16, color=BROWN):
    p.dots([(x, y, r, r, 0)], color, opacity=0.95, seed=int(x + y))


# ------------------------------------------------------------------ output
DONE = []


def save(im, pid, n):
    fn = f"{pid}-f1-{n}.jpg"
    path = os.path.join(OUT, fn)
    if os.path.exists(path) and not os.environ.get("FIX_REDO"):
        raise SystemExit(f"exists, not overwriting: {path}")
    im.convert("RGB").save(path, quality=88, optimize=True, progressive=True)
    DONE.append(fn)
    print(fn, im.size)
    return fn


POSTS = {}


def post(pid):
    def wrap_(fn):
        POSTS[pid] = fn
        return fn
    return wrap_


# ================================================================== 1. j20270103: new slide 1 photo
@post("j20270103")
def cic():
    """K, framed photo: same layout as the v5 tile, new photo (compost thermometer and fork in a pile)."""
    im = Image.new("RGB", (W, H), CREAM)
    label(im, "COMPOST INTENSIVE COURSE", 90, 80)
    text(im, "The January cohort starts this month.", 90, 140, 900, 78, h=300)
    framed(im, "R5A_3996.jpg", 90, 470, 900, 620, fx=0.5, fy=0.45)
    text(im, "Link in bio.", 90, 1130, 880, 40, kind="sans", color=BROWN)
    text(im, "Photo: Brevity Media for the Soil Food Web Foundation", 90, H - 74, 640, 22, kind="sans", color=INK)
    logo(im)
    save(im, "j20270103", 1)


# ================================================================== 3. j20270125: slide 2 micrograph
@post("j20270125")
def hyphae():
    """F, specimen: same layout as the v5 slide 2, a long septate hypha (Jen Ralston, SFW library)."""
    im = Image.new("RGB", (W, H), DEEP)
    text(im, "Hyphae on your slide mean fungi growing and working now.", 90, 140, 900, 70, color=CREAM, h=330)
    lens(im, "Fungal hypha, 40x obj, Jen Ralston.jpg", W / 2, H / 2 + 160, 620, fx=0.42, fy=0.5)
    text(im, "Micrograph: SFW library, Jen Ralston", 90, H - 74, 640, 22, kind="sans", color="#E3DDCC")
    logo(im, dark=True)
    save(im, "j20270125", 2)


# ================================================================== 4. j20270127: produce no waste
def soil_block(p, x0, y0, x1, y1, seed, mulch=True):
    """A watercolor cut-away of soil: brown layers, crumbs, pores, with mulch on top."""
    r = random.Random(seed)
    p.wash([[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], "#8A6A52", 0.85, seed=seed, amp=3)
    p.wash([[(x0, y0 + (y1 - y0) * 0.45), (x1, y0 + (y1 - y0) * 0.4), (x1, y1), (x0, y1)]], "#6E5240", 0.55,
           seed=seed + 1, amp=5)
    crumbs = [(r.uniform(x0 + 10, x1 - 10), r.uniform(y0 + 30, y1 - 12), r.uniform(4, 11), r.uniform(3, 8),
               r.uniform(0, 3)) for _ in range(int((x1 - x0) * (y1 - y0) / 2600))]
    p.dots(crumbs, "#4F3433", 0.55, seed=seed + 2)
    pores = [(r.uniform(x0 + 10, x1 - 10), r.uniform(y0 + 40, y1 - 12), r.uniform(2, 5), r.uniform(2, 4), 0)
             for _ in range(int((x1 - x0) * (y1 - y0) / 4200))]
    p.dots(pores, "#F1E7D6", 0.75, mode="gouache")
    if mulch:
        chips = []
        for _ in range(int((x1 - x0) / 5)):
            cx = r.uniform(x0 + 6, x1 - 6)
            cy = y0 - r.uniform(-6, 26)
            chips.append(leaf_poly(cx, cy, r.uniform(26, 48), r.uniform(5, 9), r.uniform(-0.5, 0.5) + r.choice((0, math.pi))))
        for i, col in enumerate(("#C89B7B", "#B07A4F", "#D8B27A")):
            p.wash(chips[i::3], col, 0.8, seed=seed + 10 + i, amp=1.2, layers=2)


def lettuce(p, cx, cy, s, seed, ang0=0.0):
    """A loose-leaf lettuce seen from the side: broad ruffled leaves fanning up from one base point (cx, cy),
    darker outer leaves, paler inner ones, pale midribs."""
    r = random.Random(seed)

    def leaves(angles, ln, wd):
        out = []
        for a in angles:
            a = math.radians(a) + ang0 + r.uniform(-0.06, 0.06)
            L = ln * r.uniform(0.92, 1.05)
            mx, my = cx + math.cos(a) * L * 0.55, cy + math.sin(a) * L * 0.55
            out.append(ellipse_poly(mx, my, L * 0.55, L * wd, a, n=90))
        return out, angles
    outer, oa = leaves((-168, -142, -38, -12), s, 0.36)
    mid, ma = leaves((-128, -104, -76, -52), s * 0.95, 0.34)
    inner, ia = leaves((-112, -90, -68), s * 0.72, 0.3)
    p.wash(outer, "#5E9A4E", 0.8, seed=seed, amp=s * 0.05, rim=0.7, freq=0.16)
    p.wash(mid, "#86B95E", 0.75, seed=seed + 2, amp=s * 0.05, rim=0.65, freq=0.16)
    p.wash(inner, "#BCD982", 0.75, seed=seed + 4, amp=s * 0.04, rim=0.6, freq=0.18)
    ribs = []
    for angs, L in ((oa, s), (ma, s * 0.95), (ia, s * 0.72)):
        for a in angs:
            a = math.radians(a) + ang0
            ribs.append(([(cx, cy), (cx + math.cos(a) * L * 0.85, cy + math.sin(a) * L * 0.85)], max(1.5, s / 60)))
    p.lines(ribs, "#EEF4DC", opacity=0.6, mode="gouache")


@post("j20270127")
def no_waste():
    """H, diagram drawn as a watercolor loop: a pruned shrub drops its prunings, they become mulch,
    fungi and roots work in the soil under it, a new plant grows. No photo, no AI."""
    p = Paper(W, H, CREAM)
    # ground: a wide soil cut-away across the lower half
    soil_block(p, 90, 860, 990, 1160, seed=11)
    # hyphae in the soil under the mulch, white gouache threads
    hy = []
    for i, x in enumerate(range(140, 980, 70)):
        hy += branch(x, 880, math.pi / 2 + random.Random(i).uniform(-0.6, 0.6), 160, seed=100 + i, steps=12,
                     spread=0.4, kids=2, maxd=2)
    p.lines([(pts, 1.4) for pts, w in hy], "#F7F2E6", opacity=0.7, mode="gouache")
    # the shrub on the left: trunk, branches, leaves
    trunk = [([(300, 862), (296, 760), (288, 660), (270, 560)], 16), ([(292, 700), (360, 600), (420, 540)], 9),
             ([(286, 640), (220, 560), (180, 500)], 8), ([(270, 560), (260, 470)], 7)]
    p.lines(trunk, "#6E5240", opacity=0.85)
    r = random.Random(5)
    leaves = []
    for (bx, by) in ((420, 540), (180, 500), (260, 470), (360, 600), (220, 560), (300, 520)):
        for _ in range(7):
            leaves.append(leaf_poly(bx + r.uniform(-30, 30), by + r.uniform(-30, 30), r.uniform(48, 70), r.uniform(14, 20),
                                    r.uniform(0, 6.28)))
    p.wash(leaves[0::2], "#59A66C", 0.75, seed=21, amp=2)
    p.wash(leaves[1::2], "#86B85A", 0.7, seed=22, amp=2)
    # prunings falling: cut twigs with leaves between the shrub and the mulch
    tw = [([(470, 640), (530, 610)], 5), ([(520, 730), (585, 750)], 5), ([(450, 800), (505, 780)], 5)]
    p.lines(tw, "#6E5240", opacity=0.85)
    fall = [leaf_poly(530, 610, 40, 12, -0.8), leaf_poly(585, 750, 40, 12, 0.6), leaf_poly(505, 780, 38, 12, -1.2)]
    p.wash(fall, "#C9A35A", 0.7, seed=23, amp=1.5)
    # roots under the shrub, and a young plant on the right with its roots
    roots = branch(300, 880, math.pi / 2, 230, seed=7, steps=16, spread=0.35, kids=3, maxd=3)
    roots += branch(760, 880, math.pi / 2, 170, seed=8, steps=14, spread=0.35, kids=3, maxd=2)
    p.lines(roots, "#3E2A22", opacity=0.75)
    p.lines([([(760, 872), (761, 800), (758, 730)], 6)], "#3F7F3C", opacity=0.85)
    p.wash([leaf_poly(758, 736, 120, 24, -2.55)], "#59A66C", 0.8, seed=31, amp=2.0)
    p.wash([leaf_poly(758, 736, 130, 25, -0.6)], "#7DB35C", 0.8, seed=32, amp=2.0)
    # the loop: prunings fall to the mulch, the soil feeds the new plant
    arrow(p, (470, 560), (600, 800), bend=-0.22)
    arrow(p, (690, 1000), (735, 900), bend=-0.25)
    im = p.image()
    label(im, "PERMACULTURE PRINCIPLE 6", 90, 80)
    text(im, "Produce no waste.", 90, 140, 900, 96, color=BROWN)
    lab = dict(size=34, color=BROWN, track=2, w=260)
    label(im, "PRUNINGS", 560, 610, **lab)
    label(im, "MULCH", 880, 800, **lab)
    label(im, "NEW GROWTH", 830, 650, **lab)
    label(im, "FUNGI AND ROOTS", 90, 1190, size=34, color=BROWN, track=2, w=420)
    logo(im)
    save(im, "j20270127", 1)


# ================================================================== 5. j20270128b: New Mexico, educational
NM_STEPS = [
    ("20260304_161051.jpg", dict(fx=0.5, fy=0.4), "Make and manage BioComplete™ Compost.",
     "Build a thermophilic pile, track it and keep it on course, with a mentor beside you."),
    ("20260304_132644.jpg", dict(fx=0.5, fy=0.45), "Brew biological liquid amendments.",
     "Compost extracts and teas, made to an inoculum grade you can rely on."),
    ("Beginner microscopy group.jpg", dict(fx=0.5, fy=0.5), "Check your own work under the microscope.",
     "Guided sessions for beginners and advanced practitioners."),
]


@post("j20270128b")
def nm():
    """J, numbered steps with a square photo: a giant numeral beside a framed square photo."""
    for k, (photo, crop, head, small) in enumerate(NM_STEPS, 1):
        im = Image.new("RGB", (W, H), TAN_T)
        framed(im, photo, 290, 90, 700, 700, line=BROWN, **crop)
        d = ImageDraw.Draw(im)
        f = font("mont8", 330)
        top = f.getbbox(str(k))[1]
        d.text((70, 80 - top), str(k), font=f, fill=FWG)
        y = text(im, head, 90, 860, 900, 64, h=170)
        text(im, small, 90, y + 30, 820, 38, kind="sans", color=INK, lh=1.25)
        label(im, "ACCELERATOR WORKSHOP · NEW MEXICO · 3 TO 14 MAY 2027", 90, 1225, size=34, track=2, w=760)
        text(im, "Photo: Soil Food Web Foundation, Synergia Ranch", 90, H - 74 + 34, 640, 20, kind="sans", color=INK)
        logo(im, size=140)
        save(im, "j20270128b", k)


# ================================================================== 6. j20270130: Fun Soil News
def world_cover():
    p = Paper(W, H, CREAM)
    pr = Proj(-168, 190, -50, 78, (20, 420, 1060, 1120))
    land = [r for f in geo("ne_50m_land")["features"] for r in rings(f) if max(la for lo, la in r) > -58]
    paint_map(p, pr, land, "#A9CDA0", 0.75, seed=3)
    spots = [(102.7, 25.0), (9.18, 47.66), (138.6, -34.93)]
    for lon, lat in spots:
        x, y = pr(lon, lat)
        marker(p, x, y, 17)
    im = p.image()
    label(im, "FUN SOIL NEWS", 90, 80)
    text(im, f"Three soil stories for {MONTH}.", 90, 140, 900, 84 if MONTH == "October" else 80, h=200)
    d = ImageDraw.Draw(im)
    names = ["YUNNAN, CHINA", "KONSTANZ, GERMANY", "ADELAIDE, AUSTRALIA"]
    offs = [(-40, -70), (-20, -72), (-160, 34)]
    for (lon, lat), n, (dx, dy) in zip(spots, names, offs):
        x, y = pr(lon, lat)
        label(im, n, x + dx, y + dy, size=34, color=BROWN, w=360)
    text(im, "Maps: Natural Earth", 90, H - 74, 640, 22, kind="sans", color=INK)
    logo(im)
    return im


def yunnan():
    p = Paper(W, H, CREAM)
    pr = Proj(72, 136, 17, 54, (60, 300, 1020, 1000))
    paint_map(p, pr, country("China"), "#CFE0C2", 0.8, seed=5)
    paint_map(p, pr, province("Yunnan", "China"), "#156826", 0.7, seed=6)
    im = p.image()
    label(im, "YUNNAN, CHINA", 90, 80)
    text(im, "A giant fungus grows up to 50 cm tall from oak roots.", 90, 140, 900, 64, h=240)
    text(im, "Dianjunus rex, a new family about 65 million years old.", 90, 1080, 760, 40, kind="sans", color=INK,
         lh=1.25)
    text(im, "Frontiers in Fungal Biology, 2026. Map: Natural Earth", 90, H - 74, 640, 22, kind="sans", color=INK)
    logo(im)
    return im


def konstanz():
    p = Paper(W, H, CREAM)
    # a bioplastic film, pale blue, with cell-sized holes eaten into it by rod bacteria
    film = [(130, 470), (950, 430), (980, 1000), (110, 1040)]
    p.wash([film], "#A7C6D9", 0.65, seed=41, amp=3, rim=0.7)
    r = random.Random(9)
    holes = []
    for _ in range(14):
        hx, hy = r.uniform(220, 880), r.uniform(540, 940)
        holes.append((hx, hy, r.uniform(26, 44), r.uniform(18, 30), r.uniform(0, 3)))
    p.dots(holes, CREAM, 0.95, mode="gouache")
    rods = []
    for hx, hy, rx, ry, a in holes:
        for _ in range(r.randint(1, 3)):
            t = r.uniform(0, 6.28)
            rods.append((hx + rx * math.cos(t), hy + ry * math.sin(t), 18, 7, t + math.pi / 2))
    for _ in range(10):
        rods.append((r.uniform(180, 900), r.uniform(520, 960), 18, 7, r.uniform(0, 3)))
    p.dots(rods, "#4F3433", 0.75, seed=43)
    # a small inset map of Germany, top right
    pr = Proj(5.5, 15.5, 47.0, 55.2, (730, 1060, 860, 1240))
    paint_map(p, pr, country("Germany"), "#CFE0C2", 0.85, seed=44)
    x, y = pr(9.18, 47.66)
    marker(p, x, y, 9)
    im = p.image()
    label(im, "KONSTANZ, GERMANY", 90, 80)
    text(im, "Forest soil bacteria eat holes in bioplastic.", 90, 140, 900, 64, h=240)
    text(im, "The films were gone in about 250 to 330 days. Ordinary polyethylene barely changed.", 90, 1080, 600,
         36, kind="sans", color=INK, lh=1.25)
    text(im, "The ISME Journal, 2026. Map: Natural Earth", 90, H - 74, 640, 22, kind="sans", color=INK)
    logo(im)
    return im


def adelaide():
    p = Paper(W, H, CREAM)
    pr = Proj(112, 155, -44.5, -9.5, (60, 320, 1020, 1040))
    paint_map(p, pr, country("Australia"), "#D8C3A5", 0.85, seed=51)
    paint_map(p, pr, province("South Australia", "Australia"), "#C89B7B", 0.6, seed=52)
    x, y = pr(138.6, -34.93)
    marker(p, x, y, 15)
    im = p.image()
    label(im, "SOUTH AUSTRALIA", 90, 80)
    text(im, "Six years after replanting, soil fungi are back at work.", 90, 140, 900, 64, h=240)
    text(im, "Their jobs kept recovering. The mix of species changed far less.", 90, 1090, 700, 38, kind="sans",
         color=INK, lh=1.25)
    text(im, "Flinders University, Molecular Ecology, 2026. Map: Natural Earth", 90, H - 74, 700, 22, kind="sans",
         color=INK)
    logo(im)
    return im


MONTH = "January"


@post("j20270130")
def news():
    for k, fn in enumerate((world_cover, yunnan, konstanz, adelaide), 1):
        save(fn(), "j20270130", k)


@post("p17")
def news_october():
    """Linnea, 30 Oct: these are October 2026 stories, so they belong in the October roundup, not January."""
    global MONTH
    MONTH = "October"
    for k, fn in enumerate((world_cover, yunnan, konstanz, adelaide), 1):
        save(fn(), "p17", k)


# ================================================================== 2. j20270124: Field Notes No. 03
def notebook():
    p = Paper(W, H, "#F7F3EA")
    return p


def ruled(im):
    d = ImageDraw.Draw(im)
    for y in range(240, H - 120, 64):
        d.line((90, y, 990, y), fill="#DCD5C5", width=2)
    d.line((150, 0, 150, H), fill="#D98A7B", width=3)


def fn_head(im, s, size=64, y=250, h=300):
    label(im, "FIELD NOTES No. 03", 190, 120, size=40, color=FWG, track=3)
    return text(im, s, 190, y, 800, size, h=h)


def fn_small(im, s, y, w=760):
    return text(im, s, 190, y, w, 38, kind="sans", color=INK, lh=1.3)


def fn_finish(im, credit=None):
    if credit:
        text(im, credit, 190, H - 74, 640, 22, kind="sans", color=INK)
    logo(im, size=140)


def fn_slide(draw, ruled_first=True):
    p = notebook()
    im = p.image()
    ruled(im)
    p.a = np.asarray(im).astype(np.float32) / 255
    draw(p)
    return p.image()


@post("j20270124")
def field_notes():
    pid = "j20270124"
    GY = (116.21, 33.53)  # Guoyang County seat

    # 1. the number and the place
    def s1(p):
        pr = Proj(73, 135, 18, 54, (190, 600, 1000, 1180))
        paint_map(p, pr, country("China"), "#CFE0C2", 0.85, seed=61)
        paint_map(p, pr, province("Anhui", "China"), "#156826", 0.75, seed=62)
        x, y = pr(*GY)
        marker(p, x, y, 6, color=BROWN)
    im = fn_slide(s1)
    fn_head(im, "28% more lettuce.", size=96, h=130)
    fn_small(im, "Guoyang County, Anhui Province, China", 400)
    fn_finish(im, "Map: Natural Earth")
    save(im, pid, 1)

    # 2. who ran it
    def s2(p):
        lettuce(p, 850, 560, 105, seed=71)
    im = fn_slide(s2)
    fn_head(im, "Josh Cheng", size=80, h=110)
    fn_small(im, "Certified Consultant, Guoyang County, Anhui Province, China", 360, w=520)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 190, 640, 980, 1160
    ph = Image.new("RGB", (x1 - x0, y1 - y0), "#FBF8F1")
    dp = ImageDraw.Draw(ph)
    for i in range(0, ph.width + ph.height, 44):
        dp.line((i - ph.height, ph.height, i, 0), fill="#E6DCCB", width=2)
    im.paste(ph, (x0, y0))
    d.rectangle((x0, y0, x1, y1), outline=BROWN, width=3)
    label(im, "PHOTO: JOSH CHENG IN HIS LETTUCE BEDS (FROM HIS TRIAL REPORT)", x0 + 60, (y0 + y1) // 2 - 22, size=34,
          color=BROWN, w=(x1 - x0) - 120, align="center", track=1)
    fn_finish(im)
    save(im, pid, 2)

    # 3. the question and the method: three treatments
    def s3(p):
        for i, x in enumerate((210, 470, 730)):
            soil_block(p, x, 820, x + 230, 960, seed=80 + i, mulch=False)
            lettuce(p, x + 62, 826, 56, seed=90 + i)
            lettuce(p, x + 166, 826, 50, seed=95 + i)
        r = random.Random(3)
        rods = [(r.uniform(225, 425), r.uniform(840, 945), 9, 4, r.uniform(0, 3)) for _ in range(18)]
        rods += [(r.uniform(745, 945), r.uniform(840, 945), 9, 4, r.uniform(0, 3)) for _ in range(18)]
        p.dots(rods, "#F3E9D2", 0.9, mode="gouache")
    im = fn_slide(s3)
    fn_head(im, "Biology, a nutrient product, or both?", size=64, h=170)
    fn_small(im, "Nine beds, three treatments, 50 days.", 470)
    for x, t in ((210, "BIOLOGY"), (470, "PRODUCT"), (730, "BOTH, PRODUCT AT HALF RATE")):
        label(im, t, x, 990, size=32, color=BROWN, w=230, track=1)
    fn_finish(im)
    save(im, pid, 3)

    # 4. what the soil did: water infiltration
    def s4(p):
        soil_block(p, 300, 820, 880, 1150, seed=101, mulch=False)
        r = random.Random(4)
        drops = []
        for _ in range(9):
            x, y = r.uniform(340, 840), r.uniform(640, 760)
            drops.append(ellipse_poly(x, y, 16, 22))
        p.wash(drops, "#3780B8", 0.6, seed=102, amp=1.5)
        streaks = []
        for i in range(8):
            x = 340 + i * 68 + r.uniform(-10, 10)
            streaks += branch(x, 830, math.pi / 2, 280, seed=110 + i, steps=12, spread=0.25, kids=1, maxd=1)
        streaks = [[(min(max(px, 312), 868), min(py, 1138)) for px, py in pts] for pts, w in streaks]
        p.lines([(pts, 7.0) for pts in streaks], "#3780B8", opacity=0.55)
    im = fn_slide(s4)
    fn_head(im, "126%", size=150, h=170)
    fn_small(im, "more water infiltration with biology plus the product at half rate.", 440, w=720)
    fn_finish(im)
    save(im, pid, 4)

    # 5. what the crop did
    def s5(p):
        soil_block(p, 190, 1040, 990, 1150, seed=123, mulch=False)
        lettuce(p, 420, 1046, 200, seed=121)
        lettuce(p, 770, 1046, 160, seed=122)
    im = fn_slide(s5)
    fn_head(im, "The combination grew the most lettuce.", size=64, h=170)
    fn_small(im, "It also carried the most bacteria all season.", 470)
    fn_finish(im)
    save(im, pid, 5)

    # 6. what did not work: an eyepiece view with bacteria and no protozoa or nematodes
    def s6(p):
        cx, cy, R = 585, 880, 270
        p.wash([ellipse_poly(cx, cy, R + 22, R + 22, n=120)], "#33302C", 0.9, seed=131, amp=0.0, jitter=False)
        p.a = np.asarray(_disc(p.image(), cx, cy, R)).astype(np.float32) / 255
        r = random.Random(6)
        rods = []
        while len(rods) < 70:
            x, y = r.uniform(cx - R, cx + R), r.uniform(cy - R, cy + R)
            if math.hypot(x - cx, y - cy) < R - 20:
                rods.append((x, y, r.uniform(7, 10), 3.5, r.uniform(0, 3)))
        p.dots(rods, "#6E5240", 0.7, seed=133)
        p.dots([(cx - 120, cy + 60, 34, 26, 0.3), (cx + 110, cy - 90, 26, 20, 1.1)], "#B98E5E", 0.45, seed=134)
    im = fn_slide(s6)
    fn_head(im, "Biology alone came last on most measures.", size=60, h=170)
    fn_small(im, "Protozoa and nematodes never established, on soil with 2% organic matter.", 460, w=740)
    fn_finish(im)
    save(im, pid, 6)

    # 7. his conclusion
    def s7(p):
        lettuce(p, 870, 1110, 95, seed=141)
    im = fn_slide(s7)
    label(im, "FIELD NOTES No. 03", 190, 120, size=40, color=FWG, track=3)
    d = ImageDraw.Draw(im)
    q = font("mont8", 200)
    d.text((182, 210 - q.getbbox("“")[1]), "“", font=q, fill=LGREEN)
    y = text(im, "Combining biology with a reduced nutrient input gave the highest yield, the highest bacterial "
                 "biomass, and the best soil structure.", 190, 370, 760, 54, h=470)
    text(im, "Josh Cheng", 190, y + 40, 700, 40, kind="path", color=FWG, track=2)
    fn_small(im, "Save this if you are mid-transition and deciding how fast to move.", 1010, w=560)
    fn_finish(im)
    save(im, pid, 7)


def _disc(im, cx, cy, R):
    """Paints a pale eyepiece field into the dark ring."""
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill="#EFEAD8")
    return im


# ================================================================== 7. st20261201: Costa Rica stories
SW, SH = 1080, 1920
STORY = [
    # Gerald and a student at the shelf of extraction kit: both men fully in frame, box over the plants and wall
    dict(photo="PXL_20251023_212203077.jpg", rect=(1180, 0, 2908, 3072), label="WHAT'S INCLUDED",
         head="10 days with mentors", small="Training, course materials\nand weekday lunch on site", box="cream",
         logo=True),
    # replaces PXL_20251022_191224781 (a landscape group shot: every 9:16 crop cut people in half and the
    # box sat on Gerald's face). Costa Rica, March 2025: a mentor standing over students at their microscopes.
    dict(photo="20250310_163510.jpg", rect=(1330, 0, 3060, 3076), label="WHO CAN JOIN",
         head="Foundation Courses students", small="Finish Foundation Course 3 before 18 January", box="green",
         hs=60, pad=40),
]


def story_frame(s):
    """A clean Instagram Story: photo edge to edge, one flat brand box across the top of the safe zone
    (y 260 to 1600), over plain wall or plants, never over a face. Logo inside the box on frame 1 only.
    The lower part stays free for the link sticker."""
    im = cover(s["photo"], SW, SH, rect=s.get("rect"), fx=s.get("fx", 0.5), fy=s.get("fy", 0.5))
    d = ImageDraw.Draw(im)
    fill, ink, lab, dark = {"cream": (CREAM, BROWN, FWG, False), "green": (FWG, CREAM, LG_T, True),
                            "brown": (BROWN, CREAM, LG_T, True)}[s["box"]]
    m, pad, hs = 64, s.get("pad", 52), s.get("hs", 74)
    bw = SW - 2 * m
    inner = bw - 2 * pad
    hl = wrap(d, s["head"], font("mont8", hs), inner)
    sl = wrap(d, s["small"], font("sans", 40), inner)
    lgh = 130 + 26 if s.get("logo") else 0
    hlh = round(hs * 1.13)
    bh = pad + lgh + 46 + 18 + len(hl) * hlh + 14 + len(sl) * 50 + pad - 14
    y0 = s.get("y", 280)
    assert 260 <= y0 and y0 + bh <= 1600, (y0, bh)
    d.rectangle((m, y0, m + bw, y0 + bh), fill=fill)
    if s.get("logo"):
        logo(im, dark=dark, size=150, x=m + pad, y=y0 + pad)
    y = y0 + pad + lgh
    label(im, s["label"], m + pad, y, size=46, color=lab, track=2, w=inner)
    y += 46 + 18
    y = text(im, s["head"], m + pad, y, inner, hs, kind="mont8", color=ink, lh=1.13)
    text(im, s["small"], m + pad, y + 14, inner, 40, kind="sans", color=ink, lh=1.25)
    return im, (m, y0, bw, bh)


@post("st20261201")
def costa():
    for k, s in enumerate(STORY, 1):
        im, box = story_frame(s)
        print("  box", box)
        save(im, "st20261201", k)


if __name__ == "__main__":
    for pid in sys.argv[1:] or list(POSTS):
        POSTS[pid]()
