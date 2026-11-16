# Native PowerPoint builder: every element is placed directly with python-pptx.
# Text heights are measured in the brand font AND a wide fallback font, and the
# layout uses the taller of the two, so nothing overlaps in any viewer.
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image, ImageFont
import os, io

PX = 9525
def E(v): return Emu(int(round(v * PX)))

FB = os.path.expanduser('~/.fonts/brand/')
FONTS = {  # name -> (brand ttf, fallback ttf)
    ('EB Garamond', False): (FB + 'EBGaramond_400Regular.ttf', os.path.expanduser('~/.fonts/noto/NotoSans_400Regular.ttf')),
    ('EB Garamond', True): (FB + 'EBGaramond_600SemiBold.ttf', os.path.expanduser('~/.fonts/noto/NotoSans_700Bold.ttf')),
    ('Source Sans 3', False): (FB + 'SourceSans3_400Regular.ttf', os.path.expanduser('~/.fonts/noto/NotoSans_400Regular.ttf')),
    ('Source Sans 3', True): (FB + 'SourceSans3_600SemiBold.ttf', os.path.expanduser('~/.fonts/noto/NotoSans_700Bold.ttf')),
    ('Montserrat', True): (FB + 'Montserrat_700Bold.ttf', os.path.expanduser('~/.fonts/noto/NotoSans_700Bold.ttf')),
    ('Montserrat', False): (FB + 'Montserrat_400Regular.ttf', os.path.expanduser('~/.fonts/noto/NotoSans_400Regular.ttf')),
}
_fc = {}
def _font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def nlines(text, font, size, bold, width, caps=False, track=0, only=None):
    """Max number of lines over brand + fallback fonts."""
    out = 0
    for path in (FONTS[(font, bold)] if only is None else FONTS[(font, bold)][only:only+1]):
        f = _font(path, max(1, int(round(size * 4))))  # measure at 4x for precision
        W = width * 4 * 0.97
        n = 0
        for hard in text.split('\n'):
            words = (hard.upper() if caps else hard).split(' ')
            line = ''
            n += 1
            for w in words:
                t = (line + ' ' + w) if line else w
                tw = f.getlength(t) + track * 4 * len(t)
                if tw > W and line:
                    n += 1; line = w
                else:
                    line = t
        out = max(out, n)
    return out

def P(t, font='Source Sans 3', size=15, color='#333130', bold=False, lh=1.45, before=0, caps=False, track=0, align='l'):
    return dict(t=t, font=font, size=size, color=color, bold=bold, lh=lh, before=before, caps=caps, track=track, align=align)

def _flat(p):
    return dict(p['runs'][-1], t=''.join(r['t'] for r in p['runs']), before=p['before'], bold=False) if p.get('runs') else p
def measure(paras, w, only=None):
    h = 0
    for i, p in enumerate(map(_flat, paras)):
        h += (p['before'] if i else 0) + nlines(p['t'], p['font'], p['size'], p['bold'], w, p['caps'], p['track'], only) * p['size'] * p['lh']
    return h

def rgb(h): h = h.lstrip('#'); return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

class Deck:
    def __init__(self, W=816, H=1056):
        self.prs = Presentation(); self.W, self.H = W, H
        self.prs.slide_width = E(W); self.prs.slide_height = E(H)
    def page(self, bg='#FFFFFF'):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(bg)
        if bg.upper() not in ('#FFFFFF', 'WHITE'):
            rect(s, -4, -4, self.W + 8, self.H + 8, bg, 'Background')
        return s
    def save(self, path): self.prs.save(path)

def rect(s, x, y, w, h, color, name='Shape'):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(color); sh.line.fill.background(); sh.shadow.inherit = False
    sh.name = name
    st = sh._element.find(qn('p:style'))
    if st is not None: sh._element.remove(st)
    return sh

def hline(s, x, y, w, color='#C9D8C4', name='Line'):
    return rect(s, x, y, w, 1, color, name)

def pic(s, path, x, y, w, h, name, fy=0.5, fx=0.5):
    """Cover-crop the photo to the box, then place it (native picture). Edge photos bleed 3 px past the page."""
    if x <= 0: w += 3 - x; x = -3
    if x + w >= 816 - 1: w = 816 + 3 - x
    if y <= 0: h += 3 - y; y = -3
    if y + h >= 1056 - 1: h = 1056 + 3 - y
    im = Image.open(path).convert('RGB')
    iw, ih = im.size; ar = w / h
    if iw / ih > ar:
        nw = int(ih * ar); x0 = int((iw - nw) * fx); im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / ar); y0 = int((ih - nh) * fy); im = im.crop((0, y0, iw, y0 + nh))
    tw = min(im.width, int(w * 2.5)); im = im.resize((tw, int(tw / ar)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=90); b.seek(0)
    p = s.shapes.add_picture(b, E(x), E(y), E(w), E(h)); p.name = name
    return p

def png(s, path, x, y, w, name, h=None):
    im = Image.open(path)
    if h is None: h = w * im.height / im.width
    p = s.shapes.add_picture(path, E(x), E(y), E(w), E(h)); p.name = name
    return h

def _run(para, p):
    r = para.add_run(); r.text = p['t'].upper() if p.get('caps') else p['t']
    f = r.font; f.name = p['font']; f.size = Pt(round(p['size'] * 0.75)); f.bold = p['bold']; f.color.rgb = rgb(p['color'])
    rPr = r._r.get_or_add_rPr()
    if p['track']: rPr.set('spc', str(int(p['track'] * 75)))
    # set east-asian/complex fallbacks to same font
    for tag in ('a:ea', 'a:cs'):
        e = OxmlElement(tag); e.set('typeface', p['font']); rPr.append(e)

def text(s, x, y, w, paras, name, h=None, anchor='t'):
    """One native text box; paragraphs flow inside it. Returns measured height."""
    mh = measure(paras, w)
    groups = []
    for i, p in enumerate(paras):
        k = bool(_flat(p).get('track'))
        # Canva drops paragraph spacing: start a new text box wherever a gap is wanted
        if groups and groups[-1][0] == k and not (i and p.get('before')): groups[-1][1].append(p)
        else: groups.append((k, [p]))
    if len(groups) > 1:
        yy = y + ((h - mh) / 2 if (h and anchor == 'm') else (h - mh) if (h and anchor == 'b') else 0)
        for gi, (_, g) in enumerate(groups):
            if gi: yy += g[0].get('before', 0)
            g = [dict(g[0], before=0)] + g[1:]
            gh = measure(g, w, 0)
            text(s, x, yy, w, g, name + (f' {gi + 1}' if gi else ''), h=gh); yy += gh
        return mh
    tb = s.shapes.add_textbox(E(x), E(y), E(w), E(h or mh))
    tf = tb.text_frame; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = {'l': PP_ALIGN.LEFT, 'r': PP_ALIGN.RIGHT, 'c': PP_ALIGN.CENTER, 'j': PP_ALIGN.JUSTIFY}[_flat(p)['align']]
        q = _flat(p); para.line_spacing = Pt(q['size'] * q['lh'] * 0.75)
        if i and p['before']: para.space_before = Pt(p['before'] * 0.75)
        for r in (p.get('runs') or [p]): _run(para, r)
    tb.name = name
    return mh

def table(s, x, y, colw, rows, name, rule='#C9D8C4', padv=12, padh=20, rulew=1, padl=0, brand=False, mid=False):
    """rows: list of lists of P() dicts (one per cell). Native table, bottom rules only."""
    heights = []; worst = []
    for r in rows:
        def m1(c, w, only=None):
            if isinstance(c, list): c = dict(c[-1], t=' '.join(x['t'] for x in c), bold=False)
            return measure([c], w, only)
        hh = max(m1(c, colw[j] - padl - (padh if j < len(r) - 1 else 0), 0) for j, c in enumerate(r))
        hw = max(m1(c, colw[j] - padl - (padh if j < len(r) - 1 else 0)) for j, c in enumerate(r))
        heights.append(hh + 2 * padv); worst.append(hw + 2 * padv)
    gf = s.shapes.add_table(len(rows), len(colw), E(x), E(y), E(sum(colw)), E(sum(heights)))
    gf.name = name
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for a in ('firstRow', 'bandRow'): tblPr.set(a, '0')
    sid = tblPr.find(qn('a:tableStyleId'))
    if sid is not None: sid.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
    for j, cw in enumerate(colw): tbl.columns[j].width = E(cw)
    for i, r in enumerate(rows):
        tbl.rows[i].height = E(heights[i])
        for j, c in enumerate(r):
            cell = tbl.cell(i, j); cell.fill.background()
            cell.margin_left = E(padl); cell.margin_right = E(padh if j < len(r) - 1 else 0)
            cell.margin_top = E(padv); cell.margin_bottom = E(padv)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE if mid else MSO_ANCHOR.TOP
            tf = cell.text_frame; tf.word_wrap = True
            cl = c if isinstance(c, list) else [c]
            para = tf.paragraphs[0]; para.line_spacing = Pt(cl[0]['size'] * cl[0]['lh'] * 0.75)
            para.alignment = {'l': PP_ALIGN.LEFT, 'r': PP_ALIGN.RIGHT, 'c': PP_ALIGN.CENTER, 'j': PP_ALIGN.JUSTIFY}[cl[0].get('align') or 'l']
            for k, x in enumerate(cl): _run(para, dict(x, t=(' ' if k else '') + x['t']) if k else x)
            tcPr = cell._tc.get_or_add_tcPr()
            for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
                ln = OxmlElement(tag)
                if tag == 'a:lnB' and rulew:
                    ln.set('w', str(int(rulew * PX))); sf = OxmlElement('a:solidFill'); cl = OxmlElement('a:srgbClr'); cl.set('val', rule.lstrip('#').upper()); sf.append(cl); ln.append(sf)
                else:
                    ln.set('w', '0'); ln.append(OxmlElement('a:noFill'))
                tcPr.append(ln)
    return sum(heights) if brand else sum(worst)
