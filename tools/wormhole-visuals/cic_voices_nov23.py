"""Mon Nov 23: Foundation Courses + Compost Intensive Course promo, CIC student experience. Linnea's slide text
unchanged: the two student quotes. Cover line is the caption's closing question. Photo: Carla's CIC image (Drive
CIC.jpeg 1afK47cpk2xJ7sRtnWA-nbgtfca3Jx1cU); slides 2-3 use crops of its own photos (same post).

  python3 tools/wormhole-visuals/cic_voices_nov23.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from bundle_three_styles_v12 import T, height
from collage import Deck, cover, fit
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
GARA = "/home/user/fonts/eb-garamond-latin-400-normal.ttf"
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
    glow = 1 + 0.35 * np.exp(-(((xx - W * 0.7) / (W * 0.6)) ** 2 + ((yy - H * 0.2) / (H * 0.45)) ** 2))
    return Image.fromarray((a * (v * glow)[..., None]).clip(0, 255).astype("uint8")).convert("RGBA")


def glass(bg, x, y, w, h, r=36, alpha=0.9, fx=0.5, fy=0.5, feather=70):
    """Linnea's soil photo in a box whose edges fade softly into the straw, with a faint cream rim of light."""
    F = feather
    soil = cover(Image.open(SOIL).convert("RGB"), w + 2 * F, h + 2 * F, fx, fy)
    a = np.asarray(soil.filter(ImageFilter.GaussianBlur(3))).astype(np.float32) * 0.6
    yy, xx = np.mgrid[0:h + 2 * F, 0:w + 2 * F].astype(np.float32)
    glow = np.exp(-(((xx - (w + 2 * F) * 0.3) / (w * 0.6)) ** 2 + ((yy - F) / (h * 0.5)) ** 2))
    a = a + glow[..., None] * np.array([40, 52, 30], np.float32)
    pan = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    m = Image.new("L", pan.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((F, F, F + w - 1, F + h - 1), r, fill=round(255 * alpha))
    pan.putalpha(m.filter(ImageFilter.GaussianBlur(F / 2.2)))
    rim = Image.new("RGBA", pan.size, (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle((F, F, F + w - 1, F + h - 1), r, outline=(244, 241, 234, 90), width=2)
    rim = rim.filter(ImageFilter.GaussianBlur(1.2))
    ra = np.asarray(rim).astype(np.float32)
    ra[..., 3] *= np.clip(1.2 - yy / (h + 2 * F) * 1.3, 0, 1)   # rim fades out toward the bottom
    pan.alpha_composite(Image.fromarray(ra.clip(0, 255).astype("uint8")))
    return pan


def ghost(h=520, op=0.28, fy=0.35, up=False):
    """The CIC call faces as a faint, fading ghost."""
    z = faces_raw(h, fy)
    t = np.linspace(0, 1, h)
    t = 1 - np.clip(t / 0.95, 0, 1) if not up else np.clip((t - 0.05) / 0.95, 0, 1)
    t = t * t * (3 - 2 * t) * op
    z.putalpha(Image.fromarray(np.repeat((t * 255)[:, None], W, axis=1).astype("uint8")))
    return z


def qmark(size=330):
    f = ImageFont.truetype(MONT, size)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, -size * 0.12), "\u201c", font=f, fill=MINT)
    return im.crop(im.getbbox())


def faces_raw(h=760, fy=0.35):
    z = Image.open(ZOOM).convert("RGB")
    z = z.crop((int(z.width * 0.062), int(z.height * 0.068), int(z.width * 0.93), int(z.height * 0.94)))
    return grade(cover(z, W, h, 0.5, fy)).convert("RGBA")


def faces(h=860):
    z = faces_raw(h)
    yy, xx = np.mgrid[0:h, 0:W].astype(np.float32)
    t = np.clip((yy / h - 0.3) / 0.7, 0, 1)
    t = t * t * (3 - 2 * t)
    side = np.clip(1 - (np.abs(xx - W / 2) / (W / 2)) ** 4 * 0.5, 0, 1)
    z.putalpha(Image.fromarray(((1 - t) * side * 255).astype("uint8")))
    return z


# ---- v6: quiet luxury. Dark soil ground, straw fading in, hairline frame, Garamond, lots of air ----
GOLDLESS_MINT = "#A9D3B2"
P1 = PRATIK[:PRATIK.index(" Assignments")]
P2 = PRATIK[PRATIK.index("Assignments"):]


def ground(fy=0.5, straw_top=True, straw_h=430, straw_op=0.5):
    soil = cover(Image.open(SOIL).convert("RGB"), W, H, 0.5, fy)
    a = np.asarray(soil).astype(np.float32) * 0.42
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.55 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2) / 2
    a = a * np.clip(v, 0.35, 1)[..., None]
    st = np.asarray(cover(Image.open(STRAW).convert("RGB"), W, H, 0.5, fy)).astype(np.float32) * 0.62
    t = (1 - yy / straw_h) if straw_top else (yy - (H - straw_h)) / straw_h
    t = np.clip(t, 0, 1)
    t = (t * t * (3 - 2 * t) * straw_op)[..., None]
    a = a * (1 - t) + st * t
    return Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")


def frame(k, d):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle((40, 40, W - 41, H - 41), outline=(244, 241, 234, 85), width=2)
    d.put(k, "Hairline frame", im, 0, 0, shadowed=False, anchor="tl")


def rule(k, d, x, y, w=90):
    im = Image.new("RGBA", (w, 3), (169, 211, 178, 255))
    d.put(k, "Hairline rule", im, x, y, shadowed=False, anchor="tl")


def gqmark(size=300, ch="\u201c"):
    f = ImageFont.truetype(GARA, size)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, fill=GOLDLESS_MINT)
    return im.crop(im.getbbox())


def qslide(d, k, text, name, fy, straw_top, size=54, mark=True):
    d.bg(k, ground(fy, straw_top), name="Soil ground with straw fading in")
    frame(k, d)
    x, w = 120, 840
    _, lines, _ = fit(text, "garamond", False, w, 3000, size, size, 1.24)
    qh = len(lines) * size * 1.24
    total = (150 if mark else 0) + qh + (130 if name else 0)
    y = (H - total) / 2 + (10 if straw_top else -30)
    if mark:
        qm = gqmark()
        d.put(k, "Quote mark", qm, x - 6, round(y), shadowed=False, anchor="tl")
        y += 150
    y = d.text(k, "Quote", text, x, round(y), w, qh + 10, size, kind="garamond", italic=False, color=CREAM, lh=1.24)
    if name:
        rule(k, d, x, round(y) + 50)
        d.text(k, "Name", name, x, round(y) + 78, w, 60, 42, kind="montserrat", italic=False,
               color=GOLDLESS_MINT, lh=1.1, track=4)


def build(v):
    d = Deck("cic20261123", 4, f"cic-student-voices-{v}", "2026-11-23")
    # 1. cover: the CIC call as one framed picture that fades into the soil, Garamond italic question
    d.bg(0, ground(0.4, False, 520, 0.55), name="Soil ground with straw fading up")
    frame(0, d)
    z = Image.open(ZOOM).convert("RGB")
    z = z.crop((int(z.width * 0.062), int(z.height * 0.068), int(z.width * 0.93), int(z.height * 0.72)))
    zw = 840
    z = grade(z.resize((zw, round(z.height * zw / z.width)), Image.LANCZOS)).convert("RGBA")
    yy, xx = np.mgrid[0:z.height, 0:zw].astype(np.float32)
    t = np.clip((yy / z.height - 0.78) / 0.22, 0, 1) * 0.85
    t = t * t * (3 - 2 * t)
    e = np.clip(np.minimum(xx, zw - 1 - xx) / 40, 0, 1) * np.clip(yy / 30, 0, 1)
    z.putalpha(Image.fromarray(((1 - t) * e * 255).astype("uint8")))
    d.put(0, "CIC call photo", z, 120, 170, shadowed=False, anchor="tl")
    d.text(0, "Eyebrow", "COMPOST INTENSIVE COURSE", 120, 100, 840, 50, 42, kind="montserrat", italic=False,
           color=GOLDLESS_MINT, lh=1.1, align="center", track=6)
    head = "Will we see you\nin the CIC next year?"
    d.text(0, "Headline", head, 90, 730, 900, 260, 86, kind="garamond", italic=True, color=CREAM, lh=1.08,
           align="center")
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((130, round(lg.height * 130 / lg.width)), Image.LANCZOS)
    d.put(0, "SFW logo", lg, (W - 130) // 2, H - 80 - lg.height, shadowed=False, anchor="tl")
    # 2. Kamai  3-4. Pratik, his quote carried over two slides at the sentence break
    qslide(d, 1, KAMAI, "–Kamai Fatma", 0.3, True)
    qslide(d, 2, P1, None, 0.6, False, size=56)
    qslide(d, 3, P2, "–Pratik Thomas", 0.8, True, size=56, mark=False)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
