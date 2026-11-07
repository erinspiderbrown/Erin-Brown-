"""AI-upscale low-res clips or photos with Real-ESRGAN (general x4 v3), locally on CPU via onnxruntime.
No credits, no generation: it sharpens and reconstructs detail in the owner's own footage.

usage:
  python3 enhance.py <in.mp4|in.jpg> <out.mp4|out.jpg> [--ss S] [--t T] [--w W] [--h H]
    --ss/--t   only this time range of a video (keeps audio for that range)
    --w/--h    final size (default: fit 4x result inside 1080x1920 for vertical, 1920x1080 for landscape;
               photos keep the full 4x size, capped at 4000 px on the long side)

The model takes fixed 128x128 tiles. Frames are cut into overlapping tiles (16 px), upscaled, and blended
with a feathered weight so no seams show. Model: editor/assets/models/real_esrgan_general_x4v3.onnx
(setup.sh downloads it)."""
import argparse, os, subprocess, sys, json
import numpy as np
import onnxruntime as ort

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, 'assets', 'models', 'real_esrgan_general_x4v3.onnx')
T, OV, S = 128, 16, 4                     # tile, overlap, scale

def session():
    o = ort.SessionOptions(); o.intra_op_num_threads = os.cpu_count() or 4
    return ort.InferenceSession(MODEL, o, providers=['CPUExecutionProvider'])

def _ramp(n, ov):
    w = np.ones(n, np.float32); r = np.linspace(0.05, 1, ov, dtype=np.float32)
    w[:ov] = r; w[-ov:] = r[::-1]; return w

WIN = np.outer(_ramp(T * S, OV * S), _ramp(T * S, OV * S))[None]

def upscale(sess, img):
    """img: HxWx3 uint8 RGB -> (4H)x(4W)x3 uint8"""
    h, w, _ = img.shape
    ph, pw = max(T, h), max(T, w)
    x = np.zeros((ph, pw, 3), np.float32); x[:h, :w] = img / 255.0
    x = np.pad(x, ((0, (-(ph - T)) % (T - OV)), (0, (-(pw - T)) % (T - OV)), (0, 0)), mode='edge')
    H, W = x.shape[:2]
    acc = np.zeros((3, H * S, W * S), np.float32); wt = np.zeros((1, H * S, W * S), np.float32)
    for y0 in range(0, H - T + 1, T - OV):
        for x0 in range(0, W - T + 1, T - OV):
            tile = x[y0:y0 + T, x0:x0 + T].transpose(2, 0, 1)[None]
            out = sess.run(None, {'image': tile})[0][0]
            acc[:, y0 * S:(y0 + T) * S, x0 * S:(x0 + T) * S] += out * WIN
            wt[:, y0 * S:(y0 + T) * S, x0 * S:(x0 + T) * S] += WIN
    y = (acc / np.maximum(wt, 1e-6))[:, :h * S, :w * S].transpose(1, 2, 0)
    return (np.clip(y, 0, 1) * 255 + 0.5).astype(np.uint8)

def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height,r_frame_rate:stream_side_data=rotation', '-of', 'json', path], capture_output=True, text=True)
    st = json.loads(r.stdout)['streams'][0]
    rot = abs(int(float(next((d.get('rotation', 0) for d in st.get('side_data_list', [])), 0))))
    w, h = (st['height'], st['width']) if rot in (90, 270) else (st['width'], st['height'])
    n, d = st['r_frame_rate'].split('/'); return w, h, float(n) / float(d)

def fit(w, h, W=None, H=None):
    if W and H: return W, H
    bw, bh = (1080, 1920) if h >= w else (1920, 1080)
    k = min(bw / w, bh / h); return int(w * k) // 2 * 2, int(h * k) // 2 * 2

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--ss', type=float, default=0); ap.add_argument('--t', type=float)
    ap.add_argument('--w', type=int); ap.add_argument('--h', type=int); a = ap.parse_args()
    sess = session(); w, h, fps = probe(a.src)
    if a.src.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        up = upscale(sess, np.frombuffer(raw, np.uint8).reshape(h, w, 3))
        k = min(1.0, 4000 / max(up.shape[:2])); W, H = (a.w, a.h) if a.w else (int(up.shape[1] * k), int(up.shape[0] * k))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{up.shape[1]}x{up.shape[0]}', '-i', '-',
                        '-vf', f'scale={W}:{H}:flags=lanczos', '-q:v', '2', a.out], input=up.tobytes(), check=True)
        print(f'{a.src}: {w}x{h} -> {W}x{H}'); return
    W, H = fit(w * S, h * S, a.w, a.h)
    rng = ['-ss', str(a.ss)] + (['-t', str(a.t)] if a.t else [])
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', *rng, '-i', a.src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    tmp = a.out + '.noaudio.mkv'           # MKV: still readable if the job is interrupted
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w * S}x{h * S}', '-r', f'{fps:.3f}',
                            '-i', '-', '-vf', f'scale={W}:{H}:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', tmp],
                           stdin=subprocess.PIPE)
    n, fb = 0, w * h * 3
    while True:
        buf = dec.stdout.read(fb)
        if len(buf) < fb: break
        enc.stdin.write(upscale(sess, np.frombuffer(buf, np.uint8).reshape(h, w, 3)).tobytes()); n += 1
        if n % 30 == 0: print(f'  {n} frames', file=sys.stderr, flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, *rng, '-i', a.src, '-map', '0:v', '-map', '1:a?', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', a.out], check=True)
    os.remove(tmp); print(f'{a.src}: {w}x{h} -> {W}x{H}, {n} frames')

if __name__ == '__main__':
    main()
