# Funding the Vision Ahead, 2 pages, same style as the 1 pager. Evan's exact draft text.
import sys; sys.argv = ['x']
exec(open('fund2.py').read().split('# ================= page 1')[0])
BX, BW = M - 24, CW + 48
amt = lambda v_, sz: [P(t_, 'EB Garamond', sz, GR, lh=1.1, align='r') for t_ in {'$10,000 to $100,000': ['$10,000 to', '$100,000'], 'Transformational gift': ['Transformational', 'gift']}.get(v_, [v_])]
# ================= page 1: header, numbers, top priorities
s = d.page(GR); textured_bg(s, GR, 0.06)
PH1 = 150
png(s, 'hay-top.png', -2, -2, W + 4, 'Hay swoosh element', PH1 + 20)
LG = 70; lgw = round(LG * 464 / 403)
lp = [P(c['eyebrow'], 'Montserrat', 15, '#CFE0B4', True, 1.25)]
tp = [P(t_, 'EB Garamond', 40, WHITE, lh=1.05) for t_ in c['title'].split('\n')]
ip = [P(c['intro'], 'Source Sans 3', 15, WHITE, lh=1.48)]
y = PH1 + 8
TXW = BW - lgw - 24
text(s, BX, y, TXW, lp, 'Label'); y += measure(lp, TXW, 0) + 6
text(s, BX, y, TXW, tp, 'Title'); ty = y; y += measure(tp, TXW, 0) + 12
png(s, 'logo-white.png', BX + BW - lgw, ty, lgw, 'SFW logo', LG)
text(s, BX, y, BW, ip, 'Intro'); y += measure(ip, BW, 0)
HB = y + 24
box_top = HB; box_bot = H - 36
y = box_top + 26
hp = [P(pr[1], 'EB Garamond', 36, GR, lh=1.1, align='c')]
hy = y; y += measure(hp, CW, 0) + 8; ry = y; y += 1
IX, IW = BX + 18, BW - 36
NW, AW = 36, 146; TW = IW - NW - 8 - AW - 6
items = []
for k, (a, b, v_) in enumerate(pr[3]):
    np_ = [P(str(k + 1), 'EB Garamond', 40, GR, lh=1.0)]
    tp_ = [dict(t=a + ' ' + b, before=0, runs=[P(a, 'Source Sans 3', 15, DG, True, 1.45), P(' ' + b, 'Source Sans 3', 15, INK, False, 1.45)])]
    vp = amt(v_, 21)
    items.append((a, np_, tp_, vp, max(measure(tp_, TW, 0), measure(vp, AW, 0), 36)))
room = box_bot - 16 - y; inner = sum(i_[4] for i_ in items); pad = (room - inner) / 10
print('p1 room', round(room), 'inner', round(inner), 'pad', round(pad, 1))
card(s, BX, box_top, BW, box_bot - box_top, '#FFFFFF', '#EEF2E6', None, 0, 'Top priorities panel', tex=0.05)
text(s, IX, hy, IW, hp, 'Heading: ' + pr[1]); hline(s, IX, ry, IW, SAGE, 'Rule')
for a, np_, tp_, vp, h in items:
    text(s, IX, y + pad - 4, NW, np_, 'Number')
    text(s, IX + NW + 8, y + pad, TW, tp_, a)
    text(s, IX + IW - AW, y + pad, AW, vp, 'Investment')
    y += h + 2 * pad
    if a != items[-1][0]: hline(s, IX, y, IW, '#D5DBCB', 'Row rule')
# ================= page 2: more ways to invest on the soft fade, footer band
s = d.page(WHITE)
PH = 350
from PIL import Image as _I, ImageDraw as _D
_curve = lambda x: PH - 6 - 26 * (1 - ((2 * x / W) - 1) ** 2)   # concave: edge rises in the middle
im = _I.open('ph/shed2.jpg').convert('RGB'); iw, ih = im.size; ar = (W + 6) / PH
nh = int(iw / ar); y0 = int((ih - nh) * 0.72); im = im.crop((0, y0, iw, y0 + nh)).resize((int((W + 6) * 2), int(PH * 2)), _I.LANCZOS).convert('RGBA')
mk = _I.new('L', im.size, 0)
pts = [(x * 2, _curve(x - 3) * 2) for x in range(0, W + 7, 4)]
_D.Draw(mk).polygon([(0, 0), (im.width, 0)] + list(reversed(pts)), fill=255); im.putalpha(mk); im.save('/tmp/shed2-curve.png')
s.shapes.add_picture('/tmp/shed2-curve.png', E(-3), E(-3), E(W + 6), E(PH)).name = 'Photo: Workshop group under a shed in India'
top = [(x, _curve(x) - 3) for x in range(-20, W + 21, 8)]
pts = top + [(x, yy + 4) for x, yy in reversed(top)]
fb = s.shapes.build_freeform(E(pts[0][0]), E(pts[0][1]), scale=1.0)
fb.add_line_segments([(E(a), E(b)) for a, b in pts[1:]], close=True)
sw = fb.convert_to_shape(); sw.fill.solid(); sw.fill.fore_color.rgb = rgb(GR); sw.line.fill.background(); sw.name = 'Green swoosh line'
st = sw._element.find(qn('p:style'))
if st is not None: sw._element.remove(st)
lines = ['Give today at soilfoodweb.com/donations', 'For customized giving, contact Evan Buckman, Executive Director,', 'evan@soilfoodweb.com, (512) 359-5206', 'www.soilfoodweb.com']
assert ' · '.join([lines[0], lines[1] + ' ' + lines[2], lines[3]]) == cl['give']
g_ = [body(x_, 14.67, WHITE, lh=1.42) for x_ in lines]
q = round(measure(g_, 470, 0)); GB = q + 48; gy = H - GB
card(s, -4, gy, W + 8, GB + 4, '#2C4628', DG, None, 0, 'Footer band', tex=0.08)
png(s, 'qr-white.png', M, gy + 24, q, 'QR code', q)
text(s, M + q + 26, gy + 22, 470, g_, 'Give online and contact')
lw_ = round(q * 464 / 403); png(s, 'logo-white.png', W - M - lw_, gy + 24, lw_, 'SFW logo', q)
y = PH + 8
cw3 = BW / 3
for k, (n, l) in enumerate(c['stats']):
    x = BX + k * cw3
    a = [P(n, 'EB Garamond', 42, GR, lh=1.0, align='c')]; b = [P(l, 'Source Sans 3', 14.67, INK, lh=1.3, align='c')]
    ah = measure(a, cw3, 0); NH = ah + 4 + measure(b, cw3, 0)
    if k: rect(s, x, y + 4, 1, NH - 8, SAGE, 'Divider')
    text(s, x, y, cw3, a, 'Number: ' + n); text(s, x, y + ah + 4, cw3, b, 'Label: ' + l)
y += NH + 16
hp = [P(mw[1], 'EB Garamond', 36, GR, lh=1.1, align='c')]
text(s, M, y, CW, hp, 'Heading: ' + mw[1]); y += measure(hp, CW, 0) + 8
hline(s, M, y, CW, SAGE, 'Rule'); y += 1
LW, AW = 200, 190; TW = CW - LW - AW - 2 * 18
items = []
for a, b, v_ in mw[3]:
    lp_ = [P(a, 'Source Sans 3', 18, DG, True, 1.3)]; tp_ = [body(b, 16, INK, lh=1.45)]; vp = [P(v_, 'EB Garamond', 24, GR, lh=1.1, align='r')]
    items.append((a, lp_, tp_, vp, max(measure(lp_, LW, 0), measure(tp_, TW, 0), measure(vp, AW, 0))))
room = gy - 24 - y; inner = sum(i_[4] for i_ in items); pad = (room - inner) / 10
print('p2 room', round(room), 'inner', round(inner), 'pad', round(pad, 1))
band_top = y; 
png(s, grad_band(round(gy - band_top + 30)), -2, band_top - 30, W + 4, 'More ways background fade', gy - band_top + 30) if False else None
for a, lp_, tp_, vp, h in items:
    text(s, M, y + pad, LW, lp_, a, h=h, anchor='m')
    text(s, M + LW + 18, y + pad, TW, tp_, 'What it does', h=h, anchor='m')
    text(s, W - M - AW, y + pad, AW, vp, 'Investment', h=h, anchor='m')
    y += h + 2 * pad
    hline(s, M, y, CW, '#D5DBCB' if a != items[-1][0] else SAGE, 'Row rule')
d.save('out/SFW Funding the Vision Ahead - 2 pages.pptx')
