"""Mon Nov 23: Foundation Courses + Compost Intensive Course promo, CIC student experience. Linnea's slide text
unchanged: the two student quotes. Cover line is the caption's closing question. Photo: Carla's CIC image (Drive
CIC.jpeg 1afK47cpk2xJ7sRtnWA-nbgtfca3Jx1cU); slides 2-3 use crops of its own photos (same post).

  python3 tools/wormhole-visuals/cic_voices_nov23.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from bundle_three_styles_v12 import T, height
from collage import Deck, cover
from nov_fill import DECKS, TILES
from suzanne_frost import grade

W, H = 1080, 1350
GREEN = (21, 104, 38)
CREAM = "#F4F1EA"
MINT = "#A9D3B2"
SRC = "/home/user/sfwlib/social/cic/cic-carla.jpg"
LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"

KAMAI = ("“What I really enjoyed about this course was the opportunity to engage with fellow participants from diverse "
         "countries during the live sessions. This exchange of experiences allowed us to gain valuable insights, "
         "especially when discussing region-specific challenges. Given that I live in a different climate, I found it "
         "particularly beneficial to learn how composting techniques can be adapted to various environments, enabling "
         "me to apply this knowledge effectively no matter where I am.”")
PRATIK = ("“The live sessions with fellow students and mentors have definitely been helpful for me personally. I prefer "
          "this format, especially when it goes beyond just theory-based content to include live teaching and "
          "discussions in our course. This approach allows me to grasp concepts more effectively and retain them "
          "better. Assignments have also been beneficial, as they help us incorporate theory into practice, providing "
          "valuable learning opportunities even when we make mistakes. The nuances are details of being able to plan "
          "and actually doing it is what actually strengthens my learning.”")


STRAW = "/home/user/sfwlib/social/cic/straw-linnea.jpg"
SOIL = "/home/user/sfwlib/social/cic/soil-linnea.jpg"
MONT = "/root/.fonts/Montserrat-Bold.ttf"
ZOOM = "/home/user/sfwlib/social/students/cic-zoom-call-blurred.jpg"   # Carla's CIC call screenshot


def logo(d, k, x, y, w=150):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def straw_bg(fy=0.5, dark=0.42):
    im = cover(Image.open(STRAW).convert("RGB"), W, H, 0.5, fy)
    a = np.asarray(im).astype(np.float32) * dark
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    return Image.fromarray((a * v[..., None]).clip(0, 255).astype("uint8")).convert("RGBA")


def glass(bg, x, y, w, h, r=36, alpha=0.86, fx=0.5, fy=0.5):
    """See-through box filled with Linnea's soil photo at 86%: straw shows faintly through, thin cream edge."""
    soil = cover(Image.open(SOIL).convert("RGB"), w, h, fx, fy)
    a = np.asarray(soil.filter(ImageFilter.GaussianBlur(3))).astype(np.float32) * 0.62
    pan = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=round(255 * alpha))
    pan.putalpha(m)
    ImageDraw.Draw(pan).rounded_rectangle((1, 1, w - 2, h - 2), r, outline=(244, 241, 234, 130), width=2)
    return pan


def qmark(size=330):
    f = ImageFont.truetype(MONT, size)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, -size * 0.12), "\u201c", font=f, fill=MINT)
    return im.crop(im.getbbox())


def faces():
    z = Image.open(ZOOM).convert("RGB")
    z = z.crop((int(z.width * 0.062), int(z.height * 0.068), int(z.width * 0.93), int(z.height * 0.94)))
    z = grade(cover(z, W, 700, 0.5, 0.35)).convert("RGBA")
    t = np.clip((np.linspace(0, 1, 700) - 0.55) / 0.45, 0, 1)
    t = t * t * (3 - 2 * t)
    z.putalpha(Image.fromarray(np.repeat(((1 - t) * 255)[:, None], W, axis=1).astype("uint8")))
    return z


def quote_slide(d, k, text, name, fy):
    bg = straw_bg(fy)
    d.bg(k, bg, name="Straw texture")
    pw, pad = 960, 60
    qh = height(text, 50, pw - 2 * pad, bold=False, lh=1.18)
    nh = height(name, 52, pw - 2 * pad, lh=1.1)
    ph = round(pad + 30 + qh + 30 + nh + pad)
    py = max(95, (H - ph) // 2 + 30)
    d.put(k, "Frosted panel", glass(bg, 60, py, pw, ph), 60, py, shadowed=True, anchor="tl")
    qm = qmark()
    d.put(k, "Quote mark", qm, 60 + pad - 10, py - qm.height // 2 - 10, shadowed=False, anchor="tl")
    y = T(d, k, "Quote", text, 60 + pad, py + pad + 30, pw - 2 * pad, qh + 8, 50, bold=False, color=CREAM,
          align="left", lh=1.18)
    T(d, k, "Name", name, 60 + pad, round(y) + 30, pw - 2 * pad, nh + 8, 52, color=MINT, align="left", lh=1.1)


def build(v):
    d = Deck("cic20261123", 3, f"cic-student-voices-{v}", "2026-11-23")
    # 1. Carla's CIC call faces fading into straw, the caption's question on a frosted panel
    bg = straw_bg(0.3)
    bg.alpha_composite(faces())
    d.bg(0, bg, name="Straw texture with CIC call faces fading in")
    head = "Will we see\nyou in the CIC\nnext year?"
    hh = height(head, 86, 840, lh=1.06)
    ph = round(hh + 120)
    py = H - 110 - ph
    d.put(0, "Frosted panel", glass(bg, 60, py, 960, ph), 60, py, shadowed=True, anchor="tl")
    T(d, 0, "Headline", head, 120, py + 60, 840, hh + 8, 86, color=CREAM, align="left", lh=1.06)
    logo(d, 0, W - 60 - 150 - 50, py + ph - 150 - 40)
    quote_slide(d, 1, KAMAI, "–Kamai Fatma", 0.25)
    quote_slide(d, 2, PRATIK, "–Pratik Thomas", 0.75)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
