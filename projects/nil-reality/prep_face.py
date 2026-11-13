"""Owner's flubs out, then crop the 4K landscape take to the 1440x1280 top-half framing.
CUTS are (start, end) in the raw take; word timings are remapped."""
import json, subprocess
CUTS = [(45.82, 46.36),   # "and they and they get nothing" -> "and they get nothing"
        (68.08, 69.60)]   # false start "If you especially attract" -> "if you showing up to track meets"
SRC, DUR = 'work/face_full.mov', 84.2875
keep, t = [], 0.0
for a, b in CUTS: keep.append((t, a)); t = b
keep.append((t, DUR))
vf, af = [], []
for i, (a, b) in enumerate(keep):
    vf.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
    af.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b-a-0.015}:d=0.015[a{i}]")
n = len(keep)
fc = ';'.join(vf + af) + ';' + ''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a];[v]null[vo]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-filter_complex', fc, '-map', '[vo]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', 'work/face.mov'], check=True)
def remap(x):
    off = 0
    for a, b in CUTS:
        if x >= b: off += b - a
        elif x > a: return None
    return x - off
W = json.load(open('work/words.json')); out = []
for w in W:
    s, e = remap(w['s']), remap(w['e'])
    if s is None or e is None: continue
    out.append({**w, 's': round(s, 3), 'e': round(e, 3)})
json.dump(out, open('work/words_cut.json', 'w'))
print(len(W), '->', len(out), 'words')
