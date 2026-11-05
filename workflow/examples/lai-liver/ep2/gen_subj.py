# SPS 白底素材 → 全屏／上半 MG 場景（multiply 去白底、會郁、#38 螢光筆大字）
import json,os
OUT=os.path.expanduser('~/hf/mg4')
TPL=r'''<!doctype html>
<html><head><meta charset="utf-8" />
<!-- @@NOTE@@ -->
<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@700;900&display=swap");
html,body{margin:0;background:transparent}
#@@ID@@{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;font-family:"Noto Sans TC",sans-serif}
#@@ID@@ .stage{position:absolute;left:0;top:0;width:1080px;height:@@H@@px;overflow:hidden;background:@@BG@@}
#@@ID@@ .deco{position:absolute;border-radius:50%}
#@@ID@@ .subj{position:absolute;left:@@SX@@px;top:@@SY@@px;width:@@SW@@px;height:@@SH@@px;transform-origin:50% 92%}
#@@ID@@ .subj img{width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply;display:block}
#@@ID@@ .bigw{position:absolute;left:0;right:0;top:@@BT@@px;text-align:center;opacity:0}
#@@ID@@ .big{display:inline-block;padding:10px 30px 18px;border-radius:22px;background-color:rgba(255,255,255,.82);box-shadow:inset 0 3px 0 #fff,0 14px 30px rgba(11,42,58,.16);font:900 @@BS@@px/1.15 "Noto Sans TC",sans-serif;color:#0B2A3A;letter-spacing:3px;white-space:nowrap;
  background-image:linear-gradient(#ffde59,#ffde59);background-repeat:no-repeat;background-position:30px 84%;background-size:0% 40%}
#@@ID@@ .edge{position:absolute;left:0;right:0;top:@@EDGE@@px;height:8px;background:linear-gradient(90deg,rgba(26,128,208,.15),#1A80D0 50%,rgba(26,128,208,.15));box-shadow:0 0 22px rgba(26,128,208,.55);display:@@EDGED@@}
@@CSS@@
</style></head>
<body>
<div id="@@ID@@" data-composition-id="@@ID@@" data-start="0" data-width="1080" data-height="1920">
  <div class="stage">@@DECO@@<div class="subj"><img src="@@IMG@@" alt="" /></div>@@EXTRA@@<div class="bigw"><span class="big">@@BIG@@</span></div></div>
  <div class="edge"></div>
</div>
<script src="assets/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {};
(function(){
const ROOT=document.querySelector('[data-composition-id="@@ID@@"]');
const DUR=+ROOT.dataset.dur||@@DUR@@; const C=(ROOT.dataset.cues||'@@CUES@@').split(',').map(Number);
const S=ROOT.querySelector('.subj'), BW=ROOT.querySelector('.bigw'), BG=ROOT.querySelector('.big'), ST=ROOT.querySelector('.stage');
const tl=gsap.timeline({paused:true});
tl.fromTo(ST,{clipPath:'@@CLIP0@@'},{clipPath:'inset(0 0 0% 0)',duration:.35,ease:'power3.out'},0)
  .fromTo(ROOT.querySelector('.edge'),{scaleX:0},{scaleX:1,duration:.4,ease:'power3.out'},0.05)
  .fromTo(ROOT.querySelectorAll('.deco'),{scale:.5,opacity:0},{scale:1,opacity:1,duration:.5,stagger:.05,ease:'power2.out'},0.05)
  .to(ROOT.querySelectorAll('.deco'),{y:-40,duration:DUR,ease:'none'},0.05)
  .fromTo(BW,{opacity:0,y:30,scale:.92},{opacity:1,y:0,scale:1,duration:.35,ease:'back.out(1.7)'},C[0])
  .fromTo(BG,{backgroundSize:'0% 40%'},{backgroundSize:'calc(100% - 60px) 40%',duration:.45,ease:'power2.out'},C[0]+.3);
@@MOTION@@
tl.to(ROOT.querySelector('#@@ID@@'),{opacity:0,duration:.25,ease:'power2.in'},DUR-.27).set({}, {}, DUR);
window.__timelines["@@ID@@"]=tl;
})();
</script>
</body></html>
'''
def deco(spec):
    return ''.join(f'<div class="deco" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{c}"></div>' for x,y,r,c in spec)
FULLBG='radial-gradient(120% 70% at 50% 45%,#FFFFFF 0%,#EAF3FB 55%,#D3E5F4 100%)'
S=[
 dict(ID='sfat',IMG='assets/sps/fatty.png',BIG='大半是肥的',DUR=2.76,CUES='1.65',H=1920,BG=FULLBG,SX=170,SY=560,SW=740,SH=925,BT=380,BS=110,EDGE=-50,EDGED='none',CLIP0='inset(0 0 0% 0)',
  NOTE='ep2 Q1：SPS 生成脂肪肝仔（白底，multiply 去白）；跌落＋肚腩擠壓回彈＋淡黃油滴背景；#38 螢光筆大字',
  DECO=deco([(60,300,120,'rgba(243,207,122,.35)'),(900,520,90,'rgba(243,207,122,.30)'),(80,1350,80,'rgba(243,207,122,.28)'),(930,1240,140,'rgba(243,207,122,.25)'),(470,1560,60,'rgba(243,207,122,.3)')]),
  MOTION="tl.fromTo(S,{y:-700,opacity:0},{y:0,opacity:1,duration:.42,ease:'power2.in'},0.05).to(S,{scaleY:.86,scaleX:1.1,duration:.1,ease:'power2.out'},0.47).to(S,{scaleY:1,scaleX:1,duration:.5,ease:'elastic.out(1,.4)'},0.57).to(S,{scaleX:1.04,scaleY:.97,duration:.32,yoyo:true,repeat:5,ease:'sine.inOut'},1.1);",CSS='',EXTRA=''),
 dict(ID='sstarch',IMG='assets/sps/starch.png',BIG='澱粉質最重要',DUR=7.02,CUES='1.35',H=1920,BG=FULLBG,SX=110,SY=520,SW=860,SH=1075,BT=380,BS=104,EDGE=-50,EDGED='none',CLIP0='inset(0 0 0% 0)',
  NOTE='ep2 Q3：SPS 澱粉質食物組；逐步升起＋慢推；講到果糖時果汁位置紅圈脈動',
  DECO=deco([(70,320,110,'rgba(255,222,89,.25)'),(930,300,80,'rgba(26,128,208,.10)'),(90,1450,90,'rgba(26,128,208,.10)'),(920,1500,120,'rgba(255,222,89,.22)')]),
  CSS='#sstarch .ring{position:absolute;left:725px;top:1060px;width:200px;height:260px;border-radius:50%;border:10px solid #E8452C;opacity:0;box-shadow:0 0 24px rgba(232,69,44,.35)}',
  EXTRA='<div class="ring"></div>',
  MOTION="tl.fromTo(S,{y:260,opacity:0,scale:.9},{y:0,opacity:1,scale:1,duration:.55,ease:'back.out(1.5)'},0.05).to(S,{scale:1.06,duration:DUR-.8,ease:'none'},0.6).fromTo(ROOT.querySelector('.ring'),{opacity:0,scale:1.6},{opacity:1,scale:1,duration:.3,ease:'back.out(2)'},5.05).to(ROOT.querySelector('.ring'),{scale:1.08,duration:.3,yoyo:true,repeat:3,ease:'sine.inOut'},5.35);"),
 dict(ID='srice',IMG='assets/sps/rice.png',BIG='吃少一點',DUR=7.3,CUES='0.2',H=860,BG='linear-gradient(180deg,#E6F1FB 0%,#F7FBFF 100%)',SX=290,SY=330,SW=500,SH=520,BT=250,BS=96,EDGE=852,EDGED='block',CLIP0='inset(0 0 100% 0)',
  NOTE='ep2 Q6：上半畫面 MG（下半教授），SPS 肝仔推開白飯；推嘅動作來回',
  DECO=deco([(60,620,90,'rgba(255,255,255,.9)'),(940,160,70,'rgba(26,128,208,.10)'),(900,640,110,'rgba(26,128,208,.08)')]),CSS='',EXTRA='',
  MOTION="tl.fromTo(S,{x:-500,opacity:0},{x:0,opacity:1,duration:.45,ease:'power3.out'},0.1).to(S,{x:22,rotation:2,duration:.28,yoyo:true,repeat:Math.floor((DUR-1)/0.28),ease:'sine.inOut'},0.6);"),
 dict(ID='sjog',IMG='assets/sps/jog.png',BIG='做運動更好',DUR=3.6,CUES='2.05',H=1920,BG=FULLBG,SX=170,SY=540,SW=740,SH=925,BT=380,BS=110,EDGE=-50,EDGED='none',CLIP0='inset(0 0 0% 0)',
  NOTE='ep2 Q7：SPS 跑步肝仔；原地跑上下彈＋背景速度線向左流',
  DECO='',CSS='#sjog .ln{position:absolute;height:10px;border-radius:5px;background:rgba(26,128,208,.16)}',
  EXTRA=''.join(f'<i class="ln" style="left:{x}px;top:{y}px;width:{w}px"></i>' for x,y,w in [(900,780,180),(980,980,120),(860,1180,220),(1000,1380,140),(920,640,100)]),
  MOTION="tl.fromTo(S,{x:700,opacity:0},{x:0,opacity:1,duration:.45,ease:'power3.out'},0.05).to(S,{y:-34,duration:.19,yoyo:true,repeat:Math.floor((DUR-.6)/0.19),ease:'sine.inOut'},0.5).fromTo(ROOT.querySelectorAll('.ln'),{x:0},{x:-1300,duration:1.1,repeat:Math.ceil(DUR/1.1),stagger:.12,ease:'none'},0.1);"),
 dict(ID='sheal',IMG='assets/sps/healthy.png',BIG='應該可以',DUR=3.71,CUES='0.16',H=1920,BG=FULLBG,SX=170,SY=560,SW=740,SH=925,BT=380,BS=116,EDGE=-50,EDGED='none',CLIP0='inset(0 0 0% 0)',
  NOTE='ep2 Q8：SPS 康復肝仔；彈跳慶祝＋彩紙＋綠剔；大字保留限定詞「應該」',
  DECO=deco([(120,700,26,'#FFDE59'),(930,760,22,'#1F9D6B'),(200,1280,20,'#1A80D0'),(860,1300,26,'#FFDE59'),(540,560,18,'#1F9D6B'),(80,1000,18,'#1A80D0'),(980,1040,20,'#FFDE59')]),
  CSS='#sheal .ok{position:absolute;left:800px;top:600px;width:130px;height:130px;border-radius:50%;background:linear-gradient(180deg,#34C08A,#1F9D6B);box-shadow:inset 0 3px 0 rgba(255,255,255,.5),0 10px 22px rgba(31,157,107,.35);opacity:0}#sheal .ok svg{position:absolute;left:26px;top:28px;width:78px;height:78px}',
  EXTRA='<div class="ok"><svg viewBox="0 0 24 24"><path d="M4 12.5 L10 18 L20 6" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>',
  MOTION="tl.fromTo(S,{y:300,opacity:0,scale:.8},{y:0,opacity:1,scale:1,duration:.45,ease:'back.out(1.8)'},0.05).to(S,{y:-60,duration:.24,yoyo:true,repeat:5,ease:'power1.out'},0.6).fromTo(ROOT.querySelector('.ok'),{opacity:0,scale:0,rotation:-30},{opacity:1,scale:1,rotation:0,duration:.35,ease:'back.out(2.2)'},1.0).to(ROOT.querySelectorAll('.deco'),{rotation:360,duration:DUR,ease:'none'},0.05);"),
]
for s in S:
    h=TPL
    for k,v in s.items(): h=h.replace('@@'+k+'@@',str(v))
    assert '@@' not in h, [x for x in h.split('@@')[1::2]]
    open(f'{OUT}/{s["ID"]}.html','w').write(h)
print('ok',[s['ID'] for s in S])
