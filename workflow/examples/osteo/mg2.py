# B 風格（精緻 2D 向量）motion graphics：全屏 1080×1920
P = '/home/claude/p/compositions'
BASE = r"""<!doctype html>
<html><head><meta charset="utf-8" />
<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@700;900&display=swap");
html,body{margin:0;background:transparent}
#ID{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;font-family:"Noto Sans TC",sans-serif;color:#0B2A3A}
#ID .bg{position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 38%,#FFFFFF 0%,#EAF3FB 55%,#D3E5F4 100%)}
#ID .title{position:absolute;left:0;right:0;top:385px;text-align:center;font:900 96px/1.1 "Noto Sans TC",sans-serif;color:#0B2A3A;opacity:0;z-index:20;white-space:nowrap}
#ID .title em{font-style:normal;color:#1A80D0}
#ID .pills{position:absolute;left:52px;right:52px;top:1265px;display:flex;justify-content:center;gap:22px;z-index:20}
#ID .pill{padding:12px 36px 18px;border-radius:999px;background:linear-gradient(180deg,#3B97E0,#1A80D0);color:#fff;font:900 76px/1 "Noto Sans TC",sans-serif;border:4px solid rgba(255,255,255,.92);box-shadow:0 12px 28px rgba(11,42,58,.22);opacity:0;white-space:nowrap}
#ID .pill.dark{background:linear-gradient(180deg,#6A6A6A,#545454)}
#ID .pill.red{background:linear-gradient(180deg,#E8474E,#C81F28)}
#ID .mark{position:absolute;height:0;border-top:7px dashed #1A80D0;opacity:0;z-index:6}
/* 椎骨／樓層 */
#ID .fl{position:absolute;left:-230px;width:460px;height:118px;transform-origin:50% 100%}
#ID .fl .body{position:absolute;inset:0;border-radius:44px;background:linear-gradient(180deg,#FFFDF8 0%,#F6EBDA 45%,#E6D3B6 100%);
  box-shadow:inset 0 10px 14px rgba(255,255,255,.9),inset 0 -14px 18px rgba(160,120,70,.22),0 14px 24px rgba(11,42,58,.16)}
#ID .fl .wing{position:absolute;top:34px;width:120px;height:52px;border-radius:26px;background:linear-gradient(180deg,#FBF4E8,#E2CDAE);box-shadow:inset 0 -6px 8px rgba(160,120,70,.2),0 6px 12px rgba(11,42,58,.12)}
#ID .fl .wing.l{left:-92px} #ID .fl .wing.r{right:-92px}
#ID .fl .win{position:absolute;top:34px;width:74px;height:50px;border-radius:14px;background:linear-gradient(160deg,#BFE4FA 0%,#7DBDE8 55%,#4F98CF 100%);box-shadow:inset 0 3px 0 rgba(255,255,255,.7),inset 0 -4px 6px rgba(20,60,110,.25)}
#ID .fl .glow{position:absolute;inset:0;border-radius:44px;background:linear-gradient(180deg,#FFF3B0,#FFDE59 55%,#F2C230);opacity:0}
#ID .disc{position:absolute;left:-150px;width:300px;height:22px;border-radius:11px;background:linear-gradient(180deg,#CFEAFB,#8CC6EC);box-shadow:inset 0 3px 0 rgba(255,255,255,.7)}
#ID .roof{position:absolute;left:-250px;width:500px;height:34px;border-radius:17px;background:linear-gradient(180deg,#4DA3E6,#1A80D0 60%,#1468AE);box-shadow:0 10px 18px rgba(26,128,208,.35)}
#ID .shadow{position:absolute;left:-330px;top:-20px;width:660px;height:60px;border-radius:50%;background:radial-gradient(closest-side,rgba(11,42,58,.28),rgba(11,42,58,0))}
#ID .dust{position:absolute;width:16px;height:16px;border-radius:50%;background:#FFDE59;opacity:0}
CSS
</style></head>
<body>
<div id="ID" data-composition-id="ID" data-start="0" data-width="1080" data-height="1920">
  <div class="bg"></div>
BODY
</div>
<script src="assets/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {};
(function(){
var ROOT=document.querySelector('[data-composition-id="ID"]');
var DUR=+ROOT.dataset.dur||DEF; var CUES=(ROOT.dataset.cues||'').split(',').filter(Boolean).map(Number);
function c(i,d){return CUES.length>i?CUES[i]:d;}
function q(s){return ROOT.querySelector(s);} function qa(s){return ROOT.querySelectorAll(s);}
var tl=gsap.timeline({paused:true});
if(!ROOT.dataset.noin) tl.fromTo(q('.bg'),{opacity:0},{opacity:1,duration:0.3},0);
function pill(el,t){ tl.fromTo(el,{opacity:0,y:30,scale:0.7},{opacity:1,y:0,scale:1,duration:0.45,ease:'back.out(1.8)'},t); }
// 疊樓工具：喺 B（容器）入面由下而上砌 N 層，回傳每層資料
function stack(B,N,wins){ var y=0,F=[];
  for(var i=0;i<N;i++){ var d=document.createElement('div'); d.className='disc'; B.appendChild(d);
    var f=document.createElement('div'); f.className='fl';
    f.innerHTML='<div class="wing l"></div><div class="wing r"></div><div class="body"></div><div class="glow"></div>'+(wins?[0,1,2,3].map(function(k){return '<div class="win" style="left:'+(52+k*94)+'px"></div>'}).join(''):'');
    B.appendChild(f); y+=22; d.style.top=(-y)+'px'; y+=118; f.style.top=(-y)+'px'; F.push({f:f,d:d,top:y}); }
  return {F:F,h:y}; }
function squash(F,ks,t){ ks.forEach(function(k){ tl.to(F[k].f,{scaleY:0.48,scaleX:1.1,duration:0.7,ease:'power2.inOut'},t); tl.to(F[k].f.querySelector('.glow'),{opacity:0.85,duration:0.5},t+0.15); });
  var loss=0; F.forEach(function(o,i){ var d=0; ks.forEach(function(k){ if(i>k) d+=118*0.52; }); if(d){ tl.to([o.f,o.d],{y:d,duration:0.7,ease:'power2.inOut'},t); } });
  ks.forEach(function(){loss+=118*0.52}); return loss; }
function dust(B,F,k,t){ for(var p=0;p<10;p++){ var s=document.createElement('div'); s.className='dust'; s.style.left=(p%2?250:-266)+'px'; s.style.top=(-(F[k].top-60))+'px'; B.appendChild(s);
  tl.fromTo(s,{opacity:0.9,x:0,y:0,scale:1},{opacity:0,x:(p%2?1:-1)*(60+p*14),y:-30+p*9,scale:0.3,duration:0.7,ease:'power2.out'},t+p*0.02); } }
JS
if(!ROOT.dataset.nofade) tl.to(ROOT.children,{opacity:0,duration:0.25,ease:'power2.in'},DUR-0.27);
tl.set({}, {}, DUR);
window.__timelines["ID"]=tl;
})();
</script>
</body></html>"""

def write(id, dflt, css, body, js):
    open(f'{P}/{id}.html', 'w').write(BASE.replace('CSS', css).replace('BODY', body).replace('JS', js).replace('DEF', str(dflt)).replace('ID', id))

# ---------- 1) 脊椎塌陷（cues：塌陷、駝背、變矮）----------
write('mg_spine', 5.9, "#mg_spine #bld{position:absolute;left:540px;top:1215px;width:0;height:0;transform:scale(0.85)}",
  '<div class="title"><em>脊椎塌陷</em></div><div class="mark" style="left:240px;width:600px"></div><div id="bld"><div class="shadow"></div></div>'
  '<div class="pills"><div class="pill p1">駝背</div><div class="pill dark p2">變矮</div></div>',
  r"""
var B=q('#bld'); var S=stack(B,5,false);
q('.mark').style.top=(1215-S.h*0.85-16)+'px';
S.F.forEach(function(o,i){ tl.fromTo([o.f,o.d],{y:-700,opacity:0},{y:0,opacity:1,duration:0.45,ease:'bounce.out'},0.2+i*0.16); });
tl.to(q('.mark'),{opacity:1,duration:0.3},1.2);
squash(S.F,[1,2],c(0,3.0)-0.3); dust(B,S.F,2,c(0,3.0)); tl.fromTo(q('.title'),{opacity:0,y:-24,scale:1.2},{opacity:1,y:0,scale:1,duration:0.45,ease:'back.out(1.8)'},c(0,3.0));
tl.to(B,{rotation:14,duration:0.8,ease:'power2.inOut',transformOrigin:'0px 0px'},c(1,5.3)-0.35); pill(q('.p1'),c(1,5.3));
tl.to(q('.mark'),{borderTopColor:'#545454',duration:0.2},c(2,6.6)-0.1); tl.fromTo(B,{x:0},{x:8,duration:0.05,yoyo:true,repeat:5},c(2,6.6)-0.1); pill(q('.p2'),c(2,6.6));
""")

# ---------- 2) 真正嘅樓（cues：標題、疊上去、壓扁、變矮、傾斜）----------
tw_css = r"""
#mg_tower #bld{position:absolute;left:540px;top:1215px;width:0;height:0;transform:scale(0.8)}
#mg_tower .bf{position:absolute;left:-220px;width:440px;height:112px;transform-origin:50% 100%}
#mg_tower .bf .wall{position:absolute;inset:0;background:linear-gradient(90deg,#E9EEF4 0%,#FFFFFF 18%,#F4F7FA 60%,#D9E2EC 100%);box-shadow:inset 0 -10px 0 #C9D5E1,inset 0 -12px 0 #B8C7D6}
#mg_tower .bf .w{position:absolute;top:18px;width:86px;height:62px;border-radius:6px;background:linear-gradient(160deg,#D8F0FF 0%,#8CC8F0 50%,#4F98CF 100%);box-shadow:inset 0 0 0 5px #FFFFFF,0 3px 6px rgba(11,42,58,.18)}
#mg_tower .bf .w::after{content:"";position:absolute;left:41px;top:5px;width:4px;bottom:5px;background:#FFFFFF}
#mg_tower .bf .bal{position:absolute;top:70px;width:110px;height:24px;border-radius:4px;background:repeating-linear-gradient(90deg,#9AAFC2 0 4px,transparent 4px 14px),linear-gradient(180deg,#B7C7D6,#9AAFC2);opacity:.9}
#mg_tower .bf .warn{position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,222,89,.0),rgba(255,222,89,.75));opacity:0}
#mg_tower .bf .crack{position:absolute;left:0;top:0;width:440px;height:112px;opacity:0}
#mg_tower .gnd{position:absolute;left:-240px;top:-150px;width:480px;height:150px}
#mg_tower .gnd .wall{position:absolute;inset:0;background:linear-gradient(90deg,#CFD9E3,#EEF2F6 30%,#E2E9F0 70%,#C3CFDB);border-radius:6px 6px 0 0}
#mg_tower .gnd .door{position:absolute;left:180px;top:46px;width:120px;height:104px;border-radius:10px 10px 0 0;background:linear-gradient(180deg,#6FA9D6,#2E6FA6)}
#mg_tower .gnd .awn{position:absolute;left:150px;top:26px;width:180px;height:26px;border-radius:8px;background:linear-gradient(180deg,#3B97E0,#1A80D0)}
#mg_tower .gnd .sw{position:absolute;top:50px;width:90px;height:60px;border-radius:6px;background:linear-gradient(160deg,#D8F0FF,#7DBDE8);box-shadow:inset 0 0 0 5px #fff}
#mg_tower .rf{position:absolute;left:-235px;width:470px;height:40px}
#mg_tower .rf .par{position:absolute;left:0;right:0;bottom:0;height:26px;border-radius:6px 6px 0 0;background:linear-gradient(180deg,#B9C8D6,#94A9BC)}
#mg_tower .rf .tank{position:absolute;left:300px;bottom:24px;width:92px;height:70px;border-radius:12px 12px 4px 4px;background:linear-gradient(90deg,#4DA3E6,#1A80D0 60%,#1468AE)}
#mg_tower .rf .ant{position:absolute;left:90px;bottom:24px;width:6px;height:80px;background:#7E98AB}
#mg_tower .sky{position:absolute;left:-330px;top:-20px;width:660px;height:60px;border-radius:50%;background:radial-gradient(closest-side,rgba(11,42,58,.28),rgba(11,42,58,0))}
"""
crack = '<svg class="crack" viewBox="0 0 440 112"><path d="M60 0 L80 30 L66 52 L92 80 L80 112 M300 0 L286 26 L312 48 L294 76 L318 112 M180 112 L196 84 L184 64 L206 40" fill="none" stroke="#545454" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
tw_body = ('<div class="title">脊椎 = <em>一棟樓</em></div><div class="mark" style="left:200px;width:680px"></div>'
  '<div id="bld"><div class="sky"></div><div class="gnd"><div class="wall"></div><div class="sw" style="left:30px"></div><div class="sw" style="left:360px"></div><div class="awn"></div><div class="door"></div></div></div>'
  '<div class="pills"><div class="pill p0">壓扁</div><div class="pill p1">變矮</div><div class="pill dark p2">向前傾斜</div></div>')
tw_js = r"""
var B=q('#bld'), N=5, FH=112, F=[], y=150;
var CR='CRACK';
for(var i=0;i<N;i++){ var f=document.createElement('div'); f.className='bf';
  f.innerHTML='<div class="wall"></div><div class="warn"></div>'+[0,1,2,3].map(function(k){return '<div class="w" style="left:'+(22+k*104)+'px"></div>'}).join('')+'<div class="bal" style="left:24px"></div><div class="bal" style="left:306px"></div>'+CR;
  y+=FH; f.style.top=(-y)+'px'; B.appendChild(f); F.push(f); }
var rf=document.createElement('div'); rf.className='rf'; rf.innerHTML='<div class="ant"></div><div class="tank"></div><div class="par"></div>'; y+=40; rf.style.top=(-y)+'px'; B.appendChild(rf);
q('.mark').style.top=(1215-y*0.8-18)+'px';
tl.fromTo(q('.title'),{opacity:0,y:-24},{opacity:1,y:0,duration:0.4,ease:'power3.out'},c(0,0.2));
tl.fromTo(q('.gnd'),{scaleY:0,transformOrigin:'50% 100%'},{scaleY:1,duration:0.4,ease:'back.out(1.6)'},0.3);
var st=0.6;
F.forEach(function(f,i){ tl.fromTo(f,{y:-800,opacity:0},{y:0,opacity:1,duration:0.5,ease:'bounce.out'},st+i*0.3);
  tl.fromTo(f,{scaleY:1},{scaleY:0.88,scaleX:1.04,duration:0.08,yoyo:true,repeat:1,ease:'sine.inOut'},st+i*0.3+0.45); });
tl.fromTo(rf,{y:-800,opacity:0},{y:0,opacity:1,duration:0.5,ease:'bounce.out'},st+N*0.3);
tl.to(q('.mark'),{opacity:1,duration:0.3},st+N*0.3+0.5);
F.forEach(function(f,i){ tl.fromTo(f.querySelector('.wall'),{filter:'brightness(1)'},{filter:'brightness(1.12)',duration:0.15,yoyo:true,repeat:1},c(1,3.9)+i*0.15); });
var ks=[1,2], t2=c(2,6.6)-0.2, loss=0;
ks.forEach(function(k){ tl.to(F[k],{scaleY:0.5,scaleX:1.06,duration:0.7,ease:'power2.inOut'},t2); tl.to(F[k].querySelector('.warn'),{opacity:1,duration:0.5},t2+0.15); tl.to(F[k].querySelector('.crack'),{opacity:1,duration:0.2},t2+0.3); loss+=FH*0.5; });
F.forEach(function(f,i){ var d=0; ks.forEach(function(k){ if(i>k) d+=FH*0.5; }); if(d) tl.to(f,{y:d,duration:0.7,ease:'power2.inOut'},t2); });
tl.to(rf,{y:loss,duration:0.7,ease:'power2.inOut'},t2);
dust(B,[{top:150+FH*2.5}],0,t2+0.3); pill(q('.p0'),c(2,6.6));
tl.to(q('.mark'),{borderTopColor:'#545454',duration:0.2},c(3,8.9)-0.1); tl.fromTo(B,{x:0,scale:0.8},{x:8,scale:0.8,duration:0.05,yoyo:true,repeat:5},c(3,8.9)-0.1); pill(q('.p1'),c(3,8.9));
var tt=c(4,10.3)-0.3, PIV=-(150+2*FH), dd=FH;
[[F[3],-(150+4*FH),0],[F[4],-(150+5*FH),0],[rf,-(150+5*FH+40),15]].forEach(function(o){
  var oy=PIV-(o[1]+dd); tl.to(o[0],{rotation:7,transformOrigin:o[2]+'px '+oy+'px',duration:0.9,ease:'power2.inOut'},tt); });
[F[1],F[2]].forEach(function(f){ tl.fromTo(f,{clipPath:'polygon(0% 0%,100% 0%,100% 100%,0% 100%)'},{clipPath:'polygon(0% 0%,100% 55%,100% 100%,0% 100%)',duration:0.9,ease:'power2.inOut'},tt); });
pill(q('.p2'),c(4,10.3));
""".replace('CRACK', crack.replace("'", "\\'"))
write('mg_tower', 10.4, tw_css, tw_body, tw_js)

# ---------- 3) 身高下降、背部痛（cues：身高下降、背部痛）----------
hcss = r"""
#mg_height .t1,#mg_height .t2{display:inline-block}
#mg_height .ruler{position:absolute;left:150px;top:560px;width:70px;height:640px;border-radius:18px;background:linear-gradient(90deg,#FFFFFF,#EAF2F9);box-shadow:inset 0 2px 0 #fff,0 10px 24px rgba(11,42,58,.16)}
#mg_height .ruler i{position:absolute;left:0;height:5px;border-radius:3px;background:#9FB7C9}
#mg_height .ruler b{position:absolute;left:84px;font:700 40px/1 "Noto Sans TC";color:#7E98AB;transform:translateY(-50%)}
#mg_height .fig{position:absolute;left:470px;top:580px;width:300px;height:620px;transform-origin:150px 620px;scale:1.0}
#mg_height .leg{position:absolute;top:420px;width:66px;height:200px;border-radius:30px 30px 18px 18px;background:linear-gradient(90deg,#8C7A66,#B9A58C 45%,#8C7A66)}
#mg_height .leg.a{left:84px} #mg_height .leg.b{left:150px}
#mg_height .shoe{position:absolute;top:596px;width:92px;height:34px;border-radius:18px;background:linear-gradient(180deg,#F4F4F4,#CFD8DF)}
#mg_height .up{position:absolute;left:0;top:0;width:300px;height:440px;transform-origin:150px 430px}
#mg_height .torso{position:absolute;left:52px;top:150px;width:196px;height:300px;border-radius:90px 90px 40px 40px;background:linear-gradient(90deg,#8B6FC6,#B49BE6 45%,#8B6FC6);box-shadow:inset 0 -14px 20px rgba(60,30,110,.25)}
#mg_height .spine{position:absolute;left:198px;top:178px;width:24px;height:240px}
#mg_height .spine i{position:absolute;left:0;width:24px;height:30px;border-radius:9px;background:rgba(255,255,255,.85);box-shadow:0 2px 4px rgba(60,30,110,.25)}
#mg_height .arm{position:absolute;top:180px;width:56px;height:230px;border-radius:28px;background:linear-gradient(90deg,#8B6FC6,#A68BDB);transform-origin:28px 20px}
#mg_height .arm.l{left:34px;transform:rotate(8deg)} #mg_height .arm.r{left:210px;transform:rotate(-8deg)}
#mg_height .neck{position:absolute;left:126px;top:122px;width:48px;height:44px;background:#F0C9A6;border-radius:12px}
#mg_height .head{position:absolute;left:84px;top:6px;width:132px;height:132px;border-radius:50%;background:radial-gradient(circle at 40% 38%,#FBE2CB,#F0C9A6 60%,#E2B48E);box-shadow:0 6px 14px rgba(11,42,58,.15)}
#mg_height .hair{position:absolute;left:78px;top:-6px;width:144px;height:78px;border-radius:72px 72px 30px 30px;background:linear-gradient(180deg,#F2F4F6,#C7CED6)}
#mg_height .bun{position:absolute;left:118px;top:-44px;width:64px;height:58px;border-radius:50%;background:linear-gradient(180deg,#F6F7F9,#C9D0D8)}
#mg_height .eye{position:absolute;top:70px;width:14px;height:18px;border-radius:50%;background:#3A2A22}
#mg_height .glass{position:absolute;top:58px;width:46px;height:40px;border-radius:50%;border:5px solid #8A6A50}
#mg_height .pain{position:absolute;left:176px;top:210px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,rgba(229,57,53,.95) 22%,rgba(229,57,53,.45) 45%,rgba(229,57,53,0) 70%);opacity:0}
#mg_height .ring{position:absolute;left:176px;top:210px;width:120px;height:120px;border-radius:50%;border:6px solid rgba(229,57,53,.8);opacity:0}
#mg_height .arrow{position:absolute;left:840px;top:640px;width:70px;height:150px;opacity:0}
#mg_height .ground{position:absolute;left:150px;top:1192px;width:780px;height:40px;border-radius:50%;background:radial-gradient(closest-side,rgba(11,42,58,.22),rgba(11,42,58,0))}
"""
ticks = ''.join(f'<i style="top:{20+k*44}px;width:{36 if k%2 else 56}px"></i>' for k in range(14))
hbody = ('<div class="title"><span class="t1">身高下降</span><span class="t2">・<em>背部痛</em></span></div><div class="ground"></div>'
  f'<div class="ruler">{ticks}</div><div class="mark" style="left:150px;width:660px;top:540px"></div>'
  '<div class="fig"><div class="leg a"></div><div class="leg b"></div><div class="shoe" style="left:70px"></div><div class="shoe" style="left:144px"></div>'
  '<div class="up"><div class="arm l"></div><div class="arm r"></div><div class="torso"></div><div class="spine">'
  + ''.join(f'<i style="top:{k*36}px"></i>' for k in range(7)) +
  '</div><div class="neck"></div><div class="head"></div><div class="hair"></div><div class="bun"></div>'
  '<div class="glass" style="left:104px"></div><div class="glass" style="left:154px"></div><div class="eye" style="left:120px"></div><div class="eye" style="left:170px"></div>'
  '<div class="pain"></div><div class="ring"></div></div></div>'
  '<svg class="arrow" viewBox="0 0 70 150"><path d="M35 0 V120 M8 96 L35 140 L62 96" fill="none" stroke="#545454" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
  '')
hjs = r"""
tl.set(q('.title'),{opacity:1},0); tl.fromTo(q('.t1'),{opacity:0},{opacity:0},0); tl.fromTo(q('.t2'),{opacity:0},{opacity:0},0);
tl.fromTo(q('.ruler'),{scaleY:0,transformOrigin:'50% 100%'},{scaleY:1,duration:0.5,ease:'power3.out'},0.15);
tl.set(q('.fig'),{transformOrigin:'150px 620px'},0); tl.fromTo(q('.fig'),{opacity:0,y:60,scale:1.0},{opacity:1,y:0,duration:0.5,ease:'back.out(1.5)'},0.25);
tl.to(q('.mark'),{opacity:1,duration:0.3},0.6);
var t0=c(0,0.2)+0.3;
tl.to(q('.fig'),{scaleY:0.88,duration:1.1,ease:'power2.inOut'},t0);
tl.to(qa('.spine i'),{scaleY:0.7,duration:1.1,ease:'power2.inOut',stagger:0.03},t0);
tl.fromTo(q('.arrow'),{opacity:0,y:-40},{opacity:1,y:30,duration:0.9,ease:'power2.out'},t0+0.2);
tl.to(q('.mark'),{borderTopColor:'#545454',duration:0.3},t0+0.6);
tl.fromTo(q('.t1'),{opacity:0,y:-20},{opacity:1,y:0,duration:0.4,ease:'back.out(1.8)'},c(0,0.2));
var t1=c(1,3.1);
tl.to(q('.up'),{rotation:22,duration:0.9,ease:'power2.inOut'},t1-0.45);
tl.to(qa('.arm'),{rotation:-18,duration:0.9,ease:'power2.inOut'},t1-0.45);
tl.fromTo(q('.pain'),{opacity:0,scale:0.6},{opacity:1,scale:1.15,duration:0.45,yoyo:true,repeat:5,ease:'sine.inOut'},t1);
tl.fromTo(q('.ring'),{opacity:0.9,scale:0.7},{opacity:0,scale:1.8,duration:0.8,repeat:2,ease:'power1.out'},t1);
tl.fromTo(q('.t2'),{opacity:0,y:-20},{opacity:1,y:0,duration:0.4,ease:'back.out(1.8)'},t1);
"""
write('mg_height', 5.6, hcss, hbody, hjs)

# ---------- 4) T-Score 直向玻璃溫度計（cues：標題、到 -1、偏低、到 -2.5、骨質疏鬆）----------
def Y(v): return 560 + (1 - v) / 4 * 760
tcss = r"""
#mg_tscore .tube{position:absolute;left:330px;width:110px;border-radius:55px;padding:10px;background:linear-gradient(90deg,rgba(255,255,255,.95),rgba(225,236,246,.85));box-shadow:0 18px 36px rgba(11,42,58,.18),inset 0 0 0 3px rgba(255,255,255,.9)}
#mg_tscore .fill{position:relative;width:90px;height:100%;border-radius:45px;overflow:hidden}
#mg_tscore .fill i{position:absolute;left:0;right:0}
#mg_tscore .shine{position:absolute;left:22px;top:24px;width:16px;bottom:24px;border-radius:8px;background:linear-gradient(180deg,rgba(255,255,255,.75),rgba(255,255,255,.15))}
#mg_tscore .lab{position:absolute;left:80px;width:210px;text-align:right;font:900 66px/1 "Noto Sans TC";color:#0B2A3A;transform:translateY(-50%)}
#mg_tscore .tk{position:absolute;left:316px;width:138px;height:6px;border-radius:3px;background:rgba(11,42,58,.28);transform:translateY(-50%)}
#mg_tscore .ptr{position:absolute;left:300px;width:170px;height:0}
#mg_tscore .ptr .ring{position:absolute;left:0;top:-34px;width:170px;height:68px;border-radius:34px;border:8px solid #0B2A3A;box-sizing:border-box;background:rgba(255,255,255,.25);box-shadow:0 6px 14px rgba(11,42,58,.25)}
#mg_tscore .ptr .val{position:absolute;left:10px;top:-120px;padding:8px 22px 12px;border-radius:20px;background:#0B2A3A;color:#fff;font:900 60px/1 "Noto Sans TC";white-space:nowrap}
#mg_tscore .zone{position:absolute;left:540px;padding:14px 28px 18px;border-radius:24px;font:900 62px/1 "Noto Sans TC";opacity:0;transform:translateY(-50%);white-space:nowrap;box-shadow:0 10px 22px rgba(11,42,58,.18)}
#mg_tscore .zone.n{background:linear-gradient(180deg,#41C172,#2EAD5B);color:#fff} #mg_tscore .zone.z1{background:linear-gradient(180deg,#FBD24E,#F2BD1E);color:#3A2E00} #mg_tscore .zone.z2{background:linear-gradient(180deg,#E8474E,#C81F28);color:#fff}
"""
T0, B_ = Y(1), Y(-3)
tbody = ('<div class="title"><em>T-Score</em> 怎樣看？</div>'
  f'<div class="tube" style="top:{T0-10}px;height:{B_-T0}px"><div class="fill">'
  f'<i style="top:0;height:{Y(-1)-T0}px;background:linear-gradient(180deg,#58D08A,#2EAD5B)"></i>'
  f'<i style="top:{Y(-1)-T0}px;height:{Y(-2.5)-Y(-1)}px;background:linear-gradient(180deg,#FCDA63,#F2BD1E)"></i>'
  f'<i style="top:{Y(-2.5)-T0}px;bottom:0;background:linear-gradient(180deg,#EF5A60,#C81F28)"></i><div class="shine"></div></div></div>'
  + ''.join(f'<div class="lab" style="top:{Y(v)}px">{l}</div><div class="tk" style="top:{Y(v)}px"></div>' for v, l in [(1, '+1'), (0, '0'), (-1, '-1'), (-2.5, '-2.5'), (-3, '-3')])
  + f'<div class="ptr" style="top:{Y(0.5)}px"><div class="ring"></div><div class="val">0.5</div></div>'
  + f'<div class="zone n" style="top:{(Y(1)+Y(-1))/2}px">正常</div>'
  + f'<div class="zone z1" style="top:{(Y(-1)+Y(-2.5))/2}px">骨質密度偏低</div>'
  + f'<div class="zone z2" style="top:{(Y(-2.5)+Y(-3))/2+12}px">骨質疏鬆</div>')
tjs = f"""
tl.fromTo(q('.title'),{{opacity:0,y:-24}},{{opacity:1,y:0,duration:0.4,ease:'power3.out'}},c(0,0.2));
tl.fromTo(q('.tube'),{{scaleY:0,transformOrigin:'50% 0'}},{{scaleY:1,duration:0.6,ease:'power3.out'}},0.25);
tl.fromTo(qa('.lab'),{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3,stagger:0.06}},0.55);
tl.fromTo(qa('.tk'),{{opacity:0}},{{opacity:1,duration:0.3,stagger:0.06}},0.55);
tl.fromTo(q('.ptr'),{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.35,ease:'back.out(1.6)'}},0.8);
tl.fromTo(q('.zone.n'),{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.35}},0.95);
var V=q('.val'), o={{v:0.5}}; function upd(){{ V.textContent=(o.v>0?'+':'')+o.v.toFixed(1); }}
tl.to(o,{{v:-1,duration:0.8,ease:'back.out(1.2)',onUpdate:upd}},c(1,1.55)-0.4);
tl.to(q('.ptr'),{{y:{Y(-1)-Y(0.5)},duration:0.8,ease:'back.out(1.2)'}},c(1,1.55)-0.4);
tl.to(q('.zone.n'),{{opacity:0.3,duration:0.3}},c(2,2.6)-0.2);
tl.fromTo(q('.z1'),{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.4,ease:'back.out(1.8)'}},c(2,2.6));
tl.to(o,{{v:-2.5,duration:0.9,ease:'back.out(1.2)',onUpdate:upd}},c(3,4.9)-0.4);
tl.to(q('.ptr'),{{y:{Y(-2.5)-Y(0.5)},duration:0.9,ease:'back.out(1.2)'}},c(3,4.9)-0.4);
tl.to(q('.z1'),{{opacity:0.3,duration:0.3}},c(4,6.9)-0.2);
tl.fromTo(q('.z2'),{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.4,ease:'back.out(1.8)'}},c(4,6.9));
"""
write('mg_tscore', 7.9, tcss, tbody, tjs)
print('ok')

# ---------- 5) 25%（cues：大字、人形、note）29 Odometer ----------
qcss = r"""
#mg_quarter .odo{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;gap:16px;align-items:center;opacity:0}
#mg_quarter .tile{position:relative;width:150px;height:200px;border-radius:24px;overflow:hidden;background:linear-gradient(180deg,#FFFFFF,#E7EFF7);box-shadow:inset 0 3px 0 #fff,0 14px 28px rgba(11,42,58,.18)}
#mg_quarter .tile::after{content:"";position:absolute;left:0;right:0;top:99px;height:3px;background:rgba(11,42,58,.12)}
#mg_quarter .col{position:absolute;left:0;top:0;width:150px}
#mg_quarter .col b{display:block;height:200px;font:900 170px/200px "Noto Sans TC";text-align:center;color:#1A80D0}
#mg_quarter .pct{font:900 150px/1 "Noto Sans TC";color:#1A80D0;margin-left:6px}
#mg_quarter .ppl{position:absolute;left:0;right:0;top:760px;display:flex;justify-content:center;gap:50px}
#mg_quarter .pp{position:relative;width:170px;height:330px;opacity:0}
#mg_quarter .pp .h{position:absolute;left:48px;top:0;width:74px;height:74px;border-radius:50%;background:radial-gradient(circle at 40% 38%,#FBE2CB,#F0C9A6 60%,#E2B48E)}
#mg_quarter .pp .hair{position:absolute;left:44px;top:-10px;width:82px;height:44px;border-radius:40px 40px 14px 14px;background:linear-gradient(180deg,#F2F4F6,#C7CED6)}
#mg_quarter .pp .bun{position:absolute;left:66px;top:-34px;width:38px;height:34px;border-radius:50%;background:linear-gradient(180deg,#F6F7F9,#C9D0D8)}
#mg_quarter .pp .bd{position:absolute;left:20px;top:86px;width:130px;height:236px;border-radius:70px 70px 26px 26px;clip-path:polygon(26% 0,74% 0,100% 100%,0 100%);background:linear-gradient(90deg,#9FB7C9,#C5D5E2 45%,#9FB7C9)}
#mg_quarter .pp.hl .bd{background:linear-gradient(90deg,#1468AE,#3B97E0 45%,#1468AE)}
#mg_quarter .pp .glow{position:absolute;left:-20px;top:-40px;width:210px;height:400px;border-radius:50%;background:radial-gradient(closest-side,rgba(26,128,208,.28),rgba(26,128,208,0));opacity:0}
"""
cols = ''.join(f'<div class="tile"><div class="col c{k}">' + ''.join(f'<b>{d}</b>' for d in list(range(10))+[0,1,2,3,4,5]) + '</div></div>' for k in range(2))
qbody = ('<div class="odo">' + cols + '<span class="pct">%</span></div><div class="ppl">'
  + ''.join(f'<div class="pp pp{i}{" hl" if i==3 else ""}"><i class="glow"></i><i class="bd"></i><i class="h"></i><i class="hair"></i><i class="bun"></i></div>' for i in range(4))
  + '</div><div class="pills"><div class="pill p0">65歲或以上女性</div></div>')
qjs = r"""
var t0=c(0,0.3);
tl.fromTo(q('.odo'),{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:'back.out(1.6)'},Math.max(0.05,t0-0.2));
tl.fromTo(q('.c0'),{y:0},{y:-200*12,duration:1.1,ease:'power3.out'},t0);
tl.fromTo(q('.c1'),{y:0},{y:-200*15,duration:1.4,ease:'power3.out'},t0);
qa('.pp').forEach(function(p,i){ tl.fromTo(p,{opacity:0,y:40},{opacity:1,y:0,duration:0.35,ease:'back.out(1.7)'},c(1,0.8)+i*0.12); });
var th=c(1,0.8)+0.7; tl.to(q('.pp3 .glow'),{opacity:1,duration:0.3},th);
tl.fromTo(q('.pp3'),{scale:1},{scale:1.1,transformOrigin:'50% 100%',duration:0.22,yoyo:true,repeat:3},th);
pill(q('.p0'),c(2,2.0));
"""
write('mg_quarter', 4.6, qcss, qbody, qjs)
