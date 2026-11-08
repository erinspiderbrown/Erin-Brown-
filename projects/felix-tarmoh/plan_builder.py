"""Felix vs Tarmoh TikTok (6:48 + poll), cut from the owner's 2024 YouTube video with his ORIGINAL voice and footage.
The source (raw/source.mp4, 1920x1080) plays in sync in a framed 4:3 middle band; real stills from the same video fill the panels.
The voice rides on a hidden carrier track (face.mov) built from voice_cut.wav. Facts: NOTES.md."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad/ft'
W = json.load(open(f'{H}/words_final.json')); CM = json.load(open(f'{H}/cut_map.json'))
TOK = [re.sub(r"[^a-z0-9.'\-]", '', x['w'].lower()).rstrip('.').strip("'") for x in W]
VOICE_END = W[-1]['e']; DUR = round(VOICE_END + 3.0, 2)
SRC = f'{H}/raw/source.mp4'; ST = lambda n: f'{H}/stills/{n}.jpg'
HAYWARD = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad/pre/ph/Hayward_Field_6_4_11.jpg'


def at(phrase, n=1, after=0.0):
    p = [re.sub(r"[^a-z0-9.'\-]", '', q).rstrip('.').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if W[i]['s'] < after: continue
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def src_t(t):      # new timeline -> source time
    r = [c for c in CM if c['new'] <= t + 1e-6][-1]
    return r['src'] + (t - r['new'])


def range_end(t):  # end of the kept range containing t (new timeline)
    i = [k for k, c in enumerate(CM) if c['new'] <= t + 1e-6][-1]
    return CM[i + 1]['new'] if i + 1 < len(CM) else VOICE_END + 3.0


BAND = [1440, 1080, 240, 0]          # 4:3 centre of the 1920x1080 source, shown at native sharpness
def band(t, top, bot, tf=(0.5, 0.5), bf=(0.5, 0.5), **kw):
    return {'type': 'full', 'start': round(t, 2), 'broll': {'src': SRC, 'ss': round(src_t(t), 3), 'fit': 'frame', 'crop': BAND,
            'top': {'src': ST(top) if '/' not in top else top, 'focus': list(tf)}, 'bottom': {'src': ST(bot) if '/' not in bot else bot, 'focus': list(bf)}}, **kw}
def full(t, src, foc=(0.5, 0.5), **kw): return {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': list(foc)}, **kw}


segs = [
    # cold open: Tarmoh (podcast)
    band(0.0, 'hug', 'finish', (0.5, 0.3), (0.5, 0.55)),
    band(at("meaning she's"), 'tarmoh_pod', 'felix_lap', (0.6, 0.3), (0.55, 0.3)),
    # the race
    full(at('in 2012 at the'), HAYWARD, (0.45, 0.5), hit=True),
    band(at('competed in the 100'), 'race2', 'felix_lap', (0.5, 0.6), (0.55, 0.3)),
    band(at('the top three'), 'race', 'race2', (0.5, 0.6), (0.5, 0.6)),
    band(at('the race ended'), 'finish', 'finish2', (0.5, 0.55), (0.5, 0.45)),
    band(at('carmelita jeter'), 'race2', 'felix_lap', (0.5, 0.6), (0.55, 0.3)),
    band(at('after the timer'), 'finish2', 'tarmoh_lap', (0.5, 0.5), (0.5, 0.35)),
    band(at('this seemed to'), 'tarmoh_lap', 'hug', (0.5, 0.3), (0.5, 0.3)),
    band(at('however things took'), 'finish', 'geer', (0.5, 0.5), (0.5, 0.35), hit=True),
    # USATF announcement
    band(at('we have an announcement'), 'geer', 'finish2', (0.5, 0.35), (0.5, 0.5)),
    band(at('in short'), 'finish', 'tarmoh_lap', (0.5, 0.5), (0.5, 0.35)),
    # golden girl / the move
    band(at('leading up into'), 'felix_lap', 'race', (0.55, 0.3), (0.5, 0.6)),
    band(at('the incident painted'), 'hug', 'felix_lap', (0.5, 0.3), (0.55, 0.3)),
    band(at('some saw her'), 'felix_lap', 'race2', (0.55, 0.3), (0.5, 0.6)),
    band(at("felix's desire"), 'race', 'tarmoh_lap', (0.5, 0.6), (0.5, 0.35)),
    band(at('tarmoh was left'), 'tarmoh_lap', 'hug', (0.5, 0.35), (0.5, 0.3)),
    # Tarmoh, ESPN
    band(at('well you know'), 'tarmoh_espn', 'hug', (0.55, 0.4), (0.5, 0.3)),
    band(at('and i said i feel'), 'tarmoh_lap', 'tarmoh_espn2', (0.5, 0.35), (0.55, 0.4)),
    band(at('i felt like if i did'), 'finish', 'tarmoh_espn', (0.5, 0.5), (0.55, 0.4)),
    band(at('we go into the meeting'), 'geer', 'tarmoh_espn2', (0.5, 0.35), (0.55, 0.4)),
    band(at('and allyson said'), 'felix_lap', 'tarmoh_espn', (0.55, 0.3), (0.55, 0.4)),
    band(at("then that's that's"), 'hug', 'felix_lap', (0.5, 0.3), (0.55, 0.3)),
    band(at('do you feel that'), 'tarmoh_espn2', 'hug', (0.55, 0.4), (0.5, 0.3)),
    # the clout question
    band(at('it seemed like her'), 'felix_lap', 'race', (0.55, 0.3), (0.5, 0.6), hit=True),
    band(at('it raised questions'), 'hug', 'felix_lap', (0.5, 0.3), (0.55, 0.3)),
    band(at("usatf's decision"), 'geer', 'finish2', (0.5, 0.35), (0.5, 0.5)),
    band(at('because everyone knew'), 'finish', 'tarmoh_lap', (0.5, 0.5), (0.5, 0.35)),
    band(at('mind you the moment'), 'tarmoh_pod', 'kersee', (0.6, 0.3), (0.5, 0.4)),
    band(at('and i was told'), 'tarmoh_pod', 'hug', (0.6, 0.3), (0.5, 0.3)),
    # runoff or coin toss
    band(at('to resolve the tie'), 'kersee', 'finish2', (0.5, 0.4), (0.5, 0.5)),
    band(at('the notion of'), 'geer', 'race', (0.5, 0.35), (0.5, 0.6)),
    band(at('delay had only'), 'felix_lap', 'geer', (0.55, 0.3), (0.5, 0.35)),
    band(at('the most damaging'), 'race2', 'felix_lap', (0.5, 0.6), (0.55, 0.3)),
    band(at('tarmoh in contrast'), 'tarmoh_lap', 'tarmoh_espn', (0.5, 0.35), (0.55, 0.4)),
    # harassed, walks away
    band(at('in the time leading'), 'tarmoh_espn2', 'tarmoh_pod', (0.55, 0.4), (0.6, 0.3), hit=True),
    band(at('in the end she'), 'tarmoh_lap', 'finish', (0.5, 0.35), (0.5, 0.5)),
    band(at('she gave up her'), 'hug', 'felix_lap', (0.5, 0.3), (0.55, 0.3)),
    # London
    band(at('felix went on'), 'felix_lap', 'race', (0.55, 0.3), (0.5, 0.6)),
    band(at('she did however'), 'race2', 'felix_lap', (0.5, 0.6), (0.55, 0.3)),
    band(at('tarmoh meanwhile'), 'tarmoh_espn', 'race', (0.55, 0.4), (0.5, 0.6)),
    band(at('and despite running'), 'tarmoh_lap', 'tarmoh_espn2', (0.5, 0.35), (0.55, 0.4)),
    band(at('the 2012 incident'), 'hug', 'geer', (0.5, 0.3), (0.5, 0.35)),
    band(at('be sure to let'), 'hug', 'finish', (0.5, 0.3), (0.5, 0.5)),
]

M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
N = lambda t, dur, rank, name, sub: {'type': 'name', 't': round(t, 2), 'dur': dur, 'rank': rank, 'name': name, 'sub': sub}
t_res = at('carmelita jeter'); t_opt = at('two options'); t_lon = at('felix went on')
gfx = [
    N(0.2, 3.2, 'USA', 'JENEBA TARMOH', 'SPRINTER · 2012 OLYMPIC TEAM'),
    M('stamp', at('blackballed') - .1, 1.4, text='BLACKBALLED', size=110),
    M('keyword', at('she\'s not going to get the money'), 2.2, text='NO MEETS. NO MONEY.'),
    M('pin', at('in 2012 at the') + .3, 2.8, text='HAYWARD FIELD', sub='US OLYMPIC TRIALS · JUNE 23, 2012'),
    M('keyword', at('the top three'), 3.0, text='TOP 3 GO TO LONDON'),
    M('stopwatch', at('identical time of') - .2, 2.6, value='11.068', unit='SECONDS', label='FELIX & TARMOH · BOTH', anim=0.9),
    M('board', t_res - .1, round(at('after the timer') - t_res, 2), title='TRIALS 100M FINAL',
      rows=[{'event': '1 · C. JETER', 'value': '10.92'}, {'event': '2 · T. MADISON', 'value': '10.96'},
            {'event': '3 · J. TARMOH', 'value': '11.068'}, {'event': '3 · A. FELIX', 'value': '11.068'}],
      times=[0.2, round(at('tianna madison') - t_res, 2), round(at('tianna madison') - t_res + .8, 2), round(at('tianna madison') - t_res + 1.2, 2)]),
    M('stamp', at('it was announced that') + .3, 1.6, text='TARMOH 3RD', size=120),
    M('keyword', at('believing she had made'), 2.2, text='SHE MADE THE TEAM… RIGHT?'),
    M('stamp', at('resulted in a tie') - .1, 1.6, text='A TIE?!', size=150),
    N(at('we have an announcement'), 3.0, 'USATF', 'JILL GEER', 'USATF SPOKESPERSON'),
    M('stamp', at('dead heat') - .1, 1.8, text='DEAD HEAT', size=130),
    M('keyword', at('golden girl') - .2, 2.6, text="NIKE'S GOLDEN GIRL"),
    M('keyword', at('painted a different'), 2.4, text='A DIFFERENT PICTURE'),
    M('keyword', at('calculated move'), 2.6, text='CALCULATED MOVE?'),
    M('keyword', at('double in both'), 2.6, text='WANTED THE 100 + 200'),
    M('stamp', at('feeling betrayed') - .1, 1.6, text='BETRAYED', size=130),
    N(at('well you know'), 3.2, 'USA', 'JENEBA TARMOH', 'ON ESPN, 2012'),
    M('keyword', at("i'm not comfortable with the runoff"), 3.4, text='"NOT COMFORTABLE WITH A COIN TOSS"'),
    M('keyword', at('fair and square'), 2.2, text='"FAIR AND SQUARE"'),
    M('keyword', at('victory lap'), 2.4, text='VICTORY LAP. PRESS CONFERENCE.'),
    M('keyword', at("i can't just give up my spot"), 2.4, text='"I CAN\'T JUST GIVE UP MY SPOT"'),
    M('stamp', at('just in shock') - .2, 1.4, text='SHOCKED', size=130),
    M('stamp', at('said one thing') - .1, 2.0, text='SAID ONE THING, DID ANOTHER', size=70),
    M('keyword', at('higher up in nike'), 2.6, text='NIKE CLOUT?'),
    M('stamp', at('opportunist') - .2, 1.6, text='OPPORTUNIST?', size=110),
    M('keyword', at('if the roles were reversed'), 3.0, text='ROLES REVERSED = NO REVIEW?'),
    M('stamp', at("that's politics") - .1, 1.6, text="THAT'S POLITICS", size=100),
    M('stamp', at('blackballed', 2) - .1, 1.4, text='BLACKBALLED', size=110),
    M('board', t_opt - .2, round(at('tarmoh was reluctant') - t_opt + .3, 2), title='USATF TIEBREAK',
      rows=[{'event': 'OPTION 1', 'value': 'RUNOFF'}, {'event': 'OPTION 2', 'value': 'COIN TOSS'}],
      times=[round(at('a runoff between') - t_opt, 2), round(at('or coin toss') - t_opt, 2)]),
    M('stamp', at('absurd') - .2, 1.6, text='FOR THE OLYMPICS?!', size=90),
    M('keyword', at('massive sponsorship'), 2.6, text='MASSIVE NIKE DEAL'),
    M('keyword', at('more marketable'), 2.4, text='MOST MARKETABLE'),
    M('keyword', at('relatively unknown'), 2.0, text='RELATIVELY UNKNOWN'),
    M('stamp', at('harassed and humiliated') - .1, 1.6, text='HARASSED', size=130),
    M('keyword', at('receiving threats'), 2.2, text='THREATS'),
    M('calendar', at('she refused to participate') - .1, 2.8, items=['JUL', '2', '2012'], hi=[1], label='THE RUNOFF NEVER HAPPENED'),
    M('stamp', at('she gave up her spot') + .2, 1.8, text='SPOT GIVEN UP', size=110),
    M('board', t_lon - .1, round(at('tarmoh meanwhile') - t_lon - .1, 2), title='FELIX IN LONDON',
      rows=[{'event': '100M', 'value': '5TH'}, {'event': '200M', 'value': 'GOLD'}, {'event': '4X100 (WR)', 'value': 'GOLD'},
            {'event': '4X400', 'value': 'GOLD'}],
      times=[round(at('did not even medal') - t_lon, 2), round(at('win gold in the 200') - t_lon + .3, 2),
             round(at('4x1') - t_lon, 2) if 'x' else 0, round(at('4x4') - t_lon, 2)]),
    M('keyword', at('despite running the prelims'), 3.0, text='RAN THE 4X100 HEATS (STILL GOT GOLD)'),
    M('stamp', at('replaced in the final') - .1, 1.6, text='LEFT OFF THE FINAL', size=95),
    M('keyword', at('lasting stain'), 2.6, text='A LASTING STAIN'),
    M('poll', at('be sure to let'), round(DUR - at('be sure to let'), 2), question='ALLYSON FELIX: TWO-FACED OR AMBITIOUS?', options=['TWO-FACED', 'AMBITIOUS']),
    # --- extra beats (Yohan pacing: a graphic every ~4-6 s)
    M('keyword', at('high stakes race'), 2.6, text='ONE RACE. ONE SPOT.'),
    M('keyword', at('the race ended'), 2.6, text='PHOTO FINISH'),
    M('stamp', at('felix finishing fourth') + .2, 1.4, text='FELIX 4TH', size=120),
    M('stamp', at('dramatic turn') - .1, 1.4, text='PLOT TWIST', size=120),
    M('keyword', at('this will be posted'), 2.6, text='USATF · THAT SAME NIGHT'),
    M('keyword', at('millions of dollars'), 2.4, text='MILLIONS BEHIND FELIX'),
    M('keyword', at('graciously accepted'), 2.4, text='JUST ACCEPT 4TH?'),
    M('keyword', at('already been announced'), 2.6, text='ALREADY ANNOUNCED 3RD'),
    M('keyword', at('we go into the meeting'), 2.6, text='THE MEETING WITH USATF'),
    M('keyword', at('then you will concede'), 1.6, text='"YOU WILL CONCEDE YOUR SPOT"'),
    M('stamp', at("and allyson said i didn't") + .4, 1.8, text='"I DIDN\'T MEAN THAT"', size=90),
    M('keyword', at('do you feel that'), 3.0, text='BETRAYED… OR MISUNDERSTOOD?'),
    M('keyword', at('felt she had earned'), 2.4, text='SHE EARNED IT?'),
    M('stamp', at('seemed suspicious') - .1, 1.6, text='SUSPICIOUS?', size=120),
    N(at('mind you the moment'), 3.0, 'USA', 'JENEBA TARMOH', 'PODCAST INTERVIEW'),
    M('keyword', at('feeling she had already won'), 2.4, text='SHE ALREADY WON?'),
    M('keyword', at('bending over backwards'), 2.4, text='BENDING OVER BACKWARDS?'),
    M('stamp', at('favoritism was in play') - .1, 1.6, text='FAVORITISM?', size=120),
    M('keyword', at('her family started'), 2.4, text='FAMILY INSULTED'),
    M('keyword', at('tarmoh meanwhile'), 2.6, text='TARMOH: RELAYS ONLY'),
]

A = lambda src, t, end, lufs, fade=1.0: {'src': src, 't': round(t, 2), 'end': round(end, 2), 'lufs': lufs, 'fade': fade}
amb = []     # the owner's source already carries the race/press audio inside his narration; no added beds

PANEL_SWAP = {'hug': 'finish2', 'finish': 'hug', 'finish2': 'race', 'race': 'felix_lap', 'race2': 'tarmoh_lap', 'felix_lap': 'race2',
              'tarmoh_lap': 'tarmoh_espn', 'tarmoh_espn': 'tarmoh_lap', 'tarmoh_espn2': 'hug', 'tarmoh_pod': 'tarmoh_espn2', 'geer': 'finish',
              'kersee': 'geer'}
STARTS = [W[i]['s'] for i in range(len(W)) if i == 0 or W[i - 1]['w'].endswith(('.', '?', '!', ','))]


def split_long(segs, limit=8.0):
    """split any framed segment longer than `limit` at the phrase start nearest its midpoint; the new half gets different panels"""
    out = []; ends = [x['start'] for x in segs[1:]] + [DUR]
    for sg, e in zip(segs, ends):
        out.append(sg); b = sg['broll']
        while b.get('fit') == 'frame' and e - out[-1]['start'] > limit:
            st = out[-1]['start']; mid = st + (e - st) / 2
            cand = [t for t in STARTS if st + 3.0 < t < e - 3.0]
            if not cand: break
            t = min(cand, key=lambda x: abs(x - mid)); prev = out[-1]['broll']
            nm = lambda p: os.path.basename(p['src'])[:-4]
            top, bot = PANEL_SWAP.get(nm(prev['bottom']), 'hug'), PANEL_SWAP.get(nm(prev['top']), 'finish')
            out.append(band(t, top, bot, (0.5, 0.35), (0.5, 0.45)))
    return out


if __name__ == '__main__':
    segs.sort(key=lambda s: s['start']); segs = split_long(segs)
    for a, b in zip(segs, segs[1:]):
        if b['start'] - a['start'] < 1.0: print('SHORT', a['start'], b['start'])
        if b['start'] - a['start'] > 9.0: print(f"LONG {a['start']:.2f} {b['start'] - a['start']:.1f}s")
    files = {s['broll'][k]['src'] for s in segs for k in ('top', 'bottom') if k in s['broll']} | {s['broll']['src'] for s in segs}
    print('segments', len(segs), '| missing files:', sorted(f for f in files if not os.path.exists(f)))
    gfx.sort(key=lambda g: g['t'])
    for a, b in zip(gfx, gfx[1:]):
        if a['t'] + a['dur'] > b['t'] + .05: print(f"OVERLAP {a['t']:.2f}+{a['dur']} {a.get('kind', a.get('type'))} / {b['t']:.2f} {b.get('kind', b.get('type'))} {b.get('text', b.get('name', ''))}")
    print(len(gfx), 'graphics; voice', VOICE_END, 'DUR', DUR)
    plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/felix_tarmoh_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0, 'duration': DUR,
            'face': {'src': f'{SP}/face.mov', 'focus': [0.5, 0.5]}, 'skip_res_check': True, 'segments': segs, 'graphics': gfx, 'ambience': amb}
    json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
