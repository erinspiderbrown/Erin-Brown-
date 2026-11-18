"""Shea Foster doping case (~1:28): 'cut every event where fewer than 16-20 people hit the standard'. Jane Hedengren format.
Facts (NOTES.md): LA28 standards (WA, 10 Nov 2026): 100m 9.93, men TJ 17.35, women TJ 14.50, men LJ 8.30. 2026 outdoor world lists
(worldathletics.org toplists): 100m 26 men <=9.93; men TJ 7 >=17.35; women TJ 12 >=14.50; men LJ 12 >=8.30, best USA 8.29.
Ultimate Championship (Budapest, 11-13 Sep 2026) left out shot put, discus, 10,000m, steeplechase, men's triple jump."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/44aa0cd6-8023-5301-82fa-277e8bea228e/scratchpad/shea11'
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


t_kenyans2, t_africans, t_comments, t_school, t_osu, t_susp, t_guess, t_white, t_houston, t_shea = at('these kenyans', 2), at('these africans'), at('this is what i always'), at('in a school'), at('oklahoma state', 1), at('was suspended'), at('and guess what'), at('he was a white'), at('from houston'), at('shea foster', 1)
t_first, t_birm, t_won, t_mile, t_3k, t_5k, t_broke, t_intro, t_lap, t_trans, t_disap = at('now, my first'), at('but freshman year'), at('he went out'), at('the mile,'), at('the 3k,'), at('the 5k,'), at('broke all three'), at('this is my introduction'), at('literally lapping'), at('but he transferred'), at('just disappeared.')
t_train, t_snitch, t_epo, t_coach, t_won2, t_para, t_caught, t_paris, t_thought, t_gault, t_dropped, t_twitter, t_shout, t_dist = at('but turns out'), at('one of his'), at('found epo'), at('the coach didn\'t'), at('i think they still'), at('came back to'), at("and that's how"), at("and that's why"), at('but i thought'), at('then the jonathan'), at('i literally dropped'), at('he literally follows'), at('hey man, shout'), at('shout out to everybody')

segs = [
    full(0.0, B('p5_hd.jpg'), 0.62, 0.4, hit=True),                     # OSU race photo (Foster #148) under the "Kenyans" claims
    split(t_kenyans2 - 0.05, B('p6_hd.jpg'), 0.5, 0.45),
    split(t_africans - 0.05, B('p5_hd.jpg'), 0.35, 0.4),
    split(at('these are the type') - 0.05, B('p7_hd.jpg'), 0.5, 0.35),
    split(t_won - 0.05, B('p5_hd.jpg'), 0.55, 0.35),
    split(at("i'm like, damn") - 0.05, B('p7_hd.jpg'), 0.42, 0.4),
    split(at('making it seem') - 0.05, B('p5_hd.jpg'), 0.7, 0.4),
    split(at('and all he went') - 0.05, B('p6_hd.jpg'), 0.15, 0.45),
    split(t_comments - 0.05, B('p6_hd.jpg'), 0.25, 0.5),
    full(t_school - 0.05, B('p6_hd.jpg'), 0.5, 0.45),
    split(t_susp - 0.6, B('p4_hd.jpg'), 0.5, 0.55),
    full(t_white - 0.05, B('p1_hd.jpg'), 0.45, 0.3, hit=True),
    split(t_first - 0.05, B('p8_hd.jpg'), 0.5, 0.35),
    split(t_birm - 0.05, B('p1_hd.jpg'), 0.5, 0.35),
    split(t_intro - 0.05, B('p8_hd.jpg'), 0.62, 0.4),
    split(t_lap - 0.05, B('p1_hd.jpg'), 0.62, 0.3),
    split(t_trans - 0.05, B('p7_hd.jpg'), 0.55, 0.4),
    split(t_train - 0.05, B('p6_hd.jpg'), 0.75, 0.45),
    full(t_snitch - 0.05, B('p5_hd.jpg'), 0.66, 0.45, hit=True),
    split(t_coach - 0.05, B('p6_hd.jpg'), 0.4, 0.45),
    full(t_para - 0.05, B('p2_hd.jpg'), 0.5, 0.4),
    split(t_caught + 0.6, B('p3_hd.jpg'), 0.5, 0.35),
    full(t_paris - 0.05, B('p3_hd.jpg'), 0.42, 0.4),
    split(t_thought - 0.05, B('p6_hd.jpg'), 0.6, 0.45),
    split(t_gault - 0.05, B('p4_hd.jpg'), 0.5, 0.25),
    split(t_dropped - 0.05, B('p4_hd.jpg'), 0.5, 0.7),
    split(t_twitter - 0.05, B('p8_hd.jpg'), 0.4, 0.35),
    split(t_shout - 0.05, B('p1_hd.jpg'), 0.42, 0.35),
    split(t_dist - 0.05, B('p7_hd.jpg'), 0.5, 0.4),
]
gfx = [
    M('keyword', 0.3, 3.0, text='"ALWAYS DOPING"'),
    M('keyword', t_kenyans2 + 0.6, 3.0, text='"ALWAYS TOO OLD"'),
    M('bubbles', t_comments, t_school - t_comments - 0.3, items=['KENYANS ALWAYS DOPING', 'ALWAYS TOO OLD', 'AFRICANS ALWAYS DOPING']),
    M('pin', t_osu - 0.3, 2.8, text='OKLAHOMA STATE', sub='STILLWATER, OK'),
    M('keyword', t_susp + 0.2, 1.4, text='SUSPENDED'),
    M('slam', t_guess + 0.6, 1.6, text='NOT KENYAN', hi=1, anchor='upper'),
    M('pin', t_houston - 0.1, 1.9, text='HOUSTON, TX', sub='CYPRESS WOODS HS'),
    M('keyword', t_birm + 1.0, 2.6, text='SOUTHLAND INDOORS 2021'),
    M('board', t_won - 0.1, t_intro - t_won + 0.3, title='2021 SOUTHLAND INDOORS',
      rows=[{'event': 'MILE · 1ST', 'value': '4:03.57'}, {'event': '3000M · 1ST', 'value': '8:00.79'}, {'event': '5000M · 1ST', 'value': '13:40.36'}],
      times=[t_mile - t_won + 0.1, t_3k - t_won + 0.1, t_5k - t_won + 0.1]),
    M('slam', t_lap + 0.3, 1.6, text='LAPPED IN A MILE', hi=0, anchor='upper'),
    M('keyword', t_trans + 0.4, 2.6, text='TRANSFER: OKLAHOMA STATE'),
    M('slam', t_disap - 0.3, 1.2, text='DISAPPEARED', hi=0, anchor='upper'),
    M('pin', t_train + 0.4, 2.6, text='FLAGSTAFF, AZ', sub='SUMMER 2022 TRAINING'),
    M('slam', t_epo - 0.1, 1.6, text='EPO FOUND', hi=0, anchor='upper'),
    M('board', t_won2 - 0.3, t_para - t_won2 + 0.2, title='2022 NCAA XC · TEAM',
      rows=[{'event': '1 · NAU', 'value': '83'}, {'event': '2 · OKLAHOMA ST', 'value': '83'}], times=[0.2, 0.9]),
    M('keyword', t_para + 1.0, 2.6, text='WON THE 2024 PARA TRIALS'),
    M('board', t_caught + 0.6, t_paris - t_caught + 0.6, title='HOW HE GOT CAUGHT',
      rows=[{'event': 'JUL 2024 TRIALS', 'value': 'POSITIVE'}, {'event': 'PARIS 2024', 'value': 'WITHDREW'}, {'event': 'OCT 2026 · CAS', 'value': '4 YEARS'}], times=[0.2, 1.4, 2.6]),
    M('slam', t_thought + 0.4, 1.8, text='THE AFRICANS?', hi=1, anchor='upper'),
    M('keyword', t_gault + 0.4, 2.6, text='LETSRUN · NOV 2026'),
    M('keyword', t_dropped + 0.6, 2.8, text='MY VIDEO CAME FIRST'),
    M('poll', t_dist, END - t_dist, question='DID YOU THINK IT WAS HIM?', options=['YES', 'NO']),
]
zooms = [[t_guess - 0.1, t_guess + 1.2, 1.1], [t_lap - 0.1, t_lap + 1.6, 1.08], [t_thought - 0.1, t_thought + 1.6, 1.1]]
segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
os.makedirs(f'{SP}/out', exist_ok=True)
plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/shea_foster_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
