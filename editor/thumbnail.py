"""Render a TikTok cover (1080x1920 JPG) in the house style, from a JSON spec.
usage: python3 thumbnail.py spec.json out.jpg [check.jpg]

spec:
{
  "bg": "path/to/frame.jpg",          # a sharp, real frame from the video (enhance it first if needed)
  "focus": [0.5, 0.5],                # crop point when the image isn't 9:16
  "zoom": 1.0,                        # >1 punches in on the focus point
  "darken": 0.35,                     # 0..1 strength of the top/bottom gradient (text contrast)
  "lines": [                          # big words; keep it to 2-4 words per line, 2-3 lines
    {"text": "LIFTS 300 LB", "y": 300, "size": 170, "color": "#FFE11A"},
    {"text": "RUNS 50.8", "y": 1180, "size": 190, "color": "#FFFFFF", "box": "#E8231E"}
  ],
  "tag": {"text": "PART 3", "y": 120}  # optional small pill
}

Safe zones (TikTok): keep text out of the bottom ~25% (caption/UI) and the right ~140 px (buttons). The profile
grid shows the centre 3:4 (y 240..1680), so key text and the subject's face should sit inside it. The script also
writes a check image (3rd arg, default <out>_check.jpg) with those zones drawn, for review only. Keep it out of exports/."""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec, out = json.load(open(sys.argv[1])), os.path.abspath(sys.argv[2])
fonts = os.path.join(HERE, 'assets', 'fonts')
bg = os.path.abspath(spec['bg'])
fx, fy = spec.get('focus', [0.5, 0.5]); zoom = spec.get('zoom', 1.0); dk = spec.get('darken', 0.35)

def line(l):
    box = (f"background:{l['box']};padding:6px 34px 0;border-radius:18px;box-shadow:0 14px 40px rgba(0,0,0,.55);"
           if l.get('box') else "")
    stroke = "" if l.get('box') else "-webkit-text-stroke:10px #000;paint-order:stroke fill;"
    return (f"<div style=\"position:absolute;left:0;width:1080px;top:{l['y']}px;text-align:center\">"
            f"<span style=\"display:inline-block;font-family:Anton;font-size:{l.get('size', 170)}px;line-height:1.08;"
            f"color:{l.get('color', '#fff')};{stroke}{box}transform:rotate({l.get('rotate', 0)}deg);"
            f"filter:drop-shadow(0 10px 24px rgba(0,0,0,.6))\">{l['text']}</span></div>")

tag = spec.get('tag')
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url('file://{fonts}/Anton-Regular.ttf')}}
@font-face{{font-family:MontB;src:url('file://{fonts}/Montserrat-Black.ttf')}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}}
#bg{{position:absolute;inset:0;background:url('file://{bg}') {fx*100}% {fy*100}%/cover no-repeat;
     transform:scale({zoom});transform-origin:{fx*100}% {fy*100}%;filter:contrast(1.06) saturate(1.1)}}
#g{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,{dk}) 0%,rgba(0,0,0,0) 32%,
     rgba(0,0,0,0) 52%,rgba(0,0,0,{dk*1.4}) 100%)}}
</style></head><body><div id="bg"></div><div id="g"></div>
{''.join(line(l) for l in spec['lines'])}
{f'<div style="position:absolute;left:0;width:1080px;top:{tag.get("y",120)}px;text-align:center"><span style="font-family:MontB;font-size:44px;letter-spacing:.12em;color:#111;background:#FFE11A;padding:12px 30px;border-radius:999px">{tag["text"]}</span></div>' if tag else ''}
</body></html>"""

tmp = tempfile.mkdtemp()
open(f'{tmp}/t.html', 'w').write(html)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});
await p.goto('file://{tmp}/t.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({{path:'{tmp}/t.png'}});await b.close();}})();"""
open(f'{tmp}/r.js', 'w').write(js)
env = dict(os.environ, NODE_PATH=subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
subprocess.run(['node', f'{tmp}/r.js'], check=True, env=env)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/t.png', '-q:v', '1', out], check=True)
# review copy: bottom UI zone, right icon rail and the 3:4 profile-grid crop
chk = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else out[:-4] + '_check.jpg'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/t.png', '-vf',
                'drawbox=x=0:y=1440:w=1080:h=480:color=red@0.25:t=fill,drawbox=x=940:y=0:w=140:h=1920:color=red@0.2:t=fill,'
                'drawbox=x=0:y=240:w=1080:h=1440:color=yellow@0.9:t=6', '-q:v', '2', chk], check=True)
print('wrote', out, 'and', chk)
