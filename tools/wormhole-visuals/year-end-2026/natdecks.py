from natlib import *

GR = '#156826'; DG = '#22371F'; INK = '#333130'; SAGE = '#A7B097'; SPEC = '#E6EADC'; LIV = '#A2AE77'; OLIVE = '#5F6A3C'
W, H, M = 816, 1056, 72
CW = W - 2 * M
def swoosh(s, y, color, thick, name, amp=34, phase=0.0):
    import math
    pts_top = [(x, y + amp * math.sin((x / W) * math.pi * 1.15 + phase)) for x in range(-20, W + 21, 8)]
    pts_bot = [(x, yy + thick) for x, yy in reversed(pts_top)]
    pts = pts_top + pts_bot
    fb = s.shapes.build_freeform(E(pts[0][0]), E(pts[0][1]), scale=1.0)
    fb.add_line_segments([(E(x), E(yy)) for x, yy in pts[1:]], close=True)
    sh = fb.convert_to_shape(); sh.fill.solid(); sh.fill.fore_color.rgb = rgb(color); sh.line.fill.background(); sh.shadow.inherit = False; sh.name = name
    return sh
def eyebrow(t, c=GR, align='l'): return P(t, 'Montserrat', 10, c, True, 1.2, caps=True, track=2.2, align=align)
def heads(s, right, c=GR):
    text(s, M, 44, 340, [eyebrow('Soil Food Web Foundation', c)], 'Running head left')
    text(s, W - M - 300, 44, 300, [eyebrow(right, c, 'r')], 'Running head right')
def heading(s, y, t, c=GR, size=32, w=CW, rulec=SAGE):
    h = text(s, M, y, w, [P(t, 'EB Garamond', size, c, lh=1.15)], 'Heading: ' + t[:30])
    hline(s, M, y + h + 10, w, rulec, 'Rule')
    return y + h + 11
def body(t, size=15.5, c=INK, before=0, lh=1.5): return P(t, 'Source Sans 3', size, c, lh=lh, before=before)

# ---------------------------------------------------------------- DONOR OVERVIEW
def donor():
    d = Deck()
    # P1 cover
    s = d.page()
    pic(s, 'ph/poppies-hi.jpg', 0, 0, W, 490, 'Photo: group in poppy field', fy=0.72)
    y = 540
    y += text(s, M, y, CW, [eyebrow('Soil Food Web Foundation: Donor Overview')], 'Eyebrow') + 14
    y += text(s, M, y, CW, [P('Healthy soil. Healthy food.\nA living legacy.', 'EB Garamond', 44, GR, lh=1.12)], 'Title') + 22
    hline(s, M, y, CW, SAGE); y += 24
    text(s, M, y, 600, [P("The Soil Food Web Foundation carries forward the life's work of Dr. Elaine Ingham, the scientist who showed the world that soil is alive. This October we celebrate our first year as a nonprofit. Our mission is to honor and grow Elaine's legacy of empowering communities to restore and protect the Earth's soil and living systems. We would not be here without the donors who have supported us and shown up. Your gift goes a long way here: $5,000 delivers comprehensive training from theory to full implementation, and together we are working to change the global food system.", 'Source Sans 3', 16.5, INK, lh=1.55)], 'Intro')
    png(s, 'logo.png', W - M - 64, H - 56 - 64, 64, 'SFW logo')

    # P2 why + what we do + photo
    s = d.page(); heads(s, 'Donor Overview')
    y = heading(s, 92, 'Why living soil matters now') + 22
    y += text(s, M, y, CW, [body("When soil loses its biology, farmers must replace it with costly synthetic fertilizers and pesticides that wash into our rivers. When soil life is restored, farms use fewer chemicals, hold more water, store more carbon and grow more nutritious food. The missing piece is knowledge, and we share it openly. Nothing we teach is proprietary. One farmer in Illinois, Adam York, reported saving about $1 million a year after implementing the Soil Food Web Approach on 10,000 acres of corn and soy, after working with Soil Food Web Consultant, Todd Harrington. Now he runs a company called Agribio Systems, servicing hundreds of thousands of acres of farmland in his region and helping other farmers transform their operations.")], 'Why living soil text') + 44
    y = heading(s, y, 'What we do') + 24
    items = [('Teach.', 'Build soil biology literacy, from free public education to professional soil consulting, for students in 140 countries.'),
             ('Research.', "Build on Elaine's experiments to advance the science, and share our data openly so practice rests on evidence."),
             ('Practice.', 'Partner with farmers and organizations to demonstrate soil food web methods in different regions and climates.'),
             ('Connect.', 'Grow a worldwide community of practitioners and leaders who share what works and support each other.')]
    colw = (CW - 40) / 2
    for row in (items[:2], items[2:]):
        hh = 0
        for k, (l, t) in enumerate(row):
            hh = max(hh, text(s, M + k * (colw + 40), y, colw, [P(l, 'EB Garamond', 20, DG, True, 1.2), body(t, 15, before=6, lh=1.45)], l[:-1]))
        y += hh + 30
    ph = max(240, H - (y + 20))
    pic(s, 'ph/group-field-duo.jpg', 0, H - ph, W, ph, 'Photo: workshop group in a field', fy=0.42)

    # P3 first year + gifts + photo
    s = d.page(); heads(s, 'Donor Overview')
    y = heading(s, 92, 'Our first year') + 1
    fy = ["Became a nonprofit and received all of the school's intellectual property, now held for the public good",
          "Redesigned our core courses and launched a Permaculture Design Certificate with the Permaculture Association UK (100 students from 23 countries)",
          "Awarded over $300,000 in scholarships in 2026, and grew our student community to nearly 10,000 individuals from 140 countries. Our organizational scholarships reach partners such as iCow in East Africa and TrashIt in Pakistan. Both of TrashIt's founders completed our foundation courses on scholarships, and TrashIt now offers microbial soil testing and reached 600+ people across 10+ districts in one Soil Health Week."]
    y += table(s, M, y, [CW], [[body(t, 15, lh=1.45)] for t in fy], 'Table: Our first year', SAGE, 12, 0) + 48
    y = heading(s, y, 'What your gift makes possible') + 1
    gm = [('Scholarships', 'open our courses to students who could not otherwise attend.'), ('Sponsored workshop seats', 'bring hands-on training to farming communities that need it most.'), ('New programs', 'such as our compost cohort, with liquid amendments and microscopy programs in development.'), ('Unrestricted gifts', 'go where the need is greatest and help us grow.')]
    y += table(s, M, y, [236, CW - 236], [[P(a, 'Source Sans 3', 15, DG, True, 1.4), body(t, 15, lh=1.45)] for a, t in gm], 'Table: What your gift makes possible', SAGE, 12, 24) + 48
    ph = H - y
    if ph >= 180: pic(s, 'ph/microscope-duo.jpg', 0, y, W, ph, 'Photo: student at the microscope', fy=0.24)
    print('donor p3 end', round(y), 'photo', round(ph))

    # P4 deep green closing page: full-bleed photo, light green swoosh, text anchored to the bottom
    s = d.page(DG)
    PH = 500
    pic(s, 'ph/walk.jpg', 0, 0, W, PH, 'Photo: students walking through a farm in India', fy=0.55)
    swoosh(s, PH + 22, '#59A66C', 7, 'Swoosh')
    swoosh(s, PH + 40, OLIVE, 3, 'Swoosh thin', amp=26, phase=0.6)
    goal = [P('Goal: raise $300,000 by December 31', 'EB Garamond', 36, '#FFFFFF', lh=1.12)]
    quote = [P('"Let me teach you so that you can do this for yourself."', 'EB Garamond', 25, '#FFFFFF', lh=1.3, before=22), dict(eyebrow('— Dr. Elaine Ingham', LIV), before=12)]
    celeb = [body("Celebrate our first year and help carry Dr. Elaine's work forward. Giving pathways: one-time gifts, monthly giving, workshop and scholarship sponsorships, and legacy gifts.", 15.5, SPEC, lh=1.5, before=24)]
    g3 = [body('Give online: soilfoodweb.com/donations · Giving Tuesday: December 1 · Contact: Evan Buckman, Executive Director, evan@soilfoodweb.com, (512) 359-5206 · www.soilfoodweb.com', 13.5, SPEC, lh=1.45),
          body('Soil Food Web Foundation is a 501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.', 10.5, LIV, before=8, lh=1.35)]
    tw = 430
    h3 = max(88, measure(g3, tw))
    qy = H - 60 - h3
    paras = goal + quote + celeb
    btop = PH + 96; bh = qy - 34 - btop
    print('p4 text room', round(bh), 'worst', round(measure(paras, CW)), 'brand', round(measure(paras, CW, 0)))
    text(s, M, btop, CW, paras, 'Goal, quote and giving pathways', h=bh, anchor='m')
    hline(s, M, qy - 22, CW, OLIVE)
    png(s, 'qr.png', M, qy, 88, 'QR code', 88)
    text(s, M + 112, qy - 2, tw, g3, 'Give online and contact')
    png(s, 'logo-white.png', W - M - 68, qy + 4, 68, 'SFW logo white')
    d.save('out/SFW Donor Overview.pptx')

# ---------------------------------------------------------------- CASE FOR SUPPORT
def case():
    d = Deck()
    s = d.page()
    pic(s, 'ph/palms.jpg', 0, 0, W, 490, 'Photo: students in a palm farm', fy=0.6)
    y = 540
    y += text(s, M, y, CW, [eyebrow('Soil Food Web Foundation: Case for Support')], 'Eyebrow') + 14
    y += text(s, M, y, CW, [P('Restoring living soil.\nGrowing a global community.', 'EB Garamond', 44, GR, lh=1.12)], 'Title') + 22
    hline(s, M, y, CW, SAGE); y += 24
    text(s, M, y, 600, [P("The Soil Food Web Foundation carries forward the life's work of Dr. Elaine Ingham, who showed the world that soil is alive, and provided a practical, scientific roadmap for restoring it. This October marks our first year as a nonprofit, created so that her essential teachings and the community of practice that has grown around them can live on for many generations to come.", 'Source Sans 3', 16.5, INK, lh=1.55)], 'Intro')
    png(s, 'logo.png', W - M - 64, H - 56 - 64, 64, 'SFW logo')

    s = d.page(); heads(s, 'Case for Support')
    y = 96
    y += text(s, M, y, CW, [P('"The paradigm shift she shows us, that soil is alive and that soil microbiology matters, has profound meaning not just for agriculture, but for human life itself on the planet."', 'EB Garamond', 24, DG, lh=1.32)], 'Leslie quote') + 16
    y += text(s, M, y, CW, [eyebrow('Leslie Lewis, Board Chair and graduate of our consultant training program')], 'Quote attribution') + 48
    y = heading(s, y, 'Why it matters now') + 22
    colw = (CW - 40) / 2
    hl = text(s, M, y, colw, [body("The green revolution brought immense change to the global food system. We saw huge increases in the total pounds of food produced around the world, which came at the cost of topsoil loss, fertility decline, lower nutrient density in our food, toxic chemicals in our bodies, food and water, extreme loss of biodiversity, and the erosion of farmer profitability.", 15),
                                   body("The world is waking up to this reality; soil health and regenerative agriculture initiatives abound from governments to corporations to grassroots initiatives.", 15, before=12)], 'Why it matters, left')
    hr = text(s, M + colw + 40, y, colw, [body("The problem is, almost all of these initiatives are ignorant to the reality of life in the soil which is absolutely fundamental. The Soil Food Web Foundation fulfills a unique role by teaching farmers, agricultural professionals, gardeners and land stewards to understand, measure, and restore the life in their soil. We empower them to transform locally available organic residues into potent biological inoculants that have proven successful for decades in improving soil health, food quality, and farmers profitability.", 15)], 'Why it matters, right')
    y += max(hl, hr) + 36
    ph = max(220, H - y)
    pic(s, 'ph/students-duo.jpg', 0, H - ph, W, ph, 'Photo: students in class', fy=0.45)
    print('case p2: text end', round(y), 'photo h', round(ph))

    s = d.page()
    pic(s, 'ph/talk-back-duo.jpg', 0, 0, W, 316, 'Photo: teaching a full room in India', fy=0.4)
    y = 356
    hl = text(s, M, y, colw, [body("Elaine’s teachings have influenced millions of people around the world, and our school has welcomed nearly 10,000 students from 140 countries into our educational programs. Our students themselves have gone on to touch and transform the lives of millions of farmers and transform millions of acres of land - from Illinois, to Kenya, to India. Our students are working every day to put these teachings into practice and are leaders in the regenerative movement.", 14.5)], 'Reach')
    hr = text(s, M + colw + 40, y, colw, [body("The demand for this knowledge is far greater than we currently have the resources to provide. Farmers around the world, for whom the knowledge of how to grow sufficient food without relying on synthetic, imported fertilizers and toxic chemicals, could mean the difference between nourishment and hunger, are eager to attain these skills. Our scholarship programs are expanding, we are hosting live workshops in new locations, working directly with farmers to implement and demonstrate this work, and actively growing our global community.", 14.5)], 'Demand')
    y += max(hl, hr) + 44
    rows = [('Few farmers and agronomists are taught how soil biology works', 'Free public education and webinars, intensive theoretical online courses, and in person practical intensives'),
            ('Inputs and training many cannot afford', 'Over $300,000 in scholarships in 2026, and compost made from free local materials'),
            ('Methods that do not fit local soils', 'Hands-on workshops, mentors and step-by-step guides, region by region')]
    hd = [P('Barriers to change', 'EB Garamond', 26, GR, lh=1.15), P('Our response', 'EB Garamond', 26, GR, lh=1.15)]
    y += table(s, M, y, [colw + 40, colw], [hd] + [[P(a, 'Source Sans 3', 15, DG, True, 1.42), body(b, 15, lh=1.42)] for a, b in rows], 'Table: Barriers and response', SAGE, 12, 40)
    lg = 56
    if y + 30 + lg < H - 40: png(s, 'logo.png', W - M - lg, H - 48 - lg, lg, 'SFW logo')
    print('case p3: table end', round(y))

    s = d.page(DG); heads(s, 'Case for Support', LIV)
    y = 100
    y += text(s, M, y, CW, [P('What your gift makes possible', 'EB Garamond', 36, '#FFFFFF', lh=1.15)], 'Heading') + 26
    gifts = [('$5,000', 'funds a full scholarship for someone to become a SFW Consultant: our Foundation Courses and The Complete Practicum'), ('$10,000', 'sponsors an all inclusive scholarship at a two-week hands-on workshop'), ('$25,000', 'sponsors a group of courses for a community in need'), ('$100,000', 'sponsors a whole workshop in a new region, such as Kenya or Brazil')]
    hd = [P('Gift', 'EB Garamond', 20, LIV, True, 1.3), P('Impact', 'EB Garamond', 20, LIV, True, 1.3)]
    y += table(s, M, y, [170, CW - 170], [hd] + [[P(a, 'EB Garamond', 26, '#FFFFFF', lh=1.15), body(t, 15.5, SPEC, lh=1.45)] for a, t in gifts], 'Table: Gifts', OLIVE, 16, 24)
    # bottom block measured upward
    b1 = [P('GOAL: RAISE $300,000 BY DECEMBER 31, 2026.', 'Montserrat', 13, '#FFFFFF', True, 1.3, caps=True, track=1.5)]
    b2 = [body("Give today at soilfoodweb.com/donations or scan the QR code. One-time gifts, monthly giving, sponsorships, and legacy gifts. For customized giving, contact Evan Buckman, Executive Director, at evan@soilfoodweb.com or (512) 359-5206. 501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.", 13.5, SPEC, lh=1.42)]
    tw = 440; hb1 = measure(b1, CW); hb2 = max(88, measure(b2, tw))
    btop = H - 56 - hb2 - 18 - hb1
    q = [P('"We see a more beautiful world, and we dedicate our lives to restoring the invisible layers of life that make that world possible."', 'EB Garamond', 24, '#FFFFFF', lh=1.34), eyebrow('Evan Buckman, Executive Director', LIV)]
    q[1]['before'] = 18
    hq = measure(q, CW)
    space = btop - 34 - y
    qy = y + (space - hq) / 2
    text(s, M, qy, CW, q, 'Evan quote')
    hline(s, M, btop - 34, CW, OLIVE)
    text(s, M, btop, CW, b1, 'Goal')
    png(s, 'qr.png', M, btop + hb1 + 18, 88, 'QR code', 88)
    text(s, M + 112, btop + hb1 + 16, tw, b2, 'Give today')
    png(s, 'logo-white.png', W - M - 60, btop + hb1 + 18, 60, 'SFW logo white')
    print('case p4: table end', round(y), 'quote', round(qy), round(qy + hq), 'bottom block', round(btop))
    d.save('out/SFW Case for Support.pptx')

if __name__ == "__main__": donor(); case()

# ---------------------------------------------------------------- FUNDING THE VISION AHEAD
def funding():
    d = Deck()
    s = d.page()
    pic(s, 'ph/microscope.jpg', 0, 0, W, 490, 'Photo: student at the microscope', fy=0.22)
    y = 540
    y += text(s, M, y, CW, [eyebrow('Soil Food Web Foundation: Funding the Vision Ahead')], 'Eyebrow') + 14
    y += text(s, M, y, CW, [P('2027 and Beyond:\nFunding the Vision Ahead', 'EB Garamond', 44, GR, lh=1.12)], 'Title') + 22
    hline(s, M, y, CW, SAGE); y += 24
    text(s, M, y, 600, [P("We would not be here without the donors who have supported us and shown up. Gifts go a long way here: $5,000 delivers $10,000 of training. Every student we train builds soil biology literacy and joins a worldwide network of practitioners and leaders working to change the global food system.", 'Source Sans 3', 16.5, INK, lh=1.55)], 'Intro')
    png(s, 'logo.png', W - M - 64, H - 56 - 64, 64, 'SFW logo')

    # P2 top priorities
    s = d.page(); heads(s, 'Funding the Vision Ahead')
    y = heading(s, 92, 'Top priorities') + 1
    pr = [('Scholarship Fund.', "Opens our courses to students anywhere in the world, regardless of means. Hundreds of people who make a strong impact in their communities are waiting for support. Organizational scholarships reach even further: both founders of TrashIt in Pakistan trained with us, and TrashIt now offers microbial soil testing to farmers. $5,000 funds a full scholarship for our Foundation Courses and The Complete Practicum, a $10,000 value. We awarded over $300,000 in scholarships in 2026.", '$100,000'),
          ('New and Updated Programs.', 'Draw on decades of experience teaching the Soil Food Web Approach, using modern pedagogy to improve our learning experience and launch new programs.', '$100,000'),
          ('Hands-On Workshops.', 'Bring two-week hands-on workshops to new places. $10,000 sponsors a group of seats in a new location, and $100,000 sponsors a whole workshop in a new region such as Kenya or Brazil.', '$10,000 to $100,000'),
          ('Open Research.', "Build on Elaine's experiments to advance the science of the Soil Food Web itself. We publish our trial and case study data openly so anyone can see why the methods work. $100,000 starts this work, and major studies range from $500,000 to $3 million.", '$100,000+'),
          ('Elaine Ingham Legacy Fund.', "Fund field research in Elaine's name, across a global network of demonstration farms where farmers can see the results on working farms.", 'Transformational gift')]
    hdr = [P('#', 'Montserrat', 10, GR, True, 1.4, caps=True, track=2), P('Priority', 'Montserrat', 10, GR, True, 1.4, caps=True, track=2), P('Investment', 'Montserrat', 10, GR, True, 1.4, caps=True, track=2)]
    rows = [hdr] + [[P(str(i + 1), 'EB Garamond', 26, GR, lh=1.0), [P(a, 'Source Sans 3', 15, DG, True, 1.45), body(t, 15, lh=1.45)], P(v, 'EB Garamond', 18, DG, lh=1.25)] for i, (a, t, v) in enumerate(pr)]
    y += table(s, M, y, [48, CW - 48 - 176, 176], rows, 'Table: Top priorities', SAGE, 13, 24) + 36
    ph = H - y
    if H - y > 140: png(s, 'logo.png', W - M - 64, H - 56 - 64, 64, 'SFW logo')
    print('funding p2 end', round(y), 'photo', round(ph))

    # P3 more ways to invest, deep green
    s = d.page(DG); heads(s, 'Funding the Vision Ahead', LIV)
    y = 100
    y += text(s, M, y, CW, [P('More ways to invest', 'EB Garamond', 36, '#FFFFFF', lh=1.15)], 'Heading') + 26
    mw = [('Living Soil Circle', 'Monthly donors whose steady support funds scholarships all year. Join on our GiveButter page.', '$100+ per month'),
          ('Founders Circle', 'Leaders who give $10,000 or more a year during our founding years and share the mission with friends.', '$10,000+ per year'),
          ('Named Scholarship', 'Fund a full scholarship in honor of a loved one, family or farm.', '$5,000'),
          ('Sponsor a Workshop or Event', 'Underwrite a compost workshop or gathering for students, farmers and supporters.', '$5,000 to $20,000'),
          ('Unrestricted Annual Fund', 'Goes where the need is greatest: scholarships, teaching and research.', 'Any amount')]
    hdr = [P(t, 'Montserrat', 10, LIV, True, 1.4, caps=True, track=2) for t in ('Way to give', 'What it does', 'Investment')]
    rows = [hdr] + [[P(a, 'EB Garamond', 20, '#FFFFFF', lh=1.2), body(b, 15, SPEC, lh=1.45), P(c, 'EB Garamond', 18, '#FFFFFF', lh=1.25)] for a, b, c in mw]
    y += table(s, M, y, [190, CW - 190 - 150, 150], rows, 'Table: More ways to invest', OLIVE, 16, 24)
    g = [body('Give today at soilfoodweb.com/donations · For customized giving, contact Evan Buckman, Executive Director, evan@soilfoodweb.com, (512) 359-5206 · www.soilfoodweb.com', 15, SPEC, lh=1.5)]
    tw = 420; hg = max(96, measure(g, tw))
    by = H - 76 - hg
    png(s, 'mycelium.png', W - 300, by - 330, 340, 'Fungal network drawing') if by - 330 > y + 30 else None
    hline(s, M, by - 34, CW, OLIVE)
    png(s, 'qr.png', M, by, 96, 'QR code', 96)
    text(s, M + 124, by - 2, tw, g, 'Give today')
    png(s, 'logo-white.png', W - M - 72, by + 6, 72, 'SFW logo white')
    print('funding p3 table end', round(y), 'bottom block', round(by))
    d.save('out/SFW Funding the Vision Ahead.pptx')

if __name__ == "__main__": funding()
