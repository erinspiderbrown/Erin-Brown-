"""Cut dead air out of a talking-head take and remap word timings to match.
usage: python3 tighten.py <face.mov> <words.json> <out_face.mov> <out_words.json> [noise_db=-38] [min_pause=0.35] [pad=0.12]
Keeps `pad` seconds of breath on each side of every pause, adds 15 ms audio fades at each joint."""
import json, re, subprocess, sys
src, wj, out_v, out_w = sys.argv[1:5]
noise = sys.argv[5] if len(sys.argv) > 5 else '-38'
mind = float(sys.argv[6]) if len(sys.argv) > 6 else 0.35
PAD = float(sys.argv[7]) if len(sys.argv) > 7 else 0.12
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                           capture_output=True, text=True).stdout)
log = subprocess.run(['ffmpeg', '-i', src, '-af', f'silencedetect=noise={noise}dB:d={mind}', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
# snap every cut to the frame grid so the joined video and audio stay the same length (else lip-sync drifts ~0.02 s per cut)
fr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', src],
                    capture_output=True, text=True).stdout.strip().split(',')[0].split('/')
FPS = float(fr[0]) / float(fr[1]); q = lambda t: round(round(t * FPS) / FPS, 6)
cuts = [(q(a + PAD), q(b - PAD)) for a, b in zip(st, en) if b - a - 2 * PAD > 0.08]
ranges, s = [], 0.0
for a, b in cuts: ranges.append((s, a)); s = b
ranges.append((s, q(dur - 0.5 / FPS)))
def remap(t):
    acc = 0
    for a, b in ranges:
        if t < a: return acc
        if t <= b: return acc + t - a
        acc += b - a
    return acc
W = json.load(open(wj))
for w in W: w['s'], w['e'] = round(remap(w['s']), 3), round(remap(w['e']), 3)
json.dump(W, open(out_w, 'w'))
# Cut each kept range separately and join them (one big trim/concat filter graph runs out of memory on 4+ minute
# 1440x1280 takes and the process dies silently with a truncated file).
import os
d = os.path.dirname(os.path.abspath(out_v)); parts = []
for i, (a, b) in enumerate(ranges):
    p = f'{d}/_tight_seg_{i:03d}.mov'; parts.append(p)
    nfr = round((b - a) * FPS); L = nfr / FPS
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.6f}', '-i', src, '-frames:v', str(nfr), '-t', f'{L:.6f}',
                        '-af', f'apad,atrim=0:{L:.6f},afade=t=in:d=0.015,afade=t=out:st={L - 0.015:.4f}:d=0.015', '-ar', '48000',
                        '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-c:a', 'pcm_s24le', p], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])
lst = f'{d}/_tight_segs.txt'
open(lst, 'w').write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out_v], capture_output=True, text=True)
for p in parts + [lst]: os.remove(p)
if r.returncode: sys.exit(r.stderr[-2000:])
new = sum(b - a for a, b in ranges)
print(f'{dur:.2f}s -> {new:.2f}s ({len(cuts)} pauses cut)')
if new < 61: print('WARNING: under 61 s, too short for the 1:01 TikTok minimum')
