"""Suzanne Shea / Farmer Veteran Coalition as an SFW "Field Report" news graphic (Linnea, 10 Nov: like a BBC or Vox
article graphic, as if SFW were its own media company). Masthead strip, big photo, kicker, headline, standfirst,
photo caption. Cream paper, Soil Brown type, Food Web Green accents. No boxes of text on photos.

  python3 tools/wormhole-visuals/suzanne_news.py <version>
"""
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

from bundle_three_styles_v12 import T, height
from collage import Deck, cover
from nov_fill import DECKS, TILES

W, H = 1080, 1350
CREAM, BROWN, GREEN, INK, GREY = "#F4F1EA", "#4F3433", "#156826", "#333130", "#6E6A64"
V = "/home/user/sfwlib/social/veterans"
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"


def paper(seed):
    a = np.full((H, W, 3), (244, 241, 234), np.float32)
    a += np.random.default_rng(seed).normal(0, 2.0, (H, W, 1)).astype(np.float32)
    return Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")


def grade(im):
    im = ImageEnhance.Color(im).enhance(0.85)
    a = np.asarray(im).astype(np.float32) * np.array([1.03, 1.0, 0.96]) + np.array([6, 5, 0])
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


def rule(d, k, x, y, w, h=3, color=BROWN):
    c = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
    d.put(k, "Rule", Image.new("RGBA", (w, h), c + (255,)), x, y, shadowed=False, anchor="tl")


def masthead(d, k, section):
    c = tuple(int(GREEN[i:i + 2], 16) for i in (1, 3, 5))
    d.put(k, "Masthead bar", Image.new("RGBA", (W, 86), c + (255,)), 0, 0, shadowed=False, anchor="tl")
    T(d, k, "Masthead", "SOIL FOOD WEB \u00b7 FIELD REPORT", 60, 16, 760, 58, 42, bold=True, color=CREAM, align="left",
      mn=42)
    T(d, k, "Section", section, 620, 18, 400, 56, 42, bold=False, color=CREAM, align="right", mn=42)


def photo(d, k, path, y, h, fx, fy, credit):
    d.put(k, "Photo", grade(cover(ImageOps.exif_transpose(Image.open(path)).convert("RGB"), W, h, fx, fy))
          .convert("RGBA"), 0, y, shadowed=False, anchor="tl")
    T(d, k, "Photo credit", credit, 60, y + h + 8, 960, 60, 42, bold=False, color=GREY, align="right", mn=42)


def logo(d, k):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((110, round(lg.height * 110 / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 60 - 110, H - 40 - lg.height, shadowed=False, anchor="tl")


def build(v):
    d = Deck("vet20261111", 3, f"veterans-day-{v}", "2026-11-11")
    # 1. lead story
    d.bg(0, paper(901), name="Background: cream paper")
    masthead(d, 0, "PEOPLE")
    photo(d, 0, f"{V}/suzanne-hoop-house.jpg", 86, 660, 0.68, 0.3, "Photo: Suzanne Shea")
    T(d, 0, "Kicker", "FARMER VETERANS", 60, 820, 960, 62, 44, bold=True, color=GREEN, align="left", mn=42)
    rule(d, 0, 60, 880, 120, 4, GREEN)
    y = T(d, 0, "Headline", "Veteran farmers are building living soil", 60, 900, 960, 190, 76, color=BROWN,
          align="left", lh=1.04)
    T(d, 0, "Standfirst", "Consultant Suzanne Shea took the soil food web to the Farmer Veteran Coalition.", 60,
      round(y) + 20, 820, 140, 46, bold=False, color=INK, align="left", lh=1.22, mn=42)
    logo(d, 0)
    # 2. the talk
    d.bg(1, paper(902), name="Background: cream paper")
    masthead(d, 1, "THE TALK")
    T(d, 1, "Kicker", "STAKEHOLDERS CONFERENCE", 60, 130, 960, 62, 44, bold=True, color=GREEN, align="left", mn=42)
    rule(d, 1, 60, 190, 120, 4, GREEN)
    T(d, 1, "Headline", "“Scaling Sustainably”", 60, 210, 960, 100, 76, color=BROWN, align="left")
    photo(d, 1, f"{V}/suzanne-fvc-conference.jpg", 340, 720, 0.45, 0.5, "Farmer Veteran Coalition")
    T(d, 1, "Caption", "Suzanne Shea presented her talk at\nthe Farmer Veteran Coalition\nStakeholders Conference.",
      60, 1140, 820, 190, 44, bold=False, color=INK, align="left", lh=1.22, mn=42)
    logo(d, 1)
    # 3. the photo, big, with a caption
    d.bg(2, paper(903), name="Background: cream paper")
    masthead(d, 2, "PHOTOS")
    photo(d, 2, f"{V}/suzanne-conference-walk.jpg", 86, 900, 0.15, 0.5, "Photo: Suzanne Shea")
    rule(d, 2, 60, 1072, 960, 2, BROWN)
    T(d, 2, "Caption", "Find a Soil Food Web\nconsultant near you", 60, 1095, 820, 150, 60, color=BROWN, align="left")
    logo(d, 2)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
