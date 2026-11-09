"""Gift Bright TikTok (~1:13): the owner's talking head (4K, cropped to 1440x1280, tightened) + his vertical Olympics clip of
the Dakar 2026 boys' 100m final + his 3 photos of Bright + Commons photos for the "Africa will dominate" open.
Yohan Blake method: hook full-screen, a graphic on almost every beat, full-screen at each turn, poll at the end.
Facts (checked, see NOTES.md): 10.28 (+1.7) Youth Olympic 100m gold, Dakar, 8 Nov 2026 (Zhang Hangyu CHN 10.57, Szymon Dolega POL 10.61),
first Nigerian to win the boys' 100m at the YOG; 200m PB 20.72 (4 Jul 2026); born 20 Dec 2010."""
import json, re, os, sys, glob
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad'
PH = f'{SP}/brph/ph'
W = json.load(open(f'{H}/work/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-]", '', x['w'].lower()).rstrip('.,').strip("'") for x in W]
CLIP = f'{H}/raw/broll_bright_gold.mp4'
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


END = round(W[-1]['e'] + 0.9, 2)
full = lambda t, src, ss=0, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
split = lambda t, src, ss=0, fx=0.5, fy=0.45, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': ss, 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
N = lambda t, dur, rank, name, sub: {'type': 'name', 't': round(t, 2), 'dur': dur, 'rank': rank, 'name': name, 'sub': sub}

t_now, t_bold, t_dom = at('now i made'), at('bold prediction'), at('i fully expect')
t_nig, t_bot, t_sa, t_mor, t_alg = at('nigeria'), at('botswana'), at('south africa'), at('morocco'), at('algeria')
t_rise, t_young, t_abund, t_quick = at("that's what i expect"), at('young talent'), at('abundance'), at("it's just coming up")
t_yog, t_15, t_named = at('but at the youth'), at('a 15 year old'), at('named gift bright')
t_shine, t_last, t_step, t_drop = at('and let me just'), at('see last year'), at('this year he'), at('he just dropped')
t_run, t_won, t_endur, t_200 = at("so he's running"), at('won the youth'), at('and he also has'), at('he ran 20.7')
t_fresh, t_hs, t_already, t_sky, t_rate, t_2028 = at('so for a 15'), at('freshman'), at("he's running 10.2", 2), at("so the sky's"), at('if you look'), at("ain't no telling")

segs = [
    full(0.0, CLIP, 22.6, 0.5, 0.45),                              # hook: Bright holding up his BRIGHT bib (his clip, vertical 1080x1920)
    split(t_now, P('4_100_metres_relay_final'), 0, 0.5, 0.4),       # bold prediction: Paris 2024 4x100 final
    full(t_dom - 0.05, P('Tebogo_JO'), 0, 0.5, 0.3, hit=True),     # Africa to dominate: Tebogo, Paris 2024
    split(t_nig - 0.05, CLIP, 19.4, 0.5, 0.55),                     # Nigeria: NIGERIA vest (his clip)
    split(t_bot - 0.05, P('Douala_17'), 0, 0.5, 0.35),              # Botswana (2024 African Championships)
    split(t_sa - 0.05, P('ISTAF_2019_100_m_men'), 0, 0.5, 0.4),     # South Africa (Simbine) ... through Morocco, Algeria
    full(t_rise - 0.05, P('press_conf'), 0, 0.5, 0.3),             # "I see their rise": Tebogo
    split(t_abund - 0.25, CLIP, 5.0, 0.5, 0.6),                     # young talent: the Dakar youth final
    full(t_yog - 0.05, CLIP, 0.0, 0.5, 0.45, hit=True),            # the race
    full(t_shine - 0.05, CLIP, 15.6, 0.5, 0.4),                    # bib / celebration
    split(t_last - 0.05, R('photo_sign'), 0, 0.5, 0.4),
    split(t_step - 0.05, R('photo_flag'), 0, 0.5, 0.4),
    full(t_drop - 0.05, CLIP, 12.6, 0.5, 0.45, hit=True),          # lands on the finish line as he says 10.28
    split(t_run - 0.05, R('photo_finish'), 0, 0.5, 0.35),
    full(t_endur - 0.05, CLIP, 16.8, 0.5, 0.4),
    split(t_fresh - 0.05, CLIP, 13.6, 0.5, 0.75),                   # finish line + clock
    full(t_already - 0.05, CLIP, 4.0, 0.5, 0.45),
    split(t_sky - 0.05, CLIP, 21.5, 0.5, 0.4),
    split(t_2028 - 0.05, P('Tebogo_JO'), 0, 0.5, 0.3),
]

gfx = [
    M('keyword', 0.15, 2.0, text='AFRICA, WE SEE YOU'),
    M('stamp', t_bold + 0.1, 1.5, text='BOLD PREDICTION', size=100, anchor='upper'),
    M('keyword', at('2028,') + 0.05, 1.5, text='LA 2028'),
    N(t_dom + 0.1, 2.6, 'BOT', 'LETSILE TEBOGO', 'OLYMPIC 200M CHAMPION · PARIS 2024'),
    M('board', t_nig - 0.1, t_rise - t_nig - 0.1, title='AFRICA RISING',
      rows=[{'event': 'NIGERIA', 'value': 'AMUSAN'}, {'event': 'BOTSWANA', 'value': 'TEBOGO'}, {'event': 'SOUTH AFRICA', 'value': 'SIMBINE'},
            {'event': 'MOROCCO', 'value': 'EL BAKKALI'}, {'event': 'ALGERIA', 'value': 'SEDJATI'}],
      times=[0.1, t_bot - t_nig + 0.1, t_sa - t_nig + 0.1, t_mor - t_nig + 0.1, t_alg - t_nig + 0.1]),
    M('keyword', t_rise + 0.9, 1.6, text='THE RISE'),
    M('keyword', t_young + 0.05, 1.8, text='YOUNG TALENT'),
    M('stamp', t_abund + 0.05, 1.4, text='ABUNDANCE', anchor='lower'),
    M('keyword', t_quick + 0.3, 1.2, text='COMING UP QUICK'),
    M('pin', t_yog + 0.3, 2.4, text='YOUTH OLYMPICS', sub='DAKAR, SENEGAL · NOV 2026'),
    N(t_15 + 0.1, 3.2, 'NGR', 'GIFT BRIGHT', 'AGE 15 · 100M / 200M'),
    M('keyword', t_shine + 1.1, 1.6, text='SHINES BRIGHT'),
    M('keyword', t_last + 0.4, 1.6, text='LAST YEAR: AGE 14'),
    M('stamp', t_step + 0.6, 1.5, text='LEVEL UP', anchor='upper'),
    M('stopwatch', t_drop + 0.2, 2.3, value='10.28', unit='SECONDS', label='100M PB · YOUTH OLYMPIC FINAL', anim=1.0),
    D('bars', t_run + 0.15, 3.3, label="Dakar 2026 · Boys' 100m Final", unit='S', lower_is_better=True, spread=0.4,
      items=[{'name': '1 · Bright (NGR)', 'value': '10.28'}, {'name': '2 · Zhang (CHN)', 'value': '10.57'}, {'name': '3 · Dolega (POL)', 'value': '10.61'}]),
    M('stamp', t_won + 0.1, 1.5, text='1ST NIGERIAN EVER', size=110, anchor='upper'),
    M('keyword', t_endur + 0.5, 1.4, text='SPEED ENDURANCE'),
    M('stopwatch', t_200 + 0.2, 2.4, value='20.72', unit='SECONDS', label='200M PB · JULY 2026', anim=1.0),
    M('keyword', t_hs - 0.1, 1.15, text='HS FRESHMAN'),
    M('board', t_already - 0.05, 2.6, title='GIFT BRIGHT · AGE 15',
      rows=[{'event': '100M', 'value': '10.28'}, {'event': '200M', 'value': '20.72'}], times=[0.1, 0.9]),
    M('keyword', t_sky + 0.3, 1.3, text="SKY'S THE LIMIT"),
    M('poll', t_2028 - 0.2, END - t_2028 + 0.2, question='AFRICA RUNS LA 2028?', options=['YES', 'NO']),
]
zooms = [[t_bold - 0.1, t_bold + 1.4, 1.1], [t_quick, t_quick + 1.4, 1.08], [t_fresh, t_fresh + 1.6, 1.1], [t_sky, t_sky + 1.3, 1.12]]

segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
plan = {'workdir': f'{SP}/brt/build', 'output': f'{SP}/brt/out/gift_bright_v2.mp4', 'words': f'{H}/work/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/face_tight.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.2: print('SHORT', a['start'], b['start'])
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
