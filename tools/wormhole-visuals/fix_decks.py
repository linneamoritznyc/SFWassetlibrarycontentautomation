"""Bring Linnea's Canva decks up to docs/slide-rules.md without changing her layout.

Sizes are measured against a 1080 px wide slide. Small text under 50 px goes to 52 px, headlines in
Pathway Gothic become Montserrat Bold, numbers in step circles go to 42 px, text boxes grow to fit,
and the dark logo on a colour box becomes the white logo.
  python3 fix_decks.py <in.pptx> <out.pptx>
"""
import copy
import sys

from pptx import Presentation
from pptx.util import Emu, Pt

WHITE_LOGO = "/home/user/SFWassetlibrarycontentautomation/apps/web/public/wormhole/brand/sfw-foundation-logo-white.png"


def main(src, dst):
    prs = Presentation(src)
    k = prs.slide_width / 1080  # EMU per slide pixel
    px = lambda pt: pt * 12700 / k  # noqa: E731  font pt -> px on a 1080 slide
    pt = lambda p: Pt(p * k / 12700)  # noqa: E731
    for slide in prs.slides:
        def walk(shapes):
            for sh in list(shapes):
                if sh.shape_type == 6:
                    walk(sh.shapes)
                    continue
                if sh.shape_type == 13 and "logo" in sh.name.lower():
                    behind = [b for b in slide.shapes if b.shape_type == 1 and b.left <= sh.left and b.top <= sh.top
                              and b.left + b.width >= sh.left + sh.width and b.top + b.height >= sh.top + sh.height]
                    dark = False
                    try:
                        c = slide.background.fill.fore_color.rgb
                        dark = (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000 < 140
                    except Exception:
                        pass
                    for b in behind:
                        try:
                            c = b.fill.fore_color.rgb
                            dark = (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000 < 140
                        except Exception:
                            pass
                    if dark:
                        new = slide.shapes.add_picture(WHITE_LOGO, sh.left, sh.top, width=sh.width)
                        new.name = "SFW logo"
                        sh._element.addprevious(new._element)
                        sh._element.getparent().remove(sh._element)
                    continue
                if not sh.has_text_frame or not sh.text_frame.text.strip():
                    continue
                grow = 1.0
                for para in sh.text_frame.paragraphs:
                    for r in para.runs:
                        if not r.font.size:
                            continue
                        s = px(r.font.size.pt)
                        name = r.font.name or ""
                        if name.startswith("Pathway"):
                            continue  # condensed labels stay as Linnea set them
                        elif sh.shape_type == 1 and s < 42:  # numbers in step circles
                            new = 42
                        elif s < 50:
                            new = 52
                        else:
                            continue
                        r.font.size = pt(new)
                        grow = max(grow, new / s)
                if grow > 1.0:
                    sh.text_frame.word_wrap = True
                    one_line = "\n" not in sh.text_frame.text and len(sh.text_frame.text) <= 14
                    if one_line and sh.shape_type == 17:  # short labels (55 to 68°C, Typical curve) widen instead of wrapping
                        extra = round(sh.width * (grow - 1)) + round(30 * k)
                        sh.left = Emu(max(0, sh.left - extra))
                        sh.width = Emu(sh.width + extra)
                        for b in slide.shapes:  # the colour box behind it widens with it
                            if b.shape_type == 1 and b is not sh and abs(b.top + b.height / 2 - (sh.top + sh.height / 2)) < b.height / 2 \
                                    and b.left <= sh.left + extra + 5 * k and b.left + b.width >= sh.left + sh.width - 5 * k \
                                    and b.width < sh.width + extra + 80 * k:
                                b.left = Emu(max(0, b.left - extra))
                                b.width = Emu(b.width + extra)
                    elif sh.shape_type == 17:
                        sh.height = Emu(round(sh.height * grow))
        walk(slide.shapes)
    prs.save(dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
