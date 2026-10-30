"""Watercolor prompts for the 28 Oct redo (Stephanie: more texture and depth, editable in Canva).

  python3 tools/wormhole-visuals/wc_redo_prompts.py name-a name-b ...   -> /home/user/wc/gen/<name>.png
Variants are <base>-a, -b, -c, -d (at most 4 generations per illustration).
"""
import sys

import watercolor_gen as G

BASE = {
    # p20 Inside a compost pile, day by day
    "p20-pile": ("A large compost heap shown as a cut-away cross-section like a cake slice, filling the picture: "
                 "layers of green grass clippings, brown straw and dry leaves, a darker glowing warm orange-brown core "
                 "in the middle, a lighter cooler outer shell, wisps of steam rising from the top. Soft painted "
                 "shadow on the ground under it.", "4:5"),
    "p20-bacteria": ("Close-up cut-away of the inside of a compost heap: dark moist crumbly material and straw, a metal "
                     "compost thermometer with a round dial pushed in from the top, and a large round magnified circle "
                     "on one side showing many small rod-shaped and round bacteria, some dividing in two.", "4:5"),
    "p20-seeds": ("Cut-away of the hot core of a compost heap with steam rising, scattered small weed seeds in the "
                  "material, the seeds near the hot centre shrivelled, dark and cracked, a few seed heads of dandelion "
                  "and dock lying on top of the heap.", "4:5"),
    "p20-turn": ("A big rounded compost heap of straw, leaves and dark compost seen from the side, with a long wooden-handled "
                 "garden pitchfork with four long steel tines stuck into its outer edge, lifting a forkful of loose "
                 "steaming material over towards the top centre of the heap, loose crumbs and wisps of steam in the air, "
                 "soft painted shadow on the ground. No people, no hands.", "4:5"),
    "p20-fungi": ("Cut-away of a cooled, dark brown mature compost heap with fine white fungal threads spreading "
                  "through it, a few small brown mushrooms on the surface, and a large round magnified circle showing "
                  "a soft blob-shaped amoeba and a small flagellate with a whip-like tail.", "4:5"),
    "p20-hands": ("Two cupped hands holding a generous mound of dark, crumbly, finished compost with fine roots and a "
                  "small earthworm in it, crumbs falling between the fingers, soft painted shadow below.", "4:5"),
}

for name, (text, ratio) in BASE.items():
    for v in "abcd":
        G.PROMPTS[f"{name}-{v}"] = (text, ratio)

if __name__ == "__main__":
    import os
    os.makedirs(G.OUT, exist_ok=True)
    for n in sys.argv[1:]:
        print(*G.run(n))
