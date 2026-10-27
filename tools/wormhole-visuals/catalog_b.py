"""Catalog swap, worker B (27 Oct): new versions of Dec 2026 posts with repeated photos
swapped for fresh photos from Linnea's SFW image catalog.

Same v2 photo-and-tag build as photo_first.py (and the brand-box layouts for x20261215):
the tag words, tag colour, tag position, logo and size are copied from the current slide.
Only the photo changes. Nothing in Wormhole is edited; this only writes new tile files.

  BOX_SRC=<catalog photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/catalog_b.py
    -> apps/web/public/wormhole/tiles/<id>-c1-<slide>.jpg  (never overwrites; bumps to c2, c3)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boxes as B  # noqa: E402
import photo_first as PF  # noqa: E402

SFW = "Photo: Soil Food Web Foundation"
G, D, BR, T, BL, L, P, CRM = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.PURPLE, B.CREAM

PF.CR.update({
    "Bacterial-feeding nematode, 40x obj, Talbot Armstrong.jpg": "Photo: Talbot Armstrong",
    "Bacterial-feeding nematode, 40x obj, Casey Williams.jpg": "Photo: Casey Williams",
    "Ciliate, 60x obj, Patricia J Coppola.jpg": "Photo: Patricia J Coppola",
    "Fungal hypha, 100x obj, Marco Trevisan.jpg": "Photo: Marco Trevisan",
    "R5A_3985.jpg": "Photo: Brevity Media",
    "R5A_4028.jpg": "Photo: Brevity Media",
})


def pic(photo, words=None, fill=D, ink=CRM, **kw):
    PF.CR.setdefault(photo, SFW)
    return PF.pic(photo, words, fill, ink, **kw)


# post id -> {slide number (1-based): image builder}
POSTS = {
    "x20261203": {
        1: lambda: pic("PXL_20251022_165704946.jpg", "Costa Rica, January", L, D, focus=(0.5, 0.5), logo=True),
        3: lambda: pic("pile turning wes 7.jpg", None, focus=(0.45, 0.5)),
    },
    "x20261204": {
        5: lambda: pic("20250312_115814.jpg", "Nematodes", G, where="top", focus=(0.72, 0.5), size=64),
    },
    "k20261205": {
        2: lambda: pic("PXL_20240716_224324982 HandsInSoil.jpg", "Volunteer with us", BR, where="top", focus=(0.5, 0.6)),
    },
    "w20261206": {
        1: lambda: pic("IMG_4305.jpg", "Not sure where to start?", G, focus=(0.5, 0.55), logo=True),
        3: lambda: pic("20250305_135420.jpg", "Find your path.", G, focus=(0.68, 0.5)),
    },
    "x20261208": {
        1: lambda: pic("Fungal hypha, 100x obj, Marco Trevisan.jpg", "Who eats whom?", T, BR, focus=(0.62, 0.5), logo=True, size=90),
        3: lambda: pic("Ciliate, 60x obj, Patricia J Coppola.jpg", None, focus=(0.53, 0.5)),
        4: lambda: pic("Bacterial-feeding nematode, 40x obj, Talbot Armstrong.jpg", None, focus=(0.36, 0.5)),
        5: lambda: pic("PXL_20240724_153917825.jpg", "And the plant eats.", G, focus=(0.5, 0.6)),
    },
    "w20261209": {
        1: lambda: pic("R5A_4028.jpg", "How does soil work?", BL, focus=(0.42, 0.5), logo=True),
        2: lambda: pic("Bacterial-feeding nematode, 40x obj, Casey Williams.jpg", None, focus=(0.62, 0.5)),
        3: lambda: pic("20250623_124027(1).jpg", "New: How it works", T, BR, focus=(0.5, 0.4)),
    },
    "x20261210": {
        1: lambda: pic("20250305_081450.jpg", "131°F for 3 days.", BR, focus=(0.5, 0.45), logo=True, size=84),
        3: lambda: pic("R5A_3985.jpg", "Then turn it.", G, focus=(0.62, 0.5), size=84),
    },
    "x20261215": {
        # brand-box layouts, as in feed_novdec.py: slide 3 is the `top` layout, slide 5 `cover`
        3: lambda: B.top(dict(heading="One farm that changes how it builds soil.", photo="IMG_2602.jpg",
                              credit=SFW, focus=(0.5, 0.45)), False, False),
        5: lambda: B.cover(dict(heading="Give before the year ends, link in bio.", photo="IMG_4524.jpg",
                                credit=SFW, focus=(0.5, 0.3)), False, True),
    },
    "x20261216": {
        3: lambda: pic("IMG_2717.jpg", "Zone 5", D, where="top", focus=(0.5, 0.6), size=80),
    },
}


OUT = os.environ.get("CB_OUT", B.OUT)  # a scratch folder for drafts


def out_path(pid, n):
    k = 1
    while True:
        p = os.path.join(OUT, f"{pid}-c{k}-{n}.jpg")
        if not os.path.exists(p):
            return p
        k += 1


if __name__ == "__main__":
    res = {}
    for pid in sys.argv[1:] or POSTS:
        for n, build in POSTS[pid].items():
            p = out_path(pid, n)
            build().convert("RGB").save(p, quality=88, optimize=True)
            res.setdefault(pid, {})[n] = "/wormhole/tiles/" + os.path.basename(p)
            print(p)
    json.dump(res, open(os.environ.get("CB_JSON", "/dev/null"), "w"), indent=1)
