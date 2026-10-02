import json, re, subprocess, sys, os
L=os.path.expanduser('~/mnt/Documents/GitHub/video-fx-skill'); P=os.path.expanduser('~/hf/d2k')
beats=json.load(open(f'{L}/storyboards/doctor2-k-beats.json'))
src=open(os.path.expanduser('~/hf/dfull5/index.html')).read()
# 1) 拆走舊 overlay HTML
def cut_line(t, pat):
    return re.sub(r'\n[^\n]*'+pat+r'[^\n]*', '', t, count=1)
for pat in [r'<div class="side" id="sg0"', r'<div class="imgc clip" id="i1"', r'<div id="hero">']:
    src=cut_line(src, pat)
src=re.sub(r'\n\s*<div id="card1".*?\n\s*</div>(?=\n\s*<div id="card2")', '', src, flags=re.S)
src=re.sub(r'\n\s*<div id="card2".*?\n\s*</div>(?=\n\s*<img id="logo")', '', src, flags=re.S)
src=re.sub(r'/\* 主角元素.*?(?=/\* 字幕 FX-051)', '/* 風格包卡 host：一定要有 z-index，否則喺 #cam（z 2）後面 */\n.cardhost{position:absolute;inset:0;z-index:12}\n.cardhost.t1{z-index:14}\n', src, flags=re.S)
# 2) 拆走舊 script 段落（主角／chip／圖片／全屏卡）
src=re.sub(r'// ---------- 主角元素.*?(?=// ---------- 字幕)', '', src, flags=re.S)
# 3) 字幕：全屏卡時段唔出
T1=[(b['t0'], b['t0']+b['dur']) for b in beats if b.get('mode')=='card']
m=re.search(r'const D=(\{.*?\});\n', src, re.S); D=json.loads(m.group(1))
D['CAM']=[[0,1.35,1.4,3.4,0],[3.4,None,1.0,3.85,0],[3.85,1.0,1.0,4.42,0],[4.42,None,1.3,6.4,0],[6.4,1.3,1.32,9.92,0],
 [9.92,1.0,1.02,17.48,0],[17.48,None,1.3,18.2,0],[18.2,1.3,1.32,20.52,0],[20.52,None,1.0,21.2,0],[21.2,1.0,1.02,26.78,0],
 [33.76,1.0,1.02,36.46,0],[36.46,None,1.3,37.2,0],[37.2,1.3,1.33,41.34,0],
 [52.36,1.1,1.12,57.76,430],[57.76,1.0,1.03,62.16,0],[62.16,None,1.3,62.9,0],[62.9,1.3,1.32,64.74,0],[64.74,None,1.0,65.4,0],[65.4,1.0,1.02,68.3,0],[73.5,1.0,1.02,76.24,0]]
# 用戶 2026-10-02：人物對人物直接硬切放大（1.0↔1.3）似跳鏡，唔自然 → 人物接人物一律用 0.7 秒平滑推／拉（s0=None）；只有由全屏畫面返嚟先硬切
D['CAPS']=[c for c in D['CAPS'] if not any(c[1] < e-0.05 and c[2] > s+0.05 for s,e in T1)]
SK=[x for b in beats for x in b.get('skipcaps',[])]
miss=[x for x in SK if not any(abs(c[1]-x)<0.02 for c in D['CAPS'])]
if miss: print('! skipcaps 搵唔到字幕：',miss)
D['CAPS']=[c for c in D['CAPS'] if not any(abs(c[1]-x)<0.02 for x in SK)]

src=src[:m.start(1)]+json.dumps(D, ensure_ascii=False)+src[m.end(1):]
# 用戶 2026-10-02：效果唔好貼面 → 名牌放右下角、開場大字同心電圖線向下移
for a,b_ in [("#tag{position:absolute;left:355px;top:965px;","#tag{position:absolute;left:640px;top:1180px;"),
             ("#ecgHook{position:absolute;left:0;top:860px;width:1080px;height:200px;","#ecgHook{position:absolute;left:0;top:1272px;width:1080px;height:110px;"),
             ('<svg id="ecgHook" viewBox="0 0 1080 200">','<svg id="ecgHook" viewBox="0 0 1080 200" preserveAspectRatio="none">'),
             ("#hook{position:absolute;left:52px;right:52px;top:1040px;","#hook{position:absolute;left:52px;right:52px;top:940px;")]:
    assert a in src, a; src=src.replace(a,b_)
old_cam="""D.CAM.forEach(([t,s0,s1,t1])=>{ if(s0!==null) tl.set('#camInner',{scale:s0},t);"""
assert old_cam in src
src=src.replace(old_cam, """D.CAM.forEach(([t,s0,s1,t1,y])=>{ if(s0!==null) tl.set('#camInner',{scale:s0,y:y||0},t);""")
# 4) 卡
mounts=[]
for i,b in enumerate(beats):
    cmd=['python3', f'{L}/tools/cards.py','use',b['card'],'--project',P,'--name',b['name'],'--dur',str(b['dur']),'--slots',json.dumps(b['slots'],ensure_ascii=False),'--cues',b['cues'],'--brand','healthy-days']
    r=subprocess.run(cmd,capture_output=True,text=True); out=r.stdout+r.stderr
    if r.returncode: sys.exit(out)
    for l in out.splitlines():
        if l.startswith('!'): print(b['name'], l)
    mounts.append(f'  <div class="cardhost{" t1" if b["tier"]=="tier1" else ""}" data-composition-id="{b["name"]}" data-composition-src="compositions/{b["name"]}.html" data-dur="{b["dur"]}" data-cues="{b["cues"]}" data-start="{b["t0"]}" data-duration="{b["dur"]}" data-width="1080" data-height="1920" data-track-index="{30+i}"></div>')
src=src.replace('  <img id="logo"', '\n'.join(mounts)+'\n  <img id="logo"', 1)
# 5) manifest：卡字
man=[x for x in json.loads(re.search(r'<script type="application/json" id="fx-manifest">(.*?)</script>', src, re.S).group(1)) if x['kind'] in ('hook','nametag','caption')]
man=[x for x in man if x['kind']!='caption' or any(abs(x['start']-c[1])<0.01 for c in D['CAPS'])]
for b in beats:
    cues=[float(c) for c in b['cues'].split(',')]
    for k,v in b['slots'].items():
        if not v: continue
        man.append({'id':f"{b['name']}_{k}",'kind':'card','text':re.sub(r'<[^>]+>|\*|｜','',v),'start':round(b['t0']+cues[0],2),'end':round(b['t0']+b['dur'],2),'spoken':k not in ('title','name','kicker','c1_k','c2_k'),'comp':b['card'],'beat':b['tier']})
src=re.sub(r'(<script type="application/json" id="fx-manifest">).*?(</script>)', lambda mm: mm.group(1)+json.dumps(man,ensure_ascii=False)+mm.group(2), src, flags=re.S)
open(f'{P}/index.html','w').write(src); print('ok', len(D['CAPS']), 'caps')
