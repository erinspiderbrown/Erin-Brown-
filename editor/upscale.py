"""Neural 2x upscale of a low-res clip: light denoise -> FSRCNN x2 -> fine sharpen -> near-lossless H.264.
Used for owner clips below 1080p (bottom half of the split only; the rules still forbid them full-screen).
usage: python3 editor/upscale.py in.mov out.mp4 [prefilter]   (prefilter: extra ffmpeg filters, e.g. a crop, applied first)"""
import subprocess, sys, json, os
import cv2, numpy as np

src, out = sys.argv[1], sys.argv[2]
pre = sys.argv[3] if len(sys.argv) > 3 else ''
MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'models', 'FSRCNN_x2.pb')   # setup.sh downloads it

vf = ','.join(x for x in [pre, 'fps=30', 'hqdn3d=1.5:1.5:3:3', 'format=bgr24'] if x)
probe = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', vf, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                       capture_output=True).stdout
first = cv2.imdecode(np.frombuffer(probe, np.uint8), cv2.IMREAD_COLOR)
h, w = first.shape[:2]
sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel(MODEL); sr.setModel('fsrcnn', 2)
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', vf, '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
W, H = w * 2 // 2 * 2, h * 2 // 2 * 2
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                        '-i', src, '-map', '0:v', '-map', '1:a?', '-c:a', 'aac', '-b:a', '256k', '-shortest',
                        '-c:v', 'libx264', '-crf', '10', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
n = 0
while True:
    buf = dec.stdout.read(w * h * 3)
    if len(buf) < w * h * 3: break
    f = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    up = sr.upsample(f)[:H, :W]
    blur = cv2.GaussianBlur(up, (0, 0), 1.2)
    up = cv2.addWeighted(up, 1.45, blur, -0.45, 0)          # fine sharpen (unsharp mask)
    enc.stdin.write(up.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print(f'{src}: {w}x{h} -> {W}x{H}, {n} frames')
