# TikTok cover in the owner's current style (9:16, 1080x1920): full-bleed real photo, subject cut out and popped in
# front of a big italic two-tone headline, red brush underline, red-ringed circle inset, red arrow.
# YouTube cover: no news-frame inset (news footage is TikTok-only).
# Real frames only: the owner's 4K take, a Pexels 4K cash shot, Livvy Dunne at the ESPYs (Veuer). Cutout: rembg u2net_human_seg.
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
import math
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
W, H = 1080, 1920
BOX = (1350, 0, 2565, 2160)                     # 4K frame of the owner (raw take, 31.4 s), downscaled 0.89x
src = Image.open('ph/f_31.4.png').convert('RGB').crop(BOX).resize((W, H), Image.LANCZOS)
from rembg import remove, new_session
mask = remove(Image.open('ph/f_31.4.png').convert('RGB').crop(BOX), session=new_session('u2net_human_seg'), only_mask=True).resize((W, H), Image.LANCZOS)
cash = Image.open('ph/cash.png').convert('RGB').resize((W, H), Image.LANCZOS)   # Pexels 4K (Tima Miroshnichenko), downscaled
mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))

def grade(im, c=1.18, s=1.15, b=1.0): return ImageEnhance.Brightness(ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(c)).enhance(s)).enhance(b)
bg = grade(cash.filter(ImageFilter.GaussianBlur(6)), 1.1, 1.05, 0.55)          # cash background, pushed back
subj = ImageEnhance.Sharpness(grade(src, 1.15, 1.12, 1.18)).enhance(1.3)       # subject punchy and crisp
# top darkening for the headline
gr = Image.new('L', (W, H), 0); d = ImageDraw.Draw(gr)
for y in range(1050, H): d.line([(0, y), (W, y)], fill=int(170 * ((y - 1050) / (H - 1050)) ** 1.3))
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

# subject: soft rim only (no halo)
SC = 0.85                                         # subject smaller so the cash background and headline breathe
sw, sh = int(W * SC), int(H * SC)
subj_s, mask_s = subj.resize((sw, sh), Image.LANCZOS), mask.resize((sw, sh), Image.LANCZOS)
ox, oy = (W - sw) // 2, H - sh - 100
fade = Image.new('L', (sw, sh), 255); df = ImageDraw.Draw(fade)          # shoulders are cut by the source frame: fade those edges out
for i in range(160):
    v = int(255 * (i / 160) ** 1.5); df.line([(i, 0), (i, sh)], fill=v); df.line([(sw - 1 - i, 0), (sw - 1 - i, sh)], fill=v)
fb = Image.new('L', (sw, sh), 255); dfb = ImageDraw.Draw(fb)
for i in range(260): dfb.line([(0, sh - 1 - i), (sw, sh - 1 - i)], fill=int(255 * (i / 260) ** 1.3))
mask_s = ImageChops.multiply(ImageChops.multiply(mask_s, fade), fb)
rim = mask_s.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4))
canvas.paste((255, 255, 255), (ox, oy), rim.point(lambda v: int(v * 0.25)))
canvas.paste(subj_s, (ox, oy), mask_s)
l1 = text_img('NO NAME?', 150, None, grad=((255, 255, 255), (205, 208, 214)))
l2 = text_img('NO NIL.', 230, None, stroke=16, grad=((255, 243, 120), (255, 190, 0)))
import random
rnd = random.Random(4)
br = Image.new('RGBA', (1000, 140), (0, 0, 0, 0)); db = ImageDraw.Draw(br)
N = 60; up, dn = [], []
for i in range(N + 1):                       # tapered brush swipe: thin at the start, thick in the middle, dry-brush ends
    x = 20 + 960 * i / N; k = i / N
    th = 14 + 62 * math.sin(math.pi * min(1, k * 1.15)) ** 0.7
    yc = 88 - 34 * k
    up.append((x, yc - th / 2 + rnd.uniform(-2.5, 2.5))); dn.append((x, yc + th / 2 + rnd.uniform(-2.5, 2.5)))
db.polygon(up + dn[::-1], fill=(232, 35, 30, 255))
br = br.filter(ImageFilter.GaussianBlur(0.6))
canvas.paste(br, (40, 1790), br)
drop(l1, ((W - l1.width) // 2, 1420))
drop(l2, ((W - l2.width) // 2 - 10, 1560))
v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i * 4, i * 4, W - i * 4, H - i * 4], outline=int(90 * (1 - i / 60)))
canvas.paste((0, 0, 0), (0, 0), v.filter(ImageFilter.GaussianBlur(40)))
out = '/home/user/Erin-Brown-/exports/thumbnails/nil_reality_yt_thumb'
canvas.save(out + '.jpg', quality=95)
canvas.crop((0, 260, W, 260 + 1440)).save(out + '_3x4.jpg', quality=95)
