#!/usr/bin/env python3
"""beatgrid.py — 節拍表 + 關鍵格靜圖頁（批核關卡：未批唔准 render）
  python3 tools/beatgrid.py <manifest.json> <chars.json> <keyframes_dir> <out.html> [sfx-events.json] [--title 名]
manifest 每項建議有：comp（零件）、state（hero 狀態 T/K…）、enter（入場方式）、beat（hook/setup/…）
輸出一頁：每行 = 一個畫面字出現嗰拍｜講緊咩｜零件／狀態｜入場｜聲效｜關鍵格
"""
import base64, glob, html, io, json, os, sys
from PIL import Image

def thumb(p, w=216):
    im = Image.open(p).convert('RGB'); im.thumbnail((w, w * 2))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=72); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def main(a):
    title = 'Beat grid'
    if '--title' in a: i = a.index('--title'); title = a[i + 1]; a = a[:i] + a[i + 2:]
    M = json.load(open(a[0])); CS = json.load(open(a[1])); kdir = a[2]; out = a[3]
    EV = json.load(open(a[4])) if len(a) > 4 and os.path.exists(a[4]) else []
    kf = sorted((int(os.path.basename(p)[3:8]) / 100, p) for p in glob.glob(os.path.join(kdir, 'kf_*.jpg')))
    items = sorted([x for x in M if x['kind'] != 'caption'], key=lambda x: x['start'])
    used, rows = set(), []
    for x in items:
        s = x['start']; spoken = ''.join(c['c'] for c in CS if s - 0.2 <= c['s'] <= s + 1.6)
        sfx = [e for e in EV if abs(e['t'] - s) <= 0.6]
        k = next(((t, p) for t, p in kf if s - 0.05 <= t <= s + 1.5 and p not in used), None)
        if k: used.add(k[1])
        comp = x.get('comp', '?') + (f"·{x['state']}" if x.get('state') else '')
        rows.append(f"""<tr><td class="t">{s:.1f}–{x['end']:.1f}s</td><td>{html.escape(x.get('beat',''))}</td><td class="sp">{html.escape(spoken)}</td>
<td><b>{html.escape(x['text'])}</b></td><td><span class="chip">{html.escape(comp)}</span></td><td>{html.escape(x.get('enter',''))}</td>
<td class="sfx">{'<br>'.join(html.escape(e['sfx'] + ' ' + e.get('why', '')) for e in sfx)}</td>
<td>{f'<img src="{thumb(k[1])}" alt="{k[0]:.1f}s">' if k else ''}</td></tr>""")
    doc = f"""<title>{html.escape(title)}</title>
<style>
:root{{--bg:#f5f7fa;--fg:#15202b;--mut:#56687a;--line:#dde3ea;--card:#ffffff;--acc:#2f68a8;--on-acc:#ffffff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#11161c;--fg:#e8edf2;--mut:#9aa8b5;--line:#2a333d;--card:#18202a;--acc:#6fa0dd;--on-acc:#0d1620;color-scheme:dark}}}}
:root[data-theme=dark]{{--bg:#11161c;--fg:#e8edf2;--mut:#9aa8b5;--line:#2a333d;--card:#18202a;--acc:#6fa0dd;--on-acc:#0d1620;color-scheme:dark}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,"PingFang HK","Noto Sans TC",sans-serif}}
main{{max-width:1180px;margin:0 auto;padding-block:24px;padding-inline:16px}} h1{{font-size:22px;margin:0 0 4px}} p{{color:var(--mut);margin:0 0 16px}}
.wrap{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}}
table{{border-collapse:collapse;width:100%;min-width:860px}} th,td{{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}}
th{{font-size:13px;color:var(--mut);font-weight:600;position:sticky;top:0;background:var(--card)}}
.t{{white-space:nowrap;font-variant-numeric:tabular-nums}} .sp{{color:var(--mut);max-width:180px}} .sfx{{font-size:13px;color:var(--mut)}}
.chip{{display:inline-block;padding:2px 10px;border-radius:999px;background:var(--acc);color:var(--on-acc);font-size:13px;white-space:nowrap}}
img{{width:150px;border-radius:8px;display:block}}
</style>
<main><h1>{html.escape(title)}</h1><p>節拍表 + 關鍵格（未 render）。批咗先砌成條片；要改就講邊一行。</p>
<div class="wrap"><table><thead><tr><th>時間</th><th>beat</th><th>講緊</th><th>畫面字</th><th>零件·狀態</th><th>入場</th><th>聲效</th><th>關鍵格</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></main>"""
    open(out, 'w').write(doc); print(f'✓ {len(rows)} 行、{len(used)} 張關鍵格 → {out}')

if __name__ == '__main__':
    if len(sys.argv) < 5: sys.exit(__doc__)
    main(sys.argv[1:])
