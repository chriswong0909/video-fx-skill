---
id: SFX-006
name: UI 點擊
name_en: UI click
category: ui
duration: 0.06
volume: 0.45
mood: [專業醫療, 高級編輯感]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中, 慢]
pairs_with: [FX-029, FX-035, FX-031, FX-080]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
UI 點擊（UI click），0.06 秒，介面類。

## 幾時用
- UI 元件、按鈕、剔選、畫面點擊示範。

## 幾時唔好用
- 唔好用嚟配文字出現（太細聲會似雜音）。

## 用法
- 建議音量 `volume: 0.45`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
