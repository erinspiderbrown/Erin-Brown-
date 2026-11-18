"""Insert Mary Cain's soundbite (ABC13/AP, 2019) into the owner's take right after "...they only 90 something pounds".
Guest takes the top slot (1440x1280 framing of the AI-upscaled clip); her audio is matched to the owner's loudness
(guest only: one static gain + limiter). Owner's voice untouched. Writes work/face_final.mov + work/words_final.json."""
import json, re, subprocess
T_INS = 27.45                         # tight timeline: just after "pounds", before "don't listen"
A0, A1 = 30.60, 37.10                 # ABC13 piece: "I was weighed in front of teammates ... five pounds too heavy."
UP_SS = 30.40                         # up/cain_bite.mp4 starts at ABC 30.40
D = A1 - A0
def lufs(args):
    e = subprocess.run(['ffmpeg', '-hide_banner', *args, '-af', 'ebur128=framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1])
lv = lufs(['-i', 'work/face_tight.mov']); lb = lufs(['-ss', str(A0), '-t', str(D), '-i', 'news/web_5686151.mp4'])
g = lv - lb
print(f'owner {lv:.1f} LUFS, bite {lb:.1f} LUFS -> bite gain {g:+.1f} dB')
fc = (f"[0:v]trim=0:{T_INS},setpts=PTS-STARTPTS[v0];[0:v]trim={T_INS},setpts=PTS-STARTPTS[v2];"
      f"[1:v]trim={A0-UP_SS}:{A1-UP_SS},setpts=PTS-STARTPTS,crop=1215:1080:(iw-1215)/2:0,scale=1440:1280:flags=lanczos,fps=30,format=yuv420p[v1];"
      f"[0:a]atrim=0:{T_INS},asetpts=PTS-STARTPTS,afade=t=out:st={T_INS-0.02}:d=0.02[a0];[0:a]atrim={T_INS},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[a2];"
      f"[2:a]atrim={A0}:{A1},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=mono,volume={g:.2f}dB,alimiter=limit=0.89:level=false,afade=t=in:d=0.03,afade=t=out:st={D-0.06}:d=0.06[a1];"
      "[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/face_tight.mov', '-i', 'up/cain_bite.mp4', '-i', 'news/web_5686151.mp4',
                '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
                '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', 'work/face_final.mov'], check=True)
W = json.load(open('work/words_tight.json')); B = json.load(open('news/web_5686151.json'))
out = [w for w in W if w['s'] < T_INS]
out += [{**w, 's': round(w['s'] - A0 + T_INS, 3), 'e': round(min(w['e'], A1) - A0 + T_INS, 3)} for w in B if A0 - 0.05 <= w['s'] < A1]
out += [{**w, 's': round(w['s'] + D, 3), 'e': round(w['e'] + D, 3)} for w in W if w['s'] >= T_INS]
json.dump(out, open('work/words_ins.json', 'w'))
print('bite', D, 's; words', len(out))
