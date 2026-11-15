from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S='/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
F='/home/user/Erin-Brown-/editor/assets/fonts/'
W,H=1080,1440; HALF=720   # TikTok profile-grid cover is 3:4
def crop_at(path,cx,cy,scale=1.0,w=W,h=HALF,bright=1.0):
    im=Image.open(path).convert('RGB')
    if scale!=1.0: im=im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS); cx*=scale; cy*=scale
    x=int(min(max(cx-w/2,0),im.width-w)); y=int(min(max(cy-h/2,0),im.height-h))
    im=im.crop((x,y,x+w,y+h)); im=ImageEnhance.Brightness(im).enhance(bright)
    im=ImageEnhance.Contrast(im).enhance(1.12); im=ImageEnhance.Color(im).enhance(1.08); return ImageEnhance.Sharpness(im).enhance(1.15)
top=crop_at(f'{S}/raw4/ph/tebogo_press.jpg',930,930,0.85)
bot=crop_at(f'{S}/raw4/ph/lyles_paris_b.jpg',1050,820,0.62,bright=1.07)
c=Image.new('RGB',(W,H)); c.paste(top,(0,0)); c.paste(bot,(0,HALF))
sh=Image.new('L',(W,140),0); d=ImageDraw.Draw(sh)
for y in range(140): d.line([(0,y),(W,y)],fill=int(150*(1-abs(y-70)/70)**2.2))
c.paste((0,0,0),(0,HALF-70),sh); ImageDraw.Draw(c).rectangle([0,HALF-1,W,HALF],fill=(200,200,200))
v=Image.new('L',(W,H),0); dv=ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i*4,i*4,W-i*4,H-i*4],outline=int(110*(1-i/60)))
c.paste((0,0,0),(0,0),v.filter(ImageFilter.GaussianBlur(40)))
f=ImageFont.truetype(F+'Anton-Regular.ttf',170); t='OPOSSUM?'
tw=ImageDraw.Draw(c).textlength(t,font=f)
txt=Image.new('RGBA',(int(tw)+80,300),(0,0,0,0)); ImageDraw.Draw(txt).text((40,20),t,font=f,fill=(255,225,26),stroke_width=12,stroke_fill=(0,0,0))
txt=txt.rotate(-4,resample=Image.BICUBIC,expand=True)
shadow=Image.new('RGBA',txt.size,(0,0,0,0)); shadow.paste((0,0,0,170),(0,0),txt.split()[3]); shadow=shadow.filter(ImageFilter.GaussianBlur(14))
px=(W-txt.width)//2; py=HALF-txt.height//2-10
c.paste(shadow,(px+6,py+14),shadow); c.paste(txt,(px,py),txt)
c.save('/home/user/Erin-Brown-/exports/thumbnails/tebogo_lyles_thumb.jpg',quality=95)
