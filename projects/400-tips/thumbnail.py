# 3:4 TikTok grid cover (1080x1440) from the owner's NCAA photo, native resolution only, light grade, two words.
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'broll/me_ncaa2.jpg'
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
W, H = 1080, 1440
im = Image.open(SRC).convert('RGB')                       # 1728x2160
cw = int(im.height * 3 / 4); x = (im.width - cw) // 2
im = im.crop((x, 0, x + cw, im.height)).resize((W, H), Image.LANCZOS)   # downscale only
im = ImageEnhance.Contrast(im).enhance(1.12); im = ImageEnhance.Color(im).enhance(1.08); im = ImageEnhance.Sharpness(im).enhance(1.15)
v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i*4, i*4, W-i*4, H-i*4], outline=int(110*(1-i/60)))
im.paste((0, 0, 0), (0, 0), v.filter(ImageFilter.GaussianBlur(40)))
f = ImageFont.truetype(F + 'Anton-Regular.ttf', 230); t = '56 → 48'
tw = ImageDraw.Draw(im).textlength(t, font=f)
txt = Image.new('RGBA', (int(tw) + 80, 380), (0, 0, 0, 0)); ImageDraw.Draw(txt).text((40, 20), t, font=f, fill=(255, 225, 26), stroke_width=14, stroke_fill=(0, 0, 0))
txt = txt.rotate(-4, resample=Image.BICUBIC, expand=True)
sh = Image.new('RGBA', txt.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (0, 0), txt.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(14))
px = (W - txt.width) // 2; py = int(H * 0.70)
im.paste(sh, (px + 6, py + 14), sh); im.paste(txt, (px, py), txt)
im.save('/home/user/Erin-Brown-/exports/thumbnails/400_tips_thumb.jpg', quality=95)
