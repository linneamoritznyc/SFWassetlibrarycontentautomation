"""Student quotes post for Fri 13 Nov (Linnea, 4 Nov): one student per slide, their quote word for word from the
bundle sales page (Testimonials), their photo from the same page. Cream paper, portrait in a green ring, quote,
name and country. Emmanuel Morales has no photo on the page, so his slide uses his initials.
No QR code yet (added at the end, per platform, when the visual is final).

  python3 tools/wormhole-visuals/student_quotes_nov13.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

import news_cards as nc
from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import FY, M, T, footer, height
from bundle_v6 import H, W
from collage import Deck
from nov_fill import BROWN, CREAM, DECKS, GREEN, INK, LGREEN, TILES

_put = Deck.put
Deck.put = lambda self, k, name, im, x, y, **kw: _put(self, k, name, im, round(x), round(y), **kw)

PH = "/home/user/sfwlib/social/students"
# (name, country, photo, face centre x, face centre y, quote verbatim from the sales page)
STUDENTS = [
    ("Zoë Unruh", "Canada", "9q52zNcBQ6WJL2tIiW6Q_zoe-unruh.jpg", 0.70, 0.42,
     "I recently completed my Foundation Courses. I had so much fun learning about regenerative agriculture, "
     "creating compost and liquid amendments, and all the little creatures that help our soils to thrive. I am super "
     "excited to put all these ideas into practice and to continue learning!"),
    ("Rob Mosier", "United States", "W2d17lkTRZW4abzCkFtS_rob-mosier.jpg", 0.50, 0.40,
     "I am overwhelmed by the depth and thoroughness of these courses... I am still amazed at the amount of content! "
     "The classes are absolutely fabulous!"),
    ("Emmanuel Morales", "United States", None, 0, 0,
     "I've taken classes on microbiology before but this course really makes a difference in the way that a story "
     "is put together that unveils a relationship between plants and all those beneficial microoragnisms that we "
     "just cannot see without a microscope."),
    ("Anusha Fatima", "Pakistan", "HMoEOlHpQfeLrbbjEKBB_anusha-fatima.jpg", 0.53, 0.45,
     "I want to help repair broken food systems by rebuilding life in the soil. Through this program, I hope to help "
     "farmers understand and work with nature's biology to regenerate land, improve resilience, and grow healthier "
     "food."),
    ("Clara Santiago", "Portugal", "EMR2z5iXTVObJxc0pQQK_clara-santiago.jpg", 0.55, 0.42,
     "The extraordinary body of knowledge Soil Food Web's Foundation Courses has to offer can certainly empower me "
     "with the required knowledge and experience to drive the work I have been developing further. As a land "
     "steward and within the projects I am developing and taking part in, I hope to have a positive impact and a "
     "considerable contribution towards soil health, land regeneration, awareness raising and ecological literacy."),
]
QW, QLH, RING = 936, 1.25, 10
PS, G1, G2 = 240, 44, 32   # one portrait size and the same gaps on every slide


def portrait(s, d):
    name, _, f, fx, fy, _ = s
    out = Image.new("RGBA", (d + 2 * RING, d + 2 * RING), (0, 0, 0, 0))
    dr = ImageDraw.Draw(out)
    dr.ellipse((0, 0, d + 2 * RING - 1, d + 2 * RING - 1), fill=rgb(LGREEN) + (255,))
    if f:
        im = Image.open(f"{PH}/{f}").convert("RGB")
        side = round(min(im.size) * 0.9)
        cx, cy = im.width * fx, im.height * fy
        x0 = min(max(cx - side / 2, 0), im.width - side)
        y0 = min(max(cy - side / 2, 0), im.height - side)
        im = im.crop((round(x0), round(y0), round(x0) + side, round(y0) + side)).resize((d, d), Image.LANCZOS)
    else:   # no photo on the page: initials
        im = Image.new("RGB", (d, d), GREEN)
        f2 = ImageFont.truetype(os.path.join(nc.FONTS, "Montserrat-Bold.ttf"), d // 3)
        ini = "".join(w[0] for w in name.split()[:2])
        dd = ImageDraw.Draw(im)
        dd.text(((d - dd.textlength(ini, font=f2)) / 2, d / 2 - d / 5.2), ini, font=f2, fill=CREAM)
    m = Image.new("L", (d * 2, d * 2), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d * 2 - 1, d * 2 - 1), fill=255)
    im = im.convert("RGBA")
    im.putalpha(m.resize((d, d), Image.LANCZOS))
    out.alpha_composite(im, (RING, RING))
    return out


def paper(seed):
    return grain(Image.new("RGB", (W, H), CREAM), seed, 3)


def build(v):
    d = Deck("tm20261113", 1 + len(STUDENTS), f"student-quotes-{v}", "2026-11-13")
    # cover
    d.bg(0, paper(60), name="Background: cream")
    hh = height("From our students", 86, 936)
    dh = height("Foundation Courses + Compost Intensive\nFall Enrollment Special\nUntil 2 December.", 52, 900,
                bold=False, lh=1.3)
    ps = 168
    total = hh + 70 + ps + 2 * RING + 70 + dh
    y = 72 + (FY - 40 - 72 - total) // 2
    T(d, 0, "Headline", "From our students", M, y, 936, hh + 6, 86, color=BROWN)
    y += hh + 70
    pics = [s for s in STUDENTS if s[2]]   # Linnea, 4 Nov: no initials circle for Emmanuel
    gap = (936 - len(pics) * (ps + 2 * RING)) // (len(pics) - 1)
    for i, s in enumerate(pics):
        d.put(0, f"Portrait {s[0]}", portrait(s, ps), M + i * (ps + 2 * RING + gap), y, shadowed=False, anchor="tl")
    y += ps + 2 * RING + 70
    T(d, 0, "Details", "Foundation Courses + Compost Intensive\nFall Enrollment Special\nUntil 2 December.",
      (W - 900) // 2, y, 900, dh + 6, 52, bold=False, color=INK, lh=1.3)
    footer(d, 0, white=False)
    # one student per slide
    for k, s in enumerate(STUDENTS, start=1):
        d.bg(k, paper(60 + k), name="Background: cream")
        q = "\u201c" + s[5] + "\u201d"
        qh = height(q, 52, QW, bold=False, lh=QLH)
        ps = PS
        # photo and name side by side, the quote below: the same layout on every slide
        from collage import font
        nw = max(font("montserrat-bold", False, 52).getlength(s[0]), font("source-reg", False, 52).getlength(s[1]))
        if not s[2]:   # no photo: just the name and country above the quote
            total = 132 + G1 + qh
            y = 60 + (FY - 20 - 60 - total) // 2
            T(d, k, "Name", s[0], M, y, 936, 70, 52, color=GREEN)
            T(d, k, "Country", s[1], M, y + 66, 936, 70, 52, bold=False, color=BROWN)
            T(d, k, "Quote", q, (W - QW) // 2, y + 132 + G1, QW, qh + 6, 52, bold=False, color=INK, lh=QLH)
            footer(d, k, white=False)
            continue
        row_w = ps + 2 * RING + 36 + nw
        total = ps + 2 * RING + G1 + qh
        room = FY - 20 - 60
        y = 60 + (room - total) // 2
        assert y >= 40, (s[0], y)
        x0 = (W - row_w) / 2
        d.put(k, f"Portrait {s[0]}", portrait(s, ps), x0, y, shadowed=False, anchor="tl")
        tx = round(x0 + ps + 2 * RING + 36)
        ty = round(y + (ps + 2 * RING) / 2 - 66)
        T(d, k, "Name", s[0], tx, ty, round(nw) + 10, 70, 52, color=GREEN, align="left")
        T(d, k, "Country", s[1], tx, ty + 66, round(nw) + 10, 70, 52, bold=False, color=BROWN, align="left")
        y += ps + 2 * RING + G1
        T(d, k, "Quote", q, (W - QW) // 2, y, QW, qh + 6, 52, bold=False, color=INK, lh=QLH)
        footer(d, k, white=False)
    return d


if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "v1"
    d = build(v)
    for k in range(1, d.n + 1):
        assert not os.path.exists(os.path.join(TILES, f"tm20261113-{v}-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
