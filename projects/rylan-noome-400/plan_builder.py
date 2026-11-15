"""Rylan Noome roast TikTok (~1:58): the owner's talking head (4K, cropped to 1440x1280, tightened) + his two vertical clips
(Rylan's 400 at a track meet, filmed from the stands; Rylan's power clean in the gym) + 2 photos of Rylan.
House method (Yohan Blake edit) with the Nov 2026 step-up: no name tags, slam text instead of stamps, freeze pop-outs.
Facts: World Athletics (born 10 Mar 2006 = 20; PBs 100m 10.48, 200m 21.45). The 300m 35.3, 400m 50.8 and 135 kg clean are the
owner's numbers (not in any published results); they're shown as he says them and flagged in NOTES."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,').strip("'") for x in W]
RACE, LIFT = f'{H}/raw/race_400.mp4', f'{H}/raw/power_clean.mp4'
R = lambda n: f'{H}/raw/{n}.jpg'


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def FRZ(name, src, ss, dur, pick, focus=(0.5, 0.5), push=1.08):
    out = f'{SP}/ryl/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
    spec = {'src': src, 'ss': ss, 'out': out, 'dur': round(dur + 0.6, 2), 'pick': pick, 'focus': list(focus), 'push': push}
    js = out[:-4] + '.json'
    if not (os.path.exists(out) and os.path.exists(js) and json.load(open(js)) == spec):
        json.dump(spec, open(js, 'w')); subprocess.run(['python3', f'{H}/../../editor/freeze.py', js], check=True)
    return out


END = round(W[-1]['e'] + 1.6, 2)
full = lambda t, src, ss=0, fx=0.5, fy=0.5, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
split = lambda t, src, ss=0, fx=0.5, fy=0.5, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_have, t_atroc, t_30 = at('and he have'), at('atrocities'), at('30 days')
t_month, t_300, t_swam, t_353 = at('a month ago'), at('ran a 300'), at('he swam'), at('35.3')
t_emb, t_nz = at('embarrassed the whole'), at('new zealand', 2)
t_train, t_ran400, t_508, t_51 = at('he had a month'), at('ran a 400', 2), at('ran 50.8'), at('damn near ran')
t_20, t_200lb, t_big, t_elec = at('as a 20'), at('at 200 pounds'), at("he's just way"), at('electric')
t_built, t_freezer, t_caf = at("he's literally built"), at('deep freezer'), at('school cafeteria')
t_after, t_world, t_lift = at('but after he'), at('whole world'), at('decided to go')
t_135, t_strong = at('he went and lifted'), at("world's strongest")
t_clean, t_meet, t_third, t_nov, t_nats = at('but he has'), at("he's going out"), at('this is his third'), at('mind you'), at('their nationals')
t_100200, t_people, t_400r, t_see = at("but he's running"), at('now a lot'), at("ain't no 400"), at('so we gonna see')
t_if, t_through, t_etern, t_put, t_waste = at('now if he'), at('we through'), at('for eternity'), at('get him put'), at("he's wasting")

segs = [
    full(0.0, FRZ('rylan_hook', LIFT, 9.1, t_have, [0.55, 0.45, 1]), 0, 0.5, 0.5),   # hook: freeze pop-out, bar racked (no name tag)
    split(t_have - 0.05, RACE, 0.0, 0.5, 0.55),                         # meets
    full(t_month - 0.05, RACE, 2.0, 0.5, 0.6, hit=True),               # the 300 a month ago
    split(t_swam - 0.05, RACE, 20.0, 0.5, 0.6),
    split(t_emb - 0.05, R('photo_kick'), 0, 0.6, 0.45),                # embarrassed New Zealand
    split(t_train - 0.05, R('photo_blocks'), 0, 0.5, 0.4),             # a month to train
    full(t_ran400 - 0.05, RACE, 47.0, 0.5, 0.65, hit=True),            # the 400: down the straight
    split(t_20 - 0.05, RACE, 51.5, 0.5, 0.6),
    full(t_200lb - 0.05, LIFT, 0.5, 0.5, 0.5),                         # 200 lbs lifting all this weight
    split(t_big + 1.0, RACE, 40.0, 0.5, 0.65),                         # nothing electric on the track
    full(t_built - 0.05, LIFT, 14.5, 0.5, 0.5),                        # deep freezer: him sitting after the lift
    split(t_caf - 0.15, R('photo_blocks'), 0, 0.5, 0.55),
    full(t_after - 0.05, RACE, 44.0, 0.5, 0.65),                       # embarrassed the whole world
    split(t_lift - 0.05, LIFT, 3.0, 0.5, 0.55),
    full(t_135 - 0.05, LIFT, 7.4, 0.5, 0.5, hit=True),                 # the clean lands on "135 kilos"
    split(t_clean - 0.05, R('photo_kick'), 0, 0.35, 0.45),             # clean up his act
    split(t_third - 0.05, RACE, 0.5, 0.5, 0.55),
    split(t_nats - 0.05, RACE, 25.0, 0.5, 0.6),
    full(t_100200 - 0.05, RACE, 4.5, 0.5, 0.6),                        # running the 100 and 200
    split(t_people - 0.05, R('photo_blocks'), 0, 0.5, 0.35),
    split(t_see, RACE, 49.0, 0.5, 0.6),
    full(t_if - 0.05, FRZ('rylan_warning', LIFT, 7.3, t_etern - t_if, [0.55, 0.45, 1]), 0, 0.5, 0.5, hit=True),
    split(t_etern - 0.05, RACE, 30.0, 0.5, 0.6),
    split(t_waste - 0.05, LIFT, 15.0, 0.5, 0.5),
]

gfx = [
    M('pin', 1.2, 2.2, text='NEW ZEALAND', sub='RYLAN NOOME · 20'),
    M('slam', t_atroc - 0.1, 1.6, text='MULTIPLE ATROCITIES', hi=1, anchor='upper'),
    M('keyword', t_30 - 0.2, 1.4, text='LAST 30 DAYS'),
    M('keyword', t_300 + 0.1, 1.5, text='THE 300'),
    M('slam', t_swam, 1.3, text='SWAM HIS WAY', hi=1, anchor='upper'),
    M('stopwatch', t_353 - 0.3, 2.0, value='35.3', unit='SECONDS', label='300M · ONE MONTH AGO', anim=0.9),
    M('keyword', t_nz - 0.4, 1.4, text='WHOLE COUNTRY'),
    M('keyword', t_train + 0.3, 1.5, text='A MONTH TO TRAIN'),
    M('stopwatch', t_508 - 0.2, 2.6, value='50.8', unit='SECONDS', label='400M · THE COMEBACK', anim=0.9),
    D('counter', t_20 + 0.2, 2.0, value='20', unit='YEARS OLD', label='Grown man', sub='born March 2006'),
    M('keyword', t_200lb + 0.3, 1.6, text='200 POUNDS'),
    M('slam', t_big + 1.6, 1.4, text='WAY TOO BIG', hi=2, anchor='upper'),
    M('keyword', t_elec - 0.1, 1.3, text='NOT ELECTRIC'),
    M('slam', t_freezer - 0.7, 1.9, text='DEEP FREEZER', hi=1),
    M('keyword', t_caf - 0.1, 1.6, text='SCHOOL CAFETERIA'),
    M('slam', t_world - 0.2, 1.6, text='THE WHOLE WORLD', hi=2, anchor='upper'),
    M('keyword', t_lift + 0.6, 1.4, text='EVEN MORE WEIGHT'),
    D('counter', t_135 + 0.4, 2.4, value='135', unit='KG', label='Power clean', sub='~298 lbs'),
    M('slam', t_strong - 0.3, 1.5, text="WORLD'S STRONGEST MAN?", hi=1, anchor='upper'),
    M('slam', t_clean + 1.4, 1.6, text='CLEAN UP HIS ACT', hi=[0, 1], anchor='upper'),
    M('board', t_third - 0.1, 3.4, title='HIS SEASON (NOV 2026)',
      rows=[{'event': 'MEET 1 · 300M', 'value': '35.3'}, {'event': 'MEET 2 · 400M', 'value': '50.8'}, {'event': 'MEET 3 · 100/200', 'value': '???'}],
      times=[0.1, 0.6, 1.1]),
    M('keyword', t_nov + 0.2, 1.6, text='EARLY NOVEMBER'),
    M('keyword', t_nats + 0.3, 2.0, text='NATIONALS: MARCH'),
    M('bubbles', t_people + 0.1, 3.4, items=['NOT A LONG SPRINTER', "AIN'T NO 400 RUNNER", 'STICK TO THE 100']),
    M('board', t_see - 0.1, 3.0, title='HIS OFFICIAL BESTS', rows=[{'event': '100M', 'value': '10.48'}, {'event': '200M', 'value': '21.45'}],
      times=[0.6, 1.4]),
    M('slam', t_through - 0.3, 1.5, text='WE THROUGH', hi=1, anchor='lower'),
    M('keyword', t_etern + 0.05, 1.5, text='FOR ETERNITY'),
    M('slam', t_waste + 0.2, 1.8, text='WASTING RESOURCES', hi=1, anchor='upper'),
    M('poll', W[-1]['e'] - 2.2, END - W[-1]['e'] + 2.2, question='100 OR 200: WHAT IS HE?', options=['100', '200']),
]
zooms = [[t_atroc - 0.2, t_atroc + 1.2, 1.1], [t_51, t_51 + 1.4, 1.1], [t_strong - 0.3, t_strong + 1.2, 1.1], [t_through - 0.3, t_through + 1.2, 1.14],
         [t_see, t_see + 1.4, 1.08]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/ryl/build', 'output': f'{SP}/ryl/out/rylan_noome_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
