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
ERIC = ("“I liked the deeper attention to understanding what was a quality material and what was not. The water level "
        "and soaking times for materials was also helpful. I feel like I now have a better understanding of the overall "
        "texture and how to work with materials (whatever they may be) that I can source locally.”")
LISE = ("“The clear, step by step instructions and the interactions between the teachers and students.  Even though the "
        "actual work was done independently, I felt more supported by seeing other people going through the same "
        "process. It was very motivating and very interesting.”")
PRATIK = ("“The live sessions with fellow students and mentors have definitely been helpful for me personally. I prefer "
          "this format, especially when it goes beyond just theory-based content to include live teaching and "
          "discussions in our course. This approach allows me to grasp concepts more effectively and retain them "
          "better. Assignments have also been beneficial, as they help us incorporate theory into practice, providing "
          "valuable learning opportunities even when we make mistakes. The nuances are details of being able to plan "
          "and actually doing it is what actually strengthens my learning.”")


STRAW = "/home/user/sfwlib/social/cic/straw-linnea.jpg"
COMPOST = "/home/user/sfwlib/social/cic/compost-linnea.jpg"
SOIL = "/home/user/sfwlib/social/cic/soil-linnea.jpg"
MONT = "/root/.fonts/Montserrat-Bold.ttf"
ZOOM = "/home/user/sfwlib/social/students/cic-zoom-call-blurred.jpg"   # Carla's CIC call screenshot


def logo(d, k, x, y, w=150):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def straw_bg(fy=0.5, dark=0.24, src=None):
    im = cover(Image.open(src or STRAW).convert("RGB"), W, H, 0.5, fy)
    a = np.asarray(im).astype(np.float32) * dark
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    e = np.clip(np.minimum(yy, H - 1 - yy) / 260, 0, 1)
    e = 0.55 + 0.45 * e * e * (3 - 2 * e)
    return Image.fromarray((a * (v * e)[..., None]).clip(0, 255).astype("uint8")).convert("RGBA")


def glass(bg, x, y, w, h, r=36, alpha=0.95, fx=0.5, fy=0.5, dim=1.0):
    """See-through box filled with Linnea's soil photo at 86%: straw shows faintly through, thin cream edge."""
    soil = cover(Image.open(SOIL).convert("RGB"), w, h, fx, fy)
    a = np.asarray(soil).astype(np.float32) * dim
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
    z = z.crop((int(z.width * 0.062), int(z.height * 0.068), int(z.width * 0.93), int(z.height * 0.72)))
    h = round(z.height * W / z.width)
    z = grade(z.resize((W, h), Image.LANCZOS)).convert("RGBA")
    yy, xx = np.mgrid[0:h, 0:W].astype(np.float32)
    t = np.clip((yy / h - 0.62) / 0.38, 0, 1)
    t = t * t * (3 - 2 * t)
    z.putalpha(Image.fromarray(((1 - t) * 255).astype("uint8")))
    return z


def quote_slide(d, k, text, name, fy, size=50):
    bg = straw_bg(fy, 0.32, COMPOST) if k % 2 == 1 else straw_bg(fy)
    d.bg(k, bg, name="Straw texture")
    pw, pad = 960, 60
    qh = height(text, size, pw - 2 * pad, bold=False, lh=1.18)
    nh = height(name, 52, pw - 2 * pad, lh=1.1)
    ph = round(pad + 30 + qh + 30 + nh + pad)
    py = max(95, (H - ph) // 2 + 30)
    d.put(k, "Frosted panel", glass(bg, 60, py, pw, ph, dim=0.45), 60, py, shadowed=True, anchor="tl")
    qm = qmark()
    d.put(k, "Quote mark", qm, 60 + pad - 10, py - qm.height // 2 - 10, shadowed=False, anchor="tl")
    y = T(d, k, "Quote", text, 60 + pad, py + pad + 30, pw - 2 * pad, qh + 8, size, bold=False, color=CREAM,
          align="left", lh=1.18)
    T(d, k, "Name", name, 60 + pad, round(y) + 30, pw - 2 * pad, nh + 8, 52, color=MINT, align="left", lh=1.1)


def build(v):
    d = Deck("cic20261123", 5, f"cic-student-voices-{v}", "2026-11-23")
    # 1. one soil card on the hay, like a mounted print: Carla's CIC call photo crisp at the top (no fade),
    #    the caption's question below, logo bottom right
    bg = straw_bg(0.3)
    d.bg(0, bg, name="Straw texture")
    cx, cy, cw, ch = 60, 85, 960, H - 170
    d.put(0, "Soil card", glass(bg, cx, cy, cw, ch, dim=0.45), cx, cy, shadowed=True, anchor="tl")
    z = Image.open(ZOOM).convert("RGB")
    z = z.crop((int(z.width * 0.062), int(z.height * 0.068), int(z.width * 0.93), int(z.height * 0.72)))
    pw = cw - 60
    z = grade(z.resize((pw, round(z.height * pw / z.width)), Image.LANCZOS)).convert("RGBA")
    m = Image.new("L", z.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, z.width - 1, z.height - 1), 22, fill=255)
    z.putalpha(m)
    ImageDraw.Draw(z).rounded_rectangle((1, 1, z.width - 2, z.height - 2), 22, outline=(244, 241, 234, 150), width=2)
    d.put(0, "CIC call photo", z, cx + 30, cy + 30, shadowed=True, anchor="tl", off=(0, 10), blur=18, alpha=0.5)
    head = "Why our students\nlove the Compost\nIntensive Course"
    hh = height(head, 86, 840, lh=1.06)
    top = cy + 30 + z.height
    y = top + (cy + ch - top - round(hh)) // 2 - 10
    d.put(0, "Mint rule", Image.new("RGBA", (110, 6), (169, 211, 178, 255)), cx + 60, y - 40, shadowed=False,
          anchor="tl")
    T(d, 0, "Headline", head, cx + 60, y, 860, hh + 8, 86, color=CREAM, align="left", lh=1.06)
    logo(d, 0, cx + cw - 150 - 50, cy + ch - 150 - 45)
    quote_slide(d, 1, KAMAI, "–Fatemah Kamai, Libya", 0.25)
    quote_slide(d, 2, PRATIK, "–Pratik Thomas, India", 0.75)
    quote_slide(d, 3, ERIC, "–Eric Daine, United States", 0.6, size=60)
    quote_slide(d, 4, LISE, "–Lise Marcell, United States", 0.1, size=60)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
