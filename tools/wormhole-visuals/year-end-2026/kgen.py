import os, pathlib
os.makedirs('/home/claude/kit/pages', exist_ok=True)
G='#156826'; D='#22371F'; L='#59A66C'; BR='#4F3433'; CR='#F4F1EA'; BL='#3780B8'
H="font-family:'Montserrat',sans-serif;font-weight:700"
S="font-family:'Source Sans 3',sans-serif;font-weight:400"
LOGO='../logo-white.png'; LOGOC='../logo.png'; QR='../qr.png'
def ph(n): return f'../ph/{n}'
def page(pid, W, H_, body, bg='#ffffff'):
    html=f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0}}
body > div{{position:relative;width:{W}px;height:{H_}px;overflow:hidden;background:{bg};{S};color:#333130}}
img{{display:block}}
</style></head><body><div class="pg">{body}</div></body></html>'''
    open(f'/home/claude/kit/pages/{pid}.html','w').write(html)

def img(src, x, y, w, h, pos='50% 50%', alt='Photo', r=0):
    rad=f'border-radius:{r}px;' if r else ''
    return f'<img src="{src}" alt="{alt}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;object-position:{pos};{rad}">'
def box(x, y, w, h, c, r=0):
    rad=f'border-radius:{r}px;' if r else ''
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};{rad}"></div>'
def txt(x, y, w, t, size, color='#fff', font=None, lh=1.08, align='left', extra=''):
    font=font or H
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;{font};font-size:{size}px;line-height:{lh};color:{color};text-align:{align};{extra}">{t}</div>'
def logo(x, y, w, src=LOGO):
    return f'<img src="{src}" alt="Soil Food Web Foundation logo" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:auto">'

# ---------------- SOCIAL 1080x1350 ----------------
W,Hh=1080,1350
soc=[]
def S1():  # photo top 63%, green box bottom
    b=img(ph('shed.jpg'),0,0,1080,850,'50% 40%','Workshop students in India gathered around fresh compost material')
    b+=box(0,850,1080,500,G)
    b+=txt(72,912,760,'5 days to Giving Tuesday',84)
    b+=txt(72,1110,700,'On December 1, every gift is doubled.',52,'#fff',S,1.2)
    b+=logo(870,1150,140)
    page('s01',W,Hh,b); soc.append('s01')
def S2():  # side band left, photo right
    b=img(ph('notes.jpg'),420,0,660,1350,'35% 50%','Students’ handwritten notes on what they hope to learn')
    b+=box(0,0,420,1350,D)
    b+=logo(60,64,150)
    b+=txt(60,330,340,'3 days to Giving Tuesday',66)
    b+=txt(60,760,320,'Hundreds of students are waiting for a scholarship.',50,'#fff',S,1.2)
    page('s02',W,Hh,b); soc.append('s02')
def S3():  # banner top, photo below
    b=box(0,0,1080,470,BR)
    b+=txt(72,72,760,'Tomorrow, your gift doubles',84)
    b+=txt(72,300,700,'Giving Tuesday, December 1',52,'#fff',S,1.2)
    b+=logo(880,300,140)
    b+=img(ph('classroom.jpg'),0,470,1080,880,'50% 45%','A full classroom of workshop students in India')
    page('s03',W,Hh,b); soc.append('s03')
def S4():  # full photo, box hugging bottom-left
    b=img(ph('walk.jpg'),0,0,1080,1350,'45% 50%','Workshop students and mentors walking under palm trees in India')
    b+=box(0,890,820,460,G)
    b+=txt(72,950,700,'Today your gift doubles',84)
    b+=txt(72,1148,560,'Every gift matched until midnight.',52,'#fff',S,1.2)
    b+=logo(640,1160,140)
    page('s04',W,Hh,b); soc.append('s04')
def S5():  # live progress
    b=img(ph('students.jpg'),0,0,1080,760,'50% 40%','Workshop students listening in class')
    b+=box(0,760,1080,590,D)
    b+=txt(72,812,936,'[AMOUNT RAISED]',84)
    b+=txt(72,930,936,'raised of our $300,000 goal',52,'#fff',S,1.2)
    b+=box(72,1040,936,44,'#ffffff',22)
    b+=box(72,1040,420,44,L,22)
    b+=logo(870,1160,140)
    page('s05',W,Hh,b); soc.append('s05')
def S6():  # scholar story TrashIt
    b=img(ph('microscope.jpg'),380,0,700,1350,'50% 50%','A student looking into a microscope')
    b+=box(0,0,560,1350,BL)
    b+=txt(60,120,460,'600+ people reached',76)
    b+=txt(60,460,440,'TrashIt’s founders in Pakistan trained with us on scholarship. Today they test soil biology for farmers.',50,'#fff',S,1.2)
    b+=logo(60,1150,140)
    page('s06',W,Hh,b); soc.append('s06')
def S7():  # scholar template
    b=box(0,0,1080,1350,G)
    b+=box(72,72,936,700,'#cfd8c9')
    b+=txt(72,390,936,'Scholar photo',52,'#4F3433',S,1.2,'center')
    b+=txt(72,830,936,'[Scholar name], [country]',72)
    b+=txt(72,1000,760,'[One line on what they do now.]',52,'#fff',S,1.2)
    b+=logo(870,1160,140)
    page('s07',W,Hh,b); soc.append('s07')
def S8():  # World Soil Day
    b=img(ph('talk-back.jpg'),0,0,1080,1350,'50% 40%','An SFW teacher in an In memory of Dr. Elaine Ingham shirt teaching a full room')
    b+=box(0,0,1080,430,D)
    b+=txt(72,64,760,'World Soil Day',84)
    b+=txt(72,190,720,'“Let me teach you so that you can do this for yourself.” Dr. Elaine Ingham',46,'#fff',S,1.25)
    b+=logo(880,190,140)
    page('s08',W,Hh,b); soc.append('s08')
def S9():  # living soil circle
    b=img(ph('extract.jpg'),0,0,1080,1350,'50% 55%','A bucket of compost extract')
    b+=box(0,0,620,640,G)
    b+=txt(72,72,500,'$100 a month',84)
    b+=txt(72,290,480,'Join the Living Soil Circle: $1,200 a year for scholarships.',50,'#fff',S,1.2)
    b+=logo(72,500,120)
    page('s09',W,Hh,b); soc.append('s09')
def S10():  # last call
    b=img(ph('palms.jpg'),0,420,1080,930,'50% 70%','Workshop students walking through a palm farm in India')
    b+=box(0,0,1080,420,G)
    b+=txt(72,72,760,'Last hours of 2026',84)
    b+=txt(72,270,700,'Gifts made today count for 2026.',52,'#fff',S,1.2)
    b+=logo(880,250,140)
    page('s10',W,Hh,b); soc.append('s10')
def S11():  # thank you
    b=img(ph('arms-up.jpg'),0,0,1080,1350,'50% 30%','Workshop students celebrating a finished compost bin')
    b+=box(0,1010,1080,340,BR)
    b+=txt(72,1060,700,'Thank you',84)
    b+=txt(72,1170,700,'We would not be here without you.',52,'#fff',S,1.2)
    b+=logo(880,1160,140)
    page('s11',W,Hh,b); soc.append('s11')
for f in [S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11]: f()

# ---------------- EMAIL HEADERS 1200x400 ----------------
em=[]
def E(pid,photo,pos,alt,title,sub,c,side='left'):
    if side=='left':
        b=img(ph(photo),460,0,740,400,pos,alt)+box(0,0,460,400,c)
        x=48
    else:
        b=img(ph(photo),0,0,740,400,pos,alt)+box(740,0,460,400,c)
        x=788
    b+=txt(x,52,364,title,44)
    b+=txt(x,240,364,sub,26,'#fff',S,1.25)
    b+=logo(x+284 if side=='left' else x+284,300,80)
    page(pid,1200,400,b); em.append(pid)
E('e1','chat.jpg','50% 35%','An SFW teacher talking with students in India','We would not be here without you','Thank you, from all of us',G)
E('e2','../../design/soil.jpg','50% 50%','Living soil up close','Learn it this winter','Cyber Monday course offer',BR,'right')
E('e3','walk.jpg','45% 40%','Workshop students walking under palm trees','Today your gift doubles','Giving Tuesday, December 1',G)
E('e4','shed2.jpg','50% 50%','A mentor teaching students around fresh compost material','Hours left to double your gift','The match ends at midnight',D,'right')
E('e5','talk-back.jpg','50% 45%','An SFW teacher in an In memory of Dr. Elaine Ingham shirt','World Soil Day','Give in her memory',D)
E('e6','students.jpg','50% 40%','Workshop students listening in class','One scholar, a whole community fed','Join the Living Soil Circle',BL,'right')
E('e7','group-field.jpg','50% 55%','Workshop students standing in a green field','Gifts by December 31 count for 2026','Our year-end tax reminder',BR)
E('e8','palms.jpg','50% 65%','Workshop students in a palm farm','Last hours of 2026','Help us reach $300,000 tonight',G,'right')

# ---------------- LINKEDIN 1200x627 ----------------
li=[]
def LI(pid,photo,pos,alt,title,c,layout):
    if layout=='band':
        b=img(ph(photo),460,0,740,627,pos,alt)+box(0,0,460,627,c)
        b+=txt(56,64,350,title,52)
        b+=logo(56,480,100)
    else:
        b=img(ph(photo),0,0,1200,627,pos,alt)+box(0,397,760,230,c)
        b+=txt(56,436,560,title,52)
        b+=logo(620,470,100)
    page(pid,1200,627,b); li.append(pid)
LI('l1','question.jpg','40% 40%','A workshop student asking a question','$300,000 in scholarships this year',G,'band')
LI('l2','speaker.jpg','55% 40%','An SFW mentor presenting to workshop students','Your gift doubles on Giving Tuesday',D,'band')
LI('l3','notes.jpg','50% 50%','Students’ notes on what they hope to learn','One scholarship can change a region',BL,'band')

# ---------------- WEB ----------------
web=[]
b=img(ph('chat.jpg'),640,0,960,800,'50% 40%','An SFW teacher talking with students in India')
b+=box(0,0,700,800,G)
b+=txt(80,110,560,'Carry the work forward',72)
b+=txt(80,330,540,'Today, every gift is doubled until midnight.',30,'#fff',S,1.3)
b+=box(80,470,280,72,BR,36)
b+=txt(80,488,280,'Give now',28,'#fff',H,1.2,'center')
b+=logo(80,630,120)
page('w1',1600,800,b); web.append('w1')
b=img('../../design/hay.jpg',0,0,1600,300,'50% 50%','Hay texture')
b+=box(0,0,1600,300,D)
b+=txt(100,60,900,'[AMOUNT RAISED] raised',56)
b+=txt(1000,72,500,'of $300,000',32,'#fff',S,1.2,'right')
b+=box(100,170,1400,40,'#ffffff',20)
b+=box(100,170,620,40,L,20)
page('w2',1600,300,b); web.append('w2')
ban=[]
for i,(t1,t2) in enumerate([('Giving Tuesday: every gift is doubled until midnight.','Give now'),('Help us raise $300,000 for scholarships by December 31.','Give now'),('Gifts by December 31 count for 2026.','Give now')]):
    b=box(0,0,1920,120,G)
    b+=txt(80,40,1080,t1,32,'#fff',H,1.2)
    b+=box(1620,30,220,60,BR,30)
    b+=txt(1620,45,220,t2,24,'#fff',H,1.2,'center')
    page(f'b{i+1}',1920,120,b); ban.append(f'b{i+1}')

# ---------------- PRINT: LETTER 816x1056 ----------------
letter=f'''
{img(ph('palms.jpg'),0,0,816,250,'50% 72%','Workshop students walking through a palm farm in India')}
{box(0,250,816,64,G)}
{txt(72,268,560,'Carry the work forward',24)}
{logo(690,262,64)}
<div style="position:absolute;left:72px;top:350px;width:672px;{S};font-size:14.5px;line-height:1.55;color:#333130">
<p style="margin:0 0 10px">Dear [FIRST NAME],</p>
<p style="margin:0 0 10px">Thank you. We would not be here without you.</p>
<p style="margin:0 0 10px">A year ago this October, the Soil Food Web Foundation became a nonprofit, so that Dr. Elaine Ingham’s teaching could keep growing for generations. Your gifts made that year possible. Nearly 10,000 students from 140 countries have now trained with us, and in 2026 we extended over $300,000 in scholarships.</p>
<p style="margin:0 0 10px">Those students are changing farms. Both founders of TrashIt in Pakistan completed our foundation certification on scholarship. Today TrashIt offers microbial soil testing, and in a single Soil Health Week it reached more than 600 people across 10 districts. In the United States, farmer Adam York now saves about $1 million a year on 10,000 acres of corn and soy using what he learned.</p>
<p style="margin:0 0 10px">The demand for this knowledge is far greater than our resources. Hundreds of students are waiting for a scholarship. This year we are setting our largest goal yet: $300,000 by December 31.</p>
<p style="margin:0 0 10px">Your gift goes a long way here. $5,000 funds a full scholarship and delivers $10,000 of training. $100 a month, as part of our Living Soil Circle, puts $1,200 a year toward scholarships. Every graduate goes on to teach and advise the farmers around them.</p>
<p style="margin:0 0 10px">On Giving Tuesday, December 1, [MATCH DONOR] will match every gift up to [MATCH AMOUNT], so your gift doubles.</p>
<p style="margin:0 0 10px">Please use the enclosed card, scan the code, or give at soilfoodweb.com/donations. Thank you for carrying the work forward with us.</p>
<p style="margin:0 0 4px">With gratitude,</p>
<p style="margin:0 0 0;padding-top:34px">Evan Buckman<br>Executive Director, Soil Food Web Foundation</p>
</div>
{box(0,964,816,92,G)}
{txt(72,990,560,'P.S. A gift of $5,000 trains one new soil consultant, who then teaches the farmers around them.',13.5,'#fff',S,1.4)}
{img(QR,672,978,64,64,'50% 50%','QR code to soilfoodweb.com/donations')}
'''
page('p1',816,1056,letter)

# ---------------- PRINT: REPLY CARD 672x480 (7x5 in) ----------------
def chk(x,y): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:14px;height:14px;border:1.5px solid #4F3433;box-sizing:border-box"></div>'
def line(x,y,w): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:1px;background:#4F3433"></div>'
card=box(0,0,236,480,G)+txt(28,36,184,'Carry the work forward',24)+txt(28,150,180,'Yes, I want to help restore living soil.',13.5,'#fff',S,1.4)
card+=img(QR,28,250,84,84,'50% 50%','QR code to soilfoodweb.com/donations')
card+=txt(28,344,184,'Give online: soilfoodweb.com/donations',11,'#fff',S,1.35)
card+=logo(28,398,72)
opts=['$100 a month: join the Living Soil Circle','$5,000: fund a full scholarship','$10,000: join the Founders Circle','Other: $']
y=40
for o in opts:
    card+=chk(268,y+3)+txt(292,y,340,o,13,'#333130',S,1.35); y+=34
card+=line(370,y-12,120)
card+=chk(268,y+14)+txt(292,y+11,350,'In honor or memory of:',13,'#333130',S,1.35)+line(292,y+52,340)
y+=80
for lab in ['Name','Email','Address','']:
    if lab: card+=txt(268,y,80,lab,11,'#4F3433',S,1.2)
    card+=line(332 if lab else 268,y+16,300 if lab else 364); y+=34
card+=txt(268,438,380,'Soil Food Web Foundation is a 501(c)(3) public charity. Gifts are tax-deductible as allowed by law. EIN 39-4439236.',9.5,'#6b6460',S,1.35)
page('r1',672,480,card)
print('ok', len(soc), len(em), len(li))
