"""words_tight.json -> words_final.json: caption-only fixes (audio untouched)."""
import json
W = json.load(open('work/words_tight.json')); out = []; i = 0
while i < len(W):
    w = dict(W[i]); t = w['w']
    if t == 'y' and i + 1 < len(W) and W[i+1]['w'] == "'all": w['w'] = "y'all"; w['e'] = W[i+1]['e']; i += 1
    elif t == 'Ryland': w['w'] = 'Rylan'
    elif t == 'Noom': w['w'] = 'Noome'
    elif t == "I'm" and i + 1 < len(W) and W[i+1]['w'] == 'is': w['w'] = "that's"; w['e'] = W[i+1]['e']; i += 1
    elif t == 'backed': w['w'] = 'back'
    elif t == 'double': w['w'] = 'doubled'
    elif t == 'god' and i + 1 < len(W) and W[i+1]['w'] == '-awful': w['w'] = 'god-awful'; w['e'] = W[i+1]['e']; i += 1
    elif t == 'grown' and i + 1 < len(W) and W[i+1]['w'] == '-ass': w['w'] = 'grown-ass'; w['e'] = W[i+1]['e']; i += 1
    out.append(w); i += 1
json.dump(out, open('work/words_final.json', 'w'))
print(' '.join(x['w'] for x in out)[:400])
