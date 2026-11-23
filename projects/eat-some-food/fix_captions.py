"""words_ins.json -> words_final.json (captions only; audio untouched)."""
import json, re
W = json.load(open('work/words_ins.json')); out = []
for w in W:
    w = dict(w)
    if w['w'] == 'cross' : pass
    if w['w'].startswith('-') and out: out[-1]['w'] += w['w']; out[-1]['e'] = w['e']; continue   # cross -country
    out.append(w)
json.dump(out, open('work/words_final.json', 'w'))
print(' '.join(x['w'] for x in out))
