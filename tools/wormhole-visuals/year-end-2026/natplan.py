from natlib import *
from natdecks import GR, DG, INK, SAGE, SPEC, LIV, OLIVE, W, H, M, CW, eyebrow, body
import natdecks

d = Deck()
BOT = H - 64
state = {'s': None, 'y': 0, 'n': 0}
def heads(s):
    text(s, M, 44, 340, [eyebrow('Soil Food Web Foundation')], 'Running head left')
    text(s, W - M - 340, 44, 340, [eyebrow('Year-End Campaign Plan 2026', GR, 'r')], 'Running head right')
def newpage():
    s = d.page(); heads(s); state.update(s=s, y=92)
def need(h):
    if state['y'] + h > BOT: newpage()
PEND = []
def H2(t, gap_before=40):
    PEND.append((t, gap_before))
def _flush(first_h):
    """place a pending heading so it stays with the first piece of the next block"""
    if not PEND: return
    t, gb = PEND.pop()
    hp = [P(t, 'EB Garamond', 30, GR, lh=1.15)]
    hh = measure(hp, CW) + 11
    if state['y'] > 100: state['y'] += gb
    if state['y'] + hh + 20 + first_h > BOT: newpage()
    s = state['s']; y = state['y']
    h = text(s, M, y, CW, hp, 'Heading: ' + t[:30])
    hline(s, M, y + h + 10, CW, SAGE, 'Rule')
    state['y'] = y + h + 11
def para(paras, gap=20, w=CW, x=M):
    h = measure(paras, w); _flush(h); state['y'] += gap; need(h)
    text(state['s'], x, state['y'], w, paras, (paras[0].get('t') or paras[0]['runs'][0]['t'])[:30]); state['y'] += h
def lead(a, b, size=15.5):
    return dict(runs=[P(a, 'Source Sans 3', size, DG, True, 1.5), P(b, 'Source Sans 3', size, INK, False, 1.5)], before=12)
def tbl(colw, rows, name, gap=0):
    scratch = Deck().page()
    rh = [table(scratch, 0, 0, colw, [r], name, SAGE, 11, 20) for r in rows]
    head, body_rows, hrh = rows[0], rows[1:], rh[0]
    if head[0].get('caps') is None or not head[0].get('caps'):  # no header row
        head, body_rows, hrh = None, rows, 0
        rh = [0] + rh
    _flush(hrh + rh[1])
    state['y'] += gap
    i = 0; part = 1
    while i < len(body_rows):
        if state['y'] + hrh + rh[1 + i] > BOT: newpage()
        chunk = []; hsum = hrh
        while i < len(body_rows) and state['y'] + hsum + rh[1 + i] <= BOT:
            chunk.append(body_rows[i]); hsum += rh[1 + i]; i += 1
        rr = ([head] if head else []) + chunk
        table(state['s'], M, state['y'], colw, rr, name + (f' ({part})' if part > 1 else ''), SAGE, 11, 20)
        state['y'] += hsum; part += 1
def hdr(*t): return [P(x, 'Montserrat', 10, GR, True, 1.4, caps=True, track=2) for x in t]
def c(t, bold=False): return P(t, 'Source Sans 3', 14, DG if bold else INK, bold, 1.42)

# ---- page 1: deep green title band
s = d.page(); state.update(s=s)
rect(s, 0, 0, W, 300, DG, 'Title band')
text(s, M, 44, 340, [eyebrow('Soil Food Web Foundation', LIV)], 'Running head left')
png(s, 'mycelium.png', W - 300, -30, 330, 'Fungal network drawing')
th = text(s, M, 150, 520, [P('Year-End Campaign Plan 2026', 'EB Garamond', 46, '#FFFFFF', lh=1.1)], 'Title')
state['y'] = 300 + 8
H2('The goal')
para([P('Raise $300,000 by December 31.', 'EB Garamond', 28, DG, lh=1.2), P('*The Donate page still shows $100,000 and needs updating.', 'Source Sans 3', 13, '#4A463F', lh=1.4, before=8)], gap=18)
para([dict(runs=[P('Theme (working): ', 'Source Sans 3', 15.5, DG, True, 1.5), P('“Carry the work forward.” This is the first giving season without Dr. Elaine Ingham. Every gift keeps her teaching growing, in her name and through the next generation of students.', 'Source Sans 3', 15.5, INK, False, 1.5)], before=0)], gap=18)
H2('Three messages')
para([dict(lead('Thank you, first. ', 'To everyone who has already given: we would not be here without you. The Foundation exists because of your gifts. Every piece to past donors opens with thanks before any ask.'), before=0),
      lead('Where your gift goes, directly. ', 'Each email, the mailer and the Donate page name exactly what a gift pays for, in dollars.'),
      lead('The stretch of your dollar. ', 'Show how far each dollar travels: $5,000 delivers $10,000 of training, and on Giving Tuesday the match doubles it.')], gap=18)
gifts = [('$100/month (Living Soil Circle)', '$1,200 a year toward scholarships', 'Four years funds nearly a full scholar'),
         ('$5,000', 'One full scholarship', 'Delivers $10,000 of training (Foundation Courses plus The Complete Practicum)'),
         ('$10,000 (Founders Circle)', 'An all-inclusive scholarship at a two-week hands-on workshop', 'Each graduate teaches and advises the farmers around them'),
         ('$25,000', 'A group of courses for a community in need', 'Trains a whole community'),
         ('Any gift on Giving Tuesday', 'The same as above', 'Doubled by the match')]
tbl([200, 236, CW - 436], [hdr('Your gift', 'Where it goes directly', 'How far it stretches')] + [[c(a, True), c(b), c(e)] for a, b, e in gifts], 'Table: Gifts', gap=28)
para([P('Nearly 10,000 students in 140 countries have trained with us so far.', 'EB Garamond', 20, GR, lh=1.3)], gap=20)

H2('Recommendation: Giving Tuesday for gifts, Cyber Monday for courses')
para([dict(lead('Giving Tuesday, Dec 1: ', 'Giving Tuesday (Dec 1) is the one donation push. It is the day people expect to be asked to give, GiveButter is built for it, and a match makes it urgent. It also opens Soil Health Week (Dec 1 to 7, with our partner TrashIt) and leads into World Soil Day (Dec 5), where last year’s first appeal began.'), before=0),
      lead('Cyber Monday, Nov 30: ', 'Cyber Monday (Nov 30) is the course offer, sent to students and subscribers, with one line added: “Or sponsor a scholar for someone who can’t afford it.” Course sales are revenue and are tracked apart from the $300,000 goal.')], gap=18)
H2('How we reach $300,000 (estimates)')
src = [('Personal asks to major and recurring donors', 'Evan, with board support', '$150,000'),
       ('Giving Tuesday match (a donor or the board puts up the match)', 'Evan to secure by Nov 13', '$50,000'),
       ('Giving Tuesday gifts that the match doubles', 'Online, all audiences', '$50,000'),
       ('Printed mailer and December emails', 'Donors, alumni, students', '$35,000'),
       ('New Living Soil Circle monthly donors (from $100/month)', 'Students and alumni', '$15,000')]
tbl([330, 220, CW - 550], [hdr('Source', 'Who', 'Target')] + [[c(a), c(b), P(t, 'EB Garamond', 17, DG, lh=1.3)] for a, b, t in src] + [[c('Total', True), c(''), P('$300,000', 'EB Garamond', 19, GR, True, 1.3)]], 'Table: How we reach $300,000', gap=6)

H2('Audiences')
aud = [('Major and recurring donors, Founders Circle prospects ($10K+/yr)', 'Personal ask, then the match invitation', 'Evan (calls, meetings)'),
       ('Current donors (fewer than 100)', 'We would not be here without you. What your gift did in Year 1, then renew or go monthly', 'Evan'),
       ('Advanced students and alumni', 'Fund the next scholar ($5,000 funds one); join the Living Soil Circle', 'A board member or alum'),
       ('Past course takers', 'Your education was the start; help it reach the next farmer', 'Evan'),
       ('Newcomers and subscribers', 'Why living soil matters; join the movement', 'Board chair'),
       ('Dr. Elaine’s wider community', 'Give in her memory (tribute gift)', '')]
tbl([236, CW - 236 - 150, 150], [hdr('Audience', 'What they hear', 'Lead voice')] + [[c(a, True), c(b), c(e)] for a, b, e in aud], 'Table: Audiences', gap=6)
H2('Channels')
para([dict(lead('Email series. ', 'About eight sends from Nov 24 to Dec 31 (calendar below). Split by audience on the key days, as last year’s three-group emails did. Anyone who gives drops off the remaining asks and gets a thank-you instead.'), before=0),
      lead('Printed mailer. ', 'A one-page letter from Evan, a reply card with giving levels ($100/month, $5,000 funds a scholar, $10,000 Founders Circle, other), a tribute line, the donate QR code and a return envelope. Send it to every donor and major prospect with a mailing address plus US alumni, timed to land around Giving Tuesday. Most students are overseas, so email remains the main channel.'),
      lead('Social. ', 'Scholar stories, a Giving Tuesday countdown, live progress on the day, and short LinkedIn posts board members can share. Posted from Foundation accounts.'),
      lead('Website. ', 'Update the Donate page goal to $300,000 and add a progress bar toward it, a working give form, a “Give monthly” button, a tribute option, a Giving Tuesday landing page, and a site-wide banner from Dec 1 to Dec 31. Add a one-year anniversary post to Foundation News.')], gap=18)

H2('Timeline')
tl = [('Nov 2 to 13', 'Board approves plan and theme. Fix the Donate page. Pull mailing list', 'Jessica, Evan, web team'),
      ('Nov 2 to 13', 'Evan starts major donor asks and secures the match. Write the mailer, emails and social posts. Collect 3 to 4 scholar stories.', 'Evan, Stephanie'),
      ('Nov 16 to 20', 'Mailer to print and in the mail. Anniversary post on the website. Giving Tuesday landing page built.', 'Stephanie'),
      ('Tue, Nov 21-24', 'Email 1: Thanksgiving thank-you (“we would not be here without you”); announce the Giving Tuesday match.', 'Evan'),
      ('Mon, Nov 30', 'Email 2: Cyber Monday course offer, plus “or sponsor a scholar.” Course audience only.', 'Soil Food Web Team'),
      ('Tue, Dec 1', 'Giving Tuesday. Email 3 (morning launch, by audience) and Email 4 (afternoon progress, last hours of the match). Social all day. Banner and progress bar go live.', 'Evan, board'),
      ('Sat, Dec 5', 'Email 5: World Soil Day. Dr. Elaine’s legacy and tribute gifts.', 'Evan, board'),
      ('Dec 8 to 18', 'Email 6: fund the next scholar, monthly giving. Evan follows up with every open major donor ask. Mailer lands and gets one reminder.', 'Evan'),
      ('Tue, Dec 29', 'Email 7: year-end tax reminder and how much is left to raise.', 'Evan'),
      ('Thu, Dec 31', 'Email 8: last call, final hours.', 'Evan'),
      ('Throughout', 'Thank every gift within 48 hours. Evan calls gifts of $1,000+.', 'Evan, Stephanie'),
      ('Mid-January', 'Thank-you and impact update to all year-end donors: the total raised and what it funds.', 'Evan, Jessica')]
tbl([130, CW - 130 - 170, 170], [hdr('When', 'What', 'Owner')] + [[c(a, True), c(b), c(e)] for a, b, e in tl], 'Table: Timeline', gap=6)

H2('Decisions needed from the board')
dec = ['Approve the theme and the Giving Tuesday and Cyber Monday split.', 'Who puts up the Giving Tuesday match, and how much.', 'Mailer budget and list size, and who signs each email (Evan, Leslie, Jenna).', 'Tribute gifts in Dr. Elaine’s memory?', 'Cyber Monday offer details (gift a course, discount code, or both).',
       'Understanding what we need to say to avoid donor-imposed restrictions for general funds (Obviously might be a different story for larger gifts) We don’t want to accidentally rasie funds that we can’t use without a lot of red tape we are equipped to monitor and manage',
       'We need legal guidance on disclaimers to place on pages, ads, mailers, etc since ourdonation messages will reach not only across state lines but also internationally. Who can provide us legal council here?']
tbl([48, CW - 48], [[P(str(i + 1), 'EB Garamond', 22, GR, lh=1.0), c(t)] for i, t in enumerate(dec)], 'Table: Decisions', gap=4)
d.save('out/SFW Year-End Campaign Plan 2026.pptx')
print('pages', len(d.prs.slides._sldIdLst), 'last y', round(state['y']))
