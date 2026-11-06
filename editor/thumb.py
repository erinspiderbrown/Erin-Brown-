"""High-effort TikTok thumbnails in the owner's reference style (see CLAUDE.md, step 8).

usage: python3 thumb.py spec.json

Style (from the owner's examples): no text; one or two REAL dramatic moments, big in frame; two photos stacked
with a clean diagonal white line; punchy, vivid, crisp grade; every source at native resolution (never enlarged
past ~1.1x). Writes both a 3:4 (1080x1440, profile-grid cover) and a 9:16 (1080x1920, upload cover) version.

spec:
  out:    "exports/thumbnails/<name>"   (writes <name>_thumb.jpg = 3:4 and <name>_thumb_916.jpg = 9:16)
  panels: [ {src, cx, cy, zoom, bw?}, {src, cx, cy, zoom} ]   one or two panels, top then bottom.
          cx, cy = the point (in source pixels) to centre in the panel; zoom = scale applied to the source
          (<= 1 keeps it sharp; a warning prints above 1.1).
  split:  fraction of the height where the diagonal line crosses the centre (default 0.5)
  tilt:   pixels the line drops from left to right (default -110: rises to the right, like the reference)
  grade:  {contrast, color, sharp, warmth}  defaults 1.12, 1.22, 1.0, 0.04
"""
import json, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageChops


def grade(im, g, bw=False):
    im = im.convert('RGB')
    if bw:
        im = ImageEnhance.Contrast(im.convert('L').convert('RGB')).enhance(g.get('contrast', 1.12) + .12)
    else:
        im = ImageEnhance.Contrast(im).enhance(g.get('contrast', 1.12))
        im = ImageEnhance.Color(im).enhance(g.get('color', 1.22))
        w = g.get('warmth', .04)
        if w:
            r, gg, b = im.split()
            r = r.point(lambda v: min(255, v * (1 + w))); b = b.point(lambda v: v * (1 - w * .6))
            im = Image.merge('RGB', (r, gg, b))
    # clarity: local-contrast boost (large-radius unsharp), then fine sharpening
    im = im.filter(ImageFilter.UnsharpMask(radius=40, percent=16, threshold=0))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=int(60 * g.get('sharp', 1.0)), threshold=2))
    return im


def panel(p, W, H, g):
    src = Image.open(p['src'])
    z = float(p.get('zoom', 1.0))
    if z > 1.1: print(f"WARNING: {p['src']} enlarged {z:.2f}x (soft)")
    src = src.convert('RGB').resize((round(src.width * z), round(src.height * z)), Image.LANCZOS)
    cx, cy = p['cx'] * z, p['cy'] * z
    x = int(min(max(cx - W / 2, 0), src.width - W)); y = int(min(max(cy - H / 2, 0), src.height - H))
    if src.width < W or src.height < H: sys.exit(f"{p['src']}: zoom {z} too small to cover {W}x{H}")
    return grade(src.crop((x, y, x + W, y + H)), g, p.get('bw'))


def build(spec, W, H):
    g = spec.get('grade', {})
    P = spec['panels']
    if len(P) == 1:
        return panel(P[0], W, H, g)
    split = spec.get('split', .5) * H; tilt = spec.get('tilt', -110) * H / 1920
    yl, yr = split - tilt / 2, split + tilt / 2                       # line endpoints at left / right edge
    top = panel(P[0], W, int(max(yl, yr)) + 40, g)
    bh = H - int(min(yl, yr)) + 40
    bot = panel(P[1], W, bh, g)
    c = Image.new('RGB', (W, H)); c.paste(top, (0, 0))
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(0, yl), (W, yr), (W, H), (0, H)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(.8))
    bl = Image.new('RGB', (W, H)); bl.paste(bot, (0, H - bh))
    c = Image.composite(bl, c, m)
    # soft shadow under the line, then the crisp white line itself
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).line([(0, yl + 10), (W, yr + 10)], fill=150, width=26)
    c = Image.composite(Image.new('RGB', (W, H)), c, sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(c); d.line([(0, yl), (W, yr)], fill=(255, 255, 255), width=round(9 * W / 1080))
    return c


def main(path):
    spec = json.load(open(path))
    for (W, H), suffix in (((1080, 1440), '_thumb.jpg'), ((1080, 1920), '_thumb_916.jpg')):
        out = spec['out'] + suffix
        build(spec, W, H).save(out, quality=96, subsampling=0)
        print('wrote', out)


if __name__ == '__main__':
    main(sys.argv[1])
