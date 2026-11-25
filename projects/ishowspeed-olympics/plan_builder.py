"""IShowSpeed at LA 2028 via citizenship by investment (~2:05): owner's talking head (4K, tightened).
B-roll: Olympic-stadium / stadium / passport / cash / island stock video (Pexels, free licence; no Olympic race footage, per owner),
owner's 3 photos (1206 px, split) and Speed Goes Pro clip (720p -> FSRCNN 2x blend -> 1080x1920, split only),
Commons: IShowSpeed portrait (hook freeze), LA Memorial Coliseum aerial. Facts in NOTES.md."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/work/words_tight.json'))
TOK = [re.sub(r"[^a-z0-9.:'\-*$,]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]
P = lambda n: f'{H}/photos/{n}.jpg'
R = lambda n: f'{H}/raw/{n}.jpg'
B = lambda n: f'{H}/broll/{n}.mp4'
CLIP = f'{H}/work/clip1_up.mp4'


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.:'\-*$,]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def FRZ(name, src, ss, dur, pick, focus=(0.5, 0.5), push=1.08):
    out = f'{SP}/spd/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
    spec = {'src': src, 'ss': ss, 'out': out, 'dur': round(dur + 0.6, 2), 'pick': pick, 'focus': list(focus), 'push': push}
    js = out[:-4] + '.json'
    if not (os.path.exists(out) and os.path.exists(js) and json.load(open(js)) == spec):
        json.dump(spec, open(js, 'w')); subprocess.run(['python3', f'{H}/../../editor/freeze.py', js], check=True)
    return out


END = round(W[-1]['e'] + 2.8, 2)
full = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
split = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_ichanged, t_finally, t_every, t_but, t_went, t_ato, t_watched, t_couldnt, t_she, t_point = (
    at('and i just changed'), at('will be finally'), at('and everybody in'), at("but they don't"), at('he just went'), at('with ato'),
    at('i watched his'), at("he couldn't even"), at('and she runs'), at('to the point'))
t_all, t_optics, t_wait1, t_wait2, t_rich, t_chance, t_become, t_there, t_so, t_doesnt = (
    at('all he has to'), at('optics is everything'), at("wait till y'all"), at("wait till y'all", 2), at('being rich'), at('he has the chance'),
    at('he can become'), at('there is countries'), at('so all he'), at("he doesn't have"))
t_company, t_dicks, t_have2, t_go, t_sent, t_when, t_these, t_blow, t_play, t_doyou, t_gout, t_speed, t_take, t_theywont, t_how = (
    at('he can have a company'), at("dick's"), at('have a company sponsor', 2), at('and go invest'), at('and be sent'), at('and when he goes'),
    at('where these guys'), at('go out there and blow'), at('and just play'), at('do you know'), at('gout gout'), at('but speed showed'),
    at("it's gonna completely"), at("they won't even"), at('how he showed'))

segs = [
    full(0.0, FRZ('speed_hook', P('speed_portrait'), 0, t_ichanged, [0.52, 0.35], (0.5, 0.35)), 0, 0.5, 0.5, hit=True),
    split(t_ichanged - 0.05, P('coliseum'), 0, 0.5, 0.5),                 # LA28 athletics venue
    full(t_finally - 0.05, B('ist1'), 1.0, 0.5, 0.5),                     # Olympic stadium aerial
    split(t_every - 0.05, B('crowd'), 1.0, 0.5, 0.5),
    split(t_but - 0.05, R('photo3'), 0, 0.5, 0.3),
    split(t_went - 0.05, CLIP, 3.0, 0.5, 0.5),                            # his run
    split(t_ato - 0.05, R('photo2'), 0, 0.5, 0.3),                        # with his coach
    split(t_couldnt - 0.05, B('blocks'), 20.0, 0.5, 0.55),
    split(t_point - 0.05, CLIP, 10.0, 0.5, 0.5),
    full(t_all - 0.05, B('berlin'), 1.0, 0.5, 0.5, hit=True),             # Olympic stadium
    split(t_wait1 - 0.05, B('ist3'), 0.5, 0.5, 0.5),
    split(t_rich - 0.05, B('cash1'), 1.0, 0.5, 0.5),
    split(t_chance - 0.05, R('photo1'), 0, 0.5, 0.3),
    full(t_become - 0.05, B('pass1'), 1.0, 0.5, 0.45, hit=True),          # passports
    split(t_there - 0.05, B('island1'), 0.5, 0.5, 0.5),
    split(t_so - 0.05, B('cash2'), 3.0, 0.5, 0.5),
    split(t_doesnt - 0.05, CLIP, 20.0, 0.5, 0.5),                         # Speed Goes Pro set (Dick's)
    split(t_have2 - 0.05, B('pass2'), 1.0, 0.5, 0.5),
    full(t_sent - 0.05, B('stad_night'), 2.0, 0.5, 0.5),                  # Olympic round 1
    split(t_these - 0.05, B('stad_color'), 4.0, 0.5, 0.5),
    split(t_blow - 0.05, CLIP, 7.0, 0.5, 0.5),
    split(t_play - 0.05, R('photo2'), 0, 0.5, 0.55),
    full(t_doyou - 0.05, B('ist2'), 0.5, 0.5, 0.5),
    split(t_speed - 0.05, CLIP, 30.0, 0.5, 0.5),
    full(t_take - 0.05, B('crowd'), 6.0, 0.5, 0.5),
    split(t_theywont - 0.05, P('coliseum'), 0, 0.45, 0.45),
    split(t_how - 0.05, R('photo1'), 0, 0.5, 0.45),
]

gfx = [
    M('keyword', 0.7, 2.6, text='SPEED AT LA 2028?'),
    M('pin', t_ichanged + 0.3, 2.6, text='LA COLISEUM', sub='LA 2028 TRACK & FIELD · JULY 15-24'),
    M('slam', t_finally + 0.6, 1.9, text='THE JOKE', hi=1, anchor='upper'),
    M('keyword', t_every + 0.3, 2.4, text='TRACK WILL BE MAD'),
    D('counter', t_went + 0.4, 3.4, value='10.35', unit='S', label='Speed · 100m', sub='unofficial · gate-timed · Nov 2026'),
    M('keyword', t_ato + 0.2, 2.6, text='COACH: ATO BOLDON'),
    D('bars', t_she - 0.2, 3.8, label='100m', unit='S', lower_is_better=True, spread=0.7,
      items=[{'name': 'Speed · day 1', 'value': '10.72'}, {'name': 'Briana Williams PB', 'value': '10.94'}, {'name': 'Speed · w/ Bolt', 'value': '10.35'}]),
    M('slam', t_all + 0.4, 2.0, text='JUST SHOW UP', hi=2, anchor='upper'),
    M('slam', t_optics, 1.8, text='OPTICS IS EVERYTHING', hi=0, anchor='upper'),
    M('keyword', t_wait1 + 0.4, 2.6, text='BIGGER THAN THE USA'),
    M('keyword', t_rich + 0.6, 2.6, text='RICH = NEW PATH'),
    M('keyword', t_chance + 0.3, 2.6, text="AVERAGE RUNNERS CAN'T"),
    M('slam', t_become + 0.5, 2.2, text='CITIZENSHIP BY INVESTMENT', hi=0, anchor='upper'),
    M('board', t_there, t_so - t_there + 0.1, title='CITIZENSHIP BY INVESTMENT · FROM', rows=[
        {'event': 'SÃO TOMÉ & PRÍNCIPE', 'value': '$90K'}, {'event': 'NAURU', 'value': '$90K', 'tag': 'TO DEC 31'},
        {'event': 'VANUATU', 'value': '$130K'}, {'event': 'DOMINICA', 'value': '$200K'}, {'event': 'ST KITTS & NEVIS', 'value': '$250K'}],
      times=[1.4, 2.0, 2.6, 3.1, 3.6]),
    M('pin', t_so + 0.3, 2.8, text='SÃO TOMÉ & PRÍNCIPE', sub='$90,000 · NATIONAL TRANSFORMATION FUND'),
    M('keyword', t_doesnt + 0.2, 2.2, text="NOT HIS OWN MONEY"),
    M('keyword', t_dicks - 0.2, 2.4, text="PRESENTED BY DICK'S"),
    M('flow', t_have2, 4.6, items=['SPONSOR PAYS', "$90K TO A GOV'T", 'NEW PASSPORT'],
      times=[0.2, round(t_go - t_have2 + 0.3, 2), round(at('and be a citizen') - t_have2, 2)]),
    M('board', t_sent + 0.2, t_these - t_sent - 0.2, title='HOW LONG IT ACTUALLY TAKES', rows=[
        {'event': 'SÃO TOMÉ', 'value': '1-4 MO'}, {'event': 'VANUATU', 'value': '2-3 MO'}, {'event': 'CARIBBEAN', 'value': '4-12 MO'}],
      times=[0.3, 0.9, 1.5]),
    M('board', t_these, t_blow - t_these + 0.6, title='PARIS 2024 · 100M PRELIM ROUND', rows=[
        {'event': 'TONGA', 'value': '12.11'}, {'event': 'LIBYA', 'value': '11.89'}, {'event': 'MONTENEGRO', 'value': '11.85'},
        {'event': 'MICRONESIA', 'value': '11.61'}, {'event': 'SLOWEST QUALIFIER', 'value': '10.54'}],
      times=[0.4, 0.9, 1.4, 1.9, 2.6]),
    M('slam', t_blow + 0.4, 1.9, text='OUT THE WATER', hi=2, anchor='upper'),
    M('keyword', t_play + 0.3, 2.6, text="\"I FELT SOMETHING\""),
    M('keyword', t_gout - 0.3, 2.6, text='THE GOUT GOUT EFFECT'),
    M('slam', t_take + 0.3, 2.0, text='TAKE OVER THE SPORT', hi=2, anchor='upper'),
    M('keyword', t_theywont + 0.2, 2.4, text='WINNER? FORGOTTEN'),
    M('poll', t_how - 0.2, END - t_how + 0.2, question='SHOULD SPEED BUY A PASSPORT FOR LA 2028?', options=['YES', 'NO']),
]
zooms = [[t_wait1 - 0.1, t_wait1 + 1.3, 1.08], [t_doyou - 0.1, t_doyou + 1.3, 1.1]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/spd/build', 'output': f'{SP}/spd/out/speed_v1.mp4', 'words': f'{H}/work/words_tight.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
