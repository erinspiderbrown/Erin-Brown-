"""Cut the owner's YouTube video "The Strange Case of Marcell Jacobs" (raw/source.mp4, 10:17) to ~7:00 for TikTok, same plot order.
Keeps his original voice untouched: each kept range is copied as-is with a 25 ms fade at the cut, nothing else.
Writes voice_cut.wav, cut_map.json (new_start, src_start, src_end per range) and words_cut.json (captions on the new timeline)."""
import json, subprocess, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); SR = 48000
W = json.load(open(f'{H}/raw/words_raw.json'))
# (src_start, src_end) at sentence boundaries; see NOTES.md for what each one is
RANGES = [
    (0.0, 31.1),       # hook: Olympic gold, "how did he get this fast?", someone paid to get inside his phone
    (32.1, 56.1),      # prosecutors; it was Giacomo Tortu, brother of teammate Filippo
    (81.6, 86.5),      # "was there actually evidence that Marcell Jacobs doped?"
    (91.2, 120.4),     # before 2021: long jumper, 10.03 PB
    (124.9, 128.7),    # 9.95 Italian record
    (136.2, 175.2),    # Tokyo: 9.94, 9.84, 9.80, first Italian champion; the doping questions
    (179.3, 212.1),    # suspicion is not proof; tests negative; 10.03 -> 9.80
    (238.0, 280.5),    # the nutritionist Spazzini, Operation Muscle Bound, terrible timing
    (288.0, 302.6),    # no public evidence; split March 2021
    (338.0, 345.7),    # "Jacobs' steroid guy got busted" isn't accurate
    (355.4, 361.5),    # never a finding that Jacobs took banned substances; he denies
    (362.4, 383.7),    # questions didn't go away; Bolt's successor; shut down his season
    (395.8, 411.7),    # his denial: hard work, blood, sweat and tears
    (427.9, 451.5),    # Paris 2024: 9.85, 5th; 2025 insane turn
    (457.1, 504.3),    # Giacomo Tortu, the hacker, the phones, the timeline
    (516.0, 521.9),    # someone wanted to know whether the champion was clean
    (527.2, 547.2),    # Equalize; communications extracted
    (573.8, 616.9),    # April 2026: 81 named; allegations, not a conviction; Filippo not accused
]


def bounds(s, e):
    """pad to the silence around the range's own words, never into a neighbouring word"""
    inr = [w for w in W if w['s'] >= s - 0.15 and w['s'] < e - 0.02 and w['e'] <= e + 0.8]   # every word that STARTS in the range, kept whole
    s0, e0 = min(w['s'] for w in inr), max(w['e'] for w in inr)
    prev = max([w['e'] for w in W if w['e'] < s0 - 0.005 and w not in inr] or [-1.0])
    nxt = min([w['s'] for w in W if w['s'] > e0 + 0.005 and w not in inr] or [e0 + 1])
    return max(0.0, prev + 0.02, s0 - 0.15), min(nxt - 0.02, e0 + 0.25)


src = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{H}/raw/source.mp4', '-vn', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                                   capture_output=True).stdout, np.float32).reshape(-1, 2)
out, cmap, words, t = [], [], [], 0.0
F = int(0.025 * SR); ramp = np.linspace(0, 1, F, dtype=np.float32)[:, None]
for s, e in RANGES:
    a, b = bounds(s, e)
    x = src[int(a * SR):int(b * SR)].copy(); x[:F] *= ramp; x[-F:] *= ramp[::-1]
    out.append(x); cmap.append({'new': round(t, 3), 'src': round(a, 3), 'end': round(b, 3)})
    for w in W:
        if a - 0.01 <= w['s'] and w['s'] < b - 0.02:
            words.append({'w': w['w'], 's': round(w['s'] - a + t, 3), 'e': round(w['e'] - a + t, 3)})
    t += len(x) / SR
y = np.concatenate(out)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s24le', f'{H}/voice_cut.wav'], input=y.tobytes())
json.dump(cmap, open(f'{H}/cut_map.json', 'w'), indent=0); json.dump(words, open(f'{H}/words_cut.json', 'w'))
print(f'{len(RANGES)} ranges, total {t:.2f} s ({int(t // 60)}:{t % 60:04.1f}), {len(words)} words')
