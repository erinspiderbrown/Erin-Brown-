"""Eat some food: female distance runners, coaches, eating disorders. v2 style, owner's layout: full-screen for the big
moments (cards, stock), talking head always split with footage under it. Mary Cain soundbite (ABC13/AP 2019) inserted
at 27.45 s (+6.5 s), so every time after that is shifted. Real cases: Mary Cain, Allie Ostrander, Marthe Katrine Myhre."""
import json
B = 6.5          # soundbite length
SEG = [  # start (final timeline), type, src, ss, transition
 (0.0,   'full',  'br/p8484861.mp4',     0, None),
 (3.7,   'split', 'br/p6547792.mp4',     0, 'cut'),
 (10.2,  'split', 'br/p6130226.mp4',     0, None),
 (12.4,  'split', 'up/cain_race.mp4',    0, None),
 (19.9,  'full',  'fx/nyt_card.mp4',     0, 'zoom'),
 (23.4,  'split', 'up/cain_race.mp4',    8, 'cut'),
 (27.45, 'split', 'up/cain_flag.mp4',    0, 'cut'),          # Mary Cain on top (soundbite)
 (27.45+B, 'split', 'br/p7299333.mp4',   0, 'cut'),
 (37.8,  'split', 'br/p5722222.mp4',     0, None),
 (42.6,  'full',  'fx/xray_card.mp4',    0, 'glitch'),
 (46.4,  'split', 'br/p6547792.mp4',     4, 'cut'),
 (53.5,  'split', 'br/p7267563.mp4',     0, None),
 (61.0,  'split', 'fx/allie_freeze.mp4', 0, 'cut'),
 (64.5,  'full',  'fx/adn_card.mp4',     0, 'zoom'),
 (69.3,  'split', 'br/p6130226.mp4',     1, 'cut'),
 (72.8,  'split', 'fx/myhre.mp4',        0, 'cut'),
 (77.9,  'full',  'fx/myhre_card.mp4',   0, 'zoom'),
 (81.5,  'split', 'br/p8459964.mp4',     2, 'cut'),
]
segs = []
for t, k, src, ss, tr in SEG:
    d = {"type": k, "start": round(t, 2), "broll": {"src": src, "ss": ss, "focus": [0.5, 0.45], **({"nograde": True} if src.startswith('fx/') else {})}}
    if tr: d["transition"] = tr
    segs.append(d)
plan = {"workdir": "build", "output": "out/eat_some_food.mp4", "words": "work/words_final.json", "voice_ss": 0.0,
        "duration": 86.07, "min_duration": 61,
        "face": {"src": "work/face_final.mov", "focus": [0.5, 0.5]},
        "face_grade": "unsharp=5:5:0.5:5:5:0,vignette=PI/6",
        "broll_grade": "eq=contrast=1.07:saturation=1.06:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rh=0.03:bh=-0.03,noise=alls=2:allf=t,vignette=PI/5",
        "caption_style": "cine", "caption_accent": "#FFC83D",
        "caption_emph": ["eat", "food", "105", "98", "die", "skinny", "disorders", "fat", "90", "weighed", "heavy", "five", "bones", "weak",
                         "fractures", "tendon", "small", "harder", "100", "organs", "dialysis", "cancer", "broken", "examples", "please"],
        "flash": False,
        "zooms": [[2.0, 3.6, 1.1], [10.6, 12.3, 1.1], [18.7, 19.8, 1.08], [52.0, 54.0, 1.1], [77.9, 78.0, 1.0], [84.0, 86.0, 1.12]],
        "segments": segs, "graphics": []}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments')
