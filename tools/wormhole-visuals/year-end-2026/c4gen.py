from tbl import table
G="font-family:'EB Garamond',serif;font-weight:400"
GS="font-family:'EB Garamond',serif;font-weight:600"
EY="font-family:'Montserrat',sans-serif;font-weight:700;font-size:10px;letter-spacing:.22em;text-transform:uppercase"
DG='#22371F'; GR='#156826'; LG='#7fbf8d'
def page(pid,body,bg='#fff'):
    open(f'pages/{pid}.html','w').write(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0}} body > div{{position:relative;width:816px;height:1056px;overflow:hidden;background:{bg};{G};color:#2b2b2b}}
img{{display:block}}
</style></head><body><div class="pg">{body}</div></body></html>''')
def heads(c=GR): return f'<div style="position:absolute;left:96px;top:44px;{EY};color:{c}">Soil Food Web Foundation</div><div style="position:absolute;right:96px;top:44px;{EY};color:{c};text-align:right">Case for Support</div>'
def T(x,y,w,t,sz=17,c='#2b2b2b',lh=1.45,f=G): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;{f};font-size:{sz}px;line-height:{lh};color:{c}">{t}</div>'
def rule(y,c='#c9d8c4',x=96,w=624): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:1px;background:{c}"></div>'
def logo(x,y,w,white=False): return f'<img src="../{"logo-white" if white else "logo"}.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:auto">'

# P1 cover
p1=f'''
<img src="../ph/palms.jpg" alt="Workshop students walking through a palm farm in India" style="position:absolute;left:0;top:0;width:816px;height:500px;object-fit:cover;object-position:50% 60%">
<div style="position:absolute;left:96px;top:548px;{EY};color:{GR}">Soil Food Web Foundation: Case for Support</div>
{T(96,572,640,'Restoring living soil.<br>Growing a global community.',40,GR,1.12)}
{rule(684)}
{T(96,706,624,"The Soil Food Web Foundation carries forward the life's work of Dr. Elaine Ingham, who showed the world that soil is alive, and provided a practical, scientific roadmap for restoring it. This October marks our first year as a nonprofit, created so that her essential teachings and the community of practice that has grown around them can live on for many generations to come.",17)}
{logo(672,962,64)}
'''
page('k1',p1)

# P2 why it matters + Leslie quote
p2=heads()+f'''
{T(96,92,624,'"The paradigm shift she shows us, that soil is alive and that soil microbiology matters, has profound meaning not just for agriculture, but for human life itself on the planet."',23,DG,1.32)}
<div style="position:absolute;left:96px;top:226px;{EY};color:{GR}">Leslie Lewis, Board Chair and graduate of our consultant training program</div>
{T(96,282,624,'Why it matters now',30,GR,1.1)}
{rule(326)}
{T(96,344,300,"The green revolution brought immense change to the global food system. We saw huge increases in the total pounds of food produced around the world, which came at the cost of topsoil loss, fertility decline, lower nutrient density in our food, toxic chemicals in our bodies, food and water, extreme loss of biodiversity, and the erosion of farmer profitability.",15.5,lh=1.45)}
{T(96,604,300,"The world is waking up to this reality; soil health and regenerative agriculture initiatives abound from governments to corporations to grassroots initiatives.",15.5,lh=1.45)}
{T(420,344,300,"The problem is, almost all of these initiatives are ignorant to the reality of life in the soil which is absolutely fundamental. The Soil Food Web Foundation fulfills a unique role by teaching farmers, agricultural professionals, gardeners and land stewards to understand, measure, and restore the life in their soil. We empower them to transform locally available organic residues into potent biological inoculants that have proven successful for decades in improving soil health, food quality, and farmers profitability.",15.5,lh=1.45)}
<img src="../ph/students-duo.jpg" alt="Workshop students listening in class" style="position:absolute;left:0;top:742px;width:816px;height:314px;object-fit:cover;object-position:50% 45%">
'''
page('k2',p2)

# P3 reach + demand, then barriers with duotone photo
rows=[('Few farmers and agronomists are taught how soil biology works','Free public education and webinars, intensive theoretical online courses, and in person practical intensives'),
      ('Inputs and training many cannot afford','Over $300,000 in scholarships in 2026, and compost made from free local materials'),
      ('Methods that do not fit local soils','Hands-on workshops, mentors and step-by-step guides, region by region')]
bt=T(96,640,300,'Barriers to change',26,GR,1.1)+T(420,640,300,'Our response',26,GR,1.1)+rule(684)
bt+=table(96,686,624,[324,300],rows,[f"{GS};font-size:15.5px;line-height:1.4;color:#2b2b2b",f"{G};font-size:15.5px;line-height:1.4;color:#2b2b2b"],'#c9d8c4',(14,24))
p3=f'''
<img src="../ph/talk-back-duo.jpg" alt="An SFW teacher in an In memory of Dr. Elaine Ingham shirt teaching a full room in India" style="position:absolute;left:0;top:0;width:816px;height:300px;object-fit:cover;object-position:50% 40%">
{T(96,336,300,"Elaine’s teachings have influenced millions of people around the world, and our school has welcomed nearly 10,000 students from 140 countries into our educational programs. Our students themselves have gone on to touch and transform the lives of millions of farmers and transform millions of acres of land - from Illinois, to Kenya, to India. Our students are working every day to put these teachings into practice and are leaders in the regenerative movement.",14.5,lh=1.42)}
{T(420,336,300,"The demand for this knowledge is far greater than we currently have the resources to provide. Farmers around the world, for whom the knowledge of how to grow sufficient food without relying on synthetic, imported fertilizers and toxic chemicals, could mean the difference between nourishment and hunger, are eager to attain these skills. Our scholarship programs are expanding, we are hosting live workshops in new locations, working directly with farmers to implement and demonstrate this work, and actively growing our global community.",14.5,lh=1.42)}
{bt}
{logo(672,972,56)}
'''
page('k3',p3)

# P4 deep green: gifts, quote, goal, give
gifts=[('$5,000','funds a full scholarship for someone to become a SFW Consultant: our Foundation Courses and The Complete Practicum'),('$10,000','sponsors an all inclusive scholarship at a two-week hands-on workshop'),('$25,000','sponsors a group of courses for a community in need'),('$100,000','sponsors a whole workshop in a new region, such as Kenya or Brazil')]
RL='#4f6a4a'
g=heads('#a9d4b3')+T(96,104,624,'What your gift makes possible',34,'#ffffff',1.1)
g+=table(96,182,624,[160,464],[('Gift','Impact')]+[((a,f"{G};font-size:24px;line-height:1.2;color:#ffffff"),(t,f"{G};font-size:16px;line-height:1.45;color:#e9f0e6;padding-top:24px")) for a,t in gifts],[f"{GS};font-size:20px;line-height:1.3;color:{LG}",f"{GS};font-size:20px;line-height:1.3;color:{LG}"],RL,(20,20))
g+=T(96,624,600,'"We see a more beautiful world, and we dedicate our lives to restoring the invisible layers of life that make that world possible."',23,'#ffffff',1.34)
g+=f'<div style="position:absolute;left:96px;top:742px;{EY};color:#a9d4b3">Evan Buckman, Executive Director</div>'
g+=rule(830,RL)
g+=f'<div style="position:absolute;left:96px;top:862px;{EY};font-size:14px;letter-spacing:.12em;color:#ffffff">GOAL: RAISE $300,000 BY DECEMBER 31, 2026.</div>'
g+=f'<img src="../qr.png" alt="QR code to soilfoodweb.com/donations" style="position:absolute;left:96px;top:906px;width:92px;height:92px">'
g+=T(212,902,440,"Give today at soilfoodweb.com/donations or scan the QR code. One-time gifts, monthly giving, sponsorships, and legacy gifts. For customized giving, contact Evan Buckman, Executive Director, at evan@soilfoodweb.com or (512) 359-5206. 501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.",13.5,'#e9f0e6',1.42)
g+=logo(664,930,56,True)
page('k4',g,DG)
