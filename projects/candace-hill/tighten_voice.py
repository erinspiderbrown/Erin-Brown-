"""Shorten every silence > 0.7 s in an assembled voice track to 0.5 s (audio-only tighten.py), remapping word timings.
usage: python3 tighten_voice.py voice.wav words.json out.wav out_words.json"""
import json, re, subprocess, sys
src, wj, ow, oj = sys.argv[1:5]; KEEP = 0.25
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
log = subprocess.run(['ffmpeg', '-i', src, '-af', 'silencedetect=noise=-42dB:d=0.7', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
cuts = [(a + KEEP, b - KEEP) for a, b in zip(st, en) if a > 0.05 and b - a > 0.7]
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
json.dump(W, open(oj, 'w'))
fc = [f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b-a-0.012:.3f}:d=0.012[a{i}]" for i, (a, b) in enumerate(ranges)]
fc.append(''.join(f'[a{i}]' for i in range(len(ranges))) + f'concat=n={len(ranges)}:v=0:a=1[o]')
r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', ';'.join(fc), '-map', '[o]', '-c:a', 'pcm_s24le', ow], capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print(f'{dur:.2f}s -> {sum(b - a for a, b in ranges):.2f}s ({len(cuts)} silences shortened)')
