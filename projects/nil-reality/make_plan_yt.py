"""YouTube cut: same edit with the news shots (TikTok-only footage) swapped for licensed Pexels B-roll."""
import json
p = json.load(open('plan.json'))
swap = {8.6: ('br/p34582654.mp4', 2, [0.5, 0.45]), 12.4: ('br/p34514149.mp4', 0, [0.5, 0.5]), 23.0: ('br/p34812214.mp4', 1, [0.5, 0.5]),
        31.1: ('br/p31229035.mp4', 3, [0.5, 0.55]), 50.6: ('br/p32067871.mp4', 1, [0.5, 0.5]), 53.4: ('br/p11123558.mp4', 12, [0.5, 0.6]),
        66.9: ('br/p7362704.mp4', 10, [0.5, 0.5])}
for s in p['segments']:
    if s['start'] in swap:
        a, b, c = swap[s['start']]; s['broll'] = {'src': a, 'ss': b, 'focus': c}
assert not [s for s in p['segments'] if s['broll']['src'].startswith(('news/', 'up/'))]
p['output'] = 'out/nil_reality_yt.mp4'
json.dump(p, open('plan_yt.json', 'w'), indent=1)
