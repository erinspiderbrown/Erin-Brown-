"""IShowSpeed 10.35 hot take (~1:56): "track people are crabs in a bucket". Jane Hedengren format.
Facts (NOTES.md): Speed 10.50 then 10.35 (Speed Goes Pro S2 "I RACED USAIN BOLT!", 22 Nov 2026, unofficial, coach Ato Boldon since ~Sep 2025);
DK Metcalf 10.37 (USATF 10.36), Golden Games, Mt. SAC, 9 May 2021; Tyreek Hill 10.15 (+1.2) LA 13 Jun 2025, 10.10w (+2.7) Texas 28 Jun 2025;
Gout Gout 19.67 (+1.7) 200m Aus Champs 12 Apr 2026; Commonwealth Games 100m 28 Jul 2026: Eseme 9.83, Kennedy 9.85, Ajayi 9.90 (+1.3);
Sam Blaskowski 9.89 (+1.5) Music City, Tennessee, 30 May 2026."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/44aa0cd6-8023-5301-82fa-277e8bea228e/scratchpad/speed14'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]

def B(n, alt=None):
    p = f'{H}/broll/{n}'
    if os.path.exists(p) or alt is None: return p
    print('MISSING', n, '-> using', alt); return B(alt)

def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
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

SPRINT, BLOCKS, THUMBS, SHIRTLESS, CROSSED = (B(f'p{i}_hd.jpg') for i in range(1, 6))
TYREEK = B('tyreek.jpg')
DK, DK2 = B('dk.jpg', 'p1_hd.jpg'), B('dk2.jpg', 'p4_hd.jpg')
ATO = B('ato.jpg', 'p3_hd.jpg')
GOUT = B('gout.jpg', 'p2_hd.jpg')
ESEME = B('eseme.jpg', 'p5_hd.jpg')
KENNEDY = B('kennedy.jpg', 'p3_hd.jpg')

t_crabs, t_this, t_try, t_dk, t_ran, t_predict, t_mt, t_saying, t_speaking, t_nfl, t_big, t_trashed = (
    at('people are crabs'), at('this is how'), at('they try to downplay'), at('i remember dk'), at('ran track and he'), at('people predicting'),
    at('he went to a real'), at('they were saying'), at('speaking about'), at('an nfl receiver'), at('230'), at('and they made it seem'))
t_tyreek, t_goes, t_havent, t_since, t_these, t_crabs2, t_speed, t_trained, t_runs, t_trust, t_asif = (
    at('tyreek hill'), at('he goes out there'), at("haven't ran"), at('since he was in college'), at('these guys running'), at('crabs in a bucket', 2),
    at('ishowspeed jump'), at('he trained with'), at('goes out and he runs'), at("oh i'm not gonna"), at('as if a real'))
t_gout, t_aus, t_official, t_sowhen, t_kennedy, t_cwg, t_earth, t_sam, t_tenn, t_when, t_what = (
    at('gout gout'), at('the australian national'), at('an official track meet'), at('so when has a'), at('lachlan kennedy'), at('show up to the commonwealth'),
    at('so when on earth'), at('sam blaskowski'), at('random meet in tennessee'), at('when has a track meet or'), at('what are we talking'))

segs = [
    full(0.0, SPRINT, 0.4, 0.35, hit=True),
    split(t_crabs - 0.05, BLOCKS, 0.5, 0.45),
    split(t_this - 0.05, CROSSED, 0.5, 0.3),
    split(t_try - 0.05, SHIRTLESS, 0.5, 0.3),
    full(t_dk - 0.05, DK, 0.5, 0.3, hit=True),
    split(t_predict - 0.05, DK2, 0.5, 0.3),
    split(t_mt - 0.05, DK, 0.5, 0.35),
    split(t_speaking - 0.05, DK2, 0.5, 0.4),
    split(t_big - 0.05, DK, 0.5, 0.5),
    full(t_tyreek - 0.05, TYREEK, 0.45, 0.35, hit=True),
    split(t_havent - 0.05, TYREEK, 0.5, 0.25),
    split(t_these - 0.05, BLOCKS, 0.5, 0.45),
    full(t_speed - 0.05, THUMBS, 0.45, 0.35),
    split(t_trained - 0.05, ATO, 0.5, 0.3),
    split(t_runs - 0.05, SPRINT, 0.4, 0.35),
    split(t_trust - 0.05, SHIRTLESS, 0.5, 0.3),
    full(t_gout - 0.05, GOUT, 0.5, 0.35, hit=True),
    split(t_official - 0.05, GOUT, 0.5, 0.4),
    split(t_sowhen - 0.05, BLOCKS, 0.5, 0.45),
    full(t_kennedy - 0.05, ESEME, 0.5, 0.3),
    split(t_earth - 0.05, KENNEDY, 0.5, 0.35),
    split(t_sam - 0.05, SPRINT, 0.4, 0.4),
    split(t_when - 0.05, THUMBS, 0.5, 0.3),
]
gfx = [
    D('counter', 0.4, 3.6, value='10.35', unit='SEC', label='IShowSpeed · 100m', sub='2nd run · 1st was 10.50'),
    M('slam', t_crabs + 0.1, 1.9, text='CRABS IN A BUCKET', hi=3, anchor='upper'),
    M('bubbles', t_try + 0.1, 3.6, items=['NOT A REAL MEET', 'THAT AIN\'T A PRO TIME', 'WAIT TIL IT\'S OFFICIAL']),
    M('pin', t_mt - 0.1, 2.0, text='MT. SAC · WALNUT, CA', sub='USATF GOLDEN GAMES · MAY 2021'),
    D('counter', t_mt + 2.0, 2.6, value='10.37', unit='SEC', label='DK Metcalf · 100m', sub='Golden Games · 9 May 2021'),
    M('keyword', t_nfl - 0.1, 2.4, text='NFL WIDE RECEIVER'),
    M('slam', t_trashed + 0.6, 1.6, text='TRASH?', hi=0, anchor='upper'),
    M('board', t_goes - 0.2, t_havent - t_goes + 0.1, title='TYREEK HILL · 2025',
      rows=[{'event': 'JUNE 13 · LA', 'value': '10.15'}, {'event': 'JUNE 28 · TEXAS', 'value': '10.10w'}], times=[0.3, 1.0]),
    M('keyword', t_havent + 0.1, 2.6, text='FIRST RACE SINCE 2014'),
    M('slam', t_crabs2 - 0.3, 1.9, text='CRABS IN A BUCKET', hi=3, anchor='upper'),
    M('keyword', t_trained + 0.2, 2.6, text='COACH: ATO BOLDON'),
    M('stopwatch', t_runs + 0.2, 2.4, value='10.35', unit='SECONDS', label='WITH USAIN BOLT WATCHING', anim=1.0),
    M('bubbles', t_trust, 3.4, items=['NOT TILL A REAL MEET', 'HAND TIMED?', 'MAKE IT OFFICIAL']),
    D('counter', t_aus + 1.2, 2.8, value='19.67', unit='SEC', label='Gout Gout · 200m', sub='Australian Champs · Apr 2026'),
    M('slam', t_official, 1.8, text='OFFICIAL MEET', hi=0, anchor='upper'),
    M('board', t_cwg - 0.2, t_earth - t_cwg + 0.2, title='COMMONWEALTH GAMES 100M',
      rows=[{'event': '1 · E. ESEME', 'value': '9.83'}, {'event': '2 · L. KENNEDY', 'value': '9.85'}, {'event': '3 · K. AJAYI', 'value': '9.90'}],
      times=[0.3, 0.8, 1.3]),
    D('counter', t_tenn - 0.2, 3.0, value='9.89', unit='SEC', label='Sam Blaskowski · 100m', sub='Music City meet, TN · May 2026'),
    M('poll', t_when + 0.3, END - t_when - 0.3, question="IS SPEED'S 10.35 LEGIT?", options=['YES', 'NO']),
]
zooms = [[t_earth - 0.1, t_earth + 1.4, 1.1], [t_what - 0.1, t_what + 1.4, 1.12], [t_asif - 0.1, t_asif + 1.4, 1.08]]
segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
os.makedirs(f'{SP}/out', exist_ok=True)
plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/speed_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
for a, b in zip(gfx, gfx[1:]):
    if b['t'] < a['t'] + a['dur'] - 0.1: print('OVERLAP', a.get('text', a.get('title', a.get('label'))), b.get('text', b.get('title', b.get('label'))))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
