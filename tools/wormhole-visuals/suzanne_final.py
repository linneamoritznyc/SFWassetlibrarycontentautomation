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
           (2200, 980)]

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
    for dy, col in ((-55, (89, 166, 108, 150)), (0, (21, 104, 38, 240))):
        line = [(x * k, (y + dy) * k) for x, y in smooth(pts)]
        dr.polygon(line + [(2 * W * k + 80, H * k + 50), (-80, H * k + 50)], fill=col)
    strip = strip.resize((2 * W, H), Image.LANCZOS)
    return strip.crop((0, 0, W, H)), strip.crop((W, 0, 2 * W, H))


def build(v):
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    # 1
    d.bg(0, frost(f"{V}/suzanne-fvc-conference.jpg", 0.45, 0.62, 0.55, 0.8), name="Photo with soft frosted fade")
    head = "Veteran farmers\nbuilding living soil"
    det = "Consultant Suzanne Shea presented at the Farmer Veteran Coalition Stakeholders Conference"
    hh = height(head, 80, 920, lh=1.04)
    dh = height(det, 48, 780, bold=False, lh=1.2)
    y = H - 70 - round(dh) - 22 - round(hh)
    y = T(d, 0, "Headline", head, 80, y, 920, hh + 8, 80, color=CREAM, align="left", lh=1.04)
    T(d, 0, "Details", det, 80, round(y) + 22, 780, dh + 8, 48, bold=False, color=CREAM, align="left", lh=1.2)
    logo(d, 0, W - 60 - 170, H - 50 - 170)
    # 2
    d.bg(1, frost(f"{V}/suzanne-hoop-house.jpg", 0.55, 0.7, 0.55, 0.8, top=True), name="Photo with soft frosted fade")
    t2 = "Her presentation taught veteran farmers about scalable sustainability through the Soil Food Web Approach."
    T(d, 1, "Text", t2, 80, 90, 900, 330, 56, bold=False, color=CREAM, align="left", lh=1.22)
    w2, w3 = wave_pair()
    d.put(1, "Green wave", w2, 0, 0, shadowed=False, anchor="tl")
    logo(d, 1, W - 60 - 170, H - 50 - 170)
    # 3 photo only
    # tight on Suzanne, the man in the background cropped out (Linnea, 10 Nov)
    sf = ImageOps.exif_transpose(Image.open(f"{V}/suzanne-conference-walk.jpg")).convert("RGB")
    cw = int(sf.width * 0.465)            # stop before the man in the green shirt
    ch = int(cw * H / W)
    y0 = sf.height - ch
    sf = sf.crop((0, y0, cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    d.bg(2, grade(sf).convert("RGBA"), name="Photo")
    d.put(2, "Green wave", w3, 0, 0, shadowed=False, anchor="tl")
    logo(d, 2, W - 60 - 170, H - 50 - 170)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
