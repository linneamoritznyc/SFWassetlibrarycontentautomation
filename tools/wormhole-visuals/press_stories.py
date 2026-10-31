"""Instagram Stories for the India workshop press coverage (Linnea, 31 Oct: "add stories about all these news
stories"). One 1080 x 1920 frame per outlet in the news card format, the same as the Times of India Story
(toi_evan.story): outlet tab, headline, one line, and the place for the link sticker under the card.
Every outlet gets its own photo from the Drive folder IN-Workshop Public Photos (checked with photo_check.py).

  python3 tools/wormhole-visuals/press_stories.py <photo dir>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

import collage
import news_cards as nc
from collage import Deck, cover
from nov_fill import BROWN, CREAM, GREEN, INK, LGREEN, box, grain
from regen_news import arrow_disc, logo_disc

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:
    pass

CREDIT = "Photo: Soil Food Web Foundation, Coimbatore"


def story(pid, slug, iso, img, outlet, headline, details, sticker, seed, fx=0.5, fy=0.5):
    """Text stays out of the top 250 and bottom 300 px (Instagram's bars)."""
    collage.H = 1920
    try:
        d = Deck(pid, 1, slug, iso)
        d.bg(0, grain(1080, 1920, seed).convert("RGBA"), name="Background")
        d.put(0, "Logo", logo_disc(120), 40, 120, shadowed=False, anchor="tl")
        cx, cw, top = 72, 936, 290
        px, pw, ph = cx + 28, cw - 56, 620
        first = len(d.items)
        d.put(0, "Photo", cover(img, pw, ph, fx, fy).convert("RGBA"), px, top + 28, shadowed=False, anchor="tl")
        tw = nc.tab_width(outlet)
        box(d, 0, "Tab", GREEN, px, top + 28 + ph - 70, tw, 70)
        d.text(0, "Tab text", outlet, px + 22, top + 28 + ph - 64, tw - 30, 62, 50, kind="source-reg", italic=True,
               color=CREAM, lh=1.0, min_size=42)
        d.text(0, "Credit", CREDIT, px, top + 28 + ph + 10, pw, 50, 42, kind="source-reg", italic=False,
               color=nc.BODY, lh=1.0, align="right", min_size=42)
        hy = top + 28 + ph + 76
        bottom = d.text(0, "Headline", headline, px + 34, hy, pw - 50, 290, 86, kind="montserrat-bold",
                        italic=False, color=BROWN, lh=1.05, min_size=84)
        box(d, 0, "Bar", LGREEN, px, hy + 8, 10, round(bottom) - hy - 14)
        end = round(d.text(0, "Details", details, px + 34, round(bottom) + 22, pw - 50, 200, 52, kind="source-reg",
                           italic=False, color=INK, lh=1.2, min_size=50)) + 50
        if end + 36 + 70 > 1920 - 300:
            raise SystemExit(f"{pid}: card runs into the bottom bar, cut words")
        box(d, 0, "Card", CREAM, cx, top, cw, end - top)  # as tall as its content
        d.items.insert(first, d.items.pop())
        d.text(0, "Sticker note", sticker, cx + 4, end + 36, 700, 70, 54, kind="mont-medium", italic=False,
               color=CREAM, lh=1.0, min_size=50)
        f = ImageFont.truetype(os.path.join(nc.FONTS, "Montserrat-SemiBold.ttf"), 54)
        w = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(sticker, font=f)
        d.put(0, "Arrow", arrow_disc().resize((56, 56), Image.LANCZOS), cx + 4 + round(w) + 24, end + 42,
              shadowed=False, anchor="tl")
        for k in (1,):
            p = os.path.join(nc.TILES, f"{pid}-{slug.rsplit('-', 1)[1]}-{k}.jpg")
            if os.path.exists(p):
                raise SystemExit(f"exists, not overwriting: {p}")
        names, _ = d.save(nc.TILES, nc.DECKS)
        return names, d.pptx_name()
    finally:
        collage.H = 1350


def photo(src, name):
    return ImageOps.exif_transpose(Image.open(os.path.join(src, name))).convert("RGB")


if __name__ == "__main__":
    src = sys.argv[1]
    print(story("st20261031n9", "news9-live-story-v1", "2026-10-31",
                photo(src, "eeb9febb-6efa-40e2-8d53-da50dae1a240.jpg"), "News9 Live",
                "“A meaningful step”",
                "Evan Buckman on bringing our Accelerator Workshop to India for the first time.",
                "Read the article", 411, fy=0.55))
    print(story("st20261031tv9", "tv9-gujarati-story-v1", "2026-10-31",
                photo(src, "99696ef1-0bb4-4626-b0c8-cf77fd2e04c7.JPG"), "TV9 Gujarati",
                "On TV9 Gujarati too!",
                "Two programmes in Coimbatore: the Life in the Soil Seminar and the Accelerator Workshop.",
                "See the post", 412, fy=0.5))
