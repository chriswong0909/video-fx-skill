import json,subprocess,re
D='/sessions/rcw-01n7urxarxhlj69paipj1efq/ep2/dn/' if False else __import__('os').path.expanduser('~/ep2/dn/')
VO=[(0.81,2.42),(4.53,6.49),(8.17,10.65),(12.64,15.64),(17.95,20.71),(22.76,24.83),(26.81,30.34),(32.81,34.91),(36.29,38.47),(40.65,43.31)]
# (source, listen_end, answer ranges)
Q=[('0007',17.90,[(17.90,27.45)]),
   ('0006',57.10,[(57.10,64.15)]),
   ('0006',74.05,[(74.05,86.10)]),
   ('0007',54.30,[(54.30,57.65)]),
   ('0006',107.56,[(110.35,120.90)]),
   ('0006',90.80,[(90.80,102.55),(126.80,129.05)]),
   ('0006',145.85,[(145.85,157.12)]),
   ('0006',197.70,[(197.70,205.30)]),
   ('0006',215.30,[(215.30,216.20),(220.30,224.25)]),
   ('0006',235.56,[(238.90,242.60),(245.30,246.20),(251.30,261.50)])]
sn=lambda t: round(round(t*50)/50,2)
def speech(src,a,b):
    r=subprocess.run(['ffmpeg','-hide_banner','-ss',str(a),'-to',str(b),'-i',D+f's{src}_c.wav','-af','silencedetect=n=-38dB:d=0.45','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',r)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',r)]
    sil=[(a+s,a+(en[i] if i<len(en) else b-a)) for i,s in enumerate(st)]
    pieces=[]; cur=a
    for s,e in sil:
        if s-cur>0.05: pieces.append([cur,s])
        cur=e
    if b-cur>0.05: pieces.append([cur,b])
    return pieces
clips=[]
for k,(src,le,rng) in enumerate(Q):
    va,vb=VO[k]; L=(vb-va)+0.30
    clips.append({'q':k+1,'kind':'listen','src':src,'a':sn(le-L),'b':sn(le),'vo':[va-0.03,vb+0.05]})
    P=[]
    for a,b in rng: P+=speech(src,a,b)
    cur=[P[0][0],P[0][1]]
    for p in P[1:]:
        if p[0]-cur[1]<=0.9: cur[1]=p[1]
        else:
            clips.append({'q':k+1,'kind':'ans','src':src,'a':sn(max(cur[0]-0.08,0)),'b':sn(cur[1]+0.12)}); cur=[p[0],p[1]]
    clips.append({'q':k+1,'kind':'ans','src':src,'a':sn(cur[0]-0.08),'b':sn(cur[1]+(0.30 if k<9 else 0.6))})
t=0
for i,c in enumerate(clips):
    c['i']=i; c['t0']=round(t,2); t+=c['b']-c['a']; c['t1']=round(t,2)
json.dump(clips,open(__import__('os').path.expanduser('~/ep2/edl.json'),'w'),indent=0)
for c in clips: print(c['i'],c['q'],c['kind'],c['src'],c['a'],c['b'],'->',c['t0'],c['t1'])
print('total',round(t,2))
