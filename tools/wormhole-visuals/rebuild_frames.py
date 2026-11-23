import copy, io
import numpy as np
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from centre import render, PX
from hug2 import lines_and_text
SRC, OUT = '23-11-2026-cic-student-voices-v29.pptx', '23-11-2026-cic-student-voices-v30.pptx'
PAD, L, Wd, R = 90, 61, 957, 28                    # frame matches the cover: x 44..1056, corner radius 30 px
src = Image.open('panel_src.png').convert('RGB').crop((60, 60, 990, 1030))   # soil only, no outline
p = Presentation(SRC); imgs = render(SRC)
for i, s in enumerate(p.slides):
    if i == 0: continue
    sh = list(s.shapes); grp = sh[1]
    lt, lb, ct, cb = lines_and_text(imgs[i], grp)
    top, bot = ct - PAD, cb + PAD
    h = round(bot - top)
    # 1. soil panel: plain picture with rounded corners, no outline baked in
    tex = src.resize((Wd, round(Wd * src.height / src.width)), Image.LANCZOS)
    if tex.height < h:
        tex = src.resize((round(h * src.width / src.height), h), Image.LANCZOS)
    tex = tex.crop(((tex.width - Wd) // 2, (tex.height - h) // 2, (tex.width - Wd) // 2 + Wd, (tex.height - h) // 2 + h)).convert('RGBA')
    m = Image.new('L', (Wd * 3, h * 3), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, Wd * 3 - 1, h * 3 - 1), R * 3, fill=255)
    tex.putalpha(m.resize((Wd, h), Image.LANCZOS))
    buf = io.BytesIO(); tex.save(buf, 'PNG'); buf.seek(0)
    pic = s.shapes.add_picture(buf, Emu(L * PX), Emu(round(top * PX)), Emu(Wd * PX), Emu(h * PX))
    pic.name = 'Soil panel'
    # 2. the outline: its own rounded-rectangle shape, no fill, thin cream line
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(L * PX), Emu(round(top * PX)), Emu(Wd * PX), Emu(h * PX))
    box.name = 'Frame line'
    box.adjustments[0] = R / min(Wd, h)
    box.fill.background()
    box.line.color.rgb = RGBColor(0xF4, 0xF1, 0xEA); box.line.width = Pt(0.75)
    ln = box.line._get_or_add_ln(); sf = ln.find('{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
    clr = sf[0]; a = clr.makeelement('{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', {'val': '55000'}); clr.append(a)
    box.shadow.inherit = False
    # order: background, soil panel, frame line, quote mark, text
    tree = s.shapes._spTree
    grp_el = grp._element
    grp_el.addprevious(pic._element); pic._element.addnext(box._element)
    tree.remove(grp_el)
    print(i + 1, 'frame', round(top), '->', round(bot))
p.save(OUT); print(OUT)
