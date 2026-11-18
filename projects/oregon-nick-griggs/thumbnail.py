# Cover in the owner's thumbnail style (CLAUDE.md step 8): full-bleed real photo, subject cut out, slanted two-tone
# Montserrat Black headline with a red brush swipe, red-ringed circle inset, red tag and arrow. Nothing enlarged:
# Hayward Field (Commons, 1920x2560 -> 0.75x), Nick Griggs from Oregon's signing photo at 1.0x, coach frame 520px -> 400px.
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import math
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
W, H = 1080, 1920
def grade(im, c=1.18, s=1.15, b=1.0): return ImageEnhance.Brightness(ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(c)).enhance(s)).enhance(b)
bgsrc = Image.open('raw/stock/hay63.jpg').convert('RGB')
k = max(W / bgsrc.width, H / bgsrc.height); bgsrc = bgsrc.resize((round(bgsrc.width * k), round(bgsrc.height * k)), Image.LANCZOS)
x0 = int((bgsrc.width - W) * 0.55); bg = bgsrc.crop((x0, 0, x0 + W, H))
bg = grade(bg.filter(ImageFilter.GaussianBlur(3)), 1.1, 1.05, 0.62)
gr = Image.new('L', (W, H), 0); d = ImageDraw.Draw(gr)
for y in range(H): d.line([(0, y), (W, y)], fill=int(150 * max(0, (700 - y) / 700) ** 1.2 + 120 * max(0, (y - 1300) / 620) ** 1.4))
bg.paste((0, 0, 0), (0, 0), gr)
canvas = bg.convert('RGB')
# subject: Nick Griggs cutout at native size, sitting on the bottom edge (the signing banner cuts him at the arms)
ph = Image.open('raw/photo1.jpg').convert('RGB'); m = Image.open('work/griggs_mask.png').convert('L')
bb = m.point(lambda v: 255 if v > 40 else 0).getbbox(); ph, m = ph.crop(bb), m.crop(bb)
import numpy as np, scipy.ndimage as ndi
_a = np.array(m) > 40; _l, _n = ndi.label(_a); _keep = (_l == (np.bincount(_l.ravel())[1:].argmax() + 1))
_mm = np.where(_keep, np.array(m), 0).astype('uint8'); _mm[-130:, :45] = 0      # drop a yellow scrap of the graphic at the cut edge
m = Image.fromarray(_mm)
m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
subj = grade(ph, 1.15, 1.1, 1.05)   # no extra sharpening: the source graphic has a woven texture overlay
sx, sy = (W - subj.width) // 2 + 150, H - subj.height
rim = Image.new('L', (W, H), 0); rim.paste(m.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(5)), (sx, sy))
canvas.paste((255, 255, 255), (0, 0), rim.point(lambda v: int(v * 0.35)))
canvas.paste(subj, (sx, sy), m)

def text_img(t, size, fill, stroke=12, grad=None, skew=0.18):
    f = ImageFont.truetype(F + 'Montserrat-Black.ttf', size)
    tw, th = int(f.getlength(t)) + 60, int(size * 1.35)
    mm = Image.new('L', (tw, th), 0); ImageDraw.Draw(mm).text((30, 0), t, font=f, fill=255)
    s = Image.new('L', (tw, th), 0); ImageDraw.Draw(s).text((30, 0), t, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    body = Image.new('RGBA', (tw, th), fill)
    if grad:
        g = Image.new('RGBA', (tw, th)); dg = ImageDraw.Draw(g)
        for y in range(th):
            kk = y / th; dg.line([(0, y), (tw, y)], fill=tuple(int(grad[0][i] * (1 - kk) + grad[1][i] * kk) for i in range(3)) + (255,))
        body = g
    out = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); out.paste((0, 0, 0, 255), (0, 0), s); out.paste(body, (0, 0), mm)
    sh = int(skew * th)
    return out.transform((tw + sh, th), Image.AFFINE, (1, skew, -sh, 0, 1, 0), Image.BICUBIC)
def drop(img, xy, blur=16, off=(8, 14), a=190):
    s = Image.new('RGBA', img.size, (0, 0, 0, 0)); s.paste((0, 0, 0, a), (0, 0), img.split()[3])
    s = s.filter(ImageFilter.GaussianBlur(blur)); canvas.paste(s, (xy[0] + off[0], xy[1] + off[1]), s); canvas.paste(img, xy, img)
def fit(img, maxw):
    if img.width <= maxw: return img
    r = maxw / img.width; return img.resize((maxw, int(img.height * r)), Image.LANCZOS)

# headline (top third, over the stadium sky)
l1 = fit(text_img('DOUBLE', 190, (255, 255, 255, 255)), 1000)
l2 = fit(text_img('STANDARD?', 170, (0, 0, 0, 255), grad=[(255, 236, 90), (255, 176, 20)]), 1040)
y1 = 250; y2 = y1 + l1.height - 30
# red brush swipe under line 2 (tapered)
br = Image.new('RGBA', (W, H), (0, 0, 0, 0)); db = ImageDraw.Draw(br)
bx0, bx1, by = 60, 1020, y2 + l2.height - 40
for i in range(60):
    t = i / 59; x = bx0 + (bx1 - bx0) * t; hh = 34 * math.sin(math.pi * min(1, t * 1.15)) + 6
    db.ellipse([x - 26, by - hh + 8 * t, x + 26, by + hh + 8 * t], fill=(232, 35, 30, 255))
canvas.paste(br, (0, 0), br)
drop(l1, ((W - l1.width) // 2, y1)); drop(l2, ((W - l2.width) // 2, y2))

# circle inset: Jerry Schumacher (frame from his interview, 520px square shown at 400px)
fr = Image.open('work/coach_f1200.png').convert('RGB').crop((100, 120, 620, 640))
R = 200; fr = grade(fr.resize((2 * R, 2 * R), Image.LANCZOS), 1.12, 1.1)
cm = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(cm).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
cx, cy = 255, 1080
glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=200)
canvas.paste((232, 35, 30), (0, 0), glow.filter(ImageFilter.GaussianBlur(28)))
dc = ImageDraw.Draw(canvas)
dc.ellipse([cx - R - 22, cy - R - 22, cx + R + 22, cy + R + 22], fill=(232, 35, 30))
dc.ellipse([cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8], fill=(255, 255, 255))
canvas.paste(fr, (cx - R, cy - R), cm)
def tagbox(t, size=56):
    tg = text_img(t, size, (255, 255, 255, 255), stroke=8, skew=0.15)
    tb = Image.new('RGBA', (tg.width + 40, tg.height + 6), (232, 35, 30, 255)); tb.paste(tg, (20, 4), tg)
    return tb.transform(tb.size, Image.AFFINE, (1, 0.12, -12, 0, 1, 0), Image.BICUBIC)
t1 = tagbox('OREGON COACH', 46); drop(t1, (cx - t1.width // 2, cy + R + 10), blur=10)
t2 = tagbox('EX-PRO', 60); tx, ty = 690, 1250; drop(t2, (tx, ty - t2.height), blur=10)
# curved red arrow (white outline) from the EX-PRO tag down to Nick
pts = [(tx + 70 + 0 * t, 0) for t in range(1)]
P0, P1, P2 = (tx + 250, ty + 15), (tx + 330, ty + 200), (sx + subj.width - 95, sy + 300)
curve = [((1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0], (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]) for t in [i / 40 for i in range(41)]]
dc.line(curve, fill=(255, 255, 255), width=26, joint='curve'); dc.line(curve, fill=(232, 35, 30), width=14, joint='curve')
ex, ey = curve[-1]; px, py = curve[-4]; ang = math.atan2(ey - py, ex - px)
head = [(ex + 34 * math.cos(ang), ey + 34 * math.sin(ang)), (ex + 30 * math.cos(ang + 2.3), ey + 30 * math.sin(ang + 2.3)), (ex + 30 * math.cos(ang - 2.3), ey + 30 * math.sin(ang - 2.3))]
dc.polygon(head, fill=(232, 35, 30), outline=(255, 255, 255))
import os; os.makedirs('../../exports/thumbnails', exist_ok=True)
canvas.save('../../exports/thumbnails/oregon_nick_griggs_thumb.jpg', quality=93)
g = canvas.crop((0, 120, W, 120 + 1440)); g.save('../../exports/thumbnails/oregon_nick_griggs_thumb_3x4.jpg', quality=93)
print('ok', subj.size, (sx, sy))
