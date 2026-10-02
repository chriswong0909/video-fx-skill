import json, glob, base64, io, html, os, re
from PIL import Image
L=os.path.expanduser('~/mnt/Documents/GitHub/video-fx-skill')
B=json.load(open(f'{L}/storyboards/doctor2-k-beats.json'))
P=json.load(open(f'{L}/styles/kallaway/portrait.json'))
fr={float(re.search(r'-at-([\d.]+)s',f).group(1)):f for f in glob.glob('snapshots/frame-*.png')}
def img(t):
    k=min(fr,key=lambda x:abs(x-t)); im=Image.open(fr[k]).convert('RGB'); im.thumbnail((360,640))
    b=io.BytesIO(); im.save(b,'JPEG',quality=74); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def fmt(s): return f'{int(s//60)}:{s%60:05.2f}'
E=html.escape
rows=[]
SN={x['id']:x['name'] for x in json.load(open(f'{L}/registry.json'))['sounds']}
EV=json.load(open('sfx-events.json'))
def sfxof(a,b): return '；'.join(f"{e['t']:.1f}s {SN.get(e['sfx'],e['sfx'])}（{e['why']}）" for e in EV if a-0.06<=e['t']<b-0.06) or '冇'
ML={'full':'全屏圖片','card':'全屏資訊卡','split':'人物加圖片（上圖下人）','pip':'人物加圖片（浮框）','person':'見人物','brand':'品牌固定'}
rows.append(dict(name='開場',t0=0,t1=4.42,cap='開場大字取代',mode='brand',card='Healthy Days 品牌開場（沿用 v5）',anchor='如果以前行樓梯沒問題，現在行一層樓梯便氣喘，便要小心',slots='行一層／便氣喘？',why='特寫＋心電圖線＋大字撞入（大字同心電圖線已向下移，離面遠啲）',imgs=[2.6],status='brand'))
rows.append(dict(name='名牌',t0=4.42,t1=7.18,mode='brand',card='Healthy Days 名牌 + 字幕',anchor='有機會可能心臟泵血功能下降',slots='心臟科專科醫生 江振昌',why='句首慢慢推近；名牌改放右下角',imgs=[5.6],status='brand'))
for b in B:
    st='ok' if P.get(b['card'],{}).get('verified') else 'new'
    sl=' ／ '.join(re.sub(r'<[^>]+>|\*','',v).replace('｜',' ') for k,v in b['slots'].items() if v and k not in ('img','pos','p1','p2','p3','p4'))
    c=[float(x) for x in b['cues'].split(',')]; tail=0.15 if b['mode'] in('full','split') else 0.55
    ts=[round(min(b['t0']+c[-1]+0.9,b['t0']+b['dur']-tail),2)]
    capnote='資訊卡時段唔出字幕' if b['mode']=='card' else ('效果字已交代，呢句字幕唔出' if b.get('skipcaps') else '照出')
    rows.append(dict(cap=capnote,name=b['name'],t0=b['t0'],t1=b['t0']+b['dur'],mode=b['mode'],card=b['card'].replace('kallaway.',''),anchor=b['anchor'],slots=sl,why=b['why'],imgs=ts,status=st))
    if b['name']=='b15': rows.append(dict(name='淨人物',t0=64.74,t1=68.3,mode='person',card='冇卡，只有字幕',anchor='如果病情是有需要的話，現在醫學上有些藥物',slots='—',why='留白畀講者，之後入藥物卡',imgs=[66.0],status='brand'))
tot={}
segs=sorted([(b['t0'],b['t0']+b['dur'],b['mode']) for b in B])
F=sum(e-s for s,e,m in segs if m in('full','card')); S=sum(e-s for s,e,m in segs if m in('split','pip')); PP=80.3-F-S
RATIO=f'見人物 {PP:.0f} 秒（{PP/80.3*100:.0f}%）｜全屏 {F:.0f} 秒（{F/80.3*100:.0f}%）｜人物加圖片 {S:.0f} 秒（{S/80.3*100:.0f}%）'
print(RATIO)
cards=[]
for r in rows:
    tierlab=ML[r['mode']]; r['tier']={'full':'tier1','card':'tier1','split':'mix','pip':'mix','person':'tier2','brand':'brand'}[r['mode']]
    stlab={'ok':'已驗證','new':'新改 · 待你批','brand':'沿用'}[r['status']]
    ims=''.join(f'<figure><img src="{img(t)}" alt="{E(r["name"])} {t} 秒畫面" loading="lazy"><figcaption>{t:.2f}s</figcaption></figure>' for t in r['imgs'])
    cards.append(f'''<article class="beat {r["tier"]}"><div class="shots">{ims}</div><div class="info">
<div class="meta"><span class="id">{E(r["name"])}</span><span class="time">{fmt(r["t0"])} – {fmt(r["t1"])}</span><span class="pill t-{r["tier"]}">{tierlab}</span><span class="pill s-{r["status"]}">{stlab}</span></div>
<p class="spoken">「{E(r["anchor"])}」</p>
<dl><dt>卡</dt><dd><code>{E(r["card"])}</code></dd><dt>卡上字</dt><dd>{E(r["slots"])}</dd><dt>點解</dt><dd>{E(r["why"])}</dd><dt>聲效</dt><dd>{E(sfxof(r["t0"],r["t1"]))}</dd><dt>字幕</dt><dd>{E(r.get("cap","照出"))}</dd></dl></div></article>''')
tpl=open('page_tpl.html').read()
open(os.path.expanduser('~/mnt/Video editing/doctor2/_work/d2k/doctor2-k-beats.html'),'w').write(tpl.replace('%%BEATS%%','\n'.join(cards)).replace('%%RATIO%%',RATIO))
print(len(cards))
