"""27 Oct redo: annual report teaser with more design (trifold-style brand boxes) and
new photos for the permaculture ethics post (x20261117).

  BOX_SRC=<catalog photos> SFW_FONTS=<fonts dir> python3 tools/wormhole-visuals/redo_1027.py
    -> apps/web/public/wormhole/tiles/ar20261123-d1-<n>.jpg, x20261117-c2-<n>.jpg
"""
import os

from PIL import Image, ImageDraw, ImageFont

import boxes as B
import photo_first as PF

W, H = 1080, 1350
F = os.environ["SFW_FONTS"]
SFW = "Photo: Soil Food Web Foundation"
PF.CR.update({
    "20250625_155834.jpg": SFW, "20250626_093348.jpg": SFW, "20250619_071702.jpg": SFW,
    "IMG_2508.jpg": SFW, "PXL_20251012_191834807.jpg": SFW,
})


def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)


def mont(s):
    return font("montserrat-latin-800-normal.woff2", s)


def gothic(s):
    return font("pathway-gothic-one-latin-400-normal.woff2", s)


def sans(s):
    return font("source-sans-3-latin-400-normal.woff2", s)


def lines(d, x, y, rows, f, fill, lh):
    for r in rows:
        top = d.textbbox((0, 0), r, font=f)[1]
        d.text((x, y - top), r, font=f, fill=fill)
        y += lh
    return y


def out(name):
    p = os.path.join(B.OUT, name)
    assert not os.path.exists(p), p
    return p


def report_cover():
    c = PF.load("20250625_155834.jpg", (W, H), (0.3, 0.45))
    d = ImageDraw.Draw(c)
    # green block offset behind the cream panel, hard edges, both overlapping the photo
    d.rectangle((0, 900, 640, 1350), fill=B.GREEN)
    d.rectangle((60, 860, 900, 1230), fill=B.CREAM)
    y = lines(d, 110, 905, ["ANNUAL REPORT  |  YEAR ONE"], gothic(46), B.GREEN, 60)
    y = lines(d, 110, y + 18, ["Our first year,", "in one report."], mont(76), B.BROWN, 88)
    lines(d, 110, y + 22, ["Soil Food Web Foundation, October 2025 to October 2026"], sans(30), B.BROWN, 40)
    PF.credit(c, SFW)
    B.logo(c, (W - 150, 40), size=90)
    return c


def report_photo():
    c = PF.load("20250626_093348.jpg", (W, H), (0.5, 0.5))
    d = ImageDraw.Draw(c)
    # one narrow brown strip down the left edge carries the label, so the photo stays the slide
    d.rectangle((0, 0, 120, H), fill=B.BROWN)
    txt = Image.new("RGBA", (900, 120), (0, 0, 0, 0))
    ImageDraw.Draw(txt).text((0, 10), "WHAT WE BUILT TOGETHER", font=gothic(64), fill=B.CREAM)
    txt = txt.rotate(90, expand=True)
    c.paste(txt, (28, 260), txt)
    PF.credit(c, SFW)
    return c


def report_soon():
    c = PF.load("20250619_071702.jpg", (W, H), (0.35, 0.5))
    d = ImageDraw.Draw(c)
    d.rectangle((380, 120, W, 400), fill=B.GREEN)
    d.rectangle((330, 345, 820, 455), fill=B.CREAM)
    lines(d, 440, 180, ["Coming soon."], mont(80), B.CREAM, 96)
    lines(d, 370, 370, ["OUT 8 DECEMBER"], gothic(58), B.GREEN, 70)
    PF.credit(c, SFW)
    return c


def ethics(n):
    if n == 1:
        return PF.pic("IMG_2508.jpg", "Earth care.", B.GREEN, B.CREAM, focus=(0.5, 0.6), logo=True)
    return PF.pic("PXL_20251012_191834807.jpg", "Fair share.", B.TAN, B.BROWN, focus=(0.45, 0.55))


def sbs(n):
    PF.CR.update({"20250620_144146.jpg": SFW, "20250620_153134.jpg": SFW})
    if n == 1:
        return PF.pic("20250620_144146.jpg", "Small Business Saturday", B.TAN, B.BROWN, focus=(0.35, 0.5), logo=True)
    return PF.pic("20250620_153134.jpg", "Shop local for your soil.", B.DEEP, B.CREAM, focus=(0.6, 0.45))


if __name__ == "__main__":
    import sys
    only = sys.argv[1:]
    for name, make in [("x20261128-c2-1.jpg", lambda: sbs(1)), ("x20261128-c2-3.jpg", lambda: sbs(3)),("ar20261123-d1-1.jpg", report_cover), ("ar20261123-d1-2.jpg", report_photo),
                       ("ar20261123-d1-3.jpg", report_soon),
                       ("x20261117-c2-1.jpg", lambda: ethics(1)), ("x20261117-c2-3.jpg", lambda: ethics(3))]:
        if only and name not in only:
            continue
        make().convert("RGB").save(out(name), quality=90)
        print(name)
