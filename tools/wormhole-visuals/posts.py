"""Every planned post's carousel, built with collage.py.

  python3 tools/wormhole-visuals/posts.py [post ids...]
    -> apps/web/public/wormhole/tiles/<id>-<n>.jpg
    -> tools/wormhole-visuals/out/decks/DD-MM-YYYY-<slug>.pptx
    -> tools/wormhole-visuals/out/manifest.json (slides per post, pptx name, visual-note additions)
"""
import json
import os
import sys

from collage import (CREAM, DEEP, GREEN, H, INK, KRAFT, PURPLE, SOIL, W, Deck, cover, cutout, flower, gradient,
                     hyphae, lens, paper, phone, print_photo, rain, rembg_cut, round_photo, roots, soil, card)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
OUT = os.path.join(HERE, "out")
DECKS = os.path.join(OUT, "decks")
NEW = "/home/user/photos/new-2026-10"
SITEIMG = "/home/user/linneamoritznyc/final-sfwsite-linnea/img"
PAST = "/home/user/photos/past-workshop-images"
PICKS = "/home/user/photos/past-workshop-picks/img"
MICRO = "/home/user/SFW-SocialMedia/assets/microscopy"
PHOTO = "/home/user/SFW-SocialMedia/assets/photo"
SHOTS = os.environ.get("SFW_SHOTS", "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/site")
OH = "/home/user/sfwlib/social/open-house-2026-10-16/cutouts"


def N(name):
    return os.path.join(NEW, name)


BUILDERS = {}


def post(pid, iso, slug, n):
    def wrap(fn):
        BUILDERS[pid] = (iso, slug, n, fn)
        return fn
    return wrap


def head(d, k, text, color, y=120, size=96, w=860, h=330, x=72, shade=False):
    return d.text(k, "headline", text, x, y, w, h, size, color=color, shade=shade)


def small(d, k, text, color, y, size=40, w=820, h=200, x=76, shade=False):
    return d.text(k, "small line", text, x, y, w, h, size, italic=False, color=color, lh=1.2, shade=shade)


# ===================================================================== Reel covers
@post("d24", "2026-10-21", "read-the-drop-reel-cover", 1)
def d24(d):
    d.bg(0, paper(DEEP, 241))
    d.put(0, "micrograph-amoeba-and-flagellate", lens(N("Naked amoeba (stellate), flagellate, 40x obj, Jimena Fuentes.jpg"), 640), 540, 820)
    d.put(0, "naked-amoeba", cutout(f"{MICRO}/cutout-2.png", w=300), 860, 1110, rot=-8)
    d.put(0, "nematode", cutout(f"{MICRO}/cutout-7.png", w=330), 210, 1170, rot=12)
    head(d, 0, "Read the drop.", CREAM, y=150, size=124, shade=True)
    small(d, 0, "Predators turn bacterial nitrogen into ammonium.", CREAM, 300, size=40, w=700, shade=True)
    d.logo(0, "tr")


@post("p18", "2026-10-31", "vampire-amoeba-reel-cover", 1)
def p18(d):
    d.bg(0, gradient(W, H, [(0, "#101A12"), (0.6, "#1D3020"), (1, "#2C4128")], 181))
    moon = round_photo(f"{MICRO}/testate-amoeba-encysting-40x-1600.jpg", 330, ring=0)
    d.put(0, "moon-testate-amoeba", moon, 800, 300, off=(0, 0), blur=24, alpha=0.25)
    d.put(0, "fungal-threads", hyphae(1080, 520, 18, color="#D9D2BE", n=5, width=2.0), 540, 1080, shadowed=False)
    d.put(0, "naked-amoeba", cutout(f"{MICRO}/cutout-2.png", w=520), 520, 860, rot=6)
    head(d, 0, "Vampire amoeba.", CREAM, y=560, size=120, w=600, h=300, shade=True)
    d.logo(0, "bl")


@post("d20", "2026-10-27", "julia-worm-bin-reel-cover", 1)
def d20(d):
    d.bg(0, paper(KRAFT, 201))
    d.put(0, "compost", soil("compost-white-fungal-threads", w=560), 360, 1010)
    d.put(0, "dark-soil", soil("dark-soil-clump", w=460), 760, 1070)
    d.put(0, "earthworm", soil("earthworm", h=420), 610, 880, rot=-35)
    d.put(0, "earthworm-2", soil("earthworm", h=300, flip=True), 300, 860, rot=25)
    d.put(0, "dry-leaves", soil("dry-leaves-twigs", w=300), 900, 820, rot=10)
    head(d, 0, "Julia's worm bin.", DEEP, y=170, size=128)
    small(d, 0, "Vermicompost, made at home.", DEEP, 470)
    d.logo(0, "tr")


# ===================================================================== science, continuous scenes
@post("p12", "2026-10-24", "leave-the-leaves", 6)
def p12(d):
    # one autumn ground, seen from above, running across all six slides
    d.bg(None, paper("#2B3A22", 121, w=W * 6, h=H))
    for i, (x, y, r) in enumerate([(300, 1150, 12), (900, 1180, -20), (1500, 1120, 30), (2150, 1190, -8), (2700, 1100, 18),
                                   (3300, 1170, -25), (3850, 1130, 6), (4500, 1180, -14), (5100, 1120, 22), (5800, 1170, -6),
                                   (6300, 1150, 14)]):
        d.put(0, f"leaf-litter-{i + 1}", soil("dry-leaves-twigs", w=360 + (i % 3) * 60), x, y, rot=r)
    d.put(0, "fungal-threads", hyphae(W * 6, 420, 7, color="#EDE6D3", n=26, width=2.0), W * 3, 1130, shadowed=False)
    d.put(1, "micrograph-fungal-hypha", lens(N("Fungal hypha, 100x obj, Marco Trevisan.jpg"), 520), 560, 660)
    d.put(2, "mushrooms", soil("mushrooms", w=420), 760, 760)
    d.put(3, "fern-fiddlehead", soil("fern-fiddlehead", w=300), 820, 720)
    d.put(3, "acorns", soil("acorns", w=280), 300, 820, rot=-10)
    d.put(4, "moss", soil("moss-clump", w=440), 560, 760)
    d.put(5, "wood-chips", soil("wood-chips-pile", w=420), 740, 760)
    texts = ["Before you bag those leaves, read this.", "Leaf litter is rich in carbon and lignin.",
             "Fungi are the main decomposers of lignin.", "That feeds the fungal soils trees and shrubs prefer.",
             "A layer of leaves shields the soil over winter.", "On a lawn, shred the leaves and move them onto your beds."]
    for k, t in enumerate(texts):
        head(d, k, t, CREAM, y=110, size=92 if k else 104, h=380, shade=True)
    d.logo(0, "tr")
    d.logo(5, "tr")


@post("p24", "2026-11-09", "most-common-animal", 3)
def p24(d):
    for k, c in enumerate([CREAM, DEEP, KRAFT]):
        d.bg(k, paper(c, 240 + k))
    d.text(0, "big number", "440,000,000,000,000,000,000", 64, 170, 960, 140, 88, kind="garamond-bold", italic=False, color=DEEP, lh=1.0)
    small(d, 0, "soil nematodes on Earth, by the 2019 estimate in Nature.", DEEP, 300, size=44, w=760)
    d.put(0, "micrograph-nematode", lens(N("Bacterial-feeding nematode, 40x obj, Casey Williams.jpg"), 600), 540, 900)
    d.put(0, "nematode", cutout(f"{MICRO}/cutout-6.png", w=420), 820, 1180, rot=-12)
    d.text(1, "big", "57 billion", 64, 200, 900, 200, 150, color=CREAM, italic=True, lh=1.0, shade=True)
    small(d, 1, "for every person alive.", CREAM, 390, size=48, shade=True)
    for i, (x, y, r, w) in enumerate([(200, 820, 20, 300), (520, 980, -30, 260), (860, 860, 50, 280), (330, 1160, -60, 240), (760, 1180, 10, 300)]):
        d.put(1, f"nematode-{i + 1}", cutout(f"{MICRO}/cutout-{[5, 6, 7, 5, 6][i]}.png", w=w), x, y, rot=r)
    head(d, 2, "Most feed on bacteria and fungi, and release nitrogen right at the root.", DEEP, y=150, size=78, h=420)
    d.put(2, "roots", roots(900, 520, 24, color="#6E5238", n=6), 540, 1050, shadowed=False)
    d.put(2, "nematode", cutout(f"{MICRO}/cutout-7.png", w=360), 600, 980, rot=15)
    d.put(2, "dark-soil", soil("dark-soil-clump", w=340), 230, 1210)
    d.logo(0, "tr")
    d.logo(2, "br")


# ===================================================================== mentors
def mentor(d, name, portrait, cover_bg, flowers_kit, organism, quote, thanks, cut=False, crop=None, fy=0.4):
    d.bg(0, paper(cover_bg, hash(name) % 997))
    dark = cover_bg in (DEEP, INK, SOIL)
    col = CREAM if dark else DEEP
    small(d, 0, "Meet our mentors", col, 120, size=40, shade=dark)
    head(d, 0, name, col, y=175, size=118, h=300, shade=dark)
    if cut:
        p = cutout(rembg_cut(portrait, "person-" + name.lower().replace(" ", "-").replace(".", ""), crop=crop), h=860)
        d.put(0, "portrait-cutout", p, 600, H - p.height // 2 - 10, off=(14, 10))
    else:
        d.put(0, "portrait", round_photo(portrait, 600, fy=fy), 560, 860)
    for i, (nm, kw, x, y, r) in enumerate(flowers_kit):
        d.put(0, nm, flower(nm, **kw), x, y, rot=r)
    d.logo(0, "tr")
    # slide 2: their organism or words
    d.bg(1, paper(CREAM if dark else DEEP, hash(name) % 991 + 1))
    col2 = DEEP if dark else CREAM
    if organism:
        src, label = organism
        d.put(1, "micrograph", lens(src, 620), 540, 900)
        small(d, 1, label, col2, 1240, size=30, w=940, shade=not dark)
    d.text(1, "quote", quote, 72, 120, 920, 470 if organism else 900, 66, color=col2, lh=1.12, shade=not dark)
    # slide 3: thank you
    d.bg(2, paper(cover_bg, hash(name) % 983 + 2))
    head(d, 2, thanks, col, y=200, size=110, h=500, shade=dark)
    for i, (nm, kw, x, y, r) in enumerate(reversed(flowers_kit)):
        d.put(2, nm + "-2", flower(nm, **kw), W - x, y + 40, rot=-r)
    d.logo(2, "tl" if False else "br")


@post("p02", "2026-10-19", "meet-casey-williams", 3)
def p02(d):
    mentor(d, "Casey Williams", N("team-casey-williams.jpg"), DEEP,
           [("santa-fe-indian-paintbrush", dict(h=380), 140, 1120, -8), ("santa-fe-chamisa", dict(w=360), 920, 1180, 6)],
           (N("Bacterial-feeding nematode, 40x obj, Casey Williams.jpg"), "A bacterial-feeding nematode, 40x, photographed by Casey."),
           "“I am deeply grateful that I get to learn from my students as well as teach them.”",
           "Thank you, Casey.")


BUILT = {}


def build(pid):
    iso, slug, n, fn = BUILDERS[pid]
    d = Deck(pid, n, slug, iso)
    fn(d)
    os.makedirs(DECKS, exist_ok=True)
    names, slides = d.save(TILES, DECKS)
    BUILT[pid] = dict(iso=iso, slides=["/wormhole/tiles/" + x for x in names], texts=d.slide_texts(), pptx=d.pptx_name(), notes=d.notes)
    # keep the manifest current whichever script did the build
    mpath = os.path.join(OUT, "manifest.json")
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {}
    manifest[pid] = BUILT[pid]
    json.dump(manifest, open(mpath, "w"), indent=1)
    return slides


if __name__ == "__main__":
    ids = sys.argv[1:] or list(BUILDERS)
    os.makedirs(OUT, exist_ok=True)
    mpath = os.path.join(OUT, "manifest.json")
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {}
    for pid in ids:
        build(pid)
        manifest[pid] = BUILT[pid]
        print(pid, len(BUILT[pid]["slides"]), BUILT[pid]["pptx"])
    json.dump(manifest, open(mpath, "w"), indent=1)
