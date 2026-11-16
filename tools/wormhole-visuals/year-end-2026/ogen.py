from tbl import table
G="font-family:'EB Garamond',serif;font-weight:400"
GS="font-family:'EB Garamond',serif;font-weight:600"
EY="font-family:'Montserrat',sans-serif;font-weight:700;font-size:10px;letter-spacing:.22em;text-transform:uppercase"
DG='#22371F'; GR='#156826'; LG='#7fbf8d'; RC='#c9d8c4'
def page(pid,body,bg='#fff'):
    open(f'pages/{pid}.html','w').write(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0}} body > div{{position:relative;width:816px;height:1056px;overflow:hidden;background:{bg};{G};color:#2b2b2b}}
img{{display:block}}
</style></head><body><div class="pg">{body}</div></body></html>''')
def heads(c=GR): return f'<div style="position:absolute;left:72px;top:44px;{EY};color:{c}">Soil Food Web Foundation</div><div style="position:absolute;right:72px;top:44px;{EY};color:{c};text-align:right">Donor Overview</div>'
def T(x,y,w,t,sz=16,c='#2b2b2b',lh=1.45,f=G): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;{f};font-size:{sz}px;line-height:{lh};color:{c}">{t}</div>'
def rule(y,c=RC,x=72,w=672): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:1px;background:{c}"></div>'
def logo(x,y,w,white=False): return f'<img src="../{"logo-white" if white else "logo"}.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:auto">'
def img(src,alt,x,y,w,h,pos='50% 50%'): return f'<img src="../ph/{src}" alt="{alt}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;object-position:{pos}">'

# P1 cover: poppies, title, intro
p1=img('poppies-hi.jpg','Workshop students in a field of red poppies',0,0,816,500,'50% 72%')+f'''
<div style="position:absolute;left:72px;top:548px;{EY};color:{GR}">Soil Food Web Foundation: Donor Overview</div>
{T(72,572,640,'Healthy soil. Healthy food.<br>A living legacy.',40,GR,1.12)}
{rule(684)}
{T(72,706,672,"The Soil Food Web Foundation carries forward the life's work of Dr. Elaine Ingham, the scientist who showed the world that soil is alive. This October we celebrate our first year as a nonprofit. Our mission is to honor and grow Elaine's legacy of empowering communities to restore and protect the Earth's soil and living systems. We would not be here without the donors who have supported us and shown up. Your gift goes a long way here: $5,000 delivers comprehensive training from theory to full implementation, and together we are working to change the global food system.",17)}
{logo(680,962,64)}
'''
page('o1',p1)

# P2: why it matters + what we do (icons, no boxes) + duotone field photo
wd=[('i-student','Teach.','Build soil biology literacy, from free public education to professional soil consulting, for students in 140 countries.'),
    ('i-fielddata','Research.',"Build on Elaine's experiments to advance the science, and share our data openly so practice rests on evidence."),
    ('i-compost','Practice.','Partner with farmers and organizations to demonstrate soil food web methods in different regions and climates.'),
    ('i-network','Connect.','Grow a worldwide community of practitioners and leaders who share what works and support each other.')]
p2=heads()+T(72,92,672,'Why living soil matters now',30,GR,1.1)+rule(136)
p2+=T(72,156,672,"When soil loses its biology, farmers must replace it with costly synthetic fertilizers and pesticides that wash into our rivers. When soil life is restored, farms use fewer chemicals, hold more water, store more carbon and grow more nutritious food. The missing piece is knowledge, and we share it openly. Nothing we teach is proprietary. One farmer in Illinois, Adam York, reported saving about $1 million a year after implementing the Soil Food Web Approach on 10,000 acres of corn and soy, after working with Soil Food Web Consultant, Todd Harrington. Now he runs a company called Agribio Systems, servicing hundreds of thousands of acres of farmland in his region and helping other farmers transform their operations.",16,lh=1.5)
p2+=T(72,412,672,'What we do',30,GR,1.1)+rule(456)
for k,(ic,l,t) in enumerate(wd):
    x=72+(k%2)*356; y=482+(k//2)*122
    p2+=T(x,y,316,l,19,DG,1.2,GS)+T(x,y+30,316,t,15,lh=1.42)
p2+=img('group-field-duo.jpg','SFW workshop group standing together in a field',0,752,816,304,'50% 45%')
page('o2',p2)

# P3: first year + gift table on white, goal block on deep green
fy=["Became a nonprofit and received all of the school's intellectual property, now held for the public good",
    "Redesigned our core courses and launched a Permaculture Design Certificate with the Permaculture Association UK (100 students from 23 countries)",
    "Awarded over $300,000 in scholarships in 2026, and grew our student community to nearly 10,000 individuals from 140 countries. Our organizational scholarships reach partners such as iCow in East Africa and TrashIt in Pakistan. Both of TrashIt's founders completed our foundation courses on scholarships, and TrashIt now offers microbial soil testing and reached 600+ people across 10+ districts in one Soil Health Week."]
p3=heads()+T(72,92,672,'Our first year',30,GR,1.1)+rule(136)
p3+=table(72,138,672,[672],[(t,) for t in fy],[f"{G};font-size:15px;line-height:1.45;color:#2b2b2b"],RC,(12,0))
gm=[('Scholarships','open our courses to students who could not otherwise attend.'),('Sponsored workshop seats','bring hands-on training to farming communities that need it most.'),('New programs','such as our compost cohort, with liquid amendments and microscopy programs in development.'),('Unrestricted gifts','go where the need is greatest and help us grow.')]
p3+=T(72,432,672,'What your gift makes possible',30,GR,1.1)+rule(476)
p3+=table(72,478,672,[230,442],gm,[f"{GS};font-size:16px;line-height:1.35;color:{DG}",f"{G};font-size:15px;line-height:1.42;color:#2b2b2b"],RC,(11,20))
p3+=f'<div style="position:absolute;left:0;top:756px;width:816px;height:300px;background:{DG}"></div>'
p3+='<img src="../mycelium.png" alt="Fungal network drawing" style="position:absolute;left:560px;top:784px;width:400px;height:auto;opacity:.8">'
p3+=T(72,780,520,'Goal: raise $300,000 by December 31',28,'#ffffff',1.15)
p3+=f'''<div style="position:absolute;left:72px;top:826px;width:600px">
<div style="{G};font-size:18px;line-height:1.35;color:#e9f0e6">"Let me teach you so that you can do this for yourself." — Dr. Elaine Ingham</div>
<div style="margin-top:8px;{G};font-size:15px;line-height:1.45;color:#e9f0e6">Celebrate our first year and help carry Dr. Elaine's work forward. Giving pathways: one-time gifts, monthly giving, workshop and scholarship sponsorships, and legacy gifts.</div></div>
<img src="../qr.png" alt="QR code to soilfoodweb.com/donations" style="position:absolute;left:72px;top:944px;width:76px;height:76px">
<div style="position:absolute;left:172px;top:940px;width:440px">
<div style="{G};font-size:13px;line-height:1.4;color:#e9f0e6">Give online: soilfoodweb.com/donations · Giving Tuesday: December 1 · Contact: Evan Buckman, Executive Director, evan@soilfoodweb.com, (512) 359-5206 · www.soilfoodweb.com</div>
<div style="margin-top:6px;{G};font-size:10.5px;line-height:1.3;color:#a9d4b3">Soil Food Web Foundation is a 501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.</div></div>'''
page('o3',p3)
