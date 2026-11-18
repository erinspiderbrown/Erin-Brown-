# TikTok cover, Oregon / Nick Griggs. Built from the approved NIL cover (projects/nil-reality/thumbnail.py): same headline
# lettering, brush swipe, circle inset, arrow and vignette. Real images only, nothing enlarged:
# - the owner's 4K take (74.3 s, sharpest skeptical look), wide crop 2400x2160 -> 0.43x, cut out with rembg u2net_human_seg
# - Hayward Field (Commons, Habst, CC BY-SA 4.0), 1920x2560 -> 0.75x
# - Nick Griggs from Oregon's signing photo, 300 px crop shown at 300 px
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
import math
from rembg import remove, new_session
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
W, H = 1080, 1920
def grade(im, c=1.18, s=1.15, b=1.0): return ImageEnhance.Brightness(ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(c)).enhance(s)).enhance(b)
_h = Image.open('raw/stock/hay63.jpg').convert('RGB'); _k = max(W / _h.width, H / _h.height)
_h = _h.resize((round(_h.width * _k), round(_h.height * _k)), Image.LANCZOS); _x = int((_h.width - W) * 0.5)
bg = grade(_h.crop((_x, 0, _x + W, H)).filter(ImageFilter.GaussianBlur(7)), 1.12, 1.1, 0.5)
gr = Image.new('L', (W, H), 0); d = ImageDraw.Draw(gr)
for y in range(1050, H): d.line([(0, y), (W, y)], fill=int(190 * ((y - 1050) / (H - 1050)) ** 1.2))
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


# subject: the owner, full head and shoulders, soft rim, bottom faded into the headline
_f = Image.open('ph/f_74.3.png').convert('RGB').crop((840, 0, 3240, 2160))
SW = 1320; SH = round(_f.height * SW / _f.width)
subj = ImageEnhance.Sharpness(grade(_f.resize((SW, SH), Image.LANCZOS), 1.12, 1.08, 1.12)).enhance(1.15)
mask = remove(_f, session=new_session('u2net_human_seg'), only_mask=True).resize((SW, SH), Image.LANCZOS)
mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
ox, oy = (W - SW) // 2, 1530 - SH
fb = Image.new('L', (SW, SH), 255); dfb = ImageDraw.Draw(fb)
for i in range(320): dfb.line([(0, SH - 1 - i), (SW, SH - 1 - i)], fill=int(255 * (i / 320) ** 1.4))
mask_s = ImageChops.multiply(mask, fb)
rim = mask_s.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4))
canvas.paste((255, 255, 255), (ox, oy), rim.point(lambda v: int(v * 0.3)))
canvas.paste(subj, (ox, oy), mask_s)
# circle inset: Nick Griggs
fr = Image.open('raw/photo1.jpg').convert('RGB').crop((445, 200, 745, 500))
R = 150; fr = grade(fr, 1.1, 1.08)
cm = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(cm).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
cx, cy = 215, 330
glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=200)
canvas.paste((232, 35, 30), (0, 0), glow.filter(ImageFilter.GaussianBlur(28)))
dc = ImageDraw.Draw(canvas)
dc.ellipse([cx - R - 22, cy - R - 22, cx + R + 22, cy + R + 22], fill=(232, 35, 30))
dc.ellipse([cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8], fill=(255, 255, 255))
canvas.paste(fr, (cx - R, cy - R), cm)
tag = text_img('EX-PUMA PRO', 50, (255, 255, 255, 255), stroke=9, skew=0.15)
tb = Image.new('RGBA', (tag.width + 40, tag.height + 6), (232, 35, 30, 255)); tb.paste(tag, (20, 4), tag)
tb = tb.transform(tb.size, Image.AFFINE, (1, 0.12, -12, 0, 1, 0), Image.BICUBIC)
drop(tb, (max(10, cx - tb.width // 2), cy + R - 20), blur=10, off=(5, 8))
# red curved arrow from the circle up to him
def arrow(p0, p1, p2, w=34):
    pts = [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / 40 for i in range(41)]]
    a = Image.new('RGBA', (W, H), (0, 0, 0, 0)); da = ImageDraw.Draw(a)
    ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0]); L = 95
    tip = (p2[0] + math.cos(ang) * 40, p2[1] + math.sin(ang) * 40)
    head = [tip, (p2[0] + math.cos(ang + 2.4) * L, p2[1] + math.sin(ang + 2.4) * L), (p2[0] + math.cos(ang - 2.4) * L, p2[1] + math.sin(ang - 2.4) * L)]
    for (r, col) in ((w // 2 + 8, (255, 255, 255, 255)), (w // 2, (232, 35, 30, 255))):
        for i in range(len(pts) - 1):
            for k in range(6):
                x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k / 6; y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k / 6
                da.ellipse([x - r, y - r, x + r, y + r], fill=col)
        hd = head if r == w // 2 else [(tip[0] + math.cos(ang) * 12, tip[1] + math.sin(ang) * 12),
              (p2[0] + math.cos(ang + 2.4) * (L + 16), p2[1] + math.sin(ang + 2.4) * (L + 16)), (p2[0] + math.cos(ang - 2.4) * (L + 16), p2[1] + math.sin(ang - 2.4) * (L + 16))]
        da.polygon(hd, fill=col)
    s = Image.new('RGBA', (W, H), (0, 0, 0, 0)); s.paste((0, 0, 0, 160), (0, 0), a.split()[3]); s = s.filter(ImageFilter.GaussianBlur(12))
    canvas.paste(s, (6, 10), s); canvas.paste(a, (0, 0), a)
arrow((120, 565), (95, 700), (170, 790))
l1 = text_img('OREGON SIGNED', 112, None, grad=((255, 255, 255), (205, 208, 214)))
l2 = text_img('A PRO?!', 240, None, stroke=16, grad=((255, 243, 120), (255, 190, 0)))
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
drop(l2, ((W - l2.width) // 2 - 10, 1540))
v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
for i in range(60): dv.rectangle([i * 4, i * 4, W - i * 4, H - i * 4], outline=int(90 * (1 - i / 60)))
canvas.paste((0, 0, 0), (0, 0), v.filter(ImageFilter.GaussianBlur(40)))
out = '/home/user/Erin-Brown-/exports/thumbnails/oregon_nick_griggs_thumb'
canvas.save(out + '.jpg', quality=95)
canvas.crop((0, 240, W, 240 + 1440)).save(out + '_3x4.jpg', quality=95)
