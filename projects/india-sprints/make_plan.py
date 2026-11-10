"""India sprints TikTok: writes plan.json for editor/build.py (talking head on top, house style)."""
import json
DUR = 121.6
BW, JM, IN, SC = 'geo/map_bw.jpg', 'geo/map_jm.jpg', 'geo/map_in.jpg', 'geo/size_compare.jpg'
RACE = 'mine/may_cc.mp4'; G = lambda n: f'gph/{n}.jpg'
SEG = [  # (start, type, src, ss, focus, extra)
 (0.0,   'full',  BW, 0, [0.5, 0.42], {}),
 (4.1,   'split', BW, 0, [0.5, 0.40], {}),
 (9.2,   'full',  JM, 0, [0.5, 0.44], {}),
 (13.0,  'split', JM, 0, [0.5, 0.44], {}),
 (19.6,  'full',  IN, 0, [0.5, 0.42], {'hit': True}),
 (25.5,  'split', IN, 0, [0.5, 0.42], {}),
 (30.6,  'split', SC, 0, [0.5, 0.30], {}),
 (37.7,  'split', RACE, 1.0, [0.5, 0.5], {}),
 (41.6,  'split', G('getset'), 0, [0.55, 0.6], {}),
 (45.4,  'split', G('wpgtrack'), 0, [0.5, 0.5], {}),
 (51.7,  'full',  SC, 0, [0.5, 0.5], {}),
 (55.2,  'split', G('zurich400'), 0, [0.5, 0.5], {}),
 (59.2,  'full',  IN, 0, [0.5, 0.40], {}),
 (66.0,  'split', RACE, 6.0, [0.5, 0.5], {}),
 (71.7,  'split', G('istanbul400'), 0, [0.5, 0.5], {}),
 (78.8,  'full',  IN, 0, [0.5, 0.45], {}),
 (85.1,  'split', SC, 0, [0.5, 0.75], {}),
 (89.3,  'split', G('wpgtrack'), 0, [0.4, 0.5], {}),
 (97.9,  'full',  RACE, 1.5, [0.48, 0.5], {}),
 (100.8, 'split', G('getset'), 0, [0.45, 0.6], {}),
 (111.6, 'full',  IN, 0, [0.5, 0.42], {'hit': True}),
 (115.6, 'split', SC, 0, [0.5, 0.40], {}),
]
GFX = [
 {"type": "data", "kind": "counter", "t": 1.4, "dur": 2.6, "value": "2.5", "unit": "MILLION", "label": "BOTSWANA · POPULATION", "sub": "UN 2025 ESTIMATE"},
 {"type": "motion", "kind": "board", "t": 4.3, "dur": 4.8, "title": "BOTSWANA · GLOBAL GOLD", "rows": [{"event": "MONTSHO 400M '11", "value": "WORLD"}, {"event": "TEBOGO 200M '24", "value": "OLYMPIC"}, {"event": "KEBINATSHIPI '25", "value": "WORLD"}, {"event": "4X400 TOKYO '25", "value": "WORLD"}], "times": [0.6, 2.5, 3.1, 3.7]},
 {"type": "data", "kind": "counter", "t": 10.6, "dur": 2.4, "value": "2.8", "unit": "MILLION", "label": "JAMAICA · POPULATION", "sub": "UN 2025 ESTIMATE"},
 {"type": "motion", "kind": "board", "t": 13.2, "dur": 6.2, "title": "JAMAICA · SPRINTS", "rows": [{"event": "BOLT 100M", "value": "9.58", "tag": "WR"}, {"event": "BOLT 200M", "value": "19.19", "tag": "WR"}, {"event": "4X100 MEN", "value": "36.84", "tag": "WR"}, {"event": "FRASER-PRYCE 100M", "value": "5X", "tag": "WORLD"}], "times": [0.7, 2.3, 2.9, 3.4]},
 {"type": "data", "kind": "counter", "t": 21.4, "dur": 3.9, "value": "1.46", "unit": "BILLION", "label": "INDIA · POPULATION", "sub": "UN 2025 ESTIMATE · NO. 1 IN THE WORLD"},
 {"type": "motion", "kind": "stamp", "t": 25.7, "dur": 3.6, "text": "0 SPRINT MEDALS", "size": 120, "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 30.7, "dur": 4.4, "text": "WHERE ARE INDIA'S SPRINTERS?"},
 {"type": "motion", "kind": "bubbles", "t": 37.9, "dur": 3.6, "items": ["IT'S A POPULATION THING", "MORE PEOPLE = MORE TALENT", "THEY'LL GET THERE"]},
 {"type": "motion", "kind": "keyword", "t": 42.1, "dur": 3.0, "text": "LOTS OF SPRINTERS"},
 {"type": "motion", "kind": "keyword", "t": 46.0, "dur": 5.0, "text": "GREAT DISTANCE RUNNERS"},
 {"type": "motion", "kind": "stamp", "t": 52.0, "dur": 2.6, "text": "GLOBALLY?", "size": 140, "anchor": "lower"},
 {"type": "motion", "kind": "pin", "t": 55.6, "dur": 3.4, "text": "BUDAPEST 2023", "sub": "WORLD CHAMPIONSHIPS"},
 {"type": "motion", "kind": "scoreboard", "t": 59.4, "dur": 6.4, "title": "MEN'S 4X400 — HEAT 1", "times": [0.6, 1.6], "rows": [{"place": "1", "name": "UNITED STATES", "team": "USA", "time": "2:58.47"}, {"place": "2", "name": "INDIA", "team": "IND", "time": "2:59.05"}]},
 {"type": "motion", "kind": "stamp", "t": 64.0, "dur": 1.9, "text": "ASIAN RECORD", "anchor": "upper"},
 {"type": "motion", "kind": "keyword", "t": 66.6, "dur": 4.4, "text": "A QUICK GLIMPSE"},
 {"type": "motion", "kind": "board", "t": 71.9, "dur": 6.4, "title": "INDIA · 4X400 BUDAPEST", "rows": [{"event": "HEAT · ASIAN RECORD", "value": "2:59.05"}, {"event": "FINAL", "value": "5TH"}], "times": [0.5, 3.6]},
 {"type": "data", "kind": "compare", "t": 80.0, "dur": 5.0, "label": "POPULATION (MILLIONS)", "unit": "M", "base": 0, "badge": "4X", "items": [{"name": "INDIA", "value": "1464"}, {"name": "USA", "value": "347"}]},
 {"type": "motion", "kind": "keyword", "t": 85.3, "dur": 3.8, "text": "A LOT OF ATHLETES"},
 {"type": "motion", "kind": "board", "t": 89.4, "dur": 8.4, "title": "MAIN SPORT?", "rows": [{"event": "INDIA", "value": "CRICKET"}, {"event": "USA", "value": "FOOTBALL"}, {"event": "BOTSWANA", "value": "SOCCER"}, {"event": "JAMAICA", "value": "TRACK"}], "times": [0.2, 1.5, 4.9, 7.4]},
 {"type": "motion", "kind": "keyword", "t": 98.4, "dur": 2.4, "text": "SAMPLE SIZE ALONE"},
 {"type": "motion", "kind": "board", "t": 101.0, "dur": 10.4, "title": "INDIA · NATIONAL RECORDS", "rows": [{"event": "100M · GURINDERVIR", "value": "10.09"}, {"event": "200M · KUJUR", "value": "20.32"}, {"event": "400M · VISHAL TK", "value": "44.98"}], "times": [1.3, 3.3, 8.2]},
 {"type": "motion", "kind": "stamp", "t": 112.0, "dur": 3.4, "text": "WHERE?", "size": 200, "anchor": "lower"},
 {"type": "motion", "kind": "poll", "t": 116.2, "dur": 5.4, "question": "DOES POPULATION MATTER?", "options": ["YES", "NO"]},
]
segs = [dict({"type": ty, "start": s, "broll": {"src": src, "ss": ss, "focus": foc}}, **ex) for s, ty, src, ss, foc, ex in SEG]
plan = {"workdir": "build", "output": "out/india_sprints.mp4", "words": "work/words_final.json", "voice_ss": 0.0, "duration": DUR,
        "face": {"src": "work/face_tight.mov", "focus": [0.5, 0.5]},
        "zooms": [[30.7, 34.9, 1.12], [52.0, 54.6, 1.1], [112.1, 115.0, 1.14], [116.4, 118.6, 1.08]],
        "segments": segs, "graphics": GFX}
json.dump(plan, open('plan.json', 'w'), indent=1)
print(len(segs), 'segments', len(GFX), 'graphics')
