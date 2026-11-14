"""Cinematic FX shots (Nov 2026 'v2' editing style: fewer stickers, effects built into the footage).
Each function renders a finished 1080x1920 30 fps clip (no audio) that build.py can use as a full-screen segment.

  freeze_pop(src, t, out, dur, title, sub)       action freezes, athlete cut out with outline + glow, bg darkens/drifts,
                                                  big title BEHIND the athlete
  text_behind(src, ss, dur, out, text, sub)      moving footage, per-frame cutout, title sits behind the athlete
  parallax(photo, out, dur, text, sub)           2.5D push: athlete layer and background move at different speeds
  ramp(src, ss, dur, out, slow_from, factor)     real-time into slow motion (motion-interpolated) speed ramp
  map_africa(out, dur, hits, final)              dark map, countries light up on the spoken word
  progression(out, dur, bg_src, bg_t, cols)      age-by-age numbers card over a blurred race frame
All of them share grade(): film contrast, warm highs / cool shadows, grain, vignette. Faces/voice untouched elsewhere."""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H, FPS = 1080, 1920, 30
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fonts')
GOLD = (255, 200, 61); WHITE = (255, 255, 255)
_sess = None

def font(name, size): return ImageFont.truetype(os.path.join(FD, name), size)

def mask_of(im):
    global _sess
    from rembg import remove, new_session
    if _sess is None: _sess = new_session('u2net_human_seg')
    return remove(im, session=_sess, only_mask=True).convert('L')

def cover(im, w=W, h=H, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    r = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x = int((r.width - w) * fx); y = int((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))

def zoom(im, k, cx=0.5, cy=0.5):
    """scale about (cx, cy) by k >= 1, same canvas size"""
    if abs(k - 1) < 1e-4: return im
    w, h = im.size; nw, nh = round(w * k), round(h * k)
    r = im.resize((nw, nh), Image.BICUBIC)
    x = int((nw - w) * cx); y = int((nh - h) * cy)
    return r.crop((x, y, x + w, y + h))

_rng = np.random.default_rng(7)
_vig = None
def grade(im, grain=0.035, strength=1.0):
    """film-ish: S-curve contrast, warm highlights / cool shadows, light grain, vignette"""
    global _vig
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    a = a + strength * 0.10 * (a - 0.5) * (1 - np.abs(2 * a - 1))               # gentle S-curve
    lum = a.mean(axis=2, keepdims=True)
    tint = np.concatenate([lum * 0.035 - 0.012, lum * 0.010 - 0.002, -lum * 0.030 + 0.016], axis=2)
    a = a + strength * tint
    if _vig is None or _vig.shape[:2] != a.shape[:2]:
        yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]].astype(np.float32)
        d = np.sqrt(((xx / a.shape[1]) - 0.5) ** 2 * 1.0 + ((yy / a.shape[0]) - 0.5) ** 2 * 0.6)
        _vig = (1 - 0.55 * np.clip((d - 0.25) / 0.45, 0, 1) ** 1.6)[..., None]
    a = a * _vig
    if grain: a = a + _rng.normal(0, grain, a.shape[:2])[..., None].astype(np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

class Writer:
    def __init__(s, out, fps=FPS):
        s.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps),
                                '-i', '-', '-c:v', 'libx264', '-crf', '13', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    def add(s, im): s.p.stdin.write(im.convert('RGB').tobytes())
    def close(s): s.p.stdin.close(); s.p.wait()

def read_frames(src, ss, dur, fx=0.5, fy=0.5, fps=FPS):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-t', f'{dur:.3f}', '-i', src, '-vf',
                        f'fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})*{fy}',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    n = len(p) // (W * H * 3)
    return [Image.frombuffer('RGB', (W, H), p[i * W * H * 3:(i + 1) * W * H * 3]).copy() for i in range(n)]

def frame_at(src, t, fx=0.5, fy=0.5):
    if src.lower().endswith(('.jpg', '.jpeg', '.png')): return cover(Image.open(src).convert('RGB'), fx=fx, fy=fy)
    return read_frames(src, t, 1 / FPS + 0.01, fx, fy)[0]

def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def ease_io(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)

def title_layer(text, size, color=WHITE, track=0, font_name='Anton-Regular.ttf', max_w=1000, shadow=True):
    f = font(font_name, size)
    while f.getlength(text) + track * len(text) > max_w and size > 40: size -= 6; f = font(font_name, size)
    tw = int(f.getlength(text) + track * len(text)) + 40; th = int(size * 1.3)
    L = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = 20
    for ch in text:
        d.text((x, 0), ch, font=f, fill=color + (255,)); x += f.getlength(ch) + track
    if shadow:
        sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (0, 0), L.split()[3])
        sh = sh.filter(ImageFilter.GaussianBlur(14)); out = Image.new('RGBA', L.size, (0, 0, 0, 0))
        out.alpha_composite(sh, (0, 6)); out.alpha_composite(L); return out
    return L

def place(canvas, layer, cx, cy, alpha=1.0, scale=1.0):
    if scale != 1.0: layer = layer.resize((max(1, int(layer.width * scale)), max(1, int(layer.height * scale))), Image.BICUBIC)
    if alpha < 1: layer = layer.copy(); layer.putalpha(layer.split()[3].point(lambda v: int(v * alpha)))
    canvas.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def outline(mask, px=7, glow=26, col=WHITE):
    ring = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(px * 2 + 1)), mask)
    g = mask.filter(ImageFilter.MaxFilter(px * 2 + 1)).filter(ImageFilter.GaussianBlur(glow))
    L = Image.new('RGBA', mask.size, col + (0,)); L.putalpha(ImageChops.lighter(ring, g.point(lambda v: int(v * 0.55))))
    return L

# ---------------------------------------------------------------- shots
def freeze_pop(src, t, out, dur, title, sub=None, fx=0.5, fy=0.5, ty=0.36, push=0.07, title_size=330, color=WHITE, sy=0.80):
    base = frame_at(src, t, fx, fy); m = mask_of(base)
    W_ = Writer(out); n = int(dur * FPS)
    for i in range(n):
        u = i / max(1, n - 1); k = ease(i / 10)
        bg = zoom(base, 1 + push * u).filter(ImageFilter.GaussianBlur(1 + 7 * k))
        bg = Image.blend(bg, Image.new('RGB', bg.size, (8, 8, 12)), 0.55 * k)
        fr = bg.convert('RGBA')
        tl = title_layer(title, title_size, color, track=4)
        place(fr, tl, W / 2, H * ty + 60 * (1 - ease(i / 9)), alpha=ease(i / 7), scale=1.12 - 0.12 * ease(i / 9))
        sm = zoom(m, 1 + push * 1.6 * u, 0.5, 0.6); sb = zoom(base, 1 + push * 1.6 * u, 0.5, 0.6)
        fr.alpha_composite(outline(sm).copy(), (0, 0)) if k > 0.2 else None
        subj = sb.convert('RGBA'); subj.putalpha(sm); fr.alpha_composite(subj)
        if sub: place(fr, title_layer(sub, 64, GOLD, track=6, font_name='Montserrat-Black.ttf'), W / 2, H * sy, alpha=ease((i - 6) / 8))
        if i < 4: fr = Image.blend(fr.convert('RGB'), Image.new('RGB', fr.size, WHITE), 0.6 * (1 - i / 4)).convert('RGBA')
        W_.add(grade(fr))
    W_.close()

def text_behind(src, ss, dur, out, text, sub=None, fx=0.5, fy=0.5, ty=0.34, size=380, color=WHITE, slow=1.0):
    frames = read_frames(src, ss, dur / slow, fx, fy)
    if slow != 1.0: frames = [frames[min(len(frames) - 1, int(i * slow))] for i in range(int(dur * FPS))]
    W_ = Writer(out); tl = title_layer(text, size, color, track=6); masks = {}
    for i, f in enumerate(frames[:int(dur * FPS)]):
        key = id(f)
        if key not in masks: masks[key] = mask_of(f)
        fr = f.convert('RGBA')
        place(fr, tl, W / 2, H * ty + 80 * (1 - ease(i / 10)), alpha=ease(i / 8), scale=1.15 - 0.15 * ease(i / 10))
        subj = f.convert('RGBA'); subj.putalpha(masks[key]); fr.alpha_composite(subj)
        if sub: place(fr, title_layer(sub, 58, GOLD, track=6, font_name='Montserrat-Black.ttf'), W / 2, H * 0.83, alpha=ease((i - 8) / 8))
        W_.add(grade(fr))
    W_.close()

def parallax(photo, out, dur, text=None, sub=None, fx=0.5, fy=0.3, ty=0.30, size=300, color=WHITE, cy=0.75, subj_scale=1.0, sy=0.86):
    im = Image.open(photo).convert('RGB'); base = cover(im, fx=fx, fy=fy); m = mask_of(base)
    bgsrc = base.filter(ImageFilter.GaussianBlur(3 if subj_scale >= 1 else 22))
    if subj_scale < 1:                       # shrink the cut-out athlete (never enlarged), bottom-anchored; bg stays full-bleed
        sw, sh = int(W * subj_scale), int(H * subj_scale)
        b2 = Image.new('RGB', (W, H)); m2 = Image.new('L', (W, H), 0)
        b2.paste(base.resize((sw, sh), Image.LANCZOS), ((W - sw) // 2, H - sh)); m2.paste(m.resize((sw, sh), Image.LANCZOS), ((W - sw) // 2, H - sh))
        base, m = b2, m2
    W_ = Writer(out); n = int(dur * FPS)
    tl = title_layer(text, size, color, track=6) if text else None
    for i in range(n):
        u = ease_io(i / max(1, n - 1))
        fr = zoom(bgsrc, 1.02 + 0.03 * u, 0.5 + 0.04 * u, 0.5).convert('RGBA')
        fr = Image.alpha_composite(fr, Image.new('RGBA', fr.size, (0, 0, 0, int(70 * ease(i / 12)))))
        if tl: place(fr, tl, W / 2, H * ty + 50 * (1 - ease(i / 12)), alpha=ease(i / 10))
        k = 1.0 + 0.10 * u
        sb = zoom(base, k, 0.5, cy); sm = zoom(m, k, 0.5, cy)
        subj = sb.convert('RGBA'); subj.putalpha(sm); fr.alpha_composite(subj)
        if sub: place(fr, title_layer(sub, 58, GOLD, track=6, font_name='Montserrat-Black.ttf'), W / 2, H * sy, alpha=ease((i - 10) / 8))
        W_.add(grade(fr, strength=0.8))
    W_.close()

def ramp(src, ss, dur, out, slow_from, factor=0.35, fx=0.5, fy=0.5):
    """plays real time until slow_from (s into the shot), then motion-interpolated slow motion at `factor` speed"""
    tmp = out + '.mi.mp4'; rt = slow_from; need = rt + (dur - rt) * factor + 0.2
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ss:.3f}', '-t', f'{need:.3f}', '-i', src, '-vf',
                    f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})*{fy},'
                    f'minterpolate=fps={int(FPS / factor)}:mi_mode=mci:mc_mode=aobmc:vsbmc=1', '-an', '-c:v', 'libx264', '-crf', '12',
                    '-preset', 'fast', tmp], check=True)
    fr = read_frames(tmp, 0, need, fps=int(FPS / factor))
    hi = int(FPS / factor); seq = []
    for i in range(int(dur * FPS)):
        t = i / FPS
        st = t if t < rt else rt + (t - rt) * factor            # source time
        seq.append(fr[min(len(fr) - 1, int(st * hi))])
    W_ = Writer(out)
    for f in seq: W_.add(grade(f))
    W_.close(); os.remove(tmp)

def _proj(lon, lat, box):
    x0, y0, x1, y1 = box
    return (lon - x0) / (x1 - x0), (y1 - lat) / (y1 - y0)

def map_africa(out, dur, hits, geo, final=None, title=None):
    """hits: [(t, ISO_A2, LABEL)] countries lighting up gold on the word; final: (t, text) big line at the end"""
    G = json.load(open(geo))['features']
    AF = [f for f in G if f['properties'].get('CONTINENT') == 'Africa']
    box0 = (-20, -36, 55, 38)                 # lon/lat window around Africa
    def polys(f):
        g = f['geometry']; cs = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        return [p[0] for p in cs]
    shapes = {f['properties']['ISO_A2']: polys(f) for f in AF}
    cent = {}
    for k, ps in shapes.items():
        big = max(ps, key=len); cent[k] = (sum(p[0] for p in big) / len(big), sum(p[1] for p in big) / len(big))
    W_ = Writer(out); n = int(dur * FPS); SS = 2
    for i in range(n):
        t = i / FPS; u = ease_io(t / dur)
        sc = 1.0 + 0.10 * u                  # slow push
        img = Image.new('RGB', (W * SS // 2, H * SS // 2), (10, 12, 18)); d = ImageDraw.Draw(img)
        ww, hh = img.size; mw = ww * 0.98 * sc; mh = mw * (box0[3] - box0[1]) / (box0[2] - box0[0]) * 1.05
        ox = (ww - mw) / 2; oy = (hh - mh) / 2 - hh * 0.02
        P = lambda lo, la: (ox + _proj(lo, la, box0)[0] * mw, oy + _proj(lo, la, box0)[1] * mh)
        lit = {h_[1]: max(0, t - h_[0]) for h_ in hits if t >= h_[0]}
        for k, ps in shapes.items():
            on = k in lit; a = ease(lit.get(k, 0) / 0.35)
            col = tuple(int(c0 + (c1 - c0) * a) for c0, c1 in zip((38, 42, 52), GOLD)) if on else (38, 42, 52)
            if final and t >= final[0]: col = tuple(int(c0 + (c1 - c0) * 0.35 * ease((t - final[0]) / 0.6)) for c0, c1 in zip(col, GOLD)) if not on else col
            for p in ps: d.polygon([P(x, y) for x, y in p], fill=col, outline=(16, 18, 24))
        img = img.resize((W, H), Image.LANCZOS).convert('RGBA')
        glow = Image.new('L', (W, H), 0); dg = ImageDraw.Draw(glow)
        for h_ in hits:
            tt, c = h_[0], h_[1]
            if t >= tt and c in cent:
                x, y = P(*cent[c]); x, y = x * 2 / SS, y * 2 / SS; r = 26 + 10 * math.sin((t - tt) * 6) * math.exp(-(t - tt) * 2)
                dg.ellipse([x - r, y - r, x + r, y + r], fill=int(200 * math.exp(-(t - tt) * 1.2)))
        img.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 255)] * 3 + [glow.filter(ImageFilter.GaussianBlur(18))]))
        for h_ in hits:
            tt, c, lab = h_[:3]; dx, dy = (h_[3], h_[4]) if len(h_) > 4 else (0, -46)
            if t >= tt and c in cent:
                x, y = P(*cent[c]); x, y = x * 2 / SS, y * 2 / SS
                place(img, title_layer(lab, 46, WHITE, track=3, font_name='Montserrat-Black.ttf'), x + dx, y + dy, alpha=ease((t - tt) / 0.25))
        if title: place(img, title_layer(title, 120, WHITE, track=4), W / 2, H * 0.12, alpha=ease(t / 0.5))
        if final and t >= final[0]: place(img, title_layer(final[1], 150, GOLD, track=4), W / 2, H * 0.88, alpha=ease((t - final[0]) / 0.4), scale=1.1 - 0.1 * ease((t - final[0]) / 0.4))
        W_.add(grade(img, grain=0.025, strength=0.6))
    W_.close()

def progression(out, dur, bg_src, bg_t, cols, title=None, fx=0.5, fy=0.5):
    """cols: [{'head': 'AGE 14', 't': s, 'rows': [('100M', '10.5'), ...], 'hi': False}, ...] left to right"""
    bg = frame_at(bg_src, bg_t, fx, fy).filter(ImageFilter.GaussianBlur(14))
    bg = Image.blend(bg, Image.new('RGB', bg.size, (6, 6, 10)), 0.62)
    W_ = Writer(out); n = int(dur * FPS); cx = [W * (0.5 + (j - (len(cols) - 1) / 2) * 0.46) for j in range(len(cols))]
    for i in range(n):
        t = i / FPS; fr = zoom(bg, 1.02 + 0.03 * t / dur).convert('RGBA')
        if title: place(fr, title_layer(title, 96, WHITE, track=4), W / 2, H * 0.22, alpha=ease(t / 0.4))
        for j, c in enumerate(cols):
            if t < c['t']: continue
            a = ease((t - c['t']) / 0.35); col = GOLD if c.get('hi') else (200, 200, 205)
            place(fr, title_layer(c['head'], 62, col, track=8, font_name='Montserrat-Black.ttf'), cx[j], H * 0.36, alpha=a)
            for r, row in enumerate(c['rows']):
                lab, val = row[0], row[1]; rt = row[2] if len(row) > 2 else c['t'] + 0.25 * r; b = ease((t - rt) / 0.35)
                if b <= 0: continue
                try:
                    v = float(val); dec = len(val.split('.')[1]) if '.' in val else 0
                    shown = f"{v * (1.25 - 0.25 * ease((t - rt) / 0.6)):.{dec}f}"
                except ValueError: shown = val
                place(fr, title_layer(shown, 210 if c.get('hi') else 170, WHITE if c.get('hi') else (215, 215, 220), track=2), cx[j], H * (0.47 + 0.17 * r), alpha=b)
                place(fr, title_layer(lab, 44, col, track=6, font_name='Montserrat-Black.ttf'), cx[j], H * (0.47 + 0.17 * r) + 120, alpha=b)
        if len(cols) > 1 and t >= cols[1]['t']:
            a = ease((t - cols[1]['t']) / 0.4); d = ImageDraw.Draw(fr)
            d.line([(W / 2 - 40, H * 0.36), (W / 2 - 40 + 80 * a, H * 0.36)], fill=GOLD + (255,), width=8)
            d.polygon([(W / 2 + 40 * a + 10, H * 0.36), (W / 2 + 40 * a - 14, H * 0.36 - 18), (W / 2 + 40 * a - 14, H * 0.36 + 18)], fill=GOLD + (int(255 * a),))
        W_.add(grade(fr, grain=0.03, strength=0.6))
    W_.close()

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    only = set(sys.argv[2:])
    for s in spec:
        if only and s['out'] not in only: continue
        if os.path.exists(s['out']) and not s.get('force'): print('cached', s['out']); continue
        fn = globals()[s.pop('fx')]; s.pop('force', None)
        print('render', s['out'], flush=True); fn(**s)
