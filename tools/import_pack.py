#!/usr/bin/env python3
"""批量匯入 CC0 聲效包（例如 Kenney）入 sounds/。

  python3 tools/import_pack.py <pack 資料夾> <pack-slug> [--license "CC0 1.0（Kenney.nl）"] [--source URL] [--limit N]

- 每個音檔 → sounds/SFX-###-<pack-slug>-<名>/{sound.mp3（立體聲 160k，峰值 -1 dBFS）, preview.mp3（單聲道 40k，效果目錄用）, peaks.json, sound.md}
- 已匯入過（sound.md 有同一個 source_file）就略過，可以重複行。
- 名、類別、建議音量按檔名關鍵字自動判斷（KEYMAP）；之後可以人手改 sound.md。
- 唔好匯入授權唔清楚嘅檔（例如 soundcn 入面嘅 wow／Blizzard 聲效）。
"""
import os, re, sys, json, glob, argparse, subprocess, tempfile, wave, datetime
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SND = os.path.join(ROOT, 'sounds')
SR = 48000

# 關鍵字（檔名去數字後）→（中文名, category, volume）
KEYMAP = {
 # interface
 'back': ('返回', 'ui', .4), 'bong': ('噹', 'ding', .3), 'click': ('點擊', 'ui', .45), 'close': ('關閉', 'ui', .4),
 'confirmation': ('確認', 'ding', .35), 'drop': ('落下', 'pop', .4), 'error': ('錯誤', 'ding', .3), 'glass': ('玻璃叮', 'ding', .3),
 'glitch': ('故障', 'accent', .3), 'maximize': ('放大', 'whoosh', .35), 'minimize': ('縮細', 'whoosh', .35), 'open': ('打開', 'ui', .4),
 'pluck': ('撥弦', 'pop', .4), 'question': ('疑問', 'ding', .3), 'scratch': ('刮擦', 'accent', .35), 'scroll': ('捲動', 'ui', .4),
 'select': ('選擇', 'ui', .4), 'switch': ('開關', 'ui', .4), 'tick': ('滴答', 'ui', .4), 'toggle': ('切換', 'ui', .4),
 # digital
 'highDown': ('高音下滑', 'ding', .3), 'highUp': ('高音上揚', 'ding', .3), 'laser': ('雷射', 'accent', .3), 'lowDown': ('低音下滑', 'accent', .3),
 'lowRandom': ('低音隨機', 'accent', .3), 'lowThreeTone': ('低音三連音', 'ding', .3), 'pepSound': ('提示嗶', 'ui', .35),
 'phaseJump': ('相位跳', 'accent', .3), 'phaserDown': ('相位下掃', 'whoosh', .3), 'phaserUp': ('相位上掃', 'riser', .3),
 'powerUp': ('升級音', 'ding', .3), 'spaceTrash': ('太空雜音', 'accent', .3), 'threeTone': ('三連音', 'ding', .3), 'tone': ('單音', 'ding', .3),
 'twoTone': ('雙音', 'ding', .3), 'zap': ('電擊', 'accent', .3), 'zapThreeToneDown': ('電擊三連降', 'accent', .3),
 'zapThreeToneUp': ('電擊三連升', 'accent', .3), 'zapTwoTone': ('電擊雙音', 'accent', .3),
 # impact
 'footstep_carpet': ('腳步（地氈）', 'foley', .45), 'footstep_concrete': ('腳步（石地）', 'foley', .45), 'footstep_grass': ('腳步（草地）', 'foley', .45),
 'footstep_snow': ('腳步（雪地）', 'foley', .45), 'footstep_wood': ('腳步（木地）', 'foley', .45), 'impactBell_heavy': ('鐘聲重擊', 'ding', .3),
 'impactGeneric_light': ('輕撞', 'impact', .4), 'impactGlass_heavy': ('玻璃重撞', 'impact', .35), 'impactGlass_light': ('玻璃輕撞', 'impact', .4),
 'impactGlass_medium': ('玻璃撞擊', 'impact', .35), 'impactMetal_heavy': ('金屬重撞', 'impact', .35), 'impactMetal_light': ('金屬輕撞', 'impact', .4),
 'impactMetal_medium': ('金屬撞擊', 'impact', .35), 'impactMining': ('敲石', 'impact', .35), 'impactPlank_medium': ('木板撞擊', 'impact', .4),
 'impactPlate_heavy': ('碟重撞', 'impact', .35), 'impactPlate_light': ('碟輕撞', 'impact', .4), 'impactPlate_medium': ('碟撞擊', 'impact', .35),
 'impactPunch_heavy': ('重拳', 'impact', .35), 'impactPunch_medium': ('拳擊', 'impact', .35), 'impactSoft_heavy': ('軟物重撞', 'impact', .4),
 'impactSoft_medium': ('軟物撞擊', 'impact', .4), 'impactTin_medium': ('鐵罐撞擊', 'impact', .35), 'impactWood_heavy': ('木重撞', 'impact', .35),
 'impactWood_light': ('木輕撞', 'impact', .4), 'impactWood_medium': ('木撞擊', 'impact', .35),
 # casino
 'card-fan': ('扇開紙牌', 'foley', .4), 'card-place': ('放牌', 'foley', .4), 'card-shove': ('推牌', 'foley', .4), 'card-shuffle': ('洗牌', 'foley', .4),
 'card-slide': ('紙卡滑動', 'foley', .4), 'cards-pack-open': ('開卡包', 'foley', .4), 'cards-pack-take-out': ('抽卡', 'foley', .4),
 'chip-lay': ('放籌碼', 'foley', .4), 'chips-collide': ('籌碼碰撞', 'foley', .4), 'chips-handle': ('拎籌碼', 'foley', .4), 'chips-stack': ('疊籌碼', 'foley', .4),
 'dice-grab': ('拎骰', 'foley', .4), 'dice-shake': ('搖骰', 'foley', .4), 'dice-throw': ('擲骰', 'foley', .4), 'die-throw': ('擲單骰', 'foley', .4),
 # rpg
 'beltHandle': ('皮帶', 'foley', .4), 'bookClose': ('合書', 'foley', .45), 'bookFlip': ('翻書', 'foley', .45), 'bookOpen': ('開書', 'foley', .45),
 'bookPlace': ('放書', 'foley', .45), 'chop': ('斬', 'impact', .35), 'cloth': ('布料', 'foley', .4), 'clothBelt': ('布料皮帶', 'foley', .4),
 'creak': ('吱吱聲', 'foley', .35), 'doorClose': ('關門', 'foley', .4), 'doorOpen': ('開門', 'foley', .4), 'drawKnife': ('拔刀', 'whoosh', .35),
 'dropLeather': ('跌皮具', 'foley', .4), 'footstep': ('腳步', 'foley', .45), 'handleCoins': ('錢幣', 'foley', .4),
 'handleSmallLeather': ('皮具', 'foley', .4), 'knifeSlice': ('切', 'foley', .35), 'metalClick': ('金屬咔', 'ui', .4), 'metalLatch': ('門閂', 'foley', .4),
 'metalPot': ('金屬鍋', 'impact', .35),
 # sci-fi
 'computerNoise': ('電腦聲', 'ambience', .2), 'engineCircular': ('引擎循環', 'ambience', .2), 'explosionCrunch': ('爆炸碎裂', 'impact', .3),
 'forceField': ('力場', 'accent', .3), 'impactMetal': ('金屬撞擊', 'impact', .35), 'laserLarge': ('大雷射', 'accent', .3), 'laserRetro': ('復古雷射', 'accent', .3),
 'laserSmall': ('細雷射', 'accent', .3), 'lowFrequency_explosion': ('低頻爆炸', 'impact', .3), 'slime': ('黏液', 'foley', .35),
 'spaceEngine': ('太空引擎', 'ambience', .2), 'spaceEngineLarge': ('大型太空引擎', 'ambience', .2), 'spaceEngineLow': ('低沉太空引擎', 'ambience', .2),
 'spaceEngineSmall': ('細型太空引擎', 'ambience', .2), 'thrusterFire': ('推進器', 'whoosh', .3),
 # jingles
 'jingles_HIT': ('打擊樂短曲', 'music', .25), 'jingles_NES': ('8-bit 短曲', 'music', .25), 'jingles_PIZZI': ('撥弦短曲', 'music', .25),
 'jingles_SAX': ('色士風短曲', 'music', .25), 'jingles_STEEL': ('鋼鼓短曲', 'music', .25),
}
CAT_WHEN = {
 'ui': '介面、按鈕、剔選、畫面點擊示範；配 UI 元件類效果。', 'pop': '元素彈出、標籤出現。', 'ding': '重點、提示、正確／錯誤、結論位。',
 'impact': '大字砸落、物件落地、轉入重點。', 'foley': '真實動作擬音：翻書、紙卡、開門、腳步、錢幣等，對準畫面動作。',
 'whoosh': '畫面移動、轉場、放大縮細。', 'riser': '揭曉之前嘅張力。', 'accent': '點綴、科技感、故障感畫面。',
 'ambience': '背景環境聲（低音量鋪底）。', 'music': '片頭、片尾、段落轉換嘅短音樂（幾秒）。'}
CAT_PACE = {'music': ['中', '慢'], 'ambience': ['中', '慢'], 'foley': ['快', '中', '慢']}
CAT_MOOD = {'ui': ['專業醫療', '高級編輯感'], 'pop': ['活潑年輕', '溫暖生活'], 'ding': ['專業醫療', '溫暖生活'], 'impact': ['高級編輯感', '活潑年輕'],
 'foley': ['溫暖生活', '專業醫療'], 'whoosh': ['高級編輯感', '活潑年輕'], 'riser': ['高級編輯感'], 'accent': ['活潑年輕'],
 'ambience': ['高級編輯感'], 'music': ['活潑年輕', '溫暖生活']}
VT_ALL = ['口播知識', '訪問對談', '醫療健康', '動畫解說', '產品廣告', '紀錄 Vlog', '新聞資訊', '品牌企業']

def ff(*a): subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)

def decode(path, ch=2):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', path, '-ac', str(ch), '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float64).reshape(-1, ch) / 32768

def write_wav(path, y):
    with wave.open(path, 'wb') as w:
        w.setnchannels(y.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype('<i2').tobytes())

def next_id():
    ids = [int(d[4:7]) for d in os.listdir(SND) if re.match(r'SFX-\d{3}-', d)]
    rm = os.path.join(SND, 'REMOVED.md')
    if os.path.exists(rm): ids += [int(x) for x in re.findall(r'SFX-(\d{3})', open(rm, encoding='utf-8').read())]
    return (max(ids) + 1) if ids else 1

def done_sources():
    s = set()
    for f in glob.glob(os.path.join(SND, 'SFX-*', 'sound.md')):
        m = re.search(r'^source_file: "?(.*?)"?$', open(f, encoding='utf-8').read(), re.M)
        if m: s.add(m.group(1))
    return s

def lst(a): return '[' + ', '.join(a) + ']'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('pack')
    ap.add_argument('--license', default='CC0 1.0（Kenney.nl），可商用、免署名'); ap.add_argument('--source', default='https://kenney.nl（經 soundcn 收錄）')
    ap.add_argument('--limit', type=int, default=0); a = ap.parse_args()
    files = sorted(f for f in glob.glob(os.path.join(a.dir, '**', '*'), recursive=True)
                   if f.lower().endswith(('.ogg', '.wav', '.mp3')) and 'preview' not in os.path.basename(f).lower())
    have = done_sources(); nid = next_id(); n = 0; today = datetime.date.today().isoformat()
    for f in files:
        rel = f'{a.pack}/{os.path.relpath(f, a.dir)}'
        if rel in have: continue
        stem = os.path.splitext(os.path.basename(f))[0]
        key = re.sub(r'[_-]*\d+$', '', stem); num = (re.search(r'(\d+)$', stem) or [None, '1'])[1]
        name, cat, vol = KEYMAP.get(key, (key, 'accent', .3))
        slug = re.sub(r'[^a-z0-9]+', '-', f'{a.pack}-{key}-{num}'.lower()).strip('-')
        sid = f'SFX-{nid:03d}'; d = os.path.join(SND, f'{sid}-{slug}'); os.makedirs(d, exist_ok=True)
        y = decode(f); pk = np.max(np.abs(y)) or 1; y = y / pk * 10 ** (-1 / 20)
        with tempfile.TemporaryDirectory() as td:
            wv = os.path.join(td, 'a.wav'); write_wav(wv, y)
            ff('-i', wv, '-c:a', 'libmp3lame', '-b:a', '160k', os.path.join(d, 'sound.mp3'))
            ff('-i', wv, '-ac', '1', '-ar', '32000', '-c:a', 'libmp3lame', '-b:a', '40k', os.path.join(d, 'preview.mp3'))
        m = np.abs(y).max(1); ch = np.array_split(m, 64); p = [float(c.max()) if len(c) else 0 for c in ch]; mx = max(p) or 1
        dur = len(y) / SR
        json.dump({'duration': round(dur, 3), 'peaks': [round(v / mx, 3) for v in p]}, open(os.path.join(d, 'peaks.json'), 'w'))
        full = f'{name} {int(num):02d}'
        open(os.path.join(d, 'sound.md'), 'w', encoding='utf-8').write(f'''---
id: {sid}
name: {full}
name_en: {stem}
category: {cat}
duration: {dur:.2f}
volume: {vol}
mood: {lst(CAT_MOOD.get(cat, []))}
video_types: {lst(VT_ALL)}
pace: {lst(CAT_PACE.get(cat, ['快', '中']))}
pairs_with: []
pack: {a.pack}
curated: false
source: "{a.source}"
source_file: "{rel}"
license: "{a.license}"
learned: {today}
used_in: []
status: active
---

## 聲效
{full}（{stem}），{dur:.2f} 秒，由 {a.pack} 聲效包匯入。

## 幾時用
- {CAT_WHEN.get(cat, '按需要')}

## 幾時唔好用
- 同一個聲效唔好短時間重複；講者講重點字嗰刻唔好落大聲。

## 用法
- 建議音量 `volume: {vol}`；混音用 `python3 tools/sfx.py mix`（見 `lessons/sound-mixing.md`）。
''')
        nid += 1; n += 1
        if a.limit and n >= a.limit: break
    print(f'✓ {a.pack}: 新增 {n} 個（共 {len(files)} 個檔）')

if __name__ == '__main__': main()
