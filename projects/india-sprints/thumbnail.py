# TikTok cover in the owner's current style (9:16 + 3:4 crop). Real frames only, never enlarged:
# the owner's 4K take (frame at 57.5 s, 0.6x) cut out with rembg, over the India flag-map scene (0.5x),
# two-tone slanted headline + red brush, ringed inset of Botswana (map scene) with a red tag.
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from rembg import remove, new_session
F = '/home/user/Erin-Brown-/editor/assets/fonts/'; W, H = 1080, 1920
bg = Image.open('geo/map_in_v2.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
bg = ImageEnhance.Brightness(bg).enhance(0.85)
canvas = Image.new('RGB', (W, H)); canvas.paste(bg, (0, -150)); canvas.paste(bg.crop((0, H - 160, W, H)), (0, H - 160))
fr = Image.open('work/thumb_frame.png').convert('RGB').crop((560, 120, 3280, 2160))      # 2720x2040
mask = remove(fr, session=new_session('u2net_human_seg'), only_mask=True)
sc = 0.5; fr = fr.resize((int(fr.width * sc), int(fr.height * sc)), Image.LANCZOS); mask = mask.resize(fr.size, Image.LANCZOS)
fr = ImageEnhance.Sharpness(ImageEnhance.Color(ImageEnhance.Contrast(fr).enhance(1.15)).enhance(1.1)).enhance(1.25)
px, py = (W - fr.width) // 2 + 70, H - fr.height
rim = Image.new('L', (W, H), 0); rim.paste(mask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(5)), (px, py))
canvas.paste((255, 255, 255), (0, 0), rim.point(lambda v: int(v * 0.3)))
canvas.paste(fr, (px, py), mask.filter(ImageFilter.GaussianBlur(1)))
def text_img(t, size, grad, stroke=12, skew=0.18):
    f = ImageFont.truetype(F + 'Montserrat-Black.ttf', size); tw, th = int(f.getlength(t)) + 60, int(size * 1.35)
    m = Image.new('L', (tw, th), 0); ImageDraw.Draw(m).text((30, 0), t, font=f, fill=255)
    s = Image.new('L', (tw, th), 0); ImageDraw.Draw(s).text((30, 0), t, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    g = Image.new('RGBA', (tw, th)); dg = ImageDraw.Draw(g)
    for y in range(th):
        k = y / th; dg.line([(0, y), (tw, y)], fill=tuple(int(grad[0][i] * (1 - k) + grad[1][i] * k) for i in range(3)) + (255,))
    out = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); out.paste((0, 0, 0, 255), (0, 0), s); out.paste(g, (0, 0), m)
    sh = int(skew * th); return out.transform((tw + sh, th), Image.AFFINE, (1, skew, -sh, 0, 1, 0), Image.BICUBIC)
def drop(img, xy, blur=16, off=(8, 14), a=190):
    s = Image.new('RGBA', img.size, (0, 0, 0, 0)); s.paste((0, 0, 0, a), (0, 0), img.split()[3])
    s = s.filter(ImageFilter.GaussianBlur(blur)); canvas.paste(s, (xy[0] + off[0], xy[1] + off[1]), s); canvas.paste(img, xy, img)
l1 = text_img('1.4 BILLION', 140, ((255, 255, 255), (205, 208, 214)))
l2 = text_img('NO SPRINTERS?', 116, ((255, 243, 120), (255, 190, 0)), stroke=14)
rnd = random.Random(4); br = Image.new('RGBA', (1000, 140), (0, 0, 0, 0)); db = ImageDraw.Draw(br); up, dn = [], []
for i in range(61):
    x = 20 + 960 * i / 60; k = i / 60; th = 14 + 62 * math.sin(math.pi * min(1, k * 1.15)) ** 0.7; yc = 88 - 34 * k
    up.append((x, yc - th / 2 + rnd.uniform(-2.5, 2.5))); dn.append((x, yc + th / 2 + rnd.uniform(-2.5, 2.5)))
db.polygon(up + dn[::-1], fill=(232, 35, 30, 255)); br = br.filter(ImageFilter.GaussianBlur(0.6))
canvas.paste(br, (40, 405), br)
drop(l1, ((W - l1.width) // 2, 120)); drop(l2, ((W - l2.width) // 2 - 6, 280))
# ringed inset: Botswana, tagged
R = 140; cx, cy = 185, 1180
ins = Image.open('geo/map_bw.jpg').convert('RGB').crop((180, 800, 1980, 2600)).resize((2 * R, 2 * R), Image.LANCZOS)
cm = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(cm).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([cx - R - 26, cy - R - 26, cx + R + 26, cy + R + 26], fill=200)
canvas.paste((232, 35, 30), (0, 0), glow.filter(ImageFilter.GaussianBlur(24)))
dc = ImageDraw.Draw(canvas); dc.ellipse([cx - R - 18, cy - R - 18, cx + R + 18, cy + R + 18], fill=(232, 35, 30)); dc.ellipse([cx - R - 7, cy - R - 7, cx + R + 7, cy + R + 7], fill=(255, 255, 255))
canvas.paste(ins, (cx - R, cy - R), cm)
tag = text_img('BOTSWANA 2.5M', 46, ((255, 255, 255), (255, 255, 255)), stroke=7, skew=0.15)
tb = Image.new('RGBA', (tag.width + 30, tag.height + 6), (232, 35, 30, 255)); tb.paste(tag, (15, 4), tag)
drop(tb, (max(10, cx - tb.width // 2), cy + R - 10), blur=10, off=(5, 8))
v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i * 4, i * 4, W - i * 4, H - i * 4], outline=int(90 * (1 - i / 60)))
canvas.paste((0, 0, 0), (0, 0), v.filter(ImageFilter.GaussianBlur(40)))
out = '/home/user/Erin-Brown-/exports/thumbnails/india_sprints_thumb'
canvas.save(out + '.jpg', quality=95); canvas.crop((0, 240, W, 240 + 1440)).save(out + '_3x4.jpg', quality=95)
