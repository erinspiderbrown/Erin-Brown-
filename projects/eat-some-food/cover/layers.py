"""Cover layers from the official Sports Illustrated photo of Mary Cain (3000x1688, downscaled only):
a graded full-bleed background and a cut-out subject PNG, composed in cover/cover.html."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from rembg import remove, new_session
W, H = 1080, 1920
P = Image.open('ph/press/si_cain.jpg').convert('RGB')
def film(im, warm=1.0):
    a = np.asarray(im).astype(np.float32) / 255
    a = a + 0.14 * (a - 0.5) * (1 - np.abs(2 * a - 1))                         # S-curve
    lum = a.mean(axis=2, keepdims=True)
    a = a * (1 - 0.18) + lum * 0.18                                            # slight desat
    a[..., 0] += 0.03 * warm * lum[..., 0]; a[..., 2] += 0.05 * (1 - lum[..., 0]) - 0.02   # warm highs, teal shadows
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
SC = 0.66
Ps = P.resize((int(P.width * SC), int(P.height * SC)), Image.LANCZOS)
m = remove(Ps, session=new_session('u2net_human_seg'), only_mask=True).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
subj = film(ImageEnhance.Sharpness(Ps).enhance(1.3), 1.2).convert('RGBA'); subj.putalpha(m)
bb = m.point(lambda v: 255 if v > 40 else 0).getbbox(); subj = subj.crop(bb); subj.save('cover/subject.png')
bg = P.crop((P.width // 2 - 480, 0, P.width // 2 + 480, P.height)).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(26))
bg = film(ImageEnhance.Brightness(bg).enhance(0.5), 0.6); bg.save('cover/bg.jpg', quality=95)
print('subject', subj.size)
