"""Soil in numbers: nematodes (p24), in the look Linnea picked (3 Nov: "the first pic is good"): a dark micrograph,
big text in a Food Web Green box, editable layers. Slide 1 reuses the nematode from the p24 v2 cover; slides 2 and 3
use unused micrographs from our photo folder.

  python3 tools/wormhole-visuals/p24_dark.py
"""
import os

from PIL import Image, ImageOps

from collage import Deck, cover
from nov_fill import CREAM, DECKS, GREEN, TILES, WHITE, box, logo
from p12_leaves import big_logo

W, H = 1080, 1350
NEW = "/home/user/photos/new-2026-10"


def slide(d, k, img, text, credit):
    d.bg(k, cover(img, W, H, 0.5, 0.45).convert("RGBA"), name="Photo")
    first = len(d.items)
    bottom = d.text(k, "Headline", text, 112, 0, 820, 400, 84, kind="montserrat-bold", italic=False, color=CREAM,
                    lh=1.05, min_size=84)
    item = d.items[-1]
    th = round(bottom)
    top = H - 150 - th - 80
    item["y"] = top + 40
    box(d, k, "Green box", GREEN, 72, top, 900, th + 80)
    d.items.insert(first, d.items.pop())
    box(d, k, "Credit box", GREEN, W - 72 - 640, H - 96, 640, 62)
    d.text(k, "Credit", credit, W - 72 - 620, H - 90, 600, 50, 42, kind="source-reg", italic=False, color=CREAM, lh=1.0,
           align="right", min_size=42)
    big_logo(d, k, GREEN)


if __name__ == "__main__":
    d = Deck("p24", 3, "soil-in-numbers-nematodes-v5", "2026-11-09")
    first = Image.open(os.path.join(TILES, "p24-v2-1.jpg")).convert("RGB")
    black = Image.new("RGB", (W, H), (0, 0, 0))
    black.paste(first.crop((0, 170, W, 860)), (0, 300))  # below the old logo
    slide(d, 0, black, "440 quintillion nematodes.", "Photo: Soil Food Web Foundation")
    slide(d, 1, ImageOps.exif_transpose(Image.open(f"{NEW}/Bacterial-feeding nematode (omnivore), 40x obj, "
                                                   "Johannes Veith.jpg")).convert("RGB"),
          "About 57 billion for every person alive.", "Photo: Johannes Veith")
    slide(d, 2, ImageOps.exif_transpose(Image.open(f"{NEW}/Bacterial-feeding nematode (omnivore), 40x obj, "
                                                   "Keisha Wheeler.jpg")).convert("RGB"),
          "Most feed on bacteria and fungi.", "Photo: Keisha Wheeler")
    for k in (1, 2, 3):
        assert not os.path.exists(os.path.join(TILES, f"p24-v5-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
