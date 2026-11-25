"""Yaseen Abdalla hot take (~2:03): "you chose Sudan, so be fully African". Jane Hedengren format + guest soundbite (his own video).
Facts (NOTES.md): Valencia Half 25 Oct 2026, 8th, 59:12 (Sudan NR); US record Conner Mantz 59:17 (Houston, Jan 2025);
not ratified: USATF requires eligibility to represent the US. Paris 2024 marathon 33rd 2:11:41; Tokyo 2025 marathon 21st 2:13:32.
African/world record Yomif Kejelcha 56:51 (Buenos Aires, 23 Aug 2026). 59:12 = tied 97th African all-time; 20th = Kennedy Kimutai 58:28.
Jacobs b. El Paso TX -> Italy; Briana Williams b. Coral Springs FL -> Jamaica; Issam Asinga b. Atlanta GA (raised St. Louis) -> Suriname;
Joseph Fahnbulleh b. Hopkins MN -> Liberia."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-Erin-Brown-/44aa0cd6-8023-5301-82fa-277e8bea228e/scratchpad/yaseen15'
W = json.load(open(f'{H}/words_final.json'))
TOK = [re.sub(r"[^a-z0-9.'\-*:]", '', x['w'].lower()).rstrip('.,?').strip("'") for x in W]
B = lambda n: f'{H}/broll/{n}'

def at(phrase, n=1):
    p = [re.sub(r"[^a-z0-9.'\-*:]", '', q).rstrip('.,?').strip("'") for q in phrase.lower().split()]; k = 0
    for i in range(len(TOK) - len(p) + 1):
        if all(TOK[i + j] == p[j] for j in range(len(p))):
            k += 1
            if k == n: return round(W[i]['s'], 2)
    sys.exit(f'not found: {phrase}')

END = round(W[-1]['e'] + 1.8, 2)
full = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'full', 'start': round(t, 2), 'broll': {'src': src, 'ss': k.pop('ss', 0), 'focus': [fx, fy]}, **k}
split = lambda t, src, fx=0.5, fy=0.4, **k: {'type': 'split', 'start': round(t, 2), 'broll': {'src': src, 'ss': k.pop('ss', 0), 'focus': [fx, fy]}, **k}
M = lambda kind, t, dur, **k: {'type': 'motion', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}
D = lambda kind, t, dur, **k: {'type': 'data', 'kind': kind, 't': round(t, 2), 'dur': dur, **k}

ROAD, PACK, CLOSE, TRACK = (B(f'p{i}_hd.jpg') for i in range(1, 5))   # owner's photos of Abdalla (Sudan kit)
JACOBS, BRIANA, ASINGA, FAHN = B('jacobs.jpg'), B('briana.jpg'), B('asinga.jpg'), B('fahn.jpg')

t_this, t_born, t_chose, t_jacobs, t_briana, t_issam, t_joseph, t_pleth, t_so, t_half, t_coming = (
    at('this is an african'), at('who was born'), at('but he chose'), at('marcell jacobs'), at('briana williams'), at('issam asinga'),
    at('joseph fahnbulleh'), at('just a plethora'), at('so yaseen decided'), at('for a half marathon'), at("he's coming online"))
t_guest = round(W[next(i for i,x in enumerate(W) if TOK[i]=='count') + 1]['s'], 2) if False else 60.3
GUEST = B('guest_hd.mp4')   # his own post, 0-5.05 s, shown full-screen as posted (title card included)
t_well, t_larp, t_dec2, t_rec, t_looked, t_road, t_goofy, t_usc, t_usc2, t_knock = (
    at('well, you decided'), at('why you keep'), at('you decided to be african', 2), at('go break the african'), at('i looked up'),
    at('i can go these'), at("but it's goofy"), at("oh, i'm a"), at("i'm a u.s.", 2), at('so knock that'))

segs = [
    full(0.0, CLOSE, 0.5, 0.35, hit=True),
    split(t_this - 0.05, PACK, 0.45, 0.35),
    split(t_born - 0.05, ROAD, 0.4, 0.3),
    full(t_chose - 0.05, TRACK, 0.3, 0.35),
    split(t_jacobs - 0.05, JACOBS, 0.85, 0.35),
    split(t_briana - 0.05, BRIANA, 0.5, 0.4),
    split(t_issam - 0.05, ASINGA, 0.5, 0.35),
    split(t_joseph - 0.05, FAHN, 0.62, 0.4),
    split(t_pleth - 0.05, PACK, 0.6, 0.4),
    full(t_so - 0.05, CLOSE, 0.5, 0.35, hit=True),
    split(t_half - 0.05, ROAD, 0.4, 0.35),
    split(t_coming - 0.05, TRACK, 0.3, 0.3),
    full(t_guest, GUEST, 0.5, 0.5, transition='cut'),
    full(t_well - 0.05, TRACK, 0.3, 0.35, hit=True),
    split(t_larp - 0.05, PACK, 0.45, 0.35),
    split(t_dec2 - 0.05, ROAD, 0.4, 0.3),
    split(t_looked - 0.05, CLOSE, 0.5, 0.4),
    split(t_road - 0.05, TRACK, 0.75, 0.35),
    full(t_goofy - 0.05, CLOSE, 0.5, 0.3),
    split(t_usc - 0.05, JACOBS, 0.85, 0.35),
    split(t_usc2 - 0.05, FAHN, 0.62, 0.4),
    split(t_knock - 0.05, PACK, 0.45, 0.35),
]
gfx = [
    M('keyword', 0.4, 3.6, text='FASTEST AMERICAN EVER?'),
    M('pin', t_this + 0.3, 2.4, text='SUDAN', sub='THE COUNTRY HE RUNS FOR'),
    M('keyword', t_born + 0.2, 3.0, text='BORN IN THE USA'),
    M('slam', t_chose + 1.6, 1.8, text='THE EASIER PATH', hi=2, anchor='upper'),
    M('board', t_jacobs - 0.2, t_pleth - t_jacobs + 0.2, title='BORN IN THE USA, RAN FOR…',
      rows=[{'event': 'M. JACOBS · TEXAS', 'value': 'ITALY'}, {'event': 'B. WILLIAMS · FLORIDA', 'value': 'JAMAICA'},
            {'event': 'I. ASINGA · GEORGIA', 'value': 'SURINAME'}, {'event': 'J. FAHNBULLEH · MINN.', 'value': 'LIBERIA'}],
      times=[0.2, t_briana - t_jacobs + 0.2, t_issam - t_jacobs + 0.2, t_joseph - t_jacobs + 0.2]),
    M('board', t_half + 1.0, t_coming - t_half - 0.9, title='VALENCIA HALF · OCT 2026',
      rows=[{'event': '8TH · Y. ABDALLA', 'value': '59:12'}], times=[0.4]),
    M('board', t_coming + 0.6, t_guest - t_coming - 0.5, title='US HALF MARATHON RECORD',
      rows=[{'event': 'C. MANTZ · OFFICIAL', 'value': '59:17'}, {'event': 'Y. ABDALLA · SUDAN', 'value': '59:12'}], times=[0.3, 1.2]),
    M('board', t_so + 1.4, t_half - t_so - 1.3, title='YASEEN FOR SUDAN',
      rows=[{'event': 'PARIS 2024 · MARATHON', 'value': '33RD'}, {'event': 'TOKYO 2025 · MARATHON', 'value': '21ST'}], times=[0.3, 1.0]),
    M('slam', t_well + 1.3, 1.9, text='BE FULLY AFRICAN', hi=2, anchor='upper'),
    M('keyword', t_larp + 1.0, 2.8, text='LARPING AS AMERICAN?'),
    M('board', t_rec, round(t_looked + 0.7 - t_rec, 2), title='AFRICAN & WORLD RECORD',
      rows=[{'event': 'Y. KEJELCHA · 2026', 'value': '56:51'}], times=[0.4]),
    M('board', t_looked + 0.8, t_road - t_looked - 0.6, title='AFRICA ALL-TIME · HALF',
      rows=[{'event': '20TH · K. KIMUTAI', 'value': '58:28'}, {'event': 'T-97TH · Y. ABDALLA', 'value': '59:12'}], times=[0.4, 1.4]),
    M('slam', t_goofy + 0.4, 1.7, text='GOOFY', hi=0, anchor='upper'),
    M('keyword', t_usc + 0.3, 2.8, text='U.S. CITIZENS TOO'),
    M('poll', t_knock - 0.4, END - t_knock + 0.4, question='SHOULD 59:12 BE THE AMERICAN RECORD?', options=['YES', 'NO']),
]
zooms = [[t_larp - 0.1, t_larp + 1.4, 1.1], [t_goofy - 0.1, t_goofy + 1.2, 1.12]]
segs.sort(key=lambda s: s['start']); gfx.sort(key=lambda g: g['t'])
os.makedirs(f'{SP}/out', exist_ok=True)
plan = {'workdir': f'{SP}/build', 'output': f'{SP}/out/yaseen_v1.mp4', 'words': f'{H}/words_final.json', 'voice_ss': 0.0,
        'duration': END, 'face': {'src': f'{H}/work/aroll.mov', 'focus': [0.5, 0.5]}, 'segments': segs, 'zooms': zooms, 'graphics': gfx}
json.dump(plan, open(f'{H}/plan.json', 'w'), indent=1)
for a, b in zip(segs, segs[1:] + [{'start': END}]):
    if b['start'] - a['start'] < 1.5 or b['start'] - a['start'] > 9: print('GAP', a['start'], b['start'], round(b['start'] - a['start'], 1))
for a, b in zip(gfx, gfx[1:]):
    if b['t'] < a['t'] + a['dur'] - 0.1: print('OVERLAP', a.get('text', a.get('title', a.get('label'))), '|', b.get('text', b.get('title', b.get('label'))))
print(f"{len(segs)} segments, {sum(1 for s in segs if s['type']=='full')} full; {len(gfx)} graphics; END {END}")
