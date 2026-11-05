#!/usr/bin/env python3
"""video-fx 對色／抓鏡頭／防手震（2026-11-05 加，參考 Threads 11 個開源剪片工具嗰篇）

  python3 tools/match.py color <src.mp4> <ref.mp4|ref.jpg> <out.mp4> [--t 秒] [--rt 秒] [--strength 0.7]
      將 src 嘅顏色夾到 ref（例：近鏡夾闊鏡、第 2 段 Teleprompter 夾第 1 段）。
      color-matcher（MKL）由一格計出轉換 → 燒成 33 點 .cube LUT → ffmpeg lut3d 套全片；音軌 copy。
      做喺 grade.py apply 之前：先對色，再用同一個 GR 預設調全部素材。
  python3 tools/match.py scenes <video> [out.json] [--threshold 3.0]
      PySceneDetect（AdaptiveDetector）抓每個鏡頭：輸出鏡頭清單、平均／中位長度、每 10 秒剪幾多下。
      用喺參考片分析（workflow/reference-to-style.md），補 ref_style.py。
  python3 tools/match.py stab <in.mp4> <out.mp4> [--shakiness 5] [--smoothing 15]
      FFmpeg 內置 vid.stab 兩 pass 防手震（腳架片唔使跑）；音軌 copy。

依賴：pip install color-matcher scenedetect opencv-python-headless（缺就自動裝）；ffmpeg 要有 vidstab（brew 版已有）。
"""
import os, sys, json, subprocess, argparse, tempfile, statistics

def need(mod, pkg):
    try: __import__(mod)
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--break-system-packages', pkg], check=True)

def ff(*a):
    subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)

def frame(path, t, out):
    if path.lower().endswith(('.jpg', '.jpeg', '.png')): return path
    ff('-ss', str(t), '-i', path, '-frames:v', '1', out); return out

def color(a):
    need('color_matcher', 'color-matcher'); need('numpy', 'numpy')
    import numpy as np
    from color_matcher import ColorMatcher
    from color_matcher.io_handler import load_img_file
    d = tempfile.mkdtemp()
    s = load_img_file(frame(a.src, a.t, os.path.join(d, 's.png'))).astype(np.float64)
    r = load_img_file(frame(a.ref, a.rt, os.path.join(d, 'r.png'))).astype(np.float64)
    if s.max() > 1.5: s = s / 255
    if r.max() > 1.5: r = r / 255
    cm = ColorMatcher()
    n = 33
    g = np.linspace(0, 1, n)
    b_, g_, r_ = np.meshgrid(g, g, g, indexing='ij')           # .cube：R 變得最快
    ident = np.stack([r_, g_, b_], -1).reshape(-1, 1, 3)
    # MKL 係線性轉換：用 src 格計參數，套落 identity LUT
    out_s = cm.transfer(src=s, ref=r, method='mkl')
    # 用最小二乘由 (s → out_s) 擬合 3x4 仿射矩陣，再套 LUT（避免依賴內部 API）
    X = np.c_[s.reshape(-1, 3), np.ones(s.shape[0] * s.shape[1])]
    M, *_ = np.linalg.lstsq(X, out_s.reshape(-1, 3), rcond=None)
    lut = np.c_[ident.reshape(-1, 3), np.ones(n ** 3)] @ M
    lut = ident.reshape(-1, 3) + a.strength * (lut - ident.reshape(-1, 3))
    lut = np.clip(lut, 0, 1)
    cube = os.path.join(d, 'match.cube')
    with open(cube, 'w') as f:
        f.write(f'LUT_3D_SIZE {n}\n')
        for v in lut: f.write(f'{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
    ff('-i', a.src, '-vf', f'lut3d={cube}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy', a.out)
    keep = os.path.splitext(a.out)[0] + '.cube'
    subprocess.run(['cp', cube, keep])
    print(json.dumps({'out': a.out, 'lut': keep, 'strength': a.strength}, ensure_ascii=False))

def scenes(a):
    need('scenedetect', 'scenedetect'); need('cv2', 'opencv-python-headless')
    from scenedetect import detect, AdaptiveDetector, ContentDetector
    sc = detect(a.video, AdaptiveDetector(adaptive_threshold=a.threshold)) or detect(a.video, ContentDetector())
    if not sc:   # 冇剪位＝成條一個鏡頭
        from scenedetect import open_video
        v = open_video(a.video); sc = [(v.base_timecode, v.base_timecode + v.duration)]
    sec = lambda x: float(getattr(x, 'seconds', None) if not callable(getattr(x, 'seconds', None)) and getattr(x, 'seconds', None) is not None else x.get_seconds())
    shots = [{'start': round(sec(s), 2), 'end': round(sec(e), 2), 'dur': round(sec(e) - sec(s), 2)} for s, e in sc]
    ds = [x['dur'] for x in shots] or [0]
    total = shots[-1]['end'] if shots else 0
    res = {'shots': len(shots), 'mean': round(statistics.mean(ds), 2), 'median': round(statistics.median(ds), 2),
           'min': min(ds), 'max': max(ds), 'cuts_per_10s': round((len(shots) - 1) / total * 10, 2) if total else 0, 'list': shots}
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out: open(a.out, 'w').write(txt)
    print(txt if not a.out else json.dumps({k: v for k, v in res.items() if k != 'list'}, ensure_ascii=False))

def stab(a):
    trf = tempfile.mktemp(suffix='.trf')
    ff('-i', a.inp, '-vf', f'vidstabdetect=shakiness={a.shakiness}:accuracy=15:result={trf}', '-f', 'null', '-')
    ff('-i', a.inp, '-vf', f'vidstabtransform=input={trf}:smoothing={a.smoothing}:zoom=0:optzoom=1,unsharp=5:5:0.6:3:3:0.3',
       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy', a.out)
    print(json.dumps({'out': a.out}))

p = argparse.ArgumentParser(); sp = p.add_subparsers(dest='cmd', required=True)
c = sp.add_parser('color'); c.add_argument('src'); c.add_argument('ref'); c.add_argument('out')
c.add_argument('--t', type=float, default=1.0); c.add_argument('--rt', type=float, default=1.0); c.add_argument('--strength', type=float, default=0.7)
s = sp.add_parser('scenes'); s.add_argument('video'); s.add_argument('out', nargs='?'); s.add_argument('--threshold', type=float, default=3.0)
t = sp.add_parser('stab'); t.add_argument('inp'); t.add_argument('out'); t.add_argument('--shakiness', type=int, default=5); t.add_argument('--smoothing', type=int, default=15)
a = p.parse_args(); {'color': color, 'scenes': scenes, 'stab': stab}[a.cmd](a)
