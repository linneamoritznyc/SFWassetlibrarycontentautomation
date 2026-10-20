"""Next 7 posts, Fibershed / Apricot Lane look: white, photos, cutouts on white, white cards."""
import sys, math, random, os
from PIL import ImageEnhance
from lib import *

IMG = '/home/claude/linneamoritznyc/final-sfwsite-linnea/img/'
OUT = '/home/claude/p05/next7c'
WHITE = (255, 255, 255)
GREY = (190, 190, 186)
GR = (34, 55, 31)


def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.08)
    r, g, b = im.split(); r = r.point(lambda v: min(255, int(v * 1.03 + 3))); b = b.point(lambda v: int(v * 0.97))
    return Image.merge('RGB', (r, g, b))


def photo(name, w=W, h=H, fx=0.5, fy=0.5):
    im = Image.open(IMG + name).convert('RGB'); s = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy)
    return grade(im.crop((x, y, x + w, y + h))).convert('RGBA')


def scrim(C, top=True, h=560, a=150):
    h = max(h, 700); a = max(a, 205)
    v = Image.new('RGBA', C.size, (0, 0, 0, 0)); d = ImageDraw.Draw(v)
    for i in range(h):
        al = int(a * (1 - i / h) ** 1.5); y = i if top else C.height - 1 - i
        d.line((0, y, C.width, y), fill=(10, 14, 10, al))
    C.alpha_composite(v)


def white(w=W, h=H):
    return Image.new('RGBA', (w, h), WHITE + (255,))


def card(C, x, y, w, h, frame=True):
    s = Image.new('RGBA', (w, h), WHITE + (255,))
    if frame: ImageDraw.Draw(s).rectangle((18, 18, w - 19, h - 19), outline=GREY + (255,), width=2)
    place(C, s, x + w / 2, y + h, off=(0, 8), blur=18, alpha=0.25)


def obj(C, f, cx, by, w=None, h=None, rot=0, flip=False):
    place(C, cut(f, w=w, h=h, rot=rot, flip=flip), cx, by, off=(8, 12), blur=14, alpha=0.22)


def roundel(C, f, cx, cy, d):
    place(C, lens(f, d, ring=0), cx, cy + d / 2, off=(6, 10), blur=14, alpha=0.22)


def K(t, x, y, col=GR, w=900, a='l'):  # small uppercase kicker
    return (t.upper(), x, y, w, 30, col, 'b', a)


def save(name, slides, sub, h=H):
    p = export(name, slides, f'{OUT}/{sub}', h=h); sheet(p, f'{OUT}/sheet-{sub}.jpg'); return p


# 1 ---------------- Elena, HealTerra
def elena():
    S = []
    a = photo('gloved-hands-red-bucket-mulch.jpg'); scrim(a, top=False, h=700, a=190)
    S.append({'bg': a, 'texts': [K('Soil Regenerators in the wild', 90, 960, CREAM), ('Food waste goes in. Living compost comes out.', 90, 1010, 900, 80, CREAM, 'i')]})
    b = white(); obj(b, FL + 's8-05-earthworm.png', 420, 1150, w=560, rot=-8); obj(b, FL + 's7-02-earthworm.png', 720, 1230, w=420, rot=25)
    S.append({'bg': b, 'texts': [K('Elena Lininger, HealTerra', 90, 120), ('Local food waste goes into a worm digester and comes out as compost and castings.', 90, 170, 900, 64, GR, 'i')]})
    c = photo('pile-turning-wes-8-scaled.jpg', fy=0.4); scrim(c, h=520, a=160)
    S.append({'bg': c, 'texts': [('Southern Oregon', 90, 110, 900, 84, CREAM, 'i'), ('Compost and worm castings, made close to home.', 92, 220, 880, 42, CREAM, 'r')]})
    d = white(); obj(d, FL + 's4-05-fern-fiddlehead.png', 540, 1220, h=520)
    S.append({'bg': d, 'texts': [('Part of the nonprofit Source One Serenity, with trail stewardship and outdoor programs for veterans.', 90, 150, 900, 64, GR, 'i')]})
    e = photo('Test tubes with sample_.jpg'); card(e, 90, 900, 900, 360)
    S.append({'bg': e, 'texts': [K('Built by our community', 140, 960, GR, 800, 'c'), ('A compost extractor built by SFW students, and biological testing with another graduate.', 140, 1020, 800, 48, GR, 'i', 'c')]})
    f = white(); obj(f, FL + 's8-02-compost-fungal-threads.png', 540, 1180, w=560)
    S.append({'bg': f, 'texts': [('Follow @healterra_org', 90, 150, 900, 84, GR, 'i', 'c'), ('Our community at its best.', 90, 270, 900, 42, GR, 'r', 'c')], 'logo': (W - 170, H - 160)})
    return save('elena-healterra', S, '1-elena')


# 2 ---------------- Earthworm story 9:16
def worm_story():
    HS = 1920; S = []
    a = photo('hand-wet-dirt-worm.jpg', W, HS); scrim(a, h=760, a=170)
    S.append({'bg': a, 'texts': [('"Is World Earthworm Day even a thing?"', 90, 200, 900, 100, CREAM, 'i')]})
    b = white(W, HS); obj(b, FL + 's8-05-earthworm.png', 540, 1600, w=760, rot=-6)
    S.append({'bg': b, 'texts': [("Yes, it's real.", 90, 200, 900, 100, GR, 'i'), ('In 2016 the Earthworm Society of Britain nominated 21 October as World Earthworm Day, to honour Charles Darwin, whose worm book came out that month.', 92, 350, 880, 50, GR, 'r')]})
    c = white(W, HS); txt = [('Which earthworm are you today?', 90, 170, 900, 88, GR, 'i')]
    rows = [('1. Epigeic', 'Lives in the leaf litter and eats fast.', 's8-06-dry-leaves.png', 's7-02-earthworm.png'),
            ('2. Endogeic', 'Stays in the topsoil and eats its way through it.', 's8-04-dark-soil.png', 's8-05-earthworm.png'),
            ('3. Anecic', 'Digs deep burrows and comes up at night.', None, 's8-05-earthworm.png')]
    for k, (nm, t, base, worm) in enumerate(rows):
        y = 560 + k * 440
        if base: obj(c, FL + base, 270, y + 330, w=340)
        obj(c, FL + worm, 270, y + 300, w=300 if k < 2 else 280, rot=[10, -15, -80][k])
        txt += [(nm, 500, y + 90, 520, 56, GR, 'i'), (t, 502, y + 170, 500, 40, GR, 'r')]
    S.append({'bg': c, 'texts': txt, 'logo': (W - 170, HS - 170)})
    return save('earthworm-story', S, '2-earthworm-story', h=HS)


# 3 ---------------- World Earthworm Day
def earthworm_day():
    S = []
    a = white(); obj(a, FL + 's8-05-earthworm.png', 540, 1230, w=860, rot=-4)
    S.append({'bg': a, 'texts': [K('World Earthworm Day, 21 October', 90, 120), ('How do worms work their magic?', 90, 170, 900, 104, GR, 'i')]})
    b = photo('handling-loose-soil.jpg'); scrim(b, h=520, a=170)
    S.append({'bg': b, 'texts': [('They dig.', 90, 110, 900, 104, CREAM, 'i'), ('Anecic earthworms dig vertical burrows 1 to 2 meters deep and break up compaction.', 92, 250, 880, 44, CREAM, 'r')]})
    c = white()
    for f, x, y, d in [(SRC + 'Ciliate, 60x obj, Patricia J Coppola.jpg', 330, 780, 400), (SRC + 'Testate amoeba, 40x obj, Joy Kaluf.jpg', 760, 900, 330), (SRC + 'Bacterial-feeding nematode, 40x obj, Casey Williams.jpg', 420, 1150, 300)]:
        roundel(c, f, x, y, d)
    S.append({'bg': c, 'texts': [('They spread microbes.', 90, 120, 900, 96, GR, 'i'), ('They line the burrow walls with mucus and casts, rich in nutrients and microbes.', 92, 250, 880, 44, GR, 'r')]})
    e = photo('hand-scooping-planter-bed-soil.jpg'); scrim(e, h=540, a=170)
    S.append({'bg': e, 'texts': [('They build the plumbing.', 90, 110, 900, 96, CREAM, 'i'), ('Their channels let rain soak in fast, so the ground stays aerobic.', 92, 340, 880, 44, CREAM, 'r')]})
    f = white()
    S.append({'bg': f, 'texts': [('How do we care for them?', 120, 560, 840, 112, GR, 'i', 'c')]})
    g = photo('2-hands-planting-shrub.jpg'); card(g, 90, 930, 900, 330)
    S.append({'bg': g, 'texts': [('Put the spade down.', 140, 990, 800, 76, GR, 'i', 'c'), ('Digging cuts the burrows. No-dig keeps the plumbing intact.', 140, 1090, 800, 42, GR, 'r', 'c')]})
    h = white(); obj(h, FL + 's8-06-dry-leaves.png', 380, 1220, w=600); obj(h, FL + 's8-03-wood-chips.png', 760, 1250, w=460); obj(h, FL + 's8-05-earthworm.png', 560, 1290, w=300, rot=-30)
    S.append({'bg': h, 'texts': [('Feed them.', 90, 120, 900, 104, GR, 'i'), ('Add organic matter, or simply leave it where it falls.', 92, 260, 880, 46, GR, 'r')], 'logo': (W - 170, 60)})
    return save('world-earthworm-day', S, '3-earthworm-day')


# 4 ---------------- Smell is a lab result
def vial(col):
    v = Image.new('RGBA', (260, 600), (0, 0, 0, 0)); vd = ImageDraw.Draw(v)
    vd.rounded_rectangle((60, 60, 200, 580), radius=66, fill=(236, 240, 242, 255), outline=(210, 214, 216, 255), width=5)
    vd.rounded_rectangle((70, 300, 190, 570), radius=58, fill=col + (255,)); vd.rectangle((50, 20, 210, 70), fill=(150, 108, 70, 255))
    return v


def smell():
    S = []
    a = photo('ctpfw-student-squeezing-compost-1.jpg'); scrim(a, h=560, a=180)
    S.append({'bg': a, 'texts': [('"Smell is a lab result."', 90, 110, 900, 104, CREAM, 'i'), ('What your compost is telling you.', 92, 250, 880, 46, CREAM, 'r')]})
    data = [('NH3', 'Ammonia', 'Nitrogen is leaving the pile as gas. Too much nitrogen, or the pH is too high.', (226, 214, 120)),
            ('H2S', 'Hydrogen sulfide, rotten eggs', 'Sulfate-reducing bacteria have taken over. There is zero oxygen.', (214, 190, 80)),
            ('CH3COOH', 'Acetic and butyric acid, vinegar or vomit', 'Fermentation products. Both are toxic to roots.', (206, 150, 160)),
            ('Geosmin', 'Earthy', 'Made by actinomycetes. This is the smell of an aerobic pile.', (130, 170, 100))]
    for form, name, txt, col in data:
        c = white(); place(c, vial(col), 820, 1270, off=(8, 12), blur=14, alpha=0.2)
        S.append({'bg': c, 'texts': [(form, 90, 130, 900, 150 if len(form) < 6 else 110, GR, 'r'), (name, 92, 380, 560, 54, GR, 'i'), (txt, 92, 540, 540, 42, GR, 'r')]})
    im = Image.open(SRC + 'Ciliate, 60x obj, Patricia J Coppola.jpg').convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s))); im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).convert('RGBA')
    card(im, 90, 960, 900, 300)
    S.append({'bg': im, 'texts': [('Under the microscope, ciliates confirm it.', 140, 1010, 800, 56, GR, 'i', 'c'), ('They indicate anaerobic conditions. Ciliate, 60x, photo Patricia J Coppola.', 140, 1150, 800, 32, GR, 'r', 'c')]})
    t = white(); th = Image.new('RGBA', (220, 900), (0, 0, 0, 0)); td = ImageDraw.Draw(th)
    td.rounded_rectangle((70, 0, 150, 760), radius=40, fill=(240, 242, 242, 255), outline=(200, 204, 206, 255), width=4); td.ellipse((40, 700, 180, 840), fill=(196, 64, 50, 255))
    td.rounded_rectangle((92, 300, 128, 760), radius=18, fill=(196, 64, 50, 255))
    for k in range(0, 700, 40): td.line((150, k + 30, 172 if k % 120 == 0 else 162, k + 30), fill=(150, 150, 150, 255), width=3)
    place(t, th, 820, 1300, off=(8, 12), blur=14, alpha=0.2)
    S.append({'bg': t, 'texts': [('The fix: structure and oxygen.', 90, 130, 900, 90, GR, 'i'), ('Keep the pile at 55 to 68°C, and turn it when it goes above 68°C.', 92, 360, 580, 46, GR, 'r')], 'logo': (60, H - 160)})
    return save('smell-is-a-lab-result', S, '4-smell')


# 5 ---------------- Christina Olivero
def christina():
    S = []
    a = white(); obj(a, FL + 's1-08-seedling.png', 540, 1150, w=820)
    S.append({'bg': a, 'texts': [K('This one makes our hearts full', 90, 140, GR, 900, 'c'), ('From advertising to a soil business.', 120, 220, 840, 100, GR, 'i', 'c')]})
    b = photo('2-hands-clasped-holding-plant-roots.jpg'); card(b, 90, 900, 900, 360)
    S.append({'bg': b, 'texts': [('Christina Olivero', 140, 950, 800, 80, GR, 'i', 'c'), ('Alter Eco Farms, Chattanooga, Tennessee', 140, 1060, 800, 40, GR, 'r', 'c'), (K('Soil Regenerators in the wild', 140, 1150, GR, 800, 'c'))]})
    im = Image.open(SRC + 'Ciliate, 60x obj, Patricia J Coppola.jpg').convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s))); im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).convert('RGBA')
    scrim(im, top=False, h=700, a=200)
    S.append({'bg': im, 'texts': [('It started with one free webinar on protozoa.', 90, 930, 900, 80, CREAM, 'i'), ('A lifelong love of biology, very little farming experience, and she kept going.', 92, 1140, 880, 40, CREAM, 'r')]})
    c = photo('soil-sample-close-up-test-tube.jpg'); card(c, 90, 90, 900, 400)
    S.append({'bg': c, 'texts': [('Today: workshops, biological amendments and soil tests.', 140, 150, 800, 60, GR, 'i', 'c'), ('Christina, we are so proud of what you have built.', 140, 370, 800, 38, GR, 'r', 'c')], 'logo': (W - 170, H - 160)})
    return save('christina-olivero', S, '5-christina')


# 6 ---------------- New website
def website():
    S = []
    a = photo('workshop-group-around-compost-pile.jpg'); card(a, 140, 420, 800, 460)
    S.append({'bg': a, 'texts': [K('New on soilfoodweb.com', 190, 490, GR, 700, 'c'), ('Our new home is live.', 190, 560, 700, 92, GR, 'i', 'c'), ('Come and look around.', 190, 760, 700, 40, GR, 'r', 'c')]})
    pages = [('cy-classes-3.jpg', 'Courses', 'Every course, in one learning path.'),
             ('aug2023-workshop-group-7.jpg', 'Workshops', 'Every workshop, past and upcoming.'),
             ('erc-panchamana-treeplanting-3-fb-img-1666271008784.jpg', 'Consultants', 'Find a soil consultant near you.'),
             ('Dr Elaine Ingham with Microscope.jpg', 'Library', "Dr. Elaine's papers, in one place.")]
    for f, k, t in pages:
        c = white(); ph = photo(f, 900, 900); place(c, ph, 540, 1260, off=(0, 8), blur=18, alpha=0.2)
        S.append({'bg': c, 'texts': [K(k, 90, 110), (t, 90, 160, 900, 72, GR, 'i')]})
    z = white()
    for f, x, y, w_ in [('norfolk-common-poppy.png', 260, 1260, 300), ('tamil-nadu-marigold.png', 560, 1290, 300), ('costa-rica-heliconia.png', 830, 1270, 280)]: obj(z, FL + f, x, y, w=w_)
    S.append({'bg': z, 'texts': [('Come on in.', 90, 200, 900, 110, GR, 'i', 'c'), ('soilfoodweb.com, link in bio.', 90, 340, 900, 46, GR, 'r', 'c')], 'logo': (W // 2 - 60, 60)})
    return save('new-website', S, '6-website')


# 7 ---------------- Leave the leaves
def leaves():
    S = []; r = random.Random(3)
    a = white()
    for _ in range(9): obj(a, FL + 's8-06-dry-leaves.png', r.randint(80, 1000), r.randint(820, 1400), w=r.randint(220, 380), rot=r.randint(0, 360))
    S.append({'bg': a, 'texts': [K('International Day of Climate Action, 24 October', 90, 120), ('Before you rake and bag those leaves, read this.', 90, 170, 900, 92, GR, 'i')]})
    b = photo('harringtons-organic-land-care-brick-york-farms-2-768x1024.jpg'); card(b, 90, 960, 900, 300)
    S.append({'bg': b, 'texts': [K('Myth', 140, 1020, GR, 800, 'c'), ('Fall leaves need to be cleaned up.', 140, 1080, 800, 66, GR, 'i', 'c')]})
    c = photo('hand-soil-roots-fungi.jpg'); scrim(c, h=560, a=180)
    S.append({'bg': c, 'texts': [('Leaf litter is rich in carbon and lignin.', 90, 110, 900, 88, CREAM, 'i'), ('And fungi are the main decomposers of lignin.', 92, 320, 880, 44, CREAM, 'r')]})
    d = white(); roundel(d, SRC + 'Fungal hypha, 100x obj, Marco Trevisan.jpg', 380, 880, 480); obj(d, FL + 's4-03-mushrooms.png', 780, 1290, w=360)
    S.append({'bg': d, 'texts': [('That feeds the fungal soils trees and shrubs prefer.', 90, 120, 900, 80, GR, 'i'), ('Fungal hypha, 100x, photo Marco Trevisan.', 92, 1260, 500, 30, GR, 'r')]})
    e = photo('fungi-in-under-grape-soil.jpg'); scrim(e, h=520, a=170)
    S.append({'bg': e, 'texts': [('A litter layer shields the soil over winter.', 90, 110, 900, 88, CREAM, 'i')]})
    f = white(); obj(f, FL + 's8-06-dry-leaves.png', 540, 1260, w=760)
    S.append({'bg': f, 'texts': [('On lawns: shred the leaves and move them to your beds.', 90, 140, 900, 88, GR, 'i')], 'logo': (W - 170, 60)})
    return save('leave-the-leaves', S, '7-leaves')


if __name__ == '__main__':
    for n in sys.argv[1:] or ['elena', 'worm_story', 'earthworm_day', 'smell', 'christina', 'website', 'leaves']:
        print(n, len(globals()[n]()))
