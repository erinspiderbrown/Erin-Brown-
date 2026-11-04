"""One-off: turn us-atlas states-albers-10m.json (pre-projected TopoJSON, 975x610, US Census boundaries)
into datagfx/us_states.js (window.US_STATES = {name: svg path}). Used by the `usmap` motion graphic.
usage: python3 make_usmap.py states-albers-10m.json"""
import json, sys
d = json.load(open(sys.argv[1]))
sx, sy = d['transform']['scale']; tx, ty = d['transform']['translate']
arcs = []
for a in d['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
    arcs.append(pts)
def arc(i): return arcs[i] if i >= 0 else arcs[~i][::-1]
def ring(r):
    pts = []
    for i in r:
        p = arc(i); pts += p if not pts else p[1:]
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'
out = {}
for g in d['objects']['states']['geometries']:
    polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
    out[g['properties']['name']] = ''.join(ring(r) for p in polys for r in p)
open('datagfx/us_states.js', 'w').write('window.US_STATES=' + json.dumps(out, separators=(',', ':')) + ';\n')
print(len(out), 'states,', sum(map(len, out.values())) // 1024, 'KB')
