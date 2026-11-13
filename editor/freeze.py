"""Freeze-frame pop-out (top sports Shorts move): the shot freezes with a white flash, the background drops dark, desaturated
and soft, and the athlete pops out of it with a white edge and a glow, slowly pushing in. Replaces name tags as the way to
"introduce" a person or land a big moment (owner, Nov 2026: no name tags, no cliche stamps, "step our editing up").

usage: python3 editor/freeze.py spec.json
spec: {src, ss (s, for video), out (.mp4), dur (default 1.6), focus [x,y] 0..1 for the 9:16 crop,
       pick [x,y] 0..1 in the 1080x1920 frame: keep only the cut-out blob nearest this point (one athlete among several),
       glow [r,g,b] (default yellow), push (end zoom, default 1.07),
       keep_x [x0,x1] 0..1: keep only this horizontal band of the cut-out (for people who touch)}
Output: 1080x1920, 30 fps, no audio; use it as the broll src of a 'full' segment. Real frame, nothing generated.
"""
import json, sys, os, subprocess, io
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from scipy import ndimage

W, H, FPS = 1080, 1920, 30


def frame(src, ss):
    if src.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        return ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', src, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                         capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(png)).convert('RGB')


def cover(im, fx, fy):
    s = max(W / im.width, H / im.height)
    if s > 1.001: print(f'NOTE: source enlarged {s:.2f}x to fill 9:16')
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int(np.clip(fx * im.width - W / 2, 0, im.width - W)); y = int(np.clip(fy * im.height - H / 2, 0, im.height - H))
    return im.crop((x, y, x + W, y + H))


def cutout(im, pick, keep_x=None):
    from rembg import remove, new_session
    a = np.array(remove(im, session=new_session('isnet-general-use')).getchannel('A'))
    m = a > 150
    if keep_x:                       # people touching/hugging: keep only this horizontal band (fractions of the width)
        x0, x1 = int(keep_x[0] * W), int(keep_x[1] * W); m[:, :x0] = False; m[:, x1:] = False
    if pick is not None:
        # opening strips thin stuff rembg sometimes keeps (lane lines, hurdles) and splits athletes that only touch,
        # then the blob nearest `pick` is grown back inside the original mask
        r = int(pick[2]) if len(pick) > 2 else 5
        st = ndimage.generate_binary_structure(2, 1)
        mo = ndimage.binary_opening(m, structure=st, iterations=r)
        lab, n = ndimage.label(mo)
        if n:
            px, py = int(pick[0] * W), int(pick[1] * H)
            ys, xs = np.nonzero(lab)
            d = (xs - px) ** 2 + (ys - py) ** 2
            keep = lab == lab[ys[d.argmin()], xs[d.argmin()]]
            m = ndimage.binary_dilation(keep, structure=st, iterations=r + 2) & m
    return Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))


def main(sp):
    S = json.load(open(sp)); dur = S.get('dur', 1.6); push = S.get('push', 1.07); glow = tuple(S.get('glow', [255, 225, 26]))
    fx, fy = S.get('focus', [0.5, 0.5])
    base = cover(frame(S['src'], S.get('ss', 0)), fx, fy)
    mask = cutout(base, S.get('pick'), S.get('keep_x'))
    subj = base.copy(); subj.putalpha(mask)
    bb = mask.getbbox(); cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    # outline + glow layers built once
    edge = mask.filter(ImageFilter.MaxFilter(13))
    white = Image.new('RGBA', (W, H), (255, 255, 255, 0)); white.putalpha(edge)
    g = Image.new('RGBA', (W, H), glow + (0,)); g.putalpha(edge.filter(ImageFilter.GaussianBlur(26)).point(lambda v: min(255, int(v * 1.6))))
    pop = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pop.alpha_composite(g); pop.alpha_composite(white); pop.alpha_composite(subj)
    dark = ImageEnhance.Brightness(ImageEnhance.Color(base).enhance(0.15)).enhance(0.38).filter(ImageFilter.GaussianBlur(7))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', S['out']], stdin=subprocess.PIPE)
    n = round(dur * FPS)
    for i in range(n):
        t = i / FPS
        k = min(1, t / 0.22); k = 1 - (1 - k) ** 3                       # background falls away over 0.22 s
        bg = Image.blend(base, dark, k)
        z = 1 + (push - 1) * (1 - (1 - min(1, t / dur)) ** 2)            # slow push-in on the subject
        s = 1 + 0.06 * (1 - min(1, t / 0.18)) ** 2 if t < 0.18 else 1    # tiny pop on the freeze
        sc = z * s
        layer = pop.resize((round(W * sc), round(H * sc)), Image.LANCZOS)
        ox, oy = round(cx - cx * sc), round(cy - cy * sc)
        fr = bg.convert('RGBA'); fr.alpha_composite(layer, (max(ox, 0), max(oy, 0)), (max(-ox, 0), max(-oy, 0)))
        if t < 0.12:                                                       # white flash on the freeze
            fr = Image.blend(fr, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.55 * (1 - t / 0.12))
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    print('wrote', S['out'], f'{n} frames')


if __name__ == '__main__':
    main(sys.argv[1])
