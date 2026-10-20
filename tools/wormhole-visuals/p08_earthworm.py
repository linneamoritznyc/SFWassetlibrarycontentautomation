"""p08 World Earthworm Day, 21 October: one soil profile across seven slides.

A deep worm burrow runs down through the scene, lined with microbes, with rain
soaking in, and ends under undug, mulched ground. Slide text is the doc's own.

  python3 tools/wormhole-visuals/p08_earthworm.py
"""
import math
import random

from collage import DEEP, H, W, draw_layer, flower, gradient, hexrgb, hyphae, lens, rain, roots, soil
from posts import MICRO, N, build, head, post

GROUND = 600  # soil surface, px from the top


def burrow(w, h, seed, x0):
    """A drawn vertical earthworm burrow: dark channel with a paler lining of casts."""
    rnd = random.Random(seed)

    def fn(d, s):
        pts, x = [], x0
        for y in range(0, h, 8):
            x += rnd.uniform(-3, 3) + 7 * math.sin(y / 80 + seed)
            pts.append((x * s, y * s))
        d.line(pts, fill=hexrgb("#C9A57A") + (255,), width=round(48 * s), joint="curve")
        d.line(pts, fill=hexrgb("#1E1510") + (255,), width=round(30 * s), joint="curve")

    return draw_layer(w, h, fn)


@post("p08", "2026-10-21", "world-earthworm-day", 7)
def p08(d):
    n = 7
    d.bg(None, gradient(W * n, H, [(0, "#F4F1EA"), (GROUND / H - 0.02, "#EFE8D8"), (GROUND / H + 0.01, "#5A4231"),
                                   (1, "#2E2219")], 81))
    # surface flowers from Norfolk, where the Earthworm Society of Britain works
    kit = [("norfolk-common-poppy", 230, 860), ("norfolk-cornflower", 190, 1960), ("norfolk-foxglove", 230, 2980),
           ("norfolk-sea-lavender", 200, 4060), ("norfolk-common-poppy", 210, 5060)]
    for i, (nm, h, x) in enumerate(kit):
        d.put(0, f"flower-{nm}-{i + 1}", flower(nm, h=h), x, GROUND - h // 2 + 30, rot=(-4, 5, -3, 4, -5)[i])
    d.put(0, "roots", roots(W * n, 700, 8, color="#D8C6A6", n=24, width=2.4), W * n // 2, GROUND + 350, shadowed=False)
    # the burrow, running from slide 2 down through slide 4
    # one vertical burrow on each of slides 2 to 4
    for k, (seed, x0) in zip((1, 2, 3), ((5, 330), (6, 520), (7, 420))):
        d.put(k, "worm-burrow", burrow(W, H - GROUND, seed, x0), W // 2, GROUND + (H - GROUND) // 2, shadowed=False)
    d.put(1, "earthworm-in-burrow", soil("earthworm", h=300), 360, 960, rot=4)
    # slide 3: microbes on the burrow walls
    d.put(2, "microbe-threads", hyphae(420, 640, 9, color="#F4F1EA", n=9, width=1.6, start=(210, 60)), 520, 960, shadowed=False)
    d.put(2, "micrograph-ciliate", lens(N("Ciliate, 60x obj, Patricia J Coppola.jpg"), 330), 850, 1060)
    # slide 4: rain soaking straight down the channel
    d.put(3, "rain", rain(W, 280, 4, color="#5F8BA3", n=160), W // 2, GROUND - 150, shadowed=False)
    d.put(3, "water-in-soil", rain(90, 640, 5, color="#9CC8DC", n=70), 420, GROUND + 330, shadowed=False)
    d.put(4, "earthworm-curled", soil("earthworm", h=280, flip=True), 540, 980, rot=30)
    d.put(4, "fern-fiddlehead", soil("fern-fiddlehead", w=220), 760, GROUND - 60)
    # slides 6 and 7: no-dig ground, mulched and fed
    d.put(5, "dry-leaves", soil("dry-leaves-twigs", w=330), 300, GROUND - 40)
    d.put(5, "wood-chips", soil("wood-chips-pile", w=330), 780, GROUND - 30)
    d.put(5, "earthworm-safe", soil("earthworm", h=260), 560, 1050, rot=-20)
    d.put(6, "compost", soil("compost-white-fungal-threads", w=360), 300, GROUND - 40)
    d.put(6, "moss", soil("moss-clump", w=300), 760, GROUND - 40)
    d.put(6, "mushrooms", soil("mushrooms", w=240), 860, 1120)
    texts = [
        "How do worms work their magic?",
        "Anecic earthworms dig vertical burrows that can reach 1 to 2 meters deep to break up compaction.",
        "They spread microbes around as they move by lining the walls with mucus and casts, rich in nutrients and microbes.",
        "Their channels let rain soak in fast without causing the ground to go anaerobic.",
        "How to care for them?",
        "Digging cuts the burrows. No-dig keeps the plumbing intact.",
        "Add organic matter (or simply don't remove it).",
    ]
    for k, t in enumerate(texts):
        big = k in (0, 4)
        head(d, k, t, DEEP, y=80, x=72, w=880, size=104 if big else 66, h=300)
    d.logo(0, "br")
    d.logo(6, "br")


if __name__ == "__main__":
    build("p08")
    print("p08 built")
