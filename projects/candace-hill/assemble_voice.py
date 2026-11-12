"""Assemble the Candace Hill voiceover: 8 voice parts in story order (no inserts).
Voice: never turned down. Parts under -14 LUFS get one static gain to -14 plus a peak limiter; a part that peaks
over full scale gets the minimum static trim to a -0.5 dBFS peak. Long pauses (>1.0 s) are shortened to 0.65 s.
usage: python3 assemble_voice.py <scratch mb dir>"""
import json, re, subprocess, sys
M = sys.argv[1]; R, WK, YT = f'{M}/raw', f'{M}/work', f'{M}/yt'
SR = 48000
def sh(c): 
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])
    return r
def loud(src, ss=None, to=None):
    a = ['ffmpeg', '-nostats'] + (['-ss', str(ss), '-to', str(to)] if ss is not None else []) + ['-i', src, '-af', 'ebur128=peak=true', '-f', 'null', '-']
    e = subprocess.run(a, capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]); P = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])
    return I, P

# pieces: (kind, src, ss, se, words-json or None, label)
P = lambda n: ('voice', f'{R}/p{n}.m4a', None, None, f'{WK}/w_p{n}.json', f'p{n}')
pieces = [P(i) for i in range(1, 9)]
GAP_PART, GAP_INSERT = 0.5, 0.45

def ranges_for(words, a, b):
    """keep [a,b] but shorten pauses > 0.62 s to 0.42 s"""
    ws = [w for w in words if w['s'] >= a - 0.01 and w['e'] <= b + 0.01]
    out, s = [], a
    for i in range(len(ws) - 1):
        g0, g1 = ws[i]['e'], ws[i + 1]['s']
        if g1 - g0 > 0.62:
            out.append((s, g0 + 0.22)); s = g1 - 0.2
    out.append((s, b)); return out

timeline, allw, segs, t = [], [], [], 0.0
gain_cache = {}
for k, (kind, src, ss, se, wj, label) in enumerate(pieces):
    W = json.load(open(wj))
    if kind.startswith('voice'):
        a = (W[0]['s'] - 0.18) if ss is None else ss
        b = (W[-1]['e'] + 0.30) if se is None else se
        if kind == 'voice8a': b = 20.20
        rng = ranges_for(W, a, b)
        if src not in gain_cache:
            I, Pk = loud(src)
            if I < -14.0: g, lim = -14.0 - I, True
            elif Pk > -0.5: g, lim = -0.5 - Pk, False
            else: g, lim = 0.0, False
            gain_cache[src] = (g, lim, I, Pk)
        g, lim, I, Pk = gain_cache[src]
    else:
        rng = [(ss, se)]
        I, Pk = loud(src, ss, se)
        g, lim = -16.0 - I, True       # archival audio sits just under the voice
    gap = 0.0 if k == 0 else (GAP_INSERT if (kind in ('nbc', 'abc') or pieces[k-1][0] in ('nbc', 'abc')) else GAP_PART)
    if kind == 'voice8b': gap = 0.35
    t += gap
    start = t
    for (r0, r1) in rng:
        for w in W:
            if w['s'] >= r0 - 0.01 and w['s'] < r1 - 0.05:
                allw.append({'w': w['w'], 's': round(t + w['s'] - r0, 3), 'e': round(t + min(w['e'], r1) - r0, 3), 'src': label})
        segs.append((src, r0, r1, g, lim))
        t += r1 - r0
    timeline.append({'label': label, 'kind': kind, 'src': src, 'out_s': round(start, 3), 'out_e': round(t, 3),
                     'ranges': rng, 'gain_db': round(g, 2), 'limiter': lim})
    print(f'{label:12s} {start:7.2f}-{t:7.2f}  gain {g:+.2f} dB{" +lim" if lim else ""}')

# render: each range -> wav, then concat with silence gaps (positions exact via adelay+amix)
inputs, fc = [], []
for i, (src, r0, r1, g, lim) in enumerate(segs):
    inputs += ['-ss', f'{r0:.3f}', '-to', f'{r1:.3f}', '-i', src]
cur, i, parts = 0.0, 0, []
pos = []
for tl in timeline:
    acc = tl['out_s']
    for (r0, r1) in tl['ranges']:
        pos.append(acc); acc += r1 - r0
for i, (src, r0, r1, g, lim) in enumerate(segs):
    chain = f'[{i}:a]aresample={SR},aformat=channel_layouts=stereo,volume={g:.3f}dB'
    if lim: chain += ',alimiter=limit=0.944:attack=1:release=50:level=false'
    d = r1 - r0
    chain += f',afade=t=in:d=0.012,afade=t=out:st={d-0.012:.3f}:d=0.012,adelay={int(pos[i]*1000)}|{int(pos[i]*1000)}[a{i}]'
    fc.append(chain)
fc.append(''.join(f'[a{i}]' for i in range(len(segs))) + f'amix=inputs={len(segs)}:normalize=0:dropout_transition=0,atrim=0:{t+0.6:.3f}[out]')
sh(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s24le', f'{WK}/voice.wav'])

# caption fixes (names, numbers, censoring)
def fix(ws):
    out = []
    for w in ws:
        x = w['w']
        if out and re.fullmatch(r'-\d+[.,?]?', x) and re.fullmatch(r'\d+', out[-1]['w']):
            out[-1]['w'] += '.' + x[1:]; out[-1]['e'] = w['e']; continue
        if out and re.fullmatch(r"'all[.,]?", x) and out[-1]['w'].lower() == 'y':
            out[-1]['w'] = "y'" + x[1:]; out[-1]['e'] = w['e']; continue
        if out and x in ('.S.', '.S.,') and out[-1]['w'] == 'U':
            out[-1]['w'] = 'U.S.'; out[-1]['e'] = w['e']; continue
        out.append(dict(w))
    rep = {'1098': '10.98', '1098.': '10.98.', '1098,': '10.98,', '2243': '22.43', '2243.': '22.43.', '1107.': '11.07.', '1107': '11.07',
           'Roxdale': 'Rockdale', 'Smith': 'MileSplit', 'Aaron': 'Erin', 'Shavers': 'Shaver', 'Alia': 'Aleia'}
    o2 = []
    for i, w in enumerate(out):
        x = w['w']
        if x in rep: w['w'] = rep[x]
        if x == 'Miles' and i + 1 < len(out) and out[i + 1]['w'] == 'Smith': continue
        if x.lower() == 'win' and i + 1 < len(out) and out[i + 1]['w'].lower().startswith(('was', 'so')) : w['w'] = 'wind'
        if x.lower() in ('win.', 'win,') and i > 0 and out[i - 1]['w'].lower() == 'legal': w['w'] = 'wind' + x[3:]
        if x == 'GoPro,':
            m = (w['s'] + w['e']) / 2
            o2 += [dict(w, w='go', e=m), dict(w, w='pro,', s=m)]; continue
        if x in ('-Am', '-20', '-20,', '-time'):
            o2[-1]['w'] += {'-Am': ' Am', '-time': '-time'}.get(x, x.replace('-', '')); o2[-1]['e'] = w['e']; continue
        o2.append(w)
    # "goes out and win the semis" -> "goes out in the semis"
    for i in range(len(o2) - 1):
        if o2[i]['w'] == 'and' and o2[i + 1]['w'] == 'win' and i > 0 and o2[i - 1]['w'] == 'out':
            o2[i]['w'] = 'in'; o2[i]['e'] = o2[i + 1]['e']; o2[i + 1]['w'] = ''
    return [w for w in o2 if w['w']]
allw = fix(allw)
json.dump(allw, open(f'{WK}/words.json', 'w'))
json.dump(timeline, open(f'{WK}/timeline.json', 'w'), indent=1)
print('total', round(t, 2), 's;', len(allw), 'words')
