"""January A (1 to 15 January 2027): v2 photo-and-tag visuals.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/jan_a.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v2-<n>.jpg (1080 x 1350, LinkedIn 1200 x 627)

Never overwrites: if <id>-v2-<n>.jpg exists the whole post moves to v3, v4 and so on.
Prints the slide list as JSON (JAN_A_JSON=<path> to save it).
"""
import json
import os
import sys

from PIL import Image

import boxes as B
import photo_first as PF

SFW = "Photo: Soil Food Web Foundation"
FILM = "/home/claude/linneamoritznyc/final-sfwsite-linnea/img/video/790985081.jpg"

# Credits: the Foundation's own photos say so; Canva-licensed stock carries none.
PF.CR.update({
    "w_cy-workshop-8.jpg": SFW,
    "costa-rica-2025-gerald-liquid-amendments.jpg": SFW,
    "costa-rica-2025-microscopy-students-mentors.jpg": SFW,
    "wild-ken-hill_IMG_1493.jpg": SFW,
    "ctpfw-student-squeezing-compost-1.jpg": SFW,
    "w_test-tubes-with-sample.jpg": SFW,
    "uploads_2.png": SFW,
    "uploads_4.png": SFW,
    "w_evan.jpg": SFW,
    "w_stephanie.jpg": SFW,
    "w_sammie.jpg": SFW,
    "w_alex.jpg": SFW,
    "w_cy-classes-4.jpg": SFW,
    "erc-panchamana-treeplanting-2-fb-img-1666270988322.jpg": SFW,
    "erc-panchamana-garden.jpg": SFW,
    "w_erc-rancho-cacachilas-agro.jpg": SFW,
    "w_erc-rancho-cacachilas-agro2.jpg": SFW,
    "fungal-spores-in-suspension.jpg": SFW,
    "Elaine_Flower_Shirt_Microscope.png": SFW,
    "uploads_mar-group-photo-2.jpg": SFW,
    "uploads_mar25-group-photo.jpg": SFW,
    "w_pile-turning-wes-8-scaled.jpg": SFW,
    "uploads_testate-amoeba-(encysting),-40x-obj,-joy-kaluf.jpg": "Photo: Joy Kaluf",
    "uploads_webinar-preview-1.jpg": SFW,
    "uploads_webinar-preview-2.jpg": SFW,
    "w_img-1942-scaled.jpg": SFW,
    "w_workshop-group-around-compost-pile.jpg": SFW,
    "ctpfw-student-moving-compost-1.jpg": SFW,
    "w_sampling-equipment.jpg": SFW,
    "sfw-amoeba-still-square.jpg": SFW,
    "w_aug2023-workshop-group-7.jpg": SFW,
    "erc-panchamana-treeplanting-3-fb-img-1666271008784.jpg": SFW,
    "uploads_Loida_Teaching_3.JPG": SFW,
    "wild-ken-hill_IMG_1495.jpg": SFW,
    "fungi-in-under-grape-soil.jpg": SFW,
    "erc-rancho-cacachilas-agro8.jpg": SFW,
    "w_erc-rancho-cacachilas-aerial-2.jpg": SFW,
    "w_erc-rancho-cacachilas-aerial-shot.jpg": SFW,
    FILM: "Still: Roberto Silva case study film",
})

pic, li, duo, tag = PF.pic, PF.li, PF.duo, PF.tag
G, D, BR, T, BL, L, CRM = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.CREAM


def cutout(name, bg, words, fill, ink=CRM, where="bottom"):
    """A microscope cutout centred on a plain ground, the look the voice guide asks for."""
    c = Image.new("RGB", (B.W, B.H), bg)
    im = Image.open(os.path.join(B.SRC, name)).convert("RGBA")
    a = im.split()[3].point(lambda v: 255 if v > 200 else 0)
    im.putalpha(a)
    im = im.crop(a.getbbox())
    k = 880 / max(im.size)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    c.paste(im, ((B.W - im.width) // 2, (B.H - im.height) // 2 - 40), im)
    tag(c, words, fill, ink, where, 72)
    PF.credit(c, SFW)
    B.logo(c, (B.W - 150, 40), size=90)
    return c


def team(portrait, other, words, fill, ink=CRM, pfocus=(0.5, 0.35)):
    """Portrait on top, a second photo below, one tag. Keeps small portraits sharp enough."""
    c = Image.new("RGB", (B.W, B.H), CRM)
    c.paste(PF.load(portrait, (B.W, B.H // 2 + 120), pfocus), (0, 0))
    c.paste(PF.load(other, (B.W, B.H // 2 - 132)), (0, B.H // 2 + 132))
    tag(c, words, fill, ink, "bottom", 64)
    PF.credit(c, SFW)
    B.logo(c, (B.W - 150, 40), size=90)
    return c


POSTS = {
    "j20270101": lambda: [
        (pic("w_cy-workshop-8.jpg", "Welcome to 2027.", G, logo=True, size=90), "Welcome to 2027."),
        (pic("w_img-1942-scaled.jpg", "Three workshops in 2027", L, D), "Costa Rica in January, New Mexico in May, the United Kingdom in September."),
        (pic("wild-ken-hill_IMG_1493.jpg", None, focus=(0.5, 0.45)), "Photo only: building piles together at Wild Ken Hill, England."),
        (pic("w_workshop-group-around-compost-pile.jpg", "See you in the field.", T, BR), "See you in the field. All 2027 workshops, link in bio."),
    ],
    "j20270102": lambda: [
        (pic("erc-rancho-cacachilas-agro8.jpg", "Stay off wet beds.", BR, logo=True, size=84), "Stay off wet beds this weekend."),
        (pic("fungi-in-under-grape-soil.jpg", "Walk on boards or mulch.", G, focus=(0.4, 0.6)), "Walk on boards or a mulched path instead."),
    ],
    "j20270103": lambda: [
        (pic("ctpfw-student-squeezing-compost-1.jpg", "Compost Intensive Course", D, focus=(0.5, 0.4), logo=True), "Compost Intensive Course."),
        (pic("ctpfw-student-moving-compost-1.jpg", None, focus=(0.5, 0.4)), "Photo only: lifting finished compost at a workshop."),
        (pic("w_test-tubes-with-sample.jpg", "Starts this month.", T, BR), "The January cohort starts this month. Link in bio."),
    ],
    "j20270104": lambda: [
        (cutout("uploads_2.png", (255, 255, 255), "Meet the naked amoeba.", BL), "Meet the naked amoeba."),
        (cutout("uploads_2.png", CRM, "It eats bacteria.", G, where="top"), "It eats bacteria and releases ammonium by the roots."),
    ],
    "j20270105": lambda: [
        (team("w_evan.jpg", "erc-panchamana-treeplanting-2-fb-img-1666270988322.jpg", "Meet Evan Buckman", G), "Meet the team: Evan Buckman, Executive Director."),
    ],
    "j20270106": lambda: [
        (pic(FILM, "Soil Regenerators in the wild", D, focus=(0.42, 0.5), logo=True, size=64), "Soil Regenerators in the wild: Roberto Silva and consultant Miles Sorel, Piura, Peru."),
    ],
    "j20270107": lambda: [
        (pic("w_sampling-equipment.jpg", "Does soil sleep in winter?", BR, logo=True, size=80), "Myth: soil life sleeps all winter."),
        (pic("fungal-spores-in-suspension.jpg", None), "Photo only: life in a drop of soil water."),
        (pic("sfw-amoeba-still-square.jpg", "Under the snow, it grows.", G, size=80), "Under the snow, microbes keep growing."),
    ],
    "j20270108": lambda: [
        (team("w_stephanie.jpg", "w_aug2023-workshop-group-7.jpg", "Meet Stephanie McDaniel", BR), "Meet the team: Stephanie McDaniel, Director of Communications."),
    ],
    "j20270109a": lambda: [
        (pic("w_erc-rancho-cacachilas-agro.jpg", "Plan your cover crops.", G, logo=True, size=84), "Plan your cover crops this weekend."),
        (pic("w_erc-rancho-cacachilas-agro2.jpg", "Legumes add nitrogen.", T, BR), "Legumes add nitrogen."),
        (pic("w_erc-rancho-cacachilas-aerial-2.jpg", "Grasses hold on to it.", BL), "Grasses hold on to it. Mix both."),
    ],
    "j20270109b": lambda: [
        (li("Elaine_Flower_Shirt_Microscope.png", "10 billion microbes in one gram of soil", G, focus=(0.5, 0.3)), "About 10 billion microorganisms in one gram of soil."),
    ],
    "j20270110a": lambda: [
        (pic("erc-panchamana-garden.jpg", "Observe and interact.", D, logo=True, size=84), "Permaculture principle 1: observe and interact."),
        (pic("erc-panchamana-treeplanting-3-fb-img-1666271008784.jpg", "Watch first.", T, BR, size=90), "Watch first, then design."),
    ],
    "j20270110b": lambda: [
        (pic("uploads_mar25-group-photo.jpg", "One week to go.", G, logo=True, size=90), "Story frame 1: one week to go. Countdown sticker to 18 January."),
        (pic("w_pile-turning-wes-8-scaled.jpg", "Piles built by hand.", BR, focus=(0.5, 0.45)), "Story frame 2: piles built by hand."),
        (pic("uploads_testate-amoeba-(encysting),-40x-obj,-joy-kaluf.jpg", "Then under the microscope.", BL, where="top"), "Story frame 3: then under the microscope. Link sticker."),
    ],
    "j20270111": lambda: [
        (pic("costa-rica-2025-microscopy-students-mentors.jpg", "One week to go.", G, focus=(0.45, 0.5), logo=True, size=90), "One week to go."),
        (pic("costa-rica-2025-gerald-liquid-amendments.jpg", "18 to 29 January", T, BR, focus=(0.5, 0.4)), "18 to 29 January at Armonía. Link in bio."),
    ],
    "j20270112": lambda: [
        (pic("uploads_4.png", "1,000 to 1,000,000", BR, focus=(0.5, 0.5), zoom=1.2, logo=True, size=84), "Protozoa per teaspoon of soil: 1,000 to 1,000,000."),
        (pic("uploads_Loida_Teaching_3.JPG", "Per teaspoon of soil.", G), "Per teaspoon of soil. The more fertile the soil, the more protozoa."),
    ],
    "j20270113": lambda: [
        (team("w_sammie.jpg", "wild-ken-hill_IMG_1495.jpg", "Meet Sammie Bass", BL), "Meet the team: Sammie Bass, Marketing Associate."),
    ],
    "j20270114": lambda: [
        (pic("uploads_webinar-preview-1.jpg", "Free webinar", G, logo=True, size=90), "Free webinar this month."),
        (pic("uploads_webinar-preview-2.jpg", "One live hour.", T, BR, focus=(0.5, 0.6)), "One live hour online, free. Link in bio."),
    ],
    "j20270115": lambda: [
        (team("w_alex.jpg", "w_cy-classes-4.jpg", "Meet Alex Andreou", D), "Meet the team: Alex Andreou, IT Manager."),
    ],
}


def version(pid, n):
    v = 2
    while any(os.path.exists(os.path.join(PF.OUT, f"{pid}-v{v}-{i}.jpg")) for i in range(1, n + 1)):
        v += 1
    return f"v{v}"


def render(pid):
    slides = POSTS[pid]()
    v = version(pid, len(slides))
    out = []
    for i, (img, text) in enumerate(slides, 1):
        name = f"{pid}-{v}-{i}.jpg"
        path = os.path.join(PF.OUT, name)
        assert not os.path.exists(path)
        img.save(path, quality=88, optimize=True)
        out.append({"text": text, "image": f"/wormhole/tiles/{name}"})
    return out


if __name__ == "__main__":
    res = {pid: render(pid) for pid in (sys.argv[1:] or POSTS)}
    json.dump(res, open(os.environ.get("JAN_A_JSON", "/dev/null"), "w"), ensure_ascii=False, indent=1)
    for k, v in res.items():
        print(k, [s["image"] for s in v])
