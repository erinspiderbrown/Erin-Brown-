"""Blurred cover background from a real photo with the athlete painted out (no ghost behind the cut-out).
usage: cleanbg.py photo.jpg out.jpg [model=u2net_human_seg] [scale_extra=1.15] [blur=14]"""
import sys, numpy as np, cv2
from PIL import Image, ImageFilter
from rembg import remove, new_session
src, out = sys.argv[1], sys.argv[2]; model = sys.argv[3] if len(sys.argv) > 3 else 'u2net_human_seg'
ex = float(sys.argv[4]) if len(sys.argv) > 4 else 1.15; blur = float(sys.argv[5]) if len(sys.argv) > 5 else 14
im = Image.open(src).convert('RGB'); im.thumbnail((1600, 1600))
m = np.array(remove(im, session=new_session(model)).split()[-1]) > 40
m = cv2.dilate(m.astype(np.uint8) * 255, np.ones((41, 41), np.uint8))
a = cv2.inpaint(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR), m, 25, cv2.INPAINT_TELEA)
im = Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB))
s = max(1080 / im.width, 1920 / im.height) * ex; im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
x = (im.width - 1080) // 2; y = (im.height - 1920) // 2
im.crop((x, y, x + 1080, y + 1920)).filter(ImageFilter.GaussianBlur(blur)).save(out, quality=95); print('wrote', out)
