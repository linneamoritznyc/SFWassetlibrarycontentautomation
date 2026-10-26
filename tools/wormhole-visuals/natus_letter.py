"""k20261120: a letter from Natus Rattanaphokil, Southern Thailand (v2 photo-and-tag).

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/natus_letter.py
    -> apps/web/public/wormhole/tiles/k20261120-v2-<n>.jpg
"""
import os

import boxes as B
import photo_first as PF

PF.CR.update({
    "w_dr-elaine-ingham-with-microscope.jpg": "Photo: Soil Food Web Foundation",
    "w_2-hands-clasped-holding-plant-roots.jpg": "Photo: Soil Food Web Foundation",
    "w_hand-soil-roots-fungi.jpg": "Photo: Soil Food Web Foundation",
})

SLIDES = [
    lambda: PF.pic("w_dr-elaine-ingham-with-microscope.jpg", "A letter for Dr. Elaine.",
                   B.PURPLE, B.CREAM, logo=True, size=72),
    lambda: PF.pic("w_2-hands-clasped-holding-plant-roots.jpg",
                   "“Every ecological piece instantly fell into place.”",
                   B.GREEN, B.CREAM, size=62),
    lambda: PF.pic("w_hand-soil-roots-fungi.jpg"),
]


def out(n):
    v = 2
    while True:
        p = os.path.join(B.OUT, f"k20261120-v{v}-{n}.jpg")
        if not os.path.exists(p):
            return p
        v += 1


for i, make in enumerate(SLIDES, 1):
    path = out(i)
    make().convert("RGB").save(path, quality=90)
    print(path)
