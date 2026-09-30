#!/usr/bin/env python3
"""ref_style.py — 由參考片自動量度，出 style-guide.md 骨架（文法欄留空俾人睇 sheet 填）
  python3 tools/ref_style.py <analyze-ref 輸出 dir> <ref.mp4> <refs/slug>
量度：鏡頭長度、剪接密度、主色板（6 色 + 佔比）、亮度／飽和度、顆粒程度。
"""
import colorsys, json, os, statistics, subprocess, sys
from PIL import Image, ImageChops, ImageFilter, ImageStat

def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout.strip())

def frames(p, tmp, fps=1):
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-vf', f'fps={fps},scale=160:-2', f'{tmp}/r_%04d.png'], check=True)
    return sorted(os.path.join(tmp, f) for f in os.listdir(tmp) if f.startswith('r_'))

def main(work, ref, out):
    os.makedirs(out, exist_ok=True)
    D = dur(ref)
    cuts = [float(x) for x in open(os.path.join(work, 'cuts.txt')).read().split() if x.strip()] if os.path.exists(os.path.join(work, 'cuts.txt')) else []
    edges = [0.0] + sorted(c for c in cuts if 0.05 < c < D - 0.05) + [D]
    shots = [round(b - a, 2) for a, b in zip(edges, edges[1:]) if b - a > 0.08]
    fs = frames(ref, os.path.join(work, 'rs'))
    big = Image.new('RGB', (160, 90 * len(fs) or 90))
    lum, sat, grain = [], [], []
    for i, f in enumerate(fs):
        im = Image.open(f).convert('RGB').resize((160, 90))
        big.paste(im, (0, 90 * i))
        g = im.convert('L'); lum.append(ImageStat.Stat(g).mean[0] / 255)
        hsv = im.convert('HSV'); sat.append(ImageStat.Stat(hsv).mean[1] / 255)
        grain.append(ImageStat.Stat(ImageChops.difference(g, g.filter(ImageFilter.GaussianBlur(1.2)))).mean[0])
    q = big.quantize(colors=6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:18]; counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    colors = []
    for c, idx in counts:
        r, g, b = pal[idx * 3: idx * 3 + 3]
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        colors.append(dict(hex='#%02x%02x%02x' % (r, g, b), share=round(c / total, 3), light=round(l, 2), sat=round(s, 2)))
    stats = dict(duration=round(D, 2), shots=len(shots),
                 shot_mean=round(statistics.mean(shots), 2) if shots else D,
                 shot_median=round(statistics.median(shots), 2) if shots else D,
                 shot_min=min(shots) if shots else D, shot_max=max(shots) if shots else D,
                 cuts_per_10s=round(len(shots) / D * 10, 1),
                 brightness=round(statistics.mean(lum), 2), saturation=round(statistics.mean(sat), 2),
                 grain=round(statistics.mean(grain), 1), palette=colors)
    json.dump(stats, open(os.path.join(out, 'measure.json'), 'w'), indent=1)
    pace = '快' if stats['shot_mean'] < 1.5 else '中' if stats['shot_mean'] < 3.5 else '慢'
    pal_md = '\n'.join(f"| {c['hex']} | {c['share']*100:.0f}% | 亮 {c['light']} 飽和 {c['sat']} | （用喺：） |" for c in colors)
    md = f"""# 風格指南：{os.path.basename(out.rstrip('/'))}
> 自動量度（tools/ref_style.py）+ 人手睇 sheet 填文法。**只拎文法，唔拎內容。**

## 量度
- 長度 {stats['duration']}s｜鏡頭 {stats['shots']} 個｜平均 {stats['shot_mean']}s、中位 {stats['shot_median']}s（最短 {stats['shot_min']}s、最長 {stats['shot_max']}s）→ 節奏：**{pace}**
- 每 10 秒剪 {stats['cuts_per_10s']} 下｜亮度 {stats['brightness']}｜飽和 {stats['saturation']}｜顆粒指數 {stats['grain']}（> 6 算有明顯顆粒）

## 色板（自動）
| hex | 佔比 | 性質 | 色彩意思 |
|---|---|---|---|
{pal_md}

## 文法（睇 sheet 填，每欄要具體到可以寫 code）
- 主角元素（hero）：
- 字體：
- 字點入：
- 字點出／handoff：
- 轉場（≤ 3 種）：
- 鏡頭運動：
- 重拍落乜：
- 質感：
- 版面同留白：
- 聲效語言：

## 唔好抄
- logo／角色／相片／原句／音樂：

## 轉做我哋動態系統卡要改嘅地方
-
"""
    p = os.path.join(out, 'style-guide.md')
    if os.path.exists(p): p = os.path.join(out, 'style-guide.auto.md')
    open(p, 'w').write(md)
    print(f'✓ {p}｜鏡頭平均 {stats["shot_mean"]}s（{pace}）｜主色 ' + ' '.join(c['hex'] for c in colors[:4]))

if __name__ == '__main__':
    if len(sys.argv) < 4: sys.exit(__doc__)
    main(*sys.argv[1:4])
