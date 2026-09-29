#!/usr/bin/env python3
"""video-fx 調色工具（只需 numpy + ffmpeg 4.4+）

  python3 tools/grade.py list                                   列出調色預設（grades/）
  python3 tools/grade.py recommend <影片類型> [情緒]             按影片類型／情緒推薦預設
  python3 tools/grade.py analyze <video>                        分析曝光、對比、偏色、膚色（輸出 JSON）
  python3 tools/grade.py compare <video> <out.jpg> [GR-001 GR-002 ...] [--t 秒]
                                                                左右對比圖（原片｜調色後），分鏡同確認用
  python3 tools/grade.py apply <video> <GR-id> <out.mp4> [--strength 0.8] [--no-fix]
                                                                輸出調色片：自動校正（白平衡、黑白位）+ 預設風格；音軌原封不動 copy
  python3 tools/grade.py previews                               重做 grades/_before.jpg 同 grades/*/after.jpg（效果目錄用；樣本 grades/_sample.mp4 唔入 git）

預設檔：grades/GR-###-slug/grade.md（front matter 有 filters）。
"""
import os, re, sys, json, subprocess, argparse, tempfile
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GR = os.path.join(ROOT, 'grades')
SAMPLE = os.path.join(GR, '_sample.mp4')   # 效果目錄預覽用樣本（使用者自己嘅片段）

def run(*a, capture=False):
    r = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', *a], capture_output=capture, check=True)
    return r.stdout

def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration',
                          '-of', 'json', path], capture_output=True, check=True).stdout
    j = json.loads(out); s = j['streams'][0]
    return s['width'], s['height'], float(j['format']['duration'])

def fm(path):
    t = open(path, encoding='utf-8').read(); m = re.match(r'^---\n([\s\S]*?)\n---', t); o = {}
    for line in (m.group(1) if m else '').split('\n'):
        k = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if not k: continue
        v = k.group(2).strip()
        if v.startswith('[') and v.endswith(']'): v = [x.strip() for x in v[1:-1].split(',') if x.strip()]
        elif len(v) > 1 and v[0] == '"' and v[-1] == '"': v = v[1:-1].replace('\\"', '"')
        o[k.group(1)] = v
    return o

def grades():
    out = {}
    if not os.path.isdir(GR): return out
    for d in sorted(os.listdir(GR)):
        f = os.path.join(GR, d, 'grade.md')
        if re.match(r'GR-\d{3}-', d) and os.path.exists(f):
            g = fm(f); g['dir'] = os.path.join(GR, d); out[g['id']] = g
    return out

# ---------- 分析 ----------
def frames(path, n=6, w=270):
    W, H, dur = probe(path); h = int(round(H * w / W / 2) * 2); arr = []
    for i in range(n):
        t = dur * (i + 0.5) / n
        raw = run('-ss', f'{t:.2f}', '-i', path, '-frames:v', '1', '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-', capture=True)
        if len(raw) == w * h * 3: arr.append(np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(np.float32) / 255)
    return np.stack(arr)

def analyze(path):
    f = frames(path); r, g, b = f[..., 0], f[..., 1], f[..., 2]
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mx0 = f.max(-1); mn0 = f.min(-1); sat0 = np.where(mx0 > 0, (mx0 - mn0) / np.maximum(mx0, 1e-6), 0)
    neu = (sat0 < 0.12) & (y > 0.35) & (y < 0.92)          # 接近中性嘅像素（白牆、恤衫、灰色）先用嚟判斷偏色
    if neu.mean() < 0.02: neu = (y > 0.25) & (y < 0.85)
    cast = {'r': float(r[neu].mean() - y[neu].mean()), 'g': float(g[neu].mean() - y[neu].mean()), 'b': float(b[neu].mean() - y[neu].mean())}
    gains = {k: float(y[neu].mean() / max(v[neu].mean(), 1e-4)) for k, v in (('r', r), ('g', g), ('b', b))}
    # 膚色：YCbCr 常用範圍
    cb = 0.5 - 0.1146 * r - 0.3854 * g + 0.5 * b; cr = 0.5 + 0.5 * r - 0.4542 * g - 0.0458 * b
    skin = (cb > 77/255) & (cb < 127/255) & (cr > 137/255) & (cr < 173/255) & (y > 0.2) & (y < 0.9)
    hue = None
    if skin.mean() > 0.01:
        R, G, B = r[skin].mean(), g[skin].mean(), b[skin].mean()
        mx, mn = max(R, G, B), min(R, G, B); d = mx - mn or 1e-6
        hue = (60 * ((G - B) / d) % 360) if mx == R else (60 * ((B - R) / d + 2) if mx == G else 60 * ((R - G) / d + 4))
    mx = f.max(-1); mn = f.min(-1); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    res = {'exposure': round(float(y.mean()), 3), 'black_p1': round(float(np.percentile(y, 1)), 3), 'white_p99': round(float(np.percentile(y, 99)), 3),
           'contrast': round(float(np.percentile(y, 99) - np.percentile(y, 1)), 3), 'saturation': round(float(sat.mean()), 3),
           'cast_neutral': {k: round(v, 4) for k, v in cast.items()}, 'wb_gains': {k: round(v, 4) for k, v in gains.items()}, 'neutral_ratio': round(float(neu.mean()), 3), 'skin_ratio': round(float(skin.mean()), 3),
           'skin_hue': None if hue is None else round(float(hue), 1)}
    notes = []
    if res['exposure'] < 0.35: notes.append('偏暗')
    if res['exposure'] > 0.62: notes.append('偏光')
    if res['contrast'] < 0.75: notes.append('對比低（灰濛）')
    if cast['r'] - cast['b'] > 0.03: notes.append('白色位偏暖／偏黃')
    if cast['b'] - cast['r'] > 0.03: notes.append('白色位偏冷／偏藍')
    if abs(cast['g']) > 0.015: notes.append('偏綠' if cast['g'] > 0 else '偏洋紅')
    if hue is not None and not (8 <= hue <= 38): notes.append(f'膚色色相 {hue:.0f}° 唔自然（正常約 15–30°）')
    res['notes'] = notes or ['大致正常']
    return res

def fix_chain(a, strength=1.0):
    """溫和自動校正：用中性像素做白平衡（只校正一半）+ 黑白位（只喺明顯灰濛時先拉）。"""
    k = 0.5 * strength; cl = lambda v: max(0.9, min(1.1, v))
    gn = {c: cl(1 + (a['wb_gains'][c] - 1) * k) for c in 'rgb'}
    parts = [f"colorchannelmixer=rr={gn['r']:.4f}:gg={gn['g']:.4f}:bb={gn['b']:.4f}"]
    lo, hi = a['black_p1'], a['white_p99']
    imin = (lo - 0.03) * 0.5 * strength if lo > 0.08 else 0.0
    imax = hi + (0.97 - hi) * 0.5 * strength if hi < 0.9 else 1.0
    if imin > 0.005 or imax < 0.995:
        parts.append(f"colorlevels=rimin={imin:.3f}:gimin={imin:.3f}:bimin={imin:.3f}:rimax={imax:.3f}:gimax={imax:.3f}:bimax={imax:.3f}")
    return ','.join(parts)

def chain(path, gid, strength=1.0, fix=True):
    g = grades()[gid]; look = g['filters']
    pre = fix_chain(analyze(path)) if fix else 'null'
    if strength >= 0.999: return f"{pre},{look}"
    return f"{pre},split[a][b];[b]{look}[g];[a][g]blend=all_mode=normal:all_opacity={strength:.2f}"

# ---------- 指令 ----------
def cmd_list(a):
    for gid, g in grades().items(): print(gid, g['name'], '｜預設用於：', '、'.join(g.get('default_for') or []) or '—', '｜', g.get('summary', ''))

REC = None
def recommend(vtype, mood=None):
    gs = grades(); pick = None
    if mood:
        for gid, g in gs.items():
            if mood in (g.get('mood_zh') or []): pick = gid; break
    if not pick:
        for gid, g in gs.items():
            if vtype in (g.get('default_for') or []): pick = gid; break
    alts = [gid for gid, g in gs.items() if vtype in (g.get('video_types') or []) and gid != pick][:2]
    return pick or 'GR-001', alts

def cmd_recommend(a):
    p, alts = recommend(a.vtype, a.mood); gs = grades()
    print(json.dumps({'recommend': p, 'name': gs[p]['name'], 'alternatives': [{'id': x, 'name': gs[x]['name']} for x in alts]}, ensure_ascii=False))

def cmd_analyze(a): print(json.dumps(analyze(a.video), ensure_ascii=False, indent=1))

def still(video, t, vf, out, w=540):
    run('-ss', f'{t:.2f}', '-i', video, '-frames:v', '1', '-vf', f'{vf},scale={w}:-2' if vf else f'scale={w}:-2', '-q:v', '3', out)

def cmd_compare(a):
    W, H, dur = probe(a.video); t = a.t if a.t is not None else dur * 0.4
    ids = a.ids or list(grades())[:4]
    with tempfile.TemporaryDirectory() as td:
        ins = [os.path.join(td, '0.jpg')]; still(a.video, t, None, ins[0])
        for i, gid in enumerate(ids, 1):
            p = os.path.join(td, f'{i}.jpg'); still(a.video, t, chain(a.video, gid, a.strength), p); ins.append(p)
        labels = ['原片'] + [f"{gid} {grades()[gid]['name']}" for gid in ids]
        args = []; fc = []
        for i, p in enumerate(ins):
            args += ['-i', p]
            fc.append(f"[{i}:v]drawbox=y=ih-56:h=56:w=iw:color=black@0.6:t=fill,drawtext=text='{labels[i]}':fontfile={font()}:fontsize=28:fontcolor=white:x=16:y=h-44[v{i}]")
        fc.append(''.join(f'[v{i}]' for i in range(len(ins))) + f'hstack=inputs={len(ins)}')
        run(*args, '-filter_complex', ';'.join(fc), '-q:v', '3', a.out)
    print('✓', a.out)

def font():
    for f in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', '/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc', '/System/Library/Fonts/PingFang.ttc',
              '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf']:
        if os.path.exists(f): return f
    return ''

def cmd_apply(a):
    vf = chain(a.video, a.gid, a.strength, not a.no_fix)
    run('-i', a.video, '-filter_complex', f'[0:v]{vf}[v]', '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
        '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', a.out)
    print('✓', a.out, '｜', a.gid, f'strength={a.strength}', '｜ 音軌 copy 不變')
    print('filter:', vf)

def cmd_previews(a):
    if not os.path.exists(SAMPLE): sys.exit(f'搵唔到樣本 {SAMPLE}')
    W, H, dur = probe(SAMPLE); t = dur * 0.4
    still(SAMPLE, t, None, os.path.join(GR, '_before.jpg'), 360)
    for gid, g in grades().items():
        still(SAMPLE, t, chain(SAMPLE, gid), os.path.join(g['dir'], 'after.jpg'), 360)
        print('✓', gid)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('list').set_defaults(f=cmd_list)
    r = sp.add_parser('recommend'); r.add_argument('vtype'); r.add_argument('mood', nargs='?'); r.set_defaults(f=cmd_recommend)
    z = sp.add_parser('analyze'); z.add_argument('video'); z.set_defaults(f=cmd_analyze)
    c = sp.add_parser('compare'); c.add_argument('video'); c.add_argument('out'); c.add_argument('ids', nargs='*'); c.add_argument('--t', type=float); c.add_argument('--strength', type=float, default=1.0); c.set_defaults(f=cmd_compare)
    p = sp.add_parser('apply'); p.add_argument('video'); p.add_argument('gid'); p.add_argument('out'); p.add_argument('--strength', type=float, default=1.0); p.add_argument('--no-fix', action='store_true'); p.set_defaults(f=cmd_apply)
    sp.add_parser('previews').set_defaults(f=cmd_previews)
    a = ap.parse_args(); a.f(a)
