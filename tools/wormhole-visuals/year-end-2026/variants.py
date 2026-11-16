# Design variations of the three fundraising documents, built natively in PowerPoint.
# One content model (content.py), several styles. Every text height is measured in the
# brand font and in Noto Sans, and the flow uses the taller one, so nothing overlaps.
import math, sys, re
from natlib import *
from pptx.enum.shapes import MSO_SHAPE
from content import DOCS

W, H, M = 816, 1056, 72
CW = W - 2 * M
GR = '#156826'; DG = '#22371F'; INK = '#333130'; SAGE = '#A7B097'; SPEC = '#E6EADC'; LIV = '#A2AE77'
OLIVE = '#5F6A3C'; BR = '#4F3433'; BLUE = '#3780B8'; LGR = '#59A66C'; CREAM = '#F4F1EA'; WHITE = '#FFFFFF'

def eyebrow(t, c=GR, align='l'): return P(t, 'Montserrat', 13, c, True, 1.25, align=align)
def body(t, size=15, c=INK, before=0, lh=1.5): return P(t, 'Source Sans 3', size, c, lh=lh, before=before)

def rrect(s, x, y, w, h, color, r=18, name='Card'):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(x), E(y), E(w), E(h))
    sh.adjustments[0] = min(0.5, r / min(w, h))
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(color); sh.line.fill.background(); sh.shadow.inherit = False
    sh.name = name
    st = sh._element.find(qn('p:style'))
    if st is not None: sh._element.remove(st)
    return sh

def round_pic(p, r, w, h):
    g = p._element.spPr.find(qn('a:prstGeom')); g.set('prst', 'roundRect')
    gd = OxmlElement('a:gd'); gd.set('name', 'adj'); gd.set('fmla', f'val {int(r / min(w, h) * 100000)}'); g.find(qn('a:avLst')).append(gd)

def swoosh(s, y, color, thick, name, amp=34, phase=0.0, x0=-20, x1=W + 20):
    top = [(x, y + amp * math.sin((x / W) * math.pi * 1.15 + phase)) for x in range(int(x0), int(x1) + 1, 8)]
    pts = top + [(x, yy + thick) for x, yy in reversed(top)]
    fb = s.shapes.build_freeform(E(pts[0][0]), E(pts[0][1]), scale=1.0)
    fb.add_line_segments([(E(x), E(yy)) for x, yy in pts[1:]], close=True)
    sh = fb.convert_to_shape(); sh.fill.solid(); sh.fill.fore_color.rgb = rgb(color); sh.line.fill.background(); sh.shadow.inherit = False; sh.name = name

def wave_fill(s, y, color, name, amp=30, phase=0.0, bottom=H):
    """filled wave from a curved top edge down to the page bottom"""
    top = [(x, y + amp * math.sin((x / W) * math.pi * 1.15 + phase)) for x in range(-20, W + 21, 8)]
    pts = top + [(W + 20, bottom + 20), (-20, bottom + 20)]
    fb = s.shapes.build_freeform(E(pts[0][0]), E(pts[0][1]), scale=1.0)
    fb.add_line_segments([(E(x), E(yy)) for x, yy in pts[1:]], close=True)
    sh = fb.convert_to_shape(); sh.fill.solid(); sh.fill.fore_color.rgb = rgb(color); sh.line.fill.background(); sh.shadow.inherit = False; sh.name = name

from fontTools.ttLib import TTFont as _TT
_lsbc = {}
def lsb(t, font, bold, size):
    out = []
    for path in FONTS[(font, bold)]:
        if path not in _lsbc: _lsbc[path] = _TT(path)
        f = _lsbc[path]; g = f.getBestCmap().get(ord(t[0]))
        out.append(f['hmtx'][g][1] * size / f['head'].unitsPerEm if g else 0)
    return sum(out) / len(out)

# --------------------------------------------------------------------------- flow
class Flow:
    def __init__(self, style, doc):
        self.st = style; self.doc = doc; self.d = Deck(); self.s = None; self.y = 0; self.top = 0; self.bot = H - 64; self.pending = None
    def newpage(self):
        self.s, self.y, self.bot = self.st.page(self); self.exact = False
        self.top = self.y
    def try_photo(self):
        if self.pending and self.s is not None:
            u = self.pending
            room = H - self.y - u.get('gap', 0)
            if room >= u['minh']:
                u['draw'](self, self.y + u.get('gap', 0), room); self.y = self.bot + 1; self.pending = None
    def place(self, units):
        i = 0
        while i < len(units):
            u = units[i]
            if u.get('flex'):
                self.pending = u; self.try_photo(); i += 1; continue
            need = u['h'] + (u.get('gap', 0) if self.y > self.top else 0)
            j = i
            while units[j].get('keep') and j + 1 < len(units):   # keep chains: heading + label row + first row
                j += 1; need += units[j]['h'] + units[j].get('gap', 0)
            if need > (H - 60 - 92):   # block taller than a page: only keep the next two units together
                need = u['h'] + sum(x['h'] + x.get('gap', 0) for x in units[i + 1:i + 3])
            if self.s is None or (self.y + need > self.bot and self.y > self.top + 80 and not getattr(self, 'exact', False)):
                self.try_photo()
                self.newpage()
            if self.y > self.top: self.y += u.get('gap', 0)
            u['draw'](self, self.y); self.y += u['h']; i += 1

def whole(us):
    # a heading, table, list or grid is never split across pages
    for u in us[:-1]: u['keep'] = True
    return us

def build(style, doc, out):
    f = Flow(style, doc)
    style.cover(f, doc)
    f.s = None
    for b in doc['blocks']:
        kind = b[0]
        if kind == 'photo_top':
            f.try_photo(); f.pending = None
            f.s = f.d.page(WHITE); PH = b[4] if len(b) > 4 else 325
            pic(f.s, 'ph/' + b[1], 0, 0, W, PH, 'Photo: ' + b[3], fy=b[2])
            f.y = PH + 52; f.top = f.y - 1; f.bot = H - 40; f.exact = True
            continue
        if kind == 'photo': f.place(style.photo(f, b[1], b[2], b[3]))
        elif kind == 'section': f.place(style.section(f, b[1], b[2]))
        elif kind == 'grid': f.place(whole(style.grid(f, b[1], b[2])))
        elif kind == 'list': f.place(whole(style.list(f, b[1], b[2])))
        elif kind == 'rows': f.place(whole(style.rows(f, b[1], b[2], b[3])))
        elif kind == 'quote': f.place(style.quote(f, b[1], b[2]))
        elif kind == 'pullquote': f.place(style.pullquote(f, b[1], b[2]))
    f.try_photo()
    style.closing(f, doc)
    f.d.save(out)
    return len(f.d.prs.slides._sldIdLst)

class _G:
    def __init__(self, g): self.shapes = g.shapes

def U(h, draw, gap=0, keep=False): return dict(h=h, draw=draw, gap=gap, keep=keep)

# --------------------------------------------------------------------------- shared closing pieces
def give_row(s, y, c, light=True, logo=True):
    g = [body(x, 14, SPEC if light else INK, lh=1.5) for x in c['give'].split(' · ')]
    tw = 340
    q = round(measure(g, tw, 0))
    png(s, 'qr-light.png' if light else 'qr.png', M, y, q, 'QR code', q)
    text(s, M + q + 26, y - 3, tw, g, 'Give online and contact')
    lw = round(q * 464 / 403)
    if logo: png(s, 'logo-white.png' if light else 'logo.png', W - M - lw, y, lw, 'SFW logo', q)
    h = max(q, measure(g, tw))
    if c.get('legal'):
        h += 18 + text(s, M, y + h + 18, CW, [body(c['legal'], 11, LIV if light else '#4A463F', lh=1.35)], 'Legal line')
    return h
def give_h(c):
    g = [body(x, 13.5, lh=1.45) for x in c['give'].split(' · ')] + ([body(c['legal'], 10.5, before=8, lh=1.35)] if c.get('legal') else [])
    return max(109, measure(g, 372))
def closing_paras(c, light=True, gsize=36, qsize=25):
    col = WHITE if light else DG
    ps = []
    if c.get('goal'):
        if c['goal'].isupper(): ps.append(P(c['goal'], 'Montserrat', 15, col, True, 1.3, ))
        else: ps.append(P(c['goal'], 'EB Garamond', gsize, col, lh=1.12))
    if c.get('quote'):
        ps.append(P(c['quote'], 'EB Garamond', qsize, col, lh=1.3, before=22 if ps else 0))
        ps.append(P(c['attr'], 'Source Sans 3', 14, LIV if light else GR, True, 1.4, before=12))
    if c.get('more'): ps.append(body(c['more'], 15.5, SPEC if light else INK, lh=1.5, before=24))
    return ps

# =========================================================================== STYLE 1: EDITORIAL
class Editorial:
    name = 'Editorial'
    def heads(self, s, short, c=GR):
        rh = lambda t, a='l': P(t, 'Montserrat', 17.33, c, True, 1.2, align=a)
        text(s, M, 44, 300, [rh('Soil Food Web Foundation')], 'Running head left')
        text(s, W - M - 300, 44, 300, [rh(short, 'r')], 'Running head right')
    def page(self, f):
        s = f.d.page(WHITE); self.heads(s, f.doc['short']); return s, 92, H - getattr(self, 'bottom_m', 60)
    def cover(self, f, doc):
        if doc['cover'].get('fade'): return cover_fade(self, f, doc)
        c = doc['cover']; s = f.d.page(WHITE)
        org, docname = c['eyebrow'].split(': ')
        ep = [P(org, 'Montserrat', 19, GR, True, 1.3), P(docname, 'Montserrat', 42, GR, True, 1.12, before=6)]
        tp = [P(c['title'], 'EB Garamond', 32, DG, lh=1.15)]
        ip = [P(c['intro'], 'Source Sans 3', 16.5, INK, lh=1.55)]
        eh = measure(ep, CW); th = measure(tp, CW); ih = measure(ip, CW - 136)
        block = eh + 14 + th + 22 + 1 + 24 + ih
        if c.get('stats'):
            sp = [([P(n, 'EB Garamond', 44, GR, lh=1.0)], [P(l, 'Source Sans 3', 15, INK, lh=1.3)]) for n, l in c['stats']]
            sh_ = max(measure(a, 160, 0) for a, _ in sp) + 6 + max(measure(b, 160, 0) for _, b in sp)
            block += 34 + sh_
        if c.get('quote'):
            QX = 44
            qp = [P(c['quote'], 'EB Garamond', 21, GR, lh=1.35)]
            ap = [P(c['attr'], 'Source Sans 3', 14, GR, True, 1.35)]
            qh = measure(qp, CW - 136 - QX, 0); ah = measure(ap, CW - 136 - QX, 0)
            block += 30 + qh + 10 + ah
        if c.get('ph_h'):
            PHh = c['ph_h']
            pic(s, 'ph/' + c['photo'], 0, 0, W, PHh, 'Photo: ' + c['alt'], fy=c['fy'])
            y = PHh + (H - 72 - PHh - block) / 2 + 8
        else:
            y = H - (130 if c.get('accent') else 72) - block
            pic(s, 'ph/' + c['photo'], 0, 0, W, y - 48 - (14 if c.get('accent') else 0), 'Photo: ' + c['alt'], fy=c['fy'])
        print('  cover text top', round(y), 'block', round(block))
        if c.get('accent'):
            pb = (c['ph_h'] if c.get('ph_h') else y - 48)
            wave_fill(s, pb - 34, WHITE, 'Photo edge wave', amp=22, phase=0.4, bottom=pb - 17)
            swoosh(s, pb - 34 - 2, GR, 5, 'Green swoosh line', amp=22, phase=0.4)
        if c.get('warm'):
            top = (c['ph_h'] if c.get('ph_h') else y - 48) - 56
            from PIL import Image as _I
            el = _I.open(c['warm']); need = round(el.width * (H - top + 4) / (W + 4))
            el.crop((0, 0, el.width, min(need, el.height))).save('/tmp/cover-el.png')
            png(s, '/tmp/cover-el.png', -2, top, W + 4, 'Swoosh element', H - top + 4)
            for p_ in ep: p_['color'] = WHITE
            ep[0]['color'] = LIV; tp[0]['color'] = WHITE; ip[0]['color'] = WHITE
        e1, e2 = ep[0], dict(ep[1], before=0)
        h1 = text(s, M - lsb(e1['t'], 'Montserrat', True, e1['size']), y, CW, [e1], 'Organisation')
        text(s, M - lsb(e2['t'], 'Montserrat', True, e2['size']), y + h1 + 6, CW, [e2], 'Document name'); y += eh + 14
        text(s, M - lsb(tp[0]['t'], 'EB Garamond', False, tp[0]['size']), y, CW, tp, 'Title'); y += th + 22
        y += 6
        text(s, M - lsb(ip[0]['t'], 'Source Sans 3', False, ip[0]['size']), y, CW - 136, ip, 'Intro')
        if c.get('stats'):
            sy = y + measure(ip, CW - 136, 0) + 34
            grp = s.shapes.add_group_shape(); grp.name = 'Key numbers'; g = _G(grp)
            from PIL import ImageFont as _F
            _f = _F.truetype(FONTS[('EB Garamond', False)][0], 44)
            xs = [M]; 
            for a, _ in sp[:-1]: xs.append(xs[-1] + _f.getlength(a[0]['t']) + 64)
            for k, (a, b) in enumerate(sp):
                x = xs[k]
                ah_ = measure(a, 160, 0)
                text(g, x - lsb(a[0]['t'], 'EB Garamond', False, 44), sy, 160, a, 'Number: ' + a[0]['t'])
                text(g, x, sy + ah_ + 6, 160, b, 'Label: ' + b[0]['t'])
        if c.get('quote'):
            qy = y + measure(ip, CW - 136, 0) + 30
            png(s, 'brandq-green.png', M, qy + 4, 30, 'Quote mark')
            text(s, M + QX, qy, CW - 136 - QX, qp, 'Leslie quote')
            text(s, M + QX, qy + qh + 10, CW - 136 - QX, ap, 'Quote attribution')
        if c.get('accent'):
            PHb = c['ph_h'] if c.get('ph_h') else None
            CS = 330
            png(s, 'el-corner-br.png', W - CS + 2, H - CS + 2, CS, 'Corner wave element', CS)
            png(s, 'logo-white.png', W - M - 112, H - 56 - 97, 112, 'SFW logo')
        else:
            png(s, 'logo-white.png' if c.get('warm') else 'logo.png', W - M - 104, H - 72 - 90, 104, 'SFW logo')
    def heading(self, t, gap=44):
        ps = [P(t, 'EB Garamond', 30, GR, lh=1.15)]; h = measure(ps, CW)
        def dr(f, y): text(f.s, M, y, CW, ps, 'Heading: ' + t[:30]); hline(f.s, M, y + h + 8, CW, SAGE, 'Rule')
        return U(h + 9, dr, gap, keep=True)
    def section(self, f, t, paras):
        us = [self.heading(t)] if t else []
        for k, p in enumerate(paras):
            ps = [body(p, 16.5, lh=1.55)]; h = measure(ps, CW)
            us.append(U(h, (lambda ps: lambda f, y: text(f.s, M, y, CW, ps, 'Text'))(ps), 18 if k == 0 and t else (14 if k else 30)))
        return us
    def grid(self, f, t, items):
        us = [self.heading(t)]
        cw = (CW - 40) / 2
        for r in range(0, len(items), 2):
            pair = items[r:r + 2]
            pss = [[P(a, 'EB Garamond', 20, DG, True, 1.2), body(b, 15, before=6, lh=1.45)] for a, b in pair]
            h = max(measure(ps, cw) for ps in pss)
            def dr(f, y, pss=pss, pair=pair):
                for k, ps in enumerate(pss): text(f.s, M + k * (cw + 40), y, cw, ps, pair[k][0][:-1])
            us.append(U(h, dr, 24 if r == 0 else 28))
        return us
    def _table_units(self, colw, rows, name, rule=SAGE, padv=12, padh=24, hdr=None):
        us = []
        scratch = Deck().page()
        if hdr and hdr[0].get('t') == 'Barriers to change':
            allr = [hdr] + rows
            h = table(scratch, 0, 0, colw, allr, name, rule, padv, padh)
            return [U(h, lambda f, y: table(f.s, M, y, colw, allr, name, rule, padv, padh), 0)]
        for k, r in enumerate(([hdr] if hdr else []) + rows):
            rw = 0 if (hdr and k == 0 and not (hdr[0].get('t') == 'Barriers to change')) else 1
            h = table(scratch, 0, 0, colw, [r], name, rule, padv, padh, rw)
            us.append(U(h, (lambda r, rw: lambda f, y: table(f.s, M, y, colw, [r], name, rule, padv, padh, rw))(r, rw), 0))
        if hdr: us[0]['keep'] = True
        return us
    def list(self, f, t, items):
        return [self.heading(t)] + self._table_units([CW], [[body(x, 15, lh=1.45)] for x in items], 'Table: ' + t)
    def rows(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows)
        if amt:
            colw = [CW - 176, 176]
            cells = [[[P(a, 'Source Sans 3', 15, DG, True, 1.45), body(b, 15, lh=1.45)], P(v, 'EB Garamond', 18, DG, lh=1.25)] for a, b, v in rows]
            h = [eyebrow(hdr[0]), eyebrow(hdr[2])] if hdr else None
        else:
            lw = (CW / 2 + 14) if (hdr and hdr[0] == 'Barriers to change') else (236 if not (hdr and hdr[0] == 'Gift') else 150)
            colw = [lw, CW - lw]
            big = hdr and hdr[0] == 'Gift'
            bs = 16 if (hdr and hdr[0] == 'Barriers to change') else 15
            cells = [[P(a, 'EB Garamond', 24, GR, lh=1.15) if big else P(a, 'Source Sans 3', bs, DG, True, 1.45), body(b, bs, lh=1.5)] for a, b, _ in rows]
            h = ([P(hdr[0], 'EB Garamond', 30, GR, lh=1.15), P(hdr[1], 'EB Garamond', 30, GR, lh=1.15)] if not big else [eyebrow(hdr[0]), eyebrow(hdr[1])]) if hdr else None
        tu = self._table_units(colw, cells, 'Table: ' + (t or hdr[0]), hdr=h)
        tu[0]['gap'] = 8 if t else 40
        if not t: tu[0]['keep'] = True
        return us + tu
    def quote(self, f, t, a):
        ps = [P(t, 'EB Garamond', 24, DG, lh=1.32), dict(eyebrow(a), before=16)]
        h = measure(ps, CW)
        return [U(h, lambda f, y: text(f.s, M, y, CW, ps, 'Quote'), 30)]
    def photo(self, f, path, fy, alt):
        def dr(f, y, room):
            print('  photo', path, 'height', round(H - y))
            if path.startswith('hay'):
                pic(f.s, 'ph/' + path, 0, y, W, H - y, 'Texture: hay', fy=fy)
                import math
                yy = y + 26
                top = [(x, yy + 20 * math.sin((x / W) * math.pi * 1.15 + 0.3)) for x in range(-20, W + 21, 8)]
                pts = [(-20, y - 4)] + top + [(W + 20, y - 4)]
                fb = f.s.shapes.build_freeform(E(pts[0][0]), E(pts[0][1]), scale=1.0)
                fb.add_line_segments([(E(a), E(b)) for a, b in pts[1:]], close=True)
                sh = fb.convert_to_shape(); sh.fill.solid(); sh.fill.fore_color.rgb = rgb(WHITE); sh.line.fill.background(); sh.name = 'Swoosh cut'
                st = sh._element.find(qn('p:style'))
                if st is not None: sh._element.remove(st)
                swoosh(f.s, yy - 3, GR, 6, 'Swoosh', amp=20, phase=0.3)
                return
            pic(f.s, 'ph/' + path, 0, y, W, H - y, 'Photo: ' + alt, fy=fy)
        return [dict(h=0, flex=True, minh=150, gap=self.photo_gap, draw=dr)]
    photo_gap = 40
    def closing(self, f, doc):
        c = doc['closing']; s = f.d.page(DG)
        gh = give_h(c); gy = H - 60 - gh
        if c.get('quote') and c.get('goal') and not c['goal'].isupper():
            gp = [P(c['goal'], 'EB Garamond', 40, WHITE, lh=1.1)]
            qp = [P(c['quote'].strip('"'), 'EB Garamond', 22, DG, lh=1.25)]
            ap = [P(c['attr'], 'Source Sans 3', 13, GR, True, 1.3)]
            mp = [body(c['more'], 17, SPEC, lh=1.5)]
            QX = 70; qw = CW - QX - 28
            qh = measure(qp, qw); ah = measure(ap, qw)
            boxh = 22 + qh + 6 + ah + 22
            mh = measure(mp, CW, 0); gh2 = measure(gp, CW, 0)
            PHh = gy - 44 - mh - 20 - gh2 - 38 - boxh - 38
            pic(s, 'ph/' + c['photo'], 0, 0, W, PHh, 'Photo: ' + c['alt'], fy=c['fy'])
            png(s, 'el-dg.png', -2, PHh - 80, W + 4, 'Deep green swoosh element', max(620, H - PHh + 82))
            y = PHh + 38
            rect(s, M, y, CW, boxh, WHITE, 'Quote box')
            png(s, 'brandq-green.png', M + 24, y + 22, 30, 'Quote mark')
            text(s, M + QX, y + 22, qw, qp, 'Elaine quote')
            text(s, M + QX, y + 22 + qh + 6, qw, ap, 'Quote attribution')
            y += boxh + 38
            text(s, M, y, CW, gp, 'Goal'); y += gh2 + 20
            text(s, M, y, CW, mp, 'Giving pathways')
            hline(s, M, gy - 22, CW, OLIVE)
            give_row(s, gy, c)
            return
        _ps = closing_paras(c)
        PHh = (gy - 56 - measure(_ps, CW) - 80) if _ps else gy - 120
        pic(s, 'ph/' + c['photo'], 0, 0, W, PHh, 'Photo: ' + c['alt'], fy=c['fy'])
        wave_fill(s, PHh - 40, DG, 'Swoosh cut', amp=28, phase=0.3, bottom=H)
        swoosh(s, PHh - 40 - 3, GR, 6, 'Swoosh', amp=28 * 1.0, phase=0.3)
        ps = closing_paras(c)
        if ps: text(s, M, PHh + 60, CW, ps, 'Goal and quote')
        hline(s, M, gy - 22, CW, OLIVE)
        give_row(s, gy, c)

# =========================================================================== STYLE 2: CARDS
class Cards(Editorial):
    name = 'Cards'
    def page(self, f):
        s = f.d.page(SPEC); pic(s, 'ph/ground-pale.jpg', 0, 0, W, H, 'Background: pale hay texture')
        self.heads(s, f.doc['short']); return s, 92, H - 52
    def cover(self, f, doc):
        c = doc['cover']; s = f.d.page(SPEC)
        pic(s, 'ph/ground-pale.jpg', 0, 0, W, H, 'Background: pale hay texture')
        tp = [P(c['title'].replace('\n', ' '), 'Montserrat', 38, WHITE, True, 1.12)]
        ip = [body(c['intro'], 16, WHITE, lh=1.55)]
        th = measure(tp, CW); ih = measure(ip, 620)
        py = 92 + th + 22 + ih + 44; ph = H - 64 - py
        pic(s, 'ph/band-green.jpg', 0, 0, W, py + ph * 0.55, 'Background: green hay band')
        text(s, M, 44, CW, [eyebrow(c['eyebrow'], WHITE)], 'Eyebrow')
        text(s, M, 92, CW, tp, 'Title')
        text(s, M, 92 + th + 22, 620, ip, 'Intro')
        p = pic(s, 'ph/' + c['photo'], M, py, CW, ph, 'Photo: ' + c['alt'], fy=c['fy']); round_pic(p, 24, CW, ph)
    def heading(self, t, gap=40):
        ps = [P(t, 'Montserrat', 24, BR, True, 1.2)]; h = measure(ps, CW)
        return U(h, lambda f, y: text(f.s, M, y, CW, ps, 'Heading: ' + t[:30]), gap, keep=True)
    def _card(self, paras, w, pad=24):
        return measure(paras, w - 2 * pad) + 2 * pad
    def section(self, f, t, paras):
        us = [self.heading(t)] if t else []
        ps = [body(p, 15.5, before=12 if k else 0) for k, p in enumerate(paras)]
        h = self._card(ps, CW)
        us.append(U(h, lambda f, y: (rrect(f.s, M, y, CW, h, WHITE, 20, 'Card'), text(f.s, M + 24, y + 24, CW - 48, ps, 'Text')), 16 if t else 36))
        return us
    def grid(self, f, t, items):
        us = [self.heading(t)]
        cw = (CW - 16) / 2
        for r in range(0, len(items), 2):
            pair = items[r:r + 2]
            pss = [[P(a, 'Montserrat', 16, GR, True, 1.3), body(b, 14.5, before=6, lh=1.45)] for a, b in pair]
            h = max(self._card(ps, cw) for ps in pss)
            def dr(f, y, pss=pss, pair=pair, h=h):
                for k, ps in enumerate(pss):
                    x = M + k * (cw + 16)
                    rrect(f.s, x, y, cw, h, WHITE, 20, 'Card: ' + pair[k][0]); text(f.s, x + 24, y + 24, cw - 48, ps, pair[k][0][:-1], h=h - 48, anchor='m')
            us.append(U(h, dr, 16 if r == 0 else 16))
        return us
    def list(self, f, t, items):
        us = [self.heading(t)]
        for k, x in enumerate(items):
            ps = [body(x, 15, lh=1.45)]; h = self._card(ps, CW - 56, 22)
            def dr(f, y, ps=ps, h=h, k=k):
                rrect(f.s, M, y, CW, h, WHITE, 18, 'Card')
                rrect(f.s, M + 22, y + h / 2 - 5, 10, 10, LGR, 5, 'Dot')
                text(f.s, M + 56, y + 22, CW - 56 - 22, ps, 'Text', h=h - 44, anchor='m')
            us.append(U(h, dr, 16 if k == 0 else 12))
        return us
    def rows(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows); icons = ['i-student.png', 'i-idea.png', 'i-compost.png', 'i-fielddata.png', 'i-barn.png']
        PAD = 18 if amt else 24; AMW = 150 if amt else 0
        use_icons = amt and hdr and hdr[0] == 'Priority'
        TX = PAD + (56 if use_icons else 0)
        if hdr:
            hp = [eyebrow(x if x else '') for x in hdr]
            def drh(f, y):
                text(f.s, M + TX, y, 300, [eyebrow(hdr[0])], 'Column label')
                if hdr[1] and not amt: text(f.s, M + PAD + (CW - 2 * PAD) * 0.42 + 12, y, 300, [eyebrow(hdr[1])], 'Column label')
                if hdr[2]: text(f.s, M + CW - PAD - AMW, y, AMW, [eyebrow(hdr[2], GR, 'r')], 'Column label')
            us.append(U(14, drh, 16 if t else 40, keep=True))
        for k, (a, b, v) in enumerate(rows):
            if amt:
                tw = CW - TX - PAD - AMW - 20
                ps = [P(a, 'Montserrat', 14, BR, True, 1.3), body(b, 13.5, before=4, lh=1.38)]
                h = measure(ps, tw) + 2 * PAD
                def dr(f, y, ps=ps, h=h, v=v, k=k, a=a, tw=tw):
                    rrect(f.s, M, y, CW, h, WHITE, 18, 'Card: ' + a)
                    if use_icons: png(f.s, icons[k % 5], M + PAD, y + (h - 34) / 2, 34, a + ' icon')
                    text(f.s, M + TX, y + PAD, tw, ps, a, h=h - 2 * PAD, anchor='m')
                    text(f.s, M + CW - PAD - AMW, y + PAD, AMW, [P(v, 'Montserrat', 16, GR, True, 1.3, align='r')], 'Amount', h=h - 2 * PAD, anchor='m')
            else:
                lw = (CW - 2 * PAD) * 0.42; rw = CW - 2 * PAD - lw - 12
                big = hdr and hdr[0] == 'Gift'
                lp = [P(a, 'EB Garamond', 28, GR, lh=1.1)] if big else [P(a, 'Montserrat', 15, BR, True, 1.35)]
                rp = [body(b, 14.5, lh=1.45)]
                h = max(measure(lp, lw), measure(rp, rw)) + 2 * PAD
                def dr(f, y, lp=lp, rp=rp, h=h, a=a, lw=lw, rw=rw):
                    rrect(f.s, M, y, CW, h, WHITE, 18, 'Card: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, lw, lp, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + PAD + lw + 12, y + PAD, rw, rp, 'Response', h=h - 2 * PAD, anchor='m')
            us.append(U(h, dr, (8 if amt else 10) if (k or hdr) else 16))
        return us
    def quote(self, f, t, a):
        ps = [P(t, 'EB Garamond', 23, WHITE, lh=1.32), dict(eyebrow(a, SPEC), before=14)]
        h = measure(ps, CW - 64) + 64
        return [U(h, lambda f, y: (rrect(f.s, M, y, CW, h, GR, 24, 'Quote card'), text(f.s, M + 32, y + 32, CW - 64, ps, 'Quote')), 30)]
    def photo(self, f, path, fy, alt):
        def dr(f, y, room):
            p = pic(f.s, 'ph/' + path, M, y, CW, room, 'Photo: ' + alt, fy=fy); round_pic(p, 22, CW, room)
        return [dict(h=0, flex=True, minh=220, gap=24, draw=dr)]
    def closing(self, f, doc):
        c = doc['closing']; s = f.d.page(DG)
        gh = give_h(c); gy = H - 60 - gh
        php = 400 if closing_paras(c) else gy - 72 - 90
        pic(s, 'ph/band-green.jpg', 0, 0, W, 72 + php * 0.6 + 50, 'Background: green hay band')
        p = pic(s, 'ph/' + c['photo'], M, 72, CW, php, 'Photo: ' + c['alt'], fy=c['fy']); round_pic(p, 24, CW, php)
        ps = closing_paras(c)
        if ps: text(s, M, 560, CW, ps, 'Goal and quote', h=gy - 34 - 560, anchor='m')
        hline(s, M, gy - 22, CW, OLIVE)
        give_row(s, gy, c)

# =========================================================================== STYLE 3: COLOR BLOCKS
BOXC = [GR, DG, BR, OLIVE]
class Blocks(Editorial):
    name = 'Color Blocks'
    def heads(self, s, short, c=DG):
        rect(s, 0, 0, W, 8, GR, 'Top bar')
        text(s, M, 40, 340, [eyebrow('Soil Food Web Foundation', c)], 'Running head left')
        text(s, W - M - 340, 40, 340, [eyebrow(short, c, 'r')], 'Running head right')
    def page(self, f):
        s = f.d.page(WHITE); self.heads(s, f.doc['short']); return s, 90, H - 56
    def cover(self, f, doc):
        self.nrows = 0
        c = doc['cover']; s = f.d.page(WHITE)
        ep = [eyebrow(c['eyebrow'], SPEC)]; tp = [P(c['title'], 'Montserrat', 34, WHITE, True, 1.18)]
        ip = [body(c['intro'], 15.5, WHITE, lh=1.55)]
        eh = measure(ep, CW); th = measure(tp, CW); ih = measure(ip, 600)
        bt = H - (48 + eh + 14 + th + 24 + ih + 56)
        pic(s, 'ph/' + c['photo'], 0, 0, W, bt, 'Photo: ' + c['alt'], fy=c['fy'])
        rect(s, 0, bt, W, H - bt, GR, 'Green box')
        y = bt + 48
        text(s, M, y, CW, ep, 'Eyebrow'); y += eh + 14
        text(s, M, y, CW, tp, 'Title'); y += th + 24
        text(s, M, y, 600, ip, 'Intro')
        png(s, 'logo-white.png', W - M - 64, H - 56 - 64, 64, 'SFW logo white')
    def heading(self, t, gap=44):
        ps = [P(t, 'Montserrat', 26, DG, True, 1.2)]; h = measure(ps, CW)
        def dr(f, y): rect(f.s, M, y + 2, 6, h - 4, LGR, 'Heading mark'); text(f.s, M + 20, y, CW - 20, ps, 'Heading: ' + t[:30])
        return U(h, dr, gap, keep=True)
    def section(self, f, t, paras):
        us = [self.heading(t)] if t else []
        if len(paras) >= 2:
            cw = (CW - 40) / 2
            half = (len(paras) + 1) // 2 if len(paras) > 2 else 1
            L = [body(p, 15, before=12 if k else 0) for k, p in enumerate(paras[:half])]
            R = [body(p, 15, before=12 if k else 0) for k, p in enumerate(paras[half:])]
            h = max(measure(L, cw), measure(R, cw))
            us.append(U(h, lambda f, y: (text(f.s, M, y, cw, L, 'Text left'), text(f.s, M + cw + 40, y, cw, R, 'Text right')), 20 if t else 36))
        else:
            ps = [body(paras[0], 15.5)]; h = measure(ps, CW)
            us.append(U(h, lambda f, y: text(f.s, M, y, CW, ps, 'Text'), 20))
        return us
    def grid(self, f, t, items):
        us = [self.heading(t)]
        cw = (CW - 12) / 2
        for r in range(0, len(items), 2):
            pair = items[r:r + 2]
            pss = [[P(a, 'Montserrat', 17, WHITE, True, 1.3), body(b, 14.5, WHITE, before=8, lh=1.45)] for a, b in pair]
            h = max(measure(ps, cw - 48) for ps in pss) + 48
            def dr(f, y, pss=pss, pair=pair, h=h, r=r):
                for k, ps in enumerate(pss):
                    x = M + k * (cw + 12)
                    rect(f.s, x, y, cw, h, BOXC[(r + k) % 4], 'Box: ' + pair[k][0])
                    text(f.s, x + 24, y + 24, cw - 48, ps, pair[k][0][:-1])
            us.append(U(h, dr, 20 if r == 0 else 12))
        return us
    def list(self, f, t, items):
        us = [self.heading(t)]
        for k, x in enumerate(items):
            ps = [body(x, 15, lh=1.45)]; h = max(measure(ps, CW - 70), 40)
            def dr(f, y, ps=ps, k=k):
                text(f.s, M, y - 6, 50, [P(f'0{k + 1}', 'Montserrat', 28, LGR, True, 1.0)], 'Number')
                text(f.s, M + 70, y, CW - 70, ps, 'Text')
            us.append(U(h, dr, 20 if k == 0 else 18))
        return us
    def rows(self, f, t, hdr, rows):
        self.nrows = getattr(self, 'nrows', 0) + 1
        if self.nrows % 2 == 0:
            return self.rows_ruled(f, t, hdr, rows)
        return self.rows_boxes(f, t, hdr, rows)
    def rows_ruled(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows)
        AB = 176 if amt else 0
        LW = CW - AB - 24 if amt else 250
        if hdr:
            def drh(f, y):
                text(f.s, M, y, 300, [eyebrow(hdr[0], GR)], 'Column label')
                if hdr[1] and not amt: text(f.s, M + LW + 24, y, 300, [eyebrow(hdr[1], GR)], 'Column label')
                if hdr[2]: text(f.s, M + CW - AB, y, AB, [eyebrow(hdr[2], GR, 'r')], 'Column label')
                rect(f.s, M, y + 22, CW, 3, DG, 'Rule')
            us.append(U(25, drh, 20 if t else 44, keep=True))
        for k, (a, b, v) in enumerate(rows):
            if amt:
                ps = [P(a, 'Montserrat', 15, DG, True, 1.3), body(b, 14, before=4, lh=1.42)]
                vs = [P(v, 'Montserrat', 17, GR, True, 1.25, align='r')]
                h = max(measure(ps, LW), measure(vs, AB)) + 32
                def dr(f, y, ps=ps, vs=vs, h=h, a=a):
                    text(f.s, M, y + 16, LW, ps, a[:30])
                    text(f.s, M + CW - AB, y + 16, AB, vs, 'Amount', h=h - 32, anchor='m')
                    hline(f.s, M, y + h - 1, CW, SAGE)
            else:
                lp = [P(a, 'Montserrat', 15, DG, True, 1.3)]; rp = [body(b, 14.5, lh=1.45)]
                h = max(measure(lp, LW), measure(rp, CW - LW - 24)) + 32
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    text(f.s, M, y + 16, LW, lp, a[:30]); text(f.s, M + LW + 24, y + 16, CW - LW - 24, rp, 'Response')
                    hline(f.s, M, y + h - 1, CW, SAGE)
            us.append(U(h, dr, 0 if (k or hdr) else 20))
        return us
    def rows_boxes(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows)
        if hdr:
            def drh(f, y):
                text(f.s, M, y, 300, [eyebrow(hdr[0], GR)], 'Column label')
                if hdr[1] and not amt: text(f.s, M + 250, y, 300, [eyebrow(hdr[1], GR)], 'Column label')
                if hdr[2]: text(f.s, M + CW - 176, y, 176, [eyebrow(hdr[2], GR, 'r')], 'Column label')
            us.append(U(14, drh, 20 if t else 44, keep=True))
        for k, (a, b, v) in enumerate(rows):
            col = DG if amt else GR
            if amt:
                AB = 176; LW = CW - AB; tw = LW - 48
                ps = [P(a, 'Montserrat', 14, WHITE, True, 1.3), body(b, 13.5, WHITE, before=4, lh=1.38)]
                vs = [P(v, 'Montserrat', 15, DG, True, 1.25, align='c')]
                h = max(measure(ps, tw), measure(vs, AB - 30)) + 48
                def dr(f, y, ps=ps, vs=vs, h=h, col=col, a=a, tw=tw):
                    rect(f.s, M, y, LW, h, col, 'Box: ' + a[:30])
                    rect(f.s, M + LW, y, AB, h, CREAM, 'Amount box')
                    text(f.s, M + 24, y + 24, tw, ps, a[:30], h=h - 48, anchor='m')
                    text(f.s, M + LW + 15, y + 24, AB - 30, vs, 'Amount', h=h - 48, anchor='m')
            else:
                LW = 250; rw = CW - LW - 48
                big = hdr and hdr[0] == 'Gift'
                lp = [P(a, 'Montserrat', 26 if big else 15, WHITE, True, 1.25, align='l')]
                rp = [body(b, 15, DG, lh=1.45)]
                h = max(measure(lp, LW - 48), measure(rp, rw)) + 44
                def dr(f, y, lp=lp, rp=rp, h=h, col=col, a=a, rw=rw):
                    rect(f.s, M, y, LW, h, col, 'Box: ' + a[:30])
                    rect(f.s, M + LW, y, CW - LW, h, CREAM, 'Response box')
                    text(f.s, M + 24, y + 22, LW - 48, lp, a[:30], h=h - 44, anchor='m')
                    text(f.s, M + LW + 24, y + 22, rw, rp, 'Response', h=h - 44, anchor='m')
            us.append(U(h, dr, (16 if amt else 12) if (k or hdr) else 20))
        return us
    def quote(self, f, t, a):
        ps = [P(t, 'EB Garamond', 24, WHITE, lh=1.32), dict(eyebrow(a, SPEC), before=14)]
        h = measure(ps, CW - 80) + 80
        def dr(f, y):
            rect(f.s, 0, y, W, h, BR, 'Quote band')
            text(f.s, M + 8, y + 40, CW - 80, ps, 'Quote')
        return [U(h, dr, 30)]
    def photo(self, f, path, fy, alt):
        def dr(f, y, room):
            pic(f.s, 'ph/' + path, 0, y, W, H - y, 'Photo: ' + alt, fy=fy)
            rect(f.s, 0, y, 16, H - y, GR, 'Photo edge bar')
        return [dict(h=0, flex=True, minh=150, gap=40, draw=dr)]
    def closing(self, f, doc):
        c = doc['closing']; s = f.d.page(WHITE)
        gh = give_h(c); gy = H - 60 - gh
        PB = 520 if closing_paras(c) else gy - 90
        pic(s, 'ph/' + c['photo'], 0, 0, W, PB, 'Photo: ' + c['alt'], fy=c['fy'])
        rect(s, 0, PB, W, H - PB, GR, 'Green box')
        rect(s, 0, PB, W, 12, BLUE, 'Blue strip')
        ps = closing_paras(c)
        if ps: text(s, M, 580, CW, ps, 'Goal and quote', h=gy - 34 - 580, anchor='m')
        hline(s, M, gy - 22, CW, '#4F9A5F')
        give_row(s, gy, c)

STYLES = [Editorial(), Cards(), Blocks()]
if __name__ == '__main__' and 'final' not in sys.argv:
    import os
    os.makedirs('out/variants', exist_ok=True)
    for st in STYLES:
        for doc in DOCS:
            n = build(st, doc, f"out/variants/SFW {doc['key']} - {st.name}.pptx")
            print(st.name, doc['key'], n, 'pages')

# =========================================================================== ONE THEME
class Theme(Editorial):
    name = 'Final'
    photo_gap = 20
    def heading(self, t, gap=30):
        ps = [P(t, 'EB Garamond', 40, GR, lh=1.15, align='c')]; h = measure(ps, CW)
        def dr(f, y): text(f.s, M, y, CW, ps, 'Heading: ' + t[:30]); hline(f.s, M, y + h + 8, CW, SAGE, 'Rule')
        return U(h + 9, dr, gap, keep=True)
    def section(self, f, t, paras):
        if not t and len(paras) == 2:
            lw, gp, rw = 292, 23, CW - 292 - 23
            L = [dict(body(paras[0], 16.5, lh=1.55), align='j')]; R = [dict(body(paras[1], 16.5, lh=1.55), align='j')]
            h = max(measure(L, lw), measure(R, rw))
            print('  text worst', round(h), 'brand', round(max(measure(L, lw, 0), measure(R, rw, 0))))
            return [U(h, lambda f, y: (text(f.s, M, y, lw, L, 'Text left'), text(f.s, M + lw + gp, y, rw, R, 'Text right')), 0)]
        if True:
            ps = [body(p, 16.5, before=14 if k else 0, lh=1.55) for k, p in enumerate(paras)]
            h = measure(ps, CW)
            us = [self.heading(t)] if t else []
            return us + [U(h, lambda f, y: text(f.s, M, y, CW, ps, 'Text'), 16 if t else (44 if t == '' else 30))]
        cw = (CW - 40) / 2
        L = [body(paras[0], 15)]; R = [body(p, 15, before=12 if k else 0) for k, p in enumerate(paras[1:])]
        h = max(measure(L, cw), measure(R, cw))
        return [U(h, lambda f, y: (text(f.s, M, y, cw, L, 'Text left'), text(f.s, M + cw + 40, y, cw, R, 'Text right')), 30)]
    def cover(self, f, doc):
        self.nrows = 0; Editorial.cover(self, f, doc)
    def grid(self, f, t, items):
        us = [self.heading(t)]
        cw = (CW - 14) / 2
        for r in range(0, len(items), 2):
            pair = items[r:r + 2]
            pss = [[P(a, 'EB Garamond', 22, WHITE, True, 1.2), body(b, 14.5, WHITE, before=0, lh=1.45)] for a, b in pair]
            h = max(measure(ps, cw - 48, 0) for ps in pss) + 46
            def dr(f, y, pss=pss, pair=pair, h=h):
                for k, ps in enumerate(pss):
                    x = M + k * (cw + 14)
                    rect(f.s, x, y, cw, h, DG, 'Box: ' + pair[k][0]); text(f.s, x + 24, y + 22, cw - 48, ps, pair[k][0][:-1])
            us.append(U(h, dr, 20 if r == 0 else 12))
        return us
    def list(self, f, t, items):
        us = [self.heading(t)]
        for k, x in enumerate(items):
            ps = [body(x, 16, lh=1.45)]; h = max(measure(ps, CW - 64), 34)
            def dr(f, y, ps=ps, k=k):
                text(f.s, M, y - 2, 50, [P(f'0{k + 1}', 'EB Garamond', 26, GR, lh=1.0)], 'Number', h=16 * 1.45 + 4, anchor='m')
                text(f.s, M + 64, y, CW - 64, ps, 'Text')
            us.append(U(h, dr, 24 if k == 0 else 18))
        return us
    def rows(self, f, t, hdr, rows):
        self.nrows += 1
        if hdr is None and not any(r[2] for r in rows):
            # label + text are one sentence: keep them together on one line
            hp = [P(t, 'EB Garamond', 40, WHITE, lh=1.15, align='c')]; hh = measure(hp, CW)
            def drh(f, y):
                top = y - 44
                png(f.s, 'el-hay.png', -2, top, W + 4, 'Hay swoosh element', max(620, H - top + 2))
                text(f.s, M, y + 20, CW, hp, 'Heading: ' + t)
            us = [U(hh + 20, drh, 50, keep=True)]
            LW = 214; RW = CW - 56 - LW - 24
            for k, (a, b, _) in enumerate(rows):
                lp = [P(a, 'EB Garamond', 16 / 0.75, GR, True, 1.2)]
                rp = [body(b[0].upper() + b[1:], 14 / 0.75, INK, lh=1.42)]
                h = max(measure(lp, LW), measure(rp, RW)) + 32
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, WHITE, 'Box: ' + a)
                    text(f.s, M + 28, y + 16, LW, lp, a, h=h - 32, anchor='m')
                    text(f.s, M + 28 + LW + 24, y + 16, RW, rp, 'Explanation', h=h - 32, anchor='m')
                us.append(U(h, dr, 24 if k == 0 else 10))
            return us
        if hdr and hdr[0] == 'Barriers to change':
            colw = [313, CW - 313]
            hd = [P(hdr[0], 'EB Garamond', 36, GR, True, 1.15), P(hdr[1], 'EB Garamond', 36, GR, True, 1.15)]
            rr = [hd] + [[P(a, 'Source Sans 3', 19, DG, True, 1.4), body(b, 19, lh=1.42)] for a, b, _ in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10, brand=True)
            print('  table brand', round(h))
            return [U(h, lambda f, y: (print('  table y', round(y), 'end', round(y + h)), table(f.s, M, y, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10), rect(f.s, -4, H - 72, W + 8, 76, '#9EA898', 'Footer band')), 32)]
        if hdr and hdr[0] == 'Priority':
            us = [self.heading(t)]
            colw = [204, CW - 204]
            rr = [[P(v.replace('Transformational gift', 'Transformational\ngift').replace('$10,000 to $100,000', '$10,000\nto $100,000'), 'EB Garamond', 23, GR, lh=1.15), [P(a, 'Source Sans 3', 17, DG, True, 1.5), body(b, 17, INK, lh=1.5)]] for a, b, v in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Top priorities', SAGE, 20, 24)
            us.append(U(h, lambda f, y: table(f.s, M, y, colw, rr, 'Table: Top priorities', SAGE, 20, 24), 6))
            print('  priorities table', round(h))
            return us
        if self.nrows % 2 == 1: return self.rows_cards(f, t, hdr, rows)
        return Editorial.rows(self, f, t, hdr, rows)
    def rows_cards(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows)
        PAD = 22
        if amt:
            AW = 170; tw = CW - 2 * PAD - AW - 20
        else:
            LW = 230; tw = CW - 2 * PAD - LW - 24
        if hdr:
            def drh(f, y):
                text(f.s, M, y, 300, [eyebrow(hdr[0])], 'Column label')
                if amt and hdr[2]: text(f.s, M + CW - PAD - AW, y, AW, [eyebrow(hdr[2], GR, 'r')], 'Column label')
                if not amt and hdr[1]: text(f.s, M + PAD + LW + 24, y, 300, [eyebrow(hdr[1])], 'Column label')
            us.append(U(16, drh, 18 if t else 32, keep=True))
        for k, (a, b, v) in enumerate(rows):
            if amt:
                ps = [P(a, 'Montserrat', 14.5, WHITE, True, 1.3), body(b, 14, WHITE, before=3, lh=1.42)]
                vs = [P(v, 'Montserrat', 15, WHITE, True, 1.3, align='r')]
                h = max(measure(ps, tw, 0), measure(vs, AW, 0)) + 2 * PAD
                def dr(f, y, ps=ps, vs=vs, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, tw, ps, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + CW - PAD - AW, y + PAD, AW, vs, 'Amount', h=h - 2 * PAD, anchor='m')
            else:
                lp = [P(a, 'Montserrat', 15, WHITE, True, 1.3)]; rp = [body(b, 14.5, WHITE, lh=1.45)]
                h = max(measure(lp, LW, 0), measure(rp, tw, 0)) + 2 * PAD
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, LW, lp, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + PAD + LW + 24, y + PAD, tw, rp, 'Response', h=h - 2 * PAD, anchor='m')
            us.append(U(h, dr, 14 if (k or hdr) else 14))
        return us
    def quote(self, f, t, a):
        ps = [P(t, 'EB Garamond', 23, WHITE, lh=1.35), P(a, 'Source Sans 3', 14, WHITE, True, 1.4, before=20)]
        h = (measure(ps, CW) + measure(ps, CW, 0)) / 2 + 96
        def dr(f, y):
            rect(f.s, 0, y, W, h, GR, 'Quote band'); text(f.s, M, y + 48, CW, ps, 'Quote', h=h - 96, anchor='m')
        return [U(h, dr, 30)]

from content import CASE as CASE_FULL
def _case_closing(self, f, doc):
    c = doc['closing']; s = f.d.page(DG)
    rh = lambda t, a='l': P(t, 'Montserrat', 17.33, LIV, True, 1.2, align=a)
    text(s, M, 44, 300, [rh('Soil Food Web Foundation')], 'Running head left')
    text(s, W - M - 300, 44, 300, [rh(doc['short'], 'r')], 'Running head right')
    gifts = [b for b in CASE_FULL['blocks'] if b[0] == 'rows' and b[2] and b[2][0] == 'Gift'][0]
    y = 100 + text(s, M, 100, CW, [P(gifts[1], 'EB Garamond', 36, WHITE, lh=1.15)], 'Heading') + 26
    hd = [P('Gift', 'EB Garamond', 20, LIV, True, 1.3), P('Impact', 'EB Garamond', 20, LIV, True, 1.3)]
    rows = [hd] + [[P(a, 'EB Garamond', 26, WHITE, lh=1.15), body(b, 15, WHITE, lh=1.45)] for a, b, _ in gifts[3]]
    y += table(s, M, y, [158, CW - 158], rows, 'Table: Gifts', OLIVE, 18, 24, 1, 6)
    # bottom block: rule, goal, QR + give text, logo
    g = [body(c['give'], 13.5, WHITE, lh=1.45)]
    tw = 420; gh = max(96, measure(g, tw)); gy = H - 44 - gh
    goal = [P(c['goal'], 'Montserrat', 20, WHITE, True, 1.3)]
    goy = gy - 22 - measure(goal, CW)
    ry = goy - 30
    hline(s, M, ry, CW, OLIVE)
    text(s, M, goy, CW, goal, 'Goal')
    q = round(measure(g, tw, 0))
    text(s, M + q + 24, gy, tw, g, 'Give today')
    png(s, 'qr-light.png', M, gy + 2, q - 4, 'QR code', q - 4)
    png(s, 'logo-white.png', W - M - 80, H - 44 - 69, 80, 'SFW logo white')
    # centred quote in the space between table and rule
    q = [P(c['quote'], 'EB Garamond', 26, WHITE, lh=1.4, align='c'), P(c['attr'], 'Montserrat', 15, LIV, False, 1.3, before=22, align='c')]
    qw = 560; qh = measure(q, qw)
    text(s, (W - qw) / 2, y + (ry - y - qh) / 2, qw, q, 'Evan quote')

from content import FUNDING as FUND_FULL
if __name__ == '__main__' and 'final' not in sys.argv:
    import os
    os.makedirs('out/variants', exist_ok=True)
    for st in STYLES:
        for doc in DOCS:
            n = build(st, doc, f"out/variants/SFW {doc['key']} - {st.name}.pptx")
            print(st.name, doc['key'], n, 'pages')

# =========================================================================== ONE THEME
class Theme(Editorial):
    name = 'Final'
    photo_gap = 20
    def heading(self, t, gap=30):
        ps = [P(t, 'EB Garamond', 40, GR, lh=1.15, align='c')]; h = measure(ps, CW)
        def dr(f, y): text(f.s, M, y, CW, ps, 'Heading: ' + t[:30]); hline(f.s, M, y + h + 8, CW, SAGE, 'Rule')
        return U(h + 9, dr, gap, keep=True)
    def section(self, f, t, paras):
        if not t and len(paras) == 2:
            lw, gp, rw = 292, 23, CW - 292 - 23
            L = [dict(body(paras[0], 16.5, lh=1.55), align='j')]; R = [dict(body(paras[1], 16.5, lh=1.55), align='j')]
            h = max(measure(L, lw), measure(R, rw))
            print('  text worst', round(h), 'brand', round(max(measure(L, lw, 0), measure(R, rw, 0))))
            return [U(h, lambda f, y: (text(f.s, M, y, lw, L, 'Text left'), text(f.s, M + lw + gp, y, rw, R, 'Text right')), 0)]
        if True:
            ps = [body(p, 16.5, before=14 if k else 0, lh=1.55) for k, p in enumerate(paras)]
            h = measure(ps, CW)
            us = [self.heading(t)] if t else []
            return us + [U(h, lambda f, y: text(f.s, M, y, CW, ps, 'Text'), 16 if t else (44 if t == '' else 30))]
        cw = (CW - 40) / 2
        L = [body(paras[0], 15)]; R = [body(p, 15, before=12 if k else 0) for k, p in enumerate(paras[1:])]
        h = max(measure(L, cw), measure(R, cw))
        return [U(h, lambda f, y: (text(f.s, M, y, cw, L, 'Text left'), text(f.s, M + cw + 40, y, cw, R, 'Text right')), 30)]
    def cover(self, f, doc):
        self.nrows = 0; Editorial.cover(self, f, doc)
    def grid(self, f, t, items):
        us = [self.heading(t)]
        cw = (CW - 14) / 2
        for r in range(0, len(items), 2):
            pair = items[r:r + 2]
            pss = [[P(a, 'EB Garamond', 22, WHITE, True, 1.2), body(b, 14.5, WHITE, before=0, lh=1.45)] for a, b in pair]
            h = max(measure(ps, cw - 48, 0) for ps in pss) + 46
            def dr(f, y, pss=pss, pair=pair, h=h):
                for k, ps in enumerate(pss):
                    x = M + k * (cw + 14)
                    rect(f.s, x, y, cw, h, DG, 'Box: ' + pair[k][0]); text(f.s, x + 24, y + 22, cw - 48, ps, pair[k][0][:-1])
            us.append(U(h, dr, 20 if r == 0 else 12))
        return us
    def list(self, f, t, items):
        us = [self.heading(t)]
        for k, x in enumerate(items):
            ps = [body(x, 16, lh=1.45)]; h = max(measure(ps, CW - 64), 34)
            def dr(f, y, ps=ps, k=k):
                text(f.s, M, y - 2, 50, [P(f'0{k + 1}', 'EB Garamond', 26, GR, lh=1.0)], 'Number', h=16 * 1.45 + 4, anchor='m')
                text(f.s, M + 64, y, CW - 64, ps, 'Text')
            us.append(U(h, dr, 24 if k == 0 else 18))
        return us
    def rows(self, f, t, hdr, rows):
        self.nrows += 1
        if hdr is None and not any(r[2] for r in rows):
            # label + text are one sentence: keep them together on one line
            hp = [P(t, 'EB Garamond', 40, WHITE, lh=1.15, align='c')]; hh = measure(hp, CW)
            def drh(f, y):
                top = y - 44
                png(f.s, 'el-hay.png', -2, top, W + 4, 'Hay swoosh element', max(620, H - top + 2))
                text(f.s, M, y + 20, CW, hp, 'Heading: ' + t)
            us = [U(hh + 20, drh, 50, keep=True)]
            LW = 214; RW = CW - 56 - LW - 24
            for k, (a, b, _) in enumerate(rows):
                lp = [P(a, 'EB Garamond', 16 / 0.75, GR, True, 1.2)]
                rp = [body(b[0].upper() + b[1:], 14 / 0.75, INK, lh=1.42)]
                h = max(measure(lp, LW), measure(rp, RW)) + 32
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, WHITE, 'Box: ' + a)
                    text(f.s, M + 28, y + 16, LW, lp, a, h=h - 32, anchor='m')
                    text(f.s, M + 28 + LW + 24, y + 16, RW, rp, 'Explanation', h=h - 32, anchor='m')
                us.append(U(h, dr, 24 if k == 0 else 10))
            return us
        if hdr and hdr[0] == 'Barriers to change':
            colw = [313, CW - 313]
            hd = [P(hdr[0], 'EB Garamond', 36, GR, True, 1.15), P(hdr[1], 'EB Garamond', 36, GR, True, 1.15)]
            rr = [hd] + [[P(a, 'Source Sans 3', 19, DG, True, 1.4), body(b, 19, lh=1.42)] for a, b, _ in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10, brand=True)
            print('  table brand', round(h))
            return [U(h, lambda f, y: (print('  table y', round(y), 'end', round(y + h)), table(f.s, M, y, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10), rect(f.s, -4, H - 72, W + 8, 76, '#9EA898', 'Footer band')), 32)]
        if hdr and hdr[0] == 'Priority':
            us = [self.heading(t)]
            colw = [204, CW - 204]
            rr = [[P(v.replace('Transformational gift', 'Transformational\ngift').replace('$10,000 to $100,000', '$10,000\nto $100,000'), 'EB Garamond', 23, GR, lh=1.15), [P(a, 'Source Sans 3', 17, DG, True, 1.5), body(b, 17, INK, lh=1.5)]] for a, b, v in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Top priorities', SAGE, 20, 24)
            us.append(U(h, lambda f, y: table(f.s, M, y, colw, rr, 'Table: Top priorities', SAGE, 20, 24), 6))
            print('  priorities table', round(h))
            return us
        if self.nrows % 2 == 1: return self.rows_cards(f, t, hdr, rows)
        return Editorial.rows(self, f, t, hdr, rows)
    def rows_cards(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows)
        PAD = 22
        if amt:
            AW = 170; tw = CW - 2 * PAD - AW - 20
        else:
            LW = 230; tw = CW - 2 * PAD - LW - 24
        if hdr:
            def drh(f, y):
                text(f.s, M, y, 300, [eyebrow(hdr[0])], 'Column label')
                if amt and hdr[2]: text(f.s, M + CW - PAD - AW, y, AW, [eyebrow(hdr[2], GR, 'r')], 'Column label')
                if not amt and hdr[1]: text(f.s, M + PAD + LW + 24, y, 300, [eyebrow(hdr[1])], 'Column label')
            us.append(U(16, drh, 18 if t else 32, keep=True))
        for k, (a, b, v) in enumerate(rows):
            if amt:
                ps = [P(a, 'Montserrat', 14.5, WHITE, True, 1.3), body(b, 14, WHITE, before=3, lh=1.42)]
                vs = [P(v, 'Montserrat', 15, WHITE, True, 1.3, align='r')]
                h = max(measure(ps, tw, 0), measure(vs, AW, 0)) + 2 * PAD
                def dr(f, y, ps=ps, vs=vs, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, tw, ps, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + CW - PAD - AW, y + PAD, AW, vs, 'Amount', h=h - 2 * PAD, anchor='m')
            else:
                lp = [P(a, 'Montserrat', 15, WHITE, True, 1.3)]; rp = [body(b, 14.5, WHITE, lh=1.45)]
                h = max(measure(lp, LW, 0), measure(rp, tw, 0)) + 2 * PAD
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, LW, lp, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + PAD + LW + 24, y + PAD, tw, rp, 'Response', h=h - 2 * PAD, anchor='m')
            us.append(U(h, dr, 14 if (k or hdr) else 14))
        return us
    def quote(self, f, t, a):
        ps = [P(t, 'EB Garamond', 23, WHITE, lh=1.35), P(a, 'Source Sans 3', 14, WHITE, True, 1.4, before=20)]
        h = (measure(ps, CW) + measure(ps, CW, 0)) / 2 + 96
        def dr(f, y):
            rect(f.s, 0, y, W, h, GR, 'Quote band'); text(f.s, M, y + 48, CW, ps, 'Quote', h=h - 96, anchor='m')
        return [U(h, dr, 30)]

from content import CASE as CASE_FULL
def _case_closing(self, f, doc):
    c = doc['closing']; s = f.d.page(DG)
    rh = lambda t, a='l': P(t, 'Montserrat', 17.33, LIV, True, 1.2, align=a)
    text(s, M, 44, 300, [rh('Soil Food Web Foundation')], 'Running head left')
    text(s, W - M - 300, 44, 300, [rh(doc['short'], 'r')], 'Running head right')
    gifts = [b for b in CASE_FULL['blocks'] if b[0] == 'rows' and b[2] and b[2][0] == 'Gift'][0]
    y = 100 + text(s, M, 100, CW, [P(gifts[1], 'EB Garamond', 36, WHITE, lh=1.15)], 'Heading') + 26
    hd = [P('Gift', 'EB Garamond', 20, LIV, True, 1.3), P('Impact', 'EB Garamond', 20, LIV, True, 1.3)]
    rows = [hd] + [[P(a, 'EB Garamond', 26, WHITE, lh=1.15), body(b, 15, WHITE, lh=1.45)] for a, b, _ in gifts[3]]
    y += table(s, M, y, [158, CW - 158], rows, 'Table: Gifts', OLIVE, 18, 24, 1, 6)
    # bottom block: rule, goal, QR + give text, logo
    g = [body(c['give'], 13.5, WHITE, lh=1.45)]
    tw = 420; gh = max(96, measure(g, tw)); gy = H - 44 - gh
    goal = [P(c['goal'], 'Montserrat', 20, WHITE, True, 1.3)]
    goy = gy - 22 - measure(goal, CW)
    ry = goy - 30
    hline(s, M, ry, CW, OLIVE)
    text(s, M, goy, CW, goal, 'Goal')
    q = round(measure(g, tw, 0))
    text(s, M + q + 24, gy, tw, g, 'Give today')
    png(s, 'qr-light.png', M, gy + 2, q - 4, 'QR code', q - 4)
    png(s, 'logo-white.png', W - M - 80, H - 44 - 69, 80, 'SFW logo white')
    # centred quote in the space between table and rule
    q = [P(c['quote'], 'EB Garamond', 26, WHITE, lh=1.4, align='c'), P(c['attr'], 'Montserrat', 15, LIV, False, 1.3, before=22, align='c')]
    qw = 560; qh = measure(q, qw)
    text(s, (W - qw) / 2, y + (ry - y - qh) / 2, qw, q, 'Evan quote')

from content import FUNDING as FUND_FULL
if __name__ == '__main__' and 'final' not in sys.argv:
    import os
    os.makedirs('out/variants', exist_ok=True)
    for st in STYLES:
        for doc in DOCS:
            n = build(st, doc, f"out/variants/SFW {doc['key']} - {st.name}.pptx")
            print(st.name, doc['key'], n, 'pages')

# =========================================================================== ONE THEME
class Theme(Editorial):
    name = 'Final'
    photo_gap = 20
    def heading(self, t, gap=30):
        ps = [P(t, 'EB Garamond', 40, GR, lh=1.15, align='c')]; h = measure(ps, CW)
        def dr(f, y): text(f.s, M, y, CW, ps, 'Heading: ' + t[:30]); hline(f.s, M, y + h + 8, CW, SAGE, 'Rule')
        return U(h + 9, dr, gap, keep=True)
    def section(self, f, t, paras):
        if not t and len(paras) == 2:
            lw, gp, rw = 292, 23, CW - 292 - 23
            L = [dict(body(paras[0], 16.5, lh=1.55), align='j')]; R = [dict(body(paras[1], 16.5, lh=1.55), align='j')]
            h = max(measure(L, lw), measure(R, rw))
            print('  text worst', round(h), 'brand', round(max(measure(L, lw, 0), measure(R, rw, 0))))
            return [U(h, lambda f, y: (text(f.s, M, y, lw, L, 'Text left'), text(f.s, M + lw + gp, y, rw, R, 'Text right')), 0)]
        if True:
            ps = [body(p, 16.5, before=14 if k else 0, lh=1.55) for k, p in enumerate(paras)]
            h = measure(ps, CW)
            us = [self.heading(t)] if t else []
            return us + [U(h, lambda f, y: text(f.s, M, y, CW, ps, 'Text'), 16 if t else (44 if t == '' else 30))]
        cw = (CW - 40) / 2
        L = [body(paras[0], 15)]; R = [body(p, 15, before=12 if k else 0) for k, p in enumerate(paras[1:])]
        h = max(measure(L, cw), measure(R, cw))
        return [U(h, lambda f, y: (text(f.s, M, y, cw, L, 'Text left'), text(f.s, M + cw + 40, y, cw, R, 'Text right')), 30)]
    def cover(self, f, doc):
        self.nrows = 0; Editorial.cover(self, f, doc)
    def grid(self, f, t, items):
        us = [self.heading(t)]
        cw = (CW - 14) / 2
        for r in range(0, len(items), 2):
            pair = items[r:r + 2]
            pss = [[P(a, 'EB Garamond', 22, WHITE, True, 1.2), body(b, 14.5, WHITE, before=0, lh=1.45)] for a, b in pair]
            h = max(measure(ps, cw - 48, 0) for ps in pss) + 46
            def dr(f, y, pss=pss, pair=pair, h=h):
                for k, ps in enumerate(pss):
                    x = M + k * (cw + 14)
                    rect(f.s, x, y, cw, h, DG, 'Box: ' + pair[k][0]); text(f.s, x + 24, y + 22, cw - 48, ps, pair[k][0][:-1])
            us.append(U(h, dr, 20 if r == 0 else 12))
        return us
    def list(self, f, t, items):
        us = [self.heading(t)]
        for k, x in enumerate(items):
            ps = [body(x, 16, lh=1.45)]; h = max(measure(ps, CW - 64), 34)
            def dr(f, y, ps=ps, k=k):
                text(f.s, M, y - 2, 50, [P(f'0{k + 1}', 'EB Garamond', 26, GR, lh=1.0)], 'Number', h=16 * 1.45 + 4, anchor='m')
                text(f.s, M + 64, y, CW - 64, ps, 'Text')
            us.append(U(h, dr, 24 if k == 0 else 18))
        return us
    def rows(self, f, t, hdr, rows):
        self.nrows += 1
        if hdr is None and not any(r[2] for r in rows):
            # label + text are one sentence: keep them together on one line
            hp = [P(t, 'EB Garamond', 40, WHITE, lh=1.15, align='c')]; hh = measure(hp, CW)
            def drh(f, y):
                top = y - 44
                png(f.s, 'el-hay.png', -2, top, W + 4, 'Hay swoosh element', max(620, H - top + 2))
                text(f.s, M, y + 20, CW, hp, 'Heading: ' + t)
            us = [U(hh + 20, drh, 50, keep=True)]
            LW = 214; RW = CW - 56 - LW - 24
            for k, (a, b, _) in enumerate(rows):
                lp = [P(a, 'EB Garamond', 16 / 0.75, GR, True, 1.2)]
                rp = [body(b[0].upper() + b[1:], 14 / 0.75, INK, lh=1.42)]
                h = max(measure(lp, LW), measure(rp, RW)) + 32
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, WHITE, 'Box: ' + a)
                    text(f.s, M + 28, y + 16, LW, lp, a, h=h - 32, anchor='m')
                    text(f.s, M + 28 + LW + 24, y + 16, RW, rp, 'Explanation', h=h - 32, anchor='m')
                us.append(U(h, dr, 24 if k == 0 else 10))
            return us
        if hdr and hdr[0] == 'Barriers to change':
            colw = [313, CW - 313]
            hd = [P(hdr[0], 'EB Garamond', 36, GR, True, 1.15), P(hdr[1], 'EB Garamond', 36, GR, True, 1.15)]
            rr = [hd] + [[P(a, 'Source Sans 3', 19, DG, True, 1.4), body(b, 19, lh=1.42)] for a, b, _ in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10, brand=True)
            print('  table brand', round(h))
            return [U(h, lambda f, y: (print('  table y', round(y), 'end', round(y + h)), table(f.s, M, y, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10), rect(f.s, -4, H - 72, W + 8, 76, '#9EA898', 'Footer band')), 32)]
        if hdr and hdr[0] == 'Priority':
            us = [self.heading(t)]
            colw = [204, CW - 204]
            rr = [[P(v.replace('Transformational gift', 'Transformational\ngift').replace('$10,000 to $100,000', '$10,000\nto $100,000'), 'EB Garamond', 23, GR, lh=1.15), [P(a, 'Source Sans 3', 17, DG, True, 1.5), body(b, 17, INK, lh=1.5)]] for a, b, v in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Top priorities', SAGE, 20, 24)
            us.append(U(h, lambda f, y: table(f.s, M, y, colw, rr, 'Table: Top priorities', SAGE, 20, 24), 6))
            print('  priorities table', round(h))
            return us
        if self.nrows % 2 == 1: return self.rows_cards(f, t, hdr, rows)
        return Editorial.rows(self, f, t, hdr, rows)
    def rows_cards(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows)
        PAD = 22
        if amt:
            AW = 170; tw = CW - 2 * PAD - AW - 20
        else:
            LW = 230; tw = CW - 2 * PAD - LW - 24
        if hdr:
            def drh(f, y):
                text(f.s, M, y, 300, [eyebrow(hdr[0])], 'Column label')
                if amt and hdr[2]: text(f.s, M + CW - PAD - AW, y, AW, [eyebrow(hdr[2], GR, 'r')], 'Column label')
                if not amt and hdr[1]: text(f.s, M + PAD + LW + 24, y, 300, [eyebrow(hdr[1])], 'Column label')
            us.append(U(16, drh, 18 if t else 32, keep=True))
        for k, (a, b, v) in enumerate(rows):
            if amt:
                ps = [P(a, 'Montserrat', 14.5, WHITE, True, 1.3), body(b, 14, WHITE, before=3, lh=1.42)]
                vs = [P(v, 'Montserrat', 15, WHITE, True, 1.3, align='r')]
                h = max(measure(ps, tw, 0), measure(vs, AW, 0)) + 2 * PAD
                def dr(f, y, ps=ps, vs=vs, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, tw, ps, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + CW - PAD - AW, y + PAD, AW, vs, 'Amount', h=h - 2 * PAD, anchor='m')
            else:
                lp = [P(a, 'Montserrat', 15, WHITE, True, 1.3)]; rp = [body(b, 14.5, WHITE, lh=1.45)]
                h = max(measure(lp, LW, 0), measure(rp, tw, 0)) + 2 * PAD
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, LW, lp, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + PAD + LW + 24, y + PAD, tw, rp, 'Response', h=h - 2 * PAD, anchor='m')
            us.append(U(h, dr, 14 if (k or hdr) else 14))
        return us
    def quote(self, f, t, a):
        ps = [P(t, 'EB Garamond', 23, WHITE, lh=1.35), P(a, 'Source Sans 3', 14, WHITE, True, 1.4, before=20)]
        h = (measure(ps, CW) + measure(ps, CW, 0)) / 2 + 96
        def dr(f, y):
            rect(f.s, 0, y, W, h, GR, 'Quote band'); text(f.s, M, y + 48, CW, ps, 'Quote', h=h - 96, anchor='m')
        return [U(h, dr, 30)]

from content import CASE as CASE_FULL
def _case_closing(self, f, doc):
    c = doc['closing']; s = f.d.page(DG)
    rh = lambda t, a='l': P(t, 'Montserrat', 17.33, LIV, True, 1.2, align=a)
    text(s, M, 44, 300, [rh('Soil Food Web Foundation')], 'Running head left')
    text(s, W - M - 300, 44, 300, [rh(doc['short'], 'r')], 'Running head right')
    gifts = [b for b in CASE_FULL['blocks'] if b[0] == 'rows' and b[2] and b[2][0] == 'Gift'][0]
    y = 100 + text(s, M, 100, CW, [P(gifts[1], 'EB Garamond', 36, WHITE, lh=1.15)], 'Heading') + 26
    hd = [P('Gift', 'EB Garamond', 20, LIV, True, 1.3), P('Impact', 'EB Garamond', 20, LIV, True, 1.3)]
    rows = [hd] + [[P(a, 'EB Garamond', 26, WHITE, lh=1.15), body(b, 15, WHITE, lh=1.45)] for a, b, _ in gifts[3]]
    y += table(s, M, y, [158, CW - 158], rows, 'Table: Gifts', OLIVE, 18, 24, 1, 6)
    # bottom block: rule, goal, QR + give text, logo
    g = [body(c['give'], 13.5, WHITE, lh=1.45)]
    tw = 420; gh = max(96, measure(g, tw)); gy = H - 44 - gh
    goal = [P(c['goal'], 'Montserrat', 20, WHITE, True, 1.3)]
    goy = gy - 22 - measure(goal, CW)
    ry = goy - 30
    hline(s, M, ry, CW, OLIVE)
    text(s, M, goy, CW, goal, 'Goal')
    q = round(measure(g, tw, 0))
    text(s, M + q + 24, gy, tw, g, 'Give today')
    png(s, 'qr-light.png', M, gy + 2, q - 4, 'QR code', q - 4)
    png(s, 'logo-white.png', W - M - 80, H - 44 - 69, 80, 'SFW logo white')
    # centred quote in the space between table and rule
    q = [P(c['quote'], 'EB Garamond', 26, WHITE, lh=1.4, align='c'), P(c['attr'], 'Montserrat', 15, LIV, False, 1.3, before=22, align='c')]
    qw = 560; qh = measure(q, qw)
    text(s, (W - qw) / 2, y + (ry - y - qh) / 2, qw, q, 'Evan quote')

from content import FUNDING as FUND_FULL
if __name__ == '__main__' and 'final' not in sys.argv:
    import os
    os.makedirs('out/variants', exist_ok=True)
    for st in STYLES:
        for doc in DOCS:
            n = build(st, doc, f"out/variants/SFW {doc['key']} - {st.name}.pptx")
            print(st.name, doc['key'], n, 'pages')

# =========================================================================== ONE THEME

def grad_band(h):
    """soft brand-green fade: light green on the left fading to white on the right"""
    from PIL import Image as _I
    w = 1640; hh = h * 2
    im = _I.new('RGB', (w, hh))
    a = (226, 232, 211); b = (255, 255, 255)
    px = im.load()
    for x in range(w):
        t = x / (w - 1); t = t * t * (3 - 2 * t)
        col = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
        for y in range(hh): px[x, y] = col
    p = f'/tmp/grad-{h}.png'; im.save(p); return p

class Theme(Editorial):
    name = 'Final'
    photo_gap = 20
    def heading(self, t, gap=30):
        ps = [P(t, 'EB Garamond', 40, GR, lh=1.15, align='c')]; h = measure(ps, CW)
        def dr(f, y): text(f.s, M, y, CW, ps, 'Heading: ' + t[:30]); hline(f.s, M, y + h + 8, CW, SAGE, 'Rule')
        return U(h + 9, dr, gap, keep=True)
    def section(self, f, t, paras):
        if t is None and len(paras) == 2:
            lw, gp, rw = 292, 23, CW - 292 - 23
            L = [body(paras[0], 16.5, lh=1.55)]; R = [body(paras[1], 16.5, lh=1.55)]
            h = max(measure(L, lw, 0), measure(R, rw, 0))
            print('  text worst', round(h), 'brand', round(max(measure(L, lw, 0), measure(R, rw, 0))))
            return [U(h, lambda f, y: (text(f.s, M, y, lw, L, 'Text left'), text(f.s, M + lw + gp, y, rw, R, 'Text right')), 0)]
        if True:
            ps = [body(p, getattr(self, 'body_px', 16.5), before=14 if k else 0, lh=1.46 if getattr(self, 'body_px', 16.5) < 16 else 1.55) for k, p in enumerate(paras)]
            h = measure(ps, CW, 0)
            us = [self.heading(t)] if t else []
            return us + [U(h, lambda f, y: text(f.s, M, y, CW, ps, 'Text'), 16 if t else (36 if t == '' else 30))]
        cw = (CW - 40) / 2
        L = [body(paras[0], 15)]; R = [body(p, 15, before=12 if k else 0) for k, p in enumerate(paras[1:])]
        h = max(measure(L, cw), measure(R, cw))
        return [U(h, lambda f, y: (text(f.s, M, y, cw, L, 'Text left'), text(f.s, M + cw + 40, y, cw, R, 'Text right')), 30)]
    def cover(self, f, doc):
        self.nrows = 0; Editorial.cover(self, f, doc)
    def grid(self, f, t, items):
        us = [self.heading(t)]
        cw = (CW - 14) / 2
        for r in range(0, len(items), 2):
            pair = items[r:r + 2]
            pss = [[P(a, 'EB Garamond', 22, WHITE, True, 1.2), body(b, 14.5, WHITE, before=0, lh=1.45)] for a, b in pair]
            h = max(measure(ps, cw - 48, 0) for ps in pss) + 46
            def dr(f, y, pss=pss, pair=pair, h=h):
                for k, ps in enumerate(pss):
                    x = M + k * (cw + 14)
                    rect(f.s, x, y, cw, h, DG, 'Box: ' + pair[k][0]); text(f.s, x + 24, y + 22, cw - 48, ps, pair[k][0][:-1])
            us.append(U(h, dr, 20 if r == 0 else 12))
        return us
    def list(self, f, t, items):
        us = [self.heading(t)]
        for k, x in enumerate(items):
            ps = [body(x, 16, lh=1.45)]; h = max(measure(ps, CW - 64), 34)
            def dr(f, y, ps=ps, k=k):
                text(f.s, M, y - 2, 50, [P(f'0{k + 1}', 'EB Garamond', 26, GR, lh=1.0)], 'Number', h=16 * 1.45 + 4, anchor='m')
                text(f.s, M + 64, y, CW - 64, ps, 'Text')
            us.append(U(h, dr, 24 if k == 0 else 18))
        return us
    def rows(self, f, t, hdr, rows):
        self.nrows += 1
        if hdr is None and not any(r[2] for r in rows):
            # label + text are one sentence: keep them together on one line
            hp = [P(t, 'EB Garamond', 40, WHITE, lh=1.15, align='c')]; hh = measure(hp, CW)
            def drh(f, y):
                top = y - 44
                png(f.s, 'el-hay.png', -2, top, W + 4, 'Hay swoosh element', max(620, H - top + 2))
                text(f.s, M, y + 20, CW, hp, 'Heading: ' + t)
            us = [U(hh + 20, drh, 50, keep=True)]
            LW = 214; RW = CW - 56 - LW - 24
            for k, (a, b, _) in enumerate(rows):
                lp = [P(a, 'EB Garamond', 16 / 0.75, GR, True, 1.2)]
                rp = [body(b[0].upper() + b[1:], 14 / 0.75, INK, lh=1.42)]
                h = max(measure(lp, LW), measure(rp, RW)) + 32
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, WHITE, 'Box: ' + a)
                    text(f.s, M + 28, y + 16, LW, lp, a, h=h - 32, anchor='m')
                    text(f.s, M + 28 + LW + 24, y + 16, RW, rp, 'Explanation', h=h - 32, anchor='m')
                us.append(U(h, dr, 24 if k == 0 else 10))
            return us
        if hdr and hdr[0] == 'Barriers to change':
            colw = [313, CW - 313]
            hd = [P(hdr[0], 'EB Garamond', 36, GR, True, 1.15), P(hdr[1], 'EB Garamond', 36, GR, True, 1.15)]
            rr = [hd] + [[P(a, 'Source Sans 3', 19, DG, True, 1.4), body(b, 19, lh=1.42)] for a, b, _ in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10, brand=True)
            print('  table brand', round(h))
            return [U(h, lambda f, y: (print('  table y', round(y), 'end', round(y + h)), table(f.s, M, y, colw, rr, 'Table: Barriers', SAGE, 14, 24, 1, 10), rect(f.s, -4, H - 72, W + 8, 76, '#9EA898', 'Footer band')), 32)]
        if hdr and hdr[0] == 'Priority':
            us = [self.heading(t)]
            colw = [204, CW - 204]
            rr = [[P(v.replace('Transformational gift', 'Transformational\ngift').replace('$10,000 to $100,000', '$10,000\nto $100,000'), 'EB Garamond', 23, GR, lh=1.15), [P(a, 'Source Sans 3', 17, DG, True, 1.5), body(b, 17, INK, lh=1.5)]] for a, b, v in rows]
            scratch = Deck().page()
            h = table(scratch, 0, 0, colw, rr, 'Table: Top priorities', SAGE, 20, 24)
            us.append(U(h, lambda f, y: table(f.s, M, y, colw, rr, 'Table: Top priorities', SAGE, 20, 24), 6))
            print('  priorities table', round(h))
            return us
        if self.nrows % 2 == 1: return self.rows_cards(f, t, hdr, rows)
        return Editorial.rows(self, f, t, hdr, rows)
    def rows_cards(self, f, t, hdr, rows):
        us = [self.heading(t)] if t else []
        amt = any(r[2] for r in rows)
        PAD = 22
        if amt:
            AW = 170; tw = CW - 2 * PAD - AW - 20
        else:
            LW = 230; tw = CW - 2 * PAD - LW - 24
        if hdr:
            def drh(f, y):
                text(f.s, M, y, 300, [eyebrow(hdr[0])], 'Column label')
                if amt and hdr[2]: text(f.s, M + CW - PAD - AW, y, AW, [eyebrow(hdr[2], GR, 'r')], 'Column label')
                if not amt and hdr[1]: text(f.s, M + PAD + LW + 24, y, 300, [eyebrow(hdr[1])], 'Column label')
            us.append(U(16, drh, 18 if t else 32, keep=True))
        for k, (a, b, v) in enumerate(rows):
            if amt:
                ps = [P(a, 'Montserrat', 14.5, WHITE, True, 1.3), body(b, 14, WHITE, before=3, lh=1.42)]
                vs = [P(v, 'Montserrat', 15, WHITE, True, 1.3, align='r')]
                h = max(measure(ps, tw, 0), measure(vs, AW, 0)) + 2 * PAD
                def dr(f, y, ps=ps, vs=vs, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, tw, ps, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + CW - PAD - AW, y + PAD, AW, vs, 'Amount', h=h - 2 * PAD, anchor='m')
            else:
                lp = [P(a, 'Montserrat', 15, WHITE, True, 1.3)]; rp = [body(b, 14.5, WHITE, lh=1.45)]
                h = max(measure(lp, LW, 0), measure(rp, tw, 0)) + 2 * PAD
                def dr(f, y, lp=lp, rp=rp, h=h, a=a):
                    rect(f.s, M, y, CW, h, DG, 'Box: ' + a[:30])
                    text(f.s, M + PAD, y + PAD, LW, lp, a[:30], h=h - 2 * PAD, anchor='m')
                    text(f.s, M + PAD + LW + 24, y + PAD, tw, rp, 'Response', h=h - 2 * PAD, anchor='m')
            us.append(U(h, dr, 14 if (k or hdr) else 14))
        return us
    def pullquote(self, f, t, a):
        QX = 52; w = CW - QX
        qp = [P(t, 'EB Garamond', 22, GR, lh=1.3)]; ap = [P(a, 'Source Sans 3', 14, GR, True, 1.35)]
        qh = measure(qp, w, 0); ah = measure(ap, w, 0); h = qh + 10 + ah
        def dr(f, y):
            png(f.s, grad_band(round(h + 48)), -2, y - 24, W + 4, 'Quote background fade', h + 48)
            png(f.s, 'brandq-green.png', M, y + 4, 34, 'Quote mark')
            text(f.s, M + QX, y, w, qp, 'Leslie quote')
            text(f.s, M + QX, y + qh + 10, w, ap, 'Quote attribution')
        return [U(h, dr, 34)]
    def quote(self, f, t, a):
        ps = [P(t, 'EB Garamond', 23, WHITE, lh=1.35), P(a, 'Source Sans 3', 14, WHITE, True, 1.4, before=20)]
        h = (measure(ps, CW) + measure(ps, CW, 0)) / 2 + 96
        def dr(f, y):
            rect(f.s, 0, y, W, h, GR, 'Quote band'); text(f.s, M, y + 48, CW, ps, 'Quote', h=h - 96, anchor='m')
        return [U(h, dr, 30)]

from content import CASE as CASE_FULL
def _case_closing(self, f, doc):
    c = doc['closing']; s = f.d.page(DG)
    rh = lambda t, a='l': P(t, 'Montserrat', 17.33, LIV, True, 1.2, align=a)
    text(s, M, 44, 300, [rh('Soil Food Web Foundation')], 'Running head left')
    text(s, W - M - 300, 44, 300, [rh(doc['short'], 'r')], 'Running head right')
    gifts = [b for b in CASE_FULL['blocks'] if b[0] == 'rows' and b[2] and b[2][0] == 'Gift'][0]
    y = 100 + text(s, M, 100, CW, [P(gifts[1], 'EB Garamond', 36, WHITE, lh=1.15)], 'Heading') + 26
    hd = [P('Gift', 'EB Garamond', 20, LIV, True, 1.3), P('Impact', 'EB Garamond', 20, LIV, True, 1.3)]
    rows = [hd] + [[P(a, 'EB Garamond', 26, WHITE, lh=1.15), body(b, 15, WHITE, lh=1.45)] for a, b, _ in gifts[3]]
    y += table(s, M, y, [158, CW - 158], rows, 'Table: Gifts', OLIVE, 18, 24, 1, 6)
    # bottom block: rule, goal, QR + give text, logo
    g = [body(c['give'], 13.5, WHITE, lh=1.45)]
    tw = 420; gh = max(96, measure(g, tw)); gy = H - 44 - gh
    goal = [P(c['goal'], 'Montserrat', 20, WHITE, True, 1.3)]
    goy = gy - 22 - measure(goal, CW)
    ry = goy - 30
    hline(s, M, ry, CW, OLIVE)
    text(s, M, goy, CW, goal, 'Goal')
    q = round(measure(g, tw, 0))
    text(s, M + q + 24, gy, tw, g, 'Give today')
    png(s, 'qr-light.png', M, gy + 2, q - 4, 'QR code', q - 4)
    png(s, 'logo-white.png', W - M - 80, H - 44 - 69, 80, 'SFW logo white')
    # centred quote in the space between table and rule
    q = [P(c['quote'], 'EB Garamond', 26, WHITE, lh=1.4, align='c'), P(c['attr'], 'Montserrat', 15, LIV, False, 1.3, before=22, align='c')]
    qw = 560; qh = measure(q, qw)
    text(s, (W - qw) / 2, y + (ry - y - qh) / 2, qw, q, 'Evan quote')

from content import FUNDING as FUND_FULL

# ---- shared footer, Linnea's final Donor Overview design (Nov 15)
BAND_H = 192
def footer_band(s, lines, legal=None, size=15, tw=404, legal_col=None):
    by = H - BAND_H - (76 if legal else 0)
    rect(s, -4, by, W + 8, (BAND_H if legal else BAND_H + 4), GR, 'Footer band')
    g = [body(x, size, WHITE, lh=1.5) for x in lines]
    q = round(measure(g, tw, 0))
    y = by + (BAND_H - q) / 2
    png(s, 'qr-white.png', M, y, q, 'QR code', q)
    text(s, M + q + 28, y - 2, tw, g, 'Give online and contact')
    lh = 100; lw = round(lh * 464 / 403)
    png(s, 'logo-white.png', W - M - lw, by + (BAND_H - lh) / 2, lw, 'SFW logo', lh)
    if legal:
        ly = by + BAND_H
        lp = [P(legal, 'Source Sans 3', 13, legal_col or WHITE, lh=1.4, align='c')]
        text(s, M - 20, ly + (H - ly - measure(lp, CW + 40, 0)) / 2, CW + 40, lp, 'Legal line')
    return by

def heads(s, doc):
    rh = lambda t, a='l': P(t, 'Montserrat', 17.33, LIV, True, 1.2, align=a)
    text(s, M, 44, 300, [rh('Soil Food Web Foundation')], 'Running head left')
    text(s, W - M - 300, 44, 300, [rh(doc['short'], 'r')], 'Running head right')

def fill_table(s, y, cw, rows, name, bottom, lo=10, hi=30, rulew=1, rule=OLIVE, mid=False):
    pad = lo
    while pad < hi and table(Deck().page(), 0, 0, cw, rows, 'x', rule, pad + 1, 24, rulew, brand=True) <= bottom - y: pad += 1
    table(s, M, y, cw, rows, name, rule, pad, 24, rulew, mid=mid)
    return y + table(Deck().page(), 0, 0, cw, rows, 'x', rule, pad, 24, rulew, brand=True), pad

def goal_badge(s, goal, x, y, D):
    """goal as a round emblem: words kept exactly, split over three lines"""
    m = re.match(r'(GOAL: RAISE) (\$[\d,]+) (BY .*)', goal); assert m and ' '.join(m.groups()) == goal
    grp = s.shapes.add_group_shape(); grp.name = 'Goal badge'; g = _G(grp)
    c1 = g.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(y), E(D), E(D)); c1.fill.solid(); c1.fill.fore_color.rgb = rgb(GR); c1.line.fill.background(); c1.name = 'Badge circle'
    k = 12
    c2 = g.shapes.add_shape(MSO_SHAPE.OVAL, E(x + k), E(y + k), E(D - 2 * k), E(D - 2 * k)); c2.fill.background(); c2.line.color.rgb = rgb(LIV); c2.line.width = E(1.5); c2.name = 'Badge ring'
    for sh in (c1, c2):
        st = sh._element.find(qn('p:style'))
        if st is not None: sh._element.remove(st)
    a = [P(m.group(1), 'Montserrat', 16, LIV, True, 1.2, align='c')]
    b = [P(m.group(2), 'EB Garamond', 52, WHITE, lh=1.0, align='c')]
    d = [P(m.group(3), 'Montserrat', 13, LIV, True, 1.3, align='c')]
    ha, hb, hd = measure(a, D, 0), measure(b, D, 0), measure(d, D - 60, 0)
    tot = ha + 6 + hb + 8 + hd; yy = y + (D - tot) / 2
    text(g, x, yy, D, a, 'Goal: raise'); yy += ha + 6
    text(g, x, yy, D, b, 'Goal amount'); yy += hb + 8
    text(g, x + 30, yy, D - 60, d, 'Goal date')

def quote_page(f, quote, attr):
    s = f.d.page(LIV)
    qp = [P(quote, 'EB Garamond', 56, DG, lh=1.18)]
    ap = [P(attr, 'Source Sans 3', 20, DG, True, 1.3)]
    QW = CW - 40
    qh = measure(qp, QW, 0); ah = measure(ap, QW, 0)
    y = (H - qh - 70 - ah) / 2
    text(s, M, y, QW, qp, 'Evan quote')
    text(s, M, y + qh + 70, QW, ap, 'Quote attribution')
    lh = 104; lw = round(lh * 464 / 403)
    png(s, 'logo-white.png', W - M - lw, H - M - lh, lw, 'SFW logo', lh)

def curved_photo(path, w, h, fy, amp=20, phase=0.4, edge_y=None):
    """photo with its bottom cut along the brand wave curve (transparent below), baked so Canva keeps it"""
    from PIL import Image as _I, ImageDraw as _D
    sc = 2
    im = _I.open(path).convert('RGB'); iw, ih = im.size; ar = w / h
    if iw / ih > ar: nw = int(ih * ar); im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(iw / ar); y0 = int((ih - nh) * fy); im = im.crop((0, y0, iw, y0 + nh))
    im = im.resize((int(w * sc), int(h * sc)), _I.LANCZOS).convert('RGBA')
    mask = _I.new('L', im.size, 0); dr = _D.Draw(mask)
    ey = edge_y if edge_y is not None else h - amp - 4
    pts = [(x * sc, (ey + amp * math.sin((x / W) * math.pi * 1.15 + phase)) * sc) for x in range(0, int(w) + 9, 4)]
    dr.polygon([(0, 0), (w * sc, 0)] + list(reversed(pts)), fill=255)
    im.putalpha(mask)
    p = f'/tmp/curved-{abs(hash(path)) % 10000}-{int(h)}.png'; im.save(p); return p, ey

def green_qr():
    from PIL import Image as _I
    im = _I.open('qr-light.png').convert('RGBA'); a = im.split()[3]
    g = _I.new('RGBA', im.size, (21, 104, 38, 255)); g.putalpha(a)
    g.save('/tmp/qr-green.png'); return '/tmp/qr-green.png'

def _case_closing(self, f, doc):
    c = doc['closing']
    quote_page(f, c['quote'], c['attr'])
    s = f.d.page(WHITE)
    gifts = [b for b in CASE_FULL['blocks'] if b[0] == 'rows' and b[2] and b[2][0] == 'Gift'][0]
    lines = ['Give today at soilfoodweb.com/donations or scan the QR code.',
             'One-time gifts, monthly giving, sponsorships, and legacy gifts.',
             'For customized giving, contact Evan Buckman,',
             'Executive Director, at evan@soilfoodweb.com or (512) 359-5206.']
    legal = '501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.'
    assert ' '.join(lines + [legal]) == c['give'], 'give text changed'
    PH = 290; amp = 20; phase = 0.4
    p, ey = curved_photo('ph/arms-up.jpg', W + 6, PH, 0.14, amp, phase)
    ph_ = s.shapes.add_picture(p, E(-3), E(-3), E(W + 6), E(PH)); ph_.name = 'Photo: Celebrating a finished compost pile'
    swoosh(s, ey - 3 - 2, GR, 5, 'Green swoosh line', amp=amp, phase=phase)
    g = [body(x, 15, INK, lh=1.5) for x in lines]
    tw = 404; q = round(measure(g, tw, 0))
    lp = [P(legal, 'Source Sans 3', 13, INK, lh=1.4)]
    lh_ = measure(lp, CW, 0)
    BH = q + 64; by = H - 48 - lh_ - 18 - BH
    png(s, grad_band(round(BH)), -2, by, W + 4, 'Contact background fade', BH)
    png(s, green_qr(), M, by + 32, q, 'QR code', q)
    text(s, M + q + 28, by + 30, tw, g, 'Give online and contact')
    lgh = 96; lgw = round(lgh * 464 / 403)
    png(s, 'logo.png', W - M - lgw, by + (BH - lgh) / 2, lgw, 'SFW logo', lgh)
    text(s, M, by + BH + 18, CW, lp, 'Legal line')
    D = 236
    bx, byy = W - M - D + 8, ey - 30
    hp = [P(gifts[1], 'EB Garamond', 40, GR, lh=1.15)]
    hy = PH + 24; text(s, M, hy, CW - D - 20, hp, 'Heading: ' + gifts[1])
    y = max(hy + measure(hp, CW - D - 20, 0), byy + D) + 18
    hd = [P('Gift', 'Source Sans 3', 16, GR, True, 1.3), P('Impact', 'Source Sans 3', 16, GR, True, 1.3)]
    rows = [hd] + [[P(a, 'EB Garamond', 28, GR, lh=1.15), body(b, 17, INK, lh=1.45)] for a, b, _ in gifts[3]]
    y, pad = fill_table(s, y, [170, CW - 170], rows, 'Table: Gifts', by - 36, 10, 22, rule=SAGE)
    goal_badge(s, c['goal'], bx, byy, D)
    print('  case closing table end', round(y), 'pad', pad, 'contact top', round(by))


def _fund_closing(self, f, doc):
    """same structure as the Case for Support closing: curved photo, table on white, contact on a soft fade"""
    c = doc['closing']; s = f.d.page(WHITE)
    mw = [b for b in FUND_FULL['blocks'] if b[0] == 'rows' and b[1] == 'More ways to invest'][0]
    lines = c['give'].replace('Evan Buckman, Executive', 'Evan Buckman,\nExecutive').replace(' · ', '\n').split('\n')
    PH = 250; amp = 20; phase = 0.4
    p, ey = curved_photo('ph/shed.jpg', W + 6, PH, 0.55, amp, phase)
    ph_ = s.shapes.add_picture(p, E(-3), E(-3), E(W + 6), E(PH)); ph_.name = 'Photo: Workshop group under a shed in India'
    swoosh(s, ey - 3 - 2, GR, 5, 'Green swoosh line', amp=amp, phase=phase)
    # contact block on the soft light green fade, same as Case for Support
    g = [body(x, 15, INK, lh=1.5) for x in lines]
    tw = 404; q = round(measure(g, tw, 0))
    BH = q + 64; by = H - 40 - BH
    png(s, grad_band(round(BH)), -2, by, W + 4, 'Contact background fade', BH)
    png(s, green_qr(), M, by + 32, q, 'QR code', q)
    text(s, M + q + 28, by + 30, tw, g, 'Give online and contact')
    lgh = 96; lgw = round(lgh * 464 / 403)
    png(s, 'logo.png', W - M - lgw, by + (BH - lgh) / 2, lgw, 'SFW logo', lgh)
    hp = [P(mw[1], 'EB Garamond', 40, GR, lh=1.15)]
    y = PH + 20; text(s, M, y, CW, hp, 'Heading: ' + mw[1]); y += measure(hp, CW, 0) + 22
    hd = [P(x, 'Source Sans 3', 16, GR, True, 1.3) for x in mw[2]]
    cw = [200, CW - 200 - 176, 176]
    grp = s.shapes.add_group_shape(); grp.name = 'Column labels'; gg = _G(grp)
    x = M
    for k, p_ in enumerate(hd):
        text(gg, x, y, cw[k] - 24, [p_], 'Column label: ' + p_['t']); x += cw[k]
    y += measure([hd[0]], 200, 0) + 10
    hline(s, M, y, CW, SAGE, 'Label rule')
    rows = [[P(a, 'Source Sans 3', 17, DG, True, 1.35), body(b, 16, INK, lh=1.4), P(v, 'EB Garamond', 21, GR, lh=1.2)] for a, b, v in mw[3]]
    y, pad = fill_table(s, y, cw, rows, 'Table: More ways to invest', by - 30, 8, 24, 1, rule=SAGE, mid=True)
    print('  fund closing table end', round(y), 'pad', pad, 'contact top', round(by))


def fade_photo(s, path, x, y, w, h, name, keep=1.0, start=0.78, color=None):
    """crop top part of the photo (keep = fraction of height kept from the top) and fade its bottom into color"""
    from PIL import Image as _I
    import io as _io
    im = _I.open(path).convert('RGB'); iw, ih = im.size
    ar = w / h
    ch = int(ih * keep); cw = int(ch * ar)
    if cw > iw: cw = iw; ch = int(cw / ar)
    x0 = (iw - cw) // 2
    im = im.crop((x0, 0, x0 + cw, ch))
    tw = min(im.width, int(w * 2.5)); im = im.resize((tw, int(tw / ar)), _I.LANCZOS)
    col = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    bg = _I.new('RGB', im.size, col)
    mask = _I.new('L', im.size, 0); H_ = im.height
    for yy in range(H_ if start < 1 else 0):
        t = (yy / H_ - start) / (1 - start)
        if t > 0:
            t = min(1, t); t = t * t * (3 - 2 * t)
            mask.paste(int(255 * t), (0, yy, im.width, yy + 1))
    im = _I.composite(bg, im, mask)
    b = _io.BytesIO(); im.save(b, 'JPEG', quality=90); b.seek(0)
    p = s.shapes.add_picture(b, E(x), E(y), E(w), E(h)); p.name = name
    return p

def cover_fade(self, f, doc):
    """Case for Support cover: photo with a curved edge, small label, one big title, logo centred below"""
    c = doc['cover']; dk = c.get('dark'); s = f.d.page(DG if dk else WHITE)
    C1 = LIV if dk else GR; C2 = WHITE if dk else GR; C3 = SPEC if dk else INK
    lp = [P(c['eyebrow'], 'Montserrat', 16, C1, True, 1.25, align='c')]
    tp = [P(t_, 'EB Garamond', 54, C2, lh=1.12, align='c') for t_ in c['title'].split('\n')]
    LOGO = 100; lw = round(LOGO * 464 / 403)
    ly = H - 56 - LOGO
    ip = [P(c['intro'], 'Source Sans 3', 16, C3, lh=1.55, align='c')]
    th = measure(tp, CW, 0); lh_ = measure(lp, CW, 0); ih = measure(ip, CW, 0)
    sh_ = 0
    if c.get('stats'):
        sp = [([P(n, 'EB Garamond', 44, C1, lh=1.0, align='c')], [P(l, 'Source Sans 3', 15, C3, lh=1.3, align='c')]) for n, l in c['stats']]
        sh_ = max(measure(a, 220, 0) for a, _ in sp) + 6 + max(measure(b, 220, 0) for _, b in sp)
        sy = ly - 40 - sh_
        ly_text = sy - 34
    else:
        ly_text = ly - 36
    iy = ly_text - ih
    ty = iy - 26 - th
    oy = ty - 18 - lh_
    ey = oy - 64
    from PIL import Image as _I
    im = _I.open('ph/' + c['photo']); im.crop((0, 0, im.width, int(im.height * c.get('keep', 1.0)))).save('/tmp/cover-src.jpg')
    p, ey = curved_photo('/tmp/cover-src.jpg', W + 6, ey + 24, c.get('cfy', 0.0), 20, 0.4, edge_y=ey)
    ph_ = s.shapes.add_picture(p, E(-3), E(-3), E(W + 6), E(ey + 24)); ph_.name = 'Photo: ' + c['alt']
    swoosh(s, ey - 3 - 2, LIV if dk else GR, 5, 'Green swoosh line', amp=20, phase=0.4)
    text(s, M, oy, CW, lp, 'Label')
    text(s, M, ty, CW, tp, 'Title')
    text(s, M, iy, CW, ip, 'Intro')
    if c.get('stats'):
        grp = s.shapes.add_group_shape(); grp.name = 'Key numbers'; g = _G(grp)
        cw3 = CW / 3
        for k, (a, b) in enumerate(sp):
            x = M + k * cw3
            text(g, x, sy, cw3, a, 'Number: ' + a[0]['t'])
            text(g, x, sy + measure(a, 220, 0) + 6, cw3, b, 'Label: ' + b[0]['t'])
    png(s, 'logo-white.png' if dk else 'logo.png', (W - lw) / 2, ly, lw, 'SFW logo', LOGO)
    print('  cover photo edge', round(ey), 'label', round(oy), 'title', round(ty))

if __name__ == '__main__' and 'final' in sys.argv:
    import copy
    th = Theme()
    for doc in DOCS:
        if doc['key'] == 'Case for Support':
            doc = copy.deepcopy(doc)
            q = [b for b in doc['blocks'] if b[0] == 'quote'][0]
            nb = []
            for b in doc['blocks']:
                if b[0] == 'quote' or (b[0] == 'rows' and b[2] and b[2][0] == 'Gift') or (b[0] == 'photo' and b[1] == 'students-duo.jpg'): continue
                if b[0] == 'section' and b[1] == 'Why it matters now':
                    nb += [('section', b[1], b[2][:3]), ('pullquote', q[1], q[2]), ('section', '', b[2][3:])]
                else: nb.append(b)
            doc['blocks'] = nb
            th.body_px = 16.5; th.bottom_m = 60
            Theme.closing = _case_closing
        elif doc['key'] == 'Funding the Vision Ahead':
            th.body_px = 16.5; th.bottom_m = 60
            doc = copy.deepcopy(doc)
            doc['blocks'] = [doc['blocks'][0]]
            Theme.closing = _fund_closing
        else:
            Theme.closing = Editorial.closing
        print(doc['key'], build(th, doc, f"out/SFW {doc['key']}.pptx"), 'pages')
