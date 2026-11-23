import copy
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.enum.text import MSO_AUTO_SIZE, MSO_ANCHOR
from PIL import ImageFont
SRC = "/root/.claude/uploads/aa85d233-831d-5e12-bf14-2ae561c4274c/ebdaf407-23-11-2026-cic-student-voices-v23_1.pptx.pptx"
OUT = "23-11-2026-cic-student-voices-v24.pptx"
F = "fonts/SourceSans3.ttf"
PX = 9525                                    # EMU per px (1080 px slide)
p = Presentation(SRC)

def lines(text, size, width):
    f = ImageFont.truetype(F, size)
    n = 0
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if f.getlength(t) <= width:
                cur = t
            else:
                n += 1; cur = w
        n += 1
    return n

for i, s in enumerate(p.slides):
    if i == 0:
        continue
    shapes = list(s.shapes)
    panel = shapes[1]
    q = next(sh for sh in shapes if sh.has_text_frame and sh.text_frame.text.startswith("“"))
    nm = next(sh for sh in shapes if sh.has_text_frame and sh.text_frame.text.startswith("–"))
    text = q.text_frame.text
    top = q.top // PX
    bottom = (panel.top + panel.height) // PX - 70
    avail = bottom - top
    width = q.width // PX * 0.93              # wrap as if 7% narrower: Canva's text runs wider
    name_px = 52
    for size in range(54, 41, -1):            # px; never below 42
        need = lines(text, size, width) * size * 1.22 + 34 + name_px * 1.2
        if need <= avail:
            break
    # name becomes a second paragraph in the quote box, so they can never overlap
    tf = q.text_frame
    for para in tf.paragraphs:
        para.line_spacing = Pt(size * 0.75 * 1.22)
        for r in para.runs:
            r.font.size = Pt(size * 0.75)
    nrun = nm.text_frame.paragraphs[0].runs[0]
    np_ = tf.add_paragraph()
    np_.space_before = Pt(26)
    np_.line_spacing = Pt(name_px * 0.75 * 1.2)
    r = np_.add_run(); r.text = nm.text_frame.text
    r.font.size = Pt(name_px * 0.75); r.font.bold = True; r.font.name = nrun.font.name or "Montserrat"
    try:
        r.font.color.rgb = nrun.font.color.rgb
    except Exception:
        pass
    nm._element.getparent().remove(nm._element)
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = MSO_ANCHOR.TOP
    q.height = Emu(avail * PX)
    q.name = "Quote and name"
    print(i + 1, "size", size, "px; lines", lines(text, size, width), "avail", avail)
p.save(OUT)
print(OUT)
