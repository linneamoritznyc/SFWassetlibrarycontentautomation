"""Photo-first visuals: every slide is a real photo, edge to edge.

Linnea, 24 Oct: "Visual should be visual. As little text as possible and only picture."
So: no slide is ever type on a plain colour, no diagrams. A slide carries at most a few
words in one small solid tag, and most slides carry none. Everything else goes in the
caption.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/photo_first.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v2-<n>.jpg   (1080 x 1350, LinkedIn 1200 x 627)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageOps

import boxes as B

W, H = B.W, B.H
LW, LH = 1200, 627
OUT = B.OUT
VERSION = "v2"

CR = {
    "bacteria_gerri.jpg": "Photo: Gerri Gassert",
    "hypha_lee.jpg": "Photo: Lee Kirk",
    "nematode_sid.jpg": "Photo: Sid Jensen",
    "collembola.jpg": "Photo: Cameron Radman",
    "testate_luke.jpg": "Photo: Luke Hardy",
    "actino_ullens.jpg": "Photo: Rodrigue Ullens",
    "pl20261114-1.jpg": "Photo: Dan Keck, CC0",
    "pl20261114-2.jpg": "Photo: United Diversity, CC BY 2.0",
    "pl20261114-3.jpg": "Photo: Belbury, CC BY 4.0",
    "pl20261114-4.jpg": "Photo: Andy Wright, CC BY 2.0",
    "pl20261114-5.jpg": "Photo: Lance Cheung, USDA",
    "pl20261115-1.jpg": "Photo: Nicholas_T, CC BY 2.0",
    "pl20261115-2.jpg": "Photo: Nicholas_T, CC BY 2.0",
    "pl20261115-3.jpg": "Photo: Nicholas_T, CC BY 2.0",
    "pl20261115-4.jpg": "Photo: John Abrams, CC BY 4.0",
    "pl20261115-5.jpg": "Photo: Brett Ortler, CC BY 2.0",
}


def load(name, box, focus=(0.5, 0.5), zoom=1.0):
    im = Image.open(os.path.join(B.SRC, name)).convert("RGB")
    if zoom > 1:
        w, h = im.size
        cw, ch = int(w / zoom), int(h / zoom)
        x = int((w - cw) * focus[0])
        y = int((h - ch) * focus[1])
        im = im.crop((x, y, x + cw, y + ch))
    return ImageOps.fit(im, box, Image.LANCZOS, centering=focus)


def tag(c, words, fill, ink, where, size, margin=64):
    """A few words in one solid block. Never more than one block on a slide."""
    d = ImageDraw.Draw(c)
    f = B.head(size)
    width = c.width - 2 * margin - 72
    lines = B.wrap(d, words, f, width)
    lh = int(size * 1.14)
    tw = max(d.textlength(l, font=f) for l in lines)
    bw, bh = int(tw) + 72, lh * len(lines) + 56
    x = margin
    y = margin + 40 if where == "top" else c.height - margin - bh - 30
    d.rectangle((x, y, x + bw, y + bh), fill=fill)
    ty = y + 26
    for l in lines:
        top = d.textbbox((0, 0), l, font=f)[1]
        d.text((x + 36, ty - top + int(size * 0.06)), l, font=f, fill=ink)
        ty += lh


def credit(c, text):
    if not text:
        return
    d = ImageDraw.Draw(c)
    f = B.body(22)
    w = d.textlength(text, font=f)
    x, y = c.width - w - 30, c.height - 44
    d.rectangle((x - 10, y - 6, c.width - 20, y + 30), fill=B.DEEP)
    d.text((x, y), text, font=f, fill=B.CREAM)


def pic(photo, words=None, fill=B.DEEP, ink=B.CREAM, where="bottom", focus=(0.5, 0.5),
        zoom=1.0, size=72, logo=False, size_box=(W, H)):
    c = load(photo, size_box, focus, zoom)
    if words:
        tag(c, words, fill, ink, where, size)
    credit(c, CR.get(photo))
    if logo:
        B.logo(c, (c.width - 150, 40), size=90)
    return c


def li(photo, words, fill=B.DEEP, ink=B.CREAM, focus=(0.5, 0.5)):
    return pic(photo, words, fill, ink, "bottom", focus, size=54, logo=True, size_box=(LW, LH))


def duo(a, b, fa=(0.5, 0.5), fb=(0.5, 0.5), words=None, fill=B.DEEP, ink=B.CREAM):
    """Two photos stacked, hard edge between them. No text unless asked."""
    c = Image.new("RGB", (W, H), B.CREAM)
    c.paste(load(a, (W, H // 2 - 6), fa), (0, 0))
    c.paste(load(b, (W, H // 2 - 6), fb), (0, H // 2 + 6))
    if words:
        tag(c, words, fill, ink, "bottom", 64)
    cr = " / ".join(x for x in (CR.get(a), CR.get(b)) if x)
    credit(c, cr)
    return c


G, D, BR, T, BL, L, P, CRM = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.PURPLE, B.CREAM

# Each slide: (image builder, slide text shown in Wormhole)
POSTS = {
    "x20261108": lambda: [
        (pic("pl20261115-3.jpg", "Happy Diwali.", T, BR, logo=True, size=96), "Happy Diwali."),
    ],
    "x20261109": lambda: [
        (li("eden_forest.jpg", "COP31 opens today.", G), "COP31 opens today."),
    ],
    "w20261106": lambda: [
        (pic("rain_soil.jpg", "Real farms. Real soil.", D, logo=True), "Real farms. Real soil."),
        (pic("misting_pile.jpg", None, focus=(0.4, 0.4)), "Photo only: misting a compost pile."),
        (pic("extract_andrew.jpg", "New: Projects pages", T, BR, focus=(0.4, 0.5)), "Our new Projects pages."),
    ],
    "x20261117": lambda: [
        (pic("pdc_beds.jpg", "Earth care.", G, logo=True, size=90), "Earth care."),
        (pic("elaine_cr.jpg", "People care.", BL, where="top", focus=(0.45, 0.3), size=90), "People care."),
        (pic("pl20261114-5.jpg", "Fair share.", T, BR, size=90), "Fair share."),
    ],
    "x20261118": lambda: [
        (pic("misting_pile.jpg", "Compost Intensive Course", D, focus=(0.4, 0.4), logo=True), "Compost Intensive Course."),
        (pic("thermometer.jpg", None, focus=(0.5, 0.3)), "Photo only: thermometer in the pile."),
        (pic("testate_luke.jpg", None, focus=(0.6, 0.55), zoom=1.4), "Photo only: testate amoeba under the microscope."),
        (pic("pile_turn.jpg", "Starts January 2027.", T, BR), "Starts January 2027. Link in bio."),
    ],
    "ev-02": lambda: [
        (pic("bacteria_gerri.jpg", "100,000 soil samples.", BR, logo=True, size=80), "100,000 soil samples, one open atlas."),
        (pic("hypha_lee.jpg", None, focus=(0.6, 0.5)), "Photo only: fungal hypha."),
        (pic("rain_soil.jpg", "beopen.earth", G), "Explore it at beopen.earth"),
    ],
    "ar20261123": lambda: [
        (pic("elaine_cr.jpg", "Our first annual report", BR, focus=(0.45, 0.35), logo=True), "Our first annual report."),
        (pic("pile_turn.jpg", None), "Photo only: turning a pile at a workshop."),
        (pic("pdc_beds.jpg", "Coming soon.", T, BR, size=90), "Coming soon."),
    ],
    "x20261128": lambda: [
        (pic("extract_andrew.jpg", "Small Business Saturday", T, BR, focus=(0.4, 0.5), logo=True), "Small Business Saturday."),
        (pic("prework_extract.jpg", None, focus=(0.5, 0.6)), "Photo only: making an extract."),
        (pic("pile_turn.jpg", "Shop local for your soil.", D), "Shop local for your soil. Find a consultant, link in bio."),
    ],
    "x20261129": lambda: [
        (pic("eden_forest.jpg", "Trees grow better with friends.", G, logo=True), "Trees grow better with friends."),
        (pic("pdc_beds.jpg", None), "Photo only: mixed planting beds."),
        (pic("pl20261114-5.jpg", None), "Photo only: chard in straw mulch."),
    ],
    "x20261130": lambda: [
        (pic("thermometer.jpg", "10 weeks of compost.", G, focus=(0.5, 0.3), logo=True), "10 weeks of compost."),
        (pic("testate_luke.jpg", "Enroll now.", T, BR, focus=(0.6, 0.55)), "Enroll now, link in bio."),
    ],
    "x20261201": lambda: [
        (pic("elaine_garden.jpg", "GivingTuesday", G, focus=(0.4, 0.5), logo=True, size=90), "Today is GivingTuesday."),
        (pic("pdc_beds.jpg", None), "Photo only: garden beds."),
        (pic("extract_andrew.jpg", "Give a scholarship.", BR, focus=(0.4, 0.5)), "Give a scholarship, link in bio."),
    ],
    "x20261202": lambda: [
        (pic("rain_soil.jpg", "From shovel to slide.", BL, logo=True), "From shovel to slide."),
        (pic("prework_extract.jpg", None, focus=(0.5, 0.65)), "Photo only: mixing the sample with water."),
        (pic("extract_andrew.jpg", None, focus=(0.4, 0.5)), "Photo only: preparing the slide."),
        (pic("nematode_sid.jpg", None, focus=(0.35, 0.75)), "Photo only: a nematode under the microscope."),
    ],
    "x20261203": lambda: [
        (pic("elaine_cr.jpg", "Costa Rica, January", L, D, focus=(0.45, 0.35), logo=True), "Costa Rica, 18 to 29 January 2027."),
        (pic("eden_forest.jpg", None), "Photo only: Costa Rican forest."),
        (pic("pile_turn.jpg", None), "Photo only: turning a pile."),
        (pic("testate_luke.jpg", "Places still open.", BR, focus=(0.6, 0.55)), "Places still open, link in bio."),
    ],
    "x20261204": lambda: [
        (pic("collembola.jpg", "Wildlife under your feet.", P, logo=True), "Wildlife Conservation Day: meet the wildlife under your feet."),
        (pic("bacteria_gerri.jpg", "Bacteria", BR, where="top", size=64), "Bacteria."),
        (pic("hypha_lee.jpg", "Fungi", D, where="top", focus=(0.6, 0.5), size=64), "Fungi."),
        (pic("ciliates.jpg", "Protozoa", BL, where="top", size=64), "Protozoa."),
        (pic("nematode_sid.jpg", "Nematodes", G, where="top", focus=(0.35, 0.75), size=64), "Nematodes."),
    ],
    "w20261206": lambda: [
        (pic("pdc_beds.jpg", "Not sure where to start?", P, logo=True), "Not sure where to start?"),
        (pic("elaine_garden.jpg", None, focus=(0.4, 0.5)), "Photo only: Dr. Elaine in the garden."),
        (pic("extract_andrew.jpg", "Find your path.", G, focus=(0.4, 0.5)), "Find your path, link in bio."),
    ],
    "x20261208": lambda: [
        (pic("hypha_lee.jpg", "Who eats whom?", T, BR, focus=(0.6, 0.5), logo=True, size=90), "Who eats whom in your soil?"),
        (pic("bacteria_gerri.jpg", None), "Photo only: bacteria."),
        (pic("ciliates.jpg", None), "Photo only: protozoa."),
        (pic("nematode_sid.jpg", None, focus=(0.35, 0.75)), "Photo only: a nematode."),
        (pic("pl20261114-5.jpg", "And the plant eats.", G), "And the plant gets fed."),
    ],
    "w20261209": lambda: [
        (pic("hypha_lee.jpg", "How does soil work?", BL, focus=(0.6, 0.5), logo=True), "How does the soil food web work?"),
        (pic("nematode_sid.jpg", None, focus=(0.35, 0.75)), "Photo only: a nematode."),
        (pic("rain_soil.jpg", "New: How it works", T, BR), "Our new How it works page, link in bio."),
    ],
    "x20261210": lambda: [
        (pic("thermometer.jpg", "131°F for 3 days.", BR, focus=(0.5, 0.3), logo=True, size=84), "131°F (55°C) for three days."),
        (pic("misting_pile.jpg", None, focus=(0.4, 0.4)), "Photo only: misting the pile."),
        (pic("pile_turn.jpg", "Then turn it.", G, size=84), "Then turn it."),
    ],
    "w20261211": lambda: [
        (li("elaine_cr.jpg", "Dr. Elaine's research, searchable.", BR, focus=(0.45, 0.4)), "Four decades of Dr. Elaine Ingham's research, searchable."),
    ],
    "x20261213": lambda: [
        (pic("testate_luke.jpg", "It built its own house.", P, focus=(0.6, 0.55), zoom=1.3, logo=True), "This amoeba built its own house."),
        (pic("testate_luke.jpg", None, focus=(0.62, 0.55), zoom=2.2), "Photo only: the shell up close."),
        (pic("bacteria_gerri.jpg", None), "Photo only: bacteria, its food."),
    ],
    "x20261216": lambda: [
        (pic("pl20261114-4.jpg", "Permaculture zones", G, logo=True), "Permaculture zones."),
        (pic("pdc_beds.jpg", "Zone 1", T, BR, where="top", size=80), "Zone 1: herbs, salad, the compost bin."),
        (pic("pl20261115-2.jpg", "Zone 5", D, where="top", size=80), "Zone 5: left wild."),
    ],
    "x20261217": lambda: [
        (pic("rain_soil.jpg", "Nitrogen from thin air.", L, D, logo=True), "Nitrogen from thin air."),
        (pic("bacteria_gerri.jpg", None), "Photo only: bacteria."),
        (pic("pl20261114-5.jpg", "No bag required.", BR), "No bag required."),
    ],
    "x20261220": lambda: [
        (pic("pdc_beds.jpg", "Congratulations, PDC class of 2026", BR, logo=True), "Congratulations to our Permaculture Design Certificate class of 2026."),
        (pic("eden_forest.jpg", None), "Photo only: food forest."),
        (pic("elaine_garden.jpg", "Go build it.", G, focus=(0.4, 0.5), size=90), "Go build it."),
    ],
    "x20261224": lambda: [
        (pic("pl20261115-2.jpg", "Your tree has one more job.", G, logo=True), "Your Christmas tree has one more job."),
        (pic("feedstock_garden.jpg", "Chip it. Mulch it.", BR, focus=(0.5, 0.4)), "Chip it. Mulch it."),
        (pic("hypha_lee.jpg", None, focus=(0.6, 0.5)), "Photo only: the fungi it feeds."),
    ],
    "x20261226": lambda: [
        (pic("feedstock_garden.jpg", "Plain paper: yes.", G, focus=(0.5, 0.45), logo=True), "Can wrapping paper go in the compost? Plain paper: yes."),
        (pic("pile_turn.jpg", "Glitter and foil: no.", P), "Glossy, foil, glitter, tape: no."),
    ],
    "x20261227": lambda: [
        (pic("pl20261114-5.jpg", "Chop and drop.", G, logo=True, size=90), "Chop and drop."),
        (pic("pl20261114-1.jpg", None), "Photo only: leaves left where they fall."),
        (pic("hypha_lee.jpg", None, focus=(0.6, 0.5)), "Photo only: the fungi underneath."),
    ],
    "x20261229": lambda: [
        (pic("hypha_lee.jpg", "2026 in soil science", D, focus=(0.6, 0.5), logo=True), "2026 in soil science."),
        (pic("bacteria_gerri.jpg", None), "Photo only: bacteria."),
        (pic("rain_soil.jpg", None), "Photo only: no-till soil after rain."),
        (pic("pl20261115-1.jpg", "More in 2027.", T, BR), "Here's to more in 2027."),
    ],
    "x20261231": lambda: [
        (pic("pl20261115-3.jpg", "Happy New Year.", BR, logo=True, size=96), "Happy New Year from the soil."),
        (pic("elaine_cr.jpg", "Costa Rica, January", L, D, focus=(0.45, 0.35)), "Costa Rica, 18 to 29 January."),
        (pic("misting_pile.jpg", "New Mexico, May", T, BR, focus=(0.4, 0.4)), "New Mexico, 3 to 14 May."),
        (pic("pile_turn.jpg", "United Kingdom, September", BL), "United Kingdom, September."),
    ],
    "pl20261114": lambda: [
        (pic("pl20261114-1.jpg", "Make leaf mold.", BR, logo=True, size=90), "Your fallen leaves can become fungal compost."),
        (pic("pl20261114-2.jpg", None), "Photo only: wet leaves packed in a wire cage."),
        (pic("pl20261114-3.jpg", None), "Photo only: leaves breaking down."),
        (pic("pl20261114-4.jpg", None), "Photo only: finished leaf mold."),
        (pic("pl20261114-5.jpg", "Free mulch.", G, size=90), "Use it as mulch or in potting soil."),
    ],
    "pl20261115": lambda: [
        (pic("pl20261115-1.jpg", "Forests without earthworms?", D, logo=True), "Imagine a world without earthworms."),
        (pic("pl20261115-2.jpg", None), "Photo only: a northern forest."),
        (pic("pl20261115-4.jpg", None), "Photo only: an introduced earthworm."),
        (pic("pl20261115-5.jpg", "Right worm, wrong place.", T, BR), "Even a good organism can be the wrong one in the wrong place."),
    ],
    "p26": lambda: [
        (pic("pile_turn.jpg", "Welcome, new consultants.", BR, logo=True), "Welcome to our newest Certified Soil Food Web Consultants."),
        (pic("kyle.webp", "Kyle Babcock", G, focus=(0.62, 0.4), size=80), "Kyle Babcock, United States."),
    ],
}


def render(pid):
    out = []
    for i, (img, text) in enumerate(POSTS[pid](), 1):
        path = os.path.join(OUT, f"{pid}-{VERSION}-{i}.jpg")
        img.save(path, quality=88, optimize=True)
        out.append((text, f"/wormhole/tiles/{pid}-{VERSION}-{i}.jpg"))
    return out


if __name__ == "__main__":
    import json
    res = {pid: render(pid) for pid in (sys.argv[1:] or POSTS)}
    json.dump(res, open(os.environ.get("PF_JSON", "/dev/null"), "w"), ensure_ascii=False, indent=1)
    for k, v in res.items():
        print(k, len(v))
