"""Save Soil shoutouts rebuilt with big text (Linnea, 31 Oct: everything to docs/slide-rules.md sizes).

Same content as savesoil.py, through the news card builder (news_cards.py): 84 px headlines, 52 px small text,
the italic green outlet tab. Long fact sentences are split into a headline and a detail line. The article photos
are cropped back out of the v2 tiles (savesoil.py's source folder is not on this machine), so every post keeps
its own photo. Instagram posts get v3 tiles; LinkedIn cards get v3 too.

  python3 tools/wormhole-visuals/ss_cards.py
"""
import os

import numpy as np
from PIL import Image

import news_cards as nc

nc.VERSION = "v3"
SRC = "consciousplanet.org/save-soil"


def ig_photo(pid):
    """The article photo on the v2 cover: find the cream card's top, take the photo above the old tab."""
    a = np.asarray(Image.open(os.path.join(nc.TILES, f"{pid}-v2-1.jpg")).convert("RGB")).astype(int)
    col = a[:, 150]
    cream = np.where((abs(col - [244, 241, 234]).sum(axis=1)) < 18)[0]
    cy0 = int(cream[0])
    return Image.fromarray(a[cy0 + 28:cy0 + 528 - 62, 168:912].astype("uint8"))


def li_photo(name):
    return Image.open(os.path.join(nc.TILES, name)).convert("RGB").crop((62, 62, 532, 508 - 56))


IG = {
    "ss-01": dict(seed=301, credit="Photo: Save Soil (Isha Foundation)",
                  headline="A coconut farm: 0.86% to 2.33% organic matter",
                  blurb="Save Soil's case study of Valluvan's farm in Tamil Nadu.",
                  facts=[("90-100 coconuts per tree, now 140", "Nothing changed in the first three years."),
                         ("Fertiliser: under 10%", "Of what he used to spend. Workers: 1, down from 10 to 20."),
                         ("1,200 mm of rain in days", "2018, after two years of drought."),
                         ("Wells 6 to 7 feet higher", "His neighbours' open wells stood 6 to 7 feet lower than his."),
                         ("What he did", "Leaf litter trenches between rows, mulch, layered crops, no burning, no "
                                         "summer ploughing.")]),
    "ss-02": dict(seed=302, credit="Photo: Donald Hobern, CC BY 2.0",
                  headline="5 numbers that show what soil life does",
                  blurb="From Save Soil's paper on soil and adaptation.",
                  facts=[("6x faster", "Water soaked into regenerative almond orchards 6 times faster. LaCanne et al. "
                                       "2021"),
                         ("133% more microbial carbon", "In regenerative organic soils. Mäder et al. 2025"),
                         ("2.4 to 13.5x more earthworms", "In diversified rotations than in rye monoculture. Bogušas "
                                                          "et al. 2022"),
                         ("+24% glomalin", "The fungal protein that glues soil crumbs together, under perennial "
                                           "pasture. Abán et al. 2025"),
                         ("+38 to 137% maize yield", "In drought years, in legume and manure systems. Lotter et al. "
                                                     "2003")]),
    "ss-05": dict(seed=305, credit="Photo: Lewis Fausak, CC BY-SA 4.0",
                  headline="Soil may be home to 59% of all life on Earth",
                  blurb="Anthony et al., PNAS 2023, via Save Soil.", facts=[]),
    "ss-06": dict(seed=306, credit="Photo: Marc-André Selosse, CC0",
                  headline="Your soil shapes your gut more than your genes",
                  blurb="From Save Soil's paper on soil and human health.",
                  facts=[("Baboons: soil beat genes 15x", "The soil around them shaped their gut microbes 15 times "
                                                          "more strongly than their genetics."),
                         ("Under 8% inherited", "Less than 8% of the human gut microbiome is inherited. Rothschild "
                                                "et al. 2018"),
                         ("Fungi carry minerals in", "Mycorrhizal fungi carry copper, iron, nitrogen, phosphorus and "
                                                     "zinc into crops."),
                         ("Rhizobia make plant food", "Bacteria in legume roots turn nitrogen from the air into "
                                                      "plant food.")]),
    "ss-08": dict(seed=308, credit="Photo: Antonio Jordán, CC BY-SA 3.0",
                  headline="Healthy soil cools the land",
                  blurb="From Save Soil's report \"The Soil Carbon Sponge\".",
                  facts=[("Water carries heat away", "Water in soil evaporates through plants and cools the land."),
                         ("Bare soil heats the air", "Degraded soil can't hold that water, so the sun heats the air "
                                                     "instead."),
                         ("Cover the ground", "Cover crops and mulch keep the ground from baking."),
                         ("Fungi hold the pores open", "Fungal threads and bacterial glues keep the sponge's pores "
                                                       "open.")]),
}
ISO = {"ss-01": "2026-11-20", "ss-02": "2026-11-22", "ss-05": "2026-11-08", "ss-06": "2026-11-24", "ss-08": "2026-11-19"}
END = ("Read the article", "From Save Soil (Isha Foundation). Link in bio.")

LI = {  # post id: (source tile, credit, headline, blurb)
    "ss-03": ("ss-03-v2-1.jpg", "Photo: High-Level Champions, CC BY 4.0",
              "USD 1 trillion for energy. USD 9 billion for agriculture.", "Save Soil's analysis of COP30."),
    "ss-04": ("ss-04-v2-1.jpg", "Photo: USDA NRCS, public domain",
              "Tilled soil released 21% more CO2", "In low-carbon soil, 29%. Abdalla et al. 2016, via Save Soil."),
    "ss-07": ("ss-07-v2-1.jpg", "Photo: Mclund, CC BY 4.0", "Soil is becoming security policy.",
              "\"Secure Soil, Save Life\", with IUCN WCEL and Save Soil."),
    "ss-01-li": ("ss-01-li-v1-1.jpg", "Photo: Save Soil (Isha Foundation)",
                 "A coconut farm: 0.86% to 2.33% organic matter", "Save Soil's case study of Valluvan's farm."),
    "ss-02-li": ("ss-02-li-v1-1.jpg", "Photo: Donald Hobern, CC BY 2.0", "5 numbers that show what soil life does",
                 "From Save Soil's paper on soil and adaptation."),
    "ss-05-li": ("ss-05-li-v1-1.jpg", "Photo: Lewis Fausak, CC BY-SA 4.0",
                 "Soil may be home to 59% of all life on Earth", "Anthony et al., PNAS 2023, via Save Soil."),
    "ss-06-li": ("ss-06-li-v1-1.jpg", "Photo: Marc-André Selosse, CC0",
                 "Where you live shapes your gut more than your genes", "From Save Soil's paper on soil and health."),
    "ss-08-li": ("ss-08-li-v1-1.jpg", "Photo: Antonio Jordán, CC BY-SA 3.0", "Healthy soil cools the land",
                 "From Save Soil's report \"The Soil Carbon Sponge\"."),
}

if __name__ == "__main__":
    for pid, p in IG.items():
        if os.path.exists(os.path.join(nc.TILES, f"{pid}-v3-1.jpg")):
            continue  # built already
        facts = p["facts"] + ([END] if p["facts"] else [])
        d = nc.instagram(pid, ISO[pid], f"{pid}-save-soil-shoutout",
                         [(ig_photo(pid), "Save Soil", p["credit"], p["headline"], p["blurb"], SRC)], facts,
                         seed=p["seed"])
        for k in range(1, d.n + 1):
            assert not os.path.exists(os.path.join(nc.TILES, f"{pid}-v3-{k}.jpg")), pid
        print(pid, d.save(nc.TILES, nc.DECKS)[0], d.pptx_name())
    for pid, (tile, credit, head, blurb) in LI.items():
        if os.path.exists(os.path.join(nc.TILES, f"{pid}-v3-1.jpg")):
            continue
        print(pid, nc.linkedin(pid, li_photo(tile), "Save Soil", credit, head, blurb, SRC,
                               seed=300 + len(pid)))
