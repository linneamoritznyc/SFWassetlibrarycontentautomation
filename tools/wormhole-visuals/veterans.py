"""Veterans Day (vet20261111, 11 Nov), one slide built to docs/slide-rules.md.

Soil Brown banner with the headline (86 px), the small text (52 px) and the white logo; below it two
labelled photo spaces for Suzanne Shea's and Warlinda Walker's own conference photos (from Allison).
Never a stand-in photo next to their names. Swap the spaces for their photos in the deck.
  python3 tools/wormhole-visuals/veterans.py
"""
import os

from PIL import Image, ImageDraw

from collage import Deck, paper

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
LOGO = os.path.join(REPO, "apps", "web", "public", "wormhole", "brand", "sfw-foundation-logo-white.png")
CORN = "/home/user/sfwlib/social/cutouts-flowers/norfolk-cornflower.png"
W, H = 1080, 1350
BROWN, CREAM, INK = "#4F3433", "#F4F1EA", "#333130"


def space(w, h):
    im = Image.new("RGBA", (w, h), (226, 220, 206, 255))
    d = ImageDraw.Draw(im)
    for i in range(-h, w, 40):
        d.line((i, h, i + h, 0), fill=(79, 52, 51, 40), width=2)
    d.rectangle((0, 0, w - 1, h - 1), outline=(79, 52, 51, 255), width=4)
    return im


def main():
    d = Deck("vet20261111", 1, "veterans-day-v1", "2026-11-11")
    d.bg(0, paper(CREAM, 11, w=W, h=H, grain=5), name="Background")
    band = 470
    d.put(0, "Brown box", Image.new("RGBA", (W, band), BROWN), 0, 0, shadowed=False, anchor="tl")
    d.text(0, "Headline", "Happy Veterans Day", 72, 72, 936, 110, 86, kind="montserrat-bold", italic=False,
           color=CREAM, lh=1.05, min_size=84)
    d.text(0, "Details", "Suzanne Shea and Warlinda Walker met at the Farmer Veteran Coalition conference.",
           72, 200, 720, 230, 52, kind="source-reg", italic=False, color=CREAM, lh=1.2, min_size=50)
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((150, round(lg.height * 150 / lg.width)), Image.LANCZOS)
    d.put(0, "SFW logo", lg, W - 72 - 150, band - 48 - lg.height, shadowed=False, anchor="tl")
    for i, name in enumerate(["Suzanne Shea", "Warlinda Walker"]):
        x = 72 + i * 480
        d.put(0, f"Photo space {name}", space(456, 700), x, band + 64, shadowed=False, anchor="tl")
        d.text(0, f"Photo label {name}", f"PHOTO: {name}", x + 30, band + 360, 396,
               160, 44, kind="source-reg", italic=False, color=INK, lh=1.2, align="center", min_size=42)
    corn = Image.open(CORN).convert("RGBA")
    corn = corn.crop(corn.getchannel("A").getbbox())
    corn = corn.resize((260, round(corn.height * 260 / corn.width)), Image.LANCZOS)
    d.put(0, "Cornflower", corn, W - 190, H - 330, shadowed=False, anchor="tl")
    names, _ = d.save(TILES, DECKS)
    print(names, d.pptx_name())


if __name__ == "__main__":
    main()
