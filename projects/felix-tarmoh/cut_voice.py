"""Cut the owner's 2024 YouTube video (raw/source.mp4, 11:14) down to <= 7:00 for TikTok, same plot order.
Keeps his original voice untouched: each kept range is copied as-is with a 25 ms fade at the cut, nothing else.
Writes voice_cut.wav, cut_map.json (new_start, src_start, src_end per range) and words_cut.json (captions on the new timeline)."""
import json, subprocess, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); SR = 48000
W = json.load(open(f'{H}/raw/words_raw.json'))
# (src_start, src_end) at sentence boundaries; see NOTES.md for what each one is
RANGES = [
    (0.00, 9.74),      # cold open: Tarmoh (podcast) "I was told if I said anything I would be blackballed…"
    (62.86, 123.22),   # the race, Tarmoh announced 3rd, USATF reverses to a tie
    (124.62, 141.60),  # USATF (Jill Geer): "we have a dead heat for third place"
    (142.38, 152.30),  # Nike/USATF golden girl
    (165.08, 172.76),  # "the incident painted a different picture"
    (183.86, 206.34),  # calculated move, wanted to double
    (207.24, 216.58),  # Tarmoh felt betrayed
    (218.46, 229.86),  # Tarmoh (ESPN): "I'm not comfortable with the runoff… coin toss"
    (236.38, 257.24),  # "if I would have won fair and square…"
    (257.58, 292.64),  # the meeting: "I worked hard for this too, I can't just give up my spot"
    (297.38, 304.54),  # "Do you feel that Allyson Felix betrayed you…"
    (310.26, 315.96),  # "I did feel betrayed. She said one thing and did another."
    (316.66, 339.10),  # Nike clout, opportunist?
    (356.68, 383.28),  # USATF suspicious; roles reversed + Tarmoh: "my coach said that's politics"
    (396.14, 400.52),  # "if I said anything I would be blackballed"
    (401.40, 423.92),  # runoff or coin toss
    (443.64, 457.18),  # USATF bending over backwards, Nike deal
    (482.10, 498.60),  # favoritism, marketable vs unknown
    (514.08, 548.10),  # harassed, refused the runoff, gave up her spot
    (557.66, 589.14),  # London
    (589.78, 597.50),  # lasting stain on Felix's image and USATF
    (663.14, 666.58),  # "let me know what you think in the comments"
]


def bounds(s, e):
    """pad to the silence around the range's own words, never into a neighbouring word"""
    inr = [w for w in W if w['s'] >= s - 0.03 and w['e'] <= e + 0.03]
    s0, e0 = min(w['s'] for w in inr), max(w['e'] for w in inr)
    prev = max([w['e'] for w in W if w['e'] < s0 - 0.005 and w not in inr] or [0.0])
    nxt = min([w['s'] for w in W if w['s'] > e0 + 0.005 and w not in inr] or [e0 + 1])
    return max(prev + 0.02, s0 - 0.15), min(nxt - 0.02, e0 + 0.25)


src = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{H}/raw/source.mp4', '-vn', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                                   capture_output=True).stdout, np.float32).reshape(-1, 2)
out, cmap, words, t = [], [], [], 0.0
F = int(0.025 * SR); ramp = np.linspace(0, 1, F, dtype=np.float32)[:, None]
for s, e in RANGES:
    a, b = bounds(s, e)
    x = src[int(a * SR):int(b * SR)].copy(); x[:F] *= ramp; x[-F:] *= ramp[::-1]
    out.append(x); cmap.append({'new': round(t, 3), 'src': round(a, 3), 'end': round(b, 3)})
    for w in W:
        if a - 0.01 <= w['s'] and w['e'] <= b + 0.03:
            words.append({'w': w['w'], 's': round(w['s'] - a + t, 3), 'e': round(w['e'] - a + t, 3)})
    t += len(x) / SR
y = np.concatenate(out)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s24le', f'{H}/voice_cut.wav'], input=y.tobytes())
json.dump(cmap, open(f'{H}/cut_map.json', 'w'), indent=0); json.dump(words, open(f'{H}/words_cut.json', 'w'))
print(f'{len(RANGES)} ranges, total {t:.2f} s ({int(t // 60)}:{t % 60:04.1f}), {len(words)} words')
