"""Athlete of the Year rant (~1:10): Duplantis top-3 finalist vs Kebinatshipi 7th. Owner's talking head (4K, untightened: the tightened
cut was 60 s, under the 61 s rule) + his 3 World Athletics award graphics (1206 px wide: split only) + Commons photos.
House method with the Nov 2026 step-up: no name tags, slam text, freeze pop-outs on each athlete's first mention.
Facts (checked, NOTES.md): Duplantis' only 2026 WR was 6.31 INDOORS (Uppsala, 12 Mar); outdoor best 6.25 (Zürich); 2026 losses:
Stockholm DL 7 Jun (Marschall), London DL 17 Jul (Kendricks). Kebinatshipi: 2025 world champion 43.53; unbeaten in the 400 in 2026;
43.40 DL record (Brussels), 43.39 PB (Budapest); ranked 7th of 10 nominees."""
import json, re, os, sys, glob, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
PH = f'{SP}/aoty/ph'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-]", '', x['w'].lower()).rstrip('.,').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'


def P(key):
    f = sorted(glob.glob(f'{PH}/*{key}*.jpg'))
    if not f: sys.exit(f'photo missing: {key}')
    return f[0]


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-]", '', q).rstrip('.,').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def FRZ(name, src, dur, pick, focus=(0.5, 0.5), push=1.08):
    out = f'{SP}/aoty/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
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

t_rid, t_mondo, t_top3, t_mind = at("it's ridiculous"), at('mondo duplantis'), at('top three'), at('mind you')
t_nowr, t_indoor, t_out2, t_lost = at('did not break'), at('he broke the'), at('but outdoors'), at('he has lost')
t_but, t_collen, t_last, t_undef = at("but he's top"), at('they have collen'), at('last place'), at('he went undefeated')
t_worlds, t_this, t_dropped, t_7a, t_7b = at('undefeated at the'), at('this year all'), at('dropped some'), at('seventh'), at('seventh place')
t_guy, t_lost2, t_top3b, t_jokes = at('but a guy'), at("who's lost"), at('is top three'), at('certain jokes')

JUMP, PRESS_V, PRESS_L = P('Duplantis_jumping'), P('Pole_rich_athletics_competition_08'), P('Pole_rich_athletics_competition_03')
segs = [
    full(0.0, JUMP, 0.5, 0.3),                                                # hook: Duplantis in the air (Athletissima)
    split(t_rid - 0.05, R('wa_finalists'), 0.5, 0.45),                       # the finalists graphic
    full(t_mondo - 0.05, FRZ('mondo', PRESS_V, t_mind - t_mondo, [0.5, 0.4]), 0.5, 0.5, hit=True),   # Mondo pops out
    split(t_mind - 0.05, PRESS_L, 0.35, 0.4),                                # no outdoor WR
    full(t_indoor - 0.05, JUMP, 0.5, 0.3),
    split(t_lost - 0.05, P('Marschall_at_the_2026_W_sima_athletics_competition_01'), 0.4, 0.45),   # Marschall (beat him in Stockholm)
    split(t_lost + 3.2, PRESS_L, 0.75, 0.4),
    split(t_but - 0.05, R('wa_runnersup'), 0.5, 0.4),                        # runners-up graphic
    full(t_collen - 0.05, FRZ('collen', P('Kebinatshipi_BOT_2025'), t_undef - t_collen, [0.6, 0.45], (0.64, 0.45)), 0.5, 0.5, hit=True),
    split(t_undef - 0.05, P('Championships_Tokyo'), 0.55, 0.45),
    split(t_dropped - 0.05, P('Kebinatshipi_BOT_2025'), 0.5, 0.45),
    split(t_7a - 0.05, R('wa_collen7th'), 0.5, 0.45),                        # the 7th graphic
    full(t_guy - 0.05, PRESS_V, 0.5, 0.4),
    split(t_lost2 - 0.35, P('Marschall_at_the_2026_W_sima_athletics_competition_05'), 0.45, 0.4),
    split(t_top3b - 0.3, R('wa_finalists'), 0.5, 0.35),
]

gfx = [
    M('keyword', 0.2, 2.2, text='WORLD ATHLETICS AWARDS'),
    M('slam', 2.6, 1.3, text='SO BLATANT', hi=1, anchor='upper'),
    M('keyword', t_top3 - 0.1, 1.8, text='TOP 3?'),
    M('board', t_nowr - 0.2, 5.2, title='MONDO · 2026 WORLD RECORDS',
      rows=[{'event': 'INDOOR · UPPSALA', 'value': '6.31 WR'}, {'event': 'OUTDOOR BEST', 'value': '6.25'}],
      times=[t_indoor - t_nowr + 0.4, t_out2 - t_nowr + 0.6]),
    M('board', t_lost - 0.1, 6.0, title='MONDO · 2026 LOSSES',
      rows=[{'event': 'STOCKHOLM · JUN 7', 'value': '2ND'}, {'event': 'LONDON · JUL 17', 'value': '2ND'}],
      times=[0.4, 1.8]),
    M('slam', t_but + 0.4, 1.4, text='STILL TOP 3', hi=1, anchor='upper'),
    M('slam', t_last - 0.4, 1.4, text='DAMN NEAR LAST', hi=2),
    M('board', t_undef - 0.1, t_dropped - t_undef + 0.1, title='COLLEN · 2026 (400M)',
      rows=[{'event': 'DIAMOND LEAGUE', 'value': '6-0'}, {'event': '2025 WORLDS', 'value': 'GOLD'}, {'event': '2026 SEASON', 'value': 'UNBEATEN'}],
      times=[0.3, t_worlds - t_undef + 0.3, t_this - t_undef + 0.3]),
    M('stopwatch', t_dropped + 0.3, 2.6, value='43.39', unit='SECONDS', label='400M PB · BUDAPEST 2026', anim=1.0),
    M('slam', t_7b - 0.1, 1.5, text='7TH PLACE?!', hi=0),
    M('board', t_lost2 - 0.3, 3.6, title='2026, HEAD TO HEAD',
      rows=[{'event': 'COLLEN · 400M', 'value': 'UNBEATEN'}, {'event': 'MONDO · PV', 'value': 'LOST 2'}], times=[0.2, 0.9]),
    M('slam', t_top3b, 1.4, text='TOP 3', hi=1, anchor='upper'),
    M('poll', t_jokes - 0.2, END - t_jokes + 0.2, question='WHO GOT ROBBED?', options=['COLLEN', 'NOBODY']),
]
zooms = [[t_rid - 0.1, t_rid + 1.3, 1.1], [t_but - 0.1, t_but + 1.3, 1.08], [t_7b - 0.2, t_7b + 1.3, 1.12], [t_jokes - 0.2, t_jokes + 1.4, 1.1]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/aoty/build', 'output': f'{SP}/aoty/out/athlete_of_year_v2.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
