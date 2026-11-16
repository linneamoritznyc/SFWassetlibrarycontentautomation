import asyncio,pathlib,sys
from playwright.async_api import async_playwright
from PIL import Image
SZ={'o':(816,1056),'k':(816,1056),'c':(816,1056),'e':(816,1056),'d':(816,1056),'s':(1080,1350),'e':(1200,400),'l':(1200,627),'w1':(1600,800),'w2':(1600,300),'b':(1920,120),'p':(816,1056),'r':(672,480)}
def size(p):
    for k,v in SZ.items():
        if p.startswith(k): return v
async def m(ids,out,cols,tw):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        ims=[]
        for i in ids:
            w,h=size(i); pg=await b.new_page(viewport={'width':w,'height':h})
            await pg.goto(pathlib.Path(f'pages/{i}.html').resolve().as_uri()); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'/tmp/k_{i}.png'); await pg.close()
            im=Image.open(f'/tmp/k_{i}.png'); im=im.resize((tw,int(tw*h/w))); ims.append(im)
        await b.close()
    rows=(len(ims)+cols-1)//cols; hh=max(i.height for i in ims)
    c=Image.new('RGB',(cols*tw+(cols-1)*10,rows*hh+(rows-1)*10),'#111')
    for k,im in enumerate(ims): c.paste(im,((k%cols)*(tw+10),(k//cols)*(hh+10)))
    c.save(out)
ids=sys.argv[3:]; asyncio.run(m(ids,sys.argv[1],int(sys.argv[2]),int(sys.argv[2+0]) and 0 or 0) if False else m(ids,sys.argv[1],int(sys.argv[2]),360))
