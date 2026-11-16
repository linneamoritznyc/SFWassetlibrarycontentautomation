# SFW Year-End Campaign 2026: social posts. Same visual family as the 4 donor documents.
import math, sys
from natlib import *
WHITE='#FFFFFF'
def body(t,size=16,color='#333130',lh=1.45,before=0): return P(t,'Source Sans 3',size,color,lh=lh,before=before)
from PIL import Image as I, ImageDraw as ID

GR, DG, LIV, SAGE, INK = '#156826', '#22371F', '#A2AE77', '#A7B097', '#333130'
PALE = '#DCE3CC'
URL = 'soilfoodweb.com/donations'


def curve_photo(s, path, W, PH, fy, name, amp=26, fx=0.5):
    """photo across the top, bottom edge rises in the middle (concave), thin green line along it"""
    cy = lambda x: PH - 6 - amp * (1 - ((2 * x / W) - 1) ** 2)
    im = I.open(path).convert('RGB'); iw, ih = im.size; ar = (W + 6) / PH
    if iw / ih > ar:
        nw = int(ih * ar); x0 = int((iw - nw) * fx); im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / ar); y0 = int((ih - nh) * fy); im = im.crop((0, y0, iw, y0 + nh))
    im = im.resize((int((W + 6) * 1.5), int(PH * 1.5)), I.LANCZOS).convert('RGBA')
    mk = I.new('L', im.size, 0)
    pts = [(x * 1.5, cy(x - 3) * 1.5) for x in range(0, W + 7, 4)]
    ID.Draw(mk).polygon([(0, 0), (im.width, 0)] + list(reversed(pts)), fill=255)
    im.putalpha(mk); out = f'/tmp/ig-{name[:12].replace(" ", "")}-{W}-{PH}.png'; im.save(out)
    s.shapes.add_picture(out, E(-3), E(-3), E(W + 6), E(PH)).name = 'Photo: ' + name
    top = [(x, cy(x) - 3) for x in range(-20, W + 21, 8)]
    poly = top + [(x, y + 5) for x, y in reversed(top)]
    fb = s.shapes.build_freeform(E(poly[0][0]), E(poly[0][1]), scale=1.0)
    fb.add_line_segments([(E(a), E(b)) for a, b in poly[1:]], close=True)
    sh = fb.convert_to_shape(); sh.fill.solid(); sh.fill.fore_color.rgb = rgb(GR); sh.line.fill.background(); sh.name = 'Green swoosh line'
    st = sh._element.find(qn('p:style'))
    if st is not None: sh._element.remove(st)
    return PH


def band(s, W, H, BH, lines, name='Giving band'):
    """deep green band at the bottom with the call to action and the white logo"""
    y = H - BH
    rect(s, -4, y, W + 8, BH + 4, DG, name)
    LG = 96; lw = round(LG * 464 / 403)
    tw = W - 2 * M - lw - 40
    hs = measure(lines, tw, 0)
    text(s, M, y + (BH - hs) / 2, tw, lines, 'Call to action')
    png(s, 'logo-white.png', W - M - lw, y + (BH - LG) / 2, lw, 'SFW logo', LG)
    return y


def label(t, col=GR, size=28):
    return P(t, 'Montserrat', size, col, True, 1.25)


def quote_block(s, x, y, w, quote, who, size=56):
    png(s, 'brandq-green.png', x, y + 6, 56, 'Quote mark')
    qp = [P(quote, 'EB Garamond', size, DG, lh=1.18)]
    ap = [P(who, 'Source Sans 3', 32, GR, True, 1.3)]
    qx = x + 80; qw = w - 80
    qh = measure(qp, qw, 0); text(s, qx, y, qw, qp, 'Quote')
    text(s, qx, y + qh + 20, qw, ap, 'Quote attribution')
    return y + qh + 20 + measure(ap, qw, 0)


def place_middle(top, bottom, h):
    return top + (bottom - top - h) / 2


M = 72
W, H = 1080, 1350
posts = []

# ---------- 1. Countdown story 1 (week of Nov 23)
d = Deck(W, H); s = d.page()
PH = curve_photo(s, 'ig/friends-laughing.jpg', W, 600, 0.15, 'Workshop participants laughing, India 2026')
cta = [P('Giving Tuesday is only 7 days away.', 'EB Garamond', 48, WHITE, lh=1.15),
       P('Can we count on your support? ' + URL, 'Source Sans 3', 32, PALE, lh=1.4, before=10)]
by = band(s, W, H, 200, cta)
q = 'I just wanted to say thank you so much for allowing me to participate in a class that otherwise would have never been accessible to me.'
qh = measure([P(q, 'EB Garamond', 56, DG, lh=1.18)], W - 2 * M - 80, 0) + 20 + 42 + 50
y = place_middle(PH + 10, by, qh)
text(s, M, y, W - 2 * M, [label('Scholar story')], 'Label')
quote_block(s, M, y + 50, W - 2 * M, q, 'Zoë Unruh, scholarship student, Canada')
d.save('out/ig/01 Countdown story 1.pptx'); posts.append('01 Countdown story 1')

# ---------- 2. Countdown story 2 (Nov 27 to 29)
d = Deck(W, H); s = d.page()
PH = curve_photo(s, 'ig/building-pile.jpg', W, 600, 0.45, 'Building a compost pile, India 2026')
cta = [P('Giving Tuesday is only 3 days away.', 'EB Garamond', 48, WHITE, lh=1.15),
       P('Can we count on your support? ' + URL, 'Source Sans 3', 32, PALE, lh=1.4, before=10)]
by = band(s, W, H, 200, cta)
q = 'My goal is to turn this knowledge into living topsoil, restored yields, and climate resilience across Kenya.'
qh = measure([P(q, 'EB Garamond', 56, DG, lh=1.18)], W - 2 * M - 80, 0) + 20 + 42 + 50
y = place_middle(PH + 10, by, qh)
text(s, M, y, W - 2 * M, [label('Scholar story')], 'Label')
quote_block(s, M, y + 50, W - 2 * M, q, 'Martin Kihara, scholarship student, Kenya')
d.save('out/ig/02 Countdown story 2.pptx'); posts.append('02 Countdown story 2')

# ---------- 3. Giving Tuesday (Dec 1)
d = Deck(W, H); s = d.page()
PH = curve_photo(s, 'ig/student-microscope.jpg', W, 560, 0.2, 'Student at the microscope, India 2026')
cta = [P('Give now at ' + URL, 'EB Garamond', 48, WHITE, lh=1.15),
       P('The match runs today only.', 'Source Sans 3', 32, PALE, lh=1.4, before=10)]
by = band(s, W, H, 200, cta)
tp = [P('Today every gift is doubled.', 'EB Garamond', 72, DG, lh=1.08)]
q = 'Through this training, I will strengthen my knowledge of soil biology and share it with farmers, youth, and rural communities across Guinea.'
qp = [P(q, 'EB Garamond', 40, DG, lh=1.25)]
ap = [P('Boubacar Tidiane Diallo, scholarship student, Guinea', 'Source Sans 3', 28, GR, True, 1.3)]
tw = W - 2 * M
blk = 44 + measure(tp, tw, 0) + 28 + measure(qp, tw - 64, 0) + 14 + measure(ap, tw - 64, 0)
y = place_middle(PH + 10, by, blk)
text(s, M, y, tw, [label('Giving Tuesday, December 1')], 'Label'); y += 44
text(s, M, y, tw, tp, 'Title'); y += measure(tp, tw, 0) + 28
png(s, 'brandq-green.png', M, y + 4, 40, 'Quote mark')
text(s, M + 64, y, tw - 64, qp, 'Quote'); y += measure(qp, tw - 64, 0) + 14
text(s, M + 64, y, tw - 64, ap, 'Quote attribution')
d.save('out/ig/03 Giving Tuesday.pptx'); posts.append('03 Giving Tuesday')

# ---------- 4. Giving Tuesday Stories, live progress (1080x1920), 3 versions
SW, SH = 1080, 1920
d = Deck(SW, SH)
for when, line, pct in [('Morning', 'Every gift today is doubled.', 0.2),
                        ('Afternoon', 'We are on our way. Every gift is still doubled.', 0.55),
                        ('Last hours', 'Last hours of the match. Every gift is still doubled.', 0.85)]:
    s = d.page(DG)
    png(s, 'hay-top.png', -2, -2, SW + 4, 'Hay swoosh element', 300)
    tw = SW - 2 * M; BW_ = tw
    lab = [P('Giving Tuesday, December 1', 'Montserrat', 36, LIV, True, 1.25, align='c')]
    amt = [P('[AMOUNT RAISED]', 'EB Garamond', 96, WHITE, lh=1.0, align='c')]
    gl = [P('raised of our $300,000 goal', 'EB Garamond', 56, PALE, lh=1.1, align='c')]
    msg = [P(line, 'EB Garamond', 64, WHITE, lh=1.15, align='c')]
    giv = [P('Give at ' + URL, 'Source Sans 3', 40, PALE, lh=1.3, align='c')]
    parts = [(lab, 40), (amt, 24), (gl, 70), ('bar', 120), (msg, 40), (giv, 0)]
    hgt = lambda p: 36 + 20 + 42 if p == 'bar' else measure(p, tw, 0)
    tot = sum(hgt(p) + g for p, g in parts)
    LG = 120; lw = round(LG * 464 / 403); ly = SH - 200 - LG
    y = 300 + (ly - 60 - 300 - tot) / 2
    names = {id(lab): 'Label', id(amt): 'Amount raised', id(gl): 'Goal', id(msg): 'Message', id(giv): 'Give line'}
    for p, g in parts:
        if p == 'bar':
            rect(s, M, y, BW_, 36, '#34532F', 'Progress bar track')
            rect(s, M, y, round(BW_ * pct), 36, LIV, 'Progress bar fill (drag to the amount)')
            text(s, M, y + 56, BW_ / 2, [P('$0', 'Source Sans 3', 32, PALE, lh=1.3)], 'Scale start')
            text(s, M + BW_ / 2, y + 56, BW_ / 2, [P('$300,000', 'Source Sans 3', 32, PALE, lh=1.3, align='r')], 'Scale end')
        else:
            text(s, M, y, tw, p, names[id(p)])
        y += hgt(p) + g
    png(s, 'logo-white.png', (SW - lw) / 2, ly, lw, 'SFW logo', LG)
    text(s, M, SH - 120, 400, [P(when, 'Montserrat', 28, '#5F6A3C', True, 1.2)], 'Version note (delete before posting)')
d.save('out/ig/04 Giving Tuesday Stories progress.pptx'); posts.append('04 Giving Tuesday Stories progress')

# ---------- 5. World Soil Day (Dec 5)
d = Deck(W, H); s = d.page()
PH = curve_photo(s, 'ig/walk-fields.jpg', W, 640, 0.5, 'Walking to the fields, India 2026')
cta = [P('Give in her name at ' + URL, 'EB Garamond', 44, WHITE, lh=1.15)]
by = band(s, W, H, 170, cta)
qp = [P('"Let me teach you so that you can do this for yourself."', 'EB Garamond', 72, DG, lh=1.12, align='c')]
ap = [P('Dr. Elaine Ingham', 'Source Sans 3', 32, GR, True, 1.3, align='c')]
tw = W - 2 * M
blk = 50 + measure(qp, tw, 0) + 24 + measure(ap, tw, 0)
y = place_middle(PH + 10, by, blk)
text(s, M, y, tw, [P('World Soil Day, December 5', 'Montserrat', 28, GR, True, 1.25, align='c')], 'Label'); y += 50
text(s, M, y, tw, qp, 'Quote'); y += measure(qp, tw, 0) + 24
text(s, M, y, tw, ap, 'Quote attribution')
d.save('out/ig/05 World Soil Day.pptx'); posts.append('05 World Soil Day')

# ---------- 6. TrashIt scholar story (week of Dec 7)
d = Deck(W, H); s = d.page()
PH = 600
rect(s, -4, -4, W + 8, PH + 4, '#E4E9DA', 'Photo placeholder')
text(s, M, PH / 2 - 30, W - 2 * M, [P('[Photo: TrashIt team in Pakistan]', 'Source Sans 3', 40, '#7D8A55', True, 1.3, align='c')], 'Placeholder note')
cta = [P('$5,000 funds a full scholarship.', 'EB Garamond', 48, WHITE, lh=1.15),
       P('Give at ' + URL, 'Source Sans 3', 32, PALE, lh=1.4, before=10)]
by = band(s, W, H, 200, cta)
tp = [P('600+ people reached in Pakistan', 'EB Garamond', 72, DG, lh=1.08)]
bp = [body('Both founders of TrashIt in Pakistan trained with us, and TrashIt now offers microbial soil testing to farmers.', 40, INK, lh=1.4)]
tw = W - 2 * M
blk = 44 + measure(tp, tw, 0) + 26 + measure(bp, tw, 0)
y = place_middle(PH, by, blk)
text(s, M, y, tw, [label('Scholar story, Pakistan')], 'Label'); y += 44
text(s, M, y, tw, tp, 'Title'); y += measure(tp, tw, 0) + 26
text(s, M, y, tw, bp, 'Body')
d.save('out/ig/06 TrashIt scholar story.pptx'); posts.append('06 TrashIt scholar story')

# ---------- 7. Alumni story, monthly giving (week of Dec 14)
d = Deck(W, H); s = d.page()
PH = curve_photo(s, 'ig/bucket-chain.jpg', W, 580, 0.35, 'Filling the compost bin, India 2026')
cta = [P('Join the Living Soil Circle: $100 a month', 'EB Garamond', 44, WHITE, lh=1.15),
       P('funds scholarships all year. ' + URL, 'Source Sans 3', 32, PALE, lh=1.4, before=10)]
by = band(s, W, H, 200, cta)
q = 'I am so excited to continue this amazing journey as I unlearn 30 years of agrochemical farming and move down the regenerative path to biological understanding.'
qh = measure([P(q, 'EB Garamond', 52, DG, lh=1.18)], W - 2 * M - 80, 0) + 20 + 42 + 50
y = place_middle(PH + 10, by, qh)
text(s, M, y, W - 2 * M, [label('Alumni story')], 'Label')
quote_block(s, M, y + 50, W - 2 * M, q, 'Norman Higgins, certified SFW lab tech, New Zealand', 52)
d.save('out/ig/07 Alumni story monthly giving.pptx'); posts.append('07 Alumni story monthly giving')

# ---------- 8. Thank you (early January)
d = Deck(W, H); s = d.page()
PH = curve_photo(s, 'ig/cert-group.jpg', W, 640, 0.3, 'October 2026 cohort with certificates, India')
by = band(s, W, H, 150, [P('soilfoodweb.com', 'Source Sans 3', 36, PALE, lh=1.3)])
tp = [P('Thank you.', 'EB Garamond', 96, DG, lh=1.0, align='c')]
bp = [P('Together you raised [TOTAL RAISED] for scholarships this season.', 'EB Garamond', 48, DG, lh=1.2, align='c')]
tw = W - 2 * M
blk = 44 + measure(tp, tw, 0) + 28 + measure(bp, tw, 0)
y = place_middle(PH + 10, by, blk)
text(s, M, y, tw, [P('Year-end 2026', 'Montserrat', 28, GR, True, 1.25, align='c')], 'Label'); y += 44
text(s, M, y, tw, tp, 'Title'); y += measure(tp, tw, 0) + 28
text(s, M, y, tw, bp, 'Body')
d.save('out/ig/08 Thank you.pptx'); posts.append('08 Thank you')

# ---------- 9. Board LinkedIn images (1200x1200)
LW_, LH_ = 1200, 1200
d = Deck(LW_, LH_)
for photo, fy, alt, lab, title, sub in [
    ('ig/group-bin.jpg', 0.3, 'Workshop group at the compost bin, India 2026', 'Year-end campaign 2026',
     'Help us raise $300,000 for scholarships by December 31.', 'Give at ' + URL),
    ('ig/filling-bin.jpg', 0.55, 'Building a compost pile, India 2026', 'Giving Tuesday, December 1',
     'On Giving Tuesday, every gift is doubled.', 'Give at ' + URL),
    ('ig/microscopy-class.jpg', 0.3, 'Soil microscopy class, India 2026', 'Fund a scholar',
     '$5,000 funds a full scholarship, a $10,000 value.', 'Foundation Courses and The Complete Practicum. ' + URL)]:
    s = d.page()
    PH = curve_photo(s, photo, LW_, 560, fy, alt)
    by = band(s, LW_, LH_, 150, [P(sub, 'Source Sans 3', 32, PALE, lh=1.35)])
    tp = [P(title, 'EB Garamond', 72, DG, lh=1.1)]
    tw = LW_ - 2 * M
    blk = 44 + measure(tp, tw, 0)
    y = place_middle(PH + 10, by, blk)
    text(s, M, y, tw, [label(lab)], 'Label'); y += 44
    text(s, M, y, tw, tp, 'Title')
d.save('out/ig/09 Board LinkedIn images.pptx'); posts.append('09 Board LinkedIn images')
print(posts)
