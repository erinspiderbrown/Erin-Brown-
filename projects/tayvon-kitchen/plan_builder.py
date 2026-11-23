"""Tayvon Kitchen NCAA XC take (~1:28): 'cut every event where fewer than 16-20 people hit the standard'. Jane Hedengren format.
Facts (NOTES.md): LA28 standards (WA, 10 Nov 2026): 100m 9.93, men TJ 17.35, women TJ 14.50, men LJ 8.30. 2026 outdoor world lists
(worldathletics.org toplists): 100m 26 men <=9.93; men TJ 7 >=17.35; women TJ 12 >=14.50; men LJ 12 >=8.30, best USA 8.29.
Ultimate Championship (Budapest, 11-13 Sep 2026) left out shot put, discus, 10,000m, steeplechase, men's triple jump."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/44aa0cd6-8023-5301-82fa-277e8bea228e/scratchpad/tayvon13'
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




t_like, t_top5, t_11th, t_one, t_now, t_just, t_african, t_so, t_but, t_now2, t_rocky, t_kicked, t_people, t_little, t_hes, t_improving, t_tilt = at('like this was'), at('it was an'), at('and we had'), at('one of probably'), at('now i inducted'), at('just the fact'), at('you african now.'), at('so you a'), at('but by the'), at('now i think'), at('rocky hansen'), at('he kicked'), at('and people try'), at('but little'), at("he's african"), at("and he's improving"), at('so i gotta')
POD = B('podium_hd.mp4')
segs = [
    full(0.0, B('p5_hd.jpg'), 0.5, 0.35, hit=True),
    split(t_like - 0.05, B('p1_hd.jpg'), 0.5, 0.4),
    split(t_top5 - 0.05, B('p2_hd.jpg'), 0.35, 0.45),
    split(t_11th - 0.05, B('p4_hd.jpg'), 0.5, 0.35),
    full(t_one - 0.05, B('p6_hd.jpg'), 0.42, 0.3, hit=True),
    split(t_now - 0.05, B('p3_hd.jpg'), 0.45, 0.35),
    split(t_just - 0.05, B('p2_hd.jpg'), 0.85, 0.4),
    split(at("that's just some") - 0.05, POD, 0.5, 0.45, ss=1.0),
    split(t_african - 0.05, B('p6_hd.jpg'), 0.45, 0.3),
    split(t_so - 0.05, B('p2_hd.jpg'), 0.5, 0.45),
    full(t_but - 0.05, B('p3_hd.jpg'), 0.4, 0.35),
    split(at("you won't be") - 0.05, B('p5_hd.jpg'), 0.5, 0.3),
    split(t_now2 - 0.05, B('p1_hd.jpg'), 0.3, 0.4),
    split(t_kicked - 0.05, B('p1_hd.jpg'), 0.7, 0.4),
    split(t_people - 0.05, POD, 0.5, 0.45, ss=3.5),
    full(t_little - 0.05, B('p5_hd.jpg'), 0.42, 0.3, hit=True),
    split(t_hes - 0.05, B('p2_hd.jpg'), 0.86, 0.35),
    split(t_improving - 0.05, B('p4_hd.jpg'), 0.5, 0.3),
    split(t_tilt - 0.05, B('p5_hd.jpg'), 0.5, 0.3),
]
gfx = [
    M('keyword', 0.3, 3.4, text='AFRICA SHOWED UP'),
    M('pin', 3.9, 1.9, text='TERRE HAUTE, IN', sub='2026 NCAA XC · MEN 10K'),
    M('board', t_top5 - 0.1, t_11th - t_top5 + 0.1, title='2026 NCAA XC · TOP 5',
      rows=[{'event': '1 · E. KIPRUTO', 'value': '28:27.7'}, {'event': '2 · D. LOKIRA', 'value': '28:30.8'}, {'event': '3 · D. KIPNGETICH', 'value': '28:32.5'},
            {'event': '4 · S. KIPCHOGE', 'value': '28:34.8'}, {'event': '5 · D. KIPRUTO', 'value': '28:36.9'}], times=[0.2, 0.7, 1.2, 1.7, 2.2]),
    M('slam', t_11th + 1.1, 1.6, text='11TH PLACE', hi=0, anchor='upper'),
    M('keyword', t_now + 0.6, 3.0, text='AFRICAN BROTHERHOOD'),
    M('slam', t_african + 1.0, 1.8, text='YOU KENYAN NOW', hi=2, anchor='upper'),
    M('slam', at('no stopping') - 0.2, 1.6, text='NO STOPPING HIM', hi=1, anchor='upper'),
    M('board', t_rocky - 0.2, t_people - t_rocky, title='WHERE THEY FINISHED',
      rows=[{'event': '6 · ROCKY HANSEN', 'value': '28:38.4'}, {'event': '11 · TAYVON KITCHEN', 'value': '28:51.0'}], times=[0.3, 1.3]),
    M('keyword', t_little + 0.5, 2.4, text='RESPECT'),
    M('board', t_improving - 0.1, t_tilt - t_improving + 0.2, title='TAYVON AT NCAA XC',
      rows=[{'event': '2025 · FRESHMAN', 'value': '32ND'}, {'event': '2026 · SOPHOMORE', 'value': '11TH'}], times=[0.2, 0.9]),
    M('poll', t_tilt, END - t_tilt, question='TOP 5 FOR TAYVON NEXT YEAR?', options=['YES', 'NO']),
]
zooms = [[at('he\'s trash') - 0.1, at('he\'s trash') + 1.0, 1.1], [at('you kenyan') - 0.1, at('you kenyan') + 1.0, 1.1]]
segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
os.makedirs(f'{SP}/out', exist_ok=True)
plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/tayvon_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
