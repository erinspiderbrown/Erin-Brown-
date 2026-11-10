"""Country-map scenes (2160x3840): silhouettes from Natural Earth 1:50m, filled with the national flag, glow + outline,
on a dark textured background. Sinusoidal projection around each country's centre, one shared km scale where compared.
usage: python3 make_maps.py <geo dir>"""
import json, math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
G = sys.argv[1]; W, H = 2160, 3840
feats = {f['properties']['ISO_A2']: f for f in json.load(open(f'{G}/ne50.geojson'))['features']}
def polys(iso, keep=None):
    g = feats[iso]['geometry']; P = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    out = [p[0] for p in P]
    if keep: out = [r for r in out if keep(r)]
    return out
def km(rings, lat0, lon0):
    return [[((lon - lon0) * 111.32 * math.cos(math.radians(lat)), (lat - lat0) * 110.57) for lon, lat in r] for r in rings]
def bg(seed=1):
    rnd = random.Random(seed); im = Image.new('RGB', (W, H), (10, 12, 18)); d = ImageDraw.Draw(im)
    for y in range(H):                                  # vertical gradient
        k = y / H; d.line([(0, y), (W, y)], fill=(int(12 + 10 * (1 - k)), int(14 + 12 * (1 - k)), int(22 + 22 * (1 - k))))
    for x in range(0, W, 120): d.line([(x, 0), (x, H)], fill=(24, 28, 38), width=2)       # faint map grid
    for y in range(0, H, 120): d.line([(0, y), (W, y)], fill=(24, 28, 38), width=2)
    n = Image.effect_noise((W, H), 18).convert('RGB'); im = Image.blend(im, ImageChops.multiply(im, n.point(lambda v: 200 + v // 4)), 0.35)
    return im
def place(rings_km, box):
    xs = [p[0] for r in rings_km for p in r]; ys = [p[1] for r in rings_km for p in r]
    return min(xs), max(xs), min(ys), max(ys)
def draw_country(im, rings_km, flag, s, ox, oy, glow=(255, 255, 255)):
    pts = [[(ox + x * s, oy - y * s) for x, y in r] for r in rings_km]
    m = Image.new('L', im.size, 0); dm = ImageDraw.Draw(m)
    for r in pts: dm.polygon(r, fill=255)
    xs = [p[0] for r in pts for p in r]; ys = [p[1] for r in pts for p in r]
    bx = (int(min(xs)), int(min(ys)), int(max(xs)) + 1, int(max(ys)) + 1)
    gl = m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(40))
    im.paste(glow, (0, 0), gl.point(lambda v: int(v * 0.55)))
    f = Image.open(flag).convert('RGB').resize((max(1, bx[2] - bx[0]), max(1, bx[3] - bx[1])), Image.LANCZOS)
    sh = m.filter(ImageFilter.GaussianBlur(24)); im.paste((0, 0, 0), (18, 30), sh.point(lambda v: int(v * 0.6)))
    layer = Image.new('RGB', im.size); layer.paste(f, bx[:2]); im.paste(layer, (0, 0), m)
    d = ImageDraw.Draw(im)
    for r in pts: d.line(r + [r[0]], fill=(255, 255, 255), width=5, joint='curve')
    return bx
def single(iso, lat0, lon0, flag, glow, out, keep=None, fill=0.80, cy=0.45):
    R = km(polys(iso, keep), lat0, lon0); x0, x1, y0, y1 = place(R, None)
    s = min(W * fill / (x1 - x0), H * 0.55 / (y1 - y0))
    im = bg(hash(iso) % 100); ox = W / 2 - (x0 + x1) / 2 * s; oy = H * cy + (y0 + y1) / 2 * s
    draw_country(im, R, flag, s, ox, oy, glow); im.save(out, quality=94)
main_ring = lambda r: len(r) > 40
single('BW', -22.3, 24.7, f'{G}/flag_bw.png', (110, 200, 255), f'{G}/map_bw.jpg')
single('JM', 18.1, -77.3, f'{G}/flag_jm.png', (255, 210, 0), f'{G}/map_jm.jpg', keep=main_ring)
single('IN', 22.0, 79.0, f'{G}/flag_in.png', (255, 150, 40), f'{G}/map_in.jpg', keep=lambda r: len(r) > 60, fill=0.86)
# same-scale size comparison: India vs Botswana vs Jamaica
im = bg(7); s = 0.52                               # px per km
RI = km(polys('IN', lambda r: len(r) > 60), 22.0, 79.0); RB = km(polys('BW'), -22.3, 24.7); RJ = km(polys('JM', main_ring), 18.1, -77.3)
draw_country(im, RI, f'{G}/flag_in.png', s, W * 0.46, H * 0.34, (255, 150, 40))
draw_country(im, RB, f'{G}/flag_bw.png', s, W * 0.30, H * 0.80, (110, 200, 255))
draw_country(im, RJ, f'{G}/flag_jm.png', s, W * 0.74, H * 0.78, (255, 210, 0))
im.save(f'{G}/size_compare.jpg', quality=94)
print('ok')
