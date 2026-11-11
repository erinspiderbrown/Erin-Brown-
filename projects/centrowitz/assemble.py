"""Top track for the Centrowitz edit: the owner's tightened take with two soundbites from the Tracksmith film
(Matt Centrowitz Sr. voiceover over the film's own, AI-upscaled pictures) cut in.
Owner's audio is untouched. The film audio gets one static gain to the owner's loudness (it's not the owner's voice).
usage: python3 assemble.py <v9 dir>"""
import json, re, subprocess, sys
V = sys.argv[1]; W = f'{V}/work'
def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])
    return r
def lufs(src, ss=None, d=None):
    a = ['ffmpeg', '-nostats'] + (['-ss', str(ss), '-t', str(d)] if ss is not None else []) + ['-i', src, '-af', 'ebur128', '-f', 'null', '-']
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', subprocess.run(a, capture_output=True, text=True).stderr)[-1])
face = f'{W}/face_tight.mov'; fw = json.load(open(f'{W}/words_tight.json'))
cw = json.load(open(f'{V}/w_clip1.json'))
owner_I = lufs(face)
# (kind, src video, video ss, dur, audio src, audio ss, words)
CUT_A, CUT_B = 21.95, 53.25
bites = {'A': (f'{V}/up/biteA.mp4', 0.0, 10.2, f'{V}/raw/clip1.mp4', 16.8),
         'B': (f'{V}/up/biteB.mp4', 0.0, 8.9, f'{V}/raw/clip1.mp4', 106.3)}
pieces = [('face', 0.0, CUT_A), ('A',), ('face', CUT_A, CUT_B), ('B',), ('face', CUT_B, None)]
D = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', face]).stdout)
parts, words, t, tl = [], [], 0.0, []
for i, p in enumerate(pieces):
    out = f'{W}/part{i}.mov'
    if p[0] == 'face':
        a, b = p[1], (p[2] if p[2] is not None else D); d = b - a
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', face, '-c:v', 'libx264', '-crf', '12', '-preset', 'fast',
             '-c:a', 'pcm_s24le', '-ar', '48000', '-ac', '2', out])
        words += [dict(x, s=round(x['s'] - a + t, 3), e=round(x['e'] - a + t, 3)) for x in fw if a <= x['s'] < b]
    else:
        vs, vss, d, asrc, ass = bites[p[0]]
        g = owner_I - lufs(asrc, ass, d)
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{vss:.3f}', '-t', f'{d:.3f}', '-i', vs, '-ss', f'{ass:.3f}', '-t', f'{d:.3f}', '-i', asrc,
             '-filter_complex', f"[0:v]scale=1440:1280:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:1280,fps=30,setsar=1[v];"
                                f"[1:a]volume={g:.2f}dB,alimiter=limit=0.944:level=false,afade=t=in:d=0.04,afade=t=out:st={d-0.06:.3f}:d=0.06[a]",
             '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-c:a', 'pcm_s24le', '-ar', '48000', '-ac', '2', out])
        words += [dict(x, s=round(x['s'] - ass + t, 3), e=round(min(x['e'], ass + d) - ass + t, 3), guest=True) for x in cw if ass <= x['s'] < ass + d - 0.05]
        print(f'bite {p[0]}: gain {g:+.2f} dB')
    tl.append({'piece': p[0], 'out_s': round(t, 3), 'out_e': round(t + d, 3)}); t += d; parts.append(out)
lst = f'{W}/parts.txt'; open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', f'{W}/face_final.mov'])
fix = {'central.': 'Centrowitz.', 'shit': 'SH*T'}
for x in words:
    x['w'] = fix.get(x['w'], x['w'])
out = []
for x in words:
    if out and x['w'].startswith("'all") and out[-1]['w'].lower() == 'y': out[-1]['w'] = "y'" + x['w'][1:]; out[-1]['e'] = x['e']; continue
    out.append(x)
json.dump(out, open(f'{W}/words_final.json', 'w')); json.dump(tl, open(f'{W}/timeline.json', 'w'), indent=1)
print('total', round(t, 2), tl)
