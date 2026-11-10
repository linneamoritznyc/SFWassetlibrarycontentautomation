"""Suzanne Shea / Veterans Day, Linnea's final text (10 Nov screenshots), text unchanged. Soft look: full-bleed
photos with a frosted, green-tinted fade where the text sits (bottom on slide 1, top on slide 2); slide 3 photo only.

  python3 tools/wormhole-visuals/suzanne_final.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

from bundle_three_styles_v12 import T, height
from collage import Deck, cover
from nov_fill import DECKS, TILES
from suzanne_frost import grade

W, H = 1080, 1350
CREAM = "#F4F1EA"
V = "/home/user/sfwlib/social/veterans"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"


def frost(path, fx, fy, a0, a1, top=False):
    sharp = grade(cover(ImageOps.exif_transpose(Image.open(path)).convert("RGB"), W, H, fx, fy))
    blur = np.asarray(sharp.filter(ImageFilter.GaussianBlur(30))).astype(np.float32)
    deep = np.array([20, 50, 30], np.float32)
    frost_ = blur * 0.38 + deep * 0.62
    y = np.linspace(0, 1, H, dtype=np.float32)
    if top:
        y = 1 - y
    t = np.clip((y - a0) / (a1 - a0), 0, 1)
    t = (t * t * (3 - 2 * t))[:, None, None]
    out = np.asarray(sharp).astype(np.float32) * (1 - t) + frost_ * t
    return Image.fromarray(out.clip(0, 255).astype("uint8")).convert("RGBA")


def logo(d, k, x, y, w=170):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def wave_pair():
    """One continuous green wave across slides 2 and 3 (Linnea's sketch, 10 Nov): starts low on the left of slide 2,
    rises to the seam, dips in slide 3 and sweeps up to the right edge. A lighter wave sits just above for depth.
    Returns (piece for slide 2, piece for slide 3), each W x H."""
    from PIL import ImageDraw
    pts = [(-40, 1400), (313, 1345), (700, 1185), (1080, 1110), (1320, 1190), (1650, 1290), (1920, 1190),
           (2200, 980)]   # Linnea's shape (v24)

    def smooth(p, n=40):
        out = []
        P = [p[0]] + p + [p[-1]]
        for i in range(1, len(P) - 2):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            for j in range(n):
                t = j / n
                out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t * t
                                        + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t ** 3) for c in (0, 1)))
        out.append(p[-1])
        return out

    k = 2
    strip = Image.new("RGBA", (2 * W * k, H * k), (0, 0, 0, 0))
    dr = ImageDraw.Draw(strip)
    # Linnea's line, steadied: four anchor heights joined, then heavily smoothed so there are no bumps
    xs = np.arange(-400, 2 * W + 401, dtype=np.float32)
    ys = np.interp(xs, [-400, 0, 1080, 1650, 2160, 2560], [1420, 1390, 1110, 1270, 1000, 900])
    g = np.exp(-0.5 * (np.arange(-600, 601) / 190.0) ** 2)
    ys = np.convolve(ys, g / g.sum(), mode="same")
    keep = (xs >= -20) & (xs <= 2 * W + 20)
    curve = list(zip(xs[keep][::4], ys[keep][::4]))
    for dy, col in ((-30, (44, 72, 138, 255)), (-16, (244, 241, 234, 255)), (0, (21, 104, 38, 255))):
        line = [(x * k, (y + dy) * k) for x, y in curve]
        dr.polygon(line + [(2 * W * k + 80, H * k + 50), (-80, H * k + 50)], fill=col)
    strip = strip.resize((2 * W, H), Image.LANCZOS)
    return strip.crop((0, 0, W, H)), strip.crop((W, 0, 2 * W, H))


def straw(w, h, seed=0):
    """Wheat field (photo Linnea sent, 10 Nov), tinted into the brand green, used at 50% inside the green."""
    src = Image.open(f"{V}/wheat-linnea.jpg").convert("RGB")
    t = np.asarray(cover(src, w, h, 0.5, 0.75).convert("L")).astype(np.float32) / 255
    t = np.clip((t - t.mean()) * 1.8 + 0.5, 0, 1)
    g = np.array([16, 84, 30], np.float32)
    light = np.array([196, 214, 150], np.float32)
    rgb = g * (1 - t[..., None]) + light * t[..., None]
    return Image.fromarray(rgb.clip(0, 255).astype("uint8"))


def swoosh3():
    """One green swoosh across all 3 slides that carries the text (Linnea, 10 Nov): tall on slide 1, easing up over
    slide 2, dipping low on slide 3 to end at the logo. One green, one thin cream line on top; heights meet at seams."""
    from PIL import ImageDraw
    k = 2
    N = 2
    strip = Image.new("RGBA", (N * W * k, H * k), (0, 0, 0, 0))
    dr = ImageDraw.Draw(strip)
    xs = np.arange(-400, N * W + 401, dtype=np.float32)
    ys = np.interp(xs, [-400, 0, 620, 1080, 1570, 1920, 2160, 2560],
                   [930, 935, 950, 1000, 1185, 1175, 1120, 1080])
    g = np.exp(-0.5 * (np.arange(-600, 601) / 170.0) ** 2)
    ys = np.convolve(ys, g / g.sum(), mode="same")
    keep = (xs >= -20) & (xs <= N * W + 20)
    curve = list(zip(xs[keep][::4], ys[keep][::4]))
    for dy, col in ((-14, (244, 241, 234, 255)), (0, (21, 104, 38, 255))):
        line = [(x * k, (y + dy) * k) for x, y in curve]
        dr.polygon(line + [(N * W * k + 80, H * k + 50), (-80, H * k + 50)], fill=col)
    # real straw texture at 50% inside the green (Linnea, 10 Nov)
    mask = Image.new("L", strip.size, 0)
    ImageDraw.Draw(mask).polygon([(x * k, y * k) for x, y in curve] + [(N * W * k + 80, H * k + 50),
                                                                       (-80, H * k + 50)], fill=128)
    tex = straw(N * W * k, H * k).convert("RGBA")
    tex.putalpha(mask)
    strip.alpha_composite(tex)
    strip = strip.resize((N * W, H), Image.LANCZOS)
    return [strip.crop((i * W, 0, (i + 1) * W, H)) for i in range(N)]


def plain(path, fx, fy, crop=None):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if crop:
        im = im.crop(crop)
    return grade(cover(im, W, H, fx, fy)).convert("RGBA")


def build(v):
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    sw = swoosh3()
    # 1. no swoosh (Linnea, 10 Nov): photo with the soft frosted fade, text on the fade
    bg0 = frost(f"{V}/suzanne-fvc-conference.jpg", 0.45, 0.62, 0.55, 0.8)
    tex0 = straw(W, H).convert("RGBA")
    yy = np.linspace(0, 1, H, dtype=np.float32)
    tt = np.clip((yy - 0.6) / 0.22, 0, 1)
    tt = tt * tt * (3 - 2 * tt) * 0.5
    tex0.putalpha(Image.fromarray(np.repeat((tt * 255)[:, None], W, axis=1).astype("uint8")))
    bg0.alpha_composite(tex0)
    d.bg(0, bg0, name="Photo with soft frosted fade and straw texture")
    head = "Veteran farmers\nbuilding living soil"
    det = "Consultant Suzanne Shea presented at the Farmer Veteran Coalition Stakeholders Conference"
    hh = height(head, 80, 920, lh=1.04)
    dh = height(det, 48, 780, bold=False, lh=1.2)
    y = H - 70 - round(dh) - 22 - round(hh)
    y = T(d, 0, "Headline", head, 80, y, 920, hh + 8, 80, color=CREAM, align="left", lh=1.04)
    T(d, 0, "Details", det, 80, round(y) + 22, 780, dh + 8, 48, bold=False, color=CREAM, align="left", lh=1.2)
    logo(d, 0, W - 60 - 170, H - 40 - 170)
    # 2. text moved down onto the swoosh (no teal fade)
    d.bg(1, plain(f"{V}/suzanne-hoop-house.jpg", 0.55, 0.35), name="Photo")
    d.put(1, "Green swoosh", sw[0], 0, 0, shadowed=False, anchor="tl")
    T(d, 1, "Text", "Her presentation taught veteran farmers about scalable sustainability through the Soil Food Web "
      "Approach.", 80, 1000, 740, 290, 50, bold=False, color=CREAM, align="left", lh=1.2, mn=46)
    logo(d, 1, W - 60 - 170, H - 40 - 170)
    # 3. photo only, the swoosh dips and ends at the logo
    sf = ImageOps.exif_transpose(Image.open(f"{V}/suzanne-conference-walk.jpg")).convert("RGB")
    cw = int(sf.width * 0.465)
    ch = int(cw * H / W)
    sf = sf.crop((0, sf.height - ch, cw, sf.height)).resize((W, H), Image.LANCZOS)
    d.bg(2, grade(sf).convert("RGBA"), name="Photo")
    d.put(2, "Green swoosh", sw[1], 0, 0, shadowed=False, anchor="tl")
    logo(d, 2, W - 60 - 170, H - 30 - 170)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
