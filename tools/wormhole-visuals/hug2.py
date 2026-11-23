import numpy as np
from pptx import Presentation
from pptx.util import Emu
from centre import render, PX
F = '23-11-2026-cic-student-voices-v28.pptx'
PAD, H = 90, 1350
def lines_and_text(img, panel):
    sx = img.shape[1] / 1080
    l, r = int((panel.left / PX + 120) * sx), int(((panel.left + panel.width) / PX - 120) * sx)
    t0, t1 = int(panel.top / PX * sx), int((panel.top + panel.height) / PX * sx)
    a = img[t0:t1, l:r]
    g = a.mean(axis=2)
    # the frame outline: a thin row that is lighter than the rows around it across most of the width
    lift = g - (np.roll(g, 3, 0) + np.roll(g, -3, 0)) / 2
    rowscore = (lift > 12).mean(axis=1)
    cand = np.where(rowscore > 0.5)[0]
    top_line = cand[cand < len(g) * 0.3].min(); bot_line = cand[cand > len(g) * 0.7].max()
    inner = a[top_line + 6:bot_line - 6, :int((r - l) * 0.6)]
    bright = (inner.max(axis=2) > 150) & ((inner.max(axis=2) - inner.min(axis=2)) < 120)
    rows = np.where(bright.sum(axis=1) > 14)[0]
    f = lambda v: (v + t0) / sx
    return f(top_line), f(bot_line), f(rows[0] + top_line + 6), f(rows[-1] + top_line + 6)
for it in range(3):
    p = Presentation(F); imgs = render(F); worst = 0
    for i, s in enumerate(p.slides):
        if i == 0: continue
        sh = list(s.shapes); panel, mark = sh[1], sh[2]
        q = next(x for x in sh if x.name == "Quote and name")
        lt, lb, ct, cb = lines_and_text(imgs[i], panel)
        above, below = ct - lt, lb - cb
        print(it, i + 1, 'line-to-text above', round(above), 'below', round(below))
        worst = max(worst, abs(above - PAD), abs(below - PAD))
        # line sits at a fixed fraction inside the panel image: scale the panel so both gaps become PAD
        k_top = (lt - panel.top / PX) / (panel.height / PX); k_bot = ((panel.top + panel.height) / PX - lb) / (panel.height / PX)
        want = (cb - ct) + 2 * PAD                      # distance between the two lines
        h = want / (1 - k_top - k_bot)
        new_top = (H - h) / 2
        new_lt = new_top + k_top * h
        shift = (new_lt + PAD) - ct
        panel.top, panel.height = Emu(round(new_top * PX)), Emu(round(h * PX))
        for x in (mark, q): x.top = Emu(round(x.top + shift * PX))
    p.save(F)
    if worst < 3: break
