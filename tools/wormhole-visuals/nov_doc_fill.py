"""Two November doc posts that had no editable deck (Linnea, 3 Nov: every visual for Stephanie's doc as pptx).

  p12  Leave the leaves (doc: 7-slide carousel "Bagging fall leaves..."): paper, flower cutouts in the corners
  p24  Soil in numbers: nematodes (doc: white slide, big number, nematode cutout), 3 slides

Text at docs/slide-rules.md sizes; every object its own layer.
  python3 tools/wormhole-visuals/nov_doc_fill.py
"""
import os

import numpy as np
from PIL import Image

from collage import Deck, paper
from nov_fill import BROWN, COLOR, CREAM, DECKS, FL, GREEN, INK, TILES, WHITE, box, logo

W, H = 1080, 1350


def flower(d, k, name, w, x, y):
    im = Image.open(f"{FL}/{name}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    d.put(k, name.split("-", 1)[-1].replace("-", " ").title(), im, x, y, shadowed=False, anchor="tl")
    return im.height


LEAVES = [  # (headline, detail, ground)
    ("Leave the leaves", "Myth: fall leaves need to be cleaned up.", "cream"),
    ("Leaves are carbon and lignin", "Leaf litter is high in carbon, cellulose and lignin.", "green"),
    ("Fungi break down lignin", "Saprotrophic fungi are the main decomposers of lignin. Leaf litter feeds fungal "
                                "biomass.", "cream"),
    ("Trees love fungal soil", "More fungi moves the soil toward the fungal dominance perennials, shrubs and trees "
                               "prefer.", "tan"),
    ("A blanket for winter", "A litter layer shields soil aggregates from raindrop impact over winter.", "green"),
    ("Fungi become soil carbon", "Microbial residues, including fungal necromass, make up a large share of stable "
                                 "soil organic carbon.", "cream"),
    ("Shred them onto your beds", "On lawns: shred the leaves and move them to your beds.", "tan"),
]
GROUND = {"cream": (CREAM, BROWN, INK, COLOR), "green": (GREEN, CREAM, CREAM, WHITE),
          "tan": ("#D8C3A5", BROWN, INK, COLOR)}
FLOWERS = ["norfolk-cornflower", "norfolk-common-poppy", "norfolk-foxglove", "norfolk-sea-lavender"]


def leaves():
    n = len(LEAVES)
    d = Deck("p12", n, "leave-the-leaves-v3", "2026-11-10")
    for k, (head, det, g) in enumerate(LEAVES):
        bg, hc, dc, lg = GROUND[g]
        d.bg(k, paper(bg, 40 + k, w=W, h=H, grain=5), name="Background")
        y = d.text(k, "Headline", head, 90, 150, 900, 300, 86 if k == 0 else 84, kind="montserrat-bold",
                   italic=False, color=hc, lh=1.05, min_size=84)
        d.text(k, "Details", det, 90, round(y) + 36, 820, 330, 52, kind="source-reg", italic=False, color=dc,
               lh=1.22, min_size=50)
        # flowers stand in the bottom corners, well below the text
        fh = flower(d, k, FLOWERS[k % 4], 200, 70 if k % 2 else W - 270, 0)
        d.items[-1]["y"] = H - fh - 40
        logo(d, k, lg, (W - 72 - 140) if k % 2 else 72, 1240, w=140)
    return d


def nematode_cutout():
    """The nematode from the p24 v2 photo (on black): black becomes transparent."""
    im = Image.open(os.path.join(TILES, "p24-v2-1.jpg")).convert("RGB").crop((0, 120, 1080, 820))
    a = np.asarray(im).astype(int)
    lum = a.max(axis=2)
    alpha = np.clip((lum - 28) * 6, 0, 255).astype("uint8")
    out = Image.fromarray(np.dstack([a.astype("uint8"), alpha]), "RGBA")
    return out.crop(out.getchannel("A").getbbox())


def nematodes():
    d = Deck("p24", 3, "soil-in-numbers-nematodes-v3", "2026-11-09")
    nem = nematode_cutout()
    for k in range(3):
        d.bg(k, paper("#FBF9F4", 60 + k, w=W, h=H, grain=4), name="Background")
    d.text(0, "Number", "440,000,000,000,000,000,000", 72, 140, 936, 420, 110, kind="montserrat-bold", italic=False,
           color=GREEN, lh=1.0, min_size=96)
    d.text(0, "Details", "Soil nematodes on Earth.", 72, 560, 900, 80, 64, kind="montserrat-bold", italic=False,
           color=BROWN, lh=1.1, min_size=60)
    w = 820
    im = nem.resize((w, round(nem.height * w / nem.width)), Image.LANCZOS)
    d.put(0, "Nematode", im, 130, 760, shadowed=False, anchor="tl")
    d.text(0, "Source", "van den Hoogen et al., Nature, 2019", 72, 1250, 700, 60, 42, kind="source-reg",
           italic=False, color=INK, lh=1.0, min_size=42)
    d.text(1, "Number", "57 billion", 72, 300, 936, 200, 160, kind="montserrat-bold", italic=False, color=GREEN,
           lh=1.0, min_size=120)
    d.text(1, "Details", "nematodes for every person alive.", 72, 520, 900, 200, 72, kind="montserrat-bold",
           italic=False, color=BROWN, lh=1.1, min_size=66)
    im2 = nem.resize((520, round(nem.height * 520 / nem.width)), Image.LANCZOS).rotate(-12, expand=True)
    d.put(1, "Nematode", im2, W - im2.width - 60, 830, shadowed=False, anchor="tl")
    d.text(2, "Headline", "Most feed on bacteria and fungi", 72, 220, 936, 300, 84, kind="montserrat-bold",
           italic=False, color=BROWN, lh=1.05, min_size=84)
    d.text(2, "Details", "When they eat, they release nitrogen in a form plant roots can take up.", 72, 520, 860,
           200, 52, kind="source-reg", italic=False, color=INK, lh=1.22, min_size=50)
    im3 = nem.resize((600, round(nem.height * 600 / nem.width)), Image.LANCZOS)
    d.put(2, "Nematode", im3, 72, 860, shadowed=False, anchor="tl")
    for k in range(3):
        logo(d, k, COLOR, W - 72 - 140, 1250, w=140)
    return d


if __name__ == "__main__":
    for d in (leaves(), nematodes()):
        for k in range(1, d.n + 1):
            p = os.path.join(TILES, f"{d.id}-v3-{k}.jpg")
            if os.path.exists(p):
                raise SystemExit(f"exists, not overwriting: {p}")
        print(d.save(TILES, DECKS)[0], d.pptx_name())
