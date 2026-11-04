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
cuts = [(a + PAD, b - PAD) for a, b in zip(st, en) if b - a - 2 * PAD > 0.08]
ranges, s = [], 0.0
for a, b in cuts: ranges.append((s, a)); s = b
ranges.append((s, dur))
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
fc = []
for i, (a, b) in enumerate(ranges):
    fc.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}]")
    fc.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b-a-0.015:.3f}:d=0.015[a{i}]")
fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(ranges))) + f'concat=n={len(ranges)}:v=1:a=1[cv][ca]')
r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', ';'.join(fc), '-map', '[cv]', '-map', '[ca]',
                    '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-c:a', 'pcm_f32le', out_v], capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-2000:])
new = sum(b - a for a, b in ranges)
print(f'{dur:.2f}s -> {new:.2f}s ({len(cuts)} pauses cut)')
if new < 61: print('WARNING: under 61 s, too short for the 1:01 TikTok minimum')
