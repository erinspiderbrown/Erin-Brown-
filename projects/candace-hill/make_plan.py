"""Candace Hill doc (voiceover only): writes plan.json (build.py) + top.json (toptrack.py).
Split = photo with slow push-in on top, a second photo / place scene below; full = sharp photos (>=1867 px tall) or place scenes."""
import json
# The beats below are timed on the first assembly (before the owner's flubs and long hesitations were cut).
# retime() maps them onto the final voice track by matching the two transcripts word by word.
import difflib, os
OLD = json.load(open('work/words_old.json')); NEW = json.load(open('work/words_t.json'))
key = lambda w: (w['src'][:2] if w['src'].startswith('p') else w['src'], w['w'])      # p2a/p2b -> p2
sm = difflib.SequenceMatcher(a=[key(w) for w in OLD], b=[key(w) for w in NEW], autojunk=False)
ANCH = [(0.0, 0.0)] + [(OLD[i + k]['s'], NEW[j + k]['s']) for i, j, n in sm.get_matching_blocks() for k in range(n)]
ANCH.sort()
def retime(t):
    for (a0, b0), (a1, b1) in zip(ANCH, ANCH[1:]):
        if a0 <= t <= a1: return round(b0 + (t - a0) * ((b1 - b0) / (a1 - a0) if a1 > a0 else 0), 2)
    return round(ANCH[-1][1] + (t - ANCH[-1][0]), 2)
DUR = round(NEW[-1]['e'] + 0.6, 2)
P = lambda n: f'ph/{n}.jpg'; M = lambda n: f'geo/{n}.jpg'; G = lambda n: f'gph/{n}.jpg'
U = lambda n, ss=0: f'up/{n}.mp4@{ss}'
SMILE, FLAG, ASICS, STAD, FIN, RUN, RUN2, U20, EYES, BLOCKS = (P('usa_smile'), P('cali_flag'), P('asics_run'), P('stadium_2021'),
    P('brooks_finish'), P('brooks_run'), P('brooks_run2'), P('u20_win'), P('eyes'), P('blocks_2x'))
# (t, 'full', src, focus) | (t, 'split', top, top_focus, bottom, bottom_focus) | extra dict optional at the end
B = [
 (0.0,   'full',  M('st_wa'), [0.5, 0.42]),
 (4.6,   'split', U('b_starts'), [0.5, 0.4], BLOCKS, [0.55, 0.5]),
 (6.4,   'full',  'gen/rec_1098.mp4@8.6', [0.5, 0.5]),
 (9.5,   'full',  ASICS, [0.5, 0.4]),
 (18.1,  'split', U('b_run1'), [0.5, 0.4], STAD, [0.55, 0.3]),
 (26.9,  'split', U('b_open'), [0.5, 0.5], FIN, [0.6, 0.5]),
 (33.3,  'full',  STAD, [0.56, 0.3], {'hit': True}),
 (39.9,  'full',  M('st_ga'), [0.5, 0.42]),
 (45.0,  'full',  'gen/rec_1098.mp4@4.6', [0.5, 0.5]),
 (52.0,  'full',  M('ct_co'), [0.5, 0.42]),
 (57.0,  'split', U('c_race'), [0.5, 0.5], U('b_cali'), [0.5, 0.45]),
 (60.4,  'split', U('c_flag'), [0.5, 0.4], FLAG, [0.56, 0.35]),
 (62.6,  'split', U('b_flag'), [0.5, 0.4], RUN2, [0.5, 0.4]),
 (71.3,  'split', U('b_run1', 2), [0.5, 0.4], BLOCKS, [0.5, 0.5]),
 (78.9,  'full',  ASICS, [0.62, 0.35]),
 (85.8,  'split', SMILE, [0.35, 0.3], ASICS, [0.4, 0.4]),
 (90.8,  'split', U('g_talk'), [0.5, 0.35], STAD, [0.5, 0.5]),
 (96.3,  'split', ASICS, [0.5, 0.35], BLOCKS, [0.6, 0.5]),
 (104.3, 'split', U('b_starts', 3), [0.5, 0.4], G('wpgtrack'), [0.5, 0.5]),
 (115.7, 'split', U('b_open', 2), [0.5, 0.5], G('getset'), [0.55, 0.6]),
 (118.5, 'full',  ASICS, [0.38, 0.45]),
 (124.2, 'split', U('b_study'), [0.5, 0.45], BLOCKS, [0.45, 0.5]),
 (134.5, 'full',  SMILE, [0.42, 0.3]),
 (141.0, 'split', U('b_open', 1), [0.5, 0.5], G('wpgtrack'), [0.4, 0.5]),
 (149.1, 'full',  M('ct_pl'), [0.5, 0.42]),
 (152.0, 'full',  'gen/rec_u20.mp4@7.0', [0.5, 0.5]),
 (156.4, 'split', U('u_smile'), [0.5, 0.35], G('getset'), [0.5, 0.6]),
 (165.2, 'split', U('g_talk', 2), [0.5, 0.35], G('wpgtrack'), [0.6, 0.5]),
 (171.7, 'split', SMILE, [0.4, 0.25], BLOCKS, [0.55, 0.5]),
 (178.6, 'full',  STAD, [0.5, 0.3], {'hit': True}),
 (185.1, 'split', EYES, [0.5, 0.5], STAD, [0.62, 0.3]),
 (194.3, 'split', STAD, [0.5, 0.2], G('getset'), [0.45, 0.6]),
 (201.8, 'split', U('b_run2', 1), [0.5, 0.4], EYES, [0.5, 0.5]),
 (208.4, 'full',  M('st_ca'), [0.5, 0.42]),
 (216.2, 'split', STAD, [0.55, 0.35], G('wpgtrack'), [0.5, 0.5]),
 (231.1, 'split', SMILE, [0.4, 0.3], FIN, [0.6, 0.5]),
 (237.4, 'full',  M('st_la'), [0.5, 0.42]),
 (247.3, 'split', U('b_study', 1), [0.5, 0.45], BLOCKS, [0.5, 0.5]),
 (249.3, 'split', SMILE, [0.45, 0.3], 'vid_w/nbc_trials24.mp4@8.5', [0.5, 0.5]),
 (263.4, 'split', U('b_starts', 1), [0.5, 0.4], STAD, [0.5, 0.4]),
 (280.3, 'split', FIN, [0.55, 0.5], FLAG, [0.6, 0.4]),
 (289.8, 'split', ASICS, [0.6, 0.4], G('wpgtrack'), [0.5, 0.5]),
 (296.2, 'split', U('u_smile', 2), [0.5, 0.35], ASICS, [0.5, 0.45]),
 (305.7, 'split', U('b_run2'), [0.5, 0.4], BLOCKS, [0.55, 0.5]),
 (313.2, 'full',  ASICS, [0.5, 0.4], {'hit': True}),
 (316.0, 'split', U('b_run1'), [0.5, 0.4], FIN, [0.55, 0.5]),
 (322.1, 'split', STAD, [0.56, 0.3], 'vid_w/nbc_trials24.mp4@107', [0.5, 0.5]),
 (326.7, 'split', U('b_open', 3), [0.5, 0.5], G('getset'), [0.5, 0.6]),
 (329.7, 'full',  FLAG, [0.56, 0.3]),
]
GFX = [
 {"type": "motion", "kind": "calendar", "t": 0.2, "dur": 2.6, "items": ["MAY", "JUNE", "JULY"], "hi": [1], "label": "JUNE 20, 2015"},
 {"type": "motion", "kind": "pin", "t": 2.9, "dur": 1.7, "text": "SHORELINE, WA", "sub": "BROOKS PR INVITATIONAL"},
 {"type": "motion", "kind": "keyword", "t": 11.1, "dur": 2.8, "text": "10-YEAR PRO DEAL"},
 {"type": "motion", "kind": "stamp", "t": 15.2, "dur": 2.6, "text": "REPORTEDLY 6 FIGURES/YR", "size": 80, "anchor": "lower"},
 {"type": "motion", "kind": "board", "t": 18.4, "dur": 14.6, "title": "SINCE THAT DAY", "rows": [{"event": "LEGAL SUB-11", "value": "0"}, {"event": "USA OLY/WORLD TEAMS", "value": "0"}, {"event": "100/200 PBS", "value": "0"}], "times": [2.6, 5.4, 9.5]},
 {"type": "motion", "kind": "keyword", "t": 34.0, "dur": 4.7, "text": "DID SHE FINESSE ASICS?"},
 {"type": "motion", "kind": "pin", "t": 41.4, "dur": 3.6, "text": "CONYERS, GEORGIA", "sub": "ROCKDALE COUNTY HIGH SCHOOL"},
 {"type": "motion", "kind": "stamp", "t": 47.1, "dur": 1.5, "text": "NO FLUKE", "anchor": "upper"},
 {"type": "motion", "kind": "keyword", "t": 48.7, "dur": 3.2, "text": "1ST HS GIRL UNDER 11"},
 {"type": "motion", "kind": "pin", "t": 54.4, "dur": 2.6, "text": "CALI, COLOMBIA", "sub": "2015 WORLD YOUTH CHAMPIONSHIPS"},
 {"type": "motion", "kind": "board", "t": 57.2, "dur": 5.3, "title": "WORLD YOUTHS 2015", "rows": [{"event": "100M", "value": "11.08", "tag": "GOLD"}, {"event": "200M", "value": "22.43", "tag": "GOLD"}], "times": [0.8, 2.3]},
 {"type": "motion", "kind": "keyword", "t": 63.0, "dur": 3.8, "text": "GATORADE NATIONAL AWARD"},
 {"type": "motion", "kind": "keyword", "t": 67.1, "dur": 3.9, "text": "AS A SOPHOMORE"},
 {"type": "motion", "kind": "keyword", "t": 72.1, "dur": 1.8, "text": "FASTEST GIRL ALIVE"},
 {"type": "motion", "kind": "bubbles", "t": 73.9, "dur": 4.6, "items": ["USC WANTS HER", "FLORIDA WANTS HER", "EVERY BIG PROGRAM"]},
 {"type": "motion", "kind": "calendar", "t": 79.1, "dur": 2.6, "items": ["OCT", "NOV", "DEC", "JAN"], "hi": [2], "label": "DEC 17, 2015"},
 {"type": "motion", "kind": "keyword", "t": 82.2, "dur": 3.4, "text": "SIGNS WITH ASICS"},
 {"type": "motion", "kind": "stamp", "t": 87.7, "dur": 2.8, "text": "YOUNGEST U.S. PRO EVER", "size": 80, "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 91.4, "dur": 4.6, "text": "NUMBER NEVER CONFIRMED"},
 {"type": "motion", "kind": "board", "t": 96.6, "dur": 7.4, "title": "THE DEAL (REPORTED)", "rows": [{"event": "PAY", "value": "6 FIGURES/YR"}, {"event": "LENGTH", "value": "10 YEARS"}, {"event": "REDUCTIONS", "value": "NONE"}], "times": [1.9, 3.2, 4.3]},
 {"type": "motion", "kind": "keyword", "t": 106.8, "dur": 3.1, "text": "REDUCTION CLAUSE"},
 {"type": "motion", "kind": "flow", "t": 110.4, "dur": 5.2, "items": ["DON'T RUN FAST", "MISS THE TEAM", "PAY CUT"], "times": [0.5, 3.0, 4.2]},
 {"type": "motion", "kind": "stamp", "t": 116.8, "dur": 1.6, "text": "NOT HER", "anchor": "lower"},
 {"type": "motion", "kind": "calendar", "t": 119.6, "dur": 4.4, "items": ["2015", "2020", "2025"], "hi": [2], "label": "THROUGH AGE 26"},
 {"type": "motion", "kind": "keyword", "t": 124.8, "dur": 2.6, "text": "COLLEGE PAID TOO"},
 {"type": "motion", "kind": "stamp", "t": 131.3, "dur": 2.4, "text": "SET FOR 10 YEARS", "size": 100},
 {"type": "motion", "kind": "calendar", "t": 135.0, "dur": 4.0, "items": ["2015", "2016", "2017"], "hi": [1], "label": "THE OLYMPIC YEAR"},
 {"type": "motion", "kind": "keyword", "t": 141.2, "dur": 2.4, "text": "MISSED 4 MONTHS"},
 {"type": "motion", "kind": "board", "t": 144.4, "dur": 4.6, "title": "2016 OLYMPIC TRIALS", "rows": [{"event": "100M", "value": "13TH"}, {"event": "200M", "value": "14TH"}], "times": [1.7, 3.4]},
 {"type": "motion", "kind": "pin", "t": 149.3, "dur": 2.7, "text": "BYDGOSZCZ, POLAND", "sub": "2016 WORLD U20 CHAMPIONSHIPS"},
 {"type": "motion", "kind": "keyword", "t": 156.6, "dur": 1.6, "text": "WORLD U20 CHAMPION"},
 {"type": "motion", "kind": "stamp", "t": 158.6, "dur": 1.5, "text": "IT STOPS", "size": 140},
 {"type": "motion", "kind": "calendar", "t": 160.0, "dur": 5.1, "items": ["2017", "2018", "2019"], "hi": [2], "label": "NO PERSONAL BEST"},
 {"type": "motion", "kind": "board", "t": 165.4, "dur": 6.2, "title": "2019 USA CHAMPS", "rows": [{"event": "100M", "value": "14TH"}, {"event": "200M", "value": "14TH"}], "times": [2.7, 4.8]},
 {"type": "motion", "kind": "keyword", "t": 172.6, "dur": 5.6, "text": "COACH AFTER COACH"},
 {"type": "motion", "kind": "keyword", "t": 179.4, "dur": 5.5, "text": "THE PART NOBODY SAW"},
 {"type": "motion", "kind": "keyword", "t": 187.8, "dur": 4.8, "text": "\"YOU MADE THE WRONG DECISION\""},
 {"type": "motion", "kind": "stamp", "t": 192.8, "dur": 1.5, "text": "SECOND-GUESSING", "size": 100, "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 195.1, "dur": 6.5, "text": "EMOTIONAL → PHYSICAL PAIN"},
 {"type": "motion", "kind": "keyword", "t": 203.8, "dur": 4.3, "text": "MIND FIRST, BODY FOLLOWS"},
 {"type": "motion", "kind": "pin", "t": 212.0, "dur": 4.0, "text": "CALIFORNIA", "sub": "JULY 2021"},
 {"type": "motion", "kind": "stopwatch", "t": 216.5, "dur": 5.6, "value": "10.99", "unit": "100M", "label": "FIRST SUB-11 IN 6 YEARS", "anim": 0.8},
 {"type": "motion", "kind": "wind", "t": 222.3, "dur": 4.6, "text": "WIND +2.5 · LIMIT +2.0"},
 {"type": "motion", "kind": "stamp", "t": 227.3, "dur": 3.0, "text": "WIND-AIDED", "anchor": "lower"},
 {"type": "motion", "kind": "board", "t": 231.3, "dur": 5.8, "title": "2021 OLYMPIC TRIALS", "rows": [{"event": "100M FINAL", "value": "11.23"}], "times": [3.2]},
 {"type": "motion", "kind": "pin", "t": 238.6, "dur": 4.2, "text": "BATON ROUGE, LA", "sub": "COACH DENNIS SHAVER"},
 {"type": "motion", "kind": "keyword", "t": 244.6, "dur": 2.7, "text": "TRAINING WITH ALEIA HOBBS"},
 {"type": "motion", "kind": "keyword", "t": 247.5, "dur": 1.8, "text": "BACK IN SCHOOL"},
 {"type": "motion", "kind": "board", "t": 251.4, "dur": 8.6, "title": "2024 OLYMPIC TRIALS", "rows": [{"event": "100M FINAL", "value": "7TH", "tag": "11.00"}], "times": [4.2]},
 {"type": "motion", "kind": "keyword", "t": 260.2, "dur": 3.0, "text": "THAT CLOSE"},
 {"type": "motion", "kind": "board", "t": 265.8, "dur": 14.3, "title": "SINCE SIGNING", "rows": [{"event": "LEGAL SUB-11S", "value": "0"}, {"event": "OLYMPIC TEAMS", "value": "0"}, {"event": "WORLD TEAMS", "value": "0"}, {"event": "100/200 PBS", "value": "0"}], "times": [3.1, 5.3, 8.3, 13.6]},
 {"type": "motion", "kind": "board", "t": 280.6, "dur": 9.0, "title": "STILL HER BESTS", "rows": [{"event": "100M · JUNE 2015", "value": "10.98"}, {"event": "200M · JULY 2015", "value": "22.43"}], "times": [2.5, 6.9]},
 {"type": "motion", "kind": "keyword", "t": 291.0, "dur": 4.4, "text": "3 YEARS LEFT (2023)"},
 {"type": "motion", "kind": "keyword", "t": 301.5, "dur": 3.0, "text": "AS A BUSINESS DEAL"},
 {"type": "motion", "kind": "stamp", "t": 304.6, "dur": 1.6, "text": "GOT THE BAG", "anchor": "lower"},
 {"type": "motion", "kind": "keyword", "t": 306.6, "dur": 5.8, "text": "THE TIME NEVER CAME BACK"},
 {"type": "motion", "kind": "stamp", "t": 314.0, "dur": 1.9, "text": "FINESSE", "size": 170},
 {"type": "motion", "kind": "keyword", "t": 316.4, "dur": 2.6, "text": "NOBODY TRICKED ASICS"},
 {"type": "motion", "kind": "keyword", "t": 319.2, "dur": 2.8, "text": "THEY MADE A BET"},
 {"type": "motion", "kind": "flow", "t": 322.2, "dur": 4.4, "items": ["NEVER QUIT", "2 TRIALS FINALS", "BACK TO SCHOOL"], "times": [0.4, 1.4, 3.1]},
 {"type": "motion", "kind": "bubbles", "t": 327.0, "dur": 2.6, "items": ["YOU MESSED UP", "WRONG DECISION", "SHOULD'VE GONE TO COLLEGE"]},
 {"type": "motion", "kind": "poll", "t": 331.4, "dur": 12.0, "question": "DID SHE FINESSE ASICS?", "options": ["SHE FINESSED", "ASICS LOST A BET"]},
]
for g in GFX:
    t0, t1 = retime(g['t']), retime(g['t'] + g['dur'])
    if 'times' in g: g['times'] = [round(retime(g['t'] + x) - t0, 2) for x in g['times']]
    g['t'], g['dur'] = t0, max(0.8, round(t1 - t0, 2))
GFX[-1]['dur'] = round(DUR - GFX[-1]['t'], 2)
B = [(retime(b[0]),) + tuple(b[1:]) for b in B]
VW = {'x4a2qs8': json.load(open('vid_w/w_x4a2qs8.json')), 'x61wzb1': json.load(open('vid_w/w_x61wzb1.json'))}
BITES = [  # label, source video, source start, top, top focus, bottom, bottom focus, badge text, badge tag
 ('bite_A', 'x4a2qs8', 42.8, U('b_A'), [0.5, 0.35], U('b_open'), [0.5, 0.5], 'CANDACE HILL', 'AGE 16 · beIN SPORTS'),
 ('bite_B', 'x4a2qs8', 297.3, U('b_B'), [0.5, 0.35], U('c_flag'), [0.5, 0.4], 'CANDACE HILL', 'AFTER CALI 2015'),
 ('bite_G', 'x4a2qs8', 359.9, U('b_G'), [0.5, 0.4], FLAG, [0.56, 0.35], 'TONY CARPENTER', 'HER COACH · 2016'),
 ('bite_C', 'x61wzb1', 173.5, U('b_run2'), [0.5, 0.4], U('u_smile'), [0.5, 0.35], 'CANDACE HILL', 'ON HER 2016 SURGERY'),
 ('bite_F', 'x4a2qs8', 157.8, U('b_F'), [0.5, 0.4], STAD, [0.55, 0.3], 'TONY CARPENTER', 'HER COACH · 2016'),
]
for lab, vid, src0, top, tf, bot, bf, who, tag in BITES:
    ws = [w for w in NEW if w['src'] == lab]
    w0 = next(x for x in VW[vid] if x['w'] == ws[0]['w'] and x['s'] >= src0 - 0.6)
    t0 = round(ws[0]['s'] - (w0['s'] - src0) - 0.05, 2); t1 = round(ws[-1]['e'] + 0.15, 2)
    B = [b for b in B if not (t0 - 0.3 < b[0] < t1)]
    B.sort(key=lambda b: b[0])
    nxt = [b for b in B if b[0] >= t1]
    if nxt and nxt[0][0] - t1 > 0.4:                # the next beat starts as soon as the bite ends
        i = B.index(nxt[0]); B[i] = (t1,) + tuple(nxt[0][1:])
    B.append((t0, 'split', top, tf, bot, bf)); B.sort(key=lambda b: b[0])
    GFX = [g for g in GFX if not (t0 - 0.2 < g['t'] < t1 - 0.3)]
    GFX.append({"type": "motion", "kind": "podcast", "t": round(t0 + 0.2, 2), "dur": round(t1 - t0 - 0.4, 2), "text": who, "tag": tag, "anchor": "lower"})
B.sort(key=lambda b: b[0]); GFX.sort(key=lambda g: g['t'])
segs, TOP = [], []
for b in B:
    ex = b[-1] if isinstance(b[-1], dict) else {}
    if b[1] == 'full':
        fs, _, fss = b[2].partition('@'); d = {"type": "full", "start": b[0], "broll": {"src": fs, "ss": float(fss or 0), "focus": b[3]}}
    elif '@' in b[4]:
        bs, _, bss = b[4].partition('@'); d = {"type": "split", "start": b[0], "broll": {"src": bs, "ss": float(bss), "focus": b[5]}}
    else:
        d = {"type": "split", "start": b[0], "broll": {"src": b[4], "ss": 0, "focus": b[5]}}
    if b[1] == 'split':
        src, _, ss = b[2].partition('@')
        TOP.append({"t": b[0], "src": src, "ss": float(ss or 0), "focus": b[3]})
    d.update(ex); segs.append(d)
TOP[0]['t'] = 0.0
plan = {"workdir": "build", "output": "out/candace_hill.mp4", "words": "work/words_final.json", "voice_ss": 0.0, "duration": DUR,
        "face": {"src": "top.mov", "focus": [0.5, 0.5]}, "face_grade": "null", "zooms": [], "skip_res_check": False,
        "segments": segs, "graphics": GFX}
json.dump(plan, open('plan.json', 'w'), indent=1)
json.dump({"duration": DUR, "voice": "work/voice_t.wav", "shots": TOP}, open('top.json', 'w'), indent=1)
full = sum((segs[i + 1]['start'] if i + 1 < len(segs) else DUR) - s['start'] for i, s in enumerate(segs) if s['type'] == 'full')
print(len(segs), 'segments,', len(GFX), 'graphics; full-screen', round(100 * full / DUR), '%')
