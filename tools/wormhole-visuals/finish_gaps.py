"""Gap fills for 26 Oct to 31 Dec 2026 (26 Oct finishing pass): v2 photo-and-tag tiles.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/finish_gaps.py
    -> apps/web/public/wormhole/tiles/<id>-v2-<n>.jpg (never overwrites; bumps to v3, v4)
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boxes as B  # noqa: E402
import photo_first as PF  # noqa: E402

W, H = B.W, B.H
SFW = "Photo: Soil Food Web Foundation"
G, D, BR, T, BL, L, CRM = B.GREEN, B.DEEP, B.BROWN, B.TAN, B.BLUE, B.LIGHT, B.CREAM


def pic(photo, words=None, fill=D, ink=CRM, **kw):
    PF.CR.setdefault(photo, SFW)
    return PF.pic(photo, words, fill, ink, **kw)


def li(photo, words, fill=D, ink=CRM, focus=(0.5, 0.5)):
    PF.CR.setdefault(photo, SFW)
    return PF.li(photo, words, fill, ink, focus)


def cut(photo, words=None, fill=D, ink=CRM, where="bottom", logo=False, size=72, scale=1.0, y=0.42):
    """A microscopy cutout on its own black ground, shown whole (never cropped)."""
    c = Image.new("RGB", (W, H), (0, 0, 0))
    im = Image.open(os.path.join(B.SRC, photo)).convert("RGB")
    w = int(W * scale)
    h = int(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    c.paste(im, ((W - w) // 2, int(H * y - h / 2)))
    if words:
        PF.tag(c, words, fill, ink, where, size)
    PF.credit(c, SFW)
    if logo:
        B.logo(c, (W - 150, 40), size=90)
    return c


POSTS = {
    "d24": lambda: [
        (cut("uploads_2.png", "Read the drop.", G, logo=True, size=90, scale=1.15),
         "Read the drop."),
        (pic("sfw-amoeba-still-square.jpg", None, focus=(0.6, 0.5)),
         "Photo only: protozoa in a drop of soil water."),
        (cut("uploads_6.png", None, scale=0.92),
         "Photo only: a nematode."),
        (pic("hand-soil-roots-fungi.jpg", "Right at the root.", T, BR, focus=(0.45, 0.55)),
         "Predators turn bacterial nitrogen into ammonium, right at the root."),
    ],
    "d20": lambda: [
        (pic("hand-wet-dirt-worm.jpg", "Julia's worm bin.", BR, logo=True, focus=(0.55, 0.5), size=90),
         "\"Where Julia lives, green waste gets trucked away.\""),
    ],
    "p24": lambda: [
        (cut("uploads_7.png", "440 quintillion nematodes.", G, logo=True, size=80, scale=0.95),
         "440,000,000,000,000,000,000. Soil nematodes on Earth."),
        (pic("2-dirty-hands.jpg", None, focus=(0.5, 0.4)),
         "About 57 billion for every person alive."),
        (pic("harringtons-organic-land-care-brick-york-farms-2-768x1024.jpg", None, focus=(0.4, 0.6)),
         "Most feed on bacteria and fungi, cycling nutrients for plants."),
    ],
    "ev-01": lambda: [
        (li("erc-rancho-cacachilas-agro.jpg", "From surviving to thriving.", G, focus=(0.5, 0.6)),
         "From surviving to thriving: the case for soil health."),
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
