import json,subprocess,wave,numpy as np
P=json.load(open('plan.json')); keep=P['keep']; types=P['types']; X=0.1
def run(a): subprocess.run(a,check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i','assets/graded.mp4','-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','g.wav'],check=True)
for i,(s,e) in enumerate(keep):
    n=round((e-s)*30)
    run(['ffmpeg','-v','error','-y','-ss',str(s),'-i','assets/graded.mp4','-frames:v',str(n),'-an','-c:v','libx264','-crf','14','-preset','veryfast','-pix_fmt','yuv420p','-r','30',f'seg/s{i:02d}.mp4'])
groups=[[0]]
for i,t in enumerate(types):
    if t=='soft': groups[-1].append(i+1)
    else: groups.append([i+1])
L=open('seg/list.txt','w')
for g,idx in enumerate(groups):
    if len(idx)==1: L.write(f"file 's{idx[0]:02d}.mp4'\n"); continue
    ins=[];fc=[];prev='[0:v]'
    for k,i in enumerate(idx): ins+=['-i',f'seg/s{i:02d}.mp4']
    durs=[round((keep[i][1]-keep[i][0])*30)/30 for i in idx]
    off=durs[0]-X
    for k in range(1,len(idx)):
        out=f'[x{k}]'; fc.append(f'{prev}[{k}:v]xfade=transition=fade:duration={X}:offset={round(off,4)}{out}'); prev=out; off+=durs[k]-X
    run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fc),'-map',prev,'-c:v','libx264','-crf','14','-preset','veryfast','-pix_fmt','yuv420p','-r','30',f'seg/g{g:02d}.mp4'])
    L.write(f"file 'g{g:02d}.mp4'\n")
L.close()
w=wave.open('g.wav'); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)
fd=int(0.008*sr); xo=int(X*sr); out=np.zeros(0,np.float32); mp=[]; acc=0
for i,(s,e) in enumerate(keep):
    n=round((e-s)*30)/30; N=int(round(n*sr)); seg=a[int(round(s*sr)):int(round(s*sr))+N].copy()
    if len(seg)<N: seg=np.pad(seg,(0,N-len(seg)))
    if i>0 and types[i-1]=='soft':
        r=np.linspace(0,1,xo); out[-xo:]=out[-xo:]*r[::-1]+seg[:xo]*r; out=np.concatenate([out,seg[xo:]]); acc-=X
    else:
        r=np.linspace(0,1,fd); seg[:fd]*=r
        if len(out): out[-fd:]*=r[::-1]
        out=np.concatenate([out,seg])
    mp.append([s,e,acc,n]); acc+=n
o=out.clip(-32768,32767).astype(np.int16); v=wave.open('joined.wav','wb'); v.setnchannels(1); v.setsampwidth(2); v.setframerate(sr); v.writeframes(o.tobytes()); v.close()
json.dump(mp,open('map.json','w')); print('audio',len(o)/sr)
run(['ffmpeg','-v','error','-y','-f','concat','-i','seg/list.txt','-c','copy','seg/joined.mp4'])
run(['ffmpeg','-v','error','-y','-i','seg/joined.mp4','-i','joined.wav','-filter_complex','[0:v]setpts=PTS/1.1,fps=30[v];[1:a]atempo=1.1[a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','16','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ac','2','-movflags','+faststart','assets/fast_full.mp4'])
print('DONE')
