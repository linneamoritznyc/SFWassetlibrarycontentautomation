"""p11, p12, p13, p05, p14 in the watercolor science-book style.

Warm white paper, loose watercolor illustrations (watercolor_gen.py) with thin grey
ink outlines, real photos and screenshots in thin ink frames, a rounded heading in
Soil Brown, Montserrat body text, thin brown hand-drawn arrows with short labels,
and the logo small in the empty bottom-right corner.

  python3 tools/wormhole-visuals/watercolor_posts.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v2-<n>.jpg and the .pptx decks
"""
import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from collage import H, W, cover, draw_layer, hexrgb, paper
from posts import build, post

GEN = "/home/user/wc/gen"
SHOTS = "/home/user/wc/shots"
PAST = "/home/user/photos/past-workshop-images"
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
PAPER = "#FBF9F4"
BROWN = "#4F3433"
BODY = "#5C4636"
INK = (96, 92, 88)


# ------------------------------------------------------------------ pieces
def wc(name, w=None, h=None):
    """A generated watercolor as a transparent layer: white paper becomes see-through."""
    im = Image.open(f"{GEN}/{name}.png").convert("RGB")
    a = np.asarray(im).astype(np.float32)
    alpha = (255 - a.min(axis=2)) / 255.0
    alpha = np.clip((alpha - 0.03) / 0.97, 0, 1)  # paper grain stays clean
    safe = np.maximum(alpha, 1e-3)[..., None]
    rgb = 255 - (255 - a) / safe
    out = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")
    box = im.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
    im = im.crop(box)
    if w and h:
        s = min(w / im.width, h / im.height)
    elif w:
        s = w / im.width
    else:
        s = h / im.height
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def wobble_rect(dr, s, x0, y0, x1, y1, seed, width=2.4):
    rnd = random.Random(seed)
    pts = []
    for (ax, ay), (bx, by) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        n = 24
        for i in range(n):
            t = i / n
            pts.append((ax + (bx - ax) * t + rnd.uniform(-1.2, 1.2), ay + (by - ay) * t + rnd.uniform(-1.2, 1.2)))
    pts.append(pts[0])
    dr.line([(x * s, y * s) for x, y in pts], fill=INK + (255,), width=max(1, round(width * s)), joint="curve")


def framed(src, w, h, seed=1, fx=0.5, fy=0.5, pad=10):
    """A real photo or screenshot set into the page with a thin hand-drawn ink border."""
    photo = cover(src, w, h, fx, fy).convert("RGBA")
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    out.alpha_composite(photo, (pad, pad))
    out.alpha_composite(draw_layer(out.width, out.height,
                                   lambda dr, s: wobble_rect(dr, s, pad - 3, pad - 3, pad + w + 3, pad + h + 3, seed)))
    return out


def browser(src, w, h, seed=1):
    """A screenshot in a drawn browser window: ink outline, a top bar with three dots."""
    bar = 46
    shot = cover(src, w, h - bar, 0.5, 0.0).convert("RGBA")
    out = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    base = Image.new("RGBA", (w, bar), hexrgb("#EFEAE0") + (255,))
    out.alpha_composite(base, (10, 10))
    out.alpha_composite(shot, (10, 10 + bar))

    def fn(dr, s):
        wobble_rect(dr, s, 8, 8, 12 + w, 12 + h, seed)
        dr.line((10 * s, (10 + bar) * s, (10 + w) * s, (10 + bar) * s), fill=INK + (255,), width=round(2 * s))
        for i, c in enumerate(("#D98C7A", "#E3C27A", "#9DBF8E")):
            cx, cy = 34 + i * 26, 10 + bar / 2
            dr.ellipse(((cx - 7) * s, (cy - 7) * s, (cx + 7) * s, (cy + 7) * s), fill=hexrgb(c) + (255,),
                       outline=INK + (255,), width=round(1.5 * s))
    out.alpha_composite(draw_layer(out.width, out.height, fn))
    return out


def arrow_layer(p0, p1, bend=0.25, seed=0):
    """A thin brown hand-drawn arrow from p0 to p1 (slide coordinates); returns (layer, x, y)."""
    rnd = random.Random(seed)
    x0, y0 = p0
    x1, y1 = p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * bend, my + dx * bend
    pts = []
    for i in range(41):
        t = i / 40
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1 + rnd.uniform(-0.6, 0.6)
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1 + rnd.uniform(-0.6, 0.6)
        pts.append((x, y))
    ex, ey = pts[-1]
    px, py = pts[-4]
    ang = math.atan2(ey - py, ex - px)
    head = [(ex - 20 * math.cos(ang - 0.45), ey - 20 * math.sin(ang - 0.45)), (ex, ey),
            (ex - 20 * math.cos(ang + 0.45), ey - 20 * math.sin(ang + 0.45))]
    xs = [p[0] for p in pts + head]
    ys = [p[1] for p in pts + head]
    left, top = int(min(xs)) - 6, int(min(ys)) - 6
    w, h = int(max(xs)) - left + 6, int(max(ys)) - top + 6

    def fn(dr, s):
        dr.line([((x - left) * s, (y - top) * s) for x, y in pts], fill=hexrgb(BROWN) + (255,), width=round(2.6 * s),
                joint="curve")
        dr.line([((x - left) * s, (y - top) * s) for x, y in head], fill=hexrgb(BROWN) + (255,), width=round(2.6 * s),
                joint="curve")
    return draw_layer(w, h, fn), left, top


# ------------------------------------------------------------------ slide helpers
def page(d, n, seed):
    for k in range(n):
        d.bg(k, paper(PAPER, seed + k, grain=6), name=f"background-{k + 1}")


def heading(d, k, text, size=78, y=90, w=900, x=90):
    return d.text(k, "headline", text, x, y, w, 330, size, kind="fredoka", italic=False, color=BROWN, lh=1.1)


def body(d, k, text, y, size=34, w=880, x=92):
    return d.text(k, "body", text, x, round(y), w, 260, size, kind="mont", italic=False, color=BODY, lh=1.35)


def label(d, k, text, x, y, w=300, size=27, align="left"):
    d.text(k, f"label {text[:20]}", text, x, y, w, 120, size, kind="mont-medium", italic=False, color=BROWN, lh=1.2,
           align=align)


def put_tl(d, k, name, im, x, y):
    d.put(k, name, im, x, y, shadowed=False, anchor="tl")
    return x, y, im.width, im.height


def at(box, fx, fy):
    x, y, w, h = box
    return x + w * fx, y + h * fy


def arrow(d, k, p0, p1, bend=0.25, seed=0):
    lay, x, y = arrow_layer(p0, p1, bend, seed)
    d.put(k, "arrow", lay, x, y, shadowed=False, anchor="tl")


def logo(d, k):
    im = Image.open(LOGO).convert("RGBA")
    im = im.resize((150, round(im.height * 150 / im.width)), Image.LANCZOS)
    d.put(k, "logo", im, W - 60 - im.width, H - 50 - im.height, shadowed=False, anchor="tl")


def centered(im, y):
    return (W - im.width) // 2, y


# ------------------------------------------------------------------ p11 Our new website is live
@post("p11", "2026-10-23", "our-new-website-is-live-v2", 4)
def p11(d):
    page(d, 4, 1100)
    hb = heading(d, 0, "Our new home is live!", size=96)
    body(d, 0, "Every course, every workshop, a map of soil consultants and Dr. Elaine's papers, in one place.", hb + 24)
    lap = wc("laptop-seedling", w=840)
    x, y = centered(lap, 420)
    box = put_tl(d, 0, "laptop", lap, x, y)
    # the real home page on the drawn screen
    sx0, sy0 = at(box, 0.215, 0.255)
    sx1, sy1 = at(box, 0.79, 0.545)
    shot = cover(f"{SHOTS}/home.png", int(sx1 - sx0), int(sy1 - sy0), 0.5, 0.0).convert("RGBA")
    d.put(0, "screenshot-home", shot, int(sx0), int(sy0), shadowed=False, anchor="tl")
    d.put(0, "seedling-again", wc("laptop-seedling", w=840).crop((int(0.36 * lap.width), int(0.47 * lap.height),
                                                                   int(0.64 * lap.width), int(0.66 * lap.height))),
          x + int(0.36 * lap.width), y + int(0.47 * lap.height), shadowed=False, anchor="tl")
    label(d, 0, "soilfoodweb.com", 90, 470, w=260)
    arrow(d, 0, (200, 520), at(box, 0.28, 0.33), bend=-0.25, seed=1)
    label(d, 0, "something new is growing", 700, 1170, w=280)
    arrow(d, 0, (760, 1165), at(box, 0.56, 0.58), bend=0.3, seed=2)
    logo(d, 0)

    pages = [("Every course, in one learning path.", "programs.png",
              "Self-paced or group classes, online or in person.", "spot-seedling", "start learning here"),
             ("Find a soil consultant near you.", "map2.png",
              "Search our directory by country and by bioregion.", "spot-globe", "filter by bioregion"),
             ("Dr. Elaine's papers, in one library.", "papers.png",
              "A growing database of soil food web science and Dr. Elaine Ingham's publications.", "spot-papers",
              "her research, open to all")]
    for k, (h, shot, line, spot, lab) in enumerate(pages, start=1):
        body(d, k, line, heading(d, k, h, size=74) + 24)
        win = browser(f"{SHOTS}/{shot}", 780, 500, seed=k)
        bx, by = 90, 470
        box = put_tl(d, k, "browser-window", win, bx, by)
        sp = wc(spot, w=230)
        put_tl(d, k, "watercolor-" + spot, sp, 720, 1000)
        label(d, k, lab, 120, 1100, w=330)
        arrow(d, k, (300, 1095), at(box, 0.45, 0.82), bend=-0.3, seed=10 + k)
        logo(d, k)


# ------------------------------------------------------------------ p12 Leave the leaves
@post("p12", "2026-10-24", "leave-the-leaves-v2", 2)
def p12(d):
    page(d, 2, 1200)
    heading(d, 0, "Leave the leaves!", size=96)
    body(d, 0, "Fallen leaves are one of the best gifts your soil gets all year.", 230)
    im = wc("leaf-cutaway", h=860)
    box = put_tl(d, 0, "leaf-cutaway", im, (W - im.width) // 2 + 40, 360)
    label(d, 0, "leaves full of carbon and lignin", 70, 400, w=270)
    arrow(d, 0, (200, 490), at(box, 0.38, 0.17), bend=-0.25, seed=1)
    label(d, 0, "fungi break the lignin down", 70, 760, w=250)
    arrow(d, 0, (250, 830), at(box, 0.17, 0.43), bend=0.2, seed=2)
    label(d, 0, "a worm pulls a leaf into its burrow", 790, 640, w=250)
    arrow(d, 0, (820, 720), at(box, 0.56, 0.52), bend=0.25, seed=3)
    label(d, 0, "beetles shelter for the winter", 800, 410, w=240)
    arrow(d, 0, (830, 480), at(box, 0.72, 0.27), bend=-0.2, seed=4)
    logo(d, 0)
    heading(d, 1, "Have a lawn?", size=96)
    body(d, 1, "Shred the leaves with the mower and move them onto your garden beds. A leaf layer protects the soil "
               "over winter.", 230)
    m = framed(f"{GEN}/mower-leaves.png", 760, 760, seed=5, fy=0.55)
    box = put_tl(d, 1, "mower-scene", m, 90, 440)
    label(d, 1, "shredded leaves", 860, 700, w=200)
    arrow(d, 1, (900, 790), at(box, 0.5, 0.82), bend=-0.3, seed=6)
    label(d, 1, "a free mulch for your beds", 860, 470, w=200)
    arrow(d, 1, (900, 590), at(box, 0.82, 0.62), bend=0.25, seed=7)
    logo(d, 1)


# ------------------------------------------------------------------ p13 Dr. Elaine's flowers in our logo
@post("p13", "2026-10-25", "dr-elaine-flowers-in-our-logo-v2", 2)
def p13(d):
    page(d, 2, 1300)
    heading(d, 0, "Look closely at our new logo.", size=84)
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((470, round(lg.height * 470 / lg.width)), Image.LANCZOS)
    box = put_tl(d, 0, "logo-large", lg, (W - lg.width) // 2, 470)
    v = wc("purple-vine", w=330)
    put_tl(d, 0, "watercolor-purple-vine", v, 60, 300)
    s = wc("purple-sprig", h=330)
    put_tl(d, 0, "watercolor-purple-sprig", s, 860, 330)
    o = wc("purple-flower-open", w=260)
    put_tl(d, 0, "watercolor-purple-flower", o, 120, 930)
    label(d, 0, "purple flowers, for Dr. Elaine", 600, 960, w=300)
    arrow(d, 0, (640, 960), at(box, 0.47, 0.25), bend=0.3, seed=1)
    arrow(d, 0, (380, 1000), at(box, 0.25, 0.22), bend=-0.3, seed=2)
    label(d, 0, "a vine growing up from the roots", 640, 1110, w=300)
    arrow(d, 0, (650, 1150), at(box, 0.7, 0.3), bend=0.35, seed=3)
    logo(d, 0)
    heading(d, 1, "Purple was her favorite color.", size=84)
    body(d, 1, "We added purple flowers to our logo in honor of Dr. Elaine Ingham. See it on our new website. "
               "Link in bio.", 300)
    big = wc("purple-vine", h=700)
    put_tl(d, 1, "watercolor-purple-vine", big, (W - big.width) // 2, 500)
    logo(d, 1)


# ------------------------------------------------------------------ p05 What can I do right now?
@post("p05", "2026-10-26", "improve-your-soil-v2", 6)
def p05(d):
    page(d, 6, 500)
    heading(d, 0, "What can I do right now to improve my soil?", size=78)
    body(d, 0, "Five things that make a difference.", 300)
    im = wc("bed-cutaway", h=820)
    box = put_tl(d, 0, "garden-bed-cutaway", im, (W - im.width) // 2, 400)
    label(d, 0, "mulch on top", 60, 470, w=200)
    arrow(d, 0, (130, 520), at(box, 0.2, 0.2), bend=-0.3, seed=1)
    label(d, 0, "seedlings and their roots", 820, 430, w=220)
    arrow(d, 0, (860, 520), at(box, 0.6, 0.12), bend=0.3, seed=2)
    label(d, 0, "fungal threads", 60, 860, w=200)
    arrow(d, 0, (140, 910), at(box, 0.3, 0.46), bend=0.25, seed=3)
    label(d, 0, "an earthworm", 860, 800, w=200)
    arrow(d, 0, (880, 850), at(box, 0.73, 0.5), bend=-0.25, seed=4)
    logo(d, 0)

    steps = [
        ("Cover your soil.", "Mulch, cover crops, or leaf litter left where it falls. Bare ground loses biology, "
         "moisture and structure.", "cover-soil",
         [("straw mulch", (70, 1150), (0.15, 0.55)), ("a clover cover crop", (390, 1180), (0.45, 0.35)),
          ("leaves left where they fall", (760, 1140), (0.8, 0.62))]),
        ("Add biologically active compost.", "Bacteria, fungi, protozoa and nematodes, all working together.",
         "compost-hand", [("a handful of compost", (70, 1140), (0.42, 0.42)),
                          ("the life inside, magnified", (780, 1140), (0.85, 0.27))]),
        ("Dig less.", "Fungal networks that took months to build can be gone in a single pass.", "spade-fungi",
         [("a spade cuts through", (760, 560), (0.6, 0.18)), ("torn fungal threads", (70, 1140), (0.45, 0.66))]),
        ("Feed the fungi.", "Woody mulch and carbon-rich material shift the balance toward fungi.", "woodchips-fungi",
         [("wood chips", (70, 560), (0.3, 0.22)), ("fungal threads grow down", (760, 1140), (0.6, 0.62))]),
        ("Tell someone what you're learning.", "Demonstration is still the most powerful thing we have.",
         "hands-seedling", [("pass it on", (90, 1150), (0.55, 0.4))]),
    ]
    for k, (h, line, img, labels) in enumerate(steps, start=1):
        bottom = body(d, k, line, heading(d, k, h, size=80) + 24)
        top = max(430, round(bottom) + 40)
        im = wc(img, w=760, h=1100 - top)
        box = put_tl(d, k, img, im, (W - im.width) // 2, top)
        for j, (txt, (lx, ly), (fx, fy)) in enumerate(labels):
            label(d, k, txt, lx, ly, w=250)
            arrow(d, k, (lx + 80, ly - 10 if ly > 800 else ly + 70), at(box, fx, fy), bend=0.25 * (-1) ** j,
                  seed=10 * k + j)
        logo(d, k)


# ------------------------------------------------------------------ p14 Costa Rica
@post("p14", "2026-10-26", "costa-rica-compost-together-v2", 4)
def p14(d):
    page(d, 4, 1400)
    a23 = f"{PAST}/accelerator-workshop-august-2023/accelerator-workshop-august-2023-"
    m25 = f"{PAST}/accelerator-workshop-march-2025/accelerator-workshop-march-2025-"
    slides = [
        ("Compost is a team sport.", "At our Accelerator Workshop in Costa Rica, students practise together with "
         "mentors beside them.", f"{a23}03-laughing-at-compost-cage.jpg", "building compost piles by hand", 0.45),
        ("Making liquid amendments.", "Students learn to make compost extracts and teas that carry living biology "
         "out onto the fields.", f"{m25}02-liquid-amendments-demonstration.jpg", "liquid amendments, step by step",
         0.4),
        ("Reading their own samples.", "Long sessions at the microscope, with mentors beside them.",
         f"{m25}01-microscopy.jpg", "the microscope", 0.4),
        ("Join us in Costa Rica.", "Our next Accelerator Workshop runs in January 2027. Join the interest list, "
         "link in bio.", f"{a23}04-students-holding-buckets.jpg", "hands-on, every day", 0.4),
    ]
    plants = [("heliconia", 260), ("torch-ginger", 300), ("banana-leaves", 280), ("heliconia", 240)]
    for k, (h, line, photo, lab, fy) in enumerate(slides):
        bottom = body(d, k, line, heading(d, k, h, size=80) + 24)
        top = max(400, round(bottom) + 50)
        fr = framed(photo, 700, 540, seed=20 + k, fy=fy)
        box = put_tl(d, k, "photo", fr, 300 if k % 2 == 0 else 80, top)
        name, ph = plants[k]
        p = wc(name, h=ph + 260)
        px = 40 if k % 2 == 0 else W - p.width - 40
        put_tl(d, k, "watercolor-" + name, p, px, H - p.height - 40)
        lx = 560 if k % 2 == 0 else 120
        label(d, k, lab, lx, top + 640, w=330)
        arrow(d, k, (lx + 60, top + 630), at(box, 0.55, 0.78), bend=0.3 if k % 2 == 0 else -0.3, seed=30 + k)
        if k == 0:
            g = wc("torch-ginger", h=420)
            put_tl(d, k, "watercolor-torch-ginger", g, 70, top - 20)
        logo(d, k)


if __name__ == "__main__":
    for pid in sys.argv[1:] or ["p11", "p12", "p13", "p05", "p14"]:
        build(pid)
        print(pid, "built")
