"""LA28 standards hot take (~1:28): 'cut every event where fewer than 16-20 people hit the standard'. Jane Hedengren format.
Facts (NOTES.md): LA28 standards (WA, 10 Nov 2026): 100m 9.93, men TJ 17.35, women TJ 14.50, men LJ 8.30. 2026 outdoor world lists
(worldathletics.org toplists): 100m 26 men <=9.93; men TJ 7 >=17.35; women TJ 12 >=14.50; men LJ 12 >=8.30, best USA 8.29.
Ultimate Championship (Budapest, 11-13 Sep 2026) left out shot put, discus, 10,000m, steeplechase, men's triple jump."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/44aa0cd6-8023-5301-82fa-277e8bea228e/scratchpad/cut10'
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

def FRZ(name, src, dur, pick, focus=(0.5, 0.5), push=1.08, glow=None):
    out = f'{SP}/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
    spec = {'src': src, 'ss': 0, 'out': out, 'dur': round(dur + 0.6, 2), 'pick': pick, 'focus': list(focus), 'push': push, **({'glow': glow} if glow else {})}
    js = out[:-4] + '.json'
    if not (os.path.exists(out) and os.path.exists(js) and json.load(open(js)) == spec):
        json.dump(spec, open(js, 'w')); subprocess.run(['python3', f'{H}/../../editor/freeze.py', js], check=True)
    return out

END = round(W[-1]['e'] + 1.8, 2)
full = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': k.pop('ss', 0), 'focus': [fx, fy]}, **k}
split = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': k.pop('ss', 0), 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_drop, t_idea, t_100, t_995, t_any, t_getrid1, t_because, t_why = at('they just dropped'), at('brilliant idea'), at('for the 100'), at('9.95'), at('i feel like any'), at('get rid of those'), at('because clearly'), at('so why the')
t_ult, t_elim, t_past, t_saw, t_mens, t_womens, t_only56, t_getrid2 = at('now the ultimate'), at('eliminating'), at('this past season'), at('we saw the best'), at("men's triple"), at("women's triple"), at('only five'), at('get rid of that', 1)
t_long, t_noam, t_12, t_getrid3, t_care, t_sowho, t_getrid4, t_bril2 = at('for the long'), at('no americans'), at('only like 12'), at('get rid of that', 2), at("we don't even care"), at('so if these'), at('get rid of that', 3), at('this is a brilliant')
t_incl, t_money, t_less, t_fan, t_cover, t_cant, t_many, t_letsgo = at('this would make'), at('it will bring'), at('we have to worry'), at('as a fan'), at('i cover track'), at("can't even tell"), at('too many damn'), at("so let's get")

segs = [
    full(0.0, B('los_angeles_memorial_coliseum.jpg'), 0.5, 0.5, hit=True),
    split(t_drop - 0.05, B('la_sunrise_4k.mp4'), 0.5, 0.5, ss=36),
    split(t_idea - 0.4, B('lyles_paris.jpg'), 0.5, 0.3),
    full(t_100 - 0.05, FRZ('lyles_100b', B('lyles_usatf2_v.jpg'), t_any - t_100, [0.55, 0.45], focus=(0.5, 0.4)), 0.5, 0.45),
    split(t_any - 0.05, B('lyles_thumb_hd.jpg'), 0.5, 0.3),
    split(t_getrid1 - 0.05, B('empty_seats.jpg'), 0.5, 0.5),
    split(t_because + 1.2, B('hollywood_4k.mp4'), 0.5, 0.5, ss=16),
    full(t_ult - 0.05, B('crouser_v.jpg'), 0.5, 0.35),
    split(t_elim - 0.6, B('sarr_1.jpg'), 0.5, 0.45),
    split(t_past - 0.05, B('tentoglou_ist.jpg'), 0.5, 0.4),
    split(t_saw - 0.05, B('lj_indoor12.jpg'), 0.5, 0.5),
    full(t_mens - 0.05, FRZ('pichardo', B('pichardo_v.jpg'), t_womens - t_mens, [0.5, 0.5], focus=(0.5, 0.45)), 0.5, 0.45, hit=True),
    split(t_womens - 0.05, B('rojas_jump.jpg'), 0.5, 0.35),
    split(t_getrid2 - 0.05, B('lafond_1.jpg'), 0.5, 0.4),
    full(t_long - 0.05, FRZ('tentoglou', B('tentoglou_v.jpg'), t_noam - t_long + 0.6, [0.5, 0.5], focus=(0.5, 0.45), glow=[232, 35, 30]), 0.5, 0.45),
    split(t_noam + 0.55, B('pinnock.jpg'), 0.5, 0.45),
    split(t_care - 0.05, B('pichardo_paris.jpg'), 0.62, 0.45),
    split(t_sowho - 0.05, B('rojas_v.jpg'), 0.5, 0.3),
    full(t_getrid4 - 0.05, B('lyles_paris.jpg'), 0.5, 0.35, hit=True),
    split(t_incl - 0.05, B('la_sunrise_4k.mp4'), 0.5, 0.5, ss=12),
    split(t_money - 0.05, B('hollywood_4k.mp4'), 0.5, 0.5, ss=30),
    split(t_less - 0.05, B('lyles_usatf2_v.jpg'), 0.5, 0.55),
    split(t_fan - 0.05, B('los_angeles_memorial_coliseum.jpg'), 0.3, 0.5),
    split(t_cant - 0.05, B('crouser_v.jpg'), 0.5, 0.45),
    split(t_letsgo - 0.05, B('tentoglou_ist.jpg'), 0.35, 0.4),
]
gfx = [
    M('keyword', 0.3, 2.8, text='TOO INCLUSIVE?'),
    M('keyword', t_drop + 0.4, 3.0, text='LA28 STANDARDS'),
    M('slam', t_idea - 0.1, 1.6, text='BRILLIANT IDEA', hi=0, anchor='upper'),
    D('counter', t_995 - 0.3, 2.9, value='9.93', unit='SECONDS', label='LA28 100M STANDARD', sub='26 men ran it in 2026'),
    M('keyword', t_any + 1.6, 3.0, text='16-20 PEOPLE OR CUT IT'),
    M('slam', t_getrid1 - 0.1, 1.3, text='GET RID OF IT', hi=0, anchor='upper'),
    M('keyword', t_why + 0.2, 2.2, text='WHY SUFFER?'),
    M('pin', t_ult + 0.6, 2.6, text='BUDAPEST', sub='ULTIMATE CHAMPIONSHIP · SEP 2026'),
    M('board', t_elim - 0.4, t_past - t_elim + 0.2, title='LEFT OUT IN BUDAPEST',
      rows=[{'event': 'SHOT PUT', 'value': 'CUT'}, {'event': 'DISCUS', 'value': 'CUT'}, {'event': '10,000M', 'value': 'CUT'},
            {'event': "MEN'S TRIPLE JUMP", 'value': 'CUT'}], times=[0.2, 0.8, 1.4, 2.0]),
    M('slam', t_saw - 0.1, 1.4, text='BEST OF THE BEST', hi=3, anchor='upper'),
    M('board', t_only56 - 0.3, t_getrid2 - t_only56 + 1.3, title='2026 · HIT THE LA28 MARK',
      rows=[{'event': "MEN'S TJ 17.35", 'value': '7'}, {'event': "WOMEN'S TJ 14.50", 'value': '12'}], times=[0.2, 0.9]),
    M('slam', t_noam - 0.05, 1.3, text='0 AMERICANS', hi=0, anchor='upper'),
    M('board', t_noam + 1.4, t_care - t_noam - 1.4, title="MEN'S LONG JUMP · 8.30",
      rows=[{'event': 'HIT IT IN 2026', 'value': '12'}, {'event': 'AMERICANS', 'value': '0'}, {'event': 'BEST AMERICAN', 'value': '8.29'}],
      times=[t_12 - t_noam - 1.2, 0.2 + 0.6, 1.9]),
    M('keyword', t_care + 0.3, 1.6, text='FIELD EVENTS?'),
    M('slam', t_getrid4 - 0.05, 1.4, text='GET RID OF IT', hi=0, anchor='upper'),
    M('keyword', t_incl + 0.4, 2.2, text='LESS INCLUSIVE'),
    M('keyword', t_money + 0.2, 2.2, text='MORE MONEY?'),
    M('keyword', t_cover + 0.1, 1.4, text='I COVER TRACK DAILY'),
    M('slam', t_many - 0.1, 1.4, text='TOO MANY EVENTS', hi=2, anchor='upper'),
    M('poll', t_letsgo, END - t_letsgo, question='SHOULD TRACK CUT EVENTS?', options=['YES', 'NO']),
]
zooms = [[t_why - 0.1, t_why + 1.4, 1.1], [t_getrid2 - 0.1, t_getrid2 + 1.0, 1.1], [t_cant - 0.1, t_cant + 1.4, 1.08]]
segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
os.makedirs(f'{SP}/out', exist_ok=True)
plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/cut_events_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
