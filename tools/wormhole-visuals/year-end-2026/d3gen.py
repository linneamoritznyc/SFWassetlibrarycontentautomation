H="font-family:'Montserrat',sans-serif;font-weight:700"
G="font-family:'EB Garamond',serif;font-weight:400"
EY="font-family:'Montserrat',sans-serif;font-weight:700;font-size:10px;letter-spacing:.22em;text-transform:uppercase"
DG='#22371F'; GR='#156826'; LG='#59A66C'; BR='#4F3433'
def page(pid,body):
    open(f'pages/{pid}.html','w').write(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0}} body > div{{position:relative;width:816px;height:1056px;overflow:hidden;background:#fff;{G};color:#2b2b2b}}
img{{display:block}}
.h2{{{H};font-size:22px;line-height:1.15;color:{DG}}}
.h3{{{H};font-size:15px;line-height:1.25;color:{DG}}}
.tx{{{G};font-size:15px;line-height:1.45;color:#2b2b2b}}
.card{{position:absolute;border:1px solid #d9e3d4;border-radius:18px;background:#fff;box-sizing:border-box;padding:22px 24px}}
</style></head><body><div class="pg">{body}</div></body></html>''')
def heads(): return f'<div style="position:absolute;left:64px;top:40px;{EY};color:{GR}">Soil Food Web Foundation</div><div style="position:absolute;right:64px;top:40px;{EY};color:{GR};text-align:right">Donor Overview</div>'
def icon(n,x,y,s=34,c='i'): return f'<img src="../{c}-{n}.png" alt="{n} icon" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px">'

# ---- PAGE 1
p1=f'''
<img src="../ph/poppies-hi.jpg" alt="Workshop students in a field of red poppies" style="position:absolute;left:0;top:0;width:816px;height:500px;object-fit:cover;object-position:50% 72%">
<div style="position:absolute;left:0;top:500px;width:836px;height:8px;background:{GR}"></div>
<div style="position:absolute;left:64px;top:548px;{EY};color:{GR}">Soil Food Web Foundation: Donor Overview</div>
<div style="position:absolute;left:64px;top:576px;width:620px;{H};font-size:40px;line-height:1.1;color:{DG}">Healthy soil. Healthy food.<br>A living legacy.</div>
<div style="position:absolute;left:64px;top:704px;width:420px;{G};font-size:16.5px;line-height:1.5">The Soil Food Web Foundation carries forward the life's work of Dr. Elaine Ingham, the scientist who showed the world that soil is alive. This October we celebrate our first year as a nonprofit. Our mission is to honor and grow Elaine's legacy of empowering communities to restore and protect the Earth's soil and living systems. We would not be here without the donors who have supported us and shown up. Your gift goes a long way here: $5,000 delivers $10,000 of training, and together we are working to change the global food system.</div>
<div style="position:absolute;left:520px;top:704px;width:232px;height:288px;border-radius:18px;background:{DG}"></div>
<div style="position:absolute;left:544px;top:730px;width:190px;{G};font-size:22px;line-height:1.3;color:#fff">“Let me teach you so that you can do this for yourself.”</div>
<div style="position:absolute;left:544px;top:878px;width:190px;{G};font-size:13px;line-height:1.3;color:#a9d4b3">— Dr. Elaine Ingham</div>
<img src="../logo-white.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:660px;top:920px;width:72px;height:auto">
'''
page('e1',p1)

# ---- PAGE 2
wwd=[('student','Teach.','Build soil biology literacy, from free public education to professional soil consulting, for students in 140 countries.'),
     ('fielddata','Research.',"Build on Elaine's experiments to advance the science, and share our data openly so practice rests on evidence."),
     ('barn','Practice.','Partner with farmers to trial soil food web methods in different regions and climates.'),
     ('network','Connect.','Grow a worldwide network of practitioners and leaders who share what works.')]
cards=''
for k,(ic,t,d) in enumerate(wwd):
    x=64+(k%2)*352; y=730+(k//2)*140
    cards+=f'<div class="card" style="left:{x}px;top:{y}px;width:336px;height:128px"></div>'
    cards+=icon(ic,x+24,y+24,34)
    cards+=f'<div class="h3" style="position:absolute;left:{x+74}px;top:{y+30}px">{t}</div>'
    cards+=f'<div class="tx" style="position:absolute;left:{x+74}px;top:{y+56}px;width:238px;font-size:14px;line-height:1.4">{d}</div>'
p2=heads()+f'''
<img src="../ph/cr-compost-group.jpg" alt="Workshop students with a finished compost bin" style="position:absolute;left:0;top:76px;width:816px;height:330px;object-fit:cover;object-position:50% 62%">
<div style="position:absolute;left:64px;top:426px;width:688px;height:240px;border-radius:18px;background:{DG}"></div>
<div style="position:absolute;left:96px;top:452px;width:620px;{H};font-size:22px;line-height:1.15;color:#fff">Why living soil matters now</div>
<div style="position:absolute;left:96px;top:490px;width:624px;{G};font-size:15.5px;line-height:1.5;color:#e9f0e6">When soil loses its biology, farmers must replace it with costly synthetic fertilizers and pesticides that wash into our rivers. When soil life is restored, farms use fewer chemicals, hold more water, store more carbon and grow more nutritious food. The missing piece is knowledge, and we share it openly. Nothing we teach is proprietary. One farmer, Adam York, now saves about $1 million a year on 10,000 acres of corn and soy using our approach.</div>
<div class="h2" style="position:absolute;left:64px;top:692px">What we do</div>
{cards}
'''
page('e2',p2)

# ---- PAGE 3
fy=["Became a nonprofit and received all of the school's intellectual property, now held for the public good",
    'Redesigned our courses and launched a Permaculture Design Certificate with the Permaculture Association UK (100 students from 23 countries)',
    "Awarded over $300,000 in scholarships in 2026, and welcomed nearly 10,000 students from 140 countries into our programs. Our organizational scholarships reach partners such as iCow in East Africa and TrashIt in Pakistan. Both of TrashIt's founders completed our foundation certification on scholarship, and TrashIt now offers microbial soil testing and reached 600+ people across 10+ districts in one Soil Health Week"]
fyc=f'<div class="h2" style="position:absolute;left:64px;top:84px">Our first year</div>'
fyc+=f'<div class="card" style="left:64px;top:126px;width:256px;height:150px;background:#f3f7f1;border:none"></div>'
fyc+=icon('barn',88,148,30)+f'<div class="tx" style="position:absolute;left:88px;top:190px;width:210px;font-size:14px;line-height:1.4">{fy[0]}</div>'
fyc+=f'<div class="card" style="left:64px;top:290px;width:256px;height:150px;background:#f3f7f1;border:none"></div>'
fyc+=icon('compost',88,312,30)+f'<div class="tx" style="position:absolute;left:88px;top:354px;width:210px;font-size:14px;line-height:1.4">{fy[1]}</div>'
fyc+=f'<div class="card" style="left:336px;top:126px;width:416px;height:314px;background:{GR};border:none"></div>'
fyc+=icon('student',360,150,34,'w')+f'<div class="tx" style="position:absolute;left:360px;top:200px;width:368px;font-size:15px;line-height:1.5;color:#fff">{fy[2]}</div>'
gift=[('student','Scholarships open our courses to students who could not otherwise attend.'),
      ('table','Sponsored workshop seats bring hands-on training to farming communities that need it most.'),
      ('idea','New programs such as our compost cohort, with liquid amendments and microscopy programs in development.'),
      ('fundraiser','Unrestricted gifts go where the need is greatest and help us grow.')]
gc=f'<div class="h2" style="position:absolute;left:64px;top:474px">What your gift makes possible</div>'
for k,(ic,d) in enumerate(gift):
    x=64+k*176
    gc+=f'<div class="card" style="left:{x}px;top:516px;width:160px;height:196px"></div>'+icon(ic,x+20,536,32)
    gc+=f'<div class="tx" style="position:absolute;left:{x+20}px;top:580px;width:122px;font-size:13.5px;line-height:1.4">{d}</div>'
band=f'''
<div style="position:absolute;left:0;top:744px;width:836px;height:312px;background:{DG}"></div>
<div style="position:absolute;left:64px;top:776px;width:520px;{H};font-size:26px;line-height:1.15;color:#fff">Goal: raise $300,000 by December 31</div>
<div style="position:absolute;left:64px;top:818px;width:540px;{G};font-size:15px;line-height:1.45;color:#e9f0e6">Celebrate our first year and help carry Elaine's work forward. Giving pathways: one-time gifts, monthly giving, workshop and scholarship sponsorships, and legacy gifts.</div>
<img src="../logo-white.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:664px;top:780px;width:88px;height:auto">
<div style="position:absolute;left:64px;top:896px;width:688px;height:1px;background:#4b6346"></div>
<img src="../qr.png" alt="QR code to soilfoodweb.com/donations" style="position:absolute;left:64px;top:918px;width:76px;height:76px">
<div style="position:absolute;left:162px;top:920px;width:560px;{G};font-size:14px;line-height:1.45;color:#e9f0e6">Give online: soilfoodweb.com/donations · Giving Tuesday: December 1 · Contact: Evan Buckman, Executive Director, evan@soilfoodweb.com, (512) 359-5206 · www.soilfoodweb.com</div>
<div style="position:absolute;left:162px;top:982px;width:560px;{G};font-size:11.5px;line-height:1.35;color:#a9d4b3">Soil Food Web Foundation is a 501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.</div>
'''
page('e3',heads()+fyc+gc+band)
