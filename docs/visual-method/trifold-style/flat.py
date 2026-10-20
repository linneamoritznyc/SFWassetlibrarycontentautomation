"""Trifold-style carousels: flat brand colours, hard edges, one curve running across every slide,
photos clipped by that curve, full-colour boxes that overlap photos and cross the slide seams.
No gradients, no fades."""
import sys, math, os
from posts7c import photo, IMG
from lib import *

OUT = '/home/claude/p05/flat'
DL = '../../../p05/dl/'
GREEN = (21, 104, 38); MOSS = (34, 55, 31); SOIL = (79, 52, 51); EDU = (55, 128, 184)
SPEC = (230, 234, 220); CREAMS = (244, 241, 234); TAN = (200, 155, 123); WHITE = (255, 255, 255); INKC = (51, 49, 48)


class Strip:
    def __init__(self, n, bg=WHITE):
        self.n = n; self.C = Image.new('RGBA', (W * n, H), bg + (255,)); self.t = []

    def curve(self, base, amp, waves, phase=0.0):
        PW = W * self.n
        return [(x, base + amp * math.sin(2 * math.pi * waves * x / PW + phase)) for x in range(0, PW + 1, 6)]

    def photo(self, img, x0, x1, y0, y1, clip=None, below=False, fx=0.5, fy=0.5):
        """clip: curve points; the photo keeps the side of the curve toward y0 (or y1 if below)."""
        ph = photo(img, x1 - x0, y1 - y0, fx=fx, fy=fy)
        m = Image.new('L', ph.size, 255)
        if clip:
            pts = [(x - x0, y - y0) for x, y in clip if x0 - 6 <= x <= x1 + 6]
            poly = ([(pts[0][0], -10)] + pts + [(pts[-1][0], -10)]) if below else ([(pts[0][0], y1 - y0 + 10)] + pts + [(pts[-1][0], y1 - y0 + 10)])
            ImageDraw.Draw(m).polygon(poly, fill=0)
        self.C.paste(ph, (x0, y0), m)

    def box(self, x0, y0, x1, y1, col):
        ImageDraw.Draw(self.C).rectangle((x0, y0, x1, y1), fill=col + (255,))

    def band(self, pts, col, up=True):
        """Fill everything above (or below) the curve with a flat colour."""
        PW = W * self.n
        poly = [(0, -10)] + pts + [(PW, -10)] if up else [(0, H + 10)] + pts + [(PW, H + 10)]
        ImageDraw.Draw(self.C).polygon(poly, fill=col + (255,))

    def text(self, slide, t, x, y, w, size, col, font, align='l'):
        self.t.append((slide, (t, x, y, w, size, col, font, align)))

    def eyebrow(self, slide, t, x, y, col, w=900):
        self.text(slide, '   '.join(' '.join(wd) for wd in t.upper().split()), x, y, w, 26, col, 'e')

    def slides(self, logo=None):
        S = []
        for i in range(self.n):
            S.append({'bg': self.C.crop((i * W, 0, (i + 1) * W, H)), 'texts': [t for s, t in self.t if s == i], 'flat': True})
        if logo: S[logo[0]]['logo'] = logo[1]
        return S


# ============ World Earthworm Day: photos across the top, one wave, colour blocks riding the wave
def p08():
    n = 7; s = Strip(n); PW = W * n
    wave = s.curve(900, 70, 2.0)
    ph = ['hand-wet-dirt-worm.jpg', 'handling-loose-soil.jpg', 'hand-soil-roots-fungi.jpg', 'hand-scooping-planter-bed-soil.jpg',
          'fist-of-dry-soil.jpg', '2-hands-planting-shrub.jpg', 'hand-of-compost.jpg']
    cuts = [0, 1350, 2500, 3550, 4700, 5750, 6650, PW]   # photo edges fall inside slides, never on the seams
    for i, p in enumerate(ph): s.photo(p, cuts[i], cuts[i + 1], 0, 1000, clip=wave)
    # flat blocks that straddle the wave and the seams
    blocks = [(70, 740, 1010, 1130, GREEN), (1160, 800, 2060, 1100, MOSS), (2240, 860, 3150, 1160, SOIL), (3300, 760, 4230, 1060, GREEN),
              (4370, 820, 5300, 1180, MOSS), (5440, 790, 6350, 1090, SOIL), (6540, 740, 7470, 1060, GREEN)]
    # thin colour rules that run on across each seam, tying the slides together
    pass
    for x0, y0, x1, y1, c in blocks: s.box(x0, y0, x1, y1, c)
    copy = [('World Earthworm Day, 21 October', 'How do worms work their magic?', None),
            ('Burrows', 'They dig.', 'Down 1 to 2 meters, breaking up compaction.'),
            ('Burrow walls', 'They spread microbes.', 'Lined with mucus and casts, rich in microbes.'),
            ('Rain', 'They build the plumbing.', 'Water soaks in fast. The ground stays aerobic.'),
            ('Your turn', 'How do we care for them?', None),
            ('No-dig', 'Put the spade down.', 'Digging cuts the burrows.'),
            ('Mulch', 'Feed them.', 'Leave organic matter where it falls.')]
    for i, (x0, y0, x1, y1, c) in enumerate(blocks):
        sl = i; lx = x0 - sl * W + 50
        if lx + (x1 - x0) > W: sl = x0 // W; lx = x0 - sl * W + 50
        eb, hd, sub = copy[i]
        s.eyebrow(sl, eb, lx, y0 + 46, (167, 176, 151), w=x1 - x0 - 100)
        s.text(sl, hd, lx, y0 + 96, min(x1 - x0 - 100, W - lx - 40), 76, WHITE, 'm')
        if sub: s.text(sl, sub, lx, y1 + 30, min(860, W - lx - 60), 46, INKC, 's')
    return export('world-earthworm-day', s.slides(logo=(6, (W - 170, H - 160))), f'{OUT}/p08')


# ============ Costa Rica: green band on top with a curved lower edge across all slides, photos underneath,
# one white event card crossing slide 1 into slide 2
def p14():
    n = 4; s = Strip(n); PW = W * n
    edge = s.curve(470, 60, 1.0, phase=0.6)
    s.photo('workshop-group-around-compost-pile.jpg', 0, 1700, 300, H, fy=0.55)
    s.photo('costa-rica-2025-gerald-liquid-amendments.jpg', 1700, 2900, 300, H)
    s.photo('costa-rica-2025-microscopy-students-mentors.jpg', 2900, PW, 300, H)
    s.band(edge, GREEN, up=True)
    s.box(120, 860, 1010, 1270, WHITE); s.box(1010, 1130, 1500, 1270, SOIL)
    ImageDraw.Draw(s.C).rectangle((146, 886, 984, 1244), outline=(190, 190, 186, 255), width=2)
    s.eyebrow(0, 'Accelerator Workshop', 90, 120, (167, 176, 151))
    s.text(0, 'Costa Rica', 90, 170, 900, 104, WHITE, 'm')
    s.text(0, 'Compost is a team sport.', 180, 930, 780, 64, MOSS, 'm')
    s.text(0, '18 to 25 January 2027', 180, 1100, 780, 44, INKC, 's')
    s.text(1, 'Link in bio', 20, 1170, 400, 40, WHITE, 'e')
    s.text(1, 'Students build the piles together, by hand.', 90, 120, 880, 56, WHITE, 'm')
    s.text(2, 'Then they read the samples under the microscope,', 90, 120, 880, 56, WHITE, 'm')
    s.text(3, 'side by side.', 90, 120, 880, 56, WHITE, 'm')
    return export('costa-rica-compost-together', s.slides(logo=(3, (W - 170, H - 160))), f'{OUT}/p14')


# ============ Natalia: scholarship = Education Blue. Her portrait, a blue field that starts under her
# and runs across the seam, then a garden photo cut by the same diagonal curve
def d18():
    n = 4; s = Strip(n); PW = W * n
    diag = [(x, 1250 - 0.13 * x) for x in range(0, PW + 1, 6)]
    s.photo(DL + 'natalia-pulido.jpg', 0, 1250, 0, H, clip=diag, fx=0.38)
    s.band(diag, EDU, up=False)
    s.box(1250, 0, 2160, 1350, EDU)
    s.photo('erc-panchamana-garden.jpg', 2160, PW, 0, H, clip=[(x, y - 60) for x, y in diag], below=False)
    s.box(3020, 860, 4100, 1180, GREEN)
    s.box(60, 900, 820, 1150, GREEN)
    s.eyebrow(0, 'Scholarship recipient', 110, 945, (167, 176, 151))
    s.text(0, 'Natalia Pulido', 110, 1000, 700, 76, WHITE, 'm')
    s.text(1, 'Jenesano, Boyacá, Colombia', 260, 140, 700, 40, WHITE, 'e')
    s.text(1, 'Steep, heavy clay. Her family land in the Andes.', 260, 210, 720, 70, WHITE, 'm')
    s.text(1, 'She is restoring it with her siblings, and sharing every step on her platform, Rural Tempo.', 262, 560, 700, 46, WHITE, 's')
    s.text(3, 'Your donations make this possible.', 40, 900, 960, 56, WHITE, 'm')
    s.text(3, 'soilfoodweb.com/donate', 42, 1075, 900, 38, (167, 176, 151), 'e')
    return export('scholarship-natalia-pulido', s.slides(logo=(3, (W - 170, 60))), f'{OUT}/d18')


if __name__ == '__main__':
    for k in sys.argv[1:] or ['p08', 'p14', 'd18']:
        p = globals()[k](); sheet(p, f'{OUT}/sheet-{k}.jpg', tw=300); print(k, len(p))
    from PIL import Image
    r = [Image.open(f'{OUT}/sheet-{k}.jpg') for k in ['p08', 'p14', 'd18'] if os.path.exists(f'{OUT}/sheet-{k}.jpg')]
    S = Image.new('RGB', (max(i.width for i in r), sum(i.height + 8 for i in r)), 'white'); y = 0
    for i in r: S.paste(i, (0, y)); y += i.height + 8
    S.save(f'{OUT}/samples.jpg', quality=85)
