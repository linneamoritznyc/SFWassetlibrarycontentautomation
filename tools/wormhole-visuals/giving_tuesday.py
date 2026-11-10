"""GivingTuesday carousel, Tue 1 Dec 2026 (Linnea, 10 Nov): sister to the Cyber Monday visual. Food Web Green leaf
texture, white (cream) line illustrations, Montserrat Bold + Source Sans 3, one reason per slide.
Facts from Linnea's brief: 40+ years (Foundation facts), India seminar and workshop numbers, the 100,000 acres goal
(bundle sales page). Confirm with Stephanie what the gifts fund before posting (slide 5).

  python3 tools/wormhole-visuals/giving_tuesday.py <version>
"""
import sys

from PIL import Image

from cyber_nov30 import CREAM, MINT, leaf_texture, lineart, logo
from bundle_three_styles_v12 import T, height
from bundle_v6 import H, W
from collage import Deck
from nov_fill import DECKS, TILES

SLIDES = [
    ("seedling-fungi", "Why give on Giving Tuesday?", None),
    ("microscope", "We carry Dr. Elaine Ingham’s science forward",
     "40+ years of soil food web research, taught by her team."),
    ("globe-sprouts", "We teach farmers around the world",
     "This year in India: 61 farmers at our Life in the Soil seminar, 46 participants from 10 countries at our workshop."),
    ("sunrise", "Our goal: 100,000 acres regenerated in 2027", None),
    ("hands", "Your gift helps a student learn to restore soil", "Link in bio"),
]


IND = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/india/raw"
NEW = "/home/user/photos/new-2026-10"
GREEN = "#156826"


def build(v):
    """v7 (Linnea, 10 Nov): slide 1 as before; slides 2 to 5 one real photo edge to edge with a solid Food Web Green
    band at the bottom, left-aligned Montserrat Bold; slide 3 has two photos side by side."""
    from PIL import ImageOps
    from collage import cover
    from bundle_three_styles import rgb
    d = Deck("x20261201", 5, f"giving-tuesday-{v}", "2026-12-01")
    # 1. cover, unchanged from v6
    d.bg(0, leaf_texture(740), name="Background: green fade with leaf texture")
    im = lineart("seedling-fungi", 480)
    hh = height(SLIDES[0][1], 86, 900)
    y = round((H - 150 - (im.height + 70 + hh)) / 2) + 40
    d.put(0, "Drawing: seedling-fungi", im, (W - im.width) // 2, y, shadowed=False, anchor="tl")
    T(d, 0, "Headline", SLIDES[0][1], 90, y + im.height + 70, 900, hh + 8, 86, color=CREAM)
    logo(d, 0)

    def ph(path):
        return ImageOps.exif_transpose(Image.open(path)).convert("RGB")

    slides = [
        ([(f"{NEW}/card-elaine-ingham-microscope.jpg", 0.5, 0.35)], "We carry Dr. Elaine Ingham\u2019s science forward"),
        ([(f"{IND}/2f8d6c80-9a4b-44f2-804c-f02f766f5a90.jpg", 0.5, 0.5),
          (f"{IND}/40c702d3-e6e9-4387-b187-2a1798fef626.jpg", 0.45, 0.45)],
         "61 farmers in India this October. 46 students from 10 countries at our workshop."),
        ([(f"{IND}/17c01e4d-cbfa-4f9c-8058-9e225aa30c5f.jpg", 0.5, 0.5)], "Our goal:\n100,000 acres\nregenerated in 2027"),
        ([(f"{NEW}/community-laughing-at-microscope.jpg", 0.5, 0.4)],
         "Your gift helps a student learn to restore soil. Link in bio"),
    ]
    for k, (photos, text) in enumerate(slides, start=1):
        hs = 64 if len(text) > 55 else 70
        th = height(text, hs, 760)
        BAND = max(340, round(th) + 150)
        bg = Image.new("RGB", (W, H), GREEN)
        d.bg(k, bg.convert("RGBA"), name="Background: Food Web Green")
        top_h = H - BAND
        if len(photos) == 1:
            p_, fx, fy = photos[0]
            d.put(k, "Photo", cover(ph(p_), W, top_h, fx, fy).convert("RGBA"), 0, 0, shadowed=False, anchor="tl")
        else:   # two photos side by side, a thin green gap between them
            hw = (W - 8) // 2
            for i, (p_, fx, fy) in enumerate(photos):
                d.put(k, f"Photo {i + 1}", cover(ph(p_), hw, top_h, fx, fy).convert("RGBA"), i * (hw + 8), 0,
                      shadowed=False, anchor="tl")
        T(d, k, "Headline", text, 72, top_h + (BAND - round(th)) // 2 - 6, 760, th + 8, hs, color=CREAM, align="left",
          lh=1.08)
        logo(d, k)
    return d


def build_story(v):
    """v11 (Linnea, 10 Nov: "put the stuff from the Givebutter text into a nice carousel, think like a non profit").
    Every line is from the campaign page https://givebutter.com/sfwf-donate. Photo slides with a green band carry the
    people; big-type slides on the leaf texture carry the argument; it ends on the goal and the gold donate button
    (gold only on donate CTAs)."""
    from PIL import ImageDraw, ImageOps
    from collage import cover
    from bundle_three_styles import rgb
    GOLD = "#C9A227"
    d = Deck("x20261201", 7, f"giving-tuesday-{v}", "2026-12-01")

    def ph(path):
        return ImageOps.exif_transpose(Image.open(path)).convert("RGB")

    def photo_slide(k, path, fx, fy, text, small=None):
        """Full-bleed photo, soft dark fade at the bottom, cream text straight on the photo (Linnea, 10 Nov: no green
        boxes)."""
        from nov_updates_nov10 import scrim
        d.bg(k, scrim(cover(ph(path), W, H, fx, fy), 0.42, 0.88).convert("RGBA"), name="Photo")
        th = height(text, 70, 820, lh=1.08)
        sh = height(small, 50, 820, bold=False, lh=1.2) if small else 0
        y = H - 110 - round(th) - (round(sh) + 24 if small else 0)
        y = T(d, k, "Headline", text, 72, y, 820, th + 8, 70, color=CREAM, align="left", lh=1.08)
        if small:
            T(d, k, "Details", small, 72, round(y) + 24, 820, sh + 8, 50, bold=False, color=MINT, align="left", lh=1.2)
        logo(d, k)

    def type_slide(k, head, line=None, art=None, seed=750, hs=73):
        d.bg(k, leaf_texture(seed + k), name="Background: green fade with leaf texture")
        im = lineart(art, 340) if art else None
        hh = height(head, hs, 880, lh=1.1)
        lh = height(line, 54, 860, bold=False, lh=1.22) if line else 0
        total = (im.height + 60 if im else 0) + hh + (36 + lh if line else 0)
        y = round((H - 120 - total) / 2) + 20
        if im:
            d.put(k, f"Drawing: {art}", im, (W - im.width) // 2, y, shadowed=False, anchor="tl")
            y += im.height + 60
        T(d, k, "Headline", head, 100, y, 880, hh + 8, hs, color=CREAM, lh=1.1)
        if line:
            T(d, k, "Details", line, 110, y + round(hh) + 36, 860, lh + 8, 54, bold=False, color=MINT, lh=1.22)
        logo(d, k)

    # v17 (Linnea, 10 Nov: "you can change the text too"): a real photo on every slide, tighter lines from the
    # Givebutter campaign (https://givebutter.com/sfwf-donate), one idea per slide
    G = "/home/user/sfwlib/social/giving"
    # v21 (Linnea, 10 Nov): the mission copy (tagline + SOP-SFWF-001 core idea + Givebutter funding line)
    G = "/home/user/sfwlib/social/giving"
    # cover: a fundraising cover names the day, the goal and the ask (gold = donate)
    from nov_updates_nov10 import scrim
    d.bg(0, leaf_texture(760), name="Background: green fade with leaf texture")
    T(d, 0, "Eyebrow", "GivingTuesday \u00b7 December 1", 72, 420, 900, 70, 54, bold=False, color=MINT, align="left")
    T(d, 0, "Headline", "Healing soil.\nFeeding humanity.\nRestoring the\nliving world.", 72, 510, 900, 330, 74,
      color=CREAM, align="left", lh=1.06)
    T(d, 0, "Details", "Help us raise $100,000", 72, 880, 900, 70, 54, bold=False, color=CREAM, align="left")
    pw0 = 680
    pill0 = Image.new("RGBA", (pw0 * 4, 100 * 4), (0, 0, 0, 0))
    ImageDraw.Draw(pill0).rounded_rectangle((0, 0, pw0 * 4 - 1, 100 * 4 - 1), 200, fill=rgb(GOLD) + (255,))
    d.put(0, "Give button (gold)", pill0.resize((pw0, 100), Image.LANCZOS), 74, 990, shadowed=False, anchor="tl")
    T(d, 0, "Give", "Give today \u00b7 Link in bio", 74, 1004, pw0, 70, 50, color="#4F3433")
    logo(d, 0)
    photo_slide(1, "/home/user/SFW-SocialMedia/assets/photo/web/fist-of-dry-soil.jpg", 0.5, 0.45,
                "The soil under our feet is alive. For decades we\u2019ve farmed it like it was dead.")
    photo_slide(2, f"{NEW}/card-elaine-ingham-microscope.jpg", 0.5, 0.35,
                "Healthy food comes from healthy soil")
    photo_slide(3, f"{G}/class-live-microscopy-cr-oct2025.jpg", 0.55, 0.45,
                "We teach farmers, agronomists and consultants to restore the living web in their soil")
    photo_slide(4, f"{NEW}/students-laughing-at-compost-cage.jpg", 0.6, 0.4,
                "One trained farmer changes a whole farm. Then the neighbours ask how.")
    photo_slide(5, f"{IND}/17c01e4d-cbfa-4f9c-8058-9e225aa30c5f.jpg", 0.5, 0.5,
                "Farm by farm, in Costa Rica, New Mexico, England, Cyprus and India")
    # 7. close on the land: the team line, the funding line and the gold donate button
    from nov_updates_nov10 import scrim
    d.bg(6, scrim(cover(ph(f"{G}/wkh-farm-track-jun2025.jpg"), W, H, 0.45, 0.35), 0.35, 0.9).convert("RGBA"),
         name="Photo: class walking a farm track, Wild Ken Hill, Jun 2025")
    T(d, 6, "Headline", "Be the mycelium\nyou want to see\nin the world", 72, 700, 820, 240, 70, color=CREAM,
      align="left", lh=1.06)
    T(d, 6, "Details", "We\u2019re raising $100,000 for scholarships,\neducational resources and research", 72, 960,
      880, 140, 50, bold=False, color=MINT, align="left", lh=1.2)
    pw = 620
    pill = Image.new("RGBA", (pw * 4, 100 * 4), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, pw * 4 - 1, 100 * 4 - 1), 200, fill=rgb(GOLD) + (255,))
    d.put(6, "Donate button (gold)", pill.resize((pw, 100), Image.LANCZOS), 74, H - 170, shadowed=False, anchor="tl")
    T(d, 6, "Donate", "Donate \u00b7 Link in bio", 74, H - 156, pw, 70, 52, color="#4F3433")
    logo(d, 6)
    return d


if __name__ == "__main__":
    from PIL import Image  # noqa: F401
    fn = build_story if sys.argv[1] >= "v11" or len(sys.argv[1]) > 3 else build
    print(fn(sys.argv[1]).save(TILES, DECKS)[0])
