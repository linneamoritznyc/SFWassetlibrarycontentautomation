"""Leave the leaves (p12), the 7-slide carousel from Stephanie's November doc, in the photo-and-box look Linnea
picked on 3 Nov, with Soil Brown boxes (the nematode post the day before has green ones). CC photos from
/home/user/photos/cc (credits-land.json, credits-micro.json), each used on no other post. Text 84 px.

  python3 tools/wormhole-visuals/p12_leaves.py
"""
import os

from PIL import Image, ImageOps

from collage import Deck, cover, paper
from nov_fill import BROWN, CREAM, DECKS, GREEN, TILES, WHITE, box, logo

W, H = 1080, 1350
CC = "/home/user/photos/cc"


def photo_slide(d, k, name, text, credit, color=BROWN, fy=0.5):
    img = ImageOps.exif_transpose(Image.open(f"{CC}/{name}")).convert("RGB")
    d.bg(k, cover(img, W, H, 0.5, fy).convert("RGBA"), name="Photo")
    first = len(d.items)
    bottom = d.text(k, "Headline", text, 112, 0, 820, 400, 84, kind="montserrat-bold", italic=False, color=CREAM,
                    lh=1.05, min_size=84)
    item = d.items[-1]
    th = round(bottom)
    top = H - 150 - th - 80
    item["y"] = top + 40
    box(d, k, "Box", color, 72, top, 900, th + 80)
    d.items.insert(first, d.items.pop())
    box(d, k, "Credit box", color, 72, H - 96, W - 144, 62)
    d.text(k, "Credit", credit, 92, H - 90, W - 184, 50, 42, kind="source-reg", italic=False, color=CREAM,
           lh=1.0, align="right", min_size=42)
    logo(d, k, WHITE, W - 72 - 120, 110, w=120)


def type_slide(d, k, head, detail):
    d.bg(k, paper(GREEN, 70 + k, w=W, h=H, grain=6), name="Background")
    y = d.text(k, "Headline", head, 90, 300, 900, 300, 84, kind="montserrat-bold", italic=False, color=CREAM,
               lh=1.05, min_size=84)
    d.text(k, "Details", detail, 90, round(y) + 40, 860, 360, 52, kind="source-reg", italic=False, color=CREAM,
           lh=1.22, min_size=50)
    logo(d, k, WHITE, W - 72 - 140, 1200, w=140)


if __name__ == "__main__":
    d = Deck("p12", 7, "leave-the-leaves-v4", "2026-11-10")
    photo_slide(d, 0, "leaf-decay-1.jpg", "Leave the leaves.", "Photo: David Lee, CC BY 2.0")
    photo_slide(d, 1, "leaf-skeleton-2.jpg", "Leaves are carbon and lignin.", "Photo: Paul VanDerWerf, CC BY 2.0",
                fy=0.4)
    photo_slide(d, 2, "fungal-hypha-2.jpg", "Fungi break down lignin.", "Photo: Matthew Rozanoff, CC BY 4.0")
    photo_slide(d, 3, "leaf-skeleton-1.jpg", "Leaf litter feeds the fungi.", "Photo: Jim Whitehead, CC BY 2.0")
    type_slide(d, 4, "Trees love fungal soil", "More fungi moves the soil toward the fungal dominance perennials, "
               "shrubs and trees prefer.")
    type_slide(d, 5, "A blanket for winter", "A litter layer shields the soil from raindrop impact over winter. "
               "Fungal residues become stable soil carbon.")
    type_slide(d, 6, "Shred them onto your beds", "On lawns: shred the leaves and move them to your beds.")
    for k in range(1, 8):
        assert not os.path.exists(os.path.join(TILES, f"p12-v4-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
