"""Synthesize clean, non-cheesy SFX as 48k stereo WAVs (whoosh, impact, pop, tick)."""
import numpy as np, wave, sys, os
SR = 48000
rng = np.random.default_rng(7)

def save(name, x):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    if x.ndim == 1: x = np.stack([x, x], 1)
    with wave.open(name, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def onepole_sweep(x, f0, f1, shape=2.0):
    n = len(x); t = np.linspace(0, 1, n)
    f = f0 * (f1 / f0) ** (t ** shape)
    a = np.exp(-2 * np.pi * f / SR)
    y = np.zeros(n); z = 0.0
    for i in range(n):
        z = (1 - a[i]) * x[i] + a[i] * z; y[i] = z
    return y

def whoosh(dur=0.45):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    lp = onepole_sweep(noise, 300, 6000, 1.0)
    bp = lp - onepole_sweep(lp, 120, 1500, 1.0)          # band-ish
    env = np.sin(np.pi * t ** 0.7) ** 2
    x = bp * env
    pan = t                                              # L -> R
    return np.stack([x * np.cos(pan * np.pi / 2), x * np.sin(pan * np.pi / 2)], 1)

def impact(dur=0.9):
    n = int(SR * dur); tt = np.arange(n) / SR
    f = 38 + 70 * np.exp(-tt * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5.5)
    click = onepole_sweep(rng.standard_normal(n), 3000, 400, 0.5) * np.exp(-tt * 60)
    return np.tanh(1.6 * (body + 0.35 * click))

def pop(dur=0.12):
    n = int(SR * dur); tt = np.arange(n) / SR
    f = 900 * np.exp(-tt * 14) + 380
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38) * (1 - np.exp(-tt * 2000))

def tick(dur=0.05):
    n = int(SR * dur); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * tt) + 0.4 * rng.standard_normal(n)) * np.exp(-tt * 140)

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    save(f'{out}/whoosh.wav', whoosh()); save(f'{out}/impact.wav', impact())
    save(f'{out}/pop.wav', pop()); save(f'{out}/tick.wav', tick())
