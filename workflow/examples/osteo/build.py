import json, subprocess, sys, re
from caps import CAPS
P = '/home/claude/p'; L = '/home/claude/lib'
END = 95.86
beats = json.load(open(f'{P}/beats.json'))
CAM = json.load(open(f'{P}/cam.json'))

T1 = [(b['t0'], b['t0'] + b['dur']) for b in beats if b['tier'] == 'tier1']
# 返講者嘅鏡頭轉換搬去全屏卡遮住嘅時候（避免卡淡出時露出舊鏡頭）
for c in CAM:
    for a_, e_ in T1:
        if abs(c[0]-e_) < 0.7 or abs(c[0]-(e_-0.6)) < 0.05: c[0] = round(a_+0.4, 3)
CAM.sort()
SK = [x for b in beats for x in b.get('skipcaps', [])] + [0.139]
caps = []
for s, e, t in CAPS:
    if any(abs(s - x) < 0.02 for x in SK): continue
    parts = t.split('｜'); n = sum(len(p) for p in parts); t0 = s
    for p in parts:
        t1 = round(t0 + (e - s) * len(p) / n, 2); caps.append([round(t0, 2), t1, p]); t0 = t1
miss = [x for x in SK if not any(abs(c[0] - x) < 0.02 for c in CAPS)]
if miss: print('! skipcaps 搵唔到：', miss)

# 38 螢光筆（Healthy Days 唔用漸變字）：實色深海軍藍字 + #ffde59 螢光筆由左至右掃過
def highlight(name, sel, t):
    f = f'{P}/compositions/{name}.html'; h = open(f).read()
    css = (f'<style>#{name} {sel}{{background-image:linear-gradient(#ffde59,#ffde59)!important;background-repeat:no-repeat!important;'
           f'background-position:0 88%!important;background-size:0% 46%;-webkit-background-clip:border-box!important;background-clip:border-box!important;'
           f'-webkit-text-fill-color:#0B2A3A!important;color:#0B2A3A!important;filter:none!important;text-shadow:none!important;display:inline-block!important;padding:0 12px}}</style>')
    js = (f'<script>(function(){{var T=window.__timelines["{name}"];var R=document.querySelector(\'[data-composition-id="{name}"]\');'
          f'var el=R.querySelector("{sel}");T.fromTo(el,{{backgroundSize:"0% 46%"}},{{backgroundSize:"100% 46%",duration:0.45,ease:"power2.out"}},{t});}})();</script>')
    h = h.replace('</head>', css + '</head>', 1) if '</head>' in h else css + h
    i = h.rfind('</body>'); h = h[:i] + js + h[i:]
    open(f, 'w').write(h)

FL = {'mg_spine': ' data-nofade="1"', 'mg_tower': ' data-noin="1"', 'mg_tscore': ' data-nofade="1"'}
mounts = []
for i, b in enumerate(beats):
    if b['card'].startswith('mg_'):
        mounts.append(f'<div class="cardhost t1"{FL.get(b["card"], "")} data-composition-id="{b["card"]}" data-composition-src="compositions/{b["card"]}.html" data-dur="{b["dur"]}" data-cues="{b["cues"]}" data-start="{b["t0"]}" data-duration="{b["dur"]}" data-width="1080" data-height="1920" data-track-index="{30+i}"></div>')
        continue
    r = subprocess.run(['python3', f'{L}/tools/cards.py', 'use', b['card'], '--project', P, '--name', b['name'], '--dur', str(b['dur']),
                        '--slots', json.dumps(b['slots'], ensure_ascii=False), '--cues', b['cues'], '--brand', 'healthy-days'], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stdout + r.stderr)
    cues = [float(c) for c in b['cues'].split(',')]
    if b['card'] == 'kallaway.t2.label.keyword':
        highlight(b['name'], '.keyword', round(cues[0] + 0.3, 2))
    elif b['card'] == 'kallaway.x.image.full' and b['slots'].get('big'):
        tb = cues[1] if (b['slots'].get('title') and len(cues) > 1) else cues[0]
        highlight(b['name'], '.big', round(tb + 0.3, 2))
    mounts.append(f'<div class="cardhost{" t1" if b["tier"]=="tier1" else ""}" data-composition-id="{b["name"]}" data-composition-src="compositions/{b["name"]}.html" '
                  f'data-dur="{b["dur"]}" data-cues="{b["cues"]}" data-start="{b["t0"]}" data-duration="{b["dur"]}" data-width="1080" data-height="1920" data-track-index="{30+i}"></div>')

D = {'CAM': CAM, 'CAPS': caps, 'END': END}
html = open(f'{P}/tpl.txt').read()
html = html.replace('/*DATA*/', json.dumps(D, ensure_ascii=False)).replace('<!--CARDS-->', '\n  '.join(mounts)).replace('{END}', str(END))
open(f'{P}/index.html', 'w').write(html)
print('ok', len(caps), 'caps,', len(mounts), 'cards')
