"""NIL reality check: plan.json for editor/build.py (Yohan Blake house style)."""
import json
B = lambda i, ss=0: (f'br/p{i}.mp4', ss)
SEG = [  # start, type, (src, ss), focus, hit
 (0.0,  'full',  B(37253080, 0),          [0.5, 0.55], False),
 (2.6,  'split', B(7362704, 2),           [0.5, 0.5],  False),
 (6.7,  'full',  B(35701013, 0),          [0.5, 0.5],  False),
 (8.6,  'split', ('up/livvy.mp4', 0),     [0.5, 0.3],  False),
 (12.4, 'split', ('up/clark.mp4', 0),     [0.5, 0.35], False),
 (14.2, 'split', B(6956639, 0),           [0.5, 0.6],  False),
 (16.7, 'split', B(6568265, 5),           [0.5, 0.5],  False),
 (18.7, 'full',  B(6266433, 1),           [0.5, 0.5],  False),
 (23.0, 'split', ('news/x8bid3z.mp4', 2.5), [0.5, 0.5], False),
 (27.6, 'split', B(8814522, 1),           [0.5, 0.5],  False),
 (31.1, 'split', ('news/x8bid3z.mp4', 8), [0.4, 0.4],  False),
 (34.7, 'split', B(8188831, 1),           [0.5, 0.45], False),
 (37.6, 'split', B(34719386, 1),          [0.5, 0.5],  False),
 (40.6, 'split', B(7735908, 2),           [0.5, 0.5],  False),
 (45.1, 'full',  B(36780065, 5),          [0.5, 0.5],  True),
 (46.5, 'split', B(30997018, 3),          [0.5, 0.55], False),
 (50.6, 'split', ('news/x8152v6.mp4', 46), [0.5, 0.5], False),
 (53.4, 'split', ('news/x8152v6.mp4', 40.5), [0.5, 0.5], False),
 (57.0, 'split', B(12893607, 2),          [0.5, 0.5],  False),
 (59.2, 'split', B(10145286, 2),          [0.5, 0.45], False),
 (62.6, 'split', B(11123558, 4),          [0.5, 0.6],  False),
 (66.9, 'split', ('up/reese.mp4', 0),     [0.5, 0.35], False),
 (69.0, 'split', B(10374888, 1),          [0.5, 0.5],  False),
 (71.0, 'full',  B(8170432, 1),           [0.5, 0.5],  True),
 (73.4, 'split', B(31229040, 10),         [0.5, 0.6],  False),
]
segs = []
for t, k, (src, ss), f, hit in SEG:
    d = {"type": k, "start": t, "broll": {"src": src, "ss": ss, "focus": f}}
    if hit: d["hit"] = True
    segs.append(d)
M = lambda kind, t, dur, **kw: {"type": "motion", "kind": kind, "t": t, "dur": dur, **kw}
GFX = [
 M('keyword', 0.3, 2.2, text="COLLEGE ATHLETES"),
 M('bubbles', 3.0, 3.4, items=["HOW DO I GET NIL?", "CAN YOU HELP ME GET A DEAL?", "WHO DO I DM?"]),
 M('stamp', 7.4, 1.6, text="FAMOUS PEOPLE", anchor="upper", size=96),
 M('keyword', 14.9, 1.8, text="FREE STUFF"),
 M('stamp', 17.2, 1.5, text="NOT REAL NIL", anchor="upper"),
 M('keyword', 21.4, 1.8, text="REAL BREAD"),
 M('flow', 24.2, 3.4, items=["NAME", "IMAGE", "LIKENESS"], times=[0.1, 0.7, 1.6]),
 M('stamp', 28.7, 1.3, text="FAIR EXCHANGE", anchor="upper"),
 M('keyword', 29.9, 1.2, text="NOT A ROBBERY"),
 M('keyword', 32.1, 1.9, text="NAME + BRAND"),
 M('keyword', 36.0, 1.6, text="MARKETABILITY"),
 M('keyword', 38.2, 1.6, text="PROFIT MARGINS"),
 M('board', 41.1, 3.9, title="WHO BENEFITS?", rows=[{"event": "THE COMPANY", "value": "ALL OF IT"}, {"event": "YOU", "value": "NOTHING"}], times=[0.6, 2.9]),
 M('stamp', 45.5, 1.3, text="NO NAME", anchor="upper"),
 M('keyword', 47.2, 1.6, text="GREATEST IN YOUR SPORT?"),
 M('stamp', 49.6, 1.0, text="NOT VALUABLE", anchor="upper"),
 M('keyword', 51.3, 1.9, text="NAME · IMAGE · LIKENESS"),
 M('stamp', 54.6, 1.0, text="UNKNOWN", anchor="upper"),
 M('keyword', 57.2, 1.7, text="WHAT DO YOU OFFER?"),
 M('keyword', 60.6, 1.3, text="NIL DMs"),
 M('stamp', 65.7, 1.2, text="NO PICTURES?", anchor="upper"),
 M('keyword', 68.2, 1.3, text="BIG NAME"),
 M('keyword', 70.1, 1.0, text="FOLLOWERS?"),
 M('stamp', 72.6, 1.0, text="NOT INTERESTED", anchor="upper", size=96),
 M('poll', 73.4, 2.26, question="WOULD A BRAND PAY YOU?", options=["YES", "NOT YET"]),
]
plan = {"workdir": "build", "output": "out/nil_reality.mp4", "words": "work/words_final.json", "voice_ss": 0.0,
        "duration": 75.666, "min_duration": 61, "face": {"src": "work/face_tight.mov", "focus": [0.5, 0.5]},
        "zooms": [[9.8, 11.6, 1.08], [57.1, 58.8, 1.12], [74.4, 75.6, 1.1]],
        "segments": segs, "graphics": GFX}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments,', len(GFX), 'graphics')
