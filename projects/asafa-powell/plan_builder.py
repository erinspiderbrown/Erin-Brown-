"""Asafa Powell (5:34). Full-screen photos only (no talking head; the narration rides on a hidden carrier track).
Every graphic is anchored to a spoken word. Results/facts are verified - see projects/asafa-powell/NOTES.md."""
import json, re, os, sys
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(S)
W = json.load(open('w8c/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-]", '', x['w'].lower()).rstrip('.') for x in W]
DUR = 336.04


def at(phrase, n=1, after=0.0):
    p = [re.sub(r"[^a-z0-9.'\-]", '', q).rstrip('.') for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if W[i]['s'] < after: continue
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')


M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
N = lambda t, dur, rank, name, sub: {'type': 'name', 't': round(t, 2), 'dur': dur, 'rank': rank, 'name': name, 'sub': sub}
t_wr = at('broke the world record')
gfx = [
    # --- hook
    N(0.3, 3.0, 'JAM', 'ASAFA POWELL', 'FORMER 100M WORLD RECORD HOLDER'),
    D('counter', at('97', 2) - .3, 3.0, value='97', unit='SUB-10s', label='Most in history', sub='100m races under 10 seconds'),
    M('board', t_wr - .1, round(at('and he ain\'t never') - t_wr + .2, 2), title='WORLD RECORDS',
      rows=[{'event': 'ATHENS 2005', 'value': '9.77'}, {'event': 'GATESHEAD 2006', 'value': '9.77', 'tag': 'TIED'},
            {'event': 'ZURICH 2006', 'value': '9.77', 'tag': 'TIED'}, {'event': 'RIETI 2007', 'value': '9.74'}],
      times=[0.1, round(at('tied it') - t_wr, 2), round(at('tied it again') - t_wr + .4, 2), round(at('then broke it') - t_wr + .3, 2)]),
    M('stamp', at('not one') - .1, 0.9, text='0 INDIVIDUAL GOLDS', size=90),
    M('keyword', at('so how you'), 3.0, text='FASTEST MAN ALIVE…'),
    # --- Jamaica / family
    M('pin', at('now asafa from'), 2.8, text='JAMAICA', sub='YOUNGEST OF 6 BOYS'),
    M('keyword', at('his mama'), 2.4, text='PARENTS: BOTH MINISTERS'),
    M('keyword', at('stephen'), 2.6, text='COACH STEPHEN FRANCIS · MVP'),
    M('keyword', at('scary fast'), 1.6, text='SCARY FAST'),
    M('keyword', at('2002'), 2.6, text='2002 · NEW YORK'),
    M('keyword', at('two of his brothers'), 3.0, text='TWO BROTHERS. GONE.'),
    # --- 2003 / 2004
    M('pin', at('paris'), 2.4, text='PARIS 2003', sub='WORLD CHAMPIONSHIPS'),
    M('stamp', at('they dq him'), 1.8, text='DQ', size=150),
    M('pin', at('athens olympics'), 2.4, text='ATHENS 2004', sub='OLYMPIC GAMES'),
    D('counter', at('fifth') - .2, 3.2, value='9.94', unit='SEC', label='5th · Olympic final', sub='Athens 2004 · no medal'),
    # --- 2005 WR, injury, 2006
    M('keyword', at('ain\'t no pressure') , 2.2, text='NO PRESSURE'),
    M('stopwatch', at('9.77') - 1.1, 2.0, value='9.77', unit='SECONDS', label='ATHENS · JUNE 2005', anim=1.0),
    M('stamp', at('world record', 1, after=at('9.77')) , 1.8, text='WORLD RECORD', size=110),
    M('keyword', at('fastest man alive'), 1.8, text='FASTEST MAN ALIVE'),
    M('stamp', at('he hurt his groin'), 1.1, text='GROIN INJURY', size=110),
    M('keyword', at('missed worlds'), 2.4, text='MISSED WORLDS 2005'),
    M('keyword', at('2006 ain\'t no'), 3.0, text='2006: NO WORLDS. NO OLYMPICS.'),
    M('board', at('he tie his own'), round(at('everybody\'s saying') - at('he tie his own') + .3, 2), title='2006 · TIED HIS OWN WR',
      rows=[{'event': 'GATESHEAD', 'value': '9.77'}, {'event': 'ZURICH', 'value': '9.77'}],
      times=[round(at('gateshead') - at('he tie his own') + .3, 2), round(at('zurich') - at('he tie his own') + .2, 2)]),
    M('keyword', at('next year'), 2.4, text='"NEXT YEAR IS HIS YEAR"'),
    # --- Osaka 2007
    M('pin', at('worlds in osaka'), 2.4, text='OSAKA 2007', sub='WORLD CHAMPIONSHIPS'),
    M('stamp', at('run him down'), 0.8, text='RUN DOWN', size=120),
    D('bars', at('tyson win it') - .2, 5.4, label='Osaka 2007 · 100m Final', unit='S', lower_is_better=True, spread=0.15,
      items=[{'name': 'Tyson Gay', 'value': '9.85'}, {'name': 'Derrick Atkins', 'value': '9.91'}, {'name': 'Powell · 3rd', 'value': '9.96'}]),
    M('keyword', at('when tyson came on') , 3.3, text='"I JUST PANICKED"'),
    N(at('and michael johnson'), 3.0, 'USA', 'MICHAEL JOHNSON', '4× OLYMPIC CHAMPION'),
    M('keyword', at('i\'m losing it'), 1.7, text='"I\'M LOSING IT…"'),
    M('stamp', at('he just gave up'), 1.6, text='GAVE UP', size=130),
    # --- Rieti 2007
    M('stopwatch', at('974') if False else at('9.74') - .9, 3.0, value='9.74', unit='SECONDS', label='RIETI · 2 WEEKS LATER', anim=0.9),
    M('stamp', at('the heats'), 2.0, text='IN THE HEATS', size=110),
    D('counter', at('win the final') , 2.8, value='9.78', unit='SEC', label='Won the final', sub='Rieti · 9 Sept 2007'),
    M('stamp', at('make it make sense'), 1.9, text='MAKE IT MAKE SENSE', size=90),
    # --- 2008
    M('pin', at('2008 beijing') + .2, 2.4, text='BEIJING 2008', sub='OLYMPIC GAMES'),
    D('counter', at('15 times') - .2, 3.2, value='15', unit='SUB-10s', label='In one season · 2008', sub='First man ever'),
    N(at('usain bolt') - .3, 3.0, 'JAM', 'USAIN BOLT', 'TOOK THE WR · 9.72 · MAY 2008'),
    D('bars', at('olympic final', 1, after=at('usain bolt')) , 5.0, label='Beijing 2008 · 100m Final', unit='S', lower_is_better=True, spread=0.3,
      items=[{'name': 'Usain Bolt', 'value': '9.69'}, {'name': 'Richard Thompson', 'value': '9.89'}, {'name': 'Walter Dix', 'value': '9.91'},
             {'name': 'Powell · 5th', 'value': '9.95'}]),
    M('keyword', at('i\'ve got no idea'), 4.4, text='"ALWAYS… FIFTH AT THE OLYMPICS"'),
    M('stopwatch', at('9.72') - .9, 3.0, value='9.72', unit='SECONDS', label='LAUSANNE · LIFETIME BEST', anim=0.9),
    M('stamp', at('after the olympics'), 1.8, text='AFTER THE OLYMPICS', size=95),
    M('keyword', at('gold in the'), 2.6, text='BEIJING 4X1: GOLD'),
    M('stamp', at('it\'s coming back'), 1.8, text='REMEMBER THIS', size=110),
    # --- 2009 / 2011 / 2012
    M('pin', at('worlds in berlin'), 1.05, text='BERLIN 2009', sub='WORLD CHAMPIONSHIPS'),
    D('bars', at('bolt run', after=at('worlds in berlin')) - .1, 4.6, label='Berlin 2009 · 100m Final', unit='S', lower_is_better=True, spread=0.3,
      items=[{'name': 'Usain Bolt', 'value': '9.58'}, {'name': 'Tyson Gay', 'value': '9.71'}, {'name': 'Powell · 3rd', 'value': '9.84'}]),
    M('keyword', at('few days later'), 2.8, text='ANCHORED 4X1 GOLD'),
    M('stamp', at('never came'), 1.8, text='NEVER CAME', size=120),
    M('pin', at('daegu'), 1.9, text='DAEGU 2011', sub='WORLD CHAMPIONSHIPS'),
    M('stamp', at('he pull out'), 1.8, text='WITHDREW', size=120),
    M('pin', at('london olympics'), 2.2, text='LONDON 2012', sub='OLYMPIC GAMES'),
    M('stamp', at('the groin give out'), 1.8, text='GROIN AGAIN', size=110),
    D('counter', at('11.99') - .5, 3.0, value='11.99', unit='SEC', label='Last place', sub='3rd Olympic final'),
    # --- 2013 / 2017
    M('stamp', at('he test positive'), 2.0, text='POSITIVE TEST', size=110),
    M('keyword', at('oxilofrine'), 2.6, text='OXILOFRINE (SUPPLEMENT)'),
    M('board', at('they give him'), round(at('but the damage') - at('they give him') + .6, 2), title='HIS BAN',
      rows=[{'event': 'ORIGINAL BAN', 'value': '18 MO'}, {'event': 'AFTER CAS APPEAL', 'value': '6 MO'}],
      times=[0.1, round(at('cas cut') - at('they give him'), 2)]),
    M('keyword', at('nesta carter') - .3, 2.6, text='NESTA CARTER · RETEST · 2017'),
    M('stamp', at('whole team get'), 2.0, text='DISQUALIFIED', size=110),
    M('keyword', at('give that medal back'), 2.6, text='MEDAL STRIPPED · 9 YEARS LATER'),
    # --- 2015 / 2016 / career
    M('keyword', at('never stopped showing up') - .3, 1.85, text='NEVER STOPPED SHOWING UP'),
    M('pin', at('at 32'), 2.4, text='BEIJING 2015', sub='WORLDS FINAL · AGE 32'),
    M('pin', at('in rio'), 2.6, text='RIO 2016', sub='OLYMPIC 4X1 · AGE 33'),
    M('stamp', at('and they win'), 1.8, text='OLYMPIC GOLD · 4X1', size=90),
    M('keyword', at('but that individual'), 3.6, text='INDIVIDUAL GOLD: NEVER'),
    M('board', at('he retired') , round(at('and out of every') - at('he retired'), 2), title='CAREER · RETIRED 2022',
      rows=[{'event': 'SUB-10 RACES', 'value': '97', 'tag': 'MOST EVER'}, {'event': 'WORLD RECORDS', 'value': '4', 'tag': 'W/ TIES'},
            {'event': 'IND. WORLD/OLY GOLD', 'value': '0'}],
      times=[round(at('97 sub-tens') - at('he retired'), 2), round(at('four world records') - at('he retired'), 2), round(at('and out of every') - at('he retired') - .6, 2)]),
    M('board', at('and out of every') + .1, round(at('so what was it') - at('and out of every') - .1, 2), title='9.72 OR FASTER · ALL-TIME',
      rows=[{'event': 'USAIN BOLT', 'value': '9.58', 'tag': 'GOLD'}, {'event': 'TYSON GAY', 'value': '9.69', 'tag': 'GOLD'},
            {'event': 'YOHAN BLAKE', 'value': '9.69', 'tag': 'GOLD'}, {'event': 'ASAFA POWELL', 'value': '9.72', 'tag': 'NONE'}],
      times=[0.2, 0.7, 1.2, round(at('the only one', 1) - at('and out of every') - .4, 2)]),
    M('keyword', at('was it nerves') , 1.0, text='NERVES?'),
    M('keyword', at('was it the injuries'), 1.35, text='INJURIES?'),
    M('keyword', at('born in the wrong era') - .3, 3.0, text='WRONG ERA?'),
    M('keyword', at('when the lights was off'), 2.4, text='LIGHTS OFF: FASTEST ALIVE'),
    M('stamp', at('when the lights came on'), 2.2, text='LIGHTS ON: GONE', size=100),
    M('poll', at('let me know') , round(DUR - at('let me know'), 2), question='NERVES OR BOLT?', options=['NERVES', 'BOLT']),
]
if __name__ == '__main__':
    gfx.sort(key=lambda g: g['t'])
    for a, b in zip(gfx, gfx[1:]):
        if a['t'] + a['dur'] > b['t'] + .05: print(f"OVERLAP {a['t']:.2f}+{a['dur']} {a.get('kind', a.get('type'))} / {b['t']:.2f} {b.get('kind', b.get('type'))} {b.get('text', b.get('name', ''))}")
    print(len(gfx), 'graphics')
    json.dump(gfx, open('w8c/gfx.json', 'w'), indent=1)


A = lambda src, t, end, lufs, fade=1.0: {'src': src, 't': round(t, 2), 'end': round(end, 2), 'lufs': lufs, 'fade': fade}
amb = [
    A('stadium_crowd_murmur', 0.0, at('but see life') + 1.0, -36, 1.5),                 # the legend / circuit
    A('stadium_crowd_murmur', at('then his first worlds') - .5, at('he says something') + .5, -36, 1.5),   # 2003-2007 meets
    A('stadium_cheer', at('9.77') - .3, at('9.77') + 4.0, -33, 0.6),                    # 2005 world record
    A('reporters_flashes', at('he says something'), at('he just gave up') + 1.5, -34, 0.8),   # post-race quotes
    A('stadium_cheer', at('9.74') - .3, at('9.74') + 4.0, -33, 0.6),                    # Rieti 9.74
    A('stadium_crowd_murmur', at('2008 beijing') - .3, at('2013 it get') - .3, -36, 1.5),     # 2008-2012
    A('crowd_victory', at('bolt run') - .2, at('bolt run') + 4.5, -32, 0.5),            # Bolt 9.69, Beijing
    A('reporters_flashes', at('2013 it get'), at('but the damage') + 2.0, -35, 0.8),    # the positive test
    A('stadium_crowd_murmur', at('in rio') - .3, at('so what was it'), -36, 1.5),     # Rio and the career recap
    A('stadium_cheer', at('and they win') - .2, at('and they win') + 4.0, -32, 0.6),    # Rio relay gold
]

# ---------------- shots ----------------
P = lambda n: f'raw8/ph/{n}.jpg'
B02, B01, B03, B06 = P('Powell_2010_06_04_Bislett_Games_02'), P('Powell_2010_06_04_Bislett_Games_01'), P('Powell_2010_06_04_Bislett_Games_03'), P('Powell_2010_06_04_Bislett_Games_06')
PA1, PA2, PA3, PA4 = (P(f'PowellAsafaParisStDenis2015_{i}') for i in (1, 2, 3, 4))
SING, DOHA, OSKH = P('Asafa_Powell_Singapore_2010'), P('Asafa_Powell_Doha_2012'), P('Osaka07_D1M_M100M_Heat_Astafa_Powell')
RIO = lambda c: P(f'Bolt_se_aposenta_com_medalha_d_s_{c}')
def full(t, src, foc=(0.5, 0.5), **kw): return {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'focus': list(foc)}, **kw}
def frame(t, src, top, bot, tf=(0.5, 0.35), bf=(0.5, 0.4), **kw):
    return {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': 0, 'fit': 'frame', 'top': {'src': top, 'focus': list(tf)}, 'bottom': {'src': bot, 'focus': list(bf)}}, **kw}
segs = [
    full(0.0, B02, (0.5, 0.3)),                                                       # hook: Powell, Oslo 2010
    full(at('97', 2) - .3, PA4, (0.62, 0.5)),                                          # racing, Paris 2015
    frame(t_wr - .1, DOHA, B01, PA3, (0.5, 0.08), (0.75, 0.35)),                         # WR board over Powell
    full(at('not one') - .2, B03, (0.5, 0.3), hit=True),
    full(at('so how you'), SING, (0.55, 0.4)),
    full(at('now asafa from'), P('Flag_of_Jamaica_02'), (0.55, 0.45)),
    full(at('his mama'), B06, (0.5, 0.3)),
    full(at('stephen'), P('Starting_block_J1'), (0.45, 0.5)),
    full(at('but see life'), P('Laitche_P063'), (0.4, 0.5)),
    full(at('about a year later'), P('Verso_Sera_al_Guidobaldi'), (0.5, 0.5)),
    full(at('then his first worlds'), PA1, (0.45, 0.5)),                               # Stade de France (2003 worlds venue)
    full(at('false start'), P('Starting_block_J1'), (0.7, 0.5)),
    full(at('athens olympics'), P('Athletissima_2012_arriv_e_du_100m_H'), (0.45, 0.5)),
    frame(at('where he finish'), DOHA, SING, P('Starting_block_J1'), (0.55, 0.3), (0.5, 0.5)),
    full(at('now peep what'), PA4, (0.4, 0.5), hit=True),                             # the 2005 WR
    full(at('world record', 1, after=at('9.77')), B06, (0.5, 0.25)),
    full(at('then he hurt'), B01, (0.5, 0.35)),
    full(at('2006 ain\'t no'), P('Athletissima_2012_arriv_e_du_100m_H_bis'), (0.5, 0.5)),
    full(at('he tie his own'), B01, (0.5, 0.3)),
    full(at('then tie it again'), PA3, (0.72, 0.4)),
    full(at('next year'), B03, (0.5, 0.25)),
    full(at('worlds in osaka'), P('Track_15797602003'), (0.6, 0.5)),                    # Nagai Stadium, Osaka
    full(at('run him down') - .2, P('Osaka07_D2A_Tyson_Gay_Victory'), (0.5, 0.4), hit=True),
    frame(at('his own cousin'), OSKH, P('Osaka07_D6A_Tyson_Gay_interview'), P('Track_15797602003'), (0.5, 0.35), (0.5, 0.5)),
    full(at('and after the race'), P('Osaka07_D6A_Tyson_Gay_interview'), (0.5, 0.4)),
    frame(at('when tyson came on'), OSKH, B02, P('Osaka07_D2A_Tyson_Gay_Victory'), (0.5, 0.08), (0.5, 0.15)),
    full(at('and michael johnson'), P('25th_Laureus_World_Sports_Awar_Michael_Johnson_240422_175402'), (0.5, 0.3)),
    full(at('i\'m losing it'), SING, (0.6, 0.4)),
    full(at('now check this out'), P('Stadio_Raul_Guidobaldi_Rieti_01'), (0.5, 0.5)),  # Rieti
    full(at('9.74') - .3, PA4, (0.55, 0.5), hit=True),
    full(at('the heats'), P('Verso_Sera_al_Guidobaldi'), (0.4, 0.5)),
    full(at('win the final'), B06, (0.5, 0.25)),
    full(at('make it make sense'), B03, (0.5, 0.3)),
    frame(at('2008 beijing'), P('Beijing_National_Stadium_and_Olympic_flame_2008_08_20_night'), P('Beijing_National_Stadium_2008_08_4'), B01, (0.5, 0.5), (0.5, 0.08), hit=True),
    full(at('15 times') - .3, PA2, (0.5, 0.45)),
    frame(at('usain bolt') - .4, P('Osaka07_D6A_M200M_nearfinish'), P('Usain_Bolt_Lightning_pose'), P('Usain_Bolt_9391717499'), (0.5, 0.3), (0.35, 0.4)),
    full(at('olympic final', 1, after=at('usain bolt')), P('Usain_Bolt_Olympics_Celebration'), (0.5, 0.35)),
    frame(at('asafa fifth'), P('Boltbeijing'), DOHA, P('Beijing_National_Stadium_2008_08_1'), (0.5, 0.3), (0.5, 0.5)),
    full(at('i\'ve got no idea'), SING, (0.5, 0.4)),
    full(at('and like two weeks'), B02, (0.5, 0.3)),
    full(at('gold in the'), RIO('1039086_19_08_2016_frz_1139'), (0.5, 0.45)),
    full(at('2009 worlds'), P('Usain_Bolt_Bislet_Games_2011'), (0.5, 0.35)),
    full(at('bolt run', after=at('worlds in berlin')) + .8, P('Usain_Bolt_9391717499'), (0.35, 0.45)),
    full(at('few days later'), P('2013_World_Championships_in_At_s_Men_s_4_100_metres_relay_04'), (0.5, 0.4)),
    full(at('by himself'), B03, (0.5, 0.3)),
    full(at('daegu'), SING, (0.45, 0.4)),
    full(at('london olympics'), P('London_Olympics_2012_Friday_Au_d_in_the_Olympic_Stadium_4959'), (0.5, 0.5)),
    full(at('and in the race'), P('Justin_Gatlin_Men_s_100m_Final_ndon_2012_Olympics_8374272018'), (0.4, 0.4), hit=True),
    full(at('dead last') - .4, P('London_Olympics_2012_Friday_Au_d_in_the_Olympic_Stadium_4959'), (0.72, 0.6)),
    frame(at('2013 it get'), DOHA, SING, P('Fans_in_the_Olympic_Park_7724429148'), (0.5, 0.35), (0.5, 0.4), hit=True),
    full(at('they give him'), B01, (0.5, 0.3)),
    full(at('and remember that'), P('Beijing_National_Stadium_2008_08_4'), (0.5, 0.5)),
    full(at('nesta carter') - .5, P('2013_World_Championships_in_At_s_Men_s_4_100_metres_relay_02'), (0.5, 0.4)),
    full(at('give that medal back') - .3, P('Osaka07_D9A_M4_100_VC') if False else B06, (0.5, 0.3)),
    full(at('here\'s the thing'), PA1, (0.4, 0.45)),
    full(at('at 32'), PA4, (0.5, 0.5)),
    full(at('in rio'), P('Est_dio_Ol_mpico_Engenh_o_nos_Jogos_Paraol_mpicos_Rio_2016'), (0.5, 0.5)),
    full(at('and they win'), RIO('1039087_19_08_2016_frz_1141'), (0.6, 0.45), hit=True),
    full(at('a relay gold'), RIO('1039105_19_08_2016_frz_1203'), (0.45, 0.4)),
    full(at('but that individual'), SING, (0.55, 0.4)),
    full(at('he retired'), PA2, (0.5, 0.45)),
    full(at('and out of every'), RIO('1039085_19_08_2016_frz_1119'), (0.4, 0.4)),
    full(at('so what was it'), B02, (0.5, 0.3)),
    full(at('born in the wrong era') - .5, P('Usain_Bolt_Olympics_Celebration'), (0.5, 0.35)),
    full(at('when the lights was off'), P('Beijing_National_Stadium_and_Olympic_flame_2008_08_20_night'), (0.6, 0.5)),
    full(at('when the lights came on'), SING, (0.5, 0.4)),
    full(at('let me know'), RIO('1039083_19_08_2016_frz_1074'), (0.5, 0.45)),
]
if __name__ == '__main__':
    import subprocess
    segs.sort(key=lambda s: s['start'])
    missing = sorted({s['broll'][k]['src'] if k != 'src' else s['broll']['src'] for s in segs for k in ('src', 'top', 'bottom') if k in s['broll']} - {p for p in []})
    missing = [m for m in missing if not os.path.exists(m)]
    print('segments', len(segs), '| missing files:', missing)
    for a, b in zip(segs, segs[1:]):
        if b['start'] - a['start'] < 1.0: print('SHORT', a['start'], b['start'])
    plan = {'workdir': 'w8/build', 'output': 'out/asafa_powell_v3.mp4', 'words': 'w8c/words_final.json', 'voice_ss': 0.0, 'duration': DUR,
            'face': {'src': 'w8c/face.mov', 'focus': [0.5, 0.5]}, 'skip_res_check': True, 'segments': segs, 'graphics': gfx, 'ambience': amb}
    json.dump(plan, open('/home/user/Erin-Brown-/projects/asafa-powell/plan.json', 'w'), indent=1)
