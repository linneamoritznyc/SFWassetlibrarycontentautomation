"""Leave the leaves (p12), exactly as Stephanie's November doc specifies (Linnea, 3 Nov): the doc's 7 slide texts word
for word and its image plan: autumn leaves on soil (slide 1), collage fungal hyphae (slides 3 and 4), microscopy of
fungal hyphae (slide 6). Photo slides in the photo-and-box look Linnea picked, Soil Brown boxes; the logo white in a
brown square, large. CC photos from /home/user/photos/cc (credits in credits-*.json), each used on no other post.

  python3 tools/wormhole-visuals/p12_leaves.py
"""
import os

from PIL import Image, ImageOps

from collage import Deck, cover, paper
from nov_fill import BROWN, CREAM, DECKS, TILES, WHITE, box

W, H = 1080, 1350
CC = "/home/user/photos/cc"
CUT = "/home/user/sfwlib/social/cutouts-soil"
LOGO_W = 190


def big_logo(d, k, color=BROWN):
    box(d, k, "Logo box", color, W - 72 - LOGO_W - 40, 72, LOGO_W + 40, LOGO_W + 40)
    lg = Image.open(WHITE).convert("RGBA")
    lg = lg.resize((LOGO_W, round(lg.height * LOGO_W / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 72 - LOGO_W - 20, 72 + 20 + (LOGO_W - lg.height) // 2, shadowed=False, anchor="tl")


def text_box(d, k, text, size):
    first = len(d.items)
    bottom = d.text(k, "Text", text, 112, 0, 830, 560, size, kind="montserrat-bold", italic=False, color=CREAM,
                    lh=1.08, min_size=size)
    item = d.items[-1]
    th = round(bottom)
    top = H - 150 - th - 80
    item["y"] = top + 40
    box(d, k, "Text box", BROWN, 72, top, 920, th + 80)
    d.items.insert(first, d.items.pop())


def credit(d, k, text):
    box(d, k, "Credit box", BROWN, 72, H - 96, W - 144, 62)
    d.text(k, "Credit", text, 92, H - 90, W - 184, 50, 42, kind="source-reg", italic=False, color=CREAM, lh=1.0,
           align="right", min_size=42)


def photo_slide(d, k, name, text, cred, size=70, fx=0.5, fy=0.5):
    img = ImageOps.exif_transpose(Image.open(f"{CC}/{name}")).convert("RGB")
    d.bg(k, cover(img, W, H, fx, fy).convert("RGBA"), name="Photo")
    text_box(d, k, text, size)
    credit(d, k, cred)
    big_logo(d, k)


def cutout(name, w):
    im = Image.open(f"{CUT}/{name}").convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def collage_slide(d, k, pieces, text):
    d.bg(k, paper(CREAM, 80 + k, w=W, h=H, grain=6), name="Background")
    for name, w, x, y in pieces:
        d.put(k, name.replace(".png", "").replace("-", " ").title(), cutout(name, w), x, y, shadowed=True,
              anchor="tl")
    text_box(d, k, text, 70)
    big_logo(d, k)


DOC = [
    "Fall leaves are free food for your soil.",
    "Leaf litter is high in carbon, cellulose and lignin.",
    "Saprotrophic fungi are the main decomposers of lignin. Leaf litter feeds fungal biomass.",
    "That pushes the fungal to bacterial ratio toward fungal dominance, which perennials, shrubs and trees prefer.",
    "A litter layer shields soil aggregates from raindrop impact over winter.",
    "Microbial residues, including fungal necromass, make up a large share of stable soil organic carbon.",
    "On lawns: shred the leaves and move them to your beds.",
]

if __name__ == "__main__":
    d = Deck("p12", 7, "leave-the-leaves-v6", "2026-11-10")
    photo_slide(d, 0, "leaf-skeleton-1.jpg", DOC[0], "Photo: Jim Whitehead, CC BY 2.0", size=84)
    photo_slide(d, 1, "leaf-skeleton-2.jpg", DOC[1], "Photo: Paul VanDerWerf, CC BY 2.0", fy=0.35)
    collage_slide(d, 2, [("dry-leaves-twigs.png", 560, 60, 120), ("compost-white-fungal-threads.png", 520, 440, 260)],
                  DOC[2])
    collage_slide(d, 3, [("compost-white-fungal-threads.png", 640, 70, 90), ("moss-clump.png", 300, 680, 360)],
                  DOC[3])
    photo_slide(d, 4, "leaf-decay-1.jpg", DOC[4], "Photo: David Lee, CC BY 2.0")
    photo_slide(d, 5, "fungal-hypha-2.jpg", DOC[5], "Fungal hyphae. Photo: Matthew Rozanoff, CC BY 4.0", size=66)
    photo_slide(d, 6, "leaf-mold-bin-2.jpg", DOC[6], "Photo: United Diversity, CC BY 2.0", fy=0.35)
    for k in range(1, 8):
        assert not os.path.exists(os.path.join(TILES, f"p12-v6-{k}.jpg"))
    print(d.save(TILES, DECKS)[0], d.pptx_name())
