"""Rylan Noome: spikes too early. plan.json for editor/build.py (Yohan Blake house style)."""
import json
B = lambda i, ss=0: (f'br/p{i}.mp4', ss)
R = lambda n, ss=0: (f'raw/{n}', ss)
SEG = [  # start, type, (src, ss), focus, hit
 (0.0,   'split', R('clip_nov06.mov', 42),   [0.5, 0.5],  False),
 (4.1,   'split', B(35829195, 1),            [0.5, 0.6],  False),
 (7.2,   'full',  B(35863230, 2),            [0.5, 0.5],  False),
 (10.0,  'split', B(10499738, 0),            [0.5, 0.45], False),
 (11.7,  'split', R('photo_nov09a.jpg'),     [0.5, 0.35], False),
 (15.9,  'full',  R('clip_nov06.mov', 33),   [0.5, 0.55], False),
 (21.0,  'split', R('clip_nov06.mov', 45),   [0.5, 0.6],  False),
 (25.6,  'split', R('photo_nov09b.jpg'),     [0.7, 0.35], False),
 (29.4,  'full',  B(39336191, 1),            [0.5, 0.5],  False),
 (32.6,  'full',  B(32168040, 5),            [0.5, 0.5],  True),
 (35.8,  'split', R('clip_nov08.mov', 6),    [0.5, 0.5],  False),
 (39.5,  'split', B(37264421, 0),            [0.5, 0.5],  False),
 (44.9,  'split', B(31229032, 3),            [0.5, 0.55], False),
 (49.0,  'split', B(37253080, 0),            [0.5, 0.55], False),
 (54.0,  'split', B(8691958, 2),             [0.5, 0.6],  False),
 (56.9,  'full',  B(11123558, 2),            [0.5, 0.55], True),
 (60.1,  'split', B(36109133, 0),            [0.5, 0.6],  False),
 (62.6,  'full',  R('photo_nov14.png'),      [0.5, 0.5],  False),
 (67.7,  'split', B(7299360, 1),             [0.5, 0.55], False),
 (74.6,  'split', B(35829195, 3),            [0.5, 0.6],  False),
 (81.5,  'split', B(5490677, 1),             [0.5, 0.5],  False),
 (85.6,  'split', R('clip_nov06.mov', 50),   [0.5, 0.55], False),
 (87.6,  'split', B(7299361, 1),             [0.5, 0.55], False),
 (93.6,  'split', B(36109133, 4),            [0.5, 0.6],  False),
 (97.0,  'split', B(31229040, 10),           [0.5, 0.6],  False),
 (99.5,  'split', B(8691958, 8),             [0.5, 0.6],  False),
 (103.6, 'split', R('clip_nov06.mov', 20),   [0.5, 0.5],  False),
 (107.6, 'split', B(35863230, 9),            [0.5, 0.5],  False),
]
segs = []
for t, k, (src, ss), f, hit in SEG:
    d = {"type": k, "start": t, "broll": {"src": src, "ss": ss, "focus": f}}
    if hit: d["hit"] = True
    segs.append(d)
M = lambda kind, t, dur, **kw: {"type": "motion", "kind": kind, "t": t, "dur": dur, **kw}
GFX = [
 M('stamp', 3.55, 1.3, text="I TOLD Y'ALL", anchor="upper"),
 M('keyword', 5.5, 1.8, text="SPIKES TOO EARLY"),
 M('stamp', 8.7, 1.4, text="EARLY GRAVE", anchor="upper"),
 M('keyword', 10.6, 1.4, text="MEET YOUR DEMISE"),
 M('pin', 12.3, 3.0, text="NEW ZEALAND", sub="RYLAN NOOME"),
 M('stopwatch', 18.4, 2.6, value="35.28", unit="300M", label="ONE REP · OCT 2026", anim=0.6),
 M('keyword', 22.2, 1.5, text="SUPER SPIKES"),
 M('stamp', 23.9, 1.4, text="GOD-AWFUL", anchor="upper"),
 M('keyword', 28.6, 1.6, text="JUDGMENT DAY"),
 M('stamp', 33.2, 1.6, text="STRAIGHT TO HELL", anchor="upper", size=96),
 M('keyword', 37.6, 1.6, text="A MONTH TO TRAIN"),
 M('keyword', 41.2, 1.6, text="400M: DAMN NEAR 51"),
 M('stamp', 43.4, 1.2, text="GROWN MAN", anchor="upper"),
 M('keyword', 45.6, 1.6, text="REDEEM HIMSELF"),
 M('keyword', 50.3, 1.6, text="100M & 200M"),
 M('keyword', 52.5, 1.4, text="PRIMED & READY"),
 M('keyword', 55.2, 1.5, text="NEVER SEEN BEFORE?"),
 M('stamp', 59.6, 1.4, text="NOTHING", anchor="upper"),
 M('keyword', 69.0, 1.5, text="HOW?!"),
 M('keyword', 71.5, 1.8, text="AIN'T EVEN RAN FAST"),
 M('calendar', 76.0, 5.2, items=["JULY", "AUG", "SEP", "OCT", "NOV"], hi=[0, 1], label="IN SPIKES SINCE"),
 M('keyword', 83.8, 1.6, text="BEFORE HALLOWEEN"),
 M('stamp', 86.2, 1.4, text="THE PRICE", anchor="upper"),
 M('keyword', 88.4, 1.8, text="NOT EVEN A REAL SEASON"),
 M('stamp', 92.9, 1.3, text="ALREADY COOKED", anchor="upper", size=96),
 {"type": "data", "kind": "counter", "t": 95.0, "dur": 2.0, "value": "5", "unit": "MONTHS", "label": "IN SPIKES", "sub": "AND THE SEASON HASN'T STARTED"},
 M('keyword', 101.0, 2.4, text="HARD HEAD = SOFT A**"),
 M('keyword', 104.3, 2.6, text="WISE MAN LEARNS FROM OTHERS"),
 M('keyword', 108.3, 1.5, text="FOOL LEARNS FROM HIS OWN"),
 M('poll', 109.9, 2.4, question="SPIKES BEFORE HALLOWEEN?", options=["NEVER", "GUILTY"]),
]
plan = {"workdir": "build", "output": "out/rylan_noome.mp4", "words": "work/words_final.json", "voice_ss": 0.0,
        "duration": 112.33, "min_duration": 61, "face": {"src": "work/face_tight.mov", "focus": [0.5, 0.5]},
        "zooms": [[3.5, 4.4, 1.22], [57.0, 58.0, 1.1], [68.9, 70.9, 1.12], [96.7, 97.6, 1.1]],
        "meme_sfx": [["sfx/vine_boom.wav", 3.47, 0.5]],     # owner: vine boom right after "don't you ever go against this shit"
        "segments": segs, "graphics": GFX}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments,', len(GFX), 'graphics')
