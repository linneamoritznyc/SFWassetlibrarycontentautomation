"""PDC congratulations (x20261220), slide 1 without the banned raised-beds photo (pdc_beds.jpg): a type card on
Food Web Green. Slides 2 and 3 stay as they are.

  python3 tools/wormhole-visuals/pdc_card.py
"""
from collage import Deck, paper
from nov_fill import CREAM, DECKS, GREEN, TILES, WHITE, logo

W, H = 1080, 1350

if __name__ == "__main__":
    d = Deck("x20261220", 1, "pdc-congratulations-v3", "2026-12-20")
    d.bg(0, paper(GREEN, 20, w=W, h=H, grain=6), name="Background")
    d.text(0, "Eyebrow", "PERMACULTURE DESIGN CERTIFICATE", 90, 300, 900, 60, 46, kind="pathway", italic=False,
           color=CREAM, lh=1.0, track=2, min_size=42)
    d.text(0, "Headline", "Congratulations, class of 2026!", 90, 380, 900, 300, 86, kind="montserrat-bold",
           italic=False, color=CREAM, lh=1.05, min_size=84)
    d.text(0, "Details", "Twelve weeks ago you started with a blank map. Now you have a design for a real place.",
           90, 690, 860, 260, 52, kind="source-reg", italic=False, color=CREAM, lh=1.22, min_size=50)
    logo(d, 0, WHITE, W - 90 - 150, 1180, w=150)
    print(d.save(TILES, DECKS)[0], d.pptx_name())
