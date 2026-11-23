"""Abdi (Abdinasir) Hassan 13:56.1 at NXR Southwest (~1:39): owner's talking head (4K, frame-accurate tighten) + the race
announcer's call (owner's vertical clip, 15.7 s, full-screen) spliced in after "ran 13:56 or something like that".
B-roll: owner's vertical race clip (full-screen), 720p race/finish clips (FSRCNN 2x, split), his 4 photos (1206 px, split),
Commons: Dathan Ritzenhein (previous record holder). Facts in NOTES.md."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/words_aroll.json'))
TOK = [re.sub(r"[^a-z0-9.:'\-*]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'
VERT, RACE, WALK = f'{H}/raw/clipV.mov', f'{H}/work/clipL_up.mp4', f'{H}/work/clipS_up.mp4'
T1, L = 27.72, 15.7


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.:'\-*]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


END = round(W[-1]['e'] + 2.6, 2)
full = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
split = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_trav, t_az, t_elev, t_broke, t_now, t_was, t_ran, t_college, t_grass, t_so, t_mesa, t_nike, t_might, t_mind, t_hey, t_but, t_real2 = (
    at('he just traveled'), at('arizona'), at('came down from elevation'), at('just broke'), at('now this record'), at('it was 14:10'), at('and he just went'),
    at('guys in college'), at('grass course'), at('so for him'), at('mesa'), at('nike nationals'), at('he might go'), at('mind you the high'),
    at('hey, man'), at('but he bout'), at('he is the real deal'))

segs = [
    full(0.0, VERT, 2.0, 0.5, 0.45, hit=True),                       # Hassan in the race (his clip)
    split(t_trav - 0.05, R('photo4'), 0, 0.5, 0.35),
    split(t_elev - 0.05, VERT, 26.0, 0.5, 0.5),
    split(t_broke - 0.05, R('photo1'), 0, 0.5, 0.25),                # the 13:55.8 finish clock
    split(t_now - 0.05, R('ritz'), 0, 0.5, 0.3),                     # Ritzenhein, 14:10.4 (2000)
    split(t_ran - 0.05, RACE, 60.0, 0.5, 0.4),
    full(T1, VERT, 9.0, 0.5, 0.45, transition='cut'),                # announcer's call (spliced audio)
    split(T1 + L, R('photo3'), 0, 0.5, 0.3),
    split(t_college - 0.05, RACE, 30.0, 0.5, 0.45),
    split(t_grass - 0.05, VERT, 4.0, 0.5, 0.55),
    full(t_so - 0.05, VERT, 22.0, 0.5, 0.45, hit=True),
    split(t_nike - 0.4, R('photo2'), 0, 0.5, 0.3),
    split(t_might - 0.05, RACE, 75.0, 0.5, 0.4),
    split(t_mind - 0.05, R('photo4'), 0, 0.5, 0.6),
    split(t_hey - 0.05, WALK, 0.0, 0.5, 0.4),
    split(t_hey + 5.5, R('photo3'), 0, 0.5, 0.55),
    full(t_but - 0.05, R('photo1'), 0, 0.5, 0.5),
    split(t_real2 + 0.6, R('photo2'), 0, 0.5, 0.6),
]

gfx = [
    M('slam', 0.6, 1.8, text='THE REAL DEAL', hi=2, anchor='upper'),
    M('usmap', t_trav + 0.2, 4.2, title='COLORADO → ARIZONA', groups=[{'names': ['Colorado'], 'label': 'CO', 'at': round(at('colorado') - t_trav - 0.2, 2)}, {'names': ['Arizona'], 'label': 'AZ', 'at': round(t_az - t_trav - 0.2, 2)}]),
    M('keyword', t_elev + 0.4, 2.6, text='DOWN FROM ALTITUDE'),
    M('slam', t_broke + 0.3, 2.0, text='HS NATIONAL RECORD', hi=0, anchor='upper'),
    M('board', t_now, t_ran - t_now + 0.2, title='HS XC 5K · FASTEST EVER', rows=[{'event': 'RITZENHEIN · 2000', 'value': '14:10.4'}, {'event': 'HASSAN · 2026', 'value': '13:56.1'}],
      times=[t_was - t_now, t_ran - t_now + 0.2]),
    M('keyword', T1 + 0.4, 3.2, text='NXR SOUTHWEST · MESA, AZ'),
    M('slam', T1 + 6.6, 1.8, text='SUB-14', hi=0, anchor='upper'),
    M('keyword', t_college + 0.4, 2.4, text='COLLEGE GUYS CAN\'T DO THIS'),
    M('keyword', t_grass, 2.6, text='GRASS · HILLS · ROUGH TERRAIN'),
    M('pin', t_mesa - 0.4, 2.4, text='MESA, ARIZONA', sub='NIKE CROSS REGIONALS SOUTHWEST'),
    M('keyword', t_nike, 2.4, text='NEXT: NIKE CROSS NATIONALS'),
    M('board', t_mind, 4.4, title='HS 5000M TRACK RECORD', rows=[{'event': 'DANIEL SIMMONS', 'value': '13:25.86'}], times=[0.4]),
    M('slam', t_but + 0.6, 1.8, text='SOMETHING BIG', hi=1, anchor='upper'),
    M('poll', t_real2 - 0.2, END - t_real2 + 0.2, question='WILL HE BREAK 14 AGAIN AT NXN?', options=['YES', 'NO']),
]
zooms = [[t_hey - 0.1, t_hey + 1.2, 1.08], [t_real2 - 0.1, t_real2 + 1.2, 1.1]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/new5/build', 'output': f'{SP}/new5/out/hassan_v1.mp4', 'words': f'{H}/words_aroll.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_aroll.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
