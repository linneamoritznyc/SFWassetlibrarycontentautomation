"""Meet our mentors (p02, p03, p04, p06, p09) in the earthworm-cover style.

Each mentor gets their own sky colour and the flowers of their region, the
same compost cross-section underneath, their own portrait as a round print, and
a slide on the organism or work they love.

  python3 tools/wormhole-visuals/mentors.py [ids...]
"""
import random
import sys

from collage import GREEN, H, W, cutout, flower, gradient, lens, round_photo, soil
from p08_earthworm import DEEP, SOIL_TOP, burrow, logo_full, soil_band
from posts import BUILDERS, N, OH, build, post

SITEIMG = "/home/user/linneamoritznyc/final-sfwsite-linnea/img"
CLOVER = f"{OH}/crimson-clover-capri.webp"


def scene(d, n, sky, plants, seed):
    _BOTTOM.clear()
    """Sky, a soil cross-section across all n slides, a row of plants and a few burrows."""
    d.bg(None, gradient(W * n, H, sky, seed))
    band = soil_band(seed)
    if band.width < W * n:  # soil_band is cut for seven slides; mentors use fewer
        pass
    d.put(0, "soil-cross-section", band.crop((0, 0, W * n, band.height)), W * n // 2,
          SOIL_TOP - 40 + band.height // 2, shadowed=False)
    rnd = random.Random(seed)
    x = 110
    i = 0
    while x < W * n - 80:
        kind, h = plants[i % len(plants)]
        im = cutout(CLOVER, h=h) if kind == "clover" else flower(kind, h=h)
        d.put(0, f"plant-{i + 1}", im, x, SOIL_TOP - im.height // 2 + 22, off=(6, 8), blur=8, alpha=0.3)
        x += rnd.randint(200, 300)
        i += 1
    for k in range(n):
        for j, bx in enumerate(rnd.sample([200, 380, 560, 760, 900], 2)):
            b = burrow(H - SOIL_TOP - 40 - j * 140, 100 * seed + 10 * k + j)
            d.put(k, f"burrow-{j + 1}", b, bx, SOIL_TOP + 10 + b.height // 2, shadowed=False)
        d.put(k, "logo", logo_full(), W - 170, 120, shadowed=False)


def headline(d, k, text, size=88, y=170, w=700):
    _BOTTOM[k] = d.text(k, "headline", text, 92, y, w, 420, size, kind="montserrat-bold", italic=False, color=DEEP, lh=1.08)


_BOTTOM = {}


def line(d, k, text, y=None, w=700, size=40):
    if y is None or _BOTTOM.get(k, 0) + 24 > y:
        y = _BOTTOM.get(k, 150) + 24
    return d.text(k, "small line", text, 94, round(y), w, 200, size, kind="source", italic=False, color=GREEN, lh=1.2)


def cover(d, name, portrait, fy=0.35):
    _BOTTOM.clear()
    d.text(0, "small line", "Meet our mentors", 94, 150, 600, 60, 44, kind="source", italic=False, color=GREEN)
    headline(d, 0, name, size=104, y=210, w=520)
    d.put(0, "portrait", round_photo(portrait, 360, ring=14, fy=fy), 830, 600)


def thanks(d, k, first, worm_x=560):
    headline(d, k, f"Thank you, {first}!", size=104, w=640)
    line(d, k, "Leave a thank-you in the comments.", 420)
    d.put(k, "earthworm", soil("earthworm", h=280), worm_x, 1110, rot=20)


PEACH = [(0, "#F7C98F"), (0.35, "#FBE0B6"), (0.6, "#FCEBCB"), (1, "#F6DDB5")]
SAGE = [(0, "#BFD7B5"), (0.35, "#D9E8CF"), (0.6, "#ECF2E3"), (1, "#E3EAD6")]
SKY = [(0, "#A9CBE0"), (0.35, "#CFE2EE"), (0.6, "#E7F0F5"), (1, "#DCE7EC")]
SUN = [(0, "#F6D77E"), (0.35, "#FAE6AE"), (0.6, "#FCF1D2"), (1, "#F3E4BE")]
CORAL = [(0, "#F4B8A0"), (0.35, "#F8D3C2"), (0.6, "#FBE6DC"), (1, "#F2D9CC")]


@post("p02", "2026-10-21", "meet-casey-williams", 3)
def casey(d):
    scene(d, 3, PEACH, [("clover", 150), ("santa-fe-chamisa", 190), ("clover", 140), ("santa-fe-indian-paintbrush", 210)], 21)
    cover(d, "Casey Williams", N("team-casey-williams.jpg"), fy=0.3)
    headline(d, 1, "Casey learns from his students as much as he teaches them.", size=74)
    d.put(1, "micrograph-nematode", lens(N("Bacterial-feeding nematode, 40x obj, Casey Williams.jpg"), 330), 800, 1060)
    line(d, 1, "A bacterial-feeding nematode at 40x, photographed by Casey.", 500, size=34)
    headline(d, 2, "His advice: put your hands in the soil. We learn best by doing.", size=74)
    d.put(2, "dark-soil", soil("dark-soil-clump", w=280), 800, SOIL_TOP - 60)
    line(d, 2, "Thank you, Casey!", 500, size=48)


@post("p03", "2026-10-22", "meet-nick-padwick", 3)
def nick(d):
    scene(d, 3, SAGE, [("norfolk-common-poppy", 210), ("norfolk-cornflower", 180), ("clover", 140), ("norfolk-foxglove", 230)], 22)
    cover(d, "Nick Padwick", f"{SITEIMG}/nick.png", fy=0.25)
    headline(d, 1, "More than 40 years farming at scale, in the UK, Italy, Spain and Argentina.", size=70)
    d.put(1, "wood-chips", soil("wood-chips-pile", w=300), 780, SOIL_TOP - 50)
    headline(d, 2, "Today he makes around 750 tons of compost a year in Norfolk.", size=74)
    d.put(2, "compost", soil("compost-white-fungal-threads", w=320), 780, SOIL_TOP - 60)
    line(d, 2, "Thank you, Nick, for showing our students what this looks like at scale.", 520, w=640, size=38)


@post("p04", "2026-10-23", "meet-wes-sander", 3)
def wes(d):
    scene(d, 3, SKY, [("clover", 150), ("norfolk-cornflower", 180), ("clover", 140), ("tamil-nadu-marigold", 180)], 23)
    cover(d, "Wes Sander", f"{SITEIMG}/wes.png", fy=0.3)
    line(d, 0, "Microscopy mentor", 480, size=40)
    headline(d, 1, "His favourite organism: the Arcella amoeba.", size=84)
    d.put(1, "micrograph-arcella", lens(N("Testate amoeba (Arcella), 40x obj, Mark Horton.jpg"), 360), 790, 1050)
    line(d, 1, "“You can almost see inside it. So cool.”", 480, size=38)
    headline(d, 2, "“It depends,” as Dr. Elaine loved to say.", size=84)
    line(d, 2, "Wes's advice: success hinges on reading the signs. Thank you, Wes!", 480, w=640, size=38)
    d.put(2, "earthworm", soil("earthworm", h=260), 700, 1110, rot=-25)


@post("p06", "2026-10-24", "meet-gerald-ramirez", 3)
def gerald(d):
    scene(d, 3, SUN, [("costa-rica-hibiscus", 160), ("clover", 140), ("costa-rica-heliconia", 230), ("costa-rica-torch-ginger", 200)], 24)
    cover(d, "Gerald Ramirez", f"{SITEIMG}/Gerald.jpg", fy=0.25)
    headline(d, 1, "Gerald teaches students to make compost extracts and teas.", size=78)
    d.put(1, "photo-liquid-amendments", round_photo(N("card-liquid-amendments-demonstration.jpg"), 360, ring=14), 790, 1050)
    line(d, 1, "Costa Rica, March 2025.", 480, size=38)
    headline(d, 2, "They carry living biology from the compost out onto the fields.", size=78)
    line(d, 2, "Thank you, Gerald!", 520, size=48)


@post("p09", "2026-10-25", "meet-dora-tkalec", 3)
def dora(d):
    scene(d, 3, CORAL, [("clover", 150), ("norfolk-common-poppy", 200), ("clover", 140), ("santa-fe-globemallow", 200)], 25)
    cover(d, "Dora Tkalec", N("team-dora-tkalec.jpg"), fy=0.35)
    headline(d, 1, "Her favourite microbe: the naked amoeba.", size=84)
    d.put(1, "micrograph-naked-amoeba", lens(N("Naked amoeba, 40x obj, Jimena Fuentes.jpg"), 360), 790, 1050)
    line(d, 1, "A slimy splotch that changes shape, and still every species keeps its own.", 480, w=640, size=38)
    headline(d, 2, "She has seen BioComplete™ compost extract help plants resist disease.", size=68)
    line(d, 2, "Thank you, Dora!", 560, size=48)


if __name__ == "__main__":
    ids = sys.argv[1:] or ["p02", "p03", "p04", "p06", "p09"]
    for pid in ids:
        build(pid)
        print(pid, "built")
