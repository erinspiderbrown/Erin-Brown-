"""Leo & Lex Young fall-off. v2 style: full-screen FX/cards for the big beats, split everywhere else.
Leo's USATF XC 2023 soundbite inserted at T_INS (+B s). Talking head: crop + downscale only, vignette only."""
import json
T_INS, B = 16.45, 13.82
SEG = [  # owner tight-timeline start, type, src, ss, focus, transition
 (0.0,   'full',  'fx/open_par.mp4',     0,    None,        None),
 (4.3,   'split', 'br/np_finish.jpg',    0,    (0.5, 0.45), 'cut'),
 (9.7,   'split', 'br/ph6_up.jpg',       0,    (0.5, 0.25), None),
 (16.45, 'split', 'br/ph2_up.jpg',       0,    (0.5, 0.4),  'cut'),
 (18.7,  'full',  'fx/np_card.mp4',      0,    None,        'zoom'),
 (23.0,  'split', 'br/lex_record.jpg',   0,    (0.5, 0.3),  'cut'),
 (27.3,  'full',  'fx/hs5k_card.mp4',    0,    None,        'whip:left'),
 (31.0,  'split', 'br/burns.jpg',        0,    (0.5, 0.3),  'cut'),
 (36.3,  'split', 'br/stan_nutty.png',   0,    (0.5, 0.4),  None),
 (40.5,  'split', 'br/stan_bu1.jpg',     0,    (0.5, 0.3),  None),
 (43.6,  'split', 'br/stan_bu2.jpg',     0,    (0.5, 0.3),  None),
 (46.9,  'split', 'br/n26start.mp4',     4,    (0.5, 0.5),  None),
 (51.4,  'split', 'br/n26fin.mp4',       21.5, (0.5, 0.5),  None),
 (53.9,  'full',  'fx/ncaa26_card.mp4',  0,    None,        'glitch'),
 (58.5,  'split', 'br/n24pack.mp4',      10,   (0.5, 0.5),  'cut'),
 (61.1,  'split', 'br/committed.jpg',    0,    (0.5, 0.4),  None),
 (65.5,  'split', 'br/lex_record.jpg',   0,    (0.5, 0.55), None),
 (70.6,  'full',  'fx/nico_par.mp4',     0,    None,        'zoom'),
 (77.7,  'split', 'br/sahlman800.jpg',   0,    (0.5, 0.4),  'cut'),
 (83.1,  'full',  'fx/sahlman_card.mp4', 0,    None,        'whip:left'),
 (88.7,  'split', 'br/sahlman3000.jpg',  0,    (0.5, 0.4),  'cut'),
 (95.6,  'split', 'br/stan_team.png',    0,    (0.5, 0.45), None),
 (101.1, 'split', 'br/n25fin.mp4',       7,    (0.5, 0.5),  None),
 (104.3, 'full',  'fx/ky_card.mp4',      0,    None,        'zoom'),
 (108.3, 'split', 'br/n24pack.mp4',      22,   (0.5, 0.5),  'cut'),
 (112.0, 'split', 'br/n26fin.mp4',       40,   (0.5, 0.5),  None),
]
segs = []
for t, k, src, ss, foc, tr in SEG:
    ft = t + B if t >= T_INS else t
    b = {"src": src, "ss": ss, "focus": list(foc or (0.5, 0.45))}
    if src.startswith('fx/'): b["nograde"] = True
    d = {"type": k, "start": round(ft, 2), "broll": b}
    if tr: d["transition"] = tr
    segs.append(d)
segs.append({"type": "split", "start": T_INS, "broll": {"src": "br/leo_usatf.jpg", "ss": 0, "focus": [0.5, 0.3]}, "transition": "cut"})
segs.sort(key=lambda d: d['start'])
plan = {"workdir": "build", "output": "out/young_twins.mp4", "words": "work/words_ins.json", "voice_ss": 0.0,
        "duration": round(116.40 + B, 2), "min_duration": 61,
        "face": {"src": "work/face_final.mov", "focus": [0.5, 0.5]},
        "face_grade": "vignette=PI/6",
        "broll_grade": "eq=contrast=1.07:saturation=1.06:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rh=0.03:bh=-0.03,noise=alls=2:allf=t,vignette=PI/5",
        "caption_style": "cine", "caption_accent": "#FFC83D",
        "caption_emph": ["leo", "lex", "young", "studied", "prodigies", "records", "american", "newbury", "greatest", "record", "5k",
                         "burns", "gasket", "apart", "stanford", "opposite", "nationals", "hundred", "fame", "kipchoge", "kiptum",
                         "nico", "nau.", "olympic", "sahlman.", "ncaa", "champion", "flagstaff", "money.", "education.", "ky", "robinson",
                         "pro", "excuses", "panning", "usa", "earn", "singlet,", "counts."],
        "flash": False, "zooms": [], "segments": segs, "graphics": []}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments, duration', plan['duration'])
