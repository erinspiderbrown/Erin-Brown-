# 3:4 TikTok grid cover (1080x1440): Boling at 18 (NBC Nightly News, 2019) over Boling at Georgia (Commons, 2020).
# Both crops are native 1:1 pixels (never enlarged), house soft seam, light grade, two words in Anton.
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
W, H, HH = 1080, 1440, 720
top = Image.open('build/nbcf_12.6.png').convert('RGB').crop((800, 30, 1880, 750))
bot = Image.open('ph/c1.jpg').convert('RGB').crop((1560, 240, 2640, 960))
def grade(im, c=1.12, s=1.06): return ImageEnhance.Sharpness(ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(c)).enhance(s)).enhance(1.1)
im = Image.new('RGB', (W, H)); im.paste(grade(top), (0, 0)); im.paste(grade(bot, 1.15), (0, HH))
sh = Image.new('L', (W, 92), 0); d = ImageDraw.Draw(sh)
for y in range(92): d.line([(0, y), (W, y)], fill=int(150 * (1 - abs(y - 46) / 46) ** 2.2))
im.paste((0, 0, 0), (0, HH - 46), sh)
ImageDraw.Draw(im).rectangle([0, HH - 1, W, HH], fill=(200, 200, 200))
v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i*4, i*4, W-i*4, H-i*4], outline=int(100*(1-i/60)))
im.paste((0, 0, 0), (0, 0), v.filter(ImageFilter.GaussianBlur(40)))
f = ImageFont.truetype(F + 'Anton-Regular.ttf', 140); t = 'WHAT HAPPENED?'
tw = ImageDraw.Draw(im).textlength(t, font=f)
txt = Image.new('RGBA', (int(tw) + 80, 300), (0, 0, 0, 0)); ImageDraw.Draw(txt).text((40, 20), t, font=f, fill=(255, 225, 26), stroke_width=12, stroke_fill=(0, 0, 0))
txt = txt.rotate(-3, resample=Image.BICUBIC, expand=True)
s2 = Image.new('RGBA', txt.size, (0, 0, 0, 0)); s2.paste((0, 0, 0, 170), (0, 0), txt.split()[3]); s2 = s2.filter(ImageFilter.GaussianBlur(14))
px = (W - txt.width) // 2; py = H - txt.height - 30
im.paste(s2, (px + 6, py + 12), s2); im.paste(txt, (px, py), txt)
im.save('/home/user/Erin-Brown-/exports/thumbnails/matthew_boling_thumb.jpg', quality=95)
