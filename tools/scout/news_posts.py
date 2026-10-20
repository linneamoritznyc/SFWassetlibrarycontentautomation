"""Scout, step 3: the collage slides for each news post Scout drafted.

  python3 tools/scout/news_posts.py
    -> apps/web/public/wormhole/tiles/<id>-<n>.jpg
    -> tools/wormhole-visuals/out/decks/DD-MM-YYYY-<slug>.pptx

One function per story. The daily Scout run adds a function here for each
story it picks, then runs this file.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wormhole-visuals"))

from collage import CREAM, DEEP, H, KRAFT, W, Deck, cutout, gradient, hyphae, lens, paper, roots, soil  # noqa: E402
from posts import BUILDERS, MICRO, N, build, head, post, small  # noqa: E402


@post("n20261023a", "2026-10-23", "news-mustard-plant-fungus", 3)
def sheffield_fungus(d):
    # One soil profile running under all three slides: roots above, threads below.
    d.bg(None, gradient(W * 3, H, [(0, "#F4F1EA"), (0.52, "#EDE6D6"), (0.56, "#5B4434"), (1, "#3A2A20")], 231))
    d.put(0, "roots", roots(W * 3, 560, 31, color="#E9DCC3", n=14, width=3.2), W * 1.5, 1030, shadowed=False)
    d.put(0, "fungal-threads", hyphae(W * 3, 520, 32, color="#F4F1EA", n=22, width=1.8), W * 1.5, 1060, shadowed=False)
    d.put(0, "dark-soil", soil("dark-soil-clump", w=380), 860, 760)
    head(d, 0, "A plant everyone said lives without fungi just proved them wrong.", DEEP, y=120, size=92, h=420)
    small(d, 0, "University of Sheffield, Current Biology, October 2026", DEEP, 560, size=32)
    d.put(1, "micrograph-fungal-hypha", lens(N("Fungal hypha, 100x obj, Marco Trevisan.jpg"), 430), 820, 760)
    head(d, 1, "The fungus carried nitrogen and phosphorus into the plant.", DEEP, y=120, size=80, w=520, h=420)
    small(d, 1, "It took more than 260% more of the plant's carbon in return.", DEEP, 520, size=38, w=500)
    d.put(2, "moss", soil("moss-clump", w=330), 820, 760)
    d.put(2, "earthworm", soil("earthworm", h=240), 300, 1180, rot=-25)
    head(d, 2, "Mustards and their cabbage cousins were thought to skip this partnership.", DEEP, y=120, size=78, h=380)
    small(d, 2, "Next the team wants to know which crops do it too. Look closer, there is life.", DEEP, 520, size=38, w=620)
    d.logo(0, "br")
    d.logo(2, "br")


@post("n20261024a", "2026-10-24", "news-restored-land-soil-fungi", 3)
def flinders_restoration(d):
    # Above ground the planting looks finished; below, the fungal threads thin out to the right.
    d.bg(None, gradient(W * 3, H, [(0, "#DCE6D2"), (0.5, "#B9CBA4"), (0.53, "#4A382B"), (1, "#2C2119")], 241))
    for i, (x, w, nm) in enumerate([(230, 300, "moss-clump"), (860, 250, "fern-fiddlehead"), (1400, 300, "moss-clump"),
                                    (1990, 260, "fern-fiddlehead"), (2560, 300, "moss-clump"), (3010, 250, "fern-fiddlehead")]):
        d.put(0, f"planting-{i + 1}", soil(nm, w=w), x, 760)
    d.put(0, "fungal-threads-thick", hyphae(W, 560, 41, color="#F4F1EA", n=16, width=2.0), W * 0.5, 1050, shadowed=False)
    d.put(0, "fungal-threads-thin", hyphae(W, 560, 42, color="#F4F1EA", n=6, width=1.4), W * 1.5, 1050, shadowed=False)
    d.put(0, "fungal-threads-few", hyphae(W, 560, 43, color="#F4F1EA", n=2, width=1.2), W * 2.5, 1050, shadowed=False)
    d.put(0, "mushrooms", soil("mushrooms", w=260), 330, 1180)
    head(d, 0, "Restored land can look finished while the fungi below are still catching up.", DEEP, y=110, size=84, h=360)
    small(d, 0, "Flinders University, Molecular Ecology, October 2026", DEEP, 470, size=32)
    head(d, 1, "Over six years, what the fungi do in the soil kept recovering.", DEEP, y=110, size=84, h=360)
    small(d, 1, "The fungal community as a whole changed very little.", DEEP, 470, size=38)
    head(d, 2, "The team points to the farming history: soils still rich in leftover nutrients.", DEEP, y=110, size=80, h=380)
    small(d, 2, "Trees are the part of restoration we can count. The soil food web takes longer.", DEEP, 500, size=38, w=760)
    d.logo(0, "br")
    d.logo(2, "br")


if __name__ == "__main__":
    ids = sys.argv[1:] or [k for k in BUILDERS if k.startswith("n")]
    for pid in ids:
        build(pid)
        print(pid, "built")
