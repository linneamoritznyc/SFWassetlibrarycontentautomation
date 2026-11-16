from natlib import *
from natdecks import GR, DG, INK, SAGE, SPEC, LIV, OLIVE, W, H, M, CW, eyebrow, body
from pptx.enum.shapes import MSO_SHAPE
BR = '#4F3433'

def rrect(s, x, y, w, h, color, r=18, name='Card'):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(x), E(y), E(w), E(h))
    sh.adjustments[0] = r / min(w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(color); sh.line.fill.background(); sh.shadow.inherit = False
    sh.name = name; return sh

def round_pic(p, r, w, h):
    g = p._element.spPr.find(qn('a:prstGeom')); g.set('prst', 'roundRect')
    av = g.find(qn('a:avLst'))
    gd = OxmlElement('a:gd'); gd.set('name', 'adj'); gd.set('fmla', f'val {int(r / min(w, h) * 100000)}'); av.append(gd)

d = Deck()
cards = [('i-student.png', 'Scholarship Fund.', "Opens our courses to students anywhere in the world, regardless of means. Hundreds of people who make a strong impact in their communities are waiting for support. Organizational scholarships reach even further: both founders of TrashIt in Pakistan trained with us, and TrashIt now offers microbial soil testing to farmers. $5,000 funds a full scholarship for our Foundation Courses and The Complete Practicum, a $10,000 value. We awarded over $300,000 in scholarships in 2026.", '$100,000'),
         ('i-idea.png', 'New and Updated Programs.', 'Draw on decades of experience teaching the Soil Food Web Approach, using modern pedagogy to improve our learning experience and launch new programs.', '$100,000'),
         ('i-compost.png', 'Hands-On Workshops.', 'Bring two-week hands-on workshops to new places. $10,000 sponsors a group of seats in a new location, and $100,000 sponsors a whole workshop in a new region such as Kenya or Brazil.', '$10,000 to $100,000'),
         ('i-fielddata.png', 'Open Research.', "Build on Elaine's experiments to advance the science of the Soil Food Web itself. We publish our trial and case study data openly so anyone can see why the methods work. $100,000 starts this work, and major studies range from $500,000 to $3 million.", '$100,000+'),
         ('i-barn.png', 'Elaine Ingham Legacy Fund.', "Fund field research in Elaine's name, across a global network of demonstration farms where farmers can see the results on working farms.", 'Transformational gift')]
PAD = 24; IC = 34; TX = PAD + IC + 22; AMW = 170
TW = CW - TX - PAD - AMW - 24
def card_paras(t, b): return [P(t, 'Montserrat', 15, BR, True, 1.3), body(b, 14.5, before=6, lh=1.45)]
def card_h(t, b): return measure(card_paras(t, b), TW) + 2 * PAD
def place_card(s, y, ic, t, b, amt):
    ch = card_h(t, b)
    rrect(s, M, y, CW, ch, '#FFFFFF', 18, 'Card: ' + t[:-1])
    png(s, ic, M + PAD, y + (ch - IC) / 2, IC, t[:-1] + ' icon')
    text(s, M + TX, y + PAD, TW, card_paras(t, b), t[:-1], h=ch - 2 * PAD, anchor='m')
    text(s, M + CW - PAD - AMW, y + PAD, AMW, [P(amt, 'Montserrat', 16, GR, True, 1.3, align='r')], 'Amount: ' + amt, h=ch - 2 * PAD, anchor='m')
    return ch
# title lines must not run into the amount: check
for _, t, _, a in cards:
    assert nlines(a, 'Montserrat', 16, True, AMW) <= 2, a

# ---- page 1: green band + first cards
s = d.page(SPEC)
pic(s, 'ph/ground-pale.jpg', 0, 0, W, H, 'Background: pale hay texture')
BAND = 456
pic(s, 'ph/band-green.jpg', 0, 0, W, BAND, 'Background: green hay band')
phw, phh = 250, 320
p = pic(s, 'ph/microscope.jpg', W - M - phw, 84, phw, phh, 'Photo: student at the microscope', fy=0.3)
round_pic(p, 22, phw, phh)
tw = W - 2 * M - phw - 36
text(s, M, 44, CW, [eyebrow('Soil Food Web Foundation: Funding the Vision Ahead', '#FFFFFF')], 'Eyebrow')
y = 92
y += text(s, M, y, tw, [P('2027 and Beyond: Funding the Vision Ahead', 'Montserrat', 34, '#FFFFFF', True, 1.12)], 'Title') + 18
y += text(s, M, y, tw, [body("We would not be here without the donors who have supported us and shown up. Gifts go a long way here: $5,000 delivers $10,000 of training. Every student we train builds soil biology literacy and joins a worldwide network of practitioners and leaders working to change the global food system.", 15, '#FFFFFF', lh=1.5)], 'Intro')
print('band text end', round(y), 'band', BAND)
y = BAND + 40
y += text(s, M, y, CW, [P('Top priorities', 'Montserrat', 24, BR, True, 1.2)], 'Heading') + 18
GAP = 14; BOT = H - 48
pages = [s]
for ic, t, b, a in cards:
    ch = card_h(t, b)
    if y + ch > BOT:
        s = d.page(SPEC); pic(s, 'ph/ground-pale.jpg', 0, 0, W, H, 'Background: pale hay texture'); pages.append(s)
        text(s, M, 44, 340, [eyebrow('Soil Food Web Foundation')], 'Running head left')
        text(s, W - M - 340, 44, 340, [eyebrow('Funding the Vision Ahead', GR, 'r')], 'Running head right')
        y = 92
    y += place_card(s, y, ic, t, b, a) + GAP
print('cards end', round(y), 'pages', len(pages))
last_y = y

# photo to fill page 2 if room
if len(pages) > 1 and BOT - last_y > 220:
    ph = BOT - last_y - 6
    pp = pic(s, 'ph/poppies-hi.jpg', M, last_y + 6, CW, ph, 'Photo: group in a poppy field', fy=0.62)
    round_pic(pp, 18, CW, ph)

# ---- page 3: more ways, deep green
s = d.page(DG)
text(s, M, 44, 340, [eyebrow('Soil Food Web Foundation', LIV)], 'Running head left')
text(s, W - M - 340, 44, 340, [eyebrow('Funding the Vision Ahead', LIV, 'r')], 'Running head right')
y = 100
y += text(s, M, y, CW, [P('More ways to invest', 'Montserrat', 30, '#FFFFFF', True, 1.15)], 'Heading') + 26
mw = [('Living Soil Circle', 'Monthly donors whose steady support funds scholarships all year. Join on our GiveButter page.', '$100+ per month'),
      ('Founders Circle', 'Leaders who give $10,000 or more a year during our founding years and share the mission with friends.', '$10,000+ per year'),
      ('Named Scholarship', 'Fund a full scholarship in honor of a loved one, family or farm.', '$5,000'),
      ('Sponsor a Workshop or Event', 'Underwrite a compost workshop or gathering for students, farmers and supporters.', '$5,000 to $20,000'),
      ('Unrestricted Annual Fund', 'Goes where the need is greatest: scholarships, teaching and research.', 'Any amount')]
hdr = [P(t, 'Montserrat', 10, LIV, True, 1.4, caps=True, track=2) for t in ('Way to give', 'What it does', 'Investment')]
rows = [hdr] + [[P(a, 'Montserrat', 15, '#FFFFFF', True, 1.3), body(b, 14.5, SPEC, lh=1.45), P(c, 'Montserrat', 14, '#FFFFFF', True, 1.35)] for a, b, c in mw]
y += table(s, M, y, [200, CW - 200 - 170, 170], rows, 'Table: More ways to invest', OLIVE, 16, 24)
g = [body('Give today at soilfoodweb.com/donations · For customized giving, contact Evan Buckman, Executive Director, evan@soilfoodweb.com, (512) 359-5206 · www.soilfoodweb.com', 15, SPEC, lh=1.5)]
tw = 420; hg = max(96, measure(g, tw)); by = H - 76 - hg
dw = 300; dh = dw * 794 / 838
if by - 60 - dh > y + 20: png(s, 'mycelium.png', (W - dw) / 2, y + (by - 34 - y - dh) / 2, dw, 'Fungal network drawing')
hline(s, M, by - 34, CW, OLIVE)
png(s, 'qr.png', M, by, 96, 'QR code', 96)
text(s, M + 124, by - 2, tw, g, 'Give today')
png(s, 'logo-white.png', W - M - 72, by + 6, 72, 'SFW logo white')
print('p3 table end', round(y), 'bottom', round(by))
d.save('out/SFW Funding the Vision Ahead - Cards.pptx')
