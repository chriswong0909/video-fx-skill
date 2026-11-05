import json,subprocess,os
H=os.path.expanduser('~/ep2'); E=json.load(open(f'{H}/edl.json')); W=f'{H}/w'; DN=f'{H}/dn'
IN={'0006':0,'0007':1,'vo':2}
f=[];labs=[]
for c in E:
    d=round(c['b']-c['a'],2); i=c['i']
    if c['kind']=='ans':
        f.append(f"[{IN[c['src']]}:a]atrim={c['a']}:{c['b']},asetpts=PTS-STARTPTS,afade=t=in:d=0.025,afade=t=out:st={d-0.025:.3f}:d=0.025,aformat=sample_rates=48000:channel_layouts=mono[a{i}]")
    else: f.append(f"anullsrc=r=48000:cl=mono,atrim=0:{d}[a{i}]")
    labs.append(f"[a{i}]")
f.append("".join(labs)+f"concat=n={len(E)}:v=0:a=1,aresample=48000[ans]")
vl=[]
for k,c in enumerate([c for c in E if c['kind']=='listen']):
    a,b=c['vo']; a=max(0,a); d=b-a
    delay=int((c['t1']-0.15-(b-0.05-a))*1000)
    c['vo_t0']=round(delay/1000,2); c['vo_t1']=round(delay/1000+d,2)
    f.append(f"[2:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.04:.3f}:d=0.04,aformat=sample_rates=48000:channel_layouts=mono,adelay={delay}[v{k}]"); vl.append(f"[v{k}]")
f.append("".join(vl)+f"amix=inputs={len(vl)}:normalize=0,apad,aresample=48000[vo]")
TOT=E[-1]['t1']
r=subprocess.run(["ffmpeg","-v","error","-y","-i",f"{DN}/s0006_c.wav","-i",f"{DN}/s0007_c.wav","-i",f"{DN}/vo_c.wav","-filter_complex",";".join(f),"-map","[ans]","-t",str(TOT),"-c:a","pcm_s16le",f"{W}/t_ans.wav","-map","[vo]","-t",str(TOT),"-c:a","pcm_s16le",f"{W}/t_vo.wav"],capture_output=True,text=True); print(r.stderr[-600:])
segs={}
for c in E:
    if c['kind']=='ans': segs.setdefault(c['q'],[c['t0'],c['t1']])[1]=c['t1']
json.dump([segs[q] for q in sorted(segs)],open(f"{W}/seg_ans.json","w"))
json.dump([[c['vo_t0'],c['vo_t1']] for c in E if c['kind']=='listen'],open(f"{W}/seg_vo.json","w"))
L=os.path.expanduser('~/mnt/video-fx-skill')
print(subprocess.run(["python3",f"{L}/tools/level_match.py",f"{W}/mix.wav","--target","-16",f"{W}/t_ans.wav:{W}/seg_ans.json",f"{W}/t_vo.wav:{W}/seg_vo.json"],capture_output=True,text=True).stdout[-400:])
json.dump(E,open(f'{H}/edl.json','w'),indent=0)
