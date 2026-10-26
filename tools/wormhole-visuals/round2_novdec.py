"""Round 2, Nov-Dec C (promo calendar and key dates, 26 Oct): v2 photo-and-tag tiles.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/round2_novdec.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v2-<n>.jpg (never overwrites; bumps to v3, v4)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boxes as B  # noqa: E402
import photo_first as PF  # noqa: E402

SFW = "Photo: Soil Food Web Foundation"
G, D, BR, T, BL, L, CRM = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.CREAM


def pic(photo, words=None, fill=D, ink=CRM, **kw):
    PF.CR.setdefault(photo, SFW)
    return PF.pic(photo, words, fill, ink, **kw)


def li(photo, words, fill=D, ink=CRM, focus=(0.5, 0.5)):
    PF.CR.setdefault(photo, SFW)
    return PF.li(photo, words, fill, ink, focus)


POSTS = {
    # Practicum 1: what it is and who it is for
    "k20261115": lambda: [
        (pic("w_cy-classes-3.jpg", "Complete Practicum", G, logo=True, focus=(0.5, 0.4), size=84),
         "The Soil Food Web Complete Practicum."),
        (pic("ctpfw-student-moving-compost-1.jpg", None, focus=(0.5, 0.45)),
         "Photo only: building a BioComplete™ compost pile."),
        (pic("w_test-tubes-with-sample.jpg", None, focus=(0.5, 0.5)),
         "Photo only: samples ready for the microscope."),
        (pic("hvdb-inplanten-002.jpg", "Your own land.", T, BR, focus=(0.45, 0.5)),
         "The Field Trial runs a full growing season on your own land. Link in bio."),
    ],
    # Acres U.S.A. Eco-Ag Conference, LinkedIn
    "k20261201": lambda: [
        (li("w_hand-of-compost.jpg", "Eco-Ag Conference, Iowa", G, focus=(0.5, 0.55)),
         "Eco-Ag Conference, Coralville, Iowa, 1 to 4 December."),
    ],
    # International Volunteer Day, Stories
    "k20261205": lambda: [
        (pic("w_workshop-group-around-compost-pile.jpg", "Thank you.", G, logo=True, focus=(0.5, 0.5), size=96),
         "Story frame 1: International Volunteer Day. Thank you."),
        (pic("w_2-dirty-hands.jpg", "Volunteer with us", BR, where="top", focus=(0.5, 0.45)),
         "Story frame 2: volunteer with us. Link sticker."),
    ],
    # Practicum 2: a graduate's field trial work
    "k20261207": lambda: [
        (pic("w_soil-sample-shovel-and-bag.jpg", "Field trials", BL, logo=True, focus=(0.6, 0.5), size=90),
         "Field trials: where the practicum meets your land."),
        (pic("w_soil-sample-close-up-test-tube.jpg", None, focus=(0.5, 0.5)),
         "Photo only: a soil sample going into a tube."),
        (pic("Sampling_equipment.jpg", "Treated vs control", T, BR, focus=(0.5, 0.5)),
         "Treated plots against control plots."),
    ],
    # UN International Year of the Woman Farmer
    "k20261218": lambda: [
        (pic("w_dora.jpg", "Year of the Woman Farmer", G, logo=True, focus=(0.5, 0.35), size=72),
         "2026 is the International Year of the Woman Farmer. Dora Tkalec, Finland."),
        (pic("uploads_Loida_Teaching_3.JPG", "Loida Vasquez", T, BR, where="top", focus=(0.45, 0.5)),
         "Loida Vasquez, Director of Advanced Education."),
        (pic("w_isadora.jpg", "Isadora Shmidt", D, where="top", focus=(0.75, 0.5)),
         "Isadora Shmidt, Soil Food Web Consultant and mentor."),
    ],
    # Practicum 3: last call before the year ends
    "k20261221": lambda: [
        (pic("uploads_MAR25_Group_Photo.jpg", "Start before 2027.", BR, where="top", logo=True, focus=(0.5, 0.5), size=90),
         "Start the Complete Practicum before 2027."),
        (pic("w_fungal-spores-in-suspension.jpg", "Link in bio.", G, focus=(0.5, 0.5)),
         "Your own mentor, from the first slide to the last trial. Link in bio."),
    ],
    # Kisan Diwas, India's National Farmers' Day
    "k20261223": lambda: [
        (pic("w_red-soil-hand.jpg", "Happy Kisan Diwas.", G, logo=True, focus=(0.5, 0.5), size=96),
         "Happy Kisan Diwas."),
        (pic("w_2-hands-clasped-holding-plant-roots.jpg", "Thank you, farmers.", T, BR, focus=(0.4, 0.5)),
         "Thank you to every farmer in India."),
    ],
}


def free_version(pid, n):
    v = 2
    while any(os.path.exists(os.path.join(B.OUT, f"{pid}-v{v}-{i}.jpg")) for i in range(1, n + 1)):
        v += 1
    return f"v{v}"


def render(pid):
    slides = POSTS[pid]()
    ver = free_version(pid, len(slides))
    out = []
    for i, (img, text) in enumerate(slides, 1):
        name = f"{pid}-{ver}-{i}.jpg"
        img.save(os.path.join(B.OUT, name), quality=88, optimize=True)
        out.append({"text": text, "image": f"/wormhole/tiles/{name}"})
    return out


if __name__ == "__main__":
    res = {pid: render(pid) for pid in (sys.argv[1:] or POSTS)}
    print(json.dumps(res, ensure_ascii=False, indent=1))
