import asyncio, pathlib, json, io
from playwright.async_api import async_playwright
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement
PX=9525; SC=2
JS=r'''
() => {
 const pg=document.body.firstElementChild && document.querySelector('.pg') || document.querySelector('body > div');
 const root=pg; const R=root.getBoundingClientRect();
 const inl=new Set(['SPAN','B','STRONG','I','EM','BR','A','SMALL']);
 const out=[]; let id=0;
 function isTextBox(e){
   if(e.tagName==='svg'||e.closest('svg')) return false;
   let hasText=false;
   for(const n of e.childNodes){
     if(n.nodeType===3 && n.textContent.trim()) hasText=true;
     if(n.nodeType===1 && !inl.has(n.tagName)) return false;
   }
   if(!hasText){ // spans only?
     for(const n of e.childNodes){ if(n.nodeType===1 && n.textContent.trim()) hasText=true; }
     if(!hasText) return false;
     for(const n of e.childNodes){ if(n.nodeType===1 && !inl.has(n.tagName)) return false; }
   }
   return true;
 }
 root.querySelectorAll('ol').forEach(ol=>{[...ol.children].forEach((li,i)=>{li.insertBefore(document.createTextNode((i+1)+'. '),li.firstChild);}); ol.style.listStyle='none';});
 // wrap loose inline runs inside mixed block containers so they become their own text boxes
 [...root.querySelectorAll('*')].forEach(el=>{
   if(el.closest('svg')||el.closest('table')) return;
   const kids=[...el.childNodes];
   const hasBlock=kids.some(n=>n.nodeType===1&&!inl.has(n.tagName));
   const hasText=kids.some(n=>n.nodeType===3&&n.textContent.trim());
   if(!hasBlock||!hasText) return;
   let run=[];
   const flush=()=>{ if(run.some(n=>(n.nodeType===3&&n.textContent.trim())||(n.nodeType===1&&n.tagName!=='BR'))){ const w=document.createElement('div'); run[0].parentNode.insertBefore(w,run[0]); run.forEach(n=>w.appendChild(n)); } run=[]; };
   for(const n of kids){ if(n.nodeType===3||(n.nodeType===1&&inl.has(n.tagName))) run.push(n); else flush(); }
   flush();
 });
 const tables=[...root.querySelectorAll('table')].map(tb=>{const r=tb.getBoundingClientRect();const rows=[...tb.rows].map(tr=>[...tr.cells].map(td=>{const c=getComputedStyle(td);const cr=td.getBoundingClientRect();const sp=td.querySelector('span,div');const sc=sp?getComputedStyle(sp):c;return {lh:parseFloat(sc.lineHeight)||parseFloat(c.lineHeight)||parseFloat(c.fontSize)*1.3,pt:parseFloat(c.paddingTop),pb:parseFloat(c.paddingBottom),pr:parseFloat(c.paddingRight),pl:parseFloat(c.paddingLeft),t:td.innerText.trim(),w:cr.width,h:cr.height,color:sc.color,bw:sc.fontWeight,size:parseFloat(c.fontSize),fam:c.fontFamily,tt:c.textTransform,align:(sp&&sp.style.textAlign)||c.textAlign,th:td.tagName==='TH'}}));tb.querySelectorAll('*').forEach(e=>e.setAttribute('data-tb','1'));return {x:r.left-R.left,y:r.top-R.top,w:r.width,rows};});
 const all=[...root.querySelectorAll('*')].filter(e=>!e.closest('table'));
 const boxes=[];
 for(const e of all){
   if(!isTextBox(e)) continue;
   if(boxes.some(b=>b.contains(e))) continue;
   boxes.push(e);
 }
 for(const e of boxes){
   const r=e.getBoundingClientRect(); const cs=getComputedStyle(e);
   const runs=[];
   function walk(node,inh){
     for(const n of node.childNodes){
       if(n.nodeType===3){ let t=n.textContent.replace(/\s+/g,' '); if(t) runs.push({t, ...inh}); }
       else if(n.tagName==='BR') runs.push({t:'\n',...inh});
       else if(n.nodeType===1){ const c=getComputedStyle(n); walk(n,{color:c.color,w:c.fontWeight,size:parseFloat(c.fontSize),fam:c.fontFamily,tt:c.textTransform}); }
     }
   }
   walk(e,{color:cs.color,w:cs.fontWeight,size:parseFloat(cs.fontSize),fam:cs.fontFamily,tt:cs.textTransform});
   // mark rendered line breaks with \u000b
   {
     const lhpx=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.3;
     let lastY=null; let nlines=1; const brk=new Map(); let ti=0;
     const tw=document.createTreeWalker(e,NodeFilter.SHOW_TEXT|NodeFilter.SHOW_ELEMENT);
     const order=[]; let n;
     while(n=tw.nextNode()){ if(n.nodeType===1){ if(n.tagName==='BR'){lastY=null;} continue;} 
       const t=n.textContent; const rg=document.createRange();
       for(let k=0;k<t.length;k++){ if(/\s/.test(t[k])) continue; rg.setStart(n,k); rg.setEnd(n,k+1); const rr=rg.getBoundingClientRect(); if(!rr.height) continue;
         if(lastY!==null && rr.top>lastY+lhpx*0.5){ brk.set(n,(brk.get(n)||[]).concat([k])); nlines++; }
         if(lastY===null || rr.top>lastY+lhpx*0.5) lastY=rr.top; }
     }
     // rebuild runs with markers
     runs.length=0;
     function walk2(node,inh){
       for(const m of node.childNodes){
         if(m.nodeType===3){ let t=m.textContent; const ks=(brk.get(m)||[]).slice().sort((a,b)=>b-a); for(const k of ks){ let j=k; while(j>0 && /\s/.test(t[j-1])) j--; t=t.slice(0,j)+'\u000b'+t.slice(k);} t=t.replace(/[ \t\n\r]+/g,' '); if(t) runs.push({t,...inh}); }
         else if(m.tagName==='BR') runs.push({t:'\n',...inh});
         else if(m.nodeType===1){ const c=getComputedStyle(m); walk2(m,{color:c.color,w:c.fontWeight,size:parseFloat(c.fontSize),fam:c.fontFamily,tt:c.textTransform}); }
       }
     }
     walk2(e,{color:cs.color,w:cs.fontWeight,size:parseFloat(cs.fontSize),fam:cs.fontFamily,tt:cs.textTransform});
     e._nlines=nlines;
   }
   // tables cells / columns
   // available slack to the right
   let cap=R.width-56;
   for(let a=e.parentElement;a&&a!==root;a=a.parentElement){const ac=getComputedStyle(a);const ar=a.getBoundingClientRect(); if(ac.backgroundColor!=='rgba(0, 0, 0, 0)'||ac.backgroundImage!=='none'||ac.borderRadius!=='0px'){cap=Math.min(cap,ar.right-R.left-parseFloat(ac.paddingRight)); break;}}
   const pl=parseFloat(cs.paddingLeft)+parseFloat(cs.borderLeftWidth),pr=parseFloat(cs.paddingRight)+parseFloat(cs.borderRightWidth),pt=parseFloat(cs.paddingTop)+parseFloat(cs.borderTopWidth),pb=parseFloat(cs.paddingBottom);
   out.push({_el:null,ex:e,nl:e._nlines,cap,x:r.left-R.left+pl,y:r.top-R.top+pt,w:r.width-pl-pr,h:r.height-pt-pb,align:cs.textAlign,lh:parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.3,runs,cols:parseInt(cs.columnCount)||1});
   e.setAttribute('data-tb','1');
 }
 const imgRects=[...root.querySelectorAll('img')].map(i=>{const r=i.getBoundingClientRect();return {x:r.left-R.left,y:r.top-R.top,w:r.width,h:r.height};});
 const tabR=tables.map(t=>({x:t.x,y:t.y,w:t.w,h:2000}));
 for(const o of out){ let cap=o.cap; const obs=out.filter(p=>p!==o).concat(imgRects);
   for(const p of obs){ if(p.x>=o.x+o.w-1 && p.y<o.y+o.h && p.y+p.h>o.y) cap=Math.min(cap,p.x-28); }
   o.slack=Math.max(0,cap-(o.x+o.w)); delete o.ex; delete o._el; }
 const imgs=[...root.querySelectorAll('img')].map(i=>{const r=i.getBoundingClientRect();return {x:r.left-R.left,y:r.top-R.top,w:r.width,h:r.height,alt:i.alt||'',rad:parseFloat(getComputedStyle(i).borderTopLeftRadius)||0,radb:parseFloat(getComputedStyle(i).borderBottomLeftRadius)||0};});
 return {texts:out,imgs,tables};
}
'''
def rgb(s):
    import re
    v=[float(x) for x in re.findall(r'[\d.]+',s)]
    return RGBColor(int(v[0]),int(v[1]),int(v[2]))
async def build(name,pages,W=816,Hh=1056):
    prs=Presentation(); prs.slide_width=Emu(W*PX); prs.slide_height=Emu(Hh*PX)
    blank=prs.slide_layouts[6]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox","--allow-file-access-from-files"])
        pg=await b.new_page(viewport={'width':W,'height':Hh},device_scale_factor=SC)
        for f in pages:
            await pg.goto(pathlib.Path(f'/home/claude/kit/pages/{f}.html').resolve().as_uri()); await pg.wait_for_timeout(500)
            data=await pg.evaluate(JS)
            await pg.add_style_tag(content='[data-tb], [data-tb] *{color:transparent !important} table, table *{border-color:transparent !important}')
            A=Image.open(io.BytesIO(await pg.screenshot(clip={'x':0,'y':0,'width':W,'height':Hh})))
            # ---- decor layers, each its own transparent picture ----
            ndec=await pg.evaluate(r"""()=>{
              const root=document.querySelector('.pg')||document.querySelector('body > div');
              const all=[...root.querySelectorAll('*')]; let n=0; const order=new Map(); all.forEach((e,i)=>order.set(e,i));
              document.querySelectorAll('img').forEach(e=>e.setAttribute('data-ord',order.get(e)));
              for(const e of all){
                if(e.closest('table')) continue;
                const svgShape=e.closest('svg') && ['path','rect','circle','ellipse','polygon','line','polyline'].includes(e.tagName.toLowerCase()) && !e.closest('defs');
                const cs=getComputedStyle(e); const bf=getComputedStyle(e,'::before');
                const paints=e.tagName==='IMG' || svgShape || (!e.closest('svg') && (
                  (cs.backgroundColor!=='rgba(0, 0, 0, 0)') || cs.backgroundImage!=='none' ||
                  (parseFloat(cs.borderTopWidth)+parseFloat(cs.borderBottomWidth)+parseFloat(cs.borderLeftWidth)+parseFloat(cs.borderRightWidth)>0 && cs.borderTopColor!=='rgba(0, 0, 0, 0)') ||
                  cs.boxShadow!=='none' || (bf.content && bf.content!=='none' && bf.content!=='normal')));
                if(paints){ e.setAttribute('data-dec',n); e.setAttribute('data-ord',order.get(e)); n++; }
              }
              root.setAttribute('data-root','1');
              return n;}""")
            await pg.add_style_tag(content='*{visibility:hidden !important}')
            # base: page root background only
            await pg.add_style_tag(content='[data-root]{visibility:visible !important}')
            Bg=Image.open(io.BytesIO(await pg.screenshot(clip={'x':0,'y':0,'width':W,'height':Hh})))
            await pg.evaluate("()=>{const r=document.querySelector('[data-root]'); r.dataset.bgsave=r.style.background; r.style.setProperty('background','transparent','important'); r.style.setProperty('background-image','none','important');}")
            layers=[]
            for k in range(ndec):
                h=await pg.add_style_tag(content=f'[data-dec="{k}"]{{visibility:visible !important}}')
                L=Image.open(io.BytesIO(await pg.screenshot(clip={'x':0,'y':0,'width':W,'height':Hh},omit_background=True))).convert('RGBA')
                await h.evaluate('e=>e.remove()')
                bb=L.getchannel('A').getbbox()
                if bb:
                    o=await pg.evaluate(f'()=>{{const e=document.querySelector(\'[data-dec="{k}"]\');return [+e.getAttribute("data-ord"),e.tagName,(e.getAttribute("alt")||"")]}}')
                    layers.append((o[0],'dec',L.crop(bb),bb,o[1],o[2]))
            imgords=await pg.evaluate("()=>[...document.querySelectorAll('img')].map(e=>+e.getAttribute('data-ord'))")
            s=prs.slides.add_slide(blank)
            bio=io.BytesIO(); Bg.convert('RGB').save(bio,'PNG'); bio.seek(0)
            bgp=s.shapes.add_picture(bio,0,0,Emu(W*PX),Emu(Hh*PX)); bgp.name='Background'
            items=list(layers)
            items.sort(key=lambda t:t[0])
            for it in items:
                if it[1]=='dec':
                    _,_,crop,bb,tag,alt=it
                    bio=io.BytesIO(); crop.save(bio,'PNG'); bio.seek(0)
                    sh=s.shapes.add_picture(bio,Emu(int(bb[0]/SC*PX)),Emu(int(bb[1]/SC*PX)),Emu(int((bb[2]-bb[0])/SC*PX)),Emu(int((bb[3]-bb[1])/SC*PX)))
                    sh.name=(alt[:60] if tag=='IMG' else {'path':'Wave','DIV':'Shape','LI':'Bullet'}.get(tag,'Shape'))
                    continue
                k=it[2]; im=data['imgs'][k]
                x0=max(0,im['x']);y0=max(0,im['y']);x1=min(W,im['x']+im['w']);y1=min(Hh,im['y']+im['h'])
                if x1-x0<2 or y1-y0<2: continue
                c=A.crop((int(x0*SC),int(y0*SC),int(x1*SC),int(y1*SC)))
                if im.get('rad') or im.get('radb'):
                    from PIL import ImageDraw
                    mk=Image.new('L',c.size,0); dr=ImageDraw.Draw(mk)
                    rt=int(im['rad']*SC); rb=int(im['radb']*SC); w_,h_=c.size
                    rr=max(rt,rb)
                    dr.rounded_rectangle((0,0,w_-1,h_-1),radius=rr,fill=255)
                    if rt!=rb:
                        if rt<rb: dr.rectangle((0,0,w_-1,h_//2),fill=255)
                        else: dr.rectangle((0,h_//2,w_-1,h_-1),fill=255)
                    c=c.convert('RGBA'); c.putalpha(mk)
                bio=io.BytesIO(); c.save(bio,'PNG'); bio.seek(0)
                sh=s.shapes.add_picture(bio,Emu(int(x0*PX)),Emu(int(y0*PX)),Emu(int((x1-x0)*PX)),Emu(int((y1-y0)*PX)))
                sh.name=(im['alt'] or f'Image {k+1}')[:60]
            for T in data.get('tables',[]):
                rows=T['rows']; nr=len(rows); nc=max(len(r) for r in rows)
                gf=s.shapes.add_table(nr,nc,Emu(int(T['x']*PX)),Emu(int(T['y']*PX)),Emu(int(T['w']*PX)),Emu(int(sum(r[0]['h'] for r in rows)*PX)))
                gf.name='Table'
                tbl=gf.table
                tblPr=tbl._tbl.tblPr
                for a in ('firstRow','bandRow'): tblPr.set(a,'0')
                sid=tblPr.find(qn('a:tableStyleId'))
                if sid is not None: sid.text='{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
                for j,cell in enumerate(rows[0]): tbl.columns[j].width=Emu(int(cell['w']*PX))
                for i,row in enumerate(rows):
                    tbl.rows[i].height=Emu(int(min(c['h'] for c in row)*PX*0.6))
                    for j,cd in enumerate(row):
                        cell=tbl.cell(i,j); cell.fill.background()
                        cell.margin_left=Emu(int(cd['pl']*PX)); cell.margin_right=Emu(int(max(0,cd['pr']-4)*PX)); cell.margin_top=Emu(int(cd['pt']*PX)); cell.margin_bottom=Emu(int(max(0,cd['pb']-1)*PX))
                        tf=cell.text_frame; tf.word_wrap=True
                        lines=cd['t'].split('\n')
                        for k,ln in enumerate(lines):
                            para=tf.paragraphs[0] if k==0 else tf.add_paragraph()
                            para.alignment=PP_ALIGN.RIGHT if cd['align'] in ('right','end') else PP_ALIGN.LEFT
                            para.line_spacing=Pt(cd['lh']*0.75)
                            r=para.add_run(); r.text=ln.upper() if cd['tt']=='uppercase' else ln
                            f=r.font; f.size=Pt(round(cd['size']*0.75*(1 if 'Montserrat' in cd['fam'] else 0.93)*2)/2); f.bold=cd['th'] or (k==0 and int(float(cd['bw']))>=600)
                            f.color.rgb=rgb(cd['color']); f.name='Montserrat' if 'Montserrat' in cd['fam'] else 'Source Sans 3'
                        tcPr=cell._tc.get_or_add_tcPr()
                        for tag in ('a:lnL','a:lnR','a:lnT','a:lnB'):
                            ln=OxmlElement(tag)
                            if tag=='a:lnB':
                                ln.set('w',str(int((2 if i==0 else 1)*PX)))
                                sf=OxmlElement('a:solidFill'); c=OxmlElement('a:srgbClr'); c.set('val','4F3433' if i==0 else 'DDD5C6'); sf.append(c); ln.append(sf)
                            else:
                                ln.set('w','0'); ln.append(OxmlElement('a:noFill'))
                            tcPr.append(ln)
            for t in data['texts']:
                al0=t['align']; want=t['w']*0.22+6
                head=all('Montserrat' in r['fam'] for r in t['runs'] if r['t'].strip())
                single=t['nl']<=1 and not any('\n' in r['t'] for r in t['runs'])
                if single:
                    if al0 in ('right','end'): ex=min(want,max(0,t['x']-40)); bx=t['x']-ex; bw=t['w']+ex
                    elif al0=='center': ex=min(want,24); bx=t['x']-ex/2; bw=t['w']+ex
                    else: ex=min(want,max(0,W-40-(t['x']+t['w']))); bx=t['x']; bw=t['w']+ex
                elif head:
                    ex=max(6,min(want,t['slack'])) if al0 not in ('right','end','center') else 6
                    bx=t['x'] if al0 not in ('right','end','center') else t['x']-3; bw=t['w']+ex
                elif al0=='center':
                    for r in t['runs']: r['t']=r['t'].replace('\u000b',' ')
                    bx=t['x']-2; bw=t['w']+4
                else:
                    for r in t['runs']: r['t']=r['t'].replace('\u000b',' ')
                    ex=max(4,min(t['slack'],t['w']*0.08+4)) if al0 not in ('right','end') else 6
                    bx=t['x'] if al0 not in ('right','end') else t['x']-3; bw=t['w']+ex
                t['bx']=bx; t['bw']=bw
            groups=[]
            for t in sorted(data['texts'],key=lambda q:(q['y'],q['x'])):
                g=None
                for G in groups:
                    L=G[-1]; gap=t['y']-(L['y']+L['h'])
                    if abs(L['x']-t['x'])<3 and L['align']==t['align'] and -1<=gap<=24 and abs(L['w']-t['w'])<0.6*max(L['w'],t['w']) and not any(im['x']<t['x']+t['w'] and im['x']+im['w']>t['x'] and im['y']<t['y'] and im['y']+im['h']>L['y']+L['h'] for im in data['imgs']):
                        g=G; break
                if g is not None: t['gap']=max(0,t['y']-(g[-1]['y']+g[-1]['h'])); g.append(t)
                else: t['gap']=0; groups.append([t])
            for G in groups:
                f0=G[0]; bx=f0['bx']; bw=min(q['bw'] for q in G); bw=max(bw,max(q['w'] for q in G)+4)
                hh=G[-1]['y']+G[-1]['h']-f0['y']
                tb=s.shapes.add_textbox(Emu(int(bx*PX)),Emu(int(f0['y']*PX)),Emu(int(bw*PX)),Emu(int(hh*PX)))
                tf=tb.text_frame; tf.word_wrap=True
                tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
                tf.vertical_anchor=MSO_ANCHOR.TOP
                txt_all=''
                for gi,t in enumerate(G):
                    para=tf.paragraphs[0] if gi==0 else tf.add_paragraph()
                    al={'center':PP_ALIGN.CENTER,'right':PP_ALIGN.RIGHT,'end':PP_ALIGN.RIGHT,'justify':PP_ALIGN.JUSTIFY}.get(t['align'],PP_ALIGN.LEFT)
                    para.alignment=al
                    if gi>0: para.space_before=Pt(t['gap']*0.75)
                    paras=[para]
                    first=True
                    for r in t['runs']:
                        parts=r['t'].split('\n')
                        for i,ptxt in enumerate(parts):
                            if i>0:
                                para=tf.add_paragraph(); para.alignment=al; paras.append(para)
                            if first: ptxt=ptxt.lstrip()
                            if not ptxt: continue
                            first=False
                            if r['tt']=='uppercase': ptxt=ptxt.upper()
                            segs=ptxt.split('\u000b')
                            for si,seg in enumerate(segs):
                                if si>0: para.add_line_break()
                                if not seg: continue
                                run=para.add_run(); run.text=seg; txt_all+=seg+' '
                                fnt=run.font; fnt.size=Pt(round(r['size']*0.75*(1 if 'Montserrat' in r['fam'] else 0.93)*2)/2); fnt.bold=int(float(r['w']))>=600
                                fnt.color.rgb=rgb(r['color'])
                                fnt.name='Montserrat' if 'Montserrat' in r['fam'] else 'Source Sans 3'
                    for pp in paras: pp.line_spacing=Pt(t['lh']*0.75)
                tb.name=(txt_all.strip()[:40] or 'Text')
        await b.close()
    prs.save(f"/home/claude/kit/out/{name}.pptx"); print("saved",name,len(prs.slides))
import sys
DECKS={
 'SFW Year-End 2026 - Mailer Letter':(['p1'],816,1056),
 'SFW Year-End 2026 - Reply Card (7x5 in)':(['r1'],672,480),
 'SFW Year-End 2026 - Social Posts':(['s01','s02','s03','s04','s05','s06','s07','s08','s09','s10','s11'],1080,1350),
 'SFW Year-End 2026 - Email Headers':(['e1','e2','e3','e4','e5','e6','e7','e8'],1200,400),
 'SFW Year-End 2026 - Board LinkedIn Images':(['l1','l2','l3'],1200,627),
 'SFW Year-End 2026 - Giving Tuesday Page Hero':(['w1'],1600,800),
 'SFW Year-End 2026 - Progress Bar':(['w2'],1600,300),
 'SFW Year-End 2026 - Site Banners':(['b1','b2','b3'],1920,120),
}
async def main():
    only=sys.argv[1:]
    for n,(pgs,w,h) in DECKS.items():
        if only and not any(o in n for o in only): continue
        await build(n,pgs,w,h)
asyncio.run(main())
