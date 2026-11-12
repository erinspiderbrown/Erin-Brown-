"""words_t.json -> words_final.json: caption fixes (names, hyphenated words, mis-heard words, a dropped 'I')."""
import json, sys
W = json.load(open(sys.argv[1])); out = []
for i, x in enumerate(W):
    t = x['w']
    if out and t.startswith('-') and not t[1:2].isdigit(): out[-1]['w'] += t; out[-1]['e'] = x['e']; continue
    if t == 'when' and i + 1 < len(W) and W[i + 1]['w'] == 'dated': out.append(dict(x, w='wind-aided', e=W[i + 1]['e'])); continue
    if t == 'dated' and out and out[-1]['w'] == 'wind-aided': continue
    t = {'grey': 'great', 'Candice': 'Candace'}.get(t, t)
    if x.get('src') == 'bite_G' and t == 'think' and not (out and out[-1].get('src') == 'bite_G'):
        out.append(dict(x, w='I', s=round(x['s'] - 0.3, 3), e=x['s']))      # "I think..." (the 'I' fell outside the transcript window)
    out.append(dict(x, w=t))
for i, x in enumerate(out):
    if x['w'].lower() == 'baton' and i + 1 < len(out): x['s'] = round(out[i + 1]['s'] - 0.32, 2)
json.dump(out, open(sys.argv[2], 'w')); print(len(out), 'words')
