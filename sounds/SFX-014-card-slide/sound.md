---
id: SFX-014
name: 卡片滑入
name_en: Card slide
category: foley
duration: 0.45
volume: 0.4
mood: [專業醫療, 溫暖生活]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-005, FX-032, FX-021, FX-041, FX-078, FX-079]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
卡片滑入（Card slide），0.45 秒，擬音類。

## 幾時用
- 卡片、紙張、相片滑入畫面。

## 幾時唔好用
- 快節奏片改用快速嗖聲。

## 用法
- 建議音量 `volume: 0.4`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
