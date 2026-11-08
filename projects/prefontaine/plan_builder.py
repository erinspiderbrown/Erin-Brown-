"""Steve Prefontaine (5:29). No talking head: the owner's default ElevenLabs voice rides on a hidden carrier track, every segment is full.
Shots: 4K reenactments full-screen, 1080p reenactments in the framed middle band (with real photos above/below), Commons photos.
Every graphic is anchored to a spoken word. Facts are checked - see NOTES.md."""
import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad/pre'
W = json.load(open(f'{HERE}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-]", '', x['w'].lower()).rstrip('.').strip("'") for x in W]
DUR = round(W[-1]['e'] + 2.4, 2)


def at(phrase, n=1, after=0.0):
    p = [re.sub(r"[^a-z0-9.'\-]", '', q).rstrip('.').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if W[i]['s'] < after: continue
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def ph(title):          # Commons file title -> downloaded file (same naming as get_pre.py)
    base = re.sub(r'[^A-Za-z0-9]+', '_', os.path.splitext(title)[0]).strip('_')
    return f"{SP}/ph/{(base if len(base) <= 60 else base[:30] + '_' + base[-29:])}.jpg"


RE = lambda n: f'{HERE}/reenact/{n}.mp4'
# film-gate crops (cropdetect, inset a little more to clear the rounded corners): [w, h, x, y]
GATE = {'01_mg_night': [2860, 2120, 490, 20], '02_crash_aftermath': [2850, 2120, 498, 20], '03_munich_lead': [3000, 2160, 420, 0],
        '05_hayward_crowd': [2960, 2120, 500, 20], '06_memorial_rock': [3600, 2160, 120, 0], '07_coos_bay': [3020, 2120, 412, 20],
        '08_dawn_trail': [3010, 2120, 409, 20], '09_hs_cinder': [1620, 1050, 204, 15], '10_cross_country': [1500, 1050, 212, 15],
        '11_feet': [1860, 1060, 30, 10], '12_waffle': [1430, 1050, 245, 15], '13_stopwatch': [1430, 1050, 245, 15],
        '14_disappointed': [1426, 1050, 249, 15], '15_officials': [1780, 990, 68, 50], '16_shoes': [1426, 1050, 247, 15],
        '17_prison': [1418, 1050, 251, 15], '18_party': [1420, 980, 252, 52], '19_police': [1418, 1050, 251, 15], '20_tribute': [1430, 1050, 245, 15]}

PRE = ph('Steve Prefontaine, Marty Liquori, and Gianni Del Buono.jpg')      # 1973, LA Times Indoor Games (the one real race photo)
ROCK16 = ph("Pre's Rock in Eugene, Oregon.jpg")
ROCK = lambda n: ph(f'Day 4 at the 2024 United States Olympic Trials (track and field) {n}.jpg')
TRIALS10 = lambda n: ph(f'Day 10 at the 2024 United States Olympic Trials (track and field) {n}.jpg')
ALTON = lambda s='': ph(f'2017-11-25 Alton Baker Park{s}.jpg')
CLASSIC13, CLASSIC = ph('Prefontaine Classic 2013.jpg'), ph('Prefontaine Classic.jpg')
HAYWARD = ph('Hayward Field 6-4-11.JPG')
MURAL = lambda h: ph(f'Mural depicting Steve Prefontaine, Coos Bay - DPLA - {h}.jpg')
M1, M2, M3 = MURAL('1a93e6baa590794d1f4c2fc71486de57'), MURAL('35d4ea3ad7d13887f677a5e705171953'), MURAL('89f5fe4ab73c9d3ce575c130233b101d')
COOS = ph('Coos Bay - DPLA - 6de9a85a20c611d789a179f70fbc4efc.jpg')
PLAQUE = ph('Steve Prefontaine Plaque, Coos Bay - DPLA - 6df7c7762f811e837362874ff6da2760.jpg')
PREROCK = ph('PreRock.jpg')
SUBS = json.load(open(f'{HERE}/photo_subs.json')) if os.path.exists(f'{HERE}/photo_subs.json') else {}


def src_ok(p): return SUBS.get(p, p)


def full(t, src, foc=(0.5, 0.5), ss=0.0, **kw):
    b = {'src': src_ok(src), 'ss': ss, 'focus': list(foc)}
    n = os.path.basename(src)[:-4]
    if src.endswith('.mp4') and n in GATE: b['fullcrop'] = GATE[n]
    return {'type': 'full', 'start': round(t, 2), 'broll': b, **kw}


def frame(t, src, top, bot, tf=(0.5, 0.4), bf=(0.5, 0.45), ss=0.0, **kw):
    n = os.path.basename(src)[:-4]
    b = {'src': src_ok(src), 'ss': ss, 'fit': 'frame', 'top': {'src': src_ok(top), 'focus': list(tf)}, 'bottom': {'src': src_ok(bot), 'focus': list(bf)}}
    if src.endswith('.mp4') and n in GATE: b['crop'] = GATE[n]
    return {'type': 'full', 'start': round(t, 2), 'broll': b, **kw}


PF = (0.43, 0.42)        # Pre in the 1973 photo
T6 = at('after the meet')
segs = [
    # ---- 01 cold open
    full(0.0, RE('01_mg_night'), (0.5, 0.5)),
    full(at('eugene oregon'), ROCK(190), (0.5, 0.5)),
    full(at('a little gold'), RE('01_mg_night'), (0.42, 0.5), ss=2.4),
    full(at('crosses the center'), RE('02_crash_aftermath'), (0.62, 0.5), hit=True),
    full(at('and trapped'), PRE, PF),
    frame(at('he held every'), PRE, ROCK(193), HAYWARD, (0.5, 0.5), (0.5, 0.55)),
    full(at('and just a few'), RE('05_hayward_crowd'), (0.42, 0.5)),
    full(at('this the story'), PRE, (0.44, 0.38)),
    # ---- 02 Coos Bay
    full(at('pre was born'), RE('07_coos_bay'), (0.5, 0.5)),
    frame(at('hardworking people') - .3, COOS, PLAQUE, M1, (0.5, 0.3), (0.5, 0.3)),
    frame(at('at marshfield'), RE('09_hs_cinder'), M1, COOS, (0.5, 0.3), (0.5, 0.45)),
    frame(at('cross country and track'), M1, COOS, PLAQUE, (0.5, 0.45), (0.5, 0.35)),
    frame(at('his senior year'), RE('13_stopwatch'), M1, COOS, (0.5, 0.3), (0.5, 0.45)),
    frame(at('then he ran the two'), RE('11_feet'), PLAQUE, M1, (0.5, 0.45), (0.5, 0.6)),
    full(at('after high school'), HAYWARD, (0.5, 0.5)),
    frame(at('bill bowerman'), RE('12_waffle'), HAYWARD, M2, (0.3, 0.5), (0.5, 0.75)),
    # ---- 03 Oregon
    full(at('and at oregon'), PRE, (0.42, 0.45), hit=True),
    frame(at('seven ncaa'), RE('10_cross_country'), ALTON(), HAYWARD, (0.5, 0.5), (0.6, 0.5)),
    full(at('he was the first'), CLASSIC, (0.5, 0.5)),
    full(at('he never lost'), RE('05_hayward_crowd'), (0.5, 0.5), ss=0.3),
    full(at('in four years'), ALTON(), (0.5, 0.5)),
    frame(at("and it wasn't just"), PRE, CLASSIC13, HAYWARD, (0.5, 0.5), (0.4, 0.5)),
    full(at('he went to the front'), RE('08_dawn_trail'), (0.52, 0.5)),
    full(at('no one will ever'), PRE, (0.45, 0.4)),
    full(at('hayward field would'), CLASSIC13, (0.5, 0.5)),
    # ---- 04 Munich
    full(at('1972 he 21'), RE('03_munich_lead'), (0.5, 0.5)),
    full(at('at the trials'), HAYWARD, (0.35, 0.5)),
    full(at('september 10th'), RE('03_munich_lead'), (0.46, 0.5), ss=0.3),
    full(at("and that ain't"), PRE, (0.44, 0.4)),
    full(at('so with a mile'), RE('03_munich_lead'), (0.55, 0.5), ss=1.0, hit=True),
    frame(at('but lasse'), RE('11_feet'), M3, CLASSIC, (0.5, 0.4), (0.5, 0.5), ss=1.0),
    full(at('virn go by him'), RE('03_munich_lead'), (0.58, 0.5), ss=3.9),
    frame(at('then mohamed'), PRE, CLASSIC13, HAYWARD, (0.5, 0.5), (0.45, 0.5)),
    frame(at('pre finished fourth'), RE('14_disappointed'), M3, PRE, (0.5, 0.35), (0.43, 0.3)),
    full(at('0.8 of a second'), PRE, (0.44, 0.36)),
    # ---- 05 fighting the system
    full(at('so he come back'), RE('08_dawn_trail'), (0.55, 0.5)),
    frame(at('but see back then'), RE('15_officials'), CLASSIC, HAYWARD, (0.5, 0.5), (0.5, 0.5)),
    full(at('if you got paid'), PRE, (0.43, 0.42)),
    frame(at('pre was taking free'), RE('16_shoes'), PRE, ALTON(' 2'), (0.43, 0.6), (0.5, 0.5)),
    frame(at('he went to war'), RE('15_officials'), PRE, CLASSIC13, (0.43, 0.3), (0.5, 0.5), ss=2.5),
    full(at('meanwhile'), RE('05_hayward_crowd'), (0.45, 0.5), hit=True),
    full(at('by 1975'), ALTON(' 2'), (0.5, 0.5)),
    full(at('the 5000', after=at('meanwhile') + 6), CLASSIC, (0.5, 0.5)),
    full(at('the 10000', after=at('meanwhile') + 6), HAYWARD, (0.6, 0.5)),
    frame(at('and here goes'), RE('17_prison'), ALTON(' 3'), PRE, (0.5, 0.5), (0.43, 0.4)),
    frame(at('that prison run'), RE('17_prison'), PRE, ALTON(), (0.45, 0.35), (0.5, 0.5), ss=1.8),
    # ---- 06 the last night
    full(at('may 29'), HAYWARD, (0.45, 0.5)),
    full(at('and he win it'), PRE, (0.42, 0.42)),
    full(at('frank shorter', after=T6 - 20), CLASSIC13, (0.6, 0.5)),
    frame(T6, RE('18_party'), HAYWARD, CLASSIC, (0.5, 0.5), (0.5, 0.5)),
    full(at('right after midnight', after=T6), RE('01_mg_night'), (0.4, 0.5)),
    full(at('then he head home', after=T6), RE('01_mg_night'), (0.58, 0.5), ss=1.4),
    full(at('his mg crossed'), RE('02_crash_aftermath'), (0.66, 0.5), ss=0.5, hit=True),
    frame(at('pre was trapped'), RE('19_police'), ROCK16, ROCK(194), (0.5, 0.45), (0.5, 0.5)),
    full(at('they pronounced'), ROCK16, (0.5, 0.5)),
    # ---- 07 the questions
    frame(at('now this is where'), RE('19_police'), PRE, ROCK(195), (0.43, 0.3), (0.5, 0.5), ss=2.0),
    full(at('the police said'), RE('02_crash_aftermath'), (0.55, 0.5), ss=1.5),
    full(at('back then in oregon'), ROCK(190), (0.5, 0.5)),
    full(at('but his friends'), PRE, (0.44, 0.4)),
    full(at('some of them believe'), RE('01_mg_night'), (0.5, 0.5), ss=1.2),
    full(at('either way'), ROCK(191), (0.5, 0.5)),
    full(at('and he never got'), RE('08_dawn_trail'), (0.6, 0.5), ss=2.0),
    # ---- 08 legacy
    frame(at('they held a meet'), RE('20_tribute'), CLASSIC13, HAYWARD, (0.5, 0.5), (0.5, 0.5)),
    full(at('the prefontaine classic'), CLASSIC13, (0.4, 0.5)),
    full(at('the spot where'), RE('06_memorial_rock'), (0.62, 0.5)),
    full(at('people still leave'), ROCK(196), (0.5, 0.5)),
    full(at('they made two'), PRE, (0.43, 0.45)),
    full(at('nike put his'), ROCK(192), (0.5, 0.5)),
    full(at('24 years old', 3), PRE, (0.44, 0.36), hit=True),
    full(at('one olympic final'), RE('03_munich_lead'), (0.5, 0.5), ss=1.0),
    full(at('and one question'), RE('08_dawn_trail'), (0.5, 0.5), ss=3.0),
    full(at('if pre made it'), PRE, (0.43, 0.42)),
]
segs.sort(key=lambda s: s['start'])
for s_, n_ in zip(segs, segs[1:]):     # a 6 s clip that overruns by <= 1.2 s: pull the next cut earlier rather than freeze
    b_ = s_['broll']
    if b_['src'].endswith('.mp4'):
        over = n_['start'] - s_['start'] + b_['ss'] - 6.0
        if 0 < over <= 1.2: n_['start'] = round(n_['start'] - over, 2)

# ---------------- graphics ----------------
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
N = lambda t, dur, rank, name, sub: {'type': 'name', 't': round(t, 2), 'dur': dur, 'rank': rank, 'name': name, 'sub': sub}
t_rec = at('meanwhile')
gfx = [
    # --- cold open
    M('calendar', at('may 30th') - .1, 2.6, items=['MAY', '30', '1975'], hi=[1], label='JUST AFTER MIDNIGHT'),
    M('pin', at('eugene oregon'), 1.45, text='EUGENE, OREGON', sub='SKYLINE BOULEVARD'),
    M('keyword', at('a little gold'), 2.6, text='GOLD MG CONVERTIBLE'),
    M('stamp', at('flips over') - .1, 1.4, text='FLIPPED', size=130),
    M('keyword', at('the greatest distance'), 2.4, text="AMERICA'S GREATEST?"),
    D('counter', at('24 years old') - .2, 1.7, value='24', unit='YEARS OLD', label='Steve Prefontaine', sub='1951 – 1975'),
    M('keyword', at('he held every'), 3.4, text='EVERY U.S. RECORD · 2K TO 10K'),
    M('stamp', at('he won a race'), 1.6, text='HOURS EARLIER: HE WON', size=90),
    N(at('steve prefontaine') - .2, 3.2, 'USA', 'STEVE PREFONTAINE', '"PRE" · OREGON · OLYMPIAN'),
    # --- Coos Bay
    M('birthday', at('pre was born') + .2, 2.4, text='JAN 25, 1951', name='PRE'),
    M('pin', at('coos bay'), 2.6, text='COOS BAY, OREGON', sub='LOGGING TOWN ON THE COAST'),
    M('keyword', at('at marshfield'), 2.8, text='MARSHFIELD HIGH · COACH WALT McCLURE'),
    M('stamp', at('pre was undefeated') + .2, 1.8, text='UNDEFEATED', size=120),
    M('stopwatch', at('the mile in') + .1, 2.6, value='246.9', format='mss1', unit='MILE', label='OREGON HS RECORD', anim=1.0, size=120),
    M('stopwatch', at('the two mile') + .1, 2.8, value='521.5', format='mss1', unit='2 MILE', label='NATIONAL HS RECORD (REPORTED)', anim=1.0, size=120),
    N(at('bill bowerman') - .2, 3.4, 'ORE', 'BILL BOWERMAN', 'OREGON COACH · NIKE CO-FOUNDER'),
    # --- Oregon
    M('keyword', at('a whole nother') - .2, 1.8, text="A WHOLE 'NOTHER LEVEL"),
    D('counter', at('seven ncaa') - .1, 3.0, value='7', unit='NCAA TITLES', label='3 cross country · 4 track', sub='University of Oregon'),
    M('keyword', at('he was the first'), 3.2, text='FIRST EVER: 4 NCAA TITLES IN ONE EVENT'),
    M('stamp', at('not one'), 1.5, text='NEVER LOST (NCAA, > MILE)', size=80),
    D('counter', at('three times') - .1, 2.6, value='3', unit='LOSSES', label='College races in Eugene', sub='All in the mile'),
    M('keyword', at("pre didn't sit back"), 3.6, text='NO KICK. HE WENT TO THE FRONT.'),
    M('keyword', at('no one will ever') - .1, 4.9, text='"NOT AGAINST ME."'),
    M('pin', at('hayward field would'), 2.6, text='HAYWARD FIELD', sub='"HIS HOUSE"'),
    # --- Munich
    M('pin', at('munich') - .1, 2.4, text='MUNICH 1972', sub='OLYMPIC GAMES · AGE 21'),
    M('stopwatch', at('1322.8') - .9, 2.6, value='802.8', format='mss1', unit='5000M', label='AMERICAN RECORD · OLY TRIALS', anim=0.9, size=120),
    M('calendar', at('september 10th') - .1, 2.2, items=['SEP', '10', '1972'], hi=[1], label='OLYMPIC 5000 FINAL'),
    M('keyword', at('slow real slow'), 2.4, text='SLOW FIRST 2 MILES'),
    M('stamp', at('hard') - .1, 1.2, text='GO!', size=150),
    N(at('but lasse') - .1, 2.8, 'FIN', 'LASSE VIRÉN', 'FINLAND'),
    M('board', at('pre finished fourth') - .2, round(at('0.8 of a second') - at('pre finished fourth') + .05, 2), title='MUNICH 1972 · 5000 FINAL',
      rows=[{'event': '1 · LASSE VIRÉN', 'value': '13:26.4'}, {'event': '2 · M. GAMMOUDI', 'value': '13:27.4'},
            {'event': '3 · IAN STEWART', 'value': '13:27.6'}, {'event': '4 · PREFONTAINE', 'value': '13:28.4'}],
      times=[0.15, 0.4, 0.65, 1.0]),
    M('stamp', at('0.8 of a second') - .1, 1.8, text='0.8 FROM BRONZE', size=95),
    M('keyword', at('he said that was'), 3.2, text='"MOST DISAPPOINTED I HAVE EVER BEEN"'),
    # --- the system / records / prison
    M('pin', at('montreal') - .1, 2.4, text='MONTREAL 1976', sub='THE NEXT OLYMPICS'),
    M('keyword', at('track was supposed'), 2.2, text='"AMATEUR" ONLY'),
    M('flow', at('the aau ran'), round(at('pre was taking free') - at('the aau ran') - .1, 2), items=['GET PAID', 'ENDORSEMENTS', 'LOSE STATUS'],
      times=[0.2, round(at('or got endorsements') - at('the aau ran'), 2), round(at('they could take') - at('the aau ran'), 2)]),
    M('keyword', at('pre was taking free'), 2.6, text='FREE GEAR FROM NIKE'),
    M('stamp', at('he went to war'), 1.6, text='WAR WITH THE AAU', size=95),
    M('board', t_rec + .2, round(at('and here goes') - t_rec - .4, 2), title='AMERICAN RECORDS · BY 1975',
      rows=[{'event': '2,000M → 10,000M', 'value': '7', 'tag': 'ALL OF THEM'}, {'event': '5000M · HELSINKI', 'value': '13:21.9'},
            {'event': '10,000M · EUGENE', 'value': '27:43.6'}],
      times=[round(at('every american record', 2) - t_rec, 2), round(at('13:21.9') - t_rec, 2), round(at('27:43.6') - t_rec, 2)]),
    M('keyword', at('here goes something'), 2.4, text="WHAT PEOPLE DON'T KNOW"),
    M('pin', at('oregon state penitentiary'), 2.6, text='OREGON STATE PENITENTIARY', sub='SALEM'),
    M('stamp', at('still going today'), 1.8, text='STILL RUNNING TODAY', size=90),
    # --- the last night
    M('calendar', at('may 29') - .1, 2.4, items=['MAY', '29', '1975'], hi=[1], label='HAYWARD FIELD · 5000M'),
    M('stopwatch', at('1323.8') - .9, 2.6, value='803.8', format='mss1', unit='5000M', label='WON · HIS LAST RACE', anim=0.9, size=120),
    N(at('frank shorter') - .1, 3.2, 'USA', 'FRANK SHORTER', '1972 OLYMPIC MARATHON CHAMP · 2ND'),
    M('keyword', at('after the meet'), 2.8, text="PARTY · GEOFF HOLLISTER'S"),
    M('keyword', at('right after midnight', after=T6), 3.2, text="DROPS SHORTER AT KENNY MOORE'S"),
    M('pin', at('then he head home', after=T6) + .4, 3.0, text='SKYLINE BLVD', sub='BY HENDRICKS PARK'),
    M('stamp', at('hit a rock wall') - .1, 1.6, text='ROCK WALL', size=120),
    M('keyword', at('pre was trapped'), 2.4, text='TRAPPED UNDERNEATH'),
    D('counter', at('24 years old', 2) - .2, 2.6, value='24', unit='YEARS OLD', label='May 30, 1975', sub='Eugene, Oregon'),
    # --- the questions
    M('stamp', at('get messy') - .3, 1.6, text='MESSY', size=150),
    M('board', at('the police said') + .2, round(at('but his friends') - at('the police said') - .2, 2), title='BLOOD ALCOHOL (POLICE)',
      rows=[{'event': 'REPORTED', 'value': '0.16'}, {'event': 'OREGON LIMIT (1975)', 'value': '0.15'}],
      times=[round(at('0.16') - at('the police said') - .4, 2), round(at('0.15') - at('the police said') - .4, 2)]),
    M('keyword', at('questioning that'), 2.6, text='QUESTIONED FOR 50 YEARS'),
    M('keyword', at('another car'), 1.95, text='ANOTHER CAR?'),
    M('stamp', at('the police ruled'), 1.6, text='RULED OUT', size=120),
    M('keyword', at('never got his shot'), 2.6, text='NO MONTREAL'),
    # --- legacy
    M('keyword', at('they held a meet'), 3.4, text='SUMMER 1975 · A MEET IN HIS HONOR'),
    M('stamp', at('the prefontaine classic') + .1, 1.9, text='PREFONTAINE CLASSIC', size=85),
    M('pin', at("pre's rock"), 1.4, text="PRE'S ROCK", sub='SKYLINE BLVD, EUGENE'),
    M('keyword', at('people still leave'), 2.8, text='BIBS. MEDALS. SHOES.'),
    M('board', at('they made two'), round(at('24 years old', 3) - at('they made two') - .2, 2), title='HIS LEGACY',
      rows=[{'event': 'PREFONTAINE', 'value': '1997', 'tag': 'FILM'}, {'event': 'WITHOUT LIMITS', 'value': '1998', 'tag': 'FILM'},
            {'event': 'NIKE HQ', 'value': 'BUILDING'}],
      times=[round(at('prefontaine in 1997') - at('they made two'), 2), round(at('without limits') - at('they made two'), 2),
             round(at('nike put his') - at('they made two'), 2)]),
    M('keyword', at('every american record', 3), 1.9, text='EVERY U.S. RECORD 2K–10K'),
    M('keyword', at('one olympic final'), 1.6, text='ONE OLYMPIC FINAL'),
    M('keyword', at('and one question') , 2.6, text='ONE QUESTION…'),
    M('poll', at('if pre made it'), round(DUR - at('if pre made it'), 2), question='PRE IN MONTREAL \'76: GOLD?', options=['YES', 'NO']),
]

A = lambda src, t, end, lufs, fade=1.0: {'src': src, 't': round(t, 2), 'end': round(end, 2), 'lufs': lufs, 'fade': fade}
amb = [
    A('stadium_crowd_murmur', at('and just a few') - .3, at('pre was born') - .3, -37, 1.2),
    A('stadium_crowd_murmur', at('and at oregon') - .3, at('1972 he 21') - .2, -36, 1.5),
    A('stadium_cheer', at('hayward field would') - .2, at('hayward field would') + 4.0, -33, 0.6),
    A('stadium_crowd_murmur', at('september 10th') - .3, at('so he come back') - .3, -36, 1.2),
    A('crowd_victory', at('virn go by him') - .2, at('virn go by him') + 4.0, -33, 0.6),
    A('reporters_flashes', at('he went to war') - .2, at('meanwhile') - .2, -36, 0.8),
    A('stadium_crowd_murmur', at('may 29') - .3, at('after the meet'), -36, 1.0),
    A('stadium_cheer', at('and he win it') - .2, at('and he win it') + 3.6, -33, 0.6),
    A('stadium_crowd_murmur', at('they held a meet') - .3, at('the spot where'), -37, 1.2),
]

if __name__ == '__main__':
    segs.sort(key=lambda s: s['start'])
    ends = [s['start'] for s in segs[1:]] + [DUR]
    for s, e in zip(segs, ends):
        b = s['broll']
        if b['src'].endswith('.mp4') and e - s['start'] + b['ss'] > 6.08:
            print(f"CLIP TOO SHORT {s['start']:.2f}->{e:.2f} ({e - s['start']:.2f}s, ss {b['ss']}) {os.path.basename(b['src'])}")
        if e - s['start'] < 1.0: print('SHORT', s['start'], e)
        if e - s['start'] > 8.5: print(f"LONG {s['start']:.2f} {e - s['start']:.1f}s {os.path.basename(b['src'])}")
    files = {s['broll'][k]['src'] for s in segs for k in ('top', 'bottom') if k in s['broll']} | {s['broll']['src'] for s in segs}
    print('segments', len(segs), '| missing files:', sorted(os.path.basename(f) for f in files if not os.path.exists(f)))
    gfx.sort(key=lambda g: g['t'])
    for a, b in zip(gfx, gfx[1:]):
        if a['t'] + a['dur'] > b['t'] + .05: print(f"OVERLAP {a['t']:.2f}+{a['dur']} {a.get('kind', a.get('type'))} / {b['t']:.2f} {b.get('kind', b.get('type'))} {b.get('text', b.get('name', ''))}")
    print(len(gfx), 'graphics; DUR', DUR)
    plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/prefontaine_v1.mp4', 'words': f'{HERE}/words_final.json', 'voice_ss': 0.0, 'duration': DUR,
            'face': {'src': f'{SP}/face.mov', 'focus': [0.5, 0.5]}, 'skip_res_check': True, 'segments': segs, 'graphics': gfx, 'ambience': amb}
    json.dump(plan, open(f'{HERE}/plan.json', 'w'), indent=1)
