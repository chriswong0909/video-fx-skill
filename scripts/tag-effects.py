#!/usr/bin/env python3
"""tag-effects.py — 每個效果加 component（屬邊類零件）同 entry（入場文法），寫入 effect.md front matter
  python3 scripts/tag-effects.py            # 補未有嘅（已人手填就唔郁）
  python3 scripts/tag-effects.py --force    # 全部重算
零件（通用 9 類）：caption 字幕｜capsule 膠囊／標籤／名牌｜headline 大字｜card 卡片／清單｜chart 圖表／數字
                   cutaway 全屏過場｜accent 點綴｜frame 版面／畫中畫｜camera 鏡頭／轉場／調色
入場：slide-edge 由邊伸出｜rise 浮入｜scale 縮放彈出｜draw 劃線／遮罩｜blur 模糊入｜fade 淡入｜rotate 轉入｜type 打字｜cut 硬切
"""
import glob, os, re, sys

CAPSULE = {'lower-third', 'name', 'pill', 'label', 'badge', 'sticker', 'tags', 'stamp', 'pills', 'top-title', 'header', 'title'}
CHART = {'chart', 'number', 'stat', 'bar-chart', 'growth', 'ranking', 'big-number', 'data', 'comparison', 'table'}

def component(fm):
    cat = fm.get('category', ''); tags = set(fm.get('tags', []))
    if cat == 'caption': return 'caption'
    if cat in ('transition', 'grade-light') and not tags & {'big-type', 'one-word', 'title', 'flash'}: return 'camera'
    if cat == 'list-chart': return 'chart' if tags & CHART else 'card'
    if cat == 'cutaway': return 'chart' if 'map' in tags else 'cutaway'
    if cat == 'layout': return 'capsule' if tags & {'chapter', 'navigation'} else 'frame'
    if cat == 'accent': return 'capsule' if tags & {'badge', 'stamp', 'notification'} else 'accent'
    if tags & CAPSULE: return 'capsule'
    return 'headline'

def entries(snip):
    out = set()
    for m in re.finditer(r'tl\.(from|fromTo)\(\s*[^,]+,\s*\{([^}]*)\}', snip):
        keys = set(re.findall(r'([A-Za-z]+)\s*:', m.group(2))) - {'duration', 'ease', 'stagger', 'delay', 'transformOrigin', 'immediateRender'}
        if keys & {'scaleX', 'scaleY', 'attr', 'strokeDashoffset', 'clipPath', 'drawSVG', 'width', 'height'}: out.add('draw')
        elif keys & {'filter'}: out.add('blur')
        elif keys & {'x', 'xPercent'}: out.add('slide-edge')
        elif keys & {'y', 'yPercent'}: out.add('rise')
        elif keys & {'scale'}: out.add('scale')
        elif keys & {'rotation', 'rotationX', 'rotationY'}: out.add('rotate')
        elif keys == {'opacity'} or keys == {'autoAlpha'}: out.add('fade')
    if 'textContent' in snip: out.add('type')
    if not out and re.search(r'tl\.set\(', snip): out.add('cut')
    return sorted(out)

def parse_fm(txt):
    m = re.match(r'^---\n(.*?)\n---', txt, re.S); fm = {}
    for line in m.group(1).split('\n'):
        mm = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if not mm: continue
        v = mm.group(2).strip()
        fm[mm.group(1)] = [x.strip().strip('"\'') for x in v[1:-1].split(',') if x.strip()] if v.startswith('[') else v.strip('"\'')
    return m, fm

if __name__ == '__main__':
    force = '--force' in sys.argv; root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')); n = 0; stat = {}
    for d in sorted(glob.glob(os.path.join(root, 'effects/FX-*'))):
        p = os.path.join(d, 'effect.md'); sp = os.path.join(d, 'snippet.html')
        if not os.path.exists(p): continue
        txt = open(p, encoding='utf-8').read(); m, fm = parse_fm(txt)
        comp = fm.get('component') if (fm.get('component') and not force) else component(fm)
        ent = fm.get('entry') if (fm.get('entry') and not force) else (entries(open(sp, encoding='utf-8').read()) if os.path.exists(sp) else [])
        body = re.sub(r'\n(component|entry):.*', '', m.group(1))
        body += f'\ncomponent: {comp}\nentry: [{", ".join(ent)}]'
        new = '---\n' + body + '\n---' + txt[m.end():]
        if new != txt: open(p, 'w', encoding='utf-8').write(new); n += 1
        stat[comp] = stat.get(comp, 0) + 1
    print(f'✓ 更新 {n} 個 effect.md；零件分佈：' + '  '.join(f'{k} {v}' for k, v in sorted(stat.items(), key=lambda x: -x[1])))
