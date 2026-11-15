"""Assemble the Prefontaine narration: picked takes, trimmed, extra air at natural pauses, 1.5 s breaths between sections."""
import json, subprocess, numpy as np, sys
D = sys.argv[1]; SR = 48000
PICK  = ['01b', '02a', '03a', '04a', '05a', '06b', '07a', '08a']
EXTRA = {'01b': .22, '02a': .3, '03a': .3, '04a': .3, '05a': .4, '06b': .3, '07a': .36, '08a': .36}   # s added per natural pause (>0.3 s)
out = []; log = []
for k in PICK:
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{D}/{k}.mp3', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                                     capture_output=True).stdout, np.float32).copy()
    W = json.load(open(f'{D}/{k}.json'))
    s0 = max(0, W[0][1] - .12); s1 = min(len(a) / SR, W[-1][2] + .35)
    cuts = [(W[i][2] + W[i + 1][1]) / 2 for i in range(len(W) - 1) if W[i + 1][1] - W[i][2] > .3]
    seg = []; p = s0
    for c in cuts:
        seg.append(a[int(p * SR):int(c * SR)]); seg.append(np.zeros(int(EXTRA[k] * SR), np.float32)); p = c
    seg.append(a[int(p * SR):int(s1 * SR)])
    x = np.concatenate(seg)
    if out: out.append(np.zeros(int(1.5 * SR), np.float32))
    log.append((k, round(sum(len(y) for y in out) / SR, 2), round(len(x) / SR, 2), len(cuts)))
    out.append(x)
y = np.concatenate(out)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s24le', f'{D}/../voice_master.wav'], input=y.tobytes())
for r in log: print(r)
print('total', round(len(y) / SR, 2), 's  peak', round(20 * np.log10(np.abs(y).max()), 2), 'dBFS')
