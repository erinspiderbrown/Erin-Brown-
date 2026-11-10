# 3:4 TikTok grid cover (1080x1440), house style like the other covers: one sharp, full-bleed real photo,
# light grade, two words in yellow Anton across the lower third. Photo: Boling sprinting for Georgia (Commons, 3840x2560),
# cropped 1920x2560 and downscaled 0.5625x (never enlarged).
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
W, H = 1080, 1440
im = Image.open('ph/c1.jpg').convert('RGB').crop((1400, 0, 3320, 2560)).resize((W, H), Image.LANCZOS)
im = ImageEnhance.Contrast(im).enhance(1.12); im = ImageEnhance.Color(im).enhance(1.08); im = ImageEnhance.Sharpness(im).enhance(1.15)
v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i*4, i*4, W-i*4, H-i*4], outline=int(110*(1-i/60)))
im.paste((0, 0, 0), (0, 0), v.filter(ImageFilter.GaussianBlur(40)))
f = ImageFont.truetype(F + 'Anton-Regular.ttf', 200); t = 'NEXT BOLT?'
tw = ImageDraw.Draw(im).textlength(t, font=f)
txt = Image.new('RGBA', (int(tw) + 80, 380), (0, 0, 0, 0)); ImageDraw.Draw(txt).text((40, 20), t, font=f, fill=(255, 225, 26), stroke_width=14, stroke_fill=(0, 0, 0))
txt = txt.rotate(-4, resample=Image.BICUBIC, expand=True)
sh = Image.new('RGBA', txt.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (0, 0), txt.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(14))
px = (W - txt.width) // 2; py = int(H * 0.70)
im.paste(sh, (px + 6, py + 14), sh); im.paste(txt, (px, py), txt)
im.save('/home/user/Erin-Brown-/exports/thumbnails/matthew_boling_thumb.jpg', quality=95)
