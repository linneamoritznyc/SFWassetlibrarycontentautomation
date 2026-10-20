"""p08 World Earthworm Day, 21 October, in Linnea's earthworm-cover style.

Warm peach sky, bold Montserrat headline in deep green, a real soil cross-section
from our own compost photos with worm burrows and root threads, crimson clover,
poppy and marigold standing on the soil line. One soil scene runs across all
seven slides. Slide text is the doc's own.

  python3 tools/wormhole-visuals/p08_earthworm.py
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from collage import GREEN, H, W, cover, cutout, draw_layer, flower, gradient, hexrgb, lens, rain, soil
from posts import MICRO, N, OH, build, post

DEEP = "#1F3A1C"
SOIL_TOP = 790
SLIDES = 7


def soil_band(seed):
    """Our compost close-ups, mirrored side by side into one long cross-section with a crumbly top edge."""
    h = H - SOIL_TOP + 40
    # the clump of finished compost in R5A_4007, without the fork or the background
    patch = Image.open(N("R5A_4007.jpg")).convert("RGB").crop((360, 280, 1020, 700))
    patch = patch.resize((round(patch.width * h / patch.height), h), Image.LANCZOS)
    band = Image.new("RGB", (W * SLIDES, h))
    for i, x in enumerate(range(0, W * SLIDES, patch.width)):
        band.paste(patch.transpose(Image.FLIP_LEFT_RIGHT) if i % 2 else patch, (x, 0))
    # darker with depth, like the reference
    a = np.array(band, np.float32)
    shade = np.linspace(1.0, 0.62, h, dtype=np.float32)[:, None, None]
    band = Image.fromarray(np.clip(a * shade, 0, 255).astype(np.uint8)).convert("RGBA")
    rnd = random.Random(seed)
    m = Image.new("L", band.size, 0)
    d = ImageDraw.Draw(m)
    top = [(x, 30 + rnd.uniform(-6, 6) + 4 * math.sin(x / 37)) for x in range(0, band.width + 12, 12)]
    d.polygon(top + [(band.width, h), (0, h)], fill=255)
    band.putalpha(m.filter(ImageFilter.GaussianBlur(1)))
    return band


def burrow(h, seed):
    """A vertical worm channel: a dark tube with pale root threads running down beside it."""
    rnd = random.Random(seed)
    w = 160

    def fn(d, s):
        pts, x = [], w / 2
        for y in range(0, h, 8):
            x += rnd.uniform(-1.5, 1.5) + 2.5 * math.sin(y / 70 + seed)
            pts.append((x * s, y * s))
        d.line(pts, fill=(40, 26, 18, 150), width=round(44 * s), joint="curve")
        d.line(pts, fill=(25, 16, 11, 200), width=round(30 * s), joint="curve")
        for side in (-1, 1):
            rp = [(px + side * 22 * s + rnd.uniform(-2, 2) * s, py) for px, py in pts[: int(len(pts) * rnd.uniform(0.6, 0.9))]]
            d.line(rp, fill=(236, 230, 214, 220), width=max(1, round(1.6 * s)))
            for j in range(4, len(rp) - 2, 7):
                bx, by = rp[j]
                L = rnd.uniform(18, 40) * s
                ang = math.radians(rnd.choice((-1, 1)) * rnd.uniform(20, 60) + 90)
                d.line((bx, by, bx + side * L * abs(math.cos(ang)), by + L * math.sin(ang) * 0.6),
                       fill=(236, 230, 214, 200), width=max(1, round(1.1 * s)))

    return draw_layer(w, h, fn)


def logo_full(w=210):
    im = Image.open("/home/user/sfwlib/img/sfwlogo-240.png").convert("RGBA")
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


@post("p08", "2026-10-21", "world-earthworm-day", SLIDES)
def p08(d):
    d.bg(None, gradient(W * SLIDES, H, [(0, "#F7C98F"), (0.35, "#FBE0B6"), (0.6, "#FCEBCB"), (1, "#F6DDB5")], 81))
    band = soil_band(3)
    d.put(0, "soil-cross-section", band, W * SLIDES // 2, SOIL_TOP - 40 + band.height // 2, shadowed=False)

    clover = f"{OH}/crimson-clover-capri.webp"
    plants = []
    rnd = random.Random(9)
    x = 120
    while x < W * SLIDES - 80:
        kind = rnd.choice(["clover", "clover", "clover", "poppy", "marigold"])
        plants.append((kind, x))
        x += rnd.randint(170, 260)
    for i, (kind, px) in enumerate(plants):
        if kind == "clover":
            im = cutout(clover, h=rnd.randint(130, 165))
        elif kind == "poppy":
            im = flower("norfolk-common-poppy", h=rnd.randint(200, 240))
        else:
            im = flower("tamil-nadu-marigold", h=rnd.randint(170, 200))
        d.put(0, f"plant-{kind}-{i + 1}", im, px, SOIL_TOP - im.height // 2 + 22, off=(6, 8), blur=8, alpha=0.3)

    # burrows on every slide, at different places
    for k in range(SLIDES):
        for j, bx in enumerate([(230, 560, 880), (300, 760), (220, 520, 860), (420, 760), (260, 640, 900), (350, 820),
                                (240, 600, 900)][k]):
            b = burrow(H - SOIL_TOP - 20 - (j % 2) * 120, 10 * k + j)
            d.put(k, f"burrow-{j + 1}", b, bx, SOIL_TOP + 10 + b.height // 2, shadowed=False)

    d.put(0, "earthworm", soil("earthworm", h=320), 560, 1110, rot=6)
    d.put(1, "earthworm-deep", soil("earthworm", h=300, flip=True), 760, 1150, rot=-10)
    d.put(2, "micrograph-ciliate", lens(N("Ciliate, 60x obj, Patricia J Coppola.jpg"), 300), 800, 1080)
    d.put(3, "rain", rain(W, 300, 4, color="#6E97AC", n=150), W // 2, SOIL_TOP - 180, shadowed=False)
    d.put(3, "water-down-burrow", rain(70, 420, 6, color="#A8D2E4", n=60), 420, SOIL_TOP + 230, shadowed=False)
    d.put(4, "earthworm-curled", soil("earthworm", h=260), 640, 1120, rot=40)
    d.put(5, "dry-leaves", soil("dry-leaves-twigs", w=240), 560, SOIL_TOP - 50)
    d.put(5, "wood-chips", soil("wood-chips-pile", w=240), 180, SOIL_TOP - 40)
    d.put(6, "compost", soil("compost-white-fungal-threads", w=260), 420, SOIL_TOP - 50)
    d.put(6, "mushrooms", soil("mushrooms", w=200), 760, SOIL_TOP - 70)

    texts = [
        ("How do worms work their magic?", "World Earthworm Day, 21 October"),
        ("Anecic earthworms dig vertical burrows that can reach 1 to 2 meters deep to break up compaction.", None),
        ("They spread microbes around as they move by lining the walls with mucus and casts, rich in nutrients and microbes.", None),
        ("Their channels let rain soak in fast without causing the ground to go anaerobic.", None),
        ("How to care for them?", None),
        ("Digging cuts the burrows. No-dig keeps the plumbing intact.", None),
        ("Add organic matter (or simply don't remove it).", None),
    ]
    for k, (t, sub) in enumerate(texts):
        size = 96 if len(t) < 40 else 64
        bottom = d.text(k, "headline", t, 92, 150, 700, 430, size, kind="montserrat-bold", italic=False,
                        color=DEEP, lh=1.08)
        if sub:
            d.text(k, "small line", sub, 94, round(bottom) + 18, 800, 60, 40, kind="source", italic=False, color=GREEN)
    for k in range(SLIDES):
        d.put(k, "logo", logo_full(), W - 170, 120, shadowed=False)


if __name__ == "__main__":
    build("p08")
    print("p08 built")
