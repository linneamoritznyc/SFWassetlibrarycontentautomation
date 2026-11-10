"""Small Business Saturday (28 Nov), Colleen Dempster: Allison Duck's final text (10 Nov), 3 slides, on the same
cream page, frame and logo as the earlier versions. Montserrat Bold + Source Sans 3, Soil Brown text, green accent.

  python3 tools/wormhole-visuals/smallbiz_allison.py <version>
"""
import sys

from PIL import Image, ImageFilter, ImageOps

from bundle_three_styles import grain, rgb
from bundle_three_styles_v12 import T, height
from bundle_v6 import H, W
from collage import Deck, cover
from nov_fill import DECKS, TILES
from nov_updates_nov10 import BROWN, CREAM, GREEN, RW_PHOTO, eyepiece, logo, rect

LAB = "/home/user/sfwlib/social/rewild/lab"
M, TW = 110, 860


def page(d, k):
    d.bg(k, grain(Image.new("RGB", (W, H), CREAM), 650 + k, 4), name="Background: Organic Cream")
    rect(d, k, "Page frame", 44, 44, W - 88, H - 88, (0, 0, 0, 0), outline=rgb(BROWN) + (255,), width=2)


def sfw(d, k):
    logo(d, k, white=False, w=130, x=W - 80 - 30 - 130, y=H - 80 - 130)


def build(v):
    d = Deck("x20261128", 3, f"small-business-saturday-rewild-soils-{v}", "2026-11-28")
    # 1. the photo, then Allison's opening line
    page(d, 0)
    ph = ImageOps.exif_transpose(Image.open(RW_PHOTO)).convert("RGB")
    d.put(0, "Photo: Compost Toronto microscope event", cover(ph, W - 160, 640, 0.45, 0.45).convert("RGBA"), 80, 80,
          shadowed=False, anchor="tl")
    t1 = ("On Small Business Saturday, we salute our Soil Food Web Consultants and Lab-Techs, like Colleen Dempster, "
          "a Lab-Tech since 2022 who is completing her Consultant certification.")
    T(d, 0, "Text", t1, M, 780, TW, 380, 54, bold=False, color=BROWN, align="left", lh=1.2)
    sfw(d, 0)
    # 2. her work and her words, over the faded micrograph from her lab (Linnea liked this background)
    page(d, 1)
    bgm = ImageOps.exif_transpose(Image.open(f"{LAB}/15eb67838c2640729439e8cbae5eb89d.jpg")).convert("RGB")
    bgm = cover(bgm, W - 160, H - 160, 0.3, 0.5).filter(ImageFilter.GaussianBlur(7))
    bgm = Image.blend(bgm, Image.new("RGB", bgm.size, (244, 241, 234)), 0.62)
    d.put(1, "Micrograph from Colleen's lab (faded)", bgm.convert("RGBA"), 80, 80, shadowed=False, anchor="tl")
    t2 = ("In addition to working as a Lab-Tech at her business, Rewild Soils, in Uxbridge, Ontario, Colleen also offers "
          "lectures and demonstrations.")
    q2 = ("Making compost and exploring samples under the microscope will always be something I enjoy. A big part of my "
          "work is educating people about soil health in the context of soil biology. Most people have never seen the "
          "microbes that make up the soil food web, so I show pictures and do live microscope demonstrations.")
    h2 = height(t2, 50, TW, bold=True, lh=1.14)
    hq = height(q2, 48, TW, bold=False, lh=1.22)
    y0 = round(80 + (H - 160 - 130 - (h2 + 150 + hq)) / 2)   # centre the block above the logo row
    y = T(d, 1, "Intro", t2, M, y0, TW, h2 + 10, 50, color=BROWN, align="left", lh=1.14)
    T(d, 1, "Quote mark", "“", M - 6, round(y) + 10, 200, 160, 200, color=GREEN, align="left")
    T(d, 1, "Quote", q2, M, round(y) + 150, TW, hq + 10, 48, bold=False, color=BROWN, align="left", lh=1.22, mn=48)
    sfw(d, 1)
    # 3. find a Lab-Tech or Consultant near you, with a micrograph from her lab
    page(d, 2)
    D = 440
    d.put(2, "Micrograph from Colleen's lab: nematode in compost, 400x",
          eyepiece(f"{LAB}/7a556d32bd164c89a18e7d39ed602b7b.jpg", D, 0.42, 0.5, 1.0), (W - D) // 2, 100,
          shadowed=False, anchor="tl")
    t3 = ("When you need a soil or compost sample analyzed or need help in transitioning your farm or garden to the "
          "Soil Food Web Approach, find certified Lab-Techs and Consultants nearest you on our website:")
    T(d, 2, "Text", t3, M, 600, TW, 400, 50, bold=False, color=BROWN, align="left", lh=1.2)
    T(d, 2, "Website", "soilfoodweb.com/\nfind-a-professional", M, 1000, TW, 130, 50, color=GREEN, align="left", lh=1.1)
    sfw(d, 2)
    return d


if __name__ == "__main__":
    print(build(sys.argv[1]).save(TILES, DECKS)[0])
