"""Picture-only looks to mix with photo_first.py, so neighbouring posts differ.

  clean   the photo alone, no words (logo only on a cover)
  mosaic  2x2 grid of photos with thin cream gutters, optional word tag
  stack   two photos, one above the other
  frame   a thick brand-colour frame around one photo, the words set in the frame
  circle  a full photo with a second photo (usually microscope) in a big circle

Linnea, 24 Oct: "why are all of these also in the same visual format?" -> mix them.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/photo_mix.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v4-<n>.jpg
"""
import os
import sys

from PIL import Image, ImageDraw

import boxes as B
import families as F
import photo_first as P
from photo_first import BL, BR, CR, D, G, L, P as PU, T, pic, load, tag, credit

W, H = B.W, B.H
VERSION = "v4"
GUT = 12


def clean(photo, focus=(0.5, 0.5), zoom=1.0, logo=False):
    return pic(photo, None, focus=focus, zoom=zoom, logo=logo)


def mosaic(photos, words=None, fill=D, ink=B.CREAM, logo=True, focus=None):
    c = Image.new("RGB", (W, H), B.CREAM)
    cw, ch = (W - GUT) // 2, (H - GUT) // 2
    focus = focus or [(0.5, 0.5)] * 4
    for i, ph in enumerate(photos):
        x, y = (i % 2) * (cw + GUT), (i // 2) * (ch + GUT)
        c.paste(load(ph, (cw, ch), focus[i]), (x, y))
    if words:
        tag(c, words, fill, ink, "bottom", 70)
    if logo:
        B.logo(c, (W - 150, 40), size=90)
    return c


def stack(a, b, words=None, fill=D, ink=B.CREAM, fa=(0.5, 0.5), fb=(0.5, 0.5), logo=True):
    c = Image.new("RGB", (W, H), B.CREAM)
    h = (H - GUT) // 2
    c.paste(load(a, (W, h), fa), (0, 0))
    c.paste(load(b, (W, h), fb), (0, h + GUT))
    if words:
        tag(c, words, fill, ink, "bottom", 70)
    if logo:
        B.logo(c, (W - 150, 40), size=90)
    return c


def frame(photo, words, ground, ink, focus=(0.5, 0.5), zoom=1.0, size=96, logo=True):
    """Thick brand-colour frame, photo filling most of it, words in the bottom band."""
    m, band = 56, 270
    c = Image.new("RGB", (W, H), ground)
    c.paste(load(photo, (W - 2 * m, H - m - band), focus, zoom), (m, m))
    d = ImageDraw.Draw(c)
    f = B.head(size)
    while d.textlength(words, font=f) > W - 2 * m - 170 and size > 56:
        size -= 4
        f = B.head(size)
    top = d.textbbox((0, 0), words, font=f)
    y = H - band + (band - (top[3] - top[1])) // 2 - top[1]
    d.text((m, y), words, font=f, fill=ink)
    if logo:
        B.logo(c, (W - m - 110, H - band + (band - 110) // 2), size=90)
    cr = CR.get(photo)
    if cr:
        d.text((m, H - 44), cr, font=B.body(22), fill=ink)
    return c


def circle(bg, inner, words=None, fill=D, ink=B.CREAM, fbg=(0.5, 0.5), fin=(0.5, 0.5), ring=B.CREAM, logo=True):
    c = load(bg, (W, H), fbg)
    disc = F.round_photo(os.path.join(B.SRC, inner), 720, fin, ring, 16)
    c.paste(disc, ((W - disc.width) // 2, 170), disc)
    if words:
        tag(c, words, fill, ink, "bottom", 72)
    credit(c, CR.get(inner))
    if logo:
        B.logo(c, (W - 150, 40), size=90)
    return c


MICRO4 = ["bacteria_gerri.jpg", "hypha_lee.jpg", "testate_luke.jpg", "ciliates.jpg"]

POSTS = {
    "w20261106": lambda: [
        (mosaic(["rain_soil.jpg", "misting_pile.jpg", "extract_andrew.jpg", "pile_turn.jpg"], "New: Projects pages", T, BR,
                focus=[(0.5, 0.5), (0.4, 0.4), (0.4, 0.5), (0.5, 0.5)]), "New: Projects pages."),
        (clean("rain_soil.jpg"), "Photo only: no-till soil after rain."),
        (pic("extract_andrew.jpg", "Real farms. Real soil.", D, focus=(0.4, 0.5)), "Real farms. Real soil."),
    ],
    "x20261108": lambda: [
        (frame("pl20261115-3.jpg", "Happy Diwali.", T, BR), "Happy Diwali."),
    ],
    "p26": lambda: [
        (frame("kyle.webp", "Welcome, Kyle.", G, B.CREAM, focus=(0.62, 0.4)), "Welcome to our newest Certified Soil Food Web Consultant, Kyle Babcock."),
        (clean("pile_turn.jpg"), "Photo only: a workshop turning a compost pile."),
    ],
    "pl20261114": lambda: [
        (clean("pl20261114-1.jpg", logo=True), "Photo only: fallen leaves. Your leaves can become fungal compost."),
        (pic("pl20261114-2.jpg", "Pack them in a cage.", BR), "Pack wet leaves into a wire cage or a bag with holes."),
        (clean("pl20261114-3.jpg"), "Photo only: leaves breaking down."),
        (clean("pl20261114-4.jpg"), "Photo only: finished leaf mold."),
        (pic("pl20261114-5.jpg", "Free mulch.", G, size=90), "Use it as mulch or in potting soil."),
    ],
    "pl20261115": lambda: [
        (mosaic(["pl20261115-1.jpg", "pl20261115-4.jpg", "pl20261115-2.jpg", "pl20261115-5.jpg"], "Forests without earthworms?", D), "Imagine a world without earthworms."),
        (clean("pl20261115-2.jpg"), "Photo only: a northern forest."),
        (clean("pl20261115-4.jpg"), "Photo only: an introduced earthworm."),
        (pic("pl20261115-3.jpg", "Right worm, wrong place.", T, BR), "Even a good organism can be the wrong one in the wrong place."),
    ],
    "x20261117": lambda: [
        (frame("pdc_beds.jpg", "Earth care.", G, B.CREAM), "Earth care."),
        (frame("elaine_cr.jpg", "People care.", BL, B.CREAM, focus=(0.45, 0.3)), "People care."),
        (frame("pl20261114-5.jpg", "Fair share.", T, BR), "Fair share."),
    ],
    "x20261118": lambda: [
        (stack("misting_pile.jpg", "testate_luke.jpg", "Compost Intensive Course", D, fa=(0.4, 0.35), fb=(0.6, 0.55)), "Compost Intensive Course."),
        (clean("thermometer.jpg", focus=(0.5, 0.3)), "Photo only: thermometer in the pile."),
        (pic("pile_turn.jpg", "Starts January 2027.", T, BR), "Starts January 2027. Link in bio."),
    ],
    "ev-02": lambda: [
        (mosaic(MICRO4, "100,000 soil samples.", BR), "100,000 soil samples, one open atlas."),
        (clean("hypha_lee.jpg", focus=(0.6, 0.5)), "Photo only: fungal hypha."),
        (pic("rain_soil.jpg", "beopen.earth", G), "Explore it at beopen.earth"),
    ],
    "ar20261123": lambda: [
        (frame("elaine_cr.jpg", "Our first annual report", BR, B.CREAM, focus=(0.45, 0.35), size=80), "Our first annual report."),
        (clean("pile_turn.jpg"), "Photo only: turning a pile at a workshop."),
        (pic("pdc_beds.jpg", "Coming soon.", T, BR, size=90), "Coming soon."),
    ],
    "x20261129": lambda: [
        (clean("eden_forest.jpg", logo=True), "Photo only: a food forest. Trees grow better with friends."),
        (stack("pdc_beds.jpg", "pl20261114-5.jpg", "Trees grow better with friends.", G), "Trees grow better with friends."),
    ],
    "x20261130": lambda: [
        (circle("pile_turn.jpg", "testate_luke.jpg", "10 weeks of compost.", G, fin=(0.6, 0.55)), "10 weeks of compost and microscope work."),
        (pic("thermometer.jpg", "Enroll now.", T, BR, focus=(0.5, 0.3)), "Enroll now, link in bio."),
    ],
    "x20261201": lambda: [
        (frame("elaine_garden.jpg", "GivingTuesday", G, B.CREAM, focus=(0.4, 0.5)), "Today is GivingTuesday."),
        (clean("pdc_beds.jpg"), "Photo only: garden beds."),
        (pic("extract_andrew.jpg", "Give a scholarship.", BR, focus=(0.4, 0.5)), "Give a scholarship, link in bio."),
    ],
    "x20261202": lambda: [
        (mosaic(["rain_soil.jpg", "prework_extract.jpg", "extract_andrew.jpg", "nematode_sid.jpg"], "From shovel to slide.", BL,
                focus=[(0.5, 0.5), (0.5, 0.65), (0.4, 0.5), (0.35, 0.75)]), "From shovel to slide."),
        (clean("prework_extract.jpg", focus=(0.5, 0.65)), "Photo only: mixing the sample with water."),
        (clean("nematode_sid.jpg", focus=(0.35, 0.75)), "Photo only: a nematode under the microscope."),
    ],
    "x20261204": lambda: [
        (circle("rain_soil.jpg", "collembola.jpg", "Wildlife under your feet.", PU), "Wildlife Conservation Day: meet the wildlife under your feet."),
        (pic("bacteria_gerri.jpg", "Bacteria", BR, where="top", size=64), "Bacteria."),
        (pic("hypha_lee.jpg", "Fungi", D, where="top", focus=(0.6, 0.5), size=64), "Fungi."),
        (pic("ciliates.jpg", "Protozoa", BL, where="top", size=64), "Protozoa."),
        (pic("nematode_sid.jpg", "Nematodes", G, where="top", focus=(0.35, 0.75), size=64), "Nematodes."),
    ],
    "w20261206": lambda: [
        (stack("pdc_beds.jpg", "elaine_garden.jpg", "Not sure where to start?", PU, fb=(0.4, 0.3)), "Not sure where to start?"),
        (pic("extract_andrew.jpg", "Find your path.", G, focus=(0.4, 0.5)), "Find your path, link in bio."),
    ],
    "x20261208": lambda: [
        (frame("hypha_lee.jpg", "Who eats whom?", T, BR, focus=(0.6, 0.5)), "Who eats whom in your soil?"),
        (clean("bacteria_gerri.jpg"), "Photo only: bacteria."),
        (clean("ciliates.jpg"), "Photo only: protozoa."),
        (clean("nematode_sid.jpg", focus=(0.35, 0.75)), "Photo only: a nematode."),
        (pic("pl20261114-5.jpg", "And the plant eats.", G), "And the plant gets fed."),
    ],
    "x20261210": lambda: [
        (circle("misting_pile.jpg", "thermometer.jpg", "131°F for 3 days.", BR, fbg=(0.4, 0.4), fin=(0.5, 0.3)), "131°F (55°C) for three days."),
        (pic("pile_turn.jpg", "Then turn it.", G, size=84), "Then turn it."),
    ],
    "x20261213": lambda: [
        (clean("testate_luke.jpg", focus=(0.62, 0.55), zoom=2.2, logo=True), "Photo only: a testate amoeba, which built its own house."),
        (pic("testate_luke.jpg", "It built its own house.", PU, focus=(0.6, 0.55), zoom=1.3), "This amoeba built its own house."),
        (clean("bacteria_gerri.jpg"), "Photo only: bacteria, its food."),
    ],
    "x20261216": lambda: [
        (mosaic(["pl20261114-4.jpg", "pdc_beds.jpg", "eden_forest.jpg", "pl20261115-2.jpg"], "Permaculture zones", G), "Permaculture zones."),
        (pic("pdc_beds.jpg", "Zone 1", T, BR, where="top", size=80), "Zone 1: herbs, salad, the compost bin."),
        (pic("pl20261115-2.jpg", "Zone 5", D, where="top", size=80), "Zone 5: left wild."),
    ],
    "x20261220": lambda: [
        (frame("pdc_beds.jpg", "Congrats, PDC class of 2026", BR, B.CREAM, size=72), "Congratulations to our Permaculture Design Certificate class of 2026."),
        (clean("eden_forest.jpg"), "Photo only: food forest."),
        (pic("elaine_garden.jpg", "Go build it.", G, focus=(0.4, 0.5), size=90), "Go build it."),
    ],
    "x20261224": lambda: [
        (stack("pl20261115-2.jpg", "feedstock_garden.jpg", "Your tree has one more job.", G, fb=(0.5, 0.4)), "Your Christmas tree has one more job."),
        (pic("feedstock_garden.jpg", "Chip it. Mulch it.", BR, focus=(0.5, 0.4)), "Chip it. Mulch it."),
        (clean("hypha_lee.jpg", focus=(0.6, 0.5)), "Photo only: the fungi it feeds."),
    ],
    "x20261227": lambda: [
        (clean("pl20261114-5.jpg", logo=True), "Photo only: chard in straw mulch. Chop and drop."),
        (pic("pl20261114-1.jpg", "Chop and drop.", G, size=90), "Chop and drop."),
        (clean("hypha_lee.jpg", focus=(0.6, 0.5)), "Photo only: the fungi underneath."),
    ],
    "x20261229": lambda: [
        (mosaic(MICRO4[::-1], "2026 in soil science", D), "2026 in soil science."),
        (clean("rain_soil.jpg"), "Photo only: no-till soil after rain."),
        (pic("pl20261115-1.jpg", "More in 2027.", T, BR), "Here's to more in 2027."),
    ],
    "x20261231": lambda: [
        (frame("pl20261115-3.jpg", "Happy New Year.", BR, B.CREAM), "Happy New Year from the soil."),
        (pic("elaine_cr.jpg", "Costa Rica, January", L, D, focus=(0.45, 0.35)), "Costa Rica, 18 to 29 January."),
        (pic("misting_pile.jpg", "New Mexico, May", T, BR, focus=(0.4, 0.4)), "New Mexico, 3 to 14 May."),
        (pic("pile_turn.jpg", "United Kingdom, September", BL), "United Kingdom, September."),
    ],
}


if __name__ == "__main__":
    import json
    P.POSTS = POSTS
    P.VERSION = VERSION
    res = {pid: P.render(pid) for pid in (sys.argv[1:] or POSTS)}
    json.dump(res, open(os.environ.get("PF_JSON", "/dev/null"), "w"), ensure_ascii=False, indent=1)
    print(len(res))
