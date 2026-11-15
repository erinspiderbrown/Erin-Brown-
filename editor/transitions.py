"""Viral-style transitions, rendered as short standalone clips from the last/first frames of two segments.

Each transition gets two windows of equal length d covering the SAME stretch of the timeline:
  A = outgoing segment, B = incoming segment. The clip it produces replaces that stretch.

kinds
  whip    fast whip-pan: slide + heavy directional motion blur + frame smear   (dir: left/right/up/down)
  zoom    zoom-through: A punches in hard with blur, B lands from zoomed-in
  spin    rotational whip with zoom + blur
  glitch  RGB split + jitter + slice offsets, hard switch mid-way
  flash   bloom to white and back
  shake   hard cut with camera shake + zoom punch on the incoming shot
  swipe   = whip, but only on the bottom half (split-screen B-roll swaps; your face stays still)
  cut     plain cut (no clip)
"""
import math, subprocess, sys

W, H, FPS = 1080, 1920, 30
HALF = H // 2
DUR = {'whip': 0.34, 'zoom': 0.40, 'spin': 0.44, 'glitch': 0.30, 'flash': 0.40, 'shake': 0.36, 'swipe': 0.30, 'cut': 0.0}


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"transition FAILED: {' '.join(cmd)}\n{r.stderr[-2500:]}")


def _cmds(name, prop, d, fn, fps=FPS):
    """sendcmd script ramping filter `name`'s `prop` by fn(p), p in [0,1] over the clip."""
    n = max(2, int(round(d * fps)))
    return ';'.join(f"{i / fps:.4f} {name} {prop} {fn(i / (n - 1)):.2f}" for i in range(n))


def _mix(d, c=0.10):
    """blend expression factor: 0 -> 1 crossfade of width c centred at d/2 (T = clip time)."""
    return f"clip((T-{d / 2 - c / 2:.4f})/{c:.4f},0,1)"


def _zoom(w, h, zexpr, rot=None):
    """time-varying zoom (and optional rotation) that always covers the frame."""
    f = [f"scale=w='trunc({w}*({zexpr})/2)*2':h=-2:eval=frame:flags=bicubic", f"crop={w}:{h}"]
    if rot: f.insert(1, f"rotate=a='{rot}':ow=iw:oh=ih:c=black")
    return ','.join(f)


def graph(kind, d, w, h, direction=None):
    """filtergraph from [0:v]=A window, [1:v]=B window to [v]."""
    bell = lambda p: math.sin(math.pi * p) ** 2
    if kind in ('whip', 'swipe'):
        dr = direction or 'left'
        xf = {'left': 'slideleft', 'right': 'slideright', 'up': 'slideup', 'down': 'slidedown'}[dr]
        ang = 0 if dr in ('left', 'right') else 90
        peak = 75 if kind == 'whip' else 55
        return (f"[0:v]setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];"
                f"[a][b]xfade=transition={xf}:duration={d * 0.9:.3f}:offset={d * 0.05:.3f},"
                f"sendcmd=c='{_cmds('dblur@w', 'radius', d, lambda p: peak * bell(p) ** 2)}',dblur@w=angle={ang}:radius=0,"
                f"tmix=frames=3:weights='1 2 1',setsar=1[v]")
    if kind == 'zoom':
        za = f"1+1.1*pow(min(t/{d / 2:.3f},1.1),2)"
        zb = f"1+0.7*pow(max(0,({d:.3f}-t)/{d / 2:.3f}),2)"
        return (f"[0:v]setpts=PTS-STARTPTS,{_zoom(w, h, za)},format=gbrp[a];"
                f"[1:v]setpts=PTS-STARTPTS,{_zoom(w, h, zb)},format=gbrp[b];"
                f"[a][b]blend=all_expr='A*(1-{_mix(d)})+B*{_mix(d)}',"
                f"sendcmd=c='{_cmds('gblur@z', 'sigma', d, lambda p: 26 * bell(p))}',gblur@z=sigma=0,"
                f"tmix=frames=2,format=yuv420p,setsar=1[v]")
    if kind == 'spin':
        th = 0.55
        za = f"1+1.0*pow(min(t/{d / 2:.3f},1.1),2)"
        zb = f"1+1.0*pow(max(0,({d:.3f}-t)/{d / 2:.3f}),2)"
        ra = f"{th}*pow(min(t/{d / 2:.3f},1.1),2)"
        rb = f"-{th}*pow(max(0,({d:.3f}-t)/{d / 2:.3f}),2)"
        return (f"[0:v]setpts=PTS-STARTPTS,scale={int(w * 1.8)}:-2,rotate=a='{ra}':c=black,"
                f"scale=w='trunc({w}*({za})/2)*2':h=-2:eval=frame,crop={w}:{h},format=gbrp[a];"
                f"[1:v]setpts=PTS-STARTPTS,scale={int(w * 1.8)}:-2,rotate=a='{rb}':c=black,"
                f"scale=w='trunc({w}*({zb})/2)*2':h=-2:eval=frame,crop={w}:{h},format=gbrp[b];"
                f"[a][b]blend=all_expr='A*(1-{_mix(d, 0.08)})+B*{_mix(d, 0.08)}',"
                f"sendcmd=c='{_cmds('gblur@s', 'sigma', d, lambda p: 18 * bell(p) ** 2)}',gblur@s=sigma=0,"
                f"tmix=frames=2,format=yuv420p,setsar=1[v]")
    if kind == 'glitch':
        def jit(p, k, a):  # deterministic jitter
            return a * math.sin(37 * p * k + k) * bell(p)
        sh = _cmds('rgbashift@g', 'rh', d, lambda p: jit(p, 3.1, 34)) + ';' + _cmds('rgbashift@g', 'bh', d, lambda p: -jit(p, 2.3, 30))
        return (f"[0:v]setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];"
                f"[a][b]blend=all_expr='if(lt(T,{d / 2:.3f}),A,B)',"
                f"scale={int(w * 1.06)}:-2,crop={w}:{h}:x='(iw-ow)/2+18*sin(t*97)*between(t,{d * .25:.3f},{d * .75:.3f})':"
                f"y='(ih-oh)/2+10*sin(t*71)*between(t,{d * .25:.3f},{d * .75:.3f})',"
                f"sendcmd=c='{sh}',rgbashift@g=rh=0:bh=0:edge=smear,"
                f"noise=alls=14:allf=t:enable='between(t,{d * .3:.3f},{d * .7:.3f})',setsar=1[v]")
    if kind == 'flash':
        wexp = f"exp(-pow((T-{d / 2:.4f})/{d * 0.18:.4f},2))"
        return (f"[0:v]setpts=PTS-STARTPTS,{_zoom(w, h, f'1+0.12*t/{d:.3f}')},format=gbrp[a];"
                f"[1:v]setpts=PTS-STARTPTS,{_zoom(w, h, f'1.08-0.08*t/{d:.3f}')},format=gbrp[b];"
                f"[a][b]blend=all_expr='min(255,(A*(1-{_mix(d, 0.06)})+B*{_mix(d, 0.06)})*(1-{wexp})+255*{wexp})',"
                f"format=yuv420p,setsar=1[v]")
    if kind == 'shake':
        m = d / 2
        za = f"1+0.10*pow(t/{m:.3f},2)"
        return (f"[0:v]setpts=PTS-STARTPTS,{_zoom(w, h, za)}[a0];[1:v]setpts=PTS-STARTPTS[b0];"
                f"[a0][b0]blend=all_expr='if(lt(T,{m:.3f}),A,B)',"
                f"scale={int(w * 1.14)}:-2,crop={w}:{h}:"
                f"x='(iw-ow)/2+if(gte(t,{m:.3f}),34*sin((t-{m:.3f})*90)*exp(-(t-{m:.3f})*14),0)':"
                f"y='(ih-oh)/2+if(gte(t,{m:.3f}),26*cos((t-{m:.3f})*77)*exp(-(t-{m:.3f})*14),0)',"
                f"setsar=1[v]")
    raise ValueError(kind)


def render(kind, a_src, a_ss, b_src, b_ss, d, out, direction=None, half=None):
    """half='bottom': transition only the bottom half; the top comes from B untouched."""
    ins = ['-ss', f'{a_ss:.3f}', '-t', f'{d:.3f}', '-i', a_src, '-ss', f'{b_ss:.3f}', '-t', f'{d:.3f}', '-i', b_src]
    if half == 'bottom':
        g = graph('whip' if kind == 'swipe' else kind, d, W, HALF, direction)
        g = g.replace('[0:v]', '[ab]', 1).replace('[1:v]', '[bb]', 1)
        fc = (f"[0:v]crop={W}:{HALF}:0:{HALF}[ab];[1:v]split[b1][b2];[b1]crop={W}:{HALF}:0:{HALF}[bb];"
              f"[b2]crop={W}:{HALF}:0:0,setpts=PTS-STARTPTS[top];" + g.replace('[v]', '[bot]') +
              f";[top][bot]vstack,format=yuv420p[v]")
    else:
        fc = graph(kind, d, W, H, direction)[:-3] + ',format=yuv420p[v]'
    _run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '[v]', '-r', str(FPS),
          '-frames:v', str(int(round(d * FPS))), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', out])
