"""What we're thankful for (thx20261126, 26 Nov), one slide, built to docs/slide-rules.md.

Food Web Green banner on top (headline 86 px Montserrat Bold, small text 52 px Source Sans 3, white logo
150 px bottom right of the banner), the photo below it, a marigold cutout breaking out of the top right.
  python3 tools/wormhole-visuals/thankful.py
"""
import os

from PIL import Image

from collage import Deck, cover

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
PHOTO = "/home/user/photos/new-2026-10/students-laughing-together.jpg"
LOGO = os.path.join(REPO, "apps", "web", "public", "wormhole", "brand", "sfw-foundation-logo-white.png")
MARIGOLD = "/home/user/sfwlib/social/cutouts-flowers/tamil-nadu-marigold.png"
W, H = 1080, 1350
GREEN, CREAM = "#156826", "#F4F1EA"


def main():
    d = Deck("thx20261126", 1, "what-we-are-thankful-for-v2", "2026-11-26")
    band = 470
    d.put(0, "Photo", cover(Image.open(PHOTO).convert("RGB"), W, H - band, 0.5, 0.3).convert("RGBA"), 0, band,
          shadowed=False, anchor="tl")
    d.put(0, "Green box", Image.new("RGBA", (W, band), GREEN), 0, 0, shadowed=False, anchor="tl")
    d.text(0, "Headline", "What we're thankful for", 72, 72, 936, 220, 86, kind="montserrat-bold", italic=False,
           color=CREAM, lh=1.05, min_size=84)
    d.text(0, "Details", "Our staff share what made an impact on them this year.", 72, 290, 720, 140, 52,
           kind="source-reg", italic=False, color=CREAM, lh=1.2, min_size=50)
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((150, round(lg.height * 150 / lg.width)), Image.LANCZOS)
    d.put(0, "SFW logo", lg, W - 72 - 150, band - 40 - lg.height, shadowed=False, anchor="tl")
    mg = Image.open(MARIGOLD).convert("RGBA")
    mg = mg.crop(mg.getchannel("A").getbbox())
    mg = mg.resize((300, round(mg.height * 300 / mg.width)), Image.LANCZOS)
    d.put(0, "Marigold", mg, W - 210, H - 250, shadowed=False, anchor="tl")
    names, _ = d.save(TILES, DECKS)
    print(names, d.pptx_name())


if __name__ == "__main__":
    main()
