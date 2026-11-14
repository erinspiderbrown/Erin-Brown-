"""Maddox Krotzer high jump take (~1:08): owner's talking head (4K, tightened) + his clip of the jump (638x1080, below the 1080p rule:
2x neural upscale, split only) + his 4 photos of Krotzer (1206 px wide: split only). B-roll is only the subject (owner, Nov 13).
Facts (NOTES.md): indoor PR 7-4.5 on 13 Nov 2026 (MileSplit); outdoor PR 7-4.25 NC state record (11 Apr 2026); 2026 World U20 HJ 4th
(2.17); T&FN 2026 HS All-America #1 HJ; class of 2027, committed to Georgia."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'
CLIP = f'{H}/raw/jump_clip_2x.mp4'


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


END = round(W[-1]['e'] + 1.8, 2)
split = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_business, t_madman, t_thanks, t_so = at('no business'), at('madman'), at("it ain't even"), at('so, you know')
t_college, t_marks, t_but, t_opens, t_like74 = at('i just really'), at('jump 7-3'), at('but as a'), at('he opens up'), at('like 7-4')
t_d1, t_teammate, t_ncaa, t_whole, t_gg, t_fight, t_daddy = at("i'd have been"), at("i ain't never"), at("it's rarely"), at('so for him'), at("it's gg's"), at('we just fight'), at('cuz daddy')

segs = [
    split(0.0, R('photo1'), 0, 0.45, 0.3),                         # clearing the bar at Hayward
    split(4.8, R('photo4'), 0, 0.55, 0.3),
    split(t_madman - 0.3, R('photo2'), 0, 0.5, 0.3),              # portrait
    split(t_thanks - 0.05, R('photo3'), 0, 0.55, 0.45),           # media day
    split(t_college - 0.05, R('photo1'), 0, 0.5, 0.55),
    split(t_marks - 0.05, R('photo2'), 0, 0.5, 0.55),
    split(t_but - 0.05, CLIP, 1.0, 0.5, 0.45),                     # season opener: approach + clearance lands on "like 7-4"
    split(t_d1 - 0.05, CLIP, 14.5, 0.5, 0.3),                      # celebrating
    split(t_ncaa - 0.05, R('photo4'), 0, 0.55, 0.45),
    split(t_whole - 0.05, R('photo1'), 0, 0.45, 0.45),
    split(t_gg - 0.05, R('photo4'), 0, 0.5, 0.55),
    split(t_daddy - 1.0, R('photo2'), 0, 0.5, 0.45),
]

gfx = [
    M('keyword', 0.2, 2.2, text='FIELD EVENTS?'),
    M('slam', t_business - 0.2, 1.5, text='NO BUSINESS DOING', hi=2, anchor='upper'),
    M('keyword', t_madman + 0.1, 1.6, text='MADMAN MADDOX'),
    M('keyword', t_thanks + 0.6, 2.2, text='BEFORE THANKSGIVING'),
    M('board', t_marks - 0.1, t_but - t_marks + 0.1, title='THOSE MARKS IN METERS',
      rows=[{'event': '7-3', 'value': '2.21 M'}, {'event': '7-4', 'value': '2.24 M'}, {'event': '7-5', 'value': '2.26 M'}],
      times=[0.1, at('7-4') - t_marks + 0.1, at('7-5') - t_marks + 0.1]),
    M('keyword', t_but + 1.4, 1.8, text='SEASON OPENER'),
    M('slam', t_opens + 0.9, 1.6, text='7-4½ INDOORS', hi=0, anchor='upper'),
    M('keyword', t_d1 + 0.6, 2.0, text='2 D1 TEAMS'),
    M('keyword', t_ncaa + 0.5, 2.6, text='RARE EVEN IN THE NCAA'),
    M('board', t_whole - 0.1, t_gg - t_whole + 0.2, title='MADDOX KROTZER',
      rows=[{'event': '2026 WORLD U20', 'value': '4TH'}, {'event': 'T&FN HS ALL-AMERICA', 'value': '#1'}, {'event': 'COMMITTED', 'value': 'GEORGIA'}],
      times=[0.3, 1.8, 3.4]),
    M('slam', t_gg + 0.5, 1.4, text='GG', hi=0),
    M('keyword', t_fight + 0.2, 1.8, text='FIGHT FOR 2ND'),
    M('poll', t_daddy - 0.6, END - t_daddy + 0.6, question='CAN ANYBODY BEAT HIM?', options=['YES', 'NO']),
]
zooms = [[t_business - 0.2, t_business + 1.2, 1.1], [t_like74 - 0.2, t_like74 + 1.2, 1.12], [t_gg - 0.1, t_gg + 1.2, 1.1]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/mdx/build', 'output': f'{SP}/mdx/out/maddox_krotzer_v2.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments; {len(gfx)} graphics; END {END}")
