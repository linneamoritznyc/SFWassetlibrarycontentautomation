# Funding the Vision Ahead, 2 pages. Evan's exact text. Soft rounded cards, tiny gradients, subtle hay texture.
import sys; _argv = sys.argv[:]; sys.argv = ['x']
from variants import *
from variants import _G, curved_photo, green_qr, fill_table
from content import FUNDING
from PIL import Image as I, ImageDraw as ID
c = FUNDING['cover']; cl = FUNDING['closing']
pr = [b for b in FUNDING['blocks'] if b[0] == 'rows' and b[1] == 'Top priorities'][0]
mw = [b for b in FUNDING['blocks'] if b[0] == 'rows' and b[1] == 'More ways to invest'][0]
d = Deck(); N = [0]

def hx(c_): return tuple(int(c_.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

_TILE = I.open('/mnt/user-data/outputs/SFW Brand Graphics/8 Hay tile.png').convert('L')
def card(s, x, y, w, h, top, bot, border=None, r=0, name='Card', alpha=255, tex=0.10):
    """straight-cornered panel: tiny diagonal gradient + faint hay texture + hairline edge, baked to PNG"""
    sc = 2; W_, H_ = int(w * sc), int(h * sc)
    a, b = hx(top), hx(bot)
    g = I.new('RGB', (W_, H_))
    px = g.load()
    for yy in range(H_):
        for xx in range(0, W_, 4):
            t = min(1, (yy / max(1, H_ - 1)) * 0.7 + (xx / max(1, W_ - 1)) * 0.3)
            col = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
            for k in range(4):
                if xx + k < W_: px[xx + k, yy] = col
    tw = max(W_, H_); tile = _TILE.resize((tw, tw)).crop((0, 0, W_, H_))
    lift = 1 if sum(a) < 380 else -1
    lit = I.new('RGB', (W_, H_), tuple(max(0, min(255, v + 34 * lift)) for v in a))
    g = I.composite(lit, g, tile.point(lambda v: int(v * tex)))
    if border:
        dr = ID.Draw(g); dr.rectangle((0, 0, W_ - 1, H_ - 1), outline=hx(border), width=2)
    N[0] += 1; p = f'/tmp/card-{N[0]}.jpg'; g.save(p, quality=90)
    s.shapes.add_picture(p, E(x), E(y), E(w), E(h)).name = name

def textured_bg(s, color, strength=0.07, name='Background texture'):
    tile = I.open('/mnt/user-data/outputs/SFW Brand Graphics/8 Hay tile.png').convert('L').resize((820, 820))
    big = I.new('L', (820, 1064)); big.paste(tile, (0, 0)); big.paste(tile.crop((0, 0, 820, 244)), (0, 820))
    base = I.new('RGB', big.size, hx(color))
    lit = I.new('RGB', big.size, tuple(min(255, v + 40) for v in hx(color)))
    mask = big.point(lambda v: int(v * strength))
    im = I.composite(lit, base, mask); p = '/tmp/texbg.jpg'; im.save(p, quality=88)
    s.shapes.add_picture(p, E(-4), E(-4), E(W + 8), E(H + 8)).name = name

PHOTO, PFY = 'shed2.jpg', 0.55

# ================= page 1: royal deep green
s = d.page(DG); textured_bg(s, DG)
y = 40
lp = [P(c['eyebrow'], 'Montserrat', 15, LIV, True, 1.25, align='c')]
tp = [P(t_, 'EB Garamond', 42, WHITE, lh=1.04, align='c') for t_ in c['title'].split('\n')]
ip = [P(c['intro'], 'Source Sans 3', 15, SPEC, lh=1.45, align='c')]
y += text(s, M, y, CW, lp, 'Label') + 6
y += text(s, M, y, CW, tp, 'Title') + 12
y += text(s, M, y, CW, ip, 'Intro') + 16
# key numbers in three soft cards
gap = 12; cw3 = (CW + 48 - 2 * gap) / 3; CH = 66
for k, (n, l) in enumerate(c['stats']):
    x = M - 24 + k * (cw3 + gap)
    if k: rect(s, x - gap / 2, y + 8, 1, CH - 16, '#7D8A55', 'Divider')
    a = [P(n, 'EB Garamond', 42, LIV, lh=1.0, align='c')]; b = [P(l, 'Source Sans 3', 15, WHITE, lh=1.3, align='c')]
    ah = measure(a, cw3, 0); bh = measure(b, cw3, 0); yy = y + (CH - ah - 4 - bh) / 2
    text(s, x, yy, cw3, a, 'Number: ' + n); text(s, x, yy + ah + 4, cw3, b, 'Label: ' + l)
y += CH + 10
BX, BW = M - 24, CW + 48; box_top = y + 6
y = box_top + 16
hp = [P(pr[1], 'EB Garamond', 34, GR, lh=1.15, align='c')]
heading_y = y; y += measure(hp, CW, 0) + 6
rule_y = y; y += 4
NW, AW = 36, 146; TW = CW - NW - AW - 2 * 12 - 14
items = []
for k, (a, b, v_) in enumerate(pr[3]):
    np_ = [P(str(k + 1), 'EB Garamond', 38, GR, lh=1.0)]
    tp_ = [dict(t=a + ' ' + b, before=0, runs=[P(a, 'Source Sans 3', 16, DG, True, 1.4), P(' ' + b, 'Source Sans 3', 16, INK, False, 1.4)])]
    vp = [P(t_, 'EB Garamond', 22, GR, lh=1.12, align='r') for t_ in {'$10,000 to $100,000': ['$10,000 to', '$100,000'], 'Transformational gift': ['Transformational', 'gift']}.get(v_, [v_])]
    items.append((a, np_, tp_, vp, max(measure(tp_, TW + 22, 0), measure(vp, AW, 0), 34)))
box_bot = H - 36
room = box_bot - 14 - y; inner = sum(i_[4] for i_ in items)
pad = max(6, min(22, (room - inner) / 10)); print('room', round(room), 'inner', round(inner))
card(s, BX, box_top, BW, box_bot - box_top, '#FFFFFF', '#EEF2E6', None, 0, 'Top priorities panel', tex=0.05)
text(s, M, heading_y, CW, hp, 'Heading: ' + pr[1]); hline(s, M, rule_y, CW, SAGE, 'Rule')
for a, np_, tp_, vp, h in items:
    ch = h + 2 * pad
    text(s, M, y + pad - 4, NW, np_, 'Number')
    text(s, M + NW + 12, y + pad, TW + 12, tp_, a)
    text(s, W - M - AW, y + pad, AW, vp, 'Investment')
    y += ch
    if a != items[-1][0]: hline(s, M, y, CW, '#D5DBCB', 'Row rule')
print('p1 end', round(y), 'pad', round(pad))

# ================= page 2: white, top priorities as soft cards, goal + giving card from Evan's one-pager
s = d.page(WHITE)
PH = 290
p, ey = curved_photo('ph/' + PHOTO, W + 6, PH, PFY, 18, 0.4)
s.shapes.add_picture(p, E(-3), E(-3), E(W + 6), E(PH)).name = 'Photo: Workshop group under a shed in India'
swoosh(s, ey - 5, GR, 4, 'Swoosh line', amp=18, phase=0.4)
# giving panel: exactly Evan's draft line, one item per line
lines = ['Give today at soilfoodweb.com/donations', 'For customized giving, contact Evan Buckman,', 'Executive Director, evan@soilfoodweb.com, (512) 359-5206', 'www.soilfoodweb.com']
assert ' · '.join([lines[0], lines[1] + ' ' + lines[2], lines[3]]) == cl['give']
IX = M - 24; IW = CW + 48; ip_ = 28
g_ = [body(x, 16, WHITE, lh=1.5) for x in lines]
q = round(measure(g_, 440, 0)); CH = q + 2 * ip_
cy = H - 44 - CH
cy = H - CH - 20
card(s, -4, cy, W + 8, H - cy + 4, '#2C4628', DG, None, 0, 'Giving band')
png(s, 'qr-white.png', M, cy + ip_, q, 'QR code', q)
text(s, M + q + 26, cy + ip_ - 2, 440, g_, 'Give online and contact')
LOGO = 100; lw_ = round(LOGO * 464 / 403)
png(s, 'logo-white.png', W - M - lw_, cy + (H - cy - LOGO) / 2, lw_, 'SFW logo', LOGO)
by = cy
hp = [P(mw[1], 'EB Garamond', 38, GR, lh=1.15, align='c')]
y = PH + 10; y += text(s, M, y, CW, hp, 'Heading: ' + mw[1]) + 8
hline(s, M, y, CW, SAGE, 'Rule'); y += 4
LW, AW = 180, 190; TW = CW - LW - AW - 2 * 18
items = []
for a, b, v_ in mw[3]:
    lp_ = [P(a, 'Source Sans 3', 17, DG, True, 1.3)]; tp_ = [body(b, 16, INK, lh=1.42)]; vp = [P(v_, 'EB Garamond', 23, GR, lh=1.15, align='r')]
    items.append((a, lp_, tp_, vp, max(measure(lp_, LW, 0), measure(tp_, TW, 0), measure(vp, AW, 0))))
room = by - 24 - y; inner = sum(i_[4] for i_ in items); cg = 10
pad = max(8, min(24, (room - inner - cg * 4) / 10))
for a, lp_, tp_, vp, h in items:
    ch = h + 2 * pad
    text(s, M, y + pad, LW, lp_, a, h=h, anchor='m')
    text(s, M + LW + 18, y + pad, TW, tp_, 'What it does', h=h, anchor='m')
    text(s, W - M - AW, y + pad, AW, vp, 'Investment', h=h, anchor='m')
    y += ch; hline(s, M, y, CW, SAGE, 'Row rule'); y += cg
print('p2 end', round(y), 'pad', round(pad), 'card top', round(cy))
d.save('out/SFW Funding the Vision Ahead - 2 pages.pptx')
