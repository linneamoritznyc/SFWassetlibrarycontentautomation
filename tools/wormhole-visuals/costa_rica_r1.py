"""Costa Rica posts, round 1 rebuild (27 Oct): new proposals for every Costa Rica carousel and story.

Linnea rejected the deck look (Fredoka, big flat colour blocks, flower cutouts). New rules:
every slide is a real Costa Rica photo, edge to edge, that shows what the slide says. Text sits in
ONE flat brand-colour box with hard edges over the photo (trifold style), under ~20% of the frame,
never over a face. Montserrat 800 headline, Pathway Gothic One caps label, Source Sans 3 small line.
Cream box with Soil Brown text, or Food Web Green / Soil Brown box with cream text. Logo small,
slide 1 only, inside the cream box. Box position varies slide to slide.

  BOX_SRC=<catalog photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/costa_rica_r1.py
    -> apps/web/public/wormhole/tiles/<id>-r1-<n>.jpg  (never overwrites)
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.environ.get("R1_OUT") or os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
LOGO = os.path.join(REPO, "apps", "web", "public", "wormhole", "sfw-foundation-wordmark-240.png")
SRC = os.environ["BOX_SRC"]
FONTS = os.environ["SFW_FONTS"]

CREAM = (0xF4, 0xF1, 0xEA)
BROWN = (0x4F, 0x34, 0x33)
GREEN = (0x15, 0x68, 0x26)
# box colour -> (headline/small text colour, label colour)
INK = {"cream": (BROWN, GREEN), "green": (CREAM, CREAM), "brown": (CREAM, CREAM)}
FILL = {"cream": CREAM, "green": GREEN, "brown": BROWN}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


HEAD = lambda s: font("montserrat-latin-800-normal.woff2", s)
LABEL = lambda s: font("pathway-gothic-one-latin-400-normal.woff2", s)
SMALL = lambda s: font("source-sans-3-latin-400-normal.woff2", s)


def cover(name, W, H, focus=(0.5, 0.5), zoom=1.0):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, name))).convert("RGB")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - W) * focus[0])
    y = round((im.height - H) * focus[1])
    return im.crop((x, y, x + W, y + H))


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(spec, W, H):
    c = cover(spec["photo"], W, H, spec.get("focus", (0.5, 0.5)), spec.get("zoom", 1.0))
    d = ImageDraw.Draw(c)
    story = H > 1500
    pad = 40 if not story else 46
    maxw = spec.get("w", 600 if not story else 700)
    hs = spec.get("hs", 64 if not story else 74)
    fh, fl, fs = HEAD(hs), LABEL(40 if not story else 46), SMALL(32 if not story else 38)
    ink, lab = INK[spec["box"]]
    inner = maxw - 2 * pad
    hl = wrap(d, spec["head"], fh, inner)
    sl = wrap(d, spec["small"], fs, inner) if spec.get("small") else []
    lab_txt = spec.get("label")
    lg = None
    if spec.get("logo"):
        lg = Image.open(LOGO).convert("RGBA")
        lg = lg.resize((150, round(150 * lg.height / lg.width)), Image.LANCZOS)
    # measure
    lh_h = round(hs * 1.12)
    content_w = max([d.textlength(t, font=fh) for t in hl] + [d.textlength(t, font=fs) for t in sl]
                    + ([d.textlength(lab_txt.upper(), font=fl) + 2 * len(lab_txt)] if lab_txt else [0])
                    + ([lg.width] if lg else [0]))
    bw = round(content_w + 2 * pad)
    bh = pad
    if lg:
        bh += lg.height + 22
    if lab_txt:
        bh += (40 + 16) if not story else (46 + 18)
    bh += lh_h * len(hl)
    if sl:
        bh += 16 + round(fs.size * 1.25) * len(sl)
    bh += pad - round(hs * 0.12)
    # place
    m = spec.get("margin", 56 if not story else 64)
    top = 260 if story else m
    bottom = 1600 if story else H - m
    pos = spec["pos"]
    x = m if "l" in pos else (W - m - bw if "r" in pos else (W - bw) // 2)
    if pos[0] == "t":
        y = top + spec.get("dy", 0)
    elif pos[0] == "b":
        y = bottom - bh - spec.get("dy", 0)
    else:
        y = (top + bottom - bh) // 2 + spec.get("dy", 0)
    d.rectangle((x, y, x + bw, y + bh), fill=FILL[spec["box"]])
    cy = y + pad
    if lg:
        c.paste(lg, (x + pad, cy), lg)
        cy += lg.height + 22
    if lab_txt:
        tx = x + pad
        for ch in lab_txt.upper():
            d.text((tx, cy - 6), ch, font=fl, fill=lab)
            tx += d.textlength(ch, font=fl) + 2
        cy += (40 + 16) if not story else (46 + 18)
    for t in hl:
        d.text((x + pad, cy - round(hs * 0.06)), t, font=fh, fill=ink)
        cy += lh_h
    if sl:
        cy += 16
        for t in sl:
            d.text((x + pad, cy), t, font=fs, fill=ink)
            cy += round(fs.size * 1.25)
    area = bw * bh / (W * H)
    if story:
        assert y >= 260 and y + bh <= 1600, (spec, y, bh)
    return c, area, (x, y, bw, bh)


def out_path(pid, n):
    p = os.path.join(OUT, f"{pid}-r1-{n}.jpg")
    if os.path.exists(p) and not os.environ.get("R1_REDO"):
        raise SystemExit(f"exists, not overwriting: {p}")
    return p


def main():
    specs = json.load(open(os.path.join(HERE, "costa_rica_r1.json")))
    only = sys.argv[1:]
    for pid, slides in specs.items():
        if only and pid not in only:
            continue
        W, H = (1080, 1920) if pid.startswith("st") else (1080, 1350)
        for n, s in enumerate(slides, 1):
            img, area, box = render(s, W, H)
            p = out_path(pid, n)
            img.save(p, quality=90)
            flag = "  BOX TOO BIG" if area > 0.2 else ""
            print(f"{pid}-r1-{n}  box {box}  {area:.1%}{flag}")


if __name__ == "__main__":
    main()
