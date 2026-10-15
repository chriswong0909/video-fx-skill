s=open('mg2.py').read()
i=s.index('# ---------- 2) 脊椎像一棟樓'); j=s.index('# ---------- 3) 身高下降')
new=r'''# ---------- 2) 真正嘅樓（cues：標題、疊上去、壓扁、變矮、傾斜）----------
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

'''
s=s[:i]+new+s[j:]
s+=r'''
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
'''
open('mg2.py','w').write(s); print('ok')
