"""Place scenes for the Candace Hill doc (2160x3840, sharp full-screen): Natural Earth 1:50m shapes filled with the
flag (US flag for states), glow + outline, a glowing city dot. Reuses the India project's look.
usage: python3 make_maps.py <geo dir>"""
import json, math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
G = sys.argv[1]; W, H = 2160, 3840
countries = {f['properties']['ISO_A2']: f for f in json.load(open(f'{G}/ne50.geojson'))['features']}
states = {f['properties']['name']: f for f in json.load(open(f'{G}/ne50_states.geojson'))['features'] if f['properties'].get('iso_a2') == 'US'}
def rings(feat, keep=None):
    g = feat['geometry']; P = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    out = [p[0] for p in P]; return [r for r in out if (keep(r) if keep else True)]
def km(rs, lat0, lon0): return [[((lon - lon0) * 111.32 * math.cos(math.radians(lat)), (lat - lat0) * 110.57) for lon, lat in r] for r in rs]
def bg(seed):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(12 + 10 * (1 - k)), int(14 + 12 * (1 - k)), int(22 + 22 * (1 - k))))
    for x in range(0, W, 120): d.line([(x, 0), (x, H)], fill=(24, 28, 38), width=2)
    for y in range(0, H, 120): d.line([(0, y), (W, y)], fill=(24, 28, 38), width=2)
    n = Image.effect_noise((W, H), 18).convert('RGB'); return Image.blend(im, ImageChops.multiply(im, n.point(lambda v: 200 + v // 4)), 0.35)
def scene(rs_deg, lat0, lon0, flag, glow, city, out, fill=0.66, cy=0.45):
    R = km(rs_deg, lat0, lon0); xs = [p[0] for r in R for p in r]; ys = [p[1] for r in R for p in r]
    s = min(W * fill / (max(xs) - min(xs)), H * 0.5 / (max(ys) - min(ys)))
    ox = W / 2 - (min(xs) + max(xs)) / 2 * s; oy = H * cy + (min(ys) + max(ys)) / 2 * s
    im = bg(1); pts = [[(ox + x * s, oy - y * s) for x, y in r] for r in R]
    m = Image.new('L', im.size, 0); dm = ImageDraw.Draw(m)
    for r in pts: dm.polygon(r, fill=255)
    bx = m.getbbox()
    im.paste(glow, (0, 0), m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.55)))
    im.paste((0, 0, 0), (18, 30), m.filter(ImageFilter.GaussianBlur(24)).point(lambda v: int(v * 0.6)))
    f = Image.open(flag).convert('RGB').resize((bx[2] - bx[0], bx[3] - bx[1]), Image.LANCZOS)
    layer = Image.new('RGB', im.size); layer.paste(f, bx[:2]); im.paste(layer, (0, 0), m)
    d = ImageDraw.Draw(im)
    for r in pts: d.line(r + [r[0]], fill=(255, 255, 255), width=5, joint='curve')
    if city:
        clat, clon = city; cx = ox + (clon - lon0) * 111.32 * math.cos(math.radians(clat)) * s; cyy = oy - (clat - lat0) * 110.57 * s
        g = Image.new('L', im.size, 0); ImageDraw.Draw(g).ellipse([cx - 90, cyy - 90, cx + 90, cyy + 90], fill=255)
        im.paste((232, 35, 30), (0, 0), g.filter(ImageFilter.GaussianBlur(40)))
        d = ImageDraw.Draw(im); d.ellipse([cx - 34, cyy - 34, cx + 34, cyy + 34], fill=(232, 35, 30), outline=(255, 255, 255), width=10)
    im.save(out, quality=94)
US = f'{G}/flag_us.png'
big = lambda n: lambda r: len(r) > n
scene(rings(states['Washington'], big(30)), 47.4, -120.5, US, (120, 160, 255), (47.756, -122.341), f'{G}/st_wa.jpg')
scene(rings(states['Georgia'], big(30)), 32.7, -83.4, US, (120, 160, 255), (33.667, -84.017), f'{G}/st_ga.jpg')
scene(rings(states['California'], big(30)), 37.2, -119.5, US, (120, 160, 255), None, f'{G}/st_ca.jpg', fill=0.6)
scene(rings(states['Louisiana'], big(30)), 31.0, -92.0, US, (120, 160, 255), (30.451, -91.187), f'{G}/st_la.jpg')
scene(rings(countries['CO'], big(40)), 4.5, -73.5, f'{G}/flag_co.png', (255, 210, 0), (3.451, -76.532), f'{G}/ct_co.jpg', fill=0.6)
scene(rings(countries['PL'], big(40)), 52.0, 19.4, f'{G}/flag_pl.png', (255, 90, 90), (53.123, 18.008), f'{G}/ct_pl.jpg')
print('ok')
