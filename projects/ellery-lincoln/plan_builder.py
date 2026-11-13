"""Ellery Lincoln early-enrollment take (~1:31): owner's talking head (4K, tightened) + his 4 photos of Lincoln (1206 px wide: split only)
+ Commons photos (Katelyn Tuohy at the 2025 Portland Track Festival: full-screen; Hayward Field: split).
Step-up rules: no name tags, slam text, freeze pop-out on Tuohy (the only sharp full-screen subject).
Facts (NOTES.md): Lincoln born 23 Jan 2009 (17); 1500 PB 4:07.06 (Pre Classic 2026) = 4th all-time US HS outdoor; 2026 USA U20 1500 2nd
(4:07.99); 2026 World U20 1500 (Eugene) 5th (4:22.60); no HS national records (Oregon state records). Tuohy: 4 NCAA individual titles
(NC State), turned pro with adidas Dec 2023. NIL numbers are the owner's own estimates."""
import json, re, os, sys, glob, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
PH = f'{SP}/elly/ph'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*,]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'


def P(key):
    f = sorted(glob.glob(f'{PH}/*{key}*.jpg'))
    if not f: sys.exit(f'photo missing: {key}')
    return f[0]


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*,]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def FRZ(name, src, dur, pick, focus=(0.5, 0.5), push=1.08):
    out = f'{SP}/elly/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
    spec = {'src': src, 'ss': 0, 'out': out, 'dur': round(dur + 0.6, 2), 'pick': pick, 'focus': list(focus), 'push': push}
    js = out[:-4] + '.json'
    if not (os.path.exists(out) and os.path.exists(js) and json.load(open(js)) == spec):
        json.dump(spec, open(js, 'w')); subprocess.run(['python3', f'{H}/../../editor/freeze.py', js], check=True)
    return out


END = round(W[-1]['e'] + 1.8, 2)
full = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': [fx, fy]}, **k}
split = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_idiot, t_ellery, t_junior, t_instead = at('most idiotic'), at('now ellery'), at("she's like a"), at('and instead of')
t_decided, t_rush, t_football, t_bball, t_track = at('she decided'), at("she's rushing"), at('now i could'), at('or basketball'), at('but for track')
t_foolish2, t_tuohy, t_disappear, t_why = at('this is foolish'), at('we always see'), at('just disappear'), at('so why expedite')
t_maybe, t_u20, t_trials, t_worlds, t_win2 = at('maybe'), at('i saw that'), at("she didn't even win the"), at('she went to the under 20 world'), at("she didn't even win that")
t_fastest, t_records, t_champ, t_exp, t_burn = at("she's one of"), at("so she ain't got"), at("she ain't the"), at("but she's expediting"), at('burn out')
t_dont, t_wrong, t_luck = at("i don't get it"), at('i could be'), at('good luck to her')

TUOHY, TUOHY_YEE = P('Tuohy_at_the_2025'), P('Tuohy_and_Regan_Yee')
segs = [
    split(0.0, R('photo4'), 0.5, 0.18),                               # RunnerSpace headline: forgoing final HS season
    split(t_ellery - 0.05, R('photo2'), 0.5, 0.3),                   # Lincoln in Oregon kit
    split(t_instead - 0.05, R('photo1'), 0.6, 0.45),                 # flags at Hayward
    split(t_rush - 0.05, R('photo3'), 0.4, 0.5),                     # racing
    split(t_football - 0.05, P('Hayward_Field'), 0.5, 0.5),          # NIL: football / basketball / track
    split(t_track - 0.05, R('photo4'), 0.5, 0.18),
    full(t_tuohy - 0.05, TUOHY, 0.5, 0.3, hit=True),   # Tuohy (runners overlap, so no pop-out)
    full(t_why - 0.05, TUOHY_YEE, 0.62, 0.45),
    split(t_u20 - 0.05, R('photo3'), 0.55, 0.5),                     # the U20s
    split(t_fastest - 0.05, R('photo1'), 0.65, 0.45),
    split(t_exp - 0.05, R('photo2'), 0.5, 0.5),
    split(t_dont - 0.05, R('photo4'), 0.5, 0.18),
    split(t_decided - 0.05, R('photo3'), 0.75, 0.45),
    split(t_bball - 0.05, R('photo1'), 0.3, 0.45),
    split(t_worlds - 0.05, R('photo2'), 0.5, 0.15),
    split(t_champ - 0.05, R('photo3'), 0.2, 0.5),
    split(t_luck + 3.0, R('photo2'), 0.5, 0.25),
]

gfx = [
    M('keyword', 0.15, 2.4, text='LEAVING HIGH SCHOOL EARLY'),
    M('slam', t_idiot - 0.1, 1.4, text='MOST IDIOTIC?', hi=1, anchor='upper'),
    D('counter', t_junior, 2.4, value='17', unit='YEARS OLD', label='Ellery Lincoln', sub='enrolling early at Oregon'),
    M('keyword', t_instead + 1.5, 2.6, text='SKIPPING HER LAST HS SEASON'),
    M('slam', t_rush + 0.3, 1.5, text='RUSHING THE PROCESS', hi=1, anchor='upper'),
    M('board', t_football + 0.6, t_track - t_football + 0.6, title='NIL MONEY (HIS ESTIMATE)',
      rows=[{'event': 'FOOTBALL', 'value': '$3–4M'}, {'event': 'BASKETBALL', 'value': '$600–700K'}, {'event': 'TRACK', 'value': '???'}],
      times=[at('three,') - t_football - 0.6, at('600,') - t_football - 0.6, t_track - t_football - 0.3]),
    M('slam', t_foolish2 - 0.2, 1.4, text='FOOLISH', hi=0),
    M('board', t_tuohy + 2.4, 3.6, title='KATELYN TUOHY · NC STATE', rows=[{'event': 'NCAA TITLES', 'value': '4'}, {'event': 'TURNED PRO', 'value': 'DEC 2023'}],
      times=[0.3, 1.2]),
    M('keyword', t_disappear - 0.1, 1.5, text='THEN DISAPPEAR?'),
    M('slam', t_why + 0.1, 1.6, text='WHY EXPEDITE?', hi=1),
    M('board', t_trials - 0.2, t_fastest - t_trials, title='ELLERY · 2026 · 1500M',
      rows=[{'event': 'USA U20 CHAMPS', 'value': '2ND'}, {'event': 'WORLD U20 (EUGENE)', 'value': '5TH'}],
      times=[0.4, t_win2 - t_trials + 0.4]),
    M('board', t_fastest + 0.6, t_exp - t_fastest - 0.6, title='HER HS BEST · 1500M',
      rows=[{'event': '4:07.06 · ALL-TIME HS', 'value': '#4'}, {'event': 'HS NATIONAL RECORD', 'value': 'NO'}],
      times=[0.4, t_records - t_fastest - 0.2]),
    M('slam', t_burn - 0.3, 1.6, text='BURN OUT FASTER?', hi=1, anchor='upper'),
    M('keyword', t_wrong + 1.0, 1.6, text='USUALLY NEVER WRONG'),
    M('poll', t_luck - 0.2, END - t_luck + 0.2, question='SHOULD SHE HAVE STAYED IN HIGH SCHOOL?', options=['YES', 'NO']),
]
zooms = [[t_idiot - 0.2, t_idiot + 1.2, 1.1], [t_why - 0.1, t_why + 1.3, 1.1], [t_dont - 0.1, t_dont + 1.2, 1.1], [t_luck + 4.4, t_luck + 5.6, 1.12]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/elly/build', 'output': f'{SP}/elly/out/ellery_lincoln_v2.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
