"""Mentor profile images in Linnea's final flower-frame design (her Tommy Tepper image, 30 Oct).

Starts from her Canva deck Mentor-Profile-Images-NoText (the flower frame), drops the top logo, moves and
scales the frame up to where it sits in her Tommy image, then makes one slide per mentor: their photo in
the frame, the name in EB Garamond italic (deep green), "Soil Food Web Mentor" in Montserrat Bold (Food
Web Green), and the logo bottom right. Every cutout, the photo, both texts and the logo stay their own layers.

  python3 tools/wormhole-visuals/mentor_frame.py <her no-text deck.pptx> <out.pptx>
"""
import copy
import io
import sys

from PIL import Image, ImageOps
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Pt

PX = 9525  # EMU per pixel; the deck is 1080 x 1350
ZIP = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/mentorzip"
SITE = "/home/user/linneamoritznyc/final-sfwsite-linnea/img/w"
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
SUB = "Soil Food Web Mentor"

MENTORS = [  # (post id, name, photo, vertical focus) in posting order
    ("p06", "Gerald Ramirez", f"{SITE}/gerald.jpg", 0.3),
    ("p03", "Nick Padwick", f"{SITE}/nick.jpg", 0.3),
    ("p09", "Dora Tkalec", f"{ZIP}/photo5.png", 0.35),
    ("d05", "Dr. Carla Portugal", f"{SITE}/carla.jpg", 0.3),
    ("p04", "Wes Sander", f"{SITE}/wes.jpg", 0.3),
    ("d11", "Brian Daubenspeck", f"{ZIP}/photo2.png", 0.3),
    ("p02", "Casey Williams", f"{ZIP}/photo1.png", 0.3),
    ("d12", "Delvin Solkinson", f"{ZIP}/photo3.png", 0.35),
    ("d13", "Tommy Tepper", f"{ZIP}/photo4.png", 0.35),
]

# Her Tommy image: the framed photo spans x 144 to 926, y 218 to 997 (the Canva deck had it at 172 to 907,
# 386 to 1133). One uniform scale about the frame centre keeps the cutouts undistorted.
SRC_BOX, DST_BOX = (172, 386, 907, 1133), (144, 218, 926, 997)
S = ((DST_BOX[2] - DST_BOX[0]) / (SRC_BOX[2] - SRC_BOX[0]) + (DST_BOX[3] - DST_BOX[1]) / (SRC_BOX[3] - SRC_BOX[1])) / 2
SRC_C = ((SRC_BOX[0] + SRC_BOX[2]) / 2, (SRC_BOX[1] + SRC_BOX[3]) / 2)
DST_C = ((DST_BOX[0] + DST_BOX[2]) / 2, (DST_BOX[1] + DST_BOX[3]) / 2)
BORDER, CREAM = 14, (251, 248, 241)
NAME_RGB, SUB_RGB = (0x22, 0x37, 0x1F), (0x15, 0x68, 0x26)
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R_EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"


def framed_photo(src, fy, w=734, h=747):
    """The mentor's photo cropped to the frame, inside the same thin cream border as Linnea's original."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    iw, ih = w - 2 * BORDER, h - 2 * BORDER
    s = max(iw / im.width, ih / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - iw) // 2, max(0, round((im.height - ih) * fy))
    out = Image.new("RGB", (w, h), CREAM)
    out.paste(im.crop((x, y, x + iw, y + ih)), (BORDER, BORDER))
    buf = io.BytesIO()
    out.save(buf, "JPEG", quality=92)
    buf.seek(0)
    return buf


def copy_slide(prs, src):
    """A new slide with every shape of src except the top logo, pictures re-linked to the same image parts."""
    new = prs.slides.add_slide(prs.slide_layouts[6])
    for shp in list(new.shapes):
        shp._element.getparent().remove(shp._element)
    rid_map = {rid: new.part.relate_to(rel.target_part, rel.reltype)
               for rid, rel in src.part.rels.items() if "image" in rel.reltype}
    for shp in src.shapes:
        if shp.name == "Group 2":  # the logo at the top; hers sits bottom right now
            continue
        el = copy.deepcopy(shp._element)
        for node in el.iter():
            if node.get(R_EMBED) in rid_map:
                node.set(R_EMBED, rid_map[node.get(R_EMBED)])
        new.shapes._spTree.append(el)
    return new


def move_up(slide):
    for shp in slide.shapes:
        x, y = shp.left / PX, shp.top / PX
        w, h = shp.width / PX, shp.height / PX
        nx = DST_C[0] + (x - SRC_C[0]) * S
        ny = DST_C[1] + (y - SRC_C[1]) * S
        shp.left, shp.top = Emu(round(nx * PX)), Emu(round(ny * PX))
        shp.width, shp.height = Emu(round(w * S * PX)), Emu(round(h * S * PX))


def text(slide, s, y, h, size, rgb, font, bold=False, italic=False):
    tb = slide.shapes.add_textbox(Emu(40 * PX), Emu(y * PX), Emu(760 * PX), Emu(h * PX))
    tb.name = s
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = s
    r.font.name, r.font.size, r.font.bold, r.font.italic = font, Pt(size * 0.75), bold, italic
    r.font.color.rgb = RGBColor(*rgb)


def main(deck, out):
    prs = Presentation(deck)
    base = prs.slides[0]
    for pid, name, photo, fy in MENTORS:
        sl = copy_slide(prs, base)
        move_up(sl)
        frame = next(s for s in sl.shapes if s.name == "Group 54").shapes[0]
        _, rid = sl.part.get_or_add_image_part(framed_photo(photo, fy))
        frame._element.find(f".//{A}blip").set(R_EMBED, rid)
        frame._element.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr").set(
            "descr", f"Photo: {name}")
        size = 104 if len(name) <= 16 else 88
        text(sl, name, 1118, 130, size, NAME_RGB, "EB Garamond", italic=True)
        text(sl, SUB, 1250, 50, 40, SUB_RGB, "Montserrat", bold=True)
        logo = Image.open(LOGO).convert("RGBA")
        buf = io.BytesIO()
        logo.save(buf, "PNG")
        buf.seek(0)
        pic = sl.shapes.add_picture(buf, Emu(826 * PX), Emu(1112 * PX), width=Emu(202 * PX))
        pic.name = "logo"
        sl.notes_slide.notes_text_frame.text = f"{name} ({pid}). Linnea's flower-frame design, from her Tommy Tepper image."
    first = prs.slides._sldIdLst[0]  # the original no-text slide
    prs.part.drop_rel(first.rId)
    prs.slides._sldIdLst.remove(first)
    prs.save(out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
