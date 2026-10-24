"""Visuals for the November and December posts added on 24 October.

Each post gets a look that differs from its neighbours in the grid: full-bleed photo,
big number, specimen in a circle, drawn diagram, type only, numbered steps or brand
boxes. Brand colours, Montserrat, Source Sans 3 and upright EB Garamond only.

  BOX_SRC=<photos> SFW_FONTS=<woff2 dir> python3 tools/wormhole-visuals/feed_novdec.py [ids...]
    -> apps/web/public/wormhole/tiles/<id>-v1-<n>.jpg
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageOps

import boxes as B
import families as F

W, H = B.W, B.H
LW, LH = 1200, 627
OUT = B.OUT

SFW = "Photo: Soil Food Web Foundation"
MIC = {
    "bacteria_gerri.jpg": "Bacteria, 40x objective. Photo: Gerri Gassert",
    "hypha_lee.jpg": "Fungal hypha, 40x objective. Photo: Lee Kirk",
    "ciliates.jpg": "Ciliates. Photo: Soil Food Web Foundation",
    "nematode_sid.jpg": "Bacterial-feeding nematode, 40x objective. Photo: Sid Jensen",
    "collembola.jpg": "Collembola, 40x objective. Photo: Cameron Radman",
    "testate_luke.jpg": "Testate amoeba, 40x objective. Photo: Luke Hardy",
    "actino_ullens.jpg": "Actinobacteria, 40x objective. Photo: Rodrigue Ullens",
}


def credit(d, xy, text, fill):
    d.text(xy, text, font=B.body(26), fill=fill)


# -------------------------------------------------------- D, full-bleed photo


def fullbleed(photo, heading, strip, ink, label=None, cr=SFW, focus=(0.5, 0.5), logo=True):
    """One photo edge to edge, one solid strip across the bottom with the heading."""
    c = B.photo(photo, (W, H), focus)
    d = ImageDraw.Draw(c)
    f = B.fit_heading(d, heading, 920, 300, start=84)
    need = B.measure(d, heading, f, 920) + (56 if label else 0)
    top = H - need - 150
    d.rectangle((0, top, W, H), fill=strip)
    y = top + 50
    if label:
        d.text((70, y), label.upper(), font=B.label_font(32), fill=ink)
        y += 56
    B.block(d, (70, y), heading, f, ink, 920)
    if cr:
        d.rectangle((56, top - 50, 70 + d.textlength(cr, font=B.body(26)) + 14, top - 6), fill=B.DEEP)
        credit(d, (70, top - 44), cr, B.CREAM)
    if logo:
        B.logo(c, (W - 150, 40))
    return c


# ------------------------------------------------------------- B, big number


def bignumber(number, line, photo=None, cr=None, ground=B.CREAM, ink=B.DEEP, focus=(0.5, 0.5), size=210):
    """A huge number in EB Garamond, one line under it, an optional photo in a circle."""
    c = Image.new("RGB", (W, H), ground)
    d = ImageDraw.Draw(c)
    f = F.garamond(size)
    while d.textlength(number, font=f) > 940:
        f = F.garamond(f.size - 10)
    d.text((70, 90), number, font=f, fill=ink)
    y = B.block(d, (78, 110 + int(f.size * 1.05)), line, F.garamond(48), ink, 900, gap=1.25)
    if photo:
        disc = F.round_photo(os.path.join(B.SRC, photo), 560, focus, ring=B.DEEP, ring_w=16)
        c.paste(disc, ((W - disc.width) // 2, max(y + 40, 640)), disc)
        if cr:
            credit(d, (70, H - 70), cr, ink)
    B.logo(c, (W - 150, H - 170))
    return c


# ---------------------------------------------------------------- F, specimen


def specimen(photo, heading, name, ground=B.DEEP, ink=B.CREAM, accent=B.TAN, focus=(0.5, 0.5), cr=None):
    """Deep ground, one microscope specimen in a circle, its name as a label."""
    c = Image.new("RGB", (W, H), ground)
    d = ImageDraw.Draw(c)
    f = B.fit_heading(d, heading, 920, 260, start=80)
    B.block(d, (80, 90), heading, f, ink, 920)
    disc = F.round_photo(os.path.join(B.SRC, photo), 680, focus, ring=accent, ring_w=14)
    c.paste(disc, ((W - disc.width) // 2, 420), disc)
    d.text((80, 1150), name, font=B.label_font(40), fill=accent)
    if cr:
        credit(d, (80, 1220), cr, ink)
    B.logo(c, (W - 150, H - 150))
    return c


# ----------------------------------------------------------------- H, diagram


def diagram_frame(ground, heading, ink):
    c = Image.new("RGB", (W, H), ground)
    d = ImageDraw.Draw(c)
    f = B.fit_heading(d, heading, 920, 230, start=76)
    B.block(d, (80, 80), heading, f, ink, 920)
    return c, d


def rings(heading, labels, colours, highlight=None, ground=B.CREAM, ink=B.BROWN):
    """Concentric rings with a label in each: zones, or a guild around a tree."""
    c, d = diagram_frame(ground, heading, ink)
    cx, cy = W // 2, 800
    n = len(labels)
    for i in reversed(range(n)):
        r = 90 + i * 78
        fill = colours[i % len(colours)]
        if highlight is not None and i != highlight:
            fill = tuple(int(v * 0.35 + g * 0.65) for v, g in zip(fill, ground))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    for i, lab in enumerate(labels):
        r = 90 + i * 78
        y = cy - 22 if i == 0 else cy - r + 12
        f = B.label_font(30 if i else 34)
        w = d.textlength(lab, font=f)
        d.text((cx - w / 2, y), lab, font=f, fill=B.CREAM)
    B.logo(c, (W - 150, H - 150))
    return c


def chain(heading, steps, colours, ground=B.CREAM, ink=B.BROWN, highlight=None):
    """Boxes stacked top to bottom with arrows: who eats whom."""
    c, d = diagram_frame(ground, heading, ink)
    top, bh, gap = 360, 150, 60
    for i, s in enumerate(steps):
        y = top + i * (bh + gap)
        col = colours[i % len(colours)]
        if highlight is not None and i != highlight:
            col = tuple(int(v * 0.35 + g * 0.65) for v, g in zip(col, ground))
        d.rectangle((120, y, 960, y + bh), fill=col)
        f = B.fit_heading(d, s, 760, bh - 40, start=46, least=30)
        lines = B.wrap(d, s, f, 760)
        ty = y + (bh - len(lines) * int(f.size * 1.12)) // 2
        B.block(d, (160, ty), s, f, B.CREAM, 760)
        if i < len(steps) - 1:
            ax = 540
            d.polygon([(ax - 30, y + bh + 8), (ax + 30, y + bh + 8), (ax, y + bh + gap - 8)], fill=ink)
    B.logo(c, (W - 150, H - 150))
    return c


def venn(heading, labels, colours, ground=B.CREAM, ink=B.BROWN):
    """Three overlapping circles, hard edged, with the overlaps left in the ground colour."""
    c, d = diagram_frame(ground, heading, ink)
    centres = [(400, 720), (680, 720), (540, 960)]
    r = 230
    for (x, y), col in zip(centres, colours):
        d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=26)
    for (x, y), lab, col in zip(centres, labels, colours):
        f = B.label_font(40)
        w = d.textlength(lab, font=f)
        dx = {0: -60, 1: 60, 2: 0}[centres.index((x, y))]
        dy = {0: -40, 1: -40, 2: 60}[centres.index((x, y))]
        d.text((x + dx - w / 2, y + dy), lab, font=f, fill=col)
    B.logo(c, (W - 150, H - 150))
    return c


def yesno(heading, yes, no, ground=B.CREAM, ink=B.BROWN):
    """Two flat columns: what goes in, what stays out."""
    c, d = diagram_frame(ground, heading, ink)
    for x, title, items, col in ((80, "YES", yes, B.GREEN), (560, "NO", no, B.BROWN)):
        d.rectangle((x, 340, x + 440, 1180), fill=col)
        d.text((x + 40, 380), title, font=B.head(80), fill=B.CREAM)
        y = 510
        for it in items:
            y = B.block(d, (x + 40, y), it, B.body(40), B.CREAM, 360, gap=1.25) + 30
    B.logo(c, (W - 150, H - 150))
    return c


# --------------------------------------------------------- LinkedIn type card


def li_card(text, ground=B.DEEP, ink=B.CREAM, kicker=None):
    c = Image.new("RGB", (LW, LH), ground)
    d = ImageDraw.Draw(c)
    f = B.fit_heading(d, text, 980, 380, start=78, least=44)
    h = B.measure(d, text, f, 980)
    y = (LH - h) // 2 + (20 if kicker else 0)
    if kicker:
        d.text((90, y - 70), kicker.upper(), font=B.label_font(30), fill=B.LIGHT)
    B.block(d, (90, y), text, f, ink, 980)
    B.logo(c, (LW - 140, LH - 140), size=86)
    return c


T = F.type_slide
S = F.step_slide
BX = B.build  # brand boxes, used through boxes_post below


def boxes_post(pid, slides):
    imgs = []
    for i, s in enumerate(slides):
        layout = s.get("layout") or B.ORDER[i % len(B.ORDER)]
        imgs.append(layout(s, i == 0, i == len(slides) - 1))
    return imgs


GUILD = ["Tree", "Chives", "Comfrey", "Clover"]
GUILD_COL = [B.BROWN, B.PURPLE, B.GREEN, B.LIGHT]
ZONES = ["0", "1", "2", "3", "4", "5"]
ZONE_COL = [B.BROWN, B.GREEN, B.LIGHT, B.TAN, B.BLUE, B.DEEP]
CHAIN = ["Roots feed bacteria and fungi", "Protozoa and nematodes eat them", "Nutrients come out by the root", "The plant takes them up"]
CHAIN_COL = [B.GREEN, B.BLUE, B.TAN, B.BROWN]

POSTS = {
    "x20261108": lambda: [
        T("Happy Diwali.", B.TAN, B.BROWN, size=150),
        T("Light, sweets and marigolds. Every one of them starts in living soil.", B.BROWN, B.CREAM, logo=True),
    ],
    "x20261109": lambda: [li_card("COP31 opens today. Agriculture's own negotiating track runs out in 2026.", kicker="Antalya, 9 to 20 November")],
    "w20261103": lambda: boxes_post("w20261103", [
        dict(label="soilfoodweb.com", heading="Our new website is here.", photo="pile_turn.jpg", credit=SFW),
        dict(heading="Learn: every course, and where to start.", photo="testate_luke.jpg", credit=MIC["testate_luke.jpg"]),
        dict(heading="Workshops and events, past and coming.", photo="misting_pile.jpg", credit=SFW, focus=(0.4, 0.4)),
        dict(heading="Find a consultant near you.", photo="extract_andrew.jpg", credit=SFW),
        dict(heading="Dr. Elaine's research, all in one place.", photo="elaine_cr.jpg", credit="Dr. Elaine Ingham in Costa Rica", layout=B.top),
        dict(heading="Take the tour, link in bio.", photo="rain_soil.jpg", credit="No-till soil after rain", layout=B.cover),
    ]),
    "w20261106": lambda: [
        fullbleed("rain_soil.jpg", "What does living soil look like on a real farm?", B.DEEP, B.CREAM, cr="No-till soil after 2 inches of rain"),
        fullbleed("pile_turn.jpg", "Our new Projects pages show you.", B.TAN, B.BROWN),
        fullbleed("misting_pile.jpg", "Farms, vineyards and restoration sites.", B.GREEN, B.CREAM, focus=(0.4, 0.4)),
        fullbleed("extract_andrew.jpg", "What they changed, and what happened.", B.BROWN, B.CREAM),
    ],
    "x20261117": lambda: [
        venn("Every permaculture design starts with three ethics.", ["Earth", "People", "Fair share"], [B.GREEN, B.BLUE, B.TAN]),
        T("Earth care.", B.GREEN, B.CREAM, kicker="Leave the land more alive", kicker_ink=B.CREAM, size=130),
        T("People care.", B.BLUE, B.CREAM, kicker="Design for who lives there", kicker_ink=B.CREAM, size=130),
        T("Fair share.", B.TAN, B.BROWN, kicker="Return the surplus", kicker_ink=B.BROWN, size=130),
        T("Living soil serves all three.", B.CREAM, B.BROWN, logo=True),
    ],
    "x20261118": lambda: [
        fullbleed("misting_pile.jpg", "Ten weeks to make compost you can prove.", B.DEEP, B.CREAM, label="Compost Intensive Course", focus=(0.4, 0.4)),
        fullbleed("pile_turn.jpg", "Starting January 2027.", B.TAN, B.BROWN),
        fullbleed("testate_luke.jpg", "Build, monitor and read your own piles under the microscope.", B.BROWN, B.CREAM, cr=MIC["testate_luke.jpg"]),
        fullbleed("thermometer.jpg", "With mentors every week.", B.GREEN, B.CREAM, focus=(0.5, 0.3)),
        T("Enroll now, link in bio.", B.DEEP, B.CREAM, logo=True, size=110),
    ],
    "ev-02": lambda: [
        bignumber("100,000", "soil samples in one open atlas of soil life.", "bacteria_gerri.jpg", MIC["bacteria_gerri.jpg"]),
        bignumber("90+", "countries, every sample analysed with one protocol.", "hypha_lee.jpg", MIC["hypha_lee.jpg"], ground=B.TAN, ink=B.BROWN, size=300),
        T("Bacteria and fungi, open to everyone. Explore the Atlas at beopen.earth", B.DEEP, B.CREAM, logo=True),
    ],
    "ar20261123": lambda: [
        T("Our first annual report is almost here.", B.BROWN, B.CREAM, kicker="One year in", kicker_ink=B.TAN, size=104),
        T("A year of courses, workshops and scholarships.", B.CREAM, B.BROWN),
        T("Coming soon.", B.TAN, B.BROWN, size=150, logo=True),
    ],
    "x20261125": lambda: boxes_post("x20261125", [
        dict(label="Foundation Courses", heading="Start learning the soil food web this winter.", photo="extract_andrew.jpg", credit=SFW),
        dict(heading="At your own pace, from anywhere.", photo="prework_extract.jpg", credit=SFW, focus=(0.5, 0.6)),
        dict(heading="The science, the compost, the extracts and teas, the microscope.", photo="testate_luke.jpg", credit=MIC["testate_luke.jpg"]),
        dict(heading="10,000+ people in 100+ countries have started here.", photo="elaine_cr.jpg", credit="Dr. Elaine Ingham in Costa Rica"),
    ]),
    "x20261128": lambda: [
        fullbleed("pile_turn.jpg", "Small Business Saturday.", B.TAN, B.BROWN, label="Shop local"),
        fullbleed("prework_extract.jpg", "Shop local for your soil too.", B.DEEP, B.CREAM, focus=(0.5, 0.6)),
        fullbleed("extract_andrew.jpg", "Certified consultants run labs, compost operations and on-farm advice.", B.GREEN, B.CREAM),
        T("Find one near you, link in bio.", B.BROWN, B.CREAM, logo=True, size=110),
    ],
    "x20261129": lambda: [
        rings("A fruit tree grows better with friends.", GUILD, GUILD_COL),
        rings("Clover underneath fixes nitrogen.", GUILD, GUILD_COL, highlight=3),
        rings("Comfrey gets cut and dropped as mulch.", GUILD, GUILD_COL, highlight=2),
        rings("Chives and other alliums fill the gaps.", GUILD, GUILD_COL, highlight=1),
        rings("Together they keep the soil covered and alive.", GUILD, GUILD_COL),
    ],
    "x20261130": lambda: [
        bignumber("10 weeks", "of making compost and checking it under the microscope.", "thermometer.jpg", SFW, focus=(0.5, 0.3)),
        T("The Compost Intensive Course starts in January.", B.GREEN, B.CREAM),
        T("Enroll now, link in bio.", B.TAN, B.BROWN, logo=True, size=120),
    ],
    "x20261201": lambda: [
        T("Today is GivingTuesday.", B.GREEN, B.CREAM, size=100),
        T("A scholarship puts a farmer, gardener or student in a course they couldn't otherwise take.", B.CREAM, B.BROWN),
        T("They take it home to their own soil, and teach their neighbours.", B.TAN, B.BROWN),
        T("Give today, link in bio.", B.BROWN, B.CREAM, logo=True, size=120),
    ],
    "x20261202": lambda: [
        T("From shovel to slide.", B.BLUE, B.CREAM, size=130),
        S(1, "Take a small sample from the root zone.", "rain_soil.jpg", "No-till soil after rain", B.CREAM, B.BROWN, B.TAN),
        S(2, "Mix it with water.", "prework_extract.jpg", SFW, B.CREAM, B.BROWN, B.LIGHT, focus=(0.5, 0.65)),
        S(3, "Put one drop on a slide.", "extract_andrew.jpg", SFW, B.CREAM, B.BROWN, B.BLUE),
        S(4, "Count what you see: bacteria, fungi, protozoa, nematodes.", "nematode_sid.jpg", "Photo: Sid Jensen", B.CREAM, B.BROWN, B.TAN),
        T("That count tells you what your soil needs.", B.DEEP, B.CREAM, logo=True),
    ],
    "x20261203": lambda: [
        bignumber("6 weeks", "to Costa Rica. 18 to 29 January 2027.", "elaine_cr.jpg", "Dr. Elaine Ingham in Costa Rica", ground=B.LIGHT, ink=B.DEEP, focus=(0.45, 0.4)),
        fullbleed("pile_turn.jpg", "Compost piles in the morning.", B.TAN, B.BROWN),
        fullbleed("testate_luke.jpg", "The microscope in the afternoon.", B.DEEP, B.CREAM, cr=MIC["testate_luke.jpg"]),
        T("Places are still open. Link in bio.", B.BROWN, B.CREAM, logo=True),
    ],
    "x20261204": lambda: [
        T("Wildlife Conservation Day.", B.DEEP, B.CREAM, size=110),
        T("Meet the wildlife under your feet.", B.CREAM, B.BROWN, size=110),
        specimen("bacteria_gerri.jpg", "Bacteria.", "Feed on what roots release", ground=B.BROWN, cr=MIC["bacteria_gerri.jpg"]),
        specimen("hypha_lee.jpg", "Fungi.", "Thread through the soil", ground=B.DEEP, cr=MIC["hypha_lee.jpg"], focus=(0.6, 0.5)),
        specimen("ciliates.jpg", "Protozoa.", "Eat bacteria, release nutrients", ground=B.BLUE, accent=B.CREAM, focus=(0.5, 0.5), cr=MIC["ciliates.jpg"]),
        specimen("nematode_sid.jpg", "Nematodes.", "Hunt bacteria, fungi and each other", ground=B.GREEN, accent=B.CREAM, focus=(0.35, 0.75), cr=MIC["nematode_sid.jpg"]),
        specimen("collembola.jpg", "Microarthropods.", "Shred, graze and carry spores", ground=B.PURPLE, accent=B.CREAM, cr=MIC["collembola.jpg"]),
        T("Protect their habitat: keep soil covered and roots growing.", B.TAN, B.BROWN, logo=True),
    ],
    "w20261206": lambda: [
        T("Not sure where to start?", B.PURPLE, B.CREAM, size=120),
        T("What brings you to the soil food web?", B.CREAM, B.BROWN, size=110),
        T("Gardener, farmer or future consultant: there's a path for you.", B.GREEN, B.CREAM),
        T("Find yours, link in bio.", B.TAN, B.BROWN, logo=True, size=120),
    ],
    "x20261208": lambda: [
        chain("Who eats whom in your soil?", CHAIN, CHAIN_COL),
        chain("Plants feed bacteria and fungi through their roots.", CHAIN, CHAIN_COL, highlight=0),
        chain("Protozoa and nematodes eat the bacteria and fungi.", CHAIN, CHAIN_COL, highlight=1),
        chain("What they don't need comes out as nutrients plants can take up.", CHAIN, CHAIN_COL, highlight=2),
        chain("Lose a link, and the plant goes hungry.", CHAIN, CHAIN_COL, highlight=3),
    ],
    "w20261209": lambda: [
        fullbleed("hypha_lee.jpg", "How does the soil food web work?", B.BLUE, B.CREAM, cr=MIC["hypha_lee.jpg"], focus=(0.6, 0.5)),
        fullbleed("rain_soil.jpg", "Our new How it works page explains it in one scroll.", B.TAN, B.BROWN, cr="No-till soil after rain"),
        fullbleed("nematode_sid.jpg", "From root to microbe to nutrient and back.", B.DEEP, B.CREAM, cr=MIC["nematode_sid.jpg"], focus=(0.35, 0.75)),
        T("Read it, link in bio.", B.GREEN, B.CREAM, logo=True, size=120),
    ],
    "x20261210": lambda: [
        bignumber("131°F", "(55°C) for three full days kills weed seeds and pathogens.", "thermometer.jpg", SFW, focus=(0.5, 0.3), size=260),
        bignumber("155°F", "(68 to 71°C) is the ceiling. Hotter, and the good organisms die too.", None, ground=B.TAN, ink=B.BROWN, size=260),
        T("Turn the pile when it climbs too high, too fast.", B.DEEP, B.CREAM),
        T("Most piles need three to five turns.", B.CREAM, B.BROWN, logo=True),
    ],
    "w20261211": lambda: [li_card("Four decades of soil biology research, searchable.", ground=B.BROWN, kicker="Dr. Elaine Ingham's publications")],
    "x20261213": lambda: [
        specimen("testate_luke.jpg", "This amoeba lives in a house it built.", "Testate amoeba", ground=B.PURPLE, accent=B.CREAM, focus=(0.6, 0.55), cr=MIC["testate_luke.jpg"]),
        specimen("testate_luke.jpg", "It builds a shell from its own secretions or from mineral grains.", "The shell is called a test", ground=B.DEEP, focus=(0.62, 0.55)),
        specimen("bacteria_gerri.jpg", "It eats bacteria and releases nutrients plants can use.", "Bacteria, its food", ground=B.BROWN, cr=MIC["bacteria_gerri.jpg"]),
        T("Lots of them usually means a wetter, fungal-rich soil.", B.TAN, B.BROWN, logo=True),
    ],
    "x20261215": lambda: boxes_post("x20261215", [
        dict(label="Year-end giving", heading="What does one scholarship become?", photo="pile_turn.jpg", credit=SFW),
        dict(heading="One course.", photo="testate_luke.jpg", credit=MIC["testate_luke.jpg"]),
        dict(heading="One farm that changes how it builds soil.", photo="misting_pile.jpg", credit=SFW, focus=(0.4, 0.4)),
        dict(heading="A neighbour who sees the difference.", photo="rain_soil.jpg", credit="No-till soil after rain"),
        dict(heading="Give before the year ends, link in bio.", photo="extract_andrew.jpg", credit=SFW, layout=B.cover),
    ]),
    "x20261216": lambda: [
        rings("Permaculture zones.", ZONES, ZONE_COL),
        rings("Zone 0: the house.", ZONES, ZONE_COL, highlight=0),
        rings("Zone 1: herbs, salad, the compost bin.", ZONES, ZONE_COL, highlight=1),
        rings("Zones 2 to 4: orchard, field, pasture, woodlot.", ZONES, ZONE_COL, highlight=3),
        rings("Zone 5: left wild.", ZONES, ZONE_COL, highlight=5),
    ],
    "x20261217": lambda: [
        T("Nitrogen from thin air.", B.LIGHT, B.DEEP, size=130),
        bignumber("78%", "of the air is nitrogen gas. Plants can't use it.", None, ground=B.CREAM, ink=B.DEEP, size=360),
        T("Rhizobia bacteria in legume roots turn it into a form plants can.", B.BROWN, B.CREAM),
        bignumber("25 to 40%", "of the world's yearly reactive nitrogen comes from biological fixation.", None, ground=B.TAN, ink=B.BROWN, size=200),
        T("No bag required.", B.DEEP, B.CREAM, logo=True, size=140),
    ],
    "x20261220": lambda: [
        T("Congratulations to our Permaculture Design Certificate cohort.", B.BROWN, B.CREAM, kicker="Class of 2026", kicker_ink=B.TAN),
        T("Twelve weeks, one design each.", B.CREAM, B.BROWN, size=120),
        T("We can't wait to see what you build.", B.GREEN, B.CREAM, logo=True),
    ],
    "x20261222": lambda: boxes_post("x20261222", [
        dict(label="Holiday reading", heading="Dr. Elaine's papers, in one place.", photo="elaine_cr.jpg", credit="Dr. Elaine Ingham in Costa Rica", layout=B.split),
        dict(heading="Four decades of research, linked one by one.", photo="actino_ullens.jpg", credit=MIC["actino_ullens.jpg"], layout=B.top),
        dict(heading="Start with one. Pour a coffee.", photo="hypha_lee.jpg", credit=MIC["hypha_lee.jpg"], layout=B.cover),
    ]),
    "x20261224": lambda: [
        T("Your Christmas tree has one more job.", B.DEEP, B.CREAM, size=110),
        T("Chip it, or ask if your town does.", B.CREAM, B.DEEP),
        T("Woody mulch feeds fungi.", B.GREEN, B.CREAM, size=120),
        T("Spread it around trees and shrubs.", B.TAN, B.BROWN, logo=True),
    ],
    "x20261226": lambda: [
        T("Can wrapping paper go in the compost?", B.PURPLE, B.CREAM, size=110),
        yesno("Plain paper: yes. Glossy and glitter: no.", ["Plain paper", "Cardboard boxes", "Shredded or torn small"], ["Glossy or foil", "Glitter", "Plastic-coated", "Tape and ribbons"]),
        T("Scrunch it. If it stays scrunched, it's usually plain paper.", B.TAN, B.BROWN),
        T("Tape and ribbons off first.", B.CREAM, B.BROWN, logo=True, size=120),
    ],
    "x20261227": lambda: [
        fullbleed("pl20261114-5.jpg", "Chop and drop.", B.GREEN, B.CREAM, cr="Photo: Lance Cheung, USDA, public domain"),
        T("Cut the plant. Leave it where it falls.", B.CREAM, B.BROWN),
        fullbleed("pl20261114-1.jpg", "It shades the soil and feeds the fungi and bacteria underneath.", B.BROWN, B.CREAM, cr="Photo: Dan Keck, CC0 1.0"),
        T("No hauling, no bare ground.", B.TAN, B.BROWN, logo=True, size=120),
    ],
    "x20261229": lambda: [
        T("2026 in soil science.", B.DEEP, B.CREAM, size=140),
        specimen("hypha_lee.jpg", "A mustard plant that 'couldn't' partner with fungi traded food with one.", "University of Sheffield, Current Biology", ground=B.GREEN, accent=B.CREAM, cr=MIC["hypha_lee.jpg"]),
        specimen("bacteria_gerri.jpg", "An open map of the bacteria and fungi in 100,000 soil samples.", "BeOpen, by Biome Makers", ground=B.BLUE, accent=B.CREAM, cr=MIC["bacteria_gerri.jpg"]),
        specimen("rain_soil.jpg", "Regenerative almond orchards: water soaked in 6x faster, same yield.", "LaCanne et al., via Save Soil", ground=B.BROWN, cr="No-till soil after rain"),
        T("Here's to more in 2027.", B.TAN, B.BROWN, logo=True, size=120),
    ],
    "x20261231": lambda: [
        T("Happy New Year from the soil.", B.DEEP, B.CREAM, size=120),
        fullbleed("elaine_cr.jpg", "Costa Rica, 18 to 29 January.", B.GREEN, B.CREAM, cr="Dr. Elaine Ingham in Costa Rica", focus=(0.45, 0.4)),
        fullbleed("misting_pile.jpg", "New Mexico, 3 to 14 May.", B.TAN, B.BROWN, focus=(0.4, 0.4)),
        fullbleed("pile_turn.jpg", "United Kingdom, September.", B.BLUE, B.CREAM),
        T("Which one is yours?", B.BROWN, B.CREAM, logo=True, size=130),
    ],
}


if __name__ == "__main__":
    for pid in sys.argv[1:] or POSTS:
        for i, img in enumerate(POSTS[pid](), 1):
            path = os.path.join(OUT, f"{pid}-v1-{i}.jpg")
            img.save(path, quality=88, optimize=True)
        print(pid, i)
