"""words_tight.json -> words_final.json: transcription fixes (captions only; audio untouched)."""
import json
W = json.load(open('work/words_tight.json'))
out = []
i = 0
while i < len(W):
    w = dict(W[i]); t = w['w']
    if t == 'DMS': w['w'] = "DMs"
    if t == 'y' and i + 1 < len(W) and W[i+1]['w'] == "'all":
        w['w'] = "y'all"; w['e'] = W[i+1]['e']; i += 1
    # "be around a bush" is how whisper heard "beat around the bush"
    if t == 'be' and i + 3 < len(W) and [x['w'] for x in W[i+1:i+4]] == ['around', 'a', 'bush']:
        w['w'] = 'beat'; out.append(w); out.append(dict(W[i+1])); a = dict(W[i+2]); a['w'] = 'the'; out.append(a); out.append(dict(W[i+3])); i += 4; continue
    if t == 'know' and i + 1 < len(W) and W[i+1]['w'] == 'big' and out and out[-1]['w'] == "ain't":
        w['w'] = 'no'
    out.append(w); i += 1
json.dump(out, open('work/words_final.json', 'w'))
print(' '.join(x['w'] for x in out))
