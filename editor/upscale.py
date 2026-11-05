"""AI upscale (Real-ESRGAN realesr-general-x4v3, SRVGGNetCompact) on CPU.
usage: python3 upscale.py <model.pth> <in> <out.mp4> <ss> <dur> <outW> <outH>
model: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth
needs: pip install torch --index-url https://download.pytorch.org/whl/cpu"""
import torch, torch.nn as nn, torch.nn.functional as F, numpy as np, subprocess, sys, time
class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=32, up=4):
        super().__init__(); s.up=up; b=[nn.Conv2d(3,nf,3,1,1), nn.PReLU(nf)]
        for _ in range(nc): b += [nn.Conv2d(nf,nf,3,1,1), nn.PReLU(nf)]
        b += [nn.Conv2d(nf,3*up*up,3,1,1), nn.PixelShuffle(up)]; s.body=nn.ModuleList(b)
    def forward(s,x):
        o=x
        for m in s.body: o=m(o)
        return o + F.interpolate(x, scale_factor=s.up, mode='nearest')
def load(p):
    m=SRVGG(); sd=torch.load(p,map_location='cpu'); sd=sd.get('params',sd); m.load_state_dict(sd); return m.eval()
if __name__=='__main__':
    # usage: srvgg.py model in.mp4 out.mp4 ss dur outW outH
    mp,src,dst,ss,dur,W,H=sys.argv[1:8]; W,H=int(W),int(H)
    torch.set_num_threads(4); m=load(mp)
    pr=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip().split(',')
    iw,ih=int(pr[0]),int(pr[1])
    dec=subprocess.Popen(['ffmpeg','-v','error','-ss',ss,'-t',dur,'-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p',dst],stdin=subprocess.PIPE)
    n=0; t0=time.time(); fs=iw*ih*3
    with torch.inference_mode():
        while True:
            buf=dec.stdout.read(fs)
            if len(buf)<fs: break
            x=torch.from_numpy(np.frombuffer(buf,np.uint8).reshape(ih,iw,3).copy()).permute(2,0,1).float().div(255)[None]
            y=m(x).clamp(0,1)
            y=F.interpolate(y,size=(H,W),mode='bicubic',antialias=True).clamp(0,1)
            enc.stdin.write((y[0].permute(1,2,0).mul(255).round().byte().numpy()).tobytes()); n+=1
            if n%30==0: print(n, f'{(time.time()-t0)/n:.2f}s/frame', flush=True)
    enc.stdin.close(); enc.wait(); print('done',n)
