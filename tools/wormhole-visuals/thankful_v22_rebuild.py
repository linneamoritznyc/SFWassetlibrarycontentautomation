import io, glob, copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
E_=9525; px=lambda v:Emu(int(round(v*E_)))
PK='/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/lib/pack/SFW Nature Cutouts/'
PC='/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/tg/pieces/'
acorn=sorted(glob.glob(PK+'Acorns and pine cones/*.png')); autumn=sorted(glob.glob(PK+'Autumn leaves/*.png'))
cones=[f for f in acorn if any(k in f for k in ('-02','-04','-05','-07','-08','-09','-10','-11','-12','-13'))]
nuts=[f for f in acorn if f not in cones]
def prep(f):
    im=Image.open(f).convert('RGBA'); im=im.crop(im.getchannel('A').getbbox())
    if max(im.size)>900: im.thumbnail((900,900),Image.LANCZOS)
    p=PC+f.split('/')[-1]; im.save(p); return p,im.size
def piece(s,f,x,y,w,rot,name):
    p,(pw,ph)=prep(f); h=w*ph/pw
    pic=s.shapes.add_picture(p,px(x),px(y),px(w),px(h)); pic.rotation=rot; pic.name=name; return pic
GREEN=RGBColor(0x15,0x68,0x26); INK=RGBColor(0x33,0x31,0x30); CREAM=RGBColor(0xF4,0xF1,0xEA)
BODY=32  # pt  (42.7 px on the 1080 canvas)
F=ImageFont.truetype('/root/.fonts/SourceSans3.ttf',43)
def nlines(t,w):
    n=0
    for para in t.split('\n'):
        cur=''
        for wd in para.split():
            tt=(cur+' '+wd).strip()
            if F.getlength(tt)>w: n+=1;cur=wd
            else: cur=tt
        n+=1
    return n
def spacing(par,pt):
    pPr=par._p.get_or_add_pPr()
    for e in pPr.findall(qn('a:lnSpc')): pPr.remove(e)
    ln=pPr.makeelement(qn('a:lnSpc'),{}); sp=ln.makeelement(qn('a:spcPts'),{'val':str(int(pt*100))}); ln.append(sp); pPr.insert(0,ln)
def tbox(s,x,y,w,h,name):
    tb=s.shapes.add_textbox(px(x),px(y),px(w),px(h)); tb.name=name; tf=tb.text_frame
    tf.word_wrap=True; tf.auto_size=MSO_AUTO_SIZE.NONE
    for a in ('margin_left','margin_right','margin_top','margin_bottom'): setattr(tf,a,0)
    return tb,tf
def run(par,text,font,size,color,bold=False):
    r=par.add_run(); r.text=text; r.font.name=font; r.font.size=Pt(size); r.font.color.rgb=color; r.font.bold=bold; return r

p=Presentation('v20.pptx')
blip=qn('a:blip'); emb=qn('r:embed')
def info(s,sh):
    b=next(sh._element.iter(blip),None)
    if b is None: return None
    return Image.open(io.BytesIO(s.part.related_part(b.get(emb)).blob)).size

# ---------- cover ----------
s=p.slides[0]
for sh in list(s.shapes):
    if sh.shape_type==6:
        sz=info(s,sh)
        if sz and sz[0]<900: sh._element.getparent().remove(sh._element)
L=autumn
piece(s,L[2],-95,-120,230,-28,'Leaf top left')
piece(s,L[5],960,-95,170,32,'Leaf top right')
piece(s,L[8],-60,1080,260,-62,'Leaf bottom left')
piece(s,nuts[0],120,1170,130,-15,'Acorn bottom left')
piece(s,cones[3],220,1215,170,8,'Pine cone bottom left')
piece(s,nuts[2%len(nuts)],60,1250,120,25,'Acorn cap bottom left')

# ---------- staff slides ----------
CX,CW,PAD,PORT,GAP=50,980,60,180,40
CB=1300; TB=1118
TW=CW-2*PAD; LOGO_W=130
for si in range(1,10):
    s=p.slides[si]; sh_by=list(s.shapes)
    name=quote=None; portrait=logo=None
    for sh in sh_by:
        if sh.name in('TextBox 28','TextBox 32'): name=sh.text_frame.text.strip()
        if sh.name in('TextBox 29','TextBox 33') and len(sh.text_frame.text)>len(quote or ''): quote=sh.text_frame.text.strip()
    for sh in sh_by:
        sz=info(s,sh) if sh.shape_type==6 else None
        if sh.shape_type==6 and sz==(1000,1000): portrait=sh; continue
        if sh.shape_type==6 and sz and sz[0]<900: sh._element.getparent().remove(sh._element); continue
        if sh.name=='SFW logo': logo=sh; continue
        if sh.name=='Paper card' or sh.has_text_frame: sh._element.getparent().remove(sh._element)
    import json; n=json.load(open('lines.json'))[str(si+1)]; T=n*BODY*1.35/0.75
    CY=TB-T-GAP-PORT-PAD; H=CB-CY
    tree=s.shapes._spTree
    card=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,px(CX),px(CY),px(CW),px(H)); card.name='Card'
    card.fill.solid(); card.fill.fore_color.rgb=CREAM; card.line.fill.background(); card.shadow.inherit=False
    # leaves behind the portrait
    k=si
    piece(s,autumn[k%9],CX-45,CY-55,150,-32,'Leaf 1')
    piece(s,autumn[(k+3)%9],CX+PAD+PORT-80,CY-50,120,24,'Leaf 2')
    piece(s,autumn[(k+6)%9],CX-40,CY+PAD+60,115,-70,'Leaf 3')
    # portrait on top of them
    pe=portrait._element; tree.remove(pe); tree.append(pe)
    portrait.left,portrait.top,portrait.width,portrait.height=px(CX+PAD),px(CY+PAD),px(PORT),px(PORT)
    piece(s,cones[k%len(cones)],CX-40,CY+PAD+PORT-110,80,-12,'Pine cone')
    piece(s,nuts[k%len(nuts)],CX+8,CY+PAD+PORT-48,46,18,'Acorn')
    # name beside the portrait, stacked
    nx=CX+PAD+PORT+35; nw=CX+CW-PAD-nx
    first,last=name.split(' ',1)
    tb,tf=tbox(s,nx,CY+PAD,nw,PORT,'Name'); tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    for i,t in enumerate((first,last)):
        par=tf.paragraphs[0] if i==0 else tf.add_paragraph(); par.alignment=PP_ALIGN.LEFT
        run(par,t,'Montserrat',48,GREEN,True); spacing(par,48*1.2)
    # logo, top right of the card
    le=logo._element; tree.remove(le); tree.append(le)
    # quote, justified
    tb,tf=tbox(s,CX+PAD,CY+PAD+PORT+GAP,TW,T,'Quote')
    for i,para in enumerate(quote.split('\n')):
        par=tf.paragraphs[0] if i==0 else tf.add_paragraph(); par.alignment=PP_ALIGN.JUSTIFY
        run(par,para,'Source Sans 3',BODY,INK); spacing(par,BODY*1.35)
    print(si+1,name,n,'lines card',round(CY),round(H))
p.save('26-11-2026-what-we-are-thankful-for-v22.pptx')
