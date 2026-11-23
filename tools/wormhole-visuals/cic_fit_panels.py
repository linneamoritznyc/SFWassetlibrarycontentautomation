from pptx import Presentation
from pptx.util import Emu
from PIL import ImageFont
SRC = "23-11-2026-cic-student-voices-v24.pptx"
OUT = "23-11-2026-cic-student-voices-v25.pptx"
PX, H = 9525, 1350
p = Presentation(SRC)

def nlines(text, size, width):
    f = ImageFont.truetype("fonts/SourceSans3.ttf", size)
    n = 0
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if f.getlength(t) <= width: cur = t
            else: n += 1; cur = w
        n += 1
    return n

for i, s in enumerate(p.slides):
    if i == 0: continue
    sh = list(s.shapes)
    panel, mark = sh[1], sh[2]
    q = next(x for x in sh if x.has_text_frame and x.name == "Quote and name")
    paras = q.text_frame.paragraphs
    quote = "\n".join(pa.text for pa in paras[:-1])
    size = round(paras[0].runs[0].font.size.pt / 0.75)
    # height as Canva sets it, with one spare line of room: wrap 4% narrower than the box
    text_h = (nlines(quote, size, q.width / PX * 0.86) + 0.5) * size * 1.22 + 34 + 52 * 1.2
    pad_top = q.top / PX - panel.top / PX
    new_h = pad_top + text_h + 60
    # keep the frame where it is horizontally, shrink it, then centre frame+mark+text vertically
    old_top = panel.top
    panel.height = Emu(round(new_h * PX))
    new_top = round(((H - new_h) / 2 + 30) * PX)
    dy = new_top - old_top
    for x in (panel, mark, q):
        x.top = Emu(x.top + dy)
    q.height = Emu(round(text_h * PX))
    print(i + 1, "size", size, "frame h", round(new_h), "top", round(new_top / PX))
p.save(OUT); print(OUT)
