#!/usr/bin/env python3
"""出節拍表頁（Artifact）：每拍真截圖、時間、原句、卡 id、卡上字、聲效、字幕出唔出、畫面比例"""
import json, base64, os, html
L=os.environ.get('FXLIB','/home/claude/lib'); P=os.path.dirname(os.path.abspath(__file__))
B=json.load(open(f'{L}/storyboards/40s-beats.json')); END=39.33
def img(p):
    return 'data:image/jpeg;base64,'+base64.b64encode(open(p,'rb').read()).decode()
SHOT={'q1':['2'],'pip1':['4.4','7.3'],'q2':['7.3'],'name':['8.8'],'img2':['10.6'],'split3':['13','15.8'],'flow4':['19','23.8'],'hold1':['26'],'img5':['29.8'],'hold2':['31.2'],'split6':['33.6'],'list7':['36.2','38']}
CAPNOTE={'q1':'「會唔會有一個憂慮」出；後半句由問題卡交代，唔出','pip1':'全句出字幕：「佢哋會唔會覺得」「AI俾我嘅判斷」「會更加準確」（Q2 唔用問題卡）','q2':'唔出（問題卡交代）','name':'「其實老師呢件事」出',
 'img2':'唔出（大字交代）','split3':'「仲有好多範圍」出；之後由關鍵詞卡交代，唔出','flow4':'唔出（資訊卡時段）','hold1':'出：「但實際上去到」「真係幫學生去了解佢」',
 'img5':'「點解佢唔鍾意作文呢」出；第一句由大字交代','hold2':'出：「好唔鍾意譬如ICT」「或者某啲科」','split6':'出：「可能都係由老師去開解」「老師去了解佢」','list7':'唔出（資訊卡時段）'}
MODE={'person':('人物','m-p'),'pip':('人物加圖片','m-x'),'split':('人物加圖片','m-x'),'full':('全屏圖片','m-f'),'card':('全屏資訊卡','m-f')}
NEW={k:'新改 9:16，等你批' for k in ('kallaway.t2.label.qmark','kallaway.t2.lower-third.glasscard','kallaway.t1.overview.flow','kallaway.x.photo.full','kallaway.x.photo.split','kallaway.x.photo.frame')}
SRC={'kallaway.t2.label.qmark':'風格包原卡 QMARK','kallaway.t2.lower-third.glasscard':'風格包原卡 GLASSCARD','kallaway.t1.overview.flow':'風格包原卡 FLOW','kallaway.t1.overview.checklist':'風格包原卡 CHECKLIST','kallaway.t2.label.keyword':'風格包原卡 KEYWORD','kallaway.x.photo.full':'圖片底，冇字','kallaway.x.photo.split':'圖片底，冇字','kallaway.x.photo.frame':'借 PORTRAITFRAME 發光邊框'}
# 比例：按畫面段落計（q2 同 pip1 同一段）
seg=[('person',0,3.567),('pip',3.567,7.69),('person',7.69,9.5),('full',9.5,11.57),('split',11.57,16.367),('card',16.367,24.37),('person',24.37,27.89),('full',27.89,30.47),('person',30.47,32.667),('split',32.667,35.21),('card',35.21,END)]
tot={'m-p':0,'m-f':0,'m-x':0}
for m,a,b in seg: tot[MODE[m][1]]+=b-a
pct={k:round(v/END*100) for k,v in tot.items()}
nsfx=sum(len(b['sfx']) for b in B)
rows=[]
KIDS={}
for b in B:
    if b.get('parent'): KIDS.setdefault(b['parent'],[]).append(b)
for b in B:
    if b.get('parent'): continue
    name,cls=MODE[b['mode']]; e=b['t0']+b['dur']
    shots=''.join(f'<figure><img src="{img(f"{P}/shots/{s}.jpg")}" alt="{b["name"]} 喺 {s} 秒嘅截圖"><figcaption>{s}s</figcaption></figure>' for s in SHOT[b['name']])
    WK=('term','term2','note','name','role','title','i1','i2','i3','i4','n1','n2','n3','n4')
    words='、'.join(html.escape(v) for x in [b]+KIDS.get(b['name'],[]) for k,v in x['slots'].items() if k in WK and v) or '（冇卡字）'
    one=lambda c: f'<code>{c}</code> <span class="src">{SRC.get(c,"")}</span>'+(f' <span class="pill s-new">{NEW[c]}</span>' if c in NEW else ' <span class="pill s-ok">已有 9:16 版</span>')
    card='<br>'.join(one(x['card']) for x in [b]+KIDS.get(b['name'],[])) if b['card'] else '冇卡，只有講者同字幕'
    color=''
    sfx=''.join(f'<li><span class="t">{s["t"]:.2f}s</span> <code>{s["sfx"]}</code> {html.escape(s["why"])}</li>' for s in b['sfx']) or '<li>冇聲效</li>'
    rows.append(f'''<article class="beat {cls}" id="{b['name']}"><div class="shots">{shots}</div><div class="info">
<div class="meta"><span class="time">{b['t0']:.2f}–{e:.2f}s</span><span class="pill {cls}">{name}</span><span class="id">{b['name']}</span></div>
<p class="spoken">{html.escape(b['anchor'])}</p>
<dl><dt>卡</dt><dd>{card}{color}</dd><dt>卡上字</dt><dd>{words}</dd><dt>字幕</dt><dd>{CAPNOTE[b['name']]}</dd><dt>聲效</dt><dd><ul class="sfx">{sfx}</ul></dd><dt>點解</dt><dd>{html.escape(b['why'])}</dd></dl></div></article>''')
tpl=open(f'{P}/page_tpl.html').read()
out=tpl.replace('%%BEATS%%','\n'.join(rows)).replace('%%P%%',str(pct['m-p'])).replace('%%F%%',str(pct['m-f'])).replace('%%X%%',str(pct['m-x'])).replace('%%NSFX%%',str(nsfx)).replace('%%GRADE%%',img('/home/claude/40S/scratch/grade_cmp.jpg'))
open(f'{P}/40s-beatsheet.html','w').write(out); print('ok',len(out)//1024,'KB',pct,nsfx)
