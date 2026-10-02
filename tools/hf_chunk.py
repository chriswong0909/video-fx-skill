# hf_chunk.py T0 T1 NAME [PROJECT_DIR] — 將主檔切一段出嚟獨立 render（device_bash 每次最多 180 秒；切位要揀冇卡嘅時間）
import re, sys, os, shutil
T0=float(sys.argv[1]); T1=float(sys.argv[2]); name=sys.argv[3]; L=round(T1-T0,3)
P=os.path.abspath(sys.argv[4]) if len(sys.argv)>4 else os.getcwd(); O=os.path.join(os.path.dirname(P),name)
os.makedirs(O,exist_ok=True)
for d in ('assets','compositions'):
    if not os.path.exists(f'{O}/{d}'): os.symlink(f'{P}/{d}',f'{O}/{d}')
for f in ('hyperframes.json','meta.json'):
    if os.path.exists(f'{P}/{f}'): shutil.copy(f'{P}/{f}',O)
src=open(f'{P}/index.html').read()
def fix(m):
    tag=m.group(0)
    s=float(re.search(r'data-start="([\d.]+)"',tag).group(1)); dm=re.search(r'data-duration="([\d.]+)"',tag)
    d=float(dm.group(1)) if dm else None
    if 'id="main"' in tag: return re.sub(r'data-duration="[\d.]+"',f'data-duration="{L}"',tag)
    e=s+d if d is not None else None
    if e is not None and (e<=T0+1e-6 or s>=T1-1e-6): return '<div hidden data-removed="1"'+('>' if tag.endswith('>') else '')
    ns=max(0,s-T0); ne=min(T1,e)-T0 if e is not None else None
    if 'data-composition-src' in tag and (s<T0-1e-6 or e>T1+1e-6): raise SystemExit(f'✗ 卡跨過切位：{tag[:120]}')
    tag=re.sub(r'data-start="[\d.]+"',f'data-start="{round(ns,3)}"',tag)
    if d is not None: tag=re.sub(r'data-duration="[\d.]+"',f'data-duration="{round(ne-ns,3)}"',tag)
    if tag.startswith('<video'): tag=tag.replace('<video',f'<video data-media-start="{round(max(T0,s)-s,3)}"',1)
    return tag
src=re.sub(r'<(?:div|video|svg|img)\b[^>]*\bdata-start="[\d.]+"[^>]*>',fix,src)
src=re.sub(r'<div hidden data-removed="1">\s*(<div class="in"></div>)?\s*</div>','',src)
a="window.__timelines['main']=tl;"
assert a in src
src=src.replace("const END=D.END;","const END=D.END; const CH0=%s, CHL=%s;"%(T0,L))
src=src.replace(a,"const W=gsap.timeline({paused:true}); W.add(tl.tweenFromTo(CH0,CH0+CHL,{ease:'none'}),0); window.__timelines['main']=W;")
open(f'{O}/index.html','w').write(src); print('ok',name,T0,T1,'removed',src.count('data-removed'))
