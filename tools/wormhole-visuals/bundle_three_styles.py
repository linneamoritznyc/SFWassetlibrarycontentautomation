"""Three bundle posts in three different styles (Linnea, 4 Nov: "3 separate posts with 3 different visuals in
different styles"), on the three angles she set. Words from the bundle sales page only (checked 4 Nov).

  x20261125  Wed 18 Nov  Two courses, one bundle   split screen: blueprint grid (science) | soil speckle (compost)
  x20261130  Wed 25 Nov  Pick your season          night ink with a glowing year timeline and the sunrise drawing
  fes20261130 Wed 2 Dec  Ends today                type-led quote card on flat cream-on-green, seedling drawing

  python3 tools/wormhole-visuals/bundle_three_styles.py
"""
import os
import re

import qrcode

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import news_cards as nc
from bundle_v6 import H, W, line_art
from collage import Deck
from nov_fill import BROWN, CREAM, DECKS, GREEN, INK, LGREEN, TILES, WHITE

COLOR_LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
V = "v11"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def grain(im, seed, amt=4):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    a += np.random.default_rng(seed).normal(0, amt, a.shape[:2] + (1,))
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8")).convert("RGBA")


def tinted(name, w, color):
    im = line_art(name, w)
    out = Image.new("RGBA", im.size, rgb(color) + (0,))
    out.putalpha(im.getchannel("A"))
    return out


URL = "https://school.soilfoodweb.com/bundles/foundation-courses-compost-intensive-course"
# Placeholder UTM until Stephanie sends the real ones (Banjo's UTM Links 2026 sheet).
UTM = "?utm_source=instagram&utm_medium=social&utm_campaign=fall_enrollment_bundle&utm_content={}"


def qr(d, k, pid, size=180):
    q = qrcode.QRCode(border=2, box_size=10)
    q.add_data(URL + UTM.format(pid))
    im = q.make_image(fill_color=INK, back_color=CREAM).convert("RGBA").resize((size, size), Image.NEAREST)
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), 16, fill=255)
    im.putalpha(m)
    d.put(k, "QR code (UTM link)", im, 72, H - 72 - size, shadowed=False, anchor="tl")


def logo(d, k, white=True, w=200):
    lg = Image.open(WHITE if white else COLOR_LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 72 - w, H - 72 - lg.height, shadowed=False, anchor="tl")


DATE = re.compile(r"\b(until |by )?(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|"
                  r"November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b")


def keep_dates(t):
    """Stephanie, 4 Nov: a date stays on one line with its words (non-breaking spaces)."""
    return DATE.sub(lambda m: (m.group(1) or "").replace(" ", "\u00a0") + m.group(2) + "\u00a0" + m.group(3), t)


def T(d, k, name, t, x, y, w, h, size, bold=True, color=CREAM, align="center", lh=None, mn=None):
    # Stephanie, 4 Nov: centre the text. A box that starts at the margin is centred on the slide.
    if align == "center" and x == 72:
        x = (W - w) // 2
    t = keep_dates(t)
    return d.text(k, name, t, x, y, w, h, size, kind="montserrat-bold" if bold else "source-reg", italic=False,
                  color=color, lh=lh or (1.06 if bold else 1.22), align=align,
                  min_size=mn or (66 if bold and size >= 66 else 50))


# ---------- 1. split screen ----------
BLUE_D, SOIL = "#1F4E79", "#4F3433"


def blueprint(w, h, seed):
    im = Image.new("RGB", (w, h), BLUE_D)
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(g)
    for x in range(0, w, 36):
        dr.line((x, 0, x, h), fill=(255, 255, 255, 40 if x % 180 == 0 else 16), width=1)
    for y in range(0, h, 36):
        dr.line((0, y, w, y), fill=(255, 255, 255, 40 if y % 180 == 0 else 16), width=1)
    im = Image.alpha_composite(im.convert("RGBA"), g)
    return grain(im, seed, 3)


def speckle(w, h, seed):
    rng = np.random.default_rng(seed)
    im = Image.new("RGBA", (w, h), rgb(SOIL) + (255,))
    dr = ImageDraw.Draw(im)
    for _ in range(2600):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(1, 4.5)
        c = rgb("#6B4A3A") if rng.random() < 0.6 else rgb("#2E1E1D")
        dr.ellipse((x - r, y - r, x + r, y + r), fill=c + (255,))
    return grain(im.filter(ImageFilter.GaussianBlur(0.6)), seed, 3)


def two_courses():
    d = Deck("x20261125", 3, f"two-courses-one-bundle-{V}", "2026-11-18")
    half = W // 2
    bg = Image.new("RGBA", (W, H))
    bg.paste(blueprint(half, H, 1), (0, 0))
    bg.paste(speckle(W - half, H, 2), (half, 0))
    dr = ImageDraw.Draw(bg)
    dr.line((half, 0, half, H), fill=rgb(CREAM) + (255,), width=6)
    dr.rectangle((0, 0, W, 230), fill=rgb(CREAM) + (255,))
    dr.rectangle((0, H - 300, W, H), fill=rgb(CREAM) + (255,))
    d.bg(0, bg, name="Background: blueprint | soil")
    for im, cx in ((line_art("microscope", 420), half // 2), (line_art("thermometer", 330), half + half // 2)):
        d.put(0, "Line drawing", im, cx - im.width // 2, 560 - im.height // 2, shadowed=False, anchor="tl")
    T(d, 0, "Label left", "Foundation Courses", 40, 800, half - 80, 160, 52)
    T(d, 0, "Label right", "Compost Intensive", half + 40, 800, half - 80, 160, 52)
    T(d, 0, "Headline", "Two courses, one bundle", 72, 72, 936, 110, 84, color=BROWN)
    T(d, 0, "Details", "Fall Enrollment Special,\nuntil 2 December.\nLink in bio.", 72, H - 270, 600, 200, 52,
      bold=False, color=INK)
    logo(d, 0, white=False, w=150)
    # slide 2: the blue half, full
    d.bg(1, blueprint(W, H, 3), name="Background: blueprint")
    im = line_art("microscope", 620)
    d.put(1, "Line drawing", im, (W - im.width) // 2, 80, shadowed=False, anchor="tl")
    y = T(d, 1, "Headline", "The Foundation Courses teach you to work out what your soil needs.", 72, 560, 936, 300,
          70)
    T(d, 1, "Details", "63 lectures and about 150 hours of study, with 40+ years of Dr. Elaine's knowledge.", 72,
      round(y) + 24, 760, 220, 52, bold=False)
    logo(d, 1)
    # slide 3: the soil half, full
    d.bg(2, speckle(W, H, 4), name="Background: soil")
    im = line_art("thermometer", 380)
    d.put(2, "Line drawing", im, (W - im.width) // 2, 50, shadowed=False, anchor="tl")
    y = T(d, 2, "Headline", "The Compost Intensive Course teaches you to make it.", 72, 500, 936, 240, 70)
    T(d, 2, "Details", "No prerequisites. Start the Foundation Courses today and build with the cohort as early as "
      "January.", 72, round(y) + 24, 760, 260, 52, bold=False)
    qr(d, 2, "x20261125")
    logo(d, 2)
    return d


# ---------- 2. night timeline ----------
NIGHT = "#0B1F14"
rgb_hex_lg = "#A8D5B0"


def glow_layer(draw_fn, blur):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(g))
    return Image.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)), g)


def pick_season():
    d = Deck("x20261130", 1, f"pick-your-season-{V}", "2026-11-25")
    bg = Image.new("RGBA", (W, H), rgb(NIGHT) + (255,))
    # soft horizon light behind the sunrise
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - 250) / H * 1.6) ** 2)
    a = np.asarray(bg).astype(np.float32)
    a[..., :3] += (np.clip(1 - r / 0.5, 0, 1) ** 2)[..., None] * np.array([40, 70, 45], np.float32)
    bg = grain(Image.fromarray(np.clip(a, 0, 255).astype("uint8")), 5, 3)
    d.bg(0, bg, name="Background: night")
    im = line_art("sunrise", 560)
    d.put(0, "Line drawing", im, (W - im.width) // 2, 50, shadowed=False, anchor="tl")
    y = T(d, 0, "Headline", "Pick your season", 72, 380, 936, 110, 84)
    T(d, 0, "Details", "Start the Foundation Courses this winter. Then build with a 2027 cohort: ten weeks, with a "
      "live mentor every week.", 72, round(y) + 18, 900, 200, 52, bold=False)
    # timeline
    x0, x1, ty = 72, W - 72, 790
    mw = (x1 - x0) / 12
    blocks = [(0 + 10 / 31, 2 + 26 / 31), (4 + 9 / 30, 6 + 25 / 31), (7 + 29 / 31, 10 + 7 / 30)]

    def draw(dr):
        dr.line((x0, ty, x1, ty), fill=rgb(CREAM) + (120,), width=4)
        for i in range(13):
            dr.line((x0 + i * mw, ty - 14, x0 + i * mw, ty + 14), fill=rgb(CREAM) + (120,), width=3)
        for s, e in blocks:
            dr.rounded_rectangle((x0 + s * mw, ty - 34, x0 + e * mw, ty + 34), 34, fill=rgb(LGREEN) + (255,))
    layer = glow_layer(draw, 14)
    d.put(0, "Timeline 2027", layer, 0, 0, shadowed=False, anchor="tl")
    f = ImageFont.truetype(os.path.join(nc.FONTS, "Montserrat-SemiBold.ttf"), 42)
    for i, m in enumerate("JFMAMJJASOND"):
        T(d, 0, f"Month {m}{i}", m, round(x0 + (i + 0.5) * mw - 35), ty - 100, 70, 56, 42, mn=42)
    for (s, e), lab in zip(blocks, ("11 Jan to 26 Mar", "10 May to 25 Jul", "30 Aug to 7 Nov")):
        cx = x0 + (s + e) / 2 * mw
        T(d, 0, f"Cohort {lab}", lab.replace(" to ", "\nto "), round(cx - 140), ty + 60, 280, 130, 42,
          bold=False, align="center", mn=42, lh=1.15)
    T(d, 0, "Date line", "One week left, until 2 December.", 72, 990, 936, 70, 52, color=rgb_hex_lg)
    qr(d, 0, "x20261130")
    logo(d, 0)
    return d


# ---------- 3. quote card ----------
def ends_today():
    d = Deck("fes20261130", 3, f"bundle-ends-today-{V}", "2026-12-02")
    # 1: big type cover on cream
    d.bg(0, grain(Image.new("RGB", (W, H), CREAM), 7, 3), name="Background: cream")
    im = tinted("sprout", 440, GREEN)
    d.put(0, "Line drawing", im, (W - im.width) // 2, H - im.height - 110, shadowed=False, anchor="tl")
    T(d, 0, "Eyebrow", "FALL ENROLLMENT SPECIAL", 72, 120, 936, 70, 52, color=GREEN, mn=50)
    T(d, 0, "Headline", "Ends today", 72, 210, 936, 330, 160, color=BROWN, mn=120, lh=1.0)
    T(d, 0, "Details", "Foundation Courses + Compost Intensive. Link in bio.", 72, 400, 820, 200, 52, bold=False,
      color=INK)
    logo(d, 0, white=False)
    # 2: the quote on green
    d.bg(1, grain(Image.new("RGB", (W, H), GREEN), 8, 4), name="Background: green")
    q = Image.new("RGBA", (360, 300), (0, 0, 0, 0))
    ImageDraw.Draw(q).text((0, -60), "“", font=ImageFont.truetype(
        os.path.join(nc.FONTS, "Montserrat-Bold.ttf"), 400), fill=rgb(LGREEN) + (255,))
    q = q.crop(q.getchannel("A").getbbox())
    d.put(1, "Quote mark", q, (W - q.width) // 2, 120, shadowed=False, anchor="tl")
    y = T(d, 1, "Quote", "The extraordinary body of knowledge Soil Food Web's Foundation Courses has to offer can "
          "certainly empower me with the required knowledge and experience to drive the work I have been "
          "developing further.", 72, 300, 936, 560, 56, bold=False, lh=1.25)
    T(d, 1, "Name", "Clara Santiago, Portugal", 72, round(y) + 40, 700, 80, 52)
    im = line_art("sprout", 260)
    d.put(1, "Line drawing", im, (W - im.width) // 2, H - im.height - 60, shadowed=False, anchor="tl")
    logo(d, 1)
    # 3: consultant pathway fact, cream card on green
    d.bg(2, grain(Image.new("RGB", (W, H), GREEN), 9, 4), name="Background: green")
    T(d, 2, "Eyebrow", "FOR CONSULTANTS", 120, 260, 840, 70, 52, color=GREEN, mn=50)
    y = T(d, 2, "Headline", "The Compost Intensive counts toward the Consultant Pathway.", 120, 350, 840, 320, 70,
          color=BROWN)
    y = T(d, 2, "Details", "It can be used to satisfy the BioComplete™ Compost Production requirement.", 120,
          round(y) + 30, 760, 220, 52, bold=False, color=INK)
    ch = round(y) + 70 - 200
    card = Image.new("RGBA", (936, ch), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, 935, ch - 1), 28, fill=rgb(CREAM) + (255,))
    first = [i for i, it in enumerate(d.items) if it.get("name") == "Eyebrow" and it["x"] >= 2 * W][0]
    d.put(2, "Card", card, 72, 200, shadowed=False, anchor="tl")
    d.items.insert(first, d.items.pop())

    T(d, 2, "Date line", "Ends today. Link in bio.", 72, 200 + ch + 70, 936, 80, 66)
    qr(d, 2, "fes20261130")
    logo(d, 2)
    return d


if __name__ == "__main__":
    for fn in (two_courses, pick_season, ends_today):
        d = fn()
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(TILES, f"{d.id}-{V}-{k}.jpg")), d.id
        print(d.save(TILES, DECKS)[0], d.pptx_name())
