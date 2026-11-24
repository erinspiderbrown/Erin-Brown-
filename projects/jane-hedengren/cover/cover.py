# Cover in the owner's reference style (exports/thumbnails/reference/oregon_nick_griggs_owner_thumb.png):
# big sharp hero (Jane, Deseret News press photo 2400x1600, downscaled), second person in a thick team-colour ring
# (Katelyn Tuohy, adidas/CITIUS MAG press photo), bold curved arrow linking them, heavily blurred team-colour backdrop
# with the team letter big behind. No headline text. Nothing enlarged.
import numpy as np, scipy.ndimage as ndi, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageChops
W, H = 1080, 1440
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
BLUE = (0, 46, 138); ROYAL = (0, 82, 204); WHITE = (255, 255, 255)
def punch(im, c=1.12, s=1.18, b=1.04, sh=1.15):
    return ImageEnhance.Sharpness(ImageEnhance.Brightness(ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(c)).enhance(s)).enhance(b)).enhance(sh)
# backdrop: the 2026 NCAA XC start (BYU in blue), blurred hard, washed in royal blue, big "Y" behind
bgp = Image.open('raw/ph/des_2026xc.jpg').convert('RGB')
k = H / bgp.height; bgp = bgp.resize((round(bgp.width * k), H), Image.LANCZOS); x0 = (bgp.width - W) // 2
bg = bgp.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(28))
bg = Image.blend(bg, Image.new('RGB', (W, H), BLUE), 0.55)
canvas = bg.copy()
f = ImageFont.truetype(F + 'Anton-Regular.ttf', 1250)
Y = Image.new('L', (W, H), 0); ImageDraw.Draw(Y).text((W * 0.58, H * 0.47), 'Y', font=f, fill=255, anchor='mm')
canvas.paste(Image.new('RGB', (W, H), (235, 240, 255)), (0, 0), Y.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.6)))
vg = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(vg)
for i in range(70): dv.rectangle([i * 5, i * 5, W - i * 5, H - i * 5], outline=int(150 * (1 - i / 70)))
canvas.paste((0, 0, 20), (0, 0), vg.filter(ImageFilter.GaussianBlur(50)))
# hero: Jane, keep only her (drop the second runner), crop, downscale only
im = Image.open('raw/ph/des_rec.jpg').convert('RGB'); m = np.array(Image.open('cover/jane_mask.png').convert('L'))
lab, n = ndi.label(m > 60); keep = None
best = max(range(1, n + 1), key=lambda i: ((lab == i) & (np.arange(m.shape[1])[None, :] > 1050)).sum())
mm = np.where(lab == best, m, 0).astype('uint8')
mm[:, :1000] = np.where(np.arange(1000)[None, :] < 880, 0, mm[:, :1000])     # trim the second runner's edge
box = (760, 0, 2120, 1600)
hero = punch(im.crop(box)); hm = Image.fromarray(mm).crop(box).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
s = 1240 / hero.height; hero = hero.resize((round(hero.width * s), 1240), Image.LANCZOS); hm = hm.resize(hero.size, Image.LANCZOS)
hx, hy = -150, H - hero.height + 10
_hm=np.array(hm); _hm[int(1085-hy):, :int(45-hx)]=0; hm=Image.fromarray(_hm)   # drop the other runner's red sliver at the left edge
sh = Image.new('L', (W, H), 0); sh.paste(hm, (hx + 18, hy + 22)); canvas.paste((0, 0, 30), (0, 0), sh.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.6)))
canvas.paste(hero, (hx, hy), hm)
# circle: Tuohy
t = Image.open('raw/ph/tuohy.jpg').convert('RGB'); R = 230
tc = punch(t.crop((1040, 290, 1720, 970)), sh=1.05).resize((2 * R, 2 * R), Image.LANCZOS)
cx, cy = 790, 330
d = ImageDraw.Draw(canvas)
gl = Image.new('L', (W, H), 0); ImageDraw.Draw(gl).ellipse([cx - R - 34, cy - R - 34, cx + R + 34, cy + R + 34], fill=170)
canvas.paste((0, 0, 0), (0, 0), gl.filter(ImageFilter.GaussianBlur(24)))
d.ellipse([cx - R - 20, cy - R - 20, cx + R + 20, cy + R + 20], fill=WHITE)
cm = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(cm).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
canvas.paste(tc, (cx - R, cy - R), cm)
# bold curved arrow (white, dark outline) from the circle down to Jane
def arrow(p0, p1, p2, w=40):
    pts = [((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0], (1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1]) for u in [i/60 for i in range(61)]]
    a = Image.new('RGBA', (W, H), (0, 0, 0, 0)); da = ImageDraw.Draw(a)
    ang = math.atan2(pts[-1][1]-pts[-5][1], pts[-1][0]-pts[-5][0]); L = 96
    for r, col in ((w//2 + 9, (10, 20, 45, 255)), (w//2, (255, 255, 255, 255))):
        for i in range(len(pts) - 1):
            for k in range(5):
                x = pts[i][0] + (pts[i+1][0]-pts[i][0])*k/5; y = pts[i][1] + (pts[i+1][1]-pts[i][1])*k/5
                da.ellipse([x-r, y-r, x+r, y+r], fill=col)
        e = 14 if r > w//2 else 0
        tip = (p2[0] + math.cos(ang)*(52+e), p2[1] + math.sin(ang)*(52+e))
        da.polygon([tip, (p2[0]+math.cos(ang+2.35)*(L+e), p2[1]+math.sin(ang+2.35)*(L+e)), (p2[0]+math.cos(ang-2.35)*(L+e), p2[1]+math.sin(ang-2.35)*(L+e))], fill=col)
    sd = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd.paste((0, 0, 0, 150), (0, 0), a.split()[3]); sd = sd.filter(ImageFilter.GaussianBlur(14))
    canvas.paste(sd, (8, 12), sd); canvas.paste(a, (0, 0), a)
arrow((515, 700), (470, 560), (580, 530))
canvas.save('../../exports/thumbnails/jane_hedengren_thumb_3x4.jpg', quality=95)
full = Image.new('RGB', (W, 1920))
top = canvas.crop((0, 0, W, 6)).resize((W, 240), Image.BILINEAR).filter(ImageFilter.GaussianBlur(30))
bot = canvas.crop((0, H - 6, W, H)).resize((W, 240), Image.BILINEAR).filter(ImageFilter.GaussianBlur(30))
full.paste(top, (0, 0)); full.paste(bot, (0, 1680)); full.paste(canvas, (0, 240))
full.save('../../exports/thumbnails/jane_hedengren_thumb.jpg', quality=95)
