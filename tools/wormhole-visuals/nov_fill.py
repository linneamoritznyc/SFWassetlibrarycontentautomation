"""Stand-in visuals for the November doc, built to docs/slide-rules.md (30 Oct).

  vet20261111     Veterans Day: type card about the event (Suzanne and Warlinda at the FVC conference)
  crinfo20261105  Costa Rica info session: Education Blue info banner, class photo below
  news-1000farms  39% soil carbon study (news: v4 split card; news-card: v5, the exact savesoil.py format)
  python3 tools/wormhole-visuals/nov_fill.py [ids]
"""
import os
import sys

from PIL import Image, ImageEnhance, ImageOps

from collage import Deck, cover, paper
from regen_news import grain

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
WHITE = os.path.join(REPO, "apps", "web", "public", "wormhole", "brand", "sfw-foundation-logo-white.png")
COLOR = "/home/user/sfwlib/img/sfwlogo-240.png"
FL = "/home/user/sfwlib/social/cutouts-flowers"
NEW = "/home/user/photos/new-2026-10"
SCR = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad"
W, H = 1080, 1350
BROWN, CREAM, INK, GREEN, BLUE, LGREEN = "#4F3433", "#F4F1EA", "#333130", "#156826", "#3780B8", "#59A66C"


def box(d, k, name, color, x, y, w, h):
    d.put(k, name, Image.new("RGBA", (w, h), color), x, y, shadowed=False, anchor="tl")


def logo(d, k, path, x, y, w=150):
    lg = Image.open(path).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, x, y - lg.height // 2, shadowed=False, anchor="tl")


def flower(d, k, name, w, x, y):
    im = Image.open(f"{FL}/{name}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    d.put(k, name.split("-", 1)[-1].replace("-", " ").title(), im, x, y, shadowed=False, anchor="tl")


def photo(path, w, h, fy=0.4, lift=1.0):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if lift != 1.0:
        im = ImageEnhance.Brightness(im).enhance(lift)
    return cover(im, w, h, 0.5, fy).convert("RGBA")


def veterans():
    """Type card about the event itself: who met, where, when. No stand-in photo (they are named)."""
    d = Deck("vet20261111", 1, "veterans-day-v3", "2026-11-11")
    d.bg(0, paper(CREAM, 11, w=W, h=H, grain=5), name="Background")
    box(d, 0, "Brown box", BROWN, 72, 150, 936, 1050)
    d.text(0, "Headline", "Happy Veterans Day", 136, 214, 808, 200, 86, kind="montserrat-bold", italic=False,
           color=CREAM, lh=1.05, min_size=84)
    d.text(0, "Details", "Suzanne Shea and Warlinda Walker, two of our community, met at the Farmer Veteran "
           "Coalition conference.\n\nWilliamsburg, Virginia, October 2026.", 136, 440, 760, 650, 52,
           kind="source-reg", italic=False, color=CREAM, lh=1.22, min_size=50)
    logo(d, 0, WHITE, W - 72 - 64 - 150, 1110)
    flower(d, 0, "norfolk-cornflower", 240, 10, 1060)
    return d


def info_session():
    d = Deck("crinfo20261105", 1, "costa-rica-info-session-v2", "2026-11-05")
    band = 450
    d.put(0, "Photo", photo(f"{SCR}/crphotos/PXL_20251024_162714282.jpg", W, H - band, 0.55, 1.3), 0, band,
          shadowed=False, anchor="tl")
    box(d, 0, "Blue box", BLUE, 0, 0, W, band)
    d.text(0, "Headline", "Costa Rica info session", 72, 64, 936, 110, 84, kind="montserrat-bold", italic=False,
           color=CREAM, lh=1.05, min_size=70)
    d.text(0, "Details", "Fri 6 Nov, 12pm Pacific, live on Zoom.\nFree. Link in bio.", 72, 200, 720, 200, 52,
           kind="source-reg", italic=False, color=CREAM, lh=1.25, min_size=50)
    logo(d, 0, WHITE, W - 72 - 155, 290, w=155)
    flower(d, 0, "costa-rica-heliconia", 220, W - 170, H - 470)
    return d


FIG = f"{SCR}/regen-news/lundgren2026-fig2.jpg"
FACTS = [
    ("The 1000 Farms Initiative measured working farms across North America.", "From the most conventional to the most regenerative. Led by Ecdysis Foundation."),
    ("39% more total soil carbon", "on the most regenerative farms."),
    ("+181% total fungi", "in the most regenerative soils (figure 3 of the paper)."),
    ("More life everywhere", "Soil microbes, insects, plants and birds. The more biodiversity, the more carbon stored."),
    ("Yields matched national averages", "and net profit per acre was similar."),
    ("One practice alone changed nothing", "Farms using a single regenerative practice looked like conventional farms."),
    ("Read the paper", "Lundgren et al., Environmental Research: Food Systems, 2026. Link in bio."),
]


def news():
    n = 1 + len(FACTS)
    d = Deck("news-1000farms", n, "regenerative-farms-39-percent-carbon-v4", "2026-11-20")
    d.bg(None, grain(W * n, H, 339).convert("RGBA"), name="Background")
    # cover: the paper's figure on top, cream card with the headline below
    box(d, 0, "Figure card", CREAM, 72, 72, 936, 560)
    d.put(0, "Photo: Figure 2, Lundgren et al. 2026", photo(FIG, 896, 460, 0.45), 92, 92, shadowed=False, anchor="tl")
    box(d, 0, "Tab", BROWN, 92, 500, 620, 52)
    d.text(0, "Tab text", "ENVIRONMENTAL RESEARCH: FOOD SYSTEMS", 112, 506, 590, 44, 40, kind="pathway",
           italic=False, color=CREAM, lh=1.0, min_size=32)
    d.text(0, "Credit", "Figure 2, Lundgren et al. 2026, CC BY 4.0", 92, 590, 896, 40, 30, kind="source-reg",
           italic=False, color=INK, lh=1.0, align="right")
    box(d, 0, "Cream card", CREAM, 72, 660, 936, 560)
    box(d, 0, "Bar", LGREEN, 112, 708, 10, 300)
    d.text(0, "Headline", "Regenerative farms stored 39% more soil carbon", 146, 700, 830, 330, 84,
           kind="montserrat-bold", italic=False, color=BROWN, lh=1.05, min_size=72)
    d.text(0, "Details", "A new study of working farms. Link in bio.", 146, 1050, 600, 150, 52, kind="source-reg",
           italic=False, color=INK, lh=1.2, min_size=50)
    logo(d, 0, COLOR, W - 72 - 40 - 150, 1150, w=150)
    for k, (headline, detail) in enumerate(FACTS, start=1):
        y_h = d.text(k, "Headline", headline, 146, 0, 830, 400, 73, kind="montserrat-bold", italic=False,
                     color=BROWN, lh=1.08, min_size=66)
        h_item = d.items[-1]
        y_d = d.text(k, "Details", detail, 146, round(y_h) + 36, 830, 320, 52, kind="source-reg", italic=False,
                     color=INK, lh=1.25, min_size=50)
        d_item = d.items[-1]
        card_h = round(y_d) + 72 + 150 + 40  # room for the logo under the text, inside the card
        top = (H - card_h - 72) // 2
        h_item["y"] += top + 72
        d_item["y"] += top + 72
        box(d, k, "Cream card", CREAM, 72, top, 936, card_h)
        box(d, k, "Bar", LGREEN, 112, top + 80, 10, round(y_h) - 12)
        logo(d, k, COLOR, W - 72 - 40 - 150, top + card_h - 40 - 60, w=150)
    return d

CARD_FACTS = [
    ("1,000 Farms", "The 1000 Farms Initiative measured working farms across North America, from the most "
     "conventional to the most regenerative. Led by Ecdysis Foundation."),
    ("39% more soil carbon", "on the most regenerative farms."),
    ("+181% total fungi", "in the most regenerative soils (figure 3 of the paper)."),
    ("More life everywhere", "Soil microbes, insects, plants and birds. The more biodiversity, the more carbon "
     "stored."),
    ("Same yields", "Yields matched national averages, and net profit per acre was similar."),
    ("The whole system counts", "Farms using one regenerative practice alone looked like conventional farms."),
    ("Read the paper", "Lundgren et al., Environmental Research: Food Systems, 2026. Link in bio."),
]


def news_card():
    """The news card format exactly as savesoil.py / the Save Soil posts: one cream card on the green grain
    (article image with outlet tab, credit, green bar + headline, blurb), Read More and Source under the card,
    the logo disc top left. Fact slides: one cream card, green bar, headline. Text at docs/slide-rules.md sizes."""
    from regen_news import arrow_disc, logo_disc
    n = 1 + len(CARD_FACTS)
    d = Deck("news-1000farms", n, "regenerative-farms-39-percent-carbon-v5", "2026-11-20")
    d.bg(None, grain(W * n, H, 339).convert("RGBA"), name="Background")
    for k in range(n):
        d.put(k, "Logo", logo_disc(110), 40, 36, shadowed=False, anchor="tl")
    cx, cw = 72, 936
    # cover
    box(d, 0, "Card", CREAM, cx, 176, cw, 1000)
    px, py, pw, ph = cx + 28, 204, cw - 56, 400
    d.put(0, "Article image: Figure 2, Lundgren et al. 2026", photo(FIG, pw, ph, 0.0), px, py, shadowed=False,
          anchor="tl")
    box(d, 0, "Tab", BROWN, px, py + ph - 64, 640, 64)
    d.text(0, "Tab text", "ENVIRONMENTAL RESEARCH: FOOD SYSTEMS", px + 20, py + ph - 58, 610, 56, 46, kind="pathway",
           italic=False, color=CREAM, lh=1.0, min_size=42)
    d.text(0, "Credit", "Figure 2, Lundgren et al. 2026, CC BY 4.0", px, py + ph + 10, pw, 50, 42, kind="source-reg",
           italic=False, color="#6E5452", lh=1.0, align="right", min_size=42)
    bottom = d.text(0, "Headline", "Regenerative farms stored 39% more soil carbon", px + 34, 676, pw - 50, 290, 84,
                    kind="montserrat-bold", italic=False, color=BROWN, lh=1.05, min_size=84)
    box(d, 0, "Bar", LGREEN, px, 684, 10, round(bottom) - 690)
    d.text(0, "Details", "A study of working farms across North America.", px + 34, round(bottom) + 24, pw - 50, 140,
           52, kind="source-reg", italic=False, color=INK, lh=1.2, min_size=50)
    d.text(0, "Read More", "Read More", cx + 4, 1204, 300, 64, 52, kind="mont-medium", italic=False, color=CREAM,
           lh=1.0, min_size=50)
    d.put(0, "Arrow", arrow_disc().resize((48, 48), Image.LANCZOS), cx + 318, 1210, shadowed=False, anchor="tl")
    d.text(0, "Source", "Source:\ndoi.org/10.1088/2976-601X/ae8f4e", cx + 380, 1200, cw - 380, 110, 42,
           kind="source-reg", italic=False, color=CREAM, lh=1.15, align="right", min_size=42)
    # facts: one card each, bar beside the headline, detail under it
    for k, (headline, detail) in enumerate(CARD_FACTS, start=1):
        y_h = d.text(k, "Headline", headline, 166, 0, 790, 460, 84, kind="montserrat-bold", italic=False,
                     color=BROWN, lh=1.05, min_size=84)
        h_item = d.items[-1]
        y_d = d.text(k, "Details", detail, 166, round(y_h) + 32, 790, 420, 52, kind="source-reg", italic=False,
                     color=INK, lh=1.22, min_size=50)
        d_item = d.items[-1]
        card_h = round(y_d) + 2 * 80
        top = (H - card_h) // 2
        h_item["y"] += top + 80
        d_item["y"] += top + 80
        box(d, k, "Card", CREAM, cx, top, cw, card_h)
        box(d, k, "Bar", LGREEN, 124, top + 90, 10, round(y_h) - 14)
    return d


BUILD = {"vet20261111": veterans, "crinfo20261105": info_session, "news-1000farms": news, "news-card": news_card}

if __name__ == "__main__":
    for pid in sys.argv[1:] or BUILD:
        d = BUILD[pid]()
        names, _ = d.save(TILES, DECKS)
        print(pid, names, d.pptx_name())
