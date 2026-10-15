import json,copy
exec(open('remap.py').read())
P=json.load(open('plan.json'))
b=json.load(open('beats_v1.json')); out=[]
for x in b:
    if x['name']=='b11b': continue
    t0=x['t0']; e=t0+x['dur']; cues=[float(c) for c in x['cues'].split(',')]
    n0=f(t0); ne=f(e)
    if x['name']=='b02': ne=f(15.95)
    if x['name']=='b14': ne=f(116.45)
    x['cues']=','.join(str(max(0,round(f(t0+c)-n0,2))) if c>0 else '0' for c in cues)
    x['t0']=n0; x['dur']=round(ne-n0,2)
    x['skipcaps']=[f(s) for s in x.get('skipcaps',[])] if x['card']=='kallaway.t2.label.keyword' else []
    for s in x.get('sfx',[]): s['t']=f(s['t'])
    out.append(x)
out.sort(key=lambda x:x['t0'])
for a,c in zip(out,out[1:]):
    g_=c['t0']-(a['t0']+a['dur'])
    if g_<0.45 and a['tier']=='tier1': a['dur']=round(c['t0']-a['t0']+0.6,2)
    elif 0<g_<0.45: a['dur']=round(c['t0']-a['t0'],2)
# CAM（draft4）
sp=[x for x in out if x['mode']=='split'][0]; s0,s1=sp['t0'],sp['t0']+sp['dur']
W=[1.12,-170]; T=[1.45,-300]; SW=[1.1,230]; ST=[1.28,170]
ev=[]
for i,t in enumerate(P['types']):
    if t=='switch': ev.append((round(M[i+1][2]/1.1,3),'sw'))
for x in out:
    if x['tier']=='tier1': ev.append((round(x['t0']+x['dur']-0.6 if any(abs(y['t0']-(x['t0']+x['dur']-0.6))<0.01 for y in out) else x['t0']+x['dur'],3),'ret'))
ev.append((s0,'spl')); ev.append((round(s1,3),'ret')); ev.sort()
cam=[[0,1.45,-300,0],[2.79,1.12,-170,0.45]]; tight=False; insp=False
for t,k in ev:
    if t<2.8: continue
    if k=='spl': insp=True; cam.append([t,*SW,0]); continue
    if insp and t>=s1-0.01: insp=False
    tight=not tight
    sc=(ST if tight else SW) if insp else (T if tight else W)
    cam.append([t,*sc,0])
e14=[x for x in out if x['name']=='b14'][0]; te=round(e14['t0']+e14['dur'],3)
cam=[c for c in cam if c[0]<te-0.05]+[[te,*T,0]]
# dedupe pass
times=[c[0] for c in cam[2:-1]]; ev2=[]
for t in times:
    if ev2 and t-ev2[-1]<0.3: continue
    ev2.append(t)
new=[cam[0],cam[1]]; tight=False
for t in ev2:
    insp = s0-0.01<=t<s1-0.01
    if abs(t-s0)<0.3: new.append([s0,1.1,230,0]); tight=False; continue
    tight=not tight
    new.append([t,*(([1.28,170] if tight else [1.1,230]) if insp else ([1.45,-300] if tight else [1.12,-170])),0])
new.append(cam[-1])
print('pre-cut CAM',new)
# draft5：b01
for x in out:
    if x['name']=='b01':
        x.update(slots={"term":"骨質疏鬆","note":"","top":"1120"},t0=8.0,dur=1.94,cues='0.21',skipcaps=[8.212],sfx=[{"t":8.3,"sfx":"SFX-011"}])
# 6.5 秒剪位
A=539/30; B=734/30; DC=B-A
def g(t): return round(t if t<=A else (A if t<B else t-DC),3)
fin=[]
for x in out:
    if x['name']=='b04': continue
    e=x['t0']+x['dur']; n0=g(x['t0']); ne=g(e)
    if x['name']=='b03': ne=A
    x['t0']=n0; x['dur']=round(ne-n0,3)
    x['skipcaps']=[g(s) for s in x.get('skipcaps',[])]
    for s in x.get('sfx',[]): s['t']=g(s['t'])
    fin.append(x)
json.dump(fin,open('beats.json','w'),ensure_ascii=False,indent=1)
cam2=[[g(c[0])]+c[1:] for c in new if not (A<c[0]<B)]
cam2=[c for c in cam2 if c[1] not in (1.1,1.28)]+[[round(A,3),1.12,-170,0]]
cam2.sort(); json.dump(cam2,open('cam.json','w')); print('CAM',cam2)
# 字幕
exec(open('caps_v1.py').read())
CAPS=[(a,c,t.replace('我們的脊椎骨｜會慢慢塌陷','我們的脊椎｜慢慢變得塌陷')) for a,c,t in CAPS]
C2=[]
for a,c,t in CAPS:
    if t=='65歲或以上的女性': C2+= [(60.76,62.3,'有四分之一的'),(62.3,64.12,'65歲或以上的女性')]
    elif t=='約四分之一｜患有骨質疏鬆症': C2.append((64.12,65.90,'就患有骨質疏鬆症'))
    else: C2.append((a,c,t))
C3=[(f(a),f(c),t) for a,c,t in C2]
C4=[(g(a),g(c),t) for a,c,t in C3 if not (A-0.05<a and c<B+0.05)]
open('caps.py','w').write('CAPS = [\n'+''.join(f' ({a}, {c}, "{t}"),\n' for a,c,t in C4)+']\n')
# 聲效
ev=[{"t":0.05,"sfx":"SFX-015"},{"t":0.9,"sfx":"SFX-011"},{"t":2.8,"sfx":"SFX-001"},{"t":3.3,"sfx":"SFX-004"}]
mgs={'mg_spine':[(0.05,'SFX-014'),('c',0),('c',1),('c',2)],'mg_tower':[('c',1,'SFX-011'),('c',2),('c',3),('c',4)],
     'mg_quarter':[(0.05,'SFX-014'),('c',0,'SFX-011'),('c',2)],'mg_height':[(0.05,'SFX-014'),('c',0),('c',1)],'mg_tscore':[(0.05,'SFX-014'),('c',1),('c',2),('c',3),('c',4)]}
for x in fin:
    if x['card'] in mgs:
        cs=[float(v) for v in x['cues'].split(',')]
        for it in mgs[x['card']]:
            if it[0]=='c': ev.append({"t":round(x['t0']+cs[it[1]]+0.15,2),"sfx":it[2] if len(it)>2 else 'SFX-005'})
            else: ev.append({"t":round(x['t0']+it[0],2),"sfx":it[1]})
    else: ev+=[{"t":s['t'],"sfx":s['sfx']} for s in x.get('sfx',[])]
ev.sort(key=lambda e:e['t']); json.dump(ev,open('sfx-events.json','w')); print(len(ev),'sfx')
for x in fin: print(x['name'],x['t0'],x['dur'],x['card'],x['cues'],x['skipcaps'])
