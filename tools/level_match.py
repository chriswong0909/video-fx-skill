#!/usr/bin/env python3
"""level_match.py — 多把聲（講者原聲 + 新 VO／旁白）逐段對齊響度，再混成一條音軌
  python3 tools/level_match.py out.wav [--target -16] [--max 15] trackA.wav:segsA.json trackB.wav:segsB.json ...
每條 track 係同一條時間線、同一長度嘅 48k mono wav（唔屬於佢嘅時間係靜音）。
segs.json：[[t0,t1],...] 每段獨立量度（例如每條答案一段、每條 VO 問題一段）。
做法：每段用 ffmpeg ebur128 量 integrated LUFS → 加減 dB 去到 target（每段最多 ±15 dB，--max 可改，太短／太靜量唔到就用該 track 中位數）
     → 段與段之間 gain 用 60ms 斜坡 → 相加 → 軟限幅（峰值 -1.5 dBFS）。印出每段前後數值，方便寫入 QA 報告。
唔做動態壓縮、唔改音色；只係搬音量。之後聲效用 sfx.py mix 疊上去。
"""
import json, re, subprocess, sys, wave
import numpy as np
MAXDB = 15.0

def lufs(x, sr):
    if len(x) < sr * 0.5: return None
    p = subprocess.run(['ffmpeg', '-hide_banner', '-f', 's16le', '-ar', str(sr), '-ac', '1', '-i', '-', '-af', 'ebur128=framelog=verbose', '-f', 'null', '-'],
                       input=(np.clip(x, -1, 1) * 32767).astype('<i2').tobytes(), capture_output=True)
    m = re.findall(r'I:\s+(-?[\d.]+) LUFS', p.stderr.decode(errors='ignore'))
    v = float(m[-1]) if m else None
    return v if v is not None and v > -60 else None

def main():
    a = sys.argv[1:]; out = a.pop(0); target = -16.0
    global MAXDB
    while a and a[0] in ('--target', '--max'):
        k = a.pop(0); v = float(a.pop(0))
        if k == '--target': target = v
        else: MAXDB = v
    mix = None; rep = []
    for spec in a:
        path, sj = spec.rsplit(':', 1); segs = json.load(open(sj))
        w = wave.open(path); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64) / 32768
        if w.getnchannels() > 1: x = x.reshape(-1, w.getnchannels()).mean(1)
        meas = [lufs(x[int(s * sr):int(e * sr)], sr) for s, e in segs]
        ok = [m for m in meas if m is not None]; med = float(np.median(ok)) if ok else target
        g = np.ones(len(x)); pts = []
        for (s, e), m in zip(segs, meas):
            db = max(-MAXDB, min(MAXDB, target - (m if m is not None else med))); pts.append((s, e, db))
            rep.append((path.split('/')[-1], s, e, m, db))
        ramp = int(0.06 * sr); cur = np.zeros(len(x))
        for s, e, db in pts: cur[max(0, int(s * sr) - ramp):min(len(x), int(e * sr) + ramp)] = db
        k = np.ones(ramp) / ramp; cur = np.convolve(cur, k, mode='same')
        y = x * (10 ** (cur / 20))
        mix = y if mix is None else (mix[:min(len(mix), len(y))] + y[:min(len(mix), len(y))])
    lim = 10 ** (-1.5 / 20); pk = np.abs(mix).max()
    over = np.abs(mix) > lim * 0.8                                  # 軟限幅：0.8×上限以上用 tanh 壓
    if pk > lim * 0.8:
        t = lim * 0.8; mix = np.where(over, np.sign(mix) * (t + (lim - t) * np.tanh((np.abs(mix) - t) / (lim - t))), mix)
    wo = wave.open(out, 'w'); wo.setnchannels(1); wo.setsampwidth(2); wo.setframerate(sr); wo.writeframes((mix * 32767).astype('<i2').tobytes()); wo.close()
    for n, s, e, m, db in rep: print(f"{n:14s} {s:6.2f}-{e:6.2f}  原本 {('%.1f' % m) if m is not None else '量唔到':>6} LUFS  調 {db:+.1f} dB")
    print(f"✓ {out}｜目標 {target} LUFS｜混音後 {lufs(mix, sr)} LUFS｜峰值 {20 * np.log10(np.abs(mix).max() + 1e-9):.1f} dBFS")
main()
