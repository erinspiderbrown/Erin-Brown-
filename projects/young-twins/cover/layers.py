"""Cover layers from the USA TODAY Network / VC Star photo of Leo Young winning the 2023 USATF U20 XC title
(8001x5334; downscaled only): graded background + cut-out subject for cover/cover.html."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from rembg import remove, new_session
W, H = 1080, 1920
P = Image.open('br/leo_usatf.jpg').convert('RGB'); P = P.resize((P.width // 2, P.height // 2), Image.LANCZOS)   # 4000x2667: still > canvas
def film(im, warm=1.0):
    a = np.asarray(im).astype(np.float32) / 255
    a = a + 0.14 * (a - 0.5) * (1 - np.abs(2 * a - 1))
    lum = a.mean(axis=2, keepdims=True)
    a = a * (1 - 0.15) + lum * 0.15
    a[..., 0] += 0.03 * warm * lum[..., 0]; a[..., 2] += 0.05 * (1 - lum[..., 0]) - 0.02
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
cx = int(P.width * 0.5); half = int(P.height * 9 / 32)
crop = P.crop((cx - half, 0, cx + half, P.height))                      # 9:16 window around him (1542x2742)
wide = P.crop((cx - 1300, 0, min(P.width, cx + 1300), P.height))           # wider window so both hands stay in
m = remove(wide, session=new_session('u2net_human_seg'), only_mask=True).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
a = np.array(m); from scipy import ndimage
lab, n = ndimage.label(a > 96)
if n > 1:
    big = 1 + int(np.argmax(ndimage.sum(np.ones_like(a), lab, range(1, n + 1)))); m = Image.fromarray((a * (lab == big)).astype('uint8'))
subj = film(ImageEnhance.Sharpness(wide).enhance(1.15), 1.2).convert('RGBA'); subj.putalpha(m)
bb = m.point(lambda v: 255 if v > 40 else 0).getbbox(); subj = subj.crop(bb); subj.save('cover/subject.png')
bg = crop.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(18))
bg = film(ImageEnhance.Brightness(bg).enhance(0.55), 0.6); bg.save('cover/bg.jpg', quality=95)
print('subject', subj.size, 'bbox in crop', bb)
