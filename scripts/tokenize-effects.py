#!/usr/bin/env python3
"""tokenize-effects.py — 將效果 snippet 寫死嘅顏色同時長換成 tokens（動態系統卡／風格預設可以接管）
  python3 scripts/tokenize-effects.py report            # 只報告，唔改檔
  python3 scripts/tokenize-effects.py apply [FX-003 …]  # 改檔（預設全部，style_bound 嘅跳過）

顏色 → 角色 token（冇 tokens 時用原本色做後備，所以預設樣貌唔變）：
  紅／橙紅 → --c-alert｜綠 → --c-positive｜藍／青／紫 → --c-accent｜黃／橙／啡／洋紅 → --c-accent2
  淺中性色 → --c-surface｜深中性色 → --c-text｜中灰 → text 同白色混合｜#fff／#000 保留
  同一角色入面較淺／較深嘅色 → color-mix(角色色, 白／黑)，保留原本嘅深淺層次
  SVG 屬性（fill/stroke/stop-color）轉做 style，因為屬性入面 var() 唔生效
時長 → DUR：≤0.27 → DUR.out｜≤0.47 → DUR.in｜≤0.8 → DUR.move；> 0.8（慢推、氣氛動作）保留
"""
import colorsys, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HEX = re.compile(r'#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])')

def norm(h):
    h = h.lower()
    return '#' + ''.join(c * 2 for c in h[1:]) if len(h) == 4 else h

def hls(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hls(r, g, b)

def role(h):
    H, L, S = hls(h); H *= 360
    if h in ('#ffffff', '#000000'): return None
    if S < 0.14 or L > 0.85 or L < 0.12 or (L < 0.25 and S < 0.45):
        return 'surface' if L > 0.85 else 'text' if L < 0.3 else 'grey'
    if (H < 22 or H >= 335) and S >= 0.45: return 'alert'
    if H < 22 or H >= 335: return 'accent2'   # 低飽和暖色（啡、磚）當第二強調色
    if 75 <= H < 170: return 'positive'
    if 170 <= H < 300: return 'accent'
    return 'accent2'

def base_of(hexes):
    """角色入面揀「最似主色」嗰隻：飽和度高、亮度近 0.5"""
    return max(hexes, key=lambda h: hls(h)[2] - 1.5 * abs(hls(h)[1] - 0.5))

def expr(h, rmap):
    r = role(h)
    if r is None: return h
    if r == 'grey':
        L = hls(h)[1]; tb = rmap.get('text') or '#111111'; Lb = hls(tb)[1]
        p = round(max(5, min(95, (1 - L) / max(1e-3, 1 - Lb) * 100)))
        return f'color-mix(in srgb, var(--c-text, {tb}) {p}%, white)'
    b = rmap[r]; var = f'var(--c-{r}, {b})'
    if h == b or r in ('surface', 'text'): return f'var(--c-{r}, {h})'
    L, Lb = hls(h)[1], hls(b)[1]
    if abs(L - Lb) < 0.06: return var
    if L > Lb: p = round(max(5, min(95, (1 - L) / max(1e-3, 1 - Lb) * 100))); return f'color-mix(in srgb, {var} {p}%, white)'
    p = round(max(5, min(95, L / max(1e-3, Lb) * 100))); return f'color-mix(in srgb, {var} {p}%, black)'

def zones(s):
    """回傳每個位置屬 script／style／markup"""
    z = []
    for m in re.finditer(r'<(script|style)\b[^>]*>(.*?)</\1>', s, re.S): z.append((m.start(2), m.end(2), m.group(1)))
    return z

def in_zone(i, z):
    for a, b, k in z:
        if a <= i < b: return k
    return 'markup'

def svg_attrs_to_style(s, rmap, log):
    def fix_tag(m):
        tag = m.group(0); moved = []
        def take(mm):
            moved.append(f"{mm.group(1)}:{expr(norm(mm.group(2)), rmap)}"); return ''
        tag2 = re.sub(r'\s(fill|stroke|stop-color)\s*=\s*"(#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3}))"', take, tag)
        if not moved: return tag
        log.append(f'SVG 屬性→style ×{len(moved)}')
        if re.search(r'\sstyle\s*=\s*"', tag2):
            return re.sub(r'(\sstyle\s*=\s*")', lambda q: q.group(1) + ';'.join(moved) + ';', tag2, count=1)
        return re.sub(r'(/?>)$', ' style="' + ';'.join(moved) + '"' + r'\1', tag2, count=1)
    return re.sub(r'<(?:path|rect|circle|ellipse|line|polyline|polygon|stop|g|text|use)\b[^>]*>', fix_tag, s)

def dur_token(m):
    d = float(m.group(2))
    if d < 0.15 or d > 0.8: return m.group(0)
    return m.group(1) + ('DUR.out' if d <= 0.27 else 'DUR.in' if d <= 0.47 else 'DUR.move')

def process(path, write):
    s0 = open(path, encoding='utf-8').read(); log = []
    cols = sorted({norm(h) for h in HEX.findall(s0) if not re.search(r'url\(' + re.escape(h), s0)})
    # 唔當色碼：id 選擇器（例如 '#c66' 係元素 id）
    ids = set(re.findall(r'id="([0-9a-fA-F]{3}|[0-9a-fA-F]{6})"', s0))
    raw = {m.lower() for m in re.findall(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b', s0)}
    ids = {i.lower() for i in ids}
    cols = [c for c in cols if c[1:] not in ids and not any(r in ids and norm('#' + r) == c for r in raw)]
    by = {}
    for c in cols:
        r = role(c)
        if r and r != 'grey': by.setdefault(r, []).append(c)
    rmap = {r: base_of(v) for r, v in by.items()}
    s = svg_attrs_to_style(s0, rmap, log)
    z = zones(s); out = []; last = 0; n = 0; skipped = 0
    for m in HEX.finditer(s):
        h = norm(m.group(0)); k = in_zone(m.start(), z)
        if m.group(0)[1:].lower() in ids or role(h) is None: continue
        pre = s[max(0, m.start() - 40):m.start()]
        if 'var(--' in pre[-24:] and pre.rstrip().endswith(','): continue          # 已經係 var(--x, #後備)
        if k == 'script':
            if not re.search(r"['\"]$", pre) or '${' in s[m.start() - 30:m.start()]: skipped += 1; continue
        out.append(s[last:m.start()]); out.append(expr(h, rmap)); last = m.end(); n += 1
    out.append(s[last:]); s = ''.join(out)
    # 時長（只喺 script）
    z = zones(s); parts = []; last = 0; nd = 0
    for a, b, k in z:
        if k != 'script': continue
        seg = s[a:b]; seg2, c = re.subn(r'(duration\s*:\s*)(\d*\.?\d+)(?![\w.])', dur_token, seg)
        nd += sum(1 for x, y in zip(re.findall(r'duration\s*:\s*([\w.]+)', seg), re.findall(r'duration\s*:\s*([\w.]+)', seg2)) if x != y)
        parts.append(s[last:a]); parts.append(seg2); last = b
    parts.append(s[last:]); s = ''.join(parts)
    if write and s != s0: open(path, 'w', encoding='utf-8').write(s)
    return dict(colors=len(cols), roles={r: rmap[r] for r in rmap}, replaced=n, script_skipped=skipped, durations=nd, notes=log[:1])

def bound_ids():
    ids = set()
    for p in glob.glob(os.path.join(ROOT, 'effects/FX-*/effect.md')):
        if re.search(r'^style_bound:\s*true', open(p, encoding='utf-8').read(), re.M): ids.add(os.path.basename(os.path.dirname(p))[:6])
    return ids

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('report', 'apply'): sys.exit(__doc__)
    write = sys.argv[1] == 'apply'; only = set(sys.argv[2:]); skip = bound_ids()
    tot = dict(colors=0, replaced=0, durations=0, files=0)
    for p in sorted(glob.glob(os.path.join(ROOT, 'effects/FX-*/snippet.html'))):
        fid = os.path.basename(os.path.dirname(p))[:6]
        if only and fid not in only: continue
        if fid in skip: print(f'{fid} 風格綁死（style_bound），跳過'); continue
        r = process(p, write)
        if r['replaced'] or r['durations']:
            tot['files'] += 1
            print(f"{fid} 色 {r['colors']} → 換 {r['replaced']}（{' '.join(f'{k}:{v}' for k, v in r['roles'].items())}）時長換 {r['durations']}" + (f"｜script 入面 {r['script_skipped']} 個色冇郁" if r['script_skipped'] else ''))
        for k in ('colors', 'replaced', 'durations'): tot[k] += r[k]
    print(f"{'已改' if write else '報告'}：{tot['files']} 個效果，色碼換 {tot['replaced']} 處，時長換 {tot['durations']} 處")
