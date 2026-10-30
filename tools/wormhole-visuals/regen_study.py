"""New study: regenerative farms store 39% more soil carbon (Lundgren et al. 2026). 8-slide editable carousel.

Real cutouts from the SFW library (soil, fungi, worm, beetle, flowers), brand fonts, one flat colour per slide.
  python3 tools/wormhole-visuals/regen_study.py  -> decks/regenerative-farms-39-percent-carbon.pptx + tiles
"""
from jan_varied import BLUE, BROWN, CREAM, DEEP, FWG, INK, LG_T, LGREEN, SAGE, TAN_T, body, eyebrow, head, logo
from novdec import build, globe, post

SOIL = "/home/user/sfwlib/social/cutouts-soil"
FL = "/home/user/sfwlib/social/cutouts-flowers"


@post("regen39", "2026-11-18", "regenerative-farms-39-percent-carbon", 8, CREAM)
def regen(p):
    bgs = [CREAM, DEEP, LG_T, DEEP, CREAM, TAN_T, BROWN, SAGE]
    for k, c in enumerate(bgs):
        p.d.bg(k, __import__("collage").paper(c, 40 + k, w=1080, h=1350, grain=5), name=f"background-{k + 1}")
    # 1
    eyebrow(p, 0, "NEW STUDY", CREAM)
    head(p, 0, "The most regenerative farms stored 39% more carbon in their soil.", CREAM, size=70)
    p.cut(0, f"{SOIL}/compost-white-fungal-threads.png", 60, 640, w=620)
    p.cut(0, f"{SOIL}/moss-clump.png", 640, 760, w=360)
    p.cut(0, f"{SOIL}/earthworm.png", 420, 1040, w=280)
    # 2
    eyebrow(p, 1, "THE 1000 FARMS INITIATIVE", DEEP)
    head(p, 1, "Working farms across North America, from the most conventional to the most regenerative.", DEEP,
         size=58)
    body(p, 1, "Led by Ecdysis Foundation.", DEEP, 560, size=40)
    p.put(1, "globe", globe(560, lon0=-98, lat0=40), 260, 680)
    # 3
    eyebrow(p, 2, "SOIL CARBON", LG_T)
    p.d.text(2, "number", "39%", 90, 160, 900, 360, 330, kind="montserrat-bold", italic=False, color=FWG, lh=1.0)
    body(p, 2, "more total soil carbon on the most regenerative farms.", LG_T, 520, size=52, w=880, color=BROWN)
    p.cut(2, f"{SOIL}/dark-soil-clump.png", 320, 780, w=560)
    # 4
    eyebrow(p, 3, "SOIL FUNGI", DEEP)
    p.d.text(3, "number", "77%", 90, 160, 900, 360, 330, kind="montserrat-bold", italic=False, color=CREAM, lh=1.0)
    body(p, 3, "more total fungi in regenerative soils.", DEEP, 520, size=52, w=880, color=CREAM)
    p.cut(3, f"{SOIL}/mushrooms.png", 360, 760, h=520)
    # 5
    eyebrow(p, 4, "MORE LIFE EVERYWHERE", CREAM)
    head(p, 4, "Soil microbes, insects, plants and birds.", CREAM, size=70)
    body(p, 4, "The more biodiversity, the more carbon stored.", CREAM, 400, size=44)
    p.cut(4, f"{FL}/norfolk-common-poppy.png", 70, 600, h=600)
    p.cut(4, f"{FL}/norfolk-cornflower.png", 330, 640, h=560)
    p.cut(4, f"{FL}/santa-fe-globemallow.png", 560, 620, h=580)
    p.cut(4, f"{SOIL}/ground-beetle.png", 560, 1090, w=190)
    # 6
    eyebrow(p, 5, "YIELD AND PROFIT", TAN_T)
    head(p, 5, "Regenerative yields matched national averages.", TAN_T, size=72)
    body(p, 5, "Net profit per acre was similar.", TAN_T, 470, size=48, color=FWG)
    p.cut(5, f"{SOIL}/cracked-corn-pile.png", 200, 720, w=680)
    # 7
    eyebrow(p, 6, "THE WHOLE SYSTEM MATTERS", BROWN)
    head(p, 6, "One practice alone changed nothing.", BROWN, y=320, size=96)
    body(p, 6, "Farms using a single regenerative practice looked like conventional farms.", BROWN, 720, size=48,
         w=860)
    # 8
    eyebrow(p, 7, "READ THE PAPER", SAGE)
    head(p, 7, "Lundgren et al., Environmental Research: Food Systems, 2026.", SAGE, size=66)
    body(p, 7, "Link in bio.", SAGE, 560, size=52, color=FWG)
    body(p, 7, "doi.org/10.1088/2976-601X/ae8f4e", SAGE, 650, size=36, color=INK)
    p.cut(7, f"{SOIL}/fern-fiddlehead.png", 480, 830, h=400)
    for k, c in enumerate(bgs):
        logo(p, k, c)


if __name__ == "__main__":
    print(build("regen39"))
