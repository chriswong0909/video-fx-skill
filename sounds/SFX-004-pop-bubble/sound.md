---
id: SFX-004
name: 彈字泡泡聲
name_en: Bubble pop
category: pop
duration: 0.16
volume: 0.4
mood: [活潑年輕, 溫暖生活]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中]
pairs_with: [FX-044, FX-057, FX-037, FX-055, FX-033]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
彈字泡泡聲（Bubble pop），0.16 秒，彈出類。

## 幾時用
- 膠囊字、徽章、圖示、通知逐個彈出；每個元素出現嗰格落聲。

## 幾時唔好用
- 連續彈 5 個以上要降音量或隔一個先落。

## 用法
- 建議音量 `volume: 0.4`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
