"""words_cut.json -> words_final.json: merge split numbers, track-time formats, name spellings (Marcell, Kerley, Spazzini, Tortu, Pegoraro)."""
import json, re
W = json.load(open('words_cut.json')); out = []
for w in W:
    if out and re.match(r'^[,.]\d', w['w']): out[-1]['w'] += w['w']; out[-1]['e'] = w['e']; continue
    out.append(dict(w))
TIMES = {'1003': '10.03', '995': '9.95', '994': '9.94', '984': '9.84', '985': '9.85'}
FIX = {'Marcel': 'Marcell', 'Curley': 'Kerley', 'spazzini': 'Spazzini', 'Gio': 'Giacomo', 'torture': 'Tortu', 'lone': 'long',
       'dopest': 'doping', 'persecutor': 'prosecutor', 'Progaro': 'Pegoraro', 'Pergraro': 'Pegoraro', 'Italia': 'Italian', 'Gabriel': 'Gabriele'}
for w in out:
    m = re.match(r"^([A-Za-z0-9]+)(.*)$", w['w'])
    if not m: continue
    core, rest = m.group(1), m.group(2)
    if core in TIMES: w['w'] = TIMES[core] + rest
    elif core in FIX: w['w'] = FIX[core] + rest
for i, w in enumerate(out):
    if w['w'] is None: continue
    if w['w'] == 'Giacomo' and i + 1 < len(out) and out[i + 1]['w'] == 'como': out[i + 1]['w'] = None
    if w['w'] == 'muscle' and i and out[i - 1]['w'] == 'Operation': w['w'] = 'Muscle'
    if w['w'].startswith('bound') and i and out[i - 1]['w'] == 'Muscle': w['w'] = 'Bound' + w['w'][5:]
    if re.match(r"^Jacob(\W|'|$)", w['w']) and not w['w'].startswith('Jacobs'): w['w'] = w['w'].replace('Jacob', 'Jacobs', 1)
out = [w for w in out if w['w']]
json.dump(out, open('words_final.json', 'w'))
print(len(out), 'words')
