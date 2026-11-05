"""Turn a finished 16:9 YouTube edit into a vertical 1080x1920 TikTok.

usage: python3 vertical.py plan.json

The full widescreen frame stays intact and sharp (scaled to 1080 wide; never cropped or enlarged),
on a dark canvas with: a chapter header on top, word-by-word captions below the frame, and a
progress bar at the bottom. Cuts are joined with short audio crossfades so the music bed doesn't jump.

plan keys:
  src        16:9 source video (the finished YouTube edit, voice + music mixed)
  words      transcript JSON in SOURCE time (transcribe.py output)
  keep       [[start, end], ...] source ranges to keep, in order
  chapters   [[source_time, "TITLE", "SUB"], ...]; the header shows the latest chapter
  title      fallback header title, e.g. "JON DRUMMOND"
  output     output .mp4
  frame_y    top of the 16:9 frame (default 600)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build   # caption styling shared with the split-screen editor

W, H, FPS, XF = 1080, 1920, 30, 0.12
FW = 1180                      # frame scaled to 1180 wide, then the outer 50 px each side (HUD corners) trimmed
FH = round(FW * 9 / 16 / 2) * 2


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"FAILED: {' '.join(cmd[:6])}...\n{r.stderr[-3000:]}")
    return r


def remap(plan):
    """source time -> output time over the kept ranges (crossfades shorten each joint by XF)."""
    keep = plan['keep']
    def f(t):
        acc = 0.0
        for i, (a, b) in enumerate(keep):
            if a <= t <= b: return acc + t - a
            acc += (b - a) - (XF if i < len(keep) - 1 else 0)
        return None
    total = sum(b - a for a, b in keep) - XF * (len(keep) - 1)
    return f, total


def ass_file(plan, path, total, f):
    style = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style.json')))
    fonts = style.get('caption_font', 'Montserrat Black')
    fy = int(plan.get('frame_y', 600)); fh = FH
    words = []
    for w in json.load(open(plan['words'])):
        s, e = f(w['s']), f(w['e'])
        if s is not None and e is not None and e > s: words.append({**w, 's': s, 'e': e})
    cap_y = fy + fh + 140
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{fonts},84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H50000000,0,0,0,0,100,100,1,0,1,6,3,5,40,40,0,1
Style: Head,Anton,124,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,40,40,0,1
Style: Sub,Montserrat ExtraBold,38,{build.hex2ass(style['caption_colors'][-1]).rstrip('&').replace('&H', '&H00')},&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,3,0,1,0,0,5,40,40,0,1
Style: Chap,Montserrat ExtraBold,30,&H00AFAFAF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,4,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = build.caption_events(words, 0, total, style['caption_colors'], cap_y)
    # chapter header: title + sub, animated in at each chapter change
    def snap(t):   # a chapter that starts inside a cut begins at the next kept moment
        if f(t) is not None: return f(t)
        nxt = [a for a, b in plan['keep'] if a >= t]
        return f(nxt[0]) if nxt else None
    chs = [(snap(t), ti, sub) for t, ti, sub in plan.get('chapters', [])]
    chs = [c for c in chs if c[0] is not None] or [(0.0, plan.get('title', ''), '')]
    if chs[0][0] > 0: chs.insert(0, (0.0, plan.get('title', ''), plan.get('subtitle', '')))
    for i, (t, ti, sub) in enumerate(chs):
        end = chs[i + 1][0] if i + 1 < len(chs) else total
        anim = r'\fscx80\fscy80\alpha&HFF&\t(0,220,\fscx100\fscy100\alpha&H00&)'
        ev.append(f'Dialogue: 3,{build.ts(t)},{build.ts(end)},Head,,0,0,0,,{{\\an5\\pos({W//2},{fy-210}){anim}}}{ti}')
        if sub: ev.append(f'Dialogue: 3,{build.ts(t+0.1)},{build.ts(end)},Sub,,0,0,0,,{{\\an5\\pos({W//2},{fy-110})\\alpha&HFF&\\t(0,260,\\alpha&H00&)}}{sub}')
        label = f'PART {i + 1} / {len(chs)}' if len(chs) > 1 else ''
        if label: ev.append(f'Dialogue: 3,{build.ts(t)},{build.ts(end)},Chap,,0,0,0,,{{\\an7\\pos(90,{H-330})}}{label}')
    open(path, 'w').write(hdr + '\n'.join(ev) + '\n')


def main(plan_path):
    plan = json.load(open(plan_path))
    wd = plan.get('workdir', 'vwork'); os.makedirs(wd, exist_ok=True)
    f, total = remap(plan)
    fy = int(plan.get('frame_y', 600))
    # 1) cut + join (video concat; audio crossfaded at each joint)
    keep = plan['keep']; fc = []
    for i, (a, b) in enumerate(keep):
        fc.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps={FPS}[v{i}]")
        fc.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]")
    vlast, alast = 'v0', 'a0'; acc = keep[0][1] - keep[0][0]
    for i in range(1, len(keep)):
        fc.append(f"[{vlast}][v{i}]xfade=transition=fade:duration={XF}:offset={acc - XF:.3f}[vx{i}]")
        fc.append(f"[{alast}][a{i}]acrossfade=d={XF}:c1=tri:c2=tri[ax{i}]")
        vlast, alast = f'vx{i}', f'ax{i}'; acc += (keep[i][1] - keep[i][0]) - XF
    ass = f'{wd}/vertical.ass'; ass_file(plan, ass, total, f)
    fontsdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/fonts')
    bar_y, bar_x, bar_w = H - 280, 90, W - 180
    fc.append(f"color=c=0x0d0e13:s={W}x{H}:r={FPS}:d={total:.3f}[bg]")
    fc.append(f"[{vlast}]scale={FW}:{FH}:flags=lanczos,crop={W}:{FH}:{(FW-W)//2}:0,setsar=1[fr]")
    fc.append(f"color=c=0xE8231E:s={bar_w}x10:r={FPS}:d={total:.3f}[bar]")
    fc.append(f"[bg][fr]overlay=0:{fy}:shortest=1,"
              f"drawbox=x=0:y={fy-2}:w={W}:h=2:color=white@0.22:t=fill,drawbox=x=0:y={fy+FH}:w={W}:h=2:color=white@0.22:t=fill,"
              f"drawbox=x={bar_x}:y={bar_y}:w={bar_w}:h=10:color=white@0.16:t=fill[base];"
              f"[base][bar]overlay=x='{bar_x}-{bar_w}+{bar_w}*t/{total:.3f}':y={bar_y}:shortest=1,"   # progress fills left to right
              f"drawbox=x=0:y={bar_y}:w={bar_x}:h=10:color=0x0d0e13:t=fill,"                     # mask the part left of the bar
              f"ass={ass}:fontsdir={fontsdir},format=yuv420p[v]")
    # 2) audio: the owner's mix, never turned down (house rule). Boost to -14 only if quieter.
    pre = f'{wd}/audio_cut.wav'
    run(['ffmpeg', '-v', 'error', '-y', '-i', plan['src'], '-filter_complex', ';'.join(
        [x for x in fc if x.startswith('[0:a]') or 'acrossfade' in x]), '-map', f'[{alast}]', '-c:a', 'pcm_s24le', pre])
    meas = run(['ffmpeg', '-hide_banner', '-i', pre, '-af', 'ebur128=peak=true', '-f', 'null', '-'])
    import re
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', meas.stderr)[-1]); pk = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', meas.stderr)[-1])
    if I < -14.0: af = f'volume={-14.0 - I:.2f}dB,alimiter=limit=0.94:level=disabled'
    elif pk > -0.5: af = f'volume={-0.5 - pk:.2f}dB'
    else: af = 'anull'
    print(f'audio: {I:.1f} LUFS, peak {pk:.1f} dBFS -> {af}')
    vfc = [x for x in fc if not (x.startswith('[0:a]') or 'acrossfade' in x)]
    run(['ffmpeg', '-v', 'error', '-y', '-i', plan['src'], '-i', pre, '-filter_complex', ';'.join(vfc) + f';[1:a]{af}[a]',
         '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-profile:v', 'high',
         '-r', str(FPS), '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', plan['output']])
    print(f"wrote {plan['output']} ({total:.1f}s)")


if __name__ == '__main__':
    main(sys.argv[1])
