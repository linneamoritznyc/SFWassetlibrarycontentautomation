H="font-family:'Montserrat',sans-serif;font-weight:700"
G="font-family:'EB Garamond',serif;font-weight:400"
EY="font-family:'Montserrat',sans-serif;font-weight:700;font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:#156826"
DG='#22371F'; GR='#156826'; RULE='#d6d6d0'
def page(pid,body):
    open(f'pages/{pid}.html','w').write(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0}} body > div{{position:relative;width:816px;height:1056px;overflow:hidden;background:#fff;{G};color:#2b2b2b}}
img{{display:block}} p{{margin:0}}
.row{{display:grid;grid-template-columns:150px minmax(0,1fr);gap:24px;padding:9px 0;border-top:1px solid {RULE}}}
.lab{{{H};font-size:12px;line-height:1.5;color:{DG}}}
.tx{{{G};font-size:13.5px;line-height:1.4;color:#2b2b2b}}
.h2{{{H};font-size:19px;line-height:1.2;color:{DG};margin:0 0 12px}}
</style></head><body><div class="pg">{body}</div></body></html>''')

p1=f'''
<img src="../ph/poppies-hi.jpg" alt="Workshop students in a field of red poppies" style="position:absolute;left:0;top:0;width:816px;height:400px;object-fit:cover;object-position:50% 74%">
<div style="position:absolute;left:64px;top:436px;{EY}">Soil Food Web Foundation: Donor Overview</div>
<div style="position:absolute;left:64px;top:462px;width:640px;{H};font-size:36px;line-height:1.12;color:{DG}">Healthy soil. Healthy food.<br>A living legacy.</div>
<div style="position:absolute;left:64px;top:574px;width:688px;height:1px;background:{RULE}"></div>
<div style="position:absolute;left:64px;top:596px;width:322px;{G};font-size:15px;line-height:1.5">The Soil Food Web Foundation carries forward the life's work of Dr. Elaine Ingham, the scientist who showed the world that soil is alive. This October we celebrate our first year as a nonprofit. Our mission is to honor and grow Elaine's legacy of empowering communities to restore and protect the Earth's soil and living systems. We would not be here without the donors who have supported us and shown up. Your gift goes a long way here: $5,000 delivers $10,000 of training, and together we are working to change the global food system.</div>
<div style="position:absolute;left:426px;top:596px;width:326px">
<div class="h2" style="font-size:15px;margin:0 0 6px">Why living soil matters now</div>
<div style="{G};font-size:15px;line-height:1.5">When soil loses its biology, farmers must replace it with costly synthetic fertilizers and pesticides that wash into our rivers. When soil life is restored, farms use fewer chemicals, hold more water, store more carbon and grow more nutritious food. The missing piece is knowledge, and we share it openly. Nothing we teach is proprietary. One farmer, Adam York, now saves about $1 million a year on 10,000 acres of corn and soy using our approach.</div>
</div>
<div style="position:absolute;left:0;top:886px;width:836px;height:170px;background:{DG}"></div>
<div style="position:absolute;left:64px;top:918px;width:560px;{G};font-size:27px;line-height:1.25;color:#ffffff">“Let me teach you so that you can do this for yourself.”</div>
<div style="position:absolute;left:64px;top:1000px;{EY};color:#a9d4b3">— Dr. Elaine Ingham</div>
<img src="../logo-white.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:664px;top:922px;width:88px;height:auto">
'''
page('d1',p1)

def full(items): return ''.join(f'<div class="row" style="grid-template-columns:minmax(0,1fr)"><div class="tx">{b}</div></div>' for b in items)
def rows(items): return ''.join(f'<div class="row"><div class="lab">{a}</div><div class="tx">{b}</div></div>' for a,b in items)
p2=f'''
<div style="position:absolute;left:64px;top:40px;{EY}">Soil Food Web Foundation</div>
<div style="position:absolute;right:64px;top:40px;{EY};text-align:right">Donor Overview</div>
<div style="position:absolute;left:64px;top:76px;width:688px">
<div class="h2">What we do</div>
{rows([('Teach.','Build soil biology literacy, from free public education to professional soil consulting, for students in 140 countries.'),('Research.',"Build on Elaine's experiments to advance the science, and share our data openly so practice rests on evidence."),('Practice.','Partner with farmers to trial soil food web methods in different regions and climates.'),('Connect.','Grow a worldwide network of practitioners and leaders who share what works.')])}
<div class="h2" style="margin-top:30px">Our first year</div>
{full(["Became a nonprofit and received all of the school's intellectual property, now held for the public good",'Redesigned our courses and launched a Permaculture Design Certificate with the Permaculture Association UK (100 students from 23 countries)',"Awarded over $300,000 in scholarships in 2026, and welcomed nearly 10,000 students from 140 countries into our programs. Our organizational scholarships reach partners such as iCow in East Africa and TrashIt in Pakistan. Both of TrashIt's founders completed our foundation certification on scholarship, and TrashIt now offers microbial soil testing and reached 600+ people across 10+ districts in one Soil Health Week"])}
<div class="h2" style="margin-top:30px">What your gift makes possible</div>
{full(['Scholarships open our courses to students who could not otherwise attend.','Sponsored workshop seats bring hands-on training to farming communities that need it most.','New programs such as our compost cohort, with liquid amendments and microscopy programs in development.','Unrestricted gifts go where the need is greatest and help us grow.'])}
</div>
<div style="position:absolute;left:0;top:800px;width:836px;height:256px;background:{DG}"></div>
<div style="position:absolute;left:64px;top:832px;width:500px;{H};font-size:22px;line-height:1.2;color:#fff">Goal: raise $300,000 by December 31</div>
<div style="position:absolute;left:64px;top:868px;width:520px;{G};font-size:13.5px;line-height:1.4;color:#e6efe3">Celebrate our first year and help carry Elaine's work forward. Giving pathways: one-time gifts, monthly giving, workshop and scholarship sponsorships, and legacy gifts.</div>
<img src="../qr.png" alt="QR code to soilfoodweb.com/donations" style="position:absolute;left:64px;top:942px;width:64px;height:64px">
<div style="position:absolute;left:146px;top:942px;width:440px;{G};font-size:13px;line-height:1.45;color:#e6efe3">Give online: soilfoodweb.com/donations · Giving Tuesday: December 1 · Contact: Evan Buckman, Executive Director, evan@soilfoodweb.com, (512) 359-5206 · www.soilfoodweb.com</div>
<div style="position:absolute;left:146px;top:1004px;width:520px;{G};font-size:10.5px;line-height:1.35;color:#a9d4b3">Soil Food Web Foundation is a 501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.</div>
<img src="../logo-white.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:664px;top:836px;width:88px;height:auto">
'''
page('d2',p2)
