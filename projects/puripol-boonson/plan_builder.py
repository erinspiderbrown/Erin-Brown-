"""Puripol Boonson / Nike / Dennis Mitchell take (~1:30): owner's talking head (4K, tightened) with Boonson's Asian Games interview
spliced in as a guest soundbite (720p -> FSRCNN 2x, top slot, 13.9 s after "Asian record in the 200").
B-roll:
- the owner's stadium phone clip of the 200 final in the rain (1080x1920 vertical: full-screen)
- owner photos: 9.90 GR board 2048x1365 (split), Mitchell 2048x2048 (split), 19.88 AR board 900x577 (under 1080p: 2x upscale, split only)
- Commons: Boonson 2025 SEA Games, 4216x5655 (full-screen + freeze)
Facts (NOTES.md):
- 2026 Asian Games (Nagoya) 100: heat 9.95, semi 9.91 GR, final 9.90 GR/NR, all sub-10. 200: 19.88 = Asian record (Xie Zhenye 2019).
- 2nd-fastest Asian ever at 100 (Su Bingtian 9.83).
- Coach Gentry Bradley: 1998 USA 200 champ, ex-USC volunteer assistant.
- Nike long-term deal announced 16 Nov 2026; invited to Star Athletics (Dennis Mitchell, Florida) 17-24 Nov to assess joining."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/words_aroll.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'
VERT = f'{H}/raw/clip_vert.mov'
PB = R('pb_crop') if os.path.exists(R('pb_crop')) else None
T1, SB = 24.6, 13.9                      # soundbite window in the A-roll


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def FRZ(name, src, dur, pick, focus=(0.5, 0.5), push=1.08, glow=None, model=None):
    out = f'{SP}/new2/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
    spec = {'src': src, 'ss': 0, 'out': out, 'dur': round(dur + 0.6, 2), 'pick': pick, 'focus': list(focus), 'push': push, **({'glow': glow} if glow else {}), **({'model': model} if model else {})}
    js = out[:-4] + '.json'
    if not (os.path.exists(out) and os.path.exists(js) and json.load(open(js)) == spec):
        json.dump(spec, open(js, 'w')); subprocess.run(['python3', f'{H}/../../editor/freeze.py', js], check=True)
    return out


END = round(W[-1]['e'] + 1.8, 2)
full = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
split = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_ruined, t_now, t_sub, t_19, t_broke, t_least = at('ruined'), at('now he put'), at('he ran sub'), at('he ran 19'), at('broke the'), at('or at least')
t_but, t_coach, t_setup, t_assume, t_nike, t_want, t_dennis = at('but it seemed'), at('he got the'), at('so his whole'), at("so i'm assuming"), at('nike', 1), at('we want you'), at('dennis')
t_move, t_know, t_protect, t_horrible, t_best, t_disregard, t_olymp, t_silly = at('so he has'), at("he don't know"), at("he ain't going"), at('this could be'), at('do the best'), at('and you disregard'), at('olympics'), at('sounds silly')

hook_end = t_now - 0.05
segs = [
    (full(0.0, PB, 0, 0.5, 0.4, hit=True) if PB else full(0.0, VERT, 8.0, 0.5, 0.5, hit=True)),   # flag photo (freeze cut-out lost his arms on the flag)
    *([full(2.6, VERT, 9.0, 0.5, 0.55)] if PB else []),       # the 200 final in the rain, Nagoya
    split(t_now - 0.05, R('photo1'), 0, 0.3, 0.45),              # 9.90 Games record board
    full(t_19 - 0.05, VERT, 30.5, 0.5, 0.35, hit=True),           # stadium screen: FINISH 19.88
    split(t_broke - 0.05, R('photo3_2x'), 0, 0.3, 0.45),          # 19.88 Asian record board
    split(T1, VERT, 14.0, 0.5, 0.55),         # his soundbite on top, race below
    split(T1 + 7.0, R('photo1'), 0, 0.75, 0.4),
    split(t_but - 0.05, R('photo1'), 0, 0.15, 0.4),
    split(t_setup - 0.05, VERT, 44.0, 0.5, 0.35),
    (full(t_assume - 0.05, R('pb_tight'), 0, 0.5, 0.3) if PB else split(t_assume - 0.05, R('photo1'), 0, 0.3, 0.3)),  # Nike deal
    split(t_dennis - 0.3, R('photo2'), 0, 0.55, 0.4),             # Dennis Mitchell, Florida
    split(t_know - 0.05, R('photo2'), 0, 0.6, 0.25),
    split(t_protect - 0.05, R('photo1'), 0, 0.3, 0.5),
    full(t_horrible - 0.05, VERT, 14.0, 0.5, 0.5, hit=True),      # running away with it: the setup that worked
    split(t_best - 0.05, R('photo3_2x'), 0, 0.3, 0.45),
    split(t_olymp - 1.2, R('photo1'), 0, 0.3, 0.45),
]

gfx = [
    M('slam', t_ruined - 0.1, 1.6, text='RUINED HIS CAREER?', hi=0, anchor='upper'),
    M('pin', t_now + 0.6, 2.4, text='NAGOYA, JAPAN', sub='2026 ASIAN GAMES'),
    M('board', t_sub - 0.1, t_19 - t_sub, title='ASIAN GAMES · 100M', rows=[{'event': 'HEAT', 'value': '9.95'}, {'event': 'SEMI', 'value': '9.91'}, {'event': 'FINAL', 'value': '9.90'}],
      times=[0.3, 0.8, 1.3]),
    M('slam', t_19 + 0.6, 1.6, text='19.88', hi=0),
    M('board', t_least - 0.2, T1 - t_least + 0.2, title='HIS RECORDS', rows=[{'event': '100M · 9.90', 'value': 'THAI REC'}, {'event': '200M · 19.88', 'value': '=ASIAN REC'}],
      times=[0.3, at('asian record in the 200') - t_least + 0.4]),
    M('keyword', T1 + 0.4, 3.6, text='"TODAY I JUST DO IT"'),
    M('board', t_coach - 0.1, t_setup - t_coach + 0.1, title='COACH GENTRY BRADLEY', rows=[{'event': 'USA 200M CHAMP', 'value': '1998'}, {'event': 'USC STAFF', 'value': 'EX'}],
      times=[0.4, at('usc') - t_coach + 0.1]),
    M('keyword', t_setup + 0.6, 2.4, text='IDEAL SETUP AT HOME'),
    M('keyword', t_nike - 0.1, 2.6, text='NIKE DEAL · NOV 16'),
    M('pin', t_dennis - 0.2, 2.8, text='FLORIDA', sub='DENNIS MITCHELL · STAR ATHLETICS'),
    M('slam', t_move + 0.8, 1.6, text='ACROSS THE WORLD', hi=2, anchor='upper'),
    M('keyword', t_know + 0.9, 2.2, text='BEST INTERESTS?'),
    M('keyword', t_protect + 0.4, 2.2, text='PROTECTED BACK HOME'),
    M('slam', t_horrible + 0.4, 1.6, text='HORRIBLE MOVE?', hi=0, anchor='upper'),
    M('board', t_best + 0.4, t_disregard - t_best + 0.6, title='FASTEST ASIANS · 100M', rows=[{'event': '1 · SU BINGTIAN', 'value': '9.83'}, {'event': '2 · BOONSON', 'value': '9.90'}],
      times=[0.3, 1.2]),
    M('keyword', t_olymp - 0.3, 2.0, text='THEN LA 2028'),
    M('poll', t_silly - 0.2, END - t_silly + 0.2, question='IS FLORIDA A MISTAKE?', options=['YES', 'NO']),
]
zooms = [[t_ruined - 0.2, t_ruined + 1.2, 1.1], [t_know - 0.1, t_know + 1.3, 1.1], [t_silly - 0.1, t_silly + 1.2, 1.1]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/new2/build', 'output': f'{SP}/new2/out/boonson_v1.mp4', 'words': f'{H}/words_aroll.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_aroll.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}; PB {bool(PB)}")
