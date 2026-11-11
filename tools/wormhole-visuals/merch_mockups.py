"""Mockups for the "Be the mycelium" merch, drawn in code (no stock templates, no AI): tote bags, tees, mug,
framed poster and a sticker. Each is 1600 x 1600; the print is multiplied into a generated fabric texture so it
reads as printed, not pasted.

  python3 tools/wormhole-visuals/merch_mockups.py <merch dir> <outdir>
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

N = 1600
K = 2
GREEN = (21, 104, 38)
DEEP = (12, 52, 24)
CREAM = (244, 241, 234)
rng = np.random.default_rng(4)


def surface(top=(236, 231, 222), bottom=(218, 210, 197)):
    t = np.linspace(0, 1, N)[:, None, None]
    a = np.array(top, np.float32) * (1 - t) + np.array(bottom, np.float32) * t
    a = np.repeat(a, N, axis=1) + rng.normal(0, 2.2, (N, N, 1))
    return Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")


def weave(n=N, strength=0.07, scale=1.0):
    """Canvas/cotton luminance texture around 1.0."""
    g = rng.normal(0, 1, (n, n)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 40) + 128).clip(0, 255).astype("uint8")).filter(
        ImageFilter.GaussianBlur(0.8 * scale))).astype(np.float32) / 128 - 1
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    w = 0.5 * np.sin(xx * 1.9 / scale) * np.sin(yy * 1.9 / scale)
    return 1 + strength * (g * 0.7 + w * 0.5)


def shadow(mask, off=(0, 18), blur=26, alpha=0.32):
    m = mask.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", mask.size, (40, 32, 24, 0))
    sh.putalpha(m)
    out = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    out.alpha_composite(sh, off)
    return out


def smooth_mask(poly, blur=1.2):
    m = Image.new("L", (N * K, N * K), 0)
    ImageDraw.Draw(m).polygon([(x * K, y * K) for x, y in poly], fill=255)
    return m.resize((N, N), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur))


def fabric_fill(mask, colour, tex, shade):
    """Garment: flat colour x weave x soft shading, cut by mask."""
    a = np.array(colour, np.float32)[None, None] * (tex * shade)[..., None]
    im = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    im.putalpha(mask)
    return im


def print_on(base, art, box, tex, ink=0.94):
    """Place art (RGBA) into box (x, y, w) and multiply its colour with the fabric texture."""
    x, y, w = box
    a = art.resize((w, round(art.height * w / art.width)), Image.LANCZOS)
    arr = np.asarray(a).astype(np.float32)
    t = tex[y:y + a.height, x:x + a.width][..., None]
    arr[..., :3] *= t
    arr[..., 3] *= ink
    base.alpha_composite(Image.fromarray(arr.clip(0, 255).astype("uint8")), (x, y))


def folds(n=N, lines=(), width=60, depth=0.08):
    """Soft shading: list of ((x0, y0), (x1, y1)) dark creases."""
    m = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(m)
    for (x0, y0), (x1, y1) in lines:
        d.line((x0, y0, x1, y1), fill=255, width=width)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(width * 0.7))).astype(np.float32) / 255
    return 1 - depth * m


# ------------------------------------------------------------------ tote
def tote(art, colour, name, out):
    bg = surface()
    x0, y0, x1, y1 = 330, 520, 1270, 1450
    tex = weave(strength=0.09, scale=1.3)
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    shade = (1 - 0.05 * ((xx - 800) / 470) ** 2) * (1 - 0.04 * (yy - y0) / (y1 - y0))
    shade *= folds(lines=[((470, 560), (430, 1430)), ((1150, 600), (1190, 1420))], width=50, depth=0.05)
    # handles: loops rising from the top edge
    hm = Image.new("L", (N * K, N * K), 0)
    hd = ImageDraw.Draw(hm)
    for cx in (560, 1040):
        pass
    hd.arc((520 * K, 150 * K, 1080 * K, 900 * K), 180, 360, fill=255, width=58 * K)
    hm = hm.resize((N, N), Image.LANCZOS)
    hcol = tuple(round(c * 0.9) for c in colour)
    handles = fabric_fill(hm, hcol, tex, np.ones((N, N), np.float32))
    body = smooth_mask([(x0, y0), (x1, y0), (x1 + 6, y1), (x0 - 6, y1)])
    bg.alpha_composite(shadow(ImageChops.lighter(body, hm)))
    bg.alpha_composite(handles)
    bag = fabric_fill(body, colour, tex, shade)
    bg.alpha_composite(bag)
    d = ImageDraw.Draw(bg)
    hem = tuple(round(c * 0.86) for c in colour)
    d.line((x0, y0 + 46, x1, y0 + 46), fill=hem + (150,), width=2)
    for x in range(x0 + 10, x1 - 10, 18):  # top hem stitching
        d.line((x, y0 + 30, x + 9, y0 + 30), fill=hem + (190,), width=3)
    print_on(bg, art, (x0 + 150, y0 + 130, (x1 - x0) - 300), tex)
    bg.convert("RGB").save(f"{out}/{name}.jpg", quality=92)


# ------------------------------------------------------------------ tee
TEE = [(650, 240), (520, 280), (300, 395), (228, 468), (332, 698), (442, 650), (455, 1432), (1145, 1432),
       (1158, 650), (1268, 698), (1372, 468), (1300, 395), (1080, 280), (950, 240)]


def chaikin(pts, n=3):
    for _ in range(n):
        q = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            q += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        q.append(pts[-1])
        pts = q
    return pts


def tee(art, colour, name, out):
    bg = surface()
    neck = [(650 + i * 300 / 30, 240 + math.sin(math.pi * i / 30) * 90) for i in range(31)]
    poly = TEE + neck[::-1]
    body = smooth_mask(poly, 1.6)
    tex = weave(strength=0.06, scale=0.9)
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    shade = 1 - 0.07 * ((xx - 800) / 400) ** 2
    shade *= folds(lines=[((470, 660), (560, 1420)), ((1130, 660), (1050, 1420)), ((450, 650), (330, 700)),
                          ((1150, 650), (1270, 700)), ((700, 1250), (900, 1400))], width=45, depth=0.07)
    bg.alpha_composite(shadow(body))
    shirt = fabric_fill(body, colour, tex, np.clip(shade, 0, 1.2))
    bg.alpha_composite(shirt)
    d = ImageDraw.Draw(bg)
    rib = tuple(round(c * 0.86) for c in colour)
    d.line([(x, y + 22) for x, y in neck], fill=rib + (255,), width=26, joint="curve")
    d.line([(x, y + 6) for x, y in neck], fill=rib + (160,), width=4, joint="curve")
    d.line((262, 520, 350, 690), fill=rib + (120,), width=3)   # sleeve hems
    d.line((1338, 520, 1250, 690), fill=rib + (120,), width=3)
    print_on(bg, art, (535, 400, 530), tex)
    bg.convert("RGB").save(f"{out}/{name}.jpg", quality=92)


# ------------------------------------------------------------------ mug
def mug(art, name, out):
    bg = surface()
    x0, x1, y0, y1 = 480, 1100, 470, 1220
    w, h = x1 - x0, y1 - y0
    body = Image.new("L", (N * K, N * K), 0)
    bd = ImageDraw.Draw(body)
    bd.rectangle((x0 * K, (y0 + 30) * K, x1 * K, (y1 - 30) * K), fill=255)
    bd.ellipse((x0 * K, (y1 - 60) * K, x1 * K, y1 * K), fill=255)
    bd.ellipse((x0 * K, y0 * K, x1 * K, (y0 + 60) * K), fill=255)
    hm = Image.new("L", (N * K, N * K), 0)
    ImageDraw.Draw(hm).ellipse((1030 * K, 620 * K, 1330 * K, 1040 * K), outline=255, width=62 * K)
    body = body.resize((N, N), Image.LANCZOS)
    hm = hm.resize((N, N), Image.LANCZOS)
    hm = ImageChops.subtract(hm, body)
    bg.alpha_composite(shadow(ImageChops.lighter(body, hm), off=(14, 22)))
    # cylinder shading
    u = np.clip((np.arange(N, dtype=np.float32) - x0) / w, 0, 1)
    cyl = 0.78 + 0.26 * np.clip(np.sin(np.pi * u), 0, 1) ** 0.6 + 0.10 * np.exp(-((u - 0.32) / 0.07) ** 2)
    shade = np.repeat(cyl[None], N, 0)
    white = (247, 246, 242)
    m_img = fabric_fill(body, white, np.ones((N, N), np.float32), shade)
    h_shade = np.repeat((0.9 + 0.1 * np.sin(np.linspace(0, np.pi, N)))[None], N, 0)
    bg.alpha_composite(fabric_fill(hm, white, np.ones((N, N), np.float32), h_shade * 0.92))
    bg.alpha_composite(m_img)
    # wrap the art around the cylinder: x on the mug = sin of the angle
    pw = 470
    a = art.resize((pw, pw), Image.LANCZOS)
    arr = np.asarray(a).astype(np.float32)
    cx = x0 + w * 0.44
    R = w / 2
    out_a = np.zeros((pw, w, 4), np.float32)
    for X in range(w):
        xs = (x0 + X - (x0 + R)) / R            # -1..1 across the mug
        ang = math.asin(max(-1, min(1, xs)))
        src = (ang * R - (cx - (x0 + R))) + pw / 2
        if 0 <= src < pw - 1:
            out_a[:, X] = arr[:, int(src)]
            out_a[:, X, 3] *= max(0, math.cos(ang)) ** 0.3
    out_a[..., :3] *= cyl[x0:x1][None, :, None]
    bg.alpha_composite(Image.fromarray(out_a.clip(0, 255).astype("uint8")), (x0, y0 + 150))
    d = ImageDraw.Draw(bg)
    d.ellipse((x0 + 8, y0 + 6, x1 - 8, y0 + 56), fill=(205, 200, 190, 255))      # inside rim
    d.ellipse((x0 + 8, y0 + 6, x1 - 8, y0 + 56), outline=(250, 249, 246, 255), width=8)
    bg.convert("RGB").save(f"{out}/{name}.jpg", quality=92)


# ------------------------------------------------------------------ poster
def poster(art_dark, name, out):
    wall = surface((231, 226, 216), (222, 215, 203))
    fw, fh = 860, 1075
    fx, fy = (N - fw) // 2, 230
    frame = Image.new("L", (N, N), 0)
    ImageDraw.Draw(frame).rectangle((fx, fy, fx + fw, fy + fh), fill=255)
    wall.alpha_composite(shadow(frame, off=(0, 26), blur=30, alpha=0.4))
    d = ImageDraw.Draw(wall)
    d.rectangle((fx, fy, fx + fw, fy + fh), fill=(30, 26, 22, 255))
    m = 34
    d.rectangle((fx + m, fy + m, fx + fw - m, fy + fh - m), fill=(246, 244, 238, 255))
    px0, py0, px1, py1 = fx + m + 70, fy + m + 70, fx + fw - m - 70, fy + fh - m - 70
    d.rectangle((px0, py0, px1, py1), fill=DEEP + (255,))
    pw = px1 - px0
    a = art_dark.resize((pw, pw), Image.LANCZOS)
    wall.alpha_composite(a, (px0, py0 + ((py1 - py0) - pw) // 2))
    # glass sheen
    g = Image.new("L", (N, N), 0)
    ImageDraw.Draw(g).polygon([(fx + m, fy + m), (fx + m + 260, fy + m), (fx + m, fy + m + 380)], fill=26)
    wall.alpha_composite(Image.merge("RGBA", (g.point(lambda v: 255),) * 3 + (g.filter(ImageFilter.GaussianBlur(30)),)))
    wall.convert("RGB").save(f"{out}/{name}.jpg", quality=92)


# ------------------------------------------------------------------ sticker
def sticker(art_dark, name, out):
    bg = surface()
    r = 430
    cx, cy = 800, 800
    m = Image.new("L", (N * K, N * K), 0)
    ImageDraw.Draw(m).ellipse(((cx - r - 34) * K, (cy - r - 34) * K, (cx + r + 34) * K, (cy + r + 34) * K), fill=255)
    m = m.resize((N, N), Image.LANCZOS)
    bg.alpha_composite(shadow(m, off=(0, 10), blur=14, alpha=0.35))
    st = Image.new("RGBA", (N, N), (252, 252, 250, 0))
    st.putalpha(m)
    bg.alpha_composite(st)
    inner = Image.new("L", (N * K, N * K), 0)
    ImageDraw.Draw(inner).ellipse(((cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K), fill=255)
    inner = inner.resize((N, N), Image.LANCZOS)
    disc = Image.new("RGBA", (N, N), DEEP + (255,))
    a = art_dark.resize((720, 720), Image.LANCZOS)
    disc.alpha_composite(a, (cx - 360, cy - 360 + 10))
    disc.putalpha(inner)
    bg.alpha_composite(disc)
    # vinyl sheen
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    s = np.clip(1 - np.hypot(xx - (cx - 200), yy - (cy - 260)) / 520, 0, 1) ** 2 * 40
    sh = Image.fromarray(np.dstack([np.full((N, N, 3), 255, np.float32), s * (np.asarray(m) / 255)]).astype("uint8"))
    bg.alpha_composite(sh)
    bg.convert("RGB").save(f"{out}/{name}.jpg", quality=92)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    light = Image.open(f"{src}/mycelium-bloom-print.png").convert("RGBA")             # mint/cream ink
    dark = Image.open(f"{src}/mycelium-bloom-print-dark-green.png").convert("RGBA")   # green ink
    tote(dark, (232, 222, 200), "tote-natural", out)
    tote(light, GREEN, "tote-green", out)
    tee(dark, (250, 249, 246), "tee-white", out)
    tee(light, DEEP, "tee-forest", out)
    mug(dark, "mug", out)
    poster(light, "poster", out)
    sticker(light, "sticker", out)
    print("done")
