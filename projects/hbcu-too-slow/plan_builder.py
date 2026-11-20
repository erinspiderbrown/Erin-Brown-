"""'An HBCU coach told me I was too slow' story (~4:00): owner's talking head (4K, tightened) + his own police-call clip
(title cropped, muted except "Thank you for your service") spliced after "thanked him for his service", and the coach's Pop the Balloon
intro (subtitles cropped, top slot) after "I seen him on Pop the Balloon".
B-roll: Commons photos of the real places: PVAMU homecoming, Panther Stadium, PV band, SWAC track, Sam Houston, Carl Lewis, ASU.
Notes on facts in NOTES.md (PV graduation-rate claim is NOT shown: the real six-year rate is ~34-45%)."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/words_aroll.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'
COP = f'{H}/work/clipB_full.mp4'
T1, LB, LA = 190.2, 4.2, 7.8
T2 = 202.7 + LB                        # Pop the Balloon insert start (A-roll time)


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
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

t_slow1, t_police1, t_10th, t_ran49, t_texas, t_comp, t_super = at('too slow'), at('called the police'), at('see, when'), at('i ran 49'), at('i was in texas'), at('but in comparison'), at('pre -super')
t_coaches, t_sat, t_1200, t_next, t_484, t_hitall, t_carl, t_everybody = at('so i started hitting'), at('take the sat'), at('scored like'), at('then my next'), at('ran 48'), at('so i hit up all'), at('carl lewis'), at('and everybody was')
t_pv, t_compare, t_coachtold, t_tooslow2, t_800, t_walk, t_wtf, t_power, t_never = at('so i hit up hbcu'), at('compare myself'), at('and their coach'), at('too damn slow'), at('start running an 800'), at('let you walk on'), at('how i\'m walking'), at('all these other power'), at("i'll never")
t_list, t_college, t_sam, t_party, t_homecoming, t_dead, t_known, t_did, t_cops, t_pulled, t_walkcar = at('so i just took'), at('went to college'), at('i went to sam'), at('sam, tsu'), at('pulled up to homecoming'), at('really dead'), at('like they supposed'), at('so you know what'), at('called the cops'), at('cops pulled up'), at('and as i was walking')
t_only, t_arizona, t_seen, t_after, t_fired, t_shout = at('and i only did'), at('the coach ended up'), at('seen him on'), at('i was like, what the f*ck', 2), at('they all got fired'), at('but shout out')

segs = [
    full(0.0, R('pv_homecoming'), 0, 0.5, 0.45, hit=True),               # real PVAMU homecoming
    split(t_10th - 0.05, R('swac1'), 0, 0.5, 0.45),                      # 400 race
    split(t_texas - 0.05, R('swac1'), 0, 0.25, 0.4),
    split(t_comp - 0.05, R('swac2'), 0, 0.5, 0.4),
    split(t_coaches - 0.05, R('pv_tsu'), 0, 0.3, 0.45),
    split(t_1200 - 0.6, R('asu_campus'), 0, 0.5, 0.45),
    split(t_next - 0.05, R('swac1'), 0, 0.75, 0.45),
    split(t_hitall - 0.05, R('pv_storm2'), 0, 0.5, 0.5),
    full(t_carl - 0.1, R('carl_lewis'), 0, 0.5, 0.35),                   # Carl Lewis
    split(t_everybody - 0.05, R('swac2'), 0, 0.2, 0.4),
    full(t_pv - 0.05, R('pv_stadium'), 0, 0.5, 0.5, hit=True),          # Prairie View: Panther Stadium
    split(t_compare - 0.05, R('swac2'), 0, 0.8, 0.4),                    # their conference meet (SWAC)
    split(t_coachtold - 0.05, R('pv_threepeat'), 0, 0.5, 0.4),
    full(t_tooslow2 - 0.4, R('swac1'), 0, 0.5, 0.45, hit=True),          # "too damn slow"
    split(t_walk - 0.6, R('pv_stadium'), 0, 0.2, 0.55),
    split(t_power - 0.05, R('swac1'), 0, 0.4, 0.5),
    split(t_never - 0.05, R('pv_storm1'), 0, 0.5, 0.5),
    split(t_list - 0.05, R('swac2'), 0, 0.45, 0.45),
    full(t_sam - 0.05, R('shsu'), 0, 0.5, 0.5),                          # Sam Houston
    split(t_party - 0.05, R('pv_tsu'), 0, 0.6, 0.45),
    full(t_homecoming - 0.05, R('pv_storm1'), 0, 0.5, 0.5, hit=True),   # homecoming at PV
    split(t_dead - 0.4, R('pv_homecoming'), 0, 0.5, 0.25),
    split(t_known - 0.05, R('pv_stadium'), 0, 0.75, 0.5),
    split(t_cops - 0.3, R('pv_storm2'), 0, 0.3, 0.5),
    split(t_pulled - 0.05, COP, 0.0, 0.5, 0.45),                         # his own clip: police lights (muted, his narration)
    split(t_walkcar - 0.05, COP, 3.0, 0.5, 0.5),
    full(T1, COP, 8.6, 0.5, 0.5, transition='cut'),                      # "Thank you for your service"
    split(T1 + LB, R('pv_storm1'), 0, 0.8, 0.5),
    full(t_arizona - 0.05, R('asu_campus'), 0, 0.5, 0.5),                # Arizona State
    split(T2, R('asu_night'), 0, 0.5, 0.55),                             # coach on Pop the Balloon (top slot)
    split(t_after - 0.05, R('asu_campus'), 0, 0.2, 0.5),
    split(t_fired - 0.05, R('asu_night'), 0, 0.3, 0.5),
    split(t_shout - 0.05, R('pv_homecoming'), 0, 0.5, 0.6),
]

gfx = [
    M('slam', t_slow1 - 0.3, 1.5, text='TOO SLOW', hi=1, anchor='upper'),
    M('keyword', t_police1, 1.6, text='CALLED THE POLICE'),
    M('slam', at('shut down') - 0.2, 1.6, text='HOMECOMING SHUT DOWN', hi=1, anchor='upper'),
    D('counter', t_ran49 - 0.1, 2.6, value='49', unit='S', label='400M · 10TH GRADE', sub='first year running'),
    M('pin', t_texas, 2.4, text='TEXAS'),
    M('keyword', t_super - 0.3, 2.0, text='PRE-SUPER SHOES'),
    M('keyword', t_sat - 0.2, 1.8, text='TAKE THE SAT'),
    D('counter', t_1200 - 0.2, 2.6, value='1200', unit='', label='SAT SCORE', sub='took it once'),
    M('board', t_484 - 0.3, 4.0, title='MY 400M', rows=[{'event': '10TH GRADE', 'value': '49'}, {'event': '11TH GRADE', 'value': '48.4'}], times=[0.2, 0.7]),
    M('keyword', at('iowa') - 0.1, 2.2, text='IOWA · NEBRASKA'),
    M('pin', t_pv + 0.4, 2.8, text='PRAIRIE VIEW, TEXAS', sub='PRAIRIE VIEW A&M · HBCU'),
    M('keyword', t_compare + 1.0, 2.6, text='TOP 5 AT THEIR CONFERENCE MEET?'),
    M('slam', t_tooslow2 - 0.2, 1.8, text='TOO DAMN SLOW', hi=2),
    M('keyword', t_800, 2.4, text='"RUN THE 800 OR THE 200"'),
    M('slam', t_walk - 0.3, 1.7, text='WALK ON?', hi=0, anchor='upper'),
    M('keyword', t_power + 0.2, 2.4, text='POWER 5 SCHOOLS CALLING'),
    M('slam', t_never + 0.4, 1.8, text='NEVER AGAIN', hi=0, anchor='upper'),
    M('pin', t_sam + 0.3, 2.6, text='HUNTSVILLE, TEXAS', sub='SAM HOUSTON STATE'),
    M('flow', t_party, 3.6, items=['SAM HOUSTON', 'TSU · UH', 'PV HOMECOMING'], times=[0.0, 0.6, t_homecoming - t_party - 0.2]),
    M('slam', t_dead - 0.1, 1.6, text='DEAD PARTY', hi=0, anchor='upper'),
    M('slam', t_cops - 0.1, 1.8, text='CALLED THE COPS', hi=2, anchor='upper'),
    M('keyword', T1 + 0.3, 3.6, text='"THANK YOU FOR YOUR SERVICE"'),
    M('slam', t_only + 1.2, 1.8, text='TOO DAMN SLOW', hi=2, anchor='upper'),
    M('pin', t_arizona + 0.8, 2.6, text='TEMPE, ARIZONA', sub='ARIZONA STATE'),
    M('keyword', t_seen, 2.4, text='POP THE BALLOON?!'),
    M('slam', t_after + 1.2, 1.6, text='TOO SLOW?', hi=1, anchor='upper'),
    M('keyword', t_fired + 0.2, 3.0, text='ASU: NEW COACHING STAFF IN 2026'),
    M('poll', t_shout - 0.2, END - t_shout + 0.2, question='PETTY OR JUSTIFIED?', options=['PETTY', 'JUSTIFIED']),
]
zooms = [[t_wtf - 0.1, t_wtf + 1.2, 1.1], [t_did - 0.1, t_did + 1.2, 1.1], [t_after - 0.1, t_after + 1.2, 1.1]]

segs.sort(key=lambda s: s['start'])
POOL = [('swac1', 0.2, 0.45), ('pv_tsu', 0.75, 0.45), ('swac2', 0.6, 0.4), ('pv_storm2', 0.2, 0.5), ('pv_stadium', 0.45, 0.6), ('pv_storm1', 0.3, 0.5),
        ('swac1', 0.6, 0.5), ('pv_threepeat', 0.3, 0.4), ('pv_tsu', 0.15, 0.5)]
fill, k = [], 0
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    gap = b['start'] - a['start']
    if gap > 8.5 and a['start'] > 9:
        n = int(gap // 6)
        for j in range(1, n + 1):
            t = a['start'] + gap * j / (n + 1); nm, fx, fy = POOL[k % len(POOL)]; k += 1
            fill.append(split(t, R(nm), 0, fx, fy))
segs = sorted(segs + fill, key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/new4/build', 'output': f'{SP}/new4/out/hbcu_v1.mp4', 'words': f'{H}/words_aroll.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_aroll.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
