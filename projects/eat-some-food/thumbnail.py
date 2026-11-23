# TikTok cover in the owner's current style (9:16, 1080x1920): full-bleed real photo, subject cut out and popped in
# front of a big italic two-tone headline, red brush underline, red-ringed circle inset, red arrow.
# v2 cover: official press photos only (no video grabs, no owner): Mary Cain (Sports Illustrated), Allie Ostrander (Women's Running), Marthe Katrine Myhre (owner's race photo).
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
import math
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
W, H = 1080, 1920

from rembg import remove, new_session
SESS = new_session('u2net_human_seg')
def grade(im, c=1.18, s=1.15, b=1.0): return ImageEnhance.Brightness(ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(c)).enhance(s)).enhance(b)
P = Image.open('ph/press/si_cain.jpg').convert('RGB')              # Mary Cain, Sports Illustrated (3000x1688)
SC = 0.62                                                           # downscale only
Ps = P.resize((int(P.width * SC), int(P.height * SC)), Image.LANCZOS)
pm = remove(Ps, session=SESS, only_mask=True).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
bb = pm.point(lambda v: 255 if v > 40 else 0).getbbox()
cxs = (bb[0] + bb[2]) // 2
bgsrc = P.crop((P.width // 2 - 470, 0, P.width // 2 + 470, P.height)).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(18))
bg = grade(bgsrc, 1.05, 0.9, 0.42)
gr = Image.new('L', (W, H), 0); dg = ImageDraw.Draw(gr)
for y in range(H): dg.line([(0, y), (W, y)], fill=int(200 * max(0, (y - 1150) / 770) ** 1.2))
bg.paste((0, 0, 0), (0, 0), gr)
canvas = bg.copy()
def text_img(t, size, fill, stroke=12, grad=None, skew=0.18):
    f = ImageFont.truetype(F + 'Montserrat-Black.ttf', size)
    tw, th = int(f.getlength(t)) + 60, int(size * 1.35)
    m = Image.new('L', (tw, th), 0); ImageDraw.Draw(m).text((30, 0), t, font=f, fill=255)
    s = Image.new('L', (tw, th), 0); ImageDraw.Draw(s).text((30, 0), t, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    body = Image.new('RGBA', (tw, th), fill)
    if grad:
        g = Image.new('RGBA', (tw, th)); dg = ImageDraw.Draw(g)
        for y in range(th):
            k = y / th; dg.line([(0, y), (tw, y)], fill=tuple(int(grad[0][i] * (1 - k) + grad[1][i] * k) for i in range(3)) + (255,))
        body = g
    out = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); out.paste((0, 0, 0, 255), (0, 0), s); out.paste(body, (0, 0), m)
    sh = int(skew * th)
    return out.transform((tw + sh, th), Image.AFFINE, (1, skew, -sh, 0, 1, 0), Image.BICUBIC)

def drop(img, xy, blur=16, off=(8, 14), a=190):
    s = Image.new('RGBA', img.size, (0, 0, 0, 0)); s.paste((0, 0, 0, a), (0, 0), img.split()[3])
    s = s.filter(ImageFilter.GaussianBlur(blur)); canvas.paste(s, (xy[0] + off[0], xy[1] + off[1]), s); canvas.paste(img, xy, img)


ox, oy = W // 2 - cxs, 330
glow = Image.new('L', (W, H), 0); glow.paste(pm.filter(ImageFilter.MaxFilter(25)), (ox, oy))
canvas.paste((232, 35, 30), (0, 0), glow.filter(ImageFilter.GaussianBlur(45)).point(lambda v: int(v * 0.55)))
fb = Image.new('L', pm.size, 255); dfb = ImageDraw.Draw(fb)
for i in range(220): dfb.line([(0, pm.height - 1 - i), (pm.width, pm.height - 1 - i)], fill=int(255 * (i / 220) ** 1.4))
pm2 = ImageChops.multiply(pm, fb)
rim = Image.new('L', (W, H), 0); rim.paste(pm2.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(3)), (ox, oy))
canvas.paste((255, 255, 255), (0, 0), rim.point(lambda v: int(v * 0.5)))
canvas.paste(ImageEnhance.Sharpness(grade(Ps, 1.12, 1.08, 1.12)).enhance(1.25), (ox, oy), pm2)
def inset(path, box, cx, cy, R, label):
    fr = Image.open(path).convert('RGB').crop(box); fr = grade(fr.resize((2 * R, 2 * R), Image.LANCZOS), 1.1, 1.08)
    cm = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(cm).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=200)
    canvas.paste((232, 35, 30), (0, 0), g.filter(ImageFilter.GaussianBlur(28)))
    dc = ImageDraw.Draw(canvas)
    dc.ellipse([cx - R - 20, cy - R - 20, cx + R + 20, cy + R + 20], fill=(232, 35, 30))
    dc.ellipse([cx - R - 7, cy - R - 7, cx + R + 7, cy + R + 7], fill=(255, 255, 255))
    canvas.paste(fr, (cx - R, cy - R), cm)
    tag = text_img(label, 40, (255, 255, 255, 255), stroke=8, skew=0.15)
    tb = Image.new('RGBA', (tag.width + 36, tag.height + 4), (232, 35, 30, 255)); tb.paste(tag, (18, 3), tag)
    tb = tb.transform(tb.size, Image.AFFINE, (1, 0.12, -12, 0, 1, 0), Image.BICUBIC)
    drop(tb, (cx - tb.width // 2, cy + R - 14), blur=10, off=(5, 8))
inset('ph/press/wr_allie.jpg', (180, 60, 820, 700), 205, 250, 135, '3× NCAA CHAMP')
inset('raw/ph1.jpg', (820, 90, 1300, 570), 900, 250, 135, 'DIED AT 39')
l1 = text_img('FASTEST GIRL IN AMERICA', 64, None, grad=((255, 255, 255), (205, 208, 214)))
l2 = text_img('5 BROKEN BONES', 102, None, stroke=14, grad=((255, 243, 120), (255, 190, 0)))
import random
rnd = random.Random(4)
br = Image.new('RGBA', (1000, 140), (0, 0, 0, 0)); db = ImageDraw.Draw(br)
N = 60; up, dn = [], []
for i in range(N + 1):
    x = 20 + 960 * i / N; k = i / N
    th = 14 + 62 * math.sin(math.pi * min(1, k * 1.15)) ** 0.7
    yc = 88 - 34 * k
    up.append((x, yc - th / 2 + rnd.uniform(-2.5, 2.5))); dn.append((x, yc + th / 2 + rnd.uniform(-2.5, 2.5)))
db.polygon(up + dn[::-1], fill=(232, 35, 30, 255))
br = br.filter(ImageFilter.GaussianBlur(0.6))
canvas.paste(br, (40, 1640), br)
drop(l1, ((W - l1.width) // 2, 1430))
drop(l2, ((W - l2.width) // 2 - 10, 1530))
v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i * 4, i * 4, W - i * 4, H - i * 4], outline=int(90 * (1 - i / 60)))
canvas.paste((0, 0, 0), (0, 0), v.filter(ImageFilter.GaussianBlur(40)))
out = '/home/user/Erin-Brown-/exports/thumbnails/eat_some_food_thumb'
canvas.save(out + '.jpg', quality=95)
canvas.crop((0, 240, W, 240 + 1440)).save(out + '_3x4.jpg', quality=95)
