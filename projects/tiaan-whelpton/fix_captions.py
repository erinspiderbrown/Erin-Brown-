"""words_tight.json -> words_final.json (captions only; audio untouched)."""
import json, re
W = json.load(open('work/words_tight.json')); out = []
for w in W:
    w = dict(w)
    if out and re.fullmatch(r'\.\d+[.,]?', w['w']):          # "10" ".28." -> "10.28"
        out[-1]['w'] += w['w'].rstrip('.,'); out[-1]['e'] = w['e']; continue
    out.append(w)
json.dump(out, open('work/words_final.json', 'w'))
print(' '.join(x['w'] for x in out))
