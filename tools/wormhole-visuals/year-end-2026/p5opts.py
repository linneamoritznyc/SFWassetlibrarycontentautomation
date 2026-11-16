# Five options for the Case for Support closing page (page 5). Same exact text in each.
import sys
sys.argv = ['x']
from variants import *
from variants import footer_band, goal_badge, fill_table, wave_fill, swoosh, _G, CASE_FULL
from content import CASE

c = CASE['closing']
gifts = [b for b in CASE_FULL['blocks'] if b[0] == 'rows' and b[2] and b[2][0] == 'Gift'][0]
LINES = ['Give today at soilfoodweb.com/donations or scan the QR code.',
         'One-time gifts, monthly giving, sponsorships, and legacy gifts.',
         'For customized giving, contact Evan Buckman,',
         'Executive Director, at evan@soilfoodweb.com or (512) 359-5206.']
LEGAL = '501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.'
assert ' '.join(LINES + [LEGAL]) == c['give']
HEAD = gifts[1]; ROWS = gifts[3]; GOAL = c['goal']


def heads(s, col):
    rh = lambda t, a='l': P(t, 'Montserrat', 17.33, col, True, 1.2, align=a)
    text(s, M, 44, 300, [rh('Soil Food Web Foundation')], 'Running head left')
    text(s, W - M - 300, 44, 300, [rh('Case for Support', 'r')], 'Running head right')


def heading(s, y, col, rule=SAGE, x=M, w=CW, align='c'):
    hp = [P(HEAD, 'EB Garamond', 40, col, lh=1.15, align=align)]
    h = measure(hp, w, 0); text(s, x, y, w, hp, 'Heading: ' + HEAD)
    if rule: hline(s, x, y + h + 8, w, rule, 'Rule')
    return y + h + 30


def gift_rows(lab, txt, hd):
    return [[P('Gift', 'Source Sans 3', 16, hd, True, 1.3), P('Impact', 'Source Sans 3', 16, hd, True, 1.3)]] + \
           [[P(a, 'EB Garamond', 28, lab, lh=1.15), body(b, 17, txt, lh=1.45)] for a, b, _ in ROWS]


def to_back(s, *shapes):
    tree = s.shapes._spTree
    for k, sh in enumerate(shapes):
        tree.remove(sh._element); tree.insert(2 + k, sh._element)


d = Deck()

# ---- A: deep green, roots growing up from the banner
s = d.page(DG); heads(s, LIV)
y = heading(s, 104, WHITE)
by = footer_band(s, LINES, LEGAL)
RH = 0
D = 240
y, _ = fill_table(s, y, [170, CW - 170], gift_rows(WHITE, WHITE, LIV), 'Table: Gifts', by - RH - D - 40, 10, 16)
goal_badge(s, GOAL, (W - D) / 2, y + (by - RH + 30 - y - D) / 2, D)

# ---- B: photo with a curved edge, goal badge as a seal on the photo, white page
s = d.page(WHITE)
PH = 330
pic(s, 'ph/students-duo.jpg', -3, -3, W + 6, PH + 3, 'Photo: Students in class', fy=0.15)
wave_fill(s, PH - 40, WHITE, 'Photo edge wave', amp=20, phase=0.4, bottom=PH - 18)
swoosh(s, PH - 42, GR, 5, 'Green swoosh line', amp=20, phase=0.4)
D = 240
goal_badge(s, GOAL, W - M - D + 10, PH - D + 70, D)
by = footer_band(s, LINES, LEGAL, legal_col=INK)
y = heading(s, PH + 40, GR, x=M, w=CW - D, align='l', rule=None) + 4
fill_table(s, y, [170, CW - 170], gift_rows(GR, INK, GR), 'Table: Gifts', by - 40, 10, 22, rule=SAGE)

# ---- C: split page, deep green goal column on the left, gifts on white on the right
s = d.page(WHITE)
by = footer_band(s, LINES, LEGAL, legal_col=INK)
CWL = 320
r = rect(s, -4, -4, CWL + 4, by + 4, DG, 'Goal column')
m = re.match(r'(GOAL: RAISE) (\$[\d,]+) (BY .*)', GOAL)
gp = [P(m.group(1), 'Montserrat', 18, LIV, True, 1.3)]
ap = [P(m.group(2), 'EB Garamond', 64, WHITE, lh=1.0)]
dp = [P(m.group(3), 'Montserrat', 15, LIV, True, 1.35)]
iw = CWL - 2 * 48
hs = [measure(gp, iw, 0), measure(ap, iw + 30, 0), measure(dp, iw, 0)]
gy = (by - sum(hs) - 28) / 2
grp = s.shapes.add_group_shape(); grp.name = 'Goal'; g = _G(grp)
text(g, 48, gy, iw, gp, 'Goal: raise'); gy += hs[0] + 10
text(g, 48 - 4, gy, iw + 40, ap, 'Goal amount'); gy += hs[1] + 18
text(g, 48, gy, iw, dp, 'Goal date')
rh = lambda t, a='l': P(t, 'Montserrat', 17.33, GR, True, 1.2, align=a)
text(s, W - M - 300, 44, 300, [rh('Case for Support', 'r')], 'Running head right')
text(s, 48, 44, 260, [P('Soil Food Web Foundation', 'Montserrat', 17.33, LIV, True, 1.2)], 'Running head left')
RX = CWL + 44; RW = W - M - RX
y = heading(s, 104, GR, x=RX, w=RW, align='l')
rows = [[P('Gift', 'Source Sans 3', 16, GR, True, 1.3), P('Impact', 'Source Sans 3', 16, GR, True, 1.3)]] + \
       [[P(a, 'EB Garamond', 28, GR, lh=1.15), body(b, 17, INK, lh=1.45)] for a, b, _ in ROWS]
pad = 10
while pad < 60 and y + table(Deck().page(), 0, 0, [140, RW - 140], rows, 'x', SAGE, pad + 1, 20, brand=True) <= by - 48: pad += 1
table(s, RX, y, [140, RW - 140], rows, 'Table: Gifts', SAGE, pad, 20)

# ---- D: hay layer with white gift boxes, badge below
s = d.page(WHITE); heads(s, GR)
y = heading(s, 104, GR)
by = footer_band(s, LINES, LEGAL, legal_col=INK)
top = y - 6
from PIL import Image as _I
el = _I.open('el-hay.png'); need = round(el.width * (by - top + 4) / (W + 4))
el.crop((0, 0, el.width, min(need, el.height))).save('/tmp/hay-p5.png')
png(s, '/tmp/hay-p5.png', -2, top, W + 4, 'Hay swoosh element', by - top + 4)
yy = top + 54
LW = 150; RW = CW - 56 - LW - 24
for a, b, _ in ROWS:
    lp = [P(a, 'EB Garamond', 26, GR, lh=1.15)]; rp = [body(b, 17, INK, lh=1.42)]
    h = max(measure(lp, LW, 0), measure(rp, RW, 0)) + 30
    rect(s, M, yy, CW, h, WHITE, 'Box: ' + a)
    text(s, M + 28, yy + 15, LW, lp, a, h=h - 30, anchor='m')
    text(s, M + 28 + LW + 24, yy + 15, RW, rp, 'Explanation', h=h - 30, anchor='m')
    yy += h + 12
D = 240
goal_badge(s, GOAL, (W - D) / 2, yy + (by - yy - D) / 2, D)

# ---- E: white page, the four gifts as big numbers in a 2 x 2 grid, deep green goal strip
s = d.page(WHITE); heads(s, GR)
y = heading(s, 104, GR) + 14
by = footer_band(s, LINES, LEGAL, legal_col=INK)
cw = (CW - 48) / 2
cells = []
for a, b, _ in ROWS:
    ap_ = [P(a, 'EB Garamond', 54, GR, lh=1.0)]; bp_ = [body(b, 17, INK, lh=1.45)]
    cells.append((a, ap_, bp_, measure(ap_, cw, 0) + 12 + measure(bp_, cw, 0)))
rowh = [max(cells[0][3], cells[1][3]), max(cells[2][3], cells[3][3])]
SH = 120
gap = (by - SH - y - sum(rowh)) / 3
for k, (a, ap_, bp_, h) in enumerate(cells):
    x = M + (k % 2) * (cw + 48); yy = y + (k // 2) * (rowh[0] + gap)
    text(s, x - lsb(a, 'EB Garamond', False, 54), yy, cw, ap_, 'Amount ' + a)
    text(s, x, yy + measure(ap_, cw, 0) + 12, cw, bp_, 'Impact ' + a)
sy = by - SH
rect(s, -4, sy, W + 8, SH, DG, 'Goal strip')
gp = [P(GOAL, 'EB Garamond', 30, WHITE, lh=1.15, align='c')]
text(s, M, sy + (SH - measure(gp, CW, 0)) / 2, CW, gp, 'Goal')

d.save('out/SFW Case for Support - page 5 options.pptx')
print('ok')
