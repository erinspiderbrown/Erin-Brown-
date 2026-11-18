"""Animated 100 m race recreation (1080x1920, 30 fps), top-down straightaway, runners as glowing dots on a dark track.
Each runner's position follows a standard sprint curve (reaction 0.15 s, exponential acceleration) solved so they cross
at their official time. Only official times are used; the clip is labeled RACE RECREATION.
usage: python3 race_recreation.py spec.json out.mp4"""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
W, H, FPS = 1080, 1920, 30; SPEED = spec.get('speed', 1.0)
F = '/home/user/Erin-Brown-/editor/assets/fonts/'
fA = lambda s: ImageFont.truetype(F + 'Anton-Regular.ttf', s); fM = lambda s: ImageFont.truetype(F + 'Montserrat-Black.ttf', s)
RED, YEL = (232, 35, 30), (255, 225, 26)
runners = spec['runners']; T_end = max(r['time'] for r in runners); HOLD = spec.get('hold', 2.2)
LANES = 8; LW = 104; X0 = (W - LANES * LW) // 2; Y_START, Y_FIN = 1620, 330
def solve(T, tau=1.15, react=0.15):
    tt = T - react; return 100.0 / (tt - tau * (1 - math.exp(-tt / tau)))
def dist(r, t, tau=1.15, react=0.15):
    if t <= react: return 0.0
    tt = t - react; v = r['_v']; return min(100.0, v * (tt - tau * (1 - math.exp(-tt / tau)))) if t < r['time'] else 100.0
for r in runners: r['_v'] = solve(r['time'])
# static background
bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
for y in range(H):
    k = y / H; d.line([(0, y), (W, y)], fill=(int(12 + 8 * (1 - k)), int(13 + 9 * (1 - k)), int(20 + 18 * (1 - k))))
track = Image.new('RGB', (LANES * LW + 40, Y_START - Y_FIN + 260), (122, 44, 38))
tn = Image.effect_noise(track.size, 30).convert('RGB'); track = Image.blend(track, ImageChops.multiply(track, tn.point(lambda v: 170 + v // 3)), 0.5)
bg.paste(track, (X0 - 20, Y_FIN - 130)); d = ImageDraw.Draw(bg)
for i in range(LANES + 1):
    x = X0 + i * LW; d.line([(x, Y_FIN - 130), (x, Y_START + 130)], fill=(235, 235, 235), width=4)
for m in range(10, 100, 10):
    y = Y_START - (Y_START - Y_FIN) * m / 100; d.text((X0 - 70, y - 14), f'{m}', font=fM(26), fill=(120, 124, 135))
    d.line([(X0 - 18, y), (X0 - 4, y)], fill=(120, 124, 135), width=3)
d.line([(X0, Y_START), (X0 + LANES * LW, Y_START)], fill=(255, 255, 255), width=6)
for i in range(LANES * 2):                                        # checkered finish line
    for j in range(2):
        c = (255, 255, 255) if (i + j) % 2 == 0 else (20, 20, 20)
        d.rectangle([X0 + i * LW // 2, Y_FIN - 12 + j * 12, X0 + (i + 1) * LW // 2, Y_FIN + j * 12], fill=c)
d.text((W // 2, 92), spec['title'], font=fM(40), fill=(255, 255, 255), anchor='mm')
d.text((W // 2, 140), spec['sub'], font=fM(26), fill=(170, 175, 185), anchor='mm')
d.rounded_rectangle([W // 2 - 170, 168, W // 2 + 170, 214], 14, fill=(30, 32, 40))
d.text((W // 2, 191), 'RACE RECREATION', font=fM(26), fill=(200, 204, 214), anchor='mm')
for r in runners:
    x = X0 + (r['lane'] - 0.5) * LW
    d.text((x, Y_START + 62), r['label'], font=fM(30), fill=RED if r.get('hero') else (190, 194, 204), anchor='mm')
    if r.get('name'): d.text((x, Y_START + 100), r['name'], font=fM(17), fill=(150, 154, 164), anchor='mm')
n = int((T_end / SPEED + HOLD) * FPS)
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
hero = next(r for r in runners if r.get('hero'))
for k in range(n):
    t = min(k / FPS * SPEED, T_end + 5); im = bg.copy()
    glow = Image.new('L', (W, H), 0); dg = ImageDraw.Draw(glow); dots = ImageDraw.Draw(im)
    for r in runners:
        x = X0 + (r['lane'] - 0.5) * LW; y = Y_START - (Y_START - Y_FIN) * dist(r, t) / 100
        col = RED if r.get('hero') else ((255, 255, 255) if r.get('ghost') else (205, 208, 218))
        if r.get('hero'): dg.ellipse([x - 70, y - 70, x + 70, y + 70], fill=255)
        trail = 8
        for j in range(trail):
            yy = Y_START - (Y_START - Y_FIN) * dist(r, max(0, t - 0.04 * (j + 1) * SPEED)) / 100
            a = int(120 * (1 - j / trail)); dots.ellipse([x - 20 + j, yy - 20 + j, x + 20 - j, yy + 20 - j], outline=col + (a,), width=2)
        rr = 36 if r.get('hero') else 28
        if r.get('ghost'): dots.ellipse([x - rr, y - rr, x + rr, y + rr], outline=col, width=5); dots.text((x, y), '11.0', font=fM(18), fill=col, anchor='mm')
        else: dots.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col, outline=(255, 255, 255), width=4)
        if t >= r['time'] and (r.get('hero') or r.get('show_time')):
            dots.text((x, Y_FIN - 60), f"{r['time']:.2f}", font=fA(46 if r.get('hero') else 32), fill=YEL if r.get('hero') else (230, 230, 230), anchor='mm')
    im.paste(RED, (0, 0), glow.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * 0.6)))
    dd = ImageDraw.Draw(im); clock = min(t, hero['time'])
    dd.rounded_rectangle([W // 2 - 200, 1790, W // 2 + 200, 1900], 20, fill=(0, 0, 0))
    dd.text((W // 2, 1845), f'{clock:05.2f}', font=fA(96), fill=YEL if t >= hero['time'] else (255, 255, 255), anchor='mm')
    if hero['time'] <= t < hero['time'] + 0.25:                    # finish flash
        im = Image.blend(im, Image.new('RGB', (W, H), (255, 255, 255)), 0.35 * (1 - (t - hero['time']) / 0.25))
    ff.stdin.write(im.tobytes())
ff.stdin.close(); ff.wait(); print('wrote', out, round(n / FPS, 2), 's')
