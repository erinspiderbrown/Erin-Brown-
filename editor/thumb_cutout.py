"""Layered "cut-out" thumbnails (owner, Nov 2026: "I definitely need more complex thumbnails"; he picked cut-out athletes).

usage: python3 editor/thumb_cutout.py spec.json

Real photos only: subjects are cut out of REAL photos (rembg, local, isnet-general-use) and layered over a real,
graded background. Nothing is generated. Writes <out>_thumb.jpg (3:4, 1080x1440) and <out>_thumb_916.jpg (9:16).

spec:
  out:   "exports/thumbnails/<name>"
  bg:    {src, cx, cy, zoom, blur, dark, bottom_shade}   background photo: centre point (source px), zoom, blur radius,
         darkening 0..1, bottom_shade = fraction of the canvas height that fades to black at the bottom (for busts)
  tint:  [r, g, b]                              colour wash over the background (optional)
  layers: [ {cut, h, x, y, stroke, glow, glow_px, dim, flip} ... ]   back to front.
          cut = transparent PNG (subject cut-out). h = height as a fraction of the canvas height (scale is capped
          so a cut-out is never enlarged past 1.1x its source). x, y = where the cut-out's bbox centre-bottom lands,
          as fractions of canvas width/height (y=1.0 sits on the bottom edge). stroke = white outline px.
          glow = [r,g,b] outer glow colour. dim = 0..1 darkening (to push a layer back).
          fade_bottom = fraction of the cut-out's height to fade out at the bottom (e.g. 0.35 for a bust).
          soft_below = from this fraction of the height down, drop the stroke/glow and feather the edges (hides ragged
          clothing edges on busts); soft_px = feather radius.
  per-size overrides: "layers_916": {...index: {key: value}} to adjust positions for 9:16.
"""
import json, sys
from PIL import Image, ImageFilter, ImageEnhance, ImageChops, ImageOps


def cover(im, W, H, cx, cy, zoom):
    im = im.resize((round(im.width * zoom), round(im.height * zoom)), Image.LANCZOS)
    s = max(W / im.width, H / im.height)
    if s > 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); cx, cy = cx * s, cy * s
    x = int(min(max(cx * zoom - W / 2, 0), im.width - W)); y = int(min(max(cy * zoom - H / 2, 0), im.height - H))
    return im.crop((x, y, x + W, y + H))


def background(spec, W, H):
    b = spec['bg']; im = Image.open(b['src']).convert('RGB')
    im = cover(im, W, H, b.get('cx', im.width / 2), b.get('cy', im.height / 2), b.get('zoom', 1.0))
    if b.get('blur'): im = im.filter(ImageFilter.GaussianBlur(b['blur']))
    im = ImageEnhance.Color(im).enhance(1.25); im = ImageEnhance.Contrast(im).enhance(1.15)
    if spec.get('tint'):
        im = Image.blend(im, Image.new('RGB', (W, H), tuple(spec['tint'])), 0.18)
    dark = b.get('dark', 0.35)
    im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), dark)
    # vignette
    v = Image.new('L', (W, H), 0); vv = Image.new('L', (W // 8, H // 8), 255)
    v.paste(vv.resize((int(W * .8), int(H * .8))), (int(W * .1), int(H * .1)))
    v = v.filter(ImageFilter.GaussianBlur(W // 6))
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), v)
    if b.get('bottom_shade'):          # fade the lower part of the background to black so a faded bust dissolves into darkness
        f0 = 1 - b['bottom_shade']; g = Image.new('L', (1, H), 0)
        for yy in range(H):
            r = (yy / H - f0) / max(1e-6, b['bottom_shade'])
            g.putpixel((0, yy), int(255 * min(1, max(0, r)) ** 1.3 * b.get('bottom_shade_max', 0.92)))
        im = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), im, g.resize((W, H)))
    return im


def layer(canvas, L, W, H):
    cut = Image.open(L['cut']).convert('RGBA'); cut = cut.crop(cut.getbbox())
    if L.get('flip'): cut = ImageOps.mirror(cut)
    th = L['h'] * H; s = min(th / cut.height, 1.1)
    cut = cut.resize((round(cut.width * s), round(cut.height * s)), Image.LANCZOS)
    rgb, a = cut.convert('RGB'), cut.getchannel('A')
    fade = None
    if L.get('fade_bottom'):          # dissolve the lowest part of a bust into the frame (hides ragged clothing edges)
        fb = int(cut.height * L['fade_bottom']); fade = Image.new('L', (1, cut.height), 255)
        for yy in range(cut.height - fb, cut.height): fade.putpixel((0, yy), int(255 * ((cut.height - yy) / fb) ** 1.6))
        fade = fade.resize(cut.size)
    rgb = ImageEnhance.Contrast(ImageEnhance.Color(rgb).enhance(1.12)).enhance(1.06)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=2))
    if L.get('dim'): rgb = Image.blend(rgb, Image.new('RGB', rgb.size, (0, 0, 0)), L['dim'])
    pad = 80; cw, ch = cut.width + 2 * pad, cut.height + 2 * pad
    A = Image.new('L', (cw, ch), 0); A.paste(a, (pad, pad))
    F = Image.new('L', (cw, ch), 255)                              # fade mask applied to shadow, glow, stroke AND photo
    if fade: F.paste(fade, (pad, pad)); F.paste(0, (0, pad + cut.height, cw, ch))
    if fade: a = ImageChops.multiply(a, fade)
    if L.get('soft_below'):             # below this fraction of the cut-out's height: no stroke/glow, and soft feathered edges
        y0s = int(cut.height * L['soft_below']); ramp = max(1, int(cut.height * 0.07))
        G = Image.new('L', (1, ch), 255)
        for yy in range(ch):
            r = (yy - pad - y0s) / ramp
            G.putpixel((0, yy), int(255 * min(1, max(0, 1 - r))))
        G = G.resize((cw, ch)); F = ImageChops.multiply(F, G)          # stroke/glow/shadow fade out below the shoulders
        soft = a.filter(ImageFilter.GaussianBlur(int(L.get('soft_px', 22)))).point(lambda v: min(255, int(v * 1.15)))
        a = Image.composite(a, ImageChops.darker(a, soft), G.crop((pad, pad, pad + cut.width, pad + cut.height)))
    x0 = int(L['x'] * W - cw / 2); y0 = int(L['y'] * H - ch + pad)
    # drop shadow
    sh = ImageChops.multiply(A.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * .75)), F)
    canvas.paste(Image.new('RGB', (cw, ch), (0, 0, 0)), (x0 + 14, y0 + 18), sh)
    # coloured outer glow
    if L.get('glow'):
        g = A.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(L.get('glow_px', 26))).point(lambda v: min(255, int(v * 1.6)))
        g = ImageChops.multiply(g, F)
        canvas.paste(Image.new('RGB', (cw, ch), tuple(L['glow'])), (x0, y0), g)
    # white stroke
    st = L.get('stroke', 10)
    if st:
        m = A.point(lambda v: 255 if v > 110 else 0)
        for _ in range(max(1, st // 4)): m = m.filter(ImageFilter.MaxFilter(9))
        m = ImageChops.multiply(m.filter(ImageFilter.GaussianBlur(1.2)), F)
        canvas.paste(Image.new('RGB', (cw, ch), (255, 255, 255)), (x0, y0), m)
    canvas.paste(rgb, (x0 + pad, y0 + pad), a)


def build(spec, W, H, key):
    c = background(spec, W, H)
    layers = [dict(L) for L in spec['layers']]
    for i, o in spec.get(key, {}).items(): layers[int(i)].update(o)
    for L in layers: layer(c, L, W, H)
    return c


def main(path):
    spec = json.load(open(path))
    for (W, H), suffix, key in (((1080, 1440), '_thumb.jpg', 'layers_34'), ((1080, 1920), '_thumb_916.jpg', 'layers_916')):
        out = spec['out'] + suffix
        build(spec, W, H, key).save(out, quality=95, subsampling=0)
        print('wrote', out)


if __name__ == '__main__':
    main(sys.argv[1])
