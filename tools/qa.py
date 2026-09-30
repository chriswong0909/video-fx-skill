#!/usr/bin/env python3
"""qa.py — 出片前 QA 關卡（唔過唔准渲染）
  python3 tools/qa.py check index.html chars.json      # 字對聲 + 字幕逐字 + 數量／重疊 + 動畫起始 lint
chars.json = 校正後逐字時間 [{"c":"心","s":5.14,"e":5.3},...]（由 asr.json + 改字表出）
index.html 入面要有 <script type="application/json" id="fx-manifest">[{id,kind,text,start,end,spoken}]</script>
  python3 tools/qa.py critique critique.json            # 自評分：最新一輪全部 ≥ 7 先交（見 workflow/critique.md）
kind：hook｜keyword｜caption｜label｜imgtag｜cardtext｜cardtitle｜nametag
一致性（緩動、時長、入場、顏色、零件）另行：node scripts/qa-motion.cjs index.html brands/<brand>/motion-system.json
"""
import json, re, sys

def units(t): return len(re.findall(r'[\u4e00-\u9fff]|[A-Za-z0-9\-]+', t))
def cjk(t): return [c for c in t if re.match(r'[一-鿿A-Za-z0-9]', c)]

def check(html_path, chars_path):
    html = open(html_path).read()
    m = re.search(r'<script type="application/json" id="fx-manifest">(.*?)</script>', html, re.S)
    if not m: sys.exit('✗ 冇 fx-manifest：每個畫面字都要登記')
    M = json.loads(m.group(1)); CS = json.load(open(chars_path))
    stream = ''.join(c['c'] for c in CS)
    fails, warns = [], []
    def spoken_in(a, b): return ''.join(c['c'] for c in CS if a <= c['s'] <= b)
    for x in M:
        k, t, s, e = x['kind'], x['text'], x['start'], x['end']
        if k == 'caption':
            win = spoken_in(s - 0.35, e + 0.35); core = ''.join(cjk(t))
            if core not in win: fails.append(f"字幕唔對聲：{s:.2f}s「{t}」；嗰段講嘅係「{spoken_in(s-0.1, e+0.1)}」")
            if units(t) > 10: fails.append(f"字幕太長（{len(core)} 字）：「{t}」")
        elif x.get('spoken', True):
            win = spoken_in(s - 0.8, s + 3.0)
            miss = [c for c in cjk(t) if c not in win and not c.isdigit()]
            if miss: fails.append(f"{k}「{t}」@{s:.2f}s 有字醫生冇講（{''.join(miss)}）；嗰刻講緊「{spoken_in(s-0.8, s+2)}」")
            first = next((c for c in CS if c['c'] in cjk(t)), None)
            # 出現時間唔可以早過講嗰個字超過 0.5 秒
            idx = [c['s'] for c in CS if c['c'] == (cjk(t) or [''])[0] and s - 0.8 <= c['s'] <= s + 3.0]
            if idx and s < min(idx) - 0.5: fails.append(f"{k}「{t}」早過講出嚟 {min(idx)-s:.2f}s")
        if k in ('keyword', 'hook', 'label', 'imgtag', 'cardtext') and units(t) > 8:
            fails.append(f"{k}「{t}」超過 8 字")
    kws = sorted([x for x in M if x['kind'] == 'keyword'], key=lambda x: x['start'])
    if len(kws) > 4: fails.append(f"頂部關鍵詞 {len(kws)} 個（上限 4）")
    for a, b in zip(kws, kws[1:]):
        if b['start'] - a['start'] < 8: warns.append(f"關鍵詞太密：「{a['text']}」{a['start']}s →「{b['text']}」{b['start']}s")
    big = [x for x in M if x['kind'] in ('hook', 'keyword')]
    for i, a in enumerate(big):
        for b in big[i + 1:]:
            if a['start'] < b['end'] and b['start'] < a['end']: fails.append(f"兩個大字同時出：「{a['text']}」同「{b['text']}」")
    n = len(re.findall(r'immediateRender\s*:\s*false', html))
    if n: fails.append(f"有 {n} 個 immediateRender:false —— 入場動畫開始前會見到元素（出咗又退再入）")
    print(f"QA：{len(M)} 個畫面字")
    for w in warns: print(' !', w)
    for f in fails: print(' ✗', f)
    print('✓ 通過' if not fails else f'✗ {len(fails)} 項唔過，改完先渲染')
    return 1 if fails else 0

DIMS = ['風格統一', '多變', '對位', '可讀性', '品牌', '節奏', '聲畫']

def critique(path, need=7):
    R = json.load(open(path)); last = R[-1]; sc = last['scores']
    miss = [d for d in DIMS if d not in sc]
    low = {d: v for d, v in sc.items() if v < need}
    print(f"自評分第 {last['round']} 輪：" + '  '.join(f"{d} {sc.get(d, '-')}" for d in DIMS))
    for d in miss: print(f' ✗ 未評：{d}')
    for d, v in low.items(): print(f' ✗ {d} {v} < {need}' + ('（≤5，要話俾用戶知）' if v <= 5 else ''))
    if low and not last.get('fixes'): print(' ✗ 有低分但冇寫 fixes')
    if low and last['round'] >= 3: print(' ! 已經 3 輪，將分數同原因交俾用戶決定')
    ok = not miss and not low
    print('✓ 自評分過關' if ok else '✗ 未過關，改完再評')
    return 0 if ok else 1

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'critique': sys.exit(critique(sys.argv[2]))
    if len(sys.argv) < 4 or sys.argv[1] != 'check': sys.exit(__doc__)
    sys.exit(check(sys.argv[2], sys.argv[3]))
