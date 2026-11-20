"""Issam Asinga comeback take (~1:28): 'cut every event where fewer than 16-20 people hit the standard'. Jane Hedengren format.
Facts (NOTES.md): LA28 standards (WA, 10 Nov 2026): 100m 9.93, men TJ 17.35, women TJ 14.50, men LJ 8.30. 2026 outdoor world lists
(worldathletics.org toplists): 100m 26 men <=9.93; men TJ 7 >=17.35; women TJ 12 >=14.50; men LJ 12 >=8.30, best USA 8.29.
Ultimate Championship (Budapest, 11-13 Sep 2026) left out shot put, discus, 10,000m, steeplechase, men's triple jump."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/44aa0cd6-8023-5301-82fa-277e8bea228e/scratchpad/asinga12'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,').strip("'") for x in W]
B = lambda n: f'{H}/broll/{n}'

def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')

def FRZ(name, src, dur, pick, focus=(0.5, 0.5), push=1.08, glow=None, model=None):
    out = f'{SP}/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
    spec = {'src': src, 'ss': 0, 'out': out, 'dur': round(dur + 0.6, 2), 'pick': pick, 'focus': list(focus), 'push': push, **({'glow': glow} if glow else {}), **({'model': model} if model else {})}
    js = out[:-4] + '.json'
    if not (os.path.exists(out) and os.path.exists(js) and json.load(open(js)) == spec):
        json.dump(spec, open(js, 'w')); subprocess.run(['python3', f'{H}/../../editor/freeze.py', js], check=True)
    return out

END = round(W[-1]['e'] + 1.8, 2)
full = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': k.pop('ss', 0), 'focus': [fx, fy]}, **k}
split = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': k.pop('ss', 0), 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}



t_issam, t_skip1, t_see, t_but, t_disap, t_how, t_2023, t_bro, t_seen, t_so, t_flower, t_only, t_hey = at('issam asinga'), at("he ain't skipped", 1), at('i see a lot'), at('but all i'), at('disappointed faces'), at('how noah'), at('2023'), at('cuz bro'), at('and i seen'), at('so if this'), at("it's finna be"), at('only 21'), at('hey, man,')
RACE, RHD = B('race.mp4'), B('race_hd.mp4')
segs = [
    full(0.0, RHD, 0.5, 0.5, ss=0.0),
    full(t_issam - 0.05, FRZ('asinga_intro', B('p1_hd.jpg'), t_skip1 - t_issam, [0.62, 0.55], focus=(0.62, 0.45), model='u2net_human_seg'), 0.5, 0.45, hit=True),
    split(t_skip1 - 0.05, B('p2_hd.jpg'), 0.76, 0.4),
    split(t_see - 0.05, RACE, 0.5, 0.45, ss=10.0),
    split(at('and even later') - 0.05, B('p1_hd.jpg'), 0.6, 0.4),
    split(t_but - 0.05, B('lyles_thumb_hd.jpg'), 0.5, 0.3),
    split(at('when a lot') - 0.05, B('lyles_paris.jpg'), 0.5, 0.3),
    full(t_how - 0.05, RHD, 0.5, 0.5, ss=1.5, hit=True),
    split(t_2023 - 0.05, B('lyles_usatf2_v.jpg'), 0.5, 0.3),
    split(t_bro - 0.05, RACE, 0.45, 0.5, ss=5.5),
    split(t_seen - 0.05, B('p2_hd.jpg'), 0.6, 0.35),
    split(at('she came back') - 0.05, RACE, 0.5, 0.45, ss=11.5),
    full(t_so - 0.05, B('p1_hd.jpg'), 0.62, 0.4),
    split(t_flower - 0.05, B('lyles_paris.jpg'), 0.35, 0.35),
    split(t_only - 0.4, B('p1_hd.jpg'), 0.62, 0.35),
    split(t_hey - 0.6, RACE, 0.5, 0.45, ss=12.5),
]
gfx = [
    M('keyword', 0.3, 3.0, text="HE'S COMING BACK"),
    M('slam', t_skip1 + 0.1, 1.6, text="AIN'T SKIPPED A BEAT", hi=1, anchor='upper'),
    M('board', t_see + 0.2, t_but - t_see - 0.3, title='THE BAN',
      rows=[{'event': 'JUL 2023', 'value': 'GW1516'}, {'event': '4-YEAR BAN', 'value': 'AIU'}, {'event': '9.89 U20 RECORD', 'value': 'WIPED'}, {'event': 'ELIGIBLE', 'value': 'AUG 2027'}],
      times=[0.2, 1.4, 2.6, at('2027') - t_see - 0.2]),
    M('keyword', t_disap - 0.4, 2.4, text='DISAPPOINTED FACES'),
    M('pin', t_how + 1.2, 2.6, text='CLERMONT, FL', sub='APR 23, 2023'),
    M('board', t_2023 - 0.1, t_bro - t_2023 + 0.3, title='CLERMONT 2023 · 100M',
      rows=[{'event': '1 · ASINGA (18)', 'value': '9.83w'}, {'event': '2 · NOAH LYLES', 'value': '9.92'}], times=[0.2, 0.9]),
    M('slam', t_bro + 1.3, 1.6, text='NO RUST', hi=1, anchor='upper'),
    M('keyword', at('she had to') - 0.1, 2.6, text='SAT OUT. CAME BACK.'),
    M('slam', t_flower + 0.5, 1.6, text='FLOWER BRINGING', hi=0, anchor='upper'),
    D('counter', t_only - 0.1, 2.4, value='21', unit='YEARS OLD', label='Issam Asinga', sub='22 when his ban ends'),
    M('poll', t_hey, END - t_hey, question='WILL ASINGA BE ELITE WHEN HE RETURNS?', options=['YES', 'NO']),
]
zooms = [[at('that\'s all') - 0.1, at('that\'s all') + 1.2, 1.1], [t_only - 0.1, t_only + 1.6, 1.08]]
segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
os.makedirs(f'{SP}/out', exist_ok=True)
plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/asinga_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
