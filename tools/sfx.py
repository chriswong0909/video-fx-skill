#!/usr/bin/env python3
"""video-fx 聲效工具（只需 numpy + ffmpeg）

  python3 tools/sfx.py synth [--only SFX-001,...] [--force]   合成內置聲效入 sounds/
  python3 tools/sfx.py add <音檔> <english-slug> <category> "<中文名>" [--start 秒 --dur 秒] [--source "..."] [--license "..."]
                                                              外來聲效（例如 Pixabay）剪裁、統一音量、入庫
  python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>  原聲（音量不變）+ 聲效混音
        cues.json：[{"sfx":"SFX-001","t":3.8,"vol":0.5}, ...]   vol 可略，預設用 sound.md 嘅 volume
  python3 tools/sfx.py peaks                                  重算所有 sounds/*/peaks.json

每個聲效資料夾：sounds/SFX-###-slug/{sound.md, sound.mp3, peaks.json}
"""
import sys, os, re, json, subprocess, argparse, datetime, tempfile, wave
import numpy as np

SR = 48000
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SND = os.path.join(ROOT, 'sounds')
rng = np.random.default_rng(7)

# ---------- DSP helpers ----------
def t_(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))

def fft_filter(x, lo=None, hi=None):
    n = len(x); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); m = np.ones_like(f)
    if lo: m *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1)) ** 4)
    if hi: m *= 1 / np.sqrt(1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, n)

def sweep_band(x, fc, q=1.2):
    """時變帶通：fc = 每個樣本嘅中心頻率 array，用 STFT overlap-add。"""
    N, H = 1024, 256; w = np.hanning(N); out = np.zeros(len(x) + N); norm = np.zeros(len(x) + N)
    xp = np.concatenate([x, np.zeros(N)]); f = np.fft.rfftfreq(N, 1 / SR)
    for s in range(0, len(x), H):
        c = fc[min(s + N // 2, len(fc) - 1)]; bw = c / q
        m = np.exp(-0.5 * ((f - c) / (bw / 2)) ** 2)
        seg = np.fft.irfft(np.fft.rfft(xp[s:s + N] * w) * m, N) * w
        out[s:s + N] += seg; norm[s:s + N] += w ** 2
    return (out / np.maximum(norm, 1e-6))[:len(x)]

def env_ar(d, a, peak=None, curve=2.0):
    t = t_(d); p = peak if peak is not None else a
    e = np.where(t < p, (t / max(p, 1e-4)) ** curve, ((d - t) / max(d - p, 1e-4)) ** curve)
    return np.clip(e, 0, 1)

def exp_dec(d, tau): return np.exp(-t_(d) / tau)

def reverb(x, dur=0.8, mix=0.2, lp=5000):
    ir = noise(dur) * np.exp(-t_(dur) / (dur / 5)); ir = fft_filter(ir, hi=lp); ir /= np.sqrt(np.sum(ir ** 2))
    n = len(x) + len(ir); y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)
    dry = np.concatenate([x, np.zeros(len(ir))])
    return dry * (1 - mix) + y * mix

def tone(freqs, d, amps=None, decays=None, phase_glide=None):
    t = t_(d); y = np.zeros_like(t)
    for i, fr in enumerate(freqs):
        a = 1 if amps is None else amps[i]; dc = 1e9 if decays is None else decays[i]
        y += a * np.sin(2 * np.pi * fr * t) * np.exp(-t / dc)
    return y

def glide(f0, f1, d, shape=3.0):
    t = t_(d); f = f1 + (f0 - f1) * np.exp(-shape * t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

def place(buf, x, at):
    i = int(at * SR); j = min(len(buf), i + len(x)); buf[i:j] += x[:j - i]; return buf

def pan(x, start=-0.6, end=0.6):
    p = np.linspace(start, end, len(x)); l = np.cos((p + 1) * np.pi / 4); r = np.sin((p + 1) * np.pi / 4)
    return np.stack([x * l, x * r], 1)

def fade(x, fi=0.003, fo=0.01):
    x = x.copy(); a = int(fi * SR); b = int(fo * SR)
    if a: x[:a] *= np.linspace(0, 1, a)[:, None] if x.ndim > 1 else np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)[:, None] if x.ndim > 1 else np.linspace(1, 0, b)
    return x

# ---------- 內置聲效配方 ----------
def r_whoosh_soft():
    d = 0.75; x = noise(d); p = t_(d) / d
    fc = 350 + 2600 * np.sin(np.pi * np.clip(p / 0.9, 0, 1)) ** 1.5
    y = sweep_band(x, fc, q=1.0) * env_ar(d, 0, peak=0.42, curve=1.8)
    return pan(reverb(y, 0.5, 0.15)[:int(d * SR)], -0.7, 0.7)

def r_whoosh_fast():
    d = 0.38; x = noise(d); p = t_(d) / d
    fc = 900 + 6500 * np.sin(np.pi * p) ** 2
    y = sweep_band(x, fc, q=1.4) * env_ar(d, 0, peak=0.35, curve=1.5)
    return pan(y, -0.8, 0.8)

def r_suck_in():
    d = 0.9; x = noise(d); p = t_(d) / d
    fc = 300 + 5000 * p ** 2.2
    y = sweep_band(x, fc, q=1.0) * p ** 2.5
    y = y + 0.25 * glide(90, 220, d, 0.0001) * p ** 3
    return fade(y, 0.02, 0.004)

def r_pop_bubble():
    d = 0.16; y = glide(1100, 320, d, 6) * exp_dec(d, 0.035)
    y[:int(0.002 * SR)] += fft_filter(noise(0.002), lo=2000) * 0.3
    return fade(y, 0.0005, 0.01)

def r_pop_soft():
    d = 0.14; y = glide(620, 230, d, 5) * exp_dec(d, 0.04) * env_ar(d, 0, peak=0.006, curve=1)
    return fade(fft_filter(y, hi=3000), 0.001, 0.01)

def r_click_ui():
    d = 0.06; y = fft_filter(noise(d), lo=2500) * exp_dec(d, 0.004) * 0.6 + tone([2300], d, decays=[0.008]) * 0.5
    return fade(y, 0.0003, 0.005)

def r_type_ticks():
    d = 1.2; buf = np.zeros(int(d * SR)); t = 0.02
    while t < d - 0.08:
        k = fft_filter(noise(0.03), lo=1800, hi=9000) * exp_dec(0.03, 0.004) * rng.uniform(0.5, 1.0)
        k += tone([rng.uniform(1600, 2600)], 0.03, decays=[0.006]) * 0.3
        place(buf, k, t); t += rng.uniform(0.07, 0.14)
    return fade(buf, 0.001, 0.02)

def r_ding():
    d = 1.6; f = 1046.5
    y = tone([f, f * 2.0, f * 2.76, f * 5.4], d, amps=[1, .35, .3, .12], decays=[.55, .3, .18, .08])
    y *= env_ar(d, 0, peak=0.002, curve=1) ** 0.2
    return fade(reverb(y, 1.0, 0.18)[:int(d * SR)], 0.001, 0.2)

def r_chime_up():
    d = 1.1; buf = np.zeros(int(d * SR))
    for at, f in [(0, 1046.5), (0.12, 1568.0)]:
        n = fade(tone([f, f * 3.0, f * 4.0], 0.9, amps=[1, .25, .1], decays=[.3, .08, .05]), 0.001, 0.3); place(buf, n, at)
    return fade(reverb(buf, 0.8, 0.2)[:int(d * SR)], 0.001, 0.15)

def r_error_buzz():
    d = 0.5; buf = np.zeros(int(d * SR)); t = t_(0.16)
    b = np.sign(np.sin(2 * np.pi * 170 * t)) * 0.6 + np.sin(2 * np.pi * 340 * t) * 0.3
    b = fft_filter(b, hi=1800) * env_ar(0.16, 0, peak=0.01, curve=0.5)
    place(buf, b, 0.0); place(buf, b, 0.22)
    return fade(buf, 0.002, 0.03)

def r_impact_low():
    d = 1.4; y = glide(130, 42, d, 5) * exp_dec(d, 0.35)
    y += fft_filter(noise(d), hi=900) * exp_dec(d, 0.05) * 0.8
    y += fft_filter(noise(d), lo=2000) * exp_dec(d, 0.012) * 0.25
    return fade(reverb(y, 1.2, 0.2, lp=2500)[:int(d * SR)], 0.0005, 0.3)

def r_riser():
    d = 2.0; p = t_(d) / d; x = noise(d)
    y = sweep_band(x, 200 + 7000 * p ** 2, q=1.3) * p ** 2
    f = 110 * 2 ** (p * 2); saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    y += fft_filter(saw, hi=2500) * 0.2 * p ** 2
    return pan(fade(y, 0.05, 0.004), -0.3, 0.3)

def r_shutter():
    d = 0.3; buf = np.zeros(int(d * SR))
    for at, a in [(0.0, 1.0), (0.075, 0.7)]:
        k = fft_filter(noise(0.05), lo=1200, hi=7000) * exp_dec(0.05, 0.006) * a
        k += tone([rng.uniform(900, 1200)], 0.05, decays=[0.01]) * 0.3 * a; place(buf, k, at)
    return fade(buf, 0.0005, 0.02)

def r_card_slide():
    d = 0.45; x = noise(d); p = t_(d) / d
    y = sweep_band(x, 2200 - 1200 * p, q=0.9) * env_ar(d, 0, peak=0.25, curve=1.2)
    y += fft_filter(noise(d), hi=400) * env_ar(d, 0, peak=0.9, curve=4) * 0.3
    return pan(fade(y, 0.005, 0.02), 0.5, -0.1)

def r_heartbeat():
    d = 1.8; buf = np.zeros(int(d * SR))
    for beat in [0.0, 0.9]:
        for off, a in [(0, 1.0), (0.26, 0.7)]:
            k = glide(75, 45, 0.18, 4) * exp_dec(0.18, 0.05) * a; place(buf, fade(fft_filter(k, hi=300), 0.004, 0.05), beat + off)
    return fade(buf, 0.002, 0.05)

def r_sparkle():
    d = 1.2; buf = np.zeros(int(d * SR))
    for i in range(14):
        at = 0.02 + i * 0.05 + rng.uniform(0, 0.03); f = rng.uniform(3000, 8000)
        place(buf, fade(tone([f], 0.25, decays=[0.05]), 0.001, 0.05) * rng.uniform(0.3, 0.8) * (1 - i / 18), at)
    return pan(fade(reverb(buf, 0.9, 0.3)[:int(d * SR)], 0.001, 0.2), -0.5, 0.5)

def r_glitch():
    d = 0.4; buf = np.zeros(int(d * SR)); t = 0.0
    while t < d - 0.03:
        L = rng.uniform(0.015, 0.05); seg = noise(L)
        seg = np.round(seg * 4) / 4; step = int(rng.integers(4, 16)); seg = np.repeat(seg[::step], step)[:int(L * SR)]
        seg = fft_filter(seg, lo=rng.uniform(300, 1500), hi=rng.uniform(3000, 9000)) * rng.uniform(0.4, 1.0)
        place(buf, seg, t); t += L + rng.uniform(0, 0.03)
    return fade(buf, 0.001, 0.01)

def r_sub_drop():
    d = 1.2; y = glide(95, 32, d, 2.5) * env_ar(d, 0, peak=0.01, curve=0.6) * exp_dec(d, 0.6)
    return fade(y, 0.001, 0.2)

VT_ALL = ['口播知識', '訪問對談', '醫療健康', '動畫解說', '產品廣告', '紀錄 Vlog', '新聞資訊', '品牌企業']
RECIPES = [
 # slug, fn, 中文名, name_en, category, volume, mood, pace, pairs_with, 幾時用, 幾時唔好用
 ('whoosh-soft', r_whoosh_soft, '柔和風聲轉場', 'Soft whoosh', 'whoosh', 0.35, ['專業醫療', '溫暖生活', '高級編輯感'], ['中', '慢'],
  ['FX-040', 'FX-006', 'FX-046', 'FX-003'], '推鏡、全屏過場入場、畫面左右滑走。聲音中心對準動作最快嗰格（約 0.3 秒後）。', '每 10 秒唔好多過一次；硬切唔使配。'),
 ('whoosh-fast', r_whoosh_fast, '快速嗖聲', 'Fast whoosh', 'whoosh', 0.3, ['活潑年輕', '高級編輯感'], ['快'],
  ['FX-046', 'FX-026', 'FX-054', 'FX-005'], '快節奏橫掃切換、閃卡、卡片快速滑入。', '慢節奏醫療片會顯得浮躁。'),
 ('suck-in', r_suck_in, '反向吸入', 'Reverse suck-in', 'riser', 0.35, ['高級編輯感', '活潑年輕'], ['快', '中'],
  ['FX-006', 'FX-017', 'FX-053', 'FX-063'], '大字或全屏畫面出現之前 0.9 秒開始，完結一刻正正係畫面出現。', '唔好連續用兩次；開場第一秒用就好。'),
 ('pop-bubble', r_pop_bubble, '彈字泡泡聲', 'Bubble pop', 'pop', 0.4, ['活潑年輕', '溫暖生活'], ['快', '中'],
  ['FX-044', 'FX-057', 'FX-037', 'FX-055', 'FX-033'], '膠囊字、徽章、圖示、通知逐個彈出；每個元素出現嗰格落聲。', '連續彈 5 個以上要降音量或隔一個先落。'),
 ('pop-soft', r_pop_soft, '柔和 pop', 'Soft pop', 'pop', 0.45, ['專業醫療', '溫暖生活'], ['中', '慢'],
  ['FX-032', 'FX-067', 'FX-038', 'FX-064'], '清單逐項出、名牌出現；比泡泡聲穩重，適合醫療。', '同一句入面唔好同泡泡聲混用。'),
 ('click-ui', r_click_ui, 'UI 點擊', 'UI click', 'ui', 0.45, ['專業醫療', '高級編輯感'], ['快', '中', '慢'],
  ['FX-029', 'FX-035', 'FX-031'], 'UI 元件、按鈕、剔選、畫面點擊示範。', '唔好用嚟配文字出現（太細聲會似雜音）。'),
 ('type-ticks', r_type_ticks, '打字聲', 'Typing ticks', 'ui', 0.3, ['專業醫療', '新聞資訊'], ['中', '慢'],
  ['FX-066', 'FX-052', 'FX-059'], '逐字打出、數字逐位出；長度可以剪到同動畫一樣。', '講者講緊重點時會搶聲，放喺停頓位。'),
 ('ding', r_ding, '重點 ding', 'Highlight ding', 'ding', 0.3, ['專業醫療', '溫暖生活'], ['中', '慢'],
  ['FX-065', 'FX-027', 'FX-022', 'FX-050'], '金句、重點字、圈註出現；一條片 1–3 次。', '唔好每句都 ding，會變廉價。'),
 ('chime-up', r_chime_up, '上升提示音', 'Positive chime', 'ding', 0.3, ['溫暖生活', '活潑年輕'], ['中', '慢'],
  ['FX-044', 'FX-057', 'FX-034'], '正確答案、建議做法、正面結果、增長曲線。', '同錯誤聲一齊用做「錯 vs 啱」對比最有效。'),
 ('error-buzz', r_error_buzz, '錯誤警示聲', 'Error buzz', 'ding', 0.3, ['活潑年輕', '專業醫療'], ['快', '中'],
  ['FX-047', 'FX-045', 'FX-013'], '打交叉、迷思、錯誤做法、警告橫額。', '嚴肅病情（例如癌症）唔好用，會輕佻。'),
 ('impact-low', r_impact_low, '低頻重擊', 'Low impact', 'impact', 0.4, ['高級編輯感', '專業醫療'], ['快', '中'],
  ['FX-017', 'FX-053', 'FX-048', 'FX-062'], '大字砸落、章節標題、物件跌落著地嗰格。', '手機喇叭聽唔到低頻，唔好靠佢做唯一提示。'),
 ('riser', r_riser, '上升張力', 'Short riser', 'riser', 0.3, ['高級編輯感', '活潑年輕'], ['快', '中'],
  ['FX-006', 'FX-053', 'FX-063'], 'Hook 開場前、揭曉答案之前 2 秒；完結位接 impact 或 ding。', '會蓋過人聲，只放喺講者停頓或開場。'),
 ('shutter', r_shutter, '相機快門', 'Camera shutter', 'foley', 0.45, ['高級編輯感', '溫暖生活'], ['快', '中'],
  ['FX-058', 'FX-061', 'FX-010'], '相片插入、出相、定格、海報框出現。', '冇相片畫面時唔好用。'),
 ('card-slide', r_card_slide, '卡片滑入', 'Card slide', 'foley', 0.4, ['專業醫療', '溫暖生活'], ['中', '慢'],
  ['FX-005', 'FX-032', 'FX-021', 'FX-041'], '卡片、紙張、相片滑入畫面。', '快節奏片改用快速嗖聲。'),
 ('heartbeat', r_heartbeat, '心跳', 'Heartbeat', 'foley', 0.5, ['專業醫療'], ['中', '慢'],
  ['FX-014', 'FX-050', 'FX-028'], '心臟、脈搏、緊張時刻、心電圖描繪。', '唔好長時間 loop；手機喇叭要加大音量。'),
 ('sparkle', r_sparkle, '閃光', 'Sparkle', 'accent', 0.3, ['溫暖生活', '活潑年輕'], ['中', '慢'],
  ['FX-063', 'FX-027', 'FX-049', 'FX-042'], '發光字、光束、Logo 結尾、線稿變彩色。', '醫療嚴肅題材少用。'),
 ('glitch', r_glitch, '故障雜訊', 'Glitch burst', 'accent', 0.3, ['活潑年輕', '高級編輯感'], ['快'],
  ['FX-054'], 'RGB 分離、故障字；對準畫面閃爍幀。', '溫暖／醫療片唔適合。'),
 ('sub-drop', r_sub_drop, '低頻下沉', 'Sub drop', 'impact', 0.45, ['高級編輯感'], ['快', '中'],
  ['FX-006', 'FX-053', 'FX-017'], '揭曉、轉入重要段落；可以同 riser 或 suck-in 接住用。', '手機喇叭幾乎聽唔到，要配畫面動作。'),
]
CAT_ZH = {'whoosh': '轉場風聲', 'pop': '彈出', 'ui': '介面', 'ding': '提示音', 'impact': '重擊', 'riser': '張力', 'foley': '擬音', 'accent': '點綴', 'music': '背景音樂', 'ambience': '環境聲'}

# ---------- I/O ----------
def write_wav(path, y):
    y = np.asarray(y, dtype=np.float64)
    if y.ndim == 1: y = np.stack([y, y], 1)
    if not np.all(np.isfinite(y)): raise ValueError('NaN in audio')
    y = y / (np.max(np.abs(y)) + 1e-9) * 10 ** (-1 / 20)  # peak -1 dBFS
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype('<i2').tobytes())

def ff(*a): subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)

def decode(path):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float32) / 32768

def make_peaks(folder):
    y = decode(os.path.join(folder, 'sound.mp3')); n = 96
    ch = np.array_split(np.abs(y), n); pk = [float(np.max(c)) if len(c) else 0 for c in ch]
    m = max(pk) or 1; pk = [round(p / m, 3) for p in pk]
    json.dump({'duration': round(len(y) / SR, 3), 'peaks': pk}, open(os.path.join(folder, 'peaks.json'), 'w'))
    return len(y) / SR

def existing():
    os.makedirs(SND, exist_ok=True)
    return {d[8:]: d for d in os.listdir(SND) if re.match(r'SFX-\d{3}-', d)}

def next_id():
    ids = [int(d[4:7]) for d in os.listdir(SND) if re.match(r'SFX-\d{3}-', d)]
    removed = os.path.join(SND, 'REMOVED.md')
    if os.path.exists(removed): ids += [int(x) for x in re.findall(r'SFX-(\d{3})', open(removed, encoding='utf-8').read())]
    return f"SFX-{(max(ids) + 1 if ids else 1):03d}"

def q(s): return '"' + str(s).replace('"', '\\"') + '"'
def lst(a): return '[' + ', '.join(a) + ']'

def write_md(folder, sid, slug, name, en, cat, vol, mood, pace, pairs, when, whennot, source, license_, dur):
    today = datetime.date.today().isoformat()
    md = f"""---
id: {sid}
name: {name}
name_en: {en}
category: {cat}
duration: {dur:.2f}
volume: {vol}
mood: {lst(mood)}
video_types: {lst(VT_ALL)}
pace: {lst(pace)}
pairs_with: {lst(pairs)}
source: {q(source)}
license: {q(license_)}
learned: {today}
used_in: []
status: active
---

## 聲效
{name}（{en}），{dur:.2f} 秒，{CAT_ZH.get(cat, cat)}類。

## 幾時用
- {when}

## 幾時唔好用
- {whennot}

## 用法
- 建議音量 `volume: {vol}`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
"""
    open(os.path.join(folder, 'sound.md'), 'w', encoding='utf-8').write(md)

def cmd_synth(args):
    have = existing(); only = set(args.only.split(',')) if args.only else None
    for slug, fn, name, en, cat, vol, mood, pace, pairs, when, whennot in RECIPES:
        if slug in have and not args.force: print('略過（已存在）', have[slug]); continue
        folder = os.path.join(SND, have.get(slug) or f"{next_id()}-{slug}")
        sid = os.path.basename(folder)[:7]
        if only and sid not in only and slug not in only: continue
        os.makedirs(folder, exist_ok=True)
        with tempfile.TemporaryDirectory() as td:
            wv = os.path.join(td, 'a.wav'); write_wav(wv, fn())
            ff('-i', wv, '-c:a', 'libmp3lame', '-b:a', '160k', os.path.join(folder, 'sound.mp3'))
        dur = make_peaks(folder)
        if args.force or not os.path.exists(os.path.join(folder, 'sound.md')):
            write_md(folder, sid, slug, name, en, cat, vol, mood, pace, pairs, when, whennot,
                     'synth: tools/sfx.py', '自製合成，無版權限制，可商用', dur)
        print('✓', os.path.basename(folder), f'{dur:.2f}s')

def cmd_add(args):
    existing(); sid = next_id(); folder = os.path.join(SND, f'{sid}-{args.slug}'); os.makedirs(folder)
    trim = (['-ss', str(args.start)] if args.start else []) + (['-t', str(args.dur)] if args.dur else [])
    with tempfile.TemporaryDirectory() as td:
        wv = os.path.join(td, 'a.wav'); ff(*trim, '-i', args.file, '-ac', '2', '-ar', str(SR), wv)
        y = decode(wv)  # mono for peak calc
        raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', wv, '-f', 's16le', '-'], capture_output=True, check=True).stdout
        st = np.frombuffer(raw, '<i2').astype(np.float64).reshape(-1, 2) / 32768
        write_wav(wv, fade(st, 0.002, 0.02))
        ff('-i', wv, '-c:a', 'libmp3lame', '-b:a', '160k', os.path.join(folder, 'sound.mp3'))
    dur = make_peaks(folder)
    write_md(folder, sid, args.slug, args.name, args.slug.replace('-', ' ').title(), args.category, 0.35, [], ['快', '中', '慢'], [],
             '（待補）', '（待補）', args.source or os.path.basename(args.file), args.license or '（請註明授權）', dur)
    print('✓ 新增', os.path.basename(folder), f'{dur:.2f}s → 請補完 sound.md 嘅 mood／pairs_with／幾時用')

def read_fm(path):
    txt = open(path, encoding='utf-8').read(); m = re.match(r'^---\n([\s\S]*?)\n---', txt); o = {}
    for line in (m.group(1) if m else '').split('\n'):
        k = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if k: o[k.group(1)] = k.group(2).strip()
    return o

def cmd_mix(args):
    cues = json.load(open(args.cues)); dirs = {d[:7]: os.path.join(SND, d) for d in os.listdir(SND) if re.match(r'SFX-\d{3}-', d)}
    inputs = ['-i', args.source]; parts = []; labels = ['[0:a]']
    for i, c in enumerate(cues, 1):
        d = dirs[c['sfx']]; vol = float(c.get('vol', read_fm(os.path.join(d, 'sound.md')).get('volume', 0.35)))
        inputs += ['-i', os.path.join(d, 'sound.mp3')]; ms = int(round(float(c['t']) * 1000))
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[s{i}]"); labels.append(f'[s{i}]')
    graph = ';'.join(parts + [f"[0:a]aresample=48000,aformat=channel_layouts=stereo[v]"]) + ';' + ''.join(['[v]'] + labels[1:]) + \
        f"amix=inputs={len(labels)}:duration=first:normalize=0:dropout_transition=0,alimiter=limit=0.97[out]"
    ff(*inputs, '-filter_complex', graph, '-map', '[out]', '-c:a', 'aac', '-b:a', '256k', args.out)
    print('✓ 混音完成', args.out, f'（{len(cues)} 個聲效；原聲音量不變，加 limiter 防爆音）')

def cmd_peaks(args):
    for d in sorted(os.listdir(SND)):
        if re.match(r'SFX-\d{3}-', d): print(d, f'{make_peaks(os.path.join(SND, d)):.2f}s')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('synth'); s.add_argument('--only'); s.add_argument('--force', action='store_true'); s.set_defaults(f=cmd_synth)
    a = sp.add_parser('add'); a.add_argument('file'); a.add_argument('slug'); a.add_argument('category'); a.add_argument('name')
    a.add_argument('--start', type=float); a.add_argument('--dur', type=float); a.add_argument('--source'); a.add_argument('--license'); a.set_defaults(f=cmd_add)
    m = sp.add_parser('mix'); m.add_argument('source'); m.add_argument('cues'); m.add_argument('out'); m.set_defaults(f=cmd_mix)
    p = sp.add_parser('peaks'); p.set_defaults(f=cmd_peaks)
    args = ap.parse_args(); args.f(args)
