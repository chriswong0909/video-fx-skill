# 第 2 集（脂肪肝篇）build：以護肝篇 build.py 做模板；規則同 variantF（jump-cuts、#186baa、≤10 字、螢光筆、SPS 素材 MG）
import json,os,re,subprocess,shutil
H=os.path.expanduser('~/hf'); P=f'{H}/ep2'; L=os.path.expanduser('~/mnt/video-fx-skill')
shutil.rmtree(P+'/compositions',ignore_errors=True); os.makedirs(P+'/compositions')
Q=[("Q1","瘦係咪就唔會","有脂肪肝？",0,1.92,0.75),("Q2","唔飲酒係咪","唔會有脂肪肝呢？",10.34,2.26,0.9),
   ("Q3","食得太油、太油膩，","容易有脂肪肝？",20.02,2.76,1.2),("Q4","咁你遇過最年輕嘅","脂肪肝病人係點㗎？",35.22,3.3,1.4),
   ("Q5","咁減肥要減幾多","先可以解決脂肪肝呢？",42.26,3.06,1.3),("Q6","有脂肪肝係咪","最好都要戒飯呢？",56.24,2.36,0.9),
   ("Q7","淨係戒口唔做運動，","減唔減到脂肪肝？",73.14,3.82,1.8),("Q8","其實脂肪肝","可唔可以完全康復呢？",88.34,2.4,0.9),
   ("Q9","咁改善脂肪肝","通常要幾耐？",98.72,2.48,1.0),("Q10","你最推薦改善脂肪肝","嘅3招會係咩呢？",105.84,2.96,1.3)]
beats=[{"name":q[0].lower(),"t0":q[3],"dur":q[4],"mode":"qcard","tier":"tier2","card":"kallaway.x.question","slots":{"num":q[0],"l1":q[1],"l2":q[2]},"cues":f"0.15,{q[5]}","skipcaps":[]} for q in Q]
beats+=[{"name":"kw1","t0":13.4,"dur":2.15,"mode":"person","tier":"tier2","card":"kallaway.t2.label.keyword","slots":{"term":"壞膽固醇","note":""},"cues":"0.1","skipcaps":[]},
        {"name":"kw2","t0":68.85,"dur":1.7,"mode":"person","tier":"tier2","card":"kallaway.t2.label.keyword","slots":{"term":"果糖","note":""},"cues":"0.1","skipcaps":[]},
        {"name":"b3z","t0":108.8,"dur":5.0,"mode":"card","tier":"tier1","card":"kallaway.t1.overview.checklist","slots":{"title":"改善脂肪肝<em>3招</em>","i1":"不要吃澱粉質","i2":"水果別吃太多","i3":"做運動","i4":""},"cues":"0.05,0.14,2.02,4.04","skipcaps":[]}]
json.dump(beats,open(P+'/beats.json','w'),ensure_ascii=False)
CAPS=[["脂肪肝大半是肥的",2.10,3.30],["喝酒會有脂肪肝",3.52,4.80],["但不喝酒",4.88,5.45],["我現在見到新的脂肪肝",5.58,7.15],["大半是肥的",7.20,8.16],["通常就是肥引起",8.36,10.30],
 ["肥",12.77,13.40],["還有壞膽固醇",13.47,15.60],["不一定喝酒",15.83,18.15],["現在很多人都不喝酒",18.31,19.63],
 ["不關油膩",22.97,24.05],["我叫他們｜不要吃那麼多澱粉質",24.17,27.0],["油當然會",28.25,29.25],["但澱粉質最重要",29.53,30.6],["飯、麵、麵包",30.93,31.80],["和果糖都很壞",31.85,34.85],
 ["沒有限年紀",38.67,39.95],["20、30歲都可以有",40.05,41.85],
 ["中國人不應該高過23",45.50,47.0],["21、22都可以",47.60,49.95],["22都可以",50.12,51.3],["如果高過23的話",51.54,53.2],["那就應該會有脂肪肝",53.58,55.85],
 ["對呀",58.73,59.35],["吃少一點",59.41,61.4],["所有甜品都（？）",61.67,63.15],["除了飯、麵",63.21,64.95],["薯仔、芋頭那些都是",65.21,68.5],["還有果糖也很壞",68.93,70.5],["我本人就不吃飯了",70.66,72.1],["所以很難說",72.22,73.0],
 ["可以",77.14,77.9],["不過如果喜歡做運動",78.02,80.05],["就更好",80.10,81.6],["因為我本人也不做運動",82.24,84.05],["所以我很少｜叫病人做運動",84.16,86.6],["但做運動沒有壞的事情",87.14,88.34],
 ["應該可以的",90.90,92.1],["如果減肥",92.24,93.15],["可以的",93.28,94.2],["不過如果你壞膽固醇高",94.52,96.85],["又應該吃藥",96.98,97.7],["我也吃了很久",97.78,98.6],
 ["很難說",101.37,102.1],["如果刻意減肥",102.31,104.4],["2至3個月",104.83,105.84],
 ["不要吃澱粉質",108.94,110.6],["不要吃那麼多水果",110.82,112.6],["如果是做運動",112.84,113.75],["真的不是很多",113.98,115.2],["我聽說印度和埃及",115.40,117.2],["最多人引致肝癌的",117.30,119.5],["就是脂肪肝",119.54,120.6],["所以不要不害怕",120.82,122.3],["真的",122.42,123.2]]
SKIP=["大半是肥的","不關油膩","但澱粉質最重要","20、30歲都可以有","吃少一點","就更好","應該可以的","2至3個月","還有壞膽固醇","還有果糖也很壞"]
W=[1.12,-170]; T=[1.45,-280]; SPL=[1.1,406]
CAM=[[0,1.35,-84,0],[0.02,1.4,-96,1.88],[1.92,*W,0],[5.9,*T,0],[10.34,*W,0],[12.6,*T,0],[15.7,*W,0],[20.02,*T,0],[22.78,*W,0],[27.6,*T,0],[28.6,*W,0],
 [38.52,*T,0],[40.35,*W,0],[45.72,*T,0],[53.4,*W,0],[56.24,*T,0],[58.6,*W,0],[59.35,*SPL,0],[65.05,*T,0],[73.14,*W,0],[76.96,*T,0],[78.4,*W,0],[84.1,*T,0],
 [88.34,*W,0],[91.14,*T,0],[97.75,*W,0],[98.72,*T,0],[101.2,*W,0],[102.58,*T,0],[109.2,*W,0],[117.3,*T,0],[120.72,*W,0]]
END=123.36
s=open(f'{H}/liver/build.py').read().replace("P=os.path.expanduser('~/hf/liver')",f"P=os.path.expanduser('{P}')")
s=re.sub(r'\nEND=91.56; VEND=91.56\n',f'\nEND={END}; VEND={END}\n',s); assert f'END={END}' in s
s=re.sub(r'\nCAPS=\[\[.*?\]\]\n','\nCAPS='+json.dumps(CAPS,ensure_ascii=False)+'\n',s,count=1,flags=re.S)
s=re.sub(r'\nCAM=\[.*?\]\]\n','\nCAM='+json.dumps(CAM)+'\n',s,count=1,flags=re.S)
assert 'CAM='+json.dumps(CAM) in s and '中國人不應該高過23' in s
s=s.replace("caps=[c for c in caps if not any(abs(c[1]-x)<0.02 for x in SK)]",
"""caps=[c for c in caps if not any(abs(c[1]-x)<0.02 for x in SK) and c[0] not in %r]
_cc=[]
for _t,_a,_b in caps:
    _p=_t.split('｜'); _n=sum(len(x) for x in _p); _s=_a
    for _x in _p:
        _e=round(_s+(_b-_a)*len(_x)/_n,2); _cc.append([_x,round(_s,2),_e]); _s=_e
caps=_cc""" % SKIP)
s=s.replace('background:#0b6f99;','background:#186baa;').replace('transform-origin:540px 660px','transform-origin:540px 420px')
old_js=s[s.find('D.CAM.forEach'):s.find('// ---------- 開場')]
s=s.replace(old_js,"D.CAM.forEach(function(c){ if(c[3]>0) tl.to('#camInner',{scale:c[1],y:c[2],duration:c[3],ease:'none'},c[0]); else tl.set('#camInner',{scale:c[1],y:c[2]},c[0]); });\n")
s=s.replace("tl.to('#vig',{opacity:0,duration:0.4,ease:'power1.out'},3.28);","tl.to('#vig',{opacity:0,duration:0.4,ease:'power1.out'},1.86);")
s=s.replace('data-start="0" data-duration="3.7" data-track-index="2"','data-start="0" data-duration="2.3" data-track-index="2"')
s=s.replace('data-start="3.5" data-duration="3.34" data-track-index="6"','data-start="2.1" data-duration="3.4" data-track-index="6"')
s=s.replace("},3.6);\ntl.to('#tag',{opacity:0,duration:0.3,ease:'power1.in'},6.5);","},2.2);\ntl.to('#tag',{opacity:0,duration:0.3,ease:'power1.in'},5.15);")
s=s.replace("'start':3.6,'end':6.7","'start':2.2,'end':5.4")
a=s.find("_p=f'{P}/compositions/b05.html'"); b=s.find("open(f'{P}/index.html','w')")
s=s[:a]+s[b:]
open(P+'/build.py','w').write(s)
r=subprocess.run(['python3',P+'/build.py'],capture_output=True,text=True,cwd=P); print(r.stdout.strip()[-300:],r.stderr[-1200:])
def highlight(name, sel, t):
    f=f'{P}/compositions/{name}.html'; h=open(f).read()
    css=(f'<style>[data-composition-id="{name}"] {sel}{{background-image:linear-gradient(#ffde59,#ffde59)!important;background-repeat:no-repeat!important;'
         f'background-position:0 88%!important;background-size:0% 46%;-webkit-background-clip:border-box!important;background-clip:border-box!important;'
         f'-webkit-text-fill-color:#0B2A3A!important;color:#0B2A3A!important;filter:none!important;text-shadow:none!important;display:inline-block!important;padding:0 12px}}</style>')
    js=(f'<script>(function(){{var T=window.__timelines["{name}"];var R=document.querySelector(\'[data-composition-id="{name}"]\');'
        f'var el=R.querySelector("{sel}");T.fromTo(el,{{backgroundSize:"0% 46%"}},{{backgroundSize:"100% 46%",duration:0.45,ease:"power2.out"}},{t});}})();</script>')
    h=h.replace('</head>',css+'</head>',1); i=h.rfind('</body>'); h=h[:i]+js+h[i:]; open(f,'w').write(h)
for x in beats:
    if x['card']=='kallaway.t2.label.keyword': highlight(x['name'],'.keyword',round(float(x['cues'].split(',')[0])+0.3,2))
for n in ('fx_stamp2','mg_age','mg_bmi','mg_month','sfat','sstarch','srice','sjog','sheal'): shutil.copy(f'{H}/mg4/{n}.html',P+'/compositions/')
M=[('sfat','sfat',5.5,2.76,'1.65',80,' t1'),('fxs','fx_stamp2',22.78,2.2,'0.22,9',81,''),('sstarch','sstarch',28.2,7.02,'1.35',82,' t1'),
   ('mga','mg_age',39.95,2.31,'0.1,0.4',83,' t1'),('mgb','mg_bmi',45.32,6.18,'0.2,2.3',84,' t1'),('srice','srice',59.35,5.7,'0.75',85,''),
   ('sjog','sjog',78.0,3.6,'2.05',86,' t1'),('sheal','sheal',90.74,3.71,'0.16',87,' t1'),('mgm','mg_month',102.18,3.66,'2.6,0.45',88,' t1')]
mounts=''.join(f'  <div id="h-{i}" class="cardhost{t}" data-composition-id="{i}" data-composition-src="compositions/{f}.html" data-dur="{d}" data-cues="{c}" data-start="{st}" data-duration="{d}" data-width="1080" data-height="1920" data-track-index="{k}"></div>\n' for i,f,st,d,c,k,t in M)
h=open(P+'/index.html').read(); h=h.replace('  <div id="caps"',mounts+'  <div id="caps"',1); open(P+'/index.html','w').write(h)
caps=json.loads(re.search(r'const D=(\{.*?\});',h,re.S).group(1))['CAPS']
print('caps>10:',[c[0] for c in caps if len(c[0])>10],'n',len(caps))
