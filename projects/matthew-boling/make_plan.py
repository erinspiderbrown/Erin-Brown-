"""Matthew Boling downfall doc: writes plan.json (build.py) and top.json (toptrack.py).
Audio-only voiceover, so the split's top half is a news-footage track (top.mov) and full-screen moments are photos.
Photos missing on disk fall back to the second name so the plan always renders."""
import json, os
from PIL import Image
DUR = 380.4
NBC, FOX, ABCI, ABCR1, ABCR2 = 'yt/nbc.mp4', 'up/fox_race.mp4', 'up/abc_int.mp4', 'up/abc_race1.mp4', 'up/abc_race2.mp4'
def ok(p):
    try: Image.open(p).verify(); return True
    except Exception: return False
def ph(name, fb):
    p = f'ph/{name}.jpg' if not name.startswith('gph/') else name + '.jpg'
    return p if ok(p) else (f'ph/{fb}.jpg' if not fb.startswith('gph/') else fb + '.jpg')

# ---- top track: clean source ranges only (never drifts into an unrelated interview) ----
POOL = {
 'race': (NBC, 0.2, 8.4, [0.5, 0.5]), 'board': (NBC, 9.0, 11.8, [0.55, 0.4]), 'intA': (NBC, 12.0, 14.5, [0.6, 0.4]),
 'walk': (NBC, 19.6, 22.4, [0.55, 0.5]), 'stairs': (NBC, 23.4, 26.4, [0.5, 0.5]), 'run': (NBC, 27.0, 30.6, [0.5, 0.45]),
 'elevate': (NBC, 42.0, 43.8, [0.6, 0.5]), 'start': (NBC, 44.0, 48.0, [0.5, 0.5]), 'intB': (NBC, 51.8, 54.6, [0.6, 0.4]),
 'twins': (NBC, 55.0, 58.6, [0.5, 0.5]), 'prom': (NBC, 59.0, 61.8, [0.5, 0.4]), 'blocks': (NBC, 66.3, 68.6, [0.5, 0.5]),
 'watch': (NBC, 69.0, 69.9, [0.5, 0.5]), 'sprint': (NBC, 70.0, 71.8, [0.5, 0.5]),
 'fox': (FOX, 0.0, 4.5, [0.42, 0.5]), 'fox2': (FOX, 4.5, 8.3, [0.42, 0.5]), 'fox3': (FOX, 8.3, 11.9, [0.42, 0.5]), 'foxall': (FOX, 0.0, 11.9, [0.42, 0.5]), 'abci': (ABCI, 0.1, 8.3, [0.42, 0.4]),
 'surreal': (NBC, 11.85, 14.80, [0.6, 0.4]), 'coach': (NBC, 14.86, 20.05, [0.6, 0.45]), 'dad': (NBC, 36.62, 41.92, [0.4, 0.4]),
 'boltq': (NBC, 51.72, 54.95, [0.6, 0.4]),
}
# per split segment start: which clips fill the top half, in order (cycled if the segment is longer)
TOPSEQ = {
 0.0: ['race'], 3.0: ['fox'], 7.5: ['fox2'], 11.3: ['fox3', 'board'], 15.6: ['board', 'intA'], 21.6: ['run', 'race'], 28.0: ['race'],
 32.4: ['intB'], 44.6: ['abci'], 49.0: ['abci'], 53.4: ['board', 'intA'], 58.6: ['race'], 64.4: ['board', 'run'],
 77.2: ['start', 'sprint'], 82.2: ['intA', 'walk'], 97.6: ['intB', 'stairs'], 101.9: ['stairs', 'run', 'intA'],
 108.4: ['run'], 116.9: ['surreal'], 120.35: ['coach'], 138.3: ['blocks', 'sprint', 'start'], 160.3: ['start', 'run'],
 174.8: ['sprint', 'watch', 'blocks'], 178.8: ['run', 'intB'], 190.4: ['twins', 'prom'], 200.4: ['elevate', 'start'],
 204.8: ['walk', 'blocks'], 212.4: ['stairs', 'run'], 236.3: ['walk', 'elevate'], 241.0: ['start'], 245.0: ['elevate', 'stairs'],
 249.6: ['dad'], 258.8: ['race', 'board'], 280.1: ['stairs', 'blocks'], 290.8: ['start', 'run', 'stairs'],
 298.8: ['sprint', 'watch', 'intA'], 329.1: ['intA', 'intB'], 333.3: ['boltq'], 337.0: ['foxall'], 346.9: ['board', 'intA', 'stairs'],
 357.4: ['blocks', 'start'], 369.9: ['intB', 'run'],
}
# ---- segments: (start, type, src, ss, focus, extra) ----
c1, c2 = 'ph/c1.jpg', 'ph/c2.jpg'
TRIALS24 = ph('c3', 'gph/zurich400'); BUD = ph('c4', 'c2'); MIX = ph('c6', 'gph/istanbul400')
BOLT1 = ph('b1', 'gph/istanbul400'); BOLT2 = ph('b2', 'gph/zurich400'); BOLT3 = ph('b3', 'gph/istanbul400'); BOLT4 = ph('b4', 'gph/zurich400')
G = lambda n: f'gph/{n}.jpg'
SEG = [
 (0.0,  'split', ABCR2, 0.0, [0.5, 0.5], {}),
 (3.0,  'split', ABCR1, 0.0, [0.5, 0.5], {}),
 (7.5,  'split', ABCR2, 0.0, [0.5, 0.5], {}),
 (11.3, 'split', G('wpgtrack'), 0, [0.5, 0.5], {}),
 (15.6, 'split', G('getset'), 0, [0.55, 0.6], {}),
 (21.6, 'split', NBC, 2.0, [0.5, 0.5], {}),
 (28.0, 'split', ABCR1, 1.0, [0.5, 0.5], {}),
 (32.4, 'split', NBC, 49.0, [0.5, 0.4], {}),
 (35.2, 'full', c1, 0, [0.6, 0.3], {}),
 (38.2, 'full', c2, 0, [0.5, 0.3], {}),
 (42.3, 'full', G('markel'), 0, [0.42, 0.4], {'hit': True}),
 (44.6, 'split', ABCR2, 0.3, [0.5, 0.5], {}),
 (49.0, 'split', G('wpgtrack'), 0, [0.6, 0.5], {}),
 (53.4, 'split', NBC, 9.2, [0.55, 0.4], {}),
 (58.6, 'split', NBC, 3.0, [0.5, 0.5], {}),
 (64.4, 'split', NBC, 7.0, [0.5, 0.5], {}),
 (67.2, 'full', G('istanbul400'), 0, [0.35, 0.5], {}),
 (71.2, 'full', G('zurich400'), 0, [0.62, 0.5], {}),
 (77.2, 'split', NBC, 27.0, [0.5, 0.5], {}),
 (82.2, 'split', c2, 0, [0.5, 0.5], {}),
 (85.6, 'full', G('getset'), 0, [0.45, 0.6], {}),
 (90.8, 'full', G('istanbul400'), 0, [0.75, 0.5], {}),
 (97.6, 'split', NBC, 44.3, [0.5, 0.5], {}),
 (101.9, 'split', NBC, 59.0, [0.5, 0.4], {}),
 (108.4, 'split', NBC, 66.3, [0.5, 0.5], {}),
 (111.2, 'full', c2, 0, [0.5, 0.25], {}),
 (116.9, 'split', NBC, 6.0, [0.5, 0.5], {}),
 (120.35, 'split', NBC, 20.3, [0.5, 0.5], {}),
 (126.2, 'full', c2, 0, [0.52, 0.35], {}),
 (131.6, 'full', c1, 0, [0.6, 0.35], {}),
 (138.3, 'split', c1, 0, [0.6, 0.4], {}),
 (143.3, 'full', G('zurich400'), 0, [0.3, 0.5], {}),
 (149.9, 'full', G('istanbul400'), 0, [0.2, 0.5], {}),
 (154.7, 'full', G('markel'), 0, [0.4, 0.4], {'hit': True}),
 (160.3, 'split', G('getset'), 0, [0.55, 0.5], {}),
 (165.2, 'full', c1, 0, [0.62, 0.5], {}),
 (170.6, 'full', c2, 0, [0.48, 0.4], {}),
 (174.8, 'split', G('zurich400'), 0, [0.5, 0.5], {}),
 (178.8, 'split', c1, 0, [0.6, 0.5], {}),
 (184.8, 'full', G('markel'), 0, [0.45, 0.45], {}),
 (190.4, 'split', G('zurich400'), 0, [0.8, 0.5], {}),
 (196.9, 'full', G('istanbul400'), 0, [0.5, 0.5], {}),
 (200.4, 'split', c2, 0, [0.5, 0.45], {}),
 (204.8, 'split', G('wpgtrack'), 0, [0.4, 0.5], {}),
 (208.9, 'full', G('zurich400'), 0, [0.15, 0.5], {}),
 (212.4, 'split', G('istanbul400'), 0, [0.5, 0.5], {}),
 (217.0, 'full', c1, 0, [0.5, 0.3], {'crop': [1260, 2240, 1650, 0]}),
 (227.2, 'full', c2, 0, [0.52, 0.4], {}),
 (231.8, 'full', c2, 0, [0.5, 0.5], {'crop': [1080, 1920, 1450, 560]}),
 (236.3, 'split', c2, 0, [0.5, 0.5], {}),
 (241.0, 'split', NBC, 42.0, [0.6, 0.5], {}),
 (245.0, 'split', G('getset'), 0, [0.45, 0.6], {}),
 (249.6, 'split', c1, 0, [0.6, 0.4], {}),
 (255.7, 'full', G('getset'), 0, [0.5, 0.6], {}),
 (258.8, 'split', NBC, 6.0, [0.5, 0.5], {}),
 (263.8, 'full', G('zurich400'), 0, [0.5, 0.5], {}),
 (268.8, 'full', c1, 0, [0.62, 0.4], {}),
 (273.4, 'full', G('wpgtrack'), 0, [0.5, 0.5], {}),
 (280.1, 'split', G('markel'), 0, [0.45, 0.5], {}),
 (286.2, 'full', G('markel'), 0, [0.4, 0.3], {'hit': True}),
 (290.8, 'split', G('zurich400'), 0, [0.5, 0.5], {}),
 (298.8, 'split', G('wpgtrack'), 0, [0.5, 0.5], {}),
 (305.0, 'full', c1, 0, [0.6, 0.4], {}),
 (313.5, 'full', c1, 0, [0.5, 0.3], {'crop': [1260, 2240, 1650, 0]}),
 (318.9, 'full', c2, 0, [0.5, 0.35], {}),
 (322.2, 'full', G('istanbul400'), 0, [0.4, 0.5], {}),
 (329.1, 'split', NBC, 48.9, [0.5, 0.4], {}),
 (333.3, 'split', NBC, 49.0, [0.5, 0.5], {}),
 (337.0, 'split', ABCR2, 0.0, [0.5, 0.5], {}),
 (341.2, 'full', c2, 0, [0.5, 0.3], {'crop': [1080, 1920, 1450, 560]}),
 (346.9, 'split', G('wpgtrack'), 0, [0.5, 0.5], {}),
 (352.9, 'full', G('zurich400'), 0, [0.7, 0.5], {}),
 (357.4, 'split', G('getset'), 0, [0.5, 0.5], {}),
 (363.9, 'full', c1, 0, [0.6, 0.3], {}),
 (369.9, 'split', c2, 0, [0.5, 0.4], {}),
 (373.9, 'full', c2, 0, [0.5, 0.3], {}),
]
GFX = [
 {"type": "motion", "kind": "keyword", "t": 0.25, "dur": 2.4, "text": "WHITE LIGHTNING"},
 {"type": "motion", "kind": "calendar", "t": 3.1, "dur": 2.7, "items": ["2017", "2018", "2019", "2020"], "hi": [2], "label": "APRIL 27, 2019"},
 {"type": "motion", "kind": "pin", "t": 5.7, "dur": 2.9, "text": "HOUSTON, TEXAS", "sub": "6A REGION III MEET"},
 {"type": "name", "t": 8.7, "dur": 2.7, "rank": "HS", "name": "MATTHEW BOLING", "sub": "STRAKE JESUIT · SENIOR"},
 {"type": "motion", "kind": "stopwatch", "t": 11.6, "dur": 3.8, "value": "9.98", "unit": "100M", "label": "HIGH SCHOOL · ALL CONDITIONS", "anim": 0.9},
 {"type": "motion", "kind": "wind", "t": 16.1, "dur": 2.4, "text": "WIND +4.2 M/S", "sub": "LEGAL LIMIT +2.0"},
 {"type": "motion", "kind": "stamp", "t": 18.8, "dur": 1.8, "text": "WIND-AIDED", "anchor": "lower"},
 {"type": "motion", "kind": "scoreboard", "t": 21.0, "dur": 3.5, "title": "6A BOYS 100M — REGION III", "times": [0.4, 0.8, 1.1, 1.4], "rows": [{"place": "1", "name": "MATTHEW BOLING", "team": "STRAKE JESUIT", "time": "9.98"}, {"place": "2", "name": "LANCE BROOME", "team": "SEVEN LAKES", "time": "10.27"}, {"place": "3", "name": "DORIAN HEWITT", "team": "NORTH SHORE", "time": "10.33"}, {"place": "4", "name": "CAMERON CROWE", "team": "CYPRESS RIDGE", "time": "10.47"}], "hi": 0},
 {"type": "motion", "kind": "tv", "t": 24.6, "dur": 4.9, "text": "ESPN · CBS · FOX · SI"},
 {"type": "motion", "kind": "keyword", "t": 30.2, "dur": 2.2, "text": "\"WHITE LIGHTNING\""},
 {"type": "motion", "kind": "bubbles", "t": 32.6, "dur": 2.6, "items": ["THE NEXT USAIN BOLT", "FASTEST HS KID EVER", "OLYMPICS NEXT YEAR"]},
 {"type": "name", "t": 35.5, "dur": 2.6, "rank": "USA", "name": "MATTHEW BOLING", "sub": "\"WHITE LIGHTNING\""},
 {"type": "motion", "kind": "stamp", "t": 38.6, "dur": 2.8, "text": "7 YEARS LATER", "anchor": "upper"},
 {"type": "motion", "kind": "stamp", "t": 42.6, "dur": 1.8, "text": "WHAT HAPPENED?", "size": 120},
 {"type": "motion", "kind": "podcast", "t": 44.8, "dur": 7.8, "text": "MATTHEW BOLING", "tag": "THE DAY AFTER · ABC13", "anchor": "lower"},
 {"type": "motion", "kind": "stamp", "t": 57.1, "dur": 1.6, "text": "NOT A FLUKE", "anchor": "lower"},
 {"type": "motion", "kind": "pin", "t": 59.0, "dur": 2.6, "text": "TEXAS STATE MEET", "sub": "UIL 6A · AUSTIN · MAY 2019"},
 {"type": "data", "kind": "counter", "t": 61.6, "dur": 3.6, "value": "10.13", "unit": "S", "label": "U.S. HIGH SCHOOL RECORD", "sub": "100M · WIND-LEGAL"},
 {"type": "motion", "kind": "board", "t": 67.4, "dur": 3.9, "title": "LONG JUMP · 2019", "rows": [{"event": "STATE TITLE", "value": "25'4.5\"", "tag": "WIND+"}, {"event": "PB · TEXAS RELAYS", "value": "26'3.5\""}], "times": [0.3, 1.9]},
 {"type": "motion", "kind": "track", "t": 72.0, "dur": 5.0, "value": "44.74", "anim": 1.4, "text": "4X400 ANCHOR SPLIT", "sub": "FROM 20+ METERS BEHIND"},
 {"type": "motion", "kind": "stamp", "t": 79.7, "dur": 1.8, "text": "STATE CHAMPS", "anchor": "lower"},
 {"type": "name", "t": 82.6, "dur": 3.0, "rank": "2019", "name": "GATORADE NATIONAL", "sub": "BOYS TRACK & FIELD PLAYER OF THE YEAR"},
 {"type": "motion", "kind": "pin", "t": 86.0, "dur": 2.8, "text": "SAN JOSÉ, COSTA RICA", "sub": "PAN AM U20 CHAMPIONSHIPS"},
 {"type": "motion", "kind": "board", "t": 89.2, "dur": 8.0, "title": "PAN AM U20 · 4 GOLDS", "rows": [{"event": "100M", "value": "10.11"}, {"event": "200M", "value": "20.31"}, {"event": "4X100", "value": "38.62", "tag": "WU20R"}, {"event": "4X400", "value": "2:59.30", "tag": "WU20R"}], "times": [1.7, 2.5, 3.4, 4.9]},
 {"type": "motion", "kind": "keyword", "t": 98.4, "dur": 2.8, "text": "HE DIDN'T LIKE THE NICKNAME"},
 {"type": "motion", "kind": "bubbles", "t": 102.2, "dur": 5.0, "items": ["WHITE LIGHTNING", "NEXT BOLT?", "THE FASTEST WHITE GUY"]},
 {"type": "motion", "kind": "keyword", "t": 108.6, "dur": 2.2, "text": "JUST WANTED TO RUN"},
 {"type": "name", "t": 111.4, "dur": 2.6, "rank": "UGA", "name": "GEORGIA BULLDOGS", "sub": "COMMITTED · 2019"},
 {"type": "motion", "kind": "keyword", "t": 114.4, "dur": 2.2, "text": "SOMETHING CRAZY"},
 {"type": "motion", "kind": "podcast", "t": 117.1, "dur": 3.0, "text": "MATTHEW BOLING", "tag": "NBC NIGHTLY NEWS · 2019", "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 123.5, "dur": 2.4, "text": "BIG-STAGE PERFORMER"},
 {"type": "motion", "kind": "calendar", "t": 126.4, "dur": 2.6, "items": ["2019", "2020", "2021"], "hi": [1], "label": "FRESHMAN YEAR"},
 {"type": "motion", "kind": "stamp", "t": 129.2, "dur": 1.8, "text": "COVID", "anchor": "lower"},
 {"type": "data", "kind": "counter", "t": 133.7, "dur": 4.3, "value": "20.19", "unit": "S", "label": "NCAA INDOOR 200M CHAMPION", "sub": "2021 · GEORGIA"},
 {"type": "motion", "kind": "keyword", "t": 140.6, "dur": 2.3, "text": "RIGHT ON SCHEDULE"},
 {"type": "motion", "kind": "pin", "t": 143.5, "dur": 2.0, "text": "EUGENE, OREGON", "sub": "2021 OLYMPIC TRIALS"},
 {"type": "motion", "kind": "board", "t": 145.6, "dur": 8.6, "title": "2021 OLYMPIC TRIALS", "rows": [{"event": "100M · SEMIS", "value": "14TH"}, {"event": "200M · SEMIS", "value": "9TH", "tag": "1 SPOT OUT"}], "times": [1.8, 5.3]},
 {"type": "motion", "kind": "stamp", "t": 158.0, "dur": 1.9, "text": "NOT HIGH SCHOOL", "size": 110},
 {"type": "motion", "kind": "keyword", "t": 160.6, "dur": 2.9, "text": "THE PART PEOPLE FORGET"},
 {"type": "motion", "kind": "stopwatch", "t": 165.3, "dur": 4.9, "value": "9.98", "unit": "100M", "label": "TOM JONES MEMORIAL · +1.6", "anim": 0.8},
 {"type": "motion", "kind": "stamp", "t": 169.4, "dur": 1.4, "text": "LEGAL", "anchor": "upper"},
 {"type": "motion", "kind": "stopwatch", "t": 171.0, "dur": 3.7, "value": "19.92", "unit": "200M", "label": "GEORGIA TECH INVITE · 1 WEEK LATER", "anim": 1.0},
 {"type": "motion", "kind": "board", "t": 175.0, "dur": 3.8, "title": "2022 · 200M", "rows": [{"event": "SEC CHAMPS", "value": "1ST", "tag": "20.01"}, {"event": "NCAA CHAMPS", "value": "2ND", "tag": "20.13"}], "times": [0.4, 2.2]},
 {"type": "motion", "kind": "keyword", "t": 181.0, "dur": 3.1, "text": "SUB-10 · SUB-20"},
 {"type": "motion", "kind": "board", "t": 185.0, "dur": 2.7, "title": "2022 USA CHAMPS · 200M", "rows": [{"event": "MATTHEW BOLING", "value": "6TH", "tag": "20.15"}], "times": [1.6]},
 {"type": "motion", "kind": "stamp", "t": 189.5, "dur": 1.6, "text": "TOP 3 ONLY", "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 191.6, "dur": 3.2, "text": "TOP 10 IN THE WORLD"},
 {"type": "motion", "kind": "stamp", "t": 195.6, "dur": 1.6, "text": "STAYING HOME", "anchor": "upper"},
 {"type": "motion", "kind": "keyword", "t": 197.6, "dur": 2.4, "text": "THAT DEEP"},
 {"type": "data", "kind": "counter", "t": 202.0, "dur": 2.8, "value": "20.12", "unit": "S", "label": "NCAA INDOOR 200M CHAMPION", "sub": "2023 · TITLE NO. 2"},
 {"type": "motion", "kind": "stamp", "t": 207.2, "dur": 1.6, "text": "NO FINAL", "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 209.3, "dur": 2.9, "text": "NEW EVENT: THE 400"},
 {"type": "motion", "kind": "board", "t": 212.6, "dur": 4.3, "title": "2023 USA CHAMPS · 400M", "rows": [{"event": "MATTHEW BOLING", "value": "6TH", "tag": "45.17"}], "times": [1.6]},
 {"type": "motion", "kind": "pin", "t": 217.3, "dur": 3.0, "text": "BUDAPEST, HUNGARY", "sub": "2023 WORLD CHAMPIONSHIPS"},
 {"type": "motion", "kind": "board", "t": 221.8, "dur": 4.6, "title": "MIXED 4X400 · BUDAPEST", "rows": [{"event": "USA · BOLING 3RD LEG", "value": "3:08.80", "tag": "WR"}], "times": [0.4]},
 {"type": "motion", "kind": "stamp", "t": 224.9, "dur": 1.4, "text": "GOLD", "anchor": "upper"},
 {"type": "motion", "kind": "keyword", "t": 227.4, "dur": 4.0, "text": "MEN'S 4X400: GOLD TOO"},
 {"type": "motion", "kind": "stamp", "t": 233.4, "dur": 2.6, "text": "2X WORLD CHAMPION", "size": 110},
 {"type": "motion", "kind": "flow", "t": 236.5, "dur": 5.4, "items": ["LEAVES GEORGIA", "TURNS PRO", "SOUTH CAROLINA"], "times": [1.4, 3.4, 4.9]},
 {"type": "name", "t": 245.5, "dur": 2.7, "rank": "PRO", "name": "ALLEYNE FRANCIQUE", "sub": "NEW COACH"},
 {"type": "motion", "kind": "keyword", "t": 247.9, "dur": 1.7, "text": "THE WORLD STAGE"},
 {"type": "name", "t": 249.9, "dur": 3.0, "rank": "DAD", "name": "MARK BOLING", "sub": "NBC NIGHTLY NEWS · 2019"},
 {"type": "motion", "kind": "calendar", "t": 255.9, "dur": 2.7, "items": ["2021", "2022", "2023", "2024"], "hi": [3], "label": "THE OLYMPIC YEAR"},
 {"type": "motion", "kind": "keyword", "t": 259.6, "dur": 3.0, "text": "THE ONE EVERYBODY WAITED ON"},
 {"type": "motion", "kind": "track", "t": 264.0, "dur": 4.4, "value": "44.84", "anim": 1.0, "text": "400M PERSONAL BEST", "sub": "2024"},
 {"type": "motion", "kind": "board", "t": 268.9, "dur": 4.3, "title": "2024 · USA RELAYS", "rows": [{"event": "WORLD INDOORS", "value": "SILVER"}, {"event": "WORLD RELAYS", "value": "GOLD"}], "times": [0.9, 3.1]},
 {"type": "motion", "kind": "scoreboard", "t": 274.0, "dur": 5.8, "title": "2024 OLYMPIC TRIALS — 400M FINAL", "times": [0.5, 4.5], "rows": [{"place": "1", "name": "QUINCY HALL", "team": "USA", "time": "44.17"}, {"place": "8", "name": "MATTHEW BOLING", "team": "USA", "time": "45.15"}], "hi": 1},
 {"type": "motion", "kind": "board", "t": 280.3, "dur": 5.2, "title": "2024 TRIALS · 200M", "rows": [{"event": "MATTHEW BOLING", "value": "9TH", "tag": "NO FINAL"}], "times": [3.2]},
 {"type": "motion", "kind": "stamp", "t": 289.2, "dur": 1.6, "text": "NO PARIS", "size": 160},
 {"type": "motion", "kind": "pin", "t": 291.0, "dur": 3.3, "text": "PHILADELPHIA", "sub": "GRAND SLAM TRACK · 2025"},
 {"type": "data", "kind": "bars", "t": 294.8, "dur": 4.0, "label": "Grand Slam Philly · 200m", "unit": "S", "lower_is_better": True, "spread": 0.4, "items": [{"name": "Boling (7th)", "value": "20.87"}]},
 {"type": "motion", "kind": "board", "t": 298.9, "dur": 3.6, "title": "GRAND SLAM PHILLY · 400M", "rows": [{"event": "MATTHEW BOLING", "value": "5TH", "tag": "45.21"}], "times": [0.4]},
 {"type": "data", "kind": "compare", "t": 305.3, "dur": 6.8, "label": "100M · BEST TIME", "unit": "S", "base": 9.5, "badge": "SAME", "items": [{"name": "AT 18 (WIND+)", "value": "9.98"}, {"name": "TODAY (PB)", "value": "9.98"}]},
 {"type": "motion", "kind": "board", "t": 313.8, "dur": 8.2, "title": "THE RESUME", "rows": [{"event": "WORLD TITLES", "value": "2", "tag": "RELAYS"}, {"event": "100M PB", "value": "9.98"}, {"event": "200M PB", "value": "19.92"}, {"event": "400M PB", "value": "44.84"}], "times": [2.4, 5.4, 7.1, 7.8]},
 {"type": "motion", "kind": "keyword", "t": 322.5, "dur": 3.5, "text": "MOST WOULD KILL FOR THAT"},
 {"type": "motion", "kind": "stamp", "t": 327.4, "dur": 1.6, "text": "BUT...", "anchor": "upper"},
 {"type": "name", "t": 329.4, "dur": 2.3, "rank": "JAM", "name": "USAIN BOLT", "sub": "WORLD RECORD · 9.58"},
 {"type": "motion", "kind": "podcast", "t": 333.5, "dur": 3.0, "text": "MATTHEW BOLING", "tag": "NBC NIGHTLY NEWS · 2019", "anchor": "lower"},
 {"type": "motion", "kind": "stamp", "t": 339.6, "dur": 1.6, "text": "NOT LEGAL", "anchor": "lower"},
 {"type": "motion", "kind": "bubbles", "t": 343.4, "dur": 3.4, "items": ["NEXT BOLT", "OLYMPIC CHAMP SOON", "GOAT IN THE MAKING"]},
 {"type": "motion", "kind": "wind", "t": 349.3, "dur": 3.0, "text": "ONE CLIP · +4.2 M/S", "sub": "TAILWIND"},
 {"type": "motion", "kind": "keyword", "t": 354.9, "dur": 2.4, "text": "HARDEST TEAM TO MAKE"},
 {"type": "motion", "kind": "stamp", "t": 361.0, "dur": 2.0, "text": "STILL HOME", "anchor": "lower"},
 {"type": "motion", "kind": "poll", "t": 364.3, "dur": 9.6, "question": "DOWNFALL OR TOO MUCH HYPE?", "options": ["DOWNFALL", "TOO MUCH HYPE"]},
 {"type": "motion", "kind": "keyword", "t": 374.3, "dur": 3.5, "text": "BOLING HYPE TRAIN 2019?"},
 {"type": "motion", "kind": "stamp", "t": 377.9, "dur": 2.5, "text": "BE HONEST", "anchor": "upper"},
]
TL = {x['label']: x['out_s'] for x in json.load(open('work/timeline.json'))}
SYNC = {'surreal': ('nbc_surreal', 11.85), 'coach': ('nbc_coach', 14.86), 'dad': ('nbc_dad', 36.62), 'boltq': ('nbc_bolt', 51.72),
        'abci': ('abc_boling', 0.1)}
TOP = []
_starts = [x[0] for x in SEG] + [DUR]
for i, (st, ty, *_r) in enumerate(SEG):
    if ty != 'split': continue
    en = _starts[i + 1]; seq = TOPSEQ.get(st, ['run']); t = st; k = 0
    while t < en - 0.05:
        key = seq[k % len(seq)]; src, a, b, foc = POOL[key]; ss = a
        if key in SYNC:                      # interview clips: lip-synced to where their audio sits in the voice track
            ss = max(0.0, a - 0.3, SYNC[key][1] + (t - TL[SYNC[key][0]]))
        d = min(b - ss, en - t) if key not in SYNC else en - t
        TOP.append((round(t, 3), src, round(ss, 3), foc)); t += d; k += 1
segs = []
for s, ty, src, ss, foc, ex in SEG:
    ex = dict(ex); cr = ex.pop('crop', None)
    d = {"type": ty, "start": s, "broll": {"src": src, "ss": ss, "focus": foc}}
    if cr: d['broll']['fullcrop'] = cr
    d.update(ex); segs.append(d)
plan = {"workdir": "build", "output": "out/matthew_boling.mp4", "words": "work/words.json", "voice_ss": 0.0, "duration": DUR,
        "face": {"src": "top.mov", "focus": [0.5, 0.5]}, "face_grade": "vignette=PI/6",
        "zooms": [[42.6, 44.4, 1.1], [154.7, 156.9, 1.08], [364.1, 366.3, 1.08]],
        "segments": segs, "graphics": GFX}
json.dump(plan, open('plan.json', 'w'), indent=1)
json.dump({"duration": DUR, "voice": "work/voice.wav", "shots": [{"t": t, "src": s, "ss": ss, "focus": f} for t, s, ss, f in TOP]}, open('top.json', 'w'), indent=1)
print(len(segs), 'segments', len(GFX), 'graphics; full-screen share:',
      round(sum((segs[i+1]['start'] if i+1 < len(segs) else DUR) - x['start'] for i, x in enumerate(segs) if x['type'] == 'full') / DUR * 100), '%')
