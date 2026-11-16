# Funding the Vision Ahead, 1 page. Evan's exact draft text. White page, brand curve header.
import sys; sys.argv = ['x']
exec(open('fund2.py').read().split('# ================= page 1')[0])
s = d.page(WHITE)
BX, BW = M - 24, CW + 48
# ---------- header: deep green with a curved bottom edge
lp = [P(c['eyebrow'], 'Montserrat', 14, LIV, True, 1.25, align='c')]
tp = [P(c['title'].replace('\n', ' '), 'EB Garamond', 34, WHITE, lh=1.05, align='c')]
ip = [P(c['intro'], 'Source Sans 3', 14, SPEC, lh=1.45, align='c')]
y = 30
hh = measure(lp, CW, 0) + 6 + measure(tp, CW, 0) + 10 + measure(ip, BW, 0)
HB = y + hh + 24
rect(s, -4, -4, W + 8, HB + 4, DG, 'Header background')
text(s, M, y, CW, lp, 'Label'); y += measure(lp, CW, 0) + 6
text(s, M, y, CW, tp, 'Title'); y += measure(tp, CW, 0) + 10
text(s, BX, y, BW, ip, 'Intro')
y = HB + 14
cw3 = BW / 3
for k, (n, l) in enumerate(c['stats']):
    x = BX + k * cw3
    a = [P(n, 'EB Garamond', 36, GR, lh=1.0, align='c')]; b = [P(l, 'Source Sans 3', 13.33, INK, lh=1.3, align='c')]
    ah = measure(a, cw3, 0); NH = ah + 2 + measure(b, cw3, 0)
    if k: rect(s, x, y + 4, 1, NH - 8, SAGE, 'Divider')
    text(s, x, y, cw3, a, 'Number: ' + n); text(s, x, y + ah + 2, cw3, b, 'Label: ' + l)
y += NH + 10
pri_top = y
# ---------- footer band
lines = ['Give today at soilfoodweb.com/donations', 'For customized giving, contact Evan Buckman, Executive Director,', 'evan@soilfoodweb.com, (512) 359-5206', 'www.soilfoodweb.com']
assert ' · '.join([lines[0], lines[1] + ' ' + lines[2], lines[3]]) == cl['give']
g_ = [body(x_, 12, WHITE, lh=1.4) for x_ in lines]
q = round(measure(g_, 430, 0)); GB = q + 26; gy = H - GB
rect(s, -4, gy, W + 8, GB + 4, DG, 'Footer band')
png(s, 'qr-white.png', BX, gy + 13, q, 'QR code', q)
text(s, BX + q + 22, gy + 12, 430, g_, 'Give online and contact')
lw_ = round(q * 464 / 403); png(s, 'logo-white.png', BX + BW - lw_, gy + 13, lw_, 'SFW logo', q)
png_y_fix = 0
# ---------- more ways to invest: five columns on the soft light green fade
cw5 = (BW - 4 * 14) / 5
mh_ = [P(mw[1], 'EB Garamond', 26, GR, lh=1.1, align='c')]
cols = []
for a, b, v_ in mw[3]:
    cols.append((a, [P(a, 'Source Sans 3', 13.33, DG, True, 1.25)], [body(b, 12, INK, lh=1.35)], [P(v_, 'EB Garamond', 18, GR, lh=1.1)]))
ha = max(measure(x[1], cw5 - 3, 0) for x in cols); hb = max(measure(x[2], cw5 - 3, 0) for x in cols); hv = max(measure(x[3], cw5 - 3, 0) for x in cols)
colh = ha + 4 + hb + 6 + hv
MB = 14 + measure(mh_, CW, 0) + 10 + colh + 16
my = gy - MB
png(s, grad_band(round(MB)), -2, my, W + 4, 'More ways background fade', MB)
yy = my + 14; text(s, M, yy, CW, mh_, 'Heading: ' + mw[1]); yy += measure(mh_, CW, 0) + 10
for k, (a, A, B, V) in enumerate(cols):
    x = BX + k * (cw5 + 14)
    if k: rect(s, x - 7, yy, 1, colh, SAGE, 'Divider')
    grp = s.shapes.add_group_shape(); grp.name = 'Column: ' + a; g = _G(grp)
    text(g, x, yy, cw5, A, 'Title: ' + a)
    text(g, x, yy + ha + 4, cw5, B, 'Description: ' + a)
    text(g, x, yy + ha + 4 + hb + 6, cw5, V, 'Amount: ' + a)
# ---------- top priorities: ruled list on white
y = pri_top
hp = [P(pr[1], 'EB Garamond', 30, GR, lh=1.1, align='c')]
text(s, M, y, CW, hp, 'Heading: ' + pr[1]); y += measure(hp, CW, 0) + 6
hline(s, BX, y, BW, SAGE, 'Rule'); y += 1
NW, AW = 30, 138; TW = BW - NW - 8 - AW - 6
items = []
for k, (a, b, v_) in enumerate(pr[3]):
    np_ = [P(str(k + 1), 'EB Garamond', 34, GR, lh=1.0)]
    tp_ = [dict(t=a + ' ' + b, before=0, runs=[P(a, 'Source Sans 3', 13.33, DG, True, 1.45), P(' ' + b, 'Source Sans 3', 13.33, INK, False, 1.45)])]
    vp = [P(t_, 'EB Garamond', 20, GR, lh=1.1, align='r') for t_ in {'$10,000 to $100,000': ['$10,000 to', '$100,000'], 'Transformational gift': ['Transformational', 'gift']}.get(v_, [v_])]
    items.append((a, np_, tp_, vp, max(measure(tp_, TW, 0), measure(vp, AW, 0), 30)))
room = my - 10 - y; inner = sum(i_[4] for i_ in items); pad = (room - inner) / 10
print('room', round(room), 'inner', round(inner), 'pad', round(pad, 1))
for a, np_, tp_, vp, h in items:
    text(s, BX, y + pad - 4, NW, np_, 'Number')
    text(s, BX + NW + 8, y + pad, TW, tp_, a)
    text(s, BX + BW - AW, y + pad, AW, vp, 'Investment')
    y += h + 2 * pad
    hline(s, BX, y, BW, '#D5DBCB' if a != items[-1][0] else SAGE, 'Row rule')
d.save('out/SFW Funding the Vision Ahead - 1 page.pptx')
