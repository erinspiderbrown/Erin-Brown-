"""TikTok editor: split-screen (talking head top / B-roll bottom) <-> full-screen B-roll.

Usage: python3 build.py plan.json
All times in the plan are OUTPUT seconds (0 = start of edit), except *_ss fields which are source seek times.
"""
import json, os, re, subprocess, sys

W, H, FPS, D = 1080, 1920, 30, 0.30          # canvas, fps, transition duration
HALF = H // 2
GOLD_ASS = '&H2CC7FF&'                        # #FFC72C in ASS BGR

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stderr[-3000:]}")

IMG = ('.jpg', '.jpeg', '.png', '.webp', '.heic')
def is_img(p): return p.lower().endswith(IMG)

def cover(w, h, crop=None, push=0.0, dur=1.0, punch=0.0):
    """crop source region, scale to cover w x h, optional slow push-in."""
    f = []
    if crop: f.append('crop=%d:%d:%d:%d' % tuple(crop))
    f.append(f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos')
    f.append(f'crop={w}:{h}')
    if push or punch:
        z = f"(1+{push}*t/{dur}+{punch}*pow(max(0,1-t/0.28),2))"
        f.append(f"scale=w='trunc({w}*{z}/2)*2':h=-2:eval=frame:flags=bicubic,crop={w}:{h}")
    f.append('unsharp=5:5:0.6:5:5:0,setsar=1')
    return ','.join(f)

_probe = {}
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

def fit_blur(br, dur):
    """Landscape clip full-screen without upscaling mush: sharp clip centred over a blurred, dimmed fill."""
    c = br.get('crop'); pre = ('crop=%d:%d:%d:%d,' % tuple(c)) if c else ''
    sw, sh = c[:2] if c else probe(br['src']); fh = int(W * sh / sw) // 2 * 2
    return (f"[1:v]{pre}split[fa][fb];"
            f"[fa]scale={W//4}:{H//4}:force_original_aspect_ratio=increase,crop={W//4}:{H//4},boxblur=20:3,"
            f"scale={W}:{H},eq=brightness=-0.12:saturation=1.1[bg];"
            f"[fb]scale={W}:-2:flags=lanczos,scale=w='trunc({W}*(1+0.05*t/{dur})/2)*2':h=-2:eval=frame,crop={W}:{fh},unsharp=5:5:0.4[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2:shortest=1,setsar=1")

def render_segment(plan, seg, a, b, out):
    face, br = plan['face'], seg['broll']
    fss = plan['voice_ss'] + a                 # face stays lip-synced to voice
    bss = max(0.0, br['ss'] + (a - seg['start']))
    dur = b - a
    grade = plan.get('face_grade', 'hqdn3d=1.5:1.5:4:4,eq=contrast=1.06:saturation=1.06:gamma=0.98,vignette=PI/6')
    bpush = 0.10 if is_img(br['src']) else 0.04
    if seg['type'] == 'split':
        fc = (f"[0:v]{cover(W, HALF, face.get('crop'))},{grade}[f];"
              f"[1:v]{cover(W, HALF, br.get('crop'), bpush, dur)}[b];"
              f"[f][b]vstack,"
              f"drawbox=y={HALF+3}:w={W}:h=12:color=black@0.35:t=fill,"
              f"drawbox=y={HALF-3}:w={W}:h=6:color=0x{plan.get('accent','#FFC72C').lstrip(chr(35))}:t=fill,fps={FPS},format=yuv420p[v]")
    else:
        sw, sh = probe(br['src']); c = br.get('fullcrop', br.get('crop'))
        cw, ch = (c[0], c[1]) if c else (sw, sh)
        upscale = max(W / cw, H / ch)
        if upscale > 1.2 and not seg.get('force_cover'):
            fc = f"{fit_blur(br, dur)},fps={FPS},format=yuv420p[v]"
        else:
            fc = (f"[1:v]{cover(W, H, c, 0.12 if is_img(br['src']) else 0.06, dur, seg.get('punch', 0.10))},"
                  f"fps={FPS},format=yuv420p[v]")
    bin_ = (['-loop', '1', '-framerate', str(FPS), '-t', f'{dur:.3f}', '-i', br['src']] if is_img(br['src'])
            else ['-ss', f'{bss:.3f}', '-t', f'{dur:.3f}', '-i', br['src']])
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{fss:.3f}', '-t', f'{dur:.3f}', '-i', face['src'], *bin_,
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
    w = re.sub(r'[^\w.%$#\'-]', '', w.upper())
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
        ev += stat_card(g) if g['type'] == 'stat' else name_card(g)
    open(path, 'w').write(hdr + '\n'.join(ev) + '\n')

# ---------- audio ----------
# ---------- SFX (Mixkit library, peak-aligned, rotated so nothing repeats back-to-back) ----------
POOLS = {
    'whoosh_in':  ['whoosh_cine_fast', 'whoosh_fast_sweep', 'whoosh_air_sweep', 'whoosh_small_sweep', 'whoosh_flying_fast'],
    'whoosh_out': ['whoosh_quick_accent', 'whoosh_cine_fast2', 'whoosh_fast_trans'],
    'whoosh_cut': ['whoosh_fast_trans2', 'whoosh_speeding'],
    'impact':     ['impact_short_bass', 'impact_sub_bass_knock', 'impact_futuristic_bass', 'impact_trailer_whoosh_hit'],
    'pop':        ['pop_hard_click', 'pop_explainer_light'],
    'tick':       ['click_box_check'],
    'photo':      ['click_camera_shutter'],
    'riser':      ['riser_synth', 'riser_space_stutter'],
}
def sfx_cues(plan):
    """-> list of (sfx name, timeline time where the SFX PEAK should land, volume)"""
    rot = {k: 0 for k in POOLS}
    def pick(pool):
        n = POOLS[pool][rot[pool] % len(POOLS[pool])]; rot[pool] += 1; return n
    cues, segs = [], plan['segments']
    for prev, nxt in zip(segs, segs[1:]):
        T = nxt['start']
        if nxt['type'] == 'full':
            cues += [(pick('whoosh_in'), T, 0.50), (pick('impact'), T + 0.02, 0.42)]
        elif prev['type'] == 'full':
            cues.append((pick('whoosh_out'), T, 0.40))
        else:
            cues.append((pick('whoosh_cut'), T, 0.30))
        if is_img(nxt['broll']['src']): cues.append((pick('photo'), T + 0.05, 0.35))
    for g in plan.get('graphics', []):
        cues.append((pick('pop'), g['t'] + 0.05, 0.45))
        if g['type'] == 'stat': cues.append((pick('tick'), g['t'] + 0.56, 0.35))
    for c in plan.get('extra_sfx', []):            # e.g. ["riser", 12.0, 0.4] -> pool or file name
        cues.append((pick(c[0]) if c[0] in POOLS else c[0], c[1], c[2]))
    return cues

def main(plan_path):
    global GOLD_ASS
    plan = json.load(open(plan_path))
    if plan.get('accent'): GOLD_ASS = hex2ass(plan['accent'])
    if not plan.get('skip_res_check'): check_sources(plan)
    wd = plan['workdir']; os.makedirs(wd, exist_ok=True)
    segs = plan['segments']; end = plan['duration']
    # 1) segments with D/2 overlap on each inner boundary
    parts = []
    for i, s in enumerate(segs):
        a = s['start'] - (D / 2 if i else 0)
        b = (segs[i + 1]['start'] + D / 2) if i + 1 < len(segs) else end
        p = f'{wd}/seg{i:02d}.mp4'; render_segment(plan, s, a, b, p); parts.append((p, a, b))
    # 2) xfade chain
    inputs, fc, last = [], [], '0:v'
    for i, (p, a, b) in enumerate(parts):
        inputs += ['-i', p]
    for i in range(1, len(parts)):
        tr = segs[i].get('transition', 'smoothup' if segs[i]['type'] == 'full' else 'smoothdown')
        off = parts[i][1]
        fc.append(f'[{last}][{i}:v]xfade=transition={tr}:duration={D}:offset={off:.3f}[x{i}]'); last = f'x{i}'
    ass = f'{wd}/gfx.ass'
    write_ass(plan, json.load(open(plan['words'])), ass)
    fontsdir = plan['fontsdir']
    fc.append(f"[{last}]ass={ass}:fontsdir={fontsdir},format=yuv420p[v]")
    # 3) audio: voice + sfx
    ai = len(parts)
    inputs += ['-ss', str(plan['voice_ss']), '-t', str(end), '-i', plan['face']['src']]
    cues = sfx_cues(plan); mix = [f'[{ai}:a]highpass=f=80,afftdn=nf=-28,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=10000:t=h:w=0.7:g=1.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,alimiter=limit=0.95[vo]']
    meta = json.load(open(f"{plan['sfxdir']}/sfx.json"))
    for j, (name, t, vol) in enumerate(cues):
        inputs += ['-i', f"{plan['sfxdir']}/{name}.wav"]
        st = t - meta[name]['peak']                       # start so the peak lands on t
        trim = f'atrim=start={-st:.3f},asetpts=PTS-STARTPTS,' if st < 0 else ''
        mix.append(f'[{ai+1+j}:a]{trim}volume={vol},adelay={int(max(st,0)*1000)}:all=1[s{j}]')
    mix.append(''.join(['[vo]'] + [f'[s{j}]' for j in range(len(cues))]) +
               f'amix=inputs={len(cues)+1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.0:LRA=9[a]')
    run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc + mix),
         '-map', '[v]', '-map', '[a]', '-t', str(end), '-c:v', 'libx264', '-crf', '17', '-preset', 'slow',
         '-profile:v', 'high', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', plan['output']])
    print('wrote', plan['output'])

if __name__ == '__main__':
    main(sys.argv[1])
