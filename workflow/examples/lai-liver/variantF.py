# variantF.py（2026-11-02）：跟最新 video-fx 規則改護肝篇 v2 → v3
# 字幕 #186baa、≤10 字、阿拉伯數字；螢光筆取代漸變字；jump-cuts 闊 1.12／近 1.45；MG 拎走膠囊、字幕照出；
# 外部效果：#03 蓋章（0:37）、#29 計數器（1:10 mg_regrow）、#38 螢光筆；#32 唔用（用戶 11-02）
import json,os,re,subprocess,shutil
H=os.path.expanduser('~/hf'); P=f'{H}/v3'
shutil.rmtree(P,ignore_errors=True); os.makedirs(P+'/compositions')
os.symlink(f'{H}/liver/assets',P+'/assets')
for f in ('hyperframes.json','meta.json'): shutil.copy(f'{H}/liver/{f}',P)
s=open(f'{H}/liver/build.py').read().replace("P=os.path.expanduser('~/hf/liver')",f"P=os.path.expanduser('{P}')")
b=[x for x in json.load(open(f'{H}/liver/beats.json')) if x['name'] not in ('b06','b09','b13','b05','b10')]
for x in b:
    if x['name']=='b08': x['slots'].pop('tags',None)
json.dump(b,open(P+'/beats.json','w'),ensure_ascii=False)
# ---- 字幕：數字、拆句、MG 字幕照出 ----
FIX={"例如如果你晚上十一時":"例如如果你｜晚上11時","睡至翌日下午三時":"睡至翌日下午3時","兩三個星期":"2至3個星期",
     "肝自己會製造自己的細胞":"肝自己會製造｜自己的細胞","你猜肝現在是否在工作？":"你猜肝現在｜是否在工作？"}
for k,v in FIX.items():
    assert f'["{k}",' in s, k; s=s.replace(f'["{k}",',f'["{v}",')
SKIPTXT=["2至3個星期","沒有可能","根本就是沒有可能"]
s=s.replace("caps=[c for c in caps if not any(abs(c[1]-x)<0.02 for x in SK)]",
"""caps=[c for c in caps if not any(abs(c[1]-x)<0.02 for x in SK) and c[0] not in %r]
_cc=[]
for _t,_a,_b in caps:
    _p=_t.split('｜'); _n=sum(len(x) for x in _p); _s=_a
    for _x in _p:
        _e=round(_s+(_b-_a)*len(_x)/_n,2); _cc.append([_x,round(_s,2),_e]); _s=_e
caps=_cc""" % SKIPTXT)
s=s.replace('background:#0b6f99;','background:#186baa;')
# ---- 鏡頭（lessons/jump-cuts.md）：闊 W 1.12／近 T 1.45，origin 540 420 ----
W=[1.12,-170]; T=[1.45,-280]; SPL=[1.1,406]
CAM=[[0,1.35,-84,0],[0.02,1.4,-96,3.2],[3.34,*W,0],[5.84,*T,0],[7.24,*W,0],[12.96,*T,0],[14.2,*SPL,0],[18.74,*W,0],
 [21.66,*T,0],[26.7,*W,0],[33.04,*T,0],[37.24,*W,0],[40.34,*SPL,0],[42.98,*T,0],[46.62,*W,0],[49.08,*T,0],[57.16,*W,0],
 [59.03,*SPL,0],[62.28,*T,0],[64.42,*W,0],[70.48,*T,0],[76.34,*W,0],[79.52,*T,0],[88.72,*W,0]]
s=re.sub(r'\nCAM=\[.*?\]\]\n','\nCAM='+json.dumps(CAM)+'\n',s,count=1,flags=re.S)
assert 'CAM='+json.dumps(CAM) in s
s=s.replace('transform-origin:540px 660px','transform-origin:540px 420px')
old_js=s[s.find('D.CAM.forEach'):s.find('// ---------- 開場')]
s=s.replace(old_js,"D.CAM.forEach(function(c){ if(c[3]>0) tl.to('#camInner',{scale:c[1],y:c[2],duration:c[3],ease:'none'},c[0]); else tl.set('#camInner',{scale:c[1],y:c[2]},c[0]); });\n")
_a=s.find("_p=f'{P}/compositions/b05.html'"); _b=s.find("_p=f'{P}/compositions/b12.html'")
s=s[:_a]+s[_b:]
open(P+'/build.py','w').write(s)
r=subprocess.run(['python3',P+'/build.py'],capture_output=True,text=True,cwd=P); print(r.stdout.strip()[-300:],r.stderr[-800:])
# ---- 38 螢光筆 ----
def highlight(name, sel, t):
    f=f'{P}/compositions/{name}.html'; h=open(f).read()
    css=(f'<style>#{name} {sel},[data-composition-id="{name}"] {sel}{{background-image:linear-gradient(#ffde59,#ffde59)!important;background-repeat:no-repeat!important;'
         f'background-position:0 88%!important;background-size:0% 46%;-webkit-background-clip:border-box!important;background-clip:border-box!important;'
         f'-webkit-text-fill-color:#0B2A3A!important;color:#0B2A3A!important;filter:none!important;text-shadow:none!important;display:inline-block!important;padding:0 12px}}</style>')
    js=(f'<script>(function(){{var T=window.__timelines["{name}"];var R=document.querySelector(\'[data-composition-id="{name}"]\');'
        f'var el=R.querySelector("{sel}");T.fromTo(el,{{backgroundSize:"0% 46%"}},{{backgroundSize:"100% 46%",duration:0.45,ease:"power2.out"}},{t});}})();</script>')
    h=h.replace('</head>',css+'</head>',1); i=h.rfind('</body>'); h=h[:i]+js+h[i:]; open(f,'w').write(h)
for x in b:
    cues=[float(c) for c in x['cues'].split(',')]
    if x['card']=='kallaway.t2.label.keyword': highlight(x['name'],'.keyword',round(cues[0]+0.3,2))
    elif x['card']=='kallaway.x.image.full' and x['slots'].get('big'):
        tb=cues[1] if (x['slots'].get('title') and len(cues)>1) else cues[0]; highlight(x['name'],'.big',round(tb+0.3,2))
# ---- MG：拎走膠囊、太陽唔用橙 ----
for n in ('mg_clock','mg_research'):
    h=open(f'{H}/mg/{n}.html').read()
    h=h.replace('.pill{position:absolute;','.pill{display:none;position:absolute;')
    h=h.replace('radial-gradient(circle at 40% 40%,#FFE08A,#FFB547);box-shadow:0 0 40px 10px rgba(255,181,71,.55)','radial-gradient(circle at 40% 40%,#FFF4B8,#FFDE59);box-shadow:0 0 40px 10px rgba(255,222,89,.6)')
    open(f'{P}/compositions/{n}.html','w').write(h)
for n in ('fx_stamp','mg_regrow'): shutil.copy(f'{H}/mg3/{n}.html',P+'/compositions/')
M=[('mgc','mg_clock',40.34,2.64,'0.62',80,''),('mgr','mg_research',59.03,3.25,'0.3,2.15',81,''),
   ('fxs','fx_stamp',37.24,3.1,'0.3,1.2',82,''),('mgw','mg_regrow',70.08,4.14,'0.15,1.3',83,' t1')]
mounts=''.join(f'  <div id="h-{i}" class="cardhost{t}" data-composition-id="{i}" data-composition-src="compositions/{f}.html" data-dur="{d}" data-cues="{c}" data-start="{st}" data-duration="{d}" data-width="1080" data-height="1920" data-track-index="{k}"></div>\n' for i,f,st,d,c,k,t in M)
h=open(P+'/index.html').read(); h=h.replace('  <div id="caps"',mounts+'  <div id="caps"',1)
assert 'pill' not in [] ; open(P+'/index.html','w').write(h)
caps=json.loads(re.search(r'const D=(\{.*?\});',h,re.S).group(1))['CAPS']
print('caps>10:',[c[0] for c in caps if len(c[0])>10]); print('ok F', len(caps))
