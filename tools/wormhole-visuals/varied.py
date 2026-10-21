"""Posts that each get their own look, chosen for their topic.

The earthworm-cover style belongs to World Earthworm Day only. Everything here
uses the shared kit (paper, real cutouts, one shadow, Garamond or Montserrat,
the logo) but a different idea per post.

  python3 tools/wormhole-visuals/varied.py [ids...]
"""
import sys

from PIL import Image

from collage import (CREAM, DEEP, GREEN, H, KRAFT, W, cutout, flower, gradient, hyphae, lens, logo_disc, paper, phone,
                     print_photo, rain, round_photo, soil)
from posts import N, OH, build, head, post, small

SITEIMG = "/home/user/linneamoritznyc/final-sfwsite-linnea/img"
CLOVER = f"{OH}/crimson-clover-capri.webp"
NIGHT = "#141A14"


def garamond(d, k, text, color, y=130, size=96, w=880, h=420, x=80):
    return d.text(k, "headline", text, x, y, w, h, size, color=color, shade=color == CREAM)


def note(d, k, text, color, y, size=40, w=860, x=84):
    return d.text(k, "small line", text, x, round(y), w, 260, size, italic=False, color=color, lh=1.25,
                  shade=color == CREAM)


# ---------------------------------------------------------------- Casey: the Turn One family
@post("p02", "2026-10-21", "meet-casey-williams", 3)
def casey(d):
    d.bg(0, paper(DEEP, 201))
    d.bg(1, paper(CREAM, 202))
    d.bg(2, paper(KRAFT, 203))
    note(d, 0, "Meet our mentors", CREAM, 120, size=40)
    garamond(d, 0, "Casey Williams", CREAM, y=180, size=128, w=600)
    d.put(0, "portrait", round_photo(N("team-casey-williams.jpg"), 470, ring=14, fy=0.3), 650, 830)
    d.put(0, "flower-paintbrush", flower("santa-fe-indian-paintbrush", h=380), 170, 1080, rot=-8)
    d.put(0, "flower-chamisa", flower("santa-fe-chamisa", w=330), 930, 1170, rot=6)
    d.logo(0, "tr")
    bottom = garamond(d, 1, "“I am deeply grateful that I get to learn from my students as well as teach them.”",
                      GREEN, y=140, size=74, h=520)
    d.put(1, "micrograph-nematode", lens(N("Bacterial-feeding nematode, 40x obj, Casey Williams.jpg"), 420), 660, 1010)
    note(d, 1, "A bacterial-feeding nematode at 40x, photographed by Casey.", DEEP, 1240, size=30, w=480)
    d.put(1, "flower-cornflower", flower("norfolk-cornflower", h=300), 150, 1060, rot=-6)
    garamond(d, 2, "His advice: put your hands in the soil. We learn best by doing.", DEEP, y=150, size=88)
    note(d, 2, "Thank you, Casey!", DEEP, 600, size=48)
    d.put(2, "earthworm", soil("earthworm", h=300), 240, 1120, rot=-20)
    d.put(2, "acorns", soil("acorns", w=240), 520, 1220)
    d.put(2, "flower-globemallow", flower("santa-fe-globemallow", h=420), 900, 1060, rot=6)
    d.logo(2, "tr")


# ---------------------------------------------------------------- Nick: a farm photo story on kraft
@post("p03", "2026-10-22", "meet-nick-padwick", 3)
def nick(d):
    for k in range(3):
        d.bg(k, paper(KRAFT, 300 + k))
    note(d, 0, "Meet our mentors", DEEP, 110, size=40)
    garamond(d, 0, "Nick Padwick", DEEP, y=160, size=120, w=900)
    note(d, 0, "Norfolk, England", DEEP, 320, size=40)
    d.put(0, "portrait-print", print_photo(f"{SITEIMG}/nick.png", 560, 640, fy=0.2), 560, 860, rot=-2)
    d.put(0, "flower-poppy", flower("norfolk-common-poppy", h=420), 170, 1060, rot=-8)
    d.put(0, "flower-cornflower", flower("norfolk-cornflower", h=360), 930, 1110, rot=6)
    garamond(d, 1, "More than 40 years farming at scale, in the UK, Italy, Spain and Argentina.", DEEP, y=150, size=84)
    d.put(1, "flower-sea-lavender", flower("norfolk-sea-lavender", h=420), 200, 1050, rot=-6)
    d.put(1, "wood-chips", soil("wood-chips-pile", w=360), 560, 1170)
    d.put(1, "flower-poppy", flower("norfolk-common-poppy", h=400), 900, 1060, rot=8)
    garamond(d, 2, "Today he makes around 750 tons of compost a year.", DEEP, y=140, size=92)
    note(d, 2, "Thank you, Nick, for showing our students what this looks like at scale.", DEEP, 520, size=40, w=800)
    for i, (x, w) in enumerate([(230, 330), (560, 380), (880, 330)]):
        d.put(2, f"compost-{i + 1}", soil("compost-white-fungal-threads" if i != 1 else "dark-soil-clump", w=w), x, 1120)
    d.put(2, "flower-foxglove", flower("norfolk-foxglove", h=380), 990, 640, rot=6)
    d.logo(2, "tl")


# ---------------------------------------------------------------- Wes: through the eyepiece, at night
@post("p04", "2026-10-23", "meet-wes-sander", 3)
def wes(d):
    for k in range(3):
        d.bg(k, gradient(W, H, [(0, "#0F1510"), (0.6, "#16211A"), (1, "#0F1510")], 400 + k), name=f"background-{k}")
    d.put(0, "portrait", round_photo(f"{SITEIMG}/wes.png", 520, ring=16, fy=0.3, ring_color="#E9E2CF"), W // 2, 760)
    note(d, 0, "Meet our mentors", CREAM, 120, size=40)
    garamond(d, 0, "Wes Sander", CREAM, y=170, size=120)
    note(d, 0, "Microscopy mentor", CREAM, 1110, size=44, w=W - 160)
    d.put(1, "micrograph-arcella", lens(N("Testate amoeba (Arcella), 40x obj, Mark Horton.jpg"), 760), W // 2, 760)
    garamond(d, 1, "His favourite organism: the Arcella amoeba.", CREAM, y=110, size=80)
    note(d, 1, "“There's just something about that large test that you can almost see inside of, with the amoeba "
         "squished up against the wall. So cool.”", CREAM, 1150, size=30)
    note(d, 1, "Arcella at 40x, photographed by student Mark Horton.", CREAM, 1280, size=24)
    garamond(d, 2, "“It depends,” as Dr. Elaine loved to say.", CREAM, y=200, size=100)
    note(d, 2, "Wes's advice: success hinges on reading the signs. Thank you, Wes!", CREAM, 640, size=42, w=820)
    for i, (f, x, y, w, r) in enumerate([("cutout-6", 220, 1050, 330, 20), ("cutout-2", 560, 1150, 260, -10),
                                         ("cutout-7", 880, 1020, 300, 40)]):
        d.put(2, f"organism-{i + 1}", cutout(f"/home/user/SFW-SocialMedia/assets/microscopy/{f}.png", w=w), x, y, rot=r)
    for k in (0, 2):
        d.logo(k, "tr")


# ---------------------------------------------------------------- Gerald: Costa Rica, painted sun
@post("p06", "2026-10-24", "meet-gerald-ramirez", 3)
def gerald(d):
    sun = [(0, "#F2A65A"), (0.5, "#F7CB7E"), (1, "#FBE7B5")]
    for k in range(3):
        d.bg(k, gradient(W, H, sun, 600 + k), name=f"background-{k}")
    note(d, 0, "Meet our mentors", DEEP, 120, size=40)
    garamond(d, 0, "Gerald Ramirez", DEEP, y=170, size=120, w=640)
    d.put(0, "portrait", round_photo(f"{SITEIMG}/Gerald.jpg", 500, ring=14, fy=0.25), 620, 820)
    d.put(0, "flower-heliconia", flower("costa-rica-heliconia", h=560), 130, 1060, rot=6)
    d.put(0, "flower-hibiscus", flower("costa-rica-hibiscus", w=300), 900, 1180, rot=-8)
    d.put(1, "photo-liquid-amendments", print_photo(N("card-liquid-amendments-demonstration.jpg"), 860, 640), W // 2, 560)
    garamond(d, 1, "Gerald teaches students to make compost extracts and teas.", DEEP, y=930, size=72, h=300)
    note(d, 1, "Costa Rica, March 2025", DEEP, 1210, size=34)
    garamond(d, 2, "They carry living biology from the compost out onto the fields.", DEEP, y=150, size=88)
    note(d, 2, "Thank you, Gerald!", DEEP, 620, size=50)
    d.put(2, "flower-torch-ginger", flower("costa-rica-torch-ginger", h=460), 200, 1060, rot=-10)
    d.put(2, "flower-poro", flower("costa-rica-poro-flower", w=320), 560, 1180)
    d.put(2, "flower-hibiscus-2", flower("costa-rica-hibiscus", w=300), 880, 1110, rot=8)
    d.logo(2, "tr")


# ---------------------------------------------------------------- Dora: a lab notebook page
@post("p09", "2026-10-25", "meet-dora-tkalec", 3)
def dora(d):
    for k in range(3):
        d.bg(k, paper("#FBF8F1", 900 + k, grain=8))
    # ruled notebook lines and a margin, drawn
    from collage import draw_layer
    def ruled(dr, s):
        for y in range(240, H, 64):
            dr.line((0, y * s, W * s, y * s), fill=(150, 180, 205, 90), width=max(1, round(1.5 * s)))
        dr.line((120 * s, 0, 120 * s, H * s), fill=(214, 120, 120, 120), width=max(1, round(2 * s)))
    lines = draw_layer(W, H, ruled)
    for k in range(3):
        d.put(k, "notebook-lines", lines, W // 2, H // 2, shadowed=False)
    note(d, 0, "Meet our mentors", GREEN, 120, size=40, x=160)
    garamond(d, 0, "Dora Tkalec", DEEP, y=170, size=120, x=156)
    d.put(0, "portrait-print", print_photo(N("team-dora-tkalec.jpg"), 520, 600, fy=0.3), 600, 820, rot=2)
    d.put(0, "flower-poppy", flower("norfolk-common-poppy", h=360), 960, 1140, rot=8)
    garamond(d, 1, "Her favourite microbe: the naked amoeba.", DEEP, y=150, size=84, x=156, w=820)
    d.put(1, "micrograph-naked-amoeba", lens(N("Naked amoeba, 40x obj, Jimena Fuentes.jpg"), 520), 640, 860)
    note(d, 1, "“A slimy splotch that changes shape, and every species keeps its own.”", GREEN, 1170, size=36,
         x=160, w=820)
    garamond(d, 2, "“I have seen plants treated with BioComplete™ compost extract being more resistant to "
             "bacterial disease.”", DEEP, y=150, size=72, x=156, w=820)
    note(d, 2, "Thank you, Dora!", GREEN, 660, size=50, x=160)
    d.put(2, "compost", soil("compost-white-fungal-threads", w=340), 360, 1050)
    d.put(2, "flower-marigold", flower("tamil-nadu-marigold", h=340), 820, 1060, rot=-6)
    d.logo(2, "br")


if __name__ == "__main__":
    for pid in sys.argv[1:] or ["p02", "p03", "p04", "p06", "p09"]:
        build(pid)
        print(pid, "built")
