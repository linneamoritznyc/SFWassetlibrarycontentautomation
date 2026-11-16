exec(open('d3gen.py').read().split('# ---- PAGE 1')[0])
def heads2(): return f'<div style="position:absolute;left:64px;top:40px;{EY};color:{GR}">Soil Food Web Foundation</div><div style="position:absolute;right:64px;top:40px;{EY};color:{GR};text-align:right">Case for Support</div>'
T=lambda x,y,w,t,sz=15,c='#2b2b2b',lh=1.5: f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;{G};font-size:{sz}px;line-height:{lh};color:{c}">{t}</div>'
# PAGE 1
p1=f'''
<img src="../ph/palms.jpg" alt="Workshop students walking through a palm farm in India" style="position:absolute;left:0;top:0;width:816px;height:480px;object-fit:cover;object-position:50% 60%">
<div style="position:absolute;left:0;top:480px;width:836px;height:8px;background:{GR}"></div>
<div style="position:absolute;left:64px;top:526px;{EY};color:{GR}">Soil Food Web Foundation: Case for Support</div>
<div style="position:absolute;left:64px;top:554px;width:660px;{H};font-size:38px;line-height:1.12;color:{DG}">Restoring living soil.<br>Growing a global community.</div>
{T(64,668,688,"The Soil Food Web Foundation carries forward the life's work of Dr. Elaine Ingham, who showed the world that soil is alive, and provided a practical, scientific roadmap for restoring it. This October marks our first year as a nonprofit, created so that her essential teachings and the community of practice that has grown around them can live on for many generations to come.",16.5)}
<div style="position:absolute;left:0;top:846px;width:836px;height:210px;background:{DG}"></div>
{T(64,876,560,'"The paradigm shift she shows us, that soil is alive and that soil microbiology matters, has profound meaning not just for agriculture, but for human life itself on the planet."',19,'#ffffff',1.35)}
<div style="position:absolute;left:64px;top:1000px;width:560px;{EY};color:#a9d4b3">Leslie Lewis, Board Chair and graduate of our consultant training program</div>
<img src="../logo-white.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:664px;top:900px;width:88px;height:auto">
'''
page('c1',p1)
# PAGE 2
p2=heads2()+f'''
<img src="../ph/talk-back.jpg" alt="An SFW teacher in an In memory of Dr. Elaine Ingham shirt teaching a full room in India" style="position:absolute;left:0;top:76px;width:816px;height:250px;object-fit:cover;object-position:50% 45%">
<div class="h2" style="position:absolute;left:64px;top:354px">Why it matters now</div>
{T(64,396,330,"The green revolution brought immense change to the global food system. We saw huge increases in the total pounds of food produced around the world, which came at the cost of topsoil loss, fertility decline, lower nutrient density in our food, toxic chemicals in our bodies, food and water, extreme loss of biodiversity, and the erosion of farmer profitability.",14.5,lh=1.45)}
{T(64,610,330,"The world is waking up to this reality; soil health and regenerative agriculture initiatives abound from governments to corporations to grassroots initiatives.",14.5,lh=1.45)}
{T(422,396,330,"The problem is, almost all of these initiatives are ignorant to the reality of life in the soil which is absolutely fundamental. The Soil Food Web Foundation fulfills a unique role by teaching farmers, agricultural professionals, gardeners and land stewards to understand, measure, and restore the life in their soil. We empower them to transform locally available organic residues into potent biological inoculants that have proven successful for decades in improving soil health, food quality, and farmers profitability.",14.5,lh=1.45)}
<div style="position:absolute;left:64px;top:726px;width:688px;height:300px;border-radius:18px;background:{DG}"></div>
{T(92,752,302,"Elaine’s teachings have influenced millions of people around the world, and our school has welcomed nearly 10,000 students from 140 countries into our educational programs. Our students themselves have gone on to touch and transform the lives of millions of farmers and transform millions of acres of land - from Illinois, to Kenya, to India. Our students are working every day to put these teachings into practice and are leaders in the regenerative movement.",13.5,'#e9f0e6',1.42)}
{T(422,752,302,"The demand for this knowledge is far greater than we currently have the resources to provide. Farmers around the world, for whom the knowledge of how to grow sufficient food without relying on synthetic, imported fertilizers and toxic chemicals, could mean the difference between nourishment and hunger, are eager to attain these skills. Our scholarship programs are expanding, we are hosting live workshops in new locations, working directly with farmers to implement and demonstrate this work, and actively growing our global community.",13.5,'#e9f0e6',1.42)}
'''
page('c2',p2)
# PAGE 3
bar=[('student','Few farmers and agronomists are taught how soil biology works','Free public education and webinars, intensive theoretical online courses, and in person practical intensives'),
     ('compost','Inputs and training many cannot afford','Over $300,000 in scholarships in 2026, and compost made from free local materials'),
     ('fielddata','Methods that do not fit local soils','Hands-on workshops, mentors and step-by-step guides, region by region')]
b=f'<div style="position:absolute;left:64px;top:84px;{EY};color:{GR}">Barriers to change</div><div style="position:absolute;left:420px;top:84px;{EY};color:{GR}">Our response</div>'
for k,(ic,l,r) in enumerate(bar):
    y=108+k*86
    b+=f'<div class="card" style="left:64px;top:{y}px;width:340px;height:76px;background:#f3f7f1;border:none"></div>'+icon(ic,84,y+21,32)
    b+=f'<div class="h3" style="position:absolute;left:132px;top:{y+18}px;width:256px;font-size:13.5px;line-height:1.3">{l}</div>'
    b+=f'<div class="card" style="left:412px;top:{y}px;width:340px;height:76px"></div>'
    b+=T(432,y+14,300,r,14,lh=1.35)
gifts=[('$5,000','funds a full scholarship for someone to become a SFW Consultant: our Foundation Courses and The Complete Practicum'),('$10,000','sponsors an all inclusive scholarship at a two-week hands-on workshop'),('$25,000','sponsors a group of courses for a community in need'),('$100,000','sponsors a whole workshop in a new region, such as Kenya or Brazil')]
g=f'<div class="h2" style="position:absolute;left:64px;top:390px">What your gift makes possible</div>'
g+=f'<div style="position:absolute;left:64px;top:430px;{EY};color:{GR}">Gift</div><div style="position:absolute;left:226px;top:430px;{EY};color:{GR}">Impact</div>'
for k,(a,t) in enumerate(gifts):
    y=452+k*56
    g+=f'<div style="position:absolute;left:64px;top:{y}px;width:688px;height:1px;background:#d9e3d4"></div>'
    g+=f'<div style="position:absolute;left:64px;top:{y+12}px;{H};font-size:22px;line-height:1.2;color:{GR}">{a}</div>'
    g+=T(226,y+10,520,t,15,lh=1.4)
g+=f'<div style="position:absolute;left:64px;top:676px;width:688px;height:1px;background:#d9e3d4"></div>'
q=T(64,700,620,'"We see a more beautiful world, and we dedicate our lives to restoring the invisible layers of life that make that world possible."',19,DG,1.35)+f'<div style="position:absolute;left:64px;top:762px;{EY};color:{GR}">Evan Buckman, Executive Director</div>'
band=f'''
<div style="position:absolute;left:0;top:800px;width:836px;height:256px;background:{DG}"></div>
<div style="position:absolute;left:64px;top:832px;width:560px;{H};font-size:22px;line-height:1.2;color:#fff">GOAL: RAISE $300,000 BY DECEMBER 31, 2026.</div>
<img src="../logo-white.png" alt="Soil Food Web Foundation logo" style="position:absolute;left:664px;top:828px;width:88px;height:auto">
<img src="../qr.png" alt="QR code to soilfoodweb.com/donations" style="position:absolute;left:64px;top:884px;width:84px;height:84px">
{T(170,880,560,"Give today at soilfoodweb.com/donations or scan the QR code. One-time gifts, monthly giving, sponsorships, and legacy gifts. For customized giving, contact Evan Buckman, Executive Director, at evan@soilfoodweb.com or (512) 359-5206. 501(c)(3) public charity, and gifts are tax-deductible as allowed by law, EIN 39-4439236.",13.5,'#e9f0e6',1.42)}
'''
page('c3',heads2()+b+g+q+band)
