"""Repair a clipped voice recording (phone mic overloaded on loud syllables).
usage: python3 declip.py <media> <out.wav> [threshold=0.95]

Finds runs of samples at/near full scale (flat-topped peaks, including the AAC ripple around them),
and rebuilds each run with a least-squares parabola through the clean samples on both sides
(capped at +4 dB over full scale). The rebuilt peak
is never allowed to be smaller than the clipped sample (it was at least that loud). Output is 32-bit
float WAV, so peaks above 1.0 survive; turn it down later in the chain, never clip it again.
Prints how many peaks were repaired and checks that no flat tops remain."""
import subprocess, sys
import numpy as np

src, out = sys.argv[1], sys.argv[2]
T = float(sys.argv[3]) if len(sys.argv) > 3 else 0.95
SR, CTX, MAXRUN = 48000, 8, 400             # context samples each side; runs longer than this are left alone
CAP = 1.6                                    # rebuilt peaks never exceed ~+4 dB over full scale (realistic overshoot)

raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-map', '0:a:0', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True).stdout
x = np.frombuffer(raw, np.float32).astype(np.float64)
y = x.copy()

def runs(a, thr):
    hi = np.abs(a) >= thr
    d = np.diff(np.concatenate([[0], hi.astype(np.int8), [0]]))
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))

fixed = skipped = 0
for s, e in runs(x, T):
    s0, e0 = max(0, s - 1), min(len(x), e + 1)        # widen by one sample: the edges are distorted too
    if e0 - s0 > MAXRUN: skipped += 1; continue
    li = np.arange(max(0, s0 - CTX), s0); ri = np.arange(e0, min(len(x), e0 + CTX))
    if len(li) < 3 or len(ri) < 3: skipped += 1; continue
    ok = np.concatenate([li, ri])
    if np.any(np.abs(x[ok]) >= T): ok = ok[np.abs(x[ok]) < T]
    if len(ok) < 4: skipped += 1; continue
    idx = np.arange(s0, e0)
    c = (s0 + e0) / 2; w = max(e0 - s0, 4)
    est = np.polyval(np.polyfit((ok - c) / w, x[ok], 2), (idx - c) / w)   # least-squares parabola: stable, no wild overshoot
    a = np.abs(est); K = 1.2                                          # soft knee above 1.2: rounded, never flat
    est = np.sign(est) * np.where(a > K, K + (CAP - K) * np.tanh((a - K) / (CAP - K)), a)
    sgn = np.sign(x[idx])
    y[idx] = sgn * np.maximum(np.abs(est) * (np.sign(est) == sgn), np.abs(x[idx]))   # never quieter than the clipped sample
    fixed += 1

subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f64le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_f32le', out],
               input=y.astype(np.float64).tobytes(), check=True)

def flat(a, thr=0.98, n=3):
    return sum(1 for s, e in runs(a, thr) if e - s >= n)
print(f'{fixed} clipped peaks rebuilt, {skipped} left (too long or no clean context); '
      f'max {np.abs(x).max():.3f} -> {np.abs(y).max():.3f}; flat tops at old ceiling: {flat(x)} -> '
      f'{sum(1 for s, e in runs(y, 0.98) if e - s >= 3 and np.ptp(y[s:e]) < 0.03)}')
