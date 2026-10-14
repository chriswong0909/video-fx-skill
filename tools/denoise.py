#!/usr/bin/env python3
"""降噪前置步驟（剪片前、轉錄前做）。用 voice-denoise skill 嘅同一條流程（DeepFilterNet3 + FFmpeg 人聲潤飾）。

  python3 tools/denoise.py check  in.mp4            # 量度並判斷洗唔洗降噪（JSON）
  python3 tools/denoise.py run    in.mp4 [out.mp4|-] [atten_db]  # 降噪 -> <name>_clean.mp4（畫面唔重新編碼）；atten 例如 20 = 降少啲
  python3 tools/denoise.py auto   in.mp4            # check，洗就 run；唔洗就只報告

判斷（任何一項中就降噪）：
  - 信噪比 SNR = 講嘢位 RMS(P90) - 靜音位 RMS(P10) < 35 dB
  - 靜音位 RMS(P10) > -55 dBFS
  - 整體響度 < -26 LUFS（聲太細，抬大會連底噪一齊抬）
2026-10-14 實測：骨質疏鬆.mp4 SNR 13 dB、靜音位 -44 dB、響度 -32.8 LUFS -> 洗；處理後 SNR 49 dB、靜音位 -63 dB、-16.3 LUFS -> 唔洗。
環境：~/venv-dfn（uv venv -p 3.11；torch==2.1.2 torchaudio==2.1.2 numpy<2 deepfilternet，
  index https://download.pytorch.org/whl/cpu）。無就自動裝。降太重人聲發乾 -> 加 --atten-lim 20。
"""
import sys, os, re, json, subprocess, tempfile, shutil

HOME = os.path.expanduser("~")
VENV = os.path.join(HOME, "venv-dfn")
DF = os.path.join(VENV, "bin", "deepFilter")

def sh(cmd, **k):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **k)

def window_rms(path, win=0.5):
    n = int(48000 * win)
    r = sh(f'ffmpeg -hide_banner -v info -i "{path}" -vn -ac 1 -ar 48000 '
           f'-af "asetnsamples=n={n}:p=0,astats=metadata=1:reset=1,'
           f'ametadata=print:key=lavfi.astats.Overall.RMS_level" -f null - 2>&1')
    vals = [float(x) for x in re.findall(r"RMS_level=(-?[\d.]+|-inf)", r.stdout) if x != "-inf"]
    return vals

def loudness(path):
    r = sh(f'ffmpeg -hide_banner -i "{path}" -vn -af ebur128 -f null - 2>&1')
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stdout)
    return float(m[-1]) if m else None

def pct(v, p):
    v = sorted(v); return v[min(len(v) - 1, int(len(v) * p))]

def check(path):
    w = window_rms(path)
    if len(w) < 10:
        return {"error": "量度唔到音軌", "need": False}
    noise, speech = pct(w, 0.10), pct(w, 0.90)
    snr, lufs = speech - noise, loudness(path)
    reasons = []
    if snr < 35: reasons.append(f"信噪比 {snr:.0f} dB < 35")
    if noise > -55: reasons.append(f"靜音位 {noise:.0f} dBFS > -55")
    if lufs is not None and lufs < -26: reasons.append(f"響度 {lufs:.1f} LUFS < -26")
    return {"file": path, "noise_p10_db": round(noise, 1), "speech_p90_db": round(speech, 1),
            "snr_db": round(snr, 1), "lufs": lufs, "need": bool(reasons), "reasons": reasons}

def ensure_env():
    if os.path.exists(DF): return
    print("裝 DeepFilterNet3 環境（一次性）…", file=sys.stderr)
    sh(f'uv venv -q -p 3.11 "{VENV}"')
    r = sh(f'VIRTUAL_ENV="{VENV}" uv pip install -q "torch==2.1.2" "torchaudio==2.1.2" "numpy<2" deepfilternet '
           f'--index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple')
    if not os.path.exists(DF):
        sys.exit("環境裝唔到：" + r.stderr[-400:])

def run(inp, out=None, atten=None):
    ensure_env()
    base = os.path.splitext(inp)[0]
    out = out or base + "_clean.mp4"
    tmp = tempfile.mkdtemp(prefix="dfn_", dir=HOME)   # 暫存放 home（唔污染用戶資料夾）
    try:
        a = os.path.join(tmp, "a.wav")
        sh(f'ffmpeg -v error -y -i "{inp}" -vn -ac 1 -ar 48000 "{a}"')
        al = f" --atten-lim {atten}" if atten else ""
        sh(f'"{DF}"{al} "{a}" -o "{tmp}"', timeout=900)
        d = os.path.join(tmp, "a_DeepFilterNet3.wav"); c = os.path.join(tmp, "clean.wav")
        sh(f'ffmpeg -v error -y -i "{d}" -af "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=100:makeup=2,'
           f'loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 "{c}"')
        sh(f'ffmpeg -v error -y -i "{inp}" -i "{c}" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart "{out}"')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    cmd, inp = sys.argv[1], sys.argv[2]
    if cmd == "check":
        print(json.dumps(check(inp), ensure_ascii=False, indent=1))
    elif cmd == "run":
        print(run(inp, sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None, sys.argv[4] if len(sys.argv) > 4 else None))
    elif cmd == "auto":
        r = check(inp); print(json.dumps(r, ensure_ascii=False, indent=1))
        if r.get("need"): print("->", run(inp))
        else: print("唔洗降噪，保持原檔")
