import sys, subprocess, numpy as np, json
from faster_whisper import WhisperModel
src, off = sys.argv[1], float(sys.argv[2]) if len(sys.argv)>2 else 0
raw = subprocess.run(['ffmpeg','-v','error','-i',src,'-f','s16le','-ac','1','-ar','16000','-'],capture_output=True).stdout
audio = np.frombuffer(raw,np.int16).astype(np.float32)/32768
m = WhisperModel('small.en',compute_type='int8')
segs,_ = m.transcribe(audio,word_timestamps=True)
words=[{'w':w.word.strip(),'s':round(w.start+off,2),'e':round(w.end+off,2)} for s in segs for w in s.words]
json.dump(words,open(sys.argv[3] if len(sys.argv)>3 else '/dev/stdout','w'))
print(' '.join(f"{x['w']}@{x['s']}" for x in words), file=sys.stderr)
