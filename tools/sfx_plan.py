#!/usr/bin/env python3
"""sfx_plan.py — 由「視覺事件表」出聲效 cues：聲效最響位對準動作落地嗰格
  python3 tools/sfx_plan.py events.json cues.json
events.json：[{"t": 落地秒數, "sfx": "SFX-011", "vol": 0.3, "why": "大字撞入"}]
cues.json：   [{"sfx": "SFX-011", "t": 開始秒數, "vol": 0.3}]  → 直接俾 tools/sfx.py mix 用
每個聲效檔嘅最響位（peak）自動量度：t_開始 = t_落地 − peak。
"""
import glob, json, os, struct, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_cache = {}

def peak(sfx):
    if sfx in _cache: return _cache[sfx]
    d = glob.glob(os.path.join(ROOT, 'sounds', sfx + '-*'))[0]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(d, 'sound.mp3'), '-ac', '1', '-ar', '8000', '-f', 's16le', '-'],
                         capture_output=True).stdout
    s = struct.unpack('<%dh' % (len(raw) // 2), raw); a = [abs(x) for x in s]
    _cache[sfx] = a.index(max(a)) / 8000
    return _cache[sfx]

def main(ev_path, out_path):
    ev = json.load(open(ev_path)); cues = []
    for e in sorted(ev, key=lambda e: e['t']):
        p = peak(e['sfx']); t = max(0.0, e['t'] - p)
        cues.append({'sfx': e['sfx'], 't': round(t, 3), 'vol': e.get('vol', 0.3)})
        print(f"{e['t']:6.2f}s 落地 ← {e['sfx']}（peak {p:.3f}s）開始 {t:6.2f}s  {e.get('why','')}")
    gaps = [b['t'] - a['t'] for a, b in zip(cues, cues[1:])]
    if gaps and min(gaps) < 0.15: print('! 有兩個聲效相隔少過 0.15 秒，會疊埋')
    json.dump(cues, open(out_path, 'w'), indent=0)
    print(f'✓ {len(cues)} 個 cue → {out_path}')

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
