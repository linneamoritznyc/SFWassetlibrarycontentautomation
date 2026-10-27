"""Catalog swap, worker C (27 Oct): new versions of repeated-photo slides, using fresh photos
from Linnea's SFW image catalog. Same tag words, colours, positions, logo and sizes as the
current v2/v3 tiles; only the photo changes. Writes <id>-c1-<n>.jpg (bumps to c2 if taken).

  BOX_SRC=<catalog photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/catalog_c.py [ids...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boxes as B  # noqa: E402
import photo_first as PF  # noqa: E402

SFW = "Photo: Soil Food Web Foundation"
G, D, BR, T, BL, L, P = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.PURPLE

PHOTOS = [
    "forest mycellium.jpg", "Cardboard trick for stacking buckets -IMG_5829.jpg", "20250304_130733.jpg",
    "20250624_170325(1).jpg", "IMG_4440.jpg", "20250620_153349.jpg", "PXL_20240725_141213340.jpg",
    "IMG_2538.jpg", "IMG_2598.jpg", "IMG_2579.jpg", "IMG_2733.jpg", "PXL_20251022_172210012.jpg",
    "20260303_180611.jpg", "IMG_5326.jpg", "20250626_093216.jpg", "IMG_2544.HEICmicroscopelearning.jpg",
    "20260225_081235.jpg", "IMG_20250626_100554.jpg", "IMG_0263.jpg", "IMG_3028.jpg",
    "20260224_094610.jpg", "Inspecting Feedstock 2.jpg", "PXL_20240712_183909990.jpg",
    "20250619_103110.jpg", "IMG_2640.jpg", "IMG_2632.jpg", "IMG_20250624_135155.jpg",
    "20250311_112453.jpg", "PXL_20251022_152058848.jpg", "20260304_161051.jpg", "20260304_132644.jpg",
    "Beginner microscopy group.jpg", "20260225_085308.jpg",
]
PF.CR.update({p: SFW for p in PHOTOS})
PF.CR["forest mycellium.jpg"] = "Photo: Aysen Ustunay"
pic = PF.pic

# Each post: {slide number: (image builder, slide text)}. Only swapped slides are listed.
POSTS = {
    "x20261224": lambda: {
        3: pic("forest mycellium.jpg", None, focus=(0.5, 0.55)),
    },
    "x20261226": lambda: {
        1: pic("Cardboard trick for stacking buckets -IMG_5829.jpg", "Plain paper: yes.", G, focus=(0.5, 0.5), logo=True),
        3: pic("20250304_130733.jpg", "Tear it small.", BL, focus=(0.5, 0.45)),
        4: pic("20250624_170325(1).jpg", None),
        5: pic("IMG_4440.jpg", "Glitter and foil: no.", P, focus=(0.72, 0.5)),
    },
    "x20261227": lambda: {
        1: pic("20250620_153349.jpg", "Chop and drop.", G, logo=True, size=90),
        3: pic("PXL_20240725_141213340.jpg", None, focus=(0.5, 0.45)),
    },
    "x20261229": lambda: {
        1: pic("IMG_2538.jpg", "2026 in soil science", D, logo=True, focus=(0.5, 0.5)),
        3: pic("IMG_2598.jpg", None, focus=(0.5, 0.6)),
        4: pic("IMG_2579.jpg", "More in 2027.", T, BR),
    },
    "x20261231": lambda: {
        1: pic("IMG_2733.jpg", "Happy New Year.", BR, logo=True, size=96, focus=(0.55, 0.5)),
        2: pic("PXL_20251022_172210012.jpg", "Costa Rica, January", L, D, focus=(0.6, 0.5)),
        3: pic("20260303_180611.jpg", "New Mexico, May", T, BR, focus=(0.5, 0.5)),
        4: pic("IMG_5326.jpg", "United Kingdom, September", BL, focus=(0.3, 0.5)),
    },
    "j20270103": lambda: {
        2: pic("20250626_093216.jpg", None, focus=(0.5, 0.35)),
        3: pic("IMG_2544.HEICmicroscopelearning.jpg", "Starts this month.", T, BR, focus=(0.5, 0.5)),
    },
    "j20270107": lambda: {
        1: pic("20260225_081235.jpg", "Does soil sleep in winter?", BR, logo=True, size=80, focus=(0.5, 0.5)),
        3: pic("IMG_20250626_100554.jpg", "Under the snow, it grows.", G, size=80, focus=(0.45, 0.66), zoom=2.0),
    },
    "j20270115b": lambda: {
        1: pic("IMG_0263.jpg", "Happy Pongal!", BR, logo=True, size=96, focus=(0.5, 0.45)),
    },
    "j20270118b": lambda: {
        1: pic("IMG_3028.jpg", "Foundation Courses", G, focus=(0.3, 0.5), logo=True, size=84),
    },
    "j20270121b": lambda: {
        1: pic("20260224_094610.jpg", "New Mexico, 3 to 14 May", T, BR, where="top", focus=(0.4, 0.5), size=72, logo=True),
        2: pic("Inspecting Feedstock 2.jpg", "Register your interest.", G, focus=(0.4, 0.5), size=72),
    },
    "j20270124": lambda: {
        2: pic("PXL_20240712_183909990.jpg", None, focus=(0.5, 0.35)),
        3: pic("20250619_103110.jpg", None, focus=(0.5, 0.45)),
        4: pic("IMG_2640.jpg", None, focus=(0.5, 0.5)),
        5: pic("IMG_2632.jpg", None, focus=(0.5, 0.5)),
    },
    "j20270125": lambda: {
        1: pic("IMG_20250624_135155.jpg", "Spores or hyphae?", BR, logo=True, size=90, focus=(0.5, 0.5), zoom=1.6),
    },
    "j20270126": lambda: {
        2: pic("20250311_112453.jpg", None, focus=(0.5, 0.45)),
    },
    "j20270127": lambda: {
        1: pic("PXL_20251022_152058848.jpg", "Produce no waste.", G, focus=(0.55, 0.5), logo=True, size=90),
    },
    "j20270128b": lambda: {
        1: pic("20260304_161051.jpg", "Build your piles.", BR, focus=(0.4, 0.5), logo=True, size=90),
        2: pic("20260304_132644.jpg", "Brew liquid amendments.", BL, focus=(0.65, 0.5), size=72),
        3: pic("Beginner microscopy group.jpg", "Microscopy at your level.", G, focus=(0.55, 0.5), size=84),
    },
    "j20270130": lambda: {
        3: pic("20260225_085308.jpg", "United States", BL, where="top", focus=(0.6, 0.5), size=90),
    },
}


def render(pid):
    out = {}
    for n, img in POSTS[pid]().items():
        v = 1
        while os.path.exists(os.path.join(PF.OUT, f"{pid}-c{v}-{n}.jpg")):
            v += 1
        name = f"{pid}-c{v}-{n}.jpg"
        img.save(os.path.join(PF.OUT, name), quality=88, optimize=True)
        out[n] = f"/wormhole/tiles/{name}"
    return out


if __name__ == "__main__":
    res = {pid: render(pid) for pid in (sys.argv[1:] or POSTS)}
    path = os.environ.get("CATALOG_C_JSON")
    if path:
        json.dump(res, open(path, "w"), indent=1)
    for k, v in res.items():
        print(k, v)
