"""New study: regenerative farms store 39% more soil carbon, in the news card format (the pinned New York
Times / Save Soil shoutout look from savesoil.py), as an editable deck.

Cover: cream card on Food Web Green, Figure 2 of the paper (CC BY 4.0) with a journal tab, Soil Brown
headline beside a Regenerative Green bar, Read More and the source. Slides 2 to 8: one fact per card.
Every card, photo, bar, text and the logo is its own layer.

  python3 tools/wormhole-visuals/regen_news.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw

from collage import Deck, cover

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
FIG = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/regen-news/lundgren2026-fig2.jpg"
W, H = 1080, 1350
CREAM, INK, BODY, GREEN, FOREST = "#F4F1EA", "#4F3433", "#6E5452", "#59A66C", "#156826"
URL = "doi.org/10.1088/2976-601X/ae8f4e"

HEADLINE = "The most regenerative farms stored 39% more carbon in their soil"
BLURB = "Lundgren et al. 2026, Environmental Research: Food Systems. The 1000 Farms Initiative, Ecdysis Foundation."
FACTS = [
    ("More soil life too: +181% total fungi, and more microbes, insects, plants and birds.",
     "Lundgren et al. 2026, figure 3"),
    ("Yields matched national averages and profit was similar. One practice alone changed nothing: the whole "
     "system matters.", ""),
]


LOGO = os.path.join(REPO, "apps", "web", "public", "wormhole", "sfw-foundation-wordmark-240.png")


def grain(w, h, seed):
    """Food Web Green with a quiet, uneven grain (the same texture as savesoil.py)."""
    rng = np.random.default_rng(seed)
    n = np.zeros((h, w), np.float32)
    for cells, amp in [(5, 1.0), (14, 0.55), (40, 0.3), (130, 0.18)]:
        g = rng.random((max(2, h * cells // w + 2), cells + 2)).astype(np.float32)
        n += amp * np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                              np.float32) / 255
    n = n / 2.03 + rng.normal(0, 0.06, (h, w)).astype(np.float32)
    n = np.clip((n - 0.25) * 1.6, 0, 1) ** 1.6
    lo, hi = np.array([14, 86, 30], np.float32), np.array([36, 122, 52], np.float32)
    return Image.fromarray(np.clip(lo + n[..., None] * (hi - lo), 0, 255).astype(np.uint8))


def rect(w, h, color):
    return Image.new("RGBA", (w, h), color)


def logo_disc(size=74):
    lg = Image.open(LOGO).convert("RGBA")
    lg.thumbnail((round(size * 0.8), round(size * 0.8)))
    disc = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, size - 1, size - 1), fill=(255, 255, 255, 255))
    disc.alpha_composite(lg, ((size - lg.width) // 2, (size - lg.height) // 2))
    return disc


def arrow_disc():
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 30, 30), fill=CREAM)
    d.polygon([(12, 8), (23, 16), (12, 24)], fill=FOREST)
    return im


def main():
    n = 1 + len(FACTS)
    d = Deck("news-regen39", n, "regenerative-farms-39-percent-carbon-news-v2", "2026-11-18")
    strip = grain(W * n, H, 339).convert("RGBA")
    d.bg(None, strip, name="background (one strip across the carousel)")
    put = lambda k, name, im, x, y: d.put(k, name, im, x, y, shadowed=False, anchor="tl")  # noqa: E731
    cx0, cx1 = 140, 940
    # cover
    cy0, cy1 = 150, 1110
    put(0, "card", rect(cx1 - cx0, cy1 - cy0, CREAM), cx0, cy0)
    px0, py0, px1, py1 = cx0 + 28, cy0 + 28, cx1 - 28, cy0 + 28 + 500
    put(0, "article image: Figure 2, Lundgren et al. 2026", cover(Image.open(FIG).convert("RGB"), px1 - px0,
                                                                   py1 - py0, 0.5, 0.45).convert("RGBA"), px0, py0)
    tab = "ENVIRONMENTAL RESEARCH: FOOD SYSTEMS"
    put(0, "tab", rect(560, 58, INK), px0, py1 - 58)
    d.text(0, "tab text", tab, px0 + 22, py1 - 52, 520, 50, 36, kind="pathway", italic=False, color=CREAM, lh=1.0,
           track=1, min_size=26)
    d.text(0, "credit", "Figure 2, Lundgren et al. 2026, CC BY 4.0", px0, py1 + 8, px1 - px0, 24, 17, kind="source-reg",
           italic=False, color=BODY, lh=1.0, align="right")
    put(0, "bar", rect(9, 168, GREEN), px0, py1 + 54)
    d.text(0, "headline", HEADLINE, px0 + 34, py1 + 48, px1 - px0 - 60, 180, 48, kind="montserrat-bold", italic=False,
               color=INK, lh=1.18, min_size=40)
    d.text(0, "blurb", BLURB, px0 + 34, py1 + 260, px1 - px0 - 60, 110, 26, kind="source-reg", italic=False,
           color=BODY, lh=1.35, min_size=20)
    d.text(0, "read more", "Read More", cx0 + 6, cy1 + 34, 200, 40, 26, kind="mont-medium", italic=False, color=CREAM,
           lh=1.0)
    put(0, "arrow", arrow_disc(), cx0 + 160, cy1 + 32)
    d.text(0, "source", "Source:\n" + URL, cx0 + 300, cy1 + 34, cx1 - cx0 - 300, 70, 22, kind="source-reg",
           italic=False, color=CREAM, lh=1.25, align="right")
    put(0, "logo", logo_disc(), 46, 42)
    # facts
    for k, (text, cite) in enumerate(FACTS, start=1):
        cy0, cy1 = 290, 1060
        put(k, "card", rect(cx1 - cx0, cy1 - cy0, CREAM), cx0, cy0)
        bottom = d.text(k, "fact", text, cx0 + 90, 0, cx1 - cx0 - 190, 480, 56, kind="montserrat-bold",
                        italic=False, color=INK, lh=1.2, min_size=36)
        th = round(bottom)
        y0 = round(cy0 + (cy1 - cy0 - th - (70 if cite else 0)) / 2)
        d.items[-1]["y"] = y0  # centre the fitted text on the card
        put(k, "bar", rect(9, th - 8, GREEN), cx0 + 56, y0 + 6)
        if cite:
            d.text(k, "cite", cite, cx0 + 92, cy1 - 80, cx1 - cx0 - 160, 40, 30, kind="source-reg", italic=False,
                   color=BODY, lh=1.2)
        if k == n - 1:
            d.text(k, "footer", "Full paper: link in bio.", 140, cy1 + 40, 800, 40, 24, kind="source-reg",
                   italic=False, color=CREAM, lh=1.0, align="center")
        put(k, "logo", logo_disc(), 46, 46)
    names, _ = d.save(TILES, DECKS)
    print(names, d.pptx_name())


if __name__ == "__main__":
    main()
