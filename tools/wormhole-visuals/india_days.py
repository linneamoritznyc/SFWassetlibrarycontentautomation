"""Kisan Diwas (k20261223) and Pongal (j20270115b) with real photos from the October 2026 India workshop
(Drive: IN-Workshop Public Photos), replacing the generic photo-and-tag stand-ins. Two different families so the
grid stays varied. Text at docs/slide-rules.md sizes.

  python3 tools/wormhole-visuals/india_days.py <photo dir>
"""
import os
import sys

from PIL import Image, ImageOps

from collage import Deck, cover, paper
from nov_fill import BROWN, COLOR, CREAM, DECKS, GREEN, INK, TILES, WHITE, box, logo

W, H = 1080, 1350


def photo(src, name):
    return ImageOps.exif_transpose(Image.open(os.path.join(src, name))).convert("RGB")


def kisan(src):
    """Family K, framed photo: cream paper, the headline on top, the group in the arecanut grove in a frame."""
    d = Deck("k20261223", 1, "kisan-diwas-v3", "2026-12-23")
    d.bg(0, paper(CREAM, 23, w=W, h=H, grain=5), name="Background")
    d.text(0, "Headline", "Happy Kisan Diwas", 72, 90, 936, 110, 86, kind="montserrat-bold", italic=False,
           color=BROWN, lh=1.05, min_size=84)
    d.text(0, "Details", "Thank you to every farmer in India.", 72, 205, 936, 70, 52, kind="source-reg",
           italic=False, color=INK, lh=1.2, min_size=50)
    box(d, 0, "Frame", BROWN, 72, 318, 936, 836)
    d.put(0, "Photo: workshop group in the arecanut grove, Coimbatore",
          cover(photo(src, "b6802170-089b-4df2-9475-2733dda763e7.jpg"), 908, 808, 0.5, 0.55).convert("RGBA"),
          86, 332, shadowed=False, anchor="tl")
    d.text(0, "Credit", "Our Accelerator Workshop at the Save Soil farm, Coimbatore, October 2026", 72, 1172, 700,
           110, 42, kind="source-reg", italic=False, color=INK, lh=1.2, min_size=42)
    logo(d, 0, COLOR, W - 72 - 140, 1232, w=140)
    return d


def pongal(src):
    """Food Web Green with the harvest offering on a banana leaf, the headline in cream below it."""
    d = Deck("j20270115b", 1, "happy-pongal-v3", "2027-01-15")
    d.bg(0, paper(GREEN, 15, w=W, h=H, grain=6), name="Background")
    box(d, 0, "Photo frame", CREAM, 72, 72, 936, 836)
    d.put(0, "Photo: harvest offering on a banana leaf, Coimbatore",
          cover(photo(src, "e696061c-21d1-45e0-9686-4bf0d8493664.jpg"), 908, 808, 0.5, 0.5).convert("RGBA"),
          86, 86, shadowed=False, anchor="tl")
    d.text(0, "Headline", "Happy Pongal!", 72, 960, 936, 110, 86, kind="montserrat-bold", italic=False,
           color=CREAM, lh=1.05, min_size=84)
    d.text(0, "Details", "To every farmer in Tamil Nadu.", 72, 1078, 760, 70, 52, kind="source-reg", italic=False,
           color=CREAM, lh=1.2, min_size=50)
    d.text(0, "Credit", "Our India workshop, October 2026", 72, 1180, 760, 60, 42, kind="source-reg",
           italic=False, color=CREAM, lh=1.2, min_size=42)
    logo(d, 0, WHITE, W - 72 - 140, 1180, w=140)
    return d


if __name__ == "__main__":
    for fn in (kisan, pongal):
        d = fn(sys.argv[1])
        for k in range(1, d.n + 1):
            p = os.path.join(TILES, f"{d.id}-v3-{k}.jpg")
            if os.path.exists(p):
                raise SystemExit(f"exists, not overwriting: {p}")
        print(d.save(TILES, DECKS)[0], d.pptx_name())
