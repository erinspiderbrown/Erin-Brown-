"""Real-photo cover background: crop the photo to the target size, blur its own background slightly, keep the athlete sharp.
usage: python3 make_bg.py photo.jpg out.png W H focus_x focus_y [blur=7] [model=u2net_human_seg]"""
import sys, numpy as np
from PIL import Image, ImageFilter, ImageOps
from rembg import remove, new_session
from scipy import ndimage
src, out, W, H, fx, fy = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
blur = float(sys.argv[7]) if len(sys.argv) > 7 else 7; model = sys.argv[8] if len(sys.argv) > 8 else 'u2net_human_seg'
im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
s = max(W / im.width, H / im.height); print(f'scale {s:.2f}x (keep <= 1.1)')
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
x = round((im.width - W) * fx); y = round((im.height - H) * fy); im = im.crop((x, y, x + W, y + H))
a = np.array(remove(im, session=new_session(model)).split()[-1]) > 120
lab, n = ndimage.label(a); a = lab == (1 + int(np.argmax(ndimage.sum(a, lab, range(1, n + 1)))))
mask = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
bg = im.filter(ImageFilter.GaussianBlur(blur))
Image.composite(im, bg, mask).save(out); print('wrote', out)
