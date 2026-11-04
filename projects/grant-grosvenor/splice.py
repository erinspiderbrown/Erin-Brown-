# splice the podcast clip into the tightened talking head (video holds a frame; it's covered by full-screen B-roll)
import json, subprocess, sys
wd = sys.argv[1]
X, PS, PE = 69.50, 13.90, 20.55
P = round(PE - PS, 3)
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{wd}/work/face_tight.mov'],capture_output=True,text=True).stdout)
fc = (f"[0:v]trim=0:{X},setpts=PTS-STARTPTS[v0];[0:v]trim={X}:{X+0.05},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={P},trim=0:{P}[v1];"
      f"[0:v]trim={X},setpts=PTS-STARTPTS[v2];"
      f"[0:a]atrim=0:{X},asetpts=PTS-STARTPTS,aresample=48000,afade=t=out:st={X-0.02}:d=0.02[a0];"
      f"[1:a]atrim={PS}:{PE},asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,afade=t=in:d=0.03,afade=t=out:st={P-0.06}:d=0.06[a1];"
      f"[0:a]atrim={X},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.02[a2];"
      f"[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]")
r = subprocess.run(['ffmpeg','-v','error','-y','-i',f'{wd}/work/face_tight.mov','-i',f'{wd}/raw/vidA.mp4','-filter_complex',fc,
                    '-map','[v]','-map','[a]','-c:v','libx264','-crf','14','-preset','fast','-c:a','pcm_s16le',f'{wd}/work/face_final.mov'],capture_output=True,text=True)
if r.returncode: sys.exit(r.stderr)
W = json.load(open(f'{wd}/work/words_tight.json'))
# hand fixes (names / numbers checked against the bib in the Oregon photo)
out = []; i = 0
while i < len(W):
    w = dict(W[i]); t = w['w']
    if t == 'Grozier': w['w'] = 'Grosvenor'
    elif t == 'NC' and W[i+1]['w'] == 'double':
        w['w'] = 'NCAA'; w['e'] = W[i+2]['e']; i += 2
    elif t == '147': w['w'] = '1:47'
    elif t == '358': w['w'] = '3:58'
    elif t == 'bros': w['w'] = "bro's"
    elif t == 'y' and i+1 < len(W) and W[i+1]['w'].startswith("'all"):
        w['w'] = "y" + W[i+1]['w']; w['e'] = W[i+1]['e']; i += 1
    elif t == 'niggas': w['w'] = 'n****s'      # caption censored; audio untouched
    elif t == 'shit': w['w'] = 'sh*t'
    out.append(w); i += 1
pod = [w for w in json.load(open(f'{wd}/work/vidA.json')) if PS - 0.1 <= w['s'] < PE - 0.05]
for w in pod:
    if w['w'] == 'nil': w['w'] = 'NIL'
final = [w for w in out if w['s'] < X]
final += [{'w': w['w'], 's': round(max(w['s'], PS) - PS + X, 3), 'e': round(min(w['e'], PE) - PS + X, 3)} for w in pod]
final += [{**w, 's': round(w['s'] + P, 3), 'e': round(w['e'] + P, 3)} for w in out if w['s'] >= X]
json.dump(final, open(f'{wd}/work/words_final.json', 'w'))
print('P', P, 'total', round(dur + P, 2)); print(' '.join(f"{x['w']}@{x['s']}" for x in final if 60 < x['s'] < 82))
