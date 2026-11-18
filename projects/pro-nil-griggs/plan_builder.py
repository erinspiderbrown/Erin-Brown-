"""'No such thing as a pro track runner' take (~1:40): owner's talking head (4K, tightened) with two bites of Oregon head coach
Jerry Schumacher (720p interview, caption block cropped off, FSRCNN 2x, top slot) on Nick Griggs / pro contracts being NIL contracts.
B-roll: Commons: 2023 Worlds 1500 heat with Griggs (vertical crop, full-screen + spotlight), Hayward Field x2 (split),
2024 Olympic Trials + a Hayward race (vertical, full-screen). Facts in NOTES.md."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/words_aroll.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'
T1, LA, T2, LB = 24.0, 19.36, 36.9 + 19.36, 10.9          # bite A at T1 (LA s), bite B at T2 (LB s), A-roll times


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


END = round(W[-1]['e'] + 3.0, 2)
full = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': [fx, fy]}, **k}
split = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_notsport, t_contract, t_oregon, t_asking, t_told = at('track is not'), at('no such thing as a professional contract'), at('the oregon coach'), at('they were asking'), at('he literally told')
t_nil1, t_paid = at('just nil contracts'), at('being paid')
t_review, t_same, t_these, t_justnil = at('gets reviewed'), at('exact same'), at('these people'), at("they're just nil", 2)
t_mf, t_haven, t_fall, t_collect, t_cheat = at('so these'), at("if you haven't"), at('fall off'), at('collect'), at('cheat code')

segs = [
    full(0.0, R('trials63'), 0.5, 0.45, hit=True),                     # Hayward, 2024 Olympic Trials
    split(5.6, R('hayward21'), 0.45, 0.6),
    split(t_contract - 0.05, R('hayward_new'), 0.3, 0.45),
    full(t_asking - 0.05, R('griggs_916'), 0.5, 0.0, hit=True),         # the pro athlete back in college: Nick Griggs
    split(t_told - 0.05, R('hayward21'), 0.75, 0.55),
    split(T1, R('hayward_race'), 0.5, 0.6),                             # coach bite A on top
    split(T1 + 7.0, R('griggs_wkb'), 0.2, 0.25),
    split(T1 + 13.5, R('hayward_new'), 0.75, 0.55),
    split(T1 + LA, R('hayward_race'), 0.5, 0.35),
    split(t_review - 0.05, R('hayward21'), 0.2, 0.55),
    split(t_same - 0.05, R('trials63'), 0.5, 0.3),
    split(T2, R('trials63'), 0.5, 0.75),                                # coach bite B on top
    split(T2 + 5.5, R('hayward_new'), 0.55, 0.7),
    full(t_these - 0.05, R('hayward_race'), 0.5, 0.5, hit=True),       # "they're just NIL athletes"
    split(t_mf - 0.05, R('griggs_wkb'), 0.7, 0.6),
    split(t_haven - 0.05, R('hayward21'), 0.5, 0.45),
    split(t_fall - 0.05, R('hayward_new'), 0.15, 0.5),
    split(at('come to college') - 0.05, R('griggs_wkb'), 0.45, 0.6),
    full(t_collect - 0.3, R('griggs_916'), 0.5, 0.25),                  # cheat code: back to college
]

gfx = [
    M('slam', 1.5, 1.8, text='NO PRO TRACK RUNNERS?', hi=1, anchor='upper'),
    M('keyword', t_notsport + 0.4, 2.2, text='NOT A PRO SPORT'),
    M('keyword', t_contract + 0.6, 2.2, text='NO "PRO" CONTRACTS'),
    M('pin', t_oregon, 2.6, text='EUGENE, OREGON', sub='OREGON HEAD COACH SPEAKS'),
    M('spotlight', t_asking + 0.6, 2.6, x=594, y=230, r=130, lx=120, ly=470, text='NICK GRIGGS'),
    M('board', t_told - 0.1, T1 - t_told + 0.1, title='NICK GRIGGS · IRELAND', rows=[{'event': 'PRO WITH PUMA', 'value': '4 YRS'}, {'event': 'NCAA ELIGIBILITY', 'value': '3 YRS'}],
      times=[0.2, 1.0]),
    M('podcast', T1 + 0.2, 4.0, text='JERRY SCHUMACHER', tag='OREGON HEAD COACH', anchor='upper'),
    M('slam', t_nil1 + 0.2, 2.0, text='JUST NIL CONTRACTS', hi=1),
    M('keyword', t_review + 0.3, 2.2, text='COMPLIANCE READS IT'),
    M('slam', t_same, 2.0, text='SAME AS NIL', hi=2, anchor='upper'),
    M('keyword', t_paid - 0.1, 3.0, text='"PAID TO WEAR THE PRODUCT"'),
    M('slam', t_justnil, 1.8, text='JUST NIL ATHLETES', hi=1, anchor='upper'),
    M('flow', t_haven + 0.2, t_collect - t_haven - 0.4, items=['SIGN A SHOE DEAL', 'FALL OFF', 'BACK TO THE NCAA'],
      times=[at('signed') - t_haven - 0.2, t_fall - t_haven - 0.2, at('come to college') - t_haven - 0.2]),
    M('slam', at('method') - 0.2, 1.6, text='CHEAT CODE', hi=0, anchor='upper'),
    M('poll', t_cheat - 0.2, END - t_cheat + 0.2, question='ARE "PRO" RUNNERS JUST NIL ATHLETES?', options=['YES', 'NO']),
]
zooms = [[t_notsport - 0.1, t_notsport + 1.3, 1.1], [t_these - 0.1, t_these + 1.2, 1.1], [t_haven - 0.1, t_haven + 1.2, 1.08]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/new3/build', 'output': f'{SP}/new3/out/pro_nil_v1.mp4', 'words': f'{H}/words_aroll.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_aroll.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
