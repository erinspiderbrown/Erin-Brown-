"""TikTok editor: split-screen (talking head top / B-roll bottom) <-> full-screen B-roll.

Usage: python3 build.py plan.json
All times in the plan are OUTPUT seconds (0 = start of edit), except *_ss fields which are source seek times.
"""
import hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import transitions

W, H, FPS, D = 1080, 1920, 30, 0.30          # canvas, fps, transition duration
HALF = H // 2
GOLD_ASS = '&H2CC7FF&'                        # #FFC72C in ASS BGR

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        err = '\n'.join(l for l in r.stderr.splitlines() if len(l) < 600)   # skip ffmpeg's echo of huge filtergraphs
        sys.exit(f"FAILED: {' '.join(cmd)[:400]}...\n{err[-3000:]}")

IMG = ('.jpg', '.jpeg', '.png', '.webp', '.heic')
def is_img(p): return p.lower().endswith(IMG)

def cover(w, h, crop=None, push=0.0, dur=1.0, punch=0.0, focus=(0.5, 0.5), zexpr=None, src_wh=None):
    """crop source region, scale to COVER w x h (never letterboxed), optional push-in / punch / zoom expr.
    focus = (x, y) 0..1 keeps the action in frame when cropping."""
    fx, fy = focus
    f = []
    if crop: f.append('crop=%d:%d:%d:%d' % tuple(crop))
    f.append(f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos')
    f.append(f"crop={w}:{h}:x='(iw-ow)*{fx}':y='(ih-oh)*{fy}'")
    z = []
    if push: z.append(f'{push}*t/{dur}')
    if punch: z.append(f'{punch}*pow(max(0,1-t/0.28),2)')
    if zexpr: z.append(zexpr)
    if z:
        zz = '(1+' + '+'.join(z) + ')'
        f.append(f"scale=w='trunc({w}*{zz}/2)*2':h=-2:eval=frame:flags=bicubic,crop={w}:{h}:x='(iw-ow)*{fx}':y='(ih-oh)*{fy}'")
    up = 1.0
    if src_wh:
        cw, ch = (crop[0], crop[1]) if crop else src_wh
        up = max(w / cw, h / ch)
    f.append(('unsharp=5:5:0.9:5:5:0' if up > 1.3 else 'unsharp=5:5:0.6:5:5:0') + ',setsar=1')
    return ','.join(f)

_probe = {}
def cached(path, expect=None):
    """A cached render counts only if it's complete. A stopped render can leave a 0-byte file, or (ffmpeg exits
    cleanly on SIGTERM) a valid but short one, so check the duration against what the render should produce."""
    if not os.path.exists(path) or os.path.getsize(path) < 1024: return False
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True)
    try: got = float(r.stdout.strip())
    except ValueError: return False
    return expect is None or got >= expect - 0.1

def probe(src):
    if src not in _probe:
        r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=width,height:stream_side_data=rotation', '-of', 'json', src], capture_output=True, text=True)
        st = json.loads(r.stdout)['streams'][0]; w, h = st['width'], st['height']
        rot = abs(int(float(next((d.get('rotation', 0) for d in st.get('side_data_list', [])), 0))))
        _probe[src] = (h, w) if rot in (90, 270) else (w, h)
    return _probe[src]

def check_sources(plan, min_short=1080):
    bad = []
    for s in plan['segments']:
        w, h = probe(s['broll']['src'])
        if min(w, h) < min_short: bad.append(f"  B-roll {os.path.basename(s['broll']['src'])}: {w}x{h}")
    fw, fh = probe(plan['face']['src'])
    if min(fw, fh) < min_short: print(f"WARNING: talking-head source is only {fw}x{fh}")
    if bad: sys.exit('B-roll below 1080p (rejected):\n' + '\n'.join(sorted(set(bad))))

def seam_assets(plan, F):
    """Alpha mask that dissolves the face into the B-roll over F px (cos^2 falloff), plus a soft dark band for caption contrast."""
    wd = plan['workdir']; HF = HALF + F // 2
    mask, shade = f'{wd}/seam_mask_{F}.png', f'{wd}/seam_shade_{F}.png'
    if not os.path.exists(mask):
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=white:s={W}x{HF}', '-vf',
             f"format=gray,geq=lum='255*if(lt(Y,{HF-F}),1,pow(cos(PI/2*(Y-{HF-F})/{F}),2))'", '-frames:v', '1', mask])
        sh = int(F * 1.4); op = float(plan.get('seam_shade', 0.30))
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=black:s={W}x{sh}', '-vf',
             f"format=rgba,geq=r=0:g=0:b=0:a='255*{op}*pow(sin(PI*Y/{sh}),2)'", '-frames:v', '1', shade])
    return mask, shade

def soft_seam_asset(plan):
    """Soft shadow band centred on the seam: darkest at the edge, fading out ~seam_soft px each way."""
    sw = int(plan.get('seam_soft', 46)); op = float(plan.get('seam_shadow', 0.55))
    path = f"{plan['workdir']}/seam_soft_{sw}_{op}.png"
    if not os.path.exists(path):
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=black:s={W}x{2*sw}', '-vf',
             f"format=rgba,geq=r=0:g=0:b=0:a='255*{op}*pow(1-abs(Y-{sw})/{sw},2.2)'", '-frames:v', '1', path])
    return path

def render_segment(plan, seg, a, b, out):
    face, br = plan['face'], seg['broll']
    fss = plan['voice_ss'] + a                 # face stays lip-synced to voice
    bss = max(0.0, br['ss'] + (a - seg['start']))
    dur = b - a
    grade = plan.get('face_grade', 'hqdn3d=1.5:1.5:4:4,eq=contrast=1.06:saturation=1.06:gamma=0.98,vignette=PI/6')
    bpush = 0.10 if is_img(br['src']) else 0.04
    if seg['type'] == 'split':
        zt = [f"{k-1}*min(1,(t+{a:.3f}-{z0})/0.12)*between(t+{a:.3f},{z0},{z1})" for z0, z1, k in plan.get('zooms', [])
              if z1 > a and z0 < b]
        ffoc = tuple(face.get('focus', (0.5, 0.35))); bfoc = tuple(br.get('focus', (0.5, 0.5)))
        if plan.get('seam_style', 'soft') == 'blend':      # face dissolves into B-roll (not the owner's preference)
            F = int(plan.get('seam_feather', 220)); HF = HALF + F // 2
            mask, shade = seam_assets(plan, F)
            fc = (f"[0:v]{cover(W, HF, face.get('crop'), focus=ffoc, zexpr='+'.join(zt) or None)},{grade},format=yuva420p[f];"
                  f"[2:v]format=gray,scale={W}:{HF}[m];[f][m]alphamerge[fa];"
                  f"[1:v]{cover(W, HF, br.get('crop'), bpush, dur, focus=bfoc, src_wh=probe(br['src']))}[b];"
                  f"color=c=black:s={W}x{H}:r={FPS}:d={dur:.3f}[bg];[bg][b]overlay=0:{H-HF}[t1];[t1][fa]overlay=0:0:shortest=1[t2];"
                  f"[3:v]format=rgba[sh];[t2][sh]overlay=0:{HALF}-h/2,fps={FPS},format=yuv420p[v]")
            extra = ['-loop', '1', '-t', f'{dur:.3f}', '-i', mask, '-loop', '1', '-t', f'{dur:.3f}', '-i', shade]
        else:                                               # 'soft': clean separation, soft shadow + faint hairline
            shade = soft_seam_asset(plan)
            hl = float(plan.get('seam_hairline', 0.22))
            fc = (f"[0:v]{cover(W, HALF, face.get('crop'), focus=ffoc, zexpr='+'.join(zt) or None)},{grade}[f];"
                  f"[1:v]{cover(W, HALF, br.get('crop'), bpush, dur, focus=bfoc, src_wh=probe(br['src']))}[b];"
                  f"[f][b]vstack[t2];[2:v]format=rgba[sh];[t2][sh]overlay=0:{HALF}-h/2:shortest=1,"
                  f"drawbox=y={HALF-1}:w={W}:h=2:color=white@{hl}:t=fill,fps={FPS},format=yuv420p[v]")
            extra = ['-loop', '1', '-t', f'{dur:.3f}', '-i', shade]
    else:
        c = br.get('fullcrop', br.get('crop'))
        fc = (f"[1:v]{cover(W, H, c, 0.12 if is_img(br['src']) else 0.06, dur, seg.get('punch', 0.10), tuple(br.get('focus', (0.5, 0.5))), src_wh=probe(br['src']))},"
              f"fps={FPS},format=yuv420p[v]")
        extra = []
    bin_ = (['-loop', '1', '-framerate', str(FPS), '-t', f'{dur:.3f}', '-i', br['src']] if is_img(br['src'])
            else ['-ss', f'{bss:.3f}', '-t', f'{dur:.3f}', '-i', br['src']])
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{fss:.3f}', '-t', f'{dur:.3f}', '-i', face['src'], *bin_, *extra,
         '-filter_complex', fc, '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', out])

# ---------- captions & graphics (ASS) ----------
def ts(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'

def rrect(w, h, r):
    return (f'm {r} 0 l {w-r} 0 b {w} 0 {w} 0 {w} {r} l {w} {h-r} b {w} {h} {w} {h} {w-r} {h} '
            f'l {r} {h} b 0 {h} 0 {h} 0 {h-r} l 0 {r} b 0 0 0 0 {r} 0')

def merge_words(words):
    out = []
    for w in words:
        if out and re.fullmatch(r'\.\d+\.?', w['w']):       # "22" ".5" -> "22.5"
            out[-1]['w'] += w['w']; out[-1]['e'] = w['e']
        else:
            out.append(dict(w))
    return out

def chunks(words, maxw=3, gap=0.35):
    cur = []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (len(cur) >= maxw or re.search(r'[.,!?]$', w['w']) or nxt is None
                or nxt['s'] - w['e'] > gap):
            yield cur; cur = []

def clean(w):
    w = re.sub(r'[^\w.%$#\'*:-]', '', w.upper())
    return re.sub(r'\.$', '', w)

def hex2ass(h):
    h = h.lstrip('#'); return f'&H{h[4:6]}{h[2:4]}{h[0:2]}&'

def caption_events(words, t0, t1, colors=('#FFE11A',), ypos=None):
    """Word-by-word karaoke: the word being spoken lights up; chunk pops in."""
    ev, cols = [], [hex2ass(c) for c in colors]
    words = [w for w in merge_words(words) if w['e'] > t0 and w['s'] < t1]
    cs = list(chunks(words))
    y = ypos or HALF
    for ci, c in enumerate(cs):
        toks = [clean(w['w']) for w in c]
        col = cols[ci % len(cols)]
        nxt = cs[ci + 1][0]['s'] if ci + 1 < len(cs) else t1
        cend = min(c[-1]['e'] + 0.15, nxt, t1)
        for wi, w in enumerate(c):
            a = max(w['s'], t0) - t0
            b = (c[wi + 1]['s'] if wi + 1 < len(c) else cend) - t0
            if b <= a: continue
            txt = ' '.join(f'{{\\c{col}}}{t}{{\\c&HFFFFFF&}}' if i == wi else t for i, t in enumerate(toks))
            anim = r'\fscx70\fscy70\t(0,80,\fscx106\fscy106)\t(80,150,\fscx100\fscy100)' if wi == 0 else ''
            ev.append(f'Dialogue: 5,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\an5\\pos({W//2},{y}){anim}}}{txt}')
    return ev

def stat_card(g):
    """Count-up stat card on the B-roll half: big number + unit + label."""
    s, e, x, y = g['t'], g['t'] + g['dur'], 70, g.get('y', 1560)
    cw, ch = 470, 250
    mv = lambda dx, dy: f'\\move({x-80+dx},{y+dy},{x+dx},{y+dy},0,220)\\fad(140,180)'
    ev = [
        f'Dialogue: 10,{ts(s)},{ts(e)},Gfx,,0,0,0,,{{\\an7{mv(10,14)}\\p1\\bord0\\shad0\\blur14\\1c&H000000&\\1a&H70&}}{rrect(cw,ch,22)}{{\\p0}}',
        f'Dialogue: 11,{ts(s)},{ts(e)},Gfx,,0,0,0,,{{\\an7{mv(0,0)}\\p1\\bord0\\shad0\\1c&H2A1A10&\\1a&H18&}}{rrect(cw,ch,22)}{{\\p0}}',
        f'Dialogue: 12,{ts(s)},{ts(e)},Gfx,,0,0,0,,{{\\an7{mv(0,0)}\\p1\\bord0\\shad0\\1c{GOLD_ASS}}}{rrect(12,ch-60,6)}{{\\p0}}'.replace(f'{y},', f'{y+30},').replace(f'{y})', f'{y+30})'),
        f'Dialogue: 13,{ts(s)},{ts(e)},Label,,0,0,0,,{{\\an7{mv(44,30)}}}{g["label"]}',
        f'Dialogue: 13,{ts(s)},{ts(e)},Unit,,0,0,0,,{{\\an1{mv(44+g.get("unit_x",215),ch-34)}}}{g["unit"]}',
    ]
    val = float(g['value']); dec = len(g['value'].split('.')[1]) if '.' in g['value'] else 0
    steps, cdur = 14, 0.55
    for i in range(steps + 1):
        a = s + cdur * i / steps; b = s + cdur * (i + 1) / steps if i < steps else e
        k = 1 - (1 - i / steps) ** 3
        num = f'{val*k:.{dec}f}'
        mvi = mv(44, ch - 26) if i == 0 else f'\\pos({x+44},{y+ch-26})'
        if i == steps: mvi += r'\t(0,120,\fscx108\fscy108)\t(120,240,\fscx100\fscy100)'
        ev.append(f'Dialogue: 13,{ts(a)},{ts(b)},Num,,0,0,0,,{{\\an1{mvi}{"\\fad(0,180)" if i==steps else ""}}}{num}')
    return ev

def name_card(g):
    """Rank badge + name plate, slides up from the bottom of the B-roll half."""
    s, e, x, y = g['t'], g['t'] + g['dur'], 60, g.get('y', 1700)
    bw, nw, h = 160, max(400, 60 + 40 * len(g['name'])), 150
    mv = lambda dx, dy, d=0: f'\\move({x+dx},{y+dy+60},{x+dx},{y+dy},{d},{d+240})\\fad(120,180)'
    return [
        f'Dialogue: 10,{ts(s)},{ts(e)},Gfx,,0,0,0,,{{\\an7{mv(8,12)}\\p1\\blur14\\1c&H000000&\\1a&H70&}}{rrect(bw+nw,h,18)}{{\\p0}}',
        f'Dialogue: 11,{ts(s)},{ts(e)},Gfx,,0,0,0,,{{\\an7{mv(bw,0,80)}\\p1\\1c&H2A1A10&\\1a&H10&}}{rrect(nw,h,18)}{{\\p0}}',
        f'Dialogue: 12,{ts(s)},{ts(e)},Gfx,,0,0,0,,{{\\an7{mv(0,0)}\\p1\\1c{GOLD_ASS}}}{rrect(bw+20,h,18)}{{\\p0}}',
        f'Dialogue: 13,{ts(s)},{ts(e)},Rank,,0,0,0,,{{\\an5{mv(bw//2+6,h//2)}}}{g["rank"]}',
        f'Dialogue: 13,{ts(s+0.08)},{ts(e)},Name,,0,0,0,,{{\\an4{mv(bw+40,h//2-14,80)}}}{g["name"]}',
        f'Dialogue: 13,{ts(s+0.08)},{ts(e)},Label,,0,0,0,,{{\\an4{mv(bw+42,h//2+36,80)}}}{g.get("sub","")}',
    ]

def write_ass(plan, words, path):
    fonts = plan.get('caption_font', 'Montserrat Black')
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{fonts},86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H50000000,0,0,0,0,100,100,1,0,1,6,3,5,40,40,0,1
Style: Gfx,Arial,10,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Num,Anton,170,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,1,0,0,0,1
Style: Unit,Bebas Neue,96,{GOLD_ASS.replace('&H','&H00')},&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,1,0,0,0,1
Style: Label,Montserrat ExtraBold,34,&H00D8D8D8,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,5,0,1,0,0,7,0,0,0,1
Style: Rank,Anton,96,&H00140C08,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Name,Anton,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    t0 = plan['voice_ss']; t1 = t0 + plan['duration']
    ev = caption_events(words, t0, t1, plan.get('caption_colors', ['#FFE11A']), plan.get('caption_y'))
    for g in plan.get('graphics', []):
        if g['type'] in ('data', 'motion', 'clip'): continue
        ev += stat_card(g) if g['type'] == 'stat' else name_card(g)
    if plan.get('flash', True):
        for sg in plan['segments'][1:]:
            if sg['type'] == 'full' and (plan.get('flash') == 'all' or sg.get('hit')):
                T = sg['start']
                ev.append(f'Dialogue: 30,{ts(T-0.04)},{ts(T+0.22)},Gfx,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\1c&HFFFFFF&\\1a&H70&\\t(40,220,\\1a&HFF&)}}{rrect(W,H,0)}{{\\p0}}')
    open(path, 'w').write(hdr + '\n'.join(ev) + '\n')

# ---------- SFX: restrained, spaced, never repeated back-to-back ----------
# House rules (owner feedback, Nov 2026):
# - B-roll swaps inside the split are SILENT; cuts to full-screen get a soft airy whoosh;
#   a short bass hit only on segments marked "hit"; graphics get one small pop/thud each.
# - NO risers or long cinematic hits (too loud, too drawn out). They're banned below and can't be requested.
# - Sound "moments" are spaced at least `sfx_min_gap` seconds apart (default 3.0): never a sound every 1-2 s.
#   Higher-priority moments (hits, full-screen cuts) win; quieter ones that crowd them are dropped.
# - The same sound file never plays twice in a row (data ticks inside one counter excepted).
# - Every cue gets a small random pitch variation.
POOLS = {
    'air':       ['air_fast_sweeping', 'air_flying_swoosh', 'air_wind_passing', 'air_cine_wind', 'air_zoom_vacuum', 'air_short_wind',
                  'whoosh_cine_fast', 'whoosh_fast_sweep'],
    'air_soft':  ['air_short_wind', 'air_wind_passing', 'air_fast_sweeping', 'whoosh_quick_accent'],
    'impact':    ['impact_short_bass', 'impact_sub_bass_knock', 'impact_futuristic_bass'],
    'pop':       ['pop_hard_click', 'pop_explainer_light', 'pop_dry_notify'],
    'tick':      ['click_box_check'],
    'data_tick': ['tick_scifi', 'tick_tech_select'],
    'thud':      ['thud_wood_hit', 'impact_sub_bass_knock', 'impact_short_bass'],
}
BANNED_SFX = {'riser', 'riser_synth', 'riser_space_stutter', 'impact_big_cine', 'impact_deep_cine_whoosh',
              'impact_quick_zoom', 'impact_trailer_whoosh_hit', 'air_windy_swoosh'}
import random
def sfx_cues(plan):
    """-> list of (sfx name, time where its PEAK lands, volume, rate)"""
    rng = random.Random(plan.get('sfx_seed', 7))
    gap = float(plan.get('sfx_min_gap', 3.0))
    lvl = float(plan.get('sfx_level', 1.0))
    moments = []                     # (anchor t, priority, [(pool|name, t, vol, is_tick)])
    def add(prio, cues):
        if cues: moments.append((min(c[1] for c in cues), prio, cues))
    segs, last_full = plan['segments'], -99
    for prev, nxt in zip(segs, segs[1:]):
        T = nxt['start']
        if nxt.get('sfx') is False: continue
        if nxt['type'] == 'full' and prev['type'] != 'full':
            wl = float(plan.get('whoosh_level', 0.24))
            add(3 if nxt.get('hit') else 2, [('air', T, wl, 0)] + ([('impact', T + 0.02, 0.26, 0)] if nxt.get('hit') and plan.get('hit_sfx', False) else []))
            last_full = T
        elif nxt['type'] != 'full' and prev['type'] == 'full':
            if T - last_full >= 6: add(0, [('air_soft', T, 0.20, 0)])
        elif nxt.get('sfx'):
            add(1, [('air_soft', T, 0.2, 0)])
    graphic_sfx = plan.get('graphic_sfx', False)        # owner: no random loud sounds mid-sentence
    for g in (plan.get('graphics', []) if graphic_sfx else []):
        t0, ev = g['t'], g.get('_ev', {})
        if g['type'] == 'data':
            add(1, [('data_tick', t0 + tk, 0.12, 1) for tk in ev.get('ticks', [])[:3]] + [('pop', t0 + ev['land'], 0.30, 0)])
        elif g['type'] == 'motion':
            first = None
            for key, pool, vol in (('drop', 'pop', 0.30), ('land', 'pop', 0.30), ('air', 'air', 0.28), ('swish', 'air_soft', 0.22)):
                if key in ev: first = (pool, t0 + ev[key] + (0.3 if key == 'air' else 0.25 if key == 'swish' else 0), vol, 0); break
            if first is None and ev.get('pops'): first = ('pop', t0 + ev['pops'][0], 0.26, 0)
            ticks = [('data_tick', t0 + tk, 0.12, 1) for tk in ev.get('ticks', [])[:3]]
            if 'thud' in ev:
                th = ('thud', t0 + ev['thud'], 0.40, 0)
                if first and th[1] - first[1] > 1.0: add(1, ticks + [first]); add(1, [th])
                else: add(1, ticks + [th])
            elif first: add(1, ticks + [first])
        elif g['type'] in ('name', 'stat'):
            add(1, [('pop', t0 + 0.05, 0.26, 0)])
    for c in (plan.get('extra_sfx', []) if plan.get('extra_sfx_on', False) else []):
        if c[0] in BANNED_SFX: print(f"NOTE: extra_sfx '{c[0]}' is banned (owner: too loud/drawn out), skipped"); continue
        add(1, [(c[0], c[1], c[2], 0)])
    # spacing: keep highest-priority moments first, then anything that is >= gap from every kept moment
    kept = []
    for m in sorted(moments, key=lambda m: (-m[1], m[0])):
        if all(abs(m[0] - k[0]) >= gap for k in kept): kept.append(m)
    kept.sort(key=lambda m: m[0])
    # resolve sound names chronologically; never the same file twice in a row
    rot = {k: rng.randrange(len(v)) for k, v in POOLS.items()}
    out, last = [], None
    for _, _, cues in kept:
        for src, t, vol, tick in sorted(cues, key=lambda c: c[1]):
            if src in POOLS:
                pool = POOLS[src]
                for _ in range(len(pool)):
                    name = pool[rot[src] % len(pool)]; rot[src] += 1
                    if tick or name != last: break
            else: name = src
            if name in BANNED_SFX: continue
            if not tick: last = name
            out.append((name, t, vol))
    print(f"SFX: {len(kept)} moments kept of {len(moments)} (min gap {gap:.1f}s): " +
          ', '.join(f"{t:.1f}s {n}" for n, t, _ in out if not n.startswith('tick')))
    return [(n, t, v * lvl, round(rng.uniform(0.92, 1.08), 3)) for n, t, v in out]

def choose_transitions(plan):
    """Pick a transition per boundary. A segment can force one with "transition": "whip:left" / "zoom" / "cut" / ...
    Auto rules (house style, viral but varied):
      into full-screen   -> rotate zoom, whip-left, spin, whip-up   ("hit" segments: flash / shake)
      out of full-screen -> rotate whip-down, zoom, whip-right, glitch
      full -> full       -> rotate whip-left, glitch, whip-right
      split -> split     -> bottom-half swipe (left/right alternating); your face never moves"""
    rot = {'in': ['zoom', 'whip:left', 'spin', 'whip:up'], 'hit': ['flash', 'shake'], 'out': ['whip:down', 'zoom', 'whip:right', 'glitch'],
           'ff': ['whip:left', 'glitch', 'whip:right'], 'ss': ['swipe:left', 'swipe:right']}
    cnt = {k: 0 for k in rot}
    def take(k):
        v = rot[k][cnt[k] % len(rot[k])]; cnt[k] += 1; return v
    segs, out = plan['segments'], [None]
    for prev, nxt in zip(segs, segs[1:]):
        if 'transition' in nxt and nxt['transition'] in transitions.DUR or ':' in str(nxt.get('transition', '')):
            spec = nxt['transition']
        elif nxt['type'] == 'full' and prev['type'] != 'full': spec = take('hit') if nxt.get('hit') else take('in')
        elif nxt['type'] != 'full' and prev['type'] == 'full': spec = take('out')
        elif nxt['type'] == 'full': spec = take('ff')
        else: spec = take('ss') if plan.get('split_swipes', True) else 'cut'
        k, _, dr = spec.partition(':')
        out.append((k, dr or None, 'bottom' if k == 'swipe' else None))
    return out

def main(plan_path):
    global GOLD_ASS
    here0 = os.path.dirname(os.path.abspath(__file__))
    style = json.load(open(f'{here0}/style.json')) if os.path.exists(f'{here0}/style.json') else {}
    style = {k: (os.path.join(here0, v) if k in ('fontsdir', 'sfxdir') and not os.path.isabs(v) else v)
             for k, v in style.items() if not k.startswith('_')}
    plan = {**style, **json.load(open(plan_path))}
    if plan['duration'] < plan.get('min_duration', 0):
        print(f"WARNING: {plan['duration']:.1f}s is under the {plan['min_duration']}s minimum")
    if plan.get('accent'): GOLD_ASS = hex2ass(plan['accent'])
    if not plan.get('skip_res_check'): check_sources(plan, plan.get('min_broll_short_side', 1080))
    wd = plan['workdir']; os.makedirs(wd, exist_ok=True)
    segs = plan['segments']; end = plan['duration']
    # 1) segments, each rendered with PAD s of overlap on both sides so any transition can use it
    PAD = 0.25
    parts = []
    for i, s in enumerate(segs):
        a = max(0.0, s['start'] - PAD) if i else 0.0
        b = min(end, segs[i + 1]['start'] + PAD) if i + 1 < len(segs) else end
        key = json.dumps([s, round(a, 3), round(b, 3), plan['face'], plan.get('zooms'), plan.get('seam_style'), plan.get('seam_feather'), plan.get('seam_shade'), plan.get('seam_soft'), plan.get('seam_shadow'), plan.get('seam_hairline'),
                          plan.get('face_grade'), plan.get('voice_ss'), plan.get('accent')], sort_keys=True)
        p = f'{wd}/seg_{hashlib.md5(key.encode()).hexdigest()[:12]}.mp4'
        if not cached(p, b - a): render_segment(plan, s, a, b, p)
        parts.append((p, a, b))
    # 2) transitions: short standalone clips built from the overlap, then everything is concatenated
    trs = choose_transitions(plan)                     # [(kind, direction, half)] per boundary (index 0 unused)
    dur = [0.0] + [transitions.DUR[k] for k, _, _ in trs[1:]]
    inputs, fc, pieces = [], [], []
    for i, (p, a, b) in enumerate(parts):
        inputs += ['-i', p]
    for i in range(len(parts)):
        a_i = parts[i][1]
        if i:
            k, dr, half = trs[i]
            if dur[i] > 0:
                d = dur[i]; T = segs[i]['start']
                key = json.dumps([k, dr, half, parts[i - 1][0], parts[i][0], round(T, 3), d])
                tp = f"{wd}/tr_{hashlib.md5(key.encode()).hexdigest()[:12]}.mp4"
                if not cached(tp, d - 0.05):
                    transitions.render(k, parts[i - 1][0], T - d / 2 - parts[i - 1][1], parts[i][0], T - d / 2 - a_i, d, tp, dr, half)
                n = len(inputs) // 2; inputs += ['-i', tp]
                pieces.append(f'[{n}:v]setpts=PTS-STARTPTS,setsar=1[t{i}]'); fc.append(pieces[-1]); pieces[-1] = f'[t{i}]'
        s0 = (segs[i]['start'] + dur[i] / 2 - a_i) if i else 0.0
        s1 = (segs[i + 1]['start'] - dur[i + 1] / 2 - a_i) if i + 1 < len(segs) else end - a_i
        fc.append(f'[{i}:v]trim=start={s0:.4f}:end={s1:.4f},setpts=PTS-STARTPTS,setsar=1[b{i}]'); pieces.append(f'[b{i}]')
    fc.append(''.join(pieces) + f'concat=n={len(pieces)}:v=1:a=0,fps={FPS}[x0]'); last = 'x0'
    here = os.path.dirname(os.path.abspath(__file__))
    for gi, g in enumerate(plan.get('graphics', [])):
        if g['type'] == 'clip':
            n = len(inputs) // 2; inputs += ['-i', g['src']]
            key = {'green': ',colorkey=0x00FF00:0.32:0.08', 'black': ',colorkey=0x000000:0.12:0.06'}.get(g.get('key'), '')
            cw = int(g.get('w', W)); x = g.get('x', (W - cw) // 2); y = g.get('y', HALF + 40)
            fc.append(f"[{n}:v]trim=start={g.get('ss',0)}:duration={g['dur']},setpts=PTS-STARTPTS+{g['t']:.3f}/TB,scale={cw}:-2,format=rgba{key}[cl{gi}];"
                      f"[{last}][cl{gi}]overlay=x={x}:y={y}:eof_action=pass[cv{gi}]"); last = f'cv{gi}'; continue
        if g['type'] not in ('data', 'motion'): continue
        spec = {k: v for k, v in g.items() if not k.startswith('_') and k not in ('type', 't')}
        spec.update(fontsdir=os.path.abspath(plan['fontsdir']), accent=plan.get('accent', '#E8231E'),
                    accent2=(plan.get('caption_colors') or ['#FFE11A'])[-1])
        if g['type'] == 'motion': spec['page'] = 'motion.html'
        sp, mov = f'{wd}/data{gi:02d}.json', f'{wd}/data{gi:02d}.mov'
        h12 = hashlib.md5(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:12]
        sp, mov = f'{wd}/gfx_{h12}.json', f'{wd}/gfx_{h12}.mov'
        if not cached(mov, g['dur'] - 0.1):
            json.dump(spec, open(sp, 'w'))
            r = subprocess.run(['node', f'{here}/datagfx/render.js', sp, mov], capture_output=True, text=True)
            if r.returncode: sys.exit('graphic failed: ' + r.stderr[-2000:])
        info = json.load(open(mov[:-4] + '.json')); g['_ev'] = info['events']
        seg = [sg for sg in segs if sg['start'] <= g['t']][-1]
        gw, gh = info['w'], info['h']
        anchor = g.get('anchor', 'lower')
        if info.get('full'): y = 0
        elif g.get('y') is not None: y = g['y']
        elif anchor == 'upper': y = 230 if seg['type'] == 'full' else max(40, HALF // 2 - gh // 2)
        elif anchor == 'center': y = (H - gh) // 2
        elif seg['type'] == 'split': y = max(HALF + 30, HALF + HALF // 2 - gh // 2)
        else: y = max(HALF + 50, H - 100 - gh)
        n = len(inputs) // 2; inputs += ['-i', mov]
        fc.append(f"[{n}:v]setpts=PTS-STARTPTS+{g['t']:.3f}/TB[dg{gi}];[{last}][dg{gi}]overlay=x={0 if info.get('full') else g.get('x', (W-gw)//2)}:y={y}:eof_action=pass[dv{gi}]")
        last = f'dv{gi}'
    ass = f'{wd}/gfx.ass'
    write_ass(plan, json.load(open(plan['words'])), ass)
    fontsdir = plan['fontsdir']
    fc.append(f"[{last}]ass={ass}:fontsdir={fontsdir},format=yuv420p[v]")
    # 3) audio: voice + sfx -> mastered WAV (two-pass, LINEAR loudness normalisation: no pumping)
    VOICE = {
        # natural: no noise reduction (it made the voice watery/muffled), gentle de-mud + air, light 2:1 compression
        'natural': 'highpass=f=70,equalizer=f=320:t=q:w=1.0:g=-1.5,equalizer=f=4500:t=h:w=0.7:g=2,'
                   'acompressor=threshold=-18dB:ratio=2:attack=15:release=200:makeup=1.5',
        'original': 'anull',          # HOUSE DEFAULT: the owner's untouched voice (EQ/compression took the bass out)
        'raw': 'anull',
        'denoise': 'highpass=f=70,afftdn=nf=-40:nr=6,equalizer=f=4500:t=h:w=0.7:g=2,acompressor=threshold=-18dB:ratio=2:attack=15:release=200',
    }
    vchain = VOICE.get(plan.get('voice_chain', 'original'), plan.get('voice_chain'))
    ain = ['-ss', str(plan['voice_ss']), '-t', str(end), '-i', plan['face']['src']]
    cues = sfx_cues(plan); mix = [f'[0:a]{vchain}[vo]']
    meta = json.load(open(f"{plan['sfxdir']}/sfx.json"))
    for j, (name, t, vol, rate) in enumerate(cues):
        ain += ['-i', f"{plan['sfxdir']}/{name}.wav"]
        st = t - meta[name]['peak'] / rate               # start so the (re-pitched) peak lands on t
        trim = f'atrim=start={-st:.3f},asetpts=PTS-STARTPTS,' if st < 0 else ''
        mix.append(f'[{1+j}:a]asetrate={int(48000*rate)},aresample=48000,{trim}volume={vol:.3f},adelay={int(max(st,0)*1000)}:all=1[s{j}]')
    # ambience beds (plan "ambience"): quiet looped atmospheres under a stretch of the story (e.g. campfire crackle,
    # night crickets). Each is levelled to its own target loudness ("lufs", default -34) far below the -14 voice, faded in/out.
    amb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'ambience')
    beds = []
    for k, a in enumerate(plan.get('ambience', [])):
        src = f"{amb_dir}/{a['src']}.wav"
        lm = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
        g = float(a.get('lufs', -34)) - float(re.findall(r'I:\s+(-?[\d.]+) LUFS', lm)[-1])
        d = a['end'] - a['t']; f = min(float(a.get('fade', 1.0)), d / 2)
        ain += ['-stream_loop', '-1', '-i', src]
        mix.append(f"[{1+len(cues)+k}:a]atrim=0:{d:.3f},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d={f:.2f},"
                   f"afade=t=out:st={d-f:.3f}:d={f:.2f},volume={g:.2f}dB,adelay={int(a['t']*1000)}:all=1[b{k}]")
        beds.append(f'[b{k}]')
    others = [f'[s{j}]' for j in range(len(cues))] + beds
    def measure(graph):
        m = subprocess.run(['ffmpeg', '-hide_banner', *ain, '-filter_complex', graph + ',ebur128=framelog=quiet:peak=sample[a]',
                            '-map', '[a]', '-f', 'null', '-'], capture_output=True, text=True).stderr
        return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.inf]+) dBFS', m)[-1])
    def graph(vg, fg):
        g = list(mix)
        if not others: return ';'.join(g) + f';[vo]volume={vg:.2f}dB'
        g.append(f'[vo]volume={vg:.2f}dB,asplit[vg][key]')
        # sfx/beds duck briefly under loud words (sidechain on the voice), so they never stack on a voice peak
        g.append(''.join(others) + f'amix=inputs={len(others)}:normalize=0,volume={fg:.2f}dB[fxr]')
        g.append('[fxr][key]sidechaincompress=threshold=0.12:ratio=6:attack=3:release=180:makeup=1[fx]')
        return ';'.join(g) + ';[vg][fx]amix=inputs=2:normalize=0:duration=first'
    # The voice is judged ON ITS OWN (not the sum with sfx/beds), so the extra sounds can never cause it to be turned down.
    # NEVER turn the owner's voice down: a take at or above -14 LUFS passes through bit-for-bit (no gain, no limiter);
    # a quiet take gets one static boost to -14, with a limiter only then.
    li, vpk = measure(';'.join(mix[:1]) + ';[vo]anull')
    fxg = 0.0
    if -14.0 - li > 0.05:
        gain = -14.0 - li
        ln = 'alimiter=limit=0.84:attack=5:release=50:level=false'   # -1.5 dBFS: AAC overshoots ~1 dB on transients
    else:
        # Untouched, except: a take that peaks right at 0 dBFS gets the minimum static trim to a -0.5 dBFS peak.
        # Measured: ffmpeg's AAC encoder squashes full-scale audio (-0.3 dB quieter + audible crunch, residual -27 dB);
        # with 0.5 dB headroom the encode is clean (residual -41 dB) and the level change is below audibility.
        gain = min(0.0, -0.5 - vpk); ln = 'anull'
        # ducking keeps the SUM within ~0.2 dB of the voice peak; if it still goes over -0.3 dBFS, turn down the sfx/beds, never the voice
        while others and fxg > -12 and measure(graph(gain, fxg))[1] > -0.3: fxg -= 1.5
    print(f'voice: {li:.1f} LUFS, peak {vpk:.1f} dBFS, static gain {gain:+.2f} dB' + (', limiter' if gain > 0.05 else ', no limiter')
          + (f'; sfx/beds {fxg:+.1f} dB to avoid clipping' if fxg else ''))
    mixed = graph(gain, fxg) + (f',{ln}' if ln != 'anull' else '')
    awav = f'{wd}/mix.wav'
    run(['ffmpeg', '-v', 'error', '-y', *ain, '-filter_complex', mixed + ',aresample=48000[a]',
         '-map', '[a]', '-t', str(end), '-c:a', 'pcm_s16le', awav])
    ai = len(inputs) // 2
    inputs += ['-i', awav]
    run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc),
         '-map', '[v]', '-map', f'{ai}:a', '-t', str(end), '-c:v', 'libx264', '-crf', '17', '-preset', 'slow',
         '-profile:v', 'high', '-r', str(FPS), '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
         '-movflags', '+faststart', plan['output']])
    print('wrote', plan['output'])

if __name__ == '__main__':
    main(sys.argv[1])
