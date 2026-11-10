"""Mon Nov 23: Foundation Courses + Compost Intensive Course promo, CIC student experience. Linnea's slide text
unchanged: the two student quotes. Cover line is the caption's closing question. Photo: Carla's CIC image (Drive
CIC.jpeg 1afK47cpk2xJ7sRtnWA-nbgtfca3Jx1cU); slides 2-3 use crops of its own photos (same post).

  python3 tools/wormhole-visuals/cic_voices_nov23.py <version>
"""
import sys

from PIL import Image

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


def logo(d, k, x, y, w=150):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y, shadowed=False, anchor="tl")


def strip(box, h, fy=0.5):
    im = Image.open(SRC).convert("RGB").crop(box)
    return grade(cover(im, W, h, 0.5, fy)).convert("RGBA")


def quote_slide(d, k, box, sh, fy, text, name):
    d.bg(k, Image.new("RGBA", (W, H), GREEN + (255,)), name="Food Web Green")
    d.put(k, "Photo", strip(box, sh, fy), 0, 0, shadowed=False, anchor="tl")
    qh = height(text, 50, 940, bold=False, lh=1.18)
    nh = height(name, 52, 940, lh=1.1)
    y = sh + max(50, (H - sh - qh - 30 - nh - 60) // 2)
    y = T(d, k, "Quote", text, 70, y, 940, qh + 8, 50, bold=False, color=CREAM, align="left", lh=1.18)
    T(d, k, "Name", name, 70, round(y) + 30, 940, nh + 8, 52, color=MINT, align="left", lh=1.1)


def build(v):
    d = Deck("cic20261123", 3, f"cic-student-voices-{v}", "2026-11-23")
    # 1. Carla's CIC image whole, the caption's question under it
    d.bg(0, Image.new("RGBA", (W, H), GREEN + (255,)), name="Food Web Green")
    ban = Image.open(SRC).convert("RGB")
    ban = grade(ban.resize((W, round(ban.height * W / ban.width)), Image.LANCZOS)).convert("RGBA")
    d.put(0, "CIC photo", ban, 0, 0, shadowed=False, anchor="tl")
    head = "Will we see\nyou in the CIC\nnext year?"
    hh = height(head, 86, 940, lh=1.06)
    T(d, 0, "Headline", head, 70, ban.height + (H - ban.height - round(hh)) // 2 - 30, 940, hh + 8, 86, color=CREAM, align="left", lh=1.06)
    logo(d, 0, W - 60 - 150, H - 50 - 150)
    # 2. Kamai, blue buckets crop  3. Pratik, compost in hand crop
    quote_slide(d, 1, (1575, 0, 2280, 780), 380, 0.55, KAMAI, "–Kamai Fatma")
    quote_slide(d, 2, (1575, 790, 2280, 1260), 300, 0.45, PRATIK, "–Pratik Thomas")
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
