"""Guard against muffled exports: compare the voice's spectral balance in the export with the source recording.
usage: python3 audio_check.py <source_media> <export_media>
Prints the share of energy per band (loud passages only) and warns if clarity (1-2.5 kHz), presence (2.5-5 kHz)
or air (5-10 kHz) in the export falls below the source. The owner wants the voice clear, never muffled."""
import subprocess, sys
import numpy as np

BANDS = [('low 80-300', 80, 300), ('body .3-1k', 300, 1000), ('clarity 1-2.5k', 1000, 2500),
         ('presence 2.5-5k', 2500, 5000), ('air 5-10k', 5000, 10000)]
MUST_NOT_DROP = ('clarity 1-2.5k', 'presence 2.5-5k', 'air 5-10k')

def shares(path, t=90):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-t', str(t), '-i', path, '-map', '0:a:0', '-f', 'f32le',
                                      '-ac', '1', '-ar', '48000', '-'], capture_output=True).stdout, np.float32).astype(float)
    N = 4096
    fr = np.lib.stride_tricks.sliding_window_view(a, N)[::N // 2]
    fr = fr[fr.std(axis=1) > np.percentile(fr.std(axis=1), 40)]
    S = (np.abs(np.fft.rfft(fr * np.hanning(N), axis=1)) ** 2).sum(axis=0)
    f = np.fft.rfftfreq(N, 1 / 48000)
    tot = S[(f > 80) & (f < 16000)].sum()
    return {n: 100 * S[(f >= lo) & (f < hi)].sum() / tot for n, lo, hi in BANDS}

def check(src, out):
    s, o = shares(src), shares(out)
    bad = [n for n in MUST_NOT_DROP if o[n] < 0.95 * s[n]]
    print('voice tone   ' + '  '.join(f'{n}: {s[n]:.2f}->{o[n]:.2f}' for n, _, _ in BANDS))
    if bad: print('WARNING: export sounds MUFFLED vs the source (' + ', '.join(bad) + ' dropped). Brighten the voice chain.')
    else: print('voice tone OK: export is at least as clear as the source')
    return not bad

if __name__ == '__main__':
    sys.exit(0 if check(sys.argv[1], sys.argv[2]) else 1)
