import numpy as np
from pptx import Presentation
from pptx.util import Emu
from centre import render, measure, PX
F = '23-11-2026-cic-student-voices-v27.pptx'
PAD, INSET, H = 90, 22, 1350            # same space above and below on every slide; frame line sits 22 px inside the image
for it in range(2):
    p = Presentation(F); imgs = render(F)
    for i, s in enumerate(p.slides):
        if i == 0: continue
        sh = list(s.shapes); panel, mark = sh[1], sh[2]
        q = next(x for x in sh if x.name == "Quote and name")
        ft, fb = panel.top / PX + INSET, (panel.top + panel.height) / PX - INSET
        top, bot = measure(imgs[i], ft, fb, panel.left / PX, (panel.left + panel.width) / PX)
        print(it, i + 1, 'above', round(top - ft), 'below', round(fb - bot))
        h = (bot - top) + 2 * PAD + 2 * INSET
        new_top = (H - h) / 2
        shift = (new_top + INSET + PAD) - top     # where the content must move to
        panel.top, panel.height = Emu(round(new_top * PX)), Emu(round(h * PX))
        for x in (mark, q): x.top = Emu(round(x.top + shift * PX))
    p.save(F)
p = Presentation(F); imgs = render(F)
for i, s in enumerate(p.slides):
    if i == 0: continue
    panel = list(s.shapes)[1]
    ft, fb = panel.top / PX + INSET, (panel.top + panel.height) / PX - INSET
    top, bot = measure(imgs[i], ft, fb, panel.left / PX, (panel.left + panel.width) / PX)
    print('final', i + 1, 'above', round(top - ft), 'below', round(fb - bot))
