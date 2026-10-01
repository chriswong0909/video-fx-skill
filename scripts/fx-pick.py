#!/usr/bin/env python3
"""fx-pick.py — 由 fx-shot auto 截圖揀「效果最完整」嗰格（畫面細節最多）→ times.json
  python3 scripts/fx-pick.py <auto_dir> <blank.png> <times.json>"""
import glob, json, os, sys
from PIL import Image, ImageChops, ImageStat
d, blank, out = sys.argv[1:4]
B = Image.open(blank).convert('RGB').resize((135, 240)); best = {}
for f in glob.glob(os.path.join(d, 'FX-*@*.png')):
    fid, t = os.path.basename(f)[:-4].split('@')
    im = Image.open(f).convert('RGB').resize((135, 240))
    # 同底圖差異（有冇疊嘢）+ 細節（stddev）：避免揀咗淨係全屏底色嗰格
    score = sum(ImageStat.Stat(ImageChops.difference(im, B)).mean) + 2 * sum(ImageStat.Stat(im).stddev) / 3
    if fid not in best or score > best[fid][1]: best[fid] = (float(t), score)
json.dump({k: v[0] for k, v in sorted(best.items())}, open(out, 'w'), indent=0)
print(f'✓ {len(best)} 個效果揀好時間 → {out}')
