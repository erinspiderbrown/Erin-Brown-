"""NCAA XC Kenyans (Nov 21, 2026 nationals). v2 style: full-screen FX/cards for big beats, split (face top, footage
under) everywhere else. Talking head: crop + downscale only, vignette only (owner rule, Nov 18). No zooms on the face."""
import json
SEG = [  # start, type, src, ss, focus, transition
 (0.0,  'full',  'fx/open_par.mp4',             0,  None,        None),
 (4.0,  'split', 'br/kurgat.jpg',               0,  (0.62, 0.3), 'cut'),
 (7.1,  'full',  'fx/champ_card.mp4',           0,  None,        'zoom'),
 (10.9, 'split', 'br/2025_ncaa_men_start.mp4',  0,  (0.5, 0.5),  'cut'),
 (14.5, 'full',  'fx/cold_card.mp4',            0,  None,        'whip:left'),
 (19.7, 'split', 'br/2024_ncaa_men_crowd.mp4',  4,  (0.5, 0.5),  'cut'),
 (24.2, 'split', 'br/2024_ncaa_men_cold.mp4',   2,  (0.5, 0.5), None),
 (27.3, 'split', 'br/2024_ncaa_men_finish.mp4', 18, (0.5, 0.5),  None),
 (32.6, 'split', 'br/lavern.jpg',               0,  (0.55, 0.4), None),
 (36.2, 'full',  'fx/weather_card.mp4',         0,  None,        'zoom'),
 (40.3, 'split', 'br/kiprotich.jpg',            0,  (0.5, 0.3),  'cut'),
 (44.6, 'split', 'br/2025_ncaa_men_start.mp4',  33, (0.5, 0.5),  None),
 (51.1, 'split', 'br/2025_ncaa_men_finish.mp4', 44.6, (0.5, 0.5), None),
 (55.0, 'split', 'br/kurgat.jpg',               0,  (0.55, 0.15), None),
 (59.0, 'split', 'fx/elsingi.mp4',              0,  None,        'cut'),
 (60.6, 'split', 'fx/meshack.mp4',              0,  None,        'cut'),
 (62.4, 'full',  'fx/kimaru_par.mp4',           0,  None,        'whip:left'),
]
segs = []
for t, k, src, ss, foc, tr in SEG:
    b = {"src": src, "ss": ss, "focus": list(foc or (0.5, 0.45))}
    if src.startswith('fx/'): b["nograde"] = True
    d = {"type": k, "start": t, "broll": b}
    if tr: d["transition"] = tr
    segs.append(d)
plan = {"workdir": "build", "output": "out/ncaa_xc_kenyans.mp4", "words": "work/words_tight.json", "voice_ss": 0.0,
        "duration": 65.41, "min_duration": 61,
        "face": {"src": "work/face_tight.mov", "focus": [0.5, 0.5]},
        "face_grade": "vignette=PI/6",
        "broll_grade": "eq=contrast=1.07:saturation=1.06:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rh=0.03:bh=-0.03,noise=alls=2:allf=t,vignette=PI/5",
        "caption_style": "cine", "caption_accent": "#FFC83D",
        "caption_emph": ["kenyans", "kenyan", "ncaa", "2019", "tomorrow", "cold", "snowy", "snow", "kenya", "extreme", "neanderthal",
                         "mountains", "thrive", "indiana", "60", "perfect", "shine", "wind", "rain", "skies", "sweep", "rocky", "hansen",
                         "victory", "louisville", "colorado", "texas", "tech"],
        "flash": False, "zooms": [], "segments": segs, "graphics": []}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments')
