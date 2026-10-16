#!/usr/bin/env python3
"""cards.py — 風格包卡片工具（新手包 kallaway / vox-explainer 為基礎，9:16 用到先改）

  python3 tools/cards.py list  [--style kallaway] [--tier tier1] [--purpose stat] [--portrait]
  python3 tools/cards.py show  <card-id>                      # slots、時長、有冇 9:16 版
  python3 tools/cards.py adapt <card-id>                      # 複製 16:9 原卡做 9:16 起點（之後人手改版面）
  python3 tools/cards.py adapt --ext 29 [--style kallaway] [--scale 2] [--top 1010] [--freeze 1.6]
        → 外部效果卡（text-motion-40 原作程式碼做起點）：header＋effect 包喺 IIFE、TL 改 paused、顏色讀品牌 tokens、
          舞台放大放 panel、登記 <style>.x.ext29（未驗證）。之後人手換字／調字級，見 workflow/external-effects.md
  python3 tools/cards.py use   <card-id> --project DIR --name beat03 --dur 8
                               [--slots '{"title":"…"}'] [--cues 0.9,1.4] [--brand healthy-days]
                               [--speed 1] [--freeze 秒] [--loops 1|3|auto] [--colors bg=#..,fg=#..,hi=#..,ink=#..]   # 後四個只用於外部效果卡
        → DIR/compositions/beat03.html（tokens 內嵌、slot 已填、時長已設、gsap 本地）＋ 印出掛載用 snippet
  python3 tools/cards.py verify <card-id> [--note "…"] [--source "text-motion-40#29"]  # 你批咗嘅 9:16 卡標記為已驗證（外部效果卡記來源）

卡片合約（新手包 style-library/GUIDE.md）：每張卡係獨立 composition；文字放 data-slot；
顏色字體緩動全部讀 tokens.css。9:16 版另外：根元素 1080×1920、可選 data-cues（逐項出現秒數，對講嘢時間）。
"""
import argparse, glob, html, json, os, re, shutil, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SD = os.path.join(ROOT, 'styles')

def styles():
    return sorted(d for d in os.listdir(SD) if os.path.isfile(os.path.join(SD, d, 'style.json')))

def load(style):
    s = json.load(open(os.path.join(SD, style, 'style.json')))
    pp = os.path.join(SD, style, 'portrait.json')
    p = json.load(open(pp)) if os.path.exists(pp) else {}
    return s, p

def find(card_id):
    style = card_id.split('.')[0]
    if style not in styles(): sys.exit(f'✗ 冇呢個風格：{style}（有：{", ".join(styles())}）')
    s, p = load(style)
    c = next((x for x in s['cards'] if x['id'] == card_id), None)
    if not c: sys.exit(f'✗ {style} 冇呢張卡：{card_id}')
    return style, s, p, c

def save_portrait(style, p):
    json.dump(p, open(os.path.join(SD, style, 'portrait.json'), 'w'), ensure_ascii=False, indent=1)

def cmd_list(a):
    n = 0
    for st in ([a.style] if a.style else styles()):
        s, p = load(st)
        for c in s['cards']:
            if a.tier and c['tier'] != a.tier: continue
            if a.purpose and c['purpose'] != a.purpose: continue
            pv = p.get(c['id'])
            if a.portrait and not pv: continue
            flag = ('9:16✓' if pv.get('verified') else '9:16…') if pv else '16:9 '
            slots = ','.join(x['name'] for x in c.get('slots', []))
            print(f"{flag}  {c['id']:42} {c['tier']}/{c['purpose']:11} slots: {slots}")
            n += 1
    print(f'— {n} 張')

def cmd_show(a):
    style, s, p, c = find(a.card)
    print(json.dumps(c, ensure_ascii=False, indent=1))
    print('9:16 版：', json.dumps(p.get(c['id']), ensure_ascii=False) if p.get(c['id']) else '未有（用 adapt 開始改）')

def ext_mod():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ext_effects
    return ext_effects

def cmd_adapt(a):
    if a.ext:
        ext_mod().build_card(a.ext, a.style, a.scale, a.top, a.freeze, a.force); return
    if not a.card: sys.exit('✗ 要俾 card-id，或者用 --ext 編號')
    style, s, p, c = find(a.card)
    src = os.path.join(SD, style, c['file']); dst_rel = f"cards-9x16/{c['id']}.html"; dst = os.path.join(SD, style, dst_rel)
    if os.path.exists(dst) and not a.force: sys.exit(f'✗ 已經有 9:16 版：{dst_rel}（--force 覆蓋）')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    t = open(src, encoding='utf-8').read()
    t = t.replace('width: 1920px; height: 1080px', 'width: 1080px; height: 1920px')
    t = t.replace('data-width="1920"', 'data-width="1080"').replace('data-height="1080"', 'data-height="1920"')
    t = t.replace('<!doctype html>', '<!doctype html>\n<!-- 9:16 改版（未完成）：由 ' + c['file'] + ' 複製。要人手重排版面：\n'
                  '  1. 安全區：左右 52px、頂 212、底 1556 以外唔放字；Healthy Days logo x742–1020 y228–360 唔好撞\n'
                  '  2. 字級：中文標題 ≥ 96px、內文 ≥ 64px（tokens-9x16.css 有 --size-* 直向版）\n'
                  '  3. 逐項出現時間讀 data-cues（例如 data-cues="0.9,1.6,2.3"），冇就用原本數值\n'
                  '  4. 寫死嘅 rgba(55,189,248,…) 改用 rgba(var(--accent-rgb),…)\n-->', 1)
    open(dst, 'w', encoding='utf-8').write(t)
    p[c['id']] = {'file': dst_rel, 'verified': False, 'note': '起點，未改版面'}
    save_portrait(style, p)
    print(f'✓ {dst_rel}（未完成：要改版面）')

def inline_tokens(style, brand):
    parts = [open(os.path.join(SD, style, 'tokens.css'), encoding='utf-8').read()]
    t916 = os.path.join(SD, style, 'tokens-9x16.css')
    if os.path.exists(t916): parts.append(open(t916, encoding='utf-8').read())
    if brand:
        b, _, variant = brand.partition(':')          # 例如 healthy-days:dark → tokens-kallaway-dark.css
        bt = os.path.join(ROOT, 'brands', b, f'tokens-{style}' + (f'-{variant}' if variant else '') + '.css')
        if os.path.exists(bt): parts.append(open(bt, encoding='utf-8').read())
        else: print(f'! 品牌 {brand} 冇 tokens-{style}.css，用風格原色')
    css = '\n'.join(parts)
    imports = re.findall(r'@import url\([^)]*\);', css)
    css = re.sub(r'@import url\([^)]*\);', '', css)
    return '\n'.join(imports), css

def fill_slot(t, name, value):
    ipat = re.compile(r'(<img\b[^>]*\bdata-slot="' + re.escape(name) + r'"[^>]*?)\ssrc="[^"]*"')
    if ipat.search(t):                                   # 圖片 slot：改 src（路徑用專案根目錄相對，例如 assets/img/x.jpg）
        return ipat.sub(lambda m: m.group(1) + ' src="' + html.escape(value, quote=True) + '"', t, count=1)
    pat = re.compile(r'(<(\w+)[^>]*\bdata-slot="' + re.escape(name) + r'"[^>]*>)(.*?)(</\2>)', re.S)
    if not pat.search(t): print(f'! 卡入面冇 slot「{name}」'); return t
    v = value if re.search(r'<\w', value) else html.escape(value)
    return pat.sub(lambda m: m.group(1) + v + m.group(4), t, count=1)

def cmd_use(a):
    style, s, p, c = find(a.card)
    pv = p.get(c['id'])
    if not pv: sys.exit(f'✗ {c["id"]} 未有 9:16 版。先 `cards.py adapt {c["id"]}` 再改版面，或者揀 `list --portrait` 入面嘅卡')
    if not pv.get('verified'): print(f'! {c["id"]} 9:16 版未驗證（{pv.get("note","")}）：出片前要睇預覽')
    t = open(os.path.join(SD, style, pv['file']), encoding='utf-8').read()
    cid = re.search(r'data-composition-id="([^"]+)"', t).group(1)
    imports, css = inline_tokens(style, a.brand)
    t = re.sub(r'<link rel="stylesheet" href="[^"]*tokens\.css"\s*/?>', f'<style>{imports}\n{css}</style>', t)
    t = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]*"></script>', '<script src="assets/gsap.min.js"></script>', t)
    slots = json.loads(a.slots) if a.slots else {}
    allowed = {x['name'] for x in c.get('slots', [])}
    for k, v in slots.items():
        if allowed and k not in allowed: print(f'! slot「{k}」唔喺卡嘅 slots（{", ".join(sorted(allowed))}）')
        t = fill_slot(t, k, v)
    extra = f' data-dur="{a.dur}"' + (f' data-cues="{a.cues}"' if a.cues else '')
    ext = pv.get('ext')
    if ext:                                              # 外部效果卡：顏色、字體、缺字、播放參數
        X = ext_mod(); ov = dict(kv.split('=', 1) for kv in a.colors.split(',')) if a.colors else {}
        colors, lines = X.check_colors(imports + css, ov)
        print('顏色（角色 → 品牌色）：', colors); [print(l) for l in lines]
        fdst = os.path.join(a.project, 'assets', 'fonts'); os.makedirs(fdst, exist_ok=True)
        for k in ext['fonts']: shutil.copy(os.path.join(X.TM, 'fonts', X.FKEY[k]), fdst)
        shown = ''.join(re.sub(r'<[^>]+>', '', v) for v in slots.values())
        miss = X.missing(shown, ext['fonts'])
        if miss:
            print('! 原作字體缺字：' + '；'.join(f'{X.FAM[k]}缺「{v}」' for k, v in miss.items()) + ' → 用到嗰段自動改用品牌字體 Noto Sans TC 900')
            have = X.brand_chars(os.path.join(a.project, 'assets', 'fonts', 'sans900.woff2')); need = {ch for ch in shown if not ch.isspace()}
            lack = need if have is None else need - have
            if lack: print(f'  要補品牌字體子集：python3 tools/ext_effects.py brandfont --project {a.project} --text "{"".join(sorted(need))}"' + ('（讀唔到現有子集，先 pip install brotli fonttools）' if have is None else ''))
            else: print('  ✓ 專案 assets/fonts/sans900.woff2 已有所需字')
            extra += ' data-miss="' + '|'.join(f'{k}:{v}' for k, v in miss.items()) + '"'
        if a.speed: extra += f' data-speed="{a.speed}"'
        if a.freeze is not None: extra += f' data-freeze="{a.freeze}"'
        if a.loops: extra += f' data-loops="{a.loops}"'
        if all(colors.get(r, '').startswith('#') for r in ('bg', 'fg', 'hi', 'ink')):
            extra += ' style="' + ';'.join(f'--ext-{r}:{colors[r]}' for r in ('bg', 'fg', 'hi', 'ink')) + '"'
    t = re.sub(r'(data-composition-id="' + re.escape(cid) + r'")', lambda m: m.group(1) + extra, t, count=1)
    t = re.sub(r'tl\.set\(\{\},\s*\{\},\s*[\d.]+\)', f'tl.set({{}}, {{}}, {a.dur})', t)
    t = re.sub(r'\.set\(\{\},\s*\{\},\s*[\d.]+\)', f'.set({{}}, {{}}, {a.dur})', t)
    t = t.replace(cid, a.name)
    out = os.path.join(a.project, 'compositions', a.name + '.html'); os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(t)
    g = os.path.join(a.project, 'assets', 'gsap.min.js')
    if not os.path.exists(g):
        os.makedirs(os.path.dirname(g), exist_ok=True); shutil.copy(os.path.join(ROOT, 'scripts', 'vendor', 'gsap.min.js'), g)
    rest = [x['name'] for x in c.get('slots', []) if x['name'] not in slots]
    if rest: print(f'! 未填 slot：{", ".join(rest)}（用卡入面預設內容；空白嘅會自動隱藏）')
    print(f'✓ {out}')
    # host 都要帶 data-dur / data-cues：卡用 document.querySelector('[data-composition-id=…]') 搵 ROOT，喺主檔會先搵到 host
    print(f'<div data-composition-id="{a.name}" data-composition-src="compositions/{a.name}.html"{extra} data-start="START" data-duration="{a.dur}" '
          f'data-width="1080" data-height="1920" data-track-index="TRACK"></div>')

def cmd_verify(a):
    style, s, p, c = find(a.card)
    if c['id'] not in p: sys.exit('✗ 未有 9:16 版')
    p[c['id']]['verified'] = True
    if a.note: p[c['id']]['note'] = a.note
    if getattr(a, 'source', None): p[c['id']]['source'] = a.source   # 外部效果來源，例如 text-motion-40#29
    save_portrait(style, p); print(f'✓ {c["id"]} 已驗證')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    x = sp.add_parser('list'); x.add_argument('--style'); x.add_argument('--tier'); x.add_argument('--purpose'); x.add_argument('--portrait', action='store_true')
    x = sp.add_parser('show'); x.add_argument('card')
    x = sp.add_parser('adapt'); x.add_argument('card', nargs='?'); x.add_argument('--force', action='store_true')
    x.add_argument('--ext'); x.add_argument('--style', default='kallaway'); x.add_argument('--scale', type=float, default=2.0)
    x.add_argument('--top', type=int, default=1010); x.add_argument('--freeze', type=float, default=0)
    x = sp.add_parser('use'); x.add_argument('card'); x.add_argument('--project', required=True); x.add_argument('--name', required=True)
    x.add_argument('--dur', type=float, required=True); x.add_argument('--slots'); x.add_argument('--cues'); x.add_argument('--brand')
    x.add_argument('--speed'); x.add_argument('--freeze', type=float); x.add_argument('--loops'); x.add_argument('--colors')
    x = sp.add_parser('verify'); x.add_argument('card'); x.add_argument('--note'); x.add_argument('--source')
    a = ap.parse_args()
    {'list': cmd_list, 'show': cmd_show, 'adapt': cmd_adapt, 'use': cmd_use, 'verify': cmd_verify}[a.cmd](a)
