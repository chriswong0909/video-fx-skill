#!/usr/bin/env python3
"""40S：讀 storyboards/40s-beats.json → 逐拍 cards.py use → 砌 index.html（由零寫，唔沿用舊主檔）
用法：python3 build.py   （L＝技能庫路徑，P＝專案路徑；本機改返 ~/mnt/…/video-fx-skill 同 ~/hf/40s）"""
import json, re, subprocess, sys, os, urllib.request, urllib.parse
L=os.environ.get('FXLIB','/home/claude/lib'); P=os.path.dirname(os.path.abspath(__file__))
END=39.333
beats=json.load(open(f'{L}/storyboards/40s-beats.json'))
# 字幕（口語，用戶已核對嘅 sentences.json；時間＝Whisper turbo 逐詞時間，clean 時間軸）
CAPS=[["會唔會有一個憂慮",0.0,1.24],["就係覺得AI會取代咗老師",1.24,3.4],
 ["佢哋會唔會覺得",3.69,5.04],["AI俾我嘅判斷",5.04,6.82],["會更加準確",6.82,7.69],
 ["其實老師呢件事",7.92,9.5],["唔止係改卷",9.56,11.3],
 ["仲有好多範圍",11.68,13.2],["包括點樣教學生",13.2,14.74],["教學生教得更加好",14.74,16.0],
 ["就算我哋出份報告出嚟",16.4,18.15],["講俾學生聽有咩錯",18.53,20.15],["然後我哋出啲練習出嚟",20.15,21.95],["話俾學生聽",21.95,22.85],["你試下咁做會好啲",22.85,24.37],
 ["但實際上去到",24.4,25.48],["真係幫學生去了解佢",25.48,27.85],
 ["譬如佢真係好唔鍾意作文",27.92,29.23],["點解佢唔鍾意作文呢",29.26,30.46],
 ["好唔鍾意譬如ICT",30.5,31.72],["或者某啲科",31.72,32.6],
 ["可能都係由老師去開解",32.7,34.2],["老師去了解佢",34.2,35.2],
 ["老師去令佢真係知道",35.24,37.1],["自己差啲咩先會更加好",37.1,39.2]]
ALLCAPS=[c[:] for c in CAPS]
T1=[(b['t0'],b['t0']+b['dur']) for b in beats if b['mode']=='card']            # 資訊卡時段唔出字幕
CAPS=[c for c in CAPS if not any(c[1]<e-0.05 and c[2]>s+0.05 for s,e in T1)]
SK=[x for b in beats for x in b.get('skipcaps',[])]
miss=[x for x in SK if not any(abs(c[1]-x)<0.02 for c in CAPS)]
if miss: print('! skipcaps 搵唔到字幕：',miss)
CAPS=[c for c in CAPS if not any(abs(c[1]-x)<0.02 for x in SK)]
# 鏡頭：原片單機位闊鏡，假機位＝推近。transform-origin 0 0；[開始, 結束, [s,x,y] 起, [s,x,y] 終]。全部硬切（唔同人／由全屏返嚟）
WIDE=[1,0,0]; HOST=[1.45,-486,-418]; GUEST=[1.45,0,-447]; SPLIT=[1.0,0,330]
CAM=[[0,3.567,WIDE,[1.05,-27,-48]],
     [3.567,7.69,HOST,[1.5,-540,-455]],
     [7.69,9.5,GUEST,[1.5,0,-485]],
     [9.6,16.367,SPLIT,[1.04,-22,318]],
     [16.5,27.89,GUEST,GUEST],[24.37,27.89,GUEST,[1.52,0,-500]],
     [28.0,32.667,WIDE,WIDE],[30.47,32.667,[1.06,-32,-58],WIDE],
     [32.667,35.21,SPLIT,[1.03,-16,321]]]
mounts=[]; man=[]
for i,b in enumerate(beats):
    if not b['card']: continue
    cmd=['python3',f'{L}/tools/cards.py','use',b['card'],'--project',P,'--name',b['name'],'--dur',str(b['dur']),'--slots',json.dumps(b['slots'],ensure_ascii=False),'--brand',b['brand']]
    if b['cues']: cmd+=['--cues',b['cues']]
    r=subprocess.run(cmd,capture_output=True,text=True); out=r.stdout+r.stderr
    if r.returncode: sys.exit(out)
    for l in out.splitlines():
        if l.startswith('!') and '未填 slot' not in l and '未驗證' not in l: print(b['name'],l)
    cues=f' data-cues="{b["cues"]}"' if b['cues'] else ''
    mounts.append(f'  <div id="host-{b["name"]}" class="cardhost{" t1" if b["tier"]=="tier1" else ""}{" ov" if b.get("z") else ""}" data-composition-id="{b["name"]}" data-composition-src="compositions/{b["name"]}.html" data-dur="{b["dur"]}"{cues} data-start="{b["t0"]}" data-duration="{b["dur"]}" data-width="1080" data-height="1920" data-track-index="{30+i}"></div>')
    cl=[float(c) for c in b['cues'].split(',')] if b['cues'] else [0]
    # 每個 slot 對返自己嘅 cue（卡入面 cues 次序：有 title 就 title 先，之後逐項）
    order=[k for k in ('title','term','term2','note','name','role','i1','i2','i3','i4','n1','n2','n3','n4') if b['slots'].get(k)]
    items=[(k,b['slots'][k]) for k in order]
    if b['slots'].get('tags'):
        if 'title' not in order and b['card'].endswith('split'): items.append(('_pad',''))   # split：第一個 cue 永遠係標題條
        items+= [('tag%d'%n,s) for n,s in enumerate(re.split('[、,，]',b['slots']['tags']))]
    NOTSPOKEN=set(b.get('notspoken',[]))|{'title','name','role'}
    for n,(k,v) in enumerate(items):
        if not v: continue
        st=b['t0']+(cl[n] if n<len(cl) else cl[-1])
        man.append({'id':f"{b['name']}_{k}",'kind':'card','text':re.sub(r'<[^>]+>|\*|｜','',v),'start':round(st,2),'end':round(b['t0']+b['dur'],2),'spoken':k not in NOTSPOKEN,'comp':b['card'],'beat':b['tier']})
for c in CAPS: man.append({'id':'cap_%.2f'%c[1],'kind':'caption','text':c[0],'start':c[1],'end':c[2],'spoken':True})
# 字型子集（lessons：&text= 只下載用到嘅字）
txt=''.join(sorted(set(''.join(c[0] for c in ALLCAPS)+''.join(str(v) for b in beats for v in b['slots'].values())+'0123456789？！，、：ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ')))
def font(fam,wt,out):
    if os.path.exists(out) and os.path.exists(out+'.txt') and open(out+'.txt').read()==txt: return
    u='https://fonts.googleapis.com/css2?family=%s:wght@%d&text=%s'%(fam,wt,urllib.parse.quote(txt))
    css=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'})).read().decode()
    src=re.search(r'url\((https://[^)]+)\)',css).group(1); open(out,'wb').write(urllib.request.urlopen(src).read()); open(out+'.txt','w').write(txt)
os.makedirs(f'{P}/assets/fonts',exist_ok=True)
font('Noto+Sans+TC',900,f'{P}/assets/fonts/sanstc-900.woff2'); font('Noto+Sans+TC',700,f'{P}/assets/fonts/sanstc-700.woff2'); font('Plus+Jakarta+Sans',800,f'{P}/assets/fonts/pjs-800.woff2')
D={'CAPS':CAPS,'CAM':CAM,'END':END}
html='''<!doctype html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"SansTC";font-weight:900;src:url("assets/fonts/sanstc-900.woff2") format("woff2")}
@font-face{font-family:"SansTC";font-weight:700;src:url("assets/fonts/sanstc-700.woff2") format("woff2")}
@font-face{font-family:"PJS";font-weight:800;src:url("assets/fonts/pjs-800.woff2") format("woff2")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}
/* 講者：非計時 wrapper 做推鏡（唔好對 video 本身做 transform） */
#cam{position:absolute;inset:0;z-index:2;overflow:hidden}
#camInner{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0}
#spk{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
/* 風格包卡 host：一定要有 z-index，否則喺 #cam 後面 */
.cardhost{position:absolute;inset:0;z-index:12}
.cardhost.t1{z-index:14}
.cardhost.ov{z-index:16}
/* 光暈字幕（FX-039）：白字 76px + 黑／深灰光暈（用戶 2026-10-04：唔使用品牌色）；全片只得呢一款 */
#caps{position:absolute;left:52px;right:52px;top:1400px;height:110px;z-index:20;text-align:center}
#caps span{position:absolute;left:0;right:0;opacity:0;white-space:nowrap;font-family:"PJS","SansTC",sans-serif;font-weight:900;font-size:76px;line-height:1.3;color:#fff;
  text-shadow:0 0 4px rgba(0,0,0,.9),0 0 10px rgba(0,0,0,.75),0 2px 22px rgba(20,20,20,.7),0 4px 40px rgba(30,30,30,.5)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__END__" data-width="1080" data-height="1920">
  <div id="cam"><div id="camInner"><video id="spk" class="clip" src="assets/graded.mp4" muted playsinline data-start="0" data-duration="__END__" data-track-index="0"></video></div></div>
__MOUNTS__
  <div id="caps"></div>
</div>
<script type="application/json" id="fx-manifest">__MAN__</script>
<script>
window.__timelines = window.__timelines || {};
const D=__D__;
const tl = gsap.timeline({ paused: true });
tl.to({}, {duration: D.END}, 0);
// ---------- 鏡頭 ----------
D.CAM.forEach(function(c){ const a=c[2], b=c[3];
  tl.set('#camInner',{scale:a[0],x:a[1],y:a[2]},c[0]);
  if(a[0]!==b[0]||a[1]!==b[1]||a[2]!==b[2]) tl.to('#camInner',{scale:b[0],x:b[1],y:b[2],duration:c[1]-c[0]-0.02,ease:'none'},c[0]+0.01); });
// ---------- 字幕 ----------
const box=document.getElementById('caps');
const est=function(w,fs){ return Array.from(w).reduce(function(n,ch){ return n+(/[\\u0000-\\u00ff]/.test(ch)?0.6:1); },0)*fs; };
D.CAPS.forEach(function(c){ const s=document.createElement('span'); s.textContent=c[0]; box.appendChild(s);
  const fs=Math.min(76,Math.floor(76*976/Math.max(1,est(c[0],76)))); s.style.fontSize=fs+'px';
  tl.set(s,{opacity:1},c[1]); tl.fromTo(s,{y:10},{y:0,duration:0.12,ease:'power2.out'},c[1]); tl.set(s,{opacity:0},c[2]); });
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
'''
html=html.replace('__END__',str(END)).replace('__MOUNTS__','\n'.join(mounts)).replace('__MAN__',json.dumps(man,ensure_ascii=False)).replace('__D__',json.dumps(D,ensure_ascii=False))
open(f'{P}/index.html','w').write(html); print('ok',len(CAPS),'caps',len(mounts),'cards')
