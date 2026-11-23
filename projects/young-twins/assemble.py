"""Insert Leo Young's USATF XC 2023 interview (owner's clip, AI-upscaled from the original 720p, blend 0.6) right after
"...a lot of these distance runners." Guest takes the top slot (1440x1280); his audio is matched to the owner's
loudness (guest only). Owner's voice untouched. Writes work/face_final.mov + work/words_ins.json."""
import json, re, subprocess
T_INS = 16.45                       # tight timeline: after "runners", before "But they were considered the ones"
A0, A1 = 0.0, 13.82                 # "I've always told myself ... I'm gonna get that USA singlet"
D = A1 - A0
def lufs(args):
    e = subprocess.run(['ffmpeg', '-hide_banner', *args, '-af', 'ebur128=framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1])
lv = lufs(['-i', 'work/face_tight.mov']); lb = lufs(['-ss', str(A0), '-t', str(D), '-i', 'raw/clip1.mp4'])
g = lv - lb
print(f'owner {lv:.1f} LUFS, bite {lb:.1f} LUFS -> bite gain {g:+.1f} dB')
fc = (f"[0:v]trim=0:{T_INS},setpts=PTS-STARTPTS,fps=30[v0];[0:v]trim={T_INS},setpts=PTS-STARTPTS,fps=30[v2];"
      f"[1:v]trim={A0}:{A1},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v1];"
      f"[0:a]atrim=0:{T_INS},asetpts=PTS-STARTPTS,afade=t=out:st={T_INS-0.02}:d=0.02[a0];[0:a]atrim={T_INS},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[a2];"
      f"[2:a]atrim={A0}:{A1},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=mono,volume={g:.2f}dB,alimiter=limit=0.89:level=false,afade=t=in:d=0.03,afade=t=out:st={D-0.06}:d=0.06[a1];"
      "[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/face_tight.mov', '-i', 'up/bite.mp4', '-i', 'raw/clip1.mp4',
                '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '12', '-preset', 'medium',
                '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', 'work/face_final.mov'], check=True)
W = json.load(open('work/words_tight.json')); B = json.load(open('work/clip_words.json'))
out = [w for w in W if w['s'] < T_INS]
out += [{**w, 's': round(w['s'] - A0 + T_INS, 3), 'e': round(min(w['e'], A1) - A0 + T_INS, 3)} for w in B if A0 - 0.05 <= w['s'] < A1]
out += [{**w, 's': round(w['s'] + D, 3), 'e': round(w['e'] + D, 3)} for w in W if w['s'] >= T_INS]
# caption fixes: names and split tokens
FIX = {'Newberry': 'Newbury', 'salamander.': 'Sahlman.', 'Kyle': 'Ky', 'flagstaff': 'Flagstaff', 'young': 'Young',
       'Cruz': 'Kipchoge', 'tools': 'Kiptum'}
res = []
for w in out:
    t = w['w']
    if t.startswith('-') and res:                      # "Nc -double -a" -> NCAA, "cross -country" -> cross-country
        res[-1] = {**res[-1], 'w': res[-1]['w'] + t, 'e': w['e']}; continue
    res.append({**w, 'w': FIX.get(t, t)})
for i, w in enumerate(res):
    if w['w'].lower().startswith('nc-double-a'): w['w'] = 'NCAA'
    if w['w'] == 'Kip' and i + 1 < len(res) and res[i + 1]['w'] in ('Kipchoge', 'Kiptum'): w['w'] = ''
res = [w for w in res if w['w']]
json.dump(res, open('work/words_ins.json', 'w'))
print('bite', round(D, 2), 's; words', len(res))
print(' '.join(w['w'] for w in res))
