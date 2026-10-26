"""January B (16 to 31 January 2027): v2 photo-and-tag visuals.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/jan_b.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v2-<n>.jpg (1080 x 1350, LinkedIn 1200 x 627)

Costa Rica photos are the real 2025 workshop photos already used in the Costa Rica decks in
apps/web/public/wormhole/decks (read straight out of the .pptx files, nothing copied in).

Never overwrites: if <id>-v2-<n>.jpg exists the whole post moves to v3, v4 and so on.
Prints the slide list as JSON (JAN_B_JSON=<path> to save it).
"""
import io
import json
import os
import sys
import zipfile

from PIL import Image, ImageOps

import boxes as B
import photo_first as PF

SFW = "Photo: Soil Food Web Foundation"
DECKS = os.path.join(B.REPO, "apps", "web", "public", "wormhole", "decks")

# Real 2025 Costa Rica workshop photos, by deck and media file.
CRP = {
    "cr_cheer": ("12-11-2026-costa-rica-a-day.pptx", "image1.jpg"),        # students cheering over a finished pile
    "cr_buckets": ("26-10-2026-ig-stories-costa-rica-2027.pptx", "image13.jpg"),  # group with buckets outdoors
    "cr_shed": ("26-10-2026-ig-stories-costa-rica-2027.pptx", "image7.jpg"),      # group gathered under the shed roof
    "cr_bags": ("16-11-2026-costa-rica-built-to-fail.pptx", "image5.jpg"),        # sorting feedstock from big bags
    "cr_build": ("26-10-2026-ig-stories-costa-rica-2027.pptx", "image4.jpg"),     # building a pile in a wire cage
    "cr_water": ("16-11-2026-costa-rica-built-to-fail.pptx", "image1.jpg"),       # hydrating a pile with a hose
    "cr_micro": ("26-10-2026-ig-stories-costa-rica-2027.pptx", "image15.jpg"),    # students at the microscopes
    "cr_liquid": ("26-10-2026-ig-stories-costa-rica-2027.pptx", "image14.jpg"),   # liquid amendments demonstration
    "cr_cert": ("26-10-2026-ig-stories-costa-rica-2027.pptx", "image18.jpg"),     # group with a certificate
    "cr_group": ("26-10-2026-ig-stories-costa-rica-2027.pptx", "image1.jpg"),     # whole group around the pile
}

PF.CR.update({k: SFW for k in CRP})
PF.CR.update({
    "w_leslie.jpg": SFW,
    "w_ib.jpg": SFW,
    "Screenshot-2025-10-22-212600.jpg": SFW,
    "hand-of-compost.jpg": None,
    "hand-scooping-planter-bed-soil.jpg": None,
    "harringtons-organic-land-care-brick-york-farms-3-768x1024.jpg": "Photo: Harrington's Organic Land Care",
    "harringtons-organic-land-care-brick-york-farms-4-768x1024.jpg": "Photo: Harrington's Organic Land Care",
    "harringtons-organic-land-care-york-farms-1-768x1024.jpg": "Photo: Harrington's Organic Land Care",
    "2-hands-clasped-holding-plant-roots.jpg": None,
    "ctpfw-student-squeezing-compost-1.jpg": SFW,
    "ctpfw-student-moving-compost-1.jpg": SFW,
    "w_test-tubes-with-sample.jpg": None,  # one credit line on the duo
    "w_sampling-equipment.jpg": SFW,
    "hvdb-inplanten-002.jpg": SFW,
    "harringtons-organic-land-care-brick-york-farms-2-768x1024.jpg": "Photo: Harrington's Organic Land Care",
    "2-hands-planting-shrub.jpg": None,
    "handling-loose-soil.jpg": None,
    "soil-sample-close-up-test-tube.jpg": None,
    "soil-sample-shovel-and-bag.jpg": None,
    "fungal-spores-in-suspension.jpg": SFW,
    "hand-soil-roots-fungi.jpg": None,
    "fungi-in-under-grape-soil.jpg": SFW,
    "uploads_6.png": SFW,
    "gloved-hands-red-bucket-mulch.jpg": None,
    "wild-ken-hill_IMG_1492.jpg": SFW,
    "w_erc-rancho-cacachilas-aerial-shot.jpg": SFW,
    "hand-wet-dirt-worm.jpg": None,
    "red-soil-hand.jpg": None,
    "2-dirty-hands.jpg": None,
    "fist-of-dry-soil.jpg": None,
})

_orig_load = PF.load


def load(name, box, focus=(0.5, 0.5), zoom=1.0):
    if name in CRP:
        deck, media = CRP[name]
        with zipfile.ZipFile(os.path.join(DECKS, deck)) as z:
            im = Image.open(io.BytesIO(z.read("ppt/media/" + media))).convert("RGB")
        if zoom > 1:
            w, h = im.size
            cw, ch = int(w / zoom), int(h / zoom)
            x, y = int((w - cw) * focus[0]), int((h - ch) * focus[1])
            im = im.crop((x, y, x + cw, y + ch))
        return ImageOps.fit(im, box, Image.LANCZOS, centering=focus)
    return _orig_load(name, box, focus, zoom)


PF.load = load


def cover_duo(a, b, words):
    """Wide photo shown whole on top (no faces cropped), second photo below, logo on top."""
    c = PF.duo(a, b, words=words, fill=B.DEEP, ink=B.CREAM)
    B.logo(c, (c.width - 150, 40), size=90)
    return c
pic, li, duo = PF.pic, PF.li, PF.duo
G, D, BR, T, BL, L, CRM = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.CREAM

POSTS = {
    "j20270116": lambda: [
        (pic("hand-of-compost.jpg", "Will it sprout?", G, logo=True, size=90), "Is your compost or potting mix ready? Let seeds tell you."),
        (pic("hand-scooping-planter-bed-soil.jpg", "100 seeds.", T, BR, size=90), "Sow 100 radish or cress seeds in moist compost."),
        (pic("handling-loose-soil.jpg", "80 or more? Ready.", D, size=84), "After 5 to 10 days, 80 or more sprouts means it is likely mature."),
    ],
    "j20270117": lambda: [
        (pic("cr_cheer", "Tomorrow we start.", G, focus=(0.5, 0.4), logo=True, size=90), "Tomorrow we start in Costa Rica."),
        (pic("cr_buckets", "Twelve days ahead.", T, BR, focus=(0.5, 0.45), size=84), "Week one: compost. Week two: biological liquid amendments."),
    ],
    "j20270118": lambda: [
        (pic("cr_shed", "Welcome to Costa Rica!", G, focus=(0.5, 0.45), logo=True, size=84), "Story frame 1: welcome to Costa Rica."),
        (pic("cr_bags", "Bienvenidos.", T, BR, focus=(0.5, 0.5), size=90), "Story frame 2: bienvenidos. Link sticker."),
    ],
    "j20270119": lambda: [
        (pic("w_leslie.jpg", "Meet Leslie Lewis", D, focus=(0.5, 0.35), logo=True, size=80), "Meet the team: Leslie W. Lewis, Ph.D., Executive Committee."),
    ],
    "j20270120": lambda: [
        (cover_duo("Screenshot-2025-10-22-212600.jpg", "w_test-tubes-with-sample.jpg", "Soil Regenerators in the wild"), "Soil Regenerators in the wild: TrashIt, Pakistan."),
    ],
    "j20270121": lambda: [
        (pic("harringtons-organic-land-care-brick-york-farms-3-768x1024.jpg", "Sand loosens clay?", BR, logo=True, size=90), "Myth: add sand to loosen clay soil."),
        (pic("harringtons-organic-land-care-brick-york-farms-4-768x1024.jpg", "Feed it instead.", G, size=90), "Add organic matter and let soil life build the crumb."),
    ],
    "j20270122": lambda: [
        (pic("cr_build", "Pile day.", G, focus=(0.5, 0.45), logo=True, size=96), "Live from Costa Rica: building the piles."),
        (pic("cr_water", None, focus=(0.55, 0.4)), "Photo only: hydrating a pile."),
    ],
    "j20270123a": lambda: [
        (li("2-hands-clasped-holding-plant-roots.jpg", "Trees that feed the soil", G, focus=(0.5, 0.5)), "Fertility trees: 33 million planted across West Africa."),
    ],
    "j20270123b": lambda: [
        (pic("ctpfw-student-squeezing-compost-1.jpg", "The squeeze test", BR, focus=(0.5, 0.4), logo=True, size=90), "The squeeze test: is your compost wet enough?"),
    ],
    "j20270124": lambda: [
        (pic("soil-sample-shovel-and-bag.jpg", "Field Notes", G, logo=True, size=96), "Field Notes #3: trial name, place and season."),
        (pic("soil-sample-close-up-test-tube.jpg", None), "The question they tested."),
        (pic("w_sampling-equipment.jpg", None), "The method in 3 lines."),
        (pic("hvdb-inplanten-002.jpg", None, focus=(0.45, 0.5)), "The result, one big number."),
        (pic("harringtons-organic-land-care-brick-york-farms-2-768x1024.jpg", None), "What surprised them, including what didn't work."),
        (pic("2-hands-planting-shrub.jpg", None), "Who ran it."),
    ],
    "j20270125": lambda: [
        (pic("fungal-spores-in-suspension.jpg", "Spores or hyphae?", BR, logo=True, size=90), "Spores or hyphae? What you see on the slide tells you something different."),
        (pic("hand-soil-roots-fungi.jpg", "Hyphae: at work.", G, focus=(0.5, 0.5), size=84), "Hyphae: fungi growing and working now."),
        (pic("fungi-in-under-grape-soil.jpg", None, focus=(0.3, 0.75)), "Photo only: fungi fruiting under vines."),
    ],
    "j20270126": lambda: [
        (pic("cr_micro", "Microscope day.", BL, focus=(0.5, 0.5), logo=True, size=90), "Live from Costa Rica: at the microscope."),
        (pic("cr_liquid", None, focus=(0.5, 0.45)), "Photo only: checking a liquid amendment."),
    ],
    "j20270127": lambda: [
        (pic("wild-ken-hill_IMG_1492.jpg", "Produce no waste.", G, focus=(0.5, 0.45), logo=True, size=90), "Permaculture principle 6: produce no waste."),
        (pic("gloved-hands-red-bucket-mulch.jpg", "Waste is food.", T, BR, size=90), "Prunings become mulch, scraps become compost."),
    ],
    "j20270128": lambda: [
        (pic("harringtons-organic-land-care-york-farms-1-768x1024.jpg", "95% of our food", BR, focus=(0.5, 0.5), logo=True, size=96), "95% of our food is produced in soil."),
        (pic("w_erc-rancho-cacachilas-aerial-shot.jpg", "Grown in living soil.", G, focus=(0.5, 0.5), size=84), "Grown in living soil."),
    ],
    "j20270129": lambda: [
        (pic("cr_cert", "Thank you, Costa Rica.", G, focus=(0.5, 0.5), logo=True, size=84), "Thank you, Costa Rica, and thank you, Armonía."),
        (pic("cr_group", None, focus=(0.5, 0.55)), "Photo only: the whole group around their pile."),
    ],
    "j20270130": lambda: [
        (pic("hand-wet-dirt-worm.jpg", "Fun Soil News", G, logo=True, size=96), "Fun Soil News: January 2027."),
        (pic("red-soil-hand.jpg", "Brazil", T, BR, where="top", size=96), "Brazil: R$250 million to turn 4,000 hectares of degraded land into cocoa agroforests."),
        (pic("2-dirty-hands.jpg", "United States", BL, where="top", size=90), "United States: USDA's Regenerative Pilot Program grows to $1 billion."),
        (pic("fist-of-dry-soil.jpg", "Germany", D, where="top", size=96), "Germany: forest soils took up about 3% more methane each year."),
    ],
    "j20270131": lambda: [
        (pic("w_ib.jpg", "Meet Ib Borup Pedersen", G, focus=(0.5, 0.35), logo=True, size=76), "Meet the team: Ib Borup Pedersen, farmer, Soil Food Web Consultant and mentor."),
    ],
}


def render(pid):
    built = POSTS[pid]()
    v = 2
    while any(os.path.exists(os.path.join(PF.OUT, f"{pid}-v{v}-{i}.jpg")) for i in range(1, len(built) + 1)):
        v += 1
    out = []
    for i, (img, text) in enumerate(built, 1):
        name = f"{pid}-v{v}-{i}.jpg"
        img.save(os.path.join(PF.OUT, name), quality=88, optimize=True)
        out.append({"text": text, "image": f"/wormhole/tiles/{name}"})
    return out


if __name__ == "__main__":
    res = {pid: render(pid) for pid in (sys.argv[1:] or POSTS)}
    path = os.environ.get("JAN_B_JSON")
    if path:
        json.dump(res, open(path, "w"), ensure_ascii=False, indent=1)
    for k, v in res.items():
        print(k, [s["image"] for s in v])
