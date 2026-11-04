import subprocess, numpy as np, json, glob, os, sys
raw, out = sys.argv[1], sys.argv[2]
MAXLEN = {'whoosh': 1.4, 'impact': 2.5, 'pop': 0.6, 'click': 0.6, 'riser': 4.0}
meta = {}
for f in sorted(glob.glob(f'{raw}/*.mp3')):
    name = os.path.basename(f)[:-4]; kind = name.split('_')[0]
    pcm = subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','2','-ar','48000','-'],capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32).reshape(-1, 2).copy()
    mono = np.abs(x).max(1)
    win = 480; env = np.convolve(mono, np.ones(win)/win, 'same')
    thr = env.max() * 0.03
    start = max(0, np.argmax(env > thr) - 240)
    x = x[start:]; env = env[start:]
    if kind == 'riser':  # keep the last 4s, which builds into the peak
        pk = int(np.argmax(env)); s0 = max(0, pk - int(MAXLEN['riser']*48000)); x = x[s0:pk+4800]; env = env[s0:pk+4800]
    n = min(len(x), int(MAXLEN[kind] * 48000)); x = x[:n]; env = env[:n]
    fl = min(int(0.25 * 48000), n // 3); x[-fl:] *= np.linspace(1, 0, fl)[:, None] ** 2
    peak_t = float(np.argmax(env)) / 48000
    rms = np.sqrt(np.mean(x[max(0, int(peak_t*48000)-4800):int(peak_t*48000)+4800]**2)) + 1e-9
    x *= min(0.25 / rms, 0.97 / (np.abs(x).max() + 1e-9))   # level-match around the peak, no clipping
    pcm16 = (np.clip(x, -1, 1) * 32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ac','2','-ar','48000','-i','-',f'{out}/{name}.wav'], input=pcm16)
    meta[name] = {'kind': kind, 'peak': round(peak_t, 3), 'dur': round(n/48000, 3)}
    print(f'{name:30s} peak@{peak_t:.2f}s len {n/48000:.2f}s')
json.dump(meta, open(f'{out}/sfx.json', 'w'), indent=1)
