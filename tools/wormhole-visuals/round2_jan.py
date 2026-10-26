"""Round 2, January C (promo calendar and key dates, 26 Oct): v2 photo-and-tag tiles.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/round2_jan.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v2-<n>.jpg (1080 x 1350, LinkedIn 1200 x 627)

Never overwrites: if a name is taken the whole post moves to v3, v4 and so on.
No New Mexico photos exist in the photo set, so the New Mexico posts use close-ups and
microscopy that show no place. Swap in real Synergia Ranch photos when Evan sends them.
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boxes as B  # noqa: E402
import photo_first as PF  # noqa: E402

SFW = "Photo: Soil Food Web Foundation"
G, D, BR, T, BL, L, CRM = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.CREAM

PF.CR.update({
    "wild-ken-hill_IMG_1497.jpg": SFW,
    "Dr_Elaine_Ingham_with_Microscope.jpg": SFW,
    "uploads_testate-amoeba-40x.jpg": "Photo: Joy Kaluf",
    "erc-panchmana-treeplanting-fb-img-1666270907385.jpg": SFW,
    "Test_tubes_with_sample_.jpg": None,
    "uploads_mar-group-photo-2.jpg": SFW,
    "uploads_cy-classes(3).jpg": SFW,
    "w_hand-of-compost.jpg": None,
    "sfw-amoeba-still-wide.jpg": SFW,
    "red-soil-hand.jpg": None,
    "hand-wet-dirt-worm.jpg": None,
    "w_2-hands-clasped-holding-plant-roots.jpg": None,
    "uploads_webinar-preview-images-800-x-800.jpg": SFW,
    "erc-rancho-cacachilas-agro.jpg": SFW,
})
pic, li = PF.pic, PF.li


def cutout(name, bg, words, fill, ink=CRM, where="bottom", logo=False):
    """A microscope cutout centred on a plain ground (same look as jan_a.py)."""
    c = Image.new("RGB", (B.W, B.H), bg)
    im = Image.open(os.path.join(B.SRC, name)).convert("RGBA")
    a = im.split()[3].point(lambda v: 255 if v > 200 else 0)
    im.putalpha(a)
    im = im.crop(a.getbbox())
    k = 880 / max(im.size)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    c.paste(im, ((B.W - im.width) // 2, (B.H - im.height) // 2 - 40), im)
    PF.tag(c, words, fill, ink, where, 72)
    PF.credit(c, SFW)
    if logo:
        B.logo(c, (B.W - 150, 40), size=90)
    return c


WHITE = (255, 255, 255)

POSTS = {
    "j20270107b": lambda: [
        (li("red-soil-hand.jpg", "Following ORFC 2027", G), "Following the Oxford Real Farming Conference, 7 to 8 January."),
    ],
    "j20270110c": lambda: [
        (pic("wild-ken-hill_IMG_1497.jpg", "Last call.", G, focus=(0.5, 0.4), logo=True, size=96), "Last call: Compost Intensive Course."),
        (cutout("uploads_5.png", CRM, "Starts the week of 18 January.", BR), "Starts the week of 18 January. Link in bio."),
    ],
    "j20270115b": lambda: [
        (pic("w_2-hands-clasped-holding-plant-roots.jpg", "Happy Pongal!", BR, logo=True, size=96), "Happy Pongal to every farmer in Tamil Nadu."),
    ],
    "j20270118b": lambda: [
        (pic("Dr_Elaine_Ingham_with_Microscope.jpg", "Foundation Courses", G, focus=(0.5, 0.3), logo=True, size=84), "Foundation Courses: start any time."),
        (pic("uploads_testate-amoeba-40x.jpg", "Learn what lives here.", D, where="top", size=80), "Learn to identify bacteria, fungi, protozoa and nematodes."),
    ],
    "j20270119b": lambda: [
        (pic("erc-panchmana-treeplanting-fb-img-1666270907385.jpg", "New: Intro to Permaculture", D, focus=(0.5, 0.5), logo=True, size=76), "New: Intro to Permaculture Course, opens 1 February."),
    ],
    "j20270120b": lambda: [
        (li("hand-wet-dirt-worm.jpg", "Following EcoFarm 2027", BR, focus=(0.5, 0.5)), "Following the EcoFarm Conference, 20 to 23 January."),
    ],
    "j20270121b": lambda: [
        (cutout("uploads_7.png", CRM, "New Mexico, 3 to 14 May", T, BR, where="top", logo=True), "Accelerator Workshop New Mexico, 3 to 14 May 2027."),
        (cutout("uploads_1.png", WHITE, "Register your interest.", G), "Register your interest. Link in bio."),
    ],
    "j20270124b": lambda: [
        (li("uploads_cy-classes(3).jpg", "International Day of Education", BL, focus=(0.5, 0.3)), "International Day of Education, 24 January."),
    ],
    "j20270125b": lambda: [
        (pic("uploads_mar-group-photo-2.jpg", "10,000+ started here.", G, where="top", focus=(0.5, 0.5), logo=True, size=90), "More than 10,000 people in over 100 countries started here."),
        (pic("erc-rancho-cacachilas-agro.jpg", "Start any time.", BR, focus=(0.5, 0.5), size=90), "Start any time, at your own pace. Link in bio."),
    ],
    "j20270128b": lambda: [
        (pic("w_hand-of-compost.jpg", "Build your piles.", BR, logo=True, size=90), "Build, monitor and maintain your piles with a mentor."),
        (cutout("uploads_3.png", WHITE, "Brew liquid amendments.", BL), "Brew a variety of liquid amendments."),
        (pic("sfw-amoeba-still-wide.jpg", "Microscopy at your level.", G, size=84), "Microscopy sessions for beginner and advanced practitioners."),
    ],
    "j20270130b": lambda: [
        (pic("uploads_webinar-preview-images-800-x-800.jpg", "Happy Seed Swap Day!", G, logo=True, size=84), "Story frame 1: Happy National Seed Swap Day!"),
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
    path = os.environ.get("ROUND2_JAN_JSON")
    if path:
        json.dump(res, open(path, "w"), ensure_ascii=False, indent=1)
    for k, v in res.items():
        print(k, [s["image"] for s in v])
