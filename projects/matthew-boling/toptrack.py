"""Render the split's top half (1440x1280) from top.json shots, with the assembled voice as its audio.
Each shot runs until the next one starts; a source that runs out holds its last frame.
usage: python3 toptrack.py top.json top.mov"""
import json, subprocess, sys, os
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
W, H, FPS = 1440, 1280, 30
shots = spec['shots']; D = spec['duration']
tmp = os.path.join(os.path.dirname(os.path.abspath(out)), 'build', 'top'); os.makedirs(tmp, exist_ok=True)
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
parts = []
for i, s in enumerate(shots):
    t0 = s['t']; t1 = shots[i + 1]['t'] if i + 1 < len(shots) else D
    d = t1 - t0; fx, fy = s['focus']
    avail = dur(s['src']) - s['ss']
    pad = max(0.0, d - avail + 0.1)
    p = f'{tmp}/s{i:03d}.mp4'; parts.append(p)
    key = json.dumps([s, round(d, 3)]); kf = p + '.key'
    if os.path.exists(p) and os.path.exists(kf) and open(kf).read() == key: continue
    vf = (f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={W}:{H}:x='(iw-ow)*{fx}':y='(ih-oh)*{fy}',setsar=1" + (f",tpad=stop_mode=clone:stop_duration={pad:.3f}" if pad > 0 else '') +
          f",trim=duration={d:.3f}")
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{s['ss']:.3f}", '-i', s['src'], '-vf', vf, '-an',
                        '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])
    open(kf, 'w').write(key)
lst = f'{tmp}/list.txt'; open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', spec['voice'], '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'pcm_s24le', '-t', f'{D:.3f}', out], capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print('wrote', out, round(dur(out), 2), 's')
