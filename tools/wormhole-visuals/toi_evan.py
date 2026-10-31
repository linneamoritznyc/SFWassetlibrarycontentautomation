"""Times of India post and Story with Linnea's pick (31 Oct): Evan Buckman teaching in Coimbatore, from the Drive
folder IN-Workshop Public Photos (file 1JdGCPIREe4n7PKLeoPSdfUIYeoA-fXuR). News card format, text at slide-rules sizes.

  python3 tools/wormhole-visuals/toi_evan.py <evan.jpg>
"""
import sys

from PIL import Image, ImageOps

import collage
import news_cards as nc
from collage import Deck, cover
from nov_fill import BROWN, CREAM, GREEN, INK, LGREEN, box, grain
from regen_news import arrow_disc, logo_disc

CREDIT = "Evan Buckman teaching in Coimbatore"
SRC = nc.TOI_SRC


def feed(img):
    n = 6
    d = Deck("toi20261031", n, "times-of-india-coimbatore-workshop-v5", "2026-10-31")
    d.bg(None, grain(1080 * n, 1350, 409).convert("RGBA"), name="Background")
    for k in range(n):
        d.put(k, "Logo", logo_disc(110), 40, 36, shadowed=False, anchor="tl")
    nc.card(d, 0, img, "The Times of India", CREDIT, "We made the Times of India",
            "Our India Accelerator Workshop, Coimbatore, Tamil Nadu.", SRC)
    nc.fact(d, 1, "46 participants from 10 countries", "Farmers, soil scientists, microbiologists and "
            "consultants, from seven Indian states and abroad.")
    nc.fact(d, 2, "At the Save Soil model farm", "Ten days at Sadhguru's Save Soil Regenerative Revolution farm, "
            "in collaboration with Isha Outreach.")
    nc.fact(d, 3, "Compost to microscope", "BioComplete™ compost, compost extracts and teas, soil sampling and "
            "microscopy sessions.")
    nc.fact(d, 4, "61 at the seminar first", "The two-day Life in the Soil Seminar ran on 16 and 17 October.")
    nc.fact(d, 5, "Read the article", "The Times of India, 30 October 2026. Link in bio.")
    return d


def story(img):
    """One 1080 x 1920 Story frame. Text stays out of the top 250 and bottom 300 px (Instagram's bars)."""
    collage.H = 1920
    try:
        d = Deck("st20261031toi", 1, "times-of-india-story-v1", "2026-10-31")
        d.bg(0, grain(1080, 1920, 410).convert("RGBA"), name="Background")
        d.put(0, "Logo", logo_disc(120), 40, 120, shadowed=False, anchor="tl")
        cx, cw, top = 72, 936, 290
        px, pw, ph = cx + 28, cw - 56, 700
        first = len(d.items)
        d.put(0, "Photo: Evan Buckman teaching", cover(img, pw, ph, 0.42, 0.45).convert("RGBA"), px, top + 28,
              shadowed=False, anchor="tl")
        tw = nc.tab_width("The Times of India")
        box(d, 0, "Tab", GREEN, px, top + 28 + ph - 70, tw, 70)
        d.text(0, "Tab text", "The Times of India", px + 22, top + 28 + ph - 64, tw - 30, 62, 50, kind="source-reg",
               italic=True, color=CREAM, lh=1.0, min_size=42)
        d.text(0, "Credit", CREDIT, px, top + 28 + ph + 10, pw, 50, 42, kind="source-reg", italic=False,
               color=nc.BODY, lh=1.0, align="right", min_size=42)
        hy = top + 28 + ph + 76
        bottom = d.text(0, "Headline", "We made the Times of India!", px + 34, hy, pw - 50, 200, 86,
                        kind="montserrat-bold", italic=False, color=BROWN, lh=1.05, min_size=84)
        box(d, 0, "Bar", LGREEN, px, hy + 8, 10, round(bottom) - hy - 14)
        end = round(d.text(0, "Details", "46 people from 10 countries learned with us in Coimbatore.", px + 34,
                           round(bottom) + 22, pw - 50, 140, 52, kind="source-reg", italic=False, color=INK, lh=1.2,
                           min_size=50)) + 50
        box(d, 0, "Card", CREAM, cx, top, cw, end - top)  # as tall as its content
        d.items.insert(first, d.items.pop())
        # where the link sticker goes, under the card
        d.text(0, "Sticker note", "Read the article", cx + 4, end + 36, 600, 70, 54, kind="mont-medium",
               italic=False, color=CREAM, lh=1.0, min_size=50)
        d.put(0, "Arrow", arrow_disc().resize((56, 56), Image.LANCZOS), cx + 520, end + 42, shadowed=False,
              anchor="tl")
        names, _ = d.save(nc.TILES, nc.DECKS)
        return names, d.pptx_name()
    finally:
        collage.H = 1350


if __name__ == "__main__":
    img = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert("RGB")
    if sys.argv[2:] != ["story"]:
        d = feed(img)
        print(d.save(nc.TILES, nc.DECKS)[0], d.pptx_name())
    print(story(img))
