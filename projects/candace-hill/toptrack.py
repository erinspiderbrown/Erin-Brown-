"""Top half (1440x1280) for a voiceover doc: a sequence of photos (slow Ken Burns push-in) or video clips,
carrying the voice track as audio. usage: python3 toptrack.py top.json top.mov"""
import json, os, subprocess, sys
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
W, H, FPS = 1440, 1280, 30; IMG = ('.jpg', '.jpeg', '.png', '.webp')
shots = spec['shots']; D = spec['duration']
tmp = os.path.join(os.path.dirname(os.path.abspath(out)), 'build', 'top'); os.makedirs(tmp, exist_ok=True)
parts = []
for i, s in enumerate(shots):
    t0 = s['t']; t1 = shots[i + 1]['t'] if i + 1 < len(shots) else D; d = t1 - t0 + 0.4      # small overlap for transitions
    fx, fy = s['focus']; push = s.get('push', 0.07); p = f'{tmp}/s{i:03d}.mp4'; parts.append((p, t1 - t0))
    key = json.dumps([s, round(d, 3)]); kf = p + '.key'
    if os.path.exists(p) and os.path.exists(kf) and open(kf).read() == key: continue
    if s['src'].lower().endswith(IMG):
        inp = ['-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', s['src']]
        z = f"(1+{push}*t/{d:.3f})"
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}:x='(iw-ow)*{fx}':y='(ih-oh)*{fy}',"
              f"scale=w='trunc({W}*{z}/2)*2':h=-2:eval=frame:flags=bicubic,crop={W}:{H}:x='(iw-ow)*{fx}':y='(ih-oh)*{fy}',unsharp=5:5:0.5:5:5:0,setsar=1,fps={FPS}")
    else:
        inp = ['-ss', f"{s.get('ss', 0):.3f}", '-t', f'{d:.3f}', '-i', s['src']]
        vf = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}:x='(iw-ow)*{fx}':y='(ih-oh)*{fy}',setsar=1,tpad=stop_mode=clone:stop_duration=5"
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-vf', vf, '-t', f'{d:.3f}', '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast',
                        '-pix_fmt', 'yuv420p', p], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])
    open(kf, 'w').write(key)
lst = f'{tmp}/list.txt'
open(lst, 'w').write(''.join(f"file '{p}'\noutpoint {dur:.3f}\n" for p, dur in parts))
r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', spec['voice'], '-map', '0:v', '-map', '1:a',
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-c:a', 'pcm_s24le', '-t', f'{D:.3f}', out], capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print('wrote', out)
