"""Jane Hedengren take (~1:08): owner's talking head (4K, tightened) + Commons/Wikipedia photos of Hedengren (BYU 2025 regional,
4696x7041: full-screen; Arcadia 2025, 1600x1124: split) + Lemngole at Zurich 2026 (Commons, vertical: full-screen) + owner's 3 photos
(photo2 1206 short side: split; photo1/photo3 under 1080p -> 2x FSRCNN upscale, split only).
Facts (NOTES.md): 2025 NCAA XC: 1 Lemngole 18:25.4, 2 Hedengren 18:38.9, 3 Olemomoi 18:46.4. Hedengren freshman: NCAA indoor 3K + 5K
champion (Mar 2026), NCAA outdoor 10K 3rd, 5K 9th (Lemngole DQ'd). Fall 2026: Big 12 XC champ (19:28.0, Oct 31); T&FN preseason #1.
Lemngole has moved to the pro ranks (T&FN 2026 preview). HS national records: 5000 14:57.93, 2 mile 9:17.75, mile 4:23.50."""
import json, re, os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*]", '', x['w'].lower()).rstrip('.,').strip("'") for x in W]
R = lambda n: f'{H}/raw/{n}.jpg'
DL1 = R('dl_01') if os.path.exists(R('dl_01')) else None
DL2 = R('dl_01c') if os.path.exists(R('dl_01c')) else DL1


def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*]", '', q).rstrip('.,').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def FRZ(name, src, dur, pick, focus=(0.5, 0.5), push=1.08, keep_x=None, glow=None):
    out = f'{SP}/new1/frz/{name}.mp4'; os.makedirs(os.path.dirname(out), exist_ok=True)
    spec = {'src': src, 'ss': 0, 'out': out, 'dur': round(dur + 0.6, 2), 'pick': pick, 'focus': list(focus), 'push': push,
            **({'keep_x': keep_x} if keep_x else {}), **({'glow': glow} if glow else {})}
    js = out[:-4] + '.json'
    if not (os.path.exists(out) and os.path.exists(js) and json.load(open(js)) == spec):
        json.dump(spec, open(js, 'w')); subprocess.run(['python3', f'{H}/../../editor/freeze.py', js], check=True)
    return out


END = round(W[-1]['e'] + 1.8, 2)
full = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': [fx, fy]}, **k}
split = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

t_paid, t_nats, t_last, t_belt, t_only, t_dq = at("i haven't"), at('nationals'), at('remember last year'), at('belt after'), at('the only way'), at("dq'd")
t_couldnot, t_ten, t_second, t_third, t_isnt = at('like she just'), at('ten times'), at('but jane would'), at('far -ass third'), at('i know that doris')
t_top, t_winning, t_byu, t_hs, t_fresh, t_kenny = at("so it's like"), at('like if she'), at('i know byu'), at('but jane she'), at('she was really good her'), at('like kenny')
t_time, t_record, t_gone = at('but this should'), at('record -breaking'), at('the top people')

segs = [
    full(0.0, FRZ('jane_hook', R('jh_byu'), t_paid - 0.05, [0.55, 0.45]), 0.55, 0.45, hit=True),   # hook: Jane pops out of her regional race
    split(t_paid - 0.05, R('photo2'), 0.5, 0.3),                       # BYU portrait
    split(t_nats - 0.3, R('photo1_2x'), 0.35, 0.3),
    (full(t_last - 0.05, FRZ('doris_intro', DL1, t_only - t_last, [0.62, 0.4], glow=[232, 35, 30]), 0.5, 0.45, hit=True)
     if DL1 else split(t_last - 0.05, R('jh_arcadia'), 0.5, 0.4)),     # Doris from Alabama: freeze pop-out (red glow = the rival)
    split(t_only - 0.05, R('jh_arcadia'), 0.45, 0.4),
    split(t_couldnot - 0.05, R('photo3_2x'), 0.55, 0.4),
    split(t_second - 0.05, R('photo1_2x'), 0.3, 0.35),                 # NCAA XC 2025 results board
    (full(t_isnt - 0.05, DL2, 0.5, 0.3) if DL2 else split(t_isnt - 0.05, R('photo2'), 0.5, 0.4)),   # Doris isn't there: gone pro
    full(t_top - 0.05, R('jh_byu_face'), 0.5, 0.4, hit=True),          # Jane the top runner now
    split(t_winning + 0.4, R('photo3_2x'), 0.45, 0.4),
    split(t_byu - 0.05, R('photo2'), 0.5, 0.25),
    split(t_hs - 0.05, R('jh_arcadia'), 0.6, 0.4),                     # high school: Arcadia 2025
    split(t_fresh - 0.05, R('photo1_2x'), 0.4, 0.3),
    full(t_time - 0.05, R('jh_byu'), 0.62, 0.3),                    # her time
]

gfx = [
    M('keyword', 0.2, 2.6, text='BEST IN COLLEGE?'),
    M('keyword', t_nats + 0.2, 2.2, text='NCAA XC NATIONALS'),
    M('slam', t_belt - 0.1, 1.8, text='BELT AFTER BELT', hi=0, anchor='upper'),
    M('keyword', t_only + 1.0, 2.6, text="ONLY IF DORIS GOT DQ'D"),
    M('slam', t_couldnot + 0.4, 1.6, text='COULD NOT BEAT HER', hi=2, anchor='upper'),
    M('board', t_second, t_isnt - t_second - 0.1, title='2025 NCAA XC · 6K',
      rows=[{'event': '1 · LEMNGOLE', 'value': '18:25.4'}, {'event': '2 · HEDENGREN', 'value': '18:38.9'}, {'event': '3 · OLEMOMOI', 'value': '18:46.4'}],
      times=[0.3, at('second', 1) - t_second + 0.1, t_third - t_second + 0.1]),
    M('keyword', t_isnt + 0.8, 2.6, text='DORIS: PRO NOW'),
    M('slam', t_top + 1.6, 1.6, text='TOP RUNNER NOW', hi=0, anchor='upper'),
    M('board', t_winning + 0.5, t_byu - t_winning - 0.4, title='JANE · FALL 2026',
      rows=[{'event': 'T&FN PRESEASON', 'value': '#1'}, {'event': 'BIG 12 XC', 'value': '1ST'}], times=[0.3, 1.6]),
    M('keyword', t_byu + 0.6, 2.4, text='50-YEAR-OLD RUNNERS?'),
    M('board', t_hs + 0.6, t_fresh - t_hs - 0.4, title='HS NATIONAL RECORDS',
      rows=[{'event': '5000M', 'value': '14:57.93'}, {'event': '2 MILE', 'value': '9:17.75'}, {'event': 'MILE', 'value': '4:23.50'}], times=[0.2, 0.9, 1.6]),
    M('board', t_fresh + 0.4, t_time - t_fresh - 0.2, title='HER FRESHMAN YEAR',
      rows=[{'event': 'NCAA INDOOR 3K', 'value': '1ST'}, {'event': 'NCAA INDOOR 5K', 'value': '1ST'}, {'event': 'NCAA XC', 'value': '2ND'}],
      times=[0.3, 1.0, t_kenny - t_fresh - 1.4]),
    M('slam', t_record - 0.3, 1.5, text='HER TIME', hi=1, anchor='upper'),
    M('poll', t_gone - 0.2, END - t_gone + 0.2, question='CAN ANYBODY BEAT JANE THIS YEAR?', options=['YES', 'NO']),
]
zooms = [[t_only - 0.1, t_only + 1.3, 1.1], [t_ten - 0.1, t_ten + 1.2, 1.1], [t_byu - 0.1, t_byu + 1.3, 1.08]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/new1/build', 'output': f'{SP}/new1/out/jane_hedengren_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}; doris photos: {bool(DL1)}")
