"""Gift Bright: v2 'cinematic' editing test. Full-screen talking head + full-screen FX shots, few splits, no stickers."""
import json
SEG = [  # start, type, src, ss, focus, transition
 (0.0,  'full',  'fx/hook.mp4',         0, None),
 (2.45, 'face',  None,                  0, 'cut'),
 (6.2,  'full',  'fx/ramp_start.mp4',   0, 'whip:left'),
 (9.3,  'full',  'fx/map.mp4',          0, 'zoom'),
 (17.3, 'face',  None,                  0, 'cut'),
 (20.1, 'split', 'br/p37253080.mp4',    0, 'cut'),
 (22.9, 'split', 'br/p31229040.mp4',    8, None),
 (25.2, 'face',  None,                  0, 'cut'),
 (27.0, 'full',  'raw/clip_clean.mp4',        5.0, 'whip:up'),
 (30.0, 'full',  'raw/clip_clean.mp4',       10.4, 'cut'),
 (32.55,'full',  'fx/freeze_name.mp4',  0, 'cut'),
 (35.65,'full',  'fx/prog14.mp4',       0, 'glitch'),
 (41.1, 'face',  None,                  0, 'cut'),
 (43.6, 'full',  'fx/p_1028.mp4',       0, 'cut'),
 (46.2, 'full',  'fx/ramp_finish.mp4',  0, 'whip:right'),
 (50.8, 'face',  None,                  0, 'cut'),
 (52.9, 'full',  'fx/freeze_200.mp4',   0, 'cut'),
 (56.4, 'face',  None,                  0, 'cut'),
 (58.8, 'split', 'br/p31229032.mp4',    3, 'cut'),
 (62.4, 'full',  'fx/prog_both.mp4',    0, 'zoom'),
 (66.3, 'full',  'fx/limit.mp4',        0, 'whip:up'),
 (69.9, 'face',  None,                  0, 'cut'),
]
FX = lambda s: s.startswith('fx/')
segs = []
for t, k, src, ss, tr in SEG:
    if k == 'face': d = {"type": "face", "start": t, "broll": {"src": "work/facev_tight.mov", "ss": t, "nograde": True}}
    else: d = {"type": k, "start": t, "broll": {"src": src, "ss": ss, "focus": [0.5, 0.5], **({"nograde": True} if FX(src) else {})}}
    if tr: d["transition"] = tr
    if src == 'fx/map.mp4': d["cap_y"] = 0.95          # keep captions off the country labels
    segs.append(d)
plan = {"workdir": "build", "output": "out/gift_bright.mp4", "words": "work/words_final.json", "voice_ss": 0.0,
        "duration": 72.53, "min_duration": 61,
        "face": {"src": "work/faces_tight.mov", "focus": [0.5, 0.5]},
        "face_v": {"src": "work/facev_tight.mov", "focus": [0.5, 0.42]},
        "face_grade": "unsharp=5:5:0.5:5:5:0,vignette=PI/6",
        "broll_grade": "eq=contrast=1.07:saturation=1.06:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rh=0.03:bh=-0.03,noise=alls=2:allf=t,vignette=PI/5",
        "caption_style": "cine", "caption_accent": "#FFC83D",
        "caption_emph": ["Africa", "Africa,", "2028", "2028,", "Olympics", "Nigeria", "Botswana", "South", "Morocco", "Algeria", "dominate",
                         "Gift", "Bright", "Bright.", "15", "14", "10.5", "21.5", "10.28", "10.2", "20.7", "200", "freshman", "limit", "sky's", "quick"],
        "flash": False, "zooms": [[3.0, 4.6, 1.08], [41.6, 43.4, 1.1], [57.3, 58.4, 1.08], [70.9, 72.5, 1.12]],
        "meme_sfx": [["impact_quick_zoom", 32.55, 0.22, 0.9], ["impact_quick_zoom", 52.9, 0.22, 0.9]],
        "segments": segs, "graphics": []}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments')
