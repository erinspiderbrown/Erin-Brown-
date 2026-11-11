"""Centrowitz TikTok: writes plan.json for editor/build.py. Times are output seconds of work/face_final.mov
(owner's take with two soundbites from the Tracksmith film cut in at 21.95 s and 63.45 s; see assemble.py)."""
import json
DUR = 97.48
FLAG = 'raw/photo2.webp'; MEDAL = 'ph/medal_2x.jpg'; G = lambda n: f'gph/{n}.jpg'
U = lambda n: f'up/{n}.mp4'
SEG = [
 (0.0,   'full',  FLAG, 0, [0.53, 0.3], {}),
 (9.3,   'split', MEDAL, 0, [0.5, 0.35], {}),
 (12.0,  'split', U('trackfront'), 0.0, [0.5, 0.5], {}),
 (18.0,  'split', U('office'), 0.0, [0.45, 0.5], {}),
 (21.95, 'split', U('city1'), 0.0, [0.5, 0.5], {}),
 (25.4,  'split', U('child'), 0.0, [0.5, 0.5], {}),
 (32.15, 'split', U('city2'), 0.0, [0.5, 0.5], {}),
 (36.9,  'full',  FLAG, 0, [0.22, 0.4], {'hit': True}),
 (45.1,  'split', G('zurich400'), 0, [0.5, 0.5], {}),
 (47.6,  'split', U('trackkid'), 0.0, [0.5, 0.5], {}),
 (51.4,  'split', MEDAL, 0, [0.5, 0.4], {}),
 (57.1,  'split', G('istanbul400'), 0, [0.5, 0.5], {}),
 (61.7,  'split', U('office'), 0.5, [0.5, 0.5], {}),
 (63.45, 'split', U('trackkid'), 0.2, [0.5, 0.5], {}),
 (68.0,  'split', U('city1'), 0.3, [0.5, 0.5], {}),
 (72.35, 'full',  FLAG, 0, [0.53, 0.25], {'hit': True}),
 (76.6,  'split', U('office'), 0.0, [0.5, 0.5], {}),
 (82.9,  'split', U('city2'), 0.0, [0.5, 0.5], {}),
 (86.3,  'split', U('trackfront'), 0.5, [0.5, 0.5], {}),
 (92.6,  'split', MEDAL, 0, [0.5, 0.35], {}),
 (94.2,  'full',  FLAG, 0, [0.6, 0.3], {}),
]
GFX = [
 {"type": "name", "t": 0.4, "dur": 3.4, "rank": "USA", "name": "MATTHEW CENTROWITZ", "sub": "OLYMPIC 1500M CHAMPION · RIO 2016"},
 {"type": "motion", "kind": "keyword", "t": 4.3, "dur": 2.6, "text": "NOT THE FLEX?"},
 {"type": "motion", "kind": "stamp", "t": 7.4, "dur": 1.9, "text": "NO ONE CARES", "anchor": "upper"},
 {"type": "motion", "kind": "board", "t": 12.3, "dur": 4.0, "title": "RIO 2016 · 1500M FINAL", "rows": [{"event": "CENTROWITZ (USA)", "value": "3:50.00", "tag": "GOLD"}], "times": [1.7]},
 {"type": "motion", "kind": "stamp", "t": 16.3, "dur": 1.8, "text": "1ST U.S. WIN SINCE 1908", "size": 90, "anchor": "lower"},
 {"type": "motion", "kind": "calendar", "t": 18.1, "dur": 2.0, "items": ["2016", "2026"], "hi": [1], "label": "10 YEARS LATER"},
 {"type": "motion", "kind": "keyword", "t": 20.2, "dur": 1.7, "text": "OFFICE JOB"},
 {"type": "name", "t": 22.2, "dur": 3.4, "rank": "DAD", "name": "MATT CENTROWITZ SR.", "sub": "HIS DAD · 1976 OLYMPIAN"},
 {"type": "motion", "kind": "keyword", "t": 32.9, "dur": 2.4, "text": "NO ONE REALLY CARES"},
 {"type": "motion", "kind": "board", "t": 37.9, "dur": 7.2, "title": "OLYMPIC 1500M CHAMPS", "rows": [{"event": "2000 · NOAH NGENY", "value": "KEN"}, {"event": "1996 · MORCELI", "value": "ALG"}, {"event": "1992 · FERMIN CACHO", "value": "ESP"}], "times": [1.3, 4.2, 6.3]},
 {"type": "motion", "kind": "bubbles", "t": 45.2, "dur": 2.4, "items": ["WHO?", "NEVER HEARD OF HIM", "WAIT, WHO WON?"]},
 {"type": "motion", "kind": "keyword", "t": 48.4, "dur": 3.0, "text": "COOL FOR A MOMENT"},
 {"type": "motion", "kind": "stamp", "t": 52.1, "dur": 2.8, "text": "REAL BENEFITS?", "size": 110, "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 57.3, "dur": 3.4, "text": "JUST AN OLYMPIAN?"},
 {"type": "motion", "kind": "stamp", "t": 61.9, "dur": 1.4, "text": "NO ONE CARES", "anchor": "lower"},
 {"type": "motion", "kind": "podcast", "t": 63.6, "dur": 8.5, "text": "MATT CENTROWITZ SR.", "tag": "HIS DAD", "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 72.6, "dur": 3.4, "text": "NOT THE FLEX"},
 {"type": "motion", "kind": "flow", "t": 76.6, "dur": 9.6, "items": ["TAKE THE BREAD", "BUILD SOMETHING", "LONGEVITY"], "times": [2.3, 6.5, 8.4]},
 {"type": "data", "kind": "counter", "t": 86.5, "dur": 5.0, "value": "35", "unit": "YEARS OLD", "label": "Entering the job market", "sub": "after the track"},
 {"type": "motion", "kind": "stamp", "t": 92.9, "dur": 1.4, "text": "INSANE", "size": 160},
 {"type": "motion", "kind": "poll", "t": 94.4, "dur": 3.08, "question": "OLYMPIC GOLD: WORTH IT?", "options": ["WORTH IT", "NOT THE FLEX"]},
]
segs = [dict({"type": ty, "start": s, "broll": {"src": src, "ss": ss, "focus": foc}}, **ex) for s, ty, src, ss, foc, ex in SEG]
plan = {"workdir": "build", "output": "out/centrowitz.mp4", "words": "work/words_final.json", "voice_ss": 0.0, "duration": DUR,
        "face": {"src": "work/face_final.mov", "focus": [0.5, 0.5]},
        "zooms": [[52.1, 54.9, 1.12], [94.3, 96.9, 1.1]], "segments": segs, "graphics": GFX}
json.dump(plan, open('plan.json', 'w'), indent=1); print(len(segs), 'segments', len(GFX), 'graphics')
