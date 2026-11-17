"""Tiaan Whelpton: 21 seconds at 6'4". v2 cinematic style. Sub-1080 footage (all his clips) stays in the split, AI-upscaled;
FX shots of that footage render at split size (1080x960)."""
import json
SEG = [  # start, type, src, ss, transition
 (0.0,  'face',  None,                  0, None),
 (2.6,  'split', 'fx/freeze_intro.mp4', 0, 'cut'),
 (8.1,  'full',  'fx/result.mp4',       0, 'zoom'),
 (11.4, 'face',  None,                  0, 'cut'),
 (13.6, 'split', 'fx/bolt.mp4',         0, 'cut'),
 (19.6, 'face',  None,                  0, 'cut'),
 (24.9, 'split', 'up/c1.mp4',           0, 'cut'),
 (28.5, 'full',  'fx/should.mp4',       0, 'glitch'),
 (30.9, 'split', 'fx/curve.mp4',        0, 'whip:left'),
 (34.2, 'face',  None,                  0, 'cut'),
 (38.1, 'split', 'up/c2.mp4',           0, 'cut'),
 (41.0, 'face',  None,                  0, 'cut'),
 (47.7, 'split', 'br/p37264421.mp4',    0, 'cut'),
 (50.5, 'full',  'fx/nov16.mp4',        0, 'zoom'),
 (54.8, 'face',  None,                  0, 'cut'),
 (57.9, 'split', 'up/c250.mp4',         0, 'cut'),
 (61.1, 'split', 'fx/freeze_22.mp4',    0, 'cut'),
 (65.4, 'face',  None,                  0, 'cut'),
 (69.1, 'split', 'br/p32240945.mp4',    2, 'cut'),
 (73.0, 'face',  None,                  0, 'cut'),
 (76.4, 'full',  'br/p39710084.mp4',    0, 'whip:up'),
 (81.4, 'face',  None,                  0, 'cut'),
 (84.6, 'full',  'br/p5229966.mp4',     1, 'whip:left'),
 (87.8, 'face',  None,                  0, 'cut'),
]
segs = []
for t, k, src, ss, tr in SEG:
    if k == 'face': d = {"type": "face", "start": t, "broll": {"src": "work/facev_tight.mov", "ss": t, "nograde": True}}
    else: d = {"type": k, "start": t, "broll": {"src": src, "ss": ss, "focus": [0.5, 0.5], **({"nograde": True} if src.startswith('fx/') else {})}}
    if tr: d["transition"] = tr
    segs.append(d)
plan = {"workdir": "build", "output": "out/tiaan_whelpton.mp4", "words": "work/words_final.json", "voice_ss": 0.0,
        "duration": 92.95, "min_duration": 61,
        "face": {"src": "work/faces_tight.mov", "focus": [0.5, 0.5]},
        "face_v": {"src": "work/facev_tight.mov", "focus": [0.5, 0.42]},
        "face_grade": "unsharp=5:5:0.5:5:5:0,vignette=PI/6",
        "broll_grade": "eq=contrast=1.07:saturation=1.06:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rh=0.03:bh=-0.03,noise=alls=2:allf=t,vignette=PI/5",
        "caption_style": "cine", "caption_accent": "#FFC83D",
        "caption_emph": ["sad", "fastest", "Zealand", "21", "200", "Bolt", "Usain", "awful", "20.3", "20.4", "flat", "horrible", "overspeed",
                         "November", "16th", "1080", "250s", "22", "nowhere", "one", "rep", "horse", "water", "drink", "old", "dog", "tricks", "cry", "disaster"],
        "flash": False,
        "zooms": [[22.6, 23.5, 1.08], [35.3, 37.7, 1.08], [49.0, 50.4, 1.1], [65.6, 66.8, 1.1], [73.1, 75.6, 1.12], [89.5, 92.9, 1.1]],
        "meme_sfx": [["impact_quick_zoom", 2.6, 0.22, 0.9], ["impact_quick_zoom", 61.1, 0.22, 0.9]],
        "segments": segs, "graphics": []}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments')
