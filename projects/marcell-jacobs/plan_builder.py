"""Marcell Jacobs TikTok (~7:00), cut from the owner's YouTube video "The Strange Case of Marcell Jacobs" with his ORIGINAL voice.
Owner's brief: more VERTICAL video/photo B-roll, high quality, really professional. So the edit alternates every ~5 s between
  F  his footage in sync, in a square band at native sharpness (1078x1078 crop, no upscale) with real stills above/below, and
  P  a vertical photo: true full-screen 9:16 for photos >= ~2000 px tall, or a near-full-screen 9:10 band (1080x1200) for the
     1920x1280 Commons photos of Jacobs (shown at native size, never enlarged).
Facts: NOTES.md (graphics show the corrected values: EUR 10,000, Sept 2020, Gabriele Pegoraro)."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad/jacb'
PH = '/tmp/claude-0/-home-user-Erin-Brown-/353a917a-eedc-5fa9-9c7e-7d1a29f0affb/scratchpad/jacph/ph'
W = json.load(open(f'{H}/words_final.json')); CM = json.load(open(f'{H}/cut_map.json'))
TOK = [re.sub(r"[^a-z0-9.'\-]", '', x['w'].lower()).rstrip('.').strip("'") for x in W]
VOICE_END = W[-1]['e']; FACTS_END = VOICE_END + 7.0; DUR = round(FACTS_END + 4.5, 2)
SRC = f'{H}/raw/source.mp4'; ST = lambda n: f'{H}/stills/{n}.jpg'; P = lambda n: f'{PH}/{n}.jpg'


def at(phrase, n=1, after=0.0):
    p = [re.sub(r"[^a-z0-9.'\-]", '', q).rstrip('.').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if W[i]['s'] < after: continue
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


def src_t(t):
    r = [c for c in CM if c['new'] <= t + 1e-6][-1]
    return r['src'] + (t - r['new'])


# ---- photos (Commons, see CREDITS.md). kind: 'full' (true 9:16) or 'band' (9:10, native size); focus x (0..1)
PHOTOS = {
    'jacobs_paris': ('full', P('Paris_Olympics_Athletics_53914712885'), 0.57),
    'jacobs_belgrade': ('band', P('Marcell_Jacobs_Belgrade_2022_2'), 0.62),
    'jacobs_child': ('band', P('Marcell_Jacobs_and_his_small_child_Belgrade_2022'), 0.3),
    'jacobs_sitting': ('band', P('Marcell_Jacobs_after_Istanbul_2023_silver_medal'), 0.38),
    'jacobs_roma': ('band', P('Marcell_Jacobs_Roma_2024'), 0.45),
    'jacobs_mattarella': ('band', P('Mattarella_Jacobs_2024'), 0.5),
    'jacobs_relay': ('band', P('4_100_Budapest_2023_Jacobs_and_Patta'), 0.72),
    'relay_podium': ('band', P('Podium_4_100_m_relay_Roma_2024'), 0.3),
    'tortu_portrait': ('full', P('Filippo_Tortu_ITA_2022'), 0.45),
    'tortu_flag': ('full', P('2022_08_19_European_Championsh_0_Metres_by_Sandro_Halank_029'), 0.5),
    'tortu_200': ('band', P('2022_08_19_European_Championsh_0_Metres_by_Sandro_Halank_004'), 0.75),
    'italy_relay': ('full', P('Italia_en_los_relevos_4x100_de__Juegos_del_Mediterr_neo_2018'), 0.42),
    'kerley': ('full', P('2018_USA_Indoor_Track_and_Field_Championships_39439538975'), 0.6),
    'thompson': ('full', P('Kishane_Thompson_JO_03_08_2024'), 0.45),
    'seville': ('full', P('Oblique_Seville_03_08_2024'), 0.4),
    'lyles_start': ('full', P('Noah_Lyles_JO_03_08_2024'), 0.5),
    'paris_line': ('full', P('Xie_Zhenye_Noah_Lyles'), 0.45),
    'tebogo': ('full', P('Letsile_Tebogo_JO_03_08_2024'), 0.5),
    # identified as Giacomo Tortu only by Corriere dell'Umbria using it as the lead image of a profile of him (no caption naming the person);
    # the owner chose to use it (Nov 9 2026) after being told it may show Filippo. Always labelled 'PER ITALIAN MEDIA · ALLEGED'.
    'hacker_still': ('band', ST('hacker'), 0.5),
    'spy_still': ('band', ST('spy'), 0.5),
    'servers_still': ('band', ST('servers'), 0.5),
    'giacomo': ('band', f'{H}/photos/giacomo_tortu_corriereumbria.jpg', 0.55),
}
PROBE = {}


def photo_seg(t, key, top='tokyo_finish', bot='euro_scoreboard', **kw):
    kind, src, fx = PHOTOS[key]
    if kind == 'full':
        return {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': [fx, 0.4]}, **kw}
    from PIL import Image
    w, h = PROBE.setdefault(src, Image.open(src).size)
    cw = int(h * (1.0 if h < 1200 else 0.9)); x = int((w - cw) * fx)   # 9:10 window at native height (square for short photos)
    return {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'fit': 'frame', 'crop': [cw, h, x, 0],
            'top': {'src': ST(top), 'focus': [0.5, 0.4]}, 'bottom': {'src': ST(bot), 'focus': [0.5, 0.45]}}, **kw}


def foot_seg(t, top, bot, fx=0.5, **kw):
    x = int((1920 - 1078) * fx)
    return {'type': 'full', 'start': round(t, 2), 'broll': {'src': SRC, 'ss': round(src_t(t), 3), 'fit': 'frame', 'crop': [1078, 1078, x, 0],
            'top': {'src': ST(top), 'focus': [0.5, 0.4]}, 'bottom': {'src': ST(bot), 'focus': [0.5, 0.45]}}, **kw}


# ---- sections: (start phrase, photo keys to rotate, panel stills to rotate). Cuts land on phrase starts ~every 5 s,
# alternating footage / photo. A photo key may repeat across the video but never back-to-back.
SECTIONS = [
    ('imagine winning', ['jacobs_sitting', 'jacobs_paris'], ['tokyo_finish', 'gold_graphic', 'euro_scoreboard', 'jacobs_tv']),
    ('now imagine that', ['jacobs_mattarella', 'jacobs_sitting'], ['hacker', 'spy', 'servers', 'jacobs_cap']),
    ("and here's where", ['jacobs_belgrade', 'jacobs_sitting', 'jacobs_roma'], ['tokyo_race', 'milan_court', 'presser', 'gold_graphic']),
    ('before 2021', ['jacobs_relay', 'relay_podium', 'jacobs_child'], ['longjump', 'euro_scoreboard', 'gym', 'jacobs_tv']),
    ('then he went to tokyo', ['kerley', 'jacobs_paris', 'relay_podium'], ['tokyo_race', 'tokyo_finish', 'gold_graphic', 'gold2']),
    ('now this is where', ['jacobs_sitting', 'jacobs_roma'], ['lab', 'pills', 'vials', 'article']),
    ('during the olympics', ['jacobs_belgrade', 'jacobs_mattarella'], ['nutri_card', 'spazzini', 'pills', 'doc']),
    ('the questions didn\'t', ['jacobs_child', 'jacobs_roma', 'jacobs_belgrade'], ['jacobs_interview', 'jacobs_tv', 'jacobs_cap2', 'tokyo_finish']),
    ('in 2024 jacobs', ['lyles_start', 'thompson', 'seville', 'paris_line', 'jacobs_paris'], ['paris_jacobs', 'indoor_60', 'jacobs_tv', 'euro_scoreboard']),
    ('italian media reported', ['hacker_still', 'jacobs_mattarella', 'spy_still'], ['spy', 'hacker', 'servers', 'milan_court']),
    ('the operation was connected', ['jacobs_roma', 'jacobs_relay'], ['servers', 'milan_court', 'presser', 'hacker']),
    ('and in april', ['servers_still', 'jacobs_paris', 'jacobs_sitting'], ['milan_court', 'presser', 'servers', 'spy']),
]
HITS = ['how did he get', 'was marcell jacobs doping', 'it was giacomo tortu', '9.80 seconds', 'because suspicion is not proof', 'insane turn',
        'not a conviction']
FULL_AT = {'fred kerley': 'kerley', 'hacker gabriele': 'hacker_still', 'imagine winning': 'jacobs_roma', 'it was giacomo tortu': 'giacomo', 'the brother of filippo': 'tortu_portrait',
           'italian media reported': 'giacomo', 'giacomo tortu amongst': 'giacomo', '9.80 seconds': 'jacobs_paris',
           'in 2024 jacobs': 'lyles_start', 'filippo tortu jacobs': 'tortu_flag'}     # forced photos on key beats

STARTS = [W[i]['s'] for i in range(len(W)) if i == 0 or W[i - 1]['w'].endswith(('.', '?', '!', ','))]
sec_t = [at(p) for p, _, _ in SECTIONS] + [VOICE_END + 10]
hit_t = {at(h) for h in HITS}; forced = {at(k): v for k, v in FULL_AT.items()}
FOOT_AT = [at('a man named')]   # his own footage of Spazzini runs under the Spazzini name tag
forced[round(VOICE_END + 0.1, 2)] = 'jacobs_roma'          # the closing 'since then' board sits on Jacobs, never on Filippo
forced[round(FACTS_END, 2)] = 'jacobs_paris'                 # and so does the poll
cuts = []
for t in STARTS + list(forced) + FOOT_AT:
    if not cuts or t - cuts[-1] >= 4.4 or t in forced or t in FOOT_AT: cuts.append(t)
cuts = sorted(set(round(c, 2) for c in cuts))
cuts = [c for i, c in enumerate(cuts) if i == 0 or c - cuts[i - 1] >= 1.6 or c in forced or c in FOOT_AT]
WSTARTS = [w['s'] for w in W]
while True:                      # no shot longer than 8 s: split long gaps at the word start nearest the middle
    ends = cuts[1:] + [DUR]; long_ = [(c, e) for c, e in zip(cuts, ends) if e - c > 8.0]
    if not long_: break
    for c, e in long_:
        cand = [t for t in WSTARTS if c + 3.0 < t < e - 3.0]
        if cand: cuts.append(round(min(cand, key=lambda x: abs(x - (c + e) / 2)), 2))
        else: cuts.append(round((c + e) / 2, 2))
    cuts = sorted(set(cuts))
segs, last_photo, kind_flip = [], None, 0
for i, t in enumerate(cuts):
    si = max(k for k in range(len(SECTIONS)) if sec_t[k] <= t + 0.01)
    _, pkeys, stills = SECTIONS[si]
    a, b = stills[i % len(stills)], stills[(i + 1) % len(stills)]
    hit = any(abs(t - h) < 0.3 for h in hit_t)
    if any(abs(t - f) < 0.05 for f in FOOT_AT):
        key = None
    elif t in forced:
        key = forced[t]
    elif kind_flip % 2 == 1:
        key = next((k for k in pkeys[(i // 2) % len(pkeys):] + pkeys if k != last_photo), pkeys[0])
    else:
        key = None
    if key:
        segs.append(photo_seg(t, key, a, b, **({'hit': True} if hit else {}))); last_photo = key
    else:
        segs.append(foot_seg(t, a, b, **({'hit': True} if hit else {})))
    kind_flip += 1

# ---------------- graphics ----------------
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
N = lambda t, dur, rank, name, sub: {'type': 'name', 't': round(t, 2), 'dur': dur, 'rank': rank, 'name': name, 'sub': sub}
t_tg = at('inside your phone'); t_tk = at('jacobs ran 9.94'); t_tar = at('the target wasn\'t just')
gfx = [
    # --- hook
    N(0.3, 3.2, 'ITA', 'MARCELL JACOBS', 'OLYMPIC 100M CHAMPION · TOKYO 2020'),
    M('keyword', at('how did he get') - .1, 1.9, text='HOW DID HE GET THIS FAST?'),
    M('stamp', at('spends over') + .3, 1.6, text='€10,000+', size=150),
    M('board', t_tg - .2, round(at('not to steal money') - t_tg + .1, 2), title='TARGETED PHONES (ALLEGED)',
      rows=[{'event': 'MARCELL JACOBS', 'value': '📱'}, {'event': 'HIS COACH', 'value': '📱'}, {'event': 'HIS NUTRITIONIST', 'value': '📱'},
            {'event': 'HIS MANAGER', 'value': '📱'}],
      times=[0.1, round(at("your coach's") - t_tg, 2), round(at('your nutritionist') - t_tg, 2), round(at("your manager's") - t_tg, 2)]),
    M('stamp', at('was marcell jacobs doping') + .2, 1.8, text='DOPING?', size=150),
    M('pin', at('shocked the world in tokyo') + .4, 1.3, text='TOKYO 2020', sub='OLYMPIC 100M · AUG 1, 2021'),
    M('keyword', at('italian prosecutors said'), 2.6, text='ITALIAN PROSECUTORS'),
    M('keyword', at("wasn't just a random"), 2.2, text='NOT A RANDOM JOURNALIST'),
    N(at('it was giacomo tortu') + .1, 2.2, 'ITA', 'GIACOMO TORTU', 'ACCUSED · NOT CONVICTED'),
    N(at('the brother of filippo') + .2, 3.2, 'ITA', 'FILIPPO TORTU', 'BROTHER · TEAMMATE · NOT ACCUSED'),
    M('keyword', at('was there actually evidence'), 2.8, text='ANY ACTUAL EVIDENCE?'),
    # --- the rise
    M('keyword', at('wasn\'t exactly the guy'), 2.6, text='NOT THE GUY YOU EXPECTED'),
    M('keyword', at('long jumper'), 2.4, text='FORMER LONG JUMPER'),
    M('stopwatch', at('was only 10.03') + .1, 2.6, value='10.03', unit='SECONDS', label='100M PB ENTERING 2021 (2019)', anim=1.0),
    M('stamp', at('different universe') - .1, 1.6, text='DIFFERENT UNIVERSE', size=95),
    M('stopwatch', at('then he ran 9.95') + .2, 2.6, value='9.95', unit='SECONDS', label='ITALIAN RECORD · MAY 2021', anim=1.0),
    M('board', t_tk - .1, round(at('and then for the final') - t_tk + 4.0, 2), title='TOKYO 2020 · 100M',
      rows=[{'event': 'HEAT', 'value': '9.94', 'tag': 'NR'}, {'event': 'SEMI-FINAL', 'value': '9.84', 'tag': 'AR'},
            {'event': 'FINAL', 'value': '9.80', 'tag': 'GOLD'}],
      times=[0.2, round(at('ran 9.84') - t_tk, 2), round(at('and then for the final') - t_tk + .6, 2)]),
    N(at('fred kerley') - .3, 3.0, 'USA', 'FRED KERLEY', 'TOKYO SILVER · 9.84'),
    M('stamp', at('9.80 seconds') + .1, 1.6, text='9.80', size=170),
    M('keyword', at('the first italian man'), 3.2, text='FIRST ITALIAN 100M CHAMPION'),
    M('keyword', at('everybody knew his name'), 2.0, text='OVERNIGHT FAME'),
    M('stamp', at('so did the doping') - .1, 1.8, text='DOPING QUESTIONS', size=95),
    # --- suspicion is not proof
    M('keyword', at('you have to be careful'), 2.4, text='CAREFUL HERE'),
    M('stamp', at('suspicion is not proof') + .1, 2.2, text='SUSPICION ≠ PROOF', size=100),
    M('keyword', at('did not fail a doping'), 2.3, text='NO FAILED TEST'),
    M('keyword', at('the aiu said'), 3.2, text='AIU: ALL TESTS NEGATIVE'),
    M('keyword', at('his improvement was enormous'), 1.6, text='ENORMOUS IMPROVEMENT'),
    D('bars', at('before 2021 10.03') - .1, 4.2, label='Jacobs · 100m', unit='S', lower_is_better=True, spread=0.3,
      items=[{'name': 'Before 2021 (PB)', 'value': '10.03'}, {'name': 'Tokyo final', 'value': '9.80'}]),
    # --- the nutritionist
    N(at('a man named') + .2, 3.4, 'ITA', 'GIACOMO SPAZZINI', 'NUTRITIONIST · WORKED WITH JACOBS'),
    M('keyword', at('operation muscle bound') + .2, 2.6, text='"OPERATION MUSCLE BOUND"'),
    M('keyword', at('anabolic steroids'), 2.8, text='STEROIDS · HGH (ALLEGED)'),
    M('stamp', at('timing was terrible') - .1, 1.6, text='TERRIBLE TIMING', size=100),
    M('keyword', at('where did this guy'), 2.4, text='"WHERE DID HE COME FROM?"'),
    M('keyword', at('international news'), 1.5, text='WORLDWIDE NEWS'),
    M('stamp', at('no public evidence') - .1, 1.8, text='NO PUBLIC EVIDENCE', size=95),
    M('calendar', at('march of 2021') - .4, 2.8, items=['MAR', '2021'], hi=[0], label='SPLIT FROM SPAZZINI'),
    M('stamp', at("isn't really accurate") - .1, 1.6, text='NOT ACCURATE', size=120),
    M('keyword', at('never finding'), 2.8, text='NO FINDING AGAINST JACOBS'),
    # --- aftermath
    M('keyword', at('successor to usain bolt'), 2.8, text="BOLT'S SUCCESSOR"),
    M('keyword', at('shut down his season'), 2.4, text='SEASON OVER'),
    M('keyword', at('blood sweat'), 2.6, text='"BLOOD, SWEAT AND TEARS"'),
    M('pin', at('final in paris') - .2, 2.4, text='PARIS 2024', sub='OLYMPIC 100M FINAL'),
    M('stopwatch', at('he ran 9.85') + .2, 2.3, value='9.85', unit='SECONDS', label='PARIS FINAL · 5TH', anim=1.0),
    M('keyword', at('fastest olympic'), 2.2, text='ONE OF THE FASTEST FINALS EVER'),
    M('stamp', at('insane turn') - .2, 1.8, text='2025: INSANE TURN', size=95),
    # --- the hacking
    N(at('italian media reported') + .1, 3.0, 'ITA', 'GIACOMO TORTU', 'ACCUSED · NOT CONVICTED'),
    M('keyword', at('become suspicious') - .2, 2.6, text='GIACOMO TORTU: SUSPICIOUS?'),
    M('keyword', at('get the answers privately') - .3, 2.4, text='ANSWERS… PRIVATELY'),
    N(at('hacker gabriele') - .2, 3.2, 'ITA', 'GABRIELE PEGORARO', 'ALLEGED HACKER'),
    M('board', t_tar, round(at('the period investigators') - t_tar, 2), title='ALLEGED TARGETS',
      rows=[{'event': 'MARCELL JACOBS', 'value': '📱'}, {'event': 'HIS COACH', 'value': '📱'}, {'event': 'HIS MANAGER', 'value': '📱'},
            {'event': 'HIS NUTRITIONIST', 'value': '📱'}],
      times=[round(at('belongings of marcell') - t_tar + .3, 2), round(at('his coach') - t_tar, 2), round(at('his manager') - t_tar, 2),
             round(at('and his nutritionist') - t_tar + .2, 2)]),
    M('calendar', at('the period investigators') + .3, 4.6, items=['SEP 2020', 'AUG 2021'], hi=[1], label='PERIOD PROSECUTORS CITE'),
    M('keyword', at('months leading up'), 3.0, text='BEFORE + DURING TOKYO'),
    M('keyword', at('actually clean'), 2.2, text='WAS HE CLEAN?'),
    M('pin', at('connected to equalize') + .2, 2.8, text='EQUALIZE', sub='MILAN INTELLIGENCE FIRM'),
    M('keyword', at('unauthorized access'), 2.8, text='DATABASES · PRIVATE FILES'),
    M('keyword', at('extracted communications'), 2.6, text='COMMUNICATIONS EXTRACTED'),
    M('calendar', at('april of 2026') - .3, 2.6, items=['APR', '2026'], hi=[0], label='PROSECUTORS CLOSE PHASE 2'),
    D('counter', at('81 people') - .2, 2.8, value='81', unit='PEOPLE NAMED', label='Equalize investigation', sub='April 2026'),
    M('stamp', at('paid over') + .3, 1.8, text='€10,000 (ALLEGED)', size=95),
    M('stamp', at('not a conviction') - .4, 2.4, text='ALLEGATIONS, NOT A CONVICTION', size=70),
    M('keyword', at('could face trial'), 2.6, text='COULD FACE TRIAL'),
    N(at('filippo tortu jacobs') + .1, 3.4, 'ITA', 'FILIPPO TORTU', 'NOT ACCUSED OF ANY WRONGDOING'),
    # facts the owner approved adding (Il Post, 9 Oct 2025); his voice is unchanged
    M('board', round(VOICE_END + 0.3, 2), 6.6, title='SINCE THEN (OCT 2025)',
      rows=[{'event': 'FIDAL BAN · G. TORTU', 'value': '3 YRS'}, {'event': 'THE USB HE GOT', 'value': 'EMPTY'},
            {'event': 'DOPING CLAIMS', 'value': 'NO BASIS'}], times=[0.3, 2.0, 3.7]),
    M('poll', round(FACTS_END, 2), round(DUR - FACTS_END, 2), question='WAS THE SUSPICION ON JACOBS FAIR?', options=['FAIR', 'UNFAIR']),
]

if __name__ == '__main__':
    segs.sort(key=lambda s: s['start'])
    full = sum(e - s['start'] for s, e in zip(segs, [x['start'] for x in segs[1:]] + [DUR]) if s['broll']['src'] != SRC)
    print(f'segments {len(segs)}; photo screen time {full:.0f}s of {DUR:.0f}s ({100 * full / DUR:.0f}%)')
    for a, b in zip(segs, segs[1:]):
        if b['start'] - a['start'] < 1.5: print('SHORT', a['start'], b['start'])
        if b['start'] - a['start'] > 9: print(f"LONG {a['start']:.1f} {b['start'] - a['start']:.1f}s")
    files = {s['broll'][k]['src'] for s in segs for k in ('top', 'bottom') if k in s['broll']} | {s['broll']['src'] for s in segs}
    print('missing:', sorted(os.path.basename(f) for f in files if not os.path.exists(f)))
    gfx.sort(key=lambda g: g['t'])
    for a, b in zip(gfx, gfx[1:]):
        if a['t'] + a['dur'] > b['t'] + .05: print(f"OVERLAP {a['t']:.2f}+{a['dur']} {a.get('kind', a.get('type'))} / {b['t']:.2f} {b.get('kind', b.get('type'))} {b.get('text', b.get('name', ''))}")
    print(len(gfx), 'graphics; voice', VOICE_END, 'DUR', DUR)
    plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/marcell_jacobs_v3.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
            'duration': DUR, 'face': {'src': f'{SP}/face_v2.mov', 'focus': [0.5, 0.5]}, 'skip_res_check': True, 'segments': segs,
            'graphics': gfx, 'ambience': []}
    json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
